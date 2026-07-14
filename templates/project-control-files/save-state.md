# Legacy Save State

Status: State-v1 migration input only
Last updated: YYYY-MM-DD

This file remains available so an existing state-v1 project can be understood
during migration. It is not current state-v2 authority or a default route.
Do not delete it and do not auto-migrate it; preserve project-specific continuity
until the owner-approved migration procedure classifies it.

The remaining sections describe the legacy state-v1 recovery shape.

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

Save-state-only decisions are continuity hints. Before using one as authority,
route scope, behavior, and acceptance-criteria changes to the active SPEC;
durable architectural rationale to an ADR; claim/evidence status to its ledger;
unresolved work to TODO/findings; and owner authorization or result acceptance
to one durable owner-decision record. Leave only pointers here.

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

## Implementation Notes

List spec-unstated assumptions, changes, compromises, rejected alternatives,
owner-relevant tradeoffs, follow-up, or verification-impact notes needed for the
next session. If the project uses `docs/implementation-notes.md`, link to the
current entry instead of duplicating it.

## Open Risks Or Unverified Items

List known blockers, partial work, skipped checks, or uncertain behavior.

## Owner Decision Needed

List any decision that should not be made by the AI alone.
