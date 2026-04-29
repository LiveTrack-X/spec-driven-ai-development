# SPEC-Driven AI Development

Status: Active
Scope: Claude Code project memory

Use this project with owner-supervised, SPEC-driven, multi-agent,
evidence-based development.

## Start Here

Before code, SPEC, prompt, or documentation work:

1. Read `docs/INDEX.md`.
2. Read `docs/Repository-Operating-Rules.md`.
3. Read active docs routed from `docs/INDEX.md`.
4. Read `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work.
5. Read `SPEC/SPEC-COMPLETE.md` and any relevant active SPEC.
6. Inspect current source code and tests before implementing from a plan.

Do not start from archived docs, old handoffs, product notes, or historical SPEC
sections without checking the current route.

## Source Of Truth

When sources conflict, prefer:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical SPEC,
4. active SPEC files,
5. current handoff files,
6. product notes and external references,
7. historical or archived records,
8. chat memory or AI confidence.

If a SPEC spans past-to-present history, current active sections override older
historical sections.

## Non-Negotiable Rules

- Evidence beats confidence.
- Active scope beats interesting future ideas.
- Open critical findings beat feature expansion unless the owner accepts the risk.
- Explicit non-goals beat assumptions.
- Partial, scaffolded, degraded, skipped, or unverified behavior must be labeled.
- Docs drift is a bug.
- Handoff is context, not authority.
- Release readiness beats feature count.
- Owner decision beats AI momentum.
- Repeated pain becomes a rule, checklist, test, or template update.

## Work Style

- Keep implementation units small enough to review and large enough to matter.
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
- Do not claim completion without commands, results, docs checked, and remaining risks.
- Use separate review or QA passes for high-risk changes.
- Do not silently promote product notes, external references, or future ideas into active work.
- If docs do not need content changes, state which docs were checked and why.

## Handoff Required

Every handoff must include:

- changed files,
- autonomy level used,
- work packet completed,
- evidence-ready units,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- open findings,
- remaining risks,
- partial/degraded/unverified behavior,
- what is not complete,
- owner decisions needed,
- owner acceptance status.

## Save-State Update Triggers

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct. If no trigger applies, say so.
