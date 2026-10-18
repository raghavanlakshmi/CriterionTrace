# Buried-exclusion test: SYN-002-control (control (buried lines removed))

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_kras_inhibitor**: not extracted
- **family_history_decoy**: sex 'Male' (primary_care_annual_visit_2023.pdf p2, verified=True); sex 'UNKNOWN' (primary_care_annual_visit_2023.pdf p2, verified=True)
- **last_chemo_dose**: prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 8 administered on 2026-03-20' (infusion_record.pdf p1, verified=True)

## Not captured by the tool, review manually

- infusion_record.pdf p1, line 8: Further cycles on hold pending clinical trial screening.
- oncology_note.pdf p1, line 10: Transferred care to this clinic in March 2026.
- oncology_note.pdf p1, line 11: Treatment history and performance status continue on page 2.
- oncology_note.pdf p2, line 8: Referred for clinical trial prescreening.
- primary_care_annual_visit_2023.pdf p1, line 6: Reason for visit: annual physical examination
- primary_care_annual_visit_2023.pdf p1, line 7: Blood pressure: 132/84 mmHg
- primary_care_annual_visit_2023.pdf p1, line 8: Weight: 84 kg
- primary_care_annual_visit_2023.pdf p1, line 9: No new complaints today.
- primary_care_annual_visit_2023.pdf p1, line 10: Past medical history and family history continue on page 2.
- primary_care_annual_visit_2023.pdf p3, line 6: Continue current medications.
- primary_care_annual_visit_2023.pdf p3, line 7: Influenza vaccine given today.
- primary_care_annual_visit_2023.pdf p3, line 8: Colonoscopy referral placed.
- primary_care_annual_visit_2023.pdf p3, line 9: Return in 12 months.

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
