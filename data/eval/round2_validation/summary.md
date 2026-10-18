# Round-two validation results

**After round-2 fixes, not blind.** Two implementation attempts were made against SYN-002/SYN-003; all attempts are retained. No third tuning attempt was made. No new patient was created.

Frozen implementation commit: `caa440b3a324428f7fdb2dc62468ad0a311667a4` (`round2-frozen`). The four fixes are separate commits. The final results commit adds artifacts only; use the recorded implementation commit for SYN-004. All runs used gpt-4.1-mini for extraction/assessment, fresh patient extraction, unchanged signed-off labels and trial data. The broad therapy time-window path is deterministic and bypasses the LLM; its results remain in the existing runner's `llm_assessor` pipeline column.

## Offline tests

**232 before; 271 after**, all passing. New coverage tests exercise history scope and exceptions, conclusion consistency and negation, actual/planned date arithmetic, event-date metadata, wrapped sentences, headings and exact source context. Existing completeness fixtures now use sentence punctuation; the older temporal test also checks the newly required arithmetic flag.

## Three-run patient scores

| Dataset | Stage | Exact | Acceptable | Unsafe false clearances |
|---|---|---|---|---|
| SYN-002 | Prior recorded runs | 41/42 | 41/42 | 0 |
| SYN-002 | Attempt 1 (preserved) | 42/42 | 42/42 | 0 |
| SYN-002 | Final attempt 2 | 39/42 | 39/42 | 0 |
| SYN-003 | Prior recorded runs | 20/30 | 26/30 | 4 |
| SYN-003 | Attempt 1 (preserved) | 23/30 | 28/30 | 0 |
| SYN-003 | Final attempt 2 | 28/30 | 28/30 | 0 |

These are repeated assessments of the same labeled pairs, not independent patients. SYN-003 was blind only for the original frozen-round-one evaluation; both round-two batches are development evaluations. UNKNOWN allowances are those declared in the original labels.

| Dataset | Run | Variant | Exact | Acceptable | Unsafe |
|---|---|---|---|---|---|
| SYN-002 | run1 | SYN-002-control | 7/7 | 7/7 | 0 |
| SYN-002 | run1 | SYN-002 | 6/7 | 6/7 | 0 |
| SYN-002 | run2 | SYN-002-control | 7/7 | 7/7 | 0 |
| SYN-002 | run2 | SYN-002 | 5/7 | 5/7 | 0 |
| SYN-002 | run3 | SYN-002-control | 7/7 | 7/7 | 0 |
| SYN-002 | run3 | SYN-002 | 7/7 | 7/7 | 0 |
| SYN-003 | run1 | SYN-003-control | 5/5 | 5/5 | 0 |
| SYN-003 | run1 | SYN-003 | 4/5 | 4/5 | 0 |
| SYN-003 | run2 | SYN-003-control | 5/5 | 5/5 | 0 |
| SYN-003 | run2 | SYN-003 | 5/5 | 5/5 | 0 |
| SYN-003 | run3 | SYN-003-control | 5/5 | 5/5 | 0 |
| SYN-003 | run3 | SYN-003 | 4/5 | 4/5 | 0 |

## SYN-001 regression (saved evidence, live assessment)

| Set | Prior round-one result | Round-two result | Unsafe before / after |
|---|---|---|---|
| in_sample | 28/29 | 28/29 | 0 / 0 |
Changed in_sample predictions: none.
| held_out | 21/21 | 21/21 | 0 / 0 |
Changed held_out predictions: none.

## Guard interventions

Counts below are final-batch assessment rows with each guard, counted once per guard per row in the `llm_assessor` pipeline. A row can trigger multiple guards. Baseline-only flags are excluded.

| Guard | SYN-002 | SYN-003 |
|---|---|---|
| History scope / exception / narrower negative | 4 | 4 |
| Status / conclusion contradiction | 0 | 1 |
| Computed therapy window | 6 | 6 |
| Legacy missing study reference | 0 | 6 |
| Prior-exposure absence | 3 | 2 |
| Unsupported conclusion (no citations) | 5 | 1 |
| Partial inclusion evidence | 0 | 0 |
| Unverified citation | 0 | 0 |
| Medication snapshot wording | 2 | 0 |

The legacy study-reference guard does not recognize every cycle-1-day-1 wording. It can emit an intermediate UNKNOWN flag, followed by the authoritative computed-window flag and final DOES_NOT_MEET. Such a legacy flag is not a final downgrade. The full flag lists and final statuses are preserved rather than hiding this interaction.

## Planned-dose and washout audit

All six SYN-003 washout assessments cite verified 2026-04-08 administration and 2026-04-20 planned first-dose evidence, report a code-computed 12-day interval, and return DOES_NOT_MEET. Outside-window and missing-reference behavior are covered offline. Scheduled events are not actual administrations and still need reviewer confirmation.

## Uncovered-sentence audit

| Patient | Run | Original raw-line gaps | Same evidence with sentence/context handling | Fresh round-two sentence gaps |
|---|---|---|---|
| SYN-003-control | run1 | 19 | 13 | 13 |
| SYN-003 | run1 | 19 | 11 | 10 |
| SYN-003-control | run2 | 20 | 13 | 14 |
| SYN-003 | run2 | 20 | 11 | 10 |
| SYN-003-control | run3 | 19 | 13 | 13 |
| SYN-003 | run3 | 20 | 11 | 10 |

The final lists do not repeat verified extracted Hodgkin/pembrolizumab sentences. In control run1 and run2 the discussed-but-never-started pembrolizumab sentence was not extracted at all; it correctly remains a manual-review gap rather than being suppressed. Full verified sentence context does not create additional fact records or establish clinical completeness. Genuine uncovered narrative (follow-up recommendations, functional statements, logistics, and other unextracted sentences) remains visible. No line from a different page is used to hide a gap.

## Remaining misses and anything worse

**SYN-002 worsened from 41/42 to 39/42 exact/acceptable** in the final repeated batch, despite zero unsafe clearances. SYN-003 improved from 20/30 exact and 26/30 acceptable with four unsafe clearances to 28/30 exact/acceptable and zero unsafe clearances. These stochastic development runs do not establish generalization.

- run1 SYN-002 NCT07559760 EXC-19: expected DOES_NOT_MEET; got UNKNOWN. Flags: EXC-19: History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN.
- run2 SYN-002 NCT06412198 EXC-02: expected DOES_NOT_MEET; got UNKNOWN. Flags: EXC-02: unsupported conclusion converted to UNKNOWN.
- run2 SYN-002 NCT06252649 EXC-03: expected DOES_NOT_MEET; got UNKNOWN. Flags: EXC-03: absence-based clearance of a prior-exposure exclusion converted to UNKNOWN.
- run1 SYN-003 NCT07559760 EXC-19: expected DOES_NOT_MEET; got UNKNOWN. Flags: EXC-19: status contradicts explanation; converted to UNKNOWN.
- run3 SYN-003 NCT07559760 EXC-19: expected DOES_NOT_MEET; got UNKNOWN. Flags: EXC-19: History clearance guard: absence of explicit scope-matching negative evidence does not clear this condition history. Converted to UNKNOWN.

The remaining SYN-003 malignancy misses are conservative UNKNOWN outcomes (one contradiction, one attempted history clearance blocked). The SYN-002 misses include missing/unsupported treatment citations and prior-exposure clearance blocked by the existing guard. The models still sometimes supply nonverbatim source quotes; those records remain unverified and cannot support a decision. No third attempt was made to recover these scores.

## Provenance and retained attempts

- Original labels, patient PDFs, trial data, saved SYN-001 evidence, earlier runs and blind-results documents are unchanged. Both batches verify protected-file SHA256 hashes and frozen-code hashes.
- First attempt: `data/eval/round2_attempt1/`; original implementation `de13fb8`, retained via tag `round2-attempt1`. Its run commands record the original output locations before archival.
- Final attempt: `data/eval/syn002_runs_round2/run1..3`, `data/eval/syn003_runs_round2/run1..3`, and `data/eval/round2_validation/syn001/`. Each run includes logs, reports, evidence (patient runs) and a timestamped manifest.
- All required processes exited successfully. Zero unsafe clearances in these synthetic runs is not clinical validation.
- The blind state on main remains at c00e021. No SYN-004 patient or label was created or inspected.
