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
- Source/artifact identity:
- Expires when:
- Evidence required before action:

Reuse this authorization only while its packet, action, conditions, expiry,
evidence prerequisite, and recorded source/artifact identity remain unchanged. An expired or failed condition is a stop.
Keep currently unsatisfied gates in the simple
state `owner_gates` list; do not create a second registry here.

## Terminal Packet Decision Record

Use an existing durable project decision surface when one exists. Before
replacing state for an `owner_accepted` or `production_ready` packet, ensure one
authoritative record binds the delivered result and its historical boundary.
If the project has no such surface, use this compact fallback:

### DEC-EXAMPLE

- Decision ID: DEC-EXAMPLE
- Decision: accepted | rejected | accepted with limits | revoked
- Revises/supersedes decisions:
  - None | path/URL/ID
- Decision claim scope:
- Packet:
- Active SPEC path and revision identity:
- Source/artifact identity:
- Evidence references and claim limits:
- Unresolved work and residual risk:
- Affected current-claim pointers:
- Owner or decision source:
- Decided at:

Evidence, claims, handoffs, and closure entries link this record by path, URL,
or ID. They do not copy its mutable decision fields. A later edit to the SPEC
path does not change the accepted historical boundary pinned here.
Never edit an old decision to express a later correction, restriction, or
revocation. Append a uniquely identified record, link the prior decision in
`Revises/supersedes decisions`, listing every direct predecessor once, and move each affected claim/evidence pointer to
the newest applicable record while retaining the prior pointer as history.
Decision lineage is acyclic and a record cannot revise itself. If parallel
records revise the same predecessor for overlapping claim scope, neither is
automatically current: hold the affected claim until an owner reconciliation
record lists and supersedes/retires every competing successor and the pointers
are updated. List order is descriptive; dates, filenames, and larger IDs cannot
choose the winner.

## Claim Limits

- Name the exact artifact, environment, hardware target, release lane, or
  production boundary covered.
- Link the evidence matrix, claim registry, artifact contract, or remote import
  review instead of copying their content.
- State skipped, partial, simulated, stale, and unverified evidence.
- Use precise readiness language; avoid an unqualified "done."

## Close Or Archive

An expired authorization is non-reusable. Remove it from the active routed view
but retain the immutable record in history with its evidence and decision
links. When any readiness record no longer affects an active claim, archive it
rather than deleting authority provenance.
