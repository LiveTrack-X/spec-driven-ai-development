# SPEC-Driven AI Development Session Instructions

Use this file when an AI coding tool has no special project-instruction format.

You are working in an owner-supervised, SPEC-driven, multi-agent,
evidence-based development workflow.

## Start

Read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md`
5. `review-findings.md`
6. `SPEC/SPEC-COMPLETE.md`
7. relevant source code and tests

## Source Of Truth

Current code, tests, migrations, and reproducible commands beat docs. Active
docs beat SPEC. Current active SPEC beats older SPEC history. Handoff and
archives are context, not authority.
Owner decisions control scope, risk tolerance, and acceptance.

## Rules

- Evidence beats confidence.
- Active scope beats interesting future ideas.
- Owner decision beats AI momentum.
- Docs drift is a bug.
- Partial, degraded, skipped, or unverified behavior must be labeled.
- Failed, missing, skipped, timed-out, or unrun tests must be reported plainly.
- Repeated pain becomes a rule, checklist, test, or template update.
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

## Handoff

Report autonomy level used, work packet completed, evidence-ready units, changed
files, behavior changed, tests/commands run, docs checked, remaining risks,
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
