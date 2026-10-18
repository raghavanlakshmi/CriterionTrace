# SYN-002 results: after fixes, not blind

These are three fresh extraction and assessment runs on the final fixes, using gpt-4.1-mini. No --reuse-evidence was used. Labels, synthetic documents, blind run folders, and the blind-results document were unchanged (see protected_manifest_before.json and validation.json). No new patient or trial data was added.

The original results were already reviewed before these fixes. The previously held-out SYN-001 set is also no longer blind. The original first-run sign-off was in chat; its later Git commit does not establish pre-run label freezing.

| Run | Variant | Exact | Acceptable | Unsafe clearances | Buried exclusions |
|---|---|---|---|---|---|
| run1 | SYN-002 | 6/7 | 6/7 | 0 | UNKNOWN, DOES_NOT_MEET, DOES_NOT_MEET |
| run1 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run2 | SYN-002 | 7/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run2 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run3 | SYN-002 | 7/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run3 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |

Exact metrics count the predefined washout alternative DOES_NOT_MEET as a mismatch against primary UNKNOWN. Acceptable metrics allow that alternative; sound reasoning must be reviewed separately.

## Extraction coverage

| Run | Variant | Verified lab analytes | BRAF | Biopsy | Dated administration | Uncovered lines |
|---|---|---|---|---|---|---|
| run1 | SYN-002 | 7/7 | yes | yes | yes | 15 |
| run1 | SYN-002-control | 7/7 | yes | yes | yes | 17 |
| run2 | SYN-002 | 7/7 | yes | yes | yes | 19 |
| run2 | SYN-002-control | 7/7 | yes | yes | yes | 17 |
| run3 | SYN-002 | 7/7 | yes | yes | yes | 15 |
| run3 | SYN-002-control | 7/7 | yes | yes | yes | 17 |

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

- **run1, SYN-002, NCT07559760 EXC-19**: expected DOES_NOT_MEET, got UNKNOWN. No cited evidence addresses this exclusion; absence of a record does not clear it. Converted to UNKNOWN. Original reasoning: The patient has a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022, which is more than 5 years ago (current evidence dated 2026). No evidence of other malignancies within the past 5 years is documented. There is no mention of basal-cell carcinoma of skin or cervical carcinoma in situ. Thus, the exclusion criterion of other malignancies within 5 years does not apply.

Compared with the blind runs: buried-malignancy flags matched the expected DOES_NOT_MEET in 2/3 final runs, versus 2/3 originally. Final unsafe clearances: 0, versus zero originally. More extracted facts do not establish a correct criterion decision. The quoted miss explanations above and their guard flags must be reviewed.

Earlier attempts exposed unsupported recovery values (including sex inferred from family-history text and UNKNOWN placeholders), missing biopsy evidence, and unsafe prior-malignancy clearances. Both attempted batches and their original outputs are retained in ../syn002_initial_fix_attempt/ and ../syn002_fix_attempt_2/. The final code adds deterministic explicit clinical fields, rejects those placeholders and unsupported sex values, and uses the same normalization for generic support terms as for cited terms. These are general rules, not patient/trial/drug exceptions.

The final coverage audit includes any remaining placeholder/scalar-support anomalies and family-history citations for manual inspection. Quote verification checks literal presence, not clinical semantics. Broad verified quotes can overstate completeness, and an empty gap list is not proof that all facts were correctly represented.

Medication-history explanations were also checked for claims of current use; the raw explanations and dated source provenance are retained in the JSON reports.

## Validation and scope

- Full offline suite: **192 passed before; 227 passed after**. The expanded extraction checklist is separate from the prepared demo review keys, preserving the existing review layout.
- Four implementation commits, one per fix; the reporting artifacts are committed separately.
- Both earlier implementation attempts are preserved separately and are not part of the final three-run table. The three final runs used one unchanged implementation revision (validation.json).
- No retrieval, trial-data, patient, label, or blind-result changes. No SYN-003 was created.
- The test scores fixed criteria rather than app retrieval, ranked candidates, or clinical validity.
- Safety flags and persistent extraction gaps remain visible for human verification. Synthetic data only; not clinical validation.
