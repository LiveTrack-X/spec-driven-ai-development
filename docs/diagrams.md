# Diagrams

Status: Active reference

## One Work Loop

```mermaid
flowchart LR
    P["Plan\noutcome, scope, evidence"] --> R["Route\nstate -> INDEX -> targeted context"]
    R --> I["Implement\nsmall reviewable changes"]
    I --> V["Verify\nrun checks, bound claims"]
    V --> O["Report\nevidence, limits, risk"]
    O --> G{"Protected action?"}
    G -- "Yes" --> D["Owner gate\nauthorize, revise, defer, reject"]
    G -- "No" --> H{"Continuity needed?"}
    D --> H
    H -- "Yes" --> C["Handoff\nlinks and last observed results"]
    H -- "No" --> N["Next unit or packet"]
```

Owner gate and handoff are triggered branches, not extra loop modes.

## Fresh Context Route

```mermaid
flowchart TD
    A["Installed tool adapter"] --> S["sdad-state.yaml\npacket, scope, validation, gates"]
    S --> X["docs/INDEX.md\nrouting map"]
    X --> C["Current source and tests"]
    C --> Q{"Current intent"}
    Q --> T["One targeted path, heading,\nactive section, or match"]
    T --> B{"Large, old, generated,\nprivate, or archived?"}
    B -- "Yes" --> L["Bounded read with limits"]
    B -- "No" --> W["Work with current evidence"]
```

`routed_docs` is an eligible selection set. It is never a startup instruction
to read every listed file.

## Authority And Continuity

```mermaid
flowchart TD
    F{"Fact type"}
    F -->|"Observed behavior"| E["Current source, tests, runtime,\nreproducible commands"]
    F -->|"Intended scope and acceptance criteria"| AS["state-declared active_spec\nsingle normative entrypoint"]
    F -->|"Current execution"| ST["sdad-state.yaml and active ledgers"]
    F -->|"Authorization or acceptance"| OD["One owner-decision record\nfor declared scope"]
    F -->|"Continuity"| CH["Optional current handoff\npointers only"]
    P["Other SPECs, references, archives,\nfilenames, dates, chat"] -. "proposal or context only" .-> F
```

`SPEC-COMPLETE.md` is an integrated baseline, not an automatic override. Owner
acceptance does not upgrade weak evidence. A new state-v2 project does not use
`save-state.md`; an existing copy is state-v1 migration input only.

## One Fact, One Home

```mermaid
flowchart TD
    F{"New durable fact"}
    F -->|"Intended scope or acceptance criteria"| S["state-declared active_spec"]
    F -->|"Observed behavior"| O["Source, tests, runtime evidence"]
    F -->|"Small spec-unstated choice"| N["Implementation notes"]
    F -->|"Hard-to-reverse architecture"| A["ADR"]
    F -->|"Unresolved work"| T["TODO or finding"]
    F -->|"Authorization or acceptance"| D["Owner-decision record"]
    F -->|"Current execution"| Y["sdad-state.yaml"]
    F -->|"Cross-session links/results"| H["Current handoff"]
```

A handoff uses Authority Pointers; it does not duplicate these records.

## Three Control Axes

```mermaid
flowchart LR
    S["Scale\npersistent control surface"]
    E["Execution scope\nunit or packet"]
    G["Owner gate\nprotected-action permission"]
    V["Validation contract\nchecks and bounded claims"]
    O["Owner acceptance\nfinal human decision"]
    S --> V
    E --> V
    G --> O
    V --> O
```

Scale does not grant permission. Execution scope does not accept risk. Validation
does not imply owner acceptance.

## Guidance Through Owner Decision

```mermaid
flowchart LR
    G["Guidance\nMarkdown and adapters"] --> V["Deterministic validation\nDoctor, tests, CI"]
    V --> E["Technical enforcement\npermissions, hooks, sandbox, branch/release controls"]
    E --> O["Owner decision\nauthorization and acceptance"]
```

Each layer has a different job. Tool-native plans, sessions, checkpoints,
memory, or doctor features may be useful diagnostics, but they are not SDAD
state, handoff, Doctor, or owner authority.

## Evidence Claim Ladder

```mermaid
flowchart TD
    D["Doctor green"] --> DS["Structural consistency claim only"]
    T["Task benchmark succeeds"] --> TS["Named task claim only"]
    C["Controlled comparison succeeds"] --> CS["Improvement claim for recorded conditions"]
```

## Rendered Diagram Assets

Use these when a static or interactive visual is more useful than Mermaid:

- `assets/spec-driven-ai-development-infographic.png`: confirmed SDAD 3.0
  artwork used as the current SDAD Protocol 3.2 public overview in the README.
  Its embedded `Spec-Driven` label is historical; current protocol wording is
  SPEC-Directed AI Development.
- `assets/spec-driven-ai-development-infographic.svg`: separate legacy,
  versionless progressive-control-plane companion visual; it is not the
  editable source for the README PNG.
- `assets/sdad-control-loop.archify.png`: rendered SDAD Control Loop diagram.
- `assets/sdad-control-loop.archify.html`: interactive Archify export for the
  same control loop.
- `assets/sdad-control-loop.archify.workflow.json`: source workflow used to
  regenerate the Archify export.

Rendered assets are explanatory references. They do not outrank the active
SPEC, source code, tests, current control files, or validator output.
