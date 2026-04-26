from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "docs/pattern-catalog.md",
    "docs/field-notes/cmp-development-method.md",
    "docs/field-notes/directpipe-development-method.md",
    "prompts/kickoff-prompt.md",
    "prompts/review-prompt.md",
    "prompts/handoff-prompt.md",
    "skills/ai-spec-project-start/SKILL.md",
    "skills/ai-spec-project-start/agents/openai.yaml",
    "skills/ai-spec-project-start/references/field-patterns.md",
    "skills/ai-spec-project-start/references/starter-templates.md",
    "templates/project-control-files/AGENTS.md",
    "templates/project-control-files/docs/INDEX.md",
    "templates/project-control-files/docs/Repository-Operating-Rules.md",
    "templates/project-control-files/docs/TODO-Open-Items.md",
    "templates/project-control-files/SPEC/SPEC-COMPLETE.md",
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
    ]:
        if phrase not in body:
            fail(f"Skill body missing expected phrase: {phrase}")


def validate_templates() -> None:
    for path in REQUIRED_FILES:
        read(path)
    agents = read("templates/project-control-files/AGENTS.md")
    for phrase in ["Mandatory First Read", "Source Of Truth", "Handoff Rule", "past-to-present"]:
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
    for phrase in ["CMP", "DirectPipe", "Owner Progress View", "current-over-historical"]:
        if phrase not in catalog:
            fail(f"Pattern catalog missing: {phrase}")


def main() -> None:
    validate_templates()
    validate_skill()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
