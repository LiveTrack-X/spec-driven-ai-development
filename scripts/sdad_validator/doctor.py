from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from .diagnostics import (
    DiagnosticError,
    DoctorPolicy,
    DoctorReport,
    Finding,
    Severity,
)
from .project_view import PathInspection, ProjectView, ReadResult
from .state_contract import (
    ACTIVE_PACKET_STATUSES,
    StateContractResult,
    StateIssue,
    inspect_state,
)


STATE_PATH = "sdad-state.yaml"
CHECK_NAMES = (
    "state_schema",
    "path_integrity",
    "packet_coherence",
    "owner_gates",
    "review_state",
)

STATE_V1_FINDING_IDS = frozenset(
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
STATE_V2_ONLY_FINDING_IDS = frozenset(
    {"handoff.path.too-large", "validation.packet-mismatch"}
)
ALLOWED_FINDING_IDS_BY_STATE_VERSION = {
    1: STATE_V1_FINDING_IDS,
    2: STATE_V1_FINDING_IDS | STATE_V2_ONLY_FINDING_IDS,
}
ALLOWED_FINDING_IDS = STATE_V1_FINDING_IDS


def _allowed_finding_ids(state_version: int | None) -> frozenset[str]:
    return ALLOWED_FINDING_IDS_BY_STATE_VERSION.get(
        state_version,
        STATE_V1_FINDING_IDS,
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

VALIDATION_CONDITIONAL_IDS = frozenset(
    finding_id
    for finding_id in CONDITIONAL_SEVERITY_IDS
    if finding_id.startswith("validation.")
)
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
    for finding_id in (
        STATE_V1_FINDING_IDS | STATE_V2_ONLY_FINDING_IDS
    ) - CONDITIONAL_SEVERITY_IDS
}


@dataclass(frozen=True)
class DoctorContext:
    view: ProjectView
    policy: DoctorPolicy
    state_result: StateContractResult


class DiagnosticCheck(Protocol):
    name: str

    def run(self, context: DoctorContext) -> tuple[Finding, ...]: ...


class _CachedProjectView:
    def __init__(self, view: ProjectView) -> None:
        self._view = view
        self._inspections: dict[str, PathInspection] = {}
        self._reads: dict[str, tuple[int, ReadResult]] = {}

    @property
    def root(self) -> Path:
        return self._view.root

    def inspect(self, relative_path: str) -> PathInspection:
        if relative_path not in self._inspections:
            try:
                inspection = self._view.inspect(relative_path)
            except OSError:
                inspection = PathInspection("unreadable", None)
            self._inspections[relative_path] = inspection
        return self._inspections[relative_path]

    def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult:
        if max_bytes < 0:
            raise ValueError("max_bytes must be non-negative")
        cached = self._reads.get(relative_path)
        if cached is not None:
            cached_limit, cached_result = cached
            if cached_result.status == "ok":
                if cached_result.data is None:
                    raise DiagnosticError(
                        "internal_error",
                        "A cached readable document has no bytes.",
                    )
                if len(cached_result.data) > max_bytes:
                    return ReadResult("too_large", None)
                return cached_result
            if cached_result.status != "too_large":
                return cached_result
            if max_bytes <= cached_limit:
                return cached_result

        inspection = self.inspect(relative_path)
        if inspection.status != "ok":
            result = ReadResult(inspection.status, None)
        else:
            try:
                result = self._view.read_bytes(relative_path, max_bytes)
            except OSError:
                result = ReadResult("unreadable", None)
        self._reads[relative_path] = (max_bytes, result)
        return result


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


def _usable_packet_status(state_result: StateContractResult) -> str | None:
    snapshot = state_result.snapshot
    if snapshot is None:
        return None
    located_status = snapshot.active_packet.get("status")
    if located_status is None or located_status.value not in ACTIVE_PACKET_STATUSES:
        return None
    return located_status.value


def _conditional_severity(
    finding_id: str,
    status: str | None,
) -> Severity | None:
    if status is None:
        return None
    if finding_id in VALIDATION_CONDITIONAL_IDS:
        return (
            Severity.ERROR
            if status in VALIDATION_REQUIRED_STATUSES
            else Severity.WARNING
        )
    if finding_id == "gate.pending-after-acceptance":
        if status == "owner_accepted":
            return Severity.WARNING
        if status == "production_ready":
            return Severity.ERROR
        return None
    if finding_id in {"packet.open-finding", "packet.open-todo"}:
        if status in COHERENCE_SENSITIVE_STATUSES:
            return Severity.WARNING
        if status in TERMINAL_STATUSES:
            return Severity.ERROR
    return None


class DiagnosticEngine:
    def diagnose(self, view: ProjectView, policy: DoctorPolicy) -> DoctorReport:
        diagnostic_view = _CachedProjectView(view)
        state_result = _read_state(diagnostic_view, policy)
        try:
            return self._diagnose_after_state_read(
                diagnostic_view,
                policy,
                state_result,
            )
        except DiagnosticError as exc:
            if exc.state_version == state_result.state_version:
                raise
            raise DiagnosticError(
                exc.kind,
                str(exc),
                state_version=state_result.state_version,
            ) from exc
        except Exception as exc:
            raise DiagnosticError(
                "internal_error",
                "Diagnostic engine failed.",
                state_version=state_result.state_version,
            ) from exc

    def _diagnose_after_state_read(
        self,
        view: _CachedProjectView,
        policy: DoctorPolicy,
        state_result: StateContractResult,
    ) -> DoctorReport:
        context = DoctorContext(
            view=view,
            policy=policy,
            state_result=state_result,
        )

        from .checks import BUILT_IN_CHECKS

        check_names = tuple(check.name for check in BUILT_IN_CHECKS)
        if check_names != CHECK_NAMES:
            raise DiagnosticError(
                "internal_error",
                "The built-in diagnostic check sequence does not match schema version 1.",
                state_version=state_result.state_version,
            )

        findings_with_order: list[tuple[int, Finding]] = []
        checks_run: list[str] = []
        checks_skipped: list[str] = []
        for check_index, check in enumerate(BUILT_IN_CHECKS):
            if check.name != "state_schema" and (
                state_result.snapshot is None
                or state_result.state_version is None
            ):
                checks_skipped.append(check.name)
                continue
            try:
                check_findings = check.run(context)
            except DiagnosticError as exc:
                raise DiagnosticError(
                    exc.kind,
                    str(exc),
                    state_version=state_result.state_version,
                ) from exc
            except Exception as exc:
                raise DiagnosticError(
                    "internal_error",
                    f"Diagnostic check {check.name} failed.",
                    state_version=state_result.state_version,
                ) from exc
            checks_run.append(check.name)
            findings_with_order.extend(
                (check_index, finding) for finding in check_findings
            )

        allowed_finding_ids = _allowed_finding_ids(state_result.state_version)
        unexpected_ids = sorted(
            {
                finding.id
                for _, finding in findings_with_order
                if finding.id not in allowed_finding_ids
            }
        )
        if unexpected_ids:
            raise DiagnosticError(
                "internal_error",
                "A diagnostic check emitted unsupported finding IDs: "
                + ", ".join(unexpected_ids),
                state_version=state_result.state_version,
            )

        non_enum_severities = sorted(
            {
                finding.id
                for _, finding in findings_with_order
                if finding.severity is not Severity.ERROR
                and finding.severity is not Severity.WARNING
            }
        )
        if non_enum_severities:
            raise DiagnosticError(
                "internal_error",
                "A diagnostic check emitted non-enum severities for: "
                + ", ".join(non_enum_severities),
                state_version=state_result.state_version,
            )

        packet_status = _usable_packet_status(state_result)
        conditional_breaches = sorted(
            {
                finding.id
                for _, finding in findings_with_order
                if finding.id in CONDITIONAL_SEVERITY_IDS
                and finding.severity
                is not _conditional_severity(finding.id, packet_status)
            }
        )
        if conditional_breaches:
            raise DiagnosticError(
                "internal_error",
                "A diagnostic check emitted invalid conditional severities for: "
                + ", ".join(conditional_breaches),
                state_version=state_result.state_version,
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
                state_version=state_result.state_version,
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
            state_version=state_result.state_version,
        )
