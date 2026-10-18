# Buried-exclusion test: SYN-004 (blind test on frozen round-2 code: buried exclusions (OCR, ED summary, neurology note))

Labels: Reviewed by Lakshmi before any run on 10/18/26. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_pneumonitis_ocr**: diagnosis 'drug-induced interstitial pneumonitis, felt to be oxaliplatin-related' (pulmonology_consult_2025_scanned.pdf p1, verified=True)
- **pneumonia_trap**: not extracted
- **buried_steroid**: prior_treatment 'prednisone 40 mg by mouth once daily for 5 days (2026-06-14 through 2026-06-18)' (ed_discharge_summary.pdf p1, verified=True); prior_treatment 'Oxaliplatin was permanently discontinued' (pulmonology_consult_2025_scanned.pdf p1, verified=True); prior_treatment 'completed a prednisone taper in April 2025' (pulmonology_consult_2025_scanned.pdf p1, verified=True)
- **steroid_last_dose**: prior_treatment 'prednisone 40 mg by mouth once daily for 5 days (2026-06-14 through 2026-06-18)' (ed_discharge_summary.pdf p1, verified=True)
- **inhaled_topical_steroid_trap**: current_medication 'Fluticasone nasal spray, 50 mcg, 2 sprays each nostril daily, Allergic rhinitis' (medication_reconciliation.pdf p1, verified=True); current_medication 'Hydrocortisone 1% cream, Topical, as needed, Eczema' (medication_reconciliation.pdf p1, verified=True); current_medication 'Fluticasone nasal spray 50 mcg, 2 sprays each nostril daily for Allergic rhinitis' (medication_reconciliation.pdf p1, verified=True); current_medication 'Hydrocortisone 1% cream topical as needed for Eczema' (medication_reconciliation.pdf p1, verified=True)
- **buried_tia**: diagnosis 'transient ischemic attack on 2026-02-09' (neurology_note_2026.pdf p1, verified=True); prior_treatment 'Started aspirin 81 mg daily and atorvastatin' (neurology_note_2026.pdf p1, verified=True)
- **vertigo_trap**: not extracted
- **autoimmune_exception_trap**: comorbidity 'Hashimoto thyroiditis on levothyroxine replacement' (oncology_note.pdf p1, verified=True); comorbidity 'gout' (oncology_note.pdf p1, verified=True)
- **brain_mri**: not extracted
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-06-22' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- ct_chest_abdomen_pelvis.pdf p1, line 7: CT chest, abdomen and pelvis with contrast
- ct_chest_abdomen_pelvis.pdf p1, line 8: Comparison: CT dated 2026-02-27.
- ct_chest_abdomen_pelvis.pdf p1, line 11: Lungs: mild bibasilar dependent atelectasis.
- ct_chest_abdomen_pelvis.pdf p1, line 11: No pulmonary nodules.
- ct_chest_abdomen_pelvis.pdf p1, line 11: No pleural effusion.
- ed_discharge_summary.pdf p1, line 8: Reason for visit: acute pain and swelling of the right big toe.
- ed_discharge_summary.pdf p1, line 11: Pain improved before discharge.
- ed_discharge_summary.pdf p1, line 12: Follow-up: primary care in one week.
- medication_reconciliation.pdf p1, line 2: Medication reconciliation
- medication_reconciliation.pdf p1, line 9: Dose and route
- medication_reconciliation.pdf p1, line 44: Reconciled with the patient at the oncology visit.
- neurology_note_2026.pdf p1, line 7: Follow-up after emergency visit Ms.
- neurology_note_2026.pdf p1, line 7: Neurological examination at this visit is normal.
- neurology_note_2026.pdf p1, line 11: MRI brain on 2026-02-10: no acute infarct, no hemorrhage, no intracranial metastases.
- neurology_note_2026.pdf p1, line 12: Plan:
- neurology_note_2026.pdf p1, line 13: carotid ultrasound; return immediately for new symptoms.
- oncology_note.pdf p1, line 7: Clinic visit
- oncology_note.pdf p1, line 15: Plan: referred for clinical trial screening.
- pulmonology_consult_2025_scanned.pdf p1, line 11: CT chest showed bilateral ground-glass and reticular opacities.
- pulmonology_consult_2025_scanned.pdf p1, line 11: She is now asymptomatic.
- pulmonology_consult_2025_scanned.pdf p1, line 11: Plan: avoid oxaliplatin; repeat pulmonary function tests in one year.
- pulmonology_consult_2025_scanned.pdf p1, line 15: Page 1 of 1 (faxed copy)
- trial_screening_letter.pdf p1, line 8: The patient has been referred for clinical trial screening.
- trial_screening_letter.pdf p1, line 10: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.43 | 0.71 | 0 | 0 | 0 |
| llm_assessor | 0.71 | 0.86 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT06252649 | EXC-04 | buried_pneumonitis_ocr | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT06252649 | INC-01 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT06412198 | INC-11 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06252649 | EXC-04 | buried_pneumonitis_ocr | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | acceptable |
| llm_assessor | NCT06252649 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-11 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT06252649 EXC-04: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT07559760 EXC-08: Compound criterion guard: Part 1: Severe/unstable angina, symptomatic congestive heart failure (NYHA ≥ II), clinically significant arrhythmia requiring treatment, arterial thrombosis, acute coronary syndrome, MI, cerebrovascular accident (including TIA) or other Grade ≥ 3 CV event within 6 months prior to first dose. => UNKNOWN. Computed time-window guard: missing selected dated event citation (missing dated administration or planned first-dose reference date). Original reasoning: Window part: The supplied evidence does not safely establish this criterion without a live criterion assessment. | Part 2: Other compound conditions => UNKNOWN. Other parts were not separately assessed. Original reasoning: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT07559760 EXC-08: Compound criterion guard: Part 1: Severe/unstable angina, symptomatic congestive heart failure (NYHA 62; II), clinically significant arrhythmia requiring treatment, arterial thrombosis, acute coronary syndrome, MI, cerebrovascular accident (including TIA) or other Grade 62; 3 CV event within 6 months prior to first dose. => UNKNOWN. Computed time-window guard: selected event has no verified event date in its quote. Original reasoning: The patient had a transient ischemic attack on 2026-02-09, within 6 months before planned first dose 2026-06-22. However, severity grade and treatment for a Grade 2; 3 cardiovascular event is not documented, so exclusion status is unknown. | Part 2: Unaddressed compound parts => UNKNOWN. Compound criterion has more conditions than returned parts. Original reasoning: The exclusion criterion requires a Grade ≥ 3 cardiovascular event within 6 months prior to the first dose date (2026-06-22). The patient had a transient ischemic attack (TIA) on 2026-02-09, which is a cerebrovascular accident (included in the exclusion list). The TIA date is approximately 4.5 months before the planned first dose date, so it is within the 6-month window. However, it is unclear whether this TIA was Grade ≥ 3 severity and if it necessitated treatment indicating this severity. The evidence does not explicitly state the severity grade or treatment indicating a Grade ≥ 3 cardiovascular event, so this is insufficient to definitively conclude the exclusion applies.
