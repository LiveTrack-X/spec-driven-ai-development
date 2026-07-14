# Evidence-Based Handoff Prompt

Prepare a compact handoff for an SDAD Protocol project only when another
session, tool, model, person, or machine needs continuity.

For state v2, the optional `current_handoff` field in `sdad-state.yaml` is the
sole current continuity pointer. Do not create or route `save-state.md`; an
existing save-state is state-v1 migration input only. Do not add the handoff to
startup context or `routed_docs` merely because it exists.

Write the handoff under:

```text
docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md
```

Use `HNNNN` as a zero-padded repository-logical sequence. Select an ID greater
than every repository-known numbered handoff, including archived numbered
handoffs; never reuse, fill a gap, or renumber an ID. The date is descriptive
only and does not establish order or currentness. Legacy `YYYY-MM-DD-topic.md`
handoffs remain valid and need no mass rename.

Use this exact structure:

```markdown
# SDAD Session Handoff

## 1. Session Identity

- Handoff ID: H0001
- Active packet: [packet:WP-EXAMPLE]
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
- Active SPEC / acceptance criteria:
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
- Authoritative authorization record, if any:
- Last-observed authorization status:
- Blockers or residual risk:

## 6. Resume Instructions

- Start route: adapter -> `sdad-state.yaml` -> `docs/INDEX.md`.
- Confirm this path is still `current_handoff` and its marker still matches the
  active packet.
- Inspect current source/tests and only the targeted Authority Pointers needed
  for the next decision.
- Repository truth overrides this checkpoint.
```

The first exact `## 1. Session Identity` section must contain exactly one
handoff ID matching the filename and exactly one valid packet marker. Start
from `- Handoff ID: H0001` and
`- Active packet: [packet:WP-EXAMPLE]`; replace `H0001` with the allocated ID
and `WP-EXAMPLE` with the exact `sdad-state.yaml#active_packet.id` value.

## Authority And Compression Rules

- Intended scope, behavior, or acceptance criteria -> state-declared `active_spec`.
- Observed behavior -> current source, tests, runtime, and reproducible commands.
- Small spec-unstated implementation decision -> implementation notes.
- Hard-to-reverse architecture decision -> ADR.
- Unresolved work -> TODO or review finding.
- Current execution declaration -> `sdad-state.yaml`.
- Protected-action authorization -> authoritative owner-decision record.
- Cross-session recovery links/results -> handoff.

Use Authority Pointers; do not duplicate full SPEC decisions, ADR rationale,
TODOs, findings, implementation notes, logs, diffs, or evidence files. State
claim limits, skipped checks, residual risk, and owner acceptance separately.
Evidence-ready is not owner-accepted.

Point to the single authoritative owner-authorization record and include only
its last-observed status in the handoff. The handoff itself is never reusable
authority. Reuse the authorization only after verifying that its recorded
packet, action, conditions, expiry, required evidence, and source/artifact identity remain
unchanged. An expired or failed condition, or a relevant source change, requires
re-approval.

## Pointer Lifecycle

After writing the file, add or update `current_handoff` only when this is the
real current resume checkpoint. Keep INDEX sourced from the state pointer:

```text
- Current handoff: use ../sdad-state.yaml#current_handoff when declared.
```

On packet switch, completion, archive, or replacement, remove or replace the
pointer in the same coherence update. Never leave a handoff for another packet
declared current. Never infer currentness from the date or greatest handoff ID.

A small correction updates the same checkpoint. A materially new recovery
checkpoint gets the next ID. If parallel branches allocate the same ID, resolve
the collision before merge by updating the filename, internal ID, and state
pointer together.

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
