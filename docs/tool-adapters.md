# Tool Adapters

Status: Active reference

SDAD Protocol is tool-neutral. An adapter is a compact rendering of the same
repository runtime kernel, not the whole method and not technical enforcement.
After installation, ordinary work follows the adapter -> `sdad-state.yaml` ->
`docs/INDEX.md` route and selects only the source/tests and routed content needed
for the current intent.

## Supported Adapters

| Tool | Adapter file |
| --- | --- |
| Codex | `AGENTS.md` plus optional `ai-spec-project-start` install/upgrade skill |
| Claude Code | `CLAUDE.md` |
| Gemini CLI | repository-root `GEMINI.md` |
| Cursor | `.cursor/rules/spec-driven-ai-development.mdc` |
| GitHub Copilot | `.github/copilot-instructions.md` |
| Generic AI coding tool | `AI-SESSION-INSTRUCTIONS.md` |

Install one adapter unless the repository intentionally uses multiple tools and
will keep their shared contract synchronized.

## Install An Adapter

PowerShell:

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter gemini-cli -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter cursor -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter github-copilot -TargetPath C:\path\to\project
.\scripts\install-agent-adapter.ps1 -Adapter generic -TargetPath C:\path\to\project
```

macOS/Linux:

```bash
./scripts/install-agent-adapter.sh claude-code /path/to/project
./scripts/install-agent-adapter.sh gemini-cli /path/to/project
./scripts/install-agent-adapter.sh cursor /path/to/project
./scripts/install-agent-adapter.sh github-copilot /path/to/project
./scripts/install-agent-adapter.sh generic /path/to/project
```

If a checkout lost executable bits, use Bash explicitly, for example:

```bash
bash ./scripts/install-agent-adapter.sh claude-code /path/to/project
```

The installer refuses to overwrite existing files unless `-Force` or `--force`
is used.

## Runtime Contract

Adapters keep only high-signal rules:

- load state and INDEX before optional guidance;
- treat `routed_docs` as eligible selections, never a full-read list;
- infer the scale, execution scope, and owner gates from repository evidence;
- default Mini to `unit` and Standard/Full to `packet`;
- use Plan -> Route -> Implement -> Verify -> Report, branching to an owner gate
  or handoff only when triggered;
- separate validation evidence, owner authorization, and owner acceptance;
- record each durable fact in its single authoritative home;
- delegate packet, objective, scope, routes, validation, gates, stop condition,
  and report requirements because a worker may not inherit parent context;
- keep archives, logs, generated artifacts, databases, and authorized private
  data behind bounded reads.

The canonical runtime kernel is
`templates/project-control-files/AGENTS.md`. Render every adapter with:

```bash
python scripts/render_agent_surfaces.py --write
```

Check parity without writing:

```bash
python scripts/render_agent_surfaces.py --check
```

## Guidance, Validation, Enforcement, And Decisions

Adapter installation produces guidance, not enforcement. Markdown can record an
authority rule, but it cannot technically block a tool. Use Doctor/tests/CI for
deterministic validation and permissions, hooks, sandboxing, deny rules, branch
protection, release gates, or deployment controls for enforcement. Owner
authorization and acceptance remain owner decisions. None of these layers may
upgrade weak evidence into a stronger claim.

Provider sandbox, policy, permission, trusted-folder, plan, checkpoint, session,
memory, and doctor/health features remain provider facilities. They can help the
workflow but do not become SDAD state, handoff, Doctor, authorization, or
acceptance authority.

## Tool Notes

Gemini CLI reads repository `GEMINI.md` as project context. Use `/memory show`
to inspect what it loaded. `GEMINI_SYSTEM_MD` replaces the system prompt; it is
not the project adapter install path. Gemini headless Plan Mode is not owner
acceptance and cannot bypass an applicable owner gate.

Nested or path-specific Claude, Cursor, Copilot, or Gemini instructions should
be added only after an observed domain-specific failure justifies the extra
always-loaded context.

Provider references:

- Claude Code project memory: <https://code.claude.com/docs/en/memory>
- Cursor project rules: <https://cursor.com/docs/rules>
- GitHub Copilot repository instructions:
  <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>
- Gemini CLI project context: <https://geminicli.com/docs/cli/gemini-md/>

Tool behavior can change. If a tool stops loading the expected path, preserve
the protocol contract and update the adapter path only after verifying the
provider's current official behavior.
