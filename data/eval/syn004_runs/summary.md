# SYN-004 blind test: three frozen-code runs

Pre-run signed-label/test commit: `b09f44e09c6757fa2b4fcd7196a5fe0a5aa4958a`; committed and pushed before dry/live execution. Branch: `syn004-blind`, created from `round2-frozen`. Implementation: `caa440b3a324428f7fdb2dc62468ad0a311667a4`. Only the supplied runner adapter and SYN-004 package were added. `src/` and `app.py` are unchanged. Both signoff lines were preserved exactly.

The dry run showed each scanned consult as OCR_REQUIRED with 0 characters. Live runs used the app's vision ingestion path with fresh OCR and extraction on every run. The runner saved all page text (including scan transcription), extracted facts and assessment reports separately. Each run has its own log and timestamped manifest. All frozen source and protected-input hashes matched before and after all three runs.

## LLM-assessor pipeline results

**Exact: 24/42. Acceptable: 33/42. Unsafe clearances: 5. False exclusions: 1 (control false exclusions: 0).** These are three repetitions of 14 labeled patient-criterion pairs, not 42 independent cases. The label-defined UNKNOWN allowances were applied unchanged.

| Run | Variant | Exact | Acceptable | Unsafe clearances | False exclusions |
|---|---|---|---|---|---|
| run1 | SYN-004 | 3/7 | 5/7 | 1 | 0 |
| run1 | SYN-004-control | 5/7 | 6/7 | 1 | 0 |
| run2 | SYN-004 | 3/7 | 5/7 | 1 | 0 |
| run2 | SYN-004-control | 5/7 | 6/7 | 1 | 0 |
| run3 | SYN-004 | 3/7 | 5/7 | 0 | 1 |
| run3 | SYN-004-control | 5/7 | 6/7 | 1 | 0 |

## Where the misses happened

- **OCR / pneumonitis:** all three buried scans were transcribed with OPENAI_VISION and contain interstitial pneumonitis. It was extracted, cited and assessed DOES_NOT_MEET in all three runs. Control pneumonia remained UNKNOWN in every run; no control false exclusion occurred.
- **Autoimmune exception:** all six autoimmune labels are UNKNOWN. The model returned MEETS in five assessments (two buried, three control), producing every unsafe clearance, and DOES_NOT_MEET for the buried patient in run3, producing the one false exclusion. No safety flag fired on those rows. This is an assessment/guard failure despite the documented thyroid-replacement exception; the frozen code did not reliably generalize to this exclusion.
- **TIA:** the buried TIA criterion was UNKNOWN in all three runs instead of DOES_NOT_MEET. The dated TIA was present in source text and extracted evidence, but the cited date/reference handling failed during assessment/guards. The flag was missing study-reference date in run1, and missing dated cited evidence in run2/run3. The full extraction and citation records below distinguish missing citation metadata from an unrecognized source fact.
- **Systemic steroid window:** the buried prednisone window remained UNKNOWN in every run (predeclared acceptable, but not the exact label). The stop date and planned first-dose date appear in verified source quotes; the computed-window path did not establish the required dated administration/reference pair for this steroid record. In run1 the treatment fact date is the start/document date, 2026-06-14, although its quote contains 2026-06-18. UNKNOWN does not demonstrate successful 4-day steroid-window reasoning.
- **Negative brain MRI:** all six answers were UNKNOWN rather than MEETS; UNKNOWN is predeclared acceptable. Two cases were blocked as unsupported exclusion clearances and four had no supporting citations. This loses exact accuracy without an unsafe clearance.
- **Sanity criteria:** both diagnosis/biomarker and ECOG criteria matched MEETS in every run for both variants.

## OCR and extraction audit

| Run | Variant | Scan method | Scan chars | Pneumonitis in scan | Pneumonia in scan | Unverified facts |
|---|---|---|---|---|---|---|
| run1 | SYN-004 | OPENAI_VISION | 769 | True | False | 0 |
| run1 | SYN-004-control | OPENAI_VISION | 699 | False | True | 0 |
| run2 | SYN-004 | OPENAI_VISION | 769 | True | False | 0 |
| run2 | SYN-004-control | OPENAI_VISION | 703 | False | True | 0 |
| run3 | SYN-004 | OPENAI_VISION | 769 | True | False | 0 |
| run3 | SYN-004-control | OPENAI_VISION | 700 | False | True | 1 |

The keyword probes measure quote presence, not clinical meaning. For example a drug discussed but not given is not administration evidence. `layer_audit.json` includes all probe hits, their dates and quote-verification flags, plus each assessment's citations, reasoning and safety flags.

| Run | Buried probe | Verified hits | Recorded dates |
|---|---|---|---|
| run1 | buried_pneumonitis_ocr | 1 | 2025-05-06 |
| run1 | buried_steroid | 4 | 2025-05-06, 2026-06-14, None |
| run1 | steroid_last_dose | 1 | 2026-06-14 |
| run1 | buried_tia | 2 | 2026-02-09, 2026-02-20 |
| run1 | scheduled_first_dose | 1 | 2026-06-22 |
| run2 | buried_pneumonitis_ocr | 2 | 2025-05-06 |
| run2 | buried_steroid | 4 | 2025-05-06, 2026-06-14, None |
| run2 | steroid_last_dose | 1 | 2026-06-14 |
| run2 | buried_tia | 0 |  |
| run2 | scheduled_first_dose | 1 | 2026-06-22 |
| run3 | buried_pneumonitis_ocr | 1 | 2025-05-06 |
| run3 | buried_steroid | 3 | 2025-05-06, 2026-06-14, April 2025 |
| run3 | steroid_last_dose | 1 | 2026-06-14 |
| run3 | buried_tia | 0 |  |
| run3 | scheduled_first_dose | 1 | 2026-06-22 |

## All criterion predictions

| Run | Variant | Trial | Criterion | Probe | Expected | Predicted | Acceptable |
|---|---|---|---|---|---|---|---|
| run1 | SYN-004 | NCT06252649 | EXC-04 | buried_pneumonitis_ocr | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run1 | SYN-004 | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | UNKNOWN | True |
| run1 | SYN-004 | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | False |
| run1 | SYN-004 | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | False |
| run1 | SYN-004 | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run1 | SYN-004 | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run1 | SYN-004 | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |
| run1 | SYN-004-control | NCT06252649 | EXC-04 | pneumonia_trap | UNKNOWN | UNKNOWN | True |
| run1 | SYN-004-control | NCT06412198 | EXC-03 | topical_steroid_trap | UNKNOWN | UNKNOWN | True |
| run1 | SYN-004-control | NCT07559760 | EXC-08 | vertigo_trap | UNKNOWN | UNKNOWN | True |
| run1 | SYN-004-control | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | False |
| run1 | SYN-004-control | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run1 | SYN-004-control | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run1 | SYN-004-control | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |
| run2 | SYN-004 | NCT06252649 | EXC-04 | buried_pneumonitis_ocr | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run2 | SYN-004 | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | UNKNOWN | True |
| run2 | SYN-004 | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | False |
| run2 | SYN-004 | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | False |
| run2 | SYN-004 | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run2 | SYN-004 | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run2 | SYN-004 | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |
| run2 | SYN-004-control | NCT06252649 | EXC-04 | pneumonia_trap | UNKNOWN | UNKNOWN | True |
| run2 | SYN-004-control | NCT06412198 | EXC-03 | topical_steroid_trap | UNKNOWN | UNKNOWN | True |
| run2 | SYN-004-control | NCT07559760 | EXC-08 | vertigo_trap | UNKNOWN | UNKNOWN | True |
| run2 | SYN-004-control | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | False |
| run2 | SYN-004-control | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run2 | SYN-004-control | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run2 | SYN-004-control | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |
| run3 | SYN-004 | NCT06252649 | EXC-04 | buried_pneumonitis_ocr | DOES_NOT_MEET | DOES_NOT_MEET | True |
| run3 | SYN-004 | NCT06412198 | EXC-03 | buried_steroid_window | DOES_NOT_MEET | UNKNOWN | True |
| run3 | SYN-004 | NCT07559760 | EXC-08 | buried_tia | DOES_NOT_MEET | UNKNOWN | False |
| run3 | SYN-004 | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | DOES_NOT_MEET | False |
| run3 | SYN-004 | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run3 | SYN-004 | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run3 | SYN-004 | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |
| run3 | SYN-004-control | NCT06252649 | EXC-04 | pneumonia_trap | UNKNOWN | UNKNOWN | True |
| run3 | SYN-004-control | NCT06412198 | EXC-03 | topical_steroid_trap | UNKNOWN | UNKNOWN | True |
| run3 | SYN-004-control | NCT07559760 | EXC-08 | vertigo_trap | UNKNOWN | UNKNOWN | True |
| run3 | SYN-004-control | NCT06412198 | EXC-04 | autoimmune_exception_trap | UNKNOWN | MEETS | False |
| run3 | SYN-004-control | NCT06252649 | EXC-01 | brain_mri_explicit_negative | MEETS | UNKNOWN | True |
| run3 | SYN-004-control | NCT06252649 | INC-01 | sanity | MEETS | MEETS | True |
| run3 | SYN-004-control | NCT06412198 | INC-11 | sanity | MEETS | MEETS | True |

## Guard interventions

Counts are final LLM-assessor pipeline rows bearing each flag, once per guard per row.

| Flag | Count |
|---|---|
| History clearance | 3 |
| Computed window missing dated pair | 6 |
| Missing study reference | 3 |
| Missing dated citation | 2 |
| Medication snapshots only | 1 |
| Unsupported exclusion clearance | 2 |
| No cited evidence | 4 |
| Status contradicts explanation | 0 |

## Rule baseline

| Run | Variant | Exact | Acceptable | Unsafe | False exclusion |
|---|---|---|---|---|---|
| run1 | SYN-004 | 3/7 | 5/7 | 0 | 0 |
| run1 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |
| run2 | SYN-004 | 3/7 | 5/7 | 0 | 0 |
| run2 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |
| run3 | SYN-004 | 3/7 | 5/7 | 0 | 0 |
| run3 | SYN-004-control | 6/7 | 7/7 | 0 | 0 |

## Comparison and limitations

The recorded round-two development runs had SYN-002 39/42 exact/acceptable and SYN-003 28/30 exact/acceptable, each with zero unsafe clearances. This blind SYN-004 check is worse: 24/42 exact, 33/42 acceptable, 5 unsafe clearances and 1 false exclusion. The tasks and criteria differ, so these counts are not a controlled estimate of a performance delta. They show that zero unsafe clearances on the development cases did not generalize to this test.

No implementation, label, patient PDF, criterion, prompt or guard was changed in response to these results. The first result inspection occurred after all three runs were recorded. A future fix must report its SYN-004 results separately as after-fix, not blind. Synthetic data only; not clinical validation.
