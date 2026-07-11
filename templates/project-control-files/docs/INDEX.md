# Project Documentation Router

Status: Active
Purpose: routing only. Explanations and procedures live in their target files.

## First Read

1. Read `../sdad-state.yaml` for the current scale, packet, gates, checks, and
   routed documents.
2. Read this table.
3. Inspect current source, tests, and runtime state.
4. Let current intent select one eligible route, heading, active section, or
   targeted match; route membership never means reading every file in full.

Do not load the full rulebook, archives, historical SPEC sections, old
handoffs, or optional evidence templates by default.

## Working Route

| Intent or trigger | Read now | Load on demand |
| --- | --- | --- |
| Any active packet | `../sdad-state.yaml`, current source/tests | routed documents selected by current intent |
| Implement or fix | active SPEC, `TODO-Open-Items.md`, `../review-findings.md` | implementation notes; ADR for a durable tradeoff |
| Review or audit | source/tests, active SPEC, active findings | relevant operating-rule heading |
| Docs or behavior change | affected docs and active SPEC | documentation-and-handoff playbook |
| Release, migration, destructive, production, data/auth/money/security, rollback | active SPEC and owner gates | rulebook risk/version sections and release evidence |
| Product, hardware, compatibility, package, remote, or public claim | `evidence-matrix.md`, `claim-registry.md` | artifact contract, packet state, remote import |
| Pause, resume, or handoff | state-declared current handoff | TODO/findings/SPEC when continuity changes authority |
| Historical or reference intake | current code/docs/SPEC first | product notes, external reference, then archive |

## On-Demand Policy And Playbooks

- authority or code policy: `Repository-Operating-Rules.md` by heading;
- large/private input: `sdad/playbooks/context-and-data.md`;
- scale, execution scope, packet, or delegation: `sdad/playbooks/work-packets.md`;
- owner gate, claim, parity, or release: `sdad/playbooks/evidence-and-risk-gates.md`;
- docs/state/handoff: `sdad/playbooks/documentation-and-handoff.md`;
- harness/eval/memory loops: `sdad/playbooks/advanced-extensions.md`.

## Write Route

| New information | Record in |
| --- | --- |
| Scope, behavior, non-goal, acceptance criterion | active SPEC |
| Current task or deferred work | `TODO-Open-Items.md` |
| Defect, blocked check, unresolved risk | `../review-findings.md` |
| Spec-unstated implementation choice | `implementation-notes.md` |
| Hard-to-reverse surprising tradeoff | numbered ADR under `../SPEC/adr/` |
| Evidence or public claim status | evidence matrix and claim registry |
| Current execution declaration | `../sdad-state.yaml` |
| Cross-session recovery pointers/results | state-declared current handoff |

## Source Of Truth

Current source/tests/runtime evidence > active runtime docs > canonical SPEC >
active SPEC > current state > current handoff > references > archives > chat confidence.
Owner decisions control scope, risk, irreversible actions, and acceptance.

## Active Catalog

- Core: `../sdad-state.yaml`, the installed tool adapter at its native path,
  `../SPEC/SPEC-COMPLETE.md`, `TODO-Open-Items.md`,
  `../review-findings.md`, `implementation-notes.md`.
- Policy: `Repository-Operating-Rules.md`.
- Procedures: `sdad/playbooks/` (load one triggered file only).
- Optional evidence: `evidence-matrix.md`, `claim-registry.md`,
  `artifact-contracts.md`, `work-packet-state.md`,
  `remote-evidence-import.md`.
- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.
- Continuity templates: `sdad/handoffs/`.
- Decisions: `../SPEC/adr/`.

## Maintenance

Keep this file below 80 lines and routing-only. Keep `sdad-state.yaml`, TODO,
findings, and any current handoff short. Archive closed history. At handoff,
state which docs changed, which were checked without changes, and which checks
ran.
