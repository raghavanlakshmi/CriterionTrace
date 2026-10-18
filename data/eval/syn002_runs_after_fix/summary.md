# SYN-002 results: after fixes, not blind

These are three fresh extraction and assessment runs on the final fixes, using gpt-4.1-mini. No --reuse-evidence was used. Labels, synthetic documents, blind run folders, and the blind-results document were unchanged (see protected_manifest_before.json and validation.json). No new patient or trial data was added.

The original results were already reviewed before these fixes. The previously held-out SYN-001 set is also no longer blind. The original first-run sign-off was in chat; its later Git commit does not establish pre-run label freezing.

| Run | Variant | Exact | Acceptable | Unsafe clearances | Buried exclusions |
|---|---|---|---|---|---|
| run1 | SYN-002 | 7/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run1 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run2 | SYN-002 | 6/7 | 6/7 | 0 | UNKNOWN, DOES_NOT_MEET, DOES_NOT_MEET |
| run2 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run3 | SYN-002 | 7/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run3 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |

Exact metrics count the predefined washout alternative DOES_NOT_MEET as a mismatch against primary UNKNOWN. Acceptable metrics allow that alternative; sound reasoning must be reviewed separately.

## Extraction coverage

| Run | Variant | Verified lab analytes | BRAF | Biopsy | Dated administration | Uncovered lines |
|---|---|---|---|---|---|---|
| run1 | SYN-002 | 7/7 | yes | yes | yes | 17 |
| run1 | SYN-002-control | 7/7 | yes | yes | yes | 17 |
| run2 | SYN-002 | 7/7 | yes | yes | yes | 15 |
| run2 | SYN-002-control | 7/7 | yes | yes | yes | 17 |
| run3 | SYN-002 | 7/7 | yes | yes | yes | 17 |
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

- **run2, SYN-002, NCT07559760 EXC-19**: expected DOES_NOT_MEET, got UNKNOWN. No cited evidence addresses this exclusion; absence of a record does not clear it. Converted to UNKNOWN. Original reasoning: The patient has a history of prostate adenocarcinoma treated with radical prostatectomy in March 2022 and has an undetectable PSA at last check. This malignancy was treated more than 5 years ago (current evidence is from 2026, and prostate cancer treatment was in 2022, which is about 4 years ago), so it is within 5 years. However, the criterion excludes other malignancies within 5 years except adequately treated basal-cell carcinoma of skin or cervical carcinoma in situ. Prostate adenocarcinoma is not an exclusion for this criterion assuming it's adequately treated and no active disease, but this is uncertain due to timeline and lack of explicit statement of adequate treatment or remission. There is no evidence of other malignancies within 5 years apart from this, and prostate cancer was treated with surgery and PSA is undetectable. Because the prostate cancer is the only malignancy noted recently and treated surgically, and no active malignancy or new malignancy within 5 years is documented, the exclusion does not apply based on available evidence.

Compared with the blind runs: buried-malignancy flags matched the expected DOES_NOT_MEET in 2/3 final runs, versus 2/3 originally. Final unsafe clearances: 0, versus zero originally. More extracted facts do not establish a correct criterion decision. The quoted miss explanations above and their guard flags must be reviewed.

Earlier attempts exposed unsupported recovery values (including sex inferred from family-history text and UNKNOWN placeholders), missing biopsy evidence, unsafe prior-malignancy clearances, and incorrect current-use wording. All three attempted batches and their original outputs are retained in ../syn002_initial_fix_attempt/, ../syn002_fix_attempt_2/, and ../syn002_fix_attempt_3/. The final code adds deterministic explicit clinical fields, rejects those placeholders and unsupported sex values, uses the same normalization for generic support terms as for cited terms, and corrects unsupported snapshot wording with a visible flag. These are general rules, not patient/trial/drug exceptions.

The final coverage audit includes any remaining placeholder/scalar-support anomalies and family-history citations for manual inspection. Quote verification checks literal presence, not clinical semantics. Broad verified quotes can overstate completeness, and an empty gap list is not proof that all facts were correctly represented.

Medication-history explanations were also checked for claims of current use; the raw explanations and dated source provenance are retained in the JSON reports.

## Validation and scope

- Full offline suite: **192 passed before; 232 passed after**. The expanded extraction checklist is separate from the prepared demo review keys, preserving the existing review layout.
- Four implementation commits, one per fix; the reporting artifacts are committed separately.
- All earlier implementation attempts are preserved separately and are not part of the final three-run table. The three final runs used one unchanged implementation revision (validation.json).
- No retrieval, trial-data, patient, label, or blind-result changes. No SYN-003 was created.
- The test scores fixed criteria rather than app retrieval, ranked candidates, or clinical validity.
- Safety flags and persistent extraction gaps remain visible for human verification. Synthetic data only; not clinical validation.


## Final audit details

- Final LLM totals: **41/42 exact and accepted**, versus **38/42 exact and 41/42 accepted** in the original three runs. Final unsafe clearances: **0**.
- Verified treatment-administration evidence, all seven lab analytes, BRAF, and biopsy were captured in all six evaluations. No family-history patient records, UNKNOWN placeholders, or scalar-support anomalies were found by the final audit.
- No current-use wording remained in the final drug-exposure explanations. The deterministic snapshot wording guard intervened twice; corrections are flagged in the JSON reports. These are reviewed outputs, not a claim that the raw model always followed the prompt.
- Washout was UNKNOWN in all six final evaluations. Prior drug exposure was flagged in all three buried variants; all corresponding control probes stayed UNKNOWN.
- The remaining run2 malignancy miss is an **assessment/guard** issue, not an extraction miss: verified evidence was present. The assessor made incorrect date and exception assumptions; the general clearance guard downgraded that unsafe answer to UNKNOWN.
- SYN-002 rule-baseline accuracy was unchanged: 3/7 for each buried variant and 6/7 for each control. Its conservatism remains expected. All SYN-001 rule-baseline predictions were unchanged.
- No final unsafe-clearance regression was observed. Earlier attempts did get worse, including three unsafe malignancy clearances in attempt 2; all attempted outputs remain preserved separately. Final malignancy sensitivity remains 2/3, the same as the original three runs, so that failure is not claimed solved.
- The line-coverage check still lists 15-17 lines per evaluation for manual review, including intentionally unextracted family-history material and other uncovered text. This is not complete semantic extraction.

For future runs, use a new destination to preserve this record:

```bash
python scripts/run_buried_exclusion_test.py --output-dir data/eval/syn002_runs_after_fix/run4
```

The raw SHA-256 manifest records evaluation-checkout bytes; text hashes can differ across checkouts because of line endings. protected_git_blobs.json records checkout-independent Git blob IDs, verified identical to base commit dc41e5c for all protected artifacts.
