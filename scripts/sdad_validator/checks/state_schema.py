from __future__ import annotations

import re
from datetime import date
from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
_DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_DATE_PLACEHOLDERS = frozenset(
    {
        "yyyy-mm-dd",
        "placeholder",
        "replace me",
        "replace-me",
        "tbd",
        "todo",
        "unknown",
    }
)

_REMEDIATIONS = {
    "state.missing": "Create the root-level sdad-state.yaml for this stateful workflow.",
    "state.too-large": "Reduce sdad-state.yaml to the supported canonical state subset.",
    "state.encoding.invalid": "Save sdad-state.yaml as valid UTF-8 text.",
    "state.syntax.unsupported": "Rewrite the state using the supported canonical YAML subset.",
    "state.schema.duplicate-key": "Keep one authoritative value for the duplicated key.",
    "state.schema.missing-key": "Add the required state key with its intended value.",
    "state.schema.unknown-key": "Remove the key or move project-specific data to a routed document.",
    "state.schema.wrong-kind": "Use the documented scalar, mapping, or list shape.",
    "state.schema.missing-version": "Declare version: 1 in sdad-state.yaml.",
    "state.schema.unsupported-version": "Use the supported version 1 state contract.",
    "state.schema.unsupported-value": "Choose one of the documented state values.",
    "state.packet.missing-field": "Add the required active_packet field.",
    "state.packet.blank-field": "Set the active_packet field to a non-blank value.",
    "state.collection.malformed-entry": "Use the documented collection-entry shape.",
}


def _issue_finding(issue_id: str, severity: str, message: str, evidence: str, line: int | None) -> Finding:
    return Finding(
        id=issue_id,
        severity=Severity(severity),
        message=message,
        path=STATE_PATH,
        line=line,
        evidence=evidence,
        remediation=_REMEDIATIONS[issue_id],
    )


def _freshness_finding(
    finding_id: str,
    message: str,
    evidence: str,
    line: int | None,
) -> Finding:
    remediations = {
        "state.updated.missing": "Record the date when the active packet state was reconciled.",
        "state.updated.placeholder": "Replace the placeholder with an ISO calendar date.",
        "state.updated.invalid": "Use a valid ISO calendar date in YYYY-MM-DD form.",
        "state.updated.stale": "Reconcile the active packet and record the current date.",
        "state.updated.future": "Correct the declared date or reconcile clock assumptions.",
    }
    return Finding(
        id=finding_id,
        severity=Severity.WARNING,
        message=message,
        path=STATE_PATH,
        line=line,
        evidence=evidence,
        remediation=remediations[finding_id],
    )


class StateSchemaCheck:
    name = "state_schema"

    def run(self, context: DoctorContext) -> tuple[Finding, ...]:
        findings = [
            _issue_finding(
                issue.id,
                issue.severity,
                issue.message,
                issue.evidence,
                issue.line,
            )
            for issue in context.state_result.issues
            if issue.id.startswith("state.")
        ]
        snapshot = context.state_result.snapshot
        if snapshot is None:
            return tuple(findings)

        updated = snapshot.scalar("updated")
        if updated is None:
            updated_has_invalid_shape = any(
                issue.id == "state.schema.wrong-kind"
                and issue.message == "State key updated must be a scalar"
                for issue in context.state_result.issues
            )
            if updated_has_invalid_shape:
                return tuple(findings)
            findings.append(
                _freshness_finding(
                    "state.updated.missing",
                    "The state does not declare when it was last reconciled.",
                    "updated is absent",
                    None,
                )
            )
            return tuple(findings)

        declared_text = updated.value.strip()
        if declared_text.casefold() in _DATE_PLACEHOLDERS:
            findings.append(
                _freshness_finding(
                    "state.updated.placeholder",
                    "The state update date is still a placeholder.",
                    updated.value,
                    updated.line,
                )
            )
            return tuple(findings)
        if not _DATE_PATTERN.fullmatch(declared_text):
            findings.append(
                _freshness_finding(
                    "state.updated.invalid",
                    "The state update date is not a valid ISO calendar date.",
                    updated.value,
                    updated.line,
                )
            )
            return tuple(findings)
        try:
            declared_date = date.fromisoformat(declared_text)
        except ValueError:
            findings.append(
                _freshness_finding(
                    "state.updated.invalid",
                    "The state update date is not a valid ISO calendar date.",
                    updated.value,
                    updated.line,
                )
            )
            return tuple(findings)

        age_days = (context.policy.today - declared_date).days
        if age_days > context.policy.stale_after_days:
            findings.append(
                _freshness_finding(
                    "state.updated.stale",
                    "The declared state date is older than the freshness threshold.",
                    f"{declared_text} is {age_days} days old",
                    updated.line,
                )
            )
        elif age_days < -1:
            findings.append(
                _freshness_finding(
                    "state.updated.future",
                    "The declared state date is more than one day in the future.",
                    f"{declared_text} is {-age_days} days in the future",
                    updated.line,
                )
            )
        return tuple(findings)
