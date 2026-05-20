from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import unquote


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
    "docs/context-stability.md",
    "docs/no-clone-quick-install.md",
    "docs/anti-patterns.md",
    "docs/fit-assessment.md",
    "docs/diagrams.md",
    "docs/autonomy-levels.md",
    "docs/implementation-discipline.md",
    "docs/implementation-notes.md",
    "docs/operating-intensity.md",
    "docs/session-handoff.md",
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
    "templates/project-control-files/docs/implementation-notes.md",
    "templates/project-control-files/docs/Repository-Operating-Rules.md",
    "templates/project-control-files/docs/sdad/handoffs/YYYY-MM-DD-topic.md",
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


def strip_fenced_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.S)


def is_external_link(target: str) -> bool:
    return target.lower().startswith(("http://", "https://", "mailto:", "tel:"))


def validate_local_markdown_links() -> None:
    link_pattern = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
    for md_path in sorted(ROOT.rglob("*.md")):
        if ".git" in md_path.parts:
            continue
        content = strip_fenced_code(md_path.read_text(encoding="utf-8"))
        for match in link_pattern.finditer(content):
            raw_target = match.group(1).strip()
            if not raw_target or raw_target.startswith("#") or is_external_link(raw_target):
                continue
            if raw_target.startswith("<") and raw_target.endswith(">"):
                raw_target = raw_target[1:-1].strip()
            target = raw_target.split("#", 1)[0].split("?", 1)[0]
            if not target:
                continue
            target = unquote(target)
            resolved = (md_path.parent / target).resolve()
            try:
                display_target = resolved.relative_to(ROOT)
            except ValueError:
                source = md_path.relative_to(ROOT)
                fail(f"Markdown link escapes repository root: {source} -> {raw_target}")
            if not resolved.exists():
                source = md_path.relative_to(ROOT)
                fail(f"Broken local Markdown link: {source} -> {raw_target} ({display_target})")


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
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "bounded reads",
        "50 KB",
        "State SDAD scale and operating intensity",
        "Autonomy",
        "Review-Worthy Development Units",
        "implementation discipline",
        "implementation notes",
        "docs/implementation-notes.md",
        "Mini Unit Completion",
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
        "Status: `1.1.4`",
        "stable documentation/package release",
        "project fit, owner discipline, and evidence quality",
        "For Beginners: Use In 60 Seconds",
        "assets/spec-driven-ai-development-infographic.png",
        "Choose Scale First",
        "Override rules beat raw yes-counts",
        "Q5=yes -> Standard SDAD minimum",
        "chat-only environment such as Claude.ai",
        "Claude Code means the local/CLI coding tool",
        "Offer deterministic fallback options",
        "For Mini SDAD at loop end",
        "Work Packets And Autonomy Levels",
        "Level 2 Work Packet Autonomy",
        "AI-complete / evidence-ready",
        "docs/autonomy-levels.md",
        "docs/implementation-discipline.md",
        "docs/implementation-notes.md",
        "docs/operating-intensity.md",
        "docs/session-handoff.md",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "execution trace",
        "Full SDAD / High",
        "control surfaces reduce controllability",
        "Do not stop for owner approval after every micro-task",
        "Proceed autonomously inside the approved work packet",
        "Mini SDAD",
        "Maintenance Cost",
        "Do not claim completion while control files are stale",
        "Mini SDAD also has a completion gate",
        "spec-unstated implementation",
        "Update save-state.md when a session pauses or ends",
        "bounded reads",
        "50 KB",
        "Do not infer adapter paths",
        "Before fetching, state which adapter you are installing and why",
        "If you cannot determine the current tool",
        "first 10 lines",
        "No terminal. No Git. No Python required.",
        "docs/getting-started.md",
        "docs/maintenance-cost.md",
        "docs/context-stability.md",
        "docs/implementation-notes.md",
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
            "1.1.4",
            "프로젝트 적합도",
            "save-state.md",
            "오너 수락",
            "Q5",
            "Full SDAD / High",
            "고급 확장",
            "chat-only",
            "리뷰 의미가 있는 개발 단위",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/operating-intensity.md",
            "docs/session-handoff.md",
            "docs/implementation-notes.md",
            "docs/no-clone-quick-install.md",
            "docs/fit-assessment.md",
        ],
        "README.zh.md": [
            "中文",
            "英文",
            "1.1.4",
            "project fit",
            "save-state.md",
            "Owner 验收",
            "Q5",
            "Full SDAD / High",
            "advanced extension",
            "chat-only",
            "有评审意义的开发单元",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/operating-intensity.md",
            "docs/session-handoff.md",
            "docs/implementation-notes.md",
            "docs/no-clone-quick-install.md",
            "docs/fit-assessment.md",
        ],
        "README.ja.md": [
            "日本語",
            "英語",
            "1.1.4",
            "project fit",
            "save-state.md",
            "Owner の受け入れ",
            "Q5",
            "Full SDAD / High",
            "advanced extension",
            "chat-only",
            "レビューする意味のある",
            "docs/getting-started.md",
            "docs/mini-sdad.md",
            "docs/maintenance-cost.md",
            "docs/operating-intensity.md",
            "docs/session-handoff.md",
            "docs/implementation-notes.md",
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
        "Context Stability Rule",
        "Context Stability applies before every item",
        "bounded reads",
        "50 KB",
        "Source Of Truth",
        "Review-Worthy Unit Rule",
        "micro-task",
        "Implementation discipline makes autonomy safe",
        "Implementation memory beats hidden rationale",
        "docs/implementation-notes.md",
        "Handoff Rule",
        "End-Of-Loop Maintenance Rule",
        "Save-State Update Triggers",
        "past-to-present",
        "Implicit Rules Made Explicit",
    ]:
        if phrase not in agents:
            fail(f"AGENTS template missing: {phrase}")
    index = read("templates/project-control-files/docs/INDEX.md")
    for phrase in [
        "Repository-Operating-Rules",
        "Minimum Documentation Update Sets",
        "docs/sdad/handoffs",
        "SDAD scale/intensity change",
        "Heavy control-file budget",
        "context-stability change",
        "implementation-notes.md",
        "Advanced extension",
    ]:
        if phrase not in index:
            fail(f"docs/INDEX template missing: {phrase}")
    rules = read("templates/project-control-files/docs/Repository-Operating-Rules.md")
    for phrase in [
        "Mandatory Start Loop",
        "Context Stability applies before every item",
        "Version Lane Rules",
        "Review And Verification Rules",
        "Review-Worthy Unit Rule",
        "Proceed autonomously inside the approved work packet",
        "Implementation discipline makes autonomy safe",
        "Implementation memory beats hidden rationale",
        "implementation notes for spec-unstated decisions",
        "End-Of-Loop Maintenance Rule",
        "Control files have maintenance cost",
        "Save-State Update Triggers",
        "Long AI coding sessions are execution traces",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "reactivation prompt",
        "Operating Intensity Rules",
        "Evidence Surface Creep",
        "Control File Budget",
        "context-stability pass",
        "bounded reads",
        "50 KB",
        "Advanced Extension Fit Gate",
        "evaluation leakage risk",
        "concrete budget",
        "compressed owner review summary",
    ]:
        if phrase not in rules:
            fail(f"Repository operating rules template missing: {phrase}")
    handoff_template = read("templates/project-control-files/docs/sdad/handoffs/YYYY-MM-DD-topic.md")
    for phrase in [
        "SDAD Session Handoff",
        "Session Identity",
        "Operating Mode",
        "Owner Review Compression",
        "Advanced Extension Status",
        "Search evidence",
        "Owner acceptance evidence",
        "Evaluation leakage risk",
        "Concrete budget used",
        "Bounded-read instructions",
        "Implementation Notes",
        "read this current handoff fully",
        "Commands / Tests Run",
        "Reactivation Prompt",
        "read this current handoff fully",
        "Do not assume the previous chat context is available",
    ]:
        if phrase not in handoff_template:
            fail(f"Session handoff template missing: {phrase}")
    save_state = read("templates/project-control-files/save-state.md")
    for phrase in [
        "Update Triggers",
        "Context Stability Rule",
        "50 KB",
        "session is ending or pausing",
        "owner changes direction",
        "blocked, skipped, partial, degraded, or unverified",
        "expensive to reconstruct",
        "Implementation Notes",
        "docs/implementation-notes.md",
    ]:
        if phrase not in save_state:
            fail(f"Save-state template missing: {phrase}")
    implementation_notes_template = read("templates/project-control-files/docs/implementation-notes.md")
    for phrase in [
        "Implementation Notes",
        "spec-unstated implementation decisions",
        "raw internal reasoning",
        "docs/TODO-Open-Items.md",
        "review-findings.md",
        "ADR",
    ]:
        if phrase not in implementation_notes_template:
            fail(f"Implementation-notes template missing: {phrase}")
    catalog = read("docs/pattern-catalog.md")
    for phrase in [
        "Documentation-governance",
        "Release-governance",
        "Owner Progress View",
        "current-over-historical",
        "implementation notes",
    ]:
        if phrase not in catalog:
            fail(f"Pattern catalog missing: {phrase}")
    implicit = read("docs/implicit-rules.md")
    for phrase in [
        "Core 5",
        "Extended Rules",
        "Current Beats Historical",
        "Evidence Beats Confidence",
        "Owner Decision Beats AI Momentum",
        "Repeated Pain Becomes A Rule",
        "Context Budget Beats Full Transcript",
        "Implementation Memory Beats Hidden Rationale",
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
        "Owner Checkpoint Checklist",
        "Maintenance Cost",
        "review-worthy development unit",
        "work packet",
        "autonomy-levels.md",
        "micro-task",
        "save-state.md",
        "session-handoff.md",
        "operating-intensity.md",
        "context-stability.md",
        "implementation-notes.md",
        "Mini SDAD, a unit may be called evidence-ready",
    ]:
        if phrase not in getting_started:
            fail(f"Getting started doc missing: {phrase}")
    no_clone = read("docs/no-clone-quick-install.md")
    for phrase in [
        "Step 0: Choose Scale",
        "Maintenance Cost",
        "Override rules beat raw yes-counts",
        "Step 0.5 - Choose autonomy",
        "Step 0.6 - Choose operating intensity",
        "Level 2 Work Packet Autonomy",
        "Q5=yes",
        "chat-only environment such as Claude.ai",
        "Claude Code means the local/CLI coding tool",
        "Offer deterministic fallback options",
        "For Mini SDAD at loop end",
        "review-worthy development unit",
        "Do not stop for owner approval after every micro-task",
        "evidence-ready",
        "save-state.md",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "docs/implementation-notes.md",
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
        "bounded reads",
    ]:
        if phrase not in no_clone:
            fail(f"No-clone quick install doc missing: {phrase}")
    mini = read("docs/mini-sdad.md")
    for phrase in [
        "Mini SDAD",
        "When To Use Mini SDAD",
        "What Mini SDAD Creates",
        "Mini SDAD Prompt",
        "Mini Review-Worthy Unit",
        "Mini Unit Completion Criteria",
        "Q5-style risk beats the raw yes-count",
        "Offer deterministic fallback options",
        "Not evidence-ready",
        "Level 1 Unit Autonomy",
        "Before fetching",
        "Escalation Rule",
    ]:
        if phrase not in mini:
            fail(f"Mini SDAD doc missing: {phrase}")
    maintenance = read("docs/maintenance-cost.md")
    for phrase in [
        "Maintenance Cost",
        "End-Of-Packet Rule",
        "review-worthy development unit",
        "not after every micro-task",
        "Save-State Update Triggers",
        "Live-State Size Budget",
        "context-stability.md",
        "implementation-notes.md",
        "session-handoff.md",
        "Control File Budget",
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
        "review-worthy unit",
        "Do not stop for owner approval after every micro-task",
        "Mini Unit Completion",
        "Implementation notes",
        "Not evidence-ready",
        "Do Not",
        "Handoff",
    ]:
        if phrase not in mini_template:
            fail(f"Mini SDAD template missing: {phrase}")
    anti_patterns = read("docs/anti-patterns.md")
    for phrase in [
        "AI Confidence As Completion",
        "Historical SPEC Override",
        "Micro-Approval Thrash",
        "Evidence Surface Creep",
        "Live-State Context Bloat",
        "Evaluation Leakage",
        "Budget Fog",
        "Hidden Implementation Memory",
        "Owner Rubber Stamp",
        "Speculative Complexity",
        "Drive-By Refactor",
    ]:
        if phrase not in anti_patterns:
            fail(f"Anti-patterns doc missing: {phrase}")
    fit = read("docs/fit-assessment.md")
    for phrase in [
        "Score",
        "Very high",
        "Output Template",
        "Implementation notes needed",
        "Maintenance cost matters",
        "Advanced Extension Fit Gate",
        "search evidence",
        "owner acceptance evidence",
        "evaluation leakage risk",
        "concrete budget",
        "unknown",
        "blocking",
    ]:
        if phrase not in fit:
            fail(f"Fit assessment doc missing: {phrase}")
    diagrams = read("docs/diagrams.md")
    for phrase in [
        "Operating Loop",
        "Fresh Session Start Guard",
        "Check file size and scope",
        "Bounded read",
        "Source Of Truth Order",
        "Review-worthy development unit",
        "implementation notes",
        "Work packet",
        "Autonomy Boundary",
        "Batch related small tasks",
        "```mermaid",
    ]:
        if phrase not in diagrams:
            fail(f"Diagrams doc missing: {phrase}")
    autonomy = read("docs/autonomy-levels.md")
    for phrase in [
        "Autonomy Levels",
        "Evidence-Ready Is Not Owner-Accepted",
        "Work Packet",
        "Level 2",
        "Stop Conditions",
        "Checkpoint Summary",
        "Owner Review Compression",
    ]:
        if phrase not in autonomy:
            fail(f"Autonomy levels doc missing: {phrase}")
    implementation = read("docs/implementation-discipline.md")
    for phrase in [
        "Implementation Discipline",
        "Surface Assumptions",
        "Prefer The Smallest Working Design",
        "Make Surgical Changes",
        "Make Goals Verifiable",
        "Preserve Implementation Memory",
        "implementation-notes.md",
        "forrestchang/andrej-karpathy-skills",
    ]:
        if phrase not in implementation:
            fail(f"Implementation discipline doc missing: {phrase}")
    implementation_notes = read("docs/implementation-notes.md")
    for phrase in [
        "Implementation Notes",
        "spec-unstated implementation choices",
        "Implementation notes preserve implementation memory",
        "assumptions used to bridge a SPEC gap",
        "alternatives considered and rejected",
        "Do not record",
        "raw internal reasoning",
        "docs/implementation-notes.md",
        "For Mini SDAD",
        "Context Stability",
    ]:
        if phrase not in implementation_notes:
            fail(f"Implementation notes doc missing: {phrase}")
    operating_intensity = read("docs/operating-intensity.md")
    for phrase in [
        "Operating Intensity",
        "Standard SDAD / High",
        "Full SDAD / Low",
        "## High",
        "## Medium",
        "## Low",
        "## Baseline Freeze",
        "Owner Review Compression",
        "implementation notes needed: yes/no",
        "Evidence Surface Rule",
        "Evaluation-Driven Extensions",
        "Advanced Extension Fit Gate",
        "search evidence",
        "owner acceptance",
        "concrete budget",
        "changes behavior, policy, boundary",
        "evidence claim, or risk acceptance",
        "handoff format",
        "docs/implementation-notes.md",
        "control surfaces reduce controllability",
    ]:
        if phrase not in operating_intensity:
            fail(f"Operating intensity doc missing: {phrase}")
    session_handoff = read("docs/session-handoff.md")
    for phrase in [
        "Session Handoff & Context Continuity",
        "Chats are execution traces",
        "Specs are authority",
        "Handoffs are continuity",
        "Bounded Resume Reads",
        "bounded reads",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "Standard Handoff Template",
        "SDAD scale / intensity used",
        "Control-file budget used",
        "Owner Review Compression",
        "Advanced Extension Status",
        "Search evidence",
        "Owner acceptance evidence",
        "Evaluation leakage risk",
        "Concrete budget used",
        "Owner acceptance status",
        "Implementation Notes",
        "docs/implementation-notes.md",
        "Reactivation Prompt",
        "Do not assume the previous chat context is available",
    ]:
        if phrase not in session_handoff:
            fail(f"Session handoff doc missing: {phrase}")
    context_stability = read("docs/context-stability.md")
    for phrase in [
        "Context Stability & Bounded Reads",
        "Bounded Read Rule",
        "Live-State Size Budget",
        "docs/implementation-notes.md",
        "Generated files, logs, local databases, private corpora",
        "Soft Size Triggers",
        "Tool Input Hygiene",
        ">50 KB",
        ">1 MB",
        "Do not treat a mandatory start loop as permission",
        "This rule does not add cleanup automation",
    ]:
        if phrase not in context_stability:
            fail(f"Context stability doc missing: {phrase}")
    kickoff = read("prompts/kickoff-prompt.md")
    for phrase in [
        "review-worthy development unit",
        "related small tasks",
        "Continue autonomously inside the approved work packet",
        "simplest working design",
        "implementation notes",
        "micro-approval steps",
    ]:
        if phrase not in kickoff:
            fail(f"Kickoff prompt missing review-worthy unit guidance: {phrase}")
    review_prompt = read("prompts/review-prompt.md")
    for phrase in [
        "Context Stability applies before review inputs",
        "bounded reads above 50 KB",
        "context-stability check above 200 KB",
        "no full startup read above 1 MB",
        "implementation-notes.md",
    ]:
        if phrase not in review_prompt:
            fail(f"Review prompt missing context-stability guidance: {phrase}")
    handoff = read("prompts/handoff-prompt.md")
    for phrase in [
        "evidence-ready units",
        "Do not request owner approval after every micro-task",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "reactivation prompt",
        "SDAD scale / intensity used",
        "compressed owner review summary",
        "advanced extension fit-gate status",
        "implementation notes for spec-unstated",
        "search evidence versus owner acceptance evidence",
        "evaluation leakage risk",
        "concrete budget",
        "bounded-read instructions",
        "docs/implementation-notes.md",
        "50 KB",
    ]:
        if phrase not in handoff:
            fail(f"Handoff prompt missing review-worthy unit guidance: {phrase}")
    adr = read("templates/project-control-files/SPEC/adr/ADR-0001-template.md")
    for phrase in ["Context", "Decision", "Consequences", "Current-Over-Historical Rule"]:
        if phrase not in adr:
            fail(f"ADR template missing: {phrase}")
    adapters = read("docs/tool-adapters.md")
    for phrase in [
        "Claude Code",
        "Cursor",
        "GitHub Copilot",
        "Generic AI coding tool",
        "context-stability",
        "implementation-notes",
        "bounded-read guard",
    ]:
        if phrase not in adapters:
            fail(f"Tool adapters doc missing: {phrase}")
    doc_governance = read("docs/field-notes/documentation-governance-method.md")
    for phrase in [
        "Reusable context-stability rule",
        "start loop is a routing requirement",
        "50 KB or 500 lines",
        "The first-read chain must apply context-stability",
        "docs/implementation-notes.md",
    ]:
        if phrase not in doc_governance:
            fail(f"Documentation governance field note missing: {phrase}")
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
        for phrase in [
            "Source Of Truth",
            "Evidence beats",
            "owner",
            "Save-State Update Triggers",
            "review-worthy",
            "Continue autonomously inside the approved work packet",
            "Implementation discipline guards autonomy",
            "Implementation notes preserve implementation memory",
            "docs/implementation-notes.md",
            "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
            "Full SDAD / High",
            "operating intensity",
            "Context Stability applies before every item",
            "bounded reads",
            "50 KB",
        ]:
            if phrase not in content:
                fail(f"{path} missing expected phrase: {phrase}")


def main() -> None:
    validate_local_markdown_links()
    validate_templates()
    validate_skill()
    print("Repository validation passed.")


if __name__ == "__main__":
    main()
