# Session Handoff & Context Continuity

Status: Active reference
Scope: Tool-agnostic continuity rules for long AI coding sessions

This is an SDAD continuity rule, not a productivity shortcut. The purpose is to
prevent context collapse, stale assumptions, and unverifiable AI continuation.

Long AI coding sessions must not be treated as permanent memory.

In SDAD, the durable source of truth is the specification, not the chat
transcript. A chat session is an execution trace: useful while work is active,
but unreliable as the only continuity mechanism once the session grows long,
changes direction, or is restarted.

SDAD should preserve continuity through explicit handoff documents.

## Operating Model

- Chats are execution traces.
- Specs are authority.
- Handoffs are continuity.
- Archives are history.
- Fresh sessions are for reliable execution.

Before closing, archiving, replacing, or restarting a long AI session, the AI
must create a session handoff document.

The handoff must be written so that a fresh AI session can continue the work
without depending on the previous chat context.

## When To Create A Handoff

Create a handoff when any of the following is true:

- the session has become long or difficult to audit,
- the AI has touched multiple files or subsystems,
- the task is paused and may resume later,
- the owner wants to restart in a fresh session,
- the implementation is incomplete,
- tests are failing or unverified,
- important decisions were made during the session,
- there are known constraints or do-not-touch areas.

When asked to restart, summarize, archive, or continue later, the AI must offer
to create or update a handoff first.

## Handoff Requirements

A valid SDAD handoff must include:

- project or repository name,
- branch or working context,
- current objective,
- completed work,
- decisions made and why,
- files touched or investigated,
- commands or tests run and results,
- known failures, warnings, or unverified assumptions,
- open decisions,
- constraints, owner preferences, and do-not-touch areas,
- next concrete steps,
- a reactivation prompt for a fresh AI session.

## Storage Location

For Standard and Full SDAD projects, store session handoffs under:

```text
docs/sdad/handoffs/YYYY-MM-DD-topic.md
```

Mini SDAD may use its normal one-file handoff unless the project has grown large
enough to need Standard SDAD continuity.

## Standard Handoff Template

````md
# SDAD Session Handoff

## 1. Session Identity
- Project:
- Repository:
- Branch / working context:
- Date:
- AI tool/model:
- Human supervisor:

## 2. Current Objective
- Primary objective:
- Non-goals:

## 3. Completed Work
-
-
-

## 4. Decisions Made
| Decision | Reason | Alternatives Rejected |
|---|---|---|
| | | |

## 5. Files Touched or Investigated
| File/Path | Change Type | Reason | Risk/Notes |
|---|---|---|---|
| | | | |

## 6. Commands / Tests Run
| Command | Result | Notes |
|---|---|---|
| | | |

## 7. Current State
- Working:
- Broken:
- Unverified:
- Unknown:

## 8. Constraints and Do-Not-Touch Areas
-
-
-

## 9. Open Decisions
-
-
-

## 10. Next Concrete Steps
1.
2.
3.

## 11. Reactivation Prompt

Paste this into a fresh AI session:

```text
You are continuing an SDAD-guided project from a handoff document.

First, read this handoff fully.
Then inspect the current repository state before making changes.
Do not assume the previous chat context is available.
Treat the project specification as the source of authority.
Confirm the current objective, constraints, files touched, test status, and next steps.
Before modifying files, produce a short implementation plan.
```
````

## Resuming From A Handoff

The AI must not rely on the previous chat as the only memory source when
resuming work. It should load the relevant spec, handoff, and current repository
state before continuing.
