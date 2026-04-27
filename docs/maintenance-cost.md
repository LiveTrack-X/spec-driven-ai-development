# Maintenance Cost

SPEC-Driven AI Development is a control layer, not a free checklist.

If you create control files, you must keep them current. Otherwise the workflow
creates stale authority, which is worse than having no workflow.

## The Cost

Standard and Full SDAD require a small maintenance pass at the end of every
review-worthy development unit, not after every micro-task.

Before handoff or owner acceptance, update or explicitly check:

- `SPEC/SPEC-COMPLETE.md` when product behavior, implementation status, scope,
  constraints, or acceptance criteria changed,
- `docs/TODO-Open-Items.md` when work was completed, added, deferred, or split,
- `review-findings.md` when bugs, risks, review findings, or blocked issues were
  found, fixed, deferred, or accepted,
- `docs/Repository-Operating-Rules.md` when repeated pain becomes a durable rule,
- ADRs when architecture, policy, release, security, data-boundary, or owner
  tradeoff decisions need durable rationale,
- `save-state.md` when work is paused, handed off, direction changes, or the
  next session would otherwise need to reconstruct context.

If no file needs a content change, the handoff must say which control files were
checked and why no update was needed.

## End-Of-Loop Rule

Every SDAD loop ends at a review-worthy unit boundary:

```text
Review-worthy unit -> Build -> Review -> Evidence -> Owner decision -> Update control files
```

Do not claim completion while control files are stale.

Completion requires:

- evidence,
- owner acceptance or requested changes,
- updated TODO/review/SPEC state,
- known stale items explicitly named.

## Save-State Update Triggers

`save-state.md` is optional. If the project uses it, it must stay current enough
for the next AI session or human maintainer to resume without guessing.

Update `save-state.md` when any of these happen:

- a session is ending or pausing before the project is fully accepted,
- an active slice completes and the next slice is not obvious from TODO/SPEC,
- the owner changes direction, priority, acceptance criteria, or risk tolerance,
- work is blocked, skipped, partial, degraded, or unverified,
- another AI tool, model, session, or person is expected to continue the work,
- current context would be expensive to reconstruct from code and docs alone,
- a decision changes what the next session should do first.

If none of these triggers apply, no save-state update is required. If
`save-state.md` exists but is stale, update it, mark it stale, or archive it
before handoff. Stale save-state is context, not authority; current code, tests,
active docs, and active SPEC still win.

## Scale Implication

If this maintenance cost is too high, choose a smaller scale:

- One-shot prompt: no persistent files.
- Mini SDAD: one instruction file and a short handoff.
- Standard SDAD: core control files kept current every loop.
- Full SDAD: core files plus review, ADRs, release/risk gates, and stronger
  documentation consistency.

The right workflow is the largest one you can keep current, not the largest one
you can generate once.

## Stale File Warning

Stale control files cause common failures:

- old SPEC sections override current code,
- completed TODOs look open,
- known bugs disappear from review,
- AI sessions trust outdated docs,
- owners get false progress signals.

Treat stale control files as a project bug.
