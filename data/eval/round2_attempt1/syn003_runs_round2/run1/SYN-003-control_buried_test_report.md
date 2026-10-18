# Buried-exclusion test: SYN-003-control (control (buried facts removed, traps kept))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_pd1**: prior_treatment 'Pembrolizumab was discussed as a possible option on a basket study, but she declined and it was not started' (outside_oncology_consult_2024.pdf p1, verified=True)
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'FOLFIRI Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True); planned_study_event 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-04-20' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed.
- dermatology_note_2023.pdf p1, line 7: Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 6: She reports good energy and walks daily.
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
| llm_assessor | 0.80 | 1.00 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

