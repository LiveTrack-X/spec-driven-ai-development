from __future__ import annotations

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "README.md",
    "README.ko.md",
    "README.zh.md",
    "README.ja.md",
    "LICENSE",
    "docs/pattern-catalog.md",
    "docs/getting-started.md",
    "docs/mini-sdad.md",
    "docs/maintenance-cost.md",
    "docs/no-clone-quick-install.md",
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
    "templates/project-control-files/save-state.md",
    "templates/mini-sdad/MINI-SDAD.md",
]

REQUIRED_ASSETS = [
    "assets/spec-driven-ai-development-infographic.png",
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
        "Beginner-Friendly Behavior",
        "Do not infer adapter paths",
        "Before fetching",
        "Codex / Claude Code / Cursor / Copilot Chat / Generic",
        "Scale Selection Rule",
        "Override rules beat raw yes-counts",
        "Q5=yes",
        "chat-only environment such as Claude.ai",
        "Claude Code means the local/CLI coding tool",
        "Offer deterministic fallback options",
        "Save-State Update Triggers",
        "Mini Slice Completion",
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
    for path in REQUIRED_ASSETS:
        if not (ROOT / path).is_file():
            fail(f"Missing required asset: {path}")
    readme = read("README.md")
    for phrase in [
        "README.ko.md",
        "README.zh.md",
        "README.ja.md",
        "canonical documentation language",
        "A control layer for AI coding",
        "Status: `1.0.7`",
        "For Beginners: Use In 60 Seconds",
        "assets/spec-driven-ai-development-infographic.png",
        "Choose Scale First",
        "Override rules beat raw yes-counts",
        "Q5=yes -> Standard SDAD minimum",
        "chat-only environment such as Claude.ai",
        "Claude Code means the local/CLI coding tool",
        "Offer deterministic fallback options",
        "For Mini SDAD at loop end",
        "Mini SDAD",
        "Maintenance Cost",
        "Do not claim completion while control files are stale",
        "Mini SDAD also has a completion gate",
        "Update save-state.md when a session pauses or ends",
        "Do not infer adapter paths",
        "Before fetching, state which adapter you are installing and why",
        "If you cannot determine the current tool",
        "first 10 lines",
        "No terminal. No Git. No Python required.",
        "docs/getting-started.md",
        "docs/maintenance-cost.md",
        "docs/no-clone-quick-install.md",
        "The Problem",
        "Why This Is Different",
        "What This Is Not",
    ]:
        if phrase not in readme:
            fail(f"README missing language guidance: {phrase}")
    readme_order = [
        "## For Beginners: Use In 60 Seconds",
        "## Languages",
        "## Choose Scale First",
        "## Maintenance Cost",
    ]
    readme_positions = [readme.find(phrase) for phrase in readme_order]
    if any(position < 0 for position in readme_positions) or readme_positions != sorted(readme_positions):
        fail("README onboarding order must be: beginners, languages, scale, maintenance")
    for phrase in [
        "The first instruction file is tool-specific",
        "Do not create all of them",
        "AI instruction file, choose one",
        "AGENTS.md",
        "CLAUDE.md",
        ".cursor/rules/spec-driven-ai-development.mdc",
        ".github/copilot-instructions.md",
        "AI-SESSION-INSTRUCTIONS.md",
    ]:
        if phrase not in readme:
            fail(f"README project structure missing tool-specific adapter guidance: {phrase}")
    localized = {
        "README.ko.md": [
            "한국어",
            "영어",
            "save-state.md",
            "오너 수락",
            "Q5",
            "chat-only",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/no-clone-quick-install.md",
            "docs/fit-assessment.md",
        ],
        "README.zh.md": [
            "中文",
            "英文",
            "save-state.md",
            "Owner 验收",
            "Q5",
            "chat-only",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/no-clone-quick-install.md",
            "docs/fit-assessment.md",
        ],
        "README.ja.md": [
            "日本語",
            "英語",
            "save-state.md",
            "Owner の受け入れ",
            "Q5",
            "chat-only",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/no-clone-quick-install.md",
            "docs/fit-assessment.md",
        ],
    }
    for path, phrases in localized.items():
        content = read(path)
        for phrase in phrases:
            if phrase not in content:
                fail(f"{path} missing localized guidance: {phrase}")
    agents = read("templates/project-control-files/AGENTS.md")
    for phrase in [
        "Mandatory First Read",
        "Source Of Truth",
        "Handoff Rule",
        "End-Of-Loop Maintenance Rule",
        "Save-State Update Triggers",
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
    for phrase in [
        "Mandatory Start Loop",
        "Version Lane Rules",
        "Review And Verification Rules",
        "End-Of-Loop Maintenance Rule",
        "Control files have maintenance cost",
        "Save-State Update Triggers",
    ]:
        if phrase not in rules:
            fail(f"Repository operating rules template missing: {phrase}")
    save_state = read("templates/project-control-files/save-state.md")
    for phrase in [
        "Update Triggers",
        "session is ending or pausing",
        "owner changes direction",
        "blocked, skipped, partial, degraded, or unverified",
        "expensive to reconstruct",
    ]:
        if phrase not in save_state:
            fail(f"Save-state template missing: {phrase}")
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
    getting_started = read("docs/getting-started.md")
    for phrase in [
        "Get This Repository",
        "Choose Scale First",
        "Override rules beat raw yes-counts",
        "Q5=yes",
        "Chat-only tools such as Claude.ai",
        "No-Clone Quick Install",
        "Complete Beginner Path",
        "Choose A Setup Path",
        "Prompt-Only Start",
        "Install A Tool Adapter",
        "Install The Codex Skill",
        "Owner Acceptance Checklist",
        "Maintenance Cost",
        "save-state.md",
        "Mini SDAD, a slice is not done",
    ]:
        if phrase not in getting_started:
            fail(f"Getting started doc missing: {phrase}")
    no_clone = read("docs/no-clone-quick-install.md")
    for phrase in [
        "Step 0: Choose Scale",
        "Maintenance Cost",
        "Override rules beat raw yes-counts",
        "Q5=yes",
        "chat-only environment such as Claude.ai",
        "Claude Code means the local/CLI coding tool",
        "Offer deterministic fallback options",
        "For Mini SDAD at loop end",
        "save-state.md",
        "Mini SDAD still has a completion gate",
        "Before You Start",
        "What Is A Codex Skill?",
        "How To Know It Worked",
        "Exact Adapter Sources",
        "Give This To Your AI Agent",
        "Before fetching",
        "Codex / Claude Code / Cursor / Copilot Chat / Generic",
        "Do not infer adapter",
        "If you cannot fetch the file",
        "One-Paste PowerShell Installer",
        "One-Paste Bash Installer",
        "raw.githubusercontent.com",
        "Do not overwrite existing project files",
    ]:
        if phrase not in no_clone:
            fail(f"No-clone quick install doc missing: {phrase}")
    mini = read("docs/mini-sdad.md")
    for phrase in [
        "Mini SDAD",
        "When To Use Mini SDAD",
        "What Mini SDAD Creates",
        "Mini SDAD Prompt",
        "Mini Slice Completion Criteria",
        "Q5-style risk beats the raw yes-count",
        "Offer deterministic fallback options",
        "Not done when",
        "Before fetching",
        "Escalation Rule",
    ]:
        if phrase not in mini:
            fail(f"Mini SDAD doc missing: {phrase}")
    maintenance = read("docs/maintenance-cost.md")
    for phrase in [
        "Maintenance Cost",
        "End-Of-Loop Rule",
        "Save-State Update Triggers",
        "session is ending or pausing",
        "owner changes direction",
        "context would be expensive to reconstruct",
        "Do not claim completion while control files are stale",
        "Scale Implication",
        "Stale File Warning",
    ]:
        if phrase not in maintenance:
            fail(f"Maintenance cost doc missing: {phrase}")
    mini_template = read("templates/mini-sdad/MINI-SDAD.md")
    for phrase in [
        "This project uses Mini SDAD",
        "Active Scope",
        "Mini Slice Completion",
        "Not done when",
        "Do Not",
        "Handoff",
    ]:
        if phrase not in mini_template:
            fail(f"Mini SDAD template missing: {phrase}")
    anti_patterns = read("docs/anti-patterns.md")
    for phrase in ["AI Confidence As Completion", "Historical SPEC Override", "Owner Rubber Stamp"]:
        if phrase not in anti_patterns:
            fail(f"Anti-patterns doc missing: {phrase}")
    fit = read("docs/fit-assessment.md")
    for phrase in ["Score", "Very high", "Output Template", "Maintenance cost matters"]:
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
    codex = read("adapters/codex/AGENTS.md")
    claude = read("adapters/claude-code/CLAUDE.md")
    cursor = read("adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc")
    copilot = read("adapters/github-copilot/.github/copilot-instructions.md")
    generic = read("adapters/generic/AI-SESSION-INSTRUCTIONS.md")
    for path, content in [
        ("Codex adapter", codex),
        ("Claude adapter", claude),
        ("Cursor adapter", cursor),
        ("Copilot adapter", copilot),
        ("Generic adapter", generic),
    ]:
        for phrase in ["Source Of Truth", "Evidence beats", "owner", "Save-State Update Triggers"]:
            if phrase not in content:
                fail(f"{path} missing expected phrase: {phrase}")


def main() -> None:
    validate_templates()
    validate_skill()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
