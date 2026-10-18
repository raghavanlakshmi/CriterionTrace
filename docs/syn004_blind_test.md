# SYN-004: blind test of the frozen round-2 code

SYN-002 and SYN-003 were used to design and tune the round-1 and round-2 fixes, so their
after-fix scores are development results. SYN-004 is the blind check. It was written after
the code was frozen (`round2-frozen`, `caa440b`), without reading the round-2 code or its run
outputs. Its labels are signed and committed before the first run, and the code is not
changed in response to its results before all three runs are recorded.

## What is new

| | SYN-002 / SYN-003 | SYN-004 |
|---|---|---|
| Exclusion types | prior cancer, prior drug, chemo washout | lung history (interstitial pneumonitis), systemic steroid within 7 days, cardiovascular event (TIA) within 6 months |
| Where the fact is hidden | old notes, medication list, narrative paragraph | **scanned fax with no text layer (OCR only)**, emergency department discharge summary, neurology note |
| Document types | notes, labs, pathology, infusion record, letter | adds a radiology report and a medication table |
| Time windows | anti-cancer therapy | a non-cancer drug (prednisone) and a clinical event |

## The two variants

Identical except for three facts.

| Document | SYN-004 (buried) | SYN-004-control |
|---|---|---|
| Pulmonology consult, 2025-05-06, **scanned** | drug-induced interstitial pneumonitis (oxaliplatin), prednisone taper April 2025 | community-acquired pneumonia, antibiotics, resolved |
| ED discharge summary, 2026-06-14 | gout flare; **prednisone 40 mg daily 2026-06-14 to 2026-06-18** | gout flare; colchicine |
| Neurology note, 2026-02-20 | **transient ischemic attack on 2026-02-09** | benign positional vertigo |
| Both | MRI brain 2026-02-10: no intracranial metastases | same |

Shared documents: oncology note (2026-06-05; Hashimoto thyroiditis on levothyroxine; ECOG 1),
pathology (KRAS G12C, MSS), labs, CT chest/abdomen/pelvis (liver metastases; bibasilar
atelectasis), medication table (levothyroxine, fluticasone nasal spray, hydrocortisone cream,
aspirin, atorvastatin, others), and a screening letter: **cycle 1 day 1 scheduled for 2026-06-22**.

Traps: pneumonia is not pneumonitis; atelectasis is not fibrosis; nasal and topical steroids
are not systemic; vertigo is not a cardiovascular event; thyroid replacement is an explicit
exception in the autoimmune criterion.

## Labels (written before any run)

`data/eval/criterion_labels_syn004.json` and `criterion_labels_syn004_control.json`.
For exclusions, MEETS means the patient appears clear.

| Trial | Criterion | Probe | SYN-004 | Control |
|---|---|---|---|---|
| NCT06252649 | EXC-04 interstitial pneumonitis history | buried, OCR only | DOES_NOT_MEET | UNKNOWN |
| NCT06412198 | EXC-03 systemic steroid within 7 days | prednisone ended 4 days before C1D1 | DOES_NOT_MEET (UNKNOWN acceptable) | UNKNOWN |
| NCT07559760 | EXC-08 TIA within 6 months | TIA 133 days before C1D1 | DOES_NOT_MEET | UNKNOWN |
| NCT06412198 | EXC-04 autoimmune disease needing systemic treatment | replacement-therapy exception | UNKNOWN | UNKNOWN |
| NCT06252649 | EXC-01 active untreated brain metastases | explicit negative MRI | MEETS (UNKNOWN acceptable) | same |
| NCT06252649 | INC-01 metastatic CRC with KRAS G12C | sanity | MEETS | MEETS |
| NCT06412198 | INC-11 ECOG 0–1 | sanity | MEETS | MEETS |

Seven criteria per variant, 14 per run, 42 over three runs. Any MEETS on a row not labeled
MEETS is an unsafe clearance. Any DOES_NOT_MEET in the control is a false exclusion.

## Run it

On a branch from the frozen commit, so `src/` is exactly `caa440b`:

```
git checkout -b syn004-blind round2-frozen
# copy in the SYN-004 files, review and sign the two label files, then:
git add scripts/create_syn004_patient.py scripts/run_buried_exclusion_test.py \
        data/patients/SYN-004 data/patients/SYN-004-control \
        data/eval/criterion_labels_syn004.json data/eval/criterion_labels_syn004_control.json \
        docs/syn004_blind_test.md
git commit -m "Add SYN-004 blind test with signed-off labels before runs"
git push -u origin syn004-blind

git diff --stat caa440b -- src          # must print nothing
python scripts/run_buried_exclusion_test.py --dry-run --variants SYN-004 SYN-004-control

for r in 1 2 3; do
  python scripts/run_buried_exclusion_test.py --variants SYN-004 SYN-004-control \
         --output-dir data/eval/syn004_runs/run$r
done
```

The dry run shows the scanned consult as `OCR_REQUIRED` with 0 characters; that is expected.
Live runs read it with the vision model (`use_ocr=True`, as the app does) and save the OCR text
to `SYN-004*_buried_test_pages.json`. The runner change only adds SYN-004 labels, probes, and
OCR for SYN-004; SYN-002 and SYN-003 ingestion is unchanged. Roughly 100 gpt-4.1-mini calls
in total.

## Reading the results

For each miss, find the layer where it happened:

1. **OCR**: does the pages file contain "interstitial pneumonitis"?
2. **Extraction**: do the report's extraction probes show a verified record for each buried
   fact and trap, with dates (2026-06-18, 2026-06-22, 2026-02-09)?
3. **Assessment and guards**: was the fact cited, and which guard flags fired?

Report results as they come out, including anything worse than SYN-002/SYN-003. If a fix
follows, SYN-004 is no longer blind and the after-fix result is reported separately.

## Results (blind, three runs on frozen code `caa440b`)

Labels were signed and committed (`b09f44e`) before the dry run and before any live run. `src/` was
unchanged. Nothing was changed in response to these results before all three runs were recorded.

| Run | Variant | Exact | Acceptable | Unsafe clearances | False exclusions |
|---|---|---|---|---|---|
| 1 | SYN-004 | 3/7 | 5/7 | 1 | 0 |
| 1 | Control | 5/7 | 6/7 | 1 | 0 |
| 2 | SYN-004 | 3/7 | 5/7 | 1 | 0 |
| 2 | Control | 5/7 | 6/7 | 1 | 0 |
| 3 | SYN-004 | 3/7 | 5/7 | 0 | 1 |
| 3 | Control | 5/7 | 6/7 | 1 | 0 |

Total: 24/42 exact, 33/42 acceptable, 5 unsafe clearances, 1 false exclusion. These are three
repetitions of 14 labeled pairs, not 42 independent cases.

- **Scanned fax (OCR):** read correctly in all runs. The pneumonitis was extracted and flagged as an
  exclusion 3/3. Control pneumonia never caused an exclusion.
- **Decoys:** pneumonia, nasal and topical steroids, and vertigo never triggered an exclusion.
- **Autoimmune exclusion (all 5 unsafe clearances):** the model reasoned "Hashimoto's is on
  replacement therapy, which is allowed, and nothing else is documented, so the patient is clear."
  No guard fired. One run also contained a date error ("April 2025 is more than 2 years before
  2026-06-22"). The one false exclusion called drug-induced pneumonitis "likely autoimmune-related,"
  which the record does not state.
- **TIA (UNKNOWN in 3/3, a safe miss):** in run 1 the TIA was extracted and the model answered
  correctly, but an older study-reference guard overrode it although the planned first-dose record was
  cited. In runs 2 and 3 the TIA was not extracted; the model concluded no event was documented, and a
  guard converted that to UNKNOWN.
- **Steroid window (UNKNOWN in 3/3, acceptable but not reasoned):** the prednisone course was stored
  with its start date (2026-06-14), not its last dose (2026-06-18), and the code-computed window did not
  treat it as a dated administration. The immunodeficiency part of the same criterion was never assessed.
- **Brain MRI (UNKNOWN in 6/6, acceptable):** guards blocked a clearance the record supports.
- **Sanity criteria:** correct in every run.

The finding: zero unsafe clearances on the development patients (SYN-002, SYN-003) did not generalize.
The guards blocked the failure patterns they were written for, in the wordings they were written for.
Any fix designed from these results makes SYN-004 a development test; its after-fix results will be
reported separately.

Reports, evidence, OCR text and logs are in `data/eval/syn004_runs/run1..3`, with the full layer audit
in `layer_audit.json`.

Synthetic data only. Not clinical validation.
