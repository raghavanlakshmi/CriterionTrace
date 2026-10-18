# Buried-exclusion test: SYN-002-control (control (buried lines removed))

Labels: APPROVED by user in chat on 2026-10-17 before first live run; original expected labels unchanged. Models: extraction gpt-4.1-mini, assessment gpt-4.1-mini.

## Extraction: were the buried facts captured?

- **buried_malignancy**: not extracted
- **buried_kras_inhibitor**: not extracted
- **family_history_decoy**: not extracted
- **last_chemo_dose**: prior_treatment 'FOLFIRI' (infusion_record.pdf p1, verified=True)

## Assessment

| Method | Accuracy | Acceptable | Unsafe false clearance | UNKNOWN to MEETS | False exclusion |
|---|---|---|---|---|---|
| rule_baseline | 0.86 | 0.86 | 0 | 0 | 0 |
| llm_assessor | 0.86 | 1.00 | 0 | 0 | 1 |

| Method | Trial | Criterion | Probe | Expected | Got | Result |
|---|---|---|---|---|---|---|
| rule_baseline | NCT07559760 | EXC-19 | buried_malignancy | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | EXC-02 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06252649 | EXC-03 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| rule_baseline | NCT06412198 | INC-01 | sanity | MEETS | UNKNOWN | **MISS** |
| rule_baseline | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| rule_baseline | NCT07559760 | EXC-05 | washout | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT07559760 | EXC-19 | buried_malignancy | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | EXC-02 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06252649 | EXC-03 | buried_kras_inhibitor | UNKNOWN | UNKNOWN | ok |
| llm_assessor | NCT06412198 | INC-01 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT06412198 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | INC-02 | sanity | MEETS | MEETS | ok |
| llm_assessor | NCT07559760 | EXC-05 | washout | UNKNOWN | DOES_NOT_MEET | acceptable |

## Explanations for misses

- rule_baseline · NCT06412198 INC-01: The matched fact covers only part of this criterion; its additional requirements are not documented.
