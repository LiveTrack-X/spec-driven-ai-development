# Known Limitations And Adoption Notes

This page names the current limits of SPEC-Driven AI Development so teams can
adopt it deliberately instead of treating the package as stronger than it is.

## Enforcement Scope

SDAD separates guidance from guarantees. Adapter files, prompts, templates, and
field notes can steer an AI coding session, but they cannot enforce behavior by
themselves. Non-negotiable behavior still belongs in CI, required tests, hooks,
permissions, deny rules, branch protection, release gates, or deployment
controls.

The repository validator protects important documentation, template, adapter,
and link contracts. It is not a substitute for downstream product tests,
security review, or owner acceptance.

## Regression Evidence And Method Claims

Repository regression tests do not establish SDAD effectiveness or comparative
gains in productivity, quality, safety, cost, or completion rate. They establish
only the package behaviors and contracts they exercise. Across studies, mixed productivity results are not consensus:
task shape, tool generation, experience, repository, and chosen metric can
change the observed outcome.

The primary sources in [Research Foundations](research-foundations.md) inform
bounded design decisions; they do not validate SDAD as a method. Public claims
need representative tasks, held-out or fresh evaluation, repeated trials when
nondeterminism matters, semantic review, and explicit limitations. A benchmark,
vendor guide, subjective speed report, or copied percentage is not sufficient.

## Validator Maintainability

`scripts/validate_repo.py` is intentionally strict and currently acts as the
main repository contract test. Agent-startup budgets, state keys, routes, and
README entry points now live in the pure
`scripts/sdad_validator/agent_experience.py` module. Adapter parity is checked
by `scripts/render_agent_surfaces.py`. Focused tests also cover Markdown/MDC
links, unittest discovery, Action pins, install-source hashes, and the diagram
CSP. The remaining legacy documentation validator is still a large change
surface. When changing method docs, templates, or required phrases:

- keep changes small and tied to a named SDAD surface,
- add or update focused tests when behavior changes,
- run `python scripts/validate_repo.py`,
- run `python -m unittest discover -s tests`,
- run `git diff --check` before release.

Remaining improvement: continue splitting `validate_templates()` by stable
semantic surface and replace prose snippets with headings, schemas, routes, or
manifests where that reduces maintenance without weakening checks.

## Installer Test Coverage

This repository includes smoke tests for the local adapter and Codex skill
installers. They cover every adapter route, expected file placement, overwrite
refusal, forced replacement, linked-path rejection, hard-link isolation,
Windows read-only targets, full skill payload parity, and transaction cleanup
on Bash and PowerShell. CI runs the suite on Ubuntu and Windows. The tests still
do not prove every shell, policy, concurrent filesystem change, path, or
permission edge case.

Automated repository tests live under `tests/`; do not create a separate
`test/` tree.

Teams with stricter deployment requirements should add their own install smoke
tests in the target environment, especially for locked-down Windows policies,
managed developer machines, WSL boundary cases, and paths with organization
specific access controls.

## Raw URL Reproducibility

The executable no-clone instructions pin the stable v3.0.0 baseline with a full
40-character commit SHA and verify each downloaded adapter with SHA-256. A
commit ID is immutable; a readable tag can move unless repository policy makes
it immutable. The one-paste installers download to a temporary file, verify it,
and only then publish it without clobbering a target that appeared concurrently.

That pinned baseline declares `progressive_control_plane=true` and includes the
compact state -> INDEX -> on-demand runtime. No-clone users should still follow
the installed baseline rather than combine it with changing `main` content. The
current working tree must not be used as an integrity pin.

`install-sources.json` is the single revision/path/hash contract. Repository
validation recomputes every listed hash from the pinned Git object and checks
that the user-facing install surfaces carry the matching URL and checksum.

Use `/main/` only when changing, unpinned instructions are intentional. Record
the chosen revision in setup notes or a handoff. Do not mix `main` and a pinned
revision in the same install unless the difference is intentional and
documented. Repository access, TLS, local trust stores, and a compromised
maintainer account remain outside what a checksum published in this repository
can fully protect.

## Collaboration Signals

This public repository may not expose a large issue or pull-request history.
Use `CHANGELOG.md`, field notes, release notes, and the current docs as the
primary public design record. Teams adopting SDAD should keep their own
roadmap, known limitations, ADRs, review findings, and owner decisions in the
target project.

## Example Depth

`examples/minimal-project/` demonstrates the minimum control-file topology. It
is not a full worked product example. Use it to understand file placement and
state-to-INDEX progressive routing, then create project-specific SPEC, TODO,
evidence, and handoff content from the real product context.

Future improvement: add a compact worked example that closes one small finding,
records implementation evidence, and shows the owner checkpoint without turning
the example into a large sample application.
