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
- SDAD scale / intensity used,
- control-file budget used: Minimal, Normal, or Heavy,
- autonomy level used,
- compressed owner review summary:
  - one-line status,
  - changed user-facing behavior,
  - safety boundary touched: yes/no,
  - checks summary,
  - owner decision needed: yes/no,
  - recommended next action,
  - links or references to detailed evidence,
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
- advanced extension fit-gate status, if applicable,
- search evidence versus owner acceptance evidence, if applicable,
- evaluation leakage risk, if applicable,
- concrete budget used for expensive or repeated eval loops, if applicable,
- context-stability notes:
  - large files or archives that should not be read in full,
  - active summaries to read first,
  - archive/history locations,
  - bounded-read instructions,
- next recommended slice,
- what is not complete,
- owner acceptance status,
- owner decisions needed,
- reactivation prompt for a fresh AI session.

## Rules

- Do not claim production readiness without deployment, migration, auth/security, backup/restore, monitoring, and rollback evidence as applicable.
- Do not let older SPEC history override newer active SPEC instructions.
- Do not rely on obvious-but-unwritten assumptions.
- State SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
- Do not request owner approval after every micro-task when the work stayed
  inside the approved work packet.
- Do not treat evidence-ready as owner-accepted unless the owner delegated that
  acceptance policy.
- Do not treat a long chat transcript as permanent memory.
- Do not make a fresh session read large state files, archives, logs, generated
  artifacts, private data, or old handoffs in full. Provide bounded-read
  instructions instead.
- Use the default soft triggers unless the project defines stricter limits:
  bounded reads above 50 KB or 500 lines, context-stability check above 200 KB
  or 2,000 lines, and no full startup read above 1 MB unless the owner asks for
  historical reconstruction.
- When asked to restart, summarize, archive, or continue later, offer to create
  or update a handoff first.
- Fresh sessions must load the relevant spec, handoff, and current repository
  state before continuing.
- Do not include speculative abstractions, drive-by refactors, or unrelated
  cleanup in the packet handoff as if they were requested work.
- Do not bury blockers in prose. Put active defects in `review-findings.md`.
- Do not leave future ideas mixed into active implementation work.
- Do not claim release readiness while Critical findings remain open.
- Do not claim generalized improvement from eval-driven work if search evidence
  and owner acceptance evidence are the same set.
- If an advanced extension was used, record unknown or blocking fit-gate fields
  instead of hiding them as assumptions.
- Update `save-state.md` when work pauses or stops mid-stream, handoff to another
  AI/tool/person is expected, owner direction or acceptance criteria changed,
  blocked/partial/unverified state remains, or context would be expensive to
  reconstruct.
- If the project uses `next-task.md`, update it when the next slice changed.
- If active state files became long or chat stability degraded, preserve old
  material in archive/history files, keep active summaries compact, and update
  routing before resuming feature work.
