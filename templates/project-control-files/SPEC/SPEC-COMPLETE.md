# SPEC COMPLETE

Status: Canonical integrated SPEC
Scope: Current product and implementation baseline

## Product Definition

Describe what this project is in one paragraph.

## Origin / Pain

Describe the previous pain or product need that created this project.

## Owner Control Model

Describe which decisions remain human-owned.

## Principles

- The owner controls direction and final acceptance.
- AI output is not completion evidence by itself.
- Active SPECs drive implementation.
- Tests, docs, and reproducible commands prove behavior.
- Future ideas stay out of active work until promoted.
- Current active SPEC sections override older historical sections.
- Obvious but consequential rules must be written down.
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

## Completion Criteria

Define tests, docs, reproducible evidence, and owner approval required for completion.

## Release / Production Readiness Gate

Define the additional evidence required before stable release or production use:
deployment, migration, security, backup/restore, observability, rollback,
manual checks, and cross-AI review as applicable.
