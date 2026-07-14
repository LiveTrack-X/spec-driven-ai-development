# Evidence Matrix

Status: Active
Scope: Requirement, claim, and evidence mapping for the current project

Use this file when a project needs explicit traceability from requirements to
evidence. Keep it short enough to read as active state. Move raw logs, completed
history, and bulky evidence into archive or artifact locations, then link them
by evidence ID.

## Status Values

- `missing`: no evidence exists yet.
- `weak`: evidence exists but is incomplete, stale, partial, or too narrow.
- `software_only`: local software checks passed, but product/hardware claims are
  not proven.
- `simulator_verified`: simulator or fake-device checks passed.
- `tester_ready`: an artifact can be sent to a tester; evidence has not returned.
- `evidence_received`: evidence arrived but is not reviewed or accepted.
- `reviewed_pass`: evidence was reviewed and supports the scoped requirement.
- `reviewed_warn`: evidence supports part of the requirement with named limits.
- `reviewed_fail`: evidence contradicts the requirement or exposes a blocker.

Evidence status stops at review. Owner authorization and acceptance live in one
authoritative owner-decision record; this matrix may reference that record but
does not copy its mutable decision fields.

## Reproducibility Tiers

- `tier0_deterministic`: unit, golden, static, or reproducible local test.
- `tier1_simulator`: simulator, fake device, mock service, or virtual target.
- `tier2_local_hardware`: hardware verified on the developer's local setup.
- `tier3_remote_tester`: external tester, second machine, or remote device.
- `tier4_external_lab`: compatibility lab, platform, certification, or
  production-like environment.

## Freshness Rules

Define when evidence becomes stale:

| Evidence type | Fresh until | Revalidate when |
| --- | --- | --- |
| Unit or golden tests | Related code changes | Parser, protocol, or business rule changes |
| Simulator evidence | Simulator contract or target path changes | Simulator, adapter, or target behavior changes |
| Hardware evidence | Hardware path changes | Firmware, driver, device, OS, wiring, or transport changes |
| Package evidence | Artifact is regenerated | Packaging script, manifest, bundled file, or installer changes |
| External service evidence | External version or policy changes | API, SDK, platform, or service contract changes |

## Matrix

| ID | Requirement or claim | Required evidence | Current evidence | Evidence status | Tier | Scope | Freshness rule | Owner decision reference | Gaps / next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| EVID-001 | Example protocol rejects invalid packets | Unit tests and invalid fixtures | `cargo test -p protocol` | software_only | tier0_deterministic | Protocol only | Related parser changes | None | Hardware path not covered |
| EVID-002 | Example device enumerates on target OS | Remote support bundle and device log | None | missing | tier3_remote_tester | Target hardware | Firmware, OS, or driver changes | None | Send tester-ready package |

## Negative Results

Failed, missing, skipped, or contradicted evidence is still evidence.

| ID | Related requirement | Result | Evidence path | Impact | Action |
| --- | --- | --- | --- | --- | --- |
| NEG-001 | Example device enumerates on target OS | fail | `docs/evidence/quarantine/...` | Keep compatibility claim blocked | Inspect descriptor and retry |

## Completion Rules

- `software_only` cannot unlock hardware, compatibility, release, or production
  claims unless the claim registry explicitly allows that narrower scope.
- `evidence_received` is not done. It must pass import, privacy, lineage, and
  review checks before it can become `reviewed_pass`.
- `reviewed_pass` makes a requirement evidence-ready only for the stated scope.
- An owner decision must name accepted scope and unresolved gaps in its
  authoritative record; reference it here without copying the decision.
- Stale evidence must be downgraded or marked with a revalidation action.

## Owner Decision References

Use this table only as last-observed pointers. The referenced owner-decision
record remains authoritative and must be rechecked before reuse.

| Evidence ID | Claim or packet | Authoritative decision path / ID | Last observed status | Evidence scope / unresolved evidence gaps |
| --- | --- | --- | --- | --- |
| EVID-001 | Example software alpha claim | None | not_requested | Hardware evidence pending |
