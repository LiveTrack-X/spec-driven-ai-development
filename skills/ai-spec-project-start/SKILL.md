---
name: ai-spec-project-start
description: >-
  Start, adopt, review, implement, reorganize, release, or hand off a project
  using owner-supervised SPEC-driven AI development. Use for new-project
  kickoff, AGENTS/docs/SPEC/TODO bootstrap, natural-language requests such as
  review this repo, implement the spec, release this, tune autonomy, or create a
  handoff, and for converting repeated project lessons into durable rules,
  playbooks, tests, or templates.
---

# AI-SPEC Project Start

Create the smallest SDAD control plane that lets an owner direct AI work,
separate evidence from confidence, and keep future sessions recoverable.

## Reference Routing

Read references only when their trigger applies:

- Read [references/runtime-contract.md](references/runtime-contract.md) before
  creating or changing an SDAD control surface. It owns scale, autonomy, stop,
  privacy, source-of-truth, evidence, and completion semantics.
- Read [references/starter-templates.md](references/starter-templates.md) when
  bootstrapping or repairing Standard/Full control files.
- Read [references/field-patterns.md](references/field-patterns.md) when
  translating lessons from another project, release/migration practice, or a
  reference implementation.
- Read [references/implicit-rules.md](references/implicit-rules.md) when repeated
  confusion or failure should become a rule, playbook, test, validator, or
  template.

Do not load every reference by default.

## Workflow

### 1. Inspect Capability And Existing State

Determine whether the environment can edit the project filesystem.

- In chat-only environments, plan and explain only. Do not install files or
  claim they were saved.
- In file-editing environments, inspect repository instructions, current files,
  version control state, source/tests, and existing SDAD surfaces before
  proposing changes.
- Preserve unrelated owner changes. Do not replace an existing control system
  merely because SDAD was requested.
- Treat review/audit requests as read-only unless the request also authorizes a
  change.

If the repository already has SDAD, start from its current adapter,
`sdad-state.yaml`, and `docs/INDEX.md`. Repair drift rather than rebuilding
from scratch.

### 2. Interpret The Request

Map plain language to the dominant intent:

- kickoff/adopt/reorganize: select scale and bootstrap;
- review/audit: inspect and report evidence;
- implement/fix: bind work to active acceptance criteria;
- release/publish/tag/deploy/migrate: activate the named owner gates;
- docs/README/guide: update affected documentation and source-of-truth state;
- handoff/resume: recover or write continuity state;
- autonomy complaints: tune packet size, autonomy, and intensity together;
- reference intake: compare source behavior, implementation, evidence, and gaps.

Compose multiple intents only when they fit one packet without changing scope,
risk, claim level, owner gate, or durable-record needs. Otherwise ask one
blocking question with a recommended default.

### 3. Select Scale

Ask:

1. Will this take more than one AI session?
2. Will the owner return later?
3. Does done need evidence beyond AI confidence?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, production, migration, destructive action, real user data,
   auth, money, security, rollback, or another owner-controlled risk?

Select:

- One-shot: zero yes; create no persistent files.
- Mini: one or two yes from questions 1-3 only, with Q4/Q5 no.
- Standard: Q4 yes, three yes total, persistent state, or a packet that only
  inspects, documents, or tests a Q5 area.
- Full: four or five yes, or a packet that changes, accepts, or executes a Q5
  gate.

Override rules beat raw counts. State the selected scale and why before creating
files. Ask whether product, hardware, compatibility, package, remote tester,
external lab, public, or release claims need evidence beyond local software
tests; create optional evidence surfaces only for active claims.

### 4. Select Tool And Install One Adapter

Identify Codex, Claude Code, Cursor, Copilot Chat, or Generic. If ambiguous, ask
which file-editing tool is active. Claude Code means the local coding tool, not
Claude.ai browser chat.

For a source checkout, prefer the repository's installer. For no-clone setup:

1. Read the canonical `install-sources.json`.
2. Read the matching route in `docs/no-clone-quick-install.md`.
3. Use the exact revision, path, target, and SHA-256 from the manifest.
4. Show the source and hash result before saving.
5. Fail closed on fetch or hash mismatch.
6. Offer retry, pasted source, terminal installer, or manual clone/download;
   never invent an adapter from memory.

Install exactly one active adapter. One-shot installs none. Mini installs only
the matching Mini instruction file. Standard/Full installs the matching
full adapter before creating project control files.

Do not overwrite an existing file without showing the proposed difference.
Use force/replace only with owner authorization and preserve rollback behavior.

### 5. Bootstrap The Progressive Control Plane

For Standard or Full, create the files defined by
[references/starter-templates.md](references/starter-templates.md). The fixed
startup path is:

1. tool adapter;
2. `sdad-state.yaml`;
3. `docs/INDEX.md`;
4. current source/tests/runtime state;
5. only documents or policy/playbook headings routed for the active packet.

Do not make the full rulebook, archives, old handoffs, or optional evidence
files mandatory startup reads.

Keep roles singular:

- adapter: always-loaded safety and execution kernel;
- `sdad-state.yaml`: current scale, intensity, autonomy, packet, gates, checks,
  and routed docs;
- `docs/INDEX.md`: trigger-to-file routing only;
- operating rules: durable policy loaded by heading;
- playbooks: procedures loaded on demand;
- SPEC/TODO/findings/notes: current authoritative work state;
- save-state/handoff: continuity only;
- evidence/claim files: created only for an active claim.

If required files already exist, inspect and merge. Do not silently replace
project-specific paths, commands, decisions, or constraints.

### 6. Bind The First Work Packet

Capture:

- owner outcome and user pain;
- smallest useful behavior;
- active SPEC slice and acceptance criteria;
- non-goals and do-not-touch areas;
- current repository evidence;
- review-worthy development units;
- validation commands and the claims they support;
- owner-controlled gates and stop conditions;
- next owner checkpoint.

Write current routing values to `sdad-state.yaml`. Keep `routed_docs` limited
to files that can affect the packet. Use the current source and tests before
implementing from a plan.

### 7. Choose Autonomy And Intensity

Use Level 1 for Mini and Level 2 Work Packet Autonomy for normal Standard/Full
implementation. Use Level 4 owner gates for release, migration, destructive
actions, data/auth/money/security decisions, rollback, and production claims.

Use Low intensity for small docs/index/helper edits, Medium for normal
implementation and review, and High only when the packet changes behavior,
policy, boundary, evidence claim, or a hard-to-reverse owner tradeoff. A Q5
project does not make every packet High.

Proceed through review-worthy units without micro-approval. Stop only for the
conditions in the runtime contract.

### 8. Execute Or Route

For review-only work, return prioritized findings with file/line evidence,
impact, and validation limits.

For implementation, use a failing test or check first when the behavior is
testable, make the smallest coherent change, run focused checks, then run the
full relevant validation surface. Keep docs and current control state aligned.

For reference-derived work, create a source behavior to implemented behavior to
evidence map and label gaps. For product/hardware/package/remote/release claims,
use the optional evidence files named by the active route.

Record spec-unstated durable implementation judgments in
`docs/implementation-notes.md`. Use an ADR only for a hard-to-reverse,
surprising tradeoff. Do not record raw internal reasoning.

### 9. Finish At The Right Boundary

Call work evidence-ready only when scoped implementation, relevant checks, docs,
and residual risk are shown. Keep owner-accepted, hardware-verified,
release-candidate, and production-ready states separate.

Return a compact checkpoint:

- scale, intensity, autonomy, and packet;
- changed files and behavior;
- checks run and what they prove;
- docs/control state changed or checked;
- open findings and unverified behavior;
- remaining risk and owner decisions;
- acceptance state and next step.

Update save-state or create a handoff only when the session pauses, changes
hands, remains blocked/partial/unverified, owner direction changes, or context
would be expensive to reconstruct. Link existing artifacts rather than copying
long transcripts.

## Existing-Project Rules

- Do not force SDAD onto a project that is better served by One-shot or Mini.
- Do not create optional files without an active job.
- Do not treat archived plans, product notes, external references, handoffs, or
  chat memory as current implementation authority.
- Do not let a lower evidence tier support a stronger claim.
- Do not use higher autonomy to bypass owner gates.
- Do not assume commit authorizes push, release, deployment, migration, or an
  external message.
- Do not hide partial, degraded, skipped, simulated, or unverified behavior.
- Do not claim completion while current control state is stale.

## Sensitive Data Boundary

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Do not read or expose credentials, keys,
tokens, cookies, `.env` contents, raw customer records, or private corpora
unless the task requires it and owner policy plus tool policy permit it. Stop
before reading when authorization is unclear.

## Guardrails

- Use evidence before questions; ask only the next blocking owner question.
- Use bounded reads for large or broad inputs.
- Prefer reversible local changes and preserve dirty working trees.
- Keep adapters self-contained; do not introduce runtime includes that their
  host tool will not load.
- Keep no-clone sources commit-pinned and hash-verified.
- Keep the fixed startup control plane inside repository line/character budgets.
- Validate links, templates, skill metadata, installers, and tests before
  declaring the bootstrap evidence-ready.
