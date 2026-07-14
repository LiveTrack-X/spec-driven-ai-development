# No-Clone Quick Install

Use this page to apply SDAD Protocol without cloning the repository first.
Option 1 is the canonical path: give the expanded prompt to a file-editing AI
agent. The README Copy-Paste Start Prompt is generated from that exact block.

## Before You Start

Chat-only tools can plan with SDAD, but cannot install project files. Use Codex,
Claude Code, Gemini CLI, Cursor, Copilot Chat, or another tool with project
filesystem access.

The AI should infer and report scale, execution scope, claim boundary, owner
gates, and explicit assumptions from your request and repository before asking
questions. It asks at most one question only when an unresolved fact would
change the scale or an owner gate:

| Scale | Default boundary | Owner gates | Persistent setup |
|---|---|---|---|
| One-shot | Current request | As applicable | None |
| Mini | `unit` | As applicable | One instruction file |
| Standard | `packet` | Named as applicable | Compact state and routing controls |
| Full | `packet` | Named for applicable risks | Additional risk controls as needed |

Scale, execution scope, and owner gates are separate. Full scale never grants a
release, migration, deployment, destructive action, sensitive-data access, auth,
money, security, rollback, or risk-acceptance decision.

## Maintenance Cost

Choose Standard or Full only when the project will maintain current state,
packet-bound validation, active TODO/findings, and conditional handoffs. Optional
evidence records and ADRs are create-on-demand. `routed_docs` is a selection set,
not a full-read instruction.

The large prompt is a one-time bootstrap, upgrade, migration, or repair entry
point. After installation, ordinary work follows:

```text
adapter -> sdad-state.yaml -> docs/INDEX.md -> current intent-selected route
```

## What Is A Codex Skill?

The optional global Codex skill helps install, upgrade, migrate, diagnose, or
repair SDAD controls. It is not required for ordinary project work after a
repository adapter is installed.

## Latest Versus Pinned Sources

The installers below use one pinned commit, path, and SHA-256 set. Do not mix
files from different revisions. A full 40-character commit SHA provides the
stable baseline; `/main/` is only for intentionally testing changing content.

[install-sources.json](../install-sources.json) is the canonical
revision/path/hash contract. Pins use the stable v3.2.2 release baseline; keep
the revision, source path, and checksum from that one manifest together.

## Option 1: Give This To Your AI Agent

Paste this into Codex, Claude Code, Gemini CLI, Cursor, Copilot Chat, or another AI coding
agent:

```text
Use the SDAD Protocol (SPEC-Directed AI Development) as a repository-local
operating protocol for AI-assisted development. It does not prescribe the
implementation method or act as an agent runtime, harness, or orchestrator.

Source repository:
https://github.com/LiveTrack-X/spec-driven-ai-development

Do not require me to clone the repository unless absolutely necessary.

First determine whether you can edit files in this project.
If this is a chat-only environment such as Claude.ai, ChatGPT web, or another
browser chat with no project filesystem, do not install adapters or claim files
were saved. Use this repository for planning only, then tell me to open the
project in Codex, Claude Code, Gemini CLI, Cursor, Copilot Chat, or another file-editing AI
coding tool.

Step 0 - Infer the controls before creating files.

Do not make me answer a fixed questionnaire. Inspect my request and the
repository first. Infer scale, execution scope, validation claim boundary, and
owner gates, and make the assumptions behind the inference explicit. Ask at
most one blocking question, with a recommended answer, only when the unresolved
fact would materially change objective/direction, authority/reference role,
execution boundary, protected action/gate, or claim boundary. Otherwise proceed.
Report:

- Scale and reason
- Execution scope
- Claim boundary
- Owner gates
- Assumptions
- Unresolved question, or `none`

I may override the inference. Keep these three axes separate:

My explicit current command authorizes only its named direction, acceptance, or
protected action for the stated boundary. Persist it and do not ask for the same
decision again. It does not waive evidence, prerequisites, tool policy, or a
different protected action. Obey a current stop/redirect immediately.

- Scale determines which persistent control surface is installed.
- Execution scope determines how far the AI may work now.
- Owner gates determine which protected actions still require my decision.

Use these defaults unless I say otherwise:

- One-shot -> current request only; create no persistent SDAD files.
- Mini -> `unit`; create one tool instruction file.
- Standard -> `packet`; create the compact state and routing controls.
- Full -> `packet` plus named owner gates for the applicable risks.

The only state-v2 execution-scope values are `unit` and `packet`. `ask_first`
is an approval condition, not a scope. A session is not a work boundary.
Multi-packet execution requires an explicitly approved packet plan or list.
Release, migration, production, destructive action, real user data, auth,
money, security, rollback, and other protected decisions remain owner gates.

Check whether product, hardware, compatibility, packaging, remote tester,
external lab, or release claims need evidence stronger than local software
tests. This chooses evidence routes; it does not by itself grant a protected
action or force Full scale.

Step 0.5 - Route natural-language requests.

Do not require me to know SDAD terms, adapter names, or skill names. Infer the
work intent from my sentence and the current repository state.

Common intents:
- "check", "review", "audit", "find bugs" -> review or audit intent.
- "implement", "build", "fix", "match the spec" -> SPEC implementation intent.
- "release", "publish", "tag" -> release intent with an owner gate.
- "document", "explain", "README", "FAQ", "guide" -> documentation intent.
- "handoff", "continue later", "next session", "lost context" -> handoff
  intent.
- "borrow from this repo", "reference this project", "can we adopt this?" ->
  reference-intake intent.
- "adopt this", "use this", "implement this" -> current change-request intent.
- "asks too often", "runs ahead" -> execution-scope or owner-gate tuning.

Classify the whole utterance: a clear imperative authorizes only its named
action and boundary; a question, hypothetical, quotation, negation, or
review/reference-only request does not authorize the action it mentions.

Treat narrative modifiers as routing signals, not automatic scope expansion.
"Carefully" increases inspection depth, "fully" continues to evidence-ready for
the approved scope, "minimal" selects compression rather than weaker evidence,
and "commit and wait" does not imply push, release, or deploy unless named.

If multiple intents match, first decide whether they can be safely composed
inside one approved packet. If one route remains dominant, proceed and briefly
state the interpreted intent, scale, execution scope, expected evidence, and
owner gates. Ask one blocking clarification question with your recommended
default only when an unresolved fact would change objective/direction,
authority/reference role, execution boundary, protected action/gate, or claim
boundary; otherwise state assumptions and proceed. Do not use natural-language
routing to bypass release,
migration, destructive action, real user data, auth, money, security, rollback,
production claim, or other owner-controlled gates.

For Mini SDAD, fetch this exact template:
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/templates/mini-sdad/MINI-SDAD.md
Expected SHA-256: 0bd02d52289bf92607520bec6ef3e08715ec91f586350ba31dda5cdb1d1db7b6

Before fetching, state that you are installing Mini SDAD and explain why this
scale was chosen.

Save it as the correct instruction file for this tool:
- Codex -> ./AGENTS.md
- Claude Code -> ./CLAUDE.md
- Gemini CLI -> ./GEMINI.md
- Cursor -> ./.cursor/rules/mini-sdad.mdc
- Copilot Chat -> ./.github/copilot-instructions.md
- Generic AI agent -> ./AI-SESSION-INSTRUCTIONS.md

For Cursor, prepend this MDC frontmatter before the fetched Mini SDAD body:
---
description: Mini SDAD rules for small, evidence-based Cursor work units.
globs:
alwaysApply: true
---

For Standard or Full SDAD, install the matching instruction file for this AI
tool. Do not infer adapter paths. Use exactly one of these source URLs:

Before fetching, state which adapter you are installing and why.
If you cannot determine the current tool, ask me to specify one of:
Codex / Claude Code / Gemini CLI / Cursor / Copilot Chat / Generic.
Claude Code means the local/CLI coding tool with project filesystem access. It
does not mean Claude.ai chat.

- Codex -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/codex/AGENTS.md -> ./AGENTS.md -> SHA-256 8237f7905ba8ce0db95e77b5d40e54200062d2654adae45e667f04743f342e08
- Claude Code -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/claude-code/CLAUDE.md -> ./CLAUDE.md -> SHA-256 57a9431eecc5d8e2dfdfe71eb59ad673ff230db5c320197291a8a7a129f875ce
- Gemini CLI -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/gemini-cli/GEMINI.md -> ./GEMINI.md -> SHA-256 b3a6e16c21e14e594bdc5560838c664e3116ef1ee1366724a6b39a19a9e2e76b
- Cursor -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc -> ./.cursor/rules/spec-driven-ai-development.mdc -> SHA-256 789d378813f7b32f0e677265fa23c7908cf6b52342fc54e92455d05293038bfc
- Copilot Chat -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/github-copilot/.github/copilot-instructions.md -> ./.github/copilot-instructions.md -> SHA-256 ee914a5ebaa5413c7bfd43d21b48e6919fc3e373afed5707bc6076acf5a573b3
- Generic AI agent -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd/adapters/generic/AI-SESSION-INSTRUCTIONS.md -> ./AI-SESSION-INSTRUCTIONS.md -> SHA-256 15e02a42c32e46b332dc217ac43abad958d35e5a153f0f9746be42a32eee5ec2

Before saving the adapter:
1. show me the source URL,
2. show me the first 10 lines of the fetched file,
3. compute SHA-256 and require an exact match,
4. confirm the target path.

If you cannot fetch the file, stop and say so. Do not create a fake adapter from
memory. Offer deterministic fallback options: retry with network access, ask me
to paste the raw file content from the source URL, use the terminal installer, or
clone/download the repository manually.

For Standard or Full SDAD, use this large prompt once for bootstrap, upgrade,
migration, or repair. After installation, ordinary sessions follow only the
installed adapter -> `sdad-state.yaml` -> `docs/INDEX.md` -> intent-selected
source and routed section. Do not paste this bootstrap prompt every session.

Before any write to an existing project, show a read-only migration preview.
For a new Standard or Full bootstrap, create this compact v2 control plane:

- new Standard/Full state uses version 2,
- active_packet is one executable leaf checkpoint,
- validation_for equals active_packet.id,
- active TODO and review records carry the packet ID,
- current_handoff is optional and packet-bound,
- existing projects receive a read-only migration preview before writes.

1. create or update `sdad-state.yaml` with `version: 2`, `scale` (`standard` or
   `full`), `execution_scope` (`unit` or `packet`), `active_packet`,
   `validation_for`, `validation`, `owner_gates`, and `routed_docs`; do not add
   v1 `intensity` or numeric `autonomy`,
2. make `active_packet` one executable leaf checkpoint and require
   `validation_for` to equal `active_packet.id`,
3. create or update docs/INDEX.md as a routing-only file,
4. create or update docs/Repository-Operating-Rules.md and the on-demand
   docs/sdad/playbooks/ files,
5. create or update SPEC/SPEC-COMPLETE.md,
6. create or update docs/TODO-Open-Items.md,
7. create or update review-findings.md,
8. create or update docs/implementation-notes.md,
9. if the product evidence flag is yes, create only the needed maintained
   product evidence templates: docs/evidence-matrix.md,
   docs/claim-registry.md, docs/artifact-contracts.md,
   docs/work-packet-state.md, and docs/remote-evidence-import.md,
10. make every active TODO and review record carry the active packet ID,
11. leave `current_handoff` absent unless a current packet-bound handoff exists,
12. ask only for unresolved product pain, smallest useful version, non-goals,
    risks, owner-controlled decisions, the first packet, its review-worthy
    units, and evidence required for completion.

State v2 does not create or route `save-state.md`. Existing state v1
`intensity`, numeric `autonomy`, and `save-state.md` are migration inputs only;
preserve their v1 behavior while previewing the v2 mapping before edits.

Keep the fixed read path compact: adapter -> sdad-state.yaml -> docs/INDEX.md ->
current source/tests -> only the intent-selected route, heading, active section,
or targeted match. `routed_docs` is an eligible selection set, not a startup
read-all list. Report only the routed documents actually read. Do not load the
whole rulebook or optional evidence set by default.
Inspect a current owner-named input within the request even when stale
`routed_docs` omits it; if it is adopted, reconcile authority and routes before
stateful implementation.

Use one work loop: Plan -> Route -> Implement -> Verify -> Report. An owner gate
and a handoff are conditional branches, not extra mandatory steps. A clean
verification makes work evidence-ready; only the owner or an explicitly
delegated policy grants owner acceptance.

A review-worthy development unit may contain multiple related small tasks. It
should be large enough that review has meaning, but small enough to verify in one
handoff. Do not stop for owner approval after every micro-task or small SPEC
item inside an approved work packet.

Proceed inside the declared `unit` or `packet` until evidence is ready. Obey my
current stop/redirect immediately. Pause for input when scope expansion is
unrequested or ambiguous, a protected condition changes, a destructive or
irreversible action remains unauthorized, an owner-controlled decision is
unresolved, verification is blocked, or the request conflicts with evidence.
If I cancel the packet without a replacement, use `status: deferred`, preserve
the cancellation reason and partial evidence in a packet-linked record, set the
resume trigger to explicit owner reactivation, and never auto-resume it.

When the plan is fuzzy, run a clarification checkpoint before coding. Inspect
the current code, tests, active docs, SPEC, TODOs, review findings, and ADRs
first. Ask me only for unresolved blocking questions, one at a time. Include
your recommended answer, why the question matters, and what changes if I choose
differently. Do not use clarification checkpoints as micro-approval.

If repeated ambiguity comes from overloaded domain terms, propose one canonical
term and one short definition. For Standard or Full SDAD, create or update a
small glossary routed from docs/INDEX.md only when terminology drift affects
implementation, review, tests, or owner decisions.

Implement from the active SPEC. Give each fact one authoritative home:

- intended scope, behavior, or acceptance criteria -> the state-declared `active_spec`,
- observed behavior -> current source, tests, runtime, and reproducible commands,
- small implementation-time non-spec decision -> implementation notes,
- hard-to-reverse architecture decision -> ADR,
- unresolved work -> TODO or finding,
- owner authorization or acceptance -> one authoritative owner-decision record,
- cross-session recovery links and results -> handoff,
- current execution state -> `sdad-state.yaml`.

For a stateful project, `sdad-state.yaml#active_spec` is the single normative
SPEC entrypoint. `SPEC-COMPLETE.md` is an integrated baseline, not immutable or
automatically active. A SPEC supplied as current requirements is a change
request unless the owner limits it to review/draft/reference; reconcile it
before affected work. A
merely discovered SPEC gains no authority from filename, date, status, or chat
order. Keep the packet only for a same-boundary non-terminal amendment; a
material change or post-acceptance change requires a new packet and validation.

Handoffs link to those authorities instead of copying them. Do not record raw
internal reasoning, mechanical edits, or large logs. For Mini SDAD, include a
short implementation-notes section in the evidence-ready summary only when a
spec-unstated decision happened.

Use ADRs sparingly. A decision normally deserves an ADR only when it is hard to
reverse, would surprise a future maintainer without context, and represents a
real tradeoff. Smaller spec-unstated implementation choices belong in
implementation notes.

Do not overwrite existing project files without showing me what will change.
Completion requires evidence, not AI confidence.

For Mini SDAD at loop end, do not check SPEC-COMPLETE, TODO, review-findings, or
ADRs unless the project has escalated. Report the active task, changed files,
check evidence, limitations or unverified behavior, evidence-ready status, owner
decisions or acceptance needed, and whether to escalate.

For Standard or Full SDAD at loop end, check whether SPEC-COMPLETE, TODO,
review-findings, rules, or ADRs must be updated at the packet or handoff
boundary. If nothing changes, say which files were checked and why no update was
needed.

Create a session handoff only when another session, tool, person, or machine
actually needs continuity and reconstruction would otherwise be costly. A stop,
redirect, block, or partial result alone does not require one. When triggered,
write it under
docs/sdad/handoffs/YYYY-MM-DD-HNNNN-topic.md. Allocate HNNNN as the next
zero-padded ID among handoffs with that same date; restart at H0001 on a new
date, and treat current_handoff as the sole currentness signal. Cite the full
date-plus-ID path because HNNNN may repeat across dates. Existing unnumbered
handoffs remain valid. Write the same ID in the first Session Identity as
`- Handoff ID: HNNNN`. Treat the chat as an execution trace, not permanent
memory; a fresh session must be able to continue from the handoff, active spec,
and current repository state.
Reference existing SPECs, ADRs, TODOs, review findings, implementation notes,
logs, or evidence files by path or URL instead of duplicating long content in
the handoff. Add `current_handoff` only while that handoff is current and require
its packet marker to match `active_packet.id`; clear or replace the pointer when
the packet changes or the handoff is retired.

When I authorize a protected action conditionally, record: Decision, Authorized
action, Packet, Conditions, Expires when, and Evidence required before action.
Reuse that authorization only while the action, packet, conditions, source/artifact identity, and
expiry remain unchanged. Ask again when any term changes or the authorization
expires.

Markdown records instructions and decisions; it does not technically prevent a
tool from acting. Permissions, hooks, sandboxes, protected branches, and service
controls provide enforcement. Tool-native sessions, checkpoints, and diagnostic
commands are conveniences, not substitutes for SDAD state, handoff, or Doctor.

For a stateful Standard or Full project, use a real SDAD checkout and run:

python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.2 [--json] [--strict]

Doctor version, state schema version, and JSON report schema version are
separate contracts. The version guard identifies the Doctor code being run.
Doctor green proves structural consistency only; it does not execute validation
commands, prove product correctness, grant owner acceptance, or prove that SDAD
3.2 is more effective than another method.

Sensitive data is an authorization boundary, not a size threshold. Use
metadata-only inspection by default. Do not read, copy, transmit, summarize, or
paste `.env` files, credentials, private keys, tokens, cookies, raw customer
records, or private corpora into AI context unless the task requires it and
owner policy plus tool policy explicitly permit it. Prefer redacted samples;
if authorization is unclear, stop before reading the content and ask.

Before reading large state files, archives, logs, generated artifacts,
authorized private data, or broad search output, check size and use bounded reads: headings,
current sections, targeted matches, output limits, and explicit excludes. If
chat stability degrades, suspect context growth before changing runtime code.
Keep repo-packing, graphing, embedding, indexing, and context-building tool
ignore files aligned with this rule.

For Mini SDAD, an AI may call a unit evidence-ready when changed files, check
evidence, implementation notes for spec-unstated decisions, and limitations or
unverified behavior are shown. Do not call final completion done until owner
acceptance is shown or the owner has explicitly delegated the acceptance policy.
```

## Option 2: One-Paste PowerShell Installer

Paste this into PowerShell from your target project root.

Change `$adapter = "codex"` if you use another tool.

```powershell
$ErrorActionPreference = "Stop"
$adapter = "codex" # codex, claude-code, gemini-cli, cursor, github-copilot, generic
$revision = "adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd" # stable v3.2.2 baseline
$base = "https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/$revision"
$files = @{
  "codex" = @("adapters/codex/AGENTS.md", "AGENTS.md", "8237f7905ba8ce0db95e77b5d40e54200062d2654adae45e667f04743f342e08")
  "claude-code" = @("adapters/claude-code/CLAUDE.md", "CLAUDE.md", "57a9431eecc5d8e2dfdfe71eb59ad673ff230db5c320197291a8a7a129f875ce")
  "gemini-cli" = @("adapters/gemini-cli/GEMINI.md", "GEMINI.md", "b3a6e16c21e14e594bdc5560838c664e3116ef1ee1366724a6b39a19a9e2e76b")
  "cursor" = @("adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc", ".cursor/rules/spec-driven-ai-development.mdc", "789d378813f7b32f0e677265fa23c7908cf6b52342fc54e92455d05293038bfc")
  "github-copilot" = @("adapters/github-copilot/.github/copilot-instructions.md", ".github/copilot-instructions.md", "ee914a5ebaa5413c7bfd43d21b48e6919fc3e373afed5707bc6076acf5a573b3")
  "generic" = @("adapters/generic/AI-SESSION-INSTRUCTIONS.md", "AI-SESSION-INSTRUCTIONS.md", "15e02a42c32e46b332dc217ac43abad958d35e5a153f0f9746be42a32eee5ec2")
}
if (-not $files.ContainsKey($adapter)) { throw "Unknown adapter: $adapter" }
$source, $target, $expectedSha256 = $files[$adapter]
$targetRoot = (Get-Location).ProviderPath
$targetParts = $target -split '[\\/]'
$targetDir = $targetRoot
for ($index = 0; $index -lt $targetParts.Length - 1; $index++) {
  $targetDir = Join-Path $targetDir $targetParts[$index]
  if (Test-Path -LiteralPath $targetDir) {
    $item = Get-Item -Force -LiteralPath $targetDir
    if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
      throw "Refusing to install through linked path: $targetDir"
    }
    if (-not $item.PSIsContainer) { throw "Target parent is not a directory: $targetDir" }
  } else {
    New-Item -ItemType Directory -Path $targetDir | Out-Null
  }
}
$targetPath = Join-Path $targetRoot $target
$targetItem = Get-Item -Force -LiteralPath $targetPath -ErrorAction SilentlyContinue
if ($targetItem) {
  if (($targetItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
    throw "Refusing to install through linked path: $targetPath"
  }
  throw "Target already exists: $targetPath"
}
$tempPath = Join-Path $targetDir (".sdad-download." + [guid]::NewGuid().ToString("N") + ".tmp")
try {
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  Invoke-WebRequest -Uri "$base/$source" -OutFile $tempPath -MaximumRedirection 0
  if (-not (Test-Path -LiteralPath $tempPath -PathType Leaf) -or (Get-Item $tempPath).Length -eq 0) {
    throw "Downloaded adapter is empty: $base/$source"
  }
  $actualSha256 = (Get-FileHash -LiteralPath $tempPath -Algorithm SHA256).Hash.ToLowerInvariant()
  if ($actualSha256 -ne $expectedSha256) {
    throw "SHA-256 mismatch for $source. Expected $expectedSha256, got $actualSha256"
  }
  [IO.File]::Move($tempPath, $targetPath)
} finally {
  if (Test-Path -LiteralPath $tempPath) { Remove-Item -LiteralPath $tempPath -Force }
}
Write-Host "Installed $adapter instructions to $targetPath"
Write-Host "Next prompt: Read $targetPath and bootstrap this project with the SDAD Protocol (SPEC-Directed AI Development)."
```

## Option 3: One-Paste Bash Installer

Paste this into Bash, zsh, WSL, macOS Terminal, or Linux shell from your target
project root.

Change `adapter="codex"` if you use another tool.

```bash
set -euo pipefail
adapter="codex" # codex, claude-code, gemini-cli, cursor, github-copilot, generic
revision="adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd" # stable v3.2.2 baseline
base="https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/$revision"
case "$adapter" in
  codex)
    source="adapters/codex/AGENTS.md"
    target="AGENTS.md"
    expected_sha256="8237f7905ba8ce0db95e77b5d40e54200062d2654adae45e667f04743f342e08"
    ;;
  claude-code)
    source="adapters/claude-code/CLAUDE.md"
    target="CLAUDE.md"
    expected_sha256="57a9431eecc5d8e2dfdfe71eb59ad673ff230db5c320197291a8a7a129f875ce"
    ;;
  gemini-cli)
    source="adapters/gemini-cli/GEMINI.md"
    target="GEMINI.md"
    expected_sha256="b3a6e16c21e14e594bdc5560838c664e3116ef1ee1366724a6b39a19a9e2e76b"
    ;;
  cursor)
    source="adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc"
    target=".cursor/rules/spec-driven-ai-development.mdc"
    expected_sha256="789d378813f7b32f0e677265fa23c7908cf6b52342fc54e92455d05293038bfc"
    ;;
  github-copilot)
    source="adapters/github-copilot/.github/copilot-instructions.md"
    target=".github/copilot-instructions.md"
    expected_sha256="ee914a5ebaa5413c7bfd43d21b48e6919fc3e373afed5707bc6076acf5a573b3"
    ;;
  generic)
    source="adapters/generic/AI-SESSION-INSTRUCTIONS.md"
    target="AI-SESSION-INSTRUCTIONS.md"
    expected_sha256="15e02a42c32e46b332dc217ac43abad958d35e5a153f0f9746be42a32eee5ec2"
    ;;
  *)
    echo "Unknown adapter: $adapter" >&2
    exit 1
    ;;
esac
target_root="$(pwd -P)"
target_parent_rel="$(dirname "$target")"
target_dir="$target_root"
if [[ "$target_parent_rel" != "." ]]; then
  IFS='/' read -r -a target_parts <<< "$target_parent_rel"
  for part in "${target_parts[@]}"; do
    next_dir="$target_dir/$part"
    if [[ -L "$next_dir" ]]; then
      echo "Refusing to install through linked path: $next_dir" >&2
      exit 1
    fi
    if [[ -e "$next_dir" && ! -d "$next_dir" ]]; then
      echo "Target parent is not a directory: $next_dir" >&2
      exit 1
    fi
    if [[ ! -e "$next_dir" ]]; then mkdir -- "$next_dir"; fi
    target_dir="$next_dir"
  done
fi
target_path="$target_dir/$(basename "$target")"
if [[ -e "$target_path" || -L "$target_path" ]]; then
  echo "Target already exists: $target_path" >&2
  exit 1
fi
temp_path="$(mktemp "$target_dir/.sdad-download.XXXXXX")"
cleanup() { rm -f -- "$temp_path"; }
trap cleanup EXIT
curl --proto '=https' --tlsv1.2 --fail --silent --show-error --location "$base/$source" --output "$temp_path"
if [[ ! -s "$temp_path" ]]; then
  echo "Downloaded adapter is empty: $base/$source" >&2
  exit 1
fi
if command -v sha256sum >/dev/null 2>&1; then
  actual_sha256="$(sha256sum "$temp_path" | awk '{print $1}')"
elif command -v shasum >/dev/null 2>&1; then
  actual_sha256="$(shasum -a 256 "$temp_path" | awk '{print $1}')"
else
  echo "A SHA-256 tool (sha256sum or shasum) is required." >&2
  exit 1
fi
if [[ "$actual_sha256" != "$expected_sha256" ]]; then
  echo "SHA-256 mismatch for $source. Expected $expected_sha256, got $actual_sha256" >&2
  exit 1
fi
if ! ln -- "$temp_path" "$target_path"; then
  echo "Target appeared during installation: $target_path. Nothing was overwritten." >&2
  exit 1
fi
if [[ ! -f "$target_path" ]]; then
  nested_temp="$target_path/$(basename "$temp_path")"
  if [[ -f "$nested_temp" ]]; then rm -- "$nested_temp"; fi
  echo "Publication did not create the exact target file: $target_path" >&2
  exit 1
fi
rm -- "$temp_path"
trap - EXIT
echo "Installed $adapter instructions to $target_path"
echo "Next prompt: Read $target_path and bootstrap this project with the SDAD Protocol (SPEC-Directed AI Development)."
```

## After The Installer

Check the capability disclosed above. The stable v3.2.2 manifest declares
`progressive_control_plane=true`, so the prompt below applies to both a local
v3.2.2 checkout and its pinned no-clone sources. Keep the revision, source path,
and checksum from one manifest together.

Open your AI coding tool in the target project and say:

```text
Read the installed SDAD Protocol instruction file. Infer the smallest scale,
`unit` or `packet` execution scope, validation claim boundary, and applicable
owner gates from my request and this repository. Report the inference and its
explicit assumptions. Ask at most one blocking question only if an unresolved
fact would change objective/direction, authority/reference role, execution
boundary, protected action/gate, or claim boundary; otherwise proceed. For
Standard or Full, bootstrap state version 2 with one executable
active packet, packet-owned validation, and the compact state -> INDEX ->
intent-selected route. Work through Plan -> Route -> Implement -> Verify ->
Report until evidence-ready, but stop before any unapproved owner gate.
```

The first successful bootstrap should create or update:

- `sdad-state.yaml`,
- `docs/INDEX.md`,
- `docs/Repository-Operating-Rules.md`,
- the on-demand files under `docs/sdad/playbooks/`,
- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- `docs/implementation-notes.md`.

It should not create or route `save-state.md` for state v2. A handoff is
conditional and becomes current only through a packet-bound `current_handoff`.

When product, hardware, compatibility, packaging, remote tester, external lab,
or release claims need evidence stronger than local software tests, it should
also create only the needed product evidence templates:

- `docs/evidence-matrix.md`,
- `docs/claim-registry.md`,
- `docs/artifact-contracts.md`,
- `docs/work-packet-state.md`,
- `docs/remote-evidence-import.md`.

These optional evidence files are create-on-demand. A lean Standard bootstrap
may route them from `docs/INDEX.md` without creating all of them immediately.
Create them only when the current claim needs that evidence boundary.

If those files already exist, the AI should show the proposed changes before
editing them.
