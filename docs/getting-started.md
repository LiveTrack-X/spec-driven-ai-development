# Getting Started With SDAD Protocol

SDAD expands to SPEC-Directed AI Development: a repository-local operating
protocol for AI-assisted development, not a prescribed implementation method or
agent runtime.

The fastest path is the expanded
[Copy-Paste Start Prompt](../README.md#copy-paste-start-prompt). It is identical
to [No-Clone Option 1](no-clone-quick-install.md#option-1-give-this-to-your-ai-agent).
Use that large prompt once for install, upgrade, migration, or repair.

The stable v3.2.1 install sources are pinned by
[`install-sources.json`](../install-sources.json) to immutable behavior baseline
`f173aa398562d6a9d86b941dc79f75f9381148f4`. See the
[v3.2.1 release notes](releases/v3.2.1.md) for the bounded change and evidence.

## Choose The Three Controls

Scale determines which persistent control surface is installed. Execution
scope determines how far the AI may work now. Owner gates determine which
protected actions still require the owner.

| Scale | Use when | Default execution boundary | Owner gates |
|---|---|---|---|
| One-shot | Current disposable request | Current request | As applicable |
| Mini | One small evidence-bearing change | `unit` | As applicable |
| Standard | Durable state, multiple sessions, or reviewers | `packet` | Named as applicable |
| Full | Risk-bearing work needs additional controls | `packet` | Named for applicable risks |

The AI should infer scale, execution scope, claim boundary, and owner gates from
the request and repository, then report them with explicit assumptions. It asks
at most one question only when the unresolved fact would change the scale or an
owner gate; otherwise it proceeds with the stated assumptions. The owner may
override the inference.

## Install Once

### No-Clone Quick Install

Use [no-clone-quick-install.md](no-clone-quick-install.md) when the target AI can
edit the project but you do not want to clone this repository. Keep the pinned
revision, source path, and SHA-256 from one manifest together.

### Clone Or Download

```bash
git clone https://github.com/LiveTrack-X/spec-driven-ai-development.git
cd spec-driven-ai-development
```

Install exactly one project adapter from the project root:

```powershell
.\scripts\install-agent-adapter.ps1 codex
```

```bash
bash ./scripts/install-agent-adapter.sh codex
```

Available targets are Codex (`AGENTS.md`), Claude Code (`CLAUDE.md`), Gemini CLI
(`GEMINI.md`), Cursor, Copilot Chat, and a generic instruction file. Do not
create all adapters.

The optional global Codex start skill is for install, upgrade, migration,
Doctor, and control-file operations:

```powershell
.\scripts\install-codex-skill.ps1
```

```bash
bash ./scripts/install-codex-skill.sh
```

Ordinary project work follows the installed repository adapter.

## Bootstrap Standard Or Full

New stateful projects use state `version: 2`:

- `scale: standard | full`
- `execution_scope: unit | packet`
- one executable leaf `active_packet`
- `validation_for` equal to `active_packet.id`
- active TODO and review records carrying the packet ID
- optional packet-bound `current_handoff`
- `routed_docs` as eligible routes, not a read-all order

State v2 has no `intensity` or numeric `autonomy`. It does not create or route
`save-state.md`. Existing projects receive a read-only migration preview before
writes, and v1 inputs remain valid until migration is accepted.

After bootstrap, the fixed startup route is:

```text
adapter -> sdad-state.yaml -> docs/INDEX.md
```

Then read current source/tests and only one intent-selected path, heading,
active section, or targeted match. Do not load the full rulebook.

Optional product-evidence templates such as `docs/evidence-matrix.md`,
`docs/claim-registry.md`, `docs/artifact-contracts.md`,
`docs/work-packet-state.md`, and `docs/remote-evidence-import.md` are
create-on-demand. Route or create only what the current claim requires.

## Work The First Packet

Use one loop:

```text
Plan -> Route -> Implement -> Verify -> Report
```

An owner gate and a handoff are conditional branches. A review-worthy unit is a
small, coherent evidence slice; a packet may contain related units. Do not stop
for every micro-task inside an approved packet.

Before editing, define the validation contract and evidence limit. At the end,
report changed files, checks, limits, documents actually read, owner decision
needed, and evidence-ready status. Evidence-ready is not owner acceptance.

## Diagnose With SDAD Doctor

Doctor is checkout-only for stateful Standard or Full projects and any project
that adopts the `sdad-state.yaml` contract:

```text
python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.1 [--json] [--strict]
```

Replace `<SDAD_CHECKOUT>` with the actual checkout path. A shell-neutral wrapper
may resolve an operator-configured checkout; do not present PowerShell `$env:`
syntax as portable validation.

The guard identifies Doctor version 3.2.1. Doctor version, state schema version,
and report schema version are separate. Existing v1 JSON calls remain schema 1;
guarded/state-v2 calls use schema 2. `root` and `state_version` may be null when
state cannot be loaded. `--json` emits exactly one versioned JSON document.
`--strict` makes warnings fail policy without changing their severity.

Missing `sdad-state.yaml` produces the completed `state.missing` finding and
exit `1`; fatal invocation or report-construction failure uses exit `2`.

Doctor never executes validation commands. Green proves structural consistency,
not checkout provenance, product correctness, effectiveness, or owner
acceptance.

## Owner Gates And Authorization

Protected actions include release, production, migration, destructive change,
sensitive-data access, auth, money, security, rollback, and risk acceptance.
Execution scope does not bypass them.

Record a conditional owner authorization with Decision, Authorized action,
Packet, Conditions, Expires when, and Evidence required before action. Reuse it
only while those terms and source/artifact identity remain unchanged.

## Daily Recovery

For a fresh session, use adapter -> state -> INDEX. Read a handoff only when
`current_handoff` names one for the active packet. Tool-native sessions,
checkpoints, or memory are conveniences, not SDAD state authority.

Name new handoffs `YYYY-MM-DD-HNNNN-topic.md`. `HNNNN` is the date-scoped
sequence: use the next ID for that date and restart at `H0001` on a new date.
The full date-plus-ID path identifies the checkpoint; only the state pointer
declares it current. Existing unnumbered handoffs remain valid.

Keep facts in their authoritative homes: requirements in SPEC, small non-spec
decisions in implementation notes, hard-to-reverse decisions in ADRs,
unresolved work in TODO/findings, recovery links in handoff, and current state
in `sdad-state.yaml`.

## Migrating From SDAD 3.1

See [autonomy-levels.md](autonomy-levels.md) and
[operating-intensity.md](operating-intensity.md). Legacy numeric autonomy,
operating intensity, Q5 wording, and `save-state.md` stay in migration history,
not the state-v2 first-use path.
