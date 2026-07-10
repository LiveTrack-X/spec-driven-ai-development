from __future__ import annotations

import re
from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity
from ..state_contract import ACTIVE_PACKET_STATUSES

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
AUTONOMY_FOUR_GATE_STATUSES = frozenset(
    {
        "not_started",
        "in_progress",
        "ai_complete",
        "software_verified",
        "tester_ready",
        "hardware_evidence_received",
        "hardware_verified",
        "blocked",
    }
)

_APPROVED_SEPARATOR_PATTERN = re.compile(r"[ _-]+")
_APPROVED_SEPARATOR_REGEX = r"[ _-]+"
_TOKEN_BOUNDARY = r"[^\W_]"


def _keyword_pattern(keyword: str) -> re.Pattern[str] | None:
    terms = tuple(
        term
        for term in _APPROVED_SEPARATOR_PATTERN.split(keyword.casefold().strip())
        if term
    )
    if not terms:
        return None
    if terms == ("real", "user", "data"):
        phrase = (
            rf"real(?:{_APPROVED_SEPARATOR_REGEX}user)?"
            rf"{_APPROVED_SEPARATOR_REGEX}data"
        )
    else:
        phrase = _APPROVED_SEPARATOR_REGEX.join(re.escape(term) for term in terms)
    return re.compile(
        rf"(?<!{_TOKEN_BOUNDARY}){phrase}(?!{_TOKEN_BOUNDARY})"
    )


def _matches_q5(objective: str, q5_keywords: frozenset[str]) -> str | None:
    normalized_objective = objective.casefold()
    for keyword in sorted(q5_keywords):
        pattern = _keyword_pattern(keyword)
        if pattern is not None and pattern.search(normalized_objective):
            return keyword
    return None


def _finding(
    finding_id: str,
    severity: Severity,
    line: int | None,
    evidence: str,
) -> Finding:
    messages = {
        "gate.required": "Autonomy level 4 requires a current owner gate in this status.",
        "gate.q5-review": "The packet objective contains a Q5-like term but has no owner gate.",
        "gate.pending-after-acceptance": "A terminal packet status still lists a current owner gate.",
    }
    remediations = {
        "gate.required": "Name the owner decision that can stop this active packet.",
        "gate.q5-review": "Have the owner review whether an explicit gate is required.",
        "gate.pending-after-acceptance": "Reconcile the packet status with its remaining owner gates.",
    }
    return Finding(
        id=finding_id,
        severity=severity,
        message=messages[finding_id],
        path=STATE_PATH,
        line=line,
        evidence=evidence,
        remediation=remediations[finding_id],
    )


class OwnerGatesCheck:
    name = "owner_gates"

    def run(self, context: DoctorContext) -> tuple[Finding, ...]:
        snapshot = context.state_result.snapshot
        if snapshot is None:
            return ()

        owner_gates_invalid = any(
            (
                issue.id == "state.schema.missing-key"
                and issue.evidence == "owner_gates"
            )
            or (
                issue.id == "state.schema.wrong-kind"
                and "State key owner_gates " in issue.message
            )
            or (
                issue.id == "state.collection.malformed-entry"
                and issue.message.startswith("owner_gates entries ")
            )
            for issue in context.state_result.issues
        )
        if owner_gates_invalid:
            return ()

        status_scalar = snapshot.active_packet.get("status")
        status = (
            status_scalar.value
            if status_scalar is not None
            and status_scalar.value in ACTIVE_PACKET_STATUSES
            else None
        )
        autonomy = snapshot.scalar("autonomy")
        objective = snapshot.active_packet.get("objective")
        gate_values = tuple(
            gate.value for gate in snapshot.owner_gates if gate.value.strip()
        )
        findings: list[Finding] = []

        if (
            autonomy is not None
            and autonomy.value == "4"
            and status in AUTONOMY_FOUR_GATE_STATUSES
            and not gate_values
        ):
            findings.append(
                _finding(
                    "gate.required",
                    Severity.ERROR,
                    status_scalar.line if status_scalar is not None else None,
                    f"autonomy 4 with status {status} and no owner_gates",
                )
            )

        if gate_values and status in {"owner_accepted", "production_ready"}:
            findings.append(
                _finding(
                    "gate.pending-after-acceptance",
                    (
                        Severity.WARNING
                        if status == "owner_accepted"
                        else Severity.ERROR
                    ),
                    status_scalar.line if status_scalar is not None else None,
                    f"{status} with owner_gates: {', '.join(gate_values)}",
                )
            )

        if not gate_values and objective is not None and objective.value.strip():
            matched_keyword = _matches_q5(
                objective.value,
                context.policy.q5_keywords,
            )
            if matched_keyword is not None:
                findings.append(
                    _finding(
                        "gate.q5-review",
                        Severity.WARNING,
                        objective.line,
                        f"objective matched injected Q5 term: {matched_keyword}",
                    )
                )
        return tuple(findings)
