# Operating Intensity

Status: Active reference
Scope: How Standard and Full SDAD reduce or raise operating weight after setup

The purpose of SDAD is not to create more control files. The purpose is to keep
the project controllable.

When control surfaces reduce controllability, lower intensity, freeze the
baseline, compress evidence, and simplify owner review.

## Scale Versus Intensity

`Mini / Standard / Full SDAD` are project scales.

`High / Medium / Low` are operating intensities used inside Standard and Full
SDAD. They are not new scales, and they are not autonomy levels.

Use this notation:

```text
Standard SDAD / High
Standard SDAD / Medium
Standard SDAD / Low
Full SDAD / High
Full SDAD / Medium
Full SDAD / Low
```

Mini SDAD does not use operating intensity tiers. It is already the
low-surface, one-file scale.

Use `Standard SDAD / High` for non-Q5 Standard projects when the current packet
requires a major product or architecture tradeoff, a broad hard-to-reverse
implementation choice, or an explicit owner checkpoint, but does not change a
release, production, migration, real-data, auth, security, money, rollback, or
other Q5 gate.

## High

Use `High` when the current packet changes behavior, policy, boundary,
evidence claim, or risk acceptance for release, production claims, migration,
destructive action, real user data handling, auth, data, money, security,
rollback, accepted-memory boundaries, external deployment, or a major
owner-controlled risk decision.

Docs, tests, or references that merely mention a risk area do not make the
packet `High`. The packet becomes `High` when it changes how that risk is
handled, claimed, accepted, or released.

A Q5 project does not make every packet `High`. Raise the current packet to
`Full SDAD / High` only when the current work changes a Q5 gate.

High intensity requires:

- evidence required by the active risk gate, not every possible artifact,
- explicit owner checkpoint,
- risk gate,
- ADR or review update when a durable decision or finding exists.

## Medium

Use `Medium` for normal feature work, bugfixes, multi-file implementation,
validation, and docs sync inside an approved scope.

Medium intensity uses:

- work packet autonomy,
- normal control-file maintenance,
- Owner Review Compression before detailed evidence,
- no new release, security, data, auth, money, rollback, or production decision.

## Low

Use `Low` for docs-only changes, typos, index updates, helper splits,
small test/check adjustments, and small README or template edits.

Low intensity uses:

- minimal control-file maintenance,
- no new evidence surface unless it reduces owner review time or protects a real
  boundary,
- Fast Patch style work when the scope is obvious and low risk.

## Baseline Freeze

Baseline Freeze is a posture, not a new scale or a new intensity value.

Use it after a usable baseline exists and more features are less valuable than
repeatability, owner review, UX simplification, and real baseline runs.

Use one of the official labels with the posture named separately, for example
`Full SDAD / Medium (Baseline Freeze)` or `Full SDAD / Low (Baseline Freeze)`.
Do not create a `Low-Medium` label.

In Baseline Freeze:

- default new packets to `Medium` or `Low`,
- do not add a feature unless it improves the baseline loop,
- do not add a verifier, viewer, report, digest, handoff format, or handoff
  report unless it reduces review time, protects a safety boundary, supports a
  release gate, or makes the baseline repeatable,
- prefer health summaries, owner review, and real-data or representative runs
  over new surface area.

If the current packet changes behavior, policy, boundary, evidence claim, or
risk acceptance for release, production claims, migration, destructive action,
real user data handling, auth, data, money, security, rollback, accepted-memory
boundaries, external deployment, or a major owner risk decision, move that
packet to `Full SDAD / High`.

## Owner Review Compression

Every `Medium` or `High` checkpoint should start with:

- one-line status,
- changed user-facing behavior,
- safety boundary touched: yes/no,
- checks summary,
- owner decision needed: yes/no,
- recommended next action,
- links or references to detailed evidence.

Detailed evidence still matters. Compression decides what the owner sees first.

## Evidence Surface Rule

Every new verifier, digest, viewer, report, handoff format, handoff report, or
parallel evidence artifact is a cost until it proves otherwise. This does not
remove the standard SDAD session handoff requirement.

Add a new evidence surface only when it:

- reduces owner review time,
- protects a real safety boundary,
- supports a release or production gate,
- or makes a baseline repeatable.

If evidence grows faster than owner clarity, lower intensity and simplify the
review path.

## Evaluation-Driven Extensions

Harness optimization, self-improving agent loops, retrieval/memory tuning, and
repeated evaluation automation are advanced extensions, not default SDAD loops.

Before running one, pass the Advanced Extension Fit Gate in
[fit-assessment.md](fit-assessment.md). State:

- what task unit repeats,
- what metric decides improvement,
- what model and tool surface stay fixed,
- what changes are allowed,
- what evidence is search evidence,
- what evidence is reserved for owner acceptance,
- what leakage risk exists,
- what concrete budget applies.

Use `Medium` only when the extension changes no Q5 boundary and the budget is
bounded. Use `High` when it changes risk acceptance, production claims,
release posture, security/data/auth/money boundaries, or owner adoption
decisions.

Discovered prompts, rules, retrieval policies, memory policies, or harnesses are
evidence-ready candidates. They are not owner-accepted until the owner reviews
the split, leakage risk, budget result, changed behavior, and adoption plan.
