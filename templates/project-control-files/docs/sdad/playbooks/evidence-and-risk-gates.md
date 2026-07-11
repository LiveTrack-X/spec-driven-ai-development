# Evidence And Risk Gates Playbook

Status: On demand
Trigger: owner-controlled risk, release, public claim, reference parity, product,
hardware, compatibility, package, remote tester, or production evidence

## Owner Gates

Release, production, migration, destructive action, real user data, auth, money,
security, rollback, and equivalent protected actions remain owner gates. Local,
reversible implementation may continue inside the declared packet, but stop
before the gated action, risk acceptance, or external publication.

Commit does not imply push; push does not imply release; release does not imply
deploy. Execution scope never substitutes for an owner gate.

## Conditional Owner Authorization

When a routed readiness record contains a conditional authorization, reuse it
only while the packet, action, conditions, expiry, evidence prerequisite, and
recorded source remain unchanged. An expired or failed condition is a stop.
Do not copy the authorization into state or invent a gate registry.

## Fresh-Context Review

For a protected-action change, release candidate, migration, destructive action,
security boundary, or public effectiveness claim, request a fresh context,
implementation-independent review when an isolated pass is available. Review the final diff,
acceptance criteria, validation evidence, open findings, and residual risk.
This is review evidence, not owner acceptance.

## Evidence Tiers

Match each claim to the strongest evidence actually obtained:

1. static inspection or local unit test;
2. local integration or rendered artifact;
3. live runtime or persisted-state observation;
4. installed/package smoke outside the source tree;
5. remote hardware, external lab, or representative environment;
6. production observation under an approved policy.

A lower tier cannot unlock a higher-tier claim. Mark skipped, partial, degraded,
simulated, stale, and unverified evidence explicitly.

## Optional Product Evidence

Create these files only on demand when an active claim needs the boundary:

- `docs/evidence-matrix.md`: claim-to-evidence status;
- `docs/claim-registry.md`: allowed, qualified, and blocked claims;
- `docs/artifact-contracts.md`: required package or report contents;
- `docs/work-packet-state.md`: optional Delivery Readiness Model and conditional
  authorization record;
- `docs/remote-evidence-import.md`: quarantine and review of external bundles.

The readiness record does not own the active packet identity, objective,
execution scope, validation contract, owner-gate list, or current status.

## Reference Parity

For reference-derived behavior, map source behavior to implemented behavior,
evidence, and every gap or deferred claim. Parity review is a claim audit, not
permission to copy the reference implementation.

## Release And Claim Boundaries

State the active release lane, artifact identity, migration/rollback checks,
and owner gate. Validate source, generated package, installed artifact, and
public release separately when those are separate claims.

Doctor green proves structural consistency. A task benchmark proves that task.
Only a controlled comparison supports an improvement claim. Owner acceptance
never upgrades weak evidence.
