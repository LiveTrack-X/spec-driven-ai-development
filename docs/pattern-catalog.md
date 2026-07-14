# Pattern Catalog

Status: Active reference
Scope: Combined workflow patterns distilled from anonymized field projects

This catalog turns field governance practice and compatible clarification
patterns into an optional pattern set for SPEC-directed AI development. The
catalog does not turn SDAD into an operating system or prescribe the method used
inside a work boundary.

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
- Repository-control-surface practice contributes the separation between
  always-loaded guidance, routed rules, on-demand procedures, isolated
  exploration, enforced guarantees, and reviewed project memory.
- Cost-aware agent-routing practice contributes lean execution, advisor
  checkpoints, orchestrator-worker packets, and bounded loops that preserve
  evidence and owner gates while reducing unnecessary model/tool spend.
- Reference-parity practice contributes a small review gate for rebuilding from
  an existing product, repo, design, demo, or field project without copying its
  implementation or losing its essential behavior.
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

The logical control spine is:

```text
Scale/compress -> Execution scope -> Active SPEC slice -> Work packet -> Validation/owner gates -> Evidence-ready -> Owner decision -> Maintenance
```

Scale selects the persistent control surface; `execution_scope` selects the
current `unit` or `packet` boundary; owner gates protect specific actions.
Validation and reference gates happen before evidence-ready. Owner acceptance
happens after evidence, not because a gate passed.

### 1. Start From Pain

The project begins with a concrete friction:

- a previous project became hard to resume,
- AI sessions lost context,
- docs scattered,
- completion claims were hard to trust,
- release or migration risk grew faster than the plan.

Convert that pain into an operating rule before writing new code.

### 2. Create Control Files Before Expansion

For Standard and Full SDAD, create the core control files before expanding
implementation:

- `AGENTS.md`
- `sdad-state.yaml`
- `docs/INDEX.md`
- `docs/Repository-Operating-Rules.md`
- `SPEC/SPEC-COMPLETE.md`
- `docs/TODO-Open-Items.md`
- `review-findings.md`
- `README.md`

These files let a non-coding owner supervise progress by reading the current
packet, validation contract, open work, review findings, and evidence.

For One-shot, Mini SDAD, or a small Standard packet, apply the Small Project
Compression Rule before creating this full set. A single evidence-ready summary
is better than stale control files when no durable surface has an active job.

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
- startup route: adapter -> `sdad-state.yaml` -> `docs/INDEX.md`,
- active control files: current SPEC, targeted source/tests, TODO, review
  findings, and implementation notes selected for the current intent,
- optional continuity: the state-declared `current_handoff`, read only for
  resume/handoff intent and used only as pointers plus last-observed status,
- on-demand references: pattern catalog, anti-patterns, field notes, setup
  guides, localized docs, and other explanatory material,
- archive and evidence: old handoffs, logs, generated reports, historical
  notes, state-v1 `save-state.md`, private data, and large local artifacts.

The AI should load the adapter and startup route by default, select only the
current controls needed for the intent, load continuity only when needed, open
on-demand references when a question requires them, and handle archive/evidence
through bounded reads and path references.

This is a context-stability rule, not a new authority model. Current source,
tests, and runtime establish observed behavior; the state-declared active SPEC
establishes intended scope and acceptance criteria. Old handoffs, archives, external
references, and AI memory establish neither.

### 3b. Route Natural-Language Intent

Do not assume users know SDAD command names, adapter names, or skill names.

Route ordinary requests by intent:

- review/audit: "check this", "review", "find bugs", "anything wrong",
- SPEC implementation: "implement", "fix", "build", "match the spec",
- release: "release", "publish", "tag",
- documentation: "docs", "README", "FAQ", "guide", "explain",
- handoff: "continue later", "handoff", "next session", "lost context",
- reference intake: "borrow from this repo", "can we adopt this idea",
- execution control: "asks too often", "runs ahead".

Treat narrative modifiers as routing signals, not automatic scope expansion.
"Carefully", "thoroughly", or "audit the whole flow" increases inspection depth
inside the current scope; it does not authorize unrelated refactors. "Fully" or
"end-to-end" means continue to evidence-ready for the approved scope and stop at
owner gates; it does not mean owner-accepted. "Quickly", "lightly", or "minimal"
selects compression, not weaker evidence. "Commit and wait" does not imply push,
release, or deploy unless those are named.

If multiple intents match, first decide whether they can be safely composed
inside one approved packet. When one route remains dominant, state the
interpreted intent, SDAD scale, `execution_scope`, applicable owner gates, and
expected evidence before proceeding. If the combination changes scope, risk,
claim level, owner gate, or durable-doc requirements, ask one blocking
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
  or implementation notes instead of rediscovering it each session,
- controlled task queue: use Codex-style background work for small fixes,
  exploratory branches, or follow-up ideas only when each item has a bounded
  packet and evidence expectation; require owner gates only for protected
  actions,
- optional multi-candidate review: use multiple candidate answers for design,
  refactor, performance, or migration tradeoffs, then record the chosen
  rationale in implementation notes or an ADR when durable.

Do not let a Codex queue become a hidden backlog. Queue items must either stay
outside active scope, enter `docs/TODO-Open-Items.md`, become a review finding,
or become an approved packet. A handoff may point to those authorities only
when continuity is needed. Do not treat the best candidate as accepted until
evidence and owner acceptance are visible.

### 3d. Layer Repository Control Surfaces

Do not put every AI rule into one always-loaded instruction file. SDAD separates
control surfaces by what they can reliably do:

- always-loaded guidance: short adapter rules every session should read,
- routed guidance: path, domain, risk, or intent rules loaded only when needed,
- on-demand procedure: repeatable playbooks, checklists, or skills,
- isolated exploration: broad research or comparison that returns a bounded
  summary instead of flooding the main context,
- enforced guarantee: CI, tests, validators, hooks, permissions, deny rules, or
  release gates that must run or must block regardless of AI memory,
- reviewed memory: implementation notes, ADRs, operating rules, and trace links
  that are safe for later sessions to trust,
- continuity checkpoint: an optional state-declared current handoff containing
  authority pointers and last-observed results, not duplicated decisions or
  current state.

Guidance vs enforcement is a safety boundary. Use guidance for judgment,
style, source-of-truth order, and owner-gate criteria. Use enforcement for
secrets, destructive commands, migrations, release artifacts, production
deploys, money/data/security boundaries, required tests, and generated-artifact
exclusion. If the project would be unsafe when the AI follows a rule only most
of the time, the rule belongs in an enforced surface or explicit risk gate, not
only in Markdown.

Route repeated work by type: research goes to isolated context, procedure goes
to a skill or playbook, guarantees go to enforcement, durable rationale goes to
ADR, spec-unstated implementation choices go to implementation notes, and
repeated failures become operating rules, tests, validators, templates, or
review gates.

Run a control surface checkup when rules, skills, MCP servers, plugins, hooks,
permissions, or local tool instructions appear stale, duplicated, slow, or
overloaded. The report can be evidence-ready, but applying cleanup, auto-mode,
permission, hook, or tool-version changes requires the appropriate owner gate.

See
[field-notes/repository-control-surface-method.md](field-notes/repository-control-surface-method.md).

### 4. Define Authority By Fact Type

Use startup order for routing, not as one universal precedence list:

- current source, tests, runtime, and reproducible commands establish observed
  behavior;
- `sdad-state.yaml#active_spec` establishes intended scope, behavior, and
  acceptance criteria;
- state and active ledgers establish current execution and unresolved work;
- an owner-decision record establishes authorization or acceptance only for its
  declared packet, action, conditions, and expiry;
- a handoff establishes continuity pointers only;
- planned SPECs, references, archives, filenames, dates, and chat cannot
  activate requirements.

Read order is routing, not authority. Owner decisions control scope, risk
tolerance, protected actions, and result acceptance only for their recorded boundary.

`SPEC-COMPLETE.md` is an integrated baseline, not an automatic override of the
state-declared active SPEC. Another SPEC is normative only for the exact scope
incorporated by the active entrypoint or after a packet transaction switches
that pointer. ADRs explain durable rationale; they cannot silently override
normative scope or acceptance criteria.

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

Each risk domain needs specific review prompts, tests, docs, and evidence. Add a
handoff pointer only when another session needs continuity.

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

For product, hardware, compatibility, package, remote tester, or user-facing
claims, use the optional Product evidence templates:

- Evidence Matrix: requirement or claim to evidence mapping,
- Claim Registry: allowed, qualified, blocked, and forbidden claims,
- Artifact Contract: required files, metadata, verifier, privacy, retention, and
  lineage for generated or imported artifacts,
- Delivery Readiness Model: explicit states from `ai_complete` through
  `production_ready`,
- Remote Evidence Import / Quarantine Pattern: quarantine, validation, privacy,
  review, and acceptance before claim changes.

These templates should reduce active-doc bloat by keeping TODOs and findings
focused on current decisions while evidence history, raw logs, and imported
bundles stay linked by ID or archived path.

### 8a. Use A Reference Parity Review Gate

When a work packet rebuilds, ports, abstracts, or borrows from an existing
product, repository, design, demo, or field project, do a small reference
parity review before calling the packet evidence-ready.

The goal is not source-code cloning, framework mimicry, or pixel-perfect
matching unless the owner explicitly asks for that. The goal is to preserve the
essential behavior, state model, evidence boundaries, and user-visible control
surface that made the reference useful.

Use a compact parity map:

- source behavior or control,
- implemented behavior or control,
- evidence path,
- known gap or deferred claim.

Check at least the pieces that define user value or owner risk: primary
workflows, mode or route distinctions, visible state labels, data persistence,
runtime/live-state differences, role or permission boundaries, generated or
imported artifacts, and claim qualifiers. For UI/product work, screenshot review
can be evidence when it checks a visible behavior or layout claim. For server,
package, hardware, or deployment work, keep test runtime, live runtime, and
persisted state as separate evidence tiers.

If parity gaps are outside the approved packet, name them as non-goals or
deferred review findings. Do not let a thin implementation pass evidence-ready
only because tests exercise the happy path while reference-critical behavior is
missing.

### 8b. Match Evidence Tiers To Claims

Evidence tier controls what the project may claim. Keep these tiers distinct:

- local test: source-level behavior, unit/contract/CLI checks, and regressions,
- browser render: visible UI, interaction, layout, and screenshot-reviewed
  controls,
- live runtime: a real local/dev process with configured dependencies,
- persisted state: reload, restart, import/export, or stored state checks,
- remote hardware: named device, tester, lab, or external-machine evidence
  after quarantine and review,
- production evidence: deployed, packaged, monitored, rollback-ready, or
  release-channel evidence for the named environment.

Do not let a lower tier unlock a higher claim. A local test does not prove
hardware compatibility. A browser screenshot does not prove persistence. A
remote tester bundle does not prove production readiness until production
evidence and owner gates exist.
No evidence tier grants owner acceptance without an owner decision or a
delegated acceptance policy.

### 8c. Compress Small Projects Before Adding Files

Small Project Compression Rule: create the smallest evidence surface that keeps
the owner in control. One evidence-ready summary is enough for One-shot, Mini
SDAD, or a small Standard packet when the packet has one active slice, no
protected-action owner gate changed, no unresolved finding must survive the turn, no durable
spec-unstated decision exists, no handoff is expected, and evidence can be
shown compactly.

Turn on separate surfaces only when their job exists: SPEC for changed behavior
or acceptance criteria, TODO for continuing work, review findings for active
defects or blocked gates, implementation notes for durable spec-unstated
choices, a packet-bound `current_handoff` only for cross-session continuity, and
product evidence templates for claims that need mapped evidence, claim
boundaries, artifact contracts, or remote evidence review. State-v2 work never
creates or routes `save-state.md`; an existing copy is v1 migration/history.

### 9. Use A Slice-First Evidence Loop

For feature delivery, prefer one vertical slice as the approved work packet or
review-worthy unit. A slice should connect behavior to evidence across the
smallest useful path, not split the work into isolated layers that cannot prove
user value.

Use the order: PLAN narrows intent, SPEC fixes the active slice, optional ADR
records hard-to-reverse decisions only when needed, TODO/work packet turns the
slice into current work, and JIT resolves missing slice details just before
implementation.

Use JIT clarification only for unresolved slice decisions. JIT means "resolve
the missing detail at the moment it matters"; it does not mean ignoring current
repository evidence, active SPECs, tests, or operating rules. Inspect routed
current evidence first, then ask the next blocking question only when the slice
still cannot be implemented safely.

Start with the strongest practical failing test or check for the slice. This may
be a unit, contract, integration, E2E, CLI smoke, snapshot, build, lint, or
manual verification check depending on the risk and project shape. Do not force
E2E tests when a narrower check proves the claim, and do not skip stronger
evidence when the claim needs it. Use TDD when behavior can be specified before
implementation; use an equivalent failing check when the work is docs, config,
tooling, migration, or verification-only.

When evidence depends on a CLI, API, file, manifest, or UI text shape, define
that output contract in the active SPEC or artifact contract before treating a
green command as proof. A command can prove "this output matched this contract";
it cannot prove an unstated contract.

Treat green results as evidence-ready, not owner-accepted. Use ADRs only when
the slice introduces hard-to-reverse architecture, policy, release, security,
data-boundary, or owner tradeoff decisions. Keep successful evidence summarized
and linked by command, artifact path, or report; keep `review-findings.md`
focused on defects, risks, and unresolved review items.

### 10. Use Cost-Aware Agent Routing

Route model/tool effort by packet difficulty, evidence need, and owner risk.
Start with a Lean Execution Contract: inspect current evidence, act when enough
information exists, use the simplest solution, report only evidenced claims,
pause only for real owner gates, and lead with the outcome.

Add an Executor-Advisor pattern when one executor can do most of the work but a
hard judgment needs review. Advisor checkpoints are useful before approach
commitment, when evidence conflicts with the plan, when repeated errors appear,
or before evidence-ready on a complex packet. Advisor approval is review evidence, not owner acceptance.

Add an Orchestrator-Worker pattern when independent units can run with isolated
context, parallelism, or specialization. Each worker needs a task boundary,
non-goals, output contract, evidence requirement, and escalation rule. Worker
completion is candidate evidence until the orchestrator integrates conflicts
against each fact's authority and the state-declared active SPEC.

Use Loop Engineering only when the next run has a clear trigger and stop rule:
turn-based, goal-based, time-based, or event-based. Every loop must declare its
done condition, maximum turns/runtime/spend, evidence contract, stop rules,
owner gate, and state surface. Scheduled and event-based loops belong in
enforced or automated surfaces, not hidden chat habits.

See
[field-notes/cost-aware-agent-routing-method.md](field-notes/cost-aware-agent-routing-method.md).

### 11. Gate Evaluation-Driven Harness Extensions

For harness optimization, self-improving loops, retrieval/memory tuning, or
repeated evaluation automation, keep the work behind the Advanced Extension Fit
Gate. The SDAD abstraction of Meta-Harness is: fixed base model and tool
surface, bounded candidate harness interface, search/held-out split, baseline
comparison, offline/online trace retention, leakage-risk review, concrete
budget, and owner adoption gate. See
[field-notes/meta-harness-method.md](field-notes/meta-harness-method.md).

### 12. Pressure-Test Plans Before Building

When a work packet is fuzzy, do a short clarification step before coding.

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

### 13. Keep Domain Language Bounded

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

### 14. Use Cross-AI Review Deliberately

Use different AI sessions, models, or reviewers for different roles:

- planner,
- SPEC writer,
- builder,
- reviewer,
- QA/verifier,
- documentation maintainer.

The goal is not more AI output. The goal is independent pressure on assumptions,
bugs, missing tests, docs drift, and false completion claims.

### 15. Convert Lessons Into Rules

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

### 16. Make Implicit Rules Explicit

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

### 17. Preserve Decisions With ADRs

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
need to survive sessions and review but are not durable enough for an ADR.

## Pattern Matrix

| Situation | Documentation-governance control | Release-governance control |
| --- | --- | --- |
| Fresh AI session starts in wrong context | Mandatory docs router and first-read loop | Version-specific rule file and workspace lane |
| Docs conflict with implementation | Source-of-truth order | Architecture responsibility map |
| AI says a feature is complete | Evidence-ready report and TODO/review ledgers | Release gate and Critical 0 threshold |
| Code contains unstated implementation choices | Implementation notes with verification impact | ADR or owner gate when the choice affects release/risk |
| Plan is fuzzy before coding | Infer from repository evidence, then ask one blocking question with a recommended answer | Owner gate when risk, release, data, security, or tradeoff changes |
| AI loads too much or too little context | Layered context route and bounded reads | Explicit resume package for release or migration work |
| User uses plain language instead of a skill name | Natural-language intent routing | Gate release, migration, destructive, data, auth, money, security, rollback, and production claims |
| Codex setup fails repeatedly | Environment improvement loop into rules, TODOs, templates, or implementation notes | Release readiness blocks until setup evidence is repeatable |
| Codex task queue accumulates side quests | Controlled task queue with packet boundaries | Owner gate before queue items become release scope |
| Several candidate solutions exist | Optional multi-candidate review | ADR or implementation note when the tradeoff is durable |
| Existing product, repo, demo, or design is used as a reference | Reference Parity Review Gate with source behavior -> implemented behavior -> evidence | Owner gate before reference-critical gaps become release or production claims |
| Claim depends on environment or product scope | Evidence tier matched to claim level | Block or qualify claims that outrun the observed tier |
| Evidence depends on command/API/file shape | Output contract named in SPEC or artifact contract before the check is evidence | Block claims based on unstated output formats |
| Small packet would create more docs than evidence | Small Project Compression Rule | One evidence-ready summary unless a durable surface has an active job |
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
10. reference parity gaps or deferred claims when rebuilding from existing work,
11. interpreted user intent when a request was routed from natural language,
12. next decision required from the owner,
13. expected risk before release or production use.

## Naming The Protocol

Recommended public name:

```text
SDAD Protocol
```

Expanded name:

```text
SPEC-Directed AI Development
```

Precise description:

```text
A repository-local operating protocol for AI-assisted development.
```

Korean description:

```text
저장소 기반 AI 보조 개발 운영 프로토콜.
```

Main slogan:

```text
Use any method. Keep scope, evidence, and owner authority clear.
```
