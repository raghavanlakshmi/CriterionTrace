# Fix spec: SYN-002 buried-exclusion findings

Hand this file to the coding assistant. Save it in the repo as `docs/fix_spec_syn002.md`.

## Context

The blind SYN-002 test (three runs, labels signed off before the first run; results in the
`syn002_runs/` folders) found four problems:

1. Extraction skips facts outside the SYN-001 checklist: the infusion record (last FOLFIRI dose
   2026-03-20), every lab except ANC, BRAF, and the biopsy line.
2. Extraction is unreliable: in run 3 the prostate cancer line on page 2 of the 2023
   primary-care note was skipped, so EXC-19 stayed UNKNOWN.
3. The assessor treated a 2025-10-02 medication list as current ("currently taking sotorasib")
   and used it to decide a 4-week washout.
4. The assessor reasoned from a biomarker to a treatment ("KRAS G12C ... indicating they are
   being treated with KRASG12C inhibition therapy").

## Ground rules

- **Do not change** any label file, any SYN-002 document, the `syn002_runs/` folders, or the
  blind results in `docs/buried_exclusion_test.md`. They are the record of the blind test.
- Do not create SYN-003 or any new test patient. That is built separately, before the
  after-fix results are looked at.
- Keep every change general. Do not special-case sotorasib, prostate cancer, SYN-002 filenames,
  or the trials used in the test.
- No LLM output may decide anything a code check can decide.
- All existing tests must still pass. Report the before and after test count.
- One commit per fix, with a clear message, so each fix can be reviewed alone.

## Fix 1: extract all patient facts, with treatment dates

Files: `src/config.py` (`FACTS_TO_LOOK_FOR`), `src/evidence_extraction.py` (`EXTRACTION_PROMPT`),
`src/schemas.py` only if a new category is truly needed.

- Expand the checklist beyond SYN-001's items: all labs with units (hemoglobin, platelets,
  creatinine, bilirubin, AST, ALT, and any others present), every documented treatment
  administration with its date, past medical history including prior cancers, and surgical
  history.
- Add to the prompt: the checklist is a minimum, not a limit. Extract every explicitly stated
  patient fact on every page.
- A treatment administration record must carry its administration date in `date`
  (for example: FOLFIRI, cycle 8, date 2026-03-20).
- Keep existing rules: no inference from absence, exact quotes, family history is not a patient
  fact.

Done when (on SYN-002): the infusion record, all seven labs, BRAF, and the biopsy line appear as
verified evidence; family history is still not recorded as a patient condition.

## Fix 2: medication lists are dated snapshots, not current use

Files: `src/evidence_extraction.py` (prompt), `src/eligibility.py`
(`assess_free_text_criterion` prompt), `src/safety.py`.

- Extraction: a medication taken from a dated list keeps the list's document date in `date`.
  Do not describe it as current unless the source page says so in a current document.
- Assessor prompt: a dated medication list shows the drug was listed as of that date. It is
  evidence of past exposure. It is not evidence of current use or of use within a recent time
  window. Time-window criteria (for example "within 4 weeks") need a dated administration or
  stop date.
- Code guard in `safety.py`: for a criterion whose text contains a time window
  ("within N days/weeks/months"), if the conclusion is MEETS or DOES_NOT_MEET and none of the
  cited evidence has a date, convert to UNKNOWN with a visible flag. If cited evidence is
  only from medication lists, also convert to UNKNOWN with a flag.
- Prior-exposure exclusions (for example "prior KRAS G12C inhibitor") are still satisfied by a
  dated list. Do not weaken those.

Done when: SYN-002 EXC-02 and EXC-03 remain DOES_NOT_MEET, their explanations no longer say
"currently taking", and EXC-05 is never decided from the 2025 medication list.

## Fix 3: guard against biomarker-to-treatment reasoning

File: `src/safety.py` (`review_assessments`).

- Detect explanations that infer a treatment from a biomarker (for example a mutation named
  together with "indicating", "suggests", "implies", "consistent with" plus "treated",
  "therapy", "inhibitor").
- If no cited evidence of category `prior_treatment` or `current_medication` supports a
  treatment, convert to UNKNOWN with a visible flag.
- If supporting treatment evidence is cited, keep the status but add a review flag saying the
  explanation contains biomarker-to-treatment reasoning.

Done when: unit tests show (a) mutation evidence only gives UNKNOWN plus flag, (b) mutation
plus a medication record keeps DOES_NOT_MEET plus a review flag, (c) an explanation without
that reasoning is unchanged.

## Fix 4: extraction completeness check

Files: new function in `src/evidence_extraction.py` (or a new small module), wired into the
workflow and the UI review list.

- After extraction and quote verification, for each page list the content lines that are not
  covered by any verified evidence quote. Ignore administrative lines: the synthetic
  disclaimer, title, patient ID, document date, page footer, and section headings.
- If a page has uncovered content lines, re-run extraction once on that page only, verify
  quotes, and merge new records (no duplicates).
- Any line still uncovered is listed as "Not captured by the tool, review manually" in the
  output and in the human review section of the app.
- This check is deterministic and makes at most one extra extraction call per affected page.

Done when: a unit test with a fake extractor that skips one line shows that line either
captured by the second pass or listed as not captured; it is never silently dropped.

## Testing and reporting

1. Run the full test suite offline; add tests for Fix 3 and Fix 4.
2. Re-run the SYN-001 criterion evaluations (in-sample and held-out). Report any change. Note
   that the held-out set is no longer blind.
3. Run `scripts/run_buried_exclusion_test.py` three times, saving each run to
   `syn002_runs_after_fix/run1`, `run2`, `run3`, with all reports and evidence files.
4. Write `syn002_runs_after_fix/summary.md` in the same format as the blind summary, labeled
   "after fixes, not blind". Do not merge it with the blind results.
5. Report anything that got worse, not just what improved.

## Out of scope

- No changes to retrieval, the UI layout beyond the "not captured" list, or the trial data.
- No new patients or labels.
