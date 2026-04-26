# Changelog

## 0.5.2 - 2026-04-26

- Added `docs/no-clone-quick-install.md` with an AI-agent handoff prompt and
  one-paste PowerShell/Bash adapter installers.
- Promoted no-clone setup into the first visible README section so new users can
  start without cloning the repository.
- Updated getting-started paths for no-clone and cloned-repository setup.
- Expanded validation to require the no-clone quick install guide.

## 0.5.1 - 2026-04-26

- Added `docs/getting-started.md` as a first-use guide for new adopters.
- Linked the getting-started guide from the canonical README.
- Expanded validation to require the getting-started guide and its setup paths.

## 0.5.0 - 2026-04-26

- Repositioned the canonical README around the "control layer for AI coding"
  framing.
- Reworked README flow around problem, positioning, core idea, loop,
  differentiation, usage, audience, and non-goals.
- Added validation checks for the README positioning sections.

## 0.4.0 - 2026-04-26

- Added Korean, Chinese, and Japanese guide READMEs linked from the canonical
  English README.
- Added language policy guidance: English docs remain canonical, localized
  READMEs are orientation guides.
- Expanded validation to check localized README presence and language links.

## 0.3.0 - 2026-04-26

- Added anti-patterns, fit assessment, diagrams, and ADR template docs.
- Reorganized implicit rules into Core 5 and Extended 15.
- Updated prompts, README, templates, and validation to route agents toward
  ADRs, anti-pattern review, fit checks, and diagrams.

## 0.2.0 - 2026-04-26

- Added multi-tool adapters for Codex, Claude Code, Cursor, GitHub Copilot, and
  generic AI coding tools.
- Added `docs/tool-adapters.md` with adapter paths and usage guidance.
- Added PowerShell and Bash adapter installer scripts.
- Expanded validation to cover adapter files.

## 0.1.4 - 2026-04-26

- Removed specific source project names from public docs, prompts, templates,
  skill references, and validation checks.
- Renamed field notes to generic documentation-governance and
  release-governance method notes.

## 0.1.3 - 2026-04-26

- Added `docs/implicit-rules.md` to make obvious-but-easy-to-miss project rules
  explicit.
- Added skill reference `implicit-rules.md` for Codex project bootstrap and
  review workflows.
- Updated prompts and templates to require explicit handling of hidden
  assumptions, partial/degraded states, unverified behavior, and owner decisions.
- Expanded validation to check the implicit-rules package.

## 0.1.2 - 2026-04-26

- Added current-over-historical SPEC precedence rules so newer active SPEC
  sections override older timeline/history sections.
- Updated prompts, templates, field patterns, and validation checks to require
  agents to identify the current active SPEC path before implementation/review.

## 0.1.1 - 2026-04-26

- Added anonymized field notes.
- Added a combined pattern catalog for field-proven controls.
- Added `docs/Repository-Operating-Rules.md` templates.
- Updated prompts, templates, and the Codex skill with version-lane, risk-domain, release-gate, and documentation-consistency rules.
- Expanded repository validation to cover the new method docs.

## 0.1.0 - 2026-04-26

- Initial public package for SPEC-driven AI development.
- Added reusable prompts for kickoff, review, and handoff.
- Added Codex skill `ai-spec-project-start`.
- Added project control file templates.
- Added minimal example project.
- Added repository validation script and GitHub Actions workflow.
