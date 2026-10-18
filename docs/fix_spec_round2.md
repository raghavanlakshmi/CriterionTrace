# Fix spec, round 2: SYN-003 findings

Hand this file to the coding assistant. Save it in the repo as `docs/fix_spec_round2.md`.

## Context

SYN-003 was built independently of the round-1 fixes, with labels committed before any run
(commit 831e76d). Three runs on the frozen round-1 code (`data/eval/syn003_runs/`) found:

1. **Cancer-history exclusion cleared unsafely (4 of 6 evaluations).** NCT07559760 EXC-19,
   "Other malignancies within 5 years, except adequately treated basal-cell carcinoma of skin
   or cervical carcinoma in situ." Two forms of the same error:
   - Control: "No other malignancies ... are documented. Therefore ... does not apply."
     (clearance from absence)
   - Control: "Since the BCC was excised ... adequately treated, and therefore the exclusion
     ... does not apply." (the excepted condition treated as clearing the whole criterion)
   The general clearance guard did not fire because the basal-cell carcinoma was cited, so the
   exclusion counted as "addressed." The prior-exposure absence guard covers drugs only.
2. **Label contradicts its own explanation (run 1, SYN-003).** The explanation ends "the
   exclusion applies," but the recorded status was MEETS (clear).
3. **Scheduled first study dose never extracted.** "Cycle 1 day 1 ... scheduled for
   2026-04-20" appears only in the uncovered-lines list. The washout therefore stayed UNKNOWN
   even though both dates are documented.
4. **Uncovered-lines list is noisy.** 15 to 20 lines per patient, including headings and
   sentences that were extracted but wrap across two lines.

## Ground rules (same as round 1, plus three)

- Do not change any label file, patient document, existing run folder, or blind-results
  document (SYN-001, SYN-002, SYN-003).
- Do not create SYN-004 or any new test patient. It is built separately, after these fixes are
  frozen, and its labels are signed before any run.
- Keep every change general. No special cases for Hodgkin lymphoma, basal-cell carcinoma,
  pembrolizumab, specific trials, or patient filenames.
- **Code decides what code can decide.** Date arithmetic and label/explanation consistency are
  computed in code, never left to the model.
- **Design each fix from the root cause above, then test.** If a fix needs more than two
  attempts against SYN-002 or SYN-003, stop and report instead of tuning further. Keep every
  attempt's outputs, as in round 1.
- One commit per fix. All existing tests must pass; report before and after counts.

## Fix A: no clearance of history exclusions without explicit evidence

Files: `src/safety.py` (`review_assessments` and the clearance guards).

Applies to exclusions about a history of a condition or disease (for example "other
malignancies within N years," "history of X," "prior diagnosis of X"), not only prior drugs.

- An exclusion may be marked MEETS (clear) only if cited, verified evidence explicitly rules
  out the condition at the scope of the criterion (for example "no history of cancer").
- A negation narrower than the criterion does not clear it ("no history of blood cancer" does
  not rule out other malignancies).
- **Evidence that only matches an exception clause does not count as addressing the
  criterion.** If the criterion contains "except ..." and every cited fact matches an excepted
  condition, a MEETS becomes UNKNOWN with a flag.
- Otherwise a MEETS becomes UNKNOWN with a visible flag naming the reason (absence, excepted
  condition only, or narrower negation).
- DOES_NOT_MEET answers supported by cited evidence of a non-excepted condition are unchanged.

Done when, with unit tests:
- excepted-condition-only evidence plus MEETS gives UNKNOWN and a flag
- no relevant evidence plus MEETS gives UNKNOWN and a flag
- a narrower negation ("no history of blood cancer") plus MEETS gives UNKNOWN and a flag
- explicit scope-matching negation ("no history of cancer") plus MEETS stays MEETS
- a cited non-excepted cancer within the window plus DOES_NOT_MEET stays DOES_NOT_MEET

## Fix B: the label must match its own explanation

Files: `src/safety.py`, `src/eligibility.py` if a structured field helps.

- After the model answers, check in code that the status agrees with the explanation's final
  conclusion. For exclusions: a clear status (MEETS) with a conclusion that the exclusion
  applies, or the reverse, is a contradiction. Same idea for inclusions.
- Preferred approach: ask the model for a separate short structured field stating its final
  conclusion (for example `exclusion_applies: true/false/unknown`) and compare it to the
  status in code. A keyword check on the explanation is an acceptable fallback, but must
  handle negations.
- On contradiction: convert to UNKNOWN with the flag "status contradicts explanation" and keep
  the original reasoning visible.

Done when: a unit test with an explanation concluding "the exclusion applies" and status MEETS
gives UNKNOWN plus the flag; a consistent answer is unchanged.

## Fix C: extract planned study dates and compute time windows in code

Files: `src/schemas.py` (category), `src/config.py`, `src/evidence_extraction.py`,
`src/safety.py` (time-window guard).

- Add an evidence category for planned or scheduled study events (for example
  `planned_study_event`) with the date in `date` and the exact quote. The extractor must record
  scheduled first study dose or cycle 1 day 1 when the source states it.
- For time-window exclusions ("within N days/weeks/months before first study dose"), when cited
  evidence includes both a dated administration and a planned first-dose date, **code computes
  the interval** and decides: inside the window gives DOES_NOT_MEET; outside the window gives
  UNKNOWN, because the absence of later therapy in the record does not prove none was given.
  The model's arithmetic is never used.
- If either date is missing, keep the round-1 behavior (UNKNOWN with flag).
- Record the computed interval in the explanation and flags.

Done when: on SYN-003, EXC-05 cites the 2026-04-08 administration and the 2026-04-20 planned
dose, the explanation shows a code-computed 12-day interval, and the status is DOES_NOT_MEET.
Unit tests cover inside window, outside window, and missing reference date.

## Fix D: make the uncovered-lines list useful

Files: `src/evidence_extraction.py` (`uncovered_content_lines`).

- Join wrapped lines into sentences before checking coverage; a sentence counts as covered if a
  verified quote covers it after whitespace normalization.
- Skip document titles and section headings (short lines without sentence punctuation, in
  addition to the administrative lines already skipped).
- Report sentences, not raw lines, with file and page.

Done when: on SYN-003 the list no longer contains headings or the extracted Hodgkin and
pembrolizumab sentences, and still contains genuinely unextracted sentences (for example family
history, or the screening-letter sentence if Fix C did not capture it). Report the before and
after count per patient.

## Testing and reporting

1. Full offline test suite, with new tests for A to D. Report before and after counts.
2. SYN-001 regression (in-sample and held-out); report any change.
3. SYN-002: three runs to `data/eval/syn002_runs_round2/run1..3`.
4. SYN-003: three runs to `data/eval/syn003_runs_round2/run1..3`, labeled "after round-2
   fixes, not blind."
5. A summary in the same format as before, with exact and acceptable scores, unsafe
   clearances, guard interventions (which guard, how often), and anything that got worse. Do
   not merge with earlier results.
6. Freeze the code (record the commit) when done. SYN-004 runs on that frozen commit.

## Out of scope

Retrieval, trial data, UI layout beyond the uncovered-sentences list, new patients or labels.
