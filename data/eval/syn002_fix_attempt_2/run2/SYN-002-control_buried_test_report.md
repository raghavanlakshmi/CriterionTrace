# Buried-exclusion test: SYN-002-control (control (buried lines removed))

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_kras_inhibitor**: not extracted
- **family_history_decoy**: not extracted
- **last_chemo_dose**: prior_treatment 'FOLFIRI
Cycle 8 administered on 2026-03-20' (infusion_record.pdf p1, verified=True); sex 'Male' (infusion_record.pdf p1, verified=True)

## Not captured by the tool, review manually

- oncology_note.pdf p1, line 10: Transferred care to this clinic in March 2026.
- oncology_note.pdf p1, line 11: Treatment history and performance status continue on page 2.
- oncology_note.pdf p2, line 8: Referred for clinical trial prescreening.
- pathology_report.pdf p1, line 6: Specimen: liver biopsy, metastatic adenocarcinoma consistent with colorectal primary
- primary_care_annual_visit_2023.pdf p1, line 10: Past medical history and family history continue on page 2.
- primary_care_annual_visit_2023.pdf p2, line 10: Cataract surgery, left eye, 2019
- primary_care_annual_visit_2023.pdf p2, line 11: Appendectomy, 1988
- primary_care_annual_visit_2023.pdf p2, line 12: Family history: mother diagnosed with breast cancer at age 70
- primary_care_annual_visit_2023.pdf p2, line 13: Family history: father with coronary artery disease

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.86 | 0.86 | 0 | 0 | 0 |
| llm_assessor | 1.00 | 1.00 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-02 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06252649 | EXC-03 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | EXC-02 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06252649 | EXC-03 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |

## Explanations for misses

- rule_baseline · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
