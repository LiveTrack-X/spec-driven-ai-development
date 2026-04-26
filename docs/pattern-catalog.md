# Pattern Catalog

Status: Active reference
Scope: Combined workflow patterns distilled from CMP and DirectPipe

This catalog turns two real project styles into a reusable operating system for
SPEC-driven AI development.

- CMP contributes documentation routing, source-of-truth discipline, backlog
  separation, and production-readiness hardening.
- DirectPipe contributes version lanes, migration/release gates, architecture
  mapping, and explicit high-risk runtime rules.

No source code is copied here. The goal is to preserve the working method.

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
- remaining risks,
- known non-goals,
- owner acceptance.

For release or production claims, add deployment, migration, backup/restore,
observability, security, and rollback evidence as applicable.

### 9. Use Cross-AI Review Deliberately

Use different AI sessions, models, or reviewers for different roles:

- planner,
- SPEC writer,
- builder,
- reviewer,
- QA/verifier,
- documentation maintainer.

The goal is not more AI output. The goal is independent pressure on assumptions,
bugs, missing tests, docs drift, and false completion claims.

### 10. Convert Lessons Into Rules

When a project hurts, do not only fix the bug. Ask:

- Should this become an `AGENTS.md` rule?
- Should it become a docs routing rule?
- Should it become a review checklist item?
- Should it become a release gate?
- Should it become a test fixture?
- Should it become a "do not implement from archive" boundary?

This is the core loop: friction becomes reusable structure.

## Pattern Matrix

| Situation | CMP-style control | DirectPipe-style control |
| --- | --- | --- |
| Fresh AI session starts in wrong context | Mandatory docs router and first-read loop | Version-specific rule file and workspace lane |
| Docs conflict with implementation | Source-of-truth order | Architecture responsibility map |
| AI says a feature is complete | Evidence handoff and TODO/review ledgers | Release gate and Critical 0 threshold |
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
7. next decision required from the owner,
8. expected risk before release or production use.

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
