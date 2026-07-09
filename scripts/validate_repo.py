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
    "CHANGELOG.md",
    "LICENSE",
    "docs/pattern-catalog.md",
    "docs/user-guide.md",
    "docs/user-guide.ko.md",
    "docs/user-guide.zh.md",
    "docs/user-guide.ja.md",
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
    "docs/product-evidence-templates.md",
    "docs/operating-intensity.md",
    "docs/session-handoff.md",
    "docs/implicit-rules.md",
    "docs/tool-adapters.md",
    "docs/field-notes/repository-control-surface-method.md",
    "docs/field-notes/cost-aware-agent-routing-method.md",
    "docs/field-notes/documentation-governance-method.md",
    "docs/field-notes/working-order-field-test.md",
    "docs/field-notes/release-governance-method.md",
    "docs/field-notes/meta-harness-method.md",
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
    "templates/project-control-files/README.md",
    "templates/project-control-files/docs/INDEX.md",
    "templates/project-control-files/docs/implementation-notes.md",
    "templates/project-control-files/docs/evidence-matrix.md",
    "templates/project-control-files/docs/claim-registry.md",
    "templates/project-control-files/docs/artifact-contracts.md",
    "templates/project-control-files/docs/work-packet-state.md",
    "templates/project-control-files/docs/remote-evidence-import.md",
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
    "assets/sdad-control-loop.archify.html",
    "assets/sdad-control-loop.archify.png",
    "assets/sdad-control-loop.archify.workflow.json",
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
        "Natural-Language Intent Routing",
        "ordinary phrases into",
        "review/audit intent",
        "reference-intake intent",
        "Review-Worthy Development Units",
        "Slice-First Evidence Loop",
        "strongest practical failing test or check",
        "Match evidence tiers to claims",
        "Small Project Compression Rule",
        "Choose scale, compression, autonomy, and operating intensity",
        "Route current state through",
        "PLAN narrows owner intent",
        "TODO/work packet",
        "JIT clarification",
        "Decision Routing Quick Check",
        "Use only the gates that apply",
        "working router for active docs",
        "YYYY-MM-DD-HHMM-start-topic.md",
        "output contract",
        "Repository Control Surface",
        "always-loaded guidance",
        "enforced guarantee",
        "Cost-aware agent routing",
        "advisor checkpoint",
        "bounded loop",
        "implementation discipline",
        "implementation notes",
        "clarification checkpoint",
        "docs/implementation-notes.md",
        "Mini Unit Completion",
        "Source Of Truth",
        "Read order is routing, not authority",
        "Owner decisions control scope",
        "decision for continuity",
        "weak evidence into stronger evidence",
        "Documentation Record Audit",
        "minimum update-set row",
        "Pain-To-Rule",
        "Evidence Rules",
        "product evidence flag",
        "docs/evidence-matrix.md",
        "owner acceptance separate",
        "Field-Proven Baselines",
        "Current-over-historical",
        "implicit-rules",
    ]:
        if phrase not in body:
            fail(f"Skill body missing expected phrase: {phrase}")
    starter_templates = read("skills/ai-spec-project-start/references/starter-templates.md")
    for phrase in [
        "When sources conflict, prefer:",
        "Product notes and external references",
        "Read order is routing, not authority",
        "Owner decisions control scope",
        "decision for continuity",
        "weak evidence into",
    ]:
        if phrase not in starter_templates:
            fail(f"Skill starter templates missing expected phrase: {phrase}")


def validate_templates() -> None:
    for path in REQUIRED_FILES:
        read(path)
    for path in REQUIRED_ASSETS:
        if not (ROOT / path).is_file():
            fail(f"Missing required asset: {path}")
    readme = read("README.md")
    changelog = read("CHANGELOG.md")
    for phrase in [
        "## Unreleased",
        "## 1.3.0 - 2026-07-06",
        "Meta-Harness field note",
        "advanced-extension fit gate",
        "Slice-First Evidence Loop",
        "failing test/check first",
        "owner acceptance",
        "GitHub funding/Sponsors",
        "Cost-Aware Agent Routing field note",
        "create-on-demand wording",
        "loop-end smoke guidance",
        "evidence-tier claim boundaries",
        "Small Project Compression",
    ]:
        if phrase not in changelog:
            fail(f"CHANGELOG missing expected note: {phrase}")
    for phrase in [
        "README.ko.md",
        "README.zh.md",
        "README.ja.md",
        "canonical documentation language",
        "A control layer for AI coding",
        "Status: `1.3.0`",
        "stable documentation/package release",
        "project fit, owner discipline, and evidence quality",
        "Start Here: User Guide",
        "If you are not sure what to do",
        "what to do when AI asks for approval too often",
        "docs/user-guide.ko.md",
        "docs/user-guide.zh.md",
        "docs/user-guide.ja.md",
        "What SDAD Gives You",
        "How SDAD Organizes Context",
        "Always-loaded instructions",
        "active control files",
        "On-demand references",
        "Natural-Language Intent Routing",
        "route natural-language requests",
        "Reference-intake intent",
        "Reference Parity Review",
        "source behavior -> implemented behavior -> evidence",
        "Evidence Tiers And Claims",
        "local test",
        "browser render",
        "remote hardware",
        "production evidence",
        "Use It When",
        "AI asks approval after every micro-task, or runs ahead too much",
        "Copy-Paste Start Prompt",
        "The block below is an execution prompt",
        "assets/spec-driven-ai-development-infographic.png",
        "docs/user-guide.md",
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
        "docs/product-evidence-templates.md",
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
        "Route current state -> Scale/compress -> PLAN",
        "optional ADR -> TODO/work packet -> JIT clarification",
        "installable router template lives at",
        "documentation routine order",
        "documentation record audit",
        "Do not claim completion while control files are stale",
        "Mini SDAD also has a completion gate",
        "Small Project Compression Rule",
        "one evidence-ready summary is enough",
        "spec-unstated implementation",
        "clarification checkpoint",
        "Use ADRs sparingly",
        "Update save-state.md when a session pauses or ends",
        "bounded reads",
        "50 KB",
        "Do not infer adapter paths",
        "Before fetching, state which adapter you are installing and why",
        "If you cannot determine the current tool",
        "first 10 lines",
        "No terminal. No Git. No Python required.",
        "docs/getting-started.md",
        "docs/user-guide.md",
        "docs/maintenance-cost.md",
        "docs/context-stability.md",
        "docs/implementation-notes.md",
        "docs/domain-language.md",
        "docs/field-notes/meta-harness-method.md",
        "docs/field-notes/repository-control-surface-method.md",
        "docs/field-notes/cost-aware-agent-routing-method.md",
        "guidance from guarantees",
        "Cost-Aware Agent Routing",
        "Advisor approval, worker completion, and a passing loop evaluator",
        "Scale/compress -> Active SPEC slice",
        "ADRs are conditional",
        "working router for active docs",
        "docs/no-clone-quick-install.md",
        "The Problem",
        "Why This Is Different",
        "What This Is Not",
        "Step 0.1 - Check product evidence flag",
        "product evidence templates",
        "docs/evidence-matrix.md",
    ]:
        if phrase not in readme:
            fail(f"README missing language guidance: {phrase}")
    readme_order = [
        "## Start Here: User Guide",
        "## Copy-Paste Start Prompt",
        "## What SDAD Gives You",
        "## Use It When",
        "## Languages",
        "## Choose Scale First",
        "## Maintenance Cost",
    ]
    readme_positions = [readme.find(phrase) for phrase in readme_order]
    if any(position < 0 for position in readme_positions) or readme_positions != sorted(readme_positions):
        fail("README onboarding order must be: user guide, prompt, explanation, use cases, languages, scale, maintenance")
    user_guide = read("docs/user-guide.md")
    for phrase in [
        "Troubleshooting FAQ",
        "The AI asks for approval too often, or runs ahead too much",
        "Adjust the autonomy level, packet boundary, and operating intensity together",
        "Use autonomy levels as a dial",
        "Level 0 Ask-first",
        "Level 1 Unit Autonomy",
        "Level 2 Work Packet Autonomy",
        "Level 3 Session Autonomy",
        "Level 4 Release-gated Autonomy",
        "Do not use higher autonomy to bypass Level 4 owner gates",
        "The AI says \"done\" but I cannot tell what changed",
        "Ask for evidence-ready status",
        "SDAD feels like too many files",
        "Use a smaller scale or lower intensity",
        "The next session keeps losing context",
        "A chat-only tool says it installed SDAD",
        "Do not solve it by raising autonomy alone",
        "How SDAD Uses Context",
        "Natural-Language Requests",
        "Codex Practice In SDAD",
        "Can I use Codex as a task queue or background worker",
        "Should I ask Codex for several possible solutions",
        "Controlled task queue",
        "multi-candidate review",
        "I do not know the right SDAD command or skill name",
        "Reference-intake intent",
        "Autonomy tuning intent",
        "The task size is unclear",
        "What should the AI check before and after changing files",
        "What evidence is enough when there is no formal test",
        "before/after change guard",
        "practical evidence",
    ]:
        if phrase not in user_guide:
            fail(f"User guide missing troubleshooting FAQ guidance: {phrase}")
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
            "1.3.0",
            "프로젝트 적합도",
            "save-state.md",
            "오너 수락",
            "Q5",
            "Full SDAD / High",
            "고급 확장",
            "chat-only",
            "문제 해결 FAQ",
            "정확한 SDAD 명령어나 skill 이름",
            "interpreted intent",
            "승인 요청",
            "Level 2 Work Packet Autonomy",
            "Level 1 Unit Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "blocking 질문",
            "리뷰 의미가 있는 개발 단위",
            "docs/getting-started.md",
            "docs/user-guide.ko.md",
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
            "1.3.0",
            "project fit",
            "save-state.md",
            "Owner 验收",
            "Q5",
            "Full SDAD / High",
            "advanced extension",
            "chat-only",
            "问题排查 FAQ",
            "正确的 SDAD 命令或 skill 名称",
            "interpreted intent",
            "批准",
            "Level 2 Work Packet Autonomy",
            "Level 1 Unit Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "blocking 问题",
            "有评审意义的开发单元",
            "docs/getting-started.md",
            "docs/user-guide.zh.md",
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
            "1.3.0",
            "project fit",
            "save-state.md",
            "Owner の受け入れ",
            "Q5",
            "Full SDAD / High",
            "advanced extension",
            "chat-only",
            "トラブルシューティング FAQ",
            "正しい SDAD command や skill 名",
            "interpreted intent",
            "承認",
            "Level 2 Work Packet Autonomy",
            "Level 1 Unit Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "blocking question",
            "レビューする意味のある",
            "docs/getting-started.md",
            "docs/user-guide.ja.md",
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
    localized_user_guides = {
        "docs/user-guide.ko.md": [
            "사용자 가이드와 FAQ",
            "영어 기준 문서",
            "빠른 선택",
            "자연어 요청",
            "정확한 SDAD 명령어나 skill 이름",
            "reference-intake intent",
            "autonomy tuning intent",
            "문제 해결 FAQ",
            "Level 0 Ask-first",
            "Level 1 Unit Autonomy",
            "Level 2 Work Packet Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "docs/implementation-notes.md",
            "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        ],
        "docs/user-guide.zh.md": [
            "用户指南和 FAQ",
            "英文规范文档",
            "快速选择",
            "自然语言请求",
            "正确的 SDAD 命令或 skill 名称",
            "reference-intake intent",
            "autonomy tuning intent",
            "问题排查 FAQ",
            "Level 0 Ask-first",
            "Level 1 Unit Autonomy",
            "Level 2 Work Packet Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "docs/implementation-notes.md",
            "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        ],
        "docs/user-guide.ja.md": [
            "ユーザーガイドと FAQ",
            "英語の正本文書",
            "早見表",
            "自然言語リクエスト",
            "正しい SDAD command や skill 名",
            "reference-intake intent",
            "autonomy tuning intent",
            "トラブルシューティング FAQ",
            "Level 0 Ask-first",
            "Level 1 Unit Autonomy",
            "Level 2 Work Packet Autonomy",
            "Level 3 Session Autonomy",
            "Level 4 Release-gated Autonomy",
            "evidence-ready",
            "docs/implementation-notes.md",
            "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        ],
    }
    for path, phrases in localized_user_guides.items():
        content = read(path)
        for phrase in phrases:
            if phrase not in content:
                fail(f"{path} missing localized user-guide guidance: {phrase}")
    agents = read("templates/project-control-files/AGENTS.md")
    for phrase in [
        "Mandatory First Read",
        "Context Stability Rule",
        "Context Stability applies before every item",
        "bounded reads",
        "50 KB",
        "Natural-Language Intent Routing",
        "review/audit intent",
        "reference-intake intent",
        "Source Of Truth",
        "Review-Worthy Unit Rule",
        "micro-task",
        "Implementation discipline makes autonomy safe",
        "Implementation memory beats hidden rationale",
        "clarification checkpoint",
        "Use ADRs sparingly",
        "docs/implementation-notes.md",
        "Handoff Rule",
        "End-Of-Loop Maintenance Rule",
        "unfinished active work packets",
        "generated artifacts or cache files",
        "smoke installed artifacts from outside the source tree",
        "Save-State Update Triggers",
        "past-to-present",
        "Implicit Rules Made Explicit",
        "working router during implementation",
        "Read order is routing, not authority",
        "decision for continuity",
        "weak evidence into stronger evidence",
        "Before implementing from a handoff-only or save-state-only decision",
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
        "domain-language.md",
        "evidence-matrix.md",
        "claim-registry.md",
        "artifact-contracts.md",
        "work-packet-state.md",
        "remote-evidence-import.md",
        "Advanced extension",
        "routes, not mandatory files",
        "Create or copy only the optional evidence files",
        "Working Route",
        "Use this table while working",
        "SDAD Working Order",
        "Decision Routing Quick Check",
        "Handoff-only or save-state-only decisions",
        "Route: read",
        "Scale/compress",
        "PLAN",
        "Optional ADR",
        "TODO/work packet",
        "JIT clarification",
        "cycle result record",
        "Single-File Bloat Risk Routes",
        "When one file starts carrying multiple jobs",
        "docs/archive/todo-history/YYYY-MM-DD-topic.md",
        "docs/review/archive/YYYY-MM-DD-topic.md",
        "YYYY-MM-DD-HHMM-start-topic.md",
        "Start: YYYY-MM-DD HH:MM",
        "blocked_until_evidence",
        "canonical artifact manifest",
        "Auditing documentation record",
        "Documentation Record Audit",
        "minimum update-set row",
        "Source Of Truth Role Map",
        "Routing order is not source-of-truth precedence",
        "Owner decisions control scope",
        "decision for continuity",
        "Before implementing from a handoff-only or save-state-only decision",
    ]:
        if phrase not in index:
            fail(f"docs/INDEX template missing: {phrase}")
    rules = read("templates/project-control-files/docs/Repository-Operating-Rules.md")
    for phrase in [
        "Mandatory Start Loop",
        "Context Stability applies before every item",
        "Natural-Language Intent Routing",
        "review/audit intent",
        "reference-intake intent",
        "Version Lane Rules",
        "Review And Verification Rules",
        "Review-Worthy Unit Rule",
        "Proceed autonomously inside the approved work packet",
        "Implementation discipline makes autonomy safe",
        "Implementation memory beats hidden rationale",
        "clarification checkpoint",
        "hard to reverse",
        "implementation notes for spec-unstated decisions",
        "End-Of-Loop Maintenance Rule",
        "Control files have maintenance cost",
        "Save-State Update Triggers",
        "Long AI coding sessions are execution traces",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "reactivation prompt",
        "Operating Intensity Rules",
        "Evidence Surface Creep",
        "Product And Hardware Evidence Gates",
        "docs/evidence-matrix.md",
        "docs/claim-registry.md",
        "docs/artifact-contracts.md",
        "docs/work-packet-state.md",
        "docs/remote-evidence-import.md",
        "Control File Budget",
        "context-stability pass",
        "bounded reads",
        "50 KB",
        "Advanced Extension Fit Gate",
        "evaluation leakage risk",
        "concrete budget",
        "compressed owner review summary",
        "installed-artifact smoke",
        "unfinished active work packets",
        "generated artifacts or cache files",
        "smoke installed artifacts from outside the source tree",
        "Match evidence tiers to claims",
        "Small Project Compression Rule",
        "Logical flow",
        "Scale/compress -> Active SPEC slice",
        "Read order is routing, not authority",
        "weak evidence into stronger evidence",
        "Documentation Record Audit",
        "minimum update-set row",
        "Before implementing from a handoff-only or save-state-only decision",
    ]:
        if phrase not in rules:
            fail(f"Repository operating rules template missing: {phrase}")
    project_readme = read("templates/project-control-files/README.md")
    for phrase in [
        "Optional product evidence files are create-on-demand",
        "optional evidence file as a setup failure",
        "evidence boundary",
        "Small Project Compression Rule",
        "do not create extra",
    ]:
        if phrase not in project_readme:
            fail(f"Project control README template missing: {phrase}")
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
        "Reference existing SPECs",
        "Documentation Record Audit",
        "Minimum update-set row",
        "Docs checked with no update needed",
        "Validation commands run",
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
        "Save-state-only decisions are continuity hints",
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
        "hard to reverse",
    ]:
        if phrase not in implementation_notes_template:
            fail(f"Implementation-notes template missing: {phrase}")
    evidence_templates = read("docs/product-evidence-templates.md")
    for phrase in [
        "Product Evidence Templates",
        "Evidence Matrix",
        "Claim Registry",
        "Artifact Contract",
        "Work Packet State Model",
        "Remote Evidence Import",
        "hardware",
        "software_verified",
        "tester_ready",
        "hardware_verified",
        "production_ready",
        "quarantine",
        "claim remains blocked",
        "product evidence flag",
        "not a new SDAD scale",
        "Owner acceptance is an acceptance field or ledger",
        "Evidence Tier Claim Boundary",
        "local_test",
        "browser_render",
        "live_runtime",
        "persisted_state",
        "remote_hardware",
        "production_evidence",
        "Claim Gate Smoke",
        "accepted_with_limits",
        "passing local test may coexist",
        "Match the check to the artifact type",
        "output contract",
        "canonical artifact manifest",
    ]:
        if phrase not in evidence_templates:
            fail(f"Product evidence templates doc missing: {phrase}")
    evidence_matrix = read("templates/project-control-files/docs/evidence-matrix.md")
    for phrase in [
        "Evidence Matrix",
        "Status Values",
        "software_only",
        "evidence_received",
        "reviewed_pass",
        "Reproducibility Tiers",
        "Freshness Rules",
        "Negative Results",
        "Evidence status stops at review",
        "Acceptance Tracking",
        "not_requested",
        "pending_owner",
    ]:
        if phrase not in evidence_matrix:
            fail(f"Evidence matrix template missing: {phrase}")
    claim_registry = read("templates/project-control-files/docs/claim-registry.md")
    for phrase in [
        "Claim Registry",
        "allowed_with_qualifier",
        "blocked_until_evidence",
        "P0_forbidden",
        "Claim Scan Checklist",
        "README.md",
        "Stop Rules",
        "Owner Acceptance",
    ]:
        if phrase not in claim_registry:
            fail(f"Claim registry template missing: {phrase}")
    artifact_contracts = read("templates/project-control-files/docs/artifact-contracts.md")
    for phrase in [
        "Artifact Contracts",
        "Artifact States",
        "tester_ready",
        "quarantined",
        "required_metadata",
        "privacy_review",
        "Baseline Gate",
        "Privacy Rules",
        "Canonical Manifest",
        "canonical artifact manifest",
        "source_commit",
    ]:
        if phrase not in artifact_contracts:
            fail(f"Artifact contracts template missing: {phrase}")
    work_packet_state = read("templates/project-control-files/docs/work-packet-state.md")
    for phrase in [
        "Work Packet State Model",
        "Packet States",
        "ai_complete",
        "software_verified",
        "tester_ready",
        "hardware_evidence_received",
        "hardware_verified",
        "owner_accepted",
        "production_ready",
        "Completion Language",
        "Stop / Continue Rule",
        "Packet states are separate from evidence matrix statuses",
    ]:
        if phrase not in work_packet_state:
            fail(f"Work packet state template missing: {phrase}")
    remote_import = read("templates/project-control-files/docs/remote-evidence-import.md")
    for phrase in [
        "Remote Evidence Import / Quarantine Pattern",
        "Standard Flow",
        "quarantine",
        "validated",
        "accepted",
        "Import Checklist",
        "Privacy Scan",
        "Review Summary Template",
        "Sufficiency Rule",
        "Trust Boundary",
    ]:
        if phrase not in remote_import:
            fail(f"Remote evidence import template missing: {phrase}")
    catalog = read("docs/pattern-catalog.md")
    for phrase in [
        "Documentation-governance",
        "Release-governance",
        "Owner Progress View",
        "For Standard and Full SDAD",
        "A single evidence-ready summary",
        "current-over-historical",
        "implementation notes",
        "Pressure-Test Plans Before Building",
        "Keep Domain Language Bounded",
        "bkit-codex",
        "Layer Context By Need",
        "Route Natural-Language Intent",
        "Keep Codex Practice Governed",
        "environment improvement loop",
        "controlled task queue",
        "optional multi-candidate review",
        "Natural-language intent routing",
        "User uses plain language instead of a skill name",
        "Codex task queue accumulates side quests",
        "pre/post change guards",
        "Product evidence templates",
        "Evidence Matrix",
        "Claim Registry",
        "Artifact Contract",
        "Remote Evidence Import",
        "Reference Parity Review Gate",
        "source behavior -> implemented behavior -> evidence",
        "test runtime, live runtime",
        "persisted state as separate evidence tiers",
        "Match Evidence Tiers To Claims",
        "Compress Small Projects Before Adding Files",
        "Small Project Compression Rule",
        "One evidence-ready summary is enough",
        "Scale/compress",
        "Slice-First Evidence Loop",
        "PLAN narrows intent",
        "TODO/work packet turns the",
        "JIT resolves missing slice details",
        "strongest practical failing test or check",
        "Use TDD when behavior can be specified",
        "output contract",
        "not owner-accepted",
        "review-findings.md",
        "Gate Evaluation-Driven Harness Extensions",
        "Layer Repository Control Surfaces",
        "Guidance vs enforcement",
        "research goes to isolated context",
        "guarantees go to enforcement",
        "Read order is routing, not authority",
        "continuity until it is promoted",
        "weak evidence into stronger",
        "Use Cost-Aware Agent Routing",
        "Lean Execution Contract",
        "Executor-Advisor",
        "Orchestrator-Worker",
        "Loop Engineering",
        "Advisor approval is review evidence, not owner acceptance",
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
        "Natural Language Intent Beats Skill Names",
        "State the interpreted intent",
        "Repository Evidence Beats Unnecessary Questions",
        "Stable Terms Beat Session Vocabulary",
        "Guarantees Beat Guidance For Non-Negotiables",
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
        "First choose One-shot, Mini, Standard, or Full SDAD",
        "Install A Tool Adapter",
        "Install The Codex Skill",
        "Owner Checkpoint Checklist",
        "Maintenance Cost",
        "review-worthy development unit",
        "work packet",
        "clarification question",
        "autonomy-levels.md",
        "micro-task",
        "save-state.md",
        "session-handoff.md",
        "operating-intensity.md",
        "context-stability.md",
        "implementation-notes.md",
        "Mini SDAD, a unit may be called evidence-ready",
        "The skill name is optional",
        "routed by intent",
        "product-evidence-templates.md",
        "evidence-matrix.md",
        "claim-registry.md",
        "artifact-contracts.md",
        "work-packet-state.md",
        "remote-evidence-import.md",
        "optional evidence templates are create-on-demand",
        "Small Project Compression Rule",
        "one evidence-ready summary is enough",
        "Evidence tier/gates",
        "Route current state -> Scale/compress -> PLAN",
        "optional ADR -> TODO/work packet -> JIT clarification",
        "ADRs are conditional",
        "Quick Routing Prompt",
        "Use docs/INDEX.md as the working router",
        "that file is a template",
        "Documentation Record Audit",
    ]:
        if phrase not in getting_started:
            fail(f"Getting started doc missing: {phrase}")
    no_clone = read("docs/no-clone-quick-install.md")
    for phrase in [
        "Step 0: Choose Scale",
        "Step 0.1 - Check product evidence flag",
        "product evidence flag",
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
        "clarification checkpoint",
        "Use ADRs sparingly",
        "evidence-ready",
        "save-state.md",
        "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        "docs/implementation-notes.md",
        "Mini SDAD still has a completion gate",
        "Route natural-language requests",
        "reference-intake intent",
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
        "docs/evidence-matrix.md",
        "docs/claim-registry.md",
        "docs/artifact-contracts.md",
        "docs/work-packet-state.md",
        "docs/remote-evidence-import.md",
        "These optional evidence files are create-on-demand",
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
        "Natural-Language Requests In Mini",
        "without knowing a skill name",
        "next blocking clarification question",
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
        "hard to reverse",
        "session-handoff.md",
        "Control File Budget",
        "Small Project Compression Rule",
        "one evidence-ready summary",
        "Evidence Matrix / Claim Registry / Artifact Contract",
        "YYYY-MM-DD-HHMM-start-topic.md",
        "Start: YYYY-MM-DD HH:MM",
        "Common single-file bloat risks",
        "Single-File Bloat Risk Routes",
        "Documentation Routine Order",
        "Documentation Record Audit",
        "minimum update-set row",
        "docs checked with no update needed",
        "session is ending or pausing",
        "owner changes direction",
        "context would be expensive to reconstruct",
        "Do not claim completion while control files are stale",
        "Minimum loop-end smoke",
        "no active numbered work packet remains unchecked",
        "generated artifacts, caches, logs",
        "smoke the installed artifact from outside the source tree",
        "Scale Implication",
        "Stale File Warning",
    ]:
        if phrase not in maintenance:
            fail(f"Maintenance cost doc missing: {phrase}")
    mini_template = read("templates/mini-sdad/MINI-SDAD.md")
    for phrase in [
        "This project uses Mini SDAD",
        "Natural-Language Intent Routing",
        "review/audit intent",
        "Active Scope",
        "review-worthy unit",
        "Do not stop for owner approval after every micro-task",
        "Mini Unit Completion",
        "Implementation notes",
        "fuzzy scope was resolved",
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
        "Trigger Word Dependency",
        "Hidden Codex Queue",
        "controlled task queues",
        "natural-language intent routing",
        "Evidence Surface Creep",
        "Live-State Context Bloat",
        "Evaluation Leakage",
        "Budget Fog",
        "Hidden Implementation Memory",
        "Question-First Without Repository Evidence",
        "Glossary Sprawl",
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
        "harness interface",
        "baseline harness",
        "offline traces",
        "online candidate traces",
        "search evidence",
        "owner acceptance evidence",
        "evaluation leakage risk",
        "concrete budget",
        "Cost-aware agent routing",
        "advisor checkpoints",
        "bounded loops",
        "searches over routing policies",
        "field-notes/cost-aware-agent-routing-method.md",
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
        "Rendered Diagram Assets",
        "Document Relationship Map",
        "Timestamped Log Split",
        "Owner decisions",
        "Owner acceptance does not upgrade",
        "assets/sdad-control-loop.archify.png",
        "assets/sdad-control-loop.archify.html",
        "assets/sdad-control-loop.archify.workflow.json",
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
        "Clarification Checkpoints",
        "Checkpoint Summary",
        "Owner Review Compression",
    ]:
        if phrase not in autonomy:
            fail(f"Autonomy levels doc missing: {phrase}")
    implementation = read("docs/implementation-discipline.md")
    for phrase in [
        "Implementation Discipline",
        "Surface Assumptions",
        "Run A Clarification Checkpoint",
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
        "Clarification checkpoint adoption",
        "bkit-codex pattern intake",
        "natural-language intent routing",
        "Natural-Language Intent Routing",
        "OpenAI Codex practice intake",
        "issue-shaped",
        "environment improvement loops",
        "controlled task queues",
        "multi-candidate review",
        "skill name",
        "layered context",
        "before/after change guards",
        "hard to reverse",
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
        "clarification checkpoint needed/resolved",
        "Evidence Surface Rule",
        "Evaluation-Driven Extensions",
        "Advanced Extension Fit Gate",
        "harness interface",
        "baseline harness",
        "offline traces",
        "online candidate traces",
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
        "Reference, Do Not Duplicate",
        "Handoff-only decisions are continuity hints",
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
        "documentation record audit",
        "minimum update-set row",
        "docs checked with no update needed",
        "validation commands",
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
        "Common split routes",
        "docs/archive/evidence/YYYY-MM-DD-HHMM-start-topic.md",
        "This rule does not add cleanup automation",
    ]:
        if phrase not in context_stability:
            fail(f"Context stability doc missing: {phrase}")
    kickoff = read("prompts/kickoff-prompt.md")
    for phrase in [
        "Natural-Language Intent Routing",
        "review intent",
        "reference-intake intent",
        "review-worthy development unit",
        "related small tasks",
        "Continue autonomously inside the approved work packet",
        "simplest working design",
        "clarification checkpoint",
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
        "clarification",
        "save-state-only decisions",
        "missing documentation record audit",
        "minimum update-set row",
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
        "clarification checkpoints resolved",
        "implementation notes for spec-unstated",
        "search evidence versus owner acceptance evidence",
        "evaluation leakage risk",
        "concrete budget",
        "bounded-read instructions",
        "documentation record audit",
        "minimum update-set row",
        "docs checked with no update needed",
        "validation commands run",
        "Handoff-only or save-state-only decisions",
        "docs/implementation-notes.md",
        "50 KB",
    ]:
        if phrase not in handoff:
            fail(f"Handoff prompt missing review-worthy unit guidance: {phrase}")
    adr = read("templates/project-control-files/SPEC/adr/ADR-0001-template.md")
    for phrase in ["Context", "Decision", "Consequences", "Current-Over-Historical Rule", "hard to reverse"]:
        if phrase not in adr:
            fail(f"ADR template missing: {phrase}")
    adapters = read("docs/tool-adapters.md")
    for phrase in [
        "Claude Code",
        "Cursor",
        "GitHub Copilot",
        "Generic AI coding tool",
        "context-stability",
        "natural-language intent routing",
        "without knowing skill names",
        "implementation-notes",
        "bounded-read guard",
        "guidance, not enforcement",
        "enforced surface",
    ]:
        if phrase not in adapters:
            fail(f"Tool adapters doc missing: {phrase}")
    control_surface = read("docs/field-notes/repository-control-surface-method.md")
    for phrase in [
        "Repository Control Surface Method",
        "Control Surface Ladder",
        "Always-loaded guidance",
        "Routed guidance",
        "On-demand procedure",
        "Isolated exploration",
        "Enforced guarantee",
        "Reviewed memory",
        "Guidance vs Enforcement",
        "Routing Rule",
        "Minimal Layout",
        "Bloat Controls",
        "Evidence Boundary",
        "Adoption Checklist",
        "CI, tests, validators, hooks, permissions",
        "implementation notes, ADRs, operating rules, handoffs",
    ]:
        if phrase not in control_surface:
            fail(f"Repository control surface field note missing: {phrase}")
    cost_routing = read("docs/field-notes/cost-aware-agent-routing-method.md")
    for phrase in [
        "Cost-Aware Agent Routing Method",
        "Lean Execution Contract",
        "Executor-Advisor",
        "Orchestrator-Worker",
        "Loop Engineering",
        "Routing Gate",
        "Evidence Boundary",
        "Stop Rules",
        "Default executor",
        "Escalation trigger",
        "Worker boundary",
        "Loop trigger",
        "Evidence contract",
        "Owner gate",
        "Advisor approval is review evidence, not owner acceptance",
        "Worker completion is candidate evidence",
        "Benchmark ratios from external sources are reference material",
        "Do not ask an agent to reproduce hidden reasoning",
    ]:
        if phrase not in cost_routing:
            fail(f"Cost-aware agent routing field note missing: {phrase}")
    doc_governance = read("docs/field-notes/documentation-governance-method.md")
    for phrase in [
        "Reusable context-stability rule",
        "start loop is a routing requirement",
        "50 KB or 500 lines",
        "The first-read chain must apply context-stability",
        "docs/implementation-notes.md",
        "chat memory or AI confidence",
        "Read order is routing, not authority",
        "Owner decisions control scope",
        "Owner acceptance does not upgrade weak evidence",
    ]:
        if phrase not in doc_governance:
            fail(f"Documentation governance field note missing: {phrase}")
    working_order = read("docs/field-notes/working-order-field-test.md")
    for phrase in [
        "Working Order Field Test",
        "Multi-agent disposable-project test",
        "Route current state -> Scale/compress -> PLAN",
        "Mini CLI",
        "Reference parity",
        "Claim/evidence package",
        "Handoff/bloat loop",
        "cycle result record",
        "problem",
        "cause",
        "action taken",
        "evidence command or artifact",
        "residual concern",
        "artifact type",
        "Passing Tests Can Coexist With A Blocked Claim",
        "checkpoint_included",
        "PowerShell-safe commands",
        "Evidence Boundary",
    ]:
        if phrase not in working_order:
            fail(f"Working order field note missing: {phrase}")
    meta_harness = read("docs/field-notes/meta-harness-method.md")
    for phrase in [
        "Meta-Harness Method",
        "SDAD Translation",
        "Harness interface",
        "search set",
        "held-out set",
        "Baselines",
        "Offline experience",
        "Online experience",
        "Eleven Harness Surfaces",
        "Evidence Boundary",
        "owner-accepted",
        "concrete budget",
        "Stop Rules",
    ]:
        if phrase not in meta_harness:
            fail(f"Meta-Harness field note missing: {phrase}")
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
            "clarification checkpoint",
            "Use ADRs sparingly",
            "docs/implementation-notes.md",
            "docs/sdad/handoffs/YYYY-MM-DD-topic.md",
            "Full SDAD / High",
            "operating intensity",
            "Context Stability applies before every item",
            "bounded reads",
            "50 KB",
            "Natural-Language Intent Routing",
            "review/audit intent",
            "reference-intake intent",
            "product evidence templates",
            "docs/evidence-matrix.md",
            "owner acceptance separate",
            "Read order is routing, not authority",
            "current handoff only for continuity",
            "Before implementing from a handoff-only or save-state-only decision",
            "does not upgrade weak evidence",
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
