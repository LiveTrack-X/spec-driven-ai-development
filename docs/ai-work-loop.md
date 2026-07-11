# AI Work Loop

Use one loop for SDAD Protocol work:

```text
Plan -> Route -> Implement -> Verify -> Report
                       |                 |
                       +-> Owner Gate    +-> Handoff, when needed
```

Owner gates and handoffs are triggered branches, not mandatory phases. Use the
smallest loop that preserves the validation contract and owner control.

## Plan

Normalize the request into one executable boundary:

- outcome or objective,
- authority or reference,
- allowed scope and constraints,
- validation and required evidence,
- owner gates and stop conditions,
- report format.

Infer and report scale, execution scope, claim boundary, owner gates, and the
assumptions behind them from the request and repository first. Ask at most one
blocking question only when an unresolved fact would change the scale or an
owner gate. Recommend a default with the question; otherwise proceed with the
explicit assumptions.

## Route

For a stateful project, read:

```text
adapter -> sdad-state.yaml -> docs/INDEX.md
```

Then select only the source, test, path, heading, active section, or targeted
match needed for the current intent. `routed_docs` is an eligible selection set,
not a read-all list. Report the routed documents actually read.

## Implement

Work within `execution_scope: unit | packet`. A unit is one review-worthy
change slice. A packet may contain related units and is the default Standard and
Full boundary. Do not pause for micro-approval inside an authorized boundary.

Give each fact one authoritative home:

| Fact | Authority |
|---|---|
| Requirement or acceptance change | SPEC |
| Small non-spec implementation decision | implementation notes |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or finding |
| Cross-session recovery links/results | handoff |
| Current execution state | `sdad-state.yaml` |

## Verify

Bind validation to the packet before implementation. For state v2,
`validation_for` must equal `active_packet.id`. Run the named checks and retain
bounded evidence, limits, and unverified areas.

Evidence-ready is not owner-accepted. Doctor green proves structural
consistency only. A successful task benchmark proves that task only. An
improvement claim requires a controlled comparison.

## Report

Report findings first, then:

- interpreted intent and active boundary,
- changed files or artifacts,
- validation evidence,
- limits and unverified areas,
- documents actually read or updated,
- owner decision or acceptance needed,
- next action.

If a current packet-bound handoff is needed, create it and set
`current_handoff`. Link to authorities rather than copying their content. Clear
or replace the pointer when it is no longer current.

## Owner Gate

Stop before protected actions such as release, migration, destructive changes,
production impact, sensitive-data access, auth, money, security, or risk
acceptance unless a valid owner authorization covers the action.

Record a reusable conditional authorization with:

```text
Decision:
Authorized action:
Packet:
Conditions:
Expires when:
Evidence required before action:
```

Reuse it only while the action, packet, conditions, source, and expiry remain
unchanged. A changed term or expired condition requires a new owner decision.

Markdown guidance and decisions do not technically prevent tools from acting.
Permissions, hooks, sandboxes, protected branches, and service controls provide
enforcement.
