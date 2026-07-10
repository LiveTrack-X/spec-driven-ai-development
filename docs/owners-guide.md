# Owner Quick Adoption Guide

Use this guide when you are the owner introducing SDAD to users, teammates, or
AI coding sessions and you want them productive quickly without teaching the
whole framework first.

The owner's job is not to memorize SDAD terms. The owner's job is to keep
direction, risk, evidence, and final acceptance visible.

## 10-Minute Rollout

1. Pick the smallest safe scale.
2. Give the AI one clear packet, not the whole dream.
3. Require evidence-ready output before accepting anything as done.
4. Keep owner gates for release, data, auth, money, security, destructive work,
   rollback, migration, and production claims.
5. Turn repeated confusion into a rule, TODO, review finding, or handoff.

## Which Link To Send First

| Audience | Send this | Why |
|---|---|---|
| New owner | [Owner Guide](owners-guide.md) | Fast adoption and owner checkpoints |
| AI agent during active work | [AI Work Loop](ai-work-loop.md) | Fast/Normal/Full execution loop |
| New user who wants explanation | [User Guide](user-guide.md) | Situation-based FAQ |
| User who wants to start immediately | [README Copy-Paste Start Prompt](../README.md#copy-paste-start-prompt) | Works in AI coding tools |
| No clone / chat-only user | [No-Clone Quick Install](no-clone-quick-install.md) | Starts without installing the repo |
| Tool setup user | [Getting Started](getting-started.md) | Adapter and skill install paths |

Do not send the full pattern catalog as the first link. Use it when a specific
pattern question appears.

## Owner Decisions That Must Stay Explicit

The owner controls:

- current product direction,
- accepted scope and non-goals,
- risk tolerance,
- release or production decisions,
- user data, auth, money, security, destructive action, migration, and rollback
  decisions,
- final owner acceptance.

The AI can prepare work and evidence inside an approved packet. It cannot turn
weak evidence into owner acceptance.

## First Prompt For A New User

```text
Use SPEC-Driven AI Development for this project.

Start with the smallest safe scale. Do not create the full SDAD structure unless
the project needs it.

First tell me:
- interpreted intent,
- chosen scale: One-shot, Mini, Standard, or Full,
- autonomy level,
- expected evidence,
- owner gates.

Then create or update only the files needed for this scale.
For Standard or Full, keep the default path compact: adapter ->
sdad-state.yaml -> docs/INDEX.md -> current source/tests -> one routed file or
playbook. Do not load the full rulebook or optional evidence set by default.
```

## First Prompt For Actual Work

```text
Work inside this approved packet:

Goal:
[one user-visible outcome]

Non-goals:
[what not to change]

Evidence required:
[test, browser check, runtime check, persisted state, remote evidence, or
production evidence]

Owner gates:
[release, data, auth, money, security, destructive action, migration, rollback,
or none]

Proceed until evidence-ready or until a real owner decision is required.
```

## What To Ask At The Checkpoint

Ask for this short evidence-ready summary:

```text
Report evidence-ready status.

Include:
- changed files,
- behavior changed,
- checks run and results,
- evidence tier,
- docs updated or checked,
- limitations or unverified behavior,
- owner decision needed,
- whether this is evidence-ready or owner-accepted.
```

If the AI cannot show evidence, the work is not evidence-ready.

## Fast Scale Rules

| Situation | Use | Owner stance |
|---|---|---|
| Disposable question or tiny edit | One-shot | No project files |
| Small task that needs proof | Mini SDAD | One instruction file or one evidence-ready summary |
| Multi-session work or reviewers | Standard SDAD | SPEC, TODO, review, and current docs stay readable |
| Release, production, user data, auth, money, security, migration, rollback, or destructive risk | Full SDAD or explicit Level 4 gates | Owner keeps risk acceptance and release decisions |

Choose smaller when it still protects evidence and owner gates. Choose larger
only when risk, continuity, or review needs it.

## Low-Friction Owner Rules

- Approve the packet boundary, not every micro-task.
- Ask for one blocking question with a recommended answer, not a menu.
- Treat "fully" as evidence-ready for the approved scope, not owner-accepted.
- Treat "commit and wait" as commit only, not push, release, or deploy.
- Do not let side quests silently become scope.
- Do not let active docs become history dumps.
- Archive old evidence; keep active state current.

## Adoption Health Check

After the first day or first packet, check:

- Can a new AI session find the current packet without chat history?
- Can the owner tell what is done, blocked, unverified, and accepted?
- Are active docs short enough to read?
- Did any repeated confusion become a rule or TODO?
- Did evidence match the claim being made?

If the answer is no, improve the routing or evidence boundary before adding more
templates.

## Common Failure Signals

| Signal | Owner response |
|---|---|
| AI asks approval after every tiny edit | Use Level 2 Work Packet Autonomy |
| AI says done without checks | Ask for evidence-ready status |
| AI reads huge history first | Ask for current context route and bounded reads |
| Docs become longer than the work | Apply Small Project Compression |
| Release or production claim appears | Require Level 4 owner gate and matching evidence tier |
| Existing product behavior is being rebuilt | Require Reference Parity Review before evidence-ready |

## The Minimum Owner Habit

For every meaningful packet, ask:

```text
What changed, what proves it, what is still unverified, and what decision do I
need to make?
```

That one question preserves the SDAD boundary: AI can write code, but evidence
decides completion and the owner decides acceptance.
