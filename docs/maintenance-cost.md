# Maintenance Cost

SDAD Protocol should cost less to maintain than the drift it prevents. Update
control files at a unit, packet, owner-gate, or handoff boundary, not after every
micro-task.

## Steady State-v2 Cost

For an active Standard or Full packet, the steady structural cost is:

- one `validation_for` value equal to `active_packet.id`;
- one copyable `[packet:WP-EXAMPLE]` marker in each active TODO or review record,
  replacing `WP-EXAMPLE` with the exact `active_packet.id` value;
- cleanup or reclassification of active records at checkpoint/packet switch;
- one optional current handoff read only when resume/handoff intent needs it.

`routed_docs` is an eligible selection set. Current intent selects a path,
heading, active section, or targeted match; membership never means read every
file. Report only routed documents actually read.

## End-Of-Packet Rule

Before an evidence-ready packet report:

1. Re-read `sdad-state.yaml` and confirm the executable leaf packet.
2. Run or explicitly defer each applicable validation command.
3. State the observable result, bounded claim, limits, and skipped checks.
4. Update only affected authorities and active records.
5. Remove closed TODO/finding markers from active sections or archive them.
6. Inspect generated artifacts, caches, logs, temporary files, and packaging
   output when the packet could have created them.
7. Keep owner authorization and owner acceptance separate from validation.
8. Report docs changed and docs checked with no update needed.

Do not claim completion while control files are stale. Evidence-ready still
does not mean owner-accepted.

## One Fact, One Authoritative Home

| Fact | Record in |
| --- | --- |
| Requirement, behavior, non-goal, acceptance change | active SPEC |
| Small spec-unstated implementation choice | `docs/implementation-notes.md` |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or review finding |
| Current execution state | `sdad-state.yaml` |
| Cross-session recovery links/results | state-declared current handoff |
| Product/evidence claim | applicable evidence or claim record |

Do not duplicate one decision across SPEC, implementation notes, ADR, handoff,
and chat. A handoff uses Authority Pointers to the applicable homes.

## Control File Budget

Use the smallest justified update:

- `Minimal`: one changed state or authority surface;
- `Normal`: state plus the affected ledger or authority;
- `Heavy`: four or more control files or a new durable decision record.

Repeated `Heavy` maintenance suggests wrong routing, duplicate facts, or stale
active history. Split or archive the specific file causing the cost before
adding another general-purpose control surface.

## Small Project Compression Rule

For One-shot, Mini, or a small Standard packet, one evidence-ready summary is
enough when there is no durable decision, no unresolved finding that another
session must recover, no product/release claim needing a ledger, and no
continuity need. Do not create empty governance files to make the process look
complete.

Mini defaults to `execution_scope: unit`. Standard defaults to `packet`. Full
also defaults to `packet` and adds only applicable owner gates; scale never
grants protected-action permission.

## Create-On-Demand Evidence Files

Create these only when a real claim triggers them:

| File | Trigger |
| --- | --- |
| Evidence Matrix / Claim Registry / Artifact Contract | public, product, hardware, package, compatibility, remote, release, or production claim |
| `docs/work-packet-state.md` | a Delivery Readiness Model is needed beyond state |
| Remote Evidence Import | external evidence requires quarantine and review |

The path `docs/work-packet-state.md` is retained for compatibility. Its role is
Delivery Readiness Model, not current execution authority; `sdad-state.yaml`
remains authoritative for the packet, validation contract, gates, and status.

## Current Handoff Maintenance

New state-v2 projects do not create or route `save-state.md`. The optional
`current_handoff` state field is the sole current continuity pointer. An existing
save-state remains state-v1 migration input only.

Declare a current handoff only when another session needs recovery. The file's
canonical name is `YYYY-MM-DD-HNNNN-topic.md`, where `HNNNN` is the next
repository-logical ID and the date is descriptive only. Its first exact
`## 1. Session Identity` section must contain the matching handoff ID and exactly
one marker matching the active packet. Existing unnumbered handoffs remain valid.
On packet switch, completion, archive, or replacement, remove or replace the
pointer in the same coherence update.

Read the handoff only for continuity intent, after adapter -> state -> INDEX,
and only as deeply as needed for the next decision.

## Conditional Owner Authorization

Record a reusable authorization with:

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

Reuse it only while the packet, action, conditions, expiry, evidence prerequisite,
and recorded source remain unchanged. A source change after approval, expired
condition, or failed prerequisite requires re-approval. Do not repeatedly ask
for the same still-valid authorization.

## Context And Archive Budgets

Keep active state and ledgers short. Route archives rather than loading them by
default. For large files, use targeted paths, headings, active sections, search
matches, explicit excludes, and output limits. Follow
[`context-stability.md`](context-stability.md) for private data and bounded-read
rules.

If evidence history must be split, prefer timestamped names such as:

```text
docs/archive/evidence/YYYY-MM-DD-HHMM-start-topic.md
Start: YYYY-MM-DD HH:MM
```

Link the archive from the active record. Do not leave both copies active.

## Documentation Record Audit

At a packet/handoff boundary, map change type to the smallest routed surface:

| Change type | Check or update |
| --- | --- |
| behavior/configuration | active SPEC and affected runtime/user docs |
| prompt/tool contract | canonical source, rendered adapter/skill, focused tests |
| security/data/destructive action | SPEC, owner gate, enforcement, finding |
| release/migration/version | release docs, validation, owner authorization |
| public/product/hardware/package claim | evidence and claim records |
| continuity | state pointer and compact handoff |

Report validation commands run and their limits. If a routed surface required no
change, name it under “docs checked with no update needed” and give the reason.

## Minimum Loop-End Smoke

Before closing a packet, confirm:

- no active numbered work packet remains unchecked without an explicit deferral;
- no active TODO/finding belongs only to a previous packet;
- source/tests and declared validation agree with the bounded claim;
- generated artifacts/caches/logs do not contradict the report;
- an installed or packaged artifact is smoked outside the source tree when that
  is the actual delivery boundary;
- applicable owner gates and authorization expiry are visible;
- owner acceptance is not inferred from Doctor green, test success, or provider
  task status.

The claim ladder stays bounded: Doctor green proves structural consistency; a
task benchmark proves that task; only controlled comparison supports an
improvement claim.

## Scale Implication And Stale File Warning

Scale determines the persistent control surface, not permission or quality.
Execution scope determines whether the current boundary is a `unit` or `packet`.
Owner gates determine where protected actions must stop.

If an old file still uses numeric autonomy, operating-intensity, checkpoint, or
save-state conventions, classify it as state-v1 migration input or historical
documentation. Do not silently let legacy vocabulary control a state-v2 packet.
