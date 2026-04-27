# Anti-Patterns

Status: Active reference
Scope: Failure modes to avoid in SPEC-driven AI development

Anti-patterns are recurring ways an AI-assisted project can look productive
while losing owner control, evidence quality, or current context. Use this file
during kickoff, review, and handoff.

## 1. AI Confidence As Completion

Symptom: the agent says the work is done because the explanation is coherent.

Why it fails: fluent summaries can hide missing tests, docs drift, migration
gaps, security regressions, or unverified runtime behavior.

Replace with: evidence-based handoff with changed files, commands run, results,
docs checked, remaining risks, and incomplete work.

## 2. Historical SPEC Override

Symptom: an older SPEC section, handoff, or archived plan overrides current code,
tests, active docs, or newer SPEC sections.

Why it fails: AI sessions often treat every written plan as active.

Replace with: current-over-historical precedence. Older material is rationale
unless reaffirmed in the active path.

## 3. Future Ideas In Active SPEC

Symptom: product notes, research links, and interesting ideas become
implementation requirements without owner promotion.

Why it fails: scope expands faster than verification.

Replace with: separate active SPEC, backlog, product notes, and archive routes.

## 4. Giant Master Plan Before Control Files

Symptom: the agent creates a large roadmap before `AGENTS.md`, `docs/INDEX.md`,
TODO, review findings, and source-of-truth rules exist.

Why it fails: the plan has no durable operating surface.

Replace with: bootstrap the control files first, then plan the first verified
slice.

## 5. One-Agent Finality

Symptom: the same agent plans, implements, reviews, accepts, and declares the
work complete.

Why it fails: one model/session repeats its own blind spots.

Replace with: separate builder, reviewer, QA, and owner acceptance roles for
risky work.

## 5a. Micro-Approval Thrash

Symptom: the AI stops after every tiny edit or TODO and waits for owner approval
before continuing.

Why it fails: owner supervision becomes a bottleneck, review has too little
substance to be useful, and implementation flow collapses.

Replace with: define a review-worthy development unit, let the AI proceed
autonomously inside that boundary, and hand off when changed files, checks,
limits, and evidence are ready. Stop early only for scope expansion, Q5 risk
changes, destructive actions, owner-controlled decisions, blocked verification,
or evidence conflicts.

## 6. Unscoped Percent Complete

Symptom: progress is reported as "80% done" without saying what scope is being
measured.

Why it fails: core MVP, full vision, release readiness, production readiness,
docs, and tests are different scopes.

Replace with: scope-specific status, such as "core MVP 80%, production readiness
40%, release packaging not started."

## 7. Handoff As Authority

Symptom: a handoff file is treated as more authoritative than current source,
tests, active docs, or active SPEC.

Why it fails: handoffs are snapshots and can become stale.

Replace with: use handoff to resume, then verify against source-of-truth order.

## 8. Docs Drift Normalization

Symptom: code behavior changes but docs are left stale because "the code is what
matters."

Why it fails: future AI sessions use docs as operating input.

Replace with: documentation consistency checks for every code change.

## 9. Silent Partial Implementation

Symptom: scaffolds, placeholders, degraded modes, skipped tests, or unsupported
platforms are not labeled.

Why it fails: later sessions and owners mistake partial work for complete work.

Replace with: explicit labels in TODO, review findings, docs, or release notes.

## 10. Release Readiness By Feature Count

Symptom: the project is called release-ready because the feature list is mostly
implemented.

Why it fails: release readiness also requires packaging, migration, rollback,
security, observability, manual checks, and risk decisions.

Replace with: a separate release or production-readiness gate.

## 11. Copy-Paste Fix Across Version Lanes

Symptom: a stable-line fix is copied into a rewrite or next-version lane without
checking architecture changes.

Why it fails: the same bug can need a different fix in a different architecture.

Replace with: lane mapping, sync rules, and "must not sync" notes.

## 12. Owner Rubber Stamp

Symptom: the owner is asked only to approve after the AI has silently chosen
scope, risk, and release posture.

Why it fails: owner supervision becomes ceremonial.

Replace with: mark owner decisions before scope expansion, release claims, risk
acceptance, and major tradeoffs.

## 13. Speculative Complexity

Symptom: the AI adds abstractions, configuration, generalized APIs, or defensive
paths that were not required by the active SPEC.

Why it fails: the owner receives more surface area to review, bugs hide in code
that does not yet need to exist, and simple work becomes expensive to verify.

Replace with: the smallest working design that satisfies the active SPEC and
evidence criteria. If a larger design is useful later, record it as backlog or
an owner decision.

## 14. Drive-By Refactor

Symptom: the AI edits adjacent code, comments, formatting, or old cleanup items
while doing an otherwise bounded task.

Why it fails: unrelated diffs make review harder and can break code the agent
did not understand deeply enough.

Replace with: surgical changes. Every changed line should trace to the active
work packet, active SPEC, review finding, or cleanup caused by the current edit.
Mention unrelated cleanup opportunities instead of performing them.
