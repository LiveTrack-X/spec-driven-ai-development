# Work Packets Playbook

Status: On demand
Trigger: scale, execution-scope, packet, delegation, planning, or implementation
decision

## One Work Loop

Use one loop: Plan -> Route -> Implement -> Verify -> Report. An owner gate or
handoff is a triggered branch, not another loop. Keep iteration bounded inside
the selected unit or packet.

## Scale And Execution Scope

Use the smallest persistent control surface that protects the work:

- One-shot: the current request only; no persistent state is implied.
- Mini: one bounded unit.
- Standard: one executable packet.
- Full: one executable packet plus every applicable owner gate.

Standard is suitable for work that inspects, documents, or tests a protected
area without taking the protected action. Full is suitable when the packet
changes, accepts, or executes a release, production, migration, destructive, data, auth,
money, security, rollback, or equivalent owner-controlled boundary.

State v2 execution scope is `unit` or `packet`. It controls the current work
boundary, not risk acceptance. Multi-packet execution requires an explicitly
approved packet plan or list. Infer scale and gates from the request and
repository first; ask at most one unresolved question when its answer changes
scale or an owner gate.

## Packet And Delegation Envelope

Every packet or delegated assignment records:

- the desired outcome or objective and its acceptance boundary;
- authority and reference paths;
- constraints, allowed scope and non-goals;
- validation commands and the claims each check supports;
- expected evidence, required evidence, and claim limits;
- owner gates and stop conditions;
- the required report, including residual risk and unverified work.

A review-worthy unit is an internal slice large enough to review and small
enough to verify. Delegated workers receive the full envelope because they may
not inherit parent context. Continue inside the declared boundary until an
evidence checkpoint unless a stop condition fires.

## Packet Switch Transaction

Treat a packet switch as one coherence transaction:

1. Select next leaf packet and outcome without changing live state.
2. Classify old active records: move closed history, defer future work, and
   relink deliberately carried work to the selected packet.
3. Review validation entries; remove stale checks, revise claim text, and add
   the smallest task-specific check.
4. Update state as one bundle: date, SPEC, packet identity/objective/status,
   `validation_for`, gates, validation, and eligible routes.
5. Remove or replace the old `current_handoff`; never carry it across
   mechanically.
6. Run Doctor strict on the coherent declaration and active ledgers.
7. Run project checks separately and record their bounded evidence.
8. Advance status only after the required evidence exists.
9. Rerun Doctor because status-sensitive severity may have changed.

## Implementation Memory

Record a small spec-unstated implementation decision in
`docs/implementation-notes.md`. Use an ADR only for a hard-to-reverse,
surprising architectural tradeoff. Put unresolved work in TODO or findings,
not in the handoff.

## Bounded Feedback Loop

For non-trivial work, use `inspect -> act -> observe -> update -> retry or stop`.
Set bounded attempts and do not repeat a failed action without new evidence, a
changed hypothesis, or an explicit remaining retry budget. Tiny work may keep
the same behavior inside the Fast Loop without a separate planning artifact.

## Stop Conditions

Stop for owner input when scope expands, a claim or owner gate changes, an
irreversible or external action is required, an owner-controlled tradeoff
remains, verification is blocked, or evidence conflicts with the plan.
