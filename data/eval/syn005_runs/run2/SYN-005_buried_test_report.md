# Buried-exclusion test: SYN-005 (blind test on frozen round-3 code: buried exclusions plus decidable criteria)

Labels: Reviewed by Lakshmi before any SYN-005 run on 10/18/26. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **qtcf_value**: lab 'Heart rate 74 bpm' (ecg_report.pdf p1, verified=True); lab 'PR interval 164 ms' (ecg_report.pdf p1, verified=True); lab 'QRS duration 92 ms' (ecg_report.pdf p1, verified=True); lab 'QT interval 446 ms' (ecg_report.pdf p1, verified=True); lab 'QTcF (Fridericia) 478 ms' (ecg_report.pdf p1, verified=True)
- **buried_major_surgery**: prior_treatment 'exploratory laparotomy with small-bowel resection and primary anastomosis, 2026-07-22, under general anesthesia' (hospital_discharge_summary.pdf p2, verified=True)
- **biopsy_trap**: not extracted
- **surgery_or_biopsy_date**: prior_treatment 'exploratory laparotomy with small-bowel resection and primary anastomosis, 2026-07-22, under general anesthesia' (hospital_discharge_summary.pdf p2, verified=True)
- **neuropathy_grade**: prior_treatment 'oxaliplatin-induced peripheral sensory neuropathy grade 2' (toxicity_phone_note.pdf p1, verified=True)
- **alopecia_exception**: prior_treatment 'alopecia grade 2' (toxicity_phone_note.pdf p1, verified=True)
- **serology**: lab 'HIV-1/2 antigen/antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis B surface antigen (HBsAg) Negative' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis B core antibody (HBcAb), total Negative' (serology_outside_lab.pdf p1, verified=True); lab 'Hepatitis C antibody Nonreactive' (serology_outside_lab.pdf p1, verified=True)
- **creatinine**: lab 'Creatinine: 1.3 mg/dL' (lab_report.pdf p1, verified=True); lab 'Creatinine: 1.3 mg/dL' (lab_report.pdf p1, verified=False)
- **weight**: not extracted
- **scheduled_first_dose**: planned_study_event 'cycle 1 day 1 of study treatment is scheduled for 2026-08-10' (trial_screening_letter.pdf p1, verified=True)

## Not captured by the tool, review manually

- ecg_report.pdf p1, line 7: Resting 12-lead ECG measurements
- ecg_report.pdf p1, line 20: Interpretation: Sinus rhythm.
- ecg_report.pdf p1, line 20: Prolonged QTc.
- hospital_discharge_summary.pdf p1, line 8: She went to the operating room the next day.
- hospital_discharge_summary.pdf p1, line 8: Her recovery was uncomplicated and she was discharged on postoperative day 5.
- hospital_discharge_summary.pdf p1, line 11: Procedure details are on page 2.
- hospital_discharge_summary.pdf p2, line 10: Wound: midline incision, healing; staples to be removed at follow-up.
- hospital_discharge_summary.pdf p2, line 11: Discharged 2026-07-27.
- hospital_discharge_summary.pdf p2, line 11: No lifting over 10 pounds for 6 weeks.
- lab_report.pdf p1, line 16: No transfusion or growth-factor support in the past 14 days.
- oncology_note.pdf p1, line 7: Clinic visit
- oncology_note.pdf p1, line 10: Weight: 52 kg
- oncology_note.pdf p1, line 14: Plan: referred for clinical trial screening.
- serology_outside_lab.pdf p1, line 2: Outside laboratory: infectious serology
- serology_outside_lab.pdf p1, line 7: Serology panel
- serology_outside_lab.pdf p1, line 23: Specimen collected 2026-07-29.
- serology_outside_lab.pdf p1, line 23: Reported by an outside reference laboratory.
- toxicity_phone_note.pdf p1, line 2: Telephone encounter: toxicity assessment
- toxicity_phone_note.pdf p1, line 10: She reports no diarrhea, mouth sores or fatigue limiting activity.
- toxicity_phone_note.pdf p1, line 10: All other treatment-related toxicities are grade 0 to 1.
- trial_screening_letter.pdf p1, line 8: The patient has been referred for clinical trial screening.
- trial_screening_letter.pdf p1, line 10: Final eligibility will be confirmed by the study team.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.12 | 0.62 | 0 | 0 | 0 |
| llm_assessor | 0.62 | 0.88 | 0 | 0 | 1 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-09 | buried_qtcf | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-11 | buried_major_surgery | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | EXC-04 | buried_toxicity_except_clause | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT06412198 | INC-10 | exception_applies_inclusion | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | EXC-14 | explicit_negative_serology | MEETS | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | INC-12 | calculated_creatinine_clearance | DOES_NOT_MEET | UNKNOWN | acceptable |
| rule_baseline | NCT07559760 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT07559760 | INC-07 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-09 | buried_qtcf | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | EXC-11 | buried_major_surgery | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT07559760 | EXC-04 | buried_toxicity_except_clause | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT06412198 | INC-10 | exception_applies_inclusion | MEETS | DOES_NOT_MEET | **MISS** |
| llm_assessor | NCT07559760 | EXC-14 | explicit_negative_serology | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-12 | calculated_creatinine_clearance | DOES_NOT_MEET | UNKNOWN | acceptable |
| llm_assessor | NCT07559760 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-07 | sanity | MEETS | MEETS | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-09: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-11: Computed time-window guard: missing selected dated event citation (missing dated administration or planned first-dose reference date). Original reasoning: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT07559760 INC-01: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT06412198 INC-10: The patient reports persistent numbness and tingling in both hands and feet since oxaliplatin treatment, with difficulty buttoning clothing and using handrails, indicating ongoing grade 2 oxaliplatin-induced peripheral sensory neuropathy (index 41). This clearly shows the patient has not recovered to ≤ Grade 1 for these treatment-related adverse effects.
