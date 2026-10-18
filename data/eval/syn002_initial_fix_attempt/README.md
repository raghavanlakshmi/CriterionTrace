# Initial after-fix attempt (not blind; superseded)

These live outputs were preserved rather than discarded. This batch completed
SYN-001 in-sample and held-out evaluations and SYN-002 run1, then was interrupted
at the start of run2. The evaluated local revision was 8c59d42 before the local
four-fix commits were organized with fixups.

Run1 exposed two implementation gaps: the study-date guard did not recognize
hyphenated reference wording, and the assessor selected unverified recovery
records alongside a verified quote. The final implementation recognizes generic
hyphenated study anchors and restricts model citation candidates to verified
records while retaining unverified records for review.

Do not count this batch as the final three after-fix runs. Those are saved in
`../syn002_runs_after_fix/`. Blind inputs and results were not changed.

Implementation checkpoint: `8c59d42`. `implementation.patch` reconstructs that attempted implementation from base commit `dc41e5c`; the final four-fix history was organized separately before integration.
