# Claim Registry

Status: Active
Scope: User-facing, release-facing, and owner-facing claims allowed by current
evidence

Use this file to prevent README, SPEC, UI, release notes, manifests, packaging,
support text, or AI handoffs from making claims stronger than the evidence
allows. Claims should link to evidence IDs from `docs/evidence-matrix.md`.

## Claim Status

- `allowed`: evidence supports the claim as written.
- `allowed_with_qualifier`: claim is allowed only with the listed qualifier.
- `blocked_until_evidence`: claim must not be used until required evidence is
  accepted.
- `forbidden`: claim is out of scope, false, unsafe, or owner-blocked.
- `retired`: old claim that should not appear in current materials.

## Claim Severity

- `P0_forbidden`: high-risk or false claim; blocks release if present.
- `P1_evidence_required`: claim needs accepted evidence before use.
- `P2_qualified`: allowed only with a clear scope or limitation.
- `P3_informational`: low-risk descriptive wording.

## Registry

| ID | Claim text or pattern | Status | Severity | Allowed locations | Required evidence | Required qualifier | Blocked locations | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CLAIM-001 | Example product is software evidence-ready | allowed_with_qualifier | P2_qualified | README, handoff | EVID-001 | "software evidence-ready; hardware pending" | release title | Do not imply production readiness |
| CLAIM-002 | Example product is production ready | blocked_until_evidence | P1_evidence_required | None | EVID-010, EVID-011, owner acceptance | None | README, UI, release notes, manifest | Requires release gate |
| CLAIM-003 | Example target compatibility guaranteed | forbidden | P0_forbidden | None | None | None | All public/user-facing text | Out of current scope |

## Claim Scan Checklist

Before release, tester distribution, public README updates, package generation,
or UI copy changes, scan:

- `README.md`
- `SPEC/SPEC-COMPLETE.md`
- release notes and changelog
- package manifests, installers, and support bundle text
- UI labels, status text, dialogs, and error messages
- docs intended for testers, customers, or operators

## Stop Rules

- If a `P0_forbidden` claim appears, stop release or distribution until removed.
- If a `P1_evidence_required` claim lacks accepted evidence, keep the gate
  blocked.
- If a claim is only `software_only`, include that qualifier wherever the claim
  appears.
- Do not upgrade a claim because a bundle arrived. Upgrade only after evidence
  import, review, matrix update, and owner gate when required.

## Owner Acceptance

| Claim ID | Accepted by | Accepted at | Accepted scope | Evidence IDs | Remaining gaps |
| --- | --- | --- | --- | --- | --- |
| CLAIM-001 | Owner name / role | YYYY-MM-DD | Software-only alpha wording | EVID-001 | Hardware evidence pending |
