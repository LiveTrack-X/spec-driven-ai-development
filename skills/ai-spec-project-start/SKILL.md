---
name: ai-spec-project-start
description: >-
  Use when starting, publishing, or reorganizing a project around
  SPEC-driven AI development as practiced by a human owner who does not
  necessarily write code directly but supervises product direction, AI planning,
  AI implementation, cross-model review, evidence-based verification, and
  completion decisions. Trigger for new project kickoff, AGENTS.md/docs/SPEC/TODO
  bootstrap, owner-supervised AI coding, multi-agent review loops, converting
  lessons from a previous project into reusable operating rules, or creating a
  public template/repo such as spec-driven-ai-development.
---

# AI-SPEC Project Start

## Identity

Treat this workflow as:

```text
Owner-supervised, SPEC-driven, multi-agent, evidence-based AI development.
```

Korean:

```text
인간 오너 감독형, SPEC 주도, 다중 AI 교차검증 기반 개발 플로우.
```

This is not "AI writes code from a spec." It is a project-control loop where a
human owner keeps direction, priority, risk judgment, and final acceptance while
AI sessions take roles such as planner, spec writer, builder, reviewer, QA, and
documentation maintainer.

## Field-Proven Baselines

This workflow should preserve two concrete families of practice:

- Documentation-governance controls for documentation routing, source-of-truth
  order, active TODO/review ledgers, and production-readiness hardening.
- Release-governance controls for version lanes, migration maps, release gates,
  risk-domain rules, and cross-AI pre-release review.

When the user asks whether their development flow is reasonable, references a
previous project, asks to encode lessons into a reusable pattern, or is starting
a project with releases/migrations/high-risk behavior, load
`references/field-patterns.md`.

When the user asks to capture "obvious" rules, reduce repeated confusion, harden
agent behavior, or prevent stale SPEC/history mistakes, load
`references/implicit-rules.md`.

When the user asks whether SDAD fits a project, whether a project is ready for
this workflow, or what to add before 1.0-style release, route to the public docs:
`docs/fit-assessment.md`, `docs/anti-patterns.md`, `docs/diagrams.md`,
`docs/autonomy-levels.md`, `docs/implementation-discipline.md`, and the ADR
template under `templates/project-control-files/SPEC/adr/`.

## Core Assumption

The owner may understand logic, architecture, product intent, risks, and user
pain without personally writing implementation code. Design the project system so
that the owner can still govern development through:

- clear SPECs,
- explicit non-goals,
- work packets and autonomy levels,
- review-worthy development units,
- implementation discipline,
- cross-model review,
- reproducible tests,
- active TODO/review ledgers,
- and evidence-based completion criteria.

## Beginner-Friendly Behavior

When the user appears new to development tools, do not lead with Git, Python,
PowerShell, Bash, or script installation.

Start with the no-clone path:

```text
Use SPEC-Driven AI Development as the project control method.
Source repository: https://github.com/LiveTrack-X/spec-driven-ai-development
First determine whether you can edit files in this project. If this is a
chat-only environment such as Claude.ai, ChatGPT web, or another browser chat
with no project filesystem, do not install adapters or claim files were saved.
Use the repository for planning only, then tell the user to open the project in
Codex, Claude Code, Cursor, Copilot Chat, or another file-editing AI coding
tool.
Before fetching, state which adapter or Mini SDAD template you are installing
and why.
If you cannot determine the current tool, ask the user to specify one of:
Codex / Claude Code / Cursor / Copilot Chat / Generic.
Do not infer adapter paths. Use the exact raw adapter URL for this tool.
Show the source URL and first 10 lines of the fetched adapter before saving.
If fetching fails, stop and report the failure instead of inventing an adapter.
Offer deterministic fallback options: retry with network access, ask the user
to paste the raw file content from the source URL, use the terminal installer,
or clone/download the repository manually.
Bootstrap the first active SPEC slice and project control files.
Ask for the first work packet and the review-worthy development units inside
it. A unit may contain multiple related small tasks and should be large enough
that review has meaning, but small enough to verify in one checkpoint.
Choose autonomy before implementation. Default to Level 1 Unit Autonomy for
Mini SDAD, treating the active unit as one small approved packet; use Level 2
Work Packet Autonomy for Standard SDAD, and Level 4 gates for Full SDAD release,
migration, destructive actions, data/auth/money/security decisions, rollback,
and production claims.
Proceed autonomously inside the approved work packet until evidence is ready.
Do not stop after every micro-task, small SPEC item, or evidence-ready unit.
Stop for owner input only when scope expands, Q5 risk changes, destructive or
irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or evidence conflicts with the plan.
Use implementation discipline inside the packet: surface assumptions, prefer the
simplest working design, make surgical changes, and tie every step to
verification.
At loop end, update save-state.md when work pauses, handoff is expected,
direction changes, blocked/partial/unverified state remains, or context would be
expensive to reconstruct.
Do not overwrite existing files without showing proposed changes.
```

Explain terms plainly:

- A Codex skill is optional and only applies to Codex.
- An adapter is a project instruction file for a specific AI coding tool.
- The user does not need Git or Python for the prompt-only path.
- Terminal commands are optional setup shortcuts, not the main requirement.
- Adapter installation is deterministic. Prefer exact raw URLs, target paths,
  and fetch evidence over model guesses.
- Before fetching, name the adapter/template and explain why. If the current
  tool is unclear, ask the user to choose Codex, Claude Code, Cursor, Copilot
  Chat, or Generic.
- Claude Code means the local/CLI coding tool with project filesystem access,
  not Claude.ai chat.
- Chat-only browser tools can plan and explain, but must not claim adapter
  installation unless they can edit files in the target project.

If a user asks "how do I start?", provide the AI-agent paste prompt first, then
offer terminal installers only as an optional path.

## Review-Worthy Development Units

Do not stop development after every micro-task.

Prefer low-intervention owner control:

- Mini SDAD: Level 1 Unit Autonomy.
- Standard SDAD: Level 2 Work Packet Autonomy.
- Full SDAD or Q5 risk: Level 2 for implementation, with Level 4 gates for
  release, migration, destructive actions, data/auth/money/security decisions,
  rollback, and production claims.

A work packet is a bounded container for one or more review-worthy development
units. The owner approves the packet boundary, not every small task inside it.
Do not use every small SPEC item as a separate owner-approval boundary by
default.

Before implementation, define a review-worthy development unit:

- one user-visible workflow,
- one bugfix with its regression check,
- one connected docs/template/prompt update,
- one risk-domain hardening pass,
- or one small feature path from behavior to evidence.

Each unit may include multiple related TODOs. Units help organize review and
evidence; they do not require separate owner approval while they stay inside the
approved packet. Continue inside the approved work packet until the packet can
be reviewed with changed files, checks, known limits, and evidence.

Use two states:

- `AI-complete / evidence-ready`: changed files, checks, docs checked, limits,
  and risks are shown.
- `Owner-accepted`: the owner accepts, rejects, revises, or defers at a
  checkpoint.

Evidence-ready units may continue inside the approved packet. Final completion
requires owner acceptance or an explicitly delegated acceptance policy.

Inside the packet, enforce implementation discipline:

- surface assumptions without hiding confusion,
- prefer the simplest working design,
- make surgical changes only,
- tie each step to verification.

Ask the owner only when:

- scope would expand beyond the approved packet,
- Q5 risk, release posture, data, auth, money, migration, or destructive action
  changes,
- a tradeoff belongs to the owner,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan.

## Scale Selection Rule

Before installing adapters or bootstrapping control files, choose the smallest
workflow scale that fits.

Ask:

1. Will this take more than one AI session?
2. Will the owner come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, user data, auth, money, or production risk?

Choose:

- `0 yes`: One-shot Prompt. Do not create SDAD files.
- `1-2 yes from questions 1-3 only, with Q4=no and Q5=no`: Mini SDAD. Create
  one instruction file from `templates/mini-sdad/MINI-SDAD.md`.
- `Q4=yes or 3 yes total`: Standard SDAD. Create core control files.
- `Q5=yes`: Standard SDAD minimum, even if it is the only yes.
- `Q5=yes with production-facing, destructive, migration, real user data, auth,
  money, release, or rollback risk`: Full SDAD.
- `4-5 yes`: Full SDAD. Use full workflow, review, ADRs, and risk gates.

Override rules beat raw yes-counts. When unsure, choose the smaller scale only
if no Q5 risk exists. Escalate when repeated pain, context loss, risk, or
multiple sessions appear.

## Operating Loop

Use this sequence:

```text
1. Prior project pain or product need
2. Owner + AI planning conversation
3. SPEC draft with scope, non-goals, risks, acceptance criteria
4. Define a work packet and review-worthy development units
5. Builder AI implements the packet, including related small tasks inside scope
6. Separate AI/model/session reviews the result
7. Tests, docs, and reproducible commands make units evidence-ready
8. Owner checkpoint accepts, revises, defers, or rejects
9. Lessons become operating rules, TODOs, ADRs, or archived notes
```

Never collapse steps 4-7 into "AI said it is done." AI-complete means
evidence-ready. Final completion is a decision based on evidence and owner
acceptance.

## Control File Maintenance Cost

Standard and Full SDAD control files are not write-once setup files. They must
be checked and updated at the end of every work packet, handoff, or session.

At loop end:

- update `SPEC/SPEC-COMPLETE.md` when behavior, implementation status, scope,
  constraints, or acceptance criteria changed,
- update `docs/TODO-Open-Items.md` when work was completed, added, deferred, or
  split,
- update `review-findings.md` when bugs, risks, review findings, or blocked
  issues were found, fixed, deferred, or accepted,
- update operating rules or ADRs when repeated pain, decisions, boundaries, or
  tradeoffs changed.

If no control file needs a content change, state which files were checked and why
no update was needed. Do not claim completion while control files are stale.

If the user cannot afford this maintenance cost, choose Mini SDAD or a one-shot
prompt instead.

Mini SDAD loop-end behavior is smaller: do not check `SPEC/SPEC-COMPLETE.md`,
`docs/TODO-Open-Items.md`, `review-findings.md`, or ADRs unless the project has
escalated. For Mini, report the active task, changed files, check evidence,
limitations or unverified behavior, evidence-ready status, owner decisions or
acceptance needed, and whether to escalate.

## Save-State Update Triggers

`save-state.md` is optional. If the project uses it, update it when:

- a session is ending or pausing before work is fully accepted,
- an active slice completes and the next slice is not obvious from TODO/SPEC,
- the owner changes direction, priority, acceptance criteria, or risk tolerance,
- work is blocked, skipped, partial, degraded, or unverified,
- another AI tool, model, session, or person is expected to continue the work,
- current context would be expensive to reconstruct from code and docs alone.

If none of these triggers apply, say so. If `save-state.md` exists but is stale,
update it, mark it stale, or archive it before handoff.

## Mini Unit Completion

For Mini SDAD, do not call a unit evidence-ready until:

- the active review-worthy unit is restated,
- changed files are listed,
- tests, commands, or manual checks are shown, or the reason they could not run
  is stated,
- user-visible behavior or output is described,
- limitations and unverified behavior are named,
- unrelated scope was not added,
- owner decisions or acceptance needed are named.

Not evidence-ready when the AI only says it is done, checks are hidden,
uncertainty is hidden, or unrelated changes were made without owner approval.
Final done still requires owner acceptance unless the owner has explicitly
delegated the acceptance policy. Requested changes or deferred decisions mean
the unit is not done.

## First Conversation

Before writing code, extract the owner's control model:

- What previous project pain triggered this project?
- What would have made that previous project easier?
- What must the next AI session know before touching code?
- Which decisions must remain owner-controlled?
- What is the smallest useful result?
- What is the first work packet?
- Which review-worthy units or related small tasks should be batched into that
  packet?
- What is explicitly not active work yet?
- What evidence proves the packet is evidence-ready?

If the owner has already given enough context, proceed and mark assumptions.

## Required Project Control Files

Create or update these early:

- `AGENTS.md`: mandatory rules for every AI agent/session.
- `docs/INDEX.md`: the single routing table for active docs.
- `docs/Repository-Operating-Rules.md`: durable rulebook for repeated rules.
- `SPEC/SPEC-COMPLETE.md`: current integrated product and implementation baseline.
- `SPEC/adr/`: decision records for durable rationale when needed.
- `docs/TODO-Open-Items.md`: current open work only.
- `review-findings.md`: active bug/review findings only.
- `README.md`: human-facing current project summary.

Optional but useful:

- `save-state.md`: current handoff if work pauses.
- `next-task.md`: next recommended slice.
- `docs/archive/`: historical docs and completed plans.
- `docs/product-notes/`: reference ideas that are not active implementation.

## Source Of Truth

When sources disagree, prefer:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical SPEC,
4. active SPEC files,
5. handoff/save-state files,
6. product notes and external references,
7. archived or historical docs,
8. chat memory or AI confidence.

Current-over-historical rule: if a SPEC includes a timeline from past to
present, prefer the newest active/current section over older sections. Treat
older SPEC material as rationale or history unless it is explicitly reaffirmed
in the current active SPEC path.

## AI Role Split

Use role separation to reduce single-model blind spots:

- Planning AI: turns owner pain into product scope and non-goals.
- SPEC AI: writes implementation-ready SPEC with acceptance criteria.
- Builder AI: implements a bounded review-worthy unit.
- Reviewer AI: finds bugs, security risks, missing tests, docs drift, and overreach.
- QA AI: tries to reproduce behavior and verify commands.
- Maintainer AI: updates docs, TODO, findings, and handoff.
- Owner: sets direction, priority, risk tolerance, and final acceptance.

One AI session may perform more than one role, but important changes should get a
separate review pass.

## SPEC Rules

Keep three layers distinct:

- Vision: desired future and product philosophy.
- Active SPEC: implementation scope for now, with completion criteria.
- Research/backlog: useful ideas not approved for current implementation.

Do not let research notes become active work just because they are exciting.
Do not let a SPEC claim implementation status without code/test evidence.
Do not implement from an older SPEC section when a newer active SPEC, current
code, or current test evidence supersedes it.

## Version And Risk Rules

If the project has stable/beta/rewrite/migration lines, define version lanes:

- allowed changes per lane,
- where agents should work,
- how critical fixes sync across lanes,
- what must not sync,
- release-channel and rollback rules.

If the project has high-risk domains, name them explicitly. Examples include
auth/tenant isolation, database migrations, backup/restore, real-time callbacks,
thread/lock ownership, platform boundaries, release assets, prompt contracts, or
model/tool permissions. Each risk domain needs review checks, docs, tests, and
handoff evidence.

## Evidence Rules

Every implementation handoff must include:

- changed files,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- what is not complete,
- owner decision needed, if any.

For production-readiness claims, require deployment, migration, auth/security,
backup/restore, monitoring, and rollback evidence as applicable.

## Pain-To-Rule Extraction

When the owner references a previous project, convert pain into reusable rules.

Examples:

- "AI sessions forgot context" -> require `AGENTS.md` and `docs/INDEX.md`.
- "Docs were scattered" -> require document classes and archive rules.
- "AI said complete but bugs remained" -> require review findings and tests.
- "Old plans misled new sessions" -> define source-of-truth order.
- "Large refactors became hard to verify" -> require review-worthy units and cross-review.

This is the heart of the workflow: past friction becomes future operating
structure.

## Bootstrap Output

For a new project, produce a compact bootstrap rather than a huge master plan:

1. product definition,
2. first user and first use case,
3. non-goals,
4. risk list,
5. required control files,
6. first active SPEC slice, work packet, and review-worthy development units,
7. validation commands,
8. review loop.

Use `references/starter-templates.md` for copyable prompts and file templates.
Use `references/field-patterns.md` when translating previous-project lessons
into operating rules.
Use `references/implicit-rules.md` for Core 5 and Extended 15 rule checks.

## Guardrails

- Keep the owner in control of scope and acceptance.
- Keep AI output auditable.
- Keep active docs smaller and clearer than archives.
- Keep future ideas out of the active implementation path.
- Make obvious but consequential rules explicit.
- Prefer a boring verified review-worthy unit over an impressive unverified
  expansion.
- Use Korean for owner-facing explanation when helpful; keep filenames and
  machine-facing identifiers stable and ASCII.
