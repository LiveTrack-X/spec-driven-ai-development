# Review Findings

Status: Active
Scope: Active bugs and review findings only

## Active Findings

None currently tracked.

Do not leave closed findings in this section. Move fixed or accepted items to
`## Recently Closed` before an evidence checkpoint or handoff.

## Future / Deferred Findings

Use this only for unresolved findings owned by a noncurrent split parent or
inactive sibling packet. Preserve the original finding text and any ID,
severity, packet marker, and evidence link; add the split-decision link, defer
reason, and explicit revisit trigger. This is not closure. When that packet
becomes current, move its intact finding back to `## Active Findings` before
work or acceptance; do not keep two copies.

## Severity Gate

- Critical findings block release or production readiness.
- High-risk domain findings block the affected slice until reviewed and tested.
- Release candidates should reach Critical 0 before owner acceptance.

## Recently Closed

- Record fixed blockers with packet, resolution kind, and evidence or an
  authoritative owner decision. Moving an unresolved finding here is not closure;
  `[packet:bootstrap]` alone is insufficient.
- Move old closed history to archive when it stops affecting current decisions.

## Guardrails

Stop feature work if critical tests fail, security boundaries regress, or production-readiness evidence is missing.
