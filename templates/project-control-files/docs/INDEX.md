# Documentation Control Center

Status: Active
Scope: Central documentation navigation and maintenance control

## Start Here

- `README.md`: human-facing overview
- `docs/Repository-Operating-Rules.md`: mandatory repository rulebook
- `SPEC/SPEC-COMPLETE.md`: canonical product and implementation baseline
- `docs/TODO-Open-Items.md`: current open implementation work
- `review-findings.md`: active bug and review backlog

## Document Classes

- Active runtime docs live under `docs/`
- Active or planned SPECs live under `SPEC/`
- Architecture decision records live under `SPEC/adr/`
- Historical docs live under `docs/archive/`
- Product notes live under `docs/product-notes/` and are references until promoted into active SPEC
- Implicit operating rules should be promoted into `docs/Repository-Operating-Rules.md`
  instead of left only in chat.

## Maintenance Rules

1. Every active document must be reachable from this file.
2. Code changes require a documentation consistency check.
3. Completed plans move to archive.
4. Product notes do not become implementation requirements until promoted.
5. When docs conflict, prefer code, tests, active docs, canonical SPEC, active SPECs, then archive/history.
6. When a SPEC spans past-to-present history, current active sections override older sections.

## Minimum Documentation Update Sets

Use this table before handoff.

| Change type | Minimum docs to check or update |
| --- | --- |
| User-facing behavior or workflow | `README.md`, relevant user docs, `SPEC/SPEC-COMPLETE.md` |
| Configuration, startup, deployment, or CLI | `README.md`, relevant runtime docs, `SPEC/SPEC-COMPLETE.md` |
| Security, identity, permissions, data boundaries, or destructive action | security docs if present, relevant SPEC, `review-findings.md` if risk remains |
| Background jobs, workers, lifecycle, retries, or maintenance | runtime docs, `docs/TODO-Open-Items.md` if gap status changes |
| Prompt behavior or AI/tool contract | prompt docs, relevant SPEC, tests if present |
| Roadmap, implementation status, placeholder, or gap closure | `SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, `review-findings.md` if review-related |
| Stable/next version lane, migration, release, or rollback | release docs if present, `docs/Repository-Operating-Rules.md`, relevant SPEC |
| High-risk domain rule such as locks, real-time path, backup, or platform boundary | module docs if present, `docs/Repository-Operating-Rules.md`, relevant tests |
| Durable architecture, policy, release, or owner tradeoff decision | `SPEC/adr/ADR-0001-template.md` copied to a numbered ADR, relevant SPEC/docs |

If no document needs a content change, handoff must state which docs were
checked and why no update was needed.
