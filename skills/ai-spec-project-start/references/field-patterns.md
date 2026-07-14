# Field Patterns

Load this reference when the owner asks whether their AI-driven development
workflow is reasonable, wants to reuse lessons from a previous project, or needs
rules for a complex project with many AI sessions, releases, migrations, or
high-risk runtime behavior.

## Documentation-Governance-Derived Rules

Use these when the project has many docs, SPEC revisions, or AI sessions:

- Start every session from `docs/INDEX.md`.
- Keep `docs/Repository-Operating-Rules.md` as the durable rulebook.
- Define authority by fact type: source/tests/runtime establish observed
  behavior; state-declared `active_spec` establishes intended scope and
  acceptance criteria; state owns execution; handoff owns continuity.
- A current applicable owner instruction can interrupt or redirect work; persist
  accepted intent before affected stateful implementation resumes. Old/provider
  chat is context only.
- Treat an owner-directed SPEC adoption as a change request. Other SPECs stay
  proposals only when non-authoritative and nonconflicting; names, dates, and
  document order do not activate scope.
- Prefer current active SPEC sections over older timeline/history sections when
  a SPEC spans past to present.
- Separate active implementation gaps from review findings.
- Use minimum documentation update sets before handoff.
- Use clarification checkpoints for fuzzy plans: inspect repository evidence
  first, then ask only the next blocking owner question with a recommended
  answer.
- Keep domain language small and routed when terminology drift affects
  implementation, review, tests, or owner decisions.
- Keep product notes and archives out of the active implementation path until
  deliberately promoted.
- Route repeated pain through finding -> root cause -> smallest durable control
  plus regression evidence -> Keep/Refine/Merge/Retire. Imported experience
  follows the current owner's apply/review/reference intent; origin alone does
  not grant or reduce authority.
- Treat production readiness as a named hardening gate.

## Release-Governance-Derived Rules

Use these when the project has releases, migrations, stable/next versions,
platform work, or fragile runtime constraints:

- Define version lanes and allowed changes per lane.
- Require stable-to-next bugfix sync with an architecture mapping table.
- Protect existing users during migration with release-channel rules, asset
  naming, compatibility checks, and rollback plans.
- Turn large refactors into named architecture maps.
- Document risk domains such as thread ownership, lock order, security
  boundaries, data migration, real-time paths, or external API contracts.
- Use release gates that combine automated tests, manual checks, AI review, and
  explicit severity thresholds such as Critical 0.
- State what AI cannot verify in the current environment.

## Mature-Project Migration Evidence

Use the canonical twelve-item procedure in the skill's
`Existing-Project Read-Only Migration Preview`; do not duplicate it here. This
reference owns mature-record inventory, history preservation, and evidence
comparison practices.

- Inventory existing adapters, state, INDEX routes, active ledgers, handoffs,
  save-state, Delivery Readiness Model records, SPECs, notes, ADRs, archives,
  file sizes, and dirty or untracked owner material before proposing changes.
- Separate live authority and unresolved work from closed history, background,
  generated output, and archive candidates. Record why each candidate is kept,
  linked, moved, or left untouched.
- Preserve history by default. Link or move continuity content into a current
  handoff or dated archive; do not silently rewrite provenance, flatten active
  and historical records, or automatically delete legacy files.
- Capture a pre-change Doctor result when available. If Doctor cannot run,
  record a read-only structural baseline with the exact limitation.
- Plan the post-change comparison as two evidence lanes: Doctor strict for SDAD structural consistency, and project validation separately for bounded product
  claims. Do not let one substitute for the other.
- Compare record counts, active packet markers, route targets, validation
  commands, handoff pointers, owner gates, and unresolved findings before and
  after the migration. Report unexplained loss or drift instead of normalizing
  it away.

## Combined Use

For a new project, ask:

1. What pain from the previous project should become a rule?
2. Which docs form the first-read chain?
3. What is the active SPEC and what is only future research?
4. Which SPEC sections are current, and which are historical rationale?
5. Are there stable/next version lanes?
6. What risk domains need special review checklists?
7. What is the first review-worthy development unit?
8. What evidence proves the first unit?
9. What evidence is required before release or production use?
10. Which obvious-but-unwritten rules should become explicit project rules?
11. Which clarification questions are blocked after repository inspection?
12. Which domain terms need a glossary route?

Do not create a giant plan first. Create the control files, then implement the
smallest useful review-worthy unit.
