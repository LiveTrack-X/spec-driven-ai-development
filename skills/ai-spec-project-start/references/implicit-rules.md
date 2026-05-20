# Implicit Rules

Load this when the owner asks to capture obvious-but-unwritten rules, when a
project has stale SPEC/history risk, or when creating/reviewing project control
files.

## Core 5

- Current beats historical: current code, tests, active docs, and active SPEC
  sections override older SPEC history, archives, old handoffs, and chat memory.
- Evidence beats confidence: no completion claim without commands, results,
  changed files, docs checked, and remaining risks.
- Active beats interesting: future ideas and external references are not active
  scope until promoted.
- Owner decision beats AI momentum: mark owner decisions before scope, risk, or
  release posture changes.
- Repeated pain becomes a rule, checklist, test, or template update.

## Extended Rules

- Work packets and review-worthy units beat micro-approval and large unverified
  progress.
- Implementation discipline makes autonomy safe: surface assumptions, prefer
  simple designs, make surgical changes, and verify goals.
- Open critical findings beat new feature work unless the owner accepts the risk.
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
