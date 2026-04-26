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

Do not start from archived docs, historical plans, product notes, or old handoff files without checking `docs/INDEX.md` first.

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

If a SPEC spans past-to-present history, current active sections override older
sections. Older SPEC material is rationale unless reaffirmed in the current
active path.

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
