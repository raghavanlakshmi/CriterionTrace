# SYN-002 confirmation runs

run1 is the original completed evaluation. run2 and run3 are fresh extraction and assessment runs after label commit dc875ac. An earlier interrupted repeat was not counted. No pipeline changes or label changes were made.

| Run | Variant | Exact | Acceptable | Unsafe clearances | Buried exclusions |
|---|---|---|---|---|---|
| run1 | SYN-002 | 6/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run1 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run2 | SYN-002 | 7/7 | 7/7 | 0 | DOES_NOT_MEET, DOES_NOT_MEET, DOES_NOT_MEET |
| run2 | SYN-002-control | 6/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |
| run3 | SYN-002 | 5/7 | 6/7 | 0 | UNKNOWN, DOES_NOT_MEET, DOES_NOT_MEET |
| run3 | SYN-002-control | 7/7 | 7/7 | 0 | UNKNOWN, UNKNOWN, UNKNOWN |

Exact metrics count the approved alternative washout DOES_NOT_MEET as a mismatch against primary UNKNOWN. Acceptable metrics allow that alternative. Review the explanations separately; acceptance alone does not validate temporal reasoning.

## Findings across all three runs

- Buried prostate malignancy was extracted and flagged in run1 and run2, but not extracted in run3; EXC-19 therefore stayed UNKNOWN in run3. This is an extraction miss.
- Sotorasib was extracted in all three buried variants; both drug exclusions were flagged in all three runs.
- All three corresponding control exclusions stayed UNKNOWN in every run.
- Final reviewed assessments had zero unsafe false clearances across all runs. In run2's buried variant, the safety guard converted an unsupported washout clearance to UNKNOWN; the raw assessor was not consistently safe on timing.
- Family history was not extracted in any of the six variant evaluations. The last chemotherapy date was extracted only in run2's control.
- Washout reasoning remained unreliable. Some explanations assumed a first study dose date or substituted a note date; that date is absent. The frozen labels accept DOES_NOT_MEET, so an acceptable score does not resolve this defect.
- All inclusion sanity checks were MEETS in the LLM assessments across all runs.

Each run folder contains two Markdown reports, two JSON reports, two evidence JSON files, and both signed-off label files. The package-level output files now contain run3; the archives preserve each run separately.
