# Operating Intensity: SDAD 3.1 Migration Note

Operating intensity is legacy state-v1 vocabulary. New state-v2 projects do
not use `High`, `Medium`, or `Low`, and they do not contain an `intensity` key.

Use the current controls instead:

- Scale selects the persistent control surface.
- `execution_scope: unit | packet` selects the current work boundary.
- Owner gates protect release, production, migration, destructive action,
  sensitive data, auth, money, security, rollback, and risk acceptance.
- The validation contract states what will be checked and what the evidence can
  support.

## Migrating From SDAD 3.1

Preserve legacy `intensity` and numeric `autonomy` exactly while a project is
still state v1. Before changing an existing project, show a read-only migration
preview. Do not translate intensity mechanically into more authority:

- legacy Low/Medium/High may inform the proposed validation depth,
- `unit` or `packet` must be chosen as the v2 execution boundary,
- every protected action still needs its applicable owner gate,
- the owner can reject or revise the preview before writes.

After a v2 migration, use the one loop in [ai-work-loop.md](ai-work-loop.md) and
record any remaining historical terms only in migration history.
