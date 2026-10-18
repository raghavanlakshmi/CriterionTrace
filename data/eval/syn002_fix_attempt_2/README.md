# Second implementation attempt (after fixes, not blind; superseded)

This completed three-run batch is preserved with its original summary, reports,
evidence, and validation metadata. It found all seven labs, BRAF, and treatment
administrations, but verified biopsy evidence was missing in five of six patient
evaluations. Some recovery records contained unsupported scalar or UNKNOWN values.
The prior-malignancy exclusion was unsafely cleared in all three buried variants.

The next revision adds deterministic extraction for explicit clinical field
labels, rejects placeholder and unsupported sex records, and fixes consistent
stemming of generic terms in the existing exclusion-clearance guard. These are
general changes, without patient, filename, drug, or trial special cases.

The final confirmation batch is in ../syn002_runs_after_fix/. Do not combine the
tables or describe these attempts as blind. No frozen inputs or results changed.

Implementation checkpoint: `6688ee1f0e2d21883dffa4e6d88c577fc1907ed4`. `implementation.patch` reconstructs that attempted implementation from base commit `dc41e5c`; the final four-fix history was organized separately before integration.
