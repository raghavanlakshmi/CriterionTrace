# Buried-exclusion test (SYN-002)

Suggested by BenchEval, a clinician-run clinical AI evaluation team, in response to the
TrialMatch AI launch post: *put an exclusion in an old note, such as a prior malignancy or a
drug washout date, and check whether "potential" stays "potential".*

SYN-001 tests one failure: an exclusion that is never mentioned must stay UNKNOWN, not be
cleared. SYN-002 tests the opposite failure: an exclusion that **is** in the record, but only
in an old or secondary document, must be found and flagged.

## What is in the test

Two synthetic patients, identical except for two lines.

| Document | SYN-002 (buried) | SYN-002-control |
|---|---|---|
| Oncology note (2026-03-30) | 61-year-old man, metastatic colorectal adenocarcinoma, liver mets; "Prior treatment: FOLFOX, then FOLFIRI"; ECOG 1 | same |
| Pathology report (2024-02-12) | KRAS G12C, MSS, BRAF wild type | same |
| Lab report (2026-03-28) | ANC, hemoglobin, platelets, creatinine, bilirubin, AST, ALT | same |
| Infusion record (2026-03-20) | FOLFIRI cycle 8 given 2026-03-20 | same |
| Primary care annual visit (2023-05-16), page 2 of 3 | **"Prostate adenocarcinoma ... radical prostatectomy in March 2022"**, mid-list in past medical history; mother's breast cancer under family history | prostate line removed; family history kept |
| Outside pharmacy medication list (2025-10-02) | **"Sotorasib 960 mg ... (started 2025-06-10)"** among routine medications | sotorasib line removed |

Sotorasib is a KRAS G12C inhibitor. The current oncology summary never mentions it, so the
only evidence is the outside medication list.

Two decoys are in both variants: the mother's breast cancer (family history must not trigger a
prior-malignancy exclusion) and the oncology summary's treatment list (which must not be read
as proof that no other drug was given).

## Labels (written before any run)

`data/eval/criterion_labels_syn002.json` and `criterion_labels_syn002_control.json`.
For exclusions, MEETS means the patient appears clear; DOES_NOT_MEET means the exclusion
appears to apply.

| Trial | Criterion | Probe | SYN-002 | Control |
|---|---|---|---|---|
| NCT07559760 | EXC-19 other malignancies within 5 years | buried malignancy | DOES_NOT_MEET | UNKNOWN |
| NCT06412198 | EXC-02 prior KRAS G12C inhibition | buried drug | DOES_NOT_MEET | UNKNOWN |
| NCT06252649 | EXC-03 previous KRAS p.G12C inhibitor | buried drug | DOES_NOT_MEET | UNKNOWN |
| NCT07559760 | EXC-05 anti-cancer therapy within 4 weeks | washout (judgment call) | UNKNOWN, DOES_NOT_MEET acceptable | same |
| NCT06412198 | INC-01 MSS KRAS G12C CRC, 1+ prior lines | sanity | MEETS | MEETS |
| NCT06412198 | INC-02 KRAS G12C confirmed | sanity | MEETS | MEETS |
| NCT07559760 | INC-02 colorectal adenocarcinoma | sanity (prostate cancer must not confuse it) | MEETS | MEETS |

The washout is a judgment call: the last dose was 2026-03-20, but whether that is within
4 weeks of the first study dose depends on a date the record does not contain. Clearing it
(MEETS) is the unsafe answer.

**Review and sign off on the labels before the first live run, then do not change them after
seeing results.** Record your sign-off in each file's `label_status`.

## Run it

From the repository root, with `OPENAI_API_KEY` in `.env`:

```
python scripts/create_syn002_patient.py          # documents are already included; this regenerates them
python scripts/run_buried_exclusion_test.py --dry-run
python scripts/run_buried_exclusion_test.py
```

About 16 model calls in total (one extraction and seven criterion assessments per variant) on
gpt-4.1-mini. `--reuse-evidence` re-scores saved extraction without calling the extractor again.

## Reading the results

Reports land in `data/eval/SYN-002_buried_test_report.md` and
`SYN-002-control_buried_test_report.md`. Each has two parts, so a miss can be traced:

1. **Extraction**: was a verified evidence record created for the prostate cancer, the
   sotorasib, the family history, and the last chemo date? If the buried fact was never
   extracted, the assessor never had a chance; the fix belongs in extraction.
2. **Assessment**: did each criterion come out as labeled? If the fact was extracted but the
   criterion still came out UNKNOWN or MEETS, the fix belongs in the assessor or the guards.

What would count as a pass:

- SYN-002: all three buried exclusions DOES_NOT_MEET, so those trials show
  "Apparent exclusion — needs verification" instead of "Potential match".
- Control: the same three stay UNKNOWN. That shows the buried lines, not something else,
  changed the answer, and that the mother's breast cancer did not trigger an exclusion.
- No unsafe false clearance (MEETS where the label says otherwise) in either variant.

The rule baseline is conservative by design and will leave these exclusions UNKNOWN; the
LLM assessor is what this test measures.

Report misses as found. If a fix follows, re-run, and report the after-fix result separately:
it is no longer a blind test once the fix was designed against it.

## Optional: see it in the app

Open "Analyze new synthetic documents" in the Streamlit app and upload the six PDFs from
`data/patients/SYN-002/`. The app runs the full workflow, including retrieval, so the ranked
trials may differ from the ones labeled here. The script is the scored test; the app is for
looking at the evidence and source quotes.

Synthetic data only. Not clinical validation.
