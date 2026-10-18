# SYN-003: generalization test for the SYN-002 fixes

The SYN-002 fixes were designed against SYN-002, so a SYN-002 re-run cannot show whether
they generalize. SYN-003 is a fresh patient built independently, without reviewing the fixes
or their results, with labels signed off before any run.

## What is different from SYN-002

| | SYN-002 | SYN-003 |
|---|---|---|
| Buried malignancy | Prostate cancer, one line in a history list | Hodgkin lymphoma, mid-paragraph in a survivorship note |
| Buried drug | Sotorasib on a medication list | Pembrolizumab (PD-1 inhibitor), mid-paragraph in a consult note |
| Washout | Last dose only; window not decidable | Last dose 2026-04-08 and first study dose scheduled 2026-04-20 |
| Traps | Mother's breast cancer | Basal-cell carcinoma (an allowed exception); a drug discussed but never started; "no history of blood cancer" |

Patients: `data/patients/SYN-003` (buried) and `data/patients/SYN-003-control` (same
documents, buried facts removed, traps kept). Documents: `scripts/create_syn003_patient.py`.

## Labels (draft until signed)

`data/eval/criterion_labels_syn003.json` and `criterion_labels_syn003_control.json`.

| Trial | Criterion | SYN-003 | Control | What it tests |
|---|---|---|---|---|
| NCT07559760 | EXC-19 other malignancies within 5 years | DOES_NOT_MEET | UNKNOWN | Finds lymphoma in narrative; does not exclude on the excepted basal-cell carcinoma |
| NCT06412198 | EXC-01 prior PD-1 or CTLA-4 therapy | DOES_NOT_MEET | UNKNOWN | Finds pembrolizumab in narrative; does not exclude on a drug that was never given |
| NCT07559760 | EXC-05 anti-cancer therapy within 4 weeks | DOES_NOT_MEET (UNKNOWN acceptable) | same | Uses the two dates; never clears it |
| NCT06412198 | INC-02 KRAS G12C | MEETS | MEETS | Sanity |
| NCT07559760 | INC-02 colorectal adenocarcinoma | MEETS | MEETS | Sanity: other cancers do not confuse the diagnosis |

## Run

```
python scripts/run_buried_exclusion_test.py --variants SYN-003 SYN-003-control --dry-run
python scripts/run_buried_exclusion_test.py --variants SYN-003 SYN-003-control --output-dir data/eval/syn003_runs/run1
```

Repeat for `run2` and `run3`. Sign the labels and commit them before the first run. Do not
change the fixes between runs; report all three runs as the generalization result.
