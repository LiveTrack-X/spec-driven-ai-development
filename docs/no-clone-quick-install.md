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

Chat-only tools such as Claude.ai, ChatGPT web, or browser chat can discuss the
workflow, but they cannot install adapters unless they have project filesystem
access. Claude Code means the local/CLI coding tool, not Claude.ai chat.

## Step 0: Choose Scale

Before installing an adapter or creating project files, choose the smallest
workflow scale that fits.

Ask:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Override rules beat raw yes-counts:

| Trigger | Scale | What to create |
|---|---|---|
| 0 yes | One-shot prompt | No project files |
| 1-2 yes from Q1-Q3 only, with Q4=no and Q5=no | Mini SDAD | One instruction file from `templates/mini-sdad/MINI-SDAD.md` |
| Q4=yes or 3 yes total | Standard SDAD | Adapter plus core control files |
| Q5=yes | Standard SDAD minimum | Adapter, core control files, and explicit risk tracking |
| Q5=yes with production-facing, destructive, migration, real user data, auth, money, release, or rollback risk | Full SDAD | Adapter, core files, review, ADRs, risk gates |
| 4-5 yes | Full SDAD | Adapter, core files, review, ADRs, risk gates |

When unsure, choose the smaller scale only if no Q5 risk exists. Escalate later
when repeated pain, context loss, risk, or multiple sessions appear.

## Maintenance Cost

Do not create Standard or Full SDAD files unless you will keep them current.

At the end of every Standard or Full SDAD work packet, handoff, or session,
check and update:

- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- operating rules or ADRs when decisions or repeated pain changed,
- `save-state.md` when a session pauses or ends, handoff is expected, owner
  direction changes, blocked/partial/unverified state remains, or context would
  be expensive to reconstruct.

If no file needs a content change, state which files were checked and why no
update was needed.

Mini SDAD still has a completion gate: changed files, check evidence, and
limitations or unverified behavior must be shown before a slice is called
evidence-ready. Owner acceptance is still required before final done unless the
owner delegates that acceptance policy.

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

Step 0.5 - Choose autonomy before implementation.

Use these defaults unless I say otherwise:
- One-shot prompt -> no persistent autonomy contract.
- Mini SDAD -> Level 1 Unit Autonomy, treated as one small approved packet.
- Standard SDAD -> Level 2 Work Packet Autonomy.
- Full SDAD or Q5 risk -> Level 2 for implementation, with Level 4 gates for
  release, migration, destructive actions, data/auth/money/security decisions,
  rollback, and production claims.

A work packet may contain one or more review-worthy development units. Do not
ask me to approve every micro-task, every small SPEC item, or every
evidence-ready unit inside an approved packet. A unit is an internal review and
evidence slice, not a separate owner-approval boundary unless I say so. Continue
until the packet reaches a checkpoint or a stop condition appears.

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
Claude Code means the local/CLI coding tool with project filesystem access. It
does not mean Claude.ai chat.

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
memory. Offer deterministic fallback options: retry with network access, ask me
to paste the raw file content from the source URL, use the terminal installer, or
clone/download the repository manually.

For Standard or Full SDAD, after installing the instruction file, bootstrap this
project:

1. create or update docs/INDEX.md,
2. create or update docs/Repository-Operating-Rules.md,
3. create or update SPEC/SPEC-COMPLETE.md,
4. create or update docs/TODO-Open-Items.md,
5. create or update review-findings.md,
6. ask me for product pain, smallest useful version, non-goals, risks,
   owner-controlled decisions, the first work packet, the review-worthy units
   inside it, and evidence required for completion.

A review-worthy development unit may contain multiple related small tasks. It
should be large enough that review has meaning, but small enough to verify in one
handoff. Do not stop for owner approval after every micro-task or small SPEC
item inside an approved work packet.

Proceed autonomously inside the approved work packet until evidence is ready.
Stop and ask me only when scope would expand, a Q5 risk changes, a destructive
or irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or the requested work conflicts with current evidence.

Do not overwrite existing project files without showing me what will change.
Completion requires evidence, not AI confidence.

For Mini SDAD at loop end, do not check SPEC-COMPLETE, TODO, review-findings, or
ADRs unless the project has escalated. Report the active task, changed files,
check evidence, limitations or unverified behavior, evidence-ready status, owner
decisions or acceptance needed, and whether to escalate.

For Standard or Full SDAD at loop end, check whether SPEC-COMPLETE, TODO,
review-findings, rules, or ADRs must be updated at the work-packet or handoff
boundary. If nothing changes, say which files were checked and why no update was
needed.

Update save-state.md when a session pauses or ends, handoff is expected, owner
direction changes, blocked/partial/unverified state remains, or context would be
expensive to reconstruct.

Before closing, archiving, replacing, or restarting a long AI coding session,
create a session handoff under docs/sdad/handoffs/YYYY-MM-DD-topic.md. Treat
the chat as an execution trace, not permanent memory; a fresh session must be
able to continue from the handoff, active spec, and current repository state.

For Mini SDAD, an AI may call a unit evidence-ready when changed files, check
evidence, and limitations or unverified behavior are shown. Do not call final
completion done until owner acceptance is shown or the owner has explicitly
delegated the acceptance policy.
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
Define the first low-intervention work packet and its review-worthy units.
Ask me for product pain, smallest useful version, non-goals, risks,
owner-controlled decisions, autonomy level, and evidence required for completion.
```

The first successful bootstrap should create or update:

- `docs/INDEX.md`,
- `docs/Repository-Operating-Rules.md`,
- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`.

If those files already exist, the AI should show the proposed changes before
editing them.
