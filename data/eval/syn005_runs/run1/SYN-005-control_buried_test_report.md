# Buried-exclusion test: SYN-005-control (matched control: buried facts replaced by look-alikes that should clear or stay UNKNOWN)

Labels: Reviewed by Lakshmi before any SYN-005 run on 10/18/26. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **qtcf_value**: not extracted
- **buried_major_surgery**: not extracted
- **biopsy_trap**: biomarker 'Ultrasound-guided core-needle biopsy of a segment VI liver lesion' (hospital_discharge_summary.pdf p2, verified=True)
- **surgery_or_biopsy_date**: biomarker 'Ultrasound-guided core-needle biopsy of a segment VI liver lesion' (hospital_discharge_summary.pdf p2, verified=True)
- **neuropathy_grade**: biomarker 'Peripheral sensory neuropathy grade 1' (toxicity_phone_note.pdf p1, verified=True)
- **alopecia_exception**: biomarker 'Alopecia grade 2' (toxicity_phone_note.pdf p1, verified=True)
- **serology**: biomarker 'HIV-1/2 antigen/antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True); biomarker 'Hepatitis B surface antigen (HBsAg) Negative' (serology_outside_lab.pdf p1, verified=True); biomarker 'Hepatitis B core antibody (HBcAb), total Negative' (serology_outside_lab.pdf p1, verified=True); biomarker 'Hepatitis C antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True); lab 'HIV-1/2 antigen/antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis B surface antigen (HBsAg) Negative' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis B core antibody (HBcAb), total Negative' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis C antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True)
- **creatinine**: lab 'Creatinine: 1.3 mg/dL' (lab_report.pdf p1, verified=True)
- **weight**: not extracted
- **scheduled_first_dose**: planned_study_event 'Cycle 1 day 1 of study treatment is scheduled for 2026-08-10' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- ecg_report.pdf p1, line 7: Resting 12-lead ECG measurements
- ecg_report.pdf p1, line 10: Heart rate 74 bpm PR interval 164 ms QRS duration 92 ms QT interval 411 ms QTcF (Fridericia) 441 ms
- ecg_report.pdf p1, line 20: Interpretation: Normal sinus rhythm.
- ecg_report.pdf p1, line 20: QTcF within normal limits.
- hospital_discharge_summary.pdf p1, line 8: Ms.
- hospital_discharge_summary.pdf p1, line 8: Lee was seen in the interventional radiology suite on 2026-07-22 for an outpatient procedure to obtain fresh tumor tissue for molecular testing.
- hospital_discharge_summary.pdf p1, line 8: She tolerated it well and went home the same day.
- hospital_discharge_summary.pdf p1, line 10: Procedure details are on page 2.
- hospital_discharge_summary.pdf p2, line 9: Anesthesia: local anesthetic with moderate sedation.
- hospital_discharge_summary.pdf p2, line 10: Complications: none.
- hospital_discharge_summary.pdf p2, line 10: Discharged the same day.
- lab_report.pdf p1, line 16: No transfusion or growth-factor support in the past 14 days.
- oncology_note.pdf p1, line 7: Clinic visit
- oncology_note.pdf p1, line 10: Weight: 52 kg
- oncology_note.pdf p1, line 14: Plan: referred for clinical trial screening.
- serology_outside_lab.pdf p1, line 2: Outside laboratory: infectious serology
- serology_outside_lab.pdf p1, line 7: Serology panel
- serology_outside_lab.pdf p1, line 23: Specimen collected 2026-07-29.
- serology_outside_lab.pdf p1, line 23: Reported by an outside reference laboratory.
- toxicity_phone_note.pdf p1, line 2: Telephone encounter: toxicity assessment
- toxicity_phone_note.pdf p1, line 8: Telephone follow-up before trial screening.
- toxicity_phone_note.pdf p1, line 8: Ms.
- toxicity_phone_note.pdf p1, line 8: Lee reports that the numbness in her fingertips from oxaliplatin has improved; she can button clothing and write without difficulty.
- toxicity_phone_note.pdf p1, line 8: She reports no diarrhea, mouth sores or fatigue limiting activity.
- toxicity_phone_note.pdf p1, line 8: All other treatment-related toxicities are grade 0 to 1.
- trial_screening_letter.pdf p1, line 8: The patient has been referred for clinical trial screening.
- trial_screening_letter.pdf p1, line 10: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.25 | 0.88 | 0 | 0 | 0 |
| llm_assessor | 0.62 | 1.00 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-09 | qtcf_below_threshold | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | EXC-11 | biopsy_trap | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT07559760 | EXC-04 | except_clause_alopecia | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-10 | recovered_to_grade1 | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | EXC-14 | explicit_negative_serology | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | INC-12 | calculated_creatinine_clearance | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | INC-07 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-09 | qtcf_below_threshold | MEETS | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | EXC-11 | biopsy_trap | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-04 | except_clause_alopecia | MEETS | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-10 | recovered_to_grade1 | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-14 | explicit_negative_serology | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-12 | calculated_creatinine_clearance | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT07559760 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-07 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT07559760 INC-01: The supplied evidence does not safely establish this criterion without a live criterion assessment.
