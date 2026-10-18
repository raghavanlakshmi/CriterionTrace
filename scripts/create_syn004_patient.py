"""Generate SYN-004: a blind test patient for the frozen round-2 code, plus a matched control.

Built after the round-2 code was frozen (round2-frozen, caa440b), without reading the round-2
code or its run outputs. Labels are signed and committed before any run. It deliberately
uses exclusion types and document types that no earlier patient used:

  - a lung-history exclusion (interstitial pneumonitis), stated only in a SCANNED pulmonology
    consult, so the fact is only reachable through OCR
  - a time window on a non-cancer drug (systemic steroid within 7 days of first dose), with
    the steroid course stated only in an emergency department discharge summary
  - a cardiovascular-event window (TIA within 6 months), stated only in a neurology note
  - a medication reconciliation laid out as a table, and a radiology report

Folders (identical except for three buried facts):

  data/patients/SYN-004/          drug-induced interstitial pneumonitis in 2025 (scanned
                                  consult); prednisone 2026-06-14 to 2026-06-18 for gout (ED);
                                  transient ischemic attack on 2026-02-09 (neurology)
  data/patients/SYN-004-control/  community-acquired pneumonia in 2025 (scanned consult);
                                  colchicine for gout, no steroid (ED); benign positional
                                  vertigo, no TIA (neurology)

Traps in both variants: Hashimoto thyroiditis on levothyroxine (replacement therapy is an
exception in the autoimmune criterion), inhaled and topical steroids on the medication table
(not systemic), bibasilar atelectasis on CT (not fibrosis), and a brain MRI with no metastases.
Cycle 1 day 1 is scheduled for 2026-06-22.

    python scripts/create_syn004_patient.py [--overwrite]
"""

import argparse
import io
import logging
import random
import textwrap
from pathlib import Path

import pymupdf
from PIL import Image, ImageDraw, ImageFilter, ImageFont


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1] / "data" / "patients"
DISCLAIMER = "SYNTHETIC PATIENT - FICTIONAL DATA - FOR DEMONSTRATION ONLY"
PATIENT_ID = "SYN-004"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def documents(control: bool) -> dict:
    if control:
        pulmonology = (
            "Ms. Roe is seen in follow-up for a respiratory illness. In March 2025 she developed "
            "cough and fever while receiving chemotherapy for colorectal cancer. Chest X-ray showed "
            "right lower lobe consolidation, and she was diagnosed with community-acquired pneumonia. "
            "She completed a 7-day course of oral amoxicillin-clavulanate. Repeat chest X-ray on "
            "2025-04-15 showed resolution of the consolidation. She is now asymptomatic. "
            "Plan: no further pulmonary follow-up is needed."
        )
        neurology = [
            "Ms. Roe presented to the emergency department on 2026-02-09 with sudden spinning "
            "dizziness on turning her head in bed, lasting under a minute per episode. Neurological "
            "examination was normal. The Dix-Hallpike test was positive on the right.",
            "MRI brain on 2026-02-10: no acute infarct, no hemorrhage, no intracranial metastases.",
            "Assessment: benign paroxysmal positional vertigo. Treated with a canalith repositioning "
            "maneuver; symptoms resolved. Plan: vestibular exercises; return if symptoms recur.",
        ]
        ed_treatment = (
            "Treatment: colchicine 0.6 mg by mouth twice daily for 5 days (2026-06-14 through "
            "2026-06-18), with ice and rest. Pain improved before discharge."
        )
    else:
        pulmonology = (
            "Ms. Roe is seen in follow-up for a respiratory illness. In March 2025 she developed dry "
            "cough and exertional dyspnea while receiving FOLFOX for colorectal cancer. CT chest showed "
            "bilateral ground-glass and reticular opacities. Infection was excluded, and she was "
            "diagnosed with drug-induced interstitial pneumonitis, felt to be oxaliplatin-related. "
            "Oxaliplatin was permanently discontinued and she completed a prednisone taper in April "
            "2025. She is now asymptomatic. Plan: avoid oxaliplatin; repeat pulmonary function "
            "tests in one year."
        )
        neurology = [
            "Ms. Roe presented to the emergency department on 2026-02-09 with sudden weakness of the "
            "left arm and slurred speech, which resolved completely within 30 minutes. Neurological "
            "examination at this visit is normal.",
            "MRI brain on 2026-02-10: no acute infarct, no hemorrhage, no intracranial metastases.",
            "Assessment: transient ischemic attack on 2026-02-09. Started aspirin 81 mg daily and "
            "atorvastatin. Plan: carotid ultrasound; return immediately for new symptoms.",
        ]
        ed_treatment = (
            "Treatment: prednisone 40 mg by mouth once daily for 5 days (2026-06-14 through "
            "2026-06-18), with ice and rest. Pain improved before discharge."
        )

    return {
        "oncology_note.pdf": {
            "title": "Oncology note", "date": "2026-06-05",
            "pages": [("Clinic visit", [
                "Age: 58 years",
                "Sex: Female",
                "Diagnosis: Metastatic colorectal adenocarcinoma, liver metastases",
                "Prior treatment: FOLFOX, then FOLFIRI with bevacizumab; last dose 2026-05-12, "
                "stopped for disease progression",
                "Past medical history: Hashimoto thyroiditis on levothyroxine replacement; gout",
                "Performance status: ECOG 1",
                "Plan: referred for clinical trial screening.",
            ])],
        },
        "pathology_report.pdf": {
            "title": "Pathology report", "date": "2024-03-11",
            "pages": [("Molecular findings", [
                "Specimen: colon biopsy, invasive adenocarcinoma",
                "KRAS: G12C mutation detected",
                "MSI: microsatellite stable (MSS)",
                "BRAF: wild type",
            ])],
        },
        "lab_report.pdf": {
            "title": "Laboratory report", "date": "2026-06-03",
            "pages": [("Reported laboratory values", [
                "Absolute neutrophil count (ANC): 3.4 x 10^9/L",
                "Hemoglobin: 11.6 g/dL",
                "Platelets: 238 x 10^9/L",
                "Creatinine: 0.9 mg/dL",
                "Total bilirubin: 0.7 mg/dL",
                "AST: 31 U/L",
                "ALT: 27 U/L",
                "TSH: 2.1 mIU/L",
            ])],
        },
        "ct_chest_abdomen_pelvis.pdf": {
            "title": "Radiology report", "date": "2026-06-01",
            "pages": [("CT chest, abdomen and pelvis with contrast", [
                "Comparison: CT dated 2026-02-27.",
                "Liver: multiple hypodense lesions; the largest, in segment VII, measures 3.4 cm "
                "(previously 2.6 cm).",
                "Lungs: mild bibasilar dependent atelectasis. No pulmonary nodules. No pleural effusion.",
                "Impression: progression of hepatic metastases, measurable by RECIST 1.1.",
            ])],
        },
        "medication_reconciliation.pdf": {
            "title": "Medication reconciliation", "date": "2026-06-05",
            "table": [
                ("Medication", "Dose and route", "Indication", "Status"),
                ("Levothyroxine", "88 mcg by mouth daily", "Hypothyroidism", "Active"),
                ("Allopurinol", "100 mg by mouth daily", "Gout", "Active"),
                ("Fluticasone nasal spray", "50 mcg, 2 sprays each nostril daily", "Allergic rhinitis", "Active"),
                ("Hydrocortisone 1% cream", "Topical, as needed", "Eczema", "Active"),
                ("Aspirin", "81 mg by mouth daily", "Cardiovascular prevention", "Active"),
                ("Atorvastatin", "40 mg by mouth daily", "Hyperlipidemia", "Active"),
                ("Ondansetron", "8 mg by mouth as needed", "Nausea", "Active"),
                ("Loperamide", "2 mg by mouth as needed", "Diarrhea", "Active"),
            ],
        },
        "neurology_note_2026.pdf": {
            "title": "Neurology clinic note", "date": "2026-02-20", "fontsize": 11,
            "pages": [("Follow-up after emergency visit", neurology)],
        },
        "pulmonology_consult_2025_scanned.pdf": {
            "title": "Pulmonology consultation", "date": "2025-05-06", "scanned": True,
            "pages": [("Consultation summary", [pulmonology])],
        },
        "ed_discharge_summary.pdf": {
            "title": "Emergency department discharge summary", "date": "2026-06-14", "fontsize": 11,
            "pages": [("Discharge summary", [
                "Reason for visit: acute pain and swelling of the right big toe.",
                "Diagnosis: acute gout flare, right first metatarsophalangeal joint.",
                ed_treatment,
                "Follow-up: primary care in one week.",
            ])],
        },
        "trial_screening_letter.pdf": {
            "title": "Trial screening letter", "date": "2026-06-16",
            "pages": [("Screening plan", [
                "The patient has been referred for clinical trial screening.",
                "If eligibility is confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-06-22.",
                "Final eligibility will be confirmed by the study team.",
            ])],
        },
    }


def _header(page, document: dict, page_number: int, page_count: int) -> None:
    page.insert_text((48, 42), DISCLAIMER, fontsize=9, color=(0.45, 0.15, 0.1))
    page.insert_text((48, 88), document["title"], fontsize=23, fontname="hebo")
    page.insert_text((48, 120), f"Patient ID: {PATIENT_ID}", fontsize=11)
    page.insert_text((48, 142), f"Document date: {document['date']}", fontsize=11)
    page.draw_line((48, 160), (564, 160), color=(0.7, 0.7, 0.7))
    page.insert_text((48, 738), "Fictional document. No real patient information.", fontsize=9)
    page.insert_text((48, 756), f"Page {page_number} of {page_count}", fontsize=9)


def _write_text_pages(pdf, path: Path, document: dict) -> None:
    fontsize = document.get("fontsize", 12)
    for page_number, (section, facts) in enumerate(document["pages"], start=1):
        page = pdf.new_page(width=612, height=792)
        _header(page, document, page_number, len(document["pages"]))
        page.insert_text((48, 192), section, fontsize=14, fontname="hebo")
        remaining = page.insert_textbox(
            pymupdf.Rect(48, 218, 564, 710), "\n\n".join(facts), fontsize=fontsize, lineheight=1.4
        )
        if remaining < 0:
            raise ValueError(f"Content overflows {path.name}, page {page_number}")


def _write_table_page(pdf, document: dict) -> None:
    page = pdf.new_page(width=612, height=792)
    _header(page, document, 1, 1)
    page.insert_text((48, 192), "Current medication list", fontsize=14, fontname="hebo")
    widths = (130, 170, 120, 96)
    top, row_height = 210, 34
    for r, row in enumerate(document["table"]):
        x = 48
        y = top + r * row_height
        for width, cell in zip(widths, row):
            page.draw_rect(pymupdf.Rect(x, y, x + width, y + row_height), color=(0.6, 0.6, 0.6), width=0.6)
            page.insert_textbox(
                pymupdf.Rect(x + 4, y + 4, x + width - 4, y + row_height - 2), cell,
                fontsize=9.5, fontname="hebo" if r == 0 else "helv",
            )
            x += width
    page.insert_text((48, top + len(document["table"]) * row_height + 24),
                     "Reconciled with the patient at the oncology visit.", fontsize=10)


def _scanned_image(document: dict) -> bytes:
    """Render the page as a slightly skewed, noisy grayscale image with no text layer."""
    scale = 2.5
    width, height = int(612 * scale), int(792 * scale)
    image = Image.new("L", (width, height), 250)
    draw = ImageDraw.Draw(image)
    small, body, title = (ImageFont.truetype(FONT, int(s * scale)) for s in (9, 11.5, 21))
    bold = ImageFont.truetype(FONT_BOLD, int(14 * scale))
    x = int(48 * scale)
    draw.text((x, int(30 * scale)), DISCLAIMER, font=small, fill=60)
    draw.text((x, int(66 * scale)), document["title"], font=title, fill=20)
    draw.text((x, int(108 * scale)), f"Patient ID: {PATIENT_ID}", font=body, fill=30)
    draw.text((x, int(130 * scale)), f"Document date: {document['date']}", font=body, fill=30)
    draw.line((x, int(160 * scale), int(564 * scale), int(160 * scale)), fill=120, width=2)
    section, facts = document["pages"][0]
    draw.text((x, int(180 * scale)), section, font=bold, fill=20)
    y = int(214 * scale)
    for paragraph in facts:
        for line in textwrap.wrap(paragraph, width=84):
            draw.text((x, y), line, font=body, fill=25)
            y += int(17 * scale)
        y += int(10 * scale)
    draw.text((x, int(730 * scale)), "Fictional document. No real patient information.", font=small, fill=60)
    draw.text((x, int(748 * scale)), "Page 1 of 1   (faxed copy)", font=small, fill=60)
    rng = random.Random(4)
    for _ in range(2500):  # fax speckle
        draw.point((rng.randrange(width), rng.randrange(height)), fill=rng.choice((90, 140)))
    image = image.rotate(0.8, resample=Image.BICUBIC, fillcolor=250).filter(ImageFilter.GaussianBlur(0.6))
    buffer = io.BytesIO()
    image.save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()


def write_pdf(path: Path, document: dict) -> None:
    with pymupdf.open() as pdf:
        pdf.set_metadata({"title": document["title"], "subject": DISCLAIMER, "author": "CriterionTrace"})
        if document.get("scanned"):
            page = pdf.new_page(width=612, height=792)
            page.insert_image(page.rect, stream=_scanned_image(document))
        elif "table" in document:
            _write_table_page(pdf, document)
        else:
            _write_text_pages(pdf, path, document)
        pdf.save(path, deflate=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overwrite", action="store_true", help="replace existing SYN-004 documents")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for folder, control in (("SYN-004", False), ("SYN-004-control", True)):
        out = ROOT / folder
        out.mkdir(parents=True, exist_ok=True)
        for name, document in documents(control).items():
            path = out / name
            if path.exists() and not args.overwrite:
                raise FileExistsError(f"{folder}/{name} exists. Use --overwrite to regenerate.")
            write_pdf(path, document)
        LOGGER.info("Created %s (%d documents)", folder, len(documents(control)))


if __name__ == "__main__":
    main()
