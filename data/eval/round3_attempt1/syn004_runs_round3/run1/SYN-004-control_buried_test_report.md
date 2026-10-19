# Buried-exclusion test: SYN-004-control (matched control: buried facts replaced by look-alike traps)

Labels: Reviewed by Lakshmi before any run on 10/18/26. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_pneumonitis_ocr**: not extracted
- **pneumonia_trap**: diagnosis 'community-acquired pneumonia' (pulmonology_consult_2025_scanned.pdf p1, verified=True)
- **buried_steroid**: not extracted
- **steroid_last_dose**: prior_treatment 'colchicine 0.6 mg by mouth twice daily for 5 days (2026-06-14 through 2026-06-18)' (ed_discharge_summary.pdf p1, verified=True)
- **inhaled_topical_steroid_trap**: current_medication 'Fluticasone nasal spray 50 mcg, 2 sprays each nostril daily' (medication_reconciliation.pdf p1, verified=True); current_medication 'Hydrocortisone 1% cream topical, as needed' (medication_reconciliation.pdf p1, verified=True)
- **buried_tia**: not extracted
- **vertigo_trap**: not extracted
- **autoimmune_exception_trap**: comorbidity 'Hashimoto thyroiditis on levothyroxine replacement' (oncology_note.pdf p1, verified=True); comorbidity 'gout' (oncology_note.pdf p1, verified=True)
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
- ed_discharge_summary.pdf p1, line 8: Reason for visit: acute pain and swelling of the right big toe.
- ed_discharge_summary.pdf p1, line 11: Pain improved before discharge.
- ed_discharge_summary.pdf p1, line 12: Follow-up: primary care in one week.
- medication_reconciliation.pdf p1, line 2: Medication reconciliation
- medication_reconciliation.pdf p1, line 9: Dose and route
- medication_reconciliation.pdf p1, line 44: Reconciled with the patient at the oncology visit.
- neurology_note_2026.pdf p1, line 7: Follow-up after emergency visit Ms.
- neurology_note_2026.pdf p1, line 7: Roe presented to the emergency department on 2026-02-09 with sudden spinning dizziness on turning her head in bed, lasting under a minute per episode.
- neurology_note_2026.pdf p1, line 7: Neurological examination was normal.
- neurology_note_2026.pdf p1, line 7: The Dix-Hallpike test was positive on the right.
- neurology_note_2026.pdf p1, line 11: MRI brain on 2026-02-10: no acute infarct, no hemorrhage, no intracranial metastases.
- neurology_note_2026.pdf p1, line 12: Assessment: benign paroxysmal positional vertigo.
- neurology_note_2026.pdf p1, line 12: Treated with a canalith repositioning maneuver;
- neurology_note_2026.pdf p1, line 13: symptoms resolved.
- neurology_note_2026.pdf p1, line 13: Plan: vestibular exercises; return if symptoms recur.
- oncology_note.pdf p1, line 7: Clinic visit
- oncology_note.pdf p1, line 15: Plan: referred for clinical trial screening.
- pulmonology_consult_2025_scanned.pdf p1, line 11: Repeat chest X-ray on 2025-04-15 showed resolution of the consolidation.
- pulmonology_consult_2025_scanned.pdf p1, line 11: She is now asymptomatic.
- pulmonology_consult_2025_scanned.pdf p1, line 11: Plan: no further pulmonary follow-up is needed.
- pulmonology_consult_2025_scanned.pdf p1, line 15: Page 1 of 1 (faxed copy)
- trial_screening_letter.pdf p1, line 8: The patient has been referred for clinical trial screening.
- trial_screening_letter.pdf p1, line 10: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.86 | 1.00 | 0 | 0 | 0 |
| llm_assessor | 0.86 | 1.00 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT06252649 | EXC-04 | pneumonia_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-03 | topical_steroid_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT07559760 | EXC-08 | vertigo_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT06252649 | INC-01 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT06412198 | INC-11 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06252649 | EXC-04 | pneumonia_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | EXC-03 | topical_steroid_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-08 | vertigo_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | acceptable |
| llm_assessor | NCT06252649 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-11 | sanity | MEETS | MEETS | ok |

## Explanations for misses

