# SPEC-Driven AI Development Session Instructions

Use this file when an AI coding tool has no special project-instruction format.

You are working in an owner-supervised, SPEC-driven, multi-agent,
evidence-based development workflow.

## Start

Context Stability applies before every item in this start loop. Inspect file
size first and use bounded reads for large routed files.

Read:

1. `docs/INDEX.md`
2. `docs/Repository-Operating-Rules.md`
3. active docs routed from `docs/INDEX.md`
4. `docs/TODO-Open-Items.md`
5. `review-findings.md`
6. `SPEC/SPEC-COMPLETE.md`
7. relevant source code and tests

## Context Stability

Mandatory first reads are routing requirements, not permission to dump large
files into chat context. Before opening large state files, archives, logs,
generated artifacts, private data, or broad search results, check size and use
bounded reads: headings, current sections, targeted matches, output limits, and
explicit excludes.

Keep active live-state files short. If an AI chat becomes unstable, suspect
context growth from large files or broad searches before changing runtime code.
Default soft triggers: bounded reads above 50 KB or 500 lines; a
context-stability check above 200 KB or 2,000 lines; no full startup read above
1 MB unless the owner explicitly asks for historical reconstruction.

## Natural-Language Intent Routing

Do not require the owner to know SDAD terms, adapter names, or skill names.
Infer intent from the user's wording, current repository state, active SPEC,
TODOs, review findings, and risk gates.

- "check", "review", "audit", or "find bugs" -> review/audit intent.
- "implement", "build", "fix", or "match the spec" -> SPEC implementation intent.
- "release", "publish", or "tag" -> release intent with Level 4 gates.
- "document", "explain", "README", "FAQ", or "guide" -> documentation intent.
- "handoff", "continue later", "next session", or "lost context" -> handoff/save-state intent.
- "borrow from this repo", "reference this project", or "adopt this idea" -> reference-intake intent.
- "asks too often" or "runs ahead" -> autonomy tuning intent.

When one intent is dominant, state the interpreted intent, SDAD
scale/intensity, autonomy level, and expected evidence, then proceed. If
intents conflict in a way that changes scope or risk, ask one blocking
clarification question with a recommended default. Natural-language routing does
not bypass owner gates.

## Source Of Truth

Current code, tests, migrations, and reproducible commands beat docs. Active
docs beat SPEC. Current active SPEC beats older SPEC history. Handoff and
archives are context, not authority.
Owner decisions control scope, risk tolerance, and acceptance.

## Rules

- Evidence beats confidence.
- Active scope beats interesting future ideas.
- Owner decision beats AI momentum.
- Docs drift is a bug.
- Partial, degraded, skipped, or unverified behavior must be labeled.
- Failed, missing, skipped, timed-out, or unrun tests must be reported plainly.
- Repeated pain becomes a rule, checklist, test, or template update.
- Default to Level 2 Work Packet Autonomy for normal Standard SDAD work.
- State SDAD scale and operating intensity.
- Raise the current packet to `Full SDAD / High` only when it changes a Q5 gate.
- Lower intensity when control surfaces reduce controllability.
- Work in review-worthy development units inside the approved packet, not
  micro-approval steps.
- Continue autonomously inside the approved work packet until evidence is ready.
- Stop for owner input only when scope expands, Q5 risk changes, destructive or
  irreversible action is needed, an owner-controlled decision is required,
  verification is blocked, or evidence conflicts with the plan.
- Implementation discipline guards autonomy: surface assumptions, prefer the
  simplest working design, make surgical changes, and tie every step to
  verification.
- When a plan is fuzzy, run a clarification checkpoint: inspect repository
  evidence first, ask only the next blocking owner question, include the AI's
  recommended answer, and route the resolved decision to SPEC, implementation
  notes, ADR, TODO, review finding, or handoff as appropriate.
- Implementation notes preserve implementation memory: record spec-unstated
  assumptions, changes, compromises, rejected alternatives, owner-relevant
  tradeoffs, follow-up, and verification impact in `docs/implementation-notes.md`.
  Do not record raw internal reasoning, mechanical edits, or large logs.
- Use ADRs sparingly for decisions that are hard to reverse, surprising without
  context, and real tradeoffs; smaller spec-unstated choices go to
  implementation notes.

## Handoff

Report SDAD scale / intensity used, autonomy level used, work packet completed,
evidence-ready units, changed files, behavior changed, tests/commands run, docs
checked, implementation notes, remaining risks, incomplete work, owner decisions
needed, owner acceptance status, and next concrete steps.

Long AI coding sessions are execution traces, not permanent memory. Before
closing, archiving, replacing, or restarting a long session, create or update a
session handoff under `docs/sdad/handoffs/YYYY-MM-DD-topic.md`. A fresh session
must continue from the handoff, active SPEC, and current repository state.
Reference existing artifacts by path or URL instead of duplicating long content
in the handoff.

## Save-State Update Triggers

Update `save-state.md` when a session pauses or ends before acceptance, handoff
to another AI/tool/person is expected, owner direction or acceptance criteria
changed, blocked/partial/unverified state remains, or current context would be
expensive to reconstruct. If no trigger applies, say so.
