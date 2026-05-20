# Project Name

One paragraph explaining what this project is and who it is for.

## Development Workflow

This project uses owner-supervised, SPEC-driven AI development.

- The owner controls direction and final acceptance.
- AI agents help plan, specify, implement, review, and verify.
- Completion requires evidence: code, tests, docs, and reproducible commands.
- Work happens in bounded work packets, not micro-approval steps.
- AI-complete means evidence-ready; owner-accepted is a separate checkpoint.
- Spec-unstated implementation decisions go in `docs/implementation-notes.md`,
  not only in chat.

## Start Here

Read:

1. `AGENTS.md`
2. `docs/INDEX.md`
3. `SPEC/SPEC-COMPLETE.md`
4. `docs/TODO-Open-Items.md`
5. `review-findings.md`
6. `docs/implementation-notes.md` when the work may depend on spec-unstated
   implementation decisions

Use `save-state.md` only when work pauses, changes hands, direction changes, or
the next session would otherwise need to reconstruct context.

Keep active state files short. Use bounded reads for large archives, logs,
generated artifacts, private data, and old handoffs instead of loading them in
full.
