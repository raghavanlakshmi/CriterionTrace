# Buried-exclusion test: SYN-003 (buried exclusions (narrative))

Labels: Reviewed by Lakshmi - 10/18/2026, before any run. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: diagnosis 'classical Hodgkin lymphoma, stage IIA' (hematology_followup_2023.pdf p1, verified=True)
- **buried_pd1**: prior_treatment 'pembrolizumab 200 mg every 3 weeks for four cycles from June to August 2024' (outside_oncology_consult_2024.pdf p1, verified=True); prior_treatment 'pembrolizumab 200 mg every 3 weeks for four cycles from June to August 2024' (outside_oncology_consult_2024.pdf p1, verified=True)
- **excepted_cancer_trap**: diagnosis 'Basal-cell carcinoma of the left cheek' (dermatology_note_2023.pdf p1, verified=True)
- **last_chemo_dose**: prior_treatment 'Cycle 10 administered on 2026-04-08' (infusion_record.pdf p1, verified=True)
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-04-20' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- dermatology_note_2023.pdf p1, line 7: No further treatment needed.
- dermatology_note_2023.pdf p1, line 7: Annual skin checks recommended.
- hematology_followup_2023.pdf p1, line 6: She has a history of classical Hodgkin lymphoma, stage IIA, diagnosed in February 2022 and treated with six cycles of ABVD completed in August 2022; PET-CT in October 2022 showed a complete metabolic response and she remains in remission.
- hematology_followup_2023.pdf p1, line 6: She reports good energy and walks daily.
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
| llm_assessor | 0.60 | 0.80 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | EXC-01 | buried_pd1 | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout_with_dates | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-01: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT07559760 EXC-19: Status contradicts explanation. Converted to UNKNOWN. Original reasoning: The criterion excludes patients with other malignancies within 5 years except adequately treated basal-cell carcinoma of the skin or cervical carcinoma in situ. The patient has a history of basal-cell carcinoma of the left cheek excised with clear margins in 2023, which is an allowed exception. She also has a history of classical Hodgkin lymphoma diagnosed in February 2022, treated with six cycles of ABVD chemotherapy completed in August 2022, and is currently in complete metabolic response/remission as of October 2022. This lymphoma is an additional malignancy within 5 years but not listed as an allowed exception, so it could be an exclusion. However, as this is a classical malignancy treated and in remission, it aligns with malignancies potentially disqualifying as per the criterion, but the criterion specifically allows basal-cell carcinoma and cervical carcinoma in situ only. Therefore, given the presence of Hodgkin lymphoma within 5 years, the exclusion applies. But if the clinical context interprets Hodgkin lymphoma remission as not counted here, it might differ. Since the criterion text is strict, exclusion applies based on the lymphoma.
