from __future__ import annotations

from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity
from ..state_contract import (
    ACTIVE_PACKET_STATUSES,
    ValidationEntry,
    is_valid_v2_packet_id,
)

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
VALIDATION_REQUIRED_STATUSES = frozenset(
    {
        "software_verified",
        "tester_ready",
        "hardware_evidence_received",
        "hardware_verified",
        "owner_accepted",
        "release_candidate",
        "production_ready",
    }
)

_MESSAGES = {
    "validation.empty": "The packet has no validation evidence contract.",
    "validation.missing-command": "A validation entry has no command.",
    "validation.blank-command": "A validation command is blank.",
    "validation.missing-proves": "A validation entry does not state what it proves.",
    "validation.blank-proves": "A validation evidence claim is blank.",
    "validation.placeholder": "A validation field still contains template placeholder text.",
    "validation.unknown-key": "A validation entry contains an unknown key.",
}

_REMEDIATIONS = {
    "validation.empty": "Add a short runnable command and the claim it supports.",
    "validation.missing-command": "Add the runnable repository-root command.",
    "validation.blank-command": "Replace the blank value with a runnable command.",
    "validation.missing-proves": "Add the bounded claim supported by the command.",
    "validation.blank-proves": "Replace the blank value with a bounded evidence claim.",
    "validation.placeholder": "Replace template text with project-specific evidence.",
    "validation.unknown-key": "Remove the key or use only command and proves.",
}


def _severity(status: str | None) -> Severity:
    return (
        Severity.ERROR
        if status in VALIDATION_REQUIRED_STATUSES
        else Severity.WARNING
    )


def _finding(
    finding_id: str,
    *,
    severity: Severity,
    line: int | None,
    evidence: str,
    message: str | None = None,
) -> Finding:
    return Finding(
        id=finding_id,
        severity=severity,
        message=message or _MESSAGES[finding_id],
        path=STATE_PATH,
        line=line,
        evidence=evidence,
        remediation=_REMEDIATIONS[finding_id],
    )


def _is_placeholder(value: str) -> bool:
    normalized = value.strip().casefold()
    return (
        normalized.startswith("replace with")
        or normalized in {"placeholder", "tbd", "todo", "replace me"}
        or (normalized.startswith("<") and normalized.endswith(">"))
    )


def _entry_for_line(
    entries: tuple[ValidationEntry, ...],
    line: int,
) -> int | None:
    for index, entry in enumerate(entries):
        next_line = entries[index + 1].line if index + 1 < len(entries) else None
        if line >= entry.line and (next_line is None or line < next_line):
            return index
    return None


class PacketCoherenceCheck:
    name = "packet_coherence"

    def run(self, context: DoctorContext) -> tuple[Finding, ...]:
        findings = [
            _finding(
                issue.id,
                severity=Severity.WARNING,
                line=issue.line,
                evidence=issue.evidence,
                message=issue.message,
            )
            for issue in context.state_result.issues
            if issue.id == "validation.unknown-key"
        ]
        snapshot = context.state_result.snapshot
        if snapshot is None:
            return tuple(findings)

        status_scalar = snapshot.active_packet.get("status")
        status = (
            status_scalar.value
            if status_scalar is not None
            and status_scalar.value in ACTIVE_PACKET_STATUSES
            else None
        )
        if status is None:
            return tuple(findings)
        conditional_severity = _severity(status)

        validation_container_invalid = False
        malformed_whole_entries = False
        for issue in context.state_result.issues:
            if issue.id == "state.schema.missing-key" and issue.evidence == "validation":
                validation_container_invalid = True
            elif (
                issue.id == "state.schema.wrong-kind"
                and "State key validation " in issue.message
            ):
                validation_container_invalid = True
            elif (
                issue.id == "state.collection.malformed-entry"
                and issue.message == "validation entries must be mappings"
            ):
                malformed_whole_entries = True

        if context.state_result.state_version == 2:
            packet = snapshot.active_packet.get("id")
            owner = snapshot.scalar("validation_for")
            if (
                packet is not None
                and owner is not None
                and is_valid_v2_packet_id(packet.value)
                and is_valid_v2_packet_id(owner.value)
                and packet.value != owner.value
            ):
                findings.append(
                    Finding(
                        id="validation.packet-mismatch",
                        severity=Severity.ERROR,
                        message=(
                            "The validation contract belongs to a different packet."
                        ),
                        path=STATE_PATH,
                        line=owner.line,
                        evidence=(
                            f"validation_for {owner.value}; "
                            f"active packet {packet.value}"
                        ),
                        remediation=(
                            "Review every validation command and proves claim, then "
                            "set validation_for to the active packet ID."
                        ),
                    )
                )

        if not snapshot.validation:
            if not validation_container_invalid and not malformed_whole_entries:
                findings.append(
                    _finding(
                        "validation.empty",
                        severity=conditional_severity,
                        line=None,
                        evidence="validation is an empty list",
                    )
                )
            return tuple(findings)
        if validation_container_invalid:
            return tuple(findings)

        invalid_fields: dict[int, set[str]] = {}
        for issue in context.state_result.issues:
            field: str | None = None
            if (
                issue.id == "state.schema.duplicate-key"
                and issue.message.startswith("Duplicate validation entry key: ")
            ):
                field = issue.evidence
            elif (
                issue.id == "state.collection.malformed-entry"
                and issue.message.startswith("validation ")
                and issue.message.endswith(" must be a scalar")
            ):
                field = issue.message[len("validation ") : -len(" must be a scalar")]
            if field is None or issue.line is None:
                continue
            entry_index = _entry_for_line(snapshot.validation, issue.line)
            if entry_index is not None:
                invalid_fields.setdefault(entry_index, set()).add(field)

        for index, entry in enumerate(snapshot.validation):
            suppressed = invalid_fields.get(index, set())
            for field, missing_id, blank_id in (
                ("command", "validation.missing-command", "validation.blank-command"),
                ("proves", "validation.missing-proves", "validation.blank-proves"),
            ):
                if field in suppressed:
                    continue
                located = entry.fields.get(field)
                if located is None:
                    findings.append(
                        _finding(
                            missing_id,
                            severity=conditional_severity,
                            line=entry.line,
                            evidence=f"validation entry on line {entry.line} has no {field}",
                        )
                    )
                    continue
                if not located.value.strip():
                    findings.append(
                        _finding(
                            blank_id,
                            severity=conditional_severity,
                            line=located.line,
                            evidence=f"validation {field} is blank",
                        )
                    )
                    continue
                if _is_placeholder(located.value):
                    findings.append(
                        _finding(
                            "validation.placeholder",
                            severity=conditional_severity,
                            line=located.line,
                            evidence=f"validation {field}: {located.value}",
                        )
                    )
        return tuple(findings)
