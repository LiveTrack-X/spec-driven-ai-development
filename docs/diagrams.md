# Diagrams

Status: Active reference
Scope: Visual overview of SPEC-driven AI development

## Operating Loop

```mermaid
flowchart TD
    A["Prior pain or product need"] --> B["Owner + AI planning"]
    B --> C["Active SPEC with scope, non-goals, risks"]
    C --> D["Work packet"]
    D --> E["Review-worthy development unit(s)"]
    E --> F["Bounded implementation"]
    F --> G["Cross-model or separate-session review"]
    G --> H["Evidence-ready checkpoint"]
    H --> I["Owner decision: accept, revise, defer, reject"]
    I --> J["Operating rule, TODO, finding, implementation note, ADR, or archive update"]
    J --> C
```

## Fresh Session Start Guard

```mermaid
flowchart TD
    A["Fresh AI session"] --> B["Tool adapter\nalways-loaded kernel"]
    B --> C["sdad-state.yaml\ncurrent packet and gates"]
    C --> D["docs/INDEX.md\nroute only"]
    D --> E["Inspect current source/tests"]
    E --> F["Select one routed policy, playbook, or current doc"]
    F --> G{"Large, stale, private, generated, or archived?"}
    G -- "Yes" --> H["Bounded read\nheadings, current sections, targeted matches"]
    G -- "No" --> I["Read the routed current file"]
    H --> J["Active SPEC, work packet, evidence state"]
    I --> J
    J --> K["Plan before changes"]
```

Use this guard before mandatory start-loop routes. The start loop routes the
session; it does not authorize full reads of large state files, old handoffs,
logs, generated artifacts, private data, or archives.

## Source Of Truth Order

```mermaid
flowchart TD
    S1["1. Source code, migrations, tests, commands"] --> S2["2. Active runtime docs"]
    S2 --> S3["3. Canonical SPEC"]
    S3 --> S4["4. Active SPEC files"]
    S4 --> S5["5. Current handoff/save-state files"]
    S5 --> S6["6. Product notes and external references"]
    S6 --> S7["7. Historical or archived records"]
    S7 --> S8["8. Chat memory or AI confidence"]
    O["Owner decisions\nscope, risk, acceptance"] -. "record durable decision" .-> S2
```

Read this as precedence: when two sources disagree, prefer the higher source.
Inside SPECs, current active sections override older historical sections.
Owner decisions gate scope, risk, and acceptance; record durable decisions in
active docs, SPEC, ADR, or claim registry. Owner acceptance does not upgrade
weak evidence into a stronger evidence tier.

## Document Relationship Map

```mermaid
flowchart TD
    O["Owner intent / Pain"] --> X["Scale + Compression"]
    X --> A["Tool adapter\nalways-loaded kernel"]
    A --> Y["sdad-state.yaml\nactive packet and gates"]
    Y --> I["docs/INDEX.md\nroute only"]
    I --> C0["Current source/tests"]
    C0 --> S["One routed current doc\nSPEC, TODO, finding, note, policy, or playbook"]
    S --> P["Work Packet\napproved autonomy boundary"]
    P --> T["TODO\nactive work"]
    P --> F["Review Findings\nbugs, risks, blockers"]
    P --> E["Evidence\nclaim tier and verification"]
    E --> C["Owner Checkpoint\nevidence-ready vs owner-accepted"]
    S --> N["Implementation Notes\nspec-unstated choices"]
    S --> ADR["ADR\nhard-to-reverse tradeoff only"]
    C --> R["Repository Rules\nrepeated pain becomes rule"]
    C --> H["Save-State / Handoff\ncontinuity for next session"]
    E --> L["Timestamped Log Split\nYYYY-MM-DD-HHMM-start-topic.md"]
```

Use `docs/INDEX.md` as the working router while the packet is active. It tells
the AI which single current document to check after source/tests and when to route long
logs, traces, or evidence records into timestamped split files instead of
growing an active state file.

## Role Split

```mermaid
flowchart LR
    O["Owner\nDirection, risk, acceptance"] --> P["Planning AI\nScope and non-goals"]
    P --> S["SPEC AI\nAcceptance criteria"]
    S --> W["Work packet\nAutonomy boundary"]
    W --> U["Review-worthy unit\nBatch related small tasks"]
    U --> B["Builder AI\nSimple surgical implementation"]
    B --> R["Reviewer AI\nBugs, drift, risks"]
    R --> Q["QA AI\nReproduction and evidence"]
    Q --> M["Maintainer AI\nDocs, TODO, findings, checkpoint"]
    M --> O
```

One AI session may perform more than one role, but risky work should receive an
independent review or QA pass.

## Autonomy Boundary

```mermaid
flowchart TD
    O["Owner defines packet\nscope, risks, non-goals, evidence"] --> A["AI works autonomously"]
    A --> Q{"Plan fuzzy?"}
    Q -- "Yes" --> P["Clarification checkpoint\ninspect repo first\nask next blocking question"]
    Q -- "No" --> B["Surface assumptions\nSimplify design\nMake surgical diffs\nVerify goals"]
    P --> B
    B --> N["Record spec-unstated decisions\nin implementation notes"]
    N --> C{"Stop condition?"}
    C -- "No" --> D["Continue inside packet"]
    D --> B
    C -- "Yes" --> E["Ask owner"]
    B --> F["Evidence-ready checkpoint"]
    F --> G["Owner accepts, revises, defers, or rejects"]
```

## Control Files

```mermaid
flowchart TD
    A["Tool adapter\nAlways-loaded kernel"] --> X["sdad-state.yaml\nCurrent packet and gates"]
    X --> I["docs/INDEX.md\nRouting table"]
    I --> C["Current source/tests"]
    C --> Q{"One routed path"}
    Q -. "active SPEC" .-> S["SPEC/SPEC-COMPLETE.md\nCurrent baseline"]
    Q -. "active work" .-> T["docs/TODO-Open-Items.md\nOpen implementation work"]
    Q -. "active finding" .-> F["review-findings.md\nActive defect/review backlog"]
    Q -. "decision note" .-> N["docs/implementation-notes.md\nSpec-unstated decisions"]
    Q -. "policy trigger" .-> R["Repository-Operating-Rules.md\nDurable policy"]
    Q -. "procedure trigger" .-> P["docs/sdad/playbooks/\nOne on-demand playbook"]
    S --> D["SPEC/adr/\nDecision records"]
```

## Level 4 Release Gate

```mermaid
flowchart TD
    A["Inspect, document, or test a risk area"] --> B["Standard minimum\ntrack the risk explicitly"]
    C["Change, accept, or execute the gate"] --> D["Full SDAD + Level 4"]
    D --> E["Build, review, and validate"]
    E --> F["Evidence-ready"]
    F --> G{"Owner release gate"}
    G -- "Approve" --> H["Push -> tag -> publish"]
    G -- "Revise, defer, or reject" --> I["Record outcome and stop"]
```

## Rendered Diagram Assets

Use these when a static or interactive visual is more useful than Mermaid:

- `assets/spec-driven-ai-development-infographic.png`: original public overview
  infographic retained by the README.
- `assets/spec-driven-ai-development-infographic.svg`: editable, versionless
  progressive-control-plane companion visual.
- `assets/sdad-control-loop.archify.png`: rendered SDAD Control Loop diagram.
- `assets/sdad-control-loop.archify.html`: interactive Archify export for the
  same control loop.
- `assets/sdad-control-loop.archify.workflow.json`: source workflow used to
  regenerate the Archify export.

Rendered assets are explanatory references. They do not outrank the active
SPEC, source code, tests, current control files, or validator output.
