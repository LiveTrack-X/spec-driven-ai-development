# Project Agent Start Rules

Status: Active
Scope: Required starting point for AI agents and maintainers

## Mandatory First Read

Context Stability applies before every item in this start loop. Inspect file
size first and use bounded reads for large routed files.

Before code, SPEC, prompt, or documentation work, read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. The active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md` and `review-findings.md` for implementation, hardening, or bugfix work
5. The relevant active SPEC before architecture, policy, or behavior changes

Do not start from archived docs, historical plans, product notes, or old handoff files without checking `docs/INDEX.md` first.

## Context Stability Rule

The mandatory first read is a routing requirement, not permission to dump large
files into chat context.

Before opening routed docs, archives, logs, generated artifacts, private data, or
search results, check whether the input is large, stale, private, generated, or
outside the active scope. Use bounded reads: file size checks, headings, current
sections, targeted keyword matches, output limits, and explicit excludes.

Keep active live-state files such as `save-state.md`, `docs/TODO-Open-Items.md`,
and `review-findings.md` short enough to read as current operating state. Move
old history to archive/history files and link it instead of keeping long
narrative journals in the startup path.

Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

If an AI chat becomes unstable, suspect context growth from large state files,
broad searches, generated output, logs, private data, or old archives before
changing runtime code.

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
- Before implementation, state current SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
- Record blockers in `review-findings.md`.
- Record open implementation work in `docs/TODO-Open-Items.md`.
- Update docs when behavior changes.
- Do not implement from archived docs or product notes unless promoted into active SPEC.
- Label partial, degraded, scaffolded, skipped, or unverified behavior.
- If the project has stable/next versions, define version lanes and bugfix sync rules.
- If the project has high-risk domains, define domain-specific review checks.

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

## Operating Intensity Rule

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
Use `Medium` for normal implementation, validation, and docs sync inside an
approved scope. Use `Low` for docs-only, typo, index, helper split, small
test/check adjustment, or small template edits.

Baseline Freeze is a posture, not a new scale or intensity value. Use labels
such as `Full SDAD / Medium (Baseline Freeze)` or `Full SDAD / Low (Baseline
Freeze)`; do not create a `Low-Medium` label. After a usable baseline exists,
prefer `Medium` or `Low`, protect repeatability, compress evidence, simplify
owner review, and avoid new evidence surfaces unless they reduce review time or
protect a real boundary, support a release gate, or make the baseline
repeatable.

For `Medium` or `High` checkpoints, start with Owner Review Compression:
one-line status, changed user-facing behavior, safety boundary touched yes/no,
checks summary, owner decision needed yes/no, recommended next action, and links
or references to detailed evidence.

Advanced extensions such as harness optimization, self-improving loops,
retrieval/memory tuning, or repeated evaluation automation require an explicit
fit gate: repeated task unit, measurable metric, fixed model/tool surface,
allowed changes, search evidence, owner acceptance evidence, leakage risk,
concrete budget, and owner adoption gate. Mark missing fields as `unknown` or
`blocking`; do not hide them as assumptions.

## Implicit Rules Made Explicit

- Current beats historical.
- Evidence beats confidence.
- Active beats interesting.
- Small verified slices beat large unverified progress.
- Review-worthy units beat micro-approval.
- Implementation discipline makes autonomy safe.
- Implementation memory beats hidden rationale.
- Open critical findings beat new feature work.
- Explicit non-goals beat assumptions.
- Stated uncertainty beats silent guessing.
- Handoff is context, not authority.
- Release readiness beats feature count.
- Owner decision beats AI momentum.
- Scope-specific percent beats vague global percent.

## Handoff Rule

Long AI coding sessions are execution traces, not permanent memory. Specs are
authority, handoffs are continuity, archives are history, and fresh sessions are
for reliable execution.

Before closing, archiving, replacing, or restarting a long AI session, create a
session handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`.

Before handoff, state:

- project or repository name,
- branch or working context,
- current objective,
- SDAD scale / intensity used,
- autonomy level used,
- work packet completed,
- review-worthy unit completed,
- changed files,
- decisions made and why,
- implementation notes for spec-unstated decisions,
- tests or commands run,
- docs checked or updated,
- remaining risks,
- constraints, owner preferences, and do-not-touch areas,
- what is not complete,
- owner decision needed, if any,
- next concrete steps,
- reactivation prompt for a fresh AI session.

When asked to restart, summarize, archive, or continue later, offer to create or
update a handoff first. When resuming, load the relevant SPEC, handoff, and
current repository state before continuing.

## End-Of-Loop Maintenance Rule

Every work packet, handoff, or session end must end by checking and updating
current control files. Do not stop after every micro-task just to update
documents, but do not hand off stale control files.

Update `SPEC/SPEC-COMPLETE.md` when product behavior, implementation status,
scope, constraints, or acceptance criteria changed.

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

If `Heavy` appears in three consecutive packets, reassess intensity and consider
Baseline Freeze.

Record the control-file budget in the handoff summary.

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
