# Minimal Example Docs Index

Status: Active
Purpose: routing only

## Working Route

| Trigger | Read now | On demand |
| --- | --- | --- |
| Any packet | `../sdad-state.yaml`, current source/tests | one eligible route selected by intent |
| Implement/fix | `../SPEC/SPEC-COMPLETE.md`, `TODO-Open-Items.md`, `../review-findings.md` | rulebook heading |
| Policy/risk change | active SPEC | `Repository-Operating-Rules.md` |
| Handoff | state-declared current handoff | TODO/findings/SPEC when authority changes |

## Write Route

- behavior/scope/acceptance -> active SPEC;
- current work -> TODO;
- defect/risk/block -> review findings;
- durable policy -> operating rules;
- current execution -> state;
- cross-session recovery -> state-declared handoff.

## Source Of Truth

Current source/tests > active docs > canonical and active SPEC > continuity >
history > chat confidence. Owner decisions control scope, risk, and acceptance.

## Active Catalog

- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.

Route membership permits selection; it never requires a full-file read.
