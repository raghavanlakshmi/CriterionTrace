# Buried-exclusion test: SYN-004 (blind test on frozen round-2 code: buried exclusions (OCR, ED summary, neurology note))

Labels: Reviewed by Lakshmi before any run on 10/18/26. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_pneumonitis_ocr**: comorbidity 'drug-induced interstitial pneumonitis, felt to be oxaliplatin-related' (pulmonology_consult_2025_scanned.pdf p1, verified=True); diagnosis 'drug-induced interstitial pneumonitis' (pulmonology_consult_2025_scanned.pdf p1, verified=True)
- **pneumonia_trap**: not extracted
- **buried_steroid**: prior_treatment 'Oxaliplatin was permanently discontinued and she completed a prednisone taper in April 2025' (pulmonology_consult_2025_scanned.pdf p1, verified=True); prior_treatment 'prednisone 40 mg by mouth once daily for 5 days (2026-06-14 through 2026-06-18)' (ed_discharge_summary.pdf p1, verified=True); prior_treatment 'oxaliplatin discontinued' (pulmonology_consult_2025_scanned.pdf p1, verified=True); prior_treatment 'prednisone taper completed in April 2025' (pulmonology_consult_2025_scanned.pdf p1, verified=True)
- **steroid_last_dose**: prior_treatment 'prednisone 40 mg by mouth once daily for 5 days (2026-06-14 through 2026-06-18)' (ed_discharge_summary.pdf p1, verified=True)
- **inhaled_topical_steroid_trap**: current_medication 'Fluticasone nasal spray 50 mcg, 2 sprays each nostril daily' (medication_reconciliation.pdf p1, verified=True); current_medication 'Hydrocortisone 1% cream topical, as needed' (medication_reconciliation.pdf p1, verified=True)
- **buried_tia**: not extracted
- **vertigo_trap**: not extracted
- **autoimmune_exception_trap**: comorbidity 'Hashimoto thyroiditis on levothyroxine replacement; gout' (oncology_note.pdf p1, verified=True); comorbidity 'Hashimoto thyroiditis on levothyroxine replacement' (oncology_note.pdf p1, verified=True); comorbidity 'gout' (oncology_note.pdf p1, verified=True)
- **brain_mri**: not extracted
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-06-22' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- ct_chest_abdomen_pelvis.pdf p1, line 7: CT chest, abdomen and pelvis with contrast
- ct_chest_abdomen_pelvis.pdf p1, line 8: Comparison: CT dated 2026-02-27.
- ct_chest_abdomen_pelvis.pdf p1, line 9: Liver: multiple hypodense lesions; the largest, in segment VII, measures 3.4 cm (previously 2.6
- ct_chest_abdomen_pelvis.pdf p1, line 10: cm).
- ct_chest_abdomen_pelvis.pdf p1, line 11: Lungs: mild bibasilar dependent atelectasis.
- ct_chest_abdomen_pelvis.pdf p1, line 11: No pulmonary nodules.
- ct_chest_abdomen_pelvis.pdf p1, line 11: No pleural effusion.
- ct_chest_abdomen_pelvis.pdf p1, line 12: Impression: progression of hepatic metastases, measurable by RECIST 1.1.
- ed_discharge_summary.pdf p1, line 8: Reason for visit: acute pain and swelling of the right big toe.
- ed_discharge_summary.pdf p1, line 11: Pain improved before discharge.
- ed_discharge_summary.pdf p1, line 12: Follow-up: primary care in one week.
- medication_reconciliation.pdf p1, line 2: Medication reconciliation
- medication_reconciliation.pdf p1, line 9: Dose and route
- medication_reconciliation.pdf p1, line 44: Reconciled with the patient at the oncology visit.
- neurology_note_2026.pdf p1, line 7: Follow-up after emergency visit Ms.
- neurology_note_2026.pdf p1, line 7: Roe presented to the emergency department on 2026-02-09 with sudden weakness of the left arm and slurred speech, which resolved completely within 30 minutes.
- neurology_note_2026.pdf p1, line 7: Neurological examination at this visit is normal.
- neurology_note_2026.pdf p1, line 11: MRI brain on 2026-02-10: no acute infarct, no hemorrhage, no intracranial metastases.
- neurology_note_2026.pdf p1, line 12: Assessment: transient ischemic attack on 2026-02-09.
- neurology_note_2026.pdf p1, line 12: Started aspirin 81 mg daily and atorvastatin.
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
| llm_assessor | 0.43 | 0.71 | 1 | 1 | 0 |

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
| llm_assessor | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | **MISS** |
| llm_assessor | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | acceptable |
| llm_assessor | NCT06252649 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-11 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT06252649 EXC-04: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT07559760 EXC-08: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT07559760 EXC-08: Time-window decision lacks dated cited evidence. Converted to UNKNOWN. Original reasoning: The exclusion criterion involves severe or unstable angina, symptomatic congestive heart failure (NYHA ≥ II), significant arrhythmia requiring treatment, arterial thrombosis, acute coronary syndrome, myocardial infarction, cerebrovascular accident including TIA, or other Grade ≥3 cardiovascular events within 6 months prior to first dose (2026-06-22). The patient evidence does not document any such cardiovascular events or diagnoses in the 6 months before the planned study first dose. The comorbidities are Hashimoto thyroiditis, gout, and drug-induced interstitial pneumonitis. Cardiovascular conditions or events relevant to this exclusion criterion are not mentioned at all. Therefore, there is no evidence of the exclusion criterion applying.
- llm_assessor · NCT06412198 EXC-04: The patient has a history of Hashimoto thyroiditis treated with levothyroxine replacement (index 4, 22, 31) which is a replacement therapy and not considered systemic treatment. There is also a history of drug-induced interstitial pneumonitis related to oxaliplatin, with a prednisone taper completed in April 2025 (index 18, 19, 37, 38). The prednisone taper was completed over 1 year before the planned study treatment date 2026-06-22 (index 6). The recent prednisone use in June 2026 (index 21) was a short 5-day course for an acute gout flare starting 2026-06-14 (index 20), which is not an autoimmune disease requiring systemic treatment. No evidence shows active autoimmune disease requiring systemic treatment in the past 2 years. Thus, the exclusion of active autoimmune disease treated systemically in the past 2 years does not apply.
