# Task 10 Report: Read-Only SDAD V2 Migration Preview

Status: implementation and verification complete. The planned commit subject is
`Add the SDAD v2 migration preview`.

## Delivered

- Narrowed the global skill trigger to SDAD install/upgrade, existing-SDAD
  migration, control-plane repair/recovery, Doctor use, and SDAD diagnosis.
  Ordinary project work now routes to the installed repository adapter.
- Replaced the five-question owner ritual with repository-first inference, one
  compact interpretation report, owner override, and at most one material
  blocking question.
- Added the canonical ordered twelve-item existing-project read-only migration
  preview before any proposed control-file write.
- Added v1 intensity/autonomy/save-state/readiness inventory and Level 0-4
  mapping, stateful-Mini preservation, Standard/Full-only v2 migration,
  conditional-authorization reuse limits, history preservation, and
  version-last ordering.
- Added the normalized packet envelope and the complete delegated-worker
  envelope without assuming parent context.
- Updated the runtime reference with steady-state v2 invariants, targeted route
  semantics, one loop, owner-gate boundaries, and separate Doctor/project claim
  limits.
- Updated field patterns with mature-record inventory, history-preservation,
  and baseline/post evidence comparison guidance without duplicating the full
  twelve-item procedure.
- Added the minimum preview gate to the standalone kickoff prompt.
- Added deterministic skill/validator contracts and temporary-home installer
  checks proving the installed skill and all updated references match repository
  sources byte-for-byte.

## TDD Evidence

- Tests were changed before production files.
- RED agent contracts: `python -m unittest discover -s tests -p
  "test_agent_experience_contracts.py" -v` ran 49 tests and produced 25
  expected assertion failures with no test errors. The failures showed the
  narrow trigger, infer-first report, material-question boundary, packet and
  delegation envelopes, twelve-item preview, v1 mapping, authorization reuse,
  and version-last rule were absent.
- RED installer contracts: `python -m unittest discover -s tests -p
  "test_install_codex_skill.py" -v` ran 4 tests and produced 12 expected
  subtest failures because the new contract phrases were absent from otherwise
  byte-identical temporary installs.
- RED validator contracts: `python -m unittest discover -s tests -p
  "test_validate_repo.py" -v` ran 75 tests and produced 2 expected failures
  because `validate_skill()` did not reject preview-order or broad-trigger
  mutations.
- No mocks of product behavior, test-only production APIs, or real-global-skill
  writes were introduced.

## GREEN Evidence

- Agent-experience contracts: 49/49 passed.
- Temporary `CODEX_HOME` installer contracts: 4/4 passed across Bash and
  PowerShell install/replace/link-safety paths.
- Repository-validator contracts: 75/75 passed.
- Full suite, run once after the final behavior change:
  `python -m unittest discover -s tests -v` -> 360 tests passed, 3 existing
  environment-gated tests skipped, 0 failures/errors.
- `python scripts/validate_repo.py` -> `Repository validation passed.`
- `python -m py_compile` passed for the changed validator and three changed
  Python test modules.
- `git diff --check` passed.
- Budgets: skill 296 lines / 13,066 characters; runtime reference 165 lines /
  7,695 characters; field patterns 89 lines / 4,445 characters; kickoff prompt
  175 lines / 8,489 characters. The enforced skill budget remains below 500
  lines / 25,000 characters.

## Files

- Modified skill source: `skills/ai-spec-project-start/SKILL.md`.
- Modified skill references:
  `skills/ai-spec-project-start/references/runtime-contract.md` and
  `skills/ai-spec-project-start/references/field-patterns.md`.
- Verified unchanged:
  `skills/ai-spec-project-start/references/starter-templates.md`.
- Modified standalone prompt: `prompts/kickoff-prompt.md`.
- Modified deterministic validation: `scripts/validate_repo.py`.
- Modified focused tests: `tests/test_agent_experience_contracts.py`,
  `tests/test_install_codex_skill.py`, and `tests/test_validate_repo.py`.
- Added this report: `.superpowers/sdd/task-10-report.md`.

## Scope And Self-Review

- Trigger review found no generic bug-fix, review, refactor, docs,
  implementation, release, or handoff trigger in skill frontmatter.
- The full twelve-item procedure exists only in the canonical skill. Runtime,
  field-pattern, and kickoff surfaces carry only their assigned responsibilities
  and link back to the canonical preview.
- Migration preserves dirty owner work, active authority, closed history,
  conditional authorization, save-state content, and the legacy
  `docs/work-packet-state.md` Delivery Readiness Model path.
- Doctor evidence remains structural and separate from project validation;
  neither grants owner acceptance or protected-action permission.
- Starter-template shapes, public README/guides, image, release metadata,
  adapters, Mini templates, Doctor implementation, and the real global skill
  were not changed. Installer tests used isolated temporary `CODEX_HOME` values.
- Self-review found no Critical, Important, or Minor defect and no Task 11
  public-document or release leakage.

## Additional Review Lenses

- Adopted in this task: exact migration wire terms, concept/order tests instead
  of whole-paragraph equality, targeted routing, separate reporting layers, and
  bounded mutation tests.
- Already satisfied by the approved design: fixed state-v2 fields, one loop,
  one canonical preview, and Standard/Full-only v2 state.
- Deferred to v3.3+: configurable control filenames, plugin/rule loading,
  generalized workflow formats, and state-v3 abstractions; Task 10 has no
  concrete defect requiring them.

## Concerns

- None blocking.
- Actual model trigger precision/recall remains the explicitly deferred
  post-release evaluation packet; deterministic tests prove only the source
  contract and negative generic-trigger wording.
