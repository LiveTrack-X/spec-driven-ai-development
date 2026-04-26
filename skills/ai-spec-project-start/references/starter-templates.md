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
CMP-style controls keep context, docs, SPECs, TODOs, review findings, and production-readiness status coherent across AI sessions.
DirectPipe-style controls keep version lanes, migrations, releases, risk domains, and pre-release review honest.
```

## AGENTS.md Template

```markdown
# Project Agent Start Rules

Status: Active
Scope: Required starting point for AI agents and maintainers

## Mandatory First Read

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. The active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. The relevant active SPEC before architecture, policy, or behavior changes

## Source Of Truth

When sources conflict, prefer:

1. Source code, migrations, tests, reproducible commands
2. Active runtime docs
3. Canonical SPEC
4. Active SPEC files
5. Handoff/save-state files
6. Product notes
7. Historical or archived records
8. Chat memory or AI confidence

## AI Development Rules

- Do not treat AI confidence as completion.
- Keep active implementation separate from future ideas.
- Record blockers in `review-findings.md`.
- Record open implementation work in `docs/TODO-Open-Items.md`.
- Update docs when behavior changes.
- Do not implement from archived docs or product notes unless promoted into active SPEC.
- If the project has stable/next versions, define version lanes and bugfix sync rules.
- If the project has high-risk domains, define domain-specific review checks.

## Handoff Rule

Before handoff, state:

- changed files,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- what is not complete,
- owner decision needed, if any.
```
