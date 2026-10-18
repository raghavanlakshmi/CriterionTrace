# Buried-exclusion test: SYN-003-control (control (buried facts removed, traps kept))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_pd1**: prior_treatment 'Pembrolizumab was discussed as a possible option on a basket study, but she declined and it was not started' (outside_oncology_consult_2024.pdf p1, verified=True)
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True); prior_treatment 'excision of Basal-cell carcinoma of the left cheek on 2023-09-05 with clear margins' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'Cycle 10 of FOLFIRI administered on 2026-04-08' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-04-20' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed.
- dermatology_note_2023.pdf p1, line 7: Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 6: She reports good energy and walks daily.
- hematology_followup_2023.pdf p1, line 6: There is no history of blood cancer.
- hematology_followup_2023.pdf p1, line 6: Bone marrow evaluation was not indicated.
- hematology_followup_2023.pdf p1, line 6: Plan: repeat ferritin in six months and continue a balanced diet.
- infusion_record.pdf p1, line 8: No further cycles scheduled at this clinic.
- oncology_note.pdf p1, line 10: Treatment history continues on page 2.
- oncology_note.pdf p2, line 8: Referred for second-line clinical trial screening.
- outside_oncology_consult_2024.pdf p1, line 7: She will continue care with her local oncologist.
- trial_screening_letter.pdf p1, line 6: The patient has been referred for second-line clinical trial screening.
- trial_screening_letter.pdf p1, line 8: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.80 | 1.00 | 0 | 0 | 0 |
| llm_assessor | 0.80 | 0.80 | 0 | 0 | 1 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | DOES_NOT_MEET | **MISS** |
| llm_assessor | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- llm_assessor · NCT07559760 EXC-19: Compound criterion guard: Part 1: Other malignancies within 5 years => UNKNOWN. History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN. Original reasoning: Basal-cell carcinoma of the left cheek was excised on 2023-09-05 with clear margins and is specifically excepted in the criterion. No other malignancies within 5 years are documented. | Part 2: except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ. => DOES_NOT_MEET. Basal-cell carcinoma of the skin was excised with clear margins, thus is an allowed exception to the exclusion of other malignancies within 5 years. Original reasoning: The patient had basal-cell carcinoma of the left cheek diagnosed and excised on 2023-09-05 with clear margins, which is within 5 years of the planned study treatment first dose (2026-04-20). However, the criterion specifically excludes other malignancies within 5 years except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ. Since the basal-cell carcinoma of the skin was excised with clear margins and is an allowed exception, it does not exclude the patient from eligibility.
