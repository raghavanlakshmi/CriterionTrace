# SYN-005: blind test of the frozen round-3 code

Round 3 brought unsafe clearances to zero on SYN-002, SYN-003 and SYN-004, but those were
development patients, and the SYN-001 regression showed the tool had become more cautious
(held-out 21/21 to 17/21). SYN-005 is the blind check of `round3-frozen` (`6da940d`). It was written
without reading the round-3 code or its run outputs. Labels are signed and committed before the
first run; the code is not changed until all three runs are recorded.

It measures **both sides**:

1. **Safety:** are hidden exclusions caught, and does anything get cleared without proof?
2. **Usefulness:** when the record contains enough to decide, does the tool decide, or does it
   leave everything UNKNOWN?

## What is new

| | Earlier patients | SYN-005 |
|---|---|---|
| Exclusion types | prior cancer, prior drug, washout, lung history, steroid, TIA, autoimmune | QTc on an ECG (numeric threshold, sex-specific), major surgery within 4 weeks, unresolved toxicity |
| Exception clauses | "except basal-cell carcinoma", "replacement therapy is not systemic treatment" | "except alopecia" and "excluding alopecia and prior oxaliplatin-induced neuropathy": **the same neuropathy excludes for one trial and is allowed by the other** |
| Should be decided, not UNKNOWN | brain MRI (one row) | negative HIV/HBV/HCV serologies, QTcF below threshold, toxicities recovered, a creatinine clearance that must be calculated |
| Document types | notes, labs, pathology, letters, scanned fax, medication table, CT | 12-lead ECG measurement table, two-page discharge summary with the procedure on page 2, telephone toxicity note, outside serology table |

## The two variants

Identical except for three facts.

| Document | SYN-005 (buried) | SYN-005-control |
|---|---|---|
| ECG report, 2026-07-30 (table) | **QTcF 478 ms** ("Prolonged QTc") | QTcF 441 ms (normal) |
| Discharge/procedure summary, page 2 | **exploratory laparotomy with small-bowel resection, 2026-07-22, general anesthesia** | ultrasound-guided core-needle liver biopsy, 2026-07-22, same-day discharge |
| Telephone toxicity note, 2026-07-28 | **oxaliplatin-induced neuropathy grade 2**; alopecia grade 2; all others grade 0-1 | neuropathy improved to grade 1; alopecia grade 2; all others grade 0-1 |

Both: female, 67 years, 52 kg, ECOG 1 (oncology note); creatinine 1.3 mg/dL (labs); serologies
all negative (outside lab table); KRAS G12C, MSS; last FOLFIRI 2026-06-30; **cycle 1 day 1
scheduled for 2026-08-10**. The surgery is 19 days before that date.

The creatinine clearance is not written anywhere. Cockcroft-Gault from the documented values:
(140 − 67) × 52 × 0.85 / (72 × 1.3) = **34.5 mL/min**, below the trial's 50.

## Labels (written before any run)

`data/eval/criterion_labels_syn005.json` and `criterion_labels_syn005_control.json`.
For exclusions, MEETS means the patient appears clear.

| Trial | Criterion | SYN-005 | Control |
|---|---|---|---|
| NCT07559760 | EXC-09 QTcF ≥ 470 ms (women) | DOES_NOT_MEET | MEETS (UNKNOWN acceptable) |
| NCT06412198 | EXC-11 major surgery within 4 weeks | DOES_NOT_MEET | UNKNOWN (biopsy is not major surgery) |
| NCT07559760 | EXC-04 toxicity not resolved to grade ≤ 1, except alopecia | DOES_NOT_MEET (UNKNOWN acceptable: investigator clause) | MEETS (UNKNOWN acceptable) |
| NCT06412198 | INC-10 recovered to grade ≤ 1, excluding alopecia and oxaliplatin neuropathy | MEETS (UNKNOWN acceptable) | MEETS (UNKNOWN acceptable) |
| NCT07559760 | EXC-14 HIV, hepatitis B or C | MEETS (UNKNOWN acceptable) | same |
| NCT07559760 | INC-12 creatinine clearance ≥ 50 (Cockcroft-Gault) | DOES_NOT_MEET (UNKNOWN acceptable) | same |
| NCT07559760 | INC-01 age 18-75 | MEETS | same |
| NCT07559760 | INC-07 ECOG 0-1 | MEETS | same |

Eight criteria per variant, 16 per run, 48 over three runs.

- **Unsafe:** MEETS on any row not labeled MEETS (for INC-12, MEETS means a patient who fails the
  kidney requirement was passed).
- **False exclusion:** DOES_NOT_MEET where the label is MEETS or UNKNOWN. Watch the control's EXC-04
  and INC-10: excluding on alopecia means an exception clause was treated as a separate condition.
- **Decided correctly (new headline number):** of the rows whose label is MEETS or DOES_NOT_MEET
  (8 in SYN-005 and 7 in the control: 15 per run, 45 over three runs), how many got exactly that
  answer. UNKNOWN is safe on those rows but counts as not decided. Report this
  next to unsafe clearances; neither number means much alone.

## Run it

On a branch from the frozen commit, so `src/` is exactly `6da940d`:

```
git checkout -b syn005-blind round3-frozen
# copy in the SYN-005 files, review and sign the two label files, then:
git add scripts/create_syn005_patient.py scripts/run_buried_exclusion_test.py \
        data/patients/SYN-005 data/patients/SYN-005-control \
        data/eval/criterion_labels_syn005.json data/eval/criterion_labels_syn005_control.json \
        docs/syn005_blind_test.md
git commit -m "Add SYN-005 blind test with signed-off labels before runs"
git push -u origin syn005-blind

git diff --stat round3-frozen -- src app.py   # must print nothing
python scripts/run_buried_exclusion_test.py --dry-run --variants SYN-005 SYN-005-control

for r in 1 2 3; do
  python scripts/run_buried_exclusion_test.py --variants SYN-005 SYN-005-control \
         --output-dir data/eval/syn005_runs/run$r
done
```

No scanned pages this time; ingestion is text-only. Roughly 60 to 80 gpt-4.1-mini calls in total.

## Reading the results

For each miss, find the layer:

1. **Extraction:** do the probes show verified records for the QTcF value, the laparotomy (page 2)
   with its date, the neuropathy grade, alopecia, the serologies, creatinine and weight?
2. **Assessment and guards:** was the fact cited, which guards fired, and for compound or exception
   criteria, what did each part decide (`assessment_details`)?

Report results as they come out, including anything worse than the development results. If a fix
follows, SYN-005 is no longer blind and the after-fix result is reported separately.

## Results (blind, three runs on frozen code `6da940d`)

Labels were signed and committed (`ec2b627`) before the dry run and any live run. `src/` and `app.py`
were unchanged; code and protected-input hashes were verified before and after every run.

| Run | Variant | Decided correctly | Exact | Acceptable | Unsafe | False exclusions |
|---|---|---|---|---|---|---|
| 1 | SYN-005 | 4/8 | 4/8 | 6/8 | 0 | 1 |
| 1 | Control | 4/7 | 5/8 | 8/8 | 0 | 0 |
| 2 | SYN-005 | 5/8 | 5/8 | 7/8 | 0 | 1 |
| 2 | Control | 3/7 | 4/8 | 8/8 | 0 | 0 |
| 3 | SYN-005 | 3/8 | 3/8 | 5/8 | 0 | 1 |
| 3 | Control | 4/7 | 5/8 | 8/8 | 0 | 0 |

Total: decided correctly 23/45, exact 26/48, acceptable 42/48, **0 unsafe clearances**, 3 false
exclusions. These are three repetitions of 16 labeled pairs, not independent cases.

| Criterion | Correct decisions | What happened |
|---|---|---|
| Major surgery within 4 weeks | 3/3 | Found on page 2; code computed the 19-day window. Control biopsy stayed UNKNOWN 3/3. |
| HIV / hepatitis B / C | 6/6 | Cleared on verified negative serologies. |
| ECOG 0–1 | 6/6 | |
| Age 18–75 | 5/6 | One run invented a 1949 birth date (age 77); the date-comparison guard blocked the wrong claim. |
| Recovery to grade ≤ 1, excluding alopecia and oxaliplatin neuropathy | 2/6 | All 3 buried runs answered DOES_NOT_MEET, ignoring the neuropathy exception. No guard flag. |
| QTcF ≥ 470 ms (women) | 1/6 | The ECG value was not extracted in 5 of 6 runs; label and value sit on separate lines in the table. |
| Toxicity not resolved, except alopecia | 0/6 | UNKNOWN 6/6 (acceptable): the criterion's investigator-discretion clause always defers. |
| Creatinine clearance ≥ 50 (Cockcroft-Gault ≈ 34.5) | 0/6 | UNKNOWN 6/6 (acceptable): weight was never extracted, and no code calculates derived values. |

The finding: the general clearance rule from round 3 held on a patient it was not designed on (0 unsafe,
compared with 4 on SYN-003 and 5 on SYN-004 in their blind runs). The remaining gaps are about
usefulness, not safety: table extraction, derived calculations, and exception handling on the
exclusion side, which no guard checks. Any fix designed from these results makes SYN-005 a development
test; its after-fix results will be reported separately.

Reports, evidence and logs are in `data/eval/syn005_runs/run1..3`, with the full layer audit in
`layer_audit.json`.

Synthetic data only. Not clinical validation.
