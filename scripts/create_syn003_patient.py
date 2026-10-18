"""Generate SYN-003: a fresh buried-exclusion patient, plus a matched control.

Built independently of the SYN-002 fixes, before their results were reviewed, to test
whether those fixes generalize. Differences from SYN-002 on purpose:

  - exclusions are buried inside narrative paragraphs, not in lists
  - a different malignancy (Hodgkin lymphoma) and a different drug class (PD-1 inhibitor)
  - a washout that is decidable from the record: last dose and scheduled first study dose
  - two traps in the control: an excepted cancer (basal-cell carcinoma) and a drug that
    was discussed but never started

Folders (identical except for the two buried facts):

  data/patients/SYN-003/          Hodgkin lymphoma treated in 2022, in a 2023 hematology
                                  survivorship note; prior pembrolizumab, in a 2024 outside
                                  oncology consult
  data/patients/SYN-003-control/  the hematology note covers anemia only; the consult says
                                  pembrolizumab was discussed and declined, never started

Both carry: basal-cell carcinoma excised in 2023 (an exception in the malignancy
criterion), FOLFIRI given 2026-04-08, and cycle 1 day 1 scheduled for 2026-04-20.

    python scripts/create_syn003_patient.py [--overwrite]
"""

import argparse
import logging
from pathlib import Path

import pymupdf


LOGGER = logging.getLogger(__name__)
ROOT = Path(__file__).resolve().parents[1] / "data" / "patients"
DISCLAIMER = "SYNTHETIC PATIENT - FICTIONAL DATA - FOR DEMONSTRATION ONLY"
PATIENT_ID = "SYN-003"


def documents(control: bool) -> dict:
    if control:
        hematology = (
            "Ms. Doe is seen for follow-up of iron-deficiency anemia first noted in early 2022. "
            "She completed a course of oral iron and her hemoglobin has normalized. She reports good "
            "energy and walks daily. There is no history of blood cancer. Bone marrow evaluation was "
            "not indicated. Plan: repeat ferritin in six months and continue a balanced diet."
        )
        consult = (
            "Ms. Doe was seen for a second opinion on metastatic colorectal cancer. Her tumor is "
            "microsatellite stable. Pembrolizumab was discussed as a possible option on a basket "
            "study, but she declined and it was not started. We reviewed second-line chemotherapy and "
            "recommended FOLFIRI, which she began in December 2024. She will continue care with her "
            "local oncologist."
        )
    else:
        hematology = (
            "Ms. Doe is seen for routine survivorship follow-up. She has a history of classical "
            "Hodgkin lymphoma, stage IIA, diagnosed in February 2022 and treated with six cycles of "
            "ABVD completed in August 2022; PET-CT in October 2022 showed a complete metabolic "
            "response and she remains in remission. She also had mild iron-deficiency anemia in early "
            "2022 that has resolved with oral iron. She reports good energy and walks daily. Plan: "
            "annual survivorship visit and repeat ferritin in six months."
        )
        consult = (
            "Ms. Doe was seen for a second opinion on metastatic colorectal cancer. Before her "
            "microsatellite status was confirmed, she received pembrolizumab 200 mg every 3 weeks for "
            "four cycles from June to August 2024 on a basket study, stopped for lack of response. "
            "Her tumor was later confirmed microsatellite stable. We reviewed second-line "
            "chemotherapy and recommended FOLFIRI, which she began in December 2024. She will "
            "continue care with her local oncologist."
        )

    return {
        "oncology_note.pdf": {
            "title": "Oncology note", "date": "2026-04-06",
            "pages": [
                ("Patient overview", [
                    "Age: 54 years",
                    "Sex: Female",
                    "Diagnosis: Metastatic colorectal adenocarcinoma",
                    "Metastatic sites: Liver, lung",
                    "Treatment history continues on page 2.",
                ]),
                ("Treatment history and performance status", [
                    "Prior treatment: FOLFOX, then FOLFIRI",
                    "Performance status: ECOG 0",
                    "Referred for second-line clinical trial screening.",
                ]),
            ],
        },
        "pathology_report.pdf": {
            "title": "Pathology report", "date": "2025-01-14",
            "pages": [("Molecular findings", [
                "Specimen: liver biopsy, metastatic adenocarcinoma consistent with colorectal primary",
                "KRAS: G12C mutation detected",
                "MSI: microsatellite stable (MSS)",
                "BRAF: wild type",
            ])],
        },
        "lab_report.pdf": {
            "title": "Laboratory report", "date": "2026-04-03",
            "pages": [("Reported laboratory values", [
                "Absolute neutrophil count (ANC): 2.8 x 10^9/L",
                "Hemoglobin: 12.1 g/dL",
                "Platelets: 205 x 10^9/L",
                "Creatinine: 0.8 mg/dL",
                "Total bilirubin: 0.6 mg/dL",
                "AST: 28 U/L",
                "ALT: 24 U/L",
            ])],
        },
        "infusion_record.pdf": {
            "title": "Infusion record", "date": "2026-04-08",
            "pages": [("Chemotherapy administration", [
                "Regimen: FOLFIRI",
                "Cycle 10 administered on 2026-04-08.",
                "No further cycles scheduled at this clinic.",
            ])],
        },
        "trial_screening_letter.pdf": {
            "title": "Trial screening letter", "date": "2026-04-09",
            "pages": [("Screening plan", [
                "The patient has been referred for second-line clinical trial screening.",
                "If eligibility is confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-04-20.",
                "Final eligibility will be confirmed by the study team.",
            ])],
        },
        "hematology_followup_2023.pdf": {
            "title": "Hematology follow-up", "date": "2023-06-12", "fontsize": 11,
            "pages": [("Visit note", [hematology])],
        },
        "outside_oncology_consult_2024.pdf": {
            "title": "Outside oncology consultation", "date": "2024-11-20", "fontsize": 11,
            "pages": [("Consultation summary", [consult])],
        },
        "dermatology_note_2023.pdf": {
            "title": "Dermatology note", "date": "2023-09-05", "fontsize": 11,
            "pages": [("Procedure note", [
                "Basal-cell carcinoma of the left cheek, excised on 2023-09-05 with clear margins.",
                "No further treatment needed. Annual skin checks recommended.",
            ])],
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
    parser.add_argument("--overwrite", action="store_true", help="replace existing SYN-003 documents")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for folder, control in (("SYN-003", False), ("SYN-003-control", True)):
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
