# SDAD Runtime Contract

Read this reference before creating or changing an SDAD control surface. It is
the semantic contract shared by the bootstrap skill, installed adapters, and
project templates.

## Scale Truth Table

Ask five yes/no questions:

1. Will the work take more than one AI session?
2. Will the owner return to the project later?
3. Does done need evidence beyond AI confidence?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, production, migration, destructive action, real user data,
   auth, money, security, rollback, or equivalent owner-controlled risk?

Apply overrides before counts:

- 0 yes: One-shot; create no persistent files.
- 1-2 yes from Q1-Q3 only, with Q4/Q5 no: Mini; one instruction file.
- Q4 yes or 3 yes total: Standard.
- A packet that only inspects, documents, or tests a Q5 area: Standard minimum.
- A packet that changes, accepts, or executes a Q5 gate, or 4-5 yes: Full.

Use the smaller scale only when no active Q5 gate or continuity need would be
lost. Merely naming a risk does not activate its gate; changing its boundary,
policy, claim, accepted risk, or external action does. Re-evaluate when
duration, collaboration, evidence, or risk changes.

## Intent Route

Infer intent from plain language and repository state:

- check/review/audit/find bugs: review and report; do not implement unless the
  request also includes a change;
- implement/build/fix/match the spec: active-SPEC implementation;
- release/publish/tag/deploy/migrate: high-risk route with owner gates;
- docs/README/FAQ/guide: affected documentation route;
- handoff/continue later/lost context: continuity route;
- borrow/reference/adopt an idea: reference-intake and parity route;
- asks too often/runs ahead: autonomy and packet-boundary tuning.

Treat carefully/thoroughly as inspection depth, fully/end-to-end as continuing
to evidence-ready inside approved scope, minimal/quickly as compression, and
commit and wait as neither push nor release. Compose intents only when they fit
one packet without changing scope, risk, claim, or owner gates.

## Autonomy And Stop Contract

- Mini: Level 1 Unit Autonomy for one small approved packet.
- Standard: Level 2 Work Packet Autonomy.
- Full: Level 2 implementation with Level 4 owner gates for release,
  migration, destructive action, data/auth/money/security decisions, rollback,
  and production claims.

Do not stop after every micro-task or internal review-worthy unit. Stop only
when scope expands, a risk or claim gate changes, an irreversible action is
required, an owner-controlled tradeoff remains unresolved, verification is
blocked, or evidence conflicts with the requested plan.

## Progressive Control Plane

For Standard or Full, read in this order:

1. the installed tool adapter;
2. `sdad-state.yaml`;
3. `docs/INDEX.md`;
4. current source/tests/runtime state;
5. only the docs and policy/playbook headings routed for the packet.

Do not load the full rulebook, archives, old handoffs, historical SPEC sections,
or optional evidence files by default. Keep the fixed startup plane below the
budgets enforced by repository tests.

## Sensitive Data Boundary

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Do not read or expose credentials, keys,
tokens, cookies, `.env` contents, raw customer records, or private corpora
unless the task requires it and owner policy plus tool policy permit it.

Prefer redacted samples, schemas, counts, filenames, and hashes. Stop before
reading when authorization is unclear. Keep sensitive content out of prompts,
logs, TODOs, findings, handoffs, and generated artifacts.

## Context Stability

Check size, freshness, generation source, sensitivity, and relevance before
opening broad input. Use headings, current sections, targeted matches, output
limits, and explicit excludes. Default to bounded reads above 50 KB or 500
lines and avoid full startup reads above 1 MB unless historical reconstruction
is requested.

## Source Of Truth

Prefer current source/tests/runtime/reproducible commands, then active docs,
canonical and active SPECs, current handoff/state, references, archives, and
finally chat confidence. Read order is routing, not authority. Owner decisions
control scope, risk tolerance, irreversible actions, and acceptance.

If a SPEC spans past-to-present history, current active sections override older
background, roadmap, and archived material. This does not promote an unapproved
draft or let current evidence choose future product scope.

Handoff and save-state are continuity. Promote any decision affecting scope,
behavior, acceptance, risk, evidence, or public claims into SPEC, ADR, claim
registry, TODO, or findings before implementing from it.

## Evidence And Completion

Match the claim to the evidence tier actually obtained: static/local test,
integration/render, live runtime/persisted state, installed artifact, remote
hardware/lab, or production observation. A lower tier cannot unlock a stronger
claim. Label partial, degraded, skipped, simulated, and unverified behavior.

AI-complete/evidence-ready and owner-accepted are separate. Release candidate,
production ready, hardware verified, and tester ready are also separate states.
Owner acceptance never upgrades weak evidence.

## Durable Records

- SPEC: scope, behavior, non-goal, acceptance criterion.
- TODO: current and deferred work.
- Review findings: defects, blocked checks, unresolved risk.
- Implementation notes: spec-unstated implementation judgments.
- ADR: hard-to-reverse, surprising tradeoff.
- Evidence/claim files: claim status and proof.
- Save-state/handoff: resume context only.

Create optional evidence files only for active product, hardware,
compatibility, package, remote, public, or release claims. Do not create control
files solely to make the process look complete.

## Finish Contract

Run the validation commands named by current state or explain the block. Report
changed files, behavior, checks, docs checked, decisions, open findings,
unverified behavior, remaining risk, owner gates, acceptance status, and next
step. Update only control files whose state changed.

Create save-state or handoff when work pauses, changes hands, remains
blocked/partial/unverified, owner direction changes, or reconstruction would be
expensive. Link existing artifacts instead of copying long transcripts.
