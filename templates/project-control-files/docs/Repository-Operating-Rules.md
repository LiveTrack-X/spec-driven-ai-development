# Repository Operating Rules

Status: Active
Scope: Mandatory rules for code, documentation, review, verification, and handoff

## Purpose

This file collects repeated project rules so they do not remain only in chat,
handoff notes, or one AI session's memory.

## Mandatory Start Loop

Context Stability applies before every item in this start loop. Inspect file
size first and use bounded reads for large routed files.

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

The start loop must stay bounded. Before opening routed docs, archives, logs,
generated artifacts, private data, or search results, check whether the input is
large, stale, private, generated, or outside the active scope. Use file size
checks, headings, current sections, targeted keyword matches, output limits, and
explicit excludes. Do not dump full live-state files, generated output, logs,
private data, broad recursive search output, or old archives into an AI chat
context.

Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

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
- Before implementation, state current SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
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

When a plan is fuzzy, run a clarification checkpoint before coding. Inspect
current code, tests, active docs, SPEC, TODOs, review findings, and ADRs first.
Ask the owner only for unresolved blocking questions, one at a time. Include the
AI's recommended answer, why the question matters, and what changes if the owner
chooses differently. Do not use clarification checkpoints as micro-approval.

Implementation notes preserve implementation memory. When implementation
requires a judgment the active SPEC did not state, record the SPEC gap,
decision, reason, rejected alternatives, verification impact, and follow-up in
`docs/implementation-notes.md`. Do not record raw internal reasoning,
mechanical edits, or large logs.

Stop and ask the owner only when:

- scope would expand beyond the approved packet,
- risk posture, Q5 domains, release posture, data, auth, money, migration, or
  destructive action changes,
- an owner-controlled product or tradeoff decision is required,
- verification is blocked or impossible,
- current evidence conflicts with the requested plan.

## Operating Intensity Rules

`Mini / Standard / Full SDAD` are project scales. `High / Medium / Low` are
operating intensities for Standard and Full SDAD:

- `Standard SDAD / High`
- `Standard SDAD / Medium`
- `Standard SDAD / Low`
- `Full SDAD / High`
- `Full SDAD / Medium`
- `Full SDAD / Low`

Use `Standard SDAD / High` for non-Q5 packets with major product or architecture
tradeoffs, hard-to-reverse implementation choices, or explicit owner
checkpoints. Use `High` when the current packet changes behavior, policy,
boundary, evidence claim, or risk acceptance for release, production,
migration, destructive action, real user data handling, auth, data, money,
security, rollback, accepted-memory boundaries, external deployment, or a major
owner-controlled risk decision. A Q5 project does not make every packet High.
Use `Medium` for normal features, bugfixes, validation, and docs sync inside an
approved scope. Use `Low` for docs-only, typo, index, helper split, small
test/check adjustment, or small template edits.

Baseline Freeze is a posture, not a new scale or intensity value. Use labels
such as `Full SDAD / Medium (Baseline Freeze)` or `Full SDAD / Low (Baseline
Freeze)`; do not create a `Low-Medium` label. After a usable baseline exists,
prefer `Medium` or `Low`, protect repeatability, compress evidence, simplify
owner review, and avoid new evidence surfaces unless they reduce review time,
protect a real safety boundary, support a release gate, or make the baseline
repeatable.

Evidence Surface Creep is a project smell: do not add a new verifier, digest,
viewer, report, handoff format, handoff report, or parallel evidence artifact
unless it reduces owner review time, protects a real boundary, supports a
release/production gate, or makes a baseline repeatable.

## Advanced Extension Fit Gate

Advanced extensions include harness optimization, self-improving agent loops,
repeated evaluation automation, retrieval/memory tuning, and workflows that
search over prompts, tools, context construction, review rules, or agent
scaffolds.

Before using one, state:

- repeated task unit,
- measurable success metric,
- fixed model and tool surface,
- allowed changes and out-of-scope changes,
- search evidence,
- owner acceptance evidence,
- held-out acceptance set or risk if none exists,
- evaluation leakage risk,
- concrete budget in time, candidate count, evaluation runs, token/API cost, or
  owner review time,
- owner adoption gate.

Each field must be answered, marked `unknown`, or marked `blocking`. A
discovered prompt, rule, retrieval policy, memory policy, or harness is
evidence-ready, not owner-accepted, until the owner reviews the split, leakage
risk, budget result, changed behavior, and adoption plan.

## Implicit Rules Made Explicit

- Current beats historical: current code, tests, active docs, and active SPEC
  sections beat older SPEC history, archives, handoffs, and chat memory.
- Evidence beats confidence: no completion claim without reproducible evidence.
- Active beats interesting: future ideas and product notes are not active scope.
- Small verified slices beat large unverified progress.
- Review-worthy units beat micro-approval.
- Implementation discipline makes autonomy safe.
- Implementation memory beats hidden rationale.
- Open critical findings beat feature expansion unless the owner accepts the risk.
- Explicit non-goals beat assumptions.
- Stated uncertainty beats silent guessing.
- Repository evidence beats unnecessary questions.
- Stable terminology beats session vocabulary.
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
- Active live-state files should stay short enough to read as current operating
  state; archive old history and link it instead of keeping long journals in the
  startup path.
- Use the minimum documentation update sets in `docs/INDEX.md` before handoff.
- If behavior changed, update the relevant active docs in the same change.
- If implementation status changed, update `SPEC/SPEC-COMPLETE.md` and
  `docs/TODO-Open-Items.md`.
- If a review finding is closed, update `review-findings.md`.
- If no doc content changed, state which docs were checked and why no update was
  needed.
- If repeated ambiguity comes from overloaded domain terms, create or update a
  small glossary routed from `docs/INDEX.md`; keep it glossary-only.
- Use ADRs for durable architecture, policy, release, source-of-truth, security,
  data-boundary, or owner-approved tradeoff decisions.
  A decision normally deserves an ADR only when it is hard to reverse, would
  surprise a future maintainer without context, and represents a real tradeoff.

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

Long AI coding sessions are execution traces, not permanent memory. Specs are
authority, handoffs are continuity, archives are history, and fresh sessions are
for reliable execution.

Before closing, archiving, replacing, or restarting a long AI session, create a
session handoff under:

```text
docs/sdad/handoffs/YYYY-MM-DD-topic.md
```

Every handoff must include:

- project or repository name,
- branch or working context,
- current objective,
- SDAD scale / intensity used,
- control-file budget used,
- autonomy level used,
- compressed owner review summary,
- work packet completed,
- review-worthy unit completed,
- changed files,
- decisions made and why,
- implementation notes for spec-unstated decisions,
- behavior changed,
- tests or commands run,
- docs checked or updated,
- open findings,
- remaining risks,
- constraints, owner preferences, and do-not-touch areas,
- what is not complete,
- owner decision needed, if any,
- next concrete steps,
- reactivation prompt for a fresh AI session.

Reference existing SPECs, ADRs, TODOs, review findings, implementation notes,
logs, or evidence files by path or URL instead of duplicating long content in
the handoff.

When asked to restart, summarize, archive, or continue later, offer to create or
update a handoff first. When resuming, load the relevant SPEC, handoff, and
current repository state before continuing.

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

Update `docs/implementation-notes.md` when the implementation required a
spec-unstated assumption, change, compromise, rejected alternative,
owner-relevant tradeoff, follow-up, or verification-impact note.

Update operating rules or ADRs when repeated pain, architecture decisions, policy
decisions, release decisions, security boundaries, data-boundary decisions, or
owner-approved tradeoffs changed.

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct.

If no control file needs a content change, state which files were checked and why
no update was needed. Do not claim completion while control files are stale.

Control File Budget for each work packet:

- `Minimal`: changed active doc or state file only.
- `Normal`: TODO/review-findings plus affected docs.
- `Heavy`: SPEC/TODO/review-findings/save-state/ADR/rules bundle, or four or
  more control files updated in one packet.

If `Heavy` appears in three consecutive packets, reassess intensity, consider
Baseline Freeze, compress evidence into an owner summary, and consolidate docs,
archive entries, or reports when possible.

Record the control-file budget in the handoff summary.

If active state files become large or an AI chat becomes unstable, run a
context-stability pass before feature work: split active/current summaries from
archive/history, update `docs/INDEX.md` routing, preserve history without
deleting it, and use bounded reads for large archives, logs, generated artifacts,
private data, local databases, dependency directories, and session transcripts.
If repo-packing, graphing, embedding, indexing, or context-building tools are
used, align their ignore files with this rule.

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
