# Implementation Notes

Status: Active
Scope: Current spec-unstated implementation decisions

Use this file when implementation requires a judgment the active SPEC did not
explicitly make.

Do not use this as a transcript of raw internal reasoning or a mechanical edit
log. Keep it short enough for a fresh AI session to read as current context.

## Current Notes

```md
## IMPL-0001 - Work packet or unit name

- Date: YYYY-MM-DD
- Applies to:
- SPEC gap:
- Decision:
- Why:
- Alternatives rejected:
- Supersedes:
- Verification impact:
- Follow-up:
```

## Routing

- If the note creates future work, update `docs/TODO-Open-Items.md`.
- If the note records a bug, risk, or blocked issue, update `review-findings.md`.
- If the note is durable architecture, policy, release, security,
  data-boundary, or owner-approved tradeoff rationale, create or update an ADR.
  A decision normally deserves an ADR only when it is hard to reverse, would
  surprise a future maintainer without context, and represents a real tradeoff.
- New durable notes use a never-reused `IMPL-NNNN` ID. Existing unnumbered notes
  remain valid. Date is descriptive; identity and supersession use the note ID.
- At packet boundaries, classify each note by current effect rather than age:
  keep current small constraints here; promote requirements to SPEC, durable
  rationale to ADR, work to TODO, and defects/risks to findings.
- When a note is promoted or superseded, leave only a pointer to the new
  authority. Do not keep two mutable copies of the same decision.
- If current notes exceed a bounded read or mix unrelated domains, split by
  topic and keep this file as the small current router. Archive only decisions
  that no longer affect current work, verify inbound links, and never route all
  archive files at startup.
