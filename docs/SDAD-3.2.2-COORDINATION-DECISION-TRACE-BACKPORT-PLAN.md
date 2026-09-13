# SDAD 3.2.2 Coordination and Decision Trace Backport Plan

> Current-direction note: the former 4.0 design has been withdrawn by the owner.
> This document is preserved as the existing 3.x backport implementation record;
> its references to 4.0 describe that former design, not current requirements.
> The new direction is [SDAD 4.0](v4/README.md). Reuse requires an explicit fit
> assessment against that plan; this record does not activate the old design.

Status: Implemented and locally validated
Target: SDAD 3.2.2-compatible document profile
Source concepts: SDAD 4.0 Core, Companion, and long-horizon review
Implementation form: Markdown rules and templates only
Runtime dependency: None
Compatibility goal: Any LLM or human operator that can read the repository
Authority: This repository copy is the implementation record; detached copies
are reference input only.

## 1. Executive Decision

Selected SDAD 4.0 concepts should be backported to the SDAD 3.x operating
pattern as an optional, document-only profile.

The backport must not reproduce the SDAD 4.0 runtime in prose. It should retain
only the concepts that remain truthful when enforced through existing SDAD 3.2.2
authority surfaces:

- active SPEC and packet state;
- TODO and review findings;
- implementation notes and ADRs;
- evidence and claim records;
- owner decisions;
- conditional handoffs.

The recommended profile name is:

> SDAD 3.x Coordination and Decision Trace Profile

This profile is additive guidance. It does not modify or replace the immutable
SDAD 3.2.2 release tag.

## 2. Problem Statement

SDAD 3.2.2 already separates scope, evidence, current state, and owner
authority. It also supports packet splitting, parallel edits, deferred work,
decision notes, evidence-ready reporting, and packet-bound handoffs.

Long-running and multi-agent work still exposes several review costs:

1. A decision may be recorded without a direct link to the TODO or packet that
   caused it.
2. Its affected paths, claims, validation, and follow-up tasks may be scattered.
3. Parallel agent results may be locally complete while sibling work remains
   pending or unknown.
4. Agent-discovered work may be mistaken for approved scope.
5. A successful integration may be described as owner acceptance or release.
6. Rule 5 candidates may accumulate without a clear Keep, Refine, Merge, or
   Retire decision.

SDAD 4.0 addresses these problems with typed entities, graph projection,
coordinator fencing, operation journals, and a Companion UI. Most of that
runtime cannot be truthfully represented by a document-only 3.x profile.

This plan therefore translates only the semantic invariants that can be
reviewed and followed without a specific executable.

## 3. Goals

The profile should:

- make each material decision traceable to the packet or TODO that caused it;
- show the decision conclusion, rationale, alternatives, and direct impacts;
- make parallel agent scope and dependencies reviewable before work starts;
- prevent packet closure while required sibling results remain unresolved;
- route agent-discovered work to a candidate surface instead of active scope;
- preserve Rule 5 lifecycle decisions and regression evidence;
- distinguish agent completion, evidence-ready, owner-accepted, released, and
  production-ready states;
- remain compatible with any agent that follows Markdown repository rules;
- preserve One Fact, One Authoritative Home;
- add no background service, database, plugin, scheduler, or required command.

## 4. Non-Goals

The profile does not:

- reproduce the SDAD 4.0 Core graph or projection engine;
- allocate repository-common identifiers;
- provide process locks, coordinator election, epochs, or fencing tokens;
- provide operation preview/confirm journals or compare-and-swap guarantees;
- automatically discover, activate, dispatch, verify, or integrate work;
- cryptographically sign owner decisions;
- guarantee cross-clone or cross-machine mutual exclusion;
- turn the existing SDAD Inspector into a required authority;
- claim that a written rule provides the same enforcement as executable code.

## 5. Preserved SDAD 3.2.2 Principles

The backport remains subordinate to the existing SDAD 3.2.2 control model.

1. Current beats historical.
2. Evidence beats confidence.
3. Active beats interesting.
4. Owner decision beats AI momentum.
5. Repeated pain becomes a rule.

The normal work loop remains:

```text
Plan -> Route -> Implement -> Verify -> Report
```

Owner gates and handoffs remain conditional branches. A handoff is a continuity
pointer, not a replacement for state, SPEC, TODO, evidence, or owner authority.

Evidence-ready remains distinct from owner-accepted. Owner acceptance remains
distinct from release and production readiness.

## 6. Backport Mapping

| SDAD 4.0 concept | SDAD 3.2.2 representation | Authority home |
| --- | --- | --- |
| Task origin of a Decision | Packet and TODO reference in the decision record | implementation note or ADR |
| Decision conclusion and rationale | Existing decision fields, strengthened with origin and impact | implementation note or ADR |
| Direct impacts | Paths, artifacts, claims, validation, TODOs, and findings | decision record with outbound links |
| Later realization | Changed files and bounded evidence references | evidence matrix, report, or decision pointer |
| Multi-agent Dispatch | A bounded TODO lane with scope and dependency fields | TODO |
| Dispatch dependency | `Depends on` references between active TODO lanes | TODO |
| Run terminal result | Terminal result and evidence link on the delegated lane | TODO or finding |
| `finalization_wait` | Packet remains open while required lanes are nonterminal | packet reconciliation checklist |
| Active discovery | Candidate finding or deferred TODO | review findings or TODO |
| Semantic deduplication | Search active and deferred records before adding a candidate | routing procedure |
| Decision impact review | One compact review block linking origin, impacts, and evidence | implementation note, ADR, or terminal decision |
| Rule lifecycle | Candidate, Active, Keep, Refine, Merge, or Retire | existing human-readable rule authority |
| Companion review surface | Optional read-only rendering of canonical Markdown | never an authority |

## 7. One Fact, One Authoritative Home

The profile must not create a second decision registry.

- A small spec-unstated implementation decision lives in implementation notes.
- A durable architecture, policy, security, release, or owner-approved
  tradeoff lives in an ADR.
- Intended behavior and acceptance criteria live in the active SPEC.
- Current or deferred work lives in TODO.
- Defects, failed checks, unresolved risks, and blocked gates live in findings.
- Evidence and claim status live in their existing evidence authorities.
- Owner authorization or acceptance lives in one owner-decision record.
- Cross-session continuity lives in a packet-bound handoff.

Other surfaces link the authoritative record by path, anchor, or stable ID. They
do not copy mutable decision fields.

## 8. Proposed Decision Record Extension

The existing implementation-note structure should receive optional origin,
impact, and realization fields.

```md
## IMPL-0042 - Decision title

- Date: YYYY-MM-DD
- Applies to:
- Origin:
  - Packet:
  - TODO or finding:
- SPEC gap:
- Decision:
- Why:
- Alternatives rejected:
- Direct impacts:
  - Work or TODO:
  - Paths or artifacts:
  - Claims or evidence:
  - Validation:
- Realized by:
  - Changed files:
  - Evidence references:
- Supersedes:
- Verification impact:
- Follow-up:
```

Rules:

1. `Origin` names the active packet and the TODO or finding that caused the
   decision.
2. `Direct impacts` lists only immediate known effects. Do not invent a complete
   transitive graph.
3. `Realized by` points to later implementation and evidence. It is not raw
   reasoning or a mechanical edit log.
4. If the decision becomes durable architecture or policy, promote it to an ADR
   and leave only a pointer in implementation notes.
5. A correction appends a superseding record. It does not rewrite the old
   historical decision.
6. Competing successors for overlapping scope require explicit reconciliation;
   filename order and date do not select a winner.

## 9. Proposed Multi-Agent TODO Lane

SDAD 3.x should represent a delegated unit as a structured TODO entry rather
than introducing Dispatch and Run entities.

```md
- [ ] [packet:auth-refresh] Refresh-token validation
  - Lane: worker-a
  - Scope: src/auth/**, tests/auth/**
  - Must not edit: src/database/**
  - Depends on: none
  - Decision references: IMPL-0042
  - Required evidence: unit test and integration test
  - Integration target: active packet branch or owner-named target
  - Terminal result: pending
  - Result evidence: none
```

Allowed terminal results:

```text
completed
failed
cancelled
rejected
superseded
```

Rules:

1. `Lane` is a human-readable assignment label, not an identity or authority.
2. Scope overlap must be resolved before parallel implementation starts.
3. A lane may not silently expand its scope.
4. A dependency is satisfied only by `completed` with all required evidence.
5. `failed`, `cancelled`, `rejected`, and `superseded` require an explicit
   disposition and do not by themselves satisfy a dependency or acceptance
   criterion.
6. A completed lane is not packet completion.
7. Integration must validate the final combined tree, not only each isolated
   lane.

## 10. Packet Finalization Barrier

The SDAD 4.0 `finalization_wait` concept should be rendered through the existing
SDAD 3.2.2 parent/child closure invariant as a packet-bound review rule:

> A packet cannot become evidence-ready while any required delegated lane is
> pending, unknown, blocked without disposition, or missing its required
> evidence.

Before packet closure, reconcile:

```md
## Parallel Result Reconciliation

- Required lanes:
- Terminal lanes:
- Pending or unknown lanes:
- Failed or cancelled lanes and disposition:
- Scope conflicts:
- Combined-tree validation:
- Remaining TODOs or findings:
- Evidence-ready: yes | no
- Owner decision needed:
```

A successful lane must not hide an unclosed sibling. A failed or cancelled
required lane remains unresolved until a replacement completes with evidence or
an owner-authorized SPEC/packet change removes the criterion. Deferral alone
cannot close an unchanged acceptance boundary.

## 11. Agent-Discovered Work

An agent may discover possible work, but discovery does not grant scope.

Newly discovered input routes as follows:

| Discovered condition | Route |
| --- | --- |
| Clear defect in active scope | Active review finding |
| Required work already implied by active acceptance criteria | Active TODO with link to the criterion |
| Improvement outside active scope | Future or deferred TODO candidate |
| Repeated failure pattern | Rule 5 candidate |
| Protected, destructive, release, production, security, or policy action | Owner gate or decision candidate |
| Duplicate or equivalent item | Link the existing record; do not create a second authority |

Recommended candidate block:

```md
### Candidate title

- Discovered by:
- Observed signal:
- Evidence:
- Possible impact:
- Duplicate search:
- Proposed route:
- Activation authority:
- Revisit trigger:
```

The candidate must not be implemented automatically unless it is already inside
the active packet and acceptance boundary.

## 12. Rule 5 Lifecycle

A portable Rule 5 proposal remains readable Markdown and contains no executable
payload.

```md
## RULE-CANDIDATE - Short title

- Status: Candidate | Active | Kept | Refined | Merged | Retired
- Origin:
- Trigger:
- Non-trigger:
- Observed failure:
- Root cause:
- Smallest durable control:
- Exceptions:
- Enforcement surface:
- Regression evidence:
- Field-use evidence:
- Limits:
- Owner decision:
- Revisit condition:
```

The lifecycle is:

```text
Finding
-> root cause
-> smallest durable control
-> regression evidence
-> field use
-> Keep | Refine | Merge | Retire
```

An agent cannot silently promote a habit or candidate into normative authority.

## 13. Evidence and Status Vocabulary

Use the following terms precisely and additively. Coordination result labels do
not replace existing SDAD 3.2.2 packet statuses or readiness lanes:

| Status | Meaning |
| --- | --- |
| Agent completed | A named lane reports its bounded task finished |
| Integrated locally | The result exists in the named local integration target |
| Evidence-ready | The declared scoped checks passed and limitations are stated |
| Software-verified | Required local software evidence passed |
| Owner-accepted | The owner accepted the named result and claim boundary |
| Released | A named release artifact or tag was actually published |
| Production-ready | Declared production evidence and owner gates completed |
| Insufficient evidence | Available evidence cannot support the requested claim |

`Agent completed`, `Integrated locally`, and `Released` are not new
`active_packet.status` values. Never collapse these terms into a generic `done`.

## 14. Handoff and Recovery

The existing packet-bound handoff model remains sufficient for the document-only
profile.

A handoff may add:

- active parallel lanes;
- pending or unknown terminal results;
- decision records created during the packet;
- direct-impact pointers;
- combined-tree validation still required;
- exact restore trigger.

The handoff must not copy full TODOs, findings, decisions, or evidence. It points
to their authoritative homes.

The profile cannot guarantee mutual exclusion, stale-process fencing, or atomic
recovery. Those remain explicit limits.

## 15. Concepts Deliberately Not Backported

The following SDAD 4.0 mechanisms require executable enforcement and stay
outside this profile:

### 15.1 Repository-common ID allocation

The 3.x profile retains existing packet, implementation-note, ADR, finding, and
handoff identifiers. It does not introduce the SDAD 4.0 date-scoped allocation
ledger because a manual document cannot guarantee collision-free concurrent
allocation.

### 15.2 Coordinator epoch and fencing

Writing an epoch or token in Markdown does not stop a stale process. Multi-agent
3.x work instead uses declared file scope, serialized integration, current
packet authority, and final-tree validation.

### 15.3 Operation preview and journal

The profile does not claim single-use confirmation, compare-and-swap, durable
apply attempts, or crash-safe side-effect recovery.

### 15.4 Automatic discovery and integration

There is no background watcher, scheduler, autonomous dispatcher, or low-risk
auto-merge loop. Agent-discovered items remain candidates until routed by the
current packet and owner rules.

### 15.5 Cryptographic owner authority

Owner decisions remain repository records under existing SDAD 3.2.2 authority
rules. The profile does not add keys, signatures, or a trust-anchor lifecycle.

## 16. Implemented Repository Changes

This plan was implemented in two bounded phases.

### Phase A - Core Profile

1. Add:
   `templates/project-control-files/docs/sdad/playbooks/coordination-and-decision-trace.md`
2. Extend:
   `templates/project-control-files/docs/implementation-notes.md`
3. Extend:
   `templates/project-control-files/docs/TODO-Open-Items.md`

Phase A establishes decision origin, direct impacts, delegated TODO lanes, and
the finalization barrier.

### Phase B - Routing and Review

1. Extend:
   `templates/project-control-files/review-findings.md`
2. Extend:
   `templates/project-control-files/docs/sdad/playbooks/work-packets.md`
3. Route the optional profile from:
   `templates/project-control-files/docs/INDEX.md`

Phase B adds candidate discovery routing, parallel result reconciliation, and
fresh-agent discoverability.

No runtime Python, JavaScript, native code, schema, Doctor check, hook, or
generated runtime file is part of either phase.

### Inspector Transfer

The separate SDAD Inspector receives one read-only integration-contract update.
The profile is displayed through the existing bounded `routed_docs` Markdown
reader. Inspector does not parse a new state, report, or snapshot schema and
does not infer dependency satisfaction, integration, acceptance, or release.
Any future structured projection requires a separate Inspector packet and
compatibility evidence.

Local Inspector transfer evidence on 2026-07-18: public repository validation
checked 131 files; the compatibility corpus checked two releases and eight
normalized reports; 118 Python tests passed with one environment skip; strict
SDAD 3.2.2 Doctor reported zero errors and zero warnings.

## 17. Scale Applicability

| Scale | Default use |
| --- | --- |
| Mini | Do not enable by default; use only the compact decision-impact fields when parallel work actually occurs |
| Standard | Enable decision trace and the finalization barrier when two or more lanes work concurrently |
| Full | Enable the complete profile for repeated multi-agent, long-horizon, or rule-lifecycle work |

The profile should remain dormant when its trigger is absent. A single-agent,
single-packet task should not acquire multi-agent ceremony.

## 18. Compatibility Requirements

The implementation must:

- preserve all existing SDAD 3.2.2 authority precedence;
- preserve current `sdad-state.yaml` semantics;
- preserve packet-bound `current_handoff`;
- preserve existing identifiers and never-reuse rules;
- keep all new fields optional outside the triggered profile;
- remain readable and usable without SDAD Inspector;
- remain usable by Codex, Claude, Gemini, other LLMs, and human-only teams;
- not require model-specific prompts or hidden memory;
- not claim fail-closed runtime behavior from prose alone.

## 19. Risks and Mitigations

### Risk: Documentation ceremony grows faster than value

Mitigation:

- trigger the profile only for actual parallel or long-horizon work;
- keep direct impacts bounded;
- archive closed history when it no longer affects current decisions;
- do not create a graph record for every mechanical edit.

### Risk: The same decision is copied across TODO, notes, and handoff

Mitigation:

- keep the decision in one authoritative note or ADR;
- use references everywhere else;
- reconcile duplicated mutable text at packet boundaries.

### Risk: Manual dependency records drift

Mitigation:

- require reconciliation before evidence-ready;
- treat unknown or stale dependencies as unresolved;
- validate the final combined tree.

### Risk: Documented coordination is mistaken for executable exclusion

Mitigation:

- state explicitly that lanes and scope declarations are procedural;
- do not use the terms lock, lease, epoch, fencing, or atomic unless an actual
  implementation provides them;
- serialize overlapping integration through an owner-named current target.

### Risk: Agent discovery expands scope without approval

Mitigation:

- route out-of-scope discoveries to candidate sections;
- require an active acceptance criterion, explicit owner direction, or packet
  change before activation.

## 20. Acceptance Criteria

The backport is acceptable when:

1. A fresh agent can determine when the profile applies from `docs/INDEX.md`.
2. A material implementation decision names its originating packet and TODO or
   finding.
3. A reviewer can identify the decision conclusion, rationale, direct impacts,
   realization evidence, and current status without reading chat history.
4. Two parallel lanes can declare non-overlapping scope, dependencies, required
   evidence, and terminal results.
5. A packet with any required nonterminal lane cannot be reported
   evidence-ready.
6. An agent-discovered out-of-scope item remains a candidate until routed.
7. Rule 5 proposals end with a visible Keep, Refine, Merge, or Retire decision.
8. No new executable, service, schema version, or required tool is introduced.
9. Existing 3.2.2 projects remain valid without adopting the optional profile.
10. Examples do not imply owner acceptance, release, or production readiness
    from local verification alone.
11. One Fact, One Authoritative Home remains true after packet reconciliation.
12. The final documentation diff passes repository documentation and formatting
    checks applicable at implementation time.

## 21. Validation Plan

Because this is a document-only profile, validation should emphasize routing and
semantic consistency.

Local protocol evidence on 2026-07-18: repository validation passed; 477 tests
passed with three environment skips; rendered agent surfaces and the
copy-paste prompt matched their canonical sources; whitespace validation passed.

### 21.1 Static review

- all referenced paths exist;
- field names are consistent across playbook and templates;
- terminology matches SDAD 3.2.2;
- no profile text overrides Core authority;
- no runtime guarantee is claimed.

### 21.2 Fresh-agent scenarios

Test at least:

1. one agent, one small task, profile remains dormant;
2. two agents, non-overlapping files, both succeed;
3. one successful lane and one pending lane, packet remains open;
4. one failed lane, result becomes a finding or explicit disposition;
5. two lanes propose conflicting decisions, owner reconciliation required;
6. agent discovers an unrelated improvement, it remains deferred;
7. a decision changes validation requirements, affected evidence is rerun;
8. a packet handoff points to current authorities without copying them;
9. an owner redirect makes a late lane result stale until rerouted;
10. parallel branches collide on an `IMPL-NNNN` ID and reconcile every link;
11. a failed required lane is deferred while unchanged acceptance still blocks
    packet closure.

### 21.3 Long-horizon review

After repeated real use, measure:

- additional tokens and review time;
- decision lookup time;
- duplicate TODO or decision rate;
- unresolved sibling-result rate;
- human intervention rate;
- Rule 5 candidates kept, refined, merged, or retired;
- maintenance burden of the added fields.

Comparative improvement claims require repeated evidence. A successful template
review alone proves structural usability, not productivity improvement.

## 22. Rollout and Rollback

### Rollout

1. Introduce the profile as optional and on demand.
2. Pilot it on one Standard or Full project with actual parallel work.
3. Review field usefulness after each packet.
4. Keep, refine, merge, or retire the profile through Rule 5.
5. Promote it more broadly only if measured review value exceeds maintenance
   cost.

### Rollback

Rollback requires no data migration:

- stop routing new work to the profile;
- retain existing decision and evidence history;
- promote still-current facts to existing SPEC, ADR, TODO, finding, or evidence
  authorities;
- remove unused optional template fields in a later documented revision.

## 23. Owner Decisions Before Implementation

Recommended defaults are shown below.

| Decision | Recommended default |
| --- | --- |
| Public name | SDAD 3.x Coordination and Decision Trace Profile |
| Compatibility | Additive and optional for SDAD 3.2.2 projects |
| Default scale | Standard and Full only when triggered |
| Identifier policy | Retain existing 3.x identifiers |
| Runtime additions | None |
| Doctor/schema changes | None in the initial profile |
| Companion dependency | None; Inspector uses existing read-only routed Markdown |
| First pilot | One real multi-agent packet before broader adoption |

## 24. Final Recommendation

The document-only backport is implemented locally. Keep it optional until one
real Standard or Full multi-agent packet completes the field-use review.

The highest-value concepts are:

1. decision origin;
2. direct-impact review;
3. bounded parallel TODO lanes;
4. packet finalization barrier;
5. candidate-only active discovery;
6. Rule 5 lifecycle closure;
7. precise evidence and acceptance vocabulary.

Do not backport runtime authority mechanisms as prose. Keep those mechanisms in
the separate SDAD 4.0-derived system where they can be implemented and tested.

This division preserves the low-friction, agent-agnostic character of SDAD 3.x
while importing the parts of SDAD 4.0 that materially improve long-running and
multi-agent review.
