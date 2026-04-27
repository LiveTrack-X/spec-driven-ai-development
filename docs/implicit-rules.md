# Implicit Rules Made Explicit

Status: Active reference
Scope: Obvious-but-dangerous rules for SPEC-driven AI development

Some rules feel obvious to a human owner but are easy for an AI session to miss.
This document turns those assumptions into explicit project rules.

Korean summary:

```text
당연해 보이지만 안 적으면 AI가 놓치기 쉬운 규칙들을 명시한다.
핵심 5개는 모든 프로젝트에서 적용하고, 확장 15개는 프로젝트 규모와 위험에 따라 적용한다.
```

## Core 5

These five rules should appear in every SPEC-driven AI project.

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

Operational form: every handoff must include commands run, results, files
changed, docs checked, remaining risks, and what is not complete.

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

## Extended 15

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

### 6a. Implementation Discipline Makes Autonomy Safe

Rule: inside an approved work packet, the AI must surface assumptions, prefer
simple designs, make surgical diffs, and tie each step to verification.

Why it matters: low-intervention autonomy only works when the agent does not
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

Operational form: record non-goals in SPEC, TODO, or handoff. Promote them only
through owner decision.

### 9. Stated Uncertainty Beats Silent Guessing

Rule: unclear assumptions must be marked, not hidden.

Why it matters: AI often fills gaps with plausible defaults. Those defaults can
be wrong for product, security, cost, or release strategy.

Operational form: use "Assumption", "Needs owner decision", or "Not verified"
labels in handoff and review.

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

Operational form: every code handoff must include a documentation consistency
check, even when no docs changed.

### 12. Handoff Is Context, Not Authority

Rule: handoff files help continuation but do not outrank current code, tests,
active docs, or current SPEC.

Why it matters: handoffs can freeze a moment-in-time view that becomes stale.

Operational form: use handoff to resume, then verify against source-of-truth
order before implementing.

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
