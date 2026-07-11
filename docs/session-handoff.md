# Session Handoff And Context Continuity

A handoff is an optional, compact cross-session recovery checkpoint. It is not
live state and it is not a second copy of the project's authorities.

For state v2, `sdad-state.yaml#current_handoff` is the sole current continuity
pointer. Do not create or route `save-state.md` for new v2 projects. An existing
`save-state.md` is state-v1 migration input only: preserve and classify it during
the read-only migration preview, but do not use it as current v2 authority.

## Authority And Continuity

- Chats are execution traces, not durable authority.
- Source, tests, runtime evidence, and the active SPEC establish product truth.
- `sdad-state.yaml` declares the current executable packet and validation
  contract.
- A handoff links to authorities and last observed results for recovery.
- Owner decisions authorize protected actions and record acceptance.

Handoff-only decisions are continuity hints. Put each durable fact in one home:

| Fact | Authoritative home |
| --- | --- |
| Requirement or acceptance change | active SPEC |
| Small spec-unstated implementation decision | `docs/implementation-notes.md` |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or review finding |
| Current execution declaration | `sdad-state.yaml` |
| Protected-action authorization | authoritative owner-decision record |
| Cross-session recovery links/results | current handoff |

Use an `## 3. Authority Pointers` section rather than copying SPEC text, ADR
rationale, TODOs, findings, implementation notes, or long command output.

## When To Create A Handoff

Create one only when another session, tool, model, person, or machine needs a
recovery checkpoint. Do not create one after every unit or packet. Ask to create
or update it first only when ending the session would otherwise lose needed
continuity.

A handoff is not part of fixed startup context. Read it only for resume/handoff
intent or another concrete continuity need, and then read only the targeted
authority pointers needed for the next decision.

## Current Pointer Lifecycle

1. Write the handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`.
2. In its first exact `## 1. Session Identity` section, include exactly one
   canonical example marker: `- Active packet: [packet:WP-EXAMPLE]`. When
   writing the handoff, replace `WP-EXAMPLE` with the exact
   `sdad-state.yaml#active_packet.id` value.
3. Set optional `current_handoff` in `sdad-state.yaml` to that in-root path.
4. Keep the exact INDEX source line:
   `- Current handoff: use ../sdad-state.yaml#current_handoff when declared.`
5. On resume, confirm the state pointer, marker, current packet, source, tests,
   and repository status still agree before relying on the handoff.
6. On packet switch, completion, archive, or replacement, remove or replace the
   state pointer in the same coherence update. A handoff for another packet
   cannot remain current.

Do not add the handoff path to `routed_docs` merely because it exists.

## Standard Handoff Template

```markdown
# SDAD Session Handoff

## 1. Session Identity

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
- Authoritative authorization record, if any:
- Last-observed authorization status:
- Blockers or residual risk:

## 6. Resume Instructions

Load the adapter, `sdad-state.yaml`, and `docs/INDEX.md`. Confirm this handoff
is still the state-declared checkpoint, then read only the targeted authority
pointers required for the next decision. Repository truth overrides this
checkpoint.
```

The handoff's last-observed status is not reusable authority. Follow its pointer
to the single authoritative authorization record and verify that the packet,
action, conditions, expiry, evidence prerequisite, and recorded source remain
unchanged. Re-approval is required after expiry, a failed condition, or relevant
source change.

## Bounded Resume Reads

Do not assume the previous chat context is available. Start with adapter ->
state -> INDEX, inspect current source/tests, and then select only the relevant
handoff pointers. Use bounded reads for archives, old handoffs, generated
artifacts, logs, databases, and authorized private data. Report the routed
documents actually read, not the complete eligible `routed_docs` set.

## Reactivation Prompt

```text
You are resuming an SDAD Protocol project. Read the installed adapter,
sdad-state.yaml, and docs/INDEX.md first. If state declares current_handoff,
verify that its first exact Session Identity section has one marker matching
active_packet.id. Treat it as continuity, not authority. Inspect current
source/tests and only the targeted Authority Pointers needed for the next
decision. State the packet, next action, validation claim and limits, owner
gates, and any stale or unverified evidence before changing files.
```
