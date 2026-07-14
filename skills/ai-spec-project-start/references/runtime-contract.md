# SDAD Runtime Contract

Read this reference before creating or changing an SDAD control surface. It is
the semantic contract shared by the bootstrap skill, installed adapters, and
project templates.

## Scale Truth Table

Infer scale from the request and repository before asking the owner. The old
five kickoff questions may remain an internal decision aid; they are not a
required questionnaire.

- One-shot: current request only; create no persistent files.
- Mini: one bounded unit and one tool instruction file.
- Standard: multiple workers or persistent state, including a packet that only
  inspects, documents, or tests a protected area.
- Full: Standard plus named owner gates when a packet changes, accepts, or executes a protected action.

Re-evaluate scale when duration, collaboration, evidence, or risk changes. Use
the smaller scale only when no continuity need or protected-action gate is lost.

## Intent Route

Infer intent from plain language and repository state:

- check/review/audit/find bugs: review and report; do not implement unless the
  request also includes a change;
- implement/build/fix/match the spec: active-SPEC implementation;
- release/publish/tag/deploy/migrate: protected-action route with owner gates;
- docs/README/FAQ/guide: affected documentation route;
- handoff/continue later/lost context: continuity route;
- borrow/reference/can we adopt an idea: reference-intake and parity route;
- adopt/use/implement this: current change-request route;
- asks too often/runs ahead: execution-scope and packet-boundary tuning.

The current applicable owner instruction supersedes an older owner direction.
On redirect, stop affected local/delegated work, re-enter Plan -> Route, and
reconcile SPEC/state before stateful implementation. Old-boundary outputs stay
stale until revalidated. Review/compare/explain/reference-only intent is read-only;
a draft request may write only the draft, not activate implementation scope.

An explicit current owner command authorizes only its named direction, acceptance,
or protected action for the stated boundary; persist it without re-asking. It
does not waive evidence, prerequisites, tool policy, or another protected action.
A question, hypothetical, quotation, negation, or review/reference-only request
does not authorize the action it mentions; classify the whole utterance.

Treat carefully/thoroughly as inspection depth, fully/end-to-end as continuing
to evidence-ready inside approved scope, minimal/quickly as compression, and
commit and wait as neither push nor release. Compose intents only when they fit
one packet without changing scope, risk, claim, or owner gates.

## Steady-State V2 Invariants

State v2 is only for Standard or Full. It requires `version: 2`, `scale` as
`standard | full`, `execution_scope: unit | packet`, an `active_packet`,
`validation_for` equal to that packet ID, `owner_gates`, `validation`, and
`routed_docs`. `current_handoff` is optional. V2 does not use `intensity` or
`autonomy`, and unapproved execution is represented by packet and owner-gate
state rather than another scope value.

One-shot and stateless Mini do not migrate. A deliberately stateful Mini remains
on v1. New Standard/Full bootstrap writes v2 only. Multi-packet execution needs
an explicitly owner-approved packet list; it is never session scope.

The operating loop is Plan -> Route -> Implement -> Verify -> Report, with owner
gate and handoff branches only when triggered.

## Authority And Enforcement Boundaries

Keep guidance, deterministic validation, technical enforcement, and owner
decision as separate layers. Markdown records authority and guidance; it does
not technically block tools or actions. Technical enforcement comes from the
host, tool, runtime, or environment rather than from prose alone.

Tool-native session, checkpoint, and Doctor features are convenience
diagnostics. They are not SDAD state, handoff, or Doctor authority and do not
replace the repository control plane.

## Execution Scope And Stop Contract

- Mini defaults to one unit without state v2.
- Standard defaults to the current packet.
- Full defaults to the current packet plus applicable named owner gates.

Execution scope does not grant permission for release, migration, destructive
actions, sensitive data, auth, money, security, rollback, or production claims.
Those remain owner gates.

Do not pause for owner input after every micro-task or internal review-worthy
unit. Obey a current owner stop/redirect. Pause for input when scope expansion
is unrequested or ambiguous, a risk/claim gate or irreversible action remains
unauthorized, an owner-controlled tradeoff is unresolved, verification is
blocked, or evidence conflicts with the requested plan.

A later owner restriction, cancellation, or revocation immediately ends the affected
authorization/execution boundary. Persist it before any further protected action;
an older record cannot keep authorization. Without replacement, use `deferred`,
record `resume only by explicit owner reactivation`, and never auto-resume it.

## Progressive Control Plane

The bootstrap, install, or upgrade prompt is one-time, not a per-session prompt.
Ordinary sessions begin with:

For Standard or Full, read in this order:

1. the installed tool adapter;
2. `sdad-state.yaml`;
3. `docs/INDEX.md`;
4. current source/tests/runtime state;
5. only the docs and policy/playbook content targeted for the packet.

Do not load the full rulebook, archives, old handoffs, historical SPEC sections,
or optional evidence files by default. Keep the fixed startup plane below the
budgets enforced by repository tests.

`routed_docs` is an eligible selection set, not a read-all list. Current intent
selects the routed path, heading, active section, or targeted match; reports name
only documents actually read. Inspect current owner-named input even if stale
routes omit it; if adopted, reconcile authority/routes before implementation.

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

Assign authority by fact type. Current source/tests/runtime/reproducible
commands establish observed behavior. The state-declared `active_spec` is the
single normative entrypoint for intended scope, behavior, and acceptance criteria. State
and active ledgers own current execution and unresolved work. Owner-decision
records control only their declared authorization or acceptance. Handoffs own
continuity pointers only. A current applicable owner instruction can interrupt
or redirect work immediately; persist accepted intent in SPEC/state before
affected stateful implementation. Planned SPECs, references, archives,
filenames, dates, and old/provider-retained chat memory cannot activate requirements.

`SPEC-COMPLETE.md` is an integrated baseline, not immutable or automatically
active. A SPEC supplied as current requirements is a change request unless the
owner limits it to review/draft/reference; reconcile it before affected work. A merely
discovered SPEC gains no authority from metadata and remains a proposal only
when nonconflicting. Incorporate a same-boundary change into a non-terminal
packet and invalidate affected evidence; use a new, never-reused packet and
fresh validation for a material or post-acceptance change. An ADR records
rationale and tradeoffs; it cannot silently override normative SPEC content.

If a SPEC spans past-to-present history, current active sections override older
background, roadmap, and archived material. This does not promote an unapproved
draft or let current evidence choose future product scope.

Handoffs provide continuity and link to authorities; they do not replace live
state or behavior authority. Legacy v1 save-state is migration input only.
Route scope, behavior, and acceptance-criteria changes to the active SPEC;
durable architecture rationale to an ADR; claim/evidence status to its ledger;
unresolved work to TODO/findings; and owner authorization or result acceptance
to one durable owner-decision record. Link these authorities elsewhere.

`active_packet.status` is the current dominant checkpoint, not a cumulative
ledger. Re-enter Plan -> Route when source, SPEC, dependency, environment,
artifact, owner gate, merge result, or external evidence changes. Keep the same
packet only for the same unfinished objective and acceptance boundary;
otherwise create a new packet. Validate the integrated tree and final artifact.

## Evidence And Completion

Match the claim to the evidence tier actually obtained: static/local test,
integration/render, live runtime/persisted state, installed artifact, remote
hardware/lab, or production observation. A lower tier cannot unlock a stronger
claim. Label partial, degraded, skipped, simulated, and unverified behavior.

Evidence-ready and owner-accepted are separate. Release candidate, production
ready, hardware verified, and tester ready are also separate states. Owner
acceptance never upgrades weak evidence.

SDAD Doctor proves structural consistency only. It does not run project checks,
prove product correctness, enforce permissions, or grant owner acceptance. Run
and report project validation separately with its bounded claim.

## Durable Records

- SPEC: scope, behavior, non-goal, acceptance criterion.
- TODO: current and deferred work.
- Review findings: defects, blocked checks, unresolved risk.
- Implementation notes: spec-unstated implementation judgments.
- ADR: hard-to-reverse, surprising tradeoff.
- Evidence/claim files: claim status and proof.
- Handoff: cross-session resume links only.

Create optional evidence files only for active product, hardware,
compatibility, package, remote, public, or release claims. Do not create control
files solely to make the process look complete.

## Finish Contract

Run the project validation commands named by current state or explain the block.
Report Doctor and project evidence separately, including changed files,
behavior, checks, claim limits, routed documents actually read, open findings,
remaining risk, owner gates, acceptance status, and next step. Update only
control files whose state changed.

Create a handoff only when another session, tool, person, or machine needs actual
continuity and reconstruction would otherwise be costly. Reconcile direction
first; a stop, redirect, block, or partial result alone does not require a
handoff. Link existing authorities instead of copying their contents.
