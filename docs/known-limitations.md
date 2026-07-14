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

## Tool-Native Features Are Not Protocol Authority

Provider session history, checkpoints, plans, memory displays, task status, and
tool-native doctor/health commands may be useful convenience or diagnostics.
They are not `sdad-state.yaml`, the state-declared current handoff, or `sdad
doctor`, and they do not replace SDAD owner gates. When a provider surface and
repository state disagree, inspect current source/tests and the repository
authority chain before proceeding.
Tool-native session and checkpoint diagnostics are not SDAD authority.

## Logical Handoff Sequence Boundary

New handoffs use `YYYY-MM-DD-HNNNN-topic.md`. The zero-padded `HNNNN` is a
repository-logical sequence; the date is descriptive and cannot establish
order or currentness. Existing unnumbered handoffs remain valid, and only
`sdad-state.yaml#current_handoff` declares the current checkpoint.

This naming contract is not a centralized allocator. Doctor validates the
state-declared handoff's path, readability, size, and packet marker, but it does
not allocate IDs, validate filename-to-ID agreement, scan handoff history, or
detect duplicate sequence IDs. Parallel branches can therefore choose the same
next ID; resolve that collision before merge by changing the filename, internal
ID, and state pointer together.

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
