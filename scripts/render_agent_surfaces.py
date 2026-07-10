from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = "templates/project-control-files/AGENTS.md"
CANONICAL_TITLE = "# Project Agent Control Plane"
CANONICAL_SCOPE = (
    "Scope: Required, always-loaded instructions for AI agents and maintainers"
)

CURSOR_PREFIX = """---
description: Route Cursor through a compact, evidence-based SDAD control plane.
globs:
alwaysApply: true
---

"""

SURFACES = {
    "adapters/codex/AGENTS.md": (
        "# SPEC-Driven AI Development Agent Contract",
        "Scope: Codex project instructions",
        "",
    ),
    "adapters/claude-code/CLAUDE.md": (
        "# SPEC-Driven AI Development",
        "Scope: Claude Code project memory",
        "",
    ),
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc": (
        "# SPEC-Driven AI Development",
        "Scope: Cursor project rule",
        CURSOR_PREFIX,
    ),
    "adapters/github-copilot/.github/copilot-instructions.md": (
        "# SPEC-Driven AI Development",
        "Scope: GitHub Copilot project instructions",
        "",
    ),
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md": (
        "# SPEC-Driven AI Development",
        "Scope: Generic AI coding-agent instructions",
        "",
    ),
}


def _read_canonical(root: Path) -> str:
    path = root / CANONICAL_PATH
    content = path.read_text(encoding="utf-8")
    if content.count(CANONICAL_TITLE) != 1:
        raise ValueError(f"canonical title must appear once in {CANONICAL_PATH}")
    if content.count(CANONICAL_SCOPE) != 1:
        raise ValueError(f"canonical scope must appear once in {CANONICAL_PATH}")
    return content.replace("\r\n", "\n")


def render_surfaces(root: Path) -> dict[str, str]:
    canonical = _read_canonical(root)
    rendered: dict[str, str] = {}
    for relative_path, (title, scope, prefix) in SURFACES.items():
        rendered[relative_path] = prefix + canonical.replace(
            CANONICAL_TITLE,
            title,
            1,
        ).replace(
            CANONICAL_SCOPE,
            scope,
            1,
        )
    return rendered


def collect_surface_drift(root: Path) -> list[str]:
    violations: list[str] = []
    for relative_path, expected in render_surfaces(root).items():
        path = root / relative_path
        if not path.is_file():
            violations.append(f"missing rendered agent surface: {relative_path}")
            continue
        actual = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if actual != expected:
            violations.append(f"rendered agent surface drift: {relative_path}")
    return violations


def write_surfaces(root: Path) -> None:
    for relative_path, content in render_surfaces(root).items():
        path = root / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render self-contained tool adapters from the canonical agent kernel."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--write", action="store_true", help="regenerate committed adapters")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args()

    root = args.root.resolve()
    if args.check:
        violations = collect_surface_drift(root)
        for violation in violations:
            print(f"ERROR: {violation}")
        if violations:
            return 1
        print("Agent surfaces match the canonical runtime kernel.")
        return 0

    write_surfaces(root)
    print(f"Rendered {len(SURFACES)} agent surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
