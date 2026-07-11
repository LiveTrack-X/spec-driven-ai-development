# Starter Templates

Use this reference only for Standard/Full bootstrap or control-plane repair.
Adapt project paths and commands; preserve existing owner decisions.

## Scale Output

- One-shot: no project files.
- Mini: one tool-specific instruction file.
- Standard: one full adapter plus the compact core below.
- Full: Standard core plus only the risk/evidence files needed by active gates.

## Single-Responsibility Control Plane

| Surface | Owns | Must not own |
| --- | --- | --- |
| Tool adapter | always-loaded safety, execution, stop, source/evidence kernel | long procedures or file catalog |
| `sdad-state.yaml` | current packet, gates, commands, routed docs | history or prose policy |
| `docs/INDEX.md` | trigger-to-file routing | workflow explanation |
| Operating rules | durable policy | mandatory startup or live state |
| Playbooks | on-demand procedures | current facts |
| SPEC/TODO/findings/notes | authoritative current work state | copied chat transcripts |
| Handoff | cross-session recovery | live state or behavior authority |
| Evidence/claim files | scoped proof and claim status | unrelated setup ceremony |

## Minimum Standard Tree

```text
<tool adapter>
sdad-state.yaml
docs/
  INDEX.md
  Repository-Operating-Rules.md
  TODO-Open-Items.md
  implementation-notes.md
  sdad/playbooks/
    context-and-data.md
    work-packets.md
    evidence-and-risk-gates.md
    documentation-and-handoff.md
    advanced-extensions.md
SPEC/
  SPEC-COMPLETE.md
  adr/ADR-0001-template.md
review-findings.md
```

Handoffs and evidence files are create-on-demand.

When a source checkout is available, use the exact files under
`templates/project-control-files/`. When only the installed skill is
available, render the compact schemas below and the semantic clauses from
`references/runtime-contract.md`.

## Active State Schema

```yaml
version: 2
updated: YYYY-MM-DD
scale: standard
execution_scope: packet
active_spec: SPEC/SPEC-COMPLETE.md
active_packet:
  id: bootstrap
  objective: Replace with the current evidence-ready objective.
  status: not_started
validation_for: bootstrap
# current_handoff: docs/sdad/handoffs/YYYY-MM-DD-topic.md
owner_gates: []
validation:
  - command: Replace with the project validation command.
    proves: Replace with the claim this command supports.
routed_docs:
  - docs/TODO-Open-Items.md
  - review-findings.md
```

Keep this file below 80 lines and 2,000 characters. `routed_docs` lists eligible
current-packet selections; intent chooses the path or targeted content actually
read. Omit a live `current_handoff` unless the named checkpoint exists.

## INDEX Schema

Keep INDEX below 80 lines and 4,000 characters. Include:

1. state -> INDEX -> current source/tests as the fixed read path;
2. a Working Route table for implement, review, docs, owner gates, claims,
   handoff, and historical/reference triggers;
3. an on-demand policy/playbook route;
4. a write route for SPEC, TODO, findings, notes, ADR, evidence, and continuity;
5. a compact source-of-truth order;
6. an active catalog and maintenance budget.

The first `## Active Catalog` contains exactly once:

```markdown
- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.
```

The canonical template is
`templates/project-control-files/docs/INDEX.md`. INDEX is routing-only.

## Adapter Contract

Install exactly one adapter at the host tool's native path. Every full adapter
must be self-contained and include:

- progressive state -> INDEX -> on-demand rule routing;
- scale, execution-scope, and owner-gate boundaries;
- sensitive-data pre-read boundary;
- source-of-truth and evidence/claim limits;
- stop conditions;
- compact finish and state-declared handoff triggers.

Do not add runtime includes unless the host tool is proven to load them. Keep
the rendered adapter below 120 lines and 6,000 characters.

## Core Rules And Playbooks

Use the canonical files under
`templates/project-control-files/docs/Repository-Operating-Rules.md` and
`templates/project-control-files/docs/sdad/playbooks/`.

The rulebook owns durable policy only. Playbooks own:

- large/private context handling;
- scale, execution-scope, packet, delegation, and clarification procedure;
- owner gates, evidence, parity, and release boundaries;
- documentation, control-file budget, state, and handoff procedure;
- advanced harness/eval/memory-loop fit gates.

Do not duplicate the Mandatory Start or intent router in the rulebook.

## Current Work Files

Create short current-state files:

- `SPEC/SPEC-COMPLETE.md`: product baseline and active acceptance criteria;
- `docs/TODO-Open-Items.md`: open work and next action only;
- `review-findings.md`: unresolved defects, failed checks, and risk only;
- `docs/implementation-notes.md`: durable spec-unstated choices only.

Use ADRs sparingly. Archive closed history rather than growing active journals.

Use exact active-ledger forms. The TODO template contains `## Active Work`,
`## Release / Production Readiness`, and `## Recently Closed`; each active
checkbox carries the packet marker:

```markdown
- [ ] [packet:bootstrap] Replace with active work.
```

Review keeps `## Active Findings` with prose `None currently tracked.` when
empty, plus `## Recently Closed` outside the active section.

Both legal open-finding forms are shown here outside the active ledger section:

```markdown
- [High] [packet:bootstrap] Replace with a classified finding.
- [packet:bootstrap] Replace with an unclassified finding.
```

## Optional Current Handoff

Create a compact recovery checkpoint only when work pauses, changes hands,
remains blocked/partial, or would be expensive to reconstruct. Declare its path
as `current_handoff` in state. Its exact identity start is:

```markdown
## 1. Session Identity

- Active packet: [packet:bootstrap]
```

The handoff links to state, SPEC, TODO/findings, notes/ADRs, and bounded evidence;
it does not duplicate those authorities. Remove or replace the pointer when the
packet changes.

## Optional Evidence Files

Create only when an active claim needs the boundary:

- `docs/evidence-matrix.md`;
- `docs/claim-registry.md`;
- `docs/artifact-contracts.md`;
- `docs/work-packet-state.md` (optional Delivery Readiness Model);
- `docs/remote-evidence-import.md`.

A missing optional file is not a setup failure when no corresponding claim
exists.

## Merge Safety

Before writing:

1. inspect existing tool instructions and control files;
2. show collisions and proposed changes;
3. preserve project-specific commands, constraints, and owner decisions;
4. do not overwrite without authorization;
5. validate the installed adapter and routed files from outside the template
   source when packaging is part of the claim.

## Bootstrap Handoff

Report the chosen scale/tool, created or merged files, active packet, validation
commands, optional files intentionally omitted, remaining owner gates, and the
first concrete next step.
