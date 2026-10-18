# Buried-exclusion test: SYN-002 (buried exclusions)

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_kras_inhibitor**: current_medication 'Sotorasib 960 mg by mouth once daily (started 2025-06-10)' (outside_pharmacy_medication_list_2025.pdf p1, verified=True)
- **family_history_decoy**: not extracted
- **last_chemo_dose**: not extracted

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.43 | 0.43 | 0 | 0 | 0 |
| llm_assessor | 0.71 | 0.86 | 0 | 0 | 1 |

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
| llm_assessor | NCT06412198 | EXC-02 | buried_kras_inhibitor | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06252649 | EXC-03 | buried_kras_inhibitor | DOES_NOT_MEET | DOES_NOT_MEET | ok |
| llm_assessor | NCT06412198 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout | UNKNOWN | DOES_NOT_MEET | acceptable |

## Explanations for misses

- rule_baseline · NCT07559760 EXC-19: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 EXC-02: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06252649 EXC-03: The supplied evidence does not safely establish this criterion without a live criterion assessment.
- rule_baseline · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
- llm_assessor · NCT07559760 EXC-19: No cited evidence addresses this exclusion; absence of a record does not clear it. Converted to UNKNOWN. Original reasoning: The patient has a diagnosis of metastatic colorectal adenocarcinoma but there is no evidence of any other malignancy within 5 years mentioned. Therefore, the exclusion criterion regarding other malignancies within 5 years does not apply.
