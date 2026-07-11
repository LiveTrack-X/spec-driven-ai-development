# Task 9 Report: Compact SDAD Protocol Agent Kernel

Status: implementation, independent review follow-up, and verification complete.
The original commit subject is `Target routed agent context precisely`; the
review fix is recorded in a separate follow-up commit containing this update.

## Delivered

- Renamed the always-loaded identity to `SDAD Protocol` while retaining one
  compact expansion to SPEC-Driven AI Development.
- Replaced routed-document startup behavior with the ordered contract that
  current intent selects one routed path, heading, active section, or targeted
  match and membership does not require a full-file read.
- Kept one work loop and current controls: scale,
  `execution_scope: unit | packet`, and named owner gates.
- Removed current-kernel Q5, intensity, numbered-autonomy, recovery-mode,
  owner-checkpoint, AI-complete, and save-state wording and prohibited Markdown
  imports of state, INDEX, and README.
- Added the compact worker/delegation envelope and ordered finish report while
  keeping guidance, validation, technical enforcement, owner decision,
  evidence-ready, and owner acceptance distinct.
- Kept continuity limited to the state-declared current handoff for resume
  intent and only refreshes that handoff when cross-session continuity is
  needed.
- Updated the minimal example with the same targeted-read meaning in two lines.
- Updated renderer title metadata and regenerated all six adapters from the
  canonical kernel without changing deterministic rendering architecture.
- Added validator and mutation contracts for targeted routes, full-read
  reversal, forbidden imports, and legacy current terminology.

## TDD Evidence

- Tests and real-file fixtures were changed before production files.
- RED: `python -m unittest discover -s tests -p
  "test_agent_experience_contracts.py" -v` ran 44 tests and produced 49
  expected failing subtests. Failures showed all seven canonical/rendered
  surfaces lacked the amended route, identity/vocabulary, and report envelopes;
  the minimal example lacked targeted-read wording; and the validator accepted
  the prohibited full-read mutation, imports, and legacy terms.
- RED: `python -m unittest discover -s tests -p
  "test_render_agent_surfaces.py" -v` failed the new `SDAD Protocol` render
  identity before renderer metadata changed.
- No mocks or test-only production APIs were introduced.

## GREEN Evidence

- Agent-experience contracts: 44/44 passed.
- Render contracts: 3/3 passed.
- Adapter installer contracts: 12 tests ran; 10 passed and 2 environment-gated
  Windows file-symlink cases skipped because symlink privilege is unavailable.
- Full suite, run once after the final behavior change:
  `python -m unittest discover -s tests -q` -> 353 tests ran; 350 passed, 3
  existing environment-gated skips, 0 failures/errors.
- `python scripts/validate_repo.py` -> `Repository validation passed.`
- `python scripts/render_agent_surfaces.py --check` -> all six adapters match
  the canonical runtime kernel.
- `python -m py_compile` passed for both changed production modules and both
  changed Python test modules.
- `git diff --check` passed.
- Budgets: canonical 114 lines / 5,479 characters; non-Cursor adapters 114
  lines / 5,426-5,436 characters; Cursor 120 lines / 5,537 characters; fixed
  adapter + state + INDEX startup 10,323 characters.

## Independent Review Follow-Up

- Review found that the original full-read mutation replaced the positive
  targeted-route sentence. Its one violation therefore proved only that the
  required positive tokens were missing, not that conflicting full-read
  wording was rejected independently.
- The regression now appends `Read every routed document in full.` to an
  otherwise valid adapter fixture, leaving every positive route token intact.
- RED: the 44-test agent-experience run produced one expected failure because
  the validator returned an empty violation list for that appended sentence.
- The validator now rejects the exact full-read instruction through the
  independent forbidden-wording check and reports one actionable violation.
- GREEN: agent-experience 44/44 and render 3/3 passed.
- Full suite, run once after the behavior fix: 353 tests passed with 3 existing
  environment-gated skips and no failures or errors.
- Repository validation, render parity, changed-Python compilation, and
  `git diff --check` passed. The kernel and fixed-startup budgets remain the
  exact values recorded above; no canonical or rendered surface changed.

## Files

- Modified canonical source:
  `templates/project-control-files/AGENTS.md`.
- Modified compact example: `examples/minimal-project/AGENTS.md`.
- Modified deterministic title metadata: `scripts/render_agent_surfaces.py`.
- Modified validation: `scripts/sdad_validator/agent_experience.py`.
- Modified focused tests: `tests/test_agent_experience_contracts.py` and
  `tests/test_render_agent_surfaces.py`.
- Regenerated the six committed adapter outputs under `adapters/`.
- Added this report: `.superpowers/sdd/task-9-report.md`.

## Scope And Self-Review

- The canonical kernel remains below both line and character budgets and
  contains only the start route plus required authority, evidence, safety,
  execution, delegation, reporting, and continuity boundaries.
- Provider differences remain confined to renderer title/scope metadata and the
  existing Cursor front matter; runtime behavior comes from one canonical file.
- Start skill/kickoff, public README/guides/prompt, release metadata, image,
  Mini template, global installed skill, and Doctor contracts were not changed.
- No dependency, schema, finding ID, severity, check order, report shape, or
  release behavior changed.
- The full-read mutation produces exactly one actionable validator violation.
- Self-review found no Critical, Important, or Minor defect and no Task 10/11
  leakage.

## Additional Review Lenses

- Adopted in this task: exact route wire tokens, one actionable mutation error,
  deterministic render parity, current terminology, bounded worker/report
  envelopes, and explicit evidence/owner-decision separation.
- Already satisfied by the approved design: fixed filenames, one canonical
  kernel, provider-neutral runtime behavior, and on-demand procedures.
- Deferred to v3.3+: configurable routes, plugin loading, generalized workflow
  formats, and state-v3 abstractions; Task 9 has no concrete defect requiring
  them.

## Concerns

- None blocking.
- Cursor is exactly at the 120-line budget because its required front matter
  adds six lines to the 114-line canonical rendering; future kernel line growth
  must be offset elsewhere or the budget contract will reject it.
