# User Guide And FAQ

Use this guide when you want to understand what SDAD does before pasting an
installer prompt or asking an AI agent to change your project.

SDAD is a control method for AI-assisted development. It does not make AI output
correct by itself. It makes scope, evidence, review, handoff, and owner
acceptance harder to lose.

## Quick Choice

| If this is your situation | Use this | What to expect |
|---|---|---|
| You need one disposable answer or change | One-shot prompt | No SDAD files |
| The task is small, but "done" needs evidence | Mini SDAD | One AI instruction file |
| The project will span sessions or reviewers | Standard SDAD | SPEC, TODO, review, and docs control files |
| There is release, migration, production, user data, auth, money, security, destructive action, or rollback risk | Full SDAD or Standard minimum with explicit gates | Review, evidence, ADRs when needed, and owner gates |
| You are in Claude.ai, ChatGPT web, or another chat-only tool | Planning only | Do not claim adapter files were installed |

Choose the smallest scale that protects the project. Risk overrides raw
yes-counts.

## What SDAD Adds

- A current SPEC so old notes do not override active work.
- Work packets so AI does not stop after every micro-task.
- Review-worthy development units so evidence is grouped into useful review
  slices.
- Evidence-ready status so "AI says done" is not treated as final done.
- Owner acceptance so risk and product direction stay human-controlled.
- Implementation notes so spec-unstated decisions are not hidden in chat.
- Handoff and save-state rules so a later session can continue from repository
  state instead of memory.
- Context-stability rules so large logs, archives, generated files, and private
  data do not flood the AI context.

## Common Situations

### I Just Want To Try It

Use the copy-paste prompt in [README.md](../README.md). Let the AI choose the
scale before it creates files.

If you only want to discuss a project in a chat-only environment, use SDAD as a
planning checklist. Install adapters later from a tool that can edit the project
folder.

### I Have A Small Project

Start with [mini-sdad.md](mini-sdad.md). Mini SDAD creates one instruction file
and asks the AI to show changed files, checks, limitations, and owner acceptance
before calling work done.

Do not create Standard or Full SDAD files unless you will keep them current.

### I Have A Real Project That Will Continue

Use Standard SDAD when work spans multiple sessions, multiple AI tools, durable
TODOs, review findings, or recurring context loss.

The important files are:

- tool instruction file: `AGENTS.md`, `CLAUDE.md`,
  `.cursor/rules/spec-driven-ai-development.mdc`,
  `.github/copilot-instructions.md`, or `AI-SESSION-INSTRUCTIONS.md`,
- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- `docs/implementation-notes.md`,
- `save-state.md` when the project uses session recovery.

### I Have Production Or Data Risk

Use Full SDAD, or at least Standard SDAD with explicit risk gates, when a packet
touches release, migration, production claims, destructive action, real user
data, auth, money, security, rollback, or another owner-controlled risk.

Not every packet in a risky project is High intensity. Raise only the packet
that changes behavior, policy, boundary, evidence claim, or risk acceptance for
a risk gate. See [operating-intensity.md](operating-intensity.md).

### The AI Keeps Asking Questions

Ask for a clarification checkpoint:

```text
Inspect the current code, tests, active docs, SPEC, TODOs, review findings, and
ADRs first. Ask only the next blocking question, include your recommended
answer, and explain what changes if I choose differently.
```

Clarification checkpoints are not micro-approval. They are for unresolved
blocking decisions after repository evidence has been checked.

### The AI Says It Is Done

Do not accept final completion until the evidence is visible.

Ask for:

- changed files,
- tests, build, lint, manual check, or reason a check could not run,
- docs checked or updated,
- implementation notes for spec-unstated decisions,
- review findings fixed or tracked,
- limitations, partial behavior, degraded behavior, or unverified behavior,
- owner decisions still needed.

`AI-complete / evidence-ready` means the AI produced reviewable evidence.
`Owner-accepted` means the owner accepted, revised, rejected, or deferred the
work.

### The AI Made A Decision The SPEC Did Not Cover

Record it in `docs/implementation-notes.md` for Standard or Full SDAD.

Use implementation notes for:

- assumptions,
- compromises,
- rejected alternatives,
- owner-relevant tradeoffs,
- follow-up risks,
- verification impact.

Do not use implementation notes as a raw thought transcript or a mechanical edit
log.

### Should This Be An ADR?

Use an ADR only when the decision is hard to reverse, would surprise a future
maintainer without context, and represents a real tradeoff.

Smaller spec-unstated implementation choices belong in implementation notes.

### When Do I Update Save-State Or Handoff?

Update `save-state.md` when a session pauses or ends, handoff is expected, owner
direction changes, blocked or unverified state remains, or context would be
expensive to reconstruct.

Create `docs/sdad/handoffs/YYYY-MM-DD-topic.md` before closing, replacing, or
restarting a long AI coding session. The handoff should reference existing
SPECs, TODOs, ADRs, review findings, implementation notes, logs, and evidence by
path or URL instead of duplicating long content.

## What Not To Do

- Do not install all adapters. Install the one instruction file for your AI
  coding tool.
- Do not treat every small task as an owner approval gate.
- Do not call evidence-ready work finally done without owner acceptance.
- Do not let old plans override the current SPEC.
- Do not create Standard or Full control files if you will not maintain them.
- Do not paste large logs, archives, generated files, or private data into AI
  context by default.

## Where To Go Next

- [getting-started.md](getting-started.md): setup paths and first 10 minutes
- [no-clone-quick-install.md](no-clone-quick-install.md): copy-paste setup
- [mini-sdad.md](mini-sdad.md): one-file SDAD for small projects
- [maintenance-cost.md](maintenance-cost.md): required loop-end updates
- [autonomy-levels.md](autonomy-levels.md): work packets and owner checkpoints
- [implementation-notes.md](implementation-notes.md): decision-log rules
- [session-handoff.md](session-handoff.md): long-session continuity
