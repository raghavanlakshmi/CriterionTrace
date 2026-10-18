# Buried-exclusion test: SYN-002 (buried exclusions)

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: comorbidity 'Hypertension' (primary_care_annual_visit_2023.pdf p2, verified=True); comorbidity 'Hyperlipidemia' (primary_care_annual_visit_2023.pdf p2, verified=True); comorbidity 'Gastroesophageal reflux disease' (primary_care_annual_visit_2023.pdf p2, verified=True); diagnosis 'Prostate adenocarcinoma, Gleason 3+4=7' (primary_care_annual_visit_2023.pdf p2, verified=True); prior_treatment 'Radical prostatectomy in March 2022' (primary_care_annual_visit_2023.pdf p2, verified=True); current_medication 'Lisinopril' (primary_care_annual_visit_2023.pdf p2, verified=True); current_medication 'Atorvastatin' (primary_care_annual_visit_2023.pdf p2, verified=True); comorbidity 'Osteoarthritis, right knee' (primary_care_annual_visit_2023.pdf p2, verified=True)
- **buried_kras_inhibitor**: biomarker 'Sotorasib 960 mg by mouth once daily (started 2025-06-10)' (outside_pharmacy_medication_list_2025.pdf p1, verified=True); current_medication 'Lisinopril 20 mg by mouth once daily' (outside_pharmacy_medication_list_2025.pdf p1, verified=True); current_medication 'Atorvastatin 40 mg by mouth once daily' (outside_pharmacy_medication_list_2025.pdf p1, verified=True); current_medication 'Omeprazole 20 mg by mouth once daily' (outside_pharmacy_medication_list_2025.pdf p1, verified=True); current_medication 'Ondansetron 8 mg by mouth every 8 hours as needed for nausea' (outside_pharmacy_medication_list_2025.pdf p1, verified=True); current_medication 'Loperamide 2 mg by mouth as needed for diarrhea' (outside_pharmacy_medication_list_2025.pdf p1, verified=True)
- **family_history_decoy**: not extracted
- **last_chemo_dose**: prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True); prior_treatment 'Cycle 8 administered on 2026-03-20' (infusion_record.pdf p1, verified=True)

## Not captured by the tool, review manually

- infusion_record.pdf p1, line 8: Further cycles on hold pending clinical trial screening.
- oncology_note.pdf p1, line 10: Transferred care to this clinic in March 2026.
- oncology_note.pdf p1, line 11: Treatment history and performance status continue on page 2.
- oncology_note.pdf p2, line 8: Referred for clinical trial prescreening.
- primary_care_annual_visit_2023.pdf p1, line 6: Reason for visit: annual physical examination
- primary_care_annual_visit_2023.pdf p1, line 7: Blood pressure: 132/84 mmHg
- primary_care_annual_visit_2023.pdf p1, line 8: Weight: 84 kg
- primary_care_annual_visit_2023.pdf p1, line 9: No new complaints today.
- primary_care_annual_visit_2023.pdf p1, line 10: Past medical history and family history continue on page 2.
- primary_care_annual_visit_2023.pdf p2, line 14: Family history: mother diagnosed with breast cancer at age 70
- primary_care_annual_visit_2023.pdf p2, line 15: Family history: father with coronary artery disease
- primary_care_annual_visit_2023.pdf p3, line 6: Continue current medications.
- primary_care_annual_visit_2023.pdf p3, line 7: Influenza vaccine given today.
- primary_care_annual_visit_2023.pdf p3, line 8: Colonoscopy referral placed.
- primary_care_annual_visit_2023.pdf p3, line 9: Return in 12 months.

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.43 | 0.43 | 0 | 0 | 0 |
| llm_assessor | 0.43 | 0.43 | 0 | 0 | 0 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | EXC-02 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06252649 | EXC-03 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | EXC-02 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06252649 | EXC-03 | buried_kras_inhibitor | DOES_NOT_MEET | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: Compound criterion guard: Part 1: Other malignancies within 5 years, except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ. => UNKNOWN. Window part: The supplied evidence does not safely establish this criterion without a live criterion assessment. | Part 2: Other compound conditions => UNKNOWN. Other parts were not separately assessed. Original reasoning: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-02: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06252649 EXC-03: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
- llm_assessor · NCT07559760 EXC-19: Compound criterion guard: Part 1: Other malignancies within 5 years, except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ. => UNKNOWN. The patient had prostate adenocarcinoma diagnosed and treated with radical prostatectomy in March 2022, which is within 5 years. There is no documented information ruling out this malignancy or indicating it was adequately treated or an exception applies. | Part 2: Unaddressed compound parts => UNKNOWN. Compound criterion has more conditions than returned parts. Original reasoning: The criterion excludes patients with other malignancies within 5 years except for adequately treated basal-cell carcinoma of the skin or cervical carcinoma in situ. The evidence shows a diagnosis of prostate adenocarcinoma treated with radical prostatectomy in March 2022. This malignancy is within 5 years but there is no information about adequacy of treatment or current status. Therefore, it is unknown whether this exclusion applies or not.
- llm_assessor · NCT06412198 EXC-02: Compound criterion guard: Part 1: Prior KRASG12C inhibition therapy => DOES_NOT_MEET. The patient was on Sotorasib, a KRASG12C inhibitor, starting 2025-06-10, indicating prior KRASG12C inhibition therapy. Original reasoning: The patient has documented use of Sotorasib starting 2025-06-10, which is a KRASG12C inhibitor, indicating prior KRASG12C inhibition therapy. Therefore, the exclusion criteria applies.
- llm_assessor · NCT06252649 EXC-03: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- llm_assessor · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
