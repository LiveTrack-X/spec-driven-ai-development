# Tool Adapters

Status: Active reference
Scope: How to use SPEC-Driven AI Development across AI coding tools

This repository is tool-neutral. Codex skills are one delivery format, not the
method itself. Use the adapter that matches the AI coding environment.

Each adapter carries the same source-of-truth, evidence, context-stability,
natural-language intent routing, work-packet autonomy, clarification-checkpoint,
implementation discipline, implementation-notes, sparse ADR, handoff, and
`save-state.md` update trigger rules.

## Supported Adapters

| Tool | Adapter file | Use when |
| --- | --- | --- |
| Codex | `AGENTS.md` + `ai-spec-project-start` skill | You want repository rules plus an installable Codex skill. |
| Claude Code | `CLAUDE.md` | You want project memory loaded by Claude Code at session start. |
| Cursor | `.cursor/rules/spec-driven-ai-development.mdc` | You want persistent project rules for Cursor Agent and inline edit. |
| GitHub Copilot | `.github/copilot-instructions.md` | You want repository-level custom instructions for Copilot Chat, review, or coding agent flows. |
| Generic AI coding tool | `AI-SESSION-INSTRUCTIONS.md` | The tool has no special instruction-file convention. |

## Install An Adapter

PowerShell:

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter cursor -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter github-copilot -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter generic -TargetPath C:\path\to\project
```

macOS/Linux:

```bash
./scripts/install-agent-adapter.sh claude-code /path/to/project
./scripts/install-agent-adapter.sh cursor /path/to/project
./scripts/install-agent-adapter.sh github-copilot /path/to/project
./scripts/install-agent-adapter.sh generic /path/to/project
```

If your checkout lost executable bits, prefix the command with `bash`, for
example `bash ./scripts/install-agent-adapter.sh claude-code /path/to/project`.

The installer refuses to overwrite existing files unless `-Force` or `--force`
is used.

## Adapter Design

Each adapter keeps only the high-signal operating rules:

- mandatory start-loop route,
- context-stability and bounded-read guard before first-read files,
- source-of-truth order,
- current-over-historical SPEC precedence,
- natural-language intent routing so users can say "review this", "implement
  this", "release this", or "create a handoff" without knowing skill names,
- evidence-based completion,
- implicit rules made explicit,
- TODO/review ledger separation,
- documentation consistency checks,
- work-packet autonomy instead of micro-approval,
- clarification checkpoints for fuzzy plans after repository evidence is
  checked,
- implementation discipline for assumptions, simplicity, surgical diffs, and
  verification,
- implementation notes for spec-unstated assumptions, changes, compromises,
  rejected alternatives, owner-relevant tradeoffs, follow-up, and verification
  impact,
- release/risk gate reminders,
- owner decision control.

Longer explanations stay in this repository's docs and templates.

Adapters are guidance, not enforcement. If a behavior must always happen or
must never happen, route it to an enforced surface such as CI, required tests,
validators, hooks, permissions, deny rules, branch protection, release gates, or
artifact verification. Keep the adapter rule as the readable explanation, but
do not rely on Markdown alone for secrets, destructive actions, migrations,
production deploys, release assets, or money/data/security boundaries.

Use
[field-notes/repository-control-surface-method.md](field-notes/repository-control-surface-method.md)
when deciding whether a repeated rule belongs in always-loaded guidance, routed
guidance, an on-demand procedure, isolated exploration, an enforced guarantee,
or reviewed project memory.

## Tool Notes

- Claude Code uses project `CLAUDE.md` memory files. See Anthropic's memory docs:
  <https://docs.anthropic.com/en/docs/claude-code/memory>
- Cursor project rules live under `.cursor/rules` as `.mdc` files. See Cursor's
  rules docs: <https://docs.cursor.com/context/rules>
- GitHub Copilot repository instructions use `.github/copilot-instructions.md`.
  See GitHub's docs: <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>

Tool behavior can change. If a tool stops loading the expected file, keep the
method content and update only the adapter path.
