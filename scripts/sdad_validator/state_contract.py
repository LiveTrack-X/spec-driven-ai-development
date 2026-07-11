from __future__ import annotations

import json
import re
from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import PurePosixPath
from types import MappingProxyType


SUPPORTED_STATE_VERSIONS = frozenset({1, 2})
V2_PACKET_ID_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")

V1_STATE_KEYS = (
    "scale",
    "intensity",
    "autonomy",
    "active_spec",
    "active_packet",
    "owner_gates",
    "validation",
    "routed_docs",
)
V2_STATE_KEYS = (*V1_STATE_KEYS, "validation_for", "current_handoff")

REQUIRED_TOP_LEVEL_KEYS_BY_VERSION = {
    1: frozenset(V1_STATE_KEYS),
    2: frozenset((*V1_STATE_KEYS, "validation_for")),
}
KNOWN_TOP_LEVEL_KEYS_BY_VERSION = {
    1: frozenset(("version", "updated", *V1_STATE_KEYS)),
    2: frozenset(("version", "updated", *V2_STATE_KEYS)),
}
STATE_ENUMS_BY_VERSION = {
    1: {
        "scale": frozenset({"one-shot", "mini", "standard", "full"}),
        "intensity": frozenset({"low", "medium", "high"}),
        "autonomy": frozenset({"0", "1", "2", "3", "4"}),
    },
    2: {
        "scale": frozenset({"standard", "full"}),
        "intensity": frozenset({"low", "medium", "high"}),
        "autonomy": frozenset({"0", "1", "2", "3", "4"}),
    },
}

ACTIVE_PACKET_KEYS = ("id", "objective", "status")
ACTIVE_PACKET_STATUSES = frozenset(
    {
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
)

STATE_COLLECTION_KINDS = {
    "active_packet": "mapping",
    "owner_gates": "list",
    "validation": "list",
    "routed_docs": "list",
}

_KEY_PATTERN = r"[A-Za-z_][\w-]*"
_MAPPING_LINE = re.compile(
    rf"^(?P<key>{_KEY_PATTERN}):(?P<tail>(?:[ \t].*)?)$"
)
_PLAIN_YAML_DIRECTIVE = re.compile(r"(?:^|\s)[&*!](?:\S+|$)")


@dataclass(frozen=True)
class LocatedScalar:
    value: str
    line: int


@dataclass(frozen=True)
class ValidationEntry:
    fields: Mapping[str, LocatedScalar]
    line: int


@dataclass(frozen=True)
class StateSnapshot:
    scalars: Mapping[str, LocatedScalar]
    active_packet: Mapping[str, LocatedScalar]
    owner_gates: tuple[LocatedScalar, ...]
    validation: tuple[ValidationEntry, ...]
    routed_docs: tuple[LocatedScalar, ...]

    def scalar(self, key: str) -> LocatedScalar | None:
        return self.scalars.get(key)


@dataclass(frozen=True)
class StateIssue:
    id: str
    severity: str
    message: str
    evidence: str
    line: int | None
    legacy_message: str | None = None


@dataclass(frozen=True)
class StateContractResult:
    snapshot: StateSnapshot | None
    issues: tuple[StateIssue, ...]
    state_version: int | None = None


@dataclass(frozen=True)
class _MappingItem:
    key: str
    node: "_Node"
    line: int


@dataclass(frozen=True)
class _Node:
    kind: str
    line: int
    scalar: str | None = None
    mapping: tuple[_MappingItem, ...] = ()
    items: tuple["_Node", ...] = ()
    inline_empty_list: bool = False


class _UnsupportedSyntax(ValueError):
    def __init__(self, message: str, line: int) -> None:
        super().__init__(message)
        self.line = line


def is_normalized_relative_posix_path(value: str) -> bool:
    if (
        not value
        or not value.strip()
        or value.startswith("/")
        or "\\" in value
        or ":" in value
    ):
        return False
    path = PurePosixPath(value)
    return (
        not path.is_absolute()
        and "." not in path.parts
        and ".." not in path.parts
        and path.as_posix() == value
    )


def is_valid_v2_packet_id(value: str) -> bool:
    return V2_PACKET_ID_PATTERN.fullmatch(value) is not None


def _issue(
    issue_id: str,
    severity: str,
    message: str,
    evidence: str,
    line: int | None,
    legacy_message: str | None = None,
) -> StateIssue:
    return StateIssue(
        id=issue_id,
        severity=severity,
        message=message,
        evidence=evidence,
        line=line,
        legacy_message=legacy_message,
    )


def _indent(line: str, line_number: int) -> int:
    prefix = line[: len(line) - len(line.lstrip(" \t"))]
    if "\t" in prefix:
        raise _UnsupportedSyntax("tabs cannot be used for indentation", line_number)
    return len(prefix)


def _is_ignorable(line: str) -> bool:
    return not line.strip() or line.lstrip().startswith("#")


def _plain_without_comment(value: str) -> str:
    for index, character in enumerate(value):
        if character == "#" and (index == 0 or value[index - 1].isspace()):
            return value[:index].rstrip()
    return value.rstrip()


def _quoted_scalar(value: str, line: int) -> str:
    quote = value[0]
    index = 1
    decoded: list[str] = []
    while index < len(value):
        character = value[index]
        if quote == "'" and character == "'":
            if index + 1 < len(value) and value[index + 1] == "'":
                decoded.append("'")
                index += 2
                continue
            raw_tail = value[index + 1 :]
            tail = raw_tail.strip()
            if tail and (
                not raw_tail[0].isspace() or not tail.startswith("#")
            ):
                raise _UnsupportedSyntax("content follows a quoted scalar", line)
            return "".join(decoded)
        if quote == '"' and character == '"':
            backslashes = 0
            cursor = index - 1
            while cursor >= 0 and value[cursor] == "\\":
                backslashes += 1
                cursor -= 1
            if backslashes % 2:
                decoded.append(character)
                index += 1
                continue
            token = value[: index + 1]
            raw_tail = value[index + 1 :]
            tail = raw_tail.strip()
            if tail and (
                not raw_tail[0].isspace() or not tail.startswith("#")
            ):
                raise _UnsupportedSyntax("content follows a quoted scalar", line)
            try:
                parsed = json.loads(token)
            except json.JSONDecodeError as exc:
                raise _UnsupportedSyntax("invalid double-quoted scalar", line) from exc
            if not isinstance(parsed, str):
                raise _UnsupportedSyntax("invalid double-quoted scalar", line)
            return parsed
        decoded.append(character)
        index += 1
    raise _UnsupportedSyntax("unterminated quoted scalar", line)


def _inline_node(raw_value: str, line: int) -> _Node | None:
    value = raw_value.strip()
    if not value or value.startswith("#"):
        return None
    if value[0] in {"'", '"'}:
        return _Node("scalar", line, scalar=_quoted_scalar(value, line))

    value = _plain_without_comment(value)
    if not value:
        return None
    if value == "[]":
        return _Node("list", line, inline_empty_list=True)
    if value.startswith(("[", "{")):
        raise _UnsupportedSyntax("flow collections other than [] are unsupported", line)
    if value.startswith(("|", ">")):
        raise _UnsupportedSyntax("multiline scalars are unsupported", line)
    if _PLAIN_YAML_DIRECTIVE.search(value):
        raise _UnsupportedSyntax("anchors, aliases, and tags are unsupported", line)
    return _Node("scalar", line, scalar=value)


def _mapping_item(line: str, indent: int, line_number: int) -> tuple[str, _Node | None]:
    content = line[indent:]
    match = _MAPPING_LINE.fullmatch(content)
    if match is None or match.group("key") == "<<":
        raise _UnsupportedSyntax("unsupported mapping entry", line_number)
    return match.group("key"), _inline_node(match.group("tail"), line_number)


def _next_content(lines: list[str], start: int, end: int) -> int | None:
    for index in range(start, end):
        if not _is_ignorable(lines[index]):
            return index
    return None


def _parse_mapping_block(lines: list[str], start: int, end: int) -> _Node:
    items: list[_MappingItem] = []
    first_line = start + 1
    for index in range(start, end):
        line = lines[index]
        if _is_ignorable(line):
            continue
        line_number = index + 1
        if _indent(line, line_number) != 2:
            raise _UnsupportedSyntax("mapping entries must use two-space indentation", line_number)
        key, node = _mapping_item(line, 2, line_number)
        items.append(_MappingItem(key, node or _Node("empty", line_number), line_number))
    return _Node("mapping", first_line, mapping=tuple(items))


def _list_mapping_item(
    lines: list[str],
    index: int,
    end: int,
    first_content: str,
) -> tuple[_Node, int]:
    line_number = index + 1
    fields: list[_MappingItem] = []
    if first_content:
        key, node = _mapping_item(first_content, 0, line_number)
        fields.append(_MappingItem(key, node or _Node("empty", line_number), line_number))
    index += 1
    while index < end:
        line = lines[index]
        if _is_ignorable(line):
            index += 1
            continue
        child_line = index + 1
        indentation = _indent(line, child_line)
        if indentation == 2:
            break
        if indentation != 4:
            raise _UnsupportedSyntax(
                "list mapping entries must use four-space indentation",
                child_line,
            )
        key, node = _mapping_item(line, 4, child_line)
        fields.append(_MappingItem(key, node or _Node("empty", child_line), child_line))
        index += 1
    if not fields:
        return _Node("empty", line_number), index
    return _Node("mapping", line_number, mapping=tuple(fields)), index


def _looks_like_mapping_entry(value: str) -> bool:
    return re.match(rf"^{_KEY_PATTERN}:(?:\s|$)", value) is not None


def _parse_list_block(lines: list[str], start: int, end: int) -> _Node:
    items: list[_Node] = []
    first_line = start + 1
    index = start
    while index < end:
        line = lines[index]
        if _is_ignorable(line):
            index += 1
            continue
        line_number = index + 1
        if _indent(line, line_number) != 2:
            raise _UnsupportedSyntax("list entries must use two-space indentation", line_number)
        content = line[2:]
        if content != "-" and not content.startswith("- "):
            raise _UnsupportedSyntax("unsupported list entry", line_number)
        value = content[1:].lstrip()
        if not value or value.startswith("#") or _looks_like_mapping_entry(value):
            node, index = _list_mapping_item(lines, index, end, value)
            items.append(node)
            continue
        node = _inline_node(value, line_number)
        items.append(node or _Node("scalar", line_number, scalar=""))
        index += 1
        next_index = _next_content(lines, index, end)
        if next_index is not None and _indent(lines[next_index], next_index + 1) > 2:
            raise _UnsupportedSyntax("scalar list entries cannot have children", next_index + 1)
    return _Node("list", first_line, items=tuple(items))


def _parse_block(lines: list[str], start: int, end: int) -> _Node:
    first = _next_content(lines, start, end)
    if first is None:
        return _Node("empty", start)
    line_number = first + 1
    if _indent(lines[first], line_number) != 2:
        raise _UnsupportedSyntax("nested content must use two-space indentation", line_number)
    content = lines[first][2:]
    if content == "-" or content.startswith("- "):
        return _parse_list_block(lines, start, end)
    return _parse_mapping_block(lines, start, end)


def _parse(text: str) -> tuple[_MappingItem, ...]:
    lines = text.splitlines()
    top_level: list[_MappingItem] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if _is_ignorable(line):
            index += 1
            continue
        line_number = index + 1
        if _indent(line, line_number) != 0:
            raise _UnsupportedSyntax("top-level keys cannot be indented", line_number)
        key, inline = _mapping_item(line, 0, line_number)
        if inline is not None:
            top_level.append(_MappingItem(key, inline, line_number))
            index += 1
            continue

        block_end = index + 1
        while block_end < len(lines):
            candidate = lines[block_end]
            if not _is_ignorable(candidate) and _indent(candidate, block_end + 1) == 0:
                break
            block_end += 1
        node = _parse_block(lines, index + 1, block_end)
        top_level.append(_MappingItem(key, node, line_number))
        index = block_end
    return tuple(top_level)


def _by_key(items: tuple[_MappingItem, ...]) -> dict[str, list[_MappingItem]]:
    grouped: dict[str, list[_MappingItem]] = {}
    for item in items:
        grouped.setdefault(item.key, []).append(item)
    return grouped


def _last_nodes(items: tuple[_MappingItem, ...]) -> dict[str, _Node]:
    return {item.key: item.node for item in items}


def _compatibility_scalar(node: _Node) -> str | None:
    if node.kind == "scalar":
        return node.scalar
    if node.inline_empty_list:
        return "[]"
    return None


def _duplicate_issues(
    grouped: dict[str, list[_MappingItem]],
    context: str,
    legacy_prefix: str | None,
) -> list[StateIssue]:
    issues: list[StateIssue] = []
    for key in sorted(key for key, values in grouped.items() if len(values) > 1):
        for duplicate_index, duplicate in enumerate(grouped[key][1:]):
            legacy = (
                f"{legacy_prefix}{key}"
                if legacy_prefix is not None and duplicate_index == 0
                else None
            )
            issues.append(
                _issue(
                    "state.schema.duplicate-key",
                    "error",
                    f"Duplicate {context} key: {key}",
                    key,
                    duplicate.line,
                    legacy,
                )
            )
    return issues


def _resolve_state_version(
    top_level: tuple[_MappingItem, ...],
) -> tuple[int | None, tuple[StateIssue, ...]]:
    grouped = _by_key(top_level)
    if "version" not in grouped:
        return (
            1,
            (
                _issue(
                    "state.schema.missing-version",
                    "warning",
                    "State version is missing; legacy version 1 compatibility is assumed",
                    "version",
                    None,
                ),
            ),
        )

    version = grouped["version"][-1].node
    if version.kind != "scalar":
        return (
            None,
            (
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    "State version must be a scalar",
                    version.kind,
                    version.line,
                ),
            ),
        )

    declared = version.scalar or ""
    for supported in SUPPORTED_STATE_VERSIONS:
        if declared == str(supported):
            return supported, ()
    return (
        None,
        (
            _issue(
                "state.schema.unsupported-version",
                "error",
                f"Unsupported state version: {declared}",
                declared,
                version.line,
            ),
        ),
    )


def _v2_contract_issues(top_level: tuple[_MappingItem, ...]) -> list[StateIssue]:
    issues: list[StateIssue] = []
    grouped = _by_key(top_level)
    nodes = _last_nodes(top_level)
    issues.extend(_duplicate_issues(grouped, "top-level", None))

    required = REQUIRED_TOP_LEVEL_KEYS_BY_VERSION[2]
    for key in V2_STATE_KEYS:
        if key in required and key not in grouped:
            issues.append(
                _issue(
                    "state.schema.missing-key",
                    "error",
                    f"Missing required state key: {key}",
                    key,
                    None,
                )
            )

    for key, allowed in STATE_ENUMS_BY_VERSION[2].items():
        node = nodes.get(key)
        if node is None:
            continue
        if node.kind != "scalar":
            issues.append(
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    f"State key {key} must be a scalar",
                    node.kind,
                    node.line,
                )
            )
        elif node.scalar not in allowed:
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported {key}: {node.scalar}",
                    node.scalar or "",
                    node.line,
                )
            )

    validation_for = nodes.get("validation_for")
    if validation_for is not None:
        if validation_for.kind != "scalar":
            issues.append(
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    "State key validation_for must be a scalar",
                    validation_for.kind,
                    validation_for.line,
                )
            )
        elif not is_valid_v2_packet_id(validation_for.scalar or ""):
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported validation_for: {validation_for.scalar}",
                    validation_for.scalar or "",
                    validation_for.line,
                )
            )

    active_spec_node = nodes.get("active_spec")
    if (
        active_spec_node is not None
        and active_spec_node.kind == "scalar"
        and not is_normalized_relative_posix_path(active_spec_node.scalar or "")
    ):
        issues.append(
            _issue(
                "path.invalid",
                "error",
                "active_spec must be a normalized repository-relative POSIX path",
                active_spec_node.scalar or "",
                active_spec_node.line,
            )
        )

    current_handoff = nodes.get("current_handoff")
    if current_handoff is not None:
        if current_handoff.kind != "scalar":
            issues.append(
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    "State key current_handoff must be a scalar",
                    current_handoff.kind,
                    current_handoff.line,
                )
            )
        elif not is_normalized_relative_posix_path(current_handoff.scalar or ""):
            issues.append(
                _issue(
                    "path.invalid",
                    "error",
                    "current_handoff must be a normalized repository-relative POSIX path",
                    current_handoff.scalar or "",
                    current_handoff.line,
                )
            )

    for key, expected in STATE_COLLECTION_KINDS.items():
        node = nodes.get(key)
        if node is None or node.kind == expected:
            continue
        issues.append(
            _issue(
                "state.schema.wrong-kind",
                "error",
                f"State key {key} must be a {expected}",
                node.kind,
                node.line,
            )
        )

    packet_node = nodes.get("active_packet")
    if packet_node is not None and packet_node.kind == "mapping":
        packet_grouped = _by_key(packet_node.mapping)
        packet_nodes = _last_nodes(packet_node.mapping)
        issues.extend(_duplicate_issues(packet_grouped, "active_packet", None))
        for key in ACTIVE_PACKET_KEYS:
            node = packet_nodes.get(key)
            if node is None:
                issues.append(
                    _issue(
                        "state.packet.missing-field",
                        "error",
                        f"active_packet is missing {key}",
                        key,
                        packet_node.line,
                    )
                )
            elif node.kind == "empty" or (
                node.kind == "scalar" and not (node.scalar or "").strip()
            ):
                issues.append(
                    _issue(
                        "state.packet.blank-field",
                        "error",
                        f"active_packet {key} must not be blank",
                        key,
                        node.line,
                    )
                )
            elif node.kind != "scalar":
                issues.append(
                    _issue(
                        "state.schema.wrong-kind",
                        "error",
                        f"active_packet {key} must be a scalar",
                        node.kind,
                        node.line,
                    )
                )

        packet_id_node = packet_nodes.get("id")
        packet_id = (
            packet_id_node.scalar
            if packet_id_node is not None and packet_id_node.kind == "scalar"
            else None
        )
        if packet_id is not None and packet_id.strip() and not is_valid_v2_packet_id(packet_id):
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported active_packet id: {packet_id}",
                    packet_id,
                    packet_id_node.line,
                )
            )

        status_node = packet_nodes.get("status")
        status = (
            status_node.scalar
            if status_node is not None and status_node.kind == "scalar"
            else None
        )
        if status is not None and status.strip() and status not in ACTIVE_PACKET_STATUSES:
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported active_packet status: {status}",
                    status,
                    status_node.line,
                )
            )
    return issues


def _unversioned_duplicate_issues(
    top_level: tuple[_MappingItem, ...],
) -> list[StateIssue]:
    issues = _duplicate_issues(_by_key(top_level), "top-level", None)
    nodes = _last_nodes(top_level)

    packet = nodes.get("active_packet")
    if packet is not None and packet.kind == "mapping":
        issues.extend(
            _duplicate_issues(_by_key(packet.mapping), "active_packet", None)
        )

    validation = nodes.get("validation")
    if validation is not None and validation.kind == "list":
        for entry in validation.items:
            if entry.kind == "mapping":
                issues.extend(
                    _duplicate_issues(
                        _by_key(entry.mapping),
                        "validation entry",
                        None,
                    )
                )
    return issues


def _legacy_issues(top_level: tuple[_MappingItem, ...]) -> list[StateIssue]:
    issues: list[StateIssue] = []
    grouped = _by_key(top_level)
    nodes = _last_nodes(top_level)
    issues.extend(
        _duplicate_issues(
            grouped,
            "top-level",
            "sdad-state.yaml duplicate top-level key: ",
        )
    )

    for key in V1_STATE_KEYS:
        if key not in grouped:
            legacy = f"sdad-state.yaml missing top-level key: {key}"
            issues.append(
                _issue(
                    "state.schema.missing-key",
                    "error",
                    f"Missing required state key: {key}",
                    key,
                    None,
                    legacy,
                )
            )

    for key, allowed in STATE_ENUMS_BY_VERSION[1].items():
        if key not in grouped:
            continue
        node = nodes[key]
        value = _compatibility_scalar(node)
        if value is None:
            legacy = f"sdad-state.yaml missing scalar value: {key}"
            issues.append(
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    f"State key {key} must be a scalar",
                    node.kind,
                    node.line,
                    legacy,
                )
            )
        elif value not in allowed:
            legacy = f"unsupported {key}: {value}"
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported {key}: {value}",
                    value,
                    node.line,
                    legacy,
                )
            )

    active_spec_node = nodes.get("active_spec")
    if active_spec_node is not None:
        active_spec = _compatibility_scalar(active_spec_node)
        if active_spec is not None and not is_normalized_relative_posix_path(active_spec):
            legacy = (
                None
                if active_spec and not active_spec.strip()
                else (
                    "sdad-state.yaml active_spec must be a relative path: "
                    f"{active_spec}"
                )
            )
            issues.append(
                _issue(
                    "path.invalid",
                    "error",
                    "active_spec must be a normalized repository-relative POSIX path",
                    active_spec,
                    active_spec_node.line,
                    legacy,
                )
            )

    for key, expected in STATE_COLLECTION_KINDS.items():
        node = nodes.get(key)
        if node is None or node.kind == expected:
            continue
        legacy = f"sdad-state.yaml {key} must be a {expected}"
        issues.append(
            _issue(
                "state.schema.wrong-kind",
                "error",
                f"State key {key} must be a {expected}",
                node.kind,
                node.line,
                legacy,
            )
        )

    packet_node = nodes.get("active_packet")
    if packet_node is not None and packet_node.kind == "mapping":
        packet_grouped = _by_key(packet_node.mapping)
        packet_nodes = _last_nodes(packet_node.mapping)
        issues.extend(
            _duplicate_issues(
                packet_grouped,
                "active_packet",
                "sdad-state.yaml active_packet duplicate key: ",
            )
        )
        for key in ACTIVE_PACKET_KEYS:
            node = packet_nodes.get(key)
            if node is None:
                legacy = f"sdad-state.yaml active_packet missing key: {key}"
                issues.append(
                    _issue(
                        "state.packet.missing-field",
                        "error",
                        f"active_packet is missing {key}",
                        key,
                        packet_node.line,
                        legacy,
                    )
                )
            elif node.kind == "empty":
                legacy = f"sdad-state.yaml active_packet missing key: {key}"
                issues.append(
                    _issue(
                        "state.packet.blank-field",
                        "error",
                        f"active_packet {key} must not be blank",
                        key,
                        node.line,
                        legacy,
                    )
                )
            elif node.kind == "scalar" and not node.scalar.strip():
                legacy = (
                    f"unsupported active_packet status: {node.scalar}"
                    if key == "status"
                    else None
                )
                issues.append(
                    _issue(
                        "state.packet.blank-field",
                        "error",
                        f"active_packet {key} must not be blank",
                        key,
                        node.line,
                        legacy,
                    )
                )
        status_node = packet_nodes.get("status")
        status = _compatibility_scalar(status_node) if status_node is not None else None
        if (
            status is not None
            and status.strip()
            and status not in ACTIVE_PACKET_STATUSES
        ):
            legacy = f"unsupported active_packet status: {status}"
            issues.append(
                _issue(
                    "state.schema.unsupported-value",
                    "error",
                    f"Unsupported active_packet status: {status}",
                    status,
                    status_node.line,
                    legacy,
                )
            )
    return issues


def _schema_issues(
    top_level: tuple[_MappingItem, ...],
    state_version: int,
) -> list[StateIssue]:
    issues: list[StateIssue] = []
    grouped = _by_key(top_level)
    nodes = _last_nodes(top_level)

    known_top_level_keys = KNOWN_TOP_LEVEL_KEYS_BY_VERSION[state_version]
    for key, values in grouped.items():
        if key not in known_top_level_keys:
            issues.append(
                _issue(
                    "state.schema.unknown-key",
                    "warning",
                    f"Unknown top-level state key: {key}",
                    key,
                    values[-1].line,
                )
            )

    for key in ("updated", "active_spec"):
        node = nodes.get(key)
        if node is not None and node.kind != "scalar":
            issues.append(
                _issue(
                    "state.schema.wrong-kind",
                    "error",
                    f"State key {key} must be a scalar",
                    node.kind,
                    node.line,
                )
            )

    packet = nodes.get("active_packet")
    if packet is not None and packet.kind == "mapping":
        packet_grouped = _by_key(packet.mapping)
        packet_nodes = _last_nodes(packet.mapping)
        for key, values in packet_grouped.items():
            if key not in ACTIVE_PACKET_KEYS:
                issues.append(
                    _issue(
                        "state.schema.unknown-key",
                        "warning",
                        f"Unknown active_packet key: {key}",
                        key,
                        values[-1].line,
                    )
                )
        for key in ACTIVE_PACKET_KEYS:
            node = packet_nodes.get(key)
            if node is None:
                continue
            if node.kind == "empty":
                continue
            if state_version == 1 and node.kind != "scalar":
                issues.append(
                    _issue(
                        "state.schema.wrong-kind",
                        "error",
                        f"active_packet {key} must be a scalar",
                        node.kind,
                        node.line,
                    )
                )

    for key in ("owner_gates", "routed_docs"):
        collection = nodes.get(key)
        if collection is None or collection.kind != "list":
            continue
        for item in collection.items:
            if item.kind != "scalar" or not item.scalar.strip():
                issues.append(
                    _issue(
                        "state.collection.malformed-entry",
                        "error",
                        f"{key} entries must be non-empty scalars",
                        item.kind if item.kind != "scalar" else "blank",
                        item.line,
                    )
                )
            elif key == "routed_docs" and not is_normalized_relative_posix_path(item.scalar):
                issues.append(
                    _issue(
                        "path.invalid",
                        "error",
                        "routed_docs entries must be normalized repository-relative POSIX paths",
                        item.scalar,
                        item.line,
                    )
                )

    validation = nodes.get("validation")
    if validation is not None and validation.kind == "list":
        for entry in validation.items:
            if entry.kind != "mapping":
                issues.append(
                    _issue(
                        "state.collection.malformed-entry",
                        "error",
                        "validation entries must be mappings",
                        entry.kind,
                        entry.line,
                    )
                )
                continue
            entry_grouped = _by_key(entry.mapping)
            issues.extend(_duplicate_issues(entry_grouped, "validation entry", None))
            for field, values in entry_grouped.items():
                node = values[-1].node
                if field not in {"command", "proves"}:
                    issues.append(
                        _issue(
                            "validation.unknown-key",
                            "warning",
                            f"Unknown validation key: {field}",
                            field,
                            values[-1].line,
                        )
                    )
                if node.kind != "scalar":
                    issues.append(
                        _issue(
                            "state.collection.malformed-entry",
                            "error",
                            f"validation {field} must be a scalar",
                            node.kind,
                            node.line,
                        )
                    )
    return issues


def _snapshot(top_level: tuple[_MappingItem, ...]) -> StateSnapshot:
    nodes = _last_nodes(top_level)
    scalars = {
        key: LocatedScalar(node.scalar or "", node.line)
        for key, node in nodes.items()
        if node.kind == "scalar"
    }

    active_packet: dict[str, LocatedScalar] = {}
    packet = nodes.get("active_packet")
    if packet is not None and packet.kind == "mapping":
        packet_nodes = _last_nodes(packet.mapping)
        active_packet = {
            key: LocatedScalar(node.scalar or "", node.line)
            for key, node in packet_nodes.items()
            if node.kind == "scalar"
        }

    def scalar_collection(key: str) -> tuple[LocatedScalar, ...]:
        node = nodes.get(key)
        if node is None or node.kind != "list":
            return ()
        return tuple(
            LocatedScalar(item.scalar or "", item.line)
            for item in node.items
            if item.kind == "scalar"
        )

    validation_entries: list[ValidationEntry] = []
    validation = nodes.get("validation")
    if validation is not None and validation.kind == "list":
        for entry in validation.items:
            if entry.kind != "mapping":
                continue
            field_nodes = _last_nodes(entry.mapping)
            fields = {
                key: LocatedScalar(node.scalar or "", node.line)
                for key, node in field_nodes.items()
                if node.kind == "scalar"
            }
            validation_entries.append(
                ValidationEntry(MappingProxyType(fields), entry.line)
            )

    return StateSnapshot(
        scalars=MappingProxyType(scalars),
        active_packet=MappingProxyType(active_packet),
        owner_gates=scalar_collection("owner_gates"),
        validation=tuple(validation_entries),
        routed_docs=scalar_collection("routed_docs"),
    )


def inspect_state(text: str) -> StateContractResult:
    try:
        top_level = _parse(text)
    except _UnsupportedSyntax as exc:
        issue = _issue(
            "state.syntax.unsupported",
            "error",
            f"Unsupported sdad-state.yaml syntax on line {exc.line}: {exc}",
            str(exc),
            exc.line,
        )
        return StateContractResult(snapshot=None, issues=(issue,))

    state_version, version_issues = _resolve_state_version(top_level)
    if state_version == 1:
        issues = (
            *_legacy_issues(top_level),
            *version_issues,
            *_schema_issues(top_level, state_version),
        )
    elif state_version == 2:
        issues = (
            *_v2_contract_issues(top_level),
            *version_issues,
            *_schema_issues(top_level, state_version),
        )
    else:
        issues = (
            *_unversioned_duplicate_issues(top_level),
            *version_issues,
        )
    return StateContractResult(
        snapshot=_snapshot(top_level),
        issues=issues,
        state_version=state_version,
    )


def collect_template_state_violations(text: str) -> list[str]:
    if not text:
        return []
    result = inspect_state(text)
    if result.snapshot is None:
        return [issue.message for issue in result.issues if issue.severity == "error"]
    if result.state_version == 2:
        return [issue.message for issue in result.issues if issue.severity == "error"]
    return [
        issue.legacy_message
        for issue in result.issues
        if issue.legacy_message is not None
    ]
