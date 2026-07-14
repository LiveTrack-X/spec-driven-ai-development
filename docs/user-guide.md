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
unresolved fact would change the scale or an owner gate; otherwise it proceeds
with the stated assumptions.

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
Expires when:
Evidence required before action:
```

The AI may reuse it only while the action, packet, conditions, source, and
expiry remain unchanged. A changed term or expiry requires a new decision.

## One Fact, One Home

| Fact | Authoritative home |
|---|---|
| Requirement or acceptance change | SPEC |
| Small implementation-time non-spec decision | implementation notes |
| Hard-to-reverse architecture decision | ADR |
| Unresolved work | TODO or finding |
| Cross-session recovery links/results | handoff |
| Current execution state | `sdad-state.yaml` |

Handoffs link to these authorities instead of duplicating their contents.

## Diagnose With SDAD Doctor

Use a real SDAD checkout for a stateful Standard or Full project:

```text
python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.1 [--json] [--strict]
```

Replace `<SDAD_CHECKOUT>` with the checkout path. A shell-neutral wrapper may
resolve an operator-configured checkout and invoke `--strict
--require-version 3.2.1`; a PowerShell `$env:` example is not portable.

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
packet marker matches `active_packet.id`. Retire the pointer when it is stale.

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
1 until migration is accepted. See
[autonomy-levels.md](autonomy-levels.md) and
[operating-intensity.md](operating-intensity.md) for the legacy mapping.

## Where To Go Next

- [No-Clone Quick Install](no-clone-quick-install.md)
- [Getting Started](getting-started.md)
- [AI Work Loop](ai-work-loop.md)
- [Owner Guide](owners-guide.md)
- [Mini SDAD](mini-sdad.md)
