# Minimal Example Docs Index

Status: Active
Purpose: routing only

## Working Route

| Trigger | Read now | On demand |
| --- | --- | --- |
| Any packet | `../sdad-state.yaml`, current source/tests | current handoff if present |
| Implement/fix | `../SPEC/SPEC-COMPLETE.md`, `TODO-Open-Items.md`, `../review-findings.md` | rulebook heading |
| Policy/risk change | active SPEC | `Repository-Operating-Rules.md` |
| Handoff | current state, TODO, findings | save-state/handoff if present |

## Write Route

- behavior/scope/acceptance -> active SPEC;
- current work -> TODO;
- defect/risk/block -> review findings;
- durable policy -> operating rules;
- continuity only -> state or handoff.

## Source Of Truth

Current source/tests > active docs > canonical and active SPEC > continuity >
history > chat confidence. Owner decisions control scope, risk, and acceptance.
