# Buried-exclusion test: SYN-003 (buried exclusions (narrative))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: diagnosis 'classical Hodgkin lymphoma' (hematology_followup_2023.pdf p1, verified=True); cancer_stage 'stage IIA' (hematology_followup_2023.pdf p1, verified=True); prior_treatment 'six cycles of ABVD completed in August 2022' (hematology_followup_2023.pdf p1, verified=True); diagnosis 'classical Hodgkin lymphoma' (hematology_followup_2023.pdf p1, verified=True); cancer_stage 'stage IIA' (hematology_followup_2023.pdf p1, verified=True)
- **buried_pd1**: prior_treatment 'pembrolizumab 200 mg every 3 weeks for four cycles from June to August 2024' (outside_oncology_consult_2024.pdf p1, verified=True)
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True); prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: not extracted

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed. Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 2: Hematology follow-up
- hematology_followup_2023.pdf p1, line 6: Ms. Doe is seen for routine survivorship follow-up. She has a history of classical Hodgkin lymphoma,
- hematology_followup_2023.pdf p1, line 8: PET-CT in October 2022 showed a complete metabolic response and she remains in remission. She also
- hematology_followup_2023.pdf p1, line 9: had mild iron-deficiency anemia in early 2022 that has resolved with oral iron. She reports good energy
- hematology_followup_2023.pdf p1, line 10: and walks daily. Plan: annual survivorship visit and repeat ferritin in six months.
- infusion_record.pdf p1, line 8: No further cycles scheduled at this clinic.
- oncology_note.pdf p1, line 10: Treatment history continues on page 2.
- oncology_note.pdf p2, line 8: Referred for second-line clinical trial screening.
- outside_oncology_consult_2024.pdf p1, line 2: Outside oncology consultation
- outside_oncology_consult_2024.pdf p1, line 5: Consultation summary
- outside_oncology_consult_2024.pdf p1, line 6: Ms. Doe was seen for a second opinion on metastatic colorectal cancer. Before her microsatellite status
- outside_oncology_consult_2024.pdf p1, line 8: 2024 on a basket study, stopped for lack of response. Her tumor was later confirmed microsatellite stable.
- outside_oncology_consult_2024.pdf p1, line 10: 2024. She will continue care with her local oncologist.
- trial_screening_letter.pdf p1, line 2: Trial screening letter
- trial_screening_letter.pdf p1, line 5: Screening plan
- trial_screening_letter.pdf p1, line 6: The patient has been referred for second-line clinical trial screening.
- trial_screening_letter.pdf p1, line 7: If eligibility is confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-04-20.
- trial_screening_letter.pdf p1, line 8: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.40 | 0.60 | 0 | 0 | 0 |
| llm_assessor | 0.60 | 0.80 | 1 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | MEETS | **MISS** |
| llm_assessor | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-01: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT07559760 EXC-19: The patient has a history of basal-cell carcinoma of the left cheek excised on 2023-09-05 with clear margins, which is excluded from this criterion. The patient also has a history of classical Hodgkin lymphoma diagnosed in February 2022 (approximately 1.5 years ago) and currently in remission as of October 2022. However, classical Hodgkin lymphoma is a malignancy diagnosed within 5 years. The exclusion criterion excludes other malignancies within 5 years but allows for adequately treated basal-cell carcinoma of the skin or cervical carcinoma in situ. Because classical Hodgkin lymphoma is not an exception listed, it qualifies as another malignancy within 5 years. Therefore, the exclusion criterion applies. However, since the patient is in remission and the basal-cell carcinoma was adequately treated, and considering trial criteria might consider remission status, there is a slight conflict. But the criterion is literally about other malignancies within 5 years, and classical Hodgkin lymphoma was diagnosed within that window, so the exclusion applies.
