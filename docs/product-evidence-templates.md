# Product Evidence Templates

Status: Active reference
Scope: Optional Standard/Full SDAD templates for product, hardware, external
tester, release, and compatibility claims

Use these templates when a project needs evidence stronger than local software
tests, especially when work depends on hardware, packaging, remote testers,
external labs, real users, generated artifacts, or product/release claims.

These templates grew from hardware/product work where SDAD kept claim gates and
evidence boundaries intact, but active docs became too large, completion states
were ambiguous, evidence mapping was scattered, and remote hardware validation
needed a first-class loop. The templates are generic by design; do not copy
project-specific names, devices, or claims unless they are true for the current
project.

## Template Set

Install only the files the project can maintain:

- **Evidence Matrix**:
  [`docs/evidence-matrix.md`](../templates/project-control-files/docs/evidence-matrix.md)
  maps requirements and claims to evidence, status, scope, freshness, and gaps.
- **Claim Registry**:
  [`docs/claim-registry.md`](../templates/project-control-files/docs/claim-registry.md)
  lists allowed, qualified, blocked, and forbidden claims across README, SPEC,
  UI, release notes, manifests, packaging, and support text.
- **Artifact Contract**:
  [`docs/artifact-contracts.md`](../templates/project-control-files/docs/artifact-contracts.md)
  defines required files, metadata, verifier commands, retention, privacy, and
  lineage for packages, firmware, support bundles, logs, or imported evidence.
- **Work Packet State Model**:
  [`docs/work-packet-state.md`](../templates/project-control-files/docs/work-packet-state.md)
  defines packet states so `ai_complete`, `software_verified`,
  `tester_ready`, `hardware_verified`, `owner_accepted`, and
  `production_ready` are not collapsed into one word: done.
- **Remote Evidence Import / Quarantine Pattern**:
  [`docs/remote-evidence-import.md`](../templates/project-control-files/docs/remote-evidence-import.md)
  defines a quarantine-to-accepted flow for remote tester bundles and external
  evidence before any claim gate changes.

## When To Use

Use this template set when any of these are true:

- a local software test cannot prove the product claim,
- hardware, firmware, device compatibility, packaging, or deployment matters,
- evidence comes from another machine, tester, user, lab, or external platform,
- generated artifacts must be traced to a commit, build, verifier, or package,
- README, UI, release notes, or manifests could overclaim support,
- active TODO, review, or save-state files are carrying too much completed
  evidence history.

Treat this as a product evidence flag, not a new SDAD scale. A yes to this flag
usually means `Standard SDAD / Medium` or higher and at least the relevant
templates from this set. Use `Full SDAD / High` only when the current packet
changes a release, production, hardware compatibility, security, data, money,
destructive-action, rollback, or other Q5 gate.

## How The Templates Work Together

Use the work-packet state model to name the current packet state.

Use the evidence matrix to decide which requirements are covered, stale,
blocked, or still software-only.

Use the claim registry to decide which public or user-facing claims are allowed.

Use artifact contracts to define what a package, support bundle, firmware image,
log set, or evidence bundle must contain before it can be reviewed.

Use remote evidence import when evidence crosses a trust boundary. Imported
evidence starts in quarantine, then becomes validated, reviewed, and accepted
only after structure, privacy, lineage, and scope checks pass.

## Required Separation

Keep packet states, evidence statuses, and owner acceptance separate:

- `ai_complete`: the AI finished an implementation slice.
- `software_verified`: local commands passed, but hardware/product claims may
  still be unproven.
- `tester_ready`: an artifact can be sent to a tester, but evidence is not back.
- `evidence_received`: a bundle arrived, but is not reviewed or accepted.
- `hardware_verified`: qualified evidence was reviewed and mapped to
  requirements.
- `owner_accepted`: the owner accepted a named scope.
- `production_ready`: release/production evidence and owner gate passed.

Evidence status values live in `docs/evidence-matrix.md` and stop at review,
such as `missing`, `software_only`, `evidence_received`, `reviewed_pass`,
`reviewed_warn`, or `reviewed_fail`.

Owner acceptance is an acceptance field or ledger, not an evidence status.

Do not use local software evidence to unlock hardware, compatibility,
production, or release claims unless the evidence matrix and claim registry
explicitly allow that scope.

## Evidence Tier Claim Boundary

Use the weakest public claim that all required evidence tiers support.

| Evidence tier | Supports claims like | Does not support by itself |
|---|---|---|
| `local_test` | source-level behavior, unit/contract/CLI checks, deterministic local regressions | browser UI, live service behavior, persistence after restart, hardware, production |
| `browser_render` | visible UI render, interaction, layout, screenshot-reviewed product controls | backend correctness, persisted state, remote hardware, deployment safety |
| `live_runtime` | service starts and works in a real local/dev runtime with its configured dependencies | state durability after restart, remote environment compatibility, production readiness |
| `persisted_state` | reload/restart/import/export proves durable state for the named scope | live hardware behavior, remote tester results, production operation |
| `remote_hardware` | named device, tester, lab, or external machine evidence after quarantine and review | all-device compatibility, production rollout, owner acceptance |
| `production_evidence` | deployed, packaged, monitored, rollback-ready, or release-channel claims for the named environment | broader claims than the deployed scope, owner acceptance without a checkpoint |

A higher-sounding tier does not automatically cover a lower one when the scope
differs. For example, a remote hardware bundle can support a device claim but
not prove browser UI parity, persisted local state, or production rollback.

## Claim Gate Smoke

Before evidence-ready, owner checkpoint, release notes, or package metadata,
scan `docs/claim-registry.md` for claims affected by the packet:

- Any `blocked_until_evidence` claim remains blocked unless the required
  evidence tier, freshness, and scope are present.
- A warning-level result can become `accepted_within_scope` only when the public
  claim is qualified to the reviewed scope.
- A release, production, hardware, compatibility, security, data, money, or
  rollback claim must fail closed when the evidence tier is missing or weaker
  than the claim.
- A passing local test may coexist with a blocked production, release, hardware,
  compatibility, or rollback claim. Report the local behavior as supported and
  keep the stronger claim blocked.
- If a CLI, API, file, manifest, or UI text shape is part of the evidence, the
  active SPEC or artifact contract must name that output contract before the
  evidence can support the claim.
- Match the check to the artifact type. A syntax check for one language does not
  prove CSS validity, HTML rendering, browser behavior, persisted state, or live
  runtime behavior.
- Keep one canonical artifact manifest for each generated package or evidence
  bundle; duplicate manifest copies are evidence drift unless one is explicitly
  marked as derived.

## Context Budget

These templates should reduce active-doc size, not create another journal.

- Keep `docs/TODO-Open-Items.md` focused on active work and next action.
- Keep `review-findings.md` focused on active bugs, risks, and blocked gates.
- Keep long evidence history, raw logs, old bundles, and completed packet
  details out of mandatory start-loop docs.
- Link to accepted evidence paths and archive locations instead of pasting logs
  into active state files.
- Use bounded reads for imported evidence, generated artifacts, logs, archives,
  and private data.

## Owner Checkpoint

Before a product, hardware, compatibility, or release claim is accepted, the
checkpoint should answer:

- Which requirement or claim is being accepted?
- Which evidence IDs support it?
- What is the evidence tier and freshness rule?
- What scope was accepted, and what remains pending?
- Did remote evidence pass quarantine, privacy, lineage, and review checks?
- Which public/user-facing claims are still blocked or must remain qualified?
- Which docs, TODOs, review findings, and artifacts were updated?

Evidence-ready still is not owner-accepted. A claim remains blocked when the
required evidence is missing, stale, quarantined, unreviewed, out of scope, or
too weak for the claim.
