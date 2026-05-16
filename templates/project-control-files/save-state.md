# Save State

Status: Active handoff
Last updated: YYYY-MM-DD

Use this file only when current context would be expensive to reconstruct from
code, active docs, SPEC, TODO, and review findings.

## Context Stability Rule

Keep this file as a compact current-state summary, not a permanent session log.

If the file becomes long, repetitive, or hard to audit, move old material to an
archive/history file, link it here, and keep this active file focused on current
goal, current state, validation, open risks, owner decisions, and the next one to
three steps.

Fresh AI sessions should use bounded reads for archives, logs, generated
artifacts, private data, and old handoffs instead of loading them in full.
Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

## Update Triggers

Update this file when:

- a session is ending or pausing before work is fully accepted,
- an active slice completes and the next slice is not obvious from TODO/SPEC,
- the owner changes direction, priority, acceptance criteria, or risk tolerance,
- work is blocked, skipped, partial, degraded, or unverified,
- another AI tool, model, session, or person is expected to continue the work,
- current context would be expensive to reconstruct from code and docs alone.

If none of these triggers apply, this file does not need a content change.

## Current Goal

What is the active goal right now?

## Current State

What changed, what was checked, and what remains unresolved?

## Next Recommended Step

What should the next session do first?

## Evidence

List commands, tests, logs, screenshots, manual checks, or review evidence.

## Open Risks Or Unverified Items

List known blockers, partial work, skipped checks, or uncertain behavior.

## Owner Decision Needed

List any decision that should not be made by the AI alone.
