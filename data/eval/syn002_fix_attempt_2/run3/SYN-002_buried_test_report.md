# Buried-exclusion test: SYN-002 (buried exclusions)

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: diagnosis 'Prostate adenocarcinoma, Gleason 3+4=7, treated with radical prostatectomy in March 2022' (primary_care_annual_visit_2023.pdf p2, verified=True); sex 'Male' (primary_care_annual_visit_2023.pdf p2, verified=True); diagnosis 'Prostate adenocarcinoma, Gleason 3+4=7' (primary_care_annual_visit_2023.pdf p2, verified=True); prior_treatment 'radical prostatectomy in March 2022' (primary_care_annual_visit_2023.pdf p2, verified=True); sex 'UNKNOWN' (primary_care_annual_visit_2023.pdf p2, verified=False)
- **buried_kras_inhibitor**: current_medication 'Sotorasib 960 mg by mouth once daily (started 2025-06-10)' (outside_pharmacy_medication_list_2025.pdf p1, verified=True)
- **family_history_decoy**: sex 'UNKNOWN' (primary_care_annual_visit_2023.pdf p2, verified=False)
- **last_chemo_dose**: cancer_stage 'Cycle 8 administered on 2026-03-20' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 8 administered on 2026-03-20.' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 8 administered on 2026-03-20' (infusion_record.pdf p1, verified=True)

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
- primary_care_annual_visit_2023.pdf p2, line 12: Cataract surgery, left eye, 2019
- primary_care_annual_visit_2023.pdf p2, line 13: Appendectomy, 1988
- primary_care_annual_visit_2023.pdf p2, line 14: Family history: mother diagnosed with breast cancer at age 70
- primary_care_annual_visit_2023.pdf p2, line 15: Family history: father with coronary artery disease
- primary_care_annual_visit_2023.pdf p3, line 6: Continue current medications.
- primary_care_annual_visit_2023.pdf p3, line 7: Influenza vaccine given today.
- primary_care_annual_visit_2023.pdf p3, line 8: Colonoscopy referral placed.
- primary_care_annual_visit_2023.pdf p3, line 9: Return in 12 months.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.43 | 0.43 | 0 | 0 | 0 |
| llm_assessor | 0.86 | 0.86 | 1 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-02 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06252649 | EXC-03 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | MEETS | **MISS** |
| llm_assessor | NCT06412198 | EXC-02 | buried_kras_inhibitor | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06252649 | EXC-03 | buried_kras_inhibitor | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-02: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06252649 EXC-03: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
- llm_assessor · NCT07559760 EXC-19: The patient has a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022, which is within the last 5 years. However, this criterion excludes other malignancies within 5 years except basal-cell carcinoma of the skin or cervical carcinoma in situ. Prostate adenocarcinoma treated with surgery is a malignancy, but the exclusion does not specify prostate cancer as an exception. Despite this, the criterion intends to exclude active or recent malignancies other than the specified exceptions. There is no evidence of any other malignancy within 5 years besides prostate cancer, and no evidence that the prostate cancer is currently active or untreated, suggesting it is adequately treated. Therefore, this exclusion does not apply given the information provided.
