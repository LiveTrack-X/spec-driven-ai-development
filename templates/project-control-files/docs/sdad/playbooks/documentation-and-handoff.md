# Documentation And Handoff Playbook

Status: On demand
Trigger: durable decision, documentation drift, close-loop maintenance, pause,
resume, handoff, or oversized control file

## One Fact, One Authoritative Home

Write each fact once:

- requirement, behavior, non-goal, or acceptance change -> active SPEC;
- small spec-unstated implementation decision -> implementation notes;
- hard-to-reverse architecture decision -> numbered ADR;
- unresolved work -> TODO or review finding;
- current execution declaration -> `sdad-state.yaml`;
- cross-session recovery pointers and observed results -> current handoff;
- claim/evidence status -> the applicable evidence or claim record.

A handoff links to these authorities. It does not duplicate full SPEC decisions,
implementation notes, ADR rationale, TODOs, findings, or long command/file logs.

## Routed Document Semantics

`routed_docs` is an eligible current-packet selection set. Current intent chooses
the path, heading, active section, or targeted match actually read. Membership
never means load every listed file in full. Report only routed documents that
were actually read.

## Control File Budget

- Minimal: one changed active state or documentation surface.
- Normal: state plus the affected ledger or authority.
- Heavy: four or more control files or a new durable decision record.

Keep active files short. Move closed TODOs/findings and old evidence to a
Recently Closed section or timestamped archive, then link them. Do not create a
file solely to make the process look complete.

## Documentation Update Check

At packet or handoff boundaries, check only affected surfaces:

- behavior/configuration -> README, runtime docs, active SPEC;
- prompt/tool contract -> adapter or skill source, tests, affected guidance;
- data/security/destructive action -> policy, SPEC, findings, owner gate;
- release/migration/version -> release docs, risk playbook, SPEC;
- public/product/hardware/package claim -> evidence and claim records;
- continuity change -> state pointer and the compact handoff.

If no update is needed, name the files checked and why. Do not claim an evidence
checkpoint while current control state is stale.

## Current Handoff

`current_handoff` is the latest resume checkpoint, not live state. Declare it in
`sdad-state.yaml` only when a real recovery document exists. Read it only for
resume or continuity intent, and verify its pointers against current repository
truth.

On a packet switch, the old pointer must be removed or replaced in the same
coherence transaction. A handoff for another packet cannot remain current.

Use `docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md`, where `HNNNN` is the next
zero-padded repository-logical ID. The date is descriptive; only the ID records
sequence, and only `current_handoff` records currentness. Never reuse or
renumber IDs. Existing unnumbered handoffs remain valid. Resolve parallel ID
collisions before merge by changing the filename, internal ID, and state pointer
together. Include only repository/branch/worktree/HEAD/dirty state, current goal
and next action, authority paths, last observed validation with claim limits,
open constraints/gates, and bounded resume instructions.

## Close-Loop Gate

Before an evidence checkpoint: run or explain routed checks; synchronize state
and changed authorities; inspect unfinished active records and generated
artifacts when relevant; record residual risk; and keep owner acceptance
separate from evidence-ready implementation.
