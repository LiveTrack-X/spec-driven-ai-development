from __future__ import annotations

from typing import TYPE_CHECKING

from ..diagnostics import Finding, Severity
from ..project_view import ReadResult
from ..state_contract import is_normalized_relative_posix_path

if TYPE_CHECKING:
    from ..doctor import DoctorContext


STATE_PATH = "sdad-state.yaml"
INDEX_PATH = "docs/INDEX.md"
OPTIONAL_CONTROL_DOCUMENTS = (
    "review-findings.md",
    "docs/TODO-Open-Items.md",
)

_PATH_STATUS_IDS = {
    "invalid": "path.invalid",
    "outside_root": "path.outside-root",
    "missing": "path.missing",
    "not_file": "path.not-file",
    "unreadable": "path.unreadable",
}

_PATH_MESSAGES = {
    "path.invalid": "A declared path is not a normalized repository-relative POSIX path.",
    "path.outside-root": "A declared path resolves outside the project root.",
    "path.missing": "A declared file does not exist.",
    "path.not-file": "A declared path is not a regular file.",
    "path.unreadable": "A declared file cannot be read.",
    "path.encoding.invalid": "An inspected control document is not valid UTF-8 text.",
    "path.too-large": "An inspected control document exceeds the configured size limit.",
    "handoff.path.too-large": "The current handoff exceeds the configured size limit.",
    "path.duplicate-route": "The same routed document is declared more than once.",
}

_PATH_REMEDIATIONS = {
    "path.invalid": "Use a normalized repository-relative POSIX path.",
    "path.outside-root": "Route only regular files that resolve inside the project root.",
    "path.missing": "Correct the declaration or create the intended file.",
    "path.not-file": "Point the declaration at a regular file.",
    "path.unreadable": "Restore read access or correct the declared path.",
    "path.encoding.invalid": "Save the control document as valid UTF-8 text.",
    "path.too-large": "Reduce or archive the control document before inspection.",
    "handoff.path.too-large": "Reduce or archive the current handoff before inspection.",
    "path.duplicate-route": "Keep one occurrence of each routed document.",
}


def _finding(
    finding_id: str,
    *,
    path: str,
    line: int | None,
    evidence: str,
) -> Finding:
    return Finding(
        id=finding_id,
        severity=(
            Severity.WARNING
            if finding_id in {"path.too-large", "path.duplicate-route"}
            else Severity.ERROR
        ),
        message=_PATH_MESSAGES[finding_id],
        path=path,
        line=line,
        evidence=evidence,
        remediation=_PATH_REMEDIATIONS[finding_id],
    )


class PathIntegrityCheck:
    name = "path_integrity"

    def run(self, context: DoctorContext) -> tuple[Finding, ...]:
        findings = [
            Finding(
                id=issue.id,
                severity=Severity(issue.severity),
                message=issue.message,
                path=STATE_PATH,
                line=issue.line,
                evidence=issue.evidence,
                remediation=_PATH_REMEDIATIONS[issue.id],
            )
            for issue in context.state_result.issues
            if issue.id.startswith("path.")
        ]
        snapshot = context.state_result.snapshot
        if snapshot is None:
            return tuple(findings)

        current_handoff_path: str | None = None
        if context.state_result.state_version == 2:
            current_handoff = snapshot.scalar("current_handoff")
            if current_handoff is not None and is_normalized_relative_posix_path(
                current_handoff.value
            ):
                current_handoff_path = current_handoff.value

        inspection_statuses: dict[str, str] = {}
        read_results: dict[str, ReadResult] = {}
        reported_status_paths: set[tuple[str, str]] = set()
        reported_content_paths: set[tuple[str, str]] = set()

        def inspect(relative_path: str) -> str:
            if relative_path not in inspection_statuses:
                inspection_statuses[relative_path] = context.view.inspect(
                    relative_path
                ).status
            return inspection_statuses[relative_path]

        def report_status(relative_path: str, status: str) -> None:
            finding_id = _PATH_STATUS_IDS.get(status)
            if finding_id is None:
                return
            occurrence = (finding_id, relative_path)
            if occurrence in reported_status_paths:
                return
            reported_status_paths.add(occurrence)
            findings.append(
                _finding(
                    finding_id,
                    path=relative_path,
                    line=None,
                    evidence=f"inspection status: {status}",
                )
            )

        def report_content(
            finding_id: str,
            relative_path: str,
            evidence: str,
        ) -> None:
            occurrence = (finding_id, relative_path)
            if occurrence in reported_content_paths:
                return
            reported_content_paths.add(occurrence)
            findings.append(
                _finding(
                    finding_id,
                    path=relative_path,
                    line=None,
                    evidence=evidence,
                )
            )

        def inspect_content(relative_path: str) -> None:
            if relative_path not in read_results:
                try:
                    read_results[relative_path] = context.view.read_bytes(
                        relative_path,
                        context.policy.max_control_document_bytes,
                    )
                except OSError:
                    read_results[relative_path] = ReadResult("unreadable", None)
            read_result = read_results[relative_path]
            status = read_result.status
            if status == "too_large":
                report_content(
                    (
                        "handoff.path.too-large"
                        if relative_path == current_handoff_path
                        else "path.too-large"
                    ),
                    relative_path,
                    "document exceeds "
                    f"{context.policy.max_control_document_bytes} bytes",
                )
                return
            if status != "ok":
                report_status(relative_path, status)
                return
            if read_result.data is None:
                report_status(relative_path, "unreadable")
                return
            try:
                read_result.data.decode("utf-8")
            except UnicodeDecodeError:
                report_content(
                    "path.encoding.invalid",
                    relative_path,
                    "UTF-8 decoding failed",
                )

        active_spec = snapshot.scalar("active_spec")
        if active_spec is not None and is_normalized_relative_posix_path(
            active_spec.value
        ):
            status = inspect(active_spec.value)
            report_status(active_spec.value, status)
            if status == "ok":
                inspect_content(active_spec.value)

        declared_routes: set[str] = set()
        for route in snapshot.routed_docs:
            if not is_normalized_relative_posix_path(route.value):
                continue
            if route.value in declared_routes:
                findings.append(
                    _finding(
                        "path.duplicate-route",
                        path=STATE_PATH,
                        line=route.line,
                        evidence=f"duplicate routed_docs entry: {route.value}",
                    )
                )
                continue
            declared_routes.add(route.value)
            status = inspect(route.value)
            report_status(route.value, status)
            if status == "ok":
                inspect_content(route.value)

        if context.state_result.state_version == 2:
            for continuity_path in (INDEX_PATH, current_handoff_path):
                if continuity_path is None:
                    continue
                status = inspect(continuity_path)
                report_status(continuity_path, status)
                if status == "ok":
                    inspect_content(continuity_path)

        for document_path in OPTIONAL_CONTROL_DOCUMENTS:
            status = inspect(document_path)
            is_declared = document_path in declared_routes
            if not is_declared and status == "missing":
                continue
            if status != "ok":
                report_status(document_path, status)
                continue
            inspect_content(document_path)

        return tuple(findings)
