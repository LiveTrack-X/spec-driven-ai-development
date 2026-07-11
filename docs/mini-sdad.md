# Mini SDAD

Mini SDAD is the one-file SDAD Protocol scale for small, bounded work. It adds a
compact evidence and scope contract without installing the Standard/Full state,
INDEX, SPEC, TODO, finding, and handoff surfaces.

## When To Use Mini SDAD

Use Mini when one or two of these are true:

- the work may continue beyond the current interaction;
- you may return later and need a compact recovery note;
- “done” needs check evidence;
- unrelated-change protection matters;
- the request is one small bugfix, workflow, UI, docs, or prompt unit.

Do not use Mini for a throwaway One-shot that needs no continuity. Use Standard
or Full when the work needs durable packet state, multiple active ledgers,
multi-session/multi-agent coordination, or protected-action owner gates such as
release, production, migration, destructive action, real user data, auth,
money, security, or rollback.

## Mini Execution Boundary

Mini defaults to one `unit`. Scale controls the persistent control surface;
execution scope controls how far the AI may work now; owner gates control
protected actions. A unit can contain the connected edits and checks needed for
one reviewable outcome. Do not stop for approval after every micro-task.

The owner can say “check this,” “fix it,” “make the README clearer,” or “create
a tiny handoff” without knowing a skill name. The AI infers intent and the unit
from repository evidence, reports the interpretation, and asks at most the next
blocking question when its answer would change scale or an owner gate.

Examples:

- one bugfix plus its regression check;
- one small UI/workflow change plus validation;
- one connected docs/prompt change;
- one necessary cleanup inside the requested outcome.

Stop when scope expands beyond the unit, a protected action needs owner
authorization, a destructive or irreversible action is required, validation is
blocked, evidence conflicts with the plan, or the owner must accept risk.

## Mini Unit Completion Criteria

A Mini unit is evidence-ready only when:

- the interpreted outcome and excluded scope are stated;
- changed files and user-visible behavior are listed;
- tests, commands, or manual checks are shown, or the gap is explicit;
- the evidence claim is bounded to what those checks establish;
- limitations, skipped checks, and unverified behavior are named;
- unrelated scope was not added;
- required owner authorization or acceptance is named separately.

AI confidence, provider task status, or a clean syntax check is not completion.
Evidence-ready is not owner-accepted.

## What Mini SDAD Creates

Mini creates one instruction file for the active tool. Until release metadata
rotates, use the stable v3.1.0 source:

```text
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/templates/mini-sdad/MINI-SDAD.md
```

Expected SHA-256:
`f5370ba6539ab55b88fc10a7589ca7f42fa6714072830620aad7dab60d21f669`.

Use `main` only when changing, unpinned instructions are intentional.

| Tool | Save as |
| --- | --- |
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | `GEMINI.md` |
| Cursor | `.cursor/rules/mini-sdad.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Generic AI tool | `AI-SESSION-INSTRUCTIONS.md` |

Cursor requires MDC frontmatter. From a clone, copy
`templates/mini-sdad/cursor-mini-sdad.mdc`. For no-clone installation, prepend:

```yaml
---
description: Mini SDAD rules for small, evidence-based Cursor work units.
globs:
alwaysApply: true
---
```

## Mini SDAD Prompt

```text
Use Mini SDAD for this project. The default execution boundary is one unit.

Fetch this exact template:
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/templates/mini-sdad/MINI-SDAD.md
Expected SHA-256: f5370ba6539ab55b88fc10a7589ca7f42fa6714072830620aad7dab60d21f669

Before fetching, state that you are installing Mini SDAD and why Mini fits.
Save it at the correct tool-native path. For Cursor, prepend the documented MDC
frontmatter.

Before saving:
1. show the source URL,
2. show the first 10 fetched lines,
3. compute SHA-256 and require an exact match,
4. confirm the target path.

If fetching fails, stop rather than inventing the template. Offer deterministic
fallback options: retry with network access, ask me to paste the raw source,
use the terminal installer, or clone/download the repository.

Infer the active unit, excluded scope, required validation, and applicable
owner gates from my request and repository evidence. Ask only the next question
whose answer would change Mini suitability or an owner gate. Report that
interpretation before editing.

Do not call the unit evidence-ready until changed files, check evidence, claim
limits, and unverified behavior are shown. Keep owner acceptance separate. If a
small spec-unstated implementation decision matters, include it in the final
Implementation notes; do not create another persistent control file unless the
project escalates.
```

## Escalation Rule

Stay Mini while one instruction file and one-unit reports remain sufficient.
Escalate only when evidence shows a need for persistent packet state or more
control: repeated context loss, durable TODOs/findings, multiple agents/sessions,
conflicting active docs, or an owner-gated release/production/migration/data/
security/destructive action.

See [Getting Started](getting-started.md) or
[No-Clone Quick Install](no-clone-quick-install.md) when escalating.

## Migrating From SDAD 3.1

Older Mini guidance may describe numeric autonomy levels or a risk-question
score. Treat those as legacy selection language, not state-v2 fields. The 3.2
interpretation is Mini -> `unit`, with protected actions governed separately by
owner gates.
