# Fix spec, round 3: SYN-004 blind findings

Hand this file to the coding assistant. Save it in the repo as `docs/fix_spec_round3.md`.

## Context

SYN-004 was built after round 2 was frozen (`caa440b`), without reading that code, with labels
committed before any run (`b09f44e`). Three runs (`data/eval/syn004_runs/`, `layer_audit.json`) found:

1. **Clearance from an allowed condition, again (5 unsafe clearances).** NCT06412198 EXC-04, "Active
   autoimmune disease that has required systemic treatment in the past 2 years ... Replacement therapy
   (e.g., thyroxine ...) is not considered a form of systemic treatment." The model reasoned:
   "Hashimoto's is on replacement therapy, which is allowed; nothing else is documented; so the patient
   is clear." No guard fired. Round-2 Fix A covered the same mistake only for exclusions worded as
   history ("history of", "other malignancies within N years").
2. **A correct answer overridden by an older guard.** Run 1, NCT07559760 EXC-08 (TIA within 6 months):
   the model cited the TIA (2026-02-09) and the planned first dose (2026-06-22) and answered
   DOES_NOT_MEET correctly. The older study-reference guard converted it to UNKNOWN ("lacks an
   explicitly documented study reference date") even though the planned-first-dose record was cited.
3. **No code-computed window for clinical events.** The computed time-window path handles therapy
   administrations only. A dated event (TIA, MI, surgery, infection) inside a window is not computed.
4. **Courses of treatment stored with the start date only.** "Prednisone 40 mg daily for 5 days
   (2026-06-14 through 2026-06-18)" was stored with date 2026-06-14. Counting from the start gives 8 days
   (outside a 7-day window); the last dose gives 4 days (inside). The computed path also reported
   "missing dated administration" although the dated prednisone record and the planned first dose were
   both cited, so it did not treat a non-cancer systemic drug as an administration.
5. **Compound criteria reduced to their time-window part.** NCT06412198 EXC-03 is "diagnosis of
   immunodeficiency OR systemic steroid / immunosuppressive therapy within 7 days." The computed path
   decided the whole criterion and bypassed the model, so the immunodeficiency part was never assessed.
6. **Model date arithmetic in explanations.** Run 1: "prednisone taper completed in April 2025, which is
   more than 2 years before ... 2026-06-22" (it is about 14 months). It also invented a rule ("short
   courses under 5 days are not considered systemic treatment") for a 5-day course.
7. **Unsupported category inference.** Run 3 false exclusion: "drug-induced interstitial pneumonitis
   (likely autoimmune-related)." The record does not say this.
8. **Extraction missed the TIA in runs 2 and 3.** The model then concluded "no cardiovascular event is
   documented," which would have been an unsafe clearance; a time-window guard converted it to UNKNOWN
   for an unrelated reason.

Also seen, not a defect to fix: the negative brain MRI (NCT06252649 EXC-01) was UNKNOWN in 6/6. It is an
explicit negative and should be allowed to clear. Use it as the check that the new guards do not
block legitimate clearances.

## Ground rules (same as rounds 1 and 2)

- Do not change any label file, patient document, existing run folder, or results document
  (SYN-001 to SYN-004).
- Do not create SYN-005 or any new test patient. It is built separately, after these fixes are frozen.
- Keep every change general. No special cases for autoimmune disease, thyroid, Hashimoto's, TIA,
  prednisone, specific trials, criterion IDs, or patient filenames. **Round 2 failed on SYN-004 because
  its guards matched specific wordings. Each fix below is a rule about structure, not wording.**
- **The model chooses which facts are relevant; code checks and computes.** Dates, intervals,
  label/explanation consistency, and whether a cited quote is negative are decided in code.
- Design each fix from the root cause above, then test. At most two attempts against SYN-002, SYN-003
  and SYN-004 combined; then stop and report. Keep every attempt's outputs.
- One commit per fix. All existing tests must pass; report before and after counts.

## Fix A: one clearance rule for every exclusion

Files: `src/eligibility.py` (assessor output), `src/safety.py`.

Replaces the history-only scope of round-2 Fix A. Keep that guard's tests; they must still pass.

- For every exclusion criterion, when the model answers MEETS (patient clear), it must also return a
  structured `clearance_basis`, one of:
  - `explicit_negative`: a cited fact explicitly rules out the condition at the criterion's scope
    (for example "no intracranial metastases" for brain metastases)
  - `exception_only`: the only relevant facts match an exception in the criterion
  - `absence`: nothing relevant is documented
  - `other`
- Code keeps MEETS only when `clearance_basis` is `explicit_negative` **and** at least one cited,
  verified quote contains a negation (no, not, negative, without, denies, ruled out, absent, free of,
  and so on, with tests for negation handling).
- Every other case becomes UNKNOWN with a flag naming the basis ("cleared from absence", "cleared on
  an allowed condition only", "no negative evidence cited").
- Round-2 narrower-negation handling (a negation narrower than the criterion does not clear it) stays.

Done when, with unit tests:
- allowed condition only + MEETS → UNKNOWN + flag (use a non-cancer, non-history wording in the test)
- absence + MEETS → UNKNOWN + flag
- `explicit_negative` with a negated, verified quote → stays MEETS
- `explicit_negative` claimed but no cited quote contains a negation → UNKNOWN + flag
- inclusion criteria are unaffected

## Fix B: retire the older study-reference guard when the reference is cited

Files: `src/safety.py`.

- If a verified `planned_study_event` record is cited, the older "missing study reference date" guard
  must not fire.
- Where the computed window (Fix C) has run, its result is authoritative; the older guard is not applied
  to that criterion at all. Remove the intermediate legacy flag noted in the round-2 summary.

Done when: a unit test with a cited dated event, a cited planned first dose, and a correct
DOES_NOT_MEET keeps DOES_NOT_MEET with no study-reference flag.

## Fix C: code-computed windows for dated clinical events

Files: `src/safety.py`, `src/eligibility.py` (structured field).

- Extend the computed window from therapy administrations to any dated event the window applies to
  (diagnosis, procedure, hospitalization, cardiovascular or infectious event, and so on).
- **The model selects the record; code does the math.** The assessor returns `window_evidence_index`:
  the cited record the time window applies to. Code checks that the record is cited and verified, has a
  date, and that a verified planned first-dose record is cited; then computes the interval.
- Inside the window → DOES_NOT_MEET. Outside → UNKNOWN (the record may be incomplete). Missing date or
  reference → UNKNOWN with a flag. Record the computed interval in the explanation and flags.
- Do not choose the record in code by keyword or category; that is how round 2 missed prednisone.

Done when: unit tests cover an event inside the window, outside the window, missing event date, and a
missing reference date. On SYN-004, EXC-08 cites the TIA and the planned dose and reports a
code-computed 133-day interval, whenever the TIA is extracted.

## Fix D: courses of treatment carry start and end dates

Files: `src/schemas.py`, `src/config.py`, `src/evidence_extraction.py`, `src/safety.py`.

- Add optional `start_date` and `end_date` (or `last_dose_date`) to evidence records. Keep `date` for
  single events.
- Extraction prompt: when a source gives a course ("for 5 days from X through Y", "from June to August",
  "taper completed in April 2025"), record both ends, at the precision given. A month-only date stays
  month-only; do not invent a day.
- Windows "within N days before first dose" count from the end date when there is one.
- Any systemic drug can be the window record (Fix C), not only anti-cancer therapy. Whether the drug
  belongs to the class in the criterion (systemic steroid, immunosuppressant) is the model's choice of
  `window_evidence_index`; route and dosage form stay visible to the reviewer.
- A month-only end date: use the last day of that month for "inside the window" and the first day for
  "outside"; if the two disagree, UNKNOWN.

Done when: unit tests show a 5-day course ending 4 days before first dose → DOES_NOT_MEET for a 7-day
window, and the same course with only a start date 8 days before → UNKNOWN. On SYN-004, the prednisone
record carries 2026-06-14 and 2026-06-18.

## Fix E: compound criteria keep all their parts

Files: `src/safety.py`, `src/eligibility.py`.

- When a criterion contains a time window plus other conditions joined by "or" (or listed), the
  computed window decides only the window part. The model still assesses the other parts.
- Combine in code: any part DOES_NOT_MEET → DOES_NOT_MEET; MEETS only if every part is cleared under
  Fix A; otherwise UNKNOWN. Show each part's result in the explanation.

Done when: a unit test for "condition X or drug Y within 7 days," with Y outside the window and X not
addressed, gives UNKNOWN with both parts shown, and the model was called.

## Fix F: code checks date claims in explanations

Files: `src/eligibility.py` (structured field), `src/safety.py`.

- The assessor returns `date_comparisons`: each comparison its decision relies on, as
  `{from_date, to_date, claimed: "within|more_than|less_than", amount, unit}`.
- Code recomputes each one. A wrong claim → UNKNOWN with the flag "explanation contains an incorrect
  date comparison," keeping the original reasoning visible.
- Fallback for explanations without structured comparisons: if the text compares two explicit dates
  with "more than / less than / within N units," parse and check them.

Done when: a unit test with "April 2025 is more than 2 years before 2026-06-22" → UNKNOWN + flag; a
correct comparison is unchanged.

## Fix G: flag unsupported category inference

Files: `src/safety.py` (generalizes round-1 Fix 3, biomarker-to-treatment).

- Detect explanations that assign a condition to a category with hedged wording ("likely ...-related",
  "probably", "suggests", "consistent with", "may represent") where no cited, verified quote states that
  category.
- If the final status depends on it (a DOES_NOT_MEET or MEETS that cites only the inferred
  link), convert to UNKNOWN with a flag. Otherwise keep the status and add a review flag.

Done when: a unit test with "pneumonitis (likely autoimmune-related)" as the only basis for an
autoimmune exclusion → UNKNOWN + flag; an explanation without hedged inference is unchanged.

## Fix H: report, then close, the extraction gap

Files: `src/evidence_extraction.py` only if the report shows a defect.

- First report: in SYN-004 runs 2 and 3, was the sentence "Assessment: transient ischemic attack on
  2026-02-09 ..." in the "Not captured by the tool, review manually" list? Was the second extraction pass
  triggered for that page?
- If the sentence was missing from the list, find why (for example, another quote from the same
  page counted as covering it) and fix it so a sentence counts as covered only when a verified quote
  covers that sentence.
- Do not try to make extraction never miss. The requirement is that a missed fact is listed for review.

Done when: a unit test with a fake extractor that skips a diagnosis sentence shows it in the review
list. Report the SYN-004 runs 2 and 3 answer either way.

## Testing and reporting

1. Full offline suite with new tests for A to H. Report before and after counts.
2. SYN-001 regression (in-sample and held-out). **Report every changed prediction, including
   MEETS → UNKNOWN**, because Fix A may make the tool more conservative.
3. Three runs each, labeled "after round-3 fixes, not blind":
   SYN-002 → `data/eval/syn002_runs_round3/run1..3`,
   SYN-003 → `data/eval/syn003_runs_round3/run1..3`,
   SYN-004 → `data/eval/syn004_runs_round3/run1..3`.
4. A summary in the same format as before: exact and acceptable scores, unsafe clearances, false
   exclusions, guard interventions, every changed result, and anything that got worse. Include the
   brain-MRI rows separately (they show whether the guards still allow legitimate clearances). Do not
   merge with earlier results.
5. Freeze the code and record the commit and a tag (`round3-frozen`). SYN-005 runs on that commit.

## Out of scope

Retrieval, trial data, UI layout beyond showing new flags and compound-criterion parts, new patients
or labels.
