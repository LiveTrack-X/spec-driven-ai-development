# SPEC-Driven AI Development

A control layer for AI coding: turn specs, agents, and outputs into a governed
development loop.

Status: `1.0.7` stable public release.

Works with Codex, Claude Code, Cursor, Copilot Chat, and generic AI coding
agents.

<p>
  <a href="https://buymeacoffee.com/livetrack">
    <img src="https://img.shields.io/badge/Buy%20Me%20a%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me a Coffee">
  </a>
</p>

![SPEC-Driven AI Development infographic](assets/spec-driven-ai-development-infographic.png)

## For Beginners: Use In 60 Seconds

No terminal. No Git. No Python required.

1. Open your project in an AI coding tool that can edit files, such as Codex,
   Claude Code, Cursor, or Copilot Chat.
2. Paste the text below.
3. Let the AI choose the scale and create only the files that scale needs.

```text
Use SPEC-Driven AI Development as the project control method.

Source:
https://github.com/LiveTrack-X/spec-driven-ai-development

First determine whether you can edit files in this project.
If this is a chat-only environment such as Claude.ai, ChatGPT web, or another
browser chat with no project filesystem, do not install adapters or claim files
were saved. Use this repository for planning only, then tell me to open the
project in Codex, Claude Code, Cursor, Copilot Chat, or another file-editing AI
coding tool.

Step 0 - Choose scale before creating files.

Ask me these five questions:
1. Will this take more than one AI session?
2. Will I come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Choose:
- 0 yes -> One-shot prompt. Do not create project files.
- 1-2 yes from questions 1-3 only, with Q4=no and Q5=no -> Mini SDAD.
  Create only one instruction file.
- Q4=yes or 3 yes total -> Standard SDAD. Create core control files.
- Q5=yes -> Standard SDAD minimum, even if it is the only yes.
- Q5=yes with production-facing, destructive, migration, real user data, auth,
  money, release, or rollback risk -> Full SDAD.
- 4-5 yes -> Full SDAD. Use full workflow, review, ADRs, and gates.

Override rules beat raw yes-counts. When unsure, choose the smaller scale only
if no Q5 risk exists, and explain why.

For Mini SDAD, fetch this exact template:
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/templates/mini-sdad/MINI-SDAD.md

Before fetching, state that you are installing Mini SDAD and explain why this
scale was chosen.

Save it as the correct instruction file for this tool:
- Codex -> ./AGENTS.md
- Claude Code -> ./CLAUDE.md
- Cursor -> ./.cursor/rules/mini-sdad.mdc
- Copilot Chat -> ./.github/copilot-instructions.md
- Generic AI agent -> ./AI-SESSION-INSTRUCTIONS.md

For Standard or Full SDAD, install the adapter for this project, then bootstrap
the first active SPEC slice and project control files.

Before fetching, state which adapter you are installing and why.
If you cannot determine the current tool, ask me to specify one of:
Codex / Claude Code / Cursor / Copilot Chat / Generic.
Claude Code means the local/CLI coding tool with project filesystem access. It
does not mean Claude.ai chat.

Do not infer adapter paths. Use exactly one of these source URLs:

- Codex -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/codex/AGENTS.md -> ./AGENTS.md
- Claude Code -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/claude-code/CLAUDE.md -> ./CLAUDE.md
- Cursor -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc -> ./.cursor/rules/spec-driven-ai-development.mdc
- Copilot Chat -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/github-copilot/.github/copilot-instructions.md -> ./.github/copilot-instructions.md
- Generic AI agent -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/generic/AI-SESSION-INSTRUCTIONS.md -> ./AI-SESSION-INSTRUCTIONS.md

Show me the source URL and first 10 lines of the fetched file before saving it.
If you cannot fetch the file, stop and say so. Do not create a fake adapter from
memory. Offer deterministic fallback options: retry with network access, ask me
to paste the raw file content from the source URL, use the terminal installer, or
clone/download the repository manually.

Ask me for product pain, smallest useful version, non-goals, risks,
owner-controlled decisions, and evidence required for completion.

For Mini SDAD at loop end, do not check SPEC-COMPLETE, TODO, review-findings, or
ADRs unless the project has escalated. Report the active task, changed files,
check evidence, limitations or unverified behavior, owner acceptance, and whether
to escalate.

For Standard or Full SDAD at loop end, check whether SPEC-COMPLETE, TODO,
review-findings, rules, or ADRs must be updated. If nothing changes, say which
files were checked and why no update was needed.

Update save-state.md when a session pauses or ends, handoff is expected, owner
direction changes, blocked/partial/unverified state remains, or context would be
expensive to reconstruct.

For Mini SDAD, do not call a slice done until changed files, check evidence,
limitations or unverified behavior, and owner acceptance are shown.

Do not overwrite existing files without showing me the proposed changes.
Completion requires evidence, not AI confidence.
```

Developers and terminal users can use the one-paste PowerShell/Bash installers
in [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md).

## Languages

English is the canonical documentation language for this repository.

- [English](README.md)
- [한국어](README.ko.md)
- [中文](README.zh.md)
- [日本語](README.ja.md)

Localized READMEs are orientation guides. If a localized guide conflicts with
the English docs, templates, or validation scripts, prefer the English canonical
files.

## Choose Scale First

Before installing anything, answer these:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Choose the smallest scale that fits:

Override rules beat raw yes-counts:

| Trigger | Use | Creates |
|---|---|---|
| 0 yes | One-shot prompt | No project files |
| 1-2 yes from Q1-Q3 only, with Q4=no and Q5=no | Mini SDAD | One instruction file |
| Q4=yes or 3 yes total | Standard SDAD | Core control files |
| Q5=yes | Standard SDAD minimum | Core control files and explicit risk tracking |
| Q5=yes with production-facing, destructive, migration, real user data, auth, money, release, or rollback risk | Full SDAD | Full workflow, review, ADRs, gates |
| 4-5 yes | Full SDAD | Full workflow, review, ADRs, gates |

When unsure, choose the smaller scale only if no Q5 risk exists. Escalate when
repeated pain, context loss, risk, or multiple sessions appear.

Small project? Start with [Mini SDAD](docs/mini-sdad.md), not the full workflow.

## Maintenance Cost

SDAD files are not write-once setup files.

If you choose Standard or Full SDAD, every loop must end by checking and updating
the control files:

- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- operating rules or ADRs when decisions or repeated pain changed,
- `save-state.md` when a session pauses or ends, handoff is expected, owner
  direction changes, blocked/partial/unverified state remains, or context would
  be expensive to reconstruct.

If no file needs a content change, the handoff must say which files were checked
and why no update was needed. Do not claim completion while control files are stale.

Mini SDAD also has a completion gate: changed files, checks or manual proof,
limitations, and owner acceptance must be shown before a slice is called done.

If that cost is too high, choose One-shot Prompt or [Mini SDAD](docs/mini-sdad.md).
See [docs/maintenance-cost.md](docs/maintenance-cost.md).

## Start Here

New to the workflow? Start with [docs/getting-started.md](docs/getting-started.md).

It shows practical paths:

- scale selection,
- no-clone quick install,
- Mini SDAD for small projects,
- maintenance cost and loop-end updates,
- prompt-only start,
- install a tool adapter into an existing project,
- install the Codex skill.

The goal is to choose the right scale first, then create only the control files
that scale needs.

## The Problem

AI coding feels solved.

But projects still break:

- specs drift from code,
- AI says "done" but bugs remain,
- context resets every session,
- docs become unreliable,
- old plans override current work,
- no one knows the real source of truth.

The hard part is no longer getting AI to produce code. The hard part is keeping
AI-assisted development governed, current, reviewed, and evidence-based.

## What This Is

This is not another spec template.

SPEC-Driven AI Development is a control system for AI-driven development. It
enforces:

- owner-supervised development,
- spec-driven execution,
- multi-agent verification,
- evidence-based completion,
- current-over-historical source of truth,
- repeated-pain-to-rule learning.

It is designed for projects where AI agents help plan, specify, implement,
review, test, document, and hand off work while a human owner keeps direction,
risk tolerance, and final acceptance.

## Core Idea

AI writes code.

The owner controls the system.

Completion is not decided by AI. Completion is decided by evidence:

- code changed,
- tests or checks ran,
- docs were checked or updated,
- review findings are known,
- risks are named,
- the owner accepts the result.

## The Loop

```text
Pain -> SPEC -> Build -> Review -> Evidence -> Owner decision -> Rule
```

This loop repeats every iteration. The goal is not only to fix problems, but to
turn repeated problems into durable rules, templates, tests, or review gates.

```mermaid
flowchart TD
    A["Pain or product need"] --> B["Active SPEC"]
    B --> C["Bounded build"]
    C --> D["Review"]
    D --> E["Evidence"]
    E --> F["Owner decision"]
    F --> G["Rule, TODO, finding, ADR, or archive update"]
    G --> B
```

## Why This Is Different

Most workflows:

```text
AI + developer
```

This workflow:

```text
AI + owner
```

The owner may be a developer, but does not have to be one. The system is built
so a non-coding owner can still supervise scope, evidence, risk, and acceptance.

Most workflows:

```text
"AI says done"
```

This workflow:

```text
Done = verified + documented + accepted
```

Most workflows fix problems.

This workflow turns problems into rules.

## Quick Usage

Fastest possible start:

```text
Use the SPEC-driven AI development workflow from this repository.
Extract my control model and create the first active SPEC slice.
```

Then follow the loop:

```text
Pain -> SPEC -> Build -> Review -> Evidence -> Owner decision -> Rule
```

For step-by-step setup, use [docs/getting-started.md](docs/getting-started.md).
For no-clone setup, use [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md).
For a fuller kickoff prompt, use [prompts/kickoff-prompt.md](prompts/kickoff-prompt.md).

## Project Structure

The first instruction file is tool-specific. Do not create all of them; install
the one that matches your AI coding tool.

```text
AI instruction file, choose one:
  AGENTS.md                                      # Codex
  CLAUDE.md                                      # Claude Code
  .cursor/rules/spec-driven-ai-development.mdc   # Cursor
  .github/copilot-instructions.md                # GitHub Copilot
  AI-SESSION-INSTRUCTIONS.md                     # generic AI agent

docs/INDEX.md                                    # documentation navigation
docs/Repository-Operating-Rules.md               # durable operating rules
SPEC/SPEC-COMPLETE.md                            # current product and implementation truth
SPEC/adr/                                        # durable decision records
docs/TODO-Open-Items.md                          # active implementation work
review-findings.md                               # active bugs and review findings
save-state.md                                    # optional session recovery handoff
```

Templates live in [templates/project-control-files](templates/project-control-files).

## Tool Adapters

Use adapters when you want the same control layer in different AI coding tools:

- Codex: `AGENTS.md` + `ai-spec-project-start` skill
- Claude Code: `CLAUDE.md`
- Cursor: `.cursor/rules/spec-driven-ai-development.mdc`
- GitHub Copilot: `.github/copilot-instructions.md`
- Generic AI tool: `AI-SESSION-INSTRUCTIONS.md`

Install examples:

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter cursor -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter github-copilot -TargetPath C:\path\to\project
```

See [docs/tool-adapters.md](docs/tool-adapters.md).

## Codex Skill

Install the Codex skill:

```powershell
.\scripts\install-codex-skill.ps1
```

macOS/Linux:

```bash
./scripts/install-codex-skill.sh
```

Then start a new Codex session and say:

```text
$ai-spec-project-start use this workflow to bootstrap my project.
```

## Who This Is For

- solo builders using AI coding tools,
- non-coders supervising AI development,
- technical owners coordinating multiple AI sessions,
- projects suffering from context loss or spec drift,
- projects where "done" must mean verified and accepted,
- teams that want repeated failures to become durable rules.

Use [docs/fit-assessment.md](docs/fit-assessment.md) if you are not sure the
workflow fits your project.

## What This Is Not

- Not a coding framework.
- Not a prompt collection.
- Not an autonomous agent system.
- Not a replacement for tests or reviews.
- Not a guarantee that AI output is correct.
- Not a reason to skip owner decisions.

## Core Rules

The Core 5:

- Current beats historical.
- Evidence beats confidence.
- Active beats interesting.
- Owner decision beats AI momentum.
- Repeated pain becomes a rule.

The Extended 15 cover docs drift, partial or degraded work, version lanes,
release readiness, environment limits, cross-review, and risk gates.

See [docs/implicit-rules.md](docs/implicit-rules.md).

## Key Docs

- [docs/pattern-catalog.md](docs/pattern-catalog.md): full method and pattern matrix
- [docs/getting-started.md](docs/getting-started.md): first-use setup guide
- [docs/no-clone-quick-install.md](docs/no-clone-quick-install.md): copy-paste setup without cloning
- [docs/anti-patterns.md](docs/anti-patterns.md): failure modes to avoid
- [docs/fit-assessment.md](docs/fit-assessment.md): project fit checklist
- [docs/maintenance-cost.md](docs/maintenance-cost.md): loop-end control file update cost
- [docs/diagrams.md](docs/diagrams.md): workflow diagrams
- [docs/tool-adapters.md](docs/tool-adapters.md): tool-specific instruction files
- [docs/field-notes/documentation-governance-method.md](docs/field-notes/documentation-governance-method.md): documentation-governance field pattern
- [docs/field-notes/release-governance-method.md](docs/field-notes/release-governance-method.md): release-governance field pattern

## Validate

```bash
python scripts/validate_repo.py
```

## License

MIT. See [LICENSE](LICENSE).
