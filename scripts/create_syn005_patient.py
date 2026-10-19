"""Generate SYN-005: a blind test patient for the frozen round-3 code, plus a matched control.

Built after the round-3 code was frozen (round3-frozen, 6da940d), without reading the round-3
code or its run outputs. Labels are signed and committed before any run.

Round 3 made the tool safer but more cautious, so SYN-005 measures both sides:
  - exclusions that should be caught (a numeric ECG value, a major surgery, an unresolved toxicity)
  - criteria that should be DECIDED, not left UNKNOWN: explicit negative serologies, a QTcF value
    below the threshold, a toxicity exception that applies, and a creatinine clearance that must be
    calculated from age, sex, weight and creatinine
  - two criteria with exception clauses ("except alopecia", "excluding ... oxaliplatin-induced
    neuropathy") where the same fact is an exclusion for one trial and allowed by the other

New document types: a 12-lead ECG report, a two-page surgical discharge summary with the
procedure on page 2, a telephone toxicity assessment, and an outside serology panel.

Folders (identical except for three facts):

  data/patients/SYN-005/          QTcF 478 ms; exploratory laparotomy with small-bowel resection
                                  on 2026-07-22; grade 2 oxaliplatin-induced neuropathy
  data/patients/SYN-005-control/  QTcF 441 ms; outpatient core-needle liver biopsy on 2026-07-22;
                                  neuropathy improved to grade 1

Both variants: 67-year-old woman, 52 kg, creatinine 1.3 mg/dL (Cockcroft-Gault about 34 mL/min),
grade 2 alopecia, negative HIV/HBV/HCV serologies, ECOG 1, cycle 1 day 1 scheduled for 2026-08-10.

    python scripts/create_syn005_patient.py [--overwrite]
"""

import argparse
import logging
from pathlib import Path

import pymupdf


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1] / "data" / "patients"
DISCLAIMER = "SYNTHETIC PATIENT - FICTIONAL DATA - FOR DEMONSTRATION ONLY"
PATIENT_ID = "SYN-005"


def documents(control: bool) -> dict:
    if control:
        qtcf, ecg_interp = "441 ms", "Normal sinus rhythm. QTcF within normal limits."
        procedure_course = (
            "Ms. Lee was seen in the interventional radiology suite on 2026-07-22 for an outpatient "
            "procedure to obtain fresh tumor tissue for molecular testing. She tolerated it well and "
            "went home the same day."
        )
        procedure = [
            "Procedure: ultrasound-guided core-needle biopsy of a segment VI liver lesion, 2026-07-22.",
            "Anesthesia: local anesthetic with moderate sedation.",
            "Complications: none. Discharged the same day.",
        ]
        toxicity = (
            "Telephone follow-up before trial screening. Ms. Lee reports that the numbness in her "
            "fingertips from oxaliplatin has improved; she can button clothing and write without "
            "difficulty. Assessed as peripheral sensory neuropathy grade 1. Hair thinning persists, "
            "alopecia grade 2. She reports no diarrhea, mouth sores or fatigue limiting activity. "
            "All other treatment-related toxicities are grade 0 to 1."
        )
    else:
        qtcf, ecg_interp = "478 ms", "Sinus rhythm. Prolonged QTc."
        procedure_course = (
            "Ms. Lee was admitted on 2026-07-21 with abdominal pain and vomiting and was found to have "
            "a small-bowel obstruction from adhesions. She went to the operating room the next day. "
            "Her recovery was uncomplicated and she was discharged on postoperative day 5."
        )
        procedure = [
            "Procedure: exploratory laparotomy with small-bowel resection and primary anastomosis, "
            "2026-07-22, under general anesthesia.",
            "Wound: midline incision, healing; staples to be removed at follow-up.",
            "Discharged 2026-07-27. No lifting over 10 pounds for 6 weeks.",
        ]
        toxicity = (
            "Telephone follow-up before trial screening. Ms. Lee reports persistent numbness and "
            "tingling in both hands and feet since oxaliplatin; she has trouble buttoning clothing "
            "and uses a handrail on stairs. Assessed as oxaliplatin-induced peripheral sensory "
            "neuropathy grade 2, limiting instrumental activities of daily living. Hair thinning "
            "persists, alopecia grade 2. She reports no diarrhea, mouth sores or fatigue limiting "
            "activity. All other treatment-related toxicities are grade 0 to 1."
        )

    return {
        "oncology_note.pdf": {
            "title": "Oncology note", "date": "2026-07-31",
            "pages": [("Clinic visit", [
                "Age: 67 years",
                "Sex: Female",
                "Weight: 52 kg",
                "Diagnosis: Metastatic colorectal adenocarcinoma, liver metastases",
                "Prior treatment: FOLFOX, then FOLFIRI; last dose 2026-06-30, stopped for disease "
                "progression",
                "Performance status: ECOG 1",
                "Plan: referred for clinical trial screening.",
            ])],
        },
        "pathology_report.pdf": {
            "title": "Pathology report", "date": "2024-09-03",
            "pages": [("Molecular findings", [
                "Specimen: sigmoid colon resection, invasive adenocarcinoma",
                "KRAS: G12C mutation detected",
                "MSI: microsatellite stable (MSS)",
                "BRAF: wild type",
            ])],
        },
        "lab_report.pdf": {
            "title": "Laboratory report", "date": "2026-07-31",
            "pages": [("Reported laboratory values", [
                "Absolute neutrophil count (ANC): 2.9 x 10^9/L",
                "White blood cell count: 5.1 x 10^9/L",
                "Hemoglobin: 10.8 g/dL",
                "Platelets: 182 x 10^9/L",
                "Creatinine: 1.3 mg/dL",
                "Total bilirubin: 0.8 mg/dL",
                "AST: 29 U/L",
                "ALT: 25 U/L",
                "No transfusion or growth-factor support in the past 14 days.",
            ])],
        },
        "serology_outside_lab.pdf": {
            "title": "Outside laboratory: infectious serology", "date": "2026-07-29",
            "table": ("Serology panel", [
                ("Test", "Result", "Reference"),
                ("HIV-1/2 antigen/antibody", "Nonreactive", "Nonreactive"),
                ("Hepatitis B surface antigen (HBsAg)", "Negative", "Negative"),
                ("Hepatitis B core antibody (HBcAb), total", "Negative", "Negative"),
                ("Hepatitis C antibody", "Nonreactive", "Nonreactive"),
            ], "Specimen collected 2026-07-29. Reported by an outside reference laboratory."),
        },
        "ecg_report.pdf": {
            "title": "12-lead ECG report", "date": "2026-07-30",
            "table": ("Resting 12-lead ECG measurements", [
                ("Measurement", "Value", ""),
                ("Heart rate", "74 bpm", ""),
                ("PR interval", "164 ms", ""),
                ("QRS duration", "92 ms", ""),
                ("QT interval", "411 ms" if control else "446 ms", ""),
                ("QTcF (Fridericia)", qtcf, ""),
            ], f"Interpretation: {ecg_interp}"),
        },
        "toxicity_phone_note.pdf": {
            "title": "Telephone encounter: toxicity assessment", "date": "2026-07-28", "fontsize": 11,
            "pages": [("Nursing telephone note", [toxicity])],
        },
        "hospital_discharge_summary.pdf": {
            "title": "Discharge summary" if not control else "Procedure summary",
            "date": "2026-07-27" if not control else "2026-07-22", "fontsize": 11,
            "pages": [
                ("Course", [procedure_course, "Procedure details are on page 2."]),
                ("Procedures", procedure),
            ],
        },
        "trial_screening_letter.pdf": {
            "title": "Trial screening letter", "date": "2026-08-03",
            "pages": [("Screening plan", [
                "The patient has been referred for clinical trial screening.",
                "If eligibility is confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-08-10.",
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
    section, rows, footer = document["table"]
    page = pdf.new_page(width=612, height=792)
    _header(page, document, 1, 1)
    page.insert_text((48, 192), section, fontsize=14, fontname="hebo")
    widths = (250, 140, 126) if rows[0][2] else (250, 140)
    top, row_height = 210, 30
    for r, row in enumerate(rows):
        x, y = 48, top + r * row_height
        for width, cell in zip(widths, row):
            page.draw_rect(pymupdf.Rect(x, y, x + width, y + row_height), color=(0.6, 0.6, 0.6), width=0.6)
            page.insert_textbox(pymupdf.Rect(x + 5, y + 8, x + width - 4, y + row_height - 2), cell,
                                fontsize=10, fontname="hebo" if r == 0 else "helv")
            x += width
    page.insert_textbox(pymupdf.Rect(48, top + len(rows) * row_height + 16, 564, 700), footer, fontsize=11)


def write_pdf(path: Path, document: dict) -> None:
    with pymupdf.open() as pdf:
        pdf.set_metadata({"title": document["title"], "subject": DISCLAIMER, "author": "CriterionTrace"})
        if "table" in document:
            _write_table_page(pdf, document)
        else:
            _write_text_pages(pdf, path, document)
        pdf.save(path, deflate=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overwrite", action="store_true", help="replace existing SYN-005 documents")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for folder, control in (("SYN-005", False), ("SYN-005-control", True)):
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
