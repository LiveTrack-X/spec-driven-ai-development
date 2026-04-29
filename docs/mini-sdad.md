# Mini SDAD

Mini SDAD is the one-file version of SPEC-Driven AI Development.

Use it when a project is too small for full docs, SPEC folders, ADRs, and review
ledgers, but still needs basic protection against scope drift, vague completion,
or context loss.

## When To Use Mini SDAD

Use Mini SDAD when one or two of these are true, and there is no Q4/Q5
multi-tool or high-risk override:

- the work may take more than one AI session,
- you may return to the project later,
- "done" needs evidence beyond "AI said so",
- you want the AI to avoid unrelated changes,
- you want a tiny handoff record without creating full project governance.

Do not use Mini SDAD for one-shot throwaway work that ends in one prompt and does
not need future context.

Use Standard or Full SDAD when multiple AI tools, durable review findings,
release gates, migrations, user data, auth, money, or production risk appears.
Q5-style risk beats the raw yes-count: one production, migration, user data,
auth, money, destructive, release, or rollback risk is enough to use Standard at
minimum, and often Full.

Mini SDAD exists because full control files have a maintenance cost. If you do
not want to update SPEC, TODO, and review ledgers at the end of every loop, stay
Mini.

## Mini Review-Worthy Unit

Mini SDAD should not stop after every micro-task. Define one small
review-worthy unit, then let the AI continue inside that boundary until it can
show evidence.

Default autonomy is Level 1 Unit Autonomy, with the active unit treated as one
small approved packet. The AI completes that boundary, reports evidence-ready
status, and asks only at the checkpoint or when a stop condition appears. Do not
turn each small SPEC item into a separate approval gate. Use Level 2 Work Packet
Autonomy only when the owner names a packet with multiple related units.

A Mini review-worthy unit may include:

- one small UI/workflow change,
- one bugfix plus its check,
- one connected docs or prompt update,
- one short cleanup needed for the requested task.

Stop and ask the owner only when scope expands, Q5-style risk appears, a
destructive or irreversible action is needed, an owner-controlled decision is
required, verification is blocked, or evidence conflicts with the plan.

## Mini Unit Completion Criteria

A Mini SDAD unit is evidence-ready only when:

- the active task is restated,
- changed files are listed,
- tests, commands, or manual checks are shown, or the reason they could not run
  is stated,
- user-visible behavior or output is described,
- limitations and unverified behavior are named,
- unrelated scope was not added,
- owner decisions or acceptance needed are named.

AI confidence is not completion.

Not evidence-ready when:

- the AI only says it is done,
- checks were not run and the gap is hidden,
- known uncertainty is not named,
- unrelated changes were made without owner approval.

Final done still requires owner acceptance unless the owner has explicitly
delegated the acceptance policy. Requested changes or deferred decisions mean
the unit is not done.

## What Mini SDAD Creates

Mini SDAD creates one instruction file for the AI tool.

Use the same content from:

```text
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/templates/mini-sdad/MINI-SDAD.md
```

Save it as the right instruction file for your tool:

| Tool | Save as |
|---|---|
| Codex | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/mini-sdad.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Generic AI tool | `AI-SESSION-INSTRUCTIONS.md` |

## Mini SDAD Prompt

Paste this into your AI coding tool:

```text
Use Mini SDAD for this project.

Fetch this exact template:
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/templates/mini-sdad/MINI-SDAD.md

Before fetching, state that you are installing Mini SDAD and explain why this
scale was chosen.

Save it as the correct instruction file for this tool:
- Codex -> ./AGENTS.md
- Claude Code -> ./CLAUDE.md
- Cursor -> ./.cursor/rules/mini-sdad.mdc
- Copilot Chat -> ./.github/copilot-instructions.md
- Generic AI agent -> ./AI-SESSION-INSTRUCTIONS.md

Before saving:
1. show me the source URL,
2. show me the first 10 lines of the fetched file,
3. confirm the target path.

If you cannot fetch the template, stop and say so. Do not invent the template
from memory. Offer deterministic fallback options: retry with network access,
ask me to paste the raw template content from the source URL, use the terminal
installer, or clone/download the repository manually.

After saving it, ask me for:
- the active task,
- what is out of scope,
- what evidence proves evidence-ready,
- whether any risk requires Standard or Full SDAD.

For each unit, do not call it evidence-ready until changed files, check evidence,
and limitations or unverified behavior are shown. Do not call final completion
done until owner acceptance is shown or the owner has explicitly delegated the
acceptance policy.
```

## Escalation Rule

Stay Mini by default.

Escalate only when evidence shows the project needs more structure:

- repeated context loss,
- TODOs or review findings that need tracking,
- multiple AI tools or sessions,
- conflicting docs or old plans,
- release, migration, user data, auth, money, or production risk.

When escalating, move to [getting-started.md](getting-started.md) or
[no-clone-quick-install.md](no-clone-quick-install.md).
