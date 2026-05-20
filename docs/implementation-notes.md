# Implementation Notes

Status: Active reference
Scope: Bounded decision log for spec-unstated implementation choices

Implementation notes preserve implementation memory.

They are not a transcript of everything the AI thought while coding. They are a
small decision log for moments when the active SPEC did not already decide what
the implementation should do.

## Rule

Implement from the active SPEC. When implementation requires a judgment the SPEC
does not explicitly cover, record the decision in implementation notes.

Record:

- assumptions used to bridge a SPEC gap,
- implementation changes that differ from the literal SPEC wording,
- compromises caused by time, environment, compatibility, dependencies, or
  verification limits,
- alternatives considered and rejected when the choice affects future work,
- owner-relevant tradeoffs,
- follow-up TODOs, review findings, or ADR needs created by the decision,
- verification impact, including what was checked and what remains unverified.

Do not record:

- raw internal reasoning or thought transcripts,
- every mechanical edit,
- routine file moves, formatting, imports, or variable names,
- duplicate notes already captured in an ADR, review finding, TODO, or handoff,
- large logs or generated output.

Implementation notes should help the next AI session or human reviewer answer:

```text
Why does the implementation look like this when the SPEC did not say so?
```

## Storage

For Standard and Full SDAD, keep current notes in:

```text
docs/implementation-notes.md
```

For Mini SDAD, do not create a persistent implementation-notes file by default.
Include a short "Implementation notes" section in the final evidence-ready
summary when a spec-unstated decision happened.

If a decision is durable architecture, policy, release, security, data-boundary,
or owner-approved tradeoff rationale, create or update an ADR instead of keeping
only a note.

A decision normally deserves an ADR only when all three are true:

- it is hard to reverse,
- it would surprise a future maintainer without context,
- it represents a real tradeoff, not just a routine implementation choice.

If the note describes a bug, risk, or blocked issue, record it in
`review-findings.md`.

If the note creates future implementation work, record it in
`docs/TODO-Open-Items.md`.

## Template

Use a compact table or bullet list:

```md
## YYYY-MM-DD - Work packet or unit name

- SPEC gap:
- Decision:
- Why:
- Alternatives rejected:
- Verification impact:
- Follow-up:
```

## Context Stability

Implementation notes are active operating state, not a permanent journal.

Keep them short enough for a fresh AI session to read as current context. If the
file becomes long, repetitive, or hard to audit, archive older entries and leave
the active file focused on current decisions, unresolved gaps, and links to
history.

Use bounded reads for archived implementation notes.

## 2026-05-20 - Clarification checkpoint adoption

- SPEC gap: SDAD did not yet define how to absorb external "grill the plan"
  style prompting without creating micro-approval or another tool dependency.
- Decision: adopt the useful behavior as SDAD-native clarification checkpoints,
  optional domain-language routing, sparse ADR criteria, and reference-not-copy
  handoff guidance. Do not import the external skill framework or require a
  default `CONTEXT.md`.
- Why: this preserves the practical value of pressure-testing plans while
  keeping SDAD's existing control layer authoritative: active SPEC, work packet
  autonomy, implementation notes, ADRs, TODOs, review findings, and handoffs.
- Alternatives rejected: wholesale skill installation; mandatory glossary files
  for every project; asking the owner a long interview before every packet;
  using ADRs for routine implementation choices.
- Verification impact: docs, prompts, adapters, templates, skill references, and
  examples must validate together because the rule affects the public workflow
  surface rather than runtime behavior.
- Follow-up: none unless owner wants a release/tag for this documentation slice.
