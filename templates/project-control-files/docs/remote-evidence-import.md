# Remote Evidence Import / Quarantine Pattern

Status: Active
Scope: Importing, reviewing, and accepting evidence from remote testers,
external machines, hardware operators, labs, or users

Use this file whenever evidence crosses a trust boundary. Remote evidence must
not directly update claims, TODO completion, or production readiness. It moves
through quarantine, validation, review, evidence mapping, and owner acceptance
when required.

## Standard Flow

```text
developer builds tester-ready artifact
-> tester runs documented steps
-> tester generates support bundle or evidence package
-> bundle enters quarantine
-> importer checks structure, metadata, checksums, and privacy
-> reviewer maps evidence to requirements and claims
-> evidence matrix, claim registry, TODO, and review findings are updated
-> owner accepts or keeps gate blocked
```

## Directory Pattern

Adapt paths to the project, but preserve the states:

```text
docs/evidence/quarantine/
docs/evidence/validated/
docs/evidence/accepted/
docs/evidence/rejected/
docs/evidence/reviews/
```

Raw bundles should not be mandatory first-read material. Link to review
summaries and evidence IDs instead.

## Import Checklist

| Check | Required? | Result | Notes |
| --- | --- | --- | --- |
| Expected archive or folder shape | yes | pending | |
| Manifest present | yes | pending | |
| Project version or source snapshot present | yes | pending | |
| Artifact checksum present | yes | pending | |
| Tester role and environment summary present | yes | pending | |
| Required command outputs present | yes | pending | |
| Relevant logs present | project-specific | pending | |
| Privacy scan passed | yes | pending | |
| Forbidden file types absent | yes | pending | |
| Evidence is fresh for current code/artifact | yes | pending | |
| Evidence maps to matrix IDs | yes | pending | |
| Claim changes reviewed against registry | yes | pending | |

## Privacy Scan

Flag or reject bundles containing:

- passwords, tokens, keys, or secrets,
- personal email, phone numbers, account IDs,
- Wi-Fi passwords,
- unnecessary usernames, home paths, or machine names,
- serial numbers unless needed and approved,
- private network details unless explicitly requested and scoped.

If sensitive data is found, keep the bundle quarantined and record a safe
summary. Do not paste private data into TODOs, review findings, handoffs, or AI
chat.

## Review Summary Template

```text
Review ID:
Bundle path:
Importer:
Reviewed at:
Source artifact:
Source commit or build:
Tester role:
Environment summary:
Privacy result:
Structure result:
Freshness result:
Evidence IDs updated:
Claim IDs affected:
Accepted scope:
Remaining gaps:
Negative results:
Decision:
  accepted_as_evidence / accepted_with_limits / rejected / needs_retest
Next action:
```

## Sufficiency Rule

A remote bundle is sufficient only when:

- manifest and metadata are present,
- command outputs or logs cover the required behavior,
- checksum/version/commit or build lineage is recorded,
- pass/fail signal is clear,
- privacy and structure checks pass,
- evidence is fresh for the current artifact,
- evidence maps to requirements in `docs/evidence-matrix.md`,
- claim impact is checked against `docs/claim-registry.md`.

If any required field is missing, mark the evidence `weak`,
`reviewed_warn`, or `reviewed_fail`; do not unlock the claim.

## Trust Boundary

Local tests, remote tester evidence, and external lab evidence have different
trust levels. Remote evidence can support a claim after review, but it should
not automatically change user-facing claims or owner acceptance. High-impact
claims may require an evidence quorum such as local software checks plus remote
hardware evidence plus owner acceptance.
