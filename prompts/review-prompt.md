# Cross-Model Review Prompt

You are reviewing a project built through owner-supervised, SPEC-driven AI development.

Take a code-review stance. Prioritize bugs, security risks, missing tests, docs
drift, false completion claims, overreach beyond the active SPEC, speculative
complexity, and unrelated drive-by changes.

## Review Inputs

Context Stability applies before review inputs. Review sessions often touch
large SPECs, TODOs, findings, handoffs, archives, and generated reports, so do
not load them in full by default.

Use bounded reads for large files: inspect file size, read headings or matching
sections, limit search output, and use explicit excludes. Default soft triggers:
bounded reads above 50 KB or 500 lines, context-stability check above 200 KB or
2,000 lines, and no full startup read above 1 MB unless the owner explicitly
asks for historical reconstruction.

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

Also identify the approved work packet, autonomy level, and evidence-ready units
if the handoff provides them.
If the implementation made decisions the SPEC did not state, inspect
`docs/implementation-notes.md` or the handoff's Implementation notes section.

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
- missing implementation notes for spec-unstated assumptions, changes,
  compromises, rejected alternatives, owner-relevant tradeoffs, follow-up, or
  verification impact,
- hidden assumptions that should become explicit rules,
- assumptions that required owner input but were silently chosen,
- speculative abstractions or generalized code that the active SPEC did not need,
- unrelated refactors, formatting, cleanup, comment rewrites, or adjacent edits,
- partial, degraded, skipped, or unverified behavior that was not labeled,
- version-lane or migration sync risk, if applicable,
- high-risk domain checklist gaps, if applicable,
- advanced extension fit-gate gaps, if applicable,
- evaluation leakage risk, if prompts, harnesses, retrieval, memory, review
  rules, or agent scaffolds were tuned,
- whether search evidence is separated from owner acceptance evidence,
- whether concrete budget was stated for expensive or repeated eval loops,
- release or production-readiness blockers, if applicable,
- missing ADRs for durable decisions, if applicable,
- assumptions,
- whether the change is safe to accept.

Do not rewrite the implementation unless asked. Do not accept "AI said complete"
or "evidence-ready" as owner acceptance.
For release candidates, call out whether Critical 0 has been met.
