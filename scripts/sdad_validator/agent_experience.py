from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__:
    from .state_contract import collect_template_state_violations
else:
    validator_root = str(Path(__file__).resolve().parents[1])
    if validator_root not in sys.path:
        sys.path.insert(0, validator_root)
    from sdad_validator.state_contract import collect_template_state_violations


SURFACE_BUDGETS = {
    "templates/project-control-files/AGENTS.md": (120, 6_000),
    "templates/project-control-files/docs/INDEX.md": (80, 4_000),
    "templates/project-control-files/sdad-state.yaml": (80, 2_000),
    "adapters/codex/AGENTS.md": (120, 6_000),
    "adapters/claude-code/CLAUDE.md": (120, 6_000),
    "adapters/gemini-cli/GEMINI.md": (120, 6_000),
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc": (120, 6_000),
    "adapters/github-copilot/.github/copilot-instructions.md": (120, 6_000),
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md": (120, 6_000),
}

STARTUP_SURFACES = (
    "templates/project-control-files/AGENTS.md",
    "adapters/codex/AGENTS.md",
    "adapters/claude-code/CLAUDE.md",
    "adapters/gemini-cli/GEMINI.md",
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
    "adapters/github-copilot/.github/copilot-instructions.md",
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
)

ORDERED_STARTUP_ROUTE = (
    "sdad-state.yaml",
    "docs/INDEX.md",
    "current source",
    "tests",
    "routed",
    "on demand",
    "docs/Repository-Operating-Rules.md",
)

INDEX_ROUTES = (
    "sdad-state.yaml",
    "SPEC/SPEC-COMPLETE.md",
    "TODO-Open-Items.md",
    "review-findings.md",
    "implementation-notes.md",
    "save-state.md",
    "sdad/playbooks/context-and-data.md",
    "sdad/playbooks/work-packets.md",
    "sdad/playbooks/evidence-and-risk-gates.md",
    "sdad/playbooks/documentation-and-handoff.md",
    "sdad/playbooks/advanced-extensions.md",
)


def _read(root: Path, relative_path: str, violations: list[str]) -> str:
    path = root / relative_path
    if not path.is_file():
        violations.append(f"missing agent-experience surface: {relative_path}")
        return ""
    return path.read_text(encoding="utf-8")


def _line_count(text: str) -> int:
    return len(text.splitlines())


def _require_ordered_tokens(
    relative_path: str,
    text: str,
    tokens: tuple[str, ...],
    violations: list[str],
) -> None:
    previous = -1
    for token in tokens:
        position = text.find(token, previous + 1)
        if position < 0:
            violations.append(f"{relative_path} missing ordered route: {token}")
            return
        previous = position


def collect_agent_experience_violations(root: Path) -> list[str]:
    """Return stable, actionable violations without printing or exiting."""

    violations: list[str] = []
    content: dict[str, str] = {}

    for relative_path, (line_budget, character_budget) in SURFACE_BUDGETS.items():
        text = _read(root, relative_path, violations)
        content[relative_path] = text
        lines = _line_count(text)
        if text and lines > line_budget:
            violations.append(
                f"{relative_path} exceeds {line_budget} lines: {lines}"
            )
        if text and len(text) > character_budget:
            violations.append(
                f"{relative_path} exceeds {character_budget} characters: {len(text)}"
            )

    fixed_startup = sum(
        len(content.get(path, ""))
        for path in (
            "templates/project-control-files/AGENTS.md",
            "templates/project-control-files/docs/INDEX.md",
            "templates/project-control-files/sdad-state.yaml",
        )
    )
    if fixed_startup > 12_000:
        violations.append(
            f"fixed startup control plane exceeds 12000 characters: {fixed_startup}"
        )

    state = content.get("templates/project-control-files/sdad-state.yaml", "")
    violations.extend(collect_template_state_violations(state))

    _read(
        root,
        "templates/project-control-files/docs/Repository-Operating-Rules.md",
        violations,
    )
    for relative_path in STARTUP_SURFACES:
        text = content.get(relative_path, "")
        if text:
            _require_ordered_tokens(
                relative_path,
                text,
                ORDERED_STARTUP_ROUTE,
                violations,
            )

    index_path = "templates/project-control-files/docs/INDEX.md"
    index = content.get(index_path, "")
    for route in INDEX_ROUTES:
        if index and route not in index:
            violations.append(f"{index_path} missing route: {route}")

    readme = _read(root, "README.md", violations)
    if readme:
        headings = re.findall(r"^## Start Here(?:\:.*)?$", readme, re.MULTILINE)
        if headings != ["## Start Here"]:
            violations.append(
                f"README must have one canonical '## Start Here' heading: {headings}"
            )
        prompt_section_match = re.search(
            r"^## Copy-Paste Start Prompt\s+(.*?)(?=^## |\Z)",
            readme,
            re.MULTILINE | re.DOTALL,
        )
        if prompt_section_match and re.search(
            r"<\s*(?:details|summary)\b",
            prompt_section_match.group(1),
            re.IGNORECASE,
        ):
            violations.append("README copy-paste start prompt must remain expanded")
        prompt_match = re.search(
            r"^## Copy-Paste Start Prompt\s+.*?^```(?:text)?\s*\n(.*?)^```",
            readme,
            re.MULTILINE | re.DOTALL,
        )
        if prompt_match is None:
            violations.append("README copy-paste start prompt is missing")
        for route in ("docs/user-guide.md", "docs/getting-started.md"):
            if route not in readme:
                violations.append(f"README Start Here missing route: {route}")

    return violations
