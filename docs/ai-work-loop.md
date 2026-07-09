# AI Work Loop

Use this document while an AI agent is actively working in an SDAD-guided
project. It is an execution loop, not a full explanation of the method.

The goal is to keep SDAD control without turning every task into a full ritual.

## Choose The Loop

| Situation | Use | Loop |
|---|---|---|
| Typo, tiny docs edit, one small test fix | Fast | Recover Lite -> Evidence Contract -> Implement -> Verify -> Compact Report |
| Normal behavior or code change | Normal | Recover Standard -> Bind Packet -> Evidence Contract -> Implement -> Verify -> Required Docs Sync -> Compact Report |
| Multiple files, SPEC impact, review findings, or next-session continuity | Full | Recover Full -> Bind Packet -> Evidence Contract -> Implement -> Verify -> Sync -> Full Report -> Handoff if needed |
| Release, production, data, auth, money, security, migration, rollback, or destructive risk | Full + Gate | Full loop plus owner-controlled gate and matching evidence tier |

Always use the smallest loop that preserves evidence and owner gates.

## Recover Modes

### Recover Lite

Use for small, local changes:

- relevant files,
- relevant tests or commands,
- active TODO/review finding search if the task mentions open work or risk.

### Recover Standard

Use for normal implementation:

- Recover Lite,
- relevant SPEC section,
- relevant TODO/review finding,
- implementation notes if the choice may be spec-unstated.

### Recover Full

Use for risk, release, continuity, or source-of-truth conflict:

- Recover Standard,
- source-of-truth conflict check,
- save-state or handoff,
- ADRs, claim registry, evidence matrix, or artifact contract when the claim
  needs them.

Do not read every historical file by default. Read only what the packet needs.

## Evidence Contract

Before implementation, state a one-line evidence contract:

```text
This packet will be evidence-ready when [check] shows [observable result];
claim limit: [what this does not prove].
```

Examples:

- `npm test -- auth-errors` passes and invalid login maps to the expected UI
  message; claim limit: production auth server behavior is not tested.
- `python scripts/validate_repo.py` passes and README links resolve; claim
  limit: external GitHub rendering is not checked.

Do not implement first and invent the evidence standard afterward.

## Bind Packet

Before editing, restate:

- goal,
- non-goals,
- active review-worthy unit,
- evidence contract,
- owner gates.

For Fast Loop, this can be one short sentence.

## Review-Worthy Unit

A review-worthy unit should:

- produce observable behavior, evidence, or a closed finding,
- be reviewable in one focused diff or summary,
- have a clear check,
- avoid mixing unrelated concerns.

Prefer:

| Too vague | Better unit |
|---|---|
| File edits | Map login failure to the correct user message |
| Add tests | Add regression coverage for auth failure mapping |
| Clean docs | Reflect the changed CLI option in README |
| Refactor | Consolidate duplicate auth error mapping in one helper |

Do not split every import, formatter change, or tiny test name into a separate
owner checkpoint.

## Docs Sync Rule

Document impact is a check, not an automatic rewrite.

| Change type | Required sync |
|---|---|
| Internal implementation only | test result; implementation note only if the choice is spec-unstated |
| User-visible behavior | README/user docs/SPEC checked or updated |
| New unresolved defect | review-findings |
| Next session must continue | save-state or handoff |
| Important spec-unstated choice | implementation notes |
| Hard-to-reverse decision | ADR |

If no document needs an update, report: `docs checked, no update needed`.

## Stop Conditions

Stop and ask the owner only if:

1. scope would expand,
2. Q5 risk appears or changes,
3. destructive or irreversible action is required,
4. an owner-controlled decision is required,
5. verification is blocked,
6. evidence contradicts the plan or claim.

## Do Not Stop For

Do not pause for:

- small implementation details inside the approved packet,
- test name or file location choices,
- obvious import fixes,
- formatter or lint fixes,
- related small tasks inside the active review-worthy unit.

Proceed, verify, and report.

## Report Format

### Compact Report

Use for Fast and Normal loops:

```text
Outcome:
Changed:
Evidence:
Limits:
Next:
```

Example:

```text
Outcome: evidence-ready for login error message mapping.
Changed: LoginForm.tsx, authErrors.test.ts.
Evidence: npm test -- authErrors passed.
Limits: production auth server not tested.
Next: owner acceptance or move to signup error mapping.
```

### Full Report

Use for Full and Full + Gate loops:

```text
Packet:
Units:
Changed files:
Checks:
Docs sync:
Risks:
Owner decisions:
Handoff:
```

Evidence-ready is not owner-accepted. Owner acceptance requires the owner
checkpoint or an explicitly delegated acceptance policy.
