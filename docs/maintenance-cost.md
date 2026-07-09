# Maintenance Cost

SPEC-Driven AI Development is a control layer, not a free checklist.

If you create control files, you must keep them current. Otherwise the workflow
creates stale authority, which is worse than having no workflow.

## The Cost

Standard and Full SDAD require a small maintenance pass at the end of every
work packet or handoff, not after every micro-task. If a packet contains
multiple review-worthy units, one consolidated maintenance pass is usually
enough.

A review-worthy development unit can be evidence-ready inside the packet before
the whole packet reaches owner acceptance.

Before handoff, owner checkpoint, or session end, update or explicitly check:

- `SPEC/SPEC-COMPLETE.md` when product behavior, implementation status, scope,
  constraints, or acceptance criteria changed,
- `docs/TODO-Open-Items.md` when work was completed, added, deferred, or split,
- `review-findings.md` when bugs, risks, review findings, or blocked issues were
  found, fixed, deferred, or accepted,
- `docs/implementation-notes.md` when implementation required a spec-unstated
  assumption, change, compromise, rejected alternative, owner-relevant tradeoff,
  follow-up, or verification-impact note,
- `docs/Repository-Operating-Rules.md` when repeated pain becomes a durable rule,
- ADRs when architecture, policy, release, security, data-boundary, or owner
  tradeoff decisions need durable rationale,
- `save-state.md` when work is paused, handed off, direction changes, or the
  next session would otherwise need to reconstruct context,
- `docs/sdad/handoffs/YYYY-MM-DD-topic.md` before closing, replacing,
  restarting, or resuming a long AI coding session in a fresh session.

If no file needs a content change, the handoff must say which control files were
checked and why no update was needed.

## Control File Budget

Choose a control-file budget for each work packet:

- `Minimal`: update one changed active doc or one state file only.
- `Normal`: update affected active docs plus TODO or review-findings.
- `Heavy`: update SPEC/TODO/review-findings/save-state/ADR/rules as a bundle,
  or update four or more control files in one packet.

If `Heavy` maintenance appears in three consecutive packets, run an intensity
reassessment:

- can Standard or Full SDAD run at lower intensity,
- is Baseline Freeze needed,
- can evidence be compressed into an owner summary,
- can docs, archive entries, or reports be consolidated.

Record the control-file budget in the handoff summary so repeated `Heavy`
packets are visible.

## Small Project Compression Rule

For One-shot, Mini SDAD, or a small Standard packet, one evidence-ready summary
is enough when all of these are true:

- one active slice or bugfix is being reviewed,
- no Q5 release, production, auth, money, user-data, destructive, or rollback
  gate changed,
- no unresolved review finding needs to survive the turn,
- no spec-unstated decision must be durable after handoff,
- no other AI/tool/person needs to resume from separate state files,
- the evidence fits in a short summary with links or command output names.

Turn on separate control files only when their job exists:

| Surface | Create or update when |
|---|---|
| `SPEC/SPEC-COMPLETE.md` | behavior, scope, constraints, or acceptance criteria changed |
| `docs/TODO-Open-Items.md` | work continues beyond the current summary or must survive sessions |
| `review-findings.md` | a defect, risk, blocked gate, or deferred review item remains active |
| `docs/implementation-notes.md` | a spec-unstated assumption, compromise, or verification-impact choice must survive |
| `save-state.md` | a future session would otherwise need to reconstruct context |
| `docs/sdad/handoffs/` | another session, AI tool, or person will continue the work |
| Evidence Matrix / Claim Registry / Artifact Contract | a product, hardware, package, remote, compatibility, or release claim needs mapped evidence |

If the table does not trigger a surface, do not create it just to look more
SDAD-like. Compression is correct when the owner can still see changed files,
checks, claim scope, known limits, and what is not complete.

## Live-State Size Budget

Active live-state files are routing summaries, not permanent session logs.

Keep files such as `save-state.md`, `next-task.md`, `review-findings.md`, and
`docs/TODO-Open-Items.md` short enough to inspect as current operating state.
Treat `docs/implementation-notes.md` the same way when a project uses it. If one
becomes long, repetitive, or difficult to audit, preserve the old material in an
archive/history file and leave the active file focused on:

- current objective,
- current/open items,
- constraints and do-not-touch areas,
- validation state,
- next one to three concrete steps,
- links to archive/history material.

Do not delete history just to reduce context. Move it out of the default startup
path and update `docs/INDEX.md` or the project routing document.

Default soft triggers:

- `>50 KB` or `>500 lines`: bounded reads by default.
- `>200 KB`, `>2,000 lines`, or hard to audit: run a context-stability check
  before feature work continues.
- `>1 MB`: do not read in full during startup unless the owner explicitly asks
  for historical reconstruction.

Use bounded reads for large archives, logs, generated artifacts, private data,
local databases, dependency directories, and session transcripts: check file
size, read headings or matching sections, limit search output, and use explicit
excludes. If an AI chat becomes unstable, suspect context growth from large
state files or broad searches before changing runtime code.

Do not keep a growing work log in one active file. When command output, review
evidence, imported evidence, screenshots, traces, or manual reproduction notes
would make TODO, review findings, implementation notes, save-state, or handoff
hard to scan, split the record into a timestamped archive/evidence file such as:

```text
docs/archive/logs/YYYY-MM-DD-HHMM-start-topic.md
```

The split file should begin with `Start: YYYY-MM-DD HH:MM`, scope, source
command or artifact path, evidence tier, supported claim or work packet, and
links back to the active docs that reference it. Active docs should keep only
the summary, status, and link.

Common single-file bloat risks:

- `TODO-Open-Items.md`: move completed work and future ideas to TODO history or
  backlog references; keep only active open work.
- `review-findings.md`: move closed findings and accepted risks to review
  archive; keep only active defects, risks, and blocked gates.
- `implementation-notes.md`: move old implementation diary material to archive;
  keep current spec-unstated choices and verification impact.
- `save-state.md`: move old session state to save-state archive or handoff;
  keep only current resume state and next steps.
- Evidence files: keep IDs, status, freshness, and claim scope active; move raw
  logs, screenshots, imports, and long traces to timestamped evidence archives.
- `Repository-Operating-Rules.md`: keep durable behavior-changing rules active;
  move procedures to playbooks/skills and guarantees to validators or CI.
- `docs/INDEX.md`: keep routes and update sets active; move explanations to
  user docs or field notes.

Use the Single-File Bloat Risk Routes table in `docs/INDEX.md` when deciding
where a split record should live.

If repository-packing, graphing, embedding, or indexing tools are used, keep
their ignore files aligned with this rule so generated, private, log, cache,
dependency, and local database surfaces do not enter AI context by default.

See [context-stability.md](context-stability.md).

## End-Of-Packet Rule

Every SDAD loop should end at a work-packet or handoff boundary:

```text
Work packet -> Build unit(s) -> Review -> Evidence-ready -> Owner checkpoint -> Update control files
```

Do not stop after every small task just to update documents. Also do not hand
off while control files are stale. Do not claim completion while control files are stale.

Use two states:

- `AI-complete / evidence-ready`: evidence exists and stale files have been
  updated or explicitly named.
- `Owner-accepted`: the owner has accepted, rejected, revised, or deferred the
  packet at a checkpoint.

Final completion requires evidence, owner acceptance or requested changes,
updated TODO/review/SPEC state, and known stale items explicitly named.

Minimum loop-end smoke:

- run the relevant tests/checks or state why they could not run,
- sync TODO, review findings, SPEC, implementation notes, and save-state when
  their status changed,
- verify that no active numbered work packet remains unchecked unless it is
  explicitly deferred or blocked,
- check the working tree for generated artifacts, caches, logs, or package
  outputs that should be ignored or removed,
- when packaging, installer, release, or product distribution is part of the
  claim, smoke the installed artifact from outside the source tree,
- keep `AI-complete / evidence-ready` separate from `Owner-accepted`.

Implementation notes sit between code comments and ADRs: they preserve why a
spec-unstated implementation choice was made, but they do not replace TODOs,
review findings, handoffs, or durable ADRs.

A decision normally deserves an ADR only when it is hard to reverse, would
surprise a future maintainer without context, and represents a real tradeoff.
This keeps ADRs durable instead of turning them into another implementation
journal.

## Save-State Update Triggers

`save-state.md` is optional. If the project uses it, it must stay current enough
for the next AI session or human maintainer to resume without guessing.

Update `save-state.md` when any of these happen:

- a session is ending or pausing before the project is fully accepted,
- an active slice completes and the next slice is not obvious from TODO/SPEC,
- the owner changes direction, priority, acceptance criteria, or risk tolerance,
- work is blocked, skipped, partial, degraded, or unverified,
- another AI tool, model, session, or person is expected to continue the work,
- current context would be expensive to reconstruct from code and docs alone,
- a decision changes what the next session should do first.

If none of these triggers apply, no save-state update is required. If
`save-state.md` exists but is stale, update it, mark it stale, or archive it
before handoff. Stale save-state is context, not authority; current code, tests,
active docs, and active SPEC still win.

Use [session-handoff.md](session-handoff.md) when the next session should not
depend on the old chat transcript. In SDAD, chats are execution traces, specs are
authority, and handoffs are continuity.

## Scale Implication

If this maintenance cost is too high, choose a smaller scale:

- One-shot prompt: no persistent files.
- Mini SDAD: one instruction file and a short handoff.
- Standard SDAD: core control files kept current at packet or handoff boundaries.
- Full SDAD: core files plus review, ADRs, release/risk gates, and stronger
  documentation consistency.

The right workflow is the largest one you can keep current, not the largest one
you can generate once.

For Standard and Full SDAD, also lower operating intensity when control surfaces
reduce controllability. Use [operating-intensity.md](operating-intensity.md) to
choose `High`, `Medium`, or `Low`.

## Stale File Warning

Stale control files cause common failures:

- old SPEC sections override current code,
- completed TODOs look open,
- known bugs disappear from review,
- AI sessions trust outdated docs,
- owners get false progress signals.

Treat stale control files as a project bug.
