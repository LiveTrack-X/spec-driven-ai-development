# Starter Templates

These templates are for `spec-driven-ai-development` style projects. Adapt them
instead of copying blindly.

## Public Repo Positioning

Recommended repo name:

```text
spec-driven-ai-development
```

Display name:

```text
SPEC-Driven AI Development
```

Short description:

```text
Owner-supervised, multi-agent, evidence-based software development with AI agents and living SPECs.
```

Korean description:

```text
인간 오너가 방향과 완료 기준을 감독하고, 여러 AI 에이전트가 기획, SPEC, 구현, 리뷰, 검증을 나눠 수행하는 개발 운영 패턴입니다.
```

Core distinction:

```text
This is not just AI writing code from a spec.
It is a project-control loop where a human owner sets direction, AI agents draft specs and implementations, other models review the work, and completion is judged by evidence: code, tests, docs, and reproducible results.
```

Field-derived controls:

```text
Documentation-governance controls keep context, docs, SPECs, TODOs, review findings, and production-readiness status coherent across AI sessions.
Release-governance controls keep version lanes, migrations, releases, risk domains, and pre-release review honest.
Context-stability controls keep active state files short and prevent large logs, generated artifacts, old archives, or private data from flooding AI chat context.
Implementation-notes controls keep spec-unstated implementation decisions visible without turning AI reasoning into a transcript.
Clarification controls inspect repository evidence before asking the owner, then ask only the next blocking question with a recommended answer.
```

Implicit rules to include:

```text
Core 5: Current beats historical. Evidence beats confidence. Active beats interesting.
Owner decision beats AI momentum. Repeated pain becomes a rule.

Extended rules cover repository-evidence-first clarification, stable domain
language, docs drift, partial/degraded work, release readiness, environment
limits, cross-review, risk gates, review-worthy units, and scope-specific
progress.
```

## AGENTS.md Template

```markdown
# Project Agent Start Rules

Status: Active
Scope: Required starting point for AI agents and maintainers

## Mandatory Start Loop

Context Stability applies before every item in this start loop. Inspect file
size first and use bounded reads for large routed files.

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. The active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. The relevant active SPEC before architecture, policy, or behavior changes

## Context Stability Rule

Mandatory first reads are routing requirements, not permission to dump large
files into chat context. Before opening large state files, archives, logs,
generated artifacts, private data, or broad search results, check size and use
bounded reads: headings, current sections, targeted matches, output limits, and
explicit excludes.

Keep active live-state files short. Move old history to archive/history files
and link it instead of keeping long journals in the startup path.

Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

## Natural-Language Intent Routing

Do not require the owner to know SDAD terms, adapter names, or skill names.
Infer intent from the user's wording, current repository state, active SPEC,
TODOs, review findings, and risk gates.

- "check", "review", "audit", or "find bugs" -> review/audit intent.
- "implement", "build", "fix", or "match the spec" -> SPEC implementation intent.
- "release", "publish", or "tag" -> release intent with Level 4 gates.
- "document", "explain", "README", "FAQ", or "guide" -> documentation intent.
- "handoff", "continue later", "next session", or "lost context" -> handoff/save-state intent.
- "borrow from this repo", "reference this project", or "adopt this idea" -> reference-intake intent.
- "asks too often" or "runs ahead" -> autonomy tuning intent.

When one intent is dominant, state the interpreted intent, SDAD
scale/intensity, autonomy level, and expected evidence, then proceed. If
intents conflict in a way that changes scope or risk, ask one blocking
clarification question with a recommended default. Natural-language routing does
not bypass owner gates.

## Source Of Truth

When sources conflict, prefer:

1. Source code, migrations, tests, reproducible commands
2. Active runtime docs
3. Canonical SPEC
4. Active SPEC files
5. current handoff/save-state files
6. Product notes and external references
7. Historical or archived records
8. Chat memory or AI confidence

Read order is routing, not authority. Owner decisions control scope, risk
tolerance, and acceptance. They become durable source of truth only when recorded
in active docs, SPEC, ADR, or claim registry. A current handoff may carry the
decision for continuity until it is promoted; it does not turn weak evidence into
stronger evidence.

If a SPEC spans past-to-present history, current active sections override older
sections. Older SPEC material is rationale unless reaffirmed in the current
active path.

## AI Development Rules

- Do not treat AI confidence as completion.
- Do not rely on obvious-but-unwritten assumptions.
- Keep active implementation separate from future ideas.
- State SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
- Work in review-worthy development units inside the approved packet, not
  micro-approval steps.
- Continue autonomously inside the approved work packet until evidence is ready.
- When the plan is fuzzy, inspect repository evidence first and ask only the
  next blocking owner question with a recommended answer.
- Surface assumptions, prefer simple designs, make surgical changes, and verify
  goals.
- Record spec-unstated implementation decisions in `docs/implementation-notes.md`
  without storing raw internal reasoning or mechanical edit logs.
- Record blockers in `review-findings.md`.
- Record open implementation work in `docs/TODO-Open-Items.md`.
- Update docs when behavior changes.
- Do not implement from archived docs or product notes unless promoted into active SPEC.
- Label partial, degraded, scaffolded, skipped, or unverified behavior.
- If the project has stable/next versions, define version lanes and bugfix sync rules.
- If the project has high-risk domains, define domain-specific review checks.

## Handoff Rule

Long AI coding sessions are execution traces, not permanent memory. Specs are
authority, handoffs are continuity, archives are history, and fresh sessions are
for reliable execution.

Before closing, archiving, replacing, or restarting a long AI session, create a
session handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`.

Before handoff, state:

- project or repository name,
- branch or working context,
- current objective,
- SDAD scale / intensity used,
- changed files,
- autonomy level used,
- work packet completed,
- evidence-ready units,
- decisions made and why,
- implementation notes for spec-unstated decisions,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- constraints, owner preferences, and do-not-touch areas,
- what is not complete,
- owner decision needed, if any,
- next concrete steps,
- reactivation prompt for a fresh AI session.

Update `save-state.md` when work pauses, handoff to another AI/tool/person is
expected, owner direction or acceptance criteria changed, blocked/partial or
unverified state remains, or context would be expensive to reconstruct.

Fresh sessions should use bounded reads for large archives, logs, generated
artifacts, private data, and old handoffs instead of loading them in full.
```

## ADR Folder

```text
SPEC/adr/
  ADR-0001-template.md
```

Use ADRs for durable decisions that future AI sessions should not re-litigate
without new evidence or owner approval. A decision normally deserves an ADR only
when it is hard to reverse, would surprise a future maintainer without context,
and represents a real tradeoff.
