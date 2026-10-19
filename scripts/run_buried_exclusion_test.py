"""Run the SYN-002 / SYN-003 / SYN-004 / SYN-005 buried-exclusion tests end to end and score them against labels.

    python scripts/run_buried_exclusion_test.py --dry-run          # ingest only, no API calls
    python scripts/run_buried_exclusion_test.py                    # SYN-002 and SYN-002-control
    python scripts/run_buried_exclusion_test.py --variants SYN-002 # one variant
    python scripts/run_buried_exclusion_test.py --reuse-evidence   # re-score saved extraction

Unlike run_criterion_eval.py (which replays the saved SYN-001 run), this runs the
live pipeline on new documents: ingest -> extract evidence (LLM) -> verify quotes ->
assess each labeled criterion (rule baseline and LLM assessor) -> safety review.

It reports two layers separately, so a miss can be traced to where it happened:
  1. extraction: did a verified evidence record capture each buried fact?
  2. assessment: did the criterion come out as labeled?

Outputs (per variant) in data/eval/:
  <variant>_buried_test_evidence.json     extracted evidence, reusable with --reuse-evidence
  <variant>_buried_test_report.json / .md scores, per-criterion results, explanations
Labels must be reviewed BEFORE the first live run; do not edit them after seeing results.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

from src.criteria import load_criteria  # noqa: E402
from src.document_ingestion import ingest_documents  # noqa: E402
from src.eligibility import assess_free_text_criterion, conservative_assessment  # noqa: E402
from src.evidence_extraction import extract_evidence, uncovered_content_lines  # noqa: E402
from src.safety import review_assessments  # noqa: E402
from src.schemas import EvidenceItem  # noqa: E402
from run_criterion_eval import score  # noqa: E402

PATIENTS = ROOT / "data" / "patients"
EVAL = ROOT / "data" / "eval"
LABEL_FILES = {
    "SYN-002": EVAL / "criterion_labels_syn002.json",
    "SYN-002-control": EVAL / "criterion_labels_syn002_control.json",
    "SYN-003": EVAL / "criterion_labels_syn003.json",
    "SYN-003-control": EVAL / "criterion_labels_syn003_control.json",
    "SYN-004": EVAL / "criterion_labels_syn004.json",
    "SYN-004-control": EVAL / "criterion_labels_syn004_control.json",
    "SYN-005": EVAL / "criterion_labels_syn005.json",
    "SYN-005-control": EVAL / "criterion_labels_syn005_control.json",
}
# Words that identify each probe's source fact in the extracted evidence.
PROBE_TERMS = {
    "buried_malignancy": ("prostate",),
    "buried_kras_inhibitor": ("sotorasib",),
    "family_history_decoy": ("breast cancer",),
    "last_chemo_dose": ("2026-03-20",),
}
# SYN-003 has its own buried facts and traps; SYN-002 keeps the original probes unchanged.
PROBE_TERMS_SYN003 = {
    "buried_malignancy": ("hodgkin",),
    "buried_pd1": ("pembrolizumab",),
    "excepted_cancer_trap": ("basal-cell", "basal cell"),
    "last_chemo_dose": ("2026-04-08",),
    "scheduled_first_dose": ("2026-04-20",),
}
# SYN-004 (blind test of the frozen round-2 code). Buried facts and the traps that replace
# them in the control, so each report shows whether a miss came from OCR/extraction or later.
PROBE_TERMS_SYN004 = {
    "buried_pneumonitis_ocr": ("pneumonitis",),
    "pneumonia_trap": ("pneumonia",),
    "buried_steroid": ("prednisone",),
    "steroid_last_dose": ("2026-06-18",),
    "inhaled_topical_steroid_trap": ("fluticasone", "hydrocortisone"),
    "buried_tia": ("transient ischemic",),
    "vertigo_trap": ("vertigo",),
    "autoimmune_exception_trap": ("hashimoto",),
    "brain_mri": ("intracranial",),
    "scheduled_first_dose": ("2026-06-22",),
}


# SYN-005 (blind test of the frozen round-3 code): buried facts, look-alikes, and the facts
# needed to decide criteria rather than leave them UNKNOWN.
PROBE_TERMS_SYN005 = {
    "qtcf_value": ("478 ms", "441 ms"),
    "buried_major_surgery": ("laparotomy",),
    "biopsy_trap": ("core-needle", "core needle"),
    "surgery_or_biopsy_date": ("2026-07-22",),
    "neuropathy_grade": ("neuropathy",),
    "alopecia_exception": ("alopecia",),
    "serology": ("hiv", "hbsag", "hepatitis"),
    "creatinine": ("creatinine",),
    "weight": ("52 kg",),
    "scheduled_first_dose": ("2026-08-10",),
}


def probe_terms_for(variant: str) -> dict:
    if variant.startswith("SYN-005"):
        return PROBE_TERMS_SYN005
    if variant.startswith("SYN-004"):
        return PROBE_TERMS_SYN004
    if variant.startswith("SYN-003"):
        return PROBE_TERMS_SYN003
    return PROBE_TERMS


def extraction_check(evidence: list[EvidenceItem], probe_terms: dict | None = None) -> dict:
    found = {}
    for probe, terms in (probe_terms or PROBE_TERMS).items():
        hits = [e for e in evidence if any(t in f"{e.value} {e.evidence_text}".casefold() for t in terms)]
        found[probe] = [
            {"category": e.category, "value": e.value, "source": f"{e.source_file} p{e.source_page}",
             "date": e.date, "quote_verified": e.quote_verified}
            for e in hits
        ]
    return found


def run_variant(variant: str, args, criteria, client) -> dict:
    folder = PATIENTS / variant
    files = sorted(folder.glob("*.pdf"))
    if not files:
        raise SystemExit(f"No documents in {folder}. Run scripts/create_syn002_patient.py first.")
    # SYN-004 includes a scanned page; read it with OCR as the app does. Earlier patients
    # have text layers only, so their ingestion is unchanged.
    use_ocr = variant.startswith("SYN-004") and not args.dry_run
    pages = ingest_documents(files, use_ocr=use_ocr, ocr_client=client if use_ocr else None)
    print(f"\n== {variant}: {len(files)} documents, {len(pages)} pages")
    if args.dry_run:
        for p in pages:
            print(f"   {p.filename} p{p.page_number} [{p.extraction_method}] {len(p.text)} chars")
        return {}
    if use_ocr:
        pages_path = args.output_dir / f"{variant}_buried_test_pages.json"
        pages_path.write_text(json.dumps([{"file": p.filename, "page": p.page_number, "method": p.extraction_method,
                                           "text": p.text} for p in pages], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(f"   wrote {pages_path.name} (OCR text kept for review)")

    evidence_path = args.output_dir / f"{variant}_buried_test_evidence.json"
    if args.reuse_evidence and evidence_path.exists():
        evidence = [EvidenceItem.model_validate(e) for e in json.loads(evidence_path.read_text(encoding="utf-8"))]
        print(f"   reusing {evidence_path.name} ({len(evidence)} records)")
    else:
        evidence = extract_evidence(pages, client=client, model=args.extraction_model)
        evidence_path.write_text(json.dumps([e.model_dump(mode="json") for e in evidence], indent=2) + "\n", encoding="utf-8")
        print(f"   extracted {len(evidence)} records ({sum(e.quote_verified for e in evidence)} verified)")

    extraction = extraction_check(evidence, probe_terms_for(variant))
    gaps = uncovered_content_lines(pages, evidence)
    for probe, hits in extraction.items():
        shown = "; ".join(f"{h['category']}: {h['value']} ({h['source']}, verified={h['quote_verified']})" for h in hits) or "NOT EXTRACTED"
        print(f"   extraction · {probe}: {shown}")

    labels = json.loads(LABEL_FILES[variant].read_text(encoding="utf-8"))
    methods = {"rule_baseline": lambda c: conservative_assessment(c, evidence)}
    if not args.rules_only:
        methods["llm_assessor"] = lambda c: assess_free_text_criterion(c, evidence, pages, client=client, model=args.model)

    rows, results = [], {}
    for name, assess in methods.items():
        pairs, acceptable_pairs = [], []
        for label in labels["labels"]:
            criterion = next(c for c in criteria[label["trial"]] if c.criterion_id == label["criterion_id"])
            reviewed, flags = review_assessments([assess(criterion)])
            predicted = reviewed[0].status
            ok = predicted == label["expected"] or predicted in label.get("also_acceptable", [])
            pairs.append((label["expected"], predicted))
            acceptable_pairs.append(ok)
            rows.append({"method": name, "trial": label["trial"], "criterion_id": label["criterion_id"],
                         "probe": label.get("probe"), "expected": label["expected"],
                         "also_acceptable": label.get("also_acceptable", []), "predicted": predicted,
                         "match": predicted == label["expected"], "acceptable": ok,
                         "judgment_call": label["judgment_call"], "flags": flags,
                         "explanation": reviewed[0].explanation,
                         "criterion_text": criterion.text,
                         "patient_evidence": [e.model_dump(mode="json") for e in reviewed[0].patient_evidence],
                         "assessment_details": reviewed[0].model_dump(mode="json")})
            print(f"   {name:13} {label['trial']} {label['criterion_id']:6} expected {label['expected']:13} got {predicted:18} {'ok' if ok else 'MISS'}")
        results[name] = score(pairs) | {"acceptable_rate": round(sum(acceptable_pairs) / len(acceptable_pairs), 4)}

    report = {"patient": variant, "variant": labels["variant"], "label_status": labels["label_status"],
              "extraction_model": args.extraction_model, "assessment_model": args.model,
              "extraction_check": extraction, "extraction_gaps": gaps, "results": results, "rows": rows}
    stem = args.output_dir / f"{variant}_buried_test_report"
    stem.with_suffix(".json").write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    lines = [f"# Buried-exclusion test: {variant} ({labels['variant']})", "",
             f"Labels: {labels['label_status']}. Models: extraction {args.extraction_model}, assessment {args.model}.", "",
             "## Extraction: were the buried facts captured?", ""]
    for probe, hits in extraction.items():
        lines.append(f"- **{probe}**: " + ("; ".join(f"{h['category']} '{h['value']}' ({h['source']}, verified={h['quote_verified']})" for h in hits) or "not extracted"))
    lines += ["", "## Not captured by the tool, review manually", ""]
    lines += [f"- {g['source_file']} p{g['source_page']}, line {g['line_number']}: {g['text']}" for g in gaps] or ["No uncovered content lines."]
    lines += ["", "## Assessment", "", "| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |", "|---|---|---|---|---|---|"]
    for name, r in results.items():
        lines.append(f"| {name} | {r['accuracy']:.2f} | {r['acceptable_rate']:.2f} | {r['unsafe_false_clearance']} | {r['unknown_to_meets']} | {r['false_exclusion']} |")
    lines += ["", "| Method | Trial | Criterion | Probe | Expected | Got | Result |", "|---|---|---|---|---|---|---|"]
    for row in rows:
        result = "ok" if row["match"] else ("acceptable" if row["acceptable"] else "**MISS**")
        lines.append(f"| {row['method']} | {row['trial']} | {row['criterion_id']} | {row['probe']} | {row['expected']} | {row['predicted']} | {result} |")
    lines += ["", "## Explanations for misses", ""]
    for row in rows:
        if not row["acceptable"]:
            lines.append(f"- {row['method']} · {row['trial']} {row['criterion_id']}: {row['explanation']}")
    stem.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"   wrote {stem.name}.md / .json")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--variants", nargs="*", default=list(LABEL_FILES), choices=list(LABEL_FILES))
    parser.add_argument("--model", default="gpt-4.1-mini", help="assessment model")
    parser.add_argument("--extraction-model", default="gpt-4.1-mini")
    parser.add_argument("--dry-run", action="store_true", help="ingest and list pages; no API calls")
    parser.add_argument("--reuse-evidence", action="store_true", help="re-score saved evidence instead of re-extracting")
    parser.add_argument("--rules-only", action="store_true", help="skip the LLM assessor (extraction still uses the API)")
    parser.add_argument("--output-dir", type=Path, default=EVAL, help="report/evidence destination; labels are always loaded from data/eval")
    args = parser.parse_args()

    criteria = load_criteria()
    client = None
    if not args.dry_run:
        args.output_dir.mkdir(parents=True, exist_ok=True)
        from run_live_assessment import _client  # noqa: E402
        client = _client()
    for variant in args.variants:
        run_variant(variant, args, criteria, client)


if __name__ == "__main__":
    main()
