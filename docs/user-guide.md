# User Guide And FAQ

[English](user-guide.md) | [한국어](user-guide.ko.md) | [中文](user-guide.zh.md) | [日本語](user-guide.ja.md)

Use this guide when you want to understand what SDAD does before pasting an
installer prompt or asking an AI agent to change your project.

English is the canonical documentation language. Localized user guides are
orientation pages; if they conflict with English docs, templates, or validation
scripts, prefer the English canonical files.

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
- Layered context rules so the AI knows what to load now, what to keep on
  demand, and what to reference only by bounded evidence.
- Before/after change checks so an autonomous packet still leaves an auditable
  trail.

## How SDAD Uses Context

SDAD does not ask an AI to read everything. It gives the AI a context route.

| Layer | What belongs there | How to use it |
|---|---|---|
| Always-loaded instructions | The tool adapter or instruction file: `AGENTS.md`, `CLAUDE.md`, Cursor rules, Copilot instructions, or generic session instructions | Keep this short enough to load at every session start. |
| Active control files | Current SPEC, TODO, review findings, implementation notes, save-state, current handoff | Read the relevant current sections before changing files. |
| On-demand references | Pattern catalog, anti-patterns, field notes, localized guides, setup docs | Open only when the current packet or owner question needs them. |
| Archive and evidence | Old handoffs, large logs, generated reports, historical notes, private or local data | Use bounded reads and links. Do not paste whole archives into chat by default. |

If the AI seems lost, do not fix it by loading more history first. Ask it to
identify the current context layer, active packet, source-of-truth file, and
evidence it still needs.

## Natural-Language Requests

You do not need to know SDAD terms, adapter names, or skill names. Describe the
thing you want in normal language. The AI should infer the intent, choose the
smallest safe route, and tell you briefly how it interpreted the request.

| If you say something like | The AI should treat it as |
|---|---|
| "Check this", "review it", "find bugs", "is anything wrong?" | Review or audit intent |
| "Implement this", "fix it", "make it match the spec" | SPEC implementation intent |
| "Release it", "publish it", "tag it" | Release intent with Level 4 owner gates |
| "The docs are confusing", "write a guide", "add FAQ" | Documentation intent |
| "Continue later", "handoff", "next session lost context" | Handoff or save-state intent |
| "Can we borrow from this repo?" | Reference-intake intent |
| "It asks approval too often", "it runs ahead" | Autonomy tuning intent |

If the intent is clear, the AI should proceed. If the request mixes conflicting
intents, it should ask one blocking question with a recommended default. It
should not make you memorize exact trigger words.

## Codex Practice In SDAD

Codex works best when requests have enough structure to act like small issues,
when the development environment can be improved over time, and when exploratory
work does not become hidden scope. SDAD keeps those habits governed.

| Codex habit | SDAD version |
|---|---|
| Ask questions before a large change | Clarification checkpoint after repository evidence is checked |
| Prompt like a GitHub issue or PR | Work packet with files, examples, constraints, non-goals, and evidence |
| Improve scripts, env vars, or setup over time | Environment improvement loop routed to TODO, rules, templates, or handoff |
| Use Codex as a lightweight task queue | Controlled task queue with packet boundaries, evidence, and owner gates |
| Generate multiple candidate solutions | Optional multi-candidate review for real tradeoffs, not final acceptance |

Use these patterns when they reduce repeated setup friction, improve review
quality, or preserve flow. Do not use them to bypass tests, docs, release gates,
or owner acceptance.

## Troubleshooting FAQ

### Q. I do not know the right SDAD command or skill name.

A. Use a natural-language request and let the AI route the intent.

Good examples:

- "Check this repo for likely bugs and tell me what needs fixing."
- "Implement the current SPEC, and record decisions the SPEC did not state."
- "This is asking approval too often. Tune the autonomy level for this packet."
- "Prepare this for release, but keep release and rollback decisions gated."
- "Make the README easier for first-time users."
- "Create a handoff so the next session can continue safely."

The AI should answer with the interpreted intent, SDAD scale/intensity,
autonomy level, expected evidence, and any owner gate. If that interpretation
would change risk or scope, it should ask one clarification question before
continuing.

Action words choose the route; modifiers tune the route. For example, "review"
or "fix" selects the work type, while "carefully", "fully", "quickly",
"minimal", or "commit and wait" changes inspection depth, compression, or stop
point without expanding scope. "Fully" still stops at evidence-ready unless the
owner accepts the result. "Commit and wait" does not mean push, release, or
deploy.

### Q. The AI asks for approval too often, or runs ahead too much.

A. Adjust the autonomy level, packet boundary, and operating intensity together.

Use autonomy levels as a dial:

| Symptom | Try | Meaning |
|---|---|---|
| It asks before every small step | Level 2 Work Packet Autonomy | You approve the packet boundary, not every micro-task inside it. |
| It should finish one small unit and stop | Level 1 Unit Autonomy | One review-worthy unit is the approved packet. |
| The setup is new, ambiguous, or risky | Level 0 Ask-first | The AI asks before each meaningful step until the boundary is clear. |
| The work is low-risk and the session goal is clear | Level 3 Session Autonomy | The AI works until the session goal, time box, or stop condition. |
| The work touches release, migration, destructive action, user data, auth, money, security, rollback, or production claims | Level 4 Release-gated Autonomy | The AI may prepare work, but owner gates risk acceptance and release decisions. |

If the AI asks after every micro-task, tell it:

```text
Use Level 2 Work Packet Autonomy for this packet. I approve the packet boundary,
not every small task inside it. Continue through related review-worthy units
until evidence is ready, unless a stop condition appears.
```

If the AI runs ahead too much, tell it:

```text
Use Level 1 Unit Autonomy for this task. Do only this unit, then stop with
changed files, checks, limitations, and owner decisions needed.
```

For Standard or Full SDAD, also choose operating intensity. Use Medium or Low
when the baseline is stable and the goal is controlled maintenance, not broad
exploration. Do not use higher autonomy to bypass Level 4 owner gates.

### Q. The AI asks questions before checking the repository.

A. Require a clarification checkpoint.

```text
Inspect repository evidence first: code, tests, active docs, SPEC, TODOs, review
findings, and ADRs. Ask only the next blocking question, include your
recommended answer, and explain what changes if I choose differently.
```

Do not let clarification checkpoints become micro-approval for every small
task.

### Q. The AI says "done" but I cannot tell what changed.

A. Ask for evidence-ready status, not final completion.

Required evidence should include changed files, checks run, docs checked or
updated, limitations, unverified behavior, review findings, implementation
notes when needed, and owner decisions still open.

### Q. Can I use Codex as a task queue or background worker?

A. Yes, but make the queue visible and bounded.

Use Codex background work for small fixes, exploratory branches, or follow-up
ideas only when each item has a packet boundary, expected evidence, and a clear
owner gate. If a queued item becomes real work, route it to
`docs/TODO-Open-Items.md`, `review-findings.md`, `save-state.md`, or handoff.

Do not let queued side quests silently become active SPEC or release scope.

### Q. Should I ask Codex for several possible solutions?

A. Use this for tradeoffs, not for routine edits.

Multiple candidate answers are useful for architecture, migration, performance,
or refactor choices. After choosing, record the rationale in implementation
notes or an ADR when the choice is durable. Evidence and owner acceptance still
decide completion.

### Q. SDAD feels like too many files.

A. Use a smaller scale or lower intensity.

For one-off work, use a one-shot prompt. For small work that still needs
evidence, use Mini SDAD. Use Standard or Full only when you will keep the
control files current.

### Q. The task size is unclear.

A. Classify by continuity and risk, not only by estimated lines of code.

| Signal | Use |
|---|---|
| Disposable answer, copy edit, or one tiny change with no future context | One-shot prompt |
| Small change where "done" still needs proof | Mini SDAD or Level 1 Unit Autonomy |
| Connected docs, prompt, template, or code update with review value | Standard SDAD with Level 2 Work Packet Autonomy |
| Multi-file behavior change, recurring bug, review findings, or context loss | Standard SDAD / Medium or High |
| Release, migration, destructive action, production claim, real user data, auth, money, security, rollback, or owner-controlled risk | Full SDAD or Standard minimum with Level 4 gates |

When unsure, choose the smallest scale that still preserves evidence and owner
control. Escalate only when risk, repeated pain, or context continuity requires
it.

### Q. What should the AI check before and after changing files?

A. Use a lightweight before/after change guard.

Before changing files, the AI should identify:

- active SPEC or owner request,
- approved work packet and autonomy level,
- allowed scope and non-goals,
- owner gates or stop conditions,
- current evidence or files that must be read first.

After changing files, the AI should report:

- changed files,
- checks run or why they could not run,
- docs and control files checked or updated,
- implementation notes needed or "none needed",
- limitations, unverified behavior, and owner decisions still open.

This is not a mandatory MCP flow. It is the minimum audit trail that keeps
autonomy from becoming invisible.

### Q. What evidence is enough when there is no formal test?

A. Use the strongest practical evidence available and label the limits.

Examples:

- command output from build, lint, typecheck, or targeted scripts,
- focused unit or regression tests,
- smoke test steps and observed result,
- curl/API response checks,
- application logs that show the relevant behavior,
- screenshots or manual reproduction notes for UI work,
- docs diff showing the user-facing contract changed,
- explicit statement of what remains unverified.

Manual or log-based evidence can support a packet, but it is not a reason to
pretend the work is fully tested.

### Q. The next session keeps losing context.

A. Update `save-state.md` or create a handoff before ending the session.

Use `save-state.md` for current goal, state, next step, evidence, risks, and
owner decisions. Use `docs/sdad/handoffs/YYYY-MM-DD-topic.md` before closing or
restarting a long session.

### Q. The SPEC does not say what to do about an implementation detail.

A. Make the decision visible.

For normal implementation judgments, record the assumption, compromise,
rejected alternative, tradeoff, follow-up, and verification impact in
`docs/implementation-notes.md`. Use an ADR only for hard-to-reverse,
surprising, real-tradeoff decisions.

### Q. Review found a bug after the AI marked work evidence-ready.

A. Treat evidence-ready as reviewable, not owner-accepted.

Fix the finding in the same packet if it fits. Otherwise, move it to
`review-findings.md` or `docs/TODO-Open-Items.md` and define the next packet.

### Q. A chat-only tool says it installed SDAD.

A. Treat that as invalid unless the tool can edit the project filesystem.

Claude.ai, ChatGPT web, and browser-only chats can plan with SDAD, but they must
not claim adapter files were saved. Install from Codex, Claude Code, Cursor,
Copilot Chat, or another file-editing AI coding tool.

### Q. The task touches release, data, auth, money, security, or destructive work.

A. Do not solve it by raising autonomy alone.

Use Standard or Full SDAD with explicit gates. Keep owner approval for risk
acceptance, rollback posture, production claims, migration, destructive actions,
and real user data handling.

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
- [context-stability.md](context-stability.md): context layers and bounded reads
- [autonomy-levels.md](autonomy-levels.md): work packets and owner checkpoints
- [implementation-notes.md](implementation-notes.md): decision-log rules
- [session-handoff.md](session-handoff.md): long-session continuity
