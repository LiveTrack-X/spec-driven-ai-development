from __future__ import annotations

import re
from pathlib import Path, PurePosixPath


SURFACE_BUDGETS = {
    "templates/project-control-files/AGENTS.md": (120, 6_000),
    "templates/project-control-files/docs/INDEX.md": (80, 4_000),
    "templates/project-control-files/sdad-state.yaml": (80, 2_000),
    "adapters/codex/AGENTS.md": (120, 6_000),
    "adapters/claude-code/CLAUDE.md": (120, 6_000),
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc": (120, 6_000),
    "adapters/github-copilot/.github/copilot-instructions.md": (120, 6_000),
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md": (120, 6_000),
}

STATE_KEYS = (
    "scale",
    "intensity",
    "autonomy",
    "active_spec",
    "active_packet",
    "owner_gates",
    "validation",
    "routed_docs",
)

STATE_ENUMS = {
    "scale": {"one-shot", "mini", "standard", "full"},
    "intensity": {"low", "medium", "high"},
    "autonomy": {"0", "1", "2", "3", "4"},
}

ACTIVE_PACKET_KEYS = ("id", "objective", "status")
ACTIVE_PACKET_STATUSES = {
    "not_started",
    "in_progress",
    "ai_complete",
    "software_verified",
    "tester_ready",
    "hardware_evidence_received",
    "hardware_verified",
    "owner_accepted",
    "release_candidate",
    "production_ready",
    "blocked",
    "deferred",
}

STATE_COLLECTION_KINDS = {
    "active_packet": "mapping",
    "owner_gates": "list",
    "validation": "list",
    "routed_docs": "list",
}

STARTUP_SURFACES = (
    "templates/project-control-files/AGENTS.md",
    "adapters/codex/AGENTS.md",
    "adapters/claude-code/CLAUDE.md",
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


def _top_level_yaml_keys(text: str) -> set[str]:
    return set(re.findall(r"^([A-Za-z_][\w-]*):(?:\s|$)", text, re.MULTILINE))


def _top_level_yaml_key_list(text: str) -> list[str]:
    return re.findall(r"^([A-Za-z_][\w-]*):(?:\s|$)", text, re.MULTILINE)


def _top_level_yaml_scalars(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(
            r"^([A-Za-z_][\w-]*):(?:[ \t]+([^#\r\n]+?))?[ \t]*(?:#.*)?$",
            line,
        )
        if match is None or match.group(2) is None:
            continue
        values[match.group(1)] = match.group(2).strip().strip("'\"")
    return values


def _top_level_yaml_value_kinds(text: str) -> dict[str, str]:
    lines = text.splitlines()
    kinds: dict[str, str] = {}
    for index, line in enumerate(lines):
        match = re.match(r"^([A-Za-z_][\w-]*):[ \t]*(.*)$", line)
        if match is None:
            continue
        key = match.group(1)
        inline = match.group(2).split("#", 1)[0].strip()
        if inline:
            if inline.startswith("{") and inline.endswith("}"):
                kinds[key] = "mapping"
            elif inline.startswith("[") and inline.endswith("]"):
                kinds[key] = "list"
            else:
                kinds[key] = "scalar"
            continue

        kinds[key] = "empty"
        for child in lines[index + 1 :]:
            if not child.strip() or child.lstrip().startswith("#"):
                continue
            if child == child.lstrip():
                break
            kinds[key] = "list" if child.lstrip().startswith("-") else "mapping"
            break
    return kinds


def _mapping_scalars(text: str, parent_key: str) -> tuple[dict[str, str], list[str]]:
    lines = text.splitlines()
    values: dict[str, str] = {}
    keys: list[str] = []
    inside = False
    for line in lines:
        if not inside:
            if re.fullmatch(rf"{re.escape(parent_key)}:\s*(?:#.*)?", line):
                inside = True
            continue
        if line and line == line.lstrip():
            break
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(
            r"^[ \t]+([A-Za-z_][\w-]*):(?:[ \t]+([^#\r\n]+?))?"
            r"[ \t]*(?:#.*)?$",
            line,
        )
        if match is None:
            continue
        key = match.group(1)
        keys.append(key)
        if match.group(2) is not None:
            values[key] = match.group(2).strip().strip("'\"")
    duplicates = sorted({key for key in keys if keys.count(key) > 1})
    return values, duplicates


def _is_normalized_relative_posix_path(value: str) -> bool:
    if not value or value.startswith("/") or "\\" in value or ":" in value:
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and "." not in path.parts
        and ".." not in path.parts
        and path.as_posix() == value
    )


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
    top_level_key_list = _top_level_yaml_key_list(state)
    for key in sorted({key for key in top_level_key_list if top_level_key_list.count(key) > 1}):
        violations.append(f"sdad-state.yaml duplicate top-level key: {key}")
    top_level_keys = _top_level_yaml_keys(state)
    for key in STATE_KEYS:
        if state and key not in top_level_keys:
            violations.append(f"sdad-state.yaml missing top-level key: {key}")
    scalar_values = _top_level_yaml_scalars(state)
    for key, allowed in STATE_ENUMS.items():
        if not state or key not in top_level_keys:
            continue
        value = scalar_values.get(key)
        if value is None:
            violations.append(f"sdad-state.yaml missing scalar value: {key}")
        elif value not in allowed:
            violations.append(f"unsupported {key}: {value}")
    active_spec = scalar_values.get("active_spec")
    if active_spec is not None and not _is_normalized_relative_posix_path(active_spec):
        violations.append(f"sdad-state.yaml active_spec must be a relative path: {active_spec}")
    value_kinds = _top_level_yaml_value_kinds(state)
    for key, expected_kind in STATE_COLLECTION_KINDS.items():
        if not state or key not in top_level_keys:
            continue
        if value_kinds.get(key) != expected_kind:
            violations.append(f"sdad-state.yaml {key} must be a {expected_kind}")
    if value_kinds.get("active_packet") == "mapping":
        packet, duplicate_packet_keys = _mapping_scalars(state, "active_packet")
        for key in duplicate_packet_keys:
            violations.append(f"sdad-state.yaml active_packet duplicate key: {key}")
        for key in ACTIVE_PACKET_KEYS:
            if key not in packet:
                violations.append(f"sdad-state.yaml active_packet missing key: {key}")
        packet_status = packet.get("status")
        if packet_status is not None and packet_status not in ACTIVE_PACKET_STATUSES:
            violations.append(f"unsupported active_packet status: {packet_status}")

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
        prompt_match = re.search(
            r"^## Copy-Paste Start Prompt\s+.*?^```(?:text)?\s*\n(.*?)^```",
            readme,
            re.MULTILINE | re.DOTALL,
        )
        if prompt_match is None:
            violations.append("README copy-paste start prompt is missing")
        else:
            prompt = prompt_match.group(1)
            prompt_lines = _line_count(prompt)
            if prompt_lines > 100:
                violations.append(
                    f"README copy-paste prompt exceeds 100 lines: {prompt_lines}"
                )
            if len(prompt) > 6_000:
                violations.append(
                    f"README copy-paste prompt exceeds 6000 characters: {len(prompt)}"
                )
        for route in ("docs/user-guide.md", "docs/getting-started.md"):
            if route not in readme:
                violations.append(f"README Start Here missing route: {route}")

    return violations
