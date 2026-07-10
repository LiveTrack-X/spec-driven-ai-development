# Work Packets Playbook

Status: On demand
Trigger: scale selection, autonomy, intensity, planning, or implementation

## Scale Selection

Use the smallest persistent control surface that protects the work:

- One-shot: zero scale questions are yes; create no persistent files.
- Mini: one or two yes answers from session/return/evidence questions only,
  with multi-tool and Q5 risk both no; keep one instruction file.
- Standard: multi-tool work, three yes answers, persistent state, or a packet
  that only inspects, documents, or tests a Q5 area.
- Full: four or five yes answers, or a packet that changes, accepts, or executes
  a release, production, migration, destructive-action, real-data, auth, money,
  security, rollback, or equivalent Q5 gate.

Re-evaluate scale only when duration, collaboration, evidence, or risk changes.
Do not escalate because a document exists; do not compress away a live gate.

## Work Packet And Unit

A work packet is the owner-approved objective, boundaries, non-goals, evidence
expectations, and stop conditions. A review-worthy unit is an internal slice
large enough to review and small enough to verify at one checkpoint. Multiple
related TODOs may belong to one unit.

Default Standard work to Level 2 Work Packet Autonomy. Mini uses Level 1 for
its single bounded unit. Full normally uses Level 2 implementation with Level 4
owner gates for release, migration, destructive action, data/auth/money/
security decisions, rollback, and production claims.

Do not request owner approval after each micro-task or evidence-ready unit.
Continue inside the packet until evidence-ready unless a stop condition fires.

## Operating Intensity

Intensity is separate from scale and autonomy:

- Low: docs-only, index, typo, helper split, small test/check, or template edit.
- Medium: normal implementation, validation, review, and docs synchronization.
- High: behavior/policy/boundary/claim changes, hard-to-reverse tradeoffs, or an
  explicit owner checkpoint.

A Q5 project does not make every packet High. Raise only the packet that changes
the Q5 gate. Lower intensity when control surfaces reduce controllability.

## Clarification Checkpoint

When a plan is fuzzy, inspect current repository evidence, active SPEC, state,
TODOs, findings, and relevant decisions first. Ask only the next unresolved
blocking question, include a recommended default, and explain what changes
with another answer. Clarification is not micro-approval.

## Implementation Memory

Record a spec-unstated assumption, compromise, rejected alternative,
owner-relevant tradeoff, follow-up, and verification impact in
`docs/implementation-notes.md`. Do not record raw internal reasoning,
mechanical edits, or large logs. Create an ADR only when the decision is hard to
reverse, surprising without context, and represents a real tradeoff.

## Stop Conditions

Stop for owner input when scope expands, a risk or evidence claim gate changes,
an irreversible action is required, an owner-controlled tradeoff remains,
verification is blocked, or evidence conflicts with the plan. Otherwise keep
working to evidence-ready.
