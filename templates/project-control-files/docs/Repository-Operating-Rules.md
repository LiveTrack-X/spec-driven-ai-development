# Repository Operating Rules

Status: Active
Scope: Mandatory rules for code, documentation, review, verification, and handoff

## Purpose

This file collects repeated project rules so they do not remain only in chat,
handoff notes, or one AI session's memory.

## Mandatory Start Loop

Before changing code, prompts, SPECs, docs, migrations, release assets, or
automation:

1. Read `docs/INDEX.md`.
2. Read this file.
3. Read `docs/TODO-Open-Items.md` and `review-findings.md` for implementation,
   hardening, or bugfix work.
4. Read `SPEC/SPEC-COMPLETE.md` and any relevant active SPEC.
5. Inspect the current source code and tests before implementing from a plan.

Do not begin from archived docs, old plans, product notes, or stale handoff
files without checking `docs/INDEX.md`.

## Source Of Truth

When sources conflict, prefer:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical SPEC,
4. active SPEC files,
5. current handoff files,
6. product notes and external references,
7. historical or archived records,
8. chat memory or AI confidence.

If a SPEC spans past-to-present history, current active sections override older
sections. Older SPEC material explains rationale; it does not define current
implementation unless reaffirmed in the active path.

## Code Consistency Rules

- Keep changes scoped to the active SPEC slice.
- Prefer additive changes unless a migration plan allows breaking changes.
- Label scaffolds, placeholders, and dummy adapters in active docs and TODO.
- Avoid broad rewrites while blocking review findings remain open.
- If the project has risk domains, follow the domain-specific checklist before
  handoff.

## Documentation Consistency Rules

- Use the minimum documentation update sets in `docs/INDEX.md` before handoff.
- If behavior changed, update the relevant active docs in the same change.
- If implementation status changed, update `SPEC/SPEC-COMPLETE.md` and
  `docs/TODO-Open-Items.md`.
- If a review finding is closed, update `review-findings.md`.
- If no doc content changed, state which docs were checked and why no update was
  needed.

## Review And Verification Rules

- Do not accept AI confidence as evidence.
- Important changes should receive a separate review pass by another AI, model,
  session, or human reviewer.
- Review should prioritize bugs, security, data loss, docs drift, missing tests,
  overreach beyond SPEC, and false completion claims.
- Release or production readiness requires deployment, migration, security,
  backup/restore, monitoring, rollback, and manual evidence as applicable.

## Version Lane Rules

If the project has stable, beta, rewrite, migration, or platform lanes, document:

- allowed changes per lane,
- which directory or branch each lane uses,
- bugfix sync rules,
- changes that must not sync,
- release-channel and rollback rules.

## Handoff Rules

Every handoff must include:

- changed files,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- open findings,
- remaining risks,
- what is not complete,
- owner decision needed, if any.
