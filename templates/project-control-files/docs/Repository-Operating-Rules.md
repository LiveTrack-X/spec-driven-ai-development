# Repository Operating Rules

Status: Active
Scope: Mandatory rules for code, documentation, review, verification, and handoff

## Purpose

This file collects repeated project rules so they do not remain only in chat,
handoff notes, or one AI session's memory.

## Mandatory Start Loop

Before changing code, prompts, SPECs, docs, migrations, release assets, or
automation:

1. Read `docs/INDEX.md`.
2. Read this file.
3. Read `docs/TODO-Open-Items.md` and `review-findings.md` for implementation,
   hardening, or bugfix work.
4. Read `SPEC/SPEC-COMPLETE.md` and any relevant active SPEC.
5. Inspect the current source code and tests before implementing from a plan.

Do not begin from archived docs, old plans, product notes, or stale handoff
files without checking `docs/INDEX.md`.

## Source Of Truth

When sources conflict, prefer:

1. source code, migrations, tests, reproducible commands,
2. active runtime docs,
3. canonical SPEC,
4. active SPEC files,
5. current handoff files,
6. product notes and external references,
7. historical or archived records,
8. chat memory or AI confidence.

If a SPEC spans past-to-present history, current active sections override older
sections. Older SPEC material explains rationale; it does not define current
implementation unless reaffirmed in the active path.

## Code Consistency Rules

- Keep changes scoped to the approved work packet and active review-worthy
  development units.
- Prefer additive changes unless a migration plan allows breaking changes.
- Label scaffolds, placeholders, and dummy adapters in active docs and TODO.
- Label skipped, degraded, partial, environment-limited, or unverified behavior.
- Avoid broad rewrites while blocking review findings remain open.
- If the project has risk domains, follow the domain-specific checklist before
  handoff.

## Review-Worthy Unit Rule

Do not stop for owner approval after every micro-task.

Default to Level 2 Work Packet Autonomy for normal Standard SDAD work: define a
bounded work packet, complete the review-worthy units inside it, then hand off a
checkpoint summary. Use Level 4 gates for release, migration, destructive
actions, data/auth/money/security decisions, rollback, and production claims.

Before implementation, identify the current review-worthy development unit. It
may contain multiple related TODOs or small edits, but it must stay inside one
bounded objective that can be reviewed in one handoff. The unit organizes review
and evidence; it is not a separate owner-approval boundary while it stays inside
the approved packet.

Proceed autonomously inside the approved work packet until evidence is ready.
Mark units as `AI-complete / evidence-ready`; do not call the packet
`Owner-accepted` until the owner checkpoint happens or the owner has delegated
that acceptance policy.

Implementation discipline guards autonomy: surface assumptions, prefer the
simplest working design, make surgical changes, and tie every step to
verification.

Stop and ask the owner only when:

- scope would expand beyond the approved packet,
- risk posture, Q5 domains, release posture, data, auth, money, migration, or
  destructive action changes,
- an owner-controlled product or tradeoff decision is required,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan.

## Implicit Rules Made Explicit

- Current beats historical: current code, tests, active docs, and active SPEC
  sections beat older SPEC history, archives, handoffs, and chat memory.
- Evidence beats confidence: no completion claim without reproducible evidence.
- Active beats interesting: future ideas and product notes are not active scope.
- Small verified slices beat large unverified progress.
- Review-worthy units beat micro-approval.
- Implementation discipline makes autonomy safe.
- Open critical findings beat feature expansion unless the owner accepts the risk.
- Explicit non-goals beat assumptions.
- Stated uncertainty beats silent guessing.
- Docs drift is a bug.
- Handoff is context, not authority.
- Archive preserves memory, not active execution.
- Release readiness beats feature count.
- Environment limits beat overclaiming.
- Cross-review beats single-agent finality.
- Owner decision beats AI momentum.
- Scope-specific percent beats vague global percent.
- Repeated pain becomes a rule, checklist, test, or template update.

## Documentation Consistency Rules

- Control files have maintenance cost. Do not create them unless they will be
  kept current.
- Use the minimum documentation update sets in `docs/INDEX.md` before handoff.
- If behavior changed, update the relevant active docs in the same change.
- If implementation status changed, update `SPEC/SPEC-COMPLETE.md` and
  `docs/TODO-Open-Items.md`.
- If a review finding is closed, update `review-findings.md`.
- If no doc content changed, state which docs were checked and why no update was
  needed.
- Use ADRs for durable architecture, policy, release, source-of-truth, security,
  data-boundary, or owner-approved tradeoff decisions.

## Review And Verification Rules

- Do not accept AI confidence as evidence.
- Report failed, skipped, timed-out, missing, or unrun tests plainly.
- Important changes should receive a separate review pass by another AI, model,
  session, or human reviewer.
- Review should prioritize bugs, security, data loss, docs drift, missing tests,
  overreach beyond SPEC, and false completion claims.
- Release or production readiness requires deployment, migration, security,
  backup/restore, monitoring, rollback, and manual evidence as applicable.

## Version Lane Rules

If the project has stable, beta, rewrite, migration, or platform lanes, document:

- allowed changes per lane,
- which directory or branch each lane uses,
- bugfix sync rules,
- changes that must not sync,
- release-channel and rollback rules.

## Handoff Rules

Every handoff must include:

- autonomy level used,
- work packet completed,
- review-worthy unit completed,
- changed files,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- open findings,
- remaining risks,
- what is not complete,
- owner decision needed, if any.

## End-Of-Loop Maintenance Rule

Every work packet, handoff, or session end ends with a control-file update
check. Do not stop after every micro-task just to update documents, but do not
hand off stale control files.

Update `SPEC/SPEC-COMPLETE.md` when behavior, implementation status, scope,
constraints, or acceptance criteria changed.

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
update it, mark it stale, or archive it before handoff. Stale save-state is
context, not authority.
