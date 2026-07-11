# Delivery Readiness Model

Status: Optional, on demand
Scope: product, hardware, release, or production claims that need readiness
evidence beyond the active execution declaration

Use this record only when an active claim needs it. `sdad-state.yaml` remains the
sole authority for current packet identity, objective, execution scope,
validation contract, owner-gate list, and current status. Link to state instead
of repeating those facts here.

## Readiness Evidence Lanes

Keep readiness claims distinct and attach bounded evidence:

| Lane | Evidence question | Example evidence |
| --- | --- | --- |
| Software evidence-ready | Did scoped local checks pass? | unit/integration results |
| Tester-ready | Is a named artifact plus procedure ready? | manifest and tester runbook |
| External evidence received | Was a returned bundle quarantined and reviewed? | lineage/privacy review |
| Hardware-verified | Does reviewed evidence support the named hardware claim? | target-device result |
| Release-candidate | Are declared build, package, migration, and rollback checks green? | release gate record |
| Production-ready | Did the applicable owner gate and production evidence complete? | authorization plus evidence |

Passing one lane does not imply another. Evidence-ready is not owner-accepted,
and owner acceptance cannot strengthen missing evidence.

## Conditional Owner Authorization

### AUTH-EXAMPLE

- Decision:
- Authorized action:
- Packet:
- Conditions:
- Expires when:
- Evidence required before action:

Reuse this authorization only while its packet, action, conditions, expiry,
evidence prerequisite, and recorded source remain unchanged. An expired or failed condition is a stop.
Keep currently unsatisfied gates in the simple
state `owner_gates` list; do not create a second registry here.

## Claim Limits

- Name the exact artifact, environment, hardware target, release lane, or
  production boundary covered.
- Link the evidence matrix, claim registry, artifact contract, or remote import
  review instead of copying their content.
- State skipped, partial, simulated, stale, and unverified evidence.
- Use precise readiness language; avoid an unqualified "done."

## Close Or Archive

Remove expired authorizations. When a readiness record no longer affects an
active claim, archive it with its evidence links rather than leaving it routed.
