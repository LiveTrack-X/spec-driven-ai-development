# Project Documentation Router

Status: Active

## First Read

1. Read `../sdad-state.yaml` for scale, packet, gates, checks, and routes.
2. Read this table; inspect current source/tests/runtime.
3. Intent selects a path/heading/section/match, not a full read.

Do not load rules/history/evidence by default.

## Working Route

Combine rows without duplicate reads; update only changed facts. Repairs cannot
bypass gates. Inspect before asking; reuse scoped authorization. Questions permit no writes.

| Intent | Read now | Update if changed | Normally omit |
| --- | --- | --- | --- |
| Explain | relevant source/tests/SPEC | none | state/evidence/handoff writes |
| Review/audit | target, SPEC, active findings | findings if recording authorized | implementation/status promotion |
| Implement/fix | SPEC, source/tests, linked TODO/findings | affected work/evidence/state | notes/ADR without a decision |
| Correct; new/conflicting SPEC | owner request, active SPEC, affected code/tests | adopted SPEC/work/evidence/state | unrelated criteria/history |
| Docs cleanup | target, current constraints, inbound links | affected docs/links | unrelated functional tests |
| Resume/handoff | current request/state/SPEC/source; checkpoint | changed facts | routine handoff/replay |
| Protected action/owner decision | SPEC, gates, decision, intersecting deferred findings | decision/evidence | unauthorized external execution |
| Product/hardware/package/remote/public claim | applicable evidence/claim records | affected claims | unrelated optional ledgers |
| Coordination/blocked/deferred/late result | state; packet TODO/finding/gate/decision | affected pointers | unrelated packet history |
| Historical/reference intake | current source/SPEC before selected reference | authorized adopted facts | archive-wide reads |

## On-Demand Policy And Playbooks

- authority/status meaning: `Repository-Operating-Rules.md` by heading;
- large/private input: `sdad/playbooks/context-and-data.md`;
- scale/packet/delegation: `sdad/playbooks/work-packets.md`;
- coordination: `sdad/playbooks/coordination-and-decision-trace.md`;
- gates/claims/reuse: `sdad/playbooks/evidence-and-risk-gates.md`;
  reuse section: `Evidence Freshness And Invalidation`;
- records/handoff: `sdad/playbooks/documentation-and-handoff.md`;
- adaptive rules/harness/eval: `sdad/playbooks/advanced-extensions.md`.

## Write Route

| Fact | Authoritative home |
| --- | --- |
| Scope/behavior/non-goals/acceptance | active SPEC |
| Work/deferred task | `TODO-Open-Items.md` |
| Defect/blocker/risk | `../review-findings.md` |
| Spec-unstated choice | `implementation-notes.md` |
| Hard-to-reverse tradeoff | ADR under `../SPEC/adr/` |
| Evidence/claim | designated record; otherwise `sdad/evidence/<packet-id>.md` on first durable need, linked from packet TODO |
| Owner authorization/result acceptance | durable decision path/URL/ID |
| Execution | `../sdad-state.yaml` |
| Continuity | state-declared handoff; summaries link authorities |

## Source Of Truth

Active SPEC owns intended scope/acceptance; source/tests/runtime show observed
behavior; state owns execution; handoff owns continuity. Persist owner redirects
before affected implementation. References/archives/names/dates do not activate
scope. Decisions have one authoritative home; summaries link it.

## Active Catalog

- Core: state, installed tool adapter, active SPEC (`../SPEC/SPEC-COMPLETE.md` default), TODO, findings, notes above.
- Optional: `evidence-matrix.md`, `claim-registry.md`, artifact/readiness/remote records; create only for an active claim.
- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.
- Continuity templates: `sdad/handoffs/`; decisions: `../SPEC/adr/`.

Checkpoint means last resume record, not live state or authority.

## Maintenance

Keep routing-only and current controls short; preserve open work and archive
closed history. At handoff, report docs changed/checked and checks run.
