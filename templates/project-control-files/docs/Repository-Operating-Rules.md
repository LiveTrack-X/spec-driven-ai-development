# Repository Operating Rules

Status: Active
Scope: durable repository policy, loaded by route rather than at every startup

## How To Use This Rulebook

The always-loaded contract is the installed tool adapter at its native path.
Current packet state is `sdad-state.yaml`. File selection belongs to
`docs/INDEX.md`. Read this rulebook only when the current packet changes policy,
authority, evidence, risk, or maintenance behavior.

Open the relevant heading, then follow a playbook only when its trigger applies.
Do not read the whole file merely because it exists. Procedures, examples, and
large checklists belong in `docs/sdad/playbooks/`; current facts belong in
state, SPEC, TODO, findings, notes, or evidence files.

## Source Of Truth

When sources conflict, prefer:

1. current source code, migrations, tests, runtime state, and reproducible
   commands for observed behavior;
2. active runtime and operating documents for current controlled state;
3. canonical SPEC for the integrated product baseline;
4. active SPEC files for the approved slice;
5. current handoff and save-state for continuity;
6. product notes and external references as unpromoted input;
7. archives and historical records as rationale;
8. chat memory and AI confidence as hints only.

If a SPEC spans past-to-present history, current active sections override older
background, roadmap, and archived material. This exception resolves chronology
inside the source; it does not let an unapproved draft override owner scope.

Read order is routing, not authority. Current evidence can disprove stale
documentation, but it cannot choose future product scope. Owner decisions
control direction, risk tolerance, irreversible actions, and acceptance. Record
durable owner decisions in the appropriate active source of truth.

A handoff or save-state decision is continuity until promoted. Before
implementation, promote anything that changes scope, acceptance criteria,
behavior, public claims, risk, evidence, or owner acceptance to SPEC, ADR,
claim registry, TODO, or findings.

## Owner Authority And Evidence States

Keep these states distinct:

- planned: the packet has not produced evidence;
- AI-complete / evidence-ready: scoped implementation and checks are shown;
- software-verified: required local software evidence passed;
- tester-ready or hardware-verified: the corresponding external evidence exists;
- release-candidate or production-ready: every named release gate passed;
- owner-accepted: the owner or delegated policy accepted the result.

Owner acceptance cannot upgrade weak evidence. A passing evaluator cannot
approve scope. A successful commit cannot authorize push, release, deploy,
migration, destructive action, or risk acceptance.

The AI may continue autonomously inside an approved packet. It must stop when
scope expands, a Q5 risk or claim gate changes, an irreversible action is
required, an owner-controlled tradeoff remains unresolved, verification is
blocked, or evidence conflicts with the requested plan.

## Non-Negotiable Boundaries

### Sensitive Data

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Do not read, copy, transmit, summarize, or
paste credentials, private keys, tokens, cookies, `.env` contents, raw
customer records, or private corpora unless the task requires it and owner policy plus tool policy explicitly permit it.

Prefer redacted samples, schemas, counts, filenames, and hashes. Keep sensitive
content out of prompts, logs, TODOs, findings, handoffs, and generated
artifacts. If authorization is unclear, stop before reading.

### Irreversible And External Actions

Release, deploy, migration, destructive action, real-user-data handling, auth,
money, security policy, rollback, public claims, and external messages require
the owner gate named by the active packet. Reversible local implementation does
not imply authority for the external action.

### Context Stability

Check size and relevance before reading large, generated, historical, or broad
inputs. Use bounded reads above 50 KB or 500 lines. Do not read files above
1 MB in full during startup unless historical reconstruction is explicitly
requested. Use the context-and-data playbook for private or oversized inputs.

## Code Consistency

Current behavior and acceptance criteria must agree. Before implementation:

- inspect current source and tests rather than trusting a plan summary;
- identify the active SPEC slice, non-goals, packet boundary, and evidence
  expectation;
- prefer the simplest design that satisfies the current contract;
- keep changes surgical and separate active implementation from future ideas;
- add a failing test/check before behavior changes when the surface is testable;
- label partial, degraded, scaffolded, simulated, skipped, and unverified work.

A green test suite proves only the claims covered by those tests. When package,
browser, persisted-state, hardware, remote, or production behavior is claimed,
run evidence at the corresponding tier.

## Durable Decision Policy

Write each decision once:

- active SPEC: scope, behavior, non-goal, acceptance criterion;
- implementation notes: a spec-unstated implementation judgment and its
  verification impact;
- ADR: a hard-to-reverse, surprising, durable tradeoff;
- TODO: current or deferred work;
- review findings: defect, failed check, unresolved risk, or blocked gate;
- claim/evidence files: allowed, qualified, or blocked claim status;
- save-state/handoff: resume context only.

Do not store raw internal reasoning, mechanical edit journals, or copied logs in
active control files. Repeated pain becomes a concise rule, playbook, test,
validator, hook, or template change at the cheapest enforceable layer.

## Review And Verification

A packet is evidence-ready only when:

1. the approved behavior or documentation change is implemented;
2. relevant tests and reproducible checks pass, or the exact block is recorded;
3. the evidence tier matches every claim;
4. changed control state, SPEC, TODO, findings, notes, and docs are synchronized;
5. unfinished packets, generated artifacts, caches, and package outputs are
   checked when relevant;
6. remaining risk, unverified behavior, owner decisions, and acceptance state are
   explicit.

Review findings outrank feature expansion unless the owner accepts the risk.
Reference-derived work requires a source-to-implementation-to-evidence parity
map. Package or release work requires smoke testing outside the source tree
when the installed artifact is part of the claim.

## On-Demand Playbooks

Load only the triggered playbook:

- `sdad/playbooks/context-and-data.md`: large/private input and context recovery;
- `sdad/playbooks/work-packets.md`: scale, autonomy, intensity, clarification;
- `sdad/playbooks/evidence-and-risk-gates.md`: Q5, claims, parity, release;
- `sdad/playbooks/documentation-and-handoff.md`: record routing, budgets,
  maintenance, save-state, and handoff;
- `sdad/playbooks/advanced-extensions.md`: harness, eval, memory, and loop fit.

## Rule Maintenance

Keep this file policy-only and reasonably short. Move procedures and examples
to playbooks. Keep INDEX routing-only and active state current. Archive closed
history. If a rule is mechanically enforceable, prefer a test or validator over
duplicated prose. If no current packet needs a rule or playbook, do not load it.
