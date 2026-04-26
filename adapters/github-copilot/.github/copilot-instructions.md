# SPEC-Driven AI Development Instructions

Use owner-supervised, SPEC-driven, evidence-based development in this repository.

## Required Reading

Before implementation, review:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. `SPEC/SPEC-COMPLETE.md`
4. `docs/TODO-Open-Items.md`
5. `review-findings.md`
6. relevant source code and tests

## Source Of Truth

Prefer current code, migrations, tests, and reproducible commands over docs.
Prefer active docs over SPEC. Prefer current active SPEC sections over older
historical SPEC sections. Treat handoffs and archive/history as context, not
authority.

## Review And Implementation Rules

- Evidence beats AI confidence.
- Do not claim completion from AI confidence.
- Keep changes scoped to the active SPEC slice.
- Do not promote future ideas into active work without owner decision.
- Label partial, scaffolded, degraded, skipped, environment-limited, or unverified behavior.
- Update docs or state which docs were checked and why no update was needed.
- Treat critical review findings, failing tests, security regressions, and release blockers as higher priority than new features.
- For release or production readiness, require migration, security, backup/restore, monitoring, rollback, and manual evidence as applicable.

## Response Expectations

When summarizing work, include changed files, tests run, docs checked, remaining
risks, incomplete work, and owner decisions needed.
