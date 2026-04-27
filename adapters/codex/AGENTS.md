# SPEC-Driven AI Development Agent Rules

Status: Active
Scope: Codex project instructions

## Mandatory First Read

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. `SPEC/SPEC-COMPLETE.md` and relevant active SPECs

## Operating Rules

- Current active code, tests, docs, and SPEC sections beat older SPEC history.
- Evidence beats AI confidence.
- Active scope beats interesting future ideas.
- Partial, degraded, skipped, or unverified behavior must be labeled.
- Critical review findings beat feature expansion unless the owner accepts the risk.
- Documentation consistency must be checked before handoff.
- Owner direction, risk tolerance, and acceptance decisions are controlling.
- Default to Level 2 Work Packet Autonomy for normal Standard SDAD work.
- Work in review-worthy development units, not micro-approval steps.
- Continue autonomously inside the approved unit or work packet until evidence
  is ready.
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

State autonomy level used, work packet completed, evidence-ready units, changed
files, behavior changed, tests run, docs checked, open findings, remaining
risks, incomplete work, owner decisions needed, and owner acceptance status.

## Save-State Update Triggers

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct. If no trigger applies, say so.
