# Documentation And Handoff Playbook

Status: On demand
Trigger: durable decision, documentation drift, close-loop maintenance, pause,
resume, handoff, or oversized control file

## Record Routing

Write each fact once in the smallest authoritative surface:

- scope, behavior, non-goal, or acceptance criterion: active SPEC;
- current or deferred work: `docs/TODO-Open-Items.md`;
- defect, failed check, blocked gate, or unresolved risk: `review-findings.md`;
- spec-unstated implementation decision: `docs/implementation-notes.md`;
- hard-to-reverse surprising tradeoff: numbered ADR;
- claim/evidence status: evidence matrix and claim registry;
- resume-only context: `save-state.md` or current handoff.

Handoff and save-state provide continuity, not implementation authority. Promote
scope, behavior, risk, claim, or acceptance decisions to SPEC, ADR, TODO,
findings, or claim registry before implementing from them.

## Control File Budget

- Minimal: one changed active state/doc surface.
- Normal: TODO/findings plus affected docs.
- Heavy: SPEC, TODO, findings, save-state, ADR, and rules, or four or more
  control files in one packet.

If Heavy repeats for three packets, reassess scale and intensity. Do not create
files solely to make the process look complete.

Keep active files current and short. Move closed TODOs/findings, old evidence,
logs, and narrative history into timestamped archives and link them. INDEX must
remain routing-only; the rulebook must remain policy-only.

## Documentation Update Check

At packet or handoff boundaries, check only surfaces affected by the change:

- behavior/configuration: README, runtime docs, canonical SPEC;
- prompt/tool contract: prompt docs, adapter/skill, tests;
- data/security/destructive action: policy/security docs, SPEC, open findings;
- release/migration/version: release docs, risk playbook, SPEC;
- public/product/hardware/package claim: evidence and claim files;
- continuity change: state, TODO/findings, and handoff.

If no update is needed, name the files checked and why. Do not claim completion
while active control state is stale.

## Handoff

Create `docs/sdad/handoffs/YYYY-MM-DD-topic.md` before closing, replacing, or
restarting a long session when another session must continue. Include objective,
branch/context, scale/intensity/autonomy, packet and unit status, changed files,
decisions, checks, docs, remaining risks, do-not-touch areas, owner decisions,
acceptance state, next steps, and a short reactivation prompt. Link evidence by
path or URL rather than copying transcripts.

## Save-State Triggers

Update `save-state.md` when work pauses before acceptance, changes hands,
direction or acceptance criteria change, blocked/partial/unverified state
remains, or reconstruction would be expensive. Otherwise omit it or state that
no trigger applied.

## Close-Loop Gate

Before evidence-ready: run or explain routed checks; synchronize SPEC, TODO,
findings, notes, state, and claims whose status changed; check unfinished active
packets and generated artifacts; record residual risk; keep owner-accepted
separate from AI-complete.
