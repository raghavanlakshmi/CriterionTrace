# SYN-002 results: after fixes, not blind

These are three fresh extraction and assessment runs on the final fixes, using gpt-4.1-mini. No --reuse-evidence was used. Labels, synthetic documents, blind run folders, and the blind-results document were unchanged (see protected_manifest_before.json and validation.json). No new patient or trial data was added.

The original results were already reviewed before these fixes. The previously held-out SYN-001 set is also no longer blind. The original first-run sign-off was in chat; its later Git commit does not establish pre-run label freezing.

| Run | Variant | Exact | Acceptable | Unsafe clearances | Buried exclusions |
|---|---|---|---|---|---|
| run1 | SYN-002 | 6/7 | 6/7 | 1 | MEETS, DOES_NOT_MEET, DOES_NOT_MEET |
| run1 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run2 | SYN-002 | 6/7 | 6/7 | 1 | MEETS, DOES_NOT_MEET, DOES_NOT_MEET |
| run2 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run3 | SYN-002 | 6/7 | 6/7 | 1 | MEETS, DOES_NOT_MEET, DOES_NOT_MEET |
| run3 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |

Exact metrics count the predefined washout alternative DOES_NOT_MEET as a mismatch against primary UNKNOWN. Acceptable metrics allow that alternative; sound reasoning must be reviewed separately.

## Extraction coverage

| Run | Variant | Verified lab analytes | BRAF | Biopsy | Dated administration | Uncovered lines |
|---|---|---|---|---|---|---|
| run1 | SYN-002 | 7/7 | yes | no | yes | 13 |
| run1 | SYN-002-control | 7/7 | yes | no | yes | 13 |
| run2 | SYN-002 | 7/7 | yes | no | yes | 15 |
| run2 | SYN-002-control | 7/7 | yes | yes | yes | 9 |
| run3 | SYN-002 | 7/7 | yes | no | yes | 17 |
| run3 | SYN-002-control | 7/7 | yes | no | yes | 9 |

Coverage is literal verified quote coverage, not proof that every interpretation is correct. Persistent uncovered lines, including family history that should not become a patient condition, are listed in each report for manual review. Unverified records remain visible in evidence outputs but cannot be model citation candidates.

## SYN-001 regression evaluations

| Set | Before exact | After exact | Before unsafe clearances | After unsafe clearances |
|---|---|---|---|---|
| in_sample | 28/29 | 28/29 | 0 | 0 |
| held_out | 20/21 | 21/21 | 0 | 0 |

Before comparators: the saved in-sample criterion_eval_report.json and the later held-out criterion_eval_report_heldout_postfix.json, copied into syn001/*/before_report.json. These regressions replay the saved SYN-001 evidence; they do not test fresh SYN-001 extraction. Model sampling also contributes to any score difference.

Changed predictions:
- held_out, llm_assessor, NCT06244771 INC-04: POTENTIAL_CONFLICT -> UNKNOWN (expected UNKNOWN).

## Misses and regressions

- **run1, SYN-002, NCT07559760 EXC-19**: expected DOES_NOT_MEET, got MEETS. The patient has a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022, with undetectable PSA at last check. This is the only other malignancy reported within the last 5 years. Since prostate adenocarcinoma treated over 4 years ago with no active disease is not listed as an exclusion, and basal-cell carcinoma or cervical carcinoma in situ are excepted, the exclusion does not apply. There is no evidence of any other malignancies within 5 years.
- **run2, SYN-002, NCT07559760 EXC-19**: expected DOES_NOT_MEET, got MEETS. The patient had a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022, which is more than 5 years before the current date evidence (2026-03-30). No other malignancies within 5 years are documented. Therefore, the exclusion for 'Other malignancies within 5 years' does not apply.
- **run3, SYN-002, NCT07559760 EXC-19**: expected DOES_NOT_MEET, got MEETS. The patient has a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022, which is within the last 5 years. However, this criterion excludes other malignancies within 5 years except basal-cell carcinoma of the skin or cervical carcinoma in situ. Prostate adenocarcinoma treated with surgery is a malignancy, but the exclusion does not specify prostate cancer as an exception. Despite this, the criterion intends to exclude active or recent malignancies other than the specified exceptions. There is no evidence of any other malignancy within 5 years besides prostate cancer, and no evidence that the prostate cancer is currently active or untreated, suggesting it is adequately treated. Therefore, this exclusion does not apply given the information provided.

Additional extraction regressions: some recovered records pair a literal source quote with an unsupported value. In run1 control, a sex=Male record cites only family-history lines. Some records have value=UNKNOWN and quote most of a page. Quote verification checks literal presence, not whether the quote supports that value. An overbroad verified quote can also make line coverage appear complete. These records are retained for review in coverage_audit.json; the completeness check does not solve semantic evidence validation.

Compared with the blind runs: the buried-malignancy probe changed from two correct flags and one UNKNOWN to three unsafe MEETS clearances. Unsafe false clearances increased from zero to three. This is a worse safety outcome even though more source facts were captured. Drug-exposure and control probes remained correct. Do not describe this batch as a successful overall safety fix.

Medication-history explanations were also checked for claims of current use; the raw explanations and dated source provenance are retained in the JSON reports.

## Validation and scope

- Full offline suite: **192 passed before; 222 passed after**. The expanded extraction checklist is separate from the prepared demo review keys, preserving the existing review layout.
- Four implementation commits, one per fix; the reporting artifacts are committed separately.
- The initial implementation attempt is preserved separately in ../syn002_initial_fix_attempt/. It exposed a study-anchor spelling gap and mixed verified/unverified citation behavior; it is not part of the final three-run table.
- No retrieval, trial-data, patient, label, or blind-result changes. No SYN-003 was created.
- The test scores fixed criteria rather than app retrieval, ranked candidates, or clinical validity.
- Safety flags and persistent extraction gaps remain visible for human verification. Synthetic data only; not clinical validation.
