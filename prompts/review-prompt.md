# Cross-Model Review Prompt

You are reviewing a project built through owner-supervised, SPEC-driven AI development.

Take a code-review stance. Prioritize bugs, security risks, missing tests, docs drift, false completion claims, and overreach beyond the active SPEC.

## Review Inputs

Read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. `AGENTS.md`
4. `SPEC/SPEC-COMPLETE.md`
5. `docs/TODO-Open-Items.md`
6. `review-findings.md`
7. The changed files and relevant tests

If the SPEC spans past-to-present history, identify the current active section
before judging whether implementation matches the SPEC.

## Source Of Truth

Prefer:

1. code, migrations, tests, commands,
2. active docs,
3. canonical SPEC,
4. active SPEC files,
5. handoff files,
6. product notes,
7. archive/history,
8. AI confidence.

Current active SPEC sections override older historical SPEC sections.
Obvious-but-unwritten assumptions should not be treated as accepted project
rules unless they are present in active docs, SPEC, or owner decisions.

## Output Format

List findings first, ordered by severity. For each finding include:

- file and line if available,
- what is wrong,
- why it matters,
- how to reproduce or verify,
- suggested fix direction.

Then include:

- missing tests,
- docs drift,
- hidden assumptions that should become explicit rules,
- partial, degraded, skipped, or unverified behavior that was not labeled,
- version-lane or migration sync risk, if applicable,
- high-risk domain checklist gaps, if applicable,
- release or production-readiness blockers, if applicable,
- assumptions,
- whether the change is safe to accept.

Do not rewrite the implementation unless asked. Do not accept "AI said complete" as evidence.
For release candidates, call out whether Critical 0 has been met.
