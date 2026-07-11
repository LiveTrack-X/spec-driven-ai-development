from __future__ import annotations

import re
import sys
from pathlib import Path

if __package__:
    from .checks.review_state import _V2_REVIEW_OPEN_RECORD, _V2_TODO_OPEN_RECORD
    from .state_contract import collect_template_state_violations, inspect_state
else:
    validator_root = str(Path(__file__).resolve().parents[1])
    if validator_root not in sys.path:
        sys.path.insert(0, validator_root)
    from sdad_validator.checks.review_state import (
        _V2_REVIEW_OPEN_RECORD,
        _V2_TODO_OPEN_RECORD,
    )
    from sdad_validator.state_contract import (
        collect_template_state_violations,
        inspect_state,
    )


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

TARGETED_ROUTE_CONTRACT = (
    "current intent",
    "routed path, heading, active section, or targeted match",
    "does not mean read the whole file",
)

FORBIDDEN_KERNEL_WORDING = (
    "@sdad-state.yaml",
    "@docs/INDEX.md",
    "@README.md",
    "Q5",
    "operating intensity",
    "autonomy",
    "recovery mode",
    "owner checkpoint",
    "AI-complete",
    "save-state.md",
)

INDEX_ROUTES = (
    "sdad-state.yaml",
    "SPEC/SPEC-COMPLETE.md",
    "TODO-Open-Items.md",
    "review-findings.md",
    "implementation-notes.md",
    "sdad/playbooks/context-and-data.md",
    "sdad/playbooks/work-packets.md",
    "sdad/playbooks/evidence-and-risk-gates.md",
    "sdad/playbooks/documentation-and-handoff.md",
    "sdad/playbooks/advanced-extensions.md",
)

CURRENT_HANDOFF_SOURCE = (
    "- Current handoff: use "
    "`../sdad-state.yaml#current_handoff` when declared."
)

TASK8_REQUIRED_PHRASES = {
    "templates/project-control-files/docs/TODO-Open-Items.md": (
        "## Active Work",
        "- [ ] [packet:bootstrap]",
        "## Release / Production Readiness",
        "## Recently Closed",
    ),
    "templates/project-control-files/review-findings.md": (
        "## Active Findings",
        "None currently tracked.",
        "## Recently Closed",
    ),
}

_MARKDOWN_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")


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


def _require_phrases(
    relative_path: str,
    text: str,
    phrases: tuple[str, ...],
    violations: list[str],
) -> None:
    for phrase in phrases:
        if phrase not in text:
            violations.append(f"{relative_path} missing canonical phrase: {phrase}")


def _validate_startup_kernel(
    relative_path: str,
    text: str,
    violations: list[str],
) -> None:
    positions = [text.find(token) for token in TARGETED_ROUTE_CONTRACT]
    if any(position < 0 for position in positions) or positions != sorted(positions):
        violations.append(
            f"{relative_path} must route current intent to one targeted path, "
            "heading, active section, or match; routed membership cannot require "
            "a full-file read"
        )

    lowered = text.lower()
    for phrase in FORBIDDEN_KERNEL_WORDING:
        if phrase.lower() in lowered:
            violations.append(
                f"{relative_path} contains forbidden always-loaded kernel "
                f"wording: {phrase}"
            )


def _visible_markdown_lines(text: str) -> list[str]:
    text = re.sub(
        r"<!--.*?-->",
        lambda match: "\n" * match.group(0).count("\n"),
        text,
        flags=re.DOTALL,
    )
    visible: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in text.splitlines():
        fence = _MARKDOWN_FENCE.match(line)
        if fence_character is None:
            if fence is not None:
                delimiter, info = fence.groups()
                if delimiter[0] != "`" or "`" not in info:
                    fence_character = delimiter[0]
                    fence_length = len(delimiter)
                    continue
            visible.append(line)
            continue
        if fence is not None:
            delimiter, trailing = fence.groups()
            if (
                delimiter[0] == fence_character
                and len(delimiter) >= fence_length
                and not trailing.strip()
            ):
                fence_character = None
                fence_length = 0
    return visible


def _first_visible_section(text: str, heading: str) -> list[str] | None:
    lines = _visible_markdown_lines(text)
    try:
        start = lines.index(heading) + 1
    except ValueError:
        return None
    end = next(
        (index for index in range(start, len(lines)) if lines[index].startswith("## ")),
        len(lines),
    )
    return lines[start:end]


def _canonical_handoff_identity_is_valid(text: str) -> bool:
    section = _first_visible_section(text, "## 1. Session Identity")
    if section is None:
        return False
    candidates = [line for line in section if line.startswith("- Active packet:")]
    return candidates == ["- Active packet: [packet:bootstrap]"]


def _active_ledger_records_are_valid(
    text: str,
    heading: str,
    kind: str,
    packet_id: str,
    *,
    require_record: bool,
) -> bool:
    section = _first_visible_section(text, heading)
    if section is None:
        return False
    records = [line for line in section if line.startswith("- ")]
    if require_record and not records:
        return False
    pattern = _V2_REVIEW_OPEN_RECORD if kind == "review" else _V2_TODO_OPEN_RECORD
    for record in records:
        match = pattern.fullmatch(record)
        if match is None or match.group("packet") != packet_id:
            return False
    return True


def _canonical_state_identity_is_valid(text: str, packet_id: str) -> bool:
    result = inspect_state(text)
    snapshot = result.snapshot
    if result.state_version != 2 or snapshot is None:
        return False
    scale = snapshot.scalar("scale")
    scope = snapshot.scalar("execution_scope")
    validation_for = snapshot.scalar("validation_for")
    active_packet_id = snapshot.active_packet.get("id")
    return (
        not result.issues
        and scale is not None
        and scale.value == "standard"
        and scope is not None
        and scope.value == "packet"
        and active_packet_id is not None
        and active_packet_id.value == packet_id
        and validation_for is not None
        and validation_for.value == packet_id
    )


def _validate_task8_templates(
    root: Path,
    canonical_state: str,
    index: str,
    violations: list[str],
) -> None:
    canonical_state_path = "templates/project-control-files/sdad-state.yaml"
    if canonical_state:
        _require_phrases(
            canonical_state_path,
            canonical_state,
            (
                "version: 2",
                "scale: standard",
                "execution_scope: packet",
                "  id: bootstrap",
                "validation_for: bootstrap",
                "# current_handoff: docs/sdad/handoffs/YYYY-MM-DD-topic.md",
            ),
            violations,
        )
        if (
            not collect_template_state_violations(canonical_state)
            and not _canonical_state_identity_is_valid(canonical_state, "bootstrap")
        ):
            violations.append(
                "canonical state active_packet.id must equal bootstrap"
            )

    for relative_path, phrases in TASK8_REQUIRED_PHRASES.items():
        text = _read(root, relative_path, violations)
        if text:
            _require_phrases(relative_path, text, phrases, violations)

    ledger_contracts = (
        (
            "templates/project-control-files/review-findings.md",
            "## Active Findings",
            "review",
            False,
        ),
        (
            "templates/project-control-files/docs/TODO-Open-Items.md",
            "## Active Work",
            "todo",
            True,
        ),
        (
            "templates/project-control-files/docs/TODO-Open-Items.md",
            "## Release / Production Readiness",
            "todo",
            True,
        ),
    )
    for relative_path, heading, kind, require_record in ledger_contracts:
        text = _read(root, relative_path, violations)
        if text and not _active_ledger_records_are_valid(
            text,
            heading,
            kind,
            "bootstrap",
            require_record=require_record,
        ):
            message = f"{relative_path} has a malformed active record"
            if message not in violations:
                violations.append(message)

    handoff_path = (
        "templates/project-control-files/docs/sdad/handoffs/YYYY-MM-DD-topic.md"
    )
    handoff = _read(root, handoff_path, violations)
    if handoff and not _canonical_handoff_identity_is_valid(handoff):
        violations.append(
            "canonical handoff first Session Identity section must contain "
            "exactly one bootstrap marker"
        )

    index_path = "templates/project-control-files/docs/INDEX.md"
    if index and index.count(CURRENT_HANDOFF_SOURCE) != 1:
        violations.append(
            f"{index_path} must contain exactly one canonical "
            "current-handoff source line"
        )


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

    _validate_task8_templates(
        root,
        state,
        content.get("templates/project-control-files/docs/INDEX.md", ""),
        violations,
    )

    _read(
        root,
        "templates/project-control-files/docs/Repository-Operating-Rules.md",
        violations,
    )
    for relative_path in STARTUP_SURFACES:
        text = content.get(relative_path, "")
        if text:
            violation_count = len(violations)
            _require_ordered_tokens(
                relative_path,
                text,
                ORDERED_STARTUP_ROUTE,
                violations,
            )
            if len(violations) == violation_count:
                _validate_startup_kernel(relative_path, text, violations)

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
