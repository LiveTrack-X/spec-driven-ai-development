# SDAD Protocol User Guide

SDAD expands to SPEC-Directed AI Development. It is a repository-local
operating protocol for AI-assisted development: use any implementation method
while keeping scope, evidence, unresolved state, and owner authority clear.
It organizes state, evidence, owner control, decisions, and handoffs; it does
not make model output correct or replace technical enforcement.

Scale determines which control documents are maintained. Execution scope
determines how far the AI may work now. Owner gates determine which actions
still require the owner.

## Quick Choice

| Situation | Scale | Default boundary | Owner gates |
|---|---|---|---|
| One disposable answer or change | One-shot | Current request | As applicable |
| Small change that needs evidence | Mini | `unit` | As applicable |
| Multi-session work, durable state, or reviewers | Standard | `packet` | Named as applicable |
| Risk-bearing work needing more controls | Full | `packet` | Named for applicable risks |

Full does not mean permission to release, migrate, deploy, read sensitive data,
or accept risk. Those remain owner gates. The AI should inspect the request and
repository first, infer and report scale, execution scope, claim boundary, owner
gates, and explicit assumptions. It asks at most one question only when an
unresolved fact would change objective/direction, authority/reference role,
execution boundary, protected action/gate, or claim boundary; otherwise it proceeds.

```text
Scale: Standard
Reason: multi-session state and review findings already exist.
Execution scope: packet
Claim boundary: structural and task validation only
Owner gates: release only
Assumptions: no production action before the release gate
Unresolved question: none
```

You can override this in ordinary language:

```text
Finish this packet, but stop before release.
```

## One Work Loop

```text
Plan -> Route -> Implement -> Verify -> Report
```

An owner gate and a handoff happen only when triggered. Verification can make
work evidence-ready; owner acceptance is a separate decision.

## How SDAD Uses Context

In a stateful project the startup route is:

```text
adapter -> sdad-state.yaml -> docs/INDEX.md
```

The AI then reads current source/tests and only the route, heading, active
section, or targeted match required by the current intent. `routed_docs` is an
eligible selection set, not an instruction to read every listed file. The
report should name only routed documents actually read.
An owner-named current input may still be inspected within the request when a
stale route omits it; if adopted, update the active authority and routes before
stateful implementation.

The large copy-paste bootstrap prompt is for one-time install, upgrade,
migration, or repair. Once installed, use the repository adapter and current
state; do not paste the bootstrap prompt into every session.

## Natural-Language Requests

You do not need SDAD command or skill names. Action words choose the route:

| Request | Interpreted route |
|---|---|
| "Review this" | Findings-first review |
| "Implement the active spec" | Packet-bounded implementation |
| "Release it" | Release preparation plus owner gate |
| "Continue next session" | Packet-bound handoff |
| "It asks too often" | Check execution scope and authorization expiry |
| "Use this other repository as a reference" | Reference intake, never imported authority |

Modifiers do not silently expand authority. For example, `commit and wait` does
not imply push, tag, release, or deployment.

A current owner instruction that redirects the work overrides an older owner
direction. The AI should stop affected old work, re-enter Plan -> Route, and
persist the new direction before resuming a stateful implementation. A request
to review, compare, explain, or use a SPEC only as reference stays read-only.
An explicit command authorizes only the named direction, acceptance, or
protected action for its stated boundary; it should not be asked again. It does
not waive evidence, prerequisites, tool policy, or a different protected action.
A question, hypothetical, quotation, negation, or review/reference-only request
does not authorize the action it mentions.

## State V2 At A Glance

New Standard and Full projects use state `version: 2`:

- `scale`: `standard | full`
- `execution_scope`: `unit | packet`
- `active_packet`: one executable leaf checkpoint
- `validation_for`: equals `active_packet.id`
- active TODO and review records: carry the packet ID
- `current_handoff`: optional and packet-bound
- `routed_docs`: eligible routes, not a read-all list

State v2 has no `intensity` or numeric `autonomy`. It does not create or route
`save-state.md`; that file remains a valid state-v1 migration input.

## Owner Authorization

A conditional authorization can persist without repeated questions when it
records:

```text
Decision:
Authorized action:
Packet:
Conditions:
Source/artifact identity:
Expires when:
Evidence required before action:
```

The AI may reuse it only while the action, packet, conditions,
source/artifact identity, and expiry remain unchanged. A changed term or expiry
requires a new decision.
A later restriction, cancellation, or revocation ends affected authorization
immediately. If a packet is cancelled without replacement, record it as
`deferred` with an explicit-owner-reactivation resume trigger; do not auto-resume.

## One Fact, One Home

| Fact | Authoritative home |
|---|---|
| Intended scope, behavior, or acceptance criteria | state-declared `active_spec` |
| Observed behavior | current source, tests, runtime, and reproducible commands |
| Small implementation-time non-spec decision | implementation notes |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or finding |
| Owner authorization or acceptance | one authoritative owner-decision record |
| Cross-session recovery links/results | handoff |
| Current execution state | `sdad-state.yaml` |

Handoffs link to these authorities instead of duplicating their contents.
`SPEC-COMPLETE.md` means integrated baseline, not immutable final truth. In a
stateful project, `active_spec` is the single normative SPEC entrypoint. A SPEC
supplied as current requirements is a change request unless the owner limits it
to review/draft/reference; hold affected work and reconcile it with the active boundary.
A merely discovered file is not authoritative by name, date, or status and may
remain a proposal only when nonconflicting. A same-boundary change may amend a
non-terminal packet; a material or post-acceptance change uses a new packet ID
and fresh validation instead of rewriting accepted history.

Before state moves past a terminal packet, one durable decision record pins the
packet ID, active SPEC path and exact revision, source/artifact identity,
evidence and claim limits, unresolved risk, and final owner decision. This
keeps accepted history reconstructible even when the same files change later.

Long-running work re-enters Plan -> Route when a SPEC, source, dependency,
environment, artifact, owner gate, or external result changes. Keep the same
packet only for the same unfinished objective and acceptance boundary;
otherwise create a never-reused packet. Validate the integrated branch and
final artifact after merge/rebase/cherry-pick. Read-only review, planning, or a
blocked packet may omit Implement or Verify, but the report must mark the phase
not applicable or blocked and must not claim its missing evidence.

An owner-decision record is one durable authority per decision, not a mandatory
global file. It can be a repository approval, issue/PR decision, signed record,
or a conditional authorization record. Authorization permits a named future
action; acceptance evaluates the delivered result. Link the same record from
evidence, claim, and handoff surfaces instead of copying its status.
If the owner later corrects, limits, or revokes a terminal decision, append a
new uniquely identified record that revises/supersedes the old one and update
affected current-claim pointers. Never rewrite the prior decision history.
If parallel decisions revise the same predecessor for overlapping claim scope,
hold the claim until an owner reconciliation record retires/supersedes all
competitors. A newer date or larger ID does not choose authority.

## Diagnose With SDAD Doctor

Use a real SDAD checkout for a stateful Standard or Full project:

```text
python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.2 [--json] [--strict]
```

Replace `<SDAD_CHECKOUT>` with the checkout path. A shell-neutral wrapper may
resolve an operator-configured checkout and invoke `--strict
--require-version 3.2.2`; a PowerShell `$env:` example is not portable.

Doctor version, state schema version, and report schema version are separate.
Existing v1 JSON calls remain report schema 1; guarded/state-v2 calls use report
schema 2. `root` and `state_version` can be null when no project state was
loaded. `--json` returns one versioned document. `--strict` changes policy exit
behavior without changing finding severity.

A missing `sdad-state.yaml` is a completed `state.missing` finding with exit
`1`, not a parser crash. Exit `2` is reserved for fatal invocation or report
construction failure.

Doctor never runs validation commands. A green result proves structural
consistency, not checkout provenance, product correctness, effectiveness, or
owner acceptance. A task benchmark supports only that task. Only a controlled
comparison supports a claim that one protocol version is better.

Tool-native session, checkpoint, memory, or diagnostic features are
conveniences. They are not SDAD state, handoff, or Doctor authority. Markdown
guidance is not technical enforcement; use permissions, hooks, sandboxes,
protected branches, or service controls for that.

## Troubleshooting FAQ

### The AI asks for approval too often, or runs ahead too much

Check the declared `unit` or `packet`, then check whether a prior conditional
authorization is still valid. Do not weaken an owner gate to reduce questions.

### The AI says "done" but I cannot tell what changed

Ask for evidence-ready status, changed files, checks, limitations, documents
read, and any owner decision still needed. Evidence-ready is not owner-accepted.

### SDAD feels like too many files

Use the smallest scale that preserves the needed state and evidence. Optional
evidence and ADR files are create-on-demand. `routed_docs` does not mean read or
create all of them.

### The next session keeps losing context

Require a current packet-bound handoff, set `current_handoff`, and verify its
packet marker matches `active_packet.id`. Name new checkpoints
`YYYY-MM-DD-HNNNN-topic.md`, using the next `HNNNN` for that date and restarting
at `H0001` on a new date. Cite the full path because `HNNNN` may repeat across
dates. Retire a stale pointer; never infer currentness from date or greatest ID.

### A chat-only tool says it installed SDAD

Chat-only tools can plan, but cannot truthfully claim repository files were
installed. Open the project in a file-editing coding tool.

### What evidence is enough when there is no formal test?

Define a practical before/after check before editing, capture its bounded
result, and state what remains unverified. Do not invent a stronger claim after
implementation.

## Migrating From SDAD 3.1

Existing projects receive a read-only migration preview before writes. Preserve
state-v1 `intensity`, numeric autonomy `0..4`, legacy messages, and report schema
1 until migration is accepted. Preserve legacy evidence/claim acceptance rows
as history; as each decision is touched, select one durable decision record and
replace other mutable acceptance fields with links to it. No mass rewrite is
required. See
[autonomy-levels.md](autonomy-levels.md) and
[operating-intensity.md](operating-intensity.md) for the legacy mapping.

## Where To Go Next

- [No-Clone Quick Install](no-clone-quick-install.md)
- [Getting Started](getting-started.md)
- [AI Work Loop](ai-work-loop.md)
- [Owner Guide](owners-guide.md)
- [Mini SDAD](mini-sdad.md)
