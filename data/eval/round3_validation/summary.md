# Round-three validation results

**After round-3 fixes, not blind. Two implementation attempts used; no third tuning attempt.** SYN-004 is now a development case. SYN-005 was not created, read or run.

Frozen implementation: `6da940d49021855cc3d03a26ece5efa001e60c5c` (`round3-frozen`). The eight fixes have separate commits. The final results commit adds artifacts only. `main` remains unchanged; review branch is `round3-fixes`. Every final run used gpt-4.1-mini, unchanged labels and fresh extraction; SYN-004 also used fresh vision OCR.

## Offline verification and protected inputs

**271 before; 315 after; all tests pass.** The history-scope tests retain their expected outcomes. Older fixture scaffolding now declares clearance bases and selected event indices. Three older topic-overlap clearances (wild-type/stable biomarker wording and an age fact) now expect UNKNOWN for model answers without a stated negative basis, as required by Fix A. The existing cited-treatment inference test now supplies an explicit category in its quote. Typed inclusion/exclusion output schemas prevent wrong-vocabulary fallbacks; the existing deterministic comparator preserves conflicting verified values instead of letting the model prefer one source.

All labels, patient documents, trial data, saved SYN-001 evidence, original run folders and earlier results documents match their protected hashes. No retrieval or UI-layout change was made. Compound parts and flags are visible in explanations and the new reports' `assessment_details`.

## Patient scores across all three runs

| Dataset | Stage | Exact | Acceptable | Unsafe clearances | False exclusions |
|---|---|---|---|---|---|
| SYN-002 | Prior recorded runs | 39/42 | 39/42 | 0 | 0 |
| SYN-002 | Attempt 1 (preserved) | 29/42 | 29/42 | 0 | 0 |
| SYN-002 | Final attempt 2 | 39/42 | 39/42 | 0 | 0 |
| SYN-003 | Prior recorded runs | 28/30 | 28/30 | 0 | 0 |
| SYN-003 | Attempt 1 (preserved) | 18/30 | 21/30 | 3 | 0 |
| SYN-003 | Final attempt 2 | 28/30 | 29/30 | 0 | 1 |
| SYN-004 | Prior recorded runs | 24/42 | 33/42 | 5 | 1 |
| SYN-004 | Attempt 1 (preserved) | 33/42 | 39/42 | 0 | 0 |
| SYN-004 | Final attempt 2 | 31/42 | 40/42 | 0 | 1 |

These are repeated assessments of fixed patient-criterion pairs, not independent patients. The prior SYN-004 batch was blind; both round-three batches are development results. Different patients and criterion sets prevent a controlled across-patient performance comparison.

| Dataset | Run | Variant | Exact | Acceptable | Unsafe | False exclusions |
|---|---|---|---|---|---|---|
| SYN-002 | run1 | SYN-002-control | 7/7 | 7/7 | 0 | 0 |
| SYN-002 | run1 | SYN-002 | 6/7 | 6/7 | 0 | 0 |
| SYN-002 | run2 | SYN-002-control | 7/7 | 7/7 | 0 | 0 |
| SYN-002 | run2 | SYN-002 | 6/7 | 6/7 | 0 | 0 |
| SYN-002 | run3 | SYN-002-control | 7/7 | 7/7 | 0 | 0 |
| SYN-002 | run3 | SYN-002 | 6/7 | 6/7 | 0 | 0 |
| SYN-003 | run1 | SYN-003-control | 5/5 | 5/5 | 0 | 0 |
| SYN-003 | run1 | SYN-003 | 4/5 | 5/5 | 0 | 0 |
| SYN-003 | run2 | SYN-003-control | 5/5 | 5/5 | 0 | 0 |
| SYN-003 | run2 | SYN-003 | 5/5 | 5/5 | 0 | 0 |
| SYN-003 | run3 | SYN-003-control | 4/5 | 4/5 | 0 | 1 |
| SYN-003 | run3 | SYN-003 | 5/5 | 5/5 | 0 | 0 |
| SYN-004 | run1 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |
| SYN-004 | run1 | SYN-004 | 4/7 | 6/7 | 0 | 1 |
| SYN-004 | run2 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |
| SYN-004 | run2 | SYN-004 | 5/7 | 7/7 | 0 | 0 |
| SYN-004 | run3 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |
| SYN-004 | run3 | SYN-004 | 4/7 | 6/7 | 0 | 0 |

## SYN-001 regression and every changed prediction

| Set | Prior round two | Attempt 1 | Final attempt 2 | Unsafe prior / attempt 1 / final |
|---|---|---|---|---|
| in_sample | 28/29 | 22/29 | 27/29 | 0 / 3 / 0 |
| held_out | 21/21 | 13/21 | 17/21 | 0 / 1 / 0 |

Every changed final SYN-001 prediction, including MEETS to UNKNOWN, is listed here. All methods and all first-attempt changes are also in `prediction_changes.md` and `prediction_changes.json`.

| Set | Method | Trial | Criterion | Expected | Prior | Final | Flags / reason |
|---|---|---|---|---|---|---|
| SYN-001/in_sample | rule_baseline | NCT06252649 | INC-04 | POTENTIAL_CONFLICT | POTENTIAL_CONFLICT | MEETS | Explicit verified evidence matches the central condition or biomarker wording; human verification is required. |
| SYN-001/in_sample | llm_assessor | NCT07559760 | INC-01 | MEETS | MEETS | UNKNOWN | INC-01: Date-comparison guard: explanation contains an incorrect date comparison. Converted to UNKNOWN. |
| SYN-001/held_out | llm_assessor | NCT05854498 | INC-04 | MEETS | MEETS | UNKNOWN | INC-04: Unsupported category-inference guard: hedged category link has no verified quote stating mismatch, proficiency, repair. Converted to UNKNOWN. |
| SYN-001/held_out | llm_assessor | NCT05854498 | EXC-02 | MEETS | MEETS | UNKNOWN | EXC-02: Exclusion clearance guard: no negative evidence cited; absence-based clearance without evidence about it. Converted to UNKNOWN. |
| SYN-001/held_out | llm_assessor | NCT05854498 | EXC-04 | MEETS | MEETS | UNKNOWN | EXC-04: Exclusion clearance guard: no negative evidence cited; absence-based clearance without evidence about it. Converted to UNKNOWN. |
| SYN-001/held_out | llm_assessor | NCT07281716 | INC-01 | MEETS | MEETS | UNKNOWN | INC-01: Unsupported category-inference guard: hedged category link has no verified quote stating pmmr. Converted to UNKNOWN. |

Do not attribute every score change to a guard: extraction and model answers vary between fresh runs. Flags and explanations distinguish observed guard downgrades from other model/extraction changes. The first attempt's performance-status unsafe clearances are retained. The second revision constrains response vocabularies and preserves the existing deterministic conflict comparator's differing-value result.

## Brain MRI: legitimate-negative check, separate from total scores

| Run | Variant | Prior blind | Attempt 1 | Final | Final clearance basis | Final flags |
|---|---|---|---|---|---|---|
| run1 | SYN-004-control | UNKNOWN | UNKNOWN | UNKNOWN | absence | EXC-01: unsupported conclusion converted to UNKNOWN. EXC-01: Exclusion clearance guard: cleared from absence. Converted to UNKNOWN. |
| run1 | SYN-004 | UNKNOWN | UNKNOWN | UNKNOWN | absence | EXC-01: unsupported conclusion converted to UNKNOWN. EXC-01: Exclusion clearance guard: cleared from absence. Converted to UNKNOWN. |
| run2 | SYN-004-control | UNKNOWN | UNKNOWN | UNKNOWN | absence | EXC-01: unsupported conclusion converted to UNKNOWN. EXC-01: Exclusion clearance guard: cleared from absence. Converted to UNKNOWN. |
| run2 | SYN-004 | UNKNOWN | UNKNOWN | UNKNOWN | explicit_negative | EXC-01: Exclusion clearance guard: no negative evidence cited; absence-based clearance without evidence about it. Converted to UNKNOWN. |
| run3 | SYN-004-control | UNKNOWN | UNKNOWN | UNKNOWN | absence | EXC-01: Exclusion clearance guard: cleared from absence. Converted to UNKNOWN. |
| run3 | SYN-004 | UNKNOWN | UNKNOWN | UNKNOWN | absence | EXC-01: unsupported conclusion converted to UNKNOWN. EXC-01: Exclusion clearance guard: cleared from absence. Converted to UNKNOWN. |

Final pipeline MRI clearances: **0/6**. A separate controlled guard-only audit supplied the exact MRI source sentence, verified by the existing quote verifier, with explicit_negative basis. That audit returned **MEETS**, with flags []. It is **not** a live extraction result or a scored case. This separates guard capability from the remaining extraction/citation/model gap; it does not establish that the pipeline reliably clears a supported negative.

## Guard interventions

Counts are assessment rows bearing a guard at least once, including child-part flags; multiple guards can occur on one row. Counts use the LLM-assessor pipeline, not the rule baseline.

| Guard | SYN-002 | SYN-003 | SYN-004 |
|---|---|---|---|
| Clearance basis / verified negative | 6 | 5 | 21 |
| History scope | 5 | 3 | 3 |
| Narrower scope | 0 | 3 | 0 |
| Code-computed window | 6 | 6 | 12 |
| Compound parts | 12 | 13 | 13 |
| Date comparisons | 1 | 0 | 6 |
| Unsupported category inference | 4 | 0 | 1 |
| Status / explanation contradiction | 0 | 1 | 0 |
| Legacy missing study reference | 0 | 0 | 0 |
| Conflict preservation | 0 | 0 | 0 |
| No patient citation | 4 | 0 | 10 |
| Unverified quote | 0 | 0 | 0 |
| Partial inclusion support | 0 | 0 | 0 |
| Investigator judgment | 0 | 0 | 0 |

## Dated events and treatment courses

| Run | Variant | TIA label | TIA result | 133-day computation visible | Steroid result | Course endpoints in verified records |
|---|---|---|---|---|---|---|
| run1 | SYN-004-control | UNKNOWN | UNKNOWN | False | UNKNOWN | None to 2026-05-12; 2026-06-22 to None; 2026-06-14 to 2026-06-18 |
| run1 | SYN-004 | DOES_NOT_MEET | DOES_NOT_MEET | False | UNKNOWN | 2026-05-12 to 2026-05-12; 2025-04 to 2025-04; 2026-06-22 to 2026-06-22; 2026-06-14 to 2026-06-18; 2025-04 to 2025-04 |
| run2 | SYN-004-control | UNKNOWN | UNKNOWN | False | UNKNOWN | None to 2026-05-12; 2026-06-14 to 2026-06-18; 2026-06-22 to None; 2026-06-14 to 2026-06-18 |
| run2 | SYN-004 | DOES_NOT_MEET | DOES_NOT_MEET | True | UNKNOWN | None to 2025-04; 2026-06-14 to 2026-06-18; None to 2026-05-12; None to 2026-05-12 |
| run3 | SYN-004-control | UNKNOWN | UNKNOWN | False | UNKNOWN | 2026-05-12 to None; 2026-06-22 to None; 2026-06-14 to 2026-06-18; 2026-06-14 to 2026-06-18; None to 2025-04-15 |
| run3 | SYN-004 | DOES_NOT_MEET | UNKNOWN | False | UNKNOWN | 2026-06-22 to None; 2026-06-14 to 2026-06-18; 2025-03 to 2025-03; None to 2025-04 |

The model chooses the event index; code validates that it is a cited verified fact and computes calendar intervals. No event is selected by drug/diagnosis keywords in the calculator. Endpoints are used at source precision. Outside-window, missing-date and ambiguous-month outcomes are UNKNOWN. Compound explanations retain non-window parts. See `temporal_audit.json` and each report's `assessment_details` for selections, sources, part decisions and explanations.

## Extraction-gap audit (Fix H)

Original SYN-004 runs 2 and 3 both list ?Assessment: transient ischemic attack on 2026-02-09.? for manual review. The existing algorithm requires the affected neurology-page retry, and a fake-extractor replay confirms that trigger while preserving the missing sentence. Original runs did not save per-pass API trace, so no claim is made that a successful retry response was captured. No extraction-gap algorithm change was warranted. The new regression test ensures another fact from the page cannot hide a skipped diagnosis sentence.

## Remaining misses and anything worse

- SYN-002: prior 39/42 exact, 39/42 acceptable, 0 unsafe, 0 false exclusions; final 39/42 exact, 39/42 acceptable, 0 unsafe, 0 false exclusions.
- SYN-003: prior 28/30 exact, 28/30 acceptable, 0 unsafe, 0 false exclusions; final 28/30 exact, 29/30 acceptable, 0 unsafe, 1 false exclusions.
- SYN-004: prior 24/42 exact, 33/42 acceptable, 5 unsafe, 1 false exclusions; final 31/42 exact, 40/42 acceptable, 0 unsafe, 1 false exclusions.
- run1 SYN-002 NCT07559760 EXC-19: expected DOES_NOT_MEET, predicted UNKNOWN. EXC-19: History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN. EXC-19: Compound criterion guard: combined UNKNOWN, UNKNOWN => UNKNOWN.
- run2 SYN-002 NCT07559760 EXC-19: expected DOES_NOT_MEET, predicted UNKNOWN. EXC-19: Time-window decision lacks dated cited evidence. Converted to UNKNOWN. EXC-19: History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN. EXC-19: Date-comparison guard: source date precision cannot verify the explanation's comparison. Converted to UNKNOWN. EXC-19: Date-comparison guard: source date precision cannot verify the explanation's comparison. Converted to UNKNOWN. EXC-19: Date-comparison guard: source date precision cannot verify the explanation's comparison. Converted to UNKNOWN. EXC-19: Compound criterion guard: combined UNKNOWN, UNKNOWN => UNKNOWN.
- run3 SYN-002 NCT06412198 INC-01: expected MEETS, predicted UNKNOWN. INC-01: Unsupported category-inference guard: hedged category link has no verified quote stating advance. Converted to UNKNOWN.
- run3 SYN-003-control NCT07559760 EXC-19: expected UNKNOWN, predicted DOES_NOT_MEET. EXC-19/part1: History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN. EXC-19: Compound criterion guard: combined UNKNOWN, DOES_NOT_MEET => DOES_NOT_MEET.
- run1 SYN-004 NCT06412198 EXC-04: expected UNKNOWN, predicted DOES_NOT_MEET. No guard flag; see model reasoning in report.
- run3 SYN-004 NCT07559760 EXC-08: expected DOES_NOT_MEET, predicted UNKNOWN. EXC-08: Computed time-window guard: selected event has no verified event date in its quote. EXC-08: Compound criterion guard: combined UNKNOWN, UNKNOWN => UNKNOWN.

SYN-001 lost exact matches relative to round two; both its decreases and any unsafe outcomes are shown above. Brain-MRI UNKNOWN results are acceptable under the original labels but are not successful clearances. The first attempt and all worsening predictions are retained. No third tuning attempt was made. These development results do not establish generalization or clinical validation.

## Rule baseline

| Dataset | Exact | Acceptable | Unsafe | False exclusions |
|---|---|---|---|---|
| SYN-002 | 27/42 | 27/42 | 0 | 0 |
| SYN-003 | 18/30 | 24/30 | 0 | 0 |
| SYN-004 | 27/42 | 36/42 | 0 | 0 |

## Acceptance checks not fully met in live runs

- The offline event/course examples pass, but the final SYN-004 systemic-steroid result is UNKNOWN in all three buried runs. Verified course records do carry 2026-06-14 and 2026-06-18; selecting and applying the correct compound window remains unreliable. This is acceptable under the old labels, but does not satisfy the requested successful 4-day course decision.
- TIA is DOES_NOT_MEET twice and UNKNOWN once. Only run2 visibly reports the code-computed 133-day interval; run1 reaches DOES_NOT_MEET without that calculation, and run3 has an invalid/missing selected date. Thus the requested live calculation is not consistently demonstrated. Model-provided part wording can fail to preserve enough temporal context for the calculator.
- One SYN-003 control cancer exclusion and one SYN-004 autoimmune exclusion are false exclusions. Zero unsafe clearances does not imply all exclusions are correct.
- The brain-MRI pipeline clears 0/6 despite a guard-only exact-source negative being accepted. This remains an end-to-end gap.
- Some correct SYN-001 results become UNKNOWN under strict negative-evidence or category-inference rules. Every changed prediction is retained, including those losses.

These are unresolved limitations at the two-attempt cutoff, not a claim that every live done-when condition passed. No third attempt was made. Any further fix requires a later development round; the current code is frozen unchanged.

## Reproducibility and next blind test

- First attempt implementation: `3930c5f`; full outputs in `data/eval/round3_attempt1/`, retained by tag `round3-attempt1`. Run manifests preserve their original paths before archival.
- Final implementation: `6da940d49021855cc3d03a26ece5efa001e60c5c`; tag `round3-frozen`. SYN-005 should start from that commit. The final output commit does not change implementation files.
- Final outputs: `data/eval/syn002_runs_round3/run1..3`, `syn003_runs_round3/run1..3`, `syn004_runs_round3/run1..3`. Both SYN-001 regressions are under `round3_validation/syn001/`.
- Each process exited successfully and verified frozen code/protected hashes. Labels and previous results were not edited. All SYN-004 after-fix results remain separate from its original blind runs.
