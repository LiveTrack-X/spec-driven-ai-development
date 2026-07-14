# Implicit Rules

Load this when the owner asks to capture obvious-but-unwritten rules, when a
project has stale SPEC/history risk, or when creating/reviewing project control
files.

## Core 5

- Current beats historical: the current applicable owner instruction plus
  current code, tests, active docs, and active SPEC sections override older
  directions, history, archives, handoffs, and chat memory; current does not
  mean newest filename or timestamp.
- Evidence beats confidence: no completion claim without commands, results,
  changed files, docs checked, and remaining risks.
- Active beats interesting: future ideas and external references are not active
  scope until promoted.
- Owner decision beats AI momentum: when the owner redirects work, stop the
  affected old direction and reconcile state before resuming; review/reference
  intent remains read-only.
- Repeated pain becomes a rule: repeated pain or one high-risk control failure
  becomes a finding/root cause, the smallest durable control plus regression
  evidence, and later a Keep/Refine/Merge/Retire decision; prefer refining
  existing controls.

Compression first. Gates stay real.

## Extended Rules

- Work packets and review-worthy units beat micro-approval and large unverified
  progress.
- Implementation discipline makes bounded execution safe: surface assumptions, prefer
  simple designs, make surgical changes, and verify goals.
- Open critical findings gate intersecting feature/claim work unless the owner
  accepts that bounded risk; unrelated findings may be explicitly deferred with
  packet links and revisit triggers.
- Explicit non-goals beat assumptions.
- Stated uncertainty beats silent guessing.
- Repository evidence beats unnecessary questions: inspect current code, tests,
  active docs, SPEC, TODOs, review findings, and ADRs before asking the owner.
- Stable terms beat session vocabulary: define execution-relevant domain terms
  when terminology drift affects implementation, review, tests, or owner
  decisions.
- Partial, scaffolded, degraded, skipped, or unverified behavior must be labeled.
- Docs drift is a bug because future AI sessions read docs as operating input.
- Handoff is context, not authority.
- Archive preserves history, not active execution.
- Version lanes beat copy-paste sync.
- Release readiness beats feature count.
- Environment limits beat overclaiming.
- Cross-review beats single-agent finality.
- Scope-specific percent beats vague global percent.
- Failed, missing, skipped, timed-out, or unrun tests beat narrative.
- Risk gates beat convenience.
- Context budget beats full transcript: large state files, archives, logs,
  generated artifacts, and private data require bounded reads.
- Implementation memory beats hidden rationale: record spec-unstated
  implementation decisions in implementation notes, not only in chat memory.
- Natural language intent beats skill names: infer review, implementation,
  release, docs, handoff, reference-intake, or execution-scope/owner-gate tuning
  intent from ordinary user wording and current repo state.
- Guarantees beat guidance for non-negotiables: keep judgment in guidance and
  put deterministic requirements in tests, validators, hooks, permissions, or
  other enforceable surfaces.

## How To Apply

When starting or reviewing a project, add these checks:

1. Which source is current?
2. Which SPEC sections are historical?
3. Which work is active, future, or archived?
4. What work packet and review-worthy development units are active?
5. What evidence makes this packet evidence-ready?
6. What tests were not run?
7. What is partial or degraded?
8. What owner decision is needed?
9. Which repeated pain should become a durable rule?
10. Which large files or archives should be read only with bounded queries?
11. Which spec-unstated implementation decisions need implementation notes?
12. Which fuzzy plan questions can be answered from repository evidence?
13. Which domain terms need a glossary route?
14. What user intent was inferred if the request did not use SDAD terms?
