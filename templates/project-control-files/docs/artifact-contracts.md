# Artifact Contracts

Status: Active
Scope: Required contents, metadata, verification, retention, privacy, and
lineage for generated or imported artifacts

Use this file for packages, installers, firmware images, support bundles,
remote tester ZIPs, logs, screenshots, reports, or evidence bundles. A file is
not reliable evidence until its contract is satisfied or the missing fields are
named as gaps.

## Artifact States

- `planned`: contract exists, artifact not created.
- `built`: artifact was produced locally.
- `tester_ready`: artifact can be sent to a tester.
- `received`: artifact arrived from tester or external source.
- `quarantined`: artifact is isolated pending structure, privacy, and lineage
  checks.
- `validated`: required files and metadata are present.
- `accepted_as_evidence`: artifact was reviewed and mapped to evidence IDs.
- `rejected`: artifact is unsafe, incomplete, stale, corrupt, or out of scope.

## Standard Contract

```yaml
artifact_id: ART-001
name: remote_support_bundle
purpose: Evidence bundle from a tester or external machine
producer: remote tester / build script / CI / lab
consumer: developer, reviewer, owner
state: planned
required_files:
  - manifest.txt
  - command-outputs/
  - logs/
  - support-message.txt
required_metadata:
  - project version
  - commit or source snapshot
  - artifact build time
  - producer role
  - platform or environment summary
  - checksum list
verifier:
  command: ./scripts/import-support-bundle --check <path>
  expected_result: structure, privacy, checksum, and version checks pass
privacy_review:
  required: true
  forbidden_fields:
    - passwords
    - personal email
    - account IDs
    - private tokens
    - Wi-Fi passwords
lineage:
  source_commit: required before tester distribution, or reason recorded
  generated_from: build command, CI run, or source package path
retention:
  keep: manifest, review summary, accepted logs needed by evidence matrix
  archive: raw bundles after acceptance
  ignore: reproducible build output and local caches
evidence_mapping:
  - EVID-002
claim_impact:
  - CLAIM-001 remains qualified until review
```

## Artifact Registry

| Artifact ID | Name | State | Path | Contract status | Verifier | Evidence IDs | Claim impact | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ART-001 | Remote support bundle | planned | `docs/evidence/quarantine/` | Not created | import checker | EVID-002 | No claim change | Waiting for tester |

## Baseline Gate

Before distributing a tester package, alpha build, firmware image, installer, or
other artifact that will be used as evidence, record:

- `git status` reviewed,
- source compiles or build gap is named,
- required tests or checks pass,
- active docs reflect current behavior,
- known gaps are documented,
- generated files are ignored, reproducible, archived, or accepted as evidence,
- baseline commit exists or the reason for deferring it is recorded.

## Privacy Rules

Collect the minimum data needed for the evidence claim. Do not collect:

- passwords or secrets,
- account IDs,
- private tokens,
- personal email or phone numbers,
- Wi-Fi passwords,
- serial numbers unless needed and owner-approved,
- unnecessary full filesystem paths or usernames.

If private data is discovered, keep the artifact quarantined, scrub or reject it,
and record only the safe summary needed for evidence.
