# Documentation Control Center

Status: Active
Scope: Central documentation navigation and maintenance control

## Start Here

- `README.md`: human-facing overview
- `docs/Repository-Operating-Rules.md`: mandatory repository rulebook
- `SPEC/SPEC-COMPLETE.md`: canonical product and implementation baseline
- `docs/TODO-Open-Items.md`: current open implementation work
- `review-findings.md`: active bug and review backlog
- `docs/implementation-notes.md`: current spec-unstated implementation decisions
- `save-state.md`: optional session recovery state when work pauses or changes hands
- `docs/sdad/handoffs/`: session handoffs for fresh AI sessions
- `docs/domain-language.md`: optional glossary for projects where terminology
  drift affects implementation, review, or tests
- `docs/evidence-matrix.md`: optional requirement-to-evidence map for product,
  hardware, release, compatibility, or remote evidence claims
- `docs/claim-registry.md`: optional allowed/blocked claim registry for README,
  UI, release notes, manifests, and packaging text
- `docs/artifact-contracts.md`: optional artifact contract registry for
  packages, firmware, support bundles, logs, and imported evidence
- `docs/work-packet-state.md`: optional state model for product packets where
  "done" must be split into software, tester, hardware, owner, and release
  states
- `docs/remote-evidence-import.md`: optional quarantine/import/review pattern
  for remote tester, lab, hardware, or external evidence bundles

Optional product evidence entries are routes, not mandatory files for every
lean bootstrap. Create or copy only the optional evidence files needed by the
claims this project actually makes.

## Working Route

Use this table while working, not only at session start.

| Moment | Check first | Then route to | Do not use for |
| --- | --- | --- | --- |
| Starting or resuming work | `AGENTS.md`, this index, current source/tests | Active SPEC, TODO, review findings, save-state or current handoff | Reading old archives before current state |
| Defining scope or acceptance | `SPEC/SPEC-COMPLETE.md` | TODO for active work, review findings for risks, ADR only for durable tradeoffs | Chat memory or old plans as authority |
| Choosing the next task | `docs/TODO-Open-Items.md` | Active SPEC for scope, review findings for blockers | Future ideas unless promoted |
| Investigating bugs or risks | `review-findings.md` | Tests, source, TODO, SPEC, evidence files | Closing findings without reproduction or rationale |
| Making a spec-unstated implementation choice | Active SPEC and source/tests | `docs/implementation-notes.md`; ADR only if hard to reverse | Hiding rationale only in chat |
| Making a public/product claim | Evidence tier, claim registry, and source/test/runtime state | Evidence Matrix, Claim Registry, Artifact Contract, Remote Evidence Import when needed | Upgrading claims from weak, unreviewed, or `blocked_until_evidence` evidence |
| Auditing documentation record | Changed files, claims, and minimum update-set row | Active docs changed/checked list, stale-doc list, archive links, validation command | Claiming evidence-ready without docs checked or no-update rationale |
| Preparing owner checkpoint | Changed files and verification evidence | TODO, review findings, SPEC, implementation notes, save-state if continuity is needed | Calling evidence-ready owner-accepted |
| Ending or handing off | Current packet state and unresolved risks | `save-state.md` or `docs/sdad/handoffs/` | Dumping a full transcript into active docs |
| Repeated pain appears | Current failure or confusion evidence | `docs/Repository-Operating-Rules.md`, tests, validators, or templates | Adding prose rules when enforcement is required |

If a moment does not match a row, start with current code/tests, active SPEC,
TODO, review findings, and this index before opening historical material.
Routing order is not source-of-truth precedence. Use this table to find the
right current files; use the Source Of Truth Role Map below when files disagree.

## SDAD Working Order

Use this order for a normal Standard or Full SDAD packet. Skip outputs whose
trigger does not exist, but state the skip reason in the evidence-ready,
owner-checkpoint, or handoff summary.

1. Route: read `AGENTS.md`, this index, current source/tests, and active runtime
   docs before archives or chat history.
2. Scale/compress: choose the smallest SDAD scale, control-file budget, and
   operating intensity that protect the packet.
3. Recover source-of-truth state: compare code/tests, active docs, canonical
   SPEC, active SPEC, and current handoff/save-state when they disagree.
4. PLAN: narrow owner intent into one packet, non-goals, boundaries, and
   claim/evidence expectations.
5. SPEC: activate or update only the current SPEC slice and acceptance criteria.
6. Optional ADR: create one only for hard-to-reverse, surprising, durable
   tradeoffs; otherwise use implementation notes.
7. TODO/work packet: turn the slice into current tasks and review-worthy units.
8. JIT clarification: after routed evidence, SPEC, and TODO still cannot decide,
   ask the next blocking question and record the resolved choice.
9. Build/review/evidence: implement, review, match evidence tiers to claims, and
   run reference parity or product-evidence gates when applicable.
10. Owner checkpoint/maintenance: distinguish evidence-ready from
    owner-accepted, run the Documentation Record Audit, update active docs, and
    archive or link long history.

When a cycle fails, is fixed, or changes release/readiness status, include a
cycle result record: problem, cause, action taken, evidence command or artifact,
and residual concern. If a reported count or status was captured before the
owner checkpoint, label that boundary.

This is a work routine, not a mandate to create every possible file. Mini SDAD
and small packets may compress the routine into one evidence-ready summary when
no durable SPEC, TODO, ADR, review finding, evidence map, or handoff job exists.

## Decision Routing Quick Check

Use this table when a decision appears during planning, implementation, review,
or handoff. If more than one row applies, record the decision in the highest
durable surface needed and link from the lighter surface.

| Decision type | Record first in | Also update when needed |
| --- | --- | --- |
| Current scope, non-goal, acceptance criterion, or behavior contract | Active SPEC | TODO, review findings, evidence matrix |
| Spec-unstated implementation choice that affects future understanding | `docs/implementation-notes.md` | TODO or review finding if follow-up remains |
| Hard-to-reverse, surprising, durable architecture, policy, release, source-of-truth, security, data-boundary, or owner tradeoff | ADR | Active SPEC, TODO, operating rules |
| Future work, deferred option, or next implementation step | `docs/TODO-Open-Items.md` | SPEC if scope changed |
| Defect, unresolved risk, failed check, or blocked gate | `review-findings.md` | TODO, SPEC, evidence matrix |
| Public, product, package, compatibility, release, hardware, or production claim | `docs/claim-registry.md` and `docs/evidence-matrix.md` | Artifact contract or remote evidence import |
| Current continuity, next step, or restart context only | `save-state.md` or `docs/sdad/handoffs/` | Promote before build if it changes scope, acceptance, risk, claim, or owner decision |

Handoff-only or save-state-only decisions are continuity hints, not durable
authority. Before implementing from a handoff-only or save-state-only decision,
promote any decision that affects scope, acceptance criteria, public claims,
risk, evidence, or owner acceptance into the active SPEC, ADR, claim registry,
TODO, or review ledger.

## Single-File Bloat Risk Routes

When one file starts carrying multiple jobs, split by job instead of appending.

| File at risk | Bloat symptom | Keep in active file | Split or archive to |
| --- | --- | --- | --- |
| `SPEC/SPEC-COMPLETE.md` | old product history hides current scope | current baseline, active scope, acceptance criteria | `SPEC/archive/` or `docs/product-notes/` |
| `docs/TODO-Open-Items.md` | completed work and future ideas mix with active work | current open work and next action | `docs/archive/todo-history/YYYY-MM-DD-topic.md` |
| `review-findings.md` | closed findings or accepted risks bury active blockers | active defects, risks, blocked gates | `docs/review/archive/YYYY-MM-DD-topic.md` |
| `docs/implementation-notes.md` | implementation diary or raw reasoning grows | current spec-unstated choices and verification impact | `docs/archive/implementation-notes/YYYY-MM-DD-topic.md` |
| `save-state.md` | session transcript replaces resume state | current objective, state, blockers, next steps | `docs/state/save-state-archive/YYYY-MM-DD-topic.md` or handoff |
| `docs/sdad/handoffs/` file | one handoff becomes a full evidence dump | resume summary and links | timestamped logs/evidence archives |
| `docs/evidence-matrix.md` | raw evidence pasted into matrix | claim-to-evidence status and IDs | `docs/archive/evidence/YYYY-MM-DD-HHMM-start-topic.md` |
| `docs/claim-registry.md` | retired claim history buries current allowed/blocked claims | current allowed, qualified, blocked claims | `docs/archive/claim-history/YYYY-MM-DD-topic.md` |
| `docs/artifact-contracts.md` | package contents or logs are pasted into contracts | artifact requirements, verifier rules, and canonical artifact manifest | evidence archive by ID or derived manifest reference |
| `docs/remote-evidence-import.md` | every imported bundle becomes one long ledger | current quarantine/review status | `docs/archive/evidence-imports/YYYY-MM-DD-HHMM-source.md` |
| `docs/Repository-Operating-Rules.md` | procedures and logs turn into a rule dump | durable rules that change behavior | playbooks, skills, validators, field notes, archives |
| `docs/INDEX.md` | explanations crowd out routing | current routes and update sets | field notes or user docs |

`review-findings.md` `## Active Findings` contains only unresolved findings.
Move fixed or accepted items to `## Recently Closed` or archive before
evidence-ready, save-state, or handoff.

## Document Classes

- Active runtime docs live under `docs/`
- Active or planned SPECs live under `SPEC/`
- Architecture decision records live under `SPEC/adr/`
- Historical docs live under `docs/archive/`
- Product notes live under `docs/product-notes/` and are references until promoted into active SPEC
- Split logs, traces, and long evidence records should live in timestamped
  archive/evidence files, then be linked from active docs.
- Implicit operating rules should be promoted into `docs/Repository-Operating-Rules.md`
  instead of left only in chat.

## Source Of Truth Role Map

| Precedence | Surface | Decides | Does not decide |
| --- | --- | --- | --- |
| 1 | Source code, migrations, tests, reproducible commands | observed behavior and reproducible evidence | owner acceptance or future scope |
| 2 | Active runtime docs | current operating state, gates, TODOs, findings, evidence status | behavior contradicted by code/tests |
| 3 | Canonical SPEC | integrated product and implementation baseline | facts disproven by current code/tests |
| 4 | Active SPEC files | active slice scope, acceptance criteria, planned changes | older history over current baseline |
| 5 | Current handoff/save-state | continuity, next steps, unresolved context | behavior authority when stale |
| 6 | Product notes and external references | reference material until promoted | implementation requirements by themselves |
| 7 | Historical or archived records | rationale and audit trail | current work direction |
| 8 | Chat memory or AI confidence | hints only | completion, acceptance, or evidence |

Owner decisions control scope, risk tolerance, and acceptance. Record durable
owner decisions in active docs, SPEC, ADR, or claim registry. A current handoff
may carry the decision for continuity until it is promoted. Do not use owner
acceptance to upgrade weak evidence into a stronger evidence tier.

## Maintenance Rules

1. Every active document must be reachable from this file.
2. Code changes require a documentation consistency check.
3. Completed plans move to archive.
4. Product notes do not become implementation requirements until promoted.
5. When docs conflict, prefer source code/tests/commands, active runtime docs,
   canonical SPEC, active SPEC files, current handoff/save-state, product
   notes/external references, archive/history, then chat or AI confidence.
6. When a SPEC spans past-to-present history, current active sections override older sections.
7. Active live-state files should stay short enough to read as current operating
   state. Move old history to archive/history files and use bounded reads there.
8. Do not keep a growing log in one active file. Split long logs or evidence
   records into timestamped files such as
   `docs/archive/logs/YYYY-MM-DD-HHMM-start-topic.md`, then link them from TODO,
   review findings, evidence matrix, save-state, or handoff.
9. A timestamped log split file should start with `Start: YYYY-MM-DD HH:MM`,
   scope, source command or artifact, evidence tier, and the active claim or
   work packet it supports.
10. Before evidence-ready, owner checkpoint, or handoff, run a Documentation Record Audit:
    list docs changed, docs checked with no update needed, stale docs found,
    archive/evidence links created, and validation commands run.

## Minimum Documentation Update Sets

Use this table before handoff.

| Change type | Minimum docs to check or update |
| --- | --- |
| User-facing behavior or workflow | `README.md`, relevant user docs, `SPEC/SPEC-COMPLETE.md` |
| Configuration, startup, deployment, or CLI | `README.md`, relevant runtime docs, `SPEC/SPEC-COMPLETE.md` |
| Security, identity, permissions, data boundaries, or destructive action | security docs if present, relevant SPEC, `review-findings.md` if risk remains |
| Background jobs, workers, lifecycle, retries, or maintenance | runtime docs, `docs/TODO-Open-Items.md` if gap status changes |
| Prompt behavior or AI/tool contract | prompt docs, relevant SPEC, tests if present |
| Fuzzy plan, unresolved scope question, overloaded term, or repeated domain-language confusion | current code/tests/docs/SPEC first, then owner clarification only for unresolved blocking questions; optional `docs/domain-language.md` if terminology drift repeats |
| Spec-unstated implementation assumption, change, compromise, rejected alternative, owner tradeoff, follow-up, or verification impact | `docs/implementation-notes.md`, `docs/TODO-Open-Items.md` if future work remains, `review-findings.md` if risk remains, ADR if durable rationale is needed |
| Roadmap, implementation status, placeholder, or gap closure | `SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, `review-findings.md` if review-related |
| Stable/next version lane, migration, release, or rollback | release docs if present, `docs/Repository-Operating-Rules.md`, relevant SPEC |
| High-risk domain rule such as locks, real-time path, backup, or platform boundary | module docs if present, `docs/Repository-Operating-Rules.md`, relevant tests |
| Product, hardware, compatibility, release, or user-facing claim | `docs/evidence-matrix.md`, `docs/claim-registry.md`, relevant SPEC, `review-findings.md` if a claim remains blocked |
| Package, firmware, support bundle, installer, generated report, or imported log becomes evidence | `docs/artifact-contracts.md`, `docs/evidence-matrix.md`, archive/evidence location, `docs/claim-registry.md` if public claims change |
| Remote tester, external lab, second machine, or user sends evidence | `docs/remote-evidence-import.md`, `docs/artifact-contracts.md`, `docs/evidence-matrix.md`, `review-findings.md` if quarantine or review fails |
| Work packet status changes across AI complete, software verified, tester ready, hardware verified, owner accepted, release candidate, or production ready | `docs/work-packet-state.md`, `docs/TODO-Open-Items.md`, `save-state.md` if handoff or pause is expected |
| Durable architecture, policy, release, or owner tradeoff decision | `SPEC/adr/ADR-0001-template.md` copied to a numbered ADR, relevant SPEC/docs |
| Repository control surface changes, including always-loaded instructions, routed rules, on-demand procedures, isolated exploration, enforced guarantees, reviewed memory, checkup cleanup, hooks, permissions, plugins, MCPs, skills, or local tool instructions | `docs/Repository-Operating-Rules.md`, relevant adapter/rule/playbook files, validators or CI checks if a guarantee must be enforced |
| Cost-aware agent routing changes, including advisor checkpoints, orchestrator-worker packets, goal loops, scheduled loops, event loops, model routing, budget, or stop rules | `docs/Repository-Operating-Rules.md`, relevant SPEC/docs, `docs/TODO-Open-Items.md`, `review-findings.md` if routing risk remains, validators or CI when loop guarantees must be enforced |
| SDAD scale/intensity change, Baseline Freeze, Evidence Surface Creep, or Heavy control-file budget | `docs/Repository-Operating-Rules.md`, relevant SPEC/docs, `docs/TODO-Open-Items.md`, `review-findings.md` if risk remains |
| Oversized live-state file, chat instability, large archive/log/generated output, or context-stability change | `docs/Repository-Operating-Rules.md`, `save-state.md`, affected active state files, archive/history location, this index |
| Advanced extension, repeated eval loop, harness optimization, retrieval/memory tuning, or self-improving agent loop | `docs/Repository-Operating-Rules.md`, relevant SPEC/docs, `docs/TODO-Open-Items.md`, `review-findings.md` if leakage, budget, or adoption risk remains |
| Session pause, handoff, owner direction change, restart, or expensive context recovery | `save-state.md`, `docs/sdad/handoffs/YYYY-MM-DD-topic.md` for long sessions, `docs/TODO-Open-Items.md`, `review-findings.md` if blocked or partial |

If no document needs a content change, handoff must state which docs were
checked and why no update was needed.
