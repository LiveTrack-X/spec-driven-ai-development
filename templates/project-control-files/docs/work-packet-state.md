# Work Packet State Model

Status: Active
Scope: Standard state names for work packets, review-worthy units, evidence, and
owner acceptance

Use this file to prevent "done" from collapsing implementation, verification,
tester readiness, evidence import, hardware validation, owner acceptance, and
production readiness into one ambiguous state.

## Packet States

Packet states are separate from evidence matrix statuses. For example,
`hardware_evidence_received` at the packet level usually corresponds to
`evidence_received` in `docs/evidence-matrix.md`, and it still requires
quarantine/import/review before any claim changes.

Do not set `owner_accepted` until an owner checkpoint accepts the named scope.
If evidence is ready but owner acceptance is pending, use the strongest verified
pre-owner state such as `software_verified`, `hardware_verified`, or
`release_candidate` and write "owner acceptance pending" in the summary.

| State | Meaning | May continue without owner? | May claim done? | Typical next action |
| --- | --- | --- | --- | --- |
| `not_started` | Packet is defined but work has not begun. | Yes, if packet is approved | No | Start implementation |
| `in_progress` | Work is underway inside approved scope. | Yes | No | Continue until evidence-ready or stop condition |
| `ai_complete` | AI finished edits or draft output. | Yes, for checks/docs inside scope | No | Run checks and update evidence |
| `software_verified` | Local software checks passed for scoped behavior. | Yes, if no owner gate changed | No for product/hardware claims | Prepare artifact or request review |
| `tester_ready` | Artifact and instructions are ready for tester/lab. | Yes, for docs/tooling | No | Send artifact or wait for tester |
| `hardware_evidence_received` | Remote or hardware evidence arrived. | No claim change yet | No | Quarantine/import/review evidence |
| `hardware_verified` | Evidence was reviewed and supports scoped hardware/product claim. | Maybe, if packet allows | Evidence-ready only | Owner checkpoint |
| `owner_accepted` | Owner accepted a named scope. | Yes, for next approved packet | Yes for accepted scope | Archive/advance |
| `release_candidate` | Release bundle is candidate-ready with known gates. | Only within release prep | No production claim | Release review |
| `production_ready` | Production/release gate passed with owner acceptance. | No, owner gate required | Yes for accepted scope | Release or deploy |
| `blocked` | Stop condition or missing dependency prevents progress. | No | No | Ask owner or record finding |
| `deferred` | Work intentionally moved out of active scope. | Yes, on other scope | No | Track in TODO/backlog |

## Work Packet Template

```yaml
id: WP-001
name: Remote hardware validation
status: tester_ready
sdad_scale_intensity: Full SDAD / Medium
autonomy_level: Level 2 with Level 4 claim gates
owner_gate: true
allowed_scope:
  - package verifier
  - tester instructions
  - support bundle import
non_goals:
  - production release
  - compatibility claim upgrade
requirements:
  - real target hardware evidence
  - package manifest evidence
evidence:
  - EVID-002
artifacts:
  - ART-001
claims:
  - CLAIM-001
blocked_by:
  - external tester hardware
continue_allowed:
  - docs
  - tooling
  - verifier hardening
must_stop_for:
  - production claim
  - compatibility claim upgrade
  - destructive migration
next_action:
  - send tester-ready package
  - import returned bundle through quarantine
```

## Completion Language

Use precise status language:

- "AI edits complete; verification pending."
- "Software evidence-ready; hardware pending."
- "Tester-ready; remote evidence not received."
- "Remote evidence received; import review pending."
- "Hardware verified for stated scope; owner acceptance pending."
- "Owner-accepted for stated scope; unresolved gaps remain."

Avoid unqualified "done" unless owner acceptance or delegated acceptance policy
is visible.

## Stop / Continue Rule

Continue inside the approved packet for:

- docs and control-file sync,
- verifier, import, packaging, or support tooling,
- local software checks,
- evidence matrix updates that do not upgrade blocked claims,
- artifact contract cleanup,
- review summary preparation.

Stop for owner input when:

- scope expands,
- release, production, compatibility, hardware, data, auth, money, security,
  destructive-action, rollback, or other Q5 gates change,
- a claim would be upgraded,
- hardware SKU, target platform, or acceptance scope is an owner decision,
- verification is blocked or contradicts the plan,
- imported evidence fails privacy, lineage, or sufficiency checks.
