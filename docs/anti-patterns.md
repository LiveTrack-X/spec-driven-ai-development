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

Symptom: the AI stops after every tiny edit, TODO, or small SPEC item and waits
for owner approval before continuing.

Why it fails: owner supervision becomes a bottleneck, review has too little
substance to be useful, and implementation flow collapses.

Replace with: define a bounded work packet, use review-worthy units inside it
for review and evidence, and let the AI proceed autonomously until changed
files, checks, limits, and evidence are ready. Stop early only for scope
expansion, Q5 risk changes, destructive actions, owner-controlled decisions,
blocked verification, or evidence conflicts.

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

## 15. Evidence Surface Creep

Symptom: every feature creates a new verifier, digest, viewer, report, handoff
format, handoff report, or parallel evidence artifact.

Why it fails: evidence grows faster than user value, the owner cannot tell which
evidence matters, and review surfaces gain more buttons without a clearer next
action.

Replace with: add a new evidence surface only when it reduces owner review time,
protects a real safety boundary, supports a release or production gate, or makes
a baseline repeatable.

## 16. Evaluation Leakage

Symptom: prompts, harnesses, retrieval rules, review rules, or specs are tuned
against the same examples later used to claim final acceptance.

Why it fails: evidence can look stronger while the project is only overfitting
to the examples, traces, or owner review set already used during search.

Replace with: separate search evidence from owner acceptance evidence when
possible. If no held-out acceptance set exists, mark that absence as a risk and
do not claim generalized improvement.

## 17. Budget Fog

Symptom: an eval-driven loop is approved because it sounds useful, but no one
states how many candidates, runs, tokens, dollars, minutes, or owner-review
cycles it may consume.

Why it fails: "just one more iteration" turns a controlled work packet into an
open-ended optimization project.

Replace with: state a concrete budget before running expensive or repeated
evaluation loops, and stop when that budget is reached unless the owner approves
a new packet.

## 18. Live-State Context Bloat

Symptom: every fresh AI session starts by reading full state files, old handoffs,
large TODO journals, review ledgers, logs, generated reports, private data, or
tool output into chat context.

Why it fails: the AI chat becomes harder to audit, more expensive to resume, and
more likely to collapse under stale or irrelevant context. The project can look
broken even when runtime code is not involved.

Replace with: keep active live-state files as short routing summaries, move old
history to archive/history files, and use bounded reads for archives, logs,
generated artifacts, private data, and search output.

## 19. Hidden Implementation Memory

Symptom: the code differs from, extends, or compromises around the SPEC, but the
reason exists only in the AI chat or not at all.

Why it fails: later owners, reviewers, and AI sessions cannot tell whether a
difference was intentional, accidental, temporary, or blocked by verification.
They may re-litigate the same choice or mistake a compromise for the desired
design.

Replace with: implementation notes for spec-unstated assumptions, changes,
compromises, rejected alternatives, owner-relevant tradeoffs, follow-up, and
verification impact. Keep the notes bounded; do not store raw internal reasoning
or mechanical edit logs.

## 20. Question-First Without Repository Evidence

Symptom: the AI asks the owner broad clarification questions that current code,
tests, active docs, SPEC, TODOs, review findings, or ADRs could answer.

Why it fails: owner checkpoints become busywork, and the AI avoids doing the
basic repository inspection that makes its recommendation useful.

Replace with: inspect repository evidence first. If ambiguity remains, ask only
the next blocking question and include the AI's recommended answer, why it
matters, and what changes if the owner chooses differently.

## 21. Glossary Sprawl

Symptom: every session creates new terms, context files, or explanation pages
for vocabulary that does not affect implementation, review, tests, or owner
decisions.

Why it fails: the project gains another journal instead of a clearer operating
surface.

Replace with: define only execution-relevant terms. Use active docs or SPEC for
feature-local language, and create a small `docs/domain-language.md` routed from
`docs/INDEX.md` only when terminology drift repeats.
