from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity
from ..state_contract import (
    ACTIVE_PACKET_STATUSES,
    is_normalized_relative_posix_path,
    is_valid_v2_packet_id,
)

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
INDEX_PATH = "docs/INDEX.md"
REVIEW_PATH = "review-findings.md"
TODO_PATH = "docs/TODO-Open-Items.md"
HANDOFF_HEADING = "## 1. Session Identity"
HANDOFF_PREFIX = "- Active packet:"
INDEX_HEADING = "## Active Catalog"
INDEX_SOURCE_PREFIX = "- Current handoff:"
INDEX_SOURCE_LINE = (
    "- Current handoff: use "
    "`../sdad-state.yaml#current_handoff` when declared."
)
REVIEW_HEADING = "## Active Findings"
TODO_HEADINGS = (
    "## Active Work",
    "## Release / Production Readiness",
)
COHERENCE_SENSITIVE_STATUSES = frozenset(
    {
        "software_verified",
        "tester_ready",
        "hardware_evidence_received",
        "hardware_verified",
        "release_candidate",
    }
)
TERMINAL_STATUSES = frozenset({"owner_accepted", "production_ready"})

_CLASSIFIED_REVIEW = re.compile(
    r"^- \[(Critical|High|Medium|Low)\] \[packet:([^\]]+)\] .+$"
)
_UNCLASSIFIED_REVIEW = re.compile(r"^- \[packet:([^\]]+)\] .+$")
_LINKED_TODO = re.compile(r"^- \[ \] \[packet:([^\]]+)\] .+$")
_HANDOFF_MARKER = re.compile(r"^- Active packet: \[packet:([^\]]+)\]$")
_MARKDOWN_FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
_V2_PACKET_MARKER = re.compile(r"\[packet:([^\]]*)\]")
_V2_PACKET_LIKE = re.compile(
    r"(?:\[[^\]\r\n]*packet[^\]\r\n]*(?:\]|$)|\bpacket\s*[:=])",
    re.IGNORECASE,
)
_V2_REVIEW_OPEN_RECORD = re.compile(
    r"^- (?:\[(?P<severity>Critical|High|Medium|Low)\] )?"
    r"\[packet:(?P<packet>[^\]]+)\] "
    r"(?P<description>\S(?:.*\S)?)$"
)
_V2_REVIEW_CLOSED_RECORD = re.compile(
    r"^- \[[xX]\] (?:\[(?P<severity>Critical|High|Medium|Low)\] )?"
    r"\[packet:(?P<packet>[^\]]+)\] "
    r"(?P<description>\S(?:.*\S)?)$"
)
_V2_TODO_OPEN_RECORD = re.compile(
    r"^- \[ \] \[packet:(?P<packet>[^\]]+)\] "
    r"(?P<description>\S(?:.*\S)?)$"
)
_V2_TODO_CLOSED_RECORD = re.compile(
    r"^- \[[xX]\] \[packet:(?P<packet>[^\]]+)\] "
    r"(?P<description>\S(?:.*\S)?)$"
)


@dataclass(frozen=True)
class _ActiveItem:
    line: int
    linked: bool
    critical: bool = False


@dataclass(frozen=True)
class _LedgerRecord:
    line: int
    closed: bool
    critical: bool
    marker_state: str
    packet_id: str | None
    grammar_valid: bool


def _read_control_document(context: DoctorContext, path: str) -> str | None:
    try:
        read_result = context.view.read_bytes(
            path,
            context.policy.max_control_document_bytes,
        )
    except OSError:
        return None
    if read_result.status != "ok" or read_result.data is None:
        return None
    try:
        return read_result.data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def _read_optional_document(context: DoctorContext, path: str) -> str | None:
    assert context.state_result.snapshot is not None
    declared = any(
        route.value == path for route in context.state_result.snapshot.routed_docs
    )
    inspection = context.view.inspect(path)
    if not declared and inspection.status == "missing":
        return None
    if inspection.status != "ok":
        return None
    return _read_control_document(context, path)


def _section_lines(
    lines: list[str],
    heading: str,
) -> list[tuple[int, str]] | None:
    try:
        heading_index = lines.index(heading)
    except ValueError:
        return None
    end_index = len(lines)
    for index in range(heading_index + 1, len(lines)):
        if lines[index].startswith("## "):
            end_index = index
            break
    return [
        (index + 1, lines[index])
        for index in range(heading_index + 1, end_index)
    ]


def _v2_section_lines(
    lines: list[str],
    heading: str,
) -> list[tuple[int, str]] | None:
    visible_lines: list[tuple[int, str]] = []
    fence_character: str | None = None
    fence_length = 0
    for line_number, line in enumerate(lines, start=1):
        fence = _MARKDOWN_FENCE.match(line)
        if fence_character is None:
            if fence is not None:
                delimiter, info = fence.groups()
                if delimiter[0] != "`" or "`" not in info:
                    fence_character = delimiter[0]
                    fence_length = len(delimiter)
                    continue
            visible_lines.append((line_number, line))
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

    heading_index = next(
        (
            index
            for index, (_, line) in enumerate(visible_lines)
            if line == heading
        ),
        None,
    )
    if heading_index is None:
        return None
    end_index = next(
        (
            index
            for index in range(heading_index + 1, len(visible_lines))
            if visible_lines[index][1].startswith("## ")
        ),
        len(visible_lines),
    )
    return visible_lines[heading_index + 1 : end_index]


def _captured_id(match: re.Match[str] | None, group: int) -> str | None:
    if match is None:
        return None
    captured = match.group(group).strip()
    return captured or None


def _review_items(text: str, packet_id: str | None) -> list[_ActiveItem] | None:
    section = _section_lines(text.splitlines(), REVIEW_HEADING)
    if section is None:
        return None
    items: list[_ActiveItem] = []
    for line_number, line in section:
        if not line.startswith("- "):
            continue
        if line.startswith("- [x] ") or line.startswith("- [X] "):
            continue
        classified = _CLASSIFIED_REVIEW.fullmatch(line)
        unclassified = _UNCLASSIFIED_REVIEW.fullmatch(line)
        captured = (
            _captured_id(classified, 2)
            if classified is not None
            else _captured_id(unclassified, 1)
        )
        items.append(
            _ActiveItem(
                line=line_number,
                linked=packet_id is not None and captured == packet_id,
                critical=(
                    classified is not None and classified.group(1) == "Critical"
                ),
            )
        )
    return items


def _todo_items(text: str, packet_id: str | None) -> list[_ActiveItem] | None:
    lines = text.splitlines()
    sections = [_section_lines(lines, heading) for heading in TODO_HEADINGS]
    if any(section is None for section in sections):
        return None
    items: list[_ActiveItem] = []
    for section in sections:
        assert section is not None
        for line_number, line in section:
            if not line.startswith("- [ ] "):
                continue
            captured = _captured_id(_LINKED_TODO.fullmatch(line), 1)
            items.append(
                _ActiveItem(
                    line=line_number,
                    linked=packet_id is not None and captured == packet_id,
                )
            )
    return items


def _parse_v2_record(
    line_number: int,
    line: str,
    *,
    open_pattern: re.Pattern[str],
    closed_pattern: re.Pattern[str],
) -> _LedgerRecord:
    closed = line.startswith(("- [x]", "- [X]"))
    grammar = (
        closed_pattern.fullmatch(line)
        if closed
        else open_pattern.fullmatch(line)
    )

    marker_candidate = _V2_PACKET_LIKE.search(line)
    marker = (
        _V2_PACKET_MARKER.fullmatch(marker_candidate.group(0))
        if marker_candidate is not None
        else None
    )
    packet_id = marker.group(1) if marker is not None else None
    if packet_id is not None and is_valid_v2_packet_id(packet_id):
        marker_state = "valid"
    elif marker_candidate is not None:
        marker_state = "invalid"
        packet_id = None
    else:
        marker_state = "missing"

    grammar_packet = grammar.group("packet") if grammar is not None else None
    grammar_valid = (
        grammar is not None
        and grammar_packet is not None
        and is_valid_v2_packet_id(grammar_packet)
    )
    severity = (
        grammar.groupdict().get("severity")
        if grammar_valid and grammar is not None
        else None
    )
    return _LedgerRecord(
        line=line_number,
        closed=closed,
        critical=severity == "Critical",
        marker_state=marker_state,
        packet_id=packet_id,
        grammar_valid=grammar_valid,
    )


def _parse_v2_review_records(text: str) -> list[_LedgerRecord] | None:
    section = _v2_section_lines(text.splitlines(), REVIEW_HEADING)
    if section is None:
        return None
    return [
        _parse_v2_record(
            line_number,
            line,
            open_pattern=_V2_REVIEW_OPEN_RECORD,
            closed_pattern=_V2_REVIEW_CLOSED_RECORD,
        )
        for line_number, line in section
        if line.startswith("- ")
    ]


def _parse_v2_todo_records(text: str) -> list[_LedgerRecord] | None:
    lines = text.splitlines()
    sections = [_v2_section_lines(lines, heading) for heading in TODO_HEADINGS]
    if any(section is None for section in sections):
        return None
    records: list[_LedgerRecord] = []
    for section in sections:
        assert section is not None
        records.extend(
            _parse_v2_record(
                line_number,
                line,
                open_pattern=_V2_TODO_OPEN_RECORD,
                closed_pattern=_V2_TODO_CLOSED_RECORD,
            )
            for line_number, line in section
            if line.startswith("- ")
        )
    return records


def _finding(
    finding_id: str,
    severity: Severity,
    *,
    path: str,
    line: int | None,
    evidence: str,
) -> Finding:
    messages = {
        "handoff.structure.missing-marker": (
            "The current handoff is missing its canonical active-packet marker."
        ),
        "handoff.structure.duplicate-marker": (
            "The current handoff contains multiple active-packet marker candidates."
        ),
        "handoff.structure.invalid-marker": (
            "The current handoff active-packet marker is malformed."
        ),
        "handoff.packet-mismatch": (
            "The current handoff marker does not match the active packet."
        ),
        "index.current-handoff-source": (
            "The INDEX current-handoff source is missing, duplicate, or noncanonical."
        ),
        "review.structure.missing-section": "The review document is missing its exact active section.",
        "todo.structure.missing-section": "The TODO document is missing a required exact section.",
        "packet.open-finding": "An active review finding remains for the current packet.",
        "packet.open-critical-finding": "A Critical current-packet finding remains at release candidate.",
        "packet.open-todo": "An unchecked TODO remains for the current packet.",
        "packet.unlinked-open-work": "Terminal packet state coexists with active unlinked work.",
        "packet.marker.unrepresentable": "The active packet ID cannot be represented by the marker grammar.",
        "ledger.open-item-missing-marker": (
            "An open active-ledger record is missing its packet marker."
        ),
        "ledger.open-item-invalid-marker": (
            "An open active-ledger record has an invalid packet marker."
        ),
        "ledger.open-item-malformed-record": (
            "An open active-ledger record violates the exact v2 grammar."
        ),
        "ledger.open-item-packet-mismatch": (
            "An open active-ledger record names another packet."
        ),
        "ledger.closed-review-in-active-section": (
            "A closed review finding remains in the active section."
        ),
        "ledger.closed-todo-in-active-section": (
            "A closed TODO remains in an active section."
        ),
    }
    remediations = {
        "handoff.structure.missing-marker": (
            "Add one canonical active-packet marker to the first exact "
            "Session Identity section."
        ),
        "handoff.structure.duplicate-marker": (
            "Keep exactly one active-packet marker in the first exact "
            "Session Identity section."
        ),
        "handoff.structure.invalid-marker": (
            "Use the exact - Active packet: [packet:ID] marker with a valid "
            "packet ID."
        ),
        "handoff.packet-mismatch": (
            "Update or replace the handoff so its marker matches active_packet.id."
        ),
        "index.current-handoff-source": (
            "Use the canonical current-handoff source line in the first exact "
            "Active Catalog section."
        ),
        "review.structure.missing-section": "Add the exact ## Active Findings section before diagnosing its contents.",
        "todo.structure.missing-section": "Add both exact active TODO section headings before diagnosing their contents.",
        "packet.open-finding": "Resolve, close, or reconcile the linked finding with packet status.",
        "packet.open-critical-finding": "Resolve the Critical finding before retaining release_candidate.",
        "packet.open-todo": "Complete, defer, or reconcile the linked TODO with packet status.",
        "packet.unlinked-open-work": "Link relevant work explicitly or reconcile the terminal packet status.",
        "packet.marker.unrepresentable": "Choose an active packet ID that does not contain a closing bracket.",
        "ledger.open-item-missing-marker": (
            "Add the exact [packet:ID] marker for the active packet."
        ),
        "ledger.open-item-invalid-marker": (
            "Use exact packet delimiters and a valid v2 packet ID."
        ),
        "ledger.open-item-malformed-record": (
            "Rewrite the line using the exact v2 active-ledger grammar."
        ),
        "ledger.open-item-packet-mismatch": (
            "Relink active work to the current packet or move it out of the active section."
        ),
        "ledger.closed-review-in-active-section": (
            "Move the closed finding to Recently Closed or an archive."
        ),
        "ledger.closed-todo-in-active-section": (
            "Move the closed TODO to Recently Closed or an archive."
        ),
    }
    return Finding(
        id=finding_id,
        severity=severity,
        message=messages[finding_id],
        path=path,
        line=line,
        evidence=evidence,
        remediation=remediations[finding_id],
    )


def _handoff_findings(
    context: DoctorContext,
    packet_id: str | None,
) -> list[Finding]:
    if context.state_result.state_version != 2:
        return []
    snapshot = context.state_result.snapshot
    if snapshot is None:
        return []
    current_handoff = snapshot.scalar("current_handoff")
    if current_handoff is None or not is_normalized_relative_posix_path(
        current_handoff.value
    ):
        return []

    path = current_handoff.value
    text = _read_control_document(context, path)
    if text is None:
        return []
    section = _v2_section_lines(text.splitlines(), HANDOFF_HEADING)
    if section is None:
        return [
            _finding(
                "handoff.structure.missing-marker",
                Severity.ERROR,
                path=path,
                line=None,
                evidence=f"missing exact section: {HANDOFF_HEADING}",
            )
        ]

    candidates = [
        entry for entry in section if entry[1].startswith(HANDOFF_PREFIX)
    ]
    if not candidates:
        return [
            _finding(
                "handoff.structure.missing-marker",
                Severity.ERROR,
                path=path,
                line=None,
                evidence=(
                    "no active-packet marker candidate in first "
                    "Session Identity section"
                ),
            )
        ]
    if len(candidates) > 1:
        return [
            _finding(
                "handoff.structure.duplicate-marker",
                Severity.ERROR,
                path=path,
                line=candidates[0][0],
                evidence=f"found {len(candidates)} active-packet marker candidates",
            )
        ]

    line_number, candidate = candidates[0]
    marker = _HANDOFF_MARKER.fullmatch(candidate)
    marker_id = marker.group(1) if marker is not None else None
    if marker_id is None or not is_valid_v2_packet_id(marker_id):
        return [
            _finding(
                "handoff.structure.invalid-marker",
                Severity.ERROR,
                path=path,
                line=line_number,
                evidence=f"invalid active-packet marker: {candidate}",
            )
        ]
    if (
        packet_id is not None
        and is_valid_v2_packet_id(packet_id)
        and marker_id != packet_id
    ):
        return [
            _finding(
                "handoff.packet-mismatch",
                Severity.ERROR,
                path=path,
                line=line_number,
                evidence=f"handoff packet {marker_id}; active packet {packet_id}",
            )
        ]
    return []


def _index_source_findings(context: DoctorContext) -> list[Finding]:
    if context.state_result.state_version != 2:
        return []
    text = _read_control_document(context, INDEX_PATH)
    if text is None:
        return []

    section = _v2_section_lines(text.splitlines(), INDEX_HEADING)
    candidates = (
        []
        if section is None
        else [
            entry
            for entry in section
            if entry[1].startswith(INDEX_SOURCE_PREFIX)
        ]
    )
    if len(candidates) == 1 and candidates[0][1] == INDEX_SOURCE_LINE:
        return []

    if section is None:
        evidence = f"missing exact section: {INDEX_HEADING}"
    elif not candidates:
        evidence = (
            "current-handoff source is missing from first Active Catalog section"
        )
    elif len(candidates) > 1:
        evidence = f"found {len(candidates)} current-handoff source candidates"
    else:
        evidence = f"noncanonical current-handoff source: {candidates[0][1]}"
    return [
        _finding(
            "index.current-handoff-source",
            Severity.WARNING,
            path=INDEX_PATH,
            line=candidates[0][0] if candidates else None,
            evidence=evidence,
        )
    ]


def _coherence_findings(
    items: list[_ActiveItem],
    *,
    path: str,
    status: str | None,
    todo: bool,
) -> list[Finding]:
    findings: list[Finding] = []
    for item in items:
        if item.linked:
            if (
                not todo
                and item.critical
                and status == "release_candidate"
            ):
                findings.append(
                    _finding(
                        "packet.open-critical-finding",
                        Severity.ERROR,
                        path=path,
                        line=item.line,
                        evidence="linked Critical finding remains active",
                    )
                )
                continue
            if status in COHERENCE_SENSITIVE_STATUSES | TERMINAL_STATUSES:
                findings.append(
                    _finding(
                        "packet.open-todo" if todo else "packet.open-finding",
                        (
                            Severity.ERROR
                            if status in TERMINAL_STATUSES
                            else Severity.WARNING
                        ),
                        path=path,
                        line=item.line,
                        evidence=f"linked active work remains at status {status}",
                    )
                )
        elif status in TERMINAL_STATUSES:
            findings.append(
                _finding(
                    "packet.unlinked-open-work",
                    Severity.WARNING,
                    path=path,
                    line=item.line,
                    evidence=f"unlinked active work remains at status {status}",
                )
            )
    return findings


def _v2_ledger_severity(status: str) -> Severity:
    return (
        Severity.ERROR
        if status in TERMINAL_STATUSES
        else Severity.WARNING
    )


def _v2_open_identity(
    record: _LedgerRecord,
    packet_id: str,
) -> tuple[str, str] | None:
    if record.marker_state == "missing":
        return (
            "ledger.open-item-missing-marker",
            "open record has no packet-looking marker",
        )
    if record.marker_state == "invalid":
        return (
            "ledger.open-item-invalid-marker",
            "open record has invalid packet delimiters or ID",
        )
    if not record.grammar_valid:
        return (
            "ledger.open-item-malformed-record",
            "open record violates exact token order or spacing",
        )
    if record.packet_id != packet_id:
        return (
            "ledger.open-item-packet-mismatch",
            f"record packet {record.packet_id}; active packet {packet_id}",
        )
    return None


def _v2_current_open_finding(
    record: _LedgerRecord,
    *,
    path: str,
    status: str,
    todo: bool,
) -> Finding | None:
    if (
        not todo
        and record.critical
        and status == "release_candidate"
    ):
        return _finding(
            "packet.open-critical-finding",
            Severity.ERROR,
            path=path,
            line=record.line,
            evidence="linked Critical finding remains active",
        )
    if status not in COHERENCE_SENSITIVE_STATUSES | TERMINAL_STATUSES:
        return None
    return _finding(
        "packet.open-todo" if todo else "packet.open-finding",
        (
            Severity.ERROR
            if status in TERMINAL_STATUSES
            else Severity.WARNING
        ),
        path=path,
        line=record.line,
        evidence=f"linked active work remains at status {status}",
    )


def _v2_closed_record_finding(
    record: _LedgerRecord,
    *,
    path: str,
    packet_id: str,
    status: str,
    todo: bool,
) -> Finding | None:
    if (
        todo
        and status == "in_progress"
        and record.grammar_valid
        and record.marker_state == "valid"
        and record.packet_id == packet_id
    ):
        return None
    return _finding(
        (
            "ledger.closed-todo-in-active-section"
            if todo
            else "ledger.closed-review-in-active-section"
        ),
        _v2_ledger_severity(status),
        path=path,
        line=record.line,
        evidence="closed record remains in an active section",
    )


def _v2_record_findings(
    records: list[_LedgerRecord],
    *,
    path: str,
    packet_id: str | None,
    status: str | None,
    todo: bool,
) -> list[Finding]:
    if (
        packet_id is None
        or not is_valid_v2_packet_id(packet_id)
        or status not in ACTIVE_PACKET_STATUSES
    ):
        return []

    findings: list[Finding] = []
    for record in records:
        if record.closed:
            finding = _v2_closed_record_finding(
                record,
                path=path,
                packet_id=packet_id,
                status=status,
                todo=todo,
            )
        else:
            identity = _v2_open_identity(record, packet_id)
            if identity is None:
                finding = _v2_current_open_finding(
                    record,
                    path=path,
                    status=status,
                    todo=todo,
                )
            else:
                finding_id, evidence = identity
                finding = _finding(
                    finding_id,
                    _v2_ledger_severity(status),
                    path=path,
                    line=record.line,
                    evidence=evidence,
                )
        if finding is not None:
            findings.append(finding)
    return findings


def _v2_ledger_findings(
    context: DoctorContext,
    packet_id: str | None,
    status: str | None,
) -> list[Finding]:
    findings: list[Finding] = []
    review_text = _read_optional_document(context, REVIEW_PATH)
    todo_text = _read_optional_document(context, TODO_PATH)

    if review_text is not None:
        review_records = _parse_v2_review_records(review_text)
        if review_records is None:
            findings.append(
                _finding(
                    "review.structure.missing-section",
                    Severity.WARNING,
                    path=REVIEW_PATH,
                    line=None,
                    evidence=f"missing exact section: {REVIEW_HEADING}",
                )
            )
        else:
            findings.extend(
                _v2_record_findings(
                    review_records,
                    path=REVIEW_PATH,
                    packet_id=packet_id,
                    status=status,
                    todo=False,
                )
            )

    if todo_text is not None:
        todo_records = _parse_v2_todo_records(todo_text)
        if todo_records is None:
            findings.append(
                _finding(
                    "todo.structure.missing-section",
                    Severity.WARNING,
                    path=TODO_PATH,
                    line=None,
                    evidence="missing one or more exact active TODO sections",
                )
            )
        else:
            findings.extend(
                _v2_record_findings(
                    todo_records,
                    path=TODO_PATH,
                    packet_id=packet_id,
                    status=status,
                    todo=True,
                )
            )
    return findings


class ReviewStateCheck:
    name = "review_state"

    def run(self, context: DoctorContext) -> tuple[Finding, ...]:
        snapshot = context.state_result.snapshot
        if snapshot is None:
            return ()

        packet_id_scalar = snapshot.active_packet.get("id")
        status_scalar = snapshot.active_packet.get("status")
        packet_id = (
            packet_id_scalar.value
            if packet_id_scalar is not None and packet_id_scalar.value.strip()
            else None
        )
        status = (
            status_scalar.value
            if status_scalar is not None
            and status_scalar.value in ACTIVE_PACKET_STATUSES
            else None
        )
        findings: list[Finding] = []
        if packet_id is not None and "]" in packet_id:
            findings.append(
                _finding(
                    "packet.marker.unrepresentable",
                    Severity.WARNING,
                    path=STATE_PATH,
                    line=packet_id_scalar.line if packet_id_scalar is not None else None,
                    evidence=f"active_packet.id contains ]: {packet_id}",
                )
            )

        findings.extend(_index_source_findings(context))
        findings.extend(_handoff_findings(context, packet_id))

        if context.state_result.state_version == 2:
            findings.extend(
                _v2_ledger_findings(
                    context,
                    packet_id,
                    status,
                )
            )
            return tuple(findings)

        review_text = _read_optional_document(context, REVIEW_PATH)
        todo_text = _read_optional_document(context, TODO_PATH)
        if review_text is not None:
            review_items = _review_items(review_text, packet_id)
            if review_items is None:
                findings.append(
                    _finding(
                        "review.structure.missing-section",
                        Severity.WARNING,
                        path=REVIEW_PATH,
                        line=None,
                        evidence=f"missing exact section: {REVIEW_HEADING}",
                    )
                )
            elif packet_id is not None:
                findings.extend(
                    _coherence_findings(
                        review_items,
                        path=REVIEW_PATH,
                        status=status,
                        todo=False,
                    )
                )

        if todo_text is not None:
            todo_items = _todo_items(todo_text, packet_id)
            if todo_items is None:
                findings.append(
                    _finding(
                        "todo.structure.missing-section",
                        Severity.WARNING,
                        path=TODO_PATH,
                        line=None,
                        evidence="missing one or more exact active TODO sections",
                    )
                )
            elif packet_id is not None:
                findings.extend(
                    _coherence_findings(
                        todo_items,
                        path=TODO_PATH,
                        status=status,
                        todo=True,
                    )
                )
        return tuple(findings)
