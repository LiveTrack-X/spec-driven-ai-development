# Product Evidence Templates

Status: Active reference

These optional Standard/Full templates support product, hardware, external
tester, package, release, production, and compatibility claims that local source
checks cannot establish. Install only the records the active claim can maintain.

## Template Set

- **Evidence Matrix**:
  [`docs/evidence-matrix.md`](../templates/project-control-files/docs/evidence-matrix.md)
  maps requirements and claims to evidence, scope, freshness, and gaps.
- **Claim Registry**:
  [`docs/claim-registry.md`](../templates/project-control-files/docs/claim-registry.md)
  records allowed, qualified, blocked, and forbidden claims.
- **Artifact Contract**:
  [`docs/artifact-contracts.md`](../templates/project-control-files/docs/artifact-contracts.md)
  defines required files, metadata, verifier commands, lineage, privacy, and
  retention for packages and evidence bundles.
- **Delivery Readiness Model**:
  [`docs/work-packet-state.md`](../templates/project-control-files/docs/work-packet-state.md)
  distinguishes software evidence, tester readiness, external evidence,
  hardware verification, release candidacy, and production readiness.
- **Remote Evidence Import / Quarantine Pattern**:
  [`docs/remote-evidence-import.md`](../templates/project-control-files/docs/remote-evidence-import.md)
  keeps external evidence quarantined until structure, privacy, lineage, scope,
  and review checks pass.

The `docs/work-packet-state.md` path is retained in 3.2 for compatibility. Its
title and role are Delivery Readiness Model. It is not current packet authority;
`sdad-state.yaml` remains authoritative for active packet identity, execution
scope, validation contract, owner gates, and status.

## When To Use

Use a relevant template when:

- a local software check cannot prove the claim;
- hardware, firmware, compatibility, packaging, or deployment matters;
- evidence arrives from another machine, tester, user, lab, or platform;
- generated artifacts need commit/build/verifier lineage;
- README, UI, release notes, manifests, or support text could overclaim;
- active TODO or finding files are carrying completed evidence history.

This is a product-evidence trigger, not a new scale. Use Standard when persistent
packet state is needed. Use Full when the same persistent surface also needs
protected-action owner gates. Scale does not grant authorization.

## Required Separation

Keep readiness lanes, evidence statuses, and owner acceptance separate:

- **Software evidence-ready**: scoped local commands support the stated claim.
- **Tester-ready**: the named artifact and procedure are ready to send.
- **External evidence received**: a bundle arrived but may still be quarantined.
- **Hardware-verified**: reviewed evidence supports the named hardware scope.
- **Release-candidate**: declared package, migration, and rollback checks passed.
- **Production-ready**: the applicable production evidence and owner gate passed.

Evidence Matrix statuses remain evidence-specific, for example `missing`,
`software_only`, `evidence_received`, `reviewed_pass`, `reviewed_warn`, and
`reviewed_fail`. Authorization and acceptance live in one authoritative
owner-decision record; the Evidence Matrix and Claim Registry store a pointer
and last-observed status instead of duplicating that decision. Evidence-ready
is not owner-accepted, and owner acceptance cannot strengthen missing evidence.
Use one durable authority per decision: an existing repository approval,
issue/PR decision, signed record, or conditional authorization entry is valid.
Authorization and result acceptance remain distinct even when recorded in the
same owner message.

Older 3.1 records may contain `ai_complete`, `software_verified`,
`tester_ready`, `hardware_verified`, `owner_accepted`, or `production_ready`.
Preserve those as historical data during migration; map current reports to the
readiness lanes and state-v2 packet status without silently rewriting evidence.

## Evidence Tier Claim Boundary

Use the weakest public claim supported by every required tier.

| Evidence tier | Supports | Does not support by itself |
| --- | --- | --- |
| `local_test` | source behavior, unit/contract/CLI checks | browser UI, live services, persistence, hardware, production |
| `browser_render` | visible render, interaction, layout | backend correctness, persistence, hardware, deployment safety |
| `live_runtime` | real local/dev service behavior | restart durability, remote compatibility, production readiness |
| `persisted_state` | reload/restart/import/export durability for named scope | hardware behavior, remote tester results, production operation |
| `remote_hardware` | reviewed evidence for a named device/tester/lab | all-device support, production rollout, owner acceptance |
| `production_evidence` | named deployed/package/monitor/rollback scope | broader environments or owner acceptance without a gate |

Tier names do not imply containment when scopes differ. A remote hardware bundle
can support a device claim while saying nothing about browser parity, persisted
local state, or production rollback.

## Claim Gate Smoke

Before an evidence-ready report, protected release action, or public/package
claim:

- keep every `blocked_until_evidence` claim blocked until required tier,
  freshness, and scope are present;
- use `accepted_within_scope` only when the public claim is qualified to the
  reviewed scope;
- fail closed when a release, production, hardware, compatibility, security,
  data, money, or rollback claim lacks sufficient evidence;
- allow a passing local test to coexist with a blocked stronger claim;
- name a CLI, API, file, manifest, UI, or other output contract in the active
  SPEC or artifact contract before treating shape checks as evidence;
- match the check to the artifact type: syntax does not prove rendering,
  persistence, hardware, or live runtime;
- keep one canonical artifact manifest for each generated package or bundle.

A claim remains blocked when required evidence is missing, stale, quarantined,
unreviewed, out of scope, or weaker than the claim.

## Conditional Owner Authorization

When an action can be pre-authorized, record:

```text
Decision:
Authorized action:
Packet:
Conditions:
Source/artifact identity:
Expires when:
Evidence required before action:
```

Reuse the authorization only while all recorded fields and source/artifact identity stay
unchanged. Expiry, failed conditions, missing required evidence, or source
changes require re-approval. Acceptance remains a separate owner decision.

## Evidence Layers And Claims

- Markdown guidance and records make expectations visible; they do not block tools.
- Doctor/tests/CI provide deterministic validation only for their defined checks.
- permissions/hooks/sandbox/branch protection/release controls provide technical enforcement.
- authorization and acceptance belong to the owner-decision layer.

Doctor green proves structural consistency. A successful task benchmark proves
the named task. Only a controlled comparison supports an improvement claim.

## Context Budget

Keep TODOs focused on unresolved work and findings focused on active defects or
risks. Link evidence paths and archive locations instead of pasting raw logs into
active state. Use bounded reads for imported evidence, generated artifacts,
archives, logs, databases, and authorized private data. A current handoff links
to these authorities; it does not duplicate them.
