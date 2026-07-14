# Known Limitations And Adoption Notes

SDAD expands to SPEC-Directed AI Development. It is a method-agnostic,
tool- and model-neutral, repository-local operating protocol for AI-assisted
development. It improves the visibility and structural consistency of scope,
state, validation, evidence, unresolved work, owner authority, and continuity;
it does not run or schedule agents, prescribe an implementation method, or make
AI output correct by itself.

## Four Control Layers

Keep these layers distinct:

| Layer | What it can establish | What it cannot establish |
| --- | --- | --- |
| Guidance | Markdown records the intended route and rules | technical blocking |
| Deterministic validation | Doctor, tests, and CI check defined contracts | product correctness outside their checks |
| Technical enforcement | permissions, hooks, sandboxing, deny rules, branch protection, release/deploy controls constrain actions | owner acceptance or implementation quality |
| Owner decision | authorization and acceptance record human control | stronger evidence than was actually collected |

Adapter files, prompts, templates, and state are recorded authority or guidance,
not technical enforcement. Put non-negotiable blocking in the applicable
permissions, hooks, sandbox, CI, branch protection, release, or deployment
surface. Tool success and provider enforcement do not prove completion.
Markdown does not technically block tools.

## Doctor Diagnostic Boundary

`sdad doctor` remains checkout-only in 3.2.1. Adapter and no-clone installation
do not install a standalone Doctor into downstream projects. An operator must
resolve a trusted checkout and run:

```text
python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.1 [--json] [--strict]
```

`--require-version 3.2.1` proves only that the invoked program reports the exact
required Doctor version. It does not prove a clean checkout, hash provenance,
command execution, or product correctness. A fork or dirty checkout may retain
the same version string. Use a shell-neutral wrapper that resolves an
operator-configured checkout and always supplies `--strict --require-version
3.2.1` when a repeatable local command is needed.

Doctor is a read-only structural diagnostic. It checks the declared state and
selected control-plane coherence. It does not execute validation commands,
mutate or fix project files, use the network, resolve ambiguous prose, inspect
the full runtime, or replace product tests, security review, release gates, and
owner judgment. Missing state is a completed finding, not an invocation crash.

Doctor version, state schema version, and JSON report schema version are
separate contracts. Existing state-v1 calls keep report schema 1 unless the
caller opts into the guarded/new report lane; guarded state-v2 calls use report
schema 2. JSON `root` and `state_version` may be null when project or state
identity is unavailable.

## Semantic Authority And Lifecycle Boundary

Doctor can verify that `active_spec` names a readable in-repository path. It
does not understand SPEC prose, detect contradictions between multiple SPECs,
prove that a changed SPEC was reaccepted, or decide whether an amendment was
material. It also cannot prove that a validation command ran on the current
commit, integrated branch, environment, or final artifact. These are review,
evidence-freshness, and owner-decision responsibilities.

Doctor also does not discover arbitrary undeclared SPEC files. A clean report
can therefore coexist with a newly supplied or conflicting SPEC that state does
not reference. The agent must distinguish an owner-directed change request from
a merely discovered file, hold affected implementation while authority or
overlap is unresolved, and persist the resulting amendment or packet switch
before resuming. Doctor green cannot make that semantic decision.

Doctor cannot observe live owner messages or determine whether a later message
adds to, narrows, cancels, or replaces prior direction. It therefore cannot
prove that state, delegated work, validation, or an authorization record reflects
the current applicable owner instruction.

SDAD prose also cannot preempt an already running blocking tool, remote job, or
delegated worker. At the next observable boundary, attempt safe cancellation
when the host supports it, launch no follow-up action on the old boundary, and
treat any late result as stale until it is rerouted and revalidated. Report when
the host could not interrupt the work; SDAD does not become an orchestrator by
describing this response.

An accepted boundary is reconstructible only when its durable decision record
pins the packet, active SPEC path and revision, source/artifact identity,
bounded evidence and claim limits, unresolved risk, and final owner decision.
Doctor does not verify that historical revision binding or decide whether a
later edit falls inside the accepted claim boundary.

State v2's `active_packet.status` is one current dominant checkpoint, not a
cumulative ledger for implementation progress, evidence freshness, owner
authorization, and acceptance. Those facts stay in their separate authorities.
Changing the meaning or required axes of state v2 after release would require a
new schema version rather than silently overloading this field.

Doctor deliberately does not scan every archive or interpret arbitrary prose.
It therefore cannot detect an unresolved item merely moved outside an active
section, a closure entry without adequate evidence, stale or contradictory
historical text, SPEC lineage cycles or overlapping supplement precedence,
duplicate `IMPL`/evidence/archive IDs on parallel branches, or
an implementation-notes file that has become semantically overloaded. The
review contract must inspect affected records before closure and integration;
startup routing must not load all history just to compensate for that limit.
`Future / Deferred Findings` is intentionally outside Doctor's active-ledger
parse. It preserves noncurrent split-packet findings without a packet-mismatch;
review must restore them to Active Findings before that packet resumes or is
accepted. A release, production, integration, or public/package-claim route
must also scan deferred findings that intersect its artifact or claim scope;
Doctor green does not perform that semantic gate.
Doctor also does not interpret owner-decision lineage, detect self/cyclic
revision, or reconcile parallel successors for overlapping claim scope. The
review contract must hold affected claims until an owner reconciliation record
resolves the fork and current pointers are updated.

## Tool-Native Features Are Not Protocol Authority

Provider session history, checkpoints, plans, memory displays, task status, and
tool-native doctor/health commands may be useful convenience or diagnostics.
They are not `sdad-state.yaml`, the state-declared current handoff, or `sdad
doctor`, and they do not replace SDAD owner gates. When a provider surface and
repository state disagree, inspect current source/tests and the repository
authority chain before proceeding.
Tool-native session and checkpoint diagnostics are not SDAD authority.

## Date-Scoped Handoff Sequence Boundary

New handoffs use `YYYY-MM-DD-HNNNN-topic.md`. The zero-padded `HNNNN` is scoped
to that date: use the next known ID for the date and restart at `H0001` on a new
date. The full date-plus-ID path is the identity; neither date nor ID establishes
currentness. Existing unnumbered handoffs remain valid, and only
`sdad-state.yaml#current_handoff` declares the current checkpoint.

This naming contract is not a centralized allocator. Doctor validates the
state-declared handoff's path, readability, size, and packet marker, but it does
not allocate IDs, validate filename-to-ID agreement, scan handoff history, or
detect duplicate date-plus-ID pairs. Parallel branches can therefore choose the
same date-scoped ID; resolve that collision before merge by changing the
filename, internal ID, and state pointer together.

## Evidence Claim Ladder

- Doctor green supports only the claim that its structural checks passed.
- A task benchmark supports only the specific task under its recorded conditions.
- Only a controlled comparison supports an improvement claim for SDAD 3.2 over
  another baseline.

Repository unit/regression tests establish only the package behaviors and
contracts they exercise. They do not establish general gains in productivity,
quality, safety, cost, or completion rate. Public method claims need
representative tasks, fresh or held-out evaluation, semantic review, repeated
trials when nondeterminism matters, and explicit limitations.

## Validator Maintainability

`scripts/validate_repo.py` is intentionally strict and remains a large change
surface. Pure contract modules and focused tests cover state keys, routes,
agent-startup budgets, adapter parity, links, Action pins, install hashes, and
other stable interfaces. Explanatory prose should be checked by concepts or
section structure; exact strings should be reserved for schemas, enums,
filenames, headings, packet markers, finding IDs, and synchronized copy prompts.

Before release run at least:

```text
python scripts/render_agent_surfaces.py --check
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

## Installer Test Coverage

Local smoke tests cover adapter placement, overwrite refusal, forced
replacement, linked-path rejection, hard-link isolation, Windows read-only
targets, full skill payload parity, and transaction cleanup on Bash and
PowerShell. CI runs on Ubuntu and Windows. These tests do not prove every shell,
policy, concurrent filesystem change, path, permission, WSL, or managed-device
edge case. Automated repository tests live under `tests/`; do not create a
separate `test/` tree.

The v3.2.1 local Windows release gate ran 392 tests, with three
privilege-dependent permission/link cases skipped. Those skips disclose
unexercised local conditions; they are not pass evidence for those scenarios.

## Raw URL Reproducibility

The executable no-clone instructions are pinned to the stable v3.2.1 baseline
at full 40-character commit SHA
`f173aa398562d6a9d86b941dc79f75f9381148f4`. Each downloaded adapter is verified
with SHA-256. `install-sources.json` is the revision/path/hash contract.

A commit ID is immutable; a tag is readable but may move unless repository
policy prevents it. Checksums published in the same repository cannot protect
against every maintainer-account, TLS, local trust-store, or repository-access
failure. Do not mix `main` and a pinned revision unless the difference is
intentional and recorded. The current working tree is never an integrity pin.

## Collaboration Signals

Public issue and pull-request history may be sparse. Use current code and docs,
`CHANGELOG.md`, release notes, field notes, active findings, and ADRs as the
public record. Historical field tests describe the version and conditions they
actually exercised; they are not current 3.2 behavior claims.

## Example Depth

`examples/minimal-project/` demonstrates the minimum topology, not a complete
product or proof of effectiveness. Real adopters must create project-specific
SPEC, TODO, validation, evidence, owner-gate, and optional handoff records.
