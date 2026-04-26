# Mini SDAD

Mini SDAD is the one-file version of SPEC-Driven AI Development.

Use it when a project is too small for full docs, SPEC folders, ADRs, and review
ledgers, but still needs basic protection against scope drift, vague completion,
or context loss.

## When To Use Mini SDAD

Use Mini SDAD when one or two of these are true:

- the work may take more than one AI session,
- you may return to the project later,
- "done" needs evidence beyond "AI said so",
- you want the AI to avoid unrelated changes,
- you want a tiny handoff record without creating full project governance.

Do not use Mini SDAD for one-shot throwaway work that ends in one prompt and does
not need future context.

Use Standard or Full SDAD when multiple AI tools, durable review findings,
release gates, migrations, user data, auth, money, or production risk appears.

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
from memory.

After saving it, ask me for:
- the active task,
- what is out of scope,
- what evidence proves done,
- whether any risk requires Standard or Full SDAD.
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
