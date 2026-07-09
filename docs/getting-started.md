# Getting Started

Use this guide when you want to apply SPEC-Driven AI Development to a real
project for the first time.

If you are still deciding whether SDAD fits your situation, start with
[user-guide.md](user-guide.md).

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

Update `docs/implementation-notes.md` when implementation required a
spec-unstated assumption, change, compromise, rejected alternative,
owner-relevant tradeoff, follow-up, or verification-impact note. Do not turn it
into a raw thought transcript or mechanical edit log.

Update `save-state.md` when a session pauses or ends, handoff is expected, owner
direction or acceptance criteria changed, blocked/partial/unverified state
remains, or context would be expensive to reconstruct.

For long AI sessions that will be closed, replaced, restarted, or resumed in a
fresh session, create a session handoff under
`docs/sdad/handoffs/YYYY-MM-DD-topic.md`. See
[session-handoff.md](session-handoff.md).

Keep active live-state files short. If state, TODO, review, or handoff files
become long journals, move old history to archive/history files and use bounded
reads for archives, logs, generated artifacts, private data, and broad search
output. See [context-stability.md](context-stability.md).
Default soft trigger: bounded reads above 50 KB or 500 lines; context-stability
check above 200 KB or 2,000 lines; no full startup read above 1 MB unless the
owner explicitly asks for historical reconstruction.

If no file needs a content change, say which files were checked and why no
update was needed.
Before evidence-ready or handoff, run the Documentation Record Audit in
[maintenance-cost.md](maintenance-cost.md): state the minimum update-set row,
docs changed, docs checked with no update needed, stale docs, archive/evidence
links, and validation commands.

If you do not want that maintenance cost, choose One-shot Prompt or
[Mini SDAD](mini-sdad.md). See [maintenance-cost.md](maintenance-cost.md).

## First Packet Routine

For Standard or Full SDAD, use `docs/INDEX.md` as the working router after SDAD
control files are installed. In this source repository, that file is a template
at `templates/project-control-files/docs/INDEX.md`:

```text
Route current state -> Scale/compress -> PLAN -> Active SPEC -> optional ADR -> TODO/work packet -> JIT clarification -> Build/review/evidence -> Owner checkpoint/maintenance
```

This order clarifies what to look at and when. It does not force every file into
every packet: skip ADR, separate TODO, evidence matrix, claim registry,
save-state, or handoff when their trigger does not exist, and say why in the
evidence-ready summary.

After Standard or Full SDAD is installed, choose an operating intensity for each
packet: `Standard SDAD / High`, `Standard SDAD / Medium`, `Standard SDAD / Low`,
`Full SDAD / High`, `Full SDAD / Medium`, or `Full SDAD / Low`. Use
[operating-intensity.md](operating-intensity.md) when a usable baseline exists
and the project should freeze, compress evidence, or simplify owner review.

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

First choose One-shot, Mini, Standard, or Full SDAD. Create only the files that
scale needs.

Start by asking for:
1. the product pain or goal,
2. the smallest useful version,
3. non-goals,
4. risks,
5. owner-controlled decisions,
6. the first work packet,
7. the review-worthy units inside that packet,
8. evidence required before I accept completion.

If Standard or Full SDAD is selected, create the first project control files:
- AGENTS.md or equivalent AI instruction file,
- docs/INDEX.md,
- docs/Repository-Operating-Rules.md,
- SPEC/SPEC-COMPLETE.md,
- docs/TODO-Open-Items.md,
- review-findings.md.

If product, hardware, compatibility, packaging, remote tester, external lab, or
release claims need evidence stronger than local software tests, also create
only the needed product evidence templates:
- docs/evidence-matrix.md,
- docs/claim-registry.md,
- docs/artifact-contracts.md,
- docs/work-packet-state.md,
- docs/remote-evidence-import.md.
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

The skill name is optional for advanced users, not a requirement for normal
owners. Natural requests such as "review this repo", "implement the current
SPEC", "prepare a release", "update the docs", or "create a handoff" should be
routed by intent after the SDAD instructions are installed.

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
If the plan is fuzzy, inspect repository evidence first, then ask only the next
blocking clarification question with your recommended answer.
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
- clarification questions resolved or still owner-blocking,
- TODO list,
- review and verification plan,
- docs that must be created or updated.

For hardware, packaged product, remote tester, compatibility, or release-claim
projects, also ask whether the optional product evidence templates are needed:
`docs/evidence-matrix.md`, `docs/claim-registry.md`,
`docs/artifact-contracts.md`, `docs/work-packet-state.md`, and
`docs/remote-evidence-import.md`. See
[product-evidence-templates.md](product-evidence-templates.md).

For lean Standard bootstraps, optional evidence templates are create-on-demand.
If `docs/INDEX.md` routes optional evidence docs that do not exist yet, create
only the ones needed by current product, hardware, package, remote evidence, or
release claims.

Small Project Compression Rule: for One-shot, Mini SDAD, or a small Standard
packet, one evidence-ready summary is enough when there is one active slice, no
Q5 gate changed, no unresolved review finding or durable spec-unstated decision
must survive the turn, no handoff is expected, and the evidence can be shown
compactly. Turn on SPEC, TODO, review findings, implementation notes,
save-state, handoff, Evidence Matrix, Claim Registry, or Artifact Contract only
when that surface has an active job.

## Daily Usage Loop

Use the same loop every session:

```text
Scale/compress -> Active SPEC slice -> Work packet -> Evidence tier/gates -> Owner checkpoint -> Maintenance
```

This is the control spine. The pain loop below is the feedback cycle, not a
separate document-read order.

Choose scale and compression before creating files. Before evidence-ready,
check only the gates that apply: reference parity for reference-derived work,
evidence tier for claim scope, product evidence templates for product/hardware
claims, and Level 4 owner gates for Q5 risk. ADRs are conditional, not a
mandatory step.

```text
Pain -> SPEC -> Work packet -> Build -> Review -> Evidence-ready -> Owner checkpoint -> Rule
```

In practice, the build/review boundary should be a work packet containing one or
more review-worthy development units. Do not stop after every micro-task inside
the approved packet.

### Quick Routing Prompt

Use this when the AI seems unsure which SDAD document to check next:

```text
Use docs/INDEX.md as the working router for this packet.
Identify the current moment: starting/resuming, defining scope, choosing next
task, investigating bug/risk, making a spec-unstated choice, making a claim,
preparing owner checkpoint, ending/handoff, or turning repeated pain into a rule.
Then report which active docs must be checked, which optional surfaces are not
needed, whether any long log/evidence record should be split into a timestamped
YYYY-MM-DD-HHMM-start-topic.md file, and whether the packet is evidence-ready
or still owner-accepted pending.
```

### Build Prompt

```text
Read the active docs and current SPEC.
Implement the next approved work packet. You may complete multiple related
review-worthy units inside that packet.
Do not stop for owner approval after every micro-task or every evidence-ready
unit. Stop only if scope would expand, Q5 risk changes, destructive or
irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or current evidence conflicts with the plan.
If the plan is fuzzy, inspect code, tests, active docs, SPEC, TODOs, review
findings, and ADRs before asking me. Ask only the next blocking question and
include your recommended answer.
Before checkpoint handoff, show changed files, verification commands, docs
checked, implementation notes when the SPEC did not cover a decision,
evidence-ready units, remaining risks, and what is not complete.
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
- Did the AI resolve fuzzy scope from repository evidence before asking you?
- Are code changes listed?
- Did tests, builds, lint, or manual checks run?
- Were docs checked or updated?
- Were spec-unstated implementation decisions recorded in implementation notes?
- Are skipped, partial, degraded, or unverified items named?
- If the packet rebuilds or borrows from an existing product, repo, design, or
  demo, did it map source behavior to implemented behavior and evidence?
- If the packet makes a product, hardware, compatibility, release, package, or
  remote evidence claim, is it mapped through the evidence matrix and claim
  registry?
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
- Passing tests while losing reference-critical behavior from the old product,
  repo, design, or demo.
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
