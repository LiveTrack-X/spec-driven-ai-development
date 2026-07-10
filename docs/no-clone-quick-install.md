# No-Clone Quick Install

Use this when you want to apply SPEC-Driven AI Development without cloning this
repository first.

The easiest option is Option 1. It does not require terminal commands, Git,
Python, or Codex.

## Before You Start

Pick the path that matches your comfort level:

| Path | Best for | Requires |
|---|---|---|
| [Give this to your AI agent](#option-1-give-this-to-your-ai-agent) | Complete beginners | An AI coding tool that can edit files |
| [One-paste PowerShell installer](#option-2-one-paste-powershell-installer) | Windows users comfortable with terminal | PowerShell and internet access |
| [One-paste Bash installer](#option-3-one-paste-bash-installer) | macOS/Linux/WSL users comfortable with terminal | Bash, curl, and internet access |
| [Clone this repository](getting-started.md#get-this-repository) | Developers who want the full package locally | Git |
| [Codex skill](../README.md#codex-skill) | Codex users only | Codex installed and configured |

Run terminal commands from the root of the project you want to control.

Chat-only tools such as Claude.ai, ChatGPT web, or browser chat can discuss the
workflow, but they cannot install adapters unless they have project filesystem
access. Claude Code means the local/CLI coding tool, not Claude.ai chat.

## Step 0: Choose Scale

Before installing an adapter or creating project files, choose the smallest
workflow scale that fits.

Ask:

1. Will this take more than one AI session?
2. Will you come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, real user data, auth, money, security, rollback,
   destructive action, or production risk?

Override rules beat raw yes-counts:

| Trigger | Scale | What to create |
|---|---|---|
| 0 yes | One-shot prompt | No project files |
| 1-2 yes from Q1-Q3 only, with Q4=no and Q5=no | Mini SDAD | One instruction file from `templates/mini-sdad/MINI-SDAD.md` |
| Q4=yes or 3 yes total | Standard SDAD | Adapter plus core control files |
| Q5=yes, but the packet only inspects, documents, or tests the risk area | Standard SDAD minimum | Adapter, core control files, and explicit risk tracking |
| Q5=yes and the packet changes, accepts, or executes the gate | Full SDAD | Adapter, core files, review, conditional ADRs, risk gates |
| 4-5 yes | Full SDAD | Adapter, core files, review, conditional ADRs, active risk gates |

When unsure, choose the smaller scale only if no Q5 gate is active. Escalate
later when repeated pain, context loss, risk, or multiple sessions appear.

Product evidence flag: ask whether product, hardware, compatibility, packaging,
remote tester, external lab, or release claims need evidence stronger than local
software tests. A yes is not automatically Full SDAD, but it triggers the
relevant product evidence templates. Use Standard SDAD minimum when those
templates must persist across sessions. Changing, accepting, or executing a Q5
release, production, user-data, auth, money, migration, destructive-action, or
rollback gate still requires Full SDAD.

## Maintenance Cost

Do not create Standard or Full SDAD files unless you will keep them current.

At the end of every Standard or Full SDAD work packet, handoff, or session,
check and update:

- `SPEC/SPEC-COMPLETE.md`,
- `docs/TODO-Open-Items.md`,
- `review-findings.md`,
- `docs/implementation-notes.md` when implementation made a spec-unstated
  assumption, change, compromise, rejected alternative, owner-relevant tradeoff,
  follow-up, or verification-impact note,
- operating rules or ADRs when decisions or repeated pain changed,
- `save-state.md` when a session pauses or ends, handoff is expected, owner
  direction changes, blocked/partial/unverified state remains, or context would
  be expensive to reconstruct.

Keep active live-state files short enough to read as current operating state.
If state, TODO, review, or handoff files become long journals, preserve old
material in archive/history files and use bounded reads for archives, logs,
generated artifacts, authorized private data, and broad search output.
As a default soft trigger, use bounded reads for files over 50 KB or 500 lines,
run a context-stability check for files over 200 KB or 2,000 lines, and do not
read files over 1 MB in full during startup unless the owner explicitly asks for
historical reconstruction.

If no file needs a content change, state which files were checked and why no
update was needed.

Mini SDAD still has a completion gate: changed files, check evidence, and
limitations or unverified behavior must be shown before a slice is called
evidence-ready. Owner acceptance is still required before final done unless the
owner delegates that acceptance policy.

If this cost is too high, choose One-shot Prompt or Mini SDAD instead.

## What Is A Codex Skill?

A Codex skill is an optional local instruction package for OpenAI Codex. It tells
Codex how to behave when starting or managing a SPEC-driven project.

You do not need the Codex skill if you use Claude Code, Cursor, GitHub Copilot,
another AI coding agent, or Option 1 below.

## How To Know It Worked

After Mini, Standard, or Full setup, your project should have one of these
instruction files:

- `AGENTS.md` for Codex,
- `CLAUDE.md` for Claude Code,
- `.cursor/rules/mini-sdad.mdc` for Cursor Mini, or
  `.cursor/rules/spec-driven-ai-development.mdc` for Cursor Standard/Full,
- `.github/copilot-instructions.md` for GitHub Copilot,
- `AI-SESSION-INSTRUCTIONS.md` for a generic AI tool.

After Standard or Full bootstrap, your project should also have control files
such as `SPEC/SPEC-COMPLETE.md`, `docs/TODO-Open-Items.md`,
`review-findings.md`, and `docs/implementation-notes.md`.

## Exact Adapter Sources

For Mini SDAD, use this exact template:

```text
https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/templates/mini-sdad/MINI-SDAD.md
```

Expected SHA-256:
`f5370ba6539ab55b88fc10a7589ca7f42fa6714072830620aad7dab60d21f669`.

Before fetching Mini SDAD, state that you are installing Mini SDAD and explain
why this scale was chosen.

For Standard or Full SDAD, do not ask an AI agent to guess adapter paths. Use
these exact source URLs:

| Tool | Source URL | Save as | SHA-256 |
|---|---|---|---|
| Codex | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/codex/AGENTS.md` | `AGENTS.md` | `fc1ecaf1d373c26784d5e1c6113531a16de295c1177bd2ee5ebcb7ba7b4d2bba` |
| Claude Code | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/claude-code/CLAUDE.md` | `CLAUDE.md` | `dc14598dee6645801ca04b3802216a38c87f5ae64fefaa0275daa01e88c865f5` |
| Gemini CLI | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/gemini-cli/GEMINI.md` | `GEMINI.md` | `a35f1210bd5f8ed688b2c7ee82d29c505b29632a8da8295fa639a6f799f1ab23` |
| Cursor | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc` | `.cursor/rules/spec-driven-ai-development.mdc` | `371ee47e6d0712e37ce8381696cc0a5c1660d9a770157f9034ac9f2a150a0c68` |
| GitHub Copilot | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/github-copilot/.github/copilot-instructions.md` | `.github/copilot-instructions.md` | `335209bcfee60dbb9ddce7a6c92def0d173d793680dec2e58b7f1757e788b3b4` |
| Generic AI tool | `https://raw.githubusercontent.com/LiveTrack-X/spec-driven-ai-development/1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa/adapters/generic/AI-SESSION-INSTRUCTIONS.md` | `AI-SESSION-INSTRUCTIONS.md` | `9664f9c868e19a585fd3e64c96d79eac717ae6696c02c721d29233d287f90e75` |

## Latest Versus Pinned Sources

The URLs above use the full 40-character commit SHA for the stable v3.1.0
baseline. A commit ID is immutable. A readable release tag can move unless the
repository makes it immutable, while `main` intentionally changes over time.

Use `/main/` only when you explicitly want the latest, unpinned instructions.
Record the chosen revision in setup notes or the project handoff. Do not mix
`main` and a pinned revision in the same install unless the difference is
intentional and documented.

[`install-sources.json`](../install-sources.json) is the canonical
revision/path/hash contract used by repository validation.

The current stable manifest declares `progressive_control_plane=true`. Its
v3.1.0 adapters include the `sdad-state.yaml -> docs/INDEX.md -> on-demand
route`. Follow the installed baseline instructions and keep its pinned revision
and hashes together; use `/main/` only when intentionally testing changing,
unpinned content.

## Option 1: Give This To Your AI Agent

Paste this into Codex, Claude Code, Gemini CLI, Cursor, Copilot Chat, or another AI coding
agent:

```text
Use SPEC-Driven AI Development as the project control method.

Source repository:
https://github.com/LiveTrack-X/spec-driven-ai-development

Do not require me to clone the repository unless absolutely necessary.

First determine whether you can edit files in this project.
If this is a chat-only environment such as Claude.ai, ChatGPT web, or another
browser chat with no project filesystem, do not install adapters or claim files
were saved. Use this repository for planning only, then tell me to open the
project in Codex, Claude Code, Gemini CLI, Cursor, Copilot Chat, or another file-editing AI
coding tool.

Step 0 - Choose scale before creating files.

Ask me these five questions:
1. Will this take more than one AI session?
2. Will I come back to this project later?
3. Does "done" need evidence beyond "AI said so"?
4. Will multiple AI tools or reviewers be involved?
5. Is there release, migration, real user data, auth, money, security, rollback,
   destructive action, or production risk?

Choose:
- 0 yes -> One-shot prompt. Do not create project files.
- 1-2 yes from questions 1-3 only, with Q4=no and Q5=no -> Mini SDAD.
  Create only one instruction file.
- Q4=yes or 3 yes total -> Standard SDAD. Create core control files.
- Q5=yes, but this packet only inspects, documents, or tests the risk area ->
  Standard SDAD minimum, even if it is the only yes.
- Q5=yes and this packet changes, accepts, or executes the gate -> Full SDAD.
- 4-5 yes -> Full SDAD. Use full workflow, review, conditional ADRs, and
  active gates.

Override rules beat raw yes-counts. When unsure, choose the smaller scale only
if no Q5 gate is active, and explain why.

Step 0.1 - Check product evidence flag.

Ask whether product, hardware, compatibility, packaging, remote tester,
external lab, or release claims need evidence stronger than local software
tests. A yes is not automatically Full SDAD, but it triggers the relevant
product evidence templates. Use Standard SDAD minimum when those templates must
persist across sessions. Changing, accepting, or executing a Q5 release,
production, user-data, auth, money, migration, destructive-action, or rollback
gate still requires Full SDAD.

Step 0.5 - Choose autonomy before implementation.

Use these defaults unless I say otherwise:
- One-shot prompt -> no persistent autonomy contract.
- Mini SDAD -> Level 1 Unit Autonomy, treated as one small approved packet.
- Standard SDAD -> Level 2 Work Packet Autonomy.
- Full SDAD or Q5 risk -> Level 2 for implementation, with Level 4 gates for
  release, migration, destructive actions, data/auth/money/security decisions,
  rollback, and production claims.

A work packet may contain one or more review-worthy development units. Do not
ask me to approve every micro-task, every small SPEC item, or every
evidence-ready unit inside an approved packet. A unit is an internal review and
evidence slice, not a separate owner-approval boundary unless I say so. Continue
until the packet reaches a checkpoint or a stop condition appears.

Step 0.6 - Choose operating intensity for Standard or Full SDAD.

Use this notation:
- Standard SDAD / High
- Standard SDAD / Medium
- Standard SDAD / Low
- Full SDAD / High
- Full SDAD / Medium
- Full SDAD / Low

High / Medium / Low are operating intensities, not new project scales or
autonomy levels. Mini SDAD does not use operating intensity tiers.

Use Standard SDAD / High for a non-Q5 packet with a major product or
architecture tradeoff, a hard-to-reverse implementation choice, or an explicit
owner checkpoint.

Q5 projects do not make every packet High. Raise the current packet to
Full SDAD / High only when it changes behavior, policy, boundary, evidence
claim, or risk acceptance for a Q5 gate: release, production claim, migration,
destructive action, real user data handling, auth, data, money, security,
rollback, accepted-memory boundary, external deployment, or major
owner-controlled risk decision. Lower intensity when control surfaces reduce
controllability.

Step 0.7 - Route natural-language requests.

Do not require me to know SDAD terms, adapter names, or skill names. Infer the
work intent from my sentence and the current repository state.

Common intents:
- "check", "review", "audit", "find bugs" -> review or audit intent.
- "implement", "build", "fix", "match the spec" -> SPEC implementation intent.
- "release", "publish", "tag" -> release intent with Level 4 gates.
- "document", "explain", "README", "FAQ", "guide" -> documentation intent.
- "handoff", "continue later", "next session", "lost context" -> handoff or
  save-state intent.
- "borrow from this repo", "reference this project", "adopt this idea" ->
  reference-intake intent.
- "asks too often", "runs ahead" -> autonomy tuning intent.

Treat narrative modifiers as routing signals, not automatic scope expansion.
"Carefully" increases inspection depth, "fully" continues to evidence-ready for
the approved scope, "minimal" selects compression rather than weaker evidence,
and "commit and wait" does not imply push, release, or deploy unless named.

If multiple intents match, first decide whether they can be safely composed
inside one approved packet. If one route remains dominant, proceed and briefly
state the interpreted intent, SDAD scale/intensity, autonomy level, and expected
evidence. If the combination changes scope, risk, claim level, owner gate, or
durable-doc requirements, ask one blocking clarification question with your
recommended default. Do not use natural-language routing to bypass release,
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

For Standard or Full SDAD, after installing the instruction file, bootstrap this
project:

1. create or update sdad-state.yaml,
2. create or update docs/INDEX.md as a routing-only file,
3. create or update docs/Repository-Operating-Rules.md and the on-demand
   docs/sdad/playbooks/ files,
4. create or update SPEC/SPEC-COMPLETE.md,
5. create or update docs/TODO-Open-Items.md,
6. create or update review-findings.md,
7. create or update docs/implementation-notes.md,
8. if the product evidence flag is yes, create only the needed maintained
   product evidence templates: docs/evidence-matrix.md,
   docs/claim-registry.md, docs/artifact-contracts.md,
   docs/work-packet-state.md, and docs/remote-evidence-import.md,
9. ask me for product pain, smallest useful version, non-goals, risks,
   owner-controlled decisions, the first work packet, the review-worthy units
   inside it, and evidence required for completion.

Keep the fixed read path compact: adapter -> sdad-state.yaml -> docs/INDEX.md ->
current source/tests -> only the routed policy heading or playbook. Do not load
the whole rulebook or optional evidence set by default.

A review-worthy development unit may contain multiple related small tasks. It
should be large enough that review has meaning, but small enough to verify in one
handoff. Do not stop for owner approval after every micro-task or small SPEC
item inside an approved work packet.

Proceed autonomously inside the approved work packet until evidence is ready.
Stop and ask me only when scope would expand, a Q5 risk changes, a destructive
or irreversible action is needed, an owner-controlled decision is required,
verification is blocked, or the requested work conflicts with current evidence.

When the plan is fuzzy, run a clarification checkpoint before coding. Inspect
the current code, tests, active docs, SPEC, TODOs, review findings, and ADRs
first. Ask me only for unresolved blocking questions, one at a time. Include
your recommended answer, why the question matters, and what changes if I choose
differently. Do not use clarification checkpoints as micro-approval.

If repeated ambiguity comes from overloaded domain terms, propose one canonical
term and one short definition. For Standard or Full SDAD, create or update a
small glossary routed from docs/INDEX.md only when terminology drift affects
implementation, review, tests, or owner decisions.

Implement from the active SPEC. When implementation requires a judgment the
SPEC does not explicitly cover, record the assumption, change, compromise,
alternative rejected, owner-relevant tradeoff, follow-up, and verification
impact in implementation notes. Do not record raw internal reasoning,
mechanical edits, or large logs. For Standard or Full SDAD, keep current notes
in docs/implementation-notes.md; for Mini SDAD, include a short Implementation
notes section in the evidence-ready summary only when a spec-unstated decision
happened.

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
review-findings, rules, or ADRs must be updated at the work-packet or handoff
boundary. If nothing changes, say which files were checked and why no update was
needed.

Update save-state.md when a session pauses or ends, handoff is expected, owner
direction changes, blocked/partial/unverified state remains, or context would be
expensive to reconstruct.

Before closing, archiving, replacing, or restarting a long AI coding session,
create a session handoff under docs/sdad/handoffs/YYYY-MM-DD-topic.md. Treat
the chat as an execution trace, not permanent memory; a fresh session must be
able to continue from the handoff, active spec, and current repository state.
Reference existing SPECs, ADRs, TODOs, review findings, implementation notes,
logs, or evidence files by path or URL instead of duplicating long content in
the handoff.

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
Read the installed SPEC-Driven AI Development instruction file.
Bootstrap the compact state -> INDEX -> on-demand route and the first active
SPEC slice.
Define the first low-intervention work packet and its review-worthy units.
Ask me for product pain, smallest useful version, non-goals, risks,
owner-controlled decisions, autonomy level, and evidence required for completion.
If my request uses normal language instead of SDAD terms or skill names, infer
the intent, state the interpreted intent briefly, then route to the smallest
safe SDAD mode.
When the plan is fuzzy, inspect repository evidence first, then ask only the
next blocking clarification question with your recommended answer.
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
