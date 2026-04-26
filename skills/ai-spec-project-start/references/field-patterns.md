# Field Patterns

Load this reference when the owner asks whether their AI-driven development
workflow is reasonable, wants to reuse lessons from a previous project, or needs
rules for a complex project with many AI sessions, releases, migrations, or
high-risk runtime behavior.

## CMP-Derived Rules

Use these when the project has many docs, SPEC revisions, or AI sessions:

- Start every session from `docs/INDEX.md`.
- Keep `docs/Repository-Operating-Rules.md` as the durable rulebook.
- Define source-of-truth order: code/tests first, active docs next, SPEC after
  evidence, archive last.
- Separate active implementation gaps from review findings.
- Use minimum documentation update sets before handoff.
- Keep product notes and archives out of the active implementation path until
  deliberately promoted.
- Treat production readiness as a named hardening gate.

## DirectPipe-Derived Rules

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

## Combined Use

For a new project, ask:

1. What pain from the previous project should become a rule?
2. Which docs form the first-read chain?
3. What is the active SPEC and what is only future research?
4. Are there stable/next version lanes?
5. What risk domains need special review checklists?
6. What evidence proves the first slice?
7. What evidence is required before release or production use?

Do not create a giant plan first. Create the control files, then implement the
smallest useful verified slice.
