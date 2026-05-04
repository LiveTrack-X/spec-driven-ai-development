# Evidence-Based Handoff Prompt

Prepare a handoff for an owner-supervised, SPEC-driven AI development project.

The handoff must let another AI session continue without guessing or relying on
the previous chat context. Treat the chat as an execution trace, the active SPEC
as authority, and the handoff as the continuity artifact.

For Standard or Full SDAD, write session handoffs under:

```text
docs/sdad/handoffs/YYYY-MM-DD-topic.md
```

## Include

- current goal,
- autonomy level used,
- work packet completed,
- evidence-ready units,
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
- owner acceptance status,
- owner decisions needed,
- reactivation prompt for a fresh AI session.

## Rules

- Do not claim production readiness without deployment, migration, auth/security, backup/restore, monitoring, and rollback evidence as applicable.
- Do not let older SPEC history override newer active SPEC instructions.
- Do not rely on obvious-but-unwritten assumptions.
- Do not request owner approval after every micro-task when the work stayed
  inside the approved work packet.
- Do not treat evidence-ready as owner-accepted unless the owner delegated that
  acceptance policy.
- Do not treat a long chat transcript as permanent memory.
- When asked to restart, summarize, archive, or continue later, offer to create
  or update a handoff first.
- Fresh sessions must load the relevant spec, handoff, and current repository
  state before continuing.
- Do not include speculative abstractions, drive-by refactors, or unrelated
  cleanup in the packet handoff as if they were requested work.
- Do not bury blockers in prose. Put active defects in `review-findings.md`.
- Do not leave future ideas mixed into active implementation work.
- Do not claim release readiness while Critical findings remain open.
- Update `save-state.md` when work pauses or stops mid-stream, handoff to another
  AI/tool/person is expected, owner direction or acceptance criteria changed,
  blocked/partial/unverified state remains, or context would be expensive to
  reconstruct.
- If the project uses `next-task.md`, update it when the next slice changed.
