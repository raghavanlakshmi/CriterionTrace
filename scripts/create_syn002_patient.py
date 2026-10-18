"""Generate SYN-002: a buried-exclusion test patient, plus a matched control.

Suggested by a clinician-run evaluation team: an exclusion that IS in the record,
but only in an old or secondary document, should still be found. The opposite
failure from SYN-001 (where an exclusion is never mentioned and must stay UNKNOWN).

Two folders are written, identical except for the two buried facts:

  data/patients/SYN-002/          prior prostate cancer (2022) buried in a 2023
                                  primary-care note, and prior sotorasib (a KRAS
                                  G12C inhibitor) buried in a 2025 outside
                                  pharmacy medication list
  data/patients/SYN-002-control/  the same documents with those two lines removed

Both variants also carry two decoys that must NOT trigger an exclusion: a family
history of breast cancer (mother) and the current oncology summary, which lists
only "FOLFOX, then FOLFIRI". The last FOLFIRI dose (2026-03-20) is the same in
both, for the washout check.

    python scripts/create_syn002_patient.py [--overwrite]
"""

import argparse
import logging
from pathlib import Path

import pymupdf


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1] / "data" / "patients"
DISCLAIMER = "SYNTHETIC PATIENT - FICTIONAL DATA - FOR DEMONSTRATION ONLY"
PATIENT_ID = "SYN-002"

BURIED_MALIGNANCY = (
    "Prostate adenocarcinoma, Gleason 3+4=7, treated with radical prostatectomy "
    "in March 2022; PSA undetectable at last check"
)
BURIED_KRAS_INHIBITOR = "Sotorasib 960 mg by mouth once daily (started 2025-06-10)"


def documents(control: bool) -> dict:
    """Return every document; the control variant drops the two buried facts."""
    history = [
        "Hypertension, on lisinopril",
        "Hyperlipidemia, on atorvastatin",
        "Gastroesophageal reflux disease",
        "Osteoarthritis, right knee",
        "Cataract surgery, left eye, 2019",
        "Appendectomy, 1988",
    ]
    if not control:
        # Placed mid-list, between routine items, on page 2 of a 2023 note.
        history.insert(3, BURIED_MALIGNANCY)

    medications = [
        "Lisinopril 20 mg by mouth once daily",
        "Atorvastatin 40 mg by mouth once daily",
        "Omeprazole 20 mg by mouth once daily",
        "Ondansetron 8 mg by mouth every 8 hours as needed for nausea",
        "Loperamide 2 mg by mouth as needed for diarrhea",
    ]
    if not control:
        medications.insert(3, BURIED_KRAS_INHIBITOR)

    return {
        "oncology_note.pdf": {
            "title": "Oncology note",
            "date": "2026-03-30",
            "pages": [
                ("Patient overview", [
                    "Age: 61 years",
                    "Sex: Male",
                    "Diagnosis: Metastatic colorectal adenocarcinoma",
                    "Metastatic site: Liver",
                    "Transferred care to this clinic in March 2026.",
                    "Treatment history and performance status continue on page 2.",
                ]),
                ("Treatment history and performance status", [
                    "Prior treatment: FOLFOX, then FOLFIRI",
                    "Performance status: ECOG 1",
                    "Referred for clinical trial prescreening.",
                ]),
            ],
        },
        "pathology_report.pdf": {
            "title": "Pathology report",
            "date": "2024-02-12",
            "pages": [
                ("Molecular findings", [
                    "Specimen: liver biopsy, metastatic adenocarcinoma consistent with colorectal primary",
                    "KRAS: G12C mutation detected",
                    "MSI: microsatellite stable (MSS)",
                    "BRAF: wild type",
                ]),
            ],
        },
        "lab_report.pdf": {
            "title": "Laboratory report",
            "date": "2026-03-28",
            "pages": [
                ("Reported laboratory values", [
                    "Absolute neutrophil count (ANC): 2.4 x 10^9/L",
                    "Hemoglobin: 11.8 g/dL",
                    "Platelets: 182 x 10^9/L",
                    "Creatinine: 1.0 mg/dL",
                    "Total bilirubin: 0.7 mg/dL",
                    "AST: 34 U/L",
                    "ALT: 29 U/L",
                ]),
            ],
        },
        "infusion_record.pdf": {
            "title": "Infusion record",
            "date": "2026-03-20",
            "pages": [
                ("Chemotherapy administration", [
                    "Regimen: FOLFIRI",
                    "Cycle 8 administered on 2026-03-20.",
                    "Further cycles on hold pending clinical trial screening.",
                ]),
            ],
        },
        "primary_care_annual_visit_2023.pdf": {
            "title": "Primary care annual visit",
            "date": "2023-05-16",
            "fontsize": 11,
            "pages": [
                ("Visit summary", [
                    "Reason for visit: annual physical examination",
                    "Blood pressure: 132/84 mmHg",
                    "Weight: 84 kg",
                    "No new complaints today.",
                    "Past medical history and family history continue on page 2.",
                ]),
                ("Past medical history", history + [
                    "Family history: mother diagnosed with breast cancer at age 70",
                    "Family history: father with coronary artery disease",
                ]),
                ("Plan", [
                    "Continue current medications.",
                    "Influenza vaccine given today.",
                    "Colonoscopy referral placed.",
                    "Return in 12 months.",
                ]),
            ],
        },
        "outside_pharmacy_medication_list_2025.pdf": {
            "title": "Outside pharmacy medication list",
            "date": "2025-10-02",
            "fontsize": 11,
            "pages": [
                ("Active medications", medications),
            ],
        },
    }


def write_pdf(path: Path, document: dict) -> None:
    fontsize = document.get("fontsize", 12)
    with pymupdf.open() as pdf:
        pdf.set_metadata({"title": document["title"], "subject": DISCLAIMER, "author": "CriterionTrace"})
        for page_number, (section, facts) in enumerate(document["pages"], start=1):
            page = pdf.new_page(width=612, height=792)
            page.insert_text((48, 42), DISCLAIMER, fontsize=9, color=(0.45, 0.15, 0.1))
            page.insert_text((48, 88), document["title"], fontsize=23, fontname="hebo")
            page.insert_text((48, 120), f"Patient ID: {PATIENT_ID}", fontsize=11)
            page.insert_text((48, 142), f"Document date: {document['date']}", fontsize=11)
            page.draw_line((48, 160), (564, 160), color=(0.7, 0.7, 0.7))
            page.insert_text((48, 192), section, fontsize=14, fontname="hebo")
            remaining = page.insert_textbox(
                pymupdf.Rect(48, 218, 564, 710), "\n\n".join(facts), fontsize=fontsize, lineheight=1.4
            )
            if remaining < 0:
                raise ValueError(f"Content overflows {path.name}, page {page_number}")
            page.insert_text((48, 738), "Fictional document. No real patient information.", fontsize=9)
            page.insert_text((48, 756), f"Page {page_number} of {len(document['pages'])}", fontsize=9)
        pdf.save(path, deflate=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--overwrite", action="store_true", help="replace existing SYN-002 documents")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for folder, control in (("SYN-002", False), ("SYN-002-control", True)):
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
