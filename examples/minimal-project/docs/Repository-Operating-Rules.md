# Repository Operating Rules

Status: Active
Scope: durable policy loaded on demand

## Source Of Truth

Current code, tests, runtime state, and reproducible commands decide observed
behavior. Active docs and SPEC decide controlled future work. Handoff and chat
are continuity and hints, not authority.

## Core Rules

- Keep changes scoped to the active SPEC slice.
- Do not treat AI confidence as completion evidence.
- Keep active work, review findings, future ideas, and archives separate.
- Update docs when behavior or implementation status changes.
- Record spec-unstated durable choices before handoff.
- Label partial, skipped, degraded, or unverified behavior.
- Owner decision beats AI momentum.
- Match claim strength to the evidence tier actually obtained.
- Ask only the next blocking owner question after inspecting repository evidence.

## Owner Gates

Stop before release, migration, destructive action, real-data/auth/money/
security decisions, rollback, production claims, or another irreversible
owner-controlled action.
