from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from .diagnostics import (
    DiagnosticError,
    DoctorPolicy,
    DoctorReport,
    Finding,
    Severity,
)
from .project_view import ProjectView
from .state_contract import StateContractResult, StateIssue, inspect_state


STATE_PATH = "sdad-state.yaml"
CHECK_NAMES = (
    "state_schema",
    "path_integrity",
    "packet_coherence",
    "owner_gates",
    "review_state",
)

ALLOWED_FINDING_IDS = frozenset(
    {
        "state.missing",
        "state.too-large",
        "state.encoding.invalid",
        "state.syntax.unsupported",
        "state.schema.duplicate-key",
        "state.schema.missing-key",
        "state.schema.unknown-key",
        "state.schema.wrong-kind",
        "state.schema.missing-version",
        "state.schema.unsupported-version",
        "state.schema.unsupported-value",
        "state.packet.missing-field",
        "state.packet.blank-field",
        "state.collection.malformed-entry",
        "state.updated.missing",
        "state.updated.placeholder",
        "state.updated.invalid",
        "state.updated.stale",
        "state.updated.future",
        "path.invalid",
        "path.outside-root",
        "path.missing",
        "path.not-file",
        "path.unreadable",
        "path.encoding.invalid",
        "path.too-large",
        "path.duplicate-route",
        "validation.empty",
        "validation.missing-command",
        "validation.blank-command",
        "validation.missing-proves",
        "validation.blank-proves",
        "validation.placeholder",
        "validation.unknown-key",
        "gate.required",
        "gate.q5-review",
        "gate.pending-after-acceptance",
        "review.structure.missing-section",
        "todo.structure.missing-section",
        "packet.open-finding",
        "packet.open-critical-finding",
        "packet.open-todo",
        "packet.unlinked-open-work",
        "packet.marker.unrepresentable",
    }
)

CONDITIONAL_SEVERITY_IDS = frozenset(
    {
        "validation.empty",
        "validation.missing-command",
        "validation.blank-command",
        "validation.missing-proves",
        "validation.blank-proves",
        "validation.placeholder",
        "gate.pending-after-acceptance",
        "packet.open-finding",
        "packet.open-todo",
    }
)

WARNING_ONLY_FINDING_IDS = frozenset(
    {
        "state.schema.unknown-key",
        "state.schema.missing-version",
        "state.updated.missing",
        "state.updated.placeholder",
        "state.updated.invalid",
        "state.updated.stale",
        "state.updated.future",
        "path.too-large",
        "path.duplicate-route",
        "validation.unknown-key",
        "gate.q5-review",
        "review.structure.missing-section",
        "todo.structure.missing-section",
        "packet.unlinked-open-work",
        "packet.marker.unrepresentable",
    }
)

FIXED_FINDING_SEVERITIES = {
    finding_id: (
        Severity.WARNING
        if finding_id in WARNING_ONLY_FINDING_IDS
        else Severity.ERROR
    )
    for finding_id in ALLOWED_FINDING_IDS - CONDITIONAL_SEVERITY_IDS
}


@dataclass(frozen=True)
class DoctorContext:
    view: ProjectView
    policy: DoctorPolicy
    state_result: StateContractResult


class DiagnosticCheck(Protocol):
    name: str

    def run(self, context: DoctorContext) -> tuple[Finding, ...]: ...


def _state_input_result(
    issue_id: str,
    message: str,
    evidence: str,
) -> StateContractResult:
    return StateContractResult(
        snapshot=None,
        issues=(
            StateIssue(
                id=issue_id,
                severity="error",
                message=message,
                evidence=evidence,
                line=None,
            ),
        ),
    )


def _read_state(view: ProjectView, policy: DoctorPolicy) -> StateContractResult:
    try:
        read_result = view.read_bytes(STATE_PATH, policy.max_state_bytes)
    except OSError as exc:
        raise DiagnosticError(
            "unreadable_state",
            "The required sdad-state.yaml file could not be read.",
        ) from exc

    if read_result.status in {"missing", "not_file"}:
        return _state_input_result(
            "state.missing",
            "The project does not have a readable regular sdad-state.yaml file.",
            f"required state status: {read_result.status}",
        )
    if read_result.status == "too_large":
        return _state_input_result(
            "state.too-large",
            "sdad-state.yaml exceeds the configured state size limit.",
            f"limit: {policy.max_state_bytes} bytes",
        )
    if read_result.status != "ok":
        raise DiagnosticError(
            "unreadable_state",
            "The required sdad-state.yaml file could not be read.",
        )
    if read_result.data is None:
        raise DiagnosticError(
            "internal_error",
            "The project view returned no bytes for readable sdad-state.yaml.",
        )

    try:
        state_text = read_result.data.decode("utf-8")
    except UnicodeDecodeError:
        return _state_input_result(
            "state.encoding.invalid",
            "sdad-state.yaml is not valid UTF-8 text.",
            "UTF-8 decoding failed",
        )
    return inspect_state(state_text)


def _root_text(view: ProjectView) -> str:
    return str(view.root).replace("\\", "/")


class DiagnosticEngine:
    def diagnose(self, view: ProjectView, policy: DoctorPolicy) -> DoctorReport:
        state_result = _read_state(view, policy)
        context = DoctorContext(view=view, policy=policy, state_result=state_result)

        from .checks import BUILT_IN_CHECKS

        check_names = tuple(check.name for check in BUILT_IN_CHECKS)
        if check_names != CHECK_NAMES:
            raise DiagnosticError(
                "internal_error",
                "The built-in diagnostic check sequence does not match schema version 1.",
            )

        findings_with_order: list[tuple[int, Finding]] = []
        checks_run: list[str] = []
        checks_skipped: list[str] = []
        for check_index, check in enumerate(BUILT_IN_CHECKS):
            if check.name != "state_schema" and state_result.snapshot is None:
                checks_skipped.append(check.name)
                continue
            try:
                check_findings = check.run(context)
            except DiagnosticError:
                raise
            except Exception as exc:
                raise DiagnosticError(
                    "internal_error",
                    f"Diagnostic check {check.name} failed.",
                ) from exc
            checks_run.append(check.name)
            findings_with_order.extend(
                (check_index, finding) for finding in check_findings
            )

        unexpected_ids = sorted(
            {
                finding.id
                for _, finding in findings_with_order
                if finding.id not in ALLOWED_FINDING_IDS
            }
        )
        if unexpected_ids:
            raise DiagnosticError(
                "internal_error",
                "A diagnostic check emitted unsupported finding IDs: "
                + ", ".join(unexpected_ids),
            )

        severity_breaches = sorted(
            {
                finding.id
                for _, finding in findings_with_order
                if finding.id in FIXED_FINDING_SEVERITIES
                and finding.severity is not FIXED_FINDING_SEVERITIES[finding.id]
            }
        )
        if severity_breaches:
            raise DiagnosticError(
                "internal_error",
                "A diagnostic check emitted invalid fixed severities for: "
                + ", ".join(severity_breaches),
            )

        findings_with_order.sort(
            key=lambda item: (
                item[0],
                item[1].path or "",
                item[1].line or 0,
                item[1].id,
            )
        )
        findings: list[Finding] = []
        seen_occurrences: set[tuple[str, str | None, int | None]] = set()
        for _, finding in findings_with_order:
            occurrence = (finding.id, finding.path, finding.line)
            if occurrence in seen_occurrences:
                continue
            seen_occurrences.add(occurrence)
            findings.append(finding)

        frozen_findings = tuple(findings)
        return DoctorReport(
            root=_root_text(view),
            findings=frozen_findings,
            checks_run=tuple(checks_run),
            checks_skipped=tuple(checks_skipped),
            error_count=sum(
                finding.severity is Severity.ERROR for finding in frozen_findings
            ),
            warning_count=sum(
                finding.severity is Severity.WARNING for finding in frozen_findings
            ),
        )
