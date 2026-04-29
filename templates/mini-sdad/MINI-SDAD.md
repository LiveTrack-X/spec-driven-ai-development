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

Implement only the requested task or the current review-worthy unit.

A review-worthy unit may contain multiple related small tasks. It should be large
enough that review has meaning, but small enough to verify in one handoff.

Default autonomy is Level 1 Unit Autonomy, with the active unit treated as one
small approved packet: complete that boundary, report evidence-ready status, and
ask only at the checkpoint or when a stop condition appears. Do not turn each
small SPEC item into a separate approval gate. Use Level 2 Work Packet Autonomy
only when the owner names a packet with multiple related units.

Do not expand into future ideas, rewrites, broad cleanup, or unrelated refactors
unless the owner explicitly promotes them into active scope.

Do not stop for owner approval after every micro-task or small SPEC item inside
the approved unit. Proceed until the unit has evidence, unless a stop condition
appears.

Stop and ask the owner only when:

- scope would expand beyond the active unit's approved boundary,
- Q5-style risk, release posture, data, auth, money, migration, or destructive
  action changes,
- an owner-controlled decision is required,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan.

## Mini Unit Completion

A Mini SDAD unit is evidence-ready only when:

- the active task is restated,
- changed files are listed,
- tests, commands, or manual checks are shown, or the reason they could not run
  is stated,
- user-visible behavior or output is described,
- limitations and unverified behavior are named,
- unrelated scope was not added,
- owner decisions or acceptance needed are named.

AI confidence is not completion.

Not evidence-ready when:

- the AI only says it is done,
- checks were not run and the gap is hidden,
- known uncertainty is not named,
- unrelated changes were made without owner approval.

Final done still requires owner acceptance unless the owner has explicitly
delegated the acceptance policy. Requested changes or deferred decisions mean
the unit is not done.

## Do Not

- Do not overwrite existing files without showing proposed changes.
- Do not invent requirements.
- Do not change unrelated code.
- Do not claim completion without evidence.
- Do not treat old notes or chat memory as more current than code.

## Handoff

At the end of work, report:

- active task,
- what changed,
- how it was checked,
- whether it is evidence-ready,
- what remains uncertain,
- owner decision needed,
- whether the project should stay Mini SDAD or escalate.
