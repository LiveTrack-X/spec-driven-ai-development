from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity
from ..state_contract import ACTIVE_PACKET_STATUSES

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
REVIEW_PATH = "review-findings.md"
TODO_PATH = "docs/TODO-Open-Items.md"
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


@dataclass(frozen=True)
class _ActiveItem:
    line: int
    linked: bool
    critical: bool = False


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


def _finding(
    finding_id: str,
    severity: Severity,
    *,
    path: str,
    line: int | None,
    evidence: str,
) -> Finding:
    messages = {
        "review.structure.missing-section": "The review document is missing its exact active section.",
        "todo.structure.missing-section": "The TODO document is missing a required exact section.",
        "packet.open-finding": "An active review finding remains for the current packet.",
        "packet.open-critical-finding": "A Critical current-packet finding remains at release candidate.",
        "packet.open-todo": "An unchecked TODO remains for the current packet.",
        "packet.unlinked-open-work": "Terminal packet state coexists with active unlinked work.",
        "packet.marker.unrepresentable": "The active packet ID cannot be represented by the marker grammar.",
    }
    remediations = {
        "review.structure.missing-section": "Add the exact ## Active Findings section before diagnosing its contents.",
        "todo.structure.missing-section": "Add both exact active TODO section headings before diagnosing their contents.",
        "packet.open-finding": "Resolve, close, or reconcile the linked finding with packet status.",
        "packet.open-critical-finding": "Resolve the Critical finding before retaining release_candidate.",
        "packet.open-todo": "Complete, defer, or reconcile the linked TODO with packet status.",
        "packet.unlinked-open-work": "Link relevant work explicitly or reconcile the terminal packet status.",
        "packet.marker.unrepresentable": "Choose an active packet ID that does not contain a closing bracket.",
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
