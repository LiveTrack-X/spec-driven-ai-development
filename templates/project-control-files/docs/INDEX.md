# Documentation Control Center

Status: Active
Scope: Central documentation navigation and maintenance control

## Start Here

- `README.md`: human-facing overview
- `SPEC/SPEC-COMPLETE.md`: canonical product and implementation baseline
- `docs/TODO-Open-Items.md`: current open implementation work
- `review-findings.md`: active bug and review backlog

## Document Classes

- Active runtime docs live under `docs/`
- Active or planned SPECs live under `SPEC/`
- Historical docs live under `docs/archive/`
- Product notes live under `docs/product-notes/` and are references until promoted into active SPEC

## Maintenance Rules

1. Every active document must be reachable from this file.
2. Code changes require a documentation consistency check.
3. Completed plans move to archive.
4. Product notes do not become implementation requirements until promoted.
5. When docs conflict, prefer code, tests, active docs, canonical SPEC, active SPECs, then archive/history.
