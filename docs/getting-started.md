# Getting Started

Use this guide when you want to apply SPEC-Driven AI Development to a real
project for the first time.

The short version:

```text
Install one instruction file, define one low-intervention work packet, then
require evidence before accepting completion.
```

## Choose Scale First

Do not start with full SDAD automatically.

Ask five questions:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Override rules beat raw yes-counts.

| Trigger | Use |
|---|---|
| 0 yes | One-shot prompt |
| 1-2 yes from Q1-Q3 only, with Q4=no and Q5=no | [Mini SDAD](mini-sdad.md) |
| Q4=yes or 3 yes total | Standard SDAD |
| Q5=yes | Standard SDAD minimum |
| Q5=yes with production-facing, destructive, migration, real user data, auth, money, release, or rollback risk | Full SDAD |
| 4-5 yes | Full SDAD |

When unsure, choose the smaller scale only if no Q5 risk exists, and escalate
later when evidence shows the project needs it.

## Maintenance Cost

Standard and Full SDAD create control files that must stay current. At the end
of every loop, check and update `SPEC/SPEC-COMPLETE.md`,
`docs/TODO-Open-Items.md`, `review-findings.md`, and any rules or ADRs affected
by the work.

Update `save-state.md` when a session pauses or ends, handoff is expected, owner
direction or acceptance criteria changed, blocked/partial/unverified state
remains, or context would be expensive to reconstruct.

For long AI sessions that will be closed, replaced, restarted, or resumed in a
fresh session, create a session handoff under
`docs/sdad/handoffs/YYYY-MM-DD-topic.md`. See
[session-handoff.md](session-handoff.md).

If no file needs a content change, say which files were checked and why no
update was needed.

If you do not want that maintenance cost, choose One-shot Prompt or
[Mini SDAD](mini-sdad.md). See [maintenance-cost.md](maintenance-cost.md).

## Complete Beginner Path

If you are not comfortable with terminals, Git, Python, or shell scripts, use
the no-clone path first:

- Open your project in an AI coding tool that can edit files.
- Copy the prompt from [no-clone quick install](no-clone-quick-install.md).
- Paste it into the AI agent.
- Let the AI choose the scale before it creates any files.

Codex is optional. A Codex skill is only for Codex users.

Chat-only tools such as Claude.ai, ChatGPT web, or browser chat can help plan,
but they cannot install adapters unless they have project filesystem access.
Claude Code means the local/CLI coding tool, not Claude.ai chat.

## Who Does What

- The owner decides product direction, risk tolerance, priorities, and final
  acceptance.
- The AI tool helps create SPECs, implement work packets and review-worthy
  units, review work, update docs, and produce evidence.
- Completion is accepted only when the evidence is clear enough for the owner to
  trust the result.

You do not need to write code yourself to use this workflow. You do need to make
clear decisions and reject vague completion claims.

The owner should not need to approve every micro-task or every evidence-ready
unit. Once a work packet is approved, the AI should continue inside that
boundary until it can hand off changed files, checks, known limits, and
evidence at a checkpoint.

Use two states:

- `AI-complete / evidence-ready`: the AI has changed files, run or explained
  checks, updated or checked docs, and named limits.
- `Owner-accepted`: the owner accepts, rejects, revises, or defers the work at a
  checkpoint.

For most Standard SDAD work, use Level 2 Work Packet Autonomy from
[autonomy-levels.md](autonomy-levels.md): the owner approves the packet boundary,
then the AI works through the included units without asking after each small
task or small SPEC item.

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

I am the owner. Help me create the first active SPEC slice and the first
low-intervention work packet.

Start by asking for:
1. the product pain or goal,
2. the smallest useful version,
3. non-goals,
4. risks,
5. owner-controlled decisions,
6. the first work packet,
7. the review-worthy units inside that packet,
8. evidence required before I accept completion.

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
Define the first work packet and the review-worthy development units inside it.
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

After setup, ask the AI for the first work packet, not the whole project and not
a tiny micro-task.

Good first request:

```text
Create the first work packet for the smallest useful version.
Keep future ideas in backlog or non-goals.
Batch related review-worthy units until the packet is meaningful to review, but
keep it small enough to verify in one checkpoint.
Use Level 2 Work Packet Autonomy unless a risk gate requires owner input.
Define the evidence required before I can accept this packet as complete.
```

The first useful output should include:

- product goal,
- target user,
- smallest useful version,
- non-goals,
- known risks,
- owner-controlled decisions,
- active SPEC slice,
- first work packet and review-worthy units,
- TODO list,
- review and verification plan,
- docs that must be created or updated.

## Daily Usage Loop

Use the same loop every session:

```text
Pain -> SPEC -> Work packet -> Build -> Review -> Evidence-ready -> Owner checkpoint -> Rule
```

In practice, the build/review boundary should be a work packet containing one or
more review-worthy development units. Do not stop after every micro-task inside
the approved packet.

### Build Prompt

```text
Read the active docs and current SPEC.
Implement the next approved work packet. You may complete multiple related
review-worthy units inside that packet.
Do not stop for owner approval after every micro-task or every evidence-ready
unit. Stop only if scope would expand, Q5 risk changes, destructive or
irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or current evidence conflicts with the plan.
Before checkpoint handoff, show changed files, verification commands, docs
checked, evidence-ready units, remaining risks, and what is not complete.
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

## Owner Checkpoint Checklist

Before accepting a work packet as "done", check:

- Is the active SPEC slice clear?
- Was the completed work a meaningful packet, not just a micro-task?
- Did the AI stay inside the active scope?
- Are code changes listed?
- Did tests, builds, lint, or manual checks run?
- Were docs checked or updated?
- Are skipped, partial, degraded, or unverified items named?
- If the project uses `save-state.md`, did a pause, handoff, direction change,
  blocked state, or expensive context trigger require an update?
- Are review findings either fixed or tracked?
- Did repeated pain become a rule, checklist, test, or template update?

If any answer is unclear, do not accept completion yet. Ask for evidence or move
the item into `docs/TODO-Open-Items.md` or `review-findings.md`.

For Mini SDAD, a unit may be called evidence-ready when the active task, changed
files, check evidence, and limitations or unverified behavior are shown. It is
not finally done until owner acceptance is shown or the owner has explicitly
delegated the acceptance policy.

## Common Mistakes

- Starting from old notes instead of the current active SPEC.
- Asking AI to build the whole project at once.
- Stopping after every micro-task instead of a work packet or review-worthy
  development unit.
- Treating each small SPEC item as a separate owner-approval gate.
- Treating evidence-ready as owner-accepted.
- Treating confident AI language as completion.
- Letting future ideas enter the active implementation unit.
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
