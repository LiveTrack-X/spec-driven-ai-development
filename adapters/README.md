# Tool Adapters

These adapters let SPEC-Driven AI Development run in different AI coding tools.

Use one or more:

- `codex/AGENTS.md`
- `claude-code/CLAUDE.md`
- `cursor/.cursor/rules/spec-driven-ai-development.mdc`
- `github-copilot/.github/copilot-instructions.md`
- `generic/AI-SESSION-INSTRUCTIONS.md`

Before installing, you can verify this repository with:

```bash
python scripts/validate_repo.py
```

Then copy an adapter manually or use an installer.

```powershell
.\scripts\install-agent-adapter.ps1 -Adapter claude-code -TargetPath C:\path\to\project
```

```bash
./scripts/install-agent-adapter.sh claude-code /path/to/project
```
