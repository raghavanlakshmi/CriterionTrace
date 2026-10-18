# Buried-exclusion test: SYN-003-control (control (buried facts removed, traps kept))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_pd1**: not extracted
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: not extracted

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed. Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 2: Hematology follow-up
- hematology_followup_2023.pdf p1, line 6: Ms. Doe is seen for follow-up of iron-deficiency anemia first noted in early 2022. She completed a course
- hematology_followup_2023.pdf p1, line 7: of oral iron and her hemoglobin has normalized. She reports good energy and walks daily. There is no
- hematology_followup_2023.pdf p1, line 8: history of blood cancer. Bone marrow evaluation was not indicated. Plan: repeat ferritin in six months and
- hematology_followup_2023.pdf p1, line 9: continue a balanced diet.
- infusion_record.pdf p1, line 8: No further cycles scheduled at this clinic.
- oncology_note.pdf p1, line 10: Treatment history continues on page 2.
- oncology_note.pdf p2, line 8: Referred for second-line clinical trial screening.
- outside_oncology_consult_2024.pdf p1, line 2: Outside oncology consultation
- outside_oncology_consult_2024.pdf p1, line 5: Consultation summary
- outside_oncology_consult_2024.pdf p1, line 6: Ms. Doe was seen for a second opinion on metastatic colorectal cancer. Her tumor is microsatellite stable.
- outside_oncology_consult_2024.pdf p1, line 7: Pembrolizumab was discussed as a possible option on a basket study, but she declined and it was not
- outside_oncology_consult_2024.pdf p1, line 8: started. We reviewed second-line chemotherapy and recommended FOLFIRI, which she began in
- outside_oncology_consult_2024.pdf p1, line 9: December 2024. She will continue care with her local oncologist.
- trial_screening_letter.pdf p1, line 2: Trial screening letter
- trial_screening_letter.pdf p1, line 5: Screening plan
- trial_screening_letter.pdf p1, line 6: The patient has been referred for second-line clinical trial screening.
- trial_screening_letter.pdf p1, line 7: If eligibility is confirmed, cycle 1 day 1 of study treatment is scheduled for 2026-04-20.
- trial_screening_letter.pdf p1, line 8: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.80 | 1.00 | 0 | 0 | 0 |
| llm_assessor | 0.60 | 0.80 | 1 | 1 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | excepted_cancer_trap | UNKNOWN | MEETS | **MISS** |
| llm_assessor | NCT06412198 | EXC-01 | discussed_not_given_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- llm_assessor · NCT07559760 EXC-19: The patient had basal-cell carcinoma (BCC) of the left cheek excised on 2023-09-05 with clear margins. The exclusion criterion exempts adequately treated basal-cell carcinoma of the skin. Since the BCC was excised with clear margins, it is considered adequately treated, and therefore the exclusion due to other malignancies within 5 years does not apply.
