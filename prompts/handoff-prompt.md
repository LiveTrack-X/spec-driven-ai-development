# Evidence-Based Handoff Prompt

Prepare a handoff for an owner-supervised, SPEC-driven AI development project.

The handoff must let another AI session continue without guessing.

## Include

- current goal,
- review-worthy development unit completed,
- changed files,
- behavior changed,
- tests and commands run,
- test results,
- docs checked or updated,
- open findings,
- remaining risks,
- current active SPEC section used, especially if older SPEC history exists,
- implicit assumptions converted into explicit rules, if any,
- ADRs created or needed, if any,
- partial, degraded, skipped, or unverified behavior,
- version-lane or migration sync status, if applicable,
- release or production-readiness gate status, if applicable,
- next recommended slice,
- what is not complete,
- owner decisions needed.

## Rules

- Do not claim production readiness without deployment, migration, auth/security, backup/restore, monitoring, and rollback evidence as applicable.
- Do not let older SPEC history override newer active SPEC instructions.
- Do not rely on obvious-but-unwritten assumptions.
- Do not request owner approval after every micro-task when the work stayed
  inside the approved review-worthy unit.
- Do not bury blockers in prose. Put active defects in `review-findings.md`.
- Do not leave future ideas mixed into active implementation work.
- Do not claim release readiness while Critical findings remain open.
- Update `save-state.md` when work pauses or stops mid-stream, handoff to another
  AI/tool/person is expected, owner direction or acceptance criteria changed,
  blocked/partial/unverified state remains, or context would be expensive to
  reconstruct.
- If the project uses `next-task.md`, update it when the next slice changed.
