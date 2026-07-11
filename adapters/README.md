# Tool Adapters

These files render the same compact SDAD Protocol runtime kernel for supported
AI coding tools:

- `codex/AGENTS.md`
- `claude-code/CLAUDE.md`
- `gemini-cli/GEMINI.md`
- `cursor/.cursor/rules/spec-driven-ai-development.mdc`
- `github-copilot/.github/copilot-instructions.md`
- `generic/AI-SESSION-INSTRUCTIONS.md`

Install the adapter matching the active tool. Install multiple adapters only
when the repository intentionally uses multiple tools and will keep them
synchronized.

Verify this checkout first:

```bash
python scripts/render_agent_surfaces.py --check
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

Repository validation requires Python 3.10 or newer. Gemini CLI installs its
adapter as repository-root `GEMINI.md`.

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter gemini-cli -TargetPath C:\path\to\project
```

```bash
./scripts/install-agent-adapter.sh gemini-cli /path/to/project
```

If a checkout lost executable bits, prefix the matching command with Bash, for
example `bash ./scripts/install-agent-adapter.sh claude-code /path/to/project`.

Installation produces guidance, not enforcement. Markdown may record authority
but cannot technically block tools. Use Doctor/tests/CI for validation,
permissions/hooks/sandbox/branch protection/release controls for enforcement,
and explicit owner records for authorization and acceptance.
