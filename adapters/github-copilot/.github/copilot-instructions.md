# SPEC-Driven AI Development Instructions

Use owner-supervised, SPEC-driven, evidence-based development in this repository.

## Required Reading

Before implementation, review:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. `SPEC/SPEC-COMPLETE.md`
4. `docs/TODO-Open-Items.md`
5. `review-findings.md`
6. relevant source code and tests

## Source Of Truth

Prefer current code, migrations, tests, and reproducible commands over docs.
Prefer active docs over SPEC. Prefer current active SPEC sections over older
historical SPEC sections. Treat handoffs and archive/history as context, not
authority.

## Review And Implementation Rules

- Evidence beats AI confidence.
- Do not claim completion from AI confidence.
- Keep changes scoped to the active SPEC slice.
- Do not promote future ideas into active work without owner decision.
- Label partial, scaffolded, degraded, skipped, environment-limited, or unverified behavior.
- Update docs or state which docs were checked and why no update was needed.
- Treat critical review findings, failing tests, security regressions, and release blockers as higher priority than new features.
- For release or production readiness, require migration, security, backup/restore, monitoring, rollback, and manual evidence as applicable.
- Default to Level 2 Work Packet Autonomy for normal Standard SDAD work.
- Work in review-worthy development units inside the approved packet, not
  micro-approval steps.
- Continue autonomously inside the approved work packet until evidence is ready.
- Stop for owner input only when scope expands, Q5 risk changes, destructive or
  irreversible action is needed, an owner-controlled decision is required,
  verification is blocked, or evidence conflicts with the plan.
- Implementation discipline guards autonomy: surface assumptions, prefer the
  simplest working design, make surgical changes, and tie every step to
  verification.

## Response Expectations

When summarizing work, include autonomy level used, work packet completed,
evidence-ready units, changed files, tests run, docs checked, remaining risks,
incomplete work, owner decisions needed, owner acceptance status, and next
concrete steps.

Long AI coding sessions are execution traces, not permanent memory. Before
closing, archiving, replacing, or restarting a long session, create or update a
session handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`. A fresh session
must continue from the handoff, active SPEC, and current repository state.

## Save-State Update Triggers

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct. If no trigger applies, say so.
