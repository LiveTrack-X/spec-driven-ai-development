# Mini SDAD Agent Rules

Use this file when the project is too small for full SPEC-Driven AI Development
but still needs basic protection against scope drift, vague completion, or
session context loss.

## Scale

This project uses Mini SDAD.

Do not create the full SDAD folder structure unless the owner asks or the work
grows beyond this file.

Escalate to Standard or Full SDAD only when:

- the work spans multiple AI sessions,
- the owner will return to the project later,
- review findings need to survive across sessions,
- multiple AI tools or reviewers become involved,
- release, migration, user data, auth, money, or production risk appears.

## Active Scope

Implement only the requested task or the current small slice.

Do not expand into future ideas, rewrites, broad cleanup, or unrelated refactors
unless the owner explicitly promotes them into active scope.

## Done Means

Completion requires evidence:

- changed files are listed,
- tests, commands, or manual checks are shown,
- limitations and unverified behavior are named,
- the owner accepts the result.

AI confidence is not completion.

## Do Not

- Do not overwrite existing files without showing proposed changes.
- Do not invent requirements.
- Do not change unrelated code.
- Do not claim completion without evidence.
- Do not treat old notes or chat memory as more current than code.

## Handoff

At the end of work, report:

- what changed,
- how it was checked,
- what remains uncertain,
- whether the project should stay Mini SDAD or escalate.
