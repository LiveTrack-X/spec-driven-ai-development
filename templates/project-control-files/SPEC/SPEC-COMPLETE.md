# SPEC COMPLETE

Status: Canonical integrated SPEC
Scope: Current product and implementation baseline

`COMPLETE` means integrated baseline, not immutable or automatically active.
For a stateful packet, `sdad-state.yaml#active_spec` selects the single
normative SPEC entrypoint.

## SPEC Authority And Lineage

This integrated baseline is not immutable, and it is not automatically active;
state selects the normative entrypoint.

An additional SPEC does not become authority merely because it is newer, has
`FINAL` or `COMPLETE` in its name, or exists under `SPEC/`. Requested action and
owner intent matter: a SPEC supplied as current requirements is a change
request, while review/draft/reference-only intent is not. Hold affected
implementation while comparing it with the active acceptance boundary; do not
demote it to proposal/reference merely because state has not been updated yet.
A SPEC only discovered in the repository may remain non-authoritative, but the
packet may continue only after it is confirmed nonconflicting. Then classify
the result as an amendment, bounded supplement, replacement, or proposal.

- Amendment: update the current active SPEC inside the existing acceptance
  boundary.
- Bounded supplement: the active SPEC links its exact path and scope; this
  active entrypoint controls conflicts and the baseline controls everything
  outside the declared override.
- Replacement: record owner scope/acceptance, name the superseded path or exact
  headings, and switch `active_spec` in the packet transaction.
- Proposal/reference: retain it as non-authoritative input until promoted.

For a non-terminal packet, an owner-requested change inside the same objective
and acceptance boundary may amend or supplement the active SPEC in the same
packet; invalidate and rerun affected evidence. A material objective,
acceptance, protected-boundary, or authorization-term change uses a new packet.
If intent or overlap cannot be determined, ask one blocking question before
affected implementation. A terminal accepted boundary is never reopened.

New additional or replacement SPECs start with this exact metadata block:

```markdown
Status: Proposal | Active | Superseded | Reference
Baseline: SPEC/path.md
Baseline revision: commit/tree/digest | Unpinned proposal
Effective packet: WP-EXAMPLE | Unassigned
Supersedes:
- SPEC/path.md#exact-heading | None (additive)
```

`Effective packet` records the first packet that activates this SPEC revision;
do not rewrite it to follow the current packet. Use `Active` only after exact
incorporation or pointer switch. Existing
single-SPEC projects remain valid without retrofitting metadata. A material
requirement change after owner acceptance uses a new, never-reused packet ID
and new validation; it does not rewrite old acceptance to cover new scope.
Pin the baseline revision when a supplement participates in a terminal packet;
an unpinned proposal remains non-authoritative.

`Active` on a supplement means the state-declared entrypoint incorporated it;
it does not create a second normative entrypoint. Normative supplements must be
readable repository-local paths. Keep lineage acyclic: a SPEC cannot supersede
itself, and overlapping supplements require explicit precedence in the active
entrypoint before implementation. External documents remain references until
their accepted requirements are incorporated repository-locally.

Do not split a SPEC merely because work continues after `COMPLETE`. Split when
targeted reads are no longer practical, independent domains need different
packets, or parallel edits repeatedly conflict. Keep `active_spec` as the short
normative entrypoint and link bounded supplements with exact inherited and
overridden scope; do not duplicate shared acceptance across leaf files.

## Product Definition

Describe what this project is in one paragraph.

## Origin / Pain

Describe the previous pain or product need that created this project.

## Owner Control Model

Describe which decisions remain human-owned.

## Principles

- The owner controls direction and final acceptance.
- AI output is not completion evidence by itself.
- The state-declared active SPEC entrypoint drives implementation.
- Tests, docs, and reproducible commands prove behavior.
- Future ideas stay out of active work until promoted.
- Current active SPEC sections override older historical sections.
- Obvious but consequential rules must be written down.
- Fuzzy plans should be checked against repository evidence before owner
  clarification.
- Partial, degraded, skipped, or unverified behavior must be labeled.

## Current Architecture

Describe main components and data flow.

## Version Lanes

If the project has stable, beta, rewrite, platform, or migration lanes, describe
allowed changes, sync rules, and release-channel rules. If not applicable, state
that the project currently has one active lane.

## Risk Domains

List any areas that need special review rules, such as auth, tenant isolation,
database migrations, backup/restore, real-time callbacks, locks, platform
boundaries, release packaging, prompt contracts, or model/tool permissions.

## Active Scope

Describe what is being implemented now.

## Non-Goals

Describe what is explicitly not being built yet.

## Risks

List security, data, operational, complexity, quality, and AI-overreach risks.

## Roadmap

List priority order for implementation.

## Decision Records

Record durable decisions under `SPEC/adr/`. Use ADRs when future agents need to
know why a decision was made, what alternatives were rejected, and what older
SPEC material was superseded.
A decision normally deserves an ADR only when it is hard to reverse, would
surprise a future maintainer without context, and represents a real tradeoff.

## Domain Language

If overloaded terms affect implementation, review, tests, or owner decisions,
define the canonical terms here or route a small glossary from `docs/INDEX.md`.

## Completion Criteria

Define tests, docs, reproducible evidence, and owner approval required for completion.

## Release / Production Readiness Gate

Define the additional evidence required before stable release or production use:
deployment, migration, security, backup/restore, observability, rollback,
manual checks, and cross-AI review as applicable.
