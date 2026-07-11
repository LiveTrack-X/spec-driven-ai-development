# Evidence-Based Handoff Prompt

Prepare a compact handoff for an SDAD Protocol project only when another
session, tool, model, person, or machine needs continuity.

For state v2, the optional `current_handoff` field in `sdad-state.yaml` is the
sole current continuity pointer. Do not create or route `save-state.md`; an
existing save-state is state-v1 migration input only. Do not add the handoff to
startup context or `routed_docs` merely because it exists.

Write the handoff under:

```text
docs/sdad/handoffs/YYYY-MM-DD-topic.md
```

Use this exact structure:

```markdown
# SDAD Session Handoff

## 1. Session Identity

- Active packet: [packet:<active_packet.id>]
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
- Active conditional authorization, if any:
  - Decision:
  - Authorized action:
  - Packet:
  - Conditions:
  - Expires when:
  - Evidence required before action:
- Blockers or residual risk:

## 6. Resume Instructions

- Start route: adapter -> `sdad-state.yaml` -> `docs/INDEX.md`.
- Confirm this path is still `current_handoff` and its marker still matches the
  active packet.
- Inspect current source/tests and only the targeted Authority Pointers needed
  for the next decision.
- Repository truth overrides this checkpoint.
```

The first exact `## 1. Session Identity` section must contain exactly one valid
marker in the exact form `- Active packet: [packet:<id>]`. Its ID must equal
`sdad-state.yaml#active_packet.id`.

## Authority And Compression Rules

- Requirement or acceptance change -> active SPEC.
- Small spec-unstated implementation decision -> implementation notes.
- Hard-to-reverse architecture decision -> ADR.
- Unresolved work -> TODO or review finding.
- Current execution declaration -> `sdad-state.yaml`.
- Cross-session recovery links/results -> handoff.

Use Authority Pointers; do not duplicate full SPEC decisions, ADR rationale,
TODOs, findings, implementation notes, logs, diffs, or evidence files. State
claim limits, skipped checks, residual risk, and owner acceptance separately.
Evidence-ready is not owner-accepted.

Preserve an owner authorization only while its recorded packet, action,
conditions, expiry, required evidence, and source remain unchanged. An expired
or failed condition, or a relevant source change, requires re-approval.

## Pointer Lifecycle

After writing the file, add or update `current_handoff` only when this is the
real current resume checkpoint. Keep INDEX sourced from the state pointer:

```text
- Current handoff: use ../sdad-state.yaml#current_handoff when declared.
```

On packet switch, completion, archive, or replacement, remove or replace the
pointer in the same coherence update. Never leave a handoff for another packet
declared current.

## Bounded-Read Instructions

The next session must not assume previous chat context. It should read the
adapter, state, and INDEX first; inspect current source/tests; then select only
the handoff pointers needed for its intent. Use bounded reads for archives, old
handoffs, generated artifacts, logs, databases, and authorized private data.
Report only routed documents actually read.

Include a short reactivation prompt with those instructions. Do not claim that
writing Markdown technically blocks tools or proves validation. Record which
validation ran, the observable result, the bounded claim it supports, and what
remains unverified.
