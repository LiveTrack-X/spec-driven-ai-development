# Getting Started

Use this guide when you want to apply SPEC-Driven AI Development to a real
project for the first time.

The short version:

```text
Install one instruction file, start with one SPEC slice, then require evidence
before accepting completion.
```

## Choose Scale First

Do not start with full SDAD automatically.

Ask five questions:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

| Yes answers | Use |
|---|---|
| 0 | One-shot prompt |
| 1-2 | [Mini SDAD](mini-sdad.md) |
| 3 | Standard SDAD |
| 4-5 | Full SDAD |

When unsure, choose the smaller scale and escalate later.

## Maintenance Cost

Standard and Full SDAD create control files that must stay current. At the end
of every loop, check and update `SPEC/SPEC-COMPLETE.md`,
`docs/TODO-Open-Items.md`, `review-findings.md`, and any rules or ADRs affected
by the work.

If no file needs a content change, say which files were checked and why no
update was needed.

If you do not want that maintenance cost, choose One-shot Prompt or
[Mini SDAD](mini-sdad.md). See [maintenance-cost.md](maintenance-cost.md).

## Complete Beginner Path

If you are not comfortable with terminals, Git, Python, or shell scripts, use
the no-clone path first:

- Open your project in an AI coding tool.
- Copy the prompt from [no-clone quick install](no-clone-quick-install.md).
- Paste it into the AI agent.
- Let the AI choose the scale before it creates any files.

Codex is optional. A Codex skill is only for Codex users.

## Who Does What

- The owner decides product direction, risk tolerance, priorities, and final
  acceptance.
- The AI tool helps create SPECs, implement bounded slices, review work, update
  docs, and produce evidence.
- Completion is accepted only when the evidence is clear enough for the owner to
  trust the result.

You do not need to write code yourself to use this workflow. You do need to make
clear decisions and reject vague completion claims.

## No-Clone Quick Install

You do not need to clone this repository to start.

If you want the easiest path, use [no-clone quick install](no-clone-quick-install.md).
It includes:

- scale selection,
- a prompt you can give directly to an AI agent,
- one-paste PowerShell installer,
- one-paste Bash installer.

## Get This Repository

For prompt-only use, you can just link to this repository.

Clone or download the repository only when you want the full package locally:

```bash
git clone https://github.com/LiveTrack-X/spec-driven-ai-development.git
cd spec-driven-ai-development
```

## Choose A Setup Path

### Path 1: Prompt-Only Start

Use this when you are evaluating the workflow or starting with a plain chat-based
AI coding tool.

Paste this into your AI tool:

```text
Use the SPEC-driven AI development workflow from
https://github.com/LiveTrack-X/spec-driven-ai-development.

I am the owner. Help me create the first active SPEC slice.

Start by asking for:
1. the product pain or goal,
2. the smallest useful version,
3. non-goals,
4. risks,
5. owner-controlled decisions,
6. evidence required before I accept completion.

Then create the first project control files:
- AGENTS.md or equivalent AI instruction file,
- docs/INDEX.md,
- docs/Repository-Operating-Rules.md,
- SPEC/SPEC-COMPLETE.md,
- docs/TODO-Open-Items.md,
- review-findings.md.
```

This path is fastest, but the AI may forget the workflow in later sessions. Move
to Path 2 or Path 3 when the project becomes serious.

### Path 2: Install A Tool Adapter

Use this when you already have a project folder and want the workflow to persist
inside that project.

For small projects, use [Mini SDAD](mini-sdad.md) first. It creates only one
instruction file and avoids the full docs/SPEC structure.

Use the no-clone installer, or clone this repository and install the adapter for
your AI coding tool.

No-clone path:

- [docs/no-clone-quick-install.md](no-clone-quick-install.md)

Cloned repository path:

PowerShell:

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter codex -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter cursor -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter github-copilot -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter generic -TargetPath C:\path\to\project
```

Bash:

```bash
./scripts/install-agent-adapter.sh codex /path/to/project
./scripts/install-agent-adapter.sh claude-code /path/to/project
./scripts/install-agent-adapter.sh cursor /path/to/project
./scripts/install-agent-adapter.sh github-copilot /path/to/project
./scripts/install-agent-adapter.sh generic /path/to/project
```

Then start your AI tool inside the target project and say:

```text
Read the installed SPEC-Driven AI Development instructions.
Bootstrap this project into an owner-supervised, SPEC-driven workflow.
Create the first active SPEC slice and the required control files.
```

### Path 3: Install The Codex Skill

Use this when you work in Codex and want the workflow available as a reusable
skill.

PowerShell:

```powershell
.\scripts\install-codex-skill.ps1
```

Bash:

```bash
./scripts/install-codex-skill.sh
```

Then start a new Codex session and say:

```text
$ai-spec-project-start use this workflow to bootstrap my project.
```

## First 10 Minutes

After setup, ask the AI for a small first slice, not the whole project.

Good first request:

```text
Create the first active SPEC slice for the smallest useful version.
Keep future ideas in backlog or non-goals.
Define the evidence required before I can accept this slice as complete.
```

The first useful output should include:

- product goal,
- target user,
- smallest useful version,
- non-goals,
- known risks,
- owner-controlled decisions,
- active SPEC slice,
- TODO list,
- review and verification plan,
- docs that must be created or updated.

## Daily Usage Loop

Use the same loop every session:

```text
Pain -> SPEC -> Build -> Review -> Evidence -> Owner decision -> Rule
```

### Build Prompt

```text
Read the active docs and current SPEC.
Implement only the next active TODO slice.
Before handoff, show changed files, verification commands, docs checked, and
remaining risks.
```

### Review Prompt

```text
Review this project as a separate AI reviewer.
Focus on bugs, missing tests, SPEC drift, docs drift, unsafe assumptions, and
claims that lack evidence.
Return findings with file paths, severity, and reproduction steps when possible.
```

### Handoff Prompt

```text
Update the project control files after this work.
Record completed work, open TODOs, review findings, verification evidence,
partial or unverified behavior, and any repeated pain that should become a rule.
If no control file needs a content change, state which files were checked and why.
```

## Owner Acceptance Checklist

Before accepting "done", check:

- Is the active SPEC slice clear?
- Did the AI stay inside the active scope?
- Are code changes listed?
- Did tests, builds, lint, or manual checks run?
- Were docs checked or updated?
- Are skipped, partial, degraded, or unverified items named?
- Are review findings either fixed or tracked?
- Did repeated pain become a rule, checklist, test, or template update?

If any answer is unclear, do not accept completion yet. Ask for evidence or move
the item into `docs/TODO-Open-Items.md` or `review-findings.md`.

## Common Mistakes

- Starting from old notes instead of the current active SPEC.
- Asking AI to build the whole project at once.
- Treating confident AI language as completion.
- Letting future ideas enter the active implementation slice.
- Forgetting to update TODOs, review findings, or docs after work.
- Not separating builder and reviewer roles.

## What Success Looks Like

A healthy project using this workflow has:

- one clear current SPEC,
- a short active TODO list,
- review findings that are tracked instead of forgotten,
- evidence attached to every completion claim,
- owner decisions recorded when tradeoffs matter,
- repeated failures converted into durable rules.

When the project has those properties, other AI sessions and other people can
join the work without relying on memory or trust alone.
