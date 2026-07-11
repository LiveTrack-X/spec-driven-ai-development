# Minimal Example Agent Rules

Read progressively:

1. `sdad-state.yaml` for the active packet, gates, checks, and routed docs.
2. `docs/INDEX.md` for trigger-to-file routing.
3. Inspect current source/tests; current intent selects the path, heading, active section, or targeted match;
   routed membership does not require a full-file read.
4. The relevant heading in `docs/Repository-Operating-Rules.md` on demand.

Evidence beats confidence. Current source/tests beat stale history. Owner
decisions control scope, risk, irreversible actions, and acceptance. Keep
evidence-ready separate from owner-accepted and label partial, skipped,
degraded, or unverified behavior.

Use metadata-only inspection by default for private or secret-bearing inputs.
Do not read `.env` files, credentials, tokens, keys, or raw customer records
without task need plus owner-policy and tool-policy authorization.

Proceed inside the active packet until evidence-ready. Stop when scope or risk
changes, an irreversible action or owner tradeoff is required, verification is
blocked, or evidence conflicts with the plan.
