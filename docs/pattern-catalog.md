# Pattern Catalog

Status: Active reference
Scope: Combined workflow patterns distilled from anonymized field projects

This catalog turns field governance practice and compatible clarification
patterns into a reusable operating system for SPEC-driven AI development.

- Documentation-governance field practice contributes documentation routing,
  source-of-truth discipline, backlog separation, and production-readiness
  hardening.
- Release-governance field practice contributes version lanes,
  migration/release gates, architecture mapping, and explicit high-risk runtime
  rules.
- Clarification patterns adapted from
  [mattpocock/skills](https://github.com/mattpocock/skills) contribute
  plan-pressure checkpoints, glossary discipline, and sparse ADR criteria.
- Context-engineering patterns adapted from
  [popup-studio-ai/bkit-codex](https://github.com/popup-studio-ai/bkit-codex)
  contribute layered context, status recovery, pre/post change guards, and
  practical evidence examples.
- Codex usage patterns described in
  [OpenAI's Codex guide](https://openai.com/ko-KR/business/guides-and-resources/how-openai-uses-codex/)
  contribute issue-shaped prompting, environment improvement loops, controlled
  task queues, and optional multi-candidate review.

No source code is copied here. SDAD adopts compatible operating patterns, not
external MCP mandates, PDCA platform requirements, or project-level terminology.
The goal is to preserve the working method.

For the explicit list of obvious-but-easy-to-miss rules, see
[`docs/implicit-rules.md`](implicit-rules.md).

Use [`docs/anti-patterns.md`](anti-patterns.md) during review, use
[`docs/fit-assessment.md`](fit-assessment.md) before project bootstrap, and use
[`docs/diagrams.md`](diagrams.md) when explaining the workflow to a new owner or
agent.

## Combined Pattern

### 1. Start From Pain

The project begins with a concrete friction:

- a previous project became hard to resume,
- AI sessions lost context,
- docs scattered,
- completion claims were hard to trust,
- release or migration risk grew faster than the plan.

Convert that pain into an operating rule before writing new code.

### 2. Create Control Files Before Expansion

Minimum control files:

- `AGENTS.md`
- `docs/INDEX.md`
- `docs/Repository-Operating-Rules.md`
- `SPEC/SPEC-COMPLETE.md`
- `docs/TODO-Open-Items.md`
- `review-findings.md`
- `README.md`

These files let a non-coding owner supervise progress by reading current scope,
open work, review findings, evidence, and handoff notes.

### 3. Route Every Agent Through The Same Entry Point

Every AI session must know where to start. The start route should answer:

- what is current,
- what is archived,
- what is planned but inactive,
- what defects are active,
- what tests or docs prove the current state,
- what the owner still needs to decide.

### 3a. Layer Context By Need

Do not treat "use the repository" as permission to load every file.

Split context into layers:

- always-loaded instructions: short tool-specific rules such as `AGENTS.md`,
  `CLAUDE.md`, Cursor rules, Copilot instructions, or generic session rules,
- active control files: current SPEC, TODO, review findings, implementation
  notes, save-state, and current handoff,
- on-demand references: pattern catalog, anti-patterns, field notes, setup
  guides, localized docs, and other explanatory material,
- archive and evidence: old handoffs, logs, generated reports, historical
  notes, private data, and large local artifacts.

The AI should load the first layer by default, read only the relevant current
sections of the second layer, open the third layer when a question requires it,
and handle the fourth layer through bounded reads and path references.

This is a context-stability rule, not a new source-of-truth order. Current code,
tests, runtime docs, and the active SPEC still outrank old handoffs, archives,
external references, and AI memory.

### 3b. Route Natural-Language Intent

Do not assume users know SDAD command names, adapter names, or skill names.

Route ordinary requests by intent:

- review/audit: "check this", "review", "find bugs", "anything wrong",
- SPEC implementation: "implement", "fix", "build", "match the spec",
- release: "release", "publish", "tag",
- documentation: "docs", "README", "FAQ", "guide", "explain",
- handoff: "continue later", "handoff", "next session", "lost context",
- reference intake: "borrow from this repo", "can we adopt this idea",
- autonomy tuning: "asks too often", "runs ahead".

When one intent is dominant, state the interpreted intent, SDAD
scale/intensity, autonomy level, and expected evidence before proceeding. When
intents conflict in a way that changes scope or risk, ask one blocking
clarification question with a recommended default.

Intent routing is not automatic permission to expand scope, read the whole
repository, skip evidence, or bypass owner gates.

### 3c. Keep Codex Practice Governed

Codex is strongest when structure, context, and repeatable improvement loops are
available. In SDAD, useful Codex practice becomes governed operating behavior:

- issue-shaped prompts: write requests like a small issue or PR description,
  with target files, examples, constraints, non-goals, and expected evidence,
- environment improvement loop: when setup, scripts, env vars, or dependency
  gaps repeatedly block verification, route the fix to TODO, rules, templates,
  or handoff instead of rediscovering it each session,
- controlled task queue: use Codex-style background work for small fixes,
  exploratory branches, or follow-up ideas only when each item has a bounded
  packet, evidence expectation, and owner gate,
- optional multi-candidate review: use multiple candidate answers for design,
  refactor, performance, or migration tradeoffs, then record the chosen
  rationale in implementation notes or an ADR when durable.

Do not let a Codex queue become a hidden backlog. Queue items must either stay
outside active scope, enter `docs/TODO-Open-Items.md`, become a review finding,
or be captured in handoff/save-state. Do not treat the best candidate as
accepted until evidence and owner acceptance are visible.

### 4. Define Source Of Truth Order

Use this default order:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical integrated SPEC,
4. active or planned SPEC files,
5. current handoff files,
6. product notes and external references,
7. historical or archived records,
8. chat memory or AI confidence.

Apply current-over-historical precedence inside SPECs: when a SPEC contains a
timeline from past to present, the newest active/current section wins over older
sections. Older SPEC material explains why the project changed; it does not
automatically define what agents should implement now.

### 5. Split Work Ledgers

Keep separate ledgers for separate meanings:

- active implementation gaps,
- active defects and review findings,
- future ideas,
- archived plans,
- release or production-readiness gates.

This prevents "everything unfinished" from becoming one unreadable list.

### 6. Add Version Lanes When Needed

If a project has stable, beta, rewrite, or migration lines, define:

- allowed changes per lane,
- where agents should work,
- how fixes sync across lanes,
- which changes must not sync,
- how releases are tagged or packaged,
- how rollback works.

### 7. Name Risk Domains

Risk domains are parts of the system where generic coding advice is not enough.
Examples:

- authentication and tenant isolation,
- database migrations and backups,
- real-time callbacks,
- thread ownership and lock ordering,
- cross-platform file paths or APIs,
- release asset selection and auto-updaters,
- prompt contracts and model/tool boundaries.

Each risk domain needs specific review prompts, tests, docs, and handoff
evidence.

### 8. Make Completion Evidence-Based

Completion requires evidence appropriate to the slice:

- changed files,
- behavior changed,
- focused tests,
- regression tests where risk is high,
- docs checked or updated,
- implementation notes for spec-unstated decisions,
- remaining risks,
- known non-goals,
- owner acceptance.

For release or production claims, add deployment, migration, backup/restore,
observability, security, and rollback evidence as applicable.

### 9. Pressure-Test Plans Before Building

When a work packet is fuzzy, do a short clarification checkpoint before coding.

The AI should first inspect the repository. If current code, tests, active docs,
SPEC, ADRs, TODOs, or review findings answer the question, use that evidence
instead of asking the owner.

For unresolved ambiguity, ask only the next blocking question and include:

- the AI's recommended answer,
- why the question matters,
- what would change if the owner chooses differently.

Use this for scope ambiguity, overloaded terms, hard-to-reverse choices,
unclear evidence, and owner tradeoffs. Do not use it to reintroduce
micro-approval. Low-risk implementation assumptions may be stated and resolved
inside the approved packet; owner-controlled product, release, risk, data,
security, money, migration, or destructive decisions still require a checkpoint.

### 10. Keep Domain Language Bounded

When terminology starts drifting, stabilize the language instead of letting each
AI session invent its own names.

Define only terms that affect execution, review, tests, or owner decisions. Keep
definitions short, name aliases to avoid, and show important relationships when
they change implementation or verification.

Do not turn glossary work into another journal. Use active docs or SPEC when a
term belongs to the current feature. If a project repeatedly suffers from domain
language confusion, create a small optional `docs/domain-language.md` routed from
`docs/INDEX.md`; keep it glossary-only and separate from implementation notes,
handoffs, ADRs, and TODOs.

### 11. Use Cross-AI Review Deliberately

Use different AI sessions, models, or reviewers for different roles:

- planner,
- SPEC writer,
- builder,
- reviewer,
- QA/verifier,
- documentation maintainer.

The goal is not more AI output. The goal is independent pressure on assumptions,
bugs, missing tests, docs drift, and false completion claims.

### 12. Convert Lessons Into Rules

When a project hurts, do not only fix the bug. Ask:

- Should this become an `AGENTS.md` rule?
- Should it become a docs routing rule?
- Should it become a review checklist item?
- Should it become an implementation note so the next session knows why the
  code differs from the literal SPEC?
- Should it become a release gate?
- Should it become a test fixture?
- Should it become a "do not implement from archive" boundary?

This is the core loop: friction becomes reusable structure.

### 13. Make Implicit Rules Explicit

Do not rely on "the next AI will understand the obvious." Write the obvious
rules down when they affect execution:

- current beats historical,
- evidence beats confidence,
- active beats interesting,
- release readiness beats feature count,
- owner decision beats AI momentum,
- docs drift is a bug,
- hidden implementation memory becomes implementation notes,
- partial or unverified behavior must be labeled.

These rules are not bureaucracy. They protect the owner from silent scope drift,
false completion claims, stale SPEC execution, and unclear progress reporting.

### 14. Preserve Decisions With ADRs

Use Architecture Decision Records for decisions that future agents must not
re-litigate casually:

- architecture direction,
- source-of-truth changes,
- release or migration strategy,
- security or data boundary decisions,
- owner-approved tradeoffs.

ADRs preserve why a decision happened, not only what was chosen.

A decision normally deserves an ADR only when it is hard to reverse, would
surprise a future maintainer without context, and represents a real tradeoff.

Use implementation notes for smaller spec-unstated implementation choices that
need to survive handoff but are not durable enough for an ADR.

## Pattern Matrix

| Situation | Documentation-governance control | Release-governance control |
| --- | --- | --- |
| Fresh AI session starts in wrong context | Mandatory docs router and first-read loop | Version-specific rule file and workspace lane |
| Docs conflict with implementation | Source-of-truth order | Architecture responsibility map |
| AI says a feature is complete | Evidence handoff and TODO/review ledgers | Release gate and Critical 0 threshold |
| Code contains unstated implementation choices | Implementation notes with verification impact | ADR or owner gate when the choice affects release/risk |
| Plan is fuzzy before coding | Clarification checkpoint with recommended answer | Owner checkpoint when risk, release, data, security, or tradeoff changes |
| AI loads too much or too little context | Layered context route and bounded reads | Explicit resume package for release or migration work |
| User uses plain language instead of a skill name | Natural-language intent routing | Gate release, migration, destructive, data, auth, money, security, rollback, and production claims |
| Codex setup fails repeatedly | Environment improvement loop into rules, TODOs, templates, or handoff | Release readiness blocks until setup evidence is repeatable |
| Codex task queue accumulates side quests | Controlled task queue with packet boundaries | Owner gate before queue items become release scope |
| Several candidate solutions exist | Optional multi-candidate review | ADR or implementation note when the tradeoff is durable |
| Domain terms drift across sessions | Small glossary routed from `docs/INDEX.md` only when needed | ADR or SPEC update when terminology defines a durable boundary |
| Old plans keep resurfacing | Archive/product-note boundaries | Stable vs next lane boundaries |
| Refactor makes bugfixes hard to port | Canonical SPEC status | Old-to-new module mapping |
| High-risk runtime behavior exists | Minimum docs update sets | Thread/lock/danger-zone rules |
| Production readiness is unclear | Named hardening track | Pre-release checklist and rollback plan |

## Owner Progress View

A project using this pattern should be able to show the owner:

1. current active slice,
2. percent complete by scope, not by optimism,
3. open implementation gaps,
4. open review findings,
5. tests or commands that prove current state,
6. docs checked or updated,
7. clarification assumptions or owner questions resolved,
8. implementation notes when the SPEC did not state a decision,
9. context layer used and any bounded-read limits,
10. interpreted user intent when a request was routed from natural language,
11. next decision required from the owner,
12. expected risk before release or production use.

## Naming The Method

Recommended public name:

```text
SPEC-Driven AI Development
```

Precise description:

```text
Owner-supervised, SPEC-driven, multi-agent, evidence-based AI development.
```

Korean description:

```text
인간 오너 감독형, SPEC 주도, 다중 AI 교차검증 기반 개발 플로우.
```
