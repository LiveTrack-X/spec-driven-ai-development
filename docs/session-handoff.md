# Session Handoff And Context Continuity

A handoff is an optional, compact cross-session recovery checkpoint. It is not
live state and it is not a second copy of the project's authorities.

For state v2, `sdad-state.yaml#current_handoff` is the sole current continuity
pointer. Do not create or route `save-state.md` for new v2 projects. An existing
`save-state.md` is state-v1 migration input only: preserve and classify it during
the read-only migration preview, but do not use it as current v2 authority.

## Authority And Continuity

- Chats are execution traces, not durable authority.
- Source, tests, runtime evidence, and reproducible commands establish observed
  behavior.
- The state-declared `active_spec` is the single normative entrypoint for
  intended scope, behavior, and acceptance criteria.
- `sdad-state.yaml` declares the current executable packet and validation
  contract.
- A handoff links to authorities and last observed results for recovery.
- Owner decisions authorize protected actions and record acceptance.

Handoff-only decisions are continuity hints. Put each durable fact in one home:

| Fact | Authoritative home |
| --- | --- |
| Intended scope, behavior, or acceptance criteria | state-declared `active_spec` |
| Observed behavior | current source, tests, runtime, and commands |
| Small spec-unstated implementation decision | `docs/implementation-notes.md` |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or review finding |
| Current execution declaration | `sdad-state.yaml` |
| Protected-action authorization | authoritative owner-decision record |
| Cross-session recovery links/results | current handoff |

`SPEC-COMPLETE.md` is an integrated baseline, not immutable or automatically
active. An additional or conflicting SPEC stays a proposal until its exact
scope is incorporated by the active entrypoint or a packet transaction switches
the pointer. A handoff cannot perform that switch.

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

1. Write each new checkpoint under
   `docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md`, where `HNNNN` is a
   zero-padded repository-logical sequence such as `H0001`.
2. Choose an ID greater than every repository-known numbered handoff, including
   archived numbered handoffs. Never reuse, fill a gap, or renumber an ID. The
   date is descriptive only: it does not establish order or currentness, so
   device clock differences cannot override the handoff sequence.
3. In its first exact `## 1. Session Identity` section, include exactly one
   `- Handoff ID: H0001` line matching the filename and exactly one canonical
   packet marker: `- Active packet: [packet:WP-EXAMPLE]`. Replace both example
   values when writing the handoff: use the allocated handoff ID and the exact
   `sdad-state.yaml#active_packet.id` value.
4. Set optional `current_handoff` in `sdad-state.yaml` to that in-root path.
5. Keep the exact INDEX source line:
   `- Current handoff: use ../sdad-state.yaml#current_handoff when declared.`
6. On resume, confirm the state pointer, ID, marker, current packet, source, tests,
   and repository status still agree before relying on the handoff.
7. On packet switch, completion, archive, or replacement, remove or replace the
   state pointer in the same coherence update. A handoff for another packet
   cannot remain current.

Existing `YYYY-MM-DD-topic.md` handoffs remain valid legacy checkpoints and do
not need a mass rename. A small correction updates the same checkpoint; a new
material recovery checkpoint gets the next ID. Parallel branches may select the
same next ID, so resolve that collision before merge by changing the filename,
internal ID, and state pointer together. The greatest ID is never implicitly
current: only `sdad-state.yaml#current_handoff` declares currentness.

Do not add the handoff path to `routed_docs` merely because it exists.

## Standard Handoff Template

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

Load the adapter, `sdad-state.yaml`, and `docs/INDEX.md`. Confirm this handoff
is still the state-declared checkpoint, then read only the targeted authority
pointers required for the next decision. Repository truth overrides this
checkpoint.
```

The handoff's last-observed status is not reusable authority. Follow its pointer
to the single authoritative authorization record and verify that the packet,
action, conditions, expiry, evidence prerequisite, and recorded source/artifact identity remain
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
