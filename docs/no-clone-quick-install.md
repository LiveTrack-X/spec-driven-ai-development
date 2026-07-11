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
revision/path/hash contract. Pins remain at the stable v3.1.0 release until the
v3.2 release metadata task rotates them.

## Option 1: Give This To Your AI Agent

Paste this into Codex, Claude Code, Gemini CLI, Cursor, Copilot Chat, or another AI coding
agent:

```text
Use the SDAD Protocol (SPEC-Driven AI Development) as the repository-local
project control method.

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
fact would materially change the scale or an owner gate. Otherwise proceed with
the explicit assumptions. Report:

- Scale and reason
- Execution scope
- Claim boundary
- Owner gates
- Assumptions
- Unresolved question, or `none`

I may override the inference. Keep these three axes separate:

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
- "borrow from this repo", "reference this project", "adopt this idea" ->
  reference-intake intent.
- "asks too often", "runs ahead" -> execution-scope or owner-gate tuning.

Treat narrative modifiers as routing signals, not automatic scope expansion.
"Carefully" increases inspection depth, "fully" continues to evidence-ready for
the approved scope, "minimal" selects compression rather than weaker evidence,
and "commit and wait" does not imply push, release, or deploy unless named.

If multiple intents match, first decide whether they can be safely composed
inside one approved packet. If one route remains dominant, proceed and briefly
state the interpreted intent, scale, execution scope, expected evidence, and
owner gates. Ask one blocking clarification question with your recommended
default only when an unresolved fact would change the scale or an owner gate;
otherwise state the assumptions and proceed. Do not use natural-language
routing to bypass release,
migration, destructive action, real user data, auth, money, security, rollback,
production claim, or other owner-controlled gates.

For Mini SDAD, fetch this exact template:
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/templates/mini-sdad/MINI-SDAD.md
Expected SHA-256: f5370ba6539ab55b88fc10a7589ca7f42fa6714072830620aad7dab60d21f669

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

- Codex -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/codex/AGENTS.md -> ./AGENTS.md -> SHA-256 fc1ecaf1d373c26784d5e1c6113531a16de295c1177bd2ee5ebcb7ba7b4d2bba
- Claude Code -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/claude-code/CLAUDE.md -> ./CLAUDE.md -> SHA-256 dc14598dee6645801ca04b3802216a38c87f5ae64fefaa0275daa01e88c865f5
- Gemini CLI -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/gemini-cli/GEMINI.md -> ./GEMINI.md -> SHA-256 a35f1210bd5f8ed688b2c7ee82d29c505b29632a8da8295fa639a6f799f1ab23
- Cursor -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc -> ./.cursor/rules/spec-driven-ai-development.mdc -> SHA-256 371ee47e6d0712e37ce8381696cc0a5c1660d9a770157f9034ac9f2a150a0c68
- Copilot Chat -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/github-copilot/.github/copilot-instructions.md -> ./.github/copilot-instructions.md -> SHA-256 335209bcfee60dbb9ddce7a6c92def0d173d793680dec2e58b7f1757e788b3b4
- Generic AI agent -> https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/generic/AI-SESSION-INSTRUCTIONS.md -> ./AI-SESSION-INSTRUCTIONS.md -> SHA-256 9664f9c868e19a585fd3e64c96d79eac717ae6696c02c721d29233d287f90e75

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

Use one work loop: Plan -> Route -> Implement -> Verify -> Report. An owner gate
and a handoff are conditional branches, not extra mandatory steps. A clean
verification makes work evidence-ready; only the owner or an explicitly
delegated policy grants owner acceptance.

A review-worthy development unit may contain multiple related small tasks. It
should be large enough that review has meaning, but small enough to verify in one
handoff. Do not stop for owner approval after every micro-task or small SPEC
item inside an approved work packet.

Proceed inside the declared `unit` or `packet` until evidence is ready. Stop and
ask me only when that boundary would expand, a protected condition changes, a
destructive or irreversible action is needed, an owner-controlled decision is
required, verification is blocked, or the request conflicts with evidence.

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

- requirement or acceptance change -> SPEC,
- small implementation-time non-spec decision -> implementation notes,
- hard-to-reverse architecture decision -> ADR,
- unresolved work -> TODO or finding,
- cross-session recovery links and results -> handoff,
- current execution state -> `sdad-state.yaml`.

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

Before closing, archiving, replacing, or restarting a long AI coding session,
create a session handoff under docs/sdad/handoffs/YYYY-MM-DD-topic.md. Treat
the chat as an execution trace, not permanent memory; a fresh session must be
able to continue from the handoff, active spec, and current repository state.
Reference existing SPECs, ADRs, TODOs, review findings, implementation notes,
logs, or evidence files by path or URL instead of duplicating long content in
the handoff. Add `current_handoff` only while that handoff is current and require
its packet marker to match `active_packet.id`; clear or replace the pointer when
the packet changes or the handoff is retired.

When I authorize a protected action conditionally, record: Decision, Authorized
action, Packet, Conditions, Expires when, and Evidence required before action.
Reuse that authorization only while the action, packet, conditions, source, and
expiry remain unchanged. Ask again when any term changes or the authorization
expires.

Markdown records instructions and decisions; it does not technically prevent a
tool from acting. Permissions, hooks, sandboxes, protected branches, and service
controls provide enforcement. Tool-native sessions, checkpoints, and diagnostic
commands are conveniences, not substitutes for SDAD state, handoff, or Doctor.

For a stateful Standard or Full project, use a real SDAD checkout and run:

python <SDAD_CHECKOUT>/scripts/sdad.py --version
python <SDAD_CHECKOUT>/scripts/sdad.py doctor [PROJECT_ROOT] --require-version 3.2.0 [--json] [--strict]

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
$revision = "1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa" # stable v3.1.0 baseline
$base = "https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/$revision"
$files = @{
  "codex" = @("adapters/codex/AGENTS.md", "AGENTS.md", "fc1ecaf1d373c26784d5e1c6113531a16de295c1177bd2ee5ebcb7ba7b4d2bba")
  "claude-code" = @("adapters/claude-code/CLAUDE.md", "CLAUDE.md", "dc14598dee6645801ca04b3802216a38c87f5ae64fefaa0275daa01e88c865f5")
  "gemini-cli" = @("adapters/gemini-cli/GEMINI.md", "GEMINI.md", "a35f1210bd5f8ed688b2c7ee82d29c505b29632a8da8295fa639a6f799f1ab23")
  "cursor" = @("adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc", ".cursor/rules/spec-driven-ai-development.mdc", "371ee47e6d0712e37ce8381696cc0a5c1660d9a770157f9034ac9f2a150a0c68")
  "github-copilot" = @("adapters/github-copilot/.github/copilot-instructions.md", ".github/copilot-instructions.md", "335209bcfee60dbb9ddce7a6c92def0d173d793680dec2e58b7f1757e788b3b4")
  "generic" = @("adapters/generic/AI-SESSION-INSTRUCTIONS.md", "AI-SESSION-INSTRUCTIONS.md", "9664f9c868e19a585fd3e64c96d79eac717ae6696c02c721d29233d287f90e75")
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
Write-Host "Next prompt: Read $targetPath and bootstrap this project into SPEC-Driven AI Development."
```

## Option 3: One-Paste Bash Installer

Paste this into Bash, zsh, WSL, macOS Terminal, or Linux shell from your target
project root.

Change `adapter="codex"` if you use another tool.

```bash
set -euo pipefail
adapter="codex" # codex, claude-code, gemini-cli, cursor, github-copilot, generic
revision="1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa" # stable v3.1.0 baseline
base="https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/$revision"
case "$adapter" in
  codex)
    source="adapters/codex/AGENTS.md"
    target="AGENTS.md"
    expected_sha256="fc1ecaf1d373c26784d5e1c6113531a16de295c1177bd2ee5ebcb7ba7b4d2bba"
    ;;
  claude-code)
    source="adapters/claude-code/CLAUDE.md"
    target="CLAUDE.md"
    expected_sha256="dc14598dee6645801ca04b3802216a38c87f5ae64fefaa0275daa01e88c865f5"
    ;;
  gemini-cli)
    source="adapters/gemini-cli/GEMINI.md"
    target="GEMINI.md"
    expected_sha256="a35f1210bd5f8ed688b2c7ee82d29c505b29632a8da8295fa639a6f799f1ab23"
    ;;
  cursor)
    source="adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc"
    target=".cursor/rules/spec-driven-ai-development.mdc"
    expected_sha256="371ee47e6d0712e37ce8381696cc0a5c1660d9a770157f9034ac9f2a150a0c68"
    ;;
  github-copilot)
    source="adapters/github-copilot/.github/copilot-instructions.md"
    target=".github/copilot-instructions.md"
    expected_sha256="335209bcfee60dbb9ddce7a6c92def0d173d793680dec2e58b7f1757e788b3b4"
    ;;
  generic)
    source="adapters/generic/AI-SESSION-INSTRUCTIONS.md"
    target="AI-SESSION-INSTRUCTIONS.md"
    expected_sha256="9664f9c868e19a585fd3e64c96d79eac717ae6696c02c721d29233d287f90e75"
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
echo "Next prompt: Read $target_path and bootstrap this project into SPEC-Driven AI Development."
```

## After The Installer

Check the capability disclosed above. The stable v3.1.0 manifest declares
`progressive_control_plane=true`, so the prompt below applies to both a local
v3.1.0 checkout and its pinned no-clone sources. Keep the revision, source path,
and checksum from one manifest together.

Open your AI coding tool in the target project and say:

```text
Read the installed SDAD Protocol instruction file. Infer the smallest scale,
`unit` or `packet` execution scope, validation claim boundary, and applicable
owner gates from my request and this repository. Report the inference and its
explicit assumptions. Ask at most one blocking question only if an unresolved
fact would change the scale or an owner gate; otherwise proceed with the stated
assumptions. For Standard or Full, bootstrap state version 2 with one executable
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
