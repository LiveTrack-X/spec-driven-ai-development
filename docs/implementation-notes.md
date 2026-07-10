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

## 2026-07-10 - Cross-model guidance translation

- SPEC gap: vendor guidance and agent research use different runtime terms and
  do not directly define an SDAD control contract.
- Decision: keep one compact external-content and semantic-validation boundary
  in the rendered kernel; route localization, packet, review, feedback, and
  evaluation detail to on-demand playbooks; keep the source matrix outside
  startup context.
- Why: the shared boundary is broadly applicable, while detailed provider and
  evaluation guidance would exceed startup needs and can change independently.
- Alternatives rejected: provider-specific kernel forks, copied benchmark
  percentages, a default model, mandatory multi-agent review, and treating
  repository regression tests as evidence of SDAD effectiveness.
- Verification impact: renderer parity, line/character budgets, semantic docs
  contracts, the exact primary-source set, and local links must pass together.
- Follow-up: refresh source dates and limitations when a cited decision changes;
  do not rewrite stable guidance merely because a provider page changes layout.

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

## 2026-05-21 - bkit-codex pattern intake

- SPEC gap: SDAD did not yet explain how to translate a context-engineering /
  PDCA-style external workflow into its own user-facing guidance without making
  SDAD depend on a specific MCP server or mandatory phase machine.
- Decision: adopt the compatible patterns as SDAD-native layered context,
  before/after change guards, task-size heuristics, and practical evidence
  examples. Keep SDAD's scale, autonomy, evidence-ready, implementation-notes,
  handoff, and owner-gate vocabulary.
- Why: these patterns help users decide what the AI should load, when it should
  keep working, and what proof to require, while preserving SDAD as a
  tool-agnostic control layer.
- Alternatives rejected: mandatory MCP-first initialization, forced PDCA phases
  for every task, line-count gates as hard rules, 90% match-rate completion
  metrics, and wholesale external terminology.
- Verification impact: README, user guides, pattern catalog, changelog, and
  validation checks should remain aligned because this changes the public
  explanation surface.
- Follow-up: consider a future optional status snapshot template only if users
  repeatedly need machine-readable recovery state.

## 2026-05-21 - natural-language intent routing

- SPEC gap: SDAD still assumed too much explicit vocabulary from users. A
  normal owner may ask "check this", "fix it", "release it", or "handoff this"
  without knowing a skill name, adapter name, autonomy term, or SDAD command.
- Decision: add Natural-Language Intent Routing as an SDAD-native rule. AI
  agents should infer review/audit, SPEC implementation, release,
  documentation, handoff, reference-intake, or autonomy-tuning intent from
  ordinary wording and current repository state.
- Why: this keeps SDAD usable for non-specialist owners while preserving the
  control layer: scale, autonomy, evidence-ready status, implementation notes,
  bounded context, and owner gates.
- Alternatives rejected: requiring users to invoke exact skill names; adding a
  rigid command grammar; treating natural-language routing as permission to read
  the whole repository or bypass risk gates.
- Verification impact: README, user guides, adapters, templates, skill prompt,
  pattern catalog, no-clone prompt, tool-adapter docs, changelog, and validation
  checks should stay aligned because this changes both the public explanation
  and the execution instructions.
- Follow-up: if users repeatedly provide mixed intents, consider a compact
  "intent conflict" checklist, but keep the default to one blocking
  clarification question.

## 2026-05-22 - OpenAI Codex practice intake

- SPEC gap: SDAD covered evidence, autonomy, handoff, and context stability, but
  did not explicitly translate OpenAI's published Codex operating habits into
  SDAD vocabulary.
- Decision: adopt compatible Codex practice as SDAD-native issue-shaped
  prompting, environment improvement loops, controlled task queues, and
  optional multi-candidate review.
- Why: these patterns preserve Codex's practical speed while keeping SDAD's
  owner control, evidence-ready status, bounded context, TODO/review ledgers,
  implementation notes, and release gates.
- Alternatives rejected: treating Codex background work as an invisible backlog;
  making Best-of-N a default acceptance policy; requiring all projects to add
  setup automation before it has repeated friction; copying OpenAI's internal
  team practice as a mandatory workflow.
- Verification impact: pattern catalog, user guide, anti-patterns, changelog,
  and validation checks should remain aligned because this is a docs/control
  behavior change.
- Follow-up: consider localized FAQ coverage if users ask how to operate Codex
  queues or multi-candidate review in Korean, Chinese, or Japanese.
