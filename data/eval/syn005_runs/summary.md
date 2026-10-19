# SYN-005 blind test: three frozen runs

**23/45 decidable rows answered correctly (51.1%); zero unsafe clearances; three false exclusions.** Overall: **26/48 exact (54.2%)**, **42/48 acceptable (87.5%)**. UNKNOWN is safe in many rows but does not count as a correct decision.

## Provenance

Branch: `syn005-blind`. Implementation: `round3-frozen` (`6da940d49021855cc3d03a26ece5efa001e60c5c`). Signed-off inputs were committed and pushed as `ec2b6275e5e8349f5eaac0f81e01808673b68fa7` on October 18, 2026, before the dry run or live runs. Both user sign-offs were preserved. The runner changes only register SYN-005 and its extraction probes; implementation fixes remained frozen.

Dry run exited 0: eight PDFs/nine pages per variant, all text, no OCR. Each live run used fresh extraction, exactly `--variants SYN-005 SYN-005-control`, and its own output folder. All three completed successfully. Code and protected-input SHA-256 hashes were verified before/after runs and before this summary. See `frozen_manifest.json`, each `run_manifest.json`, and logs. Timestamps are UTC; the runs occurred October 18, 2026 in America/New_York.

## Results

| Run | Variant | Decided correctly | Exact | Acceptable | Unsafe | False exclusions |
|---|---|---:|---:|---:|---:|---:|
| 1 | SYN-005 | 4/8 | 4/8 | 6/8 | 0 | 1 |
| 1 | SYN-005-control | 4/7 | 5/8 | 8/8 | 0 | 0 |
| 2 | SYN-005 | 5/8 | 5/8 | 7/8 | 0 | 1 |
| 2 | SYN-005-control | 3/7 | 4/8 | 8/8 | 0 | 0 |
| 3 | SYN-005 | 3/8 | 3/8 | 5/8 | 0 | 1 |
| 3 | SYN-005-control | 4/7 | 5/8 | 8/8 | 0 | 0 |

There are 16 labeled patient/criterion pairs repeated three times, not 48 independent cases. The control biopsy label is UNKNOWN, leaving 45 decidable rows. Of those, 23 were correct definitive answers, 19 UNKNOWN, and three incorrect definitive answers. Across all 48 rows, 22 were UNKNOWN; three of those exactly match the control biopsy label. Sixteen UNKNOWN answers were allowed alternatives.

## Findings by layer

- **Extraction / QTcF:** the buried QTcF exclusion was caught in run 2 only; runs 1 and 3 returned UNKNOWN. Verified QTcF probe hits were absent in those two runs and in all three controls. All control QTcF assessments were UNKNOWN. This indicates an extraction coverage gap, consistent with assessment explanations reporting no measurement. Probe absence alone is not proof that every possible representation was absent.
- **Extraction / renal calculation:** weight had no verified probe hits in all six extractions, while creatinine did. All six clearance assessments were UNKNOWN. The source/reference inputs yield Cockcroft-Gault `(140-67)*52*0.85/(72*1.3) = 34.5 mL/min`, below 50. That is the test reference calculation, not a calculation successfully performed by the pipeline.
- **Assessment / exception handling:** all three buried recovery-inclusion assessments incorrectly returned DOES_NOT_MEET despite the explicit exception for prior oxaliplatin-induced neuropathy. Neuropathy and alopecia were extracted with verified citations. No guard flag explains these three false exclusions; the reasoning mishandles the exception. Controls cleared twice and returned UNKNOWN once.
- **Guard / investigator judgment:** the unresolved-toxicity exclusion returned UNKNOWN in all six assessments, an allowed alternative. The investigator-judgment guard explains these deferrals. They contribute to acceptable answers, but no correct definitive decisions for this criterion.
- **Guard / age:** buried run 3 was changed to UNKNOWN by the date-comparison guard although the original age reasoning correctly described age 67. The assessment supplied an unsupported date comparison from 1949-07-31 to 2026-07-31 (77 years), claimed within 75 years. This extraneous comparison triggered the downgrade. The other five age assessments cleared correctly.
- **Successful temporal exclusion:** buried major surgery was caught in all three runs, with verified discharge-summary page 2 evidence and the planned first-dose reference. The computed-window guard reports the 19-day interval. Control core-needle biopsies remained UNKNOWN in all three, as labeled.
- **Successful explicit negatives:** all six HIV/HBV/HCV serology assessments returned MEETS using verified negative evidence. ECOG also cleared correctly in all six.

## Criterion-level usefulness

| Criterion | Correct definitive decisions / decidable rows |
|---|---:|
| QTcF | 1/6 |
| Major surgery (buried only; control label UNKNOWN) | 3/3 |
| Unresolved toxicity exclusion | 0/6 |
| Recovery inclusion with exceptions | 2/6 |
| Negative viral serologies | 6/6 |
| Calculated creatinine clearance | 0/6 |
| Age | 5/6 |
| ECOG | 6/6 |

## Artifacts and limits

Each run folder preserves both evidence JSON files, both report JSON files, both Markdown reports, execution log and manifest. `layer_audit.json` preserves verified probe counts, extraction gaps, and every non-exact assessment with its citations, flags, compound parts and date comparisons. `summary.json` preserves all 48 final LLM-assessor rows and aggregate counts. The individual reports also retain the rule baseline separately; the headline above is for the LLM assessor.

These are synthetic prescreening tests, not clinical validation. Zero unsafe clearances does not imply every hidden exclusion was identified: unresolved cases still require review. The recurring neuropathy false exclusions and the extraction/calculation gaps remain unresolved. No implementation, label or patient changes were made after seeing these results; any subsequent fixes make SYN-005 a development test and require separately reported results.
