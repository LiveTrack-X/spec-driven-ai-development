# Project Agent Start Rules

Status: Active
Scope: Required starting point for AI agents and maintainers

## Mandatory First Read

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. The active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. The relevant active SPEC before architecture, policy, or behavior changes

Do not start from archived docs, historical plans, product notes, or old handoff files without checking `docs/INDEX.md` first.

## Source Of Truth

When sources conflict, prefer:

1. Source code, migrations, tests, reproducible commands
2. Active runtime docs
3. Canonical SPEC
4. Active SPEC files
5. Handoff/save-state files
6. Product notes
7. Historical or archived records
8. Chat memory or AI confidence

If a SPEC spans past-to-present history, current active sections override older
sections. Older SPEC material is rationale unless reaffirmed in the current
active path.

## AI Development Rules

- Do not treat AI confidence as completion.
- Do not rely on obvious-but-unwritten assumptions.
- Keep active implementation separate from future ideas.
- Record blockers in `review-findings.md`.
- Record open implementation work in `docs/TODO-Open-Items.md`.
- Update docs when behavior changes.
- Do not implement from archived docs or product notes unless promoted into active SPEC.
- Label partial, degraded, scaffolded, skipped, or unverified behavior.
- If the project has stable/next versions, define version lanes and bugfix sync rules.
- If the project has high-risk domains, define domain-specific review checks.

## Review-Worthy Unit Rule

Do not stop for owner approval after every micro-task.

Before implementation, identify the current review-worthy development unit. It
may contain multiple related TODOs or small edits, but it must stay inside one
bounded objective that can be reviewed in one handoff.

Proceed autonomously inside the approved unit until evidence is ready.

Stop and ask the owner only when:

- scope would expand beyond the approved unit,
- risk posture, Q5 domains, release posture, data, auth, money, migration, or
  destructive action changes,
- an owner-controlled product or tradeoff decision is required,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan.

## Implicit Rules Made Explicit

- Current beats historical.
- Evidence beats confidence.
- Active beats interesting.
- Small verified slices beat large unverified progress.
- Review-worthy units beat micro-approval.
- Open critical findings beat new feature work.
- Explicit non-goals beat assumptions.
- Stated uncertainty beats silent guessing.
- Handoff is context, not authority.
- Release readiness beats feature count.
- Owner decision beats AI momentum.
- Scope-specific percent beats vague global percent.

## Handoff Rule

Before handoff, state:

- review-worthy unit completed,
- changed files,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- what is not complete,
- owner decision needed, if any.

## End-Of-Loop Maintenance Rule

Every loop must end by checking and updating current control files.

Update `SPEC/SPEC-COMPLETE.md` when product behavior, implementation status,
scope, constraints, or acceptance criteria changed.

Update `docs/TODO-Open-Items.md` when work was completed, added, deferred, or
split.

Update `review-findings.md` when bugs, risks, review findings, or blocked issues
were found, fixed, deferred, or accepted.

Update operating rules or ADRs when repeated pain, architecture decisions, policy
decisions, release decisions, security boundaries, data-boundary decisions, or
owner-approved tradeoffs changed.

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct.

If no control file needs a content change, state which files were checked and why
no update was needed. Do not claim completion while control files are stale.

## Save-State Update Triggers

`save-state.md` is optional. If this project uses it, update it when:

- a session is ending or pausing before work is fully accepted,
- an active slice completes and the next slice is not obvious from TODO/SPEC,
- the owner changes direction, priority, acceptance criteria, or risk tolerance,
- work is blocked, skipped, partial, degraded, or unverified,
- another AI tool, model, session, or person is expected to continue the work,
- current context would be expensive to reconstruct from code and docs alone.

If none of these triggers apply, say so. If `save-state.md` exists but is stale,
update it, mark it stale, or archive it before handoff.
