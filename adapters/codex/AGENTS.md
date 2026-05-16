# SPEC-Driven AI Development Agent Rules

Status: Active
Scope: Codex project instructions

## Mandatory First Read

Context Stability applies before every item in this start loop. Inspect file
size first and use bounded reads for large routed files.

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. `SPEC/SPEC-COMPLETE.md` and relevant active SPECs

## Context Stability

Mandatory first reads are routing requirements, not permission to dump large
files into chat context. Before opening large state files, archives, logs,
generated artifacts, private data, or broad search results, check size and use
bounded reads: headings, current sections, targeted matches, output limits, and
explicit excludes.

Keep active live-state files short. If an AI chat becomes unstable, suspect
context growth from large files or broad searches before changing runtime code.
Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

## Operating Rules

- Current active code, tests, docs, and SPEC sections beat older SPEC history.
- Evidence beats AI confidence.
- Active scope beats interesting future ideas.
- Partial, degraded, skipped, or unverified behavior must be labeled.
- Critical review findings beat feature expansion unless the owner accepts the risk.
- Documentation consistency must be checked before handoff.
- Owner direction, risk tolerance, and acceptance decisions are controlling.
- Default to Level 2 Work Packet Autonomy for normal Standard SDAD work.
- State SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
- Work in review-worthy development units inside the approved packet, not
  micro-approval steps.
- Continue autonomously inside the approved work packet until evidence is ready.
- Stop for owner input only when scope expands, Q5 risk changes, destructive or
  irreversible action is needed, an owner-controlled decision is required,
  verification is blocked, or evidence conflicts with the plan.
- Implementation discipline guards autonomy: surface assumptions, prefer the
  simplest working design, make surgical changes, and tie every step to
  verification.

## Source Of Truth

Prefer code, tests, migrations, and reproducible commands over docs. Prefer
active docs over SPEC. Prefer current active SPEC sections over older SPEC
history. Treat handoff and save-state files as context, not authority.

## Handoff

State SDAD scale / intensity used, autonomy level used, work packet completed,
evidence-ready units, changed files, behavior changed, tests run, docs checked,
open findings, remaining risks, incomplete work, owner decisions needed, owner
acceptance status, and next concrete steps.

Long AI coding sessions are execution traces, not permanent memory. Before
closing, archiving, replacing, or restarting a long session, create or update a
session handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`. A fresh session
must continue from the handoff, active SPEC, and current repository state.

## Save-State Update Triggers

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct. If no trigger applies, say so.
