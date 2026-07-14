# Changelog

## Unreleased

- Changed the expanded public name from `SPEC-Driven AI Development` to
  `SPEC-Directed AI Development` so the name describes direction and boundary
  rather than a prescribed implementation methodology.
- Standardized the public descriptor as "a repository-local operating protocol
  for AI-assisted development" and made its method-, tool-, model-, harness-,
  and orchestration-neutral boundary explicit across current documentation and
  agent surfaces.
- Kept the repository slug, file paths, pinned v3.2 sources, release notes, and
  historical records unchanged for compatibility and provenance.
- Removed internal Superpowers SDD plans, specifications, and task reports from
  the distributed tree, and ignored `/.superpowers/` and `/docs/superpowers/`
  so implementation coordination artifacts do not leak into future releases.

## 3.2.0 - 2026-07-12

- Added state schema v2 with one executable active packet, exact
  `execution_scope: unit | packet`, packet-owned validation, and optional
  packet-bound handoff continuity while preserving the state-v1 contract.
- Upgraded the checkout-only Doctor to 3.2.0 with explicit version guarding,
  separate Doctor/state/report version domains, report-schema compatibility,
  and deterministic INDEX, handoff, packet, TODO, and finding coherence checks.
- Added a read-only migration preview that maps legacy state without silently
  rewriting repositories, and documented conditional owner-authorization reuse
  and expiry.
- Tightened agent startup to adapter -> state -> INDEX plus one intent-selected
  route, with `routed_docs` treated as an eligible selection set rather than a
  read-all list.
- Reworked public terminology around scale, execution scope, owner gates,
  validation, evidence-ready status, and owner acceptance; kept v3.1 terminology
  in migration and historical surfaces.
- Replaced the README overview artwork and kept the expanded Copy-Paste Start
  Prompt byte-identical to No-Clone Option 1.
- Pinned all seven no-clone sources to immutable behavior baseline
  `b433b4cbf490bd875a40b76127abefbefed3f243` with SHA-256 verification.
- Added task-scoped fresh-context evidence and release validation without
  claiming comparative productivity or general effectiveness.

## 3.1.0 - 2026-07-10

- Added the checkout-only, read-only `sdad doctor` diagnostic for stateful
  Standard and Full projects, with deterministic checks, human and versioned
  JSON output, strict warning policy, and explicit exit `0`/`1`/`2` semantics.
- Added a self-contained Gemini CLI adapter, local installer routes, Mini and
  no-clone target mapping to repository-root `GEMINI.md`, and parity coverage
  across all seven pinned instruction sources.
- Hardened state parsing, path confinement, packet/review coherence, owner-gate
  diagnosis, shared bounded reads, diagnostic identities, and runtime severity
  contracts without making Doctor execute declared validation commands.
- Added cross-model guidance for treating embedded instructions in external
  content and tool output as untrusted evidence, requiring observed results and
  task-specific semantic validation rather than accepting syntactic success.
- Added progressive-context, bounded-feedback, fresh-context review, and
  evaluation guidance with an explicit research matrix of 25 official or
  primary sources and no claim that those sources establish SDAD effectiveness.
- Pinned the v3.1.0 no-clone baseline to
  `1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa`, refreshed SHA-256 values from
  immutable Git blobs, and kept README Copy-Paste Start Prompt exactly expanded
  and synchronized with no-clone Option 1.
- Documented compatibility, migration, local verification, three
  Windows privilege-dependent skips, provider-guidance limits, and the boundary
  that a clean Doctor report does not prove correctness, effectiveness, release
  approval, or owner acceptance.

## 3.0.0 - 2026-07-10

- Reworked Standard/Full startup into an agent-first progressive control plane:
  a self-contained adapter, compact `sdad-state.yaml`, routing-only
  `docs/INDEX.md`, current source/tests, and one on-demand policy or playbook
  path instead of mandatory full-rulebook reads.
- Added enforced line and character budgets for always-loaded agent surfaces,
  active-state schema and route validation, one canonical README start path,
  and focused regression tests for context-cost drift.
- Hardened validation against malformed state enums/collection shapes, skipped
  source/tests routing, empty or import-broken test modules, and unpinned
  actions hidden in named workflow steps.
- Reduced the project agent template from roughly 380 to 106 lines, the INDEX
  template from 218 to 75 lines, and the bootstrap skill from roughly 790 to
  251 lines while preserving scale, autonomy, sensitive-data, owner-gate,
  evidence, and completion contracts.
- Standardized the active-state intensity vocabulary on Low/Medium/High and
  made the Standard/Full boundary explicit: inspecting, documenting, or testing
  a Q5 area is Standard minimum; changing, accepting, or executing its gate is
  Full with owner control.
- Split procedural operating guidance into on-demand context/data, work-packet,
  evidence/risk, documentation/handoff, and advanced-extension playbooks; kept
  the repository rulebook policy-only.
- Added `scripts/render_agent_surfaces.py` so five self-contained tool adapters
  are rendered deterministically from one canonical runtime kernel and checked
  for drift without changing the single-file installer contract.
- Made `install-sources.json` the revision/path/hash contract and no-clone
  Option 1 the canonical copy-paste prompt, with the README mirror generated
  and checked for exact parity while retaining fail-closed verification.
- Added a security policy for reporting unsafe installer, adapter, raw fetch,
  or security-boundary guidance issues.
- Added known limitations and adoption notes covering validator
  maintainability, installer smoke-test scope, commit-pinned raw URLs, public
  collaboration signals, and example depth.
- Added installer smoke tests for Bash and PowerShell adapter installers,
  including all adapter routes, overwrite refusal, forced replacement,
  linked-path escape, hard-link isolation, and Windows read-only targets.
- Made Codex skill installation non-destructive by default and staged forced
  replacements before swapping the existing installation.
- Pinned no-clone downloads to an immutable commit, added SHA-256 verification,
  rejected linked destination paths, and moved verified temporary downloads
  into place atomically.
- Added `install-sources.json` as the canonical revision/path/hash contract and
  made validation check every entry against its pinned Git blob and
  user-facing install surfaces.
- Added a machine-checked no-clone runtime capability; the v3.0.0 manifest
  declares `progressive_control_plane=true` and pins its runtime sources.
- Added a Cursor-specific Mini SDAD template with always-applied MDC metadata.
- Added CI coverage on Ubuntu and Windows with Python 3.10 and 3.12, pinned
  action commits, read-only permissions, syntax checks, and Dependabot updates.
- Added Markdown/MDC fragment validation, titled and balanced-parenthesis link
  support, actual unittest discovery, structural Action pin validation, and a
  local-only CSP contract to the repository validator.
- Added a sensitive-data authorization boundary to installed adapters,
  templates, kickoff/review/handoff prompts, and no-clone entry paths, separate
  from context-size limits.
- Added a scale/tool gate to the kickoff prompt so One-shot and Mini projects do
  not receive the Standard/Full control-file set.
- Documented `tests/` as the single repository test directory.
- Preserved the existing README infographic, added an editable, versionless
  progressive-control-plane companion visual, and aligned Mermaid and Archify
  diagrams to the state -> INDEX -> source/tests -> one-routed-path contract.
- Made project control templates tool-neutral, allowed every documented
  autonomy level from 0 through 4 in active state, and corrected Mini
  escalation so normal one- or two-signal Mini projects do not self-promote.
- Tightened release contracts around manifest metadata, local-only CSP source
  directives, active-packet state, and diagram source/render parity.
- Canonicalized repository-root path comparisons so Markdown link validation
  remains correct when Windows runners expose the same directory through an
  8.3 short-path alias.
- Kept the README copy-paste start prompt permanently expanded, made no-clone
  Option 1 its exact canonical source, and added sync/parity contracts that
  reject collapsible or divergent prompt markup.

## 2.1.0 - 2026-07-09

- Added an Owner Quick Adoption Guide for introducing SDAD to users or teams
  without requiring them to learn the whole framework first.
- Added a compact AI Work Loop guide with Fast, Normal, Full, and Full + Gate
  loops, one-line evidence contracts, docs sync rules, stop conditions, and
  compact report format.

## 2.0.2 - 2026-07-09

- Replaced the README infographic with the SDAD 2.0 control-surface overview
  image.

## 2.0.1 - 2026-07-09

- Restored executable git modes for the Bash installer scripts and documented
  `bash ./scripts/...` fallbacks for checkouts that lose executable bits.
- Added repository validation for installer script presence and executable
  git modes.

## 2.0.0 - 2026-07-09

- Added the Repository Control Surface field note and pattern: always-loaded
  guidance, routed rules, on-demand procedures, isolated exploration, enforced
  guarantees, and reviewed project memory.
- Added the Cost-Aware Agent Routing field note and pattern for lean execution,
  Executor-Advisor checkpoints, Orchestrator-Worker packets, and bounded Loop
  Engineering with explicit budgets, evidence boundaries, stop rules, and owner
  gates.
- Validated SDAD on a separate sandbox across feature, bugfix, project
  validation, and local readiness loops; tightened create-on-demand wording for
  optional evidence templates and added loop-end smoke guidance.
- Repeated the sandbox through an additional bug/readiness cycle and tightened
  loop-end guidance so evidence-ready gates check unfinished active work
  packets, not only historical markers.
- Validated an installable product artifact in a clean environment and added
  installed-artifact smoke guidance for packaging or distribution claims.
- Added a Reference Parity Review Gate for rebuilds, ports, demos, designs, and
  reference-derived work so evidence-ready checks preserve essential source
  behavior without cloning old implementations.
- Clarified evidence-tier claim boundaries and the Small Project Compression
  Rule so local tests, browser renders, live runtime, persisted state, remote
  hardware, and production evidence cannot overclaim, and small packets can end
  with one evidence-ready summary instead of template sprawl.

## 1.3.0 - 2026-07-06

- Added a Meta-Harness field note that adapts harness optimization,
  retrieval/memory tuning, context selection, and repeated evaluation loops into
  SDAD's advanced-extension fit gate.
- Added the Slice-First Evidence Loop pattern for feature delivery: one
  vertical slice, JIT clarification for unresolved decisions, a practical
  failing test/check first, evidence-ready results, and owner acceptance
  separation.
- Strengthened fit assessment, operating intensity, pattern catalog, and the
  Codex skill so harness optimization and slice-first execution stay bounded by
  evidence, budget, leakage, and owner adoption gates.
- Updated the README infographic and added GitHub funding/Sponsors surfaces.

## 1.2.0 - 2026-06-29

- Added reusable product evidence templates: Evidence Matrix, Claim Registry,
  Artifact Contracts, Work Packet State, and Remote Evidence Import /
  Quarantine workflows.
- Added a product evidence flag to onboarding, fit assessment, no-clone setup,
  the Codex skill, and tool adapters so hardware, compatibility, packaging,
  remote tester, external lab, and release claims route to the right evidence
  surfaces without automatically forcing Full SDAD.
- Separated evidence status, work-packet state, and owner acceptance so
  `evidence_received` or `software_verified` cannot collapse into production
  readiness or owner acceptance.
- Expanded repository validation to preserve the new evidence templates,
  onboarding routes, adapter rules, and status-boundary invariants.

## 1.1.7 - 2026-05-22

- Moved the README `Copy-Paste Start Prompt` directly after the user-guide
  entry so first-time users find the executable prompt before deeper
  explanation sections.
- Adapted OpenAI Codex usage practices into SDAD-native issue-shaped prompts,
  environment improvement loops, controlled task queues, and optional
  multi-candidate review.

## 1.1.6 - 2026-05-21

- Added `docs/user-guide.md` as a human-facing situation guide and FAQ so users
  can choose One-shot, Mini, Standard, or Full SDAD without reading the
  copy-paste execution prompt.
- Reworked the README entry path so the copy-paste prompt is clearly presented
  as an execution block, with feature explanation and situation-based guidance
  before it.
- Added localized README situation-guide summaries and links to the new user
  guide.
- Added a symptom-based troubleshooting FAQ for common owner problems such as
  too many approval requests, vague done claims, excessive docs, context loss,
  and risk-gate confusion.
- Mirrored the troubleshooting FAQ summary in the Korean, Japanese, and Chinese
  README orientation guides.
- Merged the "asks approval too often" and "runs ahead too much" FAQ into one
  autonomy-level troubleshooting guide and made the main README user-guide link
  a first-screen entry point.
- Added localized user guide pages for Korean, Japanese, and Chinese, and
  routed localized READMEs to the matching user guide.
- Added SDAD-native guidance for layered context, before/after change guards,
  task-size heuristics, and practical evidence examples after reviewing
  compatible context-engineering patterns from `popup-studio-ai/bkit-codex`.
- Added Natural-Language Intent Routing so users can say "review this",
  "implement the spec", "release this", "update the docs", or "create a
  handoff" without knowing SDAD command names or skill triggers, with localized
  user-guide and README coverage.

## 1.1.5 - 2026-05-20

- Added SDAD-native clarification checkpoints: inspect repository evidence
  first, then ask only the next blocking owner question with a recommended
  answer.
- Added optional domain-language routing for projects where terminology drift
  affects implementation, review, tests, or owner decisions.
- Tightened ADR guidance so durable records are reserved for hard-to-reverse,
  surprising, real-tradeoff decisions, while smaller spec-unstated choices stay
  in implementation notes.
- Strengthened handoff guidance to reference existing artifacts by path or URL
  instead of duplicating long SPECs, ADRs, TODOs, logs, or evidence files.

## 1.1.4 - 2026-05-20

- Added implementation-notes guidance so AI sessions record spec-unstated
  implementation judgments, changes, compromises, and verification impact
  without turning private reasoning into a transcript.
- Added `docs/implementation-notes.md` as the Standard/Full SDAD decision-log
  surface and clarified that Mini SDAD should include short implementation
  notes in evidence-ready summaries instead of creating another control file by
  default.
- Updated adapters, prompts, templates, and validation checks so
  implementation notes stay connected to handoff, TODO, review findings, ADRs,
  and context-stability rules.

## 1.1.3 - 2026-05-16

- Added context-stability and bounded-read guidance so large live-state files,
  logs, generated artifacts, private data, and archives do not flood fresh AI
  chat sessions.
- Added live-state size-budget guidance for keeping active state files compact
  while preserving old material in archive/history files.
- Added soft size triggers and tool-input hygiene guidance so first-read loops
  check context size before loading routed files.
- Updated adapters, prompts, templates, and validation checks to preserve the
  bounded-read rule without adding cleanup automation.

## 1.1.2 - 2026-05-13

- Clarified release status wording as a stable documentation/package release
  and noted that effectiveness depends on project fit, owner discipline, and
  evidence quality.
- Added local Markdown link existence checks to repository validation without
  adding external URL checks, installer dry-runs, template snapshots, or CLI
  scaffolding.

## 1.1.1 - 2026-05-13

- Added an Advanced Extension Fit Gate for eval-driven workflows such as harness
  optimization, self-improving loops, retrieval/memory tuning, and repeated
  evaluation automation.
- Added Evaluation Leakage and Budget Fog anti-patterns to separate search
  evidence from owner acceptance evidence and require concrete budgets.

## 1.1.0 - 2026-05-08

- Added Standard/Full SDAD operating intensity guidance with High, Medium, and
  Low modes, Baseline Freeze posture, Evidence Surface Creep, Control File
  Budget, and Owner Review Compression.
- Clarified that `Standard SDAD / High` is for major non-Q5 tradeoffs, while
  `Full SDAD / High` is for packets that change Q5 gates.
- Updated the standard handoff template to include SDAD scale/intensity,
  autonomy level, control-file budget, and compressed owner review summary.
- Updated localized README guides for the 1.1 operating-intensity posture.

## 1.0.11 - 2026-05-04

- Added tool-agnostic session handoff and context continuity guidance: chats are
  execution traces, specs are authority, and long sessions should hand off to
  fresh sessions through `docs/sdad/handoffs/YYYY-MM-DD-topic.md`.

## 1.0.10 - 2026-04-29

- Clarified the default low-intervention autonomy posture: owners approve work
  packet boundaries, while review-worthy units and small SPEC items remain
  internal implementation/evidence slices unless the owner asks otherwise.

## 1.0.9 - 2026-04-27

- Added low-intervention autonomy levels and work packets so owners approve a
  meaningful boundary instead of every micro-task or evidence-ready unit.
- Split `AI-complete / evidence-ready` from `Owner-accepted` across README,
  onboarding prompts, Mini SDAD, maintenance rules, adapters, templates, and the
  Codex skill.
- Added `docs/autonomy-levels.md` with Level 0-4 autonomy, stop conditions, and
  checkpoint summaries.
- Added `docs/implementation-discipline.md`, adapting compatible lessons from
  Karpathy-inspired coding guidelines: surface assumptions, prefer simple
  designs, make surgical changes, and verify goals.
- Added anti-patterns for speculative complexity and drive-by refactors.

## 1.0.8 - 2026-04-27

- Added review-worthy development units so AI agents batch related small tasks
  into a meaningful review boundary instead of stopping after every micro-task.
- Added autonomy-within-approved-unit guidance: proceed until evidence is ready,
  and stop only for scope expansion, Q5 risk changes, destructive actions,
  owner-controlled decisions, blocked verification, or evidence conflicts.
- Updated README, no-clone onboarding, getting-started, Mini SDAD, templates,
  adapters, prompts, diagrams, implicit rules, localized READMEs, and the Codex
  skill.
- Shifted Standard/Full maintenance wording from every micro-task to every
  review-worthy development unit boundary.

## 1.0.7 - 2026-04-27

- Added risk override rules to the scale gate so Q5 production/data/auth/money/
  migration/release/rollback risk forces Standard or Full SDAD even when the raw
  yes-count is low.
- Split Mini SDAD loop-end behavior from Standard/Full control-file maintenance
  so Mini users are not asked to update files that Mini does not create.
- Added deterministic fallback guidance for failed raw-file fetches.
- Clarified that Claude Code means the local/CLI coding tool with project
  filesystem access, not Claude.ai chat, and that chat-only tools must not claim
  adapter installation.
- Updated localized READMEs and validation checks for the new onboarding rules.

## 1.0.6 - 2026-04-27

- Added explicit `save-state.md` update triggers for session pause/end, handoff,
  owner direction changes, blocked or partial state, unverified work, and
  expensive context recovery.
- Added a `save-state.md` project-control template so optional handoff state has
  a concrete update contract.
- Added Mini SDAD slice completion criteria so small projects still require
  changed files, evidence, limitations, and owner decision before "done".
- Updated README, getting-started, no-clone setup, maintenance-cost docs,
  project templates, adapters, handoff prompt, and the Codex skill.
- Expanded repository validation to preserve save-state triggers and Mini SDAD
  completion gates.

## 1.0.5 - 2026-04-27

- Added explicit maintenance-cost guidance for Standard and Full SDAD control
  files.
- Added `docs/maintenance-cost.md` with the end-of-loop update rule for
  `SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`, `review-findings.md`,
  operating rules, and ADRs.
- Updated README, getting-started, no-clone setup, fit assessment, templates,
  and the Codex skill to require loop-end control-file checks.
- Clarified that stale control files are a project bug and that projects unable
  to pay the maintenance cost should choose Mini SDAD or one-shot prompts.

## 1.0.4 - 2026-04-27

- Added adapter/tool confirmation to no-clone onboarding: agents must state
  which adapter or Mini SDAD template they are installing and why before
  fetching.
- Added fallback behavior when the current tool cannot be determined: ask the
  owner to choose Codex, Claude Code, Cursor, Copilot Chat, or Generic.
- Removed beginner-facing Codex skill wording from localized READMEs so the
  first path stays tool-neutral.
- Expanded validation and the Codex skill to preserve the adapter confirmation
  rule.

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
