# Contributing

This repository is a workflow and template package. Contributions should improve clarity, repeatability, and evidence-based project control.

## Guidelines

- Keep the human owner in control of direction and acceptance.
- Keep active work separate from future ideas.
- Prefer small, reusable templates over large theory documents.
- Do not claim a workflow works without an example, validation step, or clear acceptance criteria.
- Keep shared version, navigation, and validation contracts aligned across the
  English canonical page and the Korean, Chinese, and Japanese orientation
  pages when those surfaces are present.

## Validation

Use Python 3.10 or newer. Run the full local gate before opening a pull request:

```bash
python scripts/render_agent_surfaces.py --check
python scripts/validate_repo.py
python -m unittest discover -s tests -v
git diff --check
```

Edit `templates/project-control-files/AGENTS.md` as the canonical full-adapter
kernel, then run `python scripts/render_agent_surfaces.py --write`. Do not edit
the five rendered full adapters independently. Keep AGENTS, INDEX, state, and
skill surfaces inside the enforced line/character budgets.

Installer changes must preserve existing files by default, reject destination
paths that escape through links or reparse points, publish a staged file by
replacing its directory entry instead of rewriting an existing inode, and
include Bash plus PowerShell regression coverage for no-clobber and forced
replacement behavior.

Do not report vulnerabilities in a normal pull request or public issue. Follow
[SECURITY.md](SECURITY.md).
