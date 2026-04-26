# Evidence-Based Handoff Prompt

Prepare a handoff for an owner-supervised, SPEC-driven AI development project.

The handoff must let another AI session continue without guessing.

## Include

- current goal,
- changed files,
- behavior changed,
- tests and commands run,
- test results,
- docs checked or updated,
- open findings,
- remaining risks,
- version-lane or migration sync status, if applicable,
- release or production-readiness gate status, if applicable,
- next recommended slice,
- what is not complete,
- owner decisions needed.

## Rules

- Do not claim production readiness without deployment, migration, auth/security, backup/restore, monitoring, and rollback evidence as applicable.
- Do not bury blockers in prose. Put active defects in `review-findings.md`.
- Do not leave future ideas mixed into active implementation work.
- Do not claim release readiness while Critical findings remain open.
- If work stopped mid-stream, update `save-state.md` and `next-task.md` if the project uses them.
