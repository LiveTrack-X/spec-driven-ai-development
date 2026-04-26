from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "docs/pattern-catalog.md",
    "docs/anti-patterns.md",
    "docs/fit-assessment.md",
    "docs/diagrams.md",
    "docs/implicit-rules.md",
    "docs/tool-adapters.md",
    "docs/field-notes/documentation-governance-method.md",
    "docs/field-notes/release-governance-method.md",
    "adapters/README.md",
    "adapters/codex/AGENTS.md",
    "adapters/claude-code/CLAUDE.md",
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
    "adapters/github-copilot/.github/copilot-instructions.md",
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
    "prompts/kickoff-prompt.md",
    "prompts/review-prompt.md",
    "prompts/handoff-prompt.md",
    "skills/ai-spec-project-start/SKILL.md",
    "skills/ai-spec-project-start/agents/openai.yaml",
    "skills/ai-spec-project-start/references/field-patterns.md",
    "skills/ai-spec-project-start/references/implicit-rules.md",
    "skills/ai-spec-project-start/references/starter-templates.md",
    "scripts/install-agent-adapter.ps1",
    "scripts/install-agent-adapter.sh",
    "templates/project-control-files/AGENTS.md",
    "templates/project-control-files/docs/INDEX.md",
    "templates/project-control-files/docs/Repository-Operating-Rules.md",
    "templates/project-control-files/docs/TODO-Open-Items.md",
    "templates/project-control-files/SPEC/SPEC-COMPLETE.md",
    "templates/project-control-files/SPEC/adr/ADR-0001-template.md",
    "templates/project-control-files/review-findings.md",
]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def read(path: str) -> str:
    file_path = ROOT / path
    if not file_path.exists():
        fail(f"Missing required file: {path}")
    return file_path.read_text(encoding="utf-8")


def validate_skill() -> None:
    content = read("skills/ai-spec-project-start/SKILL.md")
    if not content.startswith("---\n"):
        fail("Skill must start with YAML frontmatter")
    match = re.match(r"---\n(.*?)\n---\n", content, flags=re.S)
    if not match:
        fail("Skill frontmatter is not closed")
    frontmatter = match.group(1)
    if "name: ai-spec-project-start" not in frontmatter:
        fail("Skill frontmatter must include name: ai-spec-project-start")
    if "description:" not in frontmatter:
        fail("Skill frontmatter must include description")
    body = content[match.end() :]
    for phrase in [
        "Owner-supervised",
        "Source Of Truth",
        "Pain-To-Rule",
        "Evidence Rules",
        "Field-Proven Baselines",
        "Current-over-historical",
        "implicit-rules",
    ]:
        if phrase not in body:
            fail(f"Skill body missing expected phrase: {phrase}")


def validate_templates() -> None:
    for path in REQUIRED_FILES:
        read(path)
    agents = read("templates/project-control-files/AGENTS.md")
    for phrase in [
        "Mandatory First Read",
        "Source Of Truth",
        "Handoff Rule",
        "past-to-present",
        "Implicit Rules Made Explicit",
    ]:
        if phrase not in agents:
            fail(f"AGENTS template missing: {phrase}")
    index = read("templates/project-control-files/docs/INDEX.md")
    for phrase in ["Repository-Operating-Rules", "Minimum Documentation Update Sets"]:
        if phrase not in index:
            fail(f"docs/INDEX template missing: {phrase}")
    rules = read("templates/project-control-files/docs/Repository-Operating-Rules.md")
    for phrase in ["Mandatory Start Loop", "Version Lane Rules", "Review And Verification Rules"]:
        if phrase not in rules:
            fail(f"Repository operating rules template missing: {phrase}")
    catalog = read("docs/pattern-catalog.md")
    for phrase in [
        "Documentation-governance",
        "Release-governance",
        "Owner Progress View",
        "current-over-historical",
    ]:
        if phrase not in catalog:
            fail(f"Pattern catalog missing: {phrase}")
    implicit = read("docs/implicit-rules.md")
    for phrase in [
        "Core 5",
        "Extended 15",
        "Current Beats Historical",
        "Evidence Beats Confidence",
        "Owner Decision Beats AI Momentum",
        "Repeated Pain Becomes A Rule",
    ]:
        if phrase not in implicit:
            fail(f"Implicit rules doc missing: {phrase}")
    anti_patterns = read("docs/anti-patterns.md")
    for phrase in ["AI Confidence As Completion", "Historical SPEC Override", "Owner Rubber Stamp"]:
        if phrase not in anti_patterns:
            fail(f"Anti-patterns doc missing: {phrase}")
    fit = read("docs/fit-assessment.md")
    for phrase in ["Score", "Very high", "Output Template"]:
        if phrase not in fit:
            fail(f"Fit assessment doc missing: {phrase}")
    diagrams = read("docs/diagrams.md")
    for phrase in ["Operating Loop", "Source Of Truth Order", "```mermaid"]:
        if phrase not in diagrams:
            fail(f"Diagrams doc missing: {phrase}")
    adr = read("templates/project-control-files/SPEC/adr/ADR-0001-template.md")
    for phrase in ["Context", "Decision", "Consequences", "Current-Over-Historical Rule"]:
        if phrase not in adr:
            fail(f"ADR template missing: {phrase}")
    adapters = read("docs/tool-adapters.md")
    for phrase in ["Claude Code", "Cursor", "GitHub Copilot", "Generic AI coding tool"]:
        if phrase not in adapters:
            fail(f"Tool adapters doc missing: {phrase}")
    claude = read("adapters/claude-code/CLAUDE.md")
    cursor = read("adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc")
    copilot = read("adapters/github-copilot/.github/copilot-instructions.md")
    for path, content in [
        ("Claude adapter", claude),
        ("Cursor adapter", cursor),
        ("Copilot adapter", copilot),
    ]:
        for phrase in ["Source Of Truth", "Evidence beats", "owner"]:
            if phrase not in content:
                fail(f"{path} missing expected phrase: {phrase}")


def main() -> None:
    validate_templates()
    validate_skill()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
