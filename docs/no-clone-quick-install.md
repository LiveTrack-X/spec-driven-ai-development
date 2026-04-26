# No-Clone Quick Install

Use this when you want to apply SPEC-Driven AI Development without cloning this
repository first.

The easiest option is Option 1. It does not require terminal commands, Git,
Python, or Codex.

## Before You Start

Pick the path that matches your comfort level:

| Path | Best for | Requires |
|---|---|---|
| Give this to your AI agent | Complete beginners | An AI coding tool that can edit files |
| One-paste PowerShell installer | Windows users comfortable with terminal | PowerShell and internet access |
| One-paste Bash installer | macOS/Linux/WSL users comfortable with terminal | Bash, curl, and internet access |
| Clone this repository | Developers who want the full package locally | Git |
| Codex skill | Codex users only | Codex installed and configured |

Run terminal commands from the root of the project you want to control.

## Step 0: Choose Scale

Before installing an adapter or creating project files, choose the smallest
workflow scale that fits.

Ask:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

| Yes answers | Scale | What to create |
|---|---|---|
| 0 | One-shot prompt | No project files |
| 1-2 | Mini SDAD | One instruction file from `templates/mini-sdad/MINI-SDAD.md` |
| 3 | Standard SDAD | Adapter plus core control files |
| 4-5 | Full SDAD | Adapter, core files, review, ADRs, risk gates |

When unsure, choose the smaller scale. Escalate later only when repeated pain,
context loss, risk, or multiple sessions appear.

## Maintenance Cost

Do not create Standard or Full SDAD files unless you will keep them current.

At the end of every Standard or Full SDAD loop, check and update:

- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- operating rules or ADRs when decisions or repeated pain changed,
- `save-state.md` when a session pauses or ends, handoff is expected, owner
  direction changes, blocked/partial/unverified state remains, or context would
  be expensive to reconstruct.

If no file needs a content change, state which files were checked and why no
update was needed.

Mini SDAD still has a completion gate: changed files, check evidence,
limitations or unverified behavior, and owner acceptance must be shown before a
slice is called done.

If this cost is too high, choose One-shot Prompt or Mini SDAD instead.

## What Is A Codex Skill?

A Codex skill is an optional local instruction package for OpenAI Codex. It tells
Codex how to behave when starting or managing a SPEC-driven project.

You do not need the Codex skill if you use Claude Code, Cursor, GitHub Copilot,
another AI coding agent, or Option 1 below.

## How To Know It Worked

After Mini, Standard, or Full setup, your project should have one of these
instruction files:

- `AGENTS.md` for Codex,
- `CLAUDE.md` for Claude Code,
- `.cursor/rules/spec-driven-ai-development.mdc` for Cursor,
- `.github/copilot-instructions.md` for GitHub Copilot,
- `AI-SESSION-INSTRUCTIONS.md` for a generic AI tool.

After Standard or Full bootstrap, your project should also have control files
such as `SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, and
`review-findings.md`.

## Exact Adapter Sources

For Mini SDAD, use this exact template:

```text
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/templates/mini-sdad/MINI-SDAD.md
```

Before fetching Mini SDAD, state that you are installing Mini SDAD and explain
why this scale was chosen.

For Standard or Full SDAD, do not ask an AI agent to guess adapter paths. Use
these exact source URLs:

| Tool | Source URL | Save as |
|---|---|---|
| Codex | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/codex/AGENTS.md` | `AGENTS.md` |
| Claude Code | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/claude-code/CLAUDE.md` | `CLAUDE.md` |
| Cursor | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc` | `.cursor/rules/spec-driven-ai-development.mdc` |
| GitHub Copilot | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/github-copilot/.github/copilot-instructions.md` | `.github/copilot-instructions.md` |
| Generic AI tool | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/generic/AI-SESSION-INSTRUCTIONS.md` | `AI-SESSION-INSTRUCTIONS.md` |

## Option 1: Give This To Your AI Agent

Paste this into Codex, Claude Code, Cursor, Copilot Chat, or another AI coding
agent:

```text
Use SPEC-Driven AI Development as the project control method.

Source repository:
https://github.com/LiveTrack-X/spec-driven-ai-development

Do not require me to clone the repository unless absolutely necessary.

Step 0 - Choose scale before creating files.

Ask me these five questions:
1. Will this take more than one AI session?
2. Will I come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Choose:
- 0 yes -> One-shot prompt. Do not create project files.
- 1-2 yes -> Mini SDAD. Create only one instruction file.
- 3 yes -> Standard SDAD. Create core control files.
- 4-5 yes -> Full SDAD. Use full workflow, review, ADRs, and gates.

When unsure, choose the smaller scale and explain why.

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

For Standard or Full SDAD, install the matching instruction file for this AI
tool. Do not infer adapter paths. Use exactly one of these source URLs:

Before fetching, state which adapter you are installing and why.
If you cannot determine the current tool, ask me to specify one of:
Codex / Claude Code / Cursor / Copilot Chat / Generic.

- Codex -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/codex/AGENTS.md -> ./AGENTS.md
- Claude Code -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/claude-code/CLAUDE.md -> ./CLAUDE.md
- Cursor -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc -> ./.cursor/rules/spec-driven-ai-development.mdc
- Copilot Chat -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/github-copilot/.github/copilot-instructions.md -> ./.github/copilot-instructions.md
- Generic AI agent -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main/adapters/generic/AI-SESSION-INSTRUCTIONS.md -> ./AI-SESSION-INSTRUCTIONS.md

Before saving the adapter:
1. show me the source URL,
2. show me the first 10 lines of the fetched file,
3. confirm the target path.

If you cannot fetch the file, stop and say so. Do not create a fake adapter from
memory.

For Standard or Full SDAD, after installing the instruction file, bootstrap this
project:

1. create or update docs/INDEX.md,
2. create or update docs/Repository-Operating-Rules.md,
3. create or update SPEC/SPEC-COMPLETE.md,
4. create or update docs/TODO-Open-Items.md,
5. create or update review-findings.md,
6. ask me for product pain, smallest useful version, non-goals, risks,
   owner-controlled decisions, and evidence required for completion.

Do not overwrite existing project files without showing me what will change.
Completion requires evidence, not AI confidence.

At the end of every loop, check whether SPEC-COMPLETE, TODO, review-findings,
rules, or ADRs must be updated. If nothing changes, say which files were checked
and why no update was needed.

Update save-state.md when a session pauses or ends, handoff is expected, owner
direction changes, blocked/partial/unverified state remains, or context would be
expensive to reconstruct.

For Mini SDAD, do not call a slice done until changed files, check evidence,
limitations or unverified behavior, and owner acceptance are shown.
```

## Option 2: One-Paste PowerShell Installer

Paste this into PowerShell from your target project root.

Change `$adapter = "codex"` if you use another tool.

```powershell
$ErrorActionPreference = "Stop"
$adapter = "codex" # codex, claude-code, cursor, github-copilot, generic
$base = "https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main"
$files = @{
  "codex" = @("adapters/codex/AGENTS.md", "AGENTS.md")
  "claude-code" = @("adapters/claude-code/CLAUDE.md", "CLAUDE.md")
  "cursor" = @("adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc", ".cursor/rules/spec-driven-ai-development.mdc")
  "github-copilot" = @("adapters/github-copilot/.github/copilot-instructions.md", ".github/copilot-instructions.md")
  "generic" = @("adapters/generic/AI-SESSION-INSTRUCTIONS.md", "AI-SESSION-INSTRUCTIONS.md")
}
if (-not $files.ContainsKey($adapter)) { throw "Unknown adapter: $adapter" }
$source, $target = $files[$adapter]
$targetDir = Split-Path -Parent $target
if ($targetDir) { New-Item -ItemType Directory -Force -Path $targetDir | Out-Null }
if (Test-Path -LiteralPath $target) { throw "Target already exists: $target" }
Invoke-WebRequest -Uri "$base/$source" -OutFile $target
Write-Host "Installed $adapter instructions to $target"
Write-Host "Next prompt: Read $target and bootstrap this project into SPEC-Driven AI Development."
```

## Option 3: One-Paste Bash Installer

Paste this into Bash, zsh, WSL, macOS Terminal, or Linux shell from your target
project root.

Change `adapter="codex"` if you use another tool.

```bash
set -euo pipefail
adapter="codex" # codex, claude-code, cursor, github-copilot, generic
base="https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/main"
case "$adapter" in
  codex)
    source="adapters/codex/AGENTS.md"
    target="AGENTS.md"
    ;;
  claude-code)
    source="adapters/claude-code/CLAUDE.md"
    target="CLAUDE.md"
    ;;
  cursor)
    source="adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc"
    target=".cursor/rules/spec-driven-ai-development.mdc"
    ;;
  github-copilot)
    source="adapters/github-copilot/.github/copilot-instructions.md"
    target=".github/copilot-instructions.md"
    ;;
  generic)
    source="adapters/generic/AI-SESSION-INSTRUCTIONS.md"
    target="AI-SESSION-INSTRUCTIONS.md"
    ;;
  *)
    echo "Unknown adapter: $adapter" >&2
    exit 1
    ;;
esac
if [ -e "$target" ]; then
  echo "Target already exists: $target" >&2
  exit 1
fi
mkdir -p "$(dirname "$target")"
curl -fsSL "$base/$source" -o "$target"
echo "Installed $adapter instructions to $target"
echo "Next prompt: Read $target and bootstrap this project into SPEC-Driven AI Development."
```

## After The Installer

Open your AI coding tool in the target project and say:

```text
Read the installed SPEC-Driven AI Development instruction file.
Bootstrap this project with the first active SPEC slice.
Ask me for product pain, smallest useful version, non-goals, risks,
owner-controlled decisions, and evidence required for completion.
```

The first successful bootstrap should create or update:

- `docs/INDEX.md`,
- `docs/Repository-Operating-Rules.md`,
- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`.

If those files already exist, the AI should show the proposed changes before
editing them.
