# SDAD Session Handoff

Use this only as a compact cross-session recovery checkpoint. Link to current
authorities; do not copy full SPEC decisions, ADR rationale, TODOs, findings,
implementation notes, or long command/file logs into the handoff.

## 1. Session Identity

- Active packet: [packet:bootstrap]
- Repository / worktree:
- Branch / HEAD:
- Dirty state:
- Date:

## 2. Resume Checkpoint

- Current goal:
- Next concrete action:
- Why continuity is needed:

## 3. Authority Pointers

- Current state: `sdad-state.yaml`
- Active SPEC / acceptance:
- Relevant TODO or finding:
- Implementation note or ADR, if any:

## 4. Last Observed Validation

- Command or check:
- Result and date:
- Bounded claim supported:
- Unverified or stale evidence:

## 5. Open Constraints And Gates

- Constraints / do-not-touch areas:
- Unsatisfied owner gates:
- Blockers or residual risk:

## 6. Resume Instructions

First load the installed tool adapter, `sdad-state.yaml`, and `docs/INDEX.md`.
Confirm that this handoff is still the state-declared current checkpoint, then
inspect current source/tests and only the targeted authorities above. Use
bounded reads for archives, old handoffs, generated artifacts, logs, and
authorized private data. If repository truth conflicts with this checkpoint,
follow repository truth and update the authoritative record before continuing.
