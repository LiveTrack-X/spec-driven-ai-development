# Tool Adapters

These adapters let SPEC-Driven AI Development run in different AI coding tools.

Install the one adapter that matches the active tool. Install multiple adapters
only when the repository intentionally uses multiple tools and will keep their
shared contract synchronized:

- `codex/AGENTS.md`
- `claude-code/CLAUDE.md`
- `gemini-cli/GEMINI.md`
- `cursor/.cursor/rules/spec-driven-ai-development.mdc`
- `github-copilot/.github/copilot-instructions.md`
- `generic/AI-SESSION-INSTRUCTIONS.md`

Before installing, you can verify this repository with:

```bash
python scripts/render_agent_surfaces.py --check
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

Repository validation requires Python 3.10 or newer.

Then copy an adapter manually or use an installer.
Gemini CLI installs its adapter as repository-root `GEMINI.md`.

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter gemini-cli -TargetPath C:\path\to\project
```

```bash
./scripts/install-agent-adapter.sh gemini-cli /path/to/project
```

If your checkout lost executable bits, use
`bash ./scripts/install-agent-adapter.sh claude-code /path/to/project` or prefix
the matching Bash command with `bash`.
Adapter installation produces guidance, not enforcement; use CI, permissions,
and owner gates for guarantees.
