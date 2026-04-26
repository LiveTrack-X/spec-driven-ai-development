---
name: ai-spec-project-start
description: >-
  Use when starting, publishing, or reorganizing a project around
  SPEC-driven AI development as practiced by a human owner who does not
  necessarily write code directly but supervises product direction, AI planning,
  AI implementation, cross-model review, evidence-based verification, and
  completion decisions. Trigger for new project kickoff, AGENTS.md/docs/SPEC/TODO
  bootstrap, owner-supervised AI coding, multi-agent review loops, converting
  lessons from a previous project into reusable operating rules, or creating a
  public template/repo such as spec-driven-ai-development.
---

# AI-SPEC Project Start

## Identity

Treat this workflow as:

```text
Owner-supervised, SPEC-driven, multi-agent, evidence-based AI development.
```

Korean:

```text
인간 오너 감독형, SPEC 주도, 다중 AI 교차검증 기반 개발 플로우.
```

This is not "AI writes code from a spec." It is a project-control loop where a
human owner keeps direction, priority, risk judgment, and final acceptance while
AI sessions take roles such as planner, spec writer, builder, reviewer, QA, and
documentation maintainer.

## Core Assumption

The owner may understand logic, architecture, product intent, risks, and user
pain without personally writing implementation code. Design the project system so
that the owner can still govern development through:

- clear SPECs,
- explicit non-goals,
- small implementation slices,
- cross-model review,
- reproducible tests,
- active TODO/review ledgers,
- and evidence-based completion criteria.

## Operating Loop

Use this sequence:

```text
1. Prior project pain or product need
2. Owner + AI planning conversation
3. SPEC draft with scope, non-goals, risks, acceptance criteria
4. Builder AI implements a small slice
5. Separate AI/model/session reviews the result
6. Tests, docs, and reproducible commands verify evidence
7. Owner accepts, revises, defers, or rejects
8. Lessons become operating rules, TODOs, or archived notes
```

Never collapse steps 4-7 into "AI said it is done." Completion is a decision
based on evidence.

## First Conversation

Before writing code, extract the owner's control model:

- What previous project pain triggered this project?
- What would have made that previous project easier?
- What must the next AI session know before touching code?
- Which decisions must remain owner-controlled?
- What is the smallest useful result?
- What is explicitly not active work yet?
- What evidence proves a slice is complete?

If the owner has already given enough context, proceed and mark assumptions.

## Required Project Control Files

Create or update these early:

- `AGENTS.md`: mandatory rules for every AI agent/session.
- `docs/INDEX.md`: the single routing table for active docs.
- `SPEC/SPEC-COMPLETE.md`: current integrated product and implementation baseline.
- `docs/TODO-Open-Items.md`: current open work only.
- `review-findings.md`: active bug/review findings only.
- `README.md`: human-facing current project summary.

Optional but useful:

- `save-state.md`: current handoff if work pauses.
- `next-task.md`: next recommended slice.
- `docs/archive/`: historical docs and completed plans.
- `docs/product-notes/`: reference ideas that are not active implementation.

## Source Of Truth

When sources disagree, prefer:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical SPEC,
4. active SPEC files,
5. handoff/save-state files,
6. product notes and external references,
7. archived or historical docs,
8. chat memory or AI confidence.

## AI Role Split

Use role separation to reduce single-model blind spots:

- Planning AI: turns owner pain into product scope and non-goals.
- SPEC AI: writes implementation-ready SPEC with acceptance criteria.
- Builder AI: implements a bounded slice.
- Reviewer AI: finds bugs, security risks, missing tests, docs drift, and overreach.
- QA AI: tries to reproduce behavior and verify commands.
- Maintainer AI: updates docs, TODO, findings, and handoff.
- Owner: sets direction, priority, risk tolerance, and final acceptance.

One AI session may perform more than one role, but important changes should get a
separate review pass.

## SPEC Rules

Keep three layers distinct:

- Vision: desired future and product philosophy.
- Active SPEC: implementation scope for now, with completion criteria.
- Research/backlog: useful ideas not approved for current implementation.

Do not let research notes become active work just because they are exciting.
Do not let a SPEC claim implementation status without code/test evidence.

## Evidence Rules

Every implementation handoff must include:

- changed files,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- what is not complete,
- owner decision needed, if any.

For production-readiness claims, require deployment, migration, auth/security,
backup/restore, monitoring, and rollback evidence as applicable.

## Pain-To-Rule Extraction

When the owner references a previous project, convert pain into reusable rules.

Examples:

- "AI sessions forgot context" -> require `AGENTS.md` and `docs/INDEX.md`.
- "Docs were scattered" -> require document classes and archive rules.
- "AI said complete but bugs remained" -> require review findings and tests.
- "Old plans misled new sessions" -> define source-of-truth order.
- "Large refactors became hard to verify" -> require small slices and cross-review.

This is the heart of the workflow: past friction becomes future operating
structure.

## Bootstrap Output

For a new project, produce a compact bootstrap rather than a huge master plan:

1. product definition,
2. first user and first use case,
3. non-goals,
4. risk list,
5. required control files,
6. first active SPEC slice,
7. validation commands,
8. review loop.

Use `references/starter-templates.md` for copyable prompts and file templates.

## Guardrails

- Keep the owner in control of scope and acceptance.
- Keep AI output auditable.
- Keep active docs smaller and clearer than archives.
- Keep future ideas out of the active implementation path.
- Prefer a boring verified slice over an impressive unverified expansion.
- Use Korean for owner-facing explanation when helpful; keep filenames and
  machine-facing identifiers stable and ASCII.
