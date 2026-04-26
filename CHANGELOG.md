# Changelog

## 1.0.3 - 2026-04-27

- Added scale selection so agents choose One-shot Prompt, Mini SDAD, Standard
  SDAD, or Full SDAD before creating files.
- Added `docs/mini-sdad.md` and `templates/mini-sdad/MINI-SDAD.md` for small
  projects that need one instruction file without the full workflow.
- Updated README, getting-started, no-clone, fit assessment, localized READMEs,
  and the Codex skill with scale-first guidance.
- Expanded validation to preserve the Scale Gate and Mini SDAD baseline.

## 1.0.2 - 2026-04-27

- Replaced generic no-clone adapter wording with exact raw adapter URLs and
  target paths for Codex, Claude Code, Cursor, Copilot Chat, and generic AI
  agents.
- Added fetch-evidence requirements so AI agents must show the source URL and
  first 10 fetched lines before saving an adapter.
- Added fail-closed guidance: if an agent cannot fetch the real adapter, it must
  stop instead of inventing adapter content.
- Updated validation and the Codex skill to preserve deterministic adapter
  installation rules.

## 1.0.1 - 2026-04-26

- Added the README infographic asset for the SPEC-driven AI development loop.
- Clarified README and GitHub About positioning around Codex, Claude Code,
  Cursor, Copilot Chat, and generic AI coding agents.

## 1.0.0 - 2026-04-26

- Promoted SPEC-Driven AI Development to its first stable public release.
- Stabilized the control-layer positioning for owner-supervised,
  SPEC-driven, multi-agent, evidence-based AI development.
- Included beginner-first README onboarding, no-clone setup, multi-tool
  adapters, Codex skill packaging, project control templates, method docs, and
  repository validation as the 1.0 baseline.

## 0.5.3 - 2026-04-26

- Promoted beginner onboarding in the README: no terminal, Git, Python, or Codex
  skill required for the first path.
- Expanded no-clone and getting-started docs with beginner prerequisites,
  Codex skill explanation, and success checks.
- Updated the Codex skill to prefer the no-clone AI-agent prompt for new users
  before suggesting terminal commands or script installation.
- Expanded validation to preserve beginner-friendly onboarding sections.

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
