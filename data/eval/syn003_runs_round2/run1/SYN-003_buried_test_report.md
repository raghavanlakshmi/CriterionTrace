# Buried-exclusion test: SYN-003 (buried exclusions (narrative))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: diagnosis 'classical Hodgkin lymphoma, stage IIA' (hematology_followup_2023.pdf p1, verified=True); prior_treatment 'six cycles of ABVD' (hematology_followup_2023.pdf p1, verified=True); diagnosis 'classical Hodgkin lymphoma, stage IIA' (hematology_followup_2023.pdf p1, verified=True); prior_treatment 'six cycles of ABVD completed in August 2022' (hematology_followup_2023.pdf p1, verified=True); diagnosis 'complete metabolic response' (hematology_followup_2023.pdf p1, verified=True)
- **buried_pd1**: prior_treatment 'pembrolizumab 200 mg every 3 weeks for four cycles from June to August 2024' (outside_oncology_consult_2024.pdf p1, verified=True); prior_treatment 'pembrolizumab 200 mg every 3 weeks for four cycles from June to August 2024 on a basket study' (outside_oncology_consult_2024.pdf p1, verified=True)
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True); prior_treatment 'excised on 2023-09-05 with clear margins' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'FOLFIRI, Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True); prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-04-20' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed.
- dermatology_note_2023.pdf p1, line 7: Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 6: She reports good energy and walks daily.
- hematology_followup_2023.pdf p1, line 6: Plan: annual survivorship visit and repeat ferritin in six months.
- infusion_record.pdf p1, line 8: No further cycles scheduled at this clinic.
- oncology_note.pdf p1, line 10: Treatment history continues on page 2.
- oncology_note.pdf p2, line 8: Referred for second-line clinical trial screening.
- outside_oncology_consult_2024.pdf p1, line 9: She will continue care with her local oncologist.
- trial_screening_letter.pdf p1, line 6: The patient has been referred for second-line clinical trial screening.
- trial_screening_letter.pdf p1, line 8: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.40 | 0.60 | 0 | 0 | 0 |
| llm_assessor | 0.80 | 0.80 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-01: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT07559760 EXC-19: Status contradicts explanation. Converted to UNKNOWN. Original reasoning: The patient has a history of classical Hodgkin lymphoma diagnosed in February 2022 and treated with six cycles of ABVD completed in August 2022, with remission confirmed in October 2022. This diagnosis and treatment fall within the past 5 years. Since this is a malignancy within 5 years, it would typically be an exclusion. However, the exclusion lists exceptions for adequately treated basal-cell carcinoma of skin and cervical carcinoma in situ only. The basal-cell carcinoma of the left cheek was excised with clear margins in September 2023, which is an exception and does not count as exclusion. The Hodgkin lymphoma is a separate malignancy, but the criterion does not mention hematologic malignancies or provide an exception. Given the recent history of classical Hodgkin lymphoma (less than 5 years ago), this would qualify as another malignancy within 5 years, thus the exclusion applies due to the Hodgkin lymphoma. However, the criterion text applies exclusion for 'other malignancies within 5 years, except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ.' The Hodgkin lymphoma represents another malignancy within 5 years, which means this exclusion applies. Therefore, the patient meets the exclusion criterion based on the Hodgkin lymphoma diagnosis within the past 5 years.
