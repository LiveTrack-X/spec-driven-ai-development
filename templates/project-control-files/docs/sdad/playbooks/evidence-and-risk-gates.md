# Evidence And Risk Gates Playbook

Status: On demand
Trigger: Q5 risk, release, public claim, reference parity, product, hardware,
compatibility, package, remote tester, or production evidence

## Q5 Owner Gates

Q5 includes release, production, migration, destructive action, real user data,
auth, money, security, rollback, and equivalent owner-controlled risk. Any Q5
yes is Standard minimum when the packet only inspects, documents, or tests the
area. Use Full when the current packet changes, accepts, or executes a Q5 gate,
including its boundary, policy, evidence claim, accepted risk, or external
action.

Level 4 means implementation may proceed inside the approved packet, but the
AI must stop before the gated action or owner acceptance. Commit does not imply
push; push does not imply release; release does not imply deploy.

## Evidence Tiers

Match claims to the strongest evidence actually obtained:

1. static inspection or local unit test,
2. local integration or rendered artifact,
3. live runtime or persisted-state observation,
4. installed/package smoke outside the source tree,
5. remote hardware, external lab, or representative environment,
6. production observation under an approved policy.

A lower tier cannot unlock a higher-tier claim. Passing tests do not prove
hardware behavior, package contents, production safety, or owner acceptance.
Mark skipped, partial, degraded, simulated, and unverified evidence explicitly.

## Product Evidence Files

Create only the files needed by an active claim:

- `docs/evidence-matrix.md`: claim-to-evidence status;
- `docs/claim-registry.md`: allowed, qualified, and blocked claims;
- `docs/artifact-contracts.md`: required package or report contents;
- `docs/work-packet-state.md`: AI-complete through production-ready states;
- `docs/remote-evidence-import.md`: quarantine and review of external bundles.

Keep evidence-ready, tester-ready, hardware-verified, release-candidate, and
owner-accepted states separate.

## Reference Parity

When behavior is derived from another product, repository, design, demo, or
field project, map source behavior to implemented behavior, evidence, and every
gap or deferred claim. Reference parity is a claim audit, not permission to copy
the reference implementation.

## Release And Version Lanes

When stable and next-version work coexist, state the active lane, forward-port
or backport policy, artifact identity, migration/rollback checks, and release
owner gate. Validate source, generated package, installed artifact, and public
release separately when those are separate claims.

Before evidence-ready, check unfinished packets, generated or cache files,
artifact manifests, version surfaces, and installed-artifact smoke from outside
the source tree. Owner acceptance never upgrades weak evidence.
