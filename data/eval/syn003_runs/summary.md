# SYN-003 generalization: three fresh runs

Labels and test inputs were committed before execution in `831e76d7943b7603893728e0f20981ed6ebf94b3` (2026-10-18T10:58:03-04:00). All runs used that same commit, gpt-4.1-mini for extraction and assessment, fresh extraction (no --reuse-evidence), and the supplied signed-off labels without edits. No implementation fixes were made between or after runs. Each manifest records UTC start/end times and SHA256 hashes for source code, runner, labels, patient PDFs and trial criteria; all frozen hash checks passed.

## LLM assessor results

| Run | Variant | Exact | Acceptable | Unsafe false clearances |
|---|---|---|---|---|
| run1 | SYN-003 | 3/5 | 4/5 | 1 |
| run1 | SYN-003-control | 3/5 | 4/5 | 1 |
| run2 | SYN-003 | 4/5 | 5/5 | 0 |
| run2 | SYN-003-control | 3/5 | 4/5 | 1 |
| run3 | SYN-003 | 4/5 | 5/5 | 0 |
| run3 | SYN-003-control | 3/5 | 4/5 | 1 |

Combined repeated assessments: **20/30 exact**, **26/30 acceptable**, **4 unsafe false clearances**. These are repeated assessments of ten labeled patient-criterion pairs, not 30 independent cases. UNKNOWN was predeclared acceptable for the two washout labels.

## All LLM assessor predictions

| Run | Variant | Trial | Criterion | Expected | Predicted | Acceptable |
|---|---|---|---|---|---|---|
| run1 | SYN-003 | NCT07559760 | EXC-19 | DOES_NOT_MEET | MEETS | False |
| run1 | SYN-003 | NCT06412198 | EXC-01 | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run1 | SYN-003 | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run1 | SYN-003 | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run1 | SYN-003 | NCT07559760 | INC-02 | MEETS | MEETS | True |
| run1 | SYN-003-control | NCT07559760 | EXC-19 | UNKNOWN | MEETS | False |
| run1 | SYN-003-control | NCT06412198 | EXC-01 | UNKNOWN | UNKNOWN | True |
| run1 | SYN-003-control | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run1 | SYN-003-control | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run1 | SYN-003-control | NCT07559760 | INC-02 | MEETS | MEETS | True |
| run2 | SYN-003 | NCT07559760 | EXC-19 | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run2 | SYN-003 | NCT06412198 | EXC-01 | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run2 | SYN-003 | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run2 | SYN-003 | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run2 | SYN-003 | NCT07559760 | INC-02 | MEETS | MEETS | True |
| run2 | SYN-003-control | NCT07559760 | EXC-19 | UNKNOWN | MEETS | False |
| run2 | SYN-003-control | NCT06412198 | EXC-01 | UNKNOWN | UNKNOWN | True |
| run2 | SYN-003-control | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run2 | SYN-003-control | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run2 | SYN-003-control | NCT07559760 | INC-02 | MEETS | MEETS | True |
| run3 | SYN-003 | NCT07559760 | EXC-19 | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run3 | SYN-003 | NCT06412198 | EXC-01 | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run3 | SYN-003 | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run3 | SYN-003 | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run3 | SYN-003 | NCT07559760 | INC-02 | MEETS | MEETS | True |
| run3 | SYN-003-control | NCT07559760 | EXC-19 | UNKNOWN | MEETS | False |
| run3 | SYN-003-control | NCT06412198 | EXC-01 | UNKNOWN | UNKNOWN | True |
| run3 | SYN-003-control | NCT07559760 | EXC-05 | DOES_NOT_MEET | UNKNOWN | True |
| run3 | SYN-003-control | NCT06412198 | INC-02 | MEETS | MEETS | True |
| run3 | SYN-003-control | NCT07559760 | INC-02 | MEETS | MEETS | True |

## Findings

- The malignancy exclusion (NCT07559760 EXC-19) was incorrectly cleared (MEETS) for the control patient in all three runs; the signed-off label is UNKNOWN. It was also incorrectly cleared for the buried-lymphoma patient in run1; that label is DOES_NOT_MEET. These account for all four unsafe false clearances.
- The buried-lymphoma exclusion was correctly detected in run2 and run3, showing variability with the same frozen implementation and inputs.
- The PD-1 therapy and both diagnosis/biomarker sanity criteria matched their labels in every run for both variants.
- Washout remained UNKNOWN for both variants in every run. This is acceptable under the predeclared labels, but does not demonstrate successful use of the two dates to decide the 12-day interval.
- The SYN-002 fixes therefore do not establish reliable generalization to SYN-003. No fixes were attempted in response to these results.

## Rule baseline

| Run | Variant | Exact accuracy | Acceptable rate | Unsafe false clearances |
|---|---|---|---|---|
| run1 | SYN-003 | 0.4 | 0.6 | 0 |
| run1 | SYN-003-control | 0.8 | 1.0 | 0 |
| run2 | SYN-003 | 0.4 | 0.6 | 0 |
| run2 | SYN-003-control | 0.8 | 1.0 | 0 |
| run3 | SYN-003 | 0.4 | 0.6 | 0 |
| run3 | SYN-003-control | 0.8 | 1.0 | 0 |
