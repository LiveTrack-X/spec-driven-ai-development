# Diagrams

Status: Active reference
Scope: Visual overview of SPEC-driven AI development

## Operating Loop

```mermaid
flowchart TD
    A["Prior pain or product need"] --> B["Owner + AI planning"]
    B --> C["Active SPEC with scope, non-goals, risks"]
    C --> D["Review-worthy development unit"]
    D --> E["Bounded implementation"]
    E --> F["Cross-model or separate-session review"]
    F --> G["Tests, docs, and reproducible evidence"]
    G --> H["Owner decision: accept, revise, defer, reject"]
    H --> I["Operating rule, TODO, finding, ADR, or archive update"]
    I --> C
```

## Source Of Truth Order

```mermaid
flowchart TD
    S1["1. Source code, migrations, tests, commands"] --> S2["2. Active runtime docs"]
    S2 --> S3["3. Canonical SPEC"]
    S3 --> S4["4. Active SPEC files"]
    S4 --> S5["5. Current handoff files"]
    S5 --> S6["6. Product notes and external references"]
    S6 --> S7["7. Historical or archived records"]
    S7 --> S8["8. Chat memory or AI confidence"]
```

Read this as precedence: when two sources disagree, prefer the higher source.
Inside SPECs, current active sections override older historical sections.

## Role Split

```mermaid
flowchart LR
    O["Owner\nDirection, risk, acceptance"] --> P["Planning AI\nScope and non-goals"]
    P --> S["SPEC AI\nAcceptance criteria"]
    S --> U["Review-worthy unit\nBatch related small tasks"]
    U --> B["Builder AI\nBounded implementation"]
    B --> R["Reviewer AI\nBugs, drift, risks"]
    R --> Q["QA AI\nReproduction and evidence"]
    Q --> M["Maintainer AI\nDocs, TODO, findings, handoff"]
    M --> O
```

One AI session may perform more than one role, but risky work should receive an
independent review or QA pass.

## Control Files

```mermaid
flowchart TD
    A["AGENTS.md\nEntry rules"] --> I["docs/INDEX.md\nRouting table"]
    I --> R["docs/Repository-Operating-Rules.md\nDurable rulebook"]
    I --> S["SPEC/SPEC-COMPLETE.md\nCurrent baseline"]
    I --> T["docs/TODO-Open-Items.md\nOpen implementation work"]
    I --> F["review-findings.md\nActive defect/review backlog"]
    S --> D["SPEC/adr/\nDecision records"]
```
