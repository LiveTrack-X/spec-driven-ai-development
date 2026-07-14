# Implicit Rules Made Explicit

Status: Active reference
Scope: Obvious-but-dangerous rules for SPEC-directed AI development

Some rules feel obvious to a human owner but are easy for an AI session to miss.
This document turns those assumptions into explicit project rules.

Korean summary:

```text
당연해 보이지만 안 적으면 AI가 놓치기 쉬운 규칙들을 명시한다.
핵심 5개는 모든 프로젝트에서 적용하고, 확장 15개는 프로젝트 규모와 위험에 따라 적용한다.
```

## Core 5

These five rules should appear in every stateful SDAD project.

### 1. Current Beats Historical

Rule: current active code, tests, docs, and SPEC sections beat older SPEC
history, old handoffs, archived plans, and chat memory.

Why it matters: AI can read a long timeline and treat every historical idea as
still active. That creates regressions, scope creep, and repeated old decisions.

Operational form: before implementation or review, identify which SPEC section
is current. Treat older sections as rationale unless reaffirmed in the active
path.

### 2. Evidence Beats Confidence

Rule: AI confidence, fluent explanations, and "looks done" are never completion
evidence.

Why it matters: AI agents can sound certain while missing tests, migrations,
edge cases, docs drift, or runtime failures.

Operational form: every evidence-ready report must name commands run, results,
files changed, docs checked, remaining risks, and what is not complete. When a
handoff is needed, it links to that evidence and records only last-observed
status needed for recovery.

### 3. Active Beats Interesting

Rule: active SPEC scope beats interesting research, product notes, external
links, and future ideas.

Why it matters: AI tends to expand toward useful-looking ideas. That can turn a
small verified slice into an unreviewable rewrite.

Operational form: future ideas stay in backlog or product notes until the owner
promotes them into active SPEC.

### 4. Owner Decision Beats AI Momentum

Rule: the owner controls direction, priority, risk tolerance, and acceptance.

Why it matters: AI can keep moving because it can generate plausible next steps.
Momentum is not consent.

Operational form: mark decisions that require owner approval and do not silently
convert suggestions into active scope.

### 5. Repeated Pain Becomes A Rule

Rule: when the same confusion or bug pattern happens twice, convert it into a
repository rule, review checklist, test, or template.

Why it matters: chat memory does not scale across sessions.

Operational form: update `docs/Repository-Operating-Rules.md`,
`docs/INDEX.md`, prompts, tests, or templates so the lesson persists.

## Extended Rules

Use these when the project grows in scope, risk, team size, tool count, or
release maturity.

### 6. Small Verified Slices Beat Large Unverified Progress

Rule: prefer a review-worthy development unit with tests and docs over a broad
implementation that cannot be reviewed quickly.

Why it matters: non-coding owners need clear supervision points. Large AI
patches hide mistakes and make review expensive. But stopping after every
micro-task creates too much owner intervention and prevents useful flow.

Operational form: define the smallest useful work packet, review-worthy units,
acceptance evidence, and rollback or deferral path before implementation
expands. The packet may batch multiple related units when they belong to one
reviewable objective.

Stop for the owner only when scope expands, risk posture changes, a destructive
or irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or evidence conflicts with the plan.

### 6a. Implementation Discipline Makes Bounded Execution Safe

Rule: inside an approved work packet, the AI must surface assumptions, prefer
simple designs, make surgical diffs, and tie each step to verification.

Why it matters: low-intervention execution only works when the agent does not
hide confusion, overbuild, touch unrelated code, or claim success without a
goal-matched check.

Operational form: local low-risk assumptions may be stated and verified without
stopping. Product, risk, release, data, auth, money, destructive, or policy
assumptions require owner input.

### 7. Open Findings Beat New Features

Rule: critical review findings, failing tests, security regressions, and
production-readiness blockers take priority over feature expansion.

Why it matters: AI can keep adding capability while known defects become
normalized.

Operational form: if `review-findings.md` has critical or blocking items, do not
start broad feature work until the owner explicitly accepts the risk.

### 8. Explicit Non-Goals Beat Assumptions

Rule: if a feature, platform, workflow, or risk is not in active scope, it is not
implicitly included.

Why it matters: "reasonable assumptions" can become silent commitments.

Operational form: record non-goals in the active SPEC. Put unresolved work in
TODO or findings. A handoff points to those authorities when continuity needs
them.

### 9. Stated Uncertainty Beats Silent Guessing

Rule: unclear assumptions must be marked, not hidden.

Why it matters: AI often fills gaps with plausible defaults. Those defaults can
be wrong for product, security, cost, or release strategy.

Operational form: use "Assumption", "Needs owner decision", or "Not verified"
labels in the applicable SPEC, implementation note, TODO/finding, or evidence
report. A handoff links to the authoritative record.

### 9a. Repository Evidence Beats Unnecessary Questions

Rule: before asking the owner a clarification question, inspect current code,
tests, active docs, SPEC, TODOs, review findings, and ADRs when those sources
can answer it.

Why it matters: owner gates are valuable, but unnecessary questions create
approval fatigue and slow down work packets that are already bounded.

Operational form: use a clarification checkpoint for fuzzy plans. Ask only the
next blocking question, include the AI's recommended answer, and explain the
impact of a different answer. If the answer is a low-risk implementation
assumption, state it, proceed, verify, and record it when needed. If it changes
scope, product behavior, release posture, risk, data, security, money,
migration, destructive action, or an owner tradeoff, stop for the owner.

### 9b. Stable Terms Beat Session Vocabulary

Rule: when domain terms drift across sessions, define the execution-relevant
terms in active docs instead of letting each AI invent names.

Why it matters: unstable vocabulary creates duplicated concepts, mismatched
tests, and SPEC/code disagreement.

Operational form: define only terms that affect implementation, review, tests,
or owner decisions. For repeated domain-language confusion, add a small
`docs/domain-language.md` routed from `docs/INDEX.md`; keep it glossary-only,
not a handoff, TODO list, ADR, or implementation journal.

### 10. Degraded Or Partial Means Label It

Rule: scaffolds, placeholders, degraded behavior, dummy adapters, partial
support, skipped tests, and environment limitations must be named.

Why it matters: partial work can look complete to later sessions.

Operational form: label partial states in active docs, TODO, review findings, or
release notes. Do not hide them in prose.

### 11. Docs Drift Is A Bug

Rule: when behavior changes, stale docs are a project defect, not a cosmetic
issue.

Why it matters: AI agents often start from docs. Stale docs become future bugs.

Operational form: every code packet report must include a documentation
consistency check, even when no docs changed.

### 12. Handoff Is Context, Not Authority

Rule: handoff files help continuation but do not replace current behavior
evidence, the state-declared active SPEC, or current execution state.

Why it matters: handoffs can freeze a moment-in-time view that becomes stale.

Operational form: read a handoff only when state v2 declares it through optional
`current_handoff` and continuity is needed. Verify each pointer against the
authority for that fact type before implementing. It is never operating-state
authority.

### 13. Archive Preserves Memory, Not Active Work

Rule: archived docs preserve rationale and history. They do not define current
execution unless promoted back into active docs or SPEC.

Why it matters: deleting old docs loses context, but executing from them causes
stale work.

Operational form: archive old material with clear status instead of deleting it
or leaving it mixed with active docs.

### 14. Version Lanes Beat Copy-Paste Sync

Rule: stable, beta, rewrite, and migration lanes may share bugs but not always
the same fix.

Why it matters: architecture often changes across lanes. Blind sync can port the
wrong abstraction, old workaround, or release rule.

Operational form: define lane roles, sync rules, "must not sync" cases, and old
to new responsibility maps.

### 15. Release Readiness Beats Feature Count

Rule: a feature-complete project is not automatically release-ready or
production-ready.

Why it matters: release needs packaging, migration, rollback, security,
observability, manual checks, and known-risk decisions.

Operational form: keep release or production readiness as a separate gate with
explicit evidence.

### 16. Environment Limits Beat Overclaiming

Rule: if the current AI environment cannot verify something, say so.

Why it matters: platform, hardware, network, deployment, or data limitations can
make a claim unproven even when code looks correct.

Operational form: record what was verified locally, what was not verified, and
what requires owner or external tester confirmation.

### 17. Cross-Review Beats Single-Agent Finality

Rule: important changes should not be accepted solely because the builder says
they are correct.

Why it matters: the same model/session that made a mistake can miss it during
self-review.

Operational form: use another model, session, reviewer, or QA pass for risky
changes, releases, migrations, and security-sensitive work.

### 18. Scope-Specific Percent Beats Global Percent

Rule: completion percentages must name the scope they measure.

Why it matters: "80% done" can mean core runtime, MVP, production readiness,
full roadmap, docs, or release packaging.

Operational form: report progress by scope, such as core MVP, full vision,
production readiness, release readiness, docs, tests, and open blockers.

### 19. Failing Or Missing Tests Beat Narrative

Rule: failed tests, skipped tests, timeouts, missing coverage, and unrun checks
must be reported plainly.

Why it matters: summaries can accidentally hide the exact evidence an owner
needs.

Operational form: include test command, result, failure/skip/timeout status, and
why any check was not run.

### 20. Risk Gates Beat Convenience

Rule: security, data loss, migration, backup, tenant isolation, destructive
actions, real-time safety, and release-channel risks require explicit gates.

Why it matters: these are the areas where "quick implementation" can create
expensive damage.

Operational form: document risk domains, required checks, reviewer focus, and
release blockers.

### 21. Context Budget Beats Full Transcript

Rule: active control files should route fresh AI sessions, not replay the whole
project journal.

Why it matters: long state files, logs, generated artifacts, private corpora,
and broad search output can make AI chat sessions unstable or unverifiable even
when runtime code is not the problem.

Operational form: check file size before reading large routed files, use
headings and targeted sections, move old state into archives, and keep the
startup path focused on current objective, open items, constraints, validation,
and next steps.

### 22. Implementation Memory Beats Hidden Rationale

Rule: when implementation requires a choice the active SPEC did not explicitly
make, record the choice in implementation notes.

Why it matters: code often contains necessary judgments, compromises, and
unstated assumptions. If those stay only in chat memory, the next AI session or
human reviewer cannot distinguish intentional implementation from drift.

Operational form: record the SPEC gap, decision, reason, rejected alternatives,
verification impact, and follow-up in `docs/implementation-notes.md` for
Standard/Full SDAD. For Mini SDAD, include a short implementation-notes section
in the evidence-ready summary only when needed. Do not record raw internal
reasoning, every mechanical edit, or large logs.

### 23. Natural Language Intent Beats Skill Names

Rule: users should not need to know SDAD command names, adapter names, or skill
names before the AI can route the request.

Why it matters: real owners usually say "check this", "fix it", "release it",
"make the docs easier", or "create a handoff". If SDAD only works when users
name the exact skill, the workflow is brittle.

Operational form: infer matching intents from the user's wording and current
repository state. If multiple intents match, first decide whether they can be
safely composed inside one approved packet. State the interpreted intent, SDAD
scale, `execution_scope`, applicable owner gates, and expected evidence. If the combination
changes scope, risk, claim level, owner gate, or durable-doc requirements, ask
one blocking clarification question with a recommended default. Do not use
intent routing to bypass owner gates.

### 24. Guarantees Beat Guidance For Non-Negotiables

Rule: if a behavior must always happen or must never happen, enforce it with
tooling or a risk gate instead of relying only on an AI instruction file.

Why it matters: Markdown guidance can be missed under context pressure,
adapter differences, tool changes, or human error. Secrets, destructive
actions, migrations, release artifacts, production deploys, and
money/data/security boundaries need deterministic controls.

Operational form: keep the readable rule in the adapter or operating rules, but
back it with CI, required tests, validators, hooks, permissions, deny rules,
branch protection, release gates, artifact checks, or equivalent tooling. Use
guidance for judgment and enforcement for non-negotiable guarantees.
