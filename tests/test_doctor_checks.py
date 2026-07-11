from __future__ import annotations

import sys
import unittest
from collections import Counter
from datetime import date
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.diagnostics import (  # noqa: E402
    DiagnosticError,
    DoctorPolicy,
    DoctorReport,
    Finding,
    Severity,
)
from sdad_validator.doctor import (  # noqa: E402
    ALLOWED_FINDING_IDS,
    DiagnosticEngine,
    _CachedProjectView,
)
from sdad_validator.project_view import (  # noqa: E402
    PathInspection,
    ReadResult,
)


STATE_PATH_FINDING_IDS = frozenset(
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
    }
)

PACKET_GATE_FINDING_IDS = frozenset(
    {
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
    }
)

REVIEW_TODO_FINDING_IDS = frozenset(
    {
        "review.structure.missing-section",
        "todo.structure.missing-section",
        "packet.open-finding",
        "packet.open-critical-finding",
        "packet.open-todo",
        "packet.unlinked-open-work",
        "packet.marker.unrepresentable",
    }
)

ALL_SCHEMA_V1_FINDING_IDS = (
    STATE_PATH_FINDING_IDS | PACKET_GATE_FINDING_IDS | REVIEW_TODO_FINDING_IDS
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

FIXED_CHECKS = (
    "state_schema",
    "path_integrity",
    "packet_coherence",
    "owner_gates",
    "review_state",
)


def _scalar_list(key: str, values: tuple[str, ...]) -> list[str]:
    if not values:
        return [f"{key}: []"]
    return [f"{key}:", *(f"  - {value}" for value in values)]


def valid_state(
    *,
    updated: str = "2026-07-10",
    scale: str = "standard",
    intensity: str = "medium",
    autonomy: str = "2",
    active_spec: str = "SPEC/current.md",
    packet_id: str = "WP-001",
    objective: str = "Implement the current bounded packet.",
    status: str = "in_progress",
    owner_gates: tuple[str, ...] = (),
    validation: tuple[dict[str, str], ...] | None = None,
    routed_docs: tuple[str, ...] = (),
) -> str:
    if validation is None:
        validation = (
            {
                "command": "python -m unittest discover -s tests",
                "proves": "The project unit tests pass.",
            },
        )
    lines = [
        "version: 1",
        f"updated: {updated}",
        f"scale: {scale}",
        f"intensity: {intensity}",
        f"autonomy: {autonomy}",
        f"active_spec: {active_spec}",
        "active_packet:",
        f"  id: {packet_id}",
        f"  objective: {objective}",
        f"  status: {status}",
        *_scalar_list("owner_gates", owner_gates),
    ]
    if validation:
        lines.append("validation:")
        for entry in validation:
            fields = list(entry.items())
            first_key, first_value = fields[0]
            lines.append(f"  - {first_key}: {first_value}")
            lines.extend(f"    {key}: {value}" for key, value in fields[1:])
    else:
        lines.append("validation: []")
    lines.extend(_scalar_list("routed_docs", routed_docs))
    return "\n".join(lines) + "\n"


def replace_validation_block(state: str, replacement: str) -> str:
    canonical = (
        "validation:\n"
        "  - command: python -m unittest discover -s tests\n"
        "    proves: The project unit tests pass.\n"
    )
    if canonical not in state:
        raise AssertionError("canonical validation block was not present")
    return state.replace(canonical, replacement.rstrip() + "\n", 1)


class InMemoryProjectView:
    def __init__(
        self,
        files: dict[str, bytes] | None = None,
        statuses: dict[str, str] | None = None,
        read_statuses: dict[str, str] | None = None,
        read_exceptions: dict[str, OSError] | None = None,
    ) -> None:
        self._root = Path("C:/project")
        self.files = dict(files or {})
        self.statuses = dict(statuses or {})
        self.read_statuses = dict(read_statuses or {})
        self.read_exceptions = dict(read_exceptions or {})
        self.read_counts: Counter[str] = Counter()
        self.inspect_counts: Counter[str] = Counter()

    @property
    def root(self) -> Path:
        return self._root

    def inspect(self, relative_path: str) -> PathInspection:
        self.inspect_counts[relative_path] += 1
        status = self.statuses.get(relative_path)
        if status is None:
            status = "ok" if relative_path in self.files else "missing"
        resolved = self._root / relative_path if status != "invalid" else None
        return PathInspection(status, resolved)

    def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult:
        self.read_counts[relative_path] += 1
        if relative_path in self.read_exceptions:
            raise self.read_exceptions[relative_path]
        status = self.read_statuses.get(relative_path)
        if status is None:
            status = self.statuses.get(relative_path)
        if status is None:
            status = "ok" if relative_path in self.files else "missing"
        if status != "ok":
            return ReadResult(status, None)
        data = self.files[relative_path]
        if len(data) > max_bytes:
            return ReadResult("too_large", None)
        return ReadResult("ok", data)


def make_view(
    state: str | bytes | None = None,
    *,
    files: dict[str, str | bytes] | None = None,
    statuses: dict[str, str] | None = None,
    read_statuses: dict[str, str] | None = None,
    read_exceptions: dict[str, OSError] | None = None,
) -> InMemoryProjectView:
    payloads: dict[str, bytes] = {"SPEC/current.md": b"# Current spec\n"}
    if state is None:
        state = valid_state()
    if state is not False:
        payloads["sdad-state.yaml"] = (
            state.encode("utf-8") if isinstance(state, str) else state
        )
    for path, content in (files or {}).items():
        payloads[path] = content.encode("utf-8") if isinstance(content, str) else content
    return InMemoryProjectView(
        payloads,
        statuses,
        read_statuses,
        read_exceptions,
    )


def diagnose(
    state: str | bytes | None | bool = None,
    *,
    files: dict[str, str | bytes] | None = None,
    statuses: dict[str, str] | None = None,
    read_statuses: dict[str, str] | None = None,
    read_exceptions: dict[str, OSError] | None = None,
    policy: DoctorPolicy | None = None,
) -> DoctorReport:
    view = make_view(
        state,
        files=files,
        statuses=statuses,
        read_statuses=read_statuses,
        read_exceptions=read_exceptions,
    )
    return DiagnosticEngine().diagnose(
        view,
        policy or DoctorPolicy(today=date(2026, 7, 10)),
    )


class DoctorAssertions:
    def assertFinding(
        self,
        report: DoctorReport,
        finding_id: str,
        severity: Severity | None = None,
    ) -> None:
        matches = [finding for finding in report.findings if finding.id == finding_id]
        self.assertTrue(matches, f"missing {finding_id}: {report.findings}")
        if severity is not None:
            self.assertTrue(
                any(finding.severity is severity for finding in matches),
                f"{finding_id} did not have severity {severity}: {matches}",
            )

    def assertNotFinding(self, report: DoctorReport, finding_id: str) -> None:
        self.assertFalse(
            any(finding.id == finding_id for finding in report.findings),
            f"unexpected {finding_id}: {report.findings}",
        )


class DoctorStateAndPathTests(DoctorAssertions, unittest.TestCase):
    def test_missing_and_non_file_state_are_normal_completed_reports(self) -> None:
        for status in ("missing", "not_file"):
            with self.subTest(status=status):
                report = diagnose(False, statuses={"sdad-state.yaml": status})

                self.assertFinding(report, "state.missing", Severity.ERROR)
                self.assertEqual(report.checks_run, ("state_schema",))
                self.assertEqual(report.checks_skipped, FIXED_CHECKS[1:])
                self.assertEqual(report.error_count, 1)
                self.assertEqual(report.warning_count, 0)

    def test_os_failure_reading_required_state_raises_diagnostic_error(self) -> None:
        with self.assertRaises(DiagnosticError) as caught:
            diagnose(False, statuses={"sdad-state.yaml": "unreadable"})

        self.assertEqual(caught.exception.kind, "unreadable_state")

    def test_unusable_state_bytes_are_findings_and_skip_dependent_checks(self) -> None:
        cases = (
            (
                "state.too-large",
                b"version: 1\n" * 8,
                DoctorPolicy(today=date(2026, 7, 10), max_state_bytes=8),
            ),
            (
                "state.encoding.invalid",
                b"version: 1\n\xff",
                DoctorPolicy(today=date(2026, 7, 10)),
            ),
            (
                "state.syntax.unsupported",
                "version: 1\nscale: &shared standard\n",
                DoctorPolicy(today=date(2026, 7, 10)),
            ),
        )
        for finding_id, state, policy in cases:
            with self.subTest(finding_id=finding_id):
                report = diagnose(state, policy=policy)

                self.assertFinding(report, finding_id, Severity.ERROR)
                self.assertEqual(report.checks_run, ("state_schema",))
                self.assertEqual(report.checks_skipped, FIXED_CHECKS[1:])

    def test_state_is_read_exactly_once_for_a_complete_diagnosis(self) -> None:
        view = make_view(valid_state())

        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(today=date(2026, 7, 10)),
        )

        self.assertEqual(view.read_counts["sdad-state.yaml"], 1)
        self.assertEqual(report.checks_run, FIXED_CHECKS)
        self.assertEqual(report.checks_skipped, ())

    def test_schema_contract_routes_every_state_schema_id_once(self) -> None:
        baseline = valid_state()
        cases = {
            "state.schema.duplicate-key": baseline + "scale: standard\n",
            "state.schema.missing-key": baseline.replace("intensity: medium\n", ""),
            "state.schema.unknown-key": baseline + "custom_key: preserved\n",
            "state.schema.wrong-kind": baseline.replace(
                "owner_gates: []\n", "owner_gates:\n  gate: approval\n"
            ),
            "state.schema.missing-version": baseline.replace("version: 1\n", ""),
            "state.schema.unsupported-version": baseline.replace(
                "version: 1", "version: 99"
            ),
            "state.schema.unsupported-value": baseline.replace(
                "scale: standard", "scale: enormous"
            ),
            "state.packet.missing-field": baseline.replace(
                "  objective: Implement the current bounded packet.\n", ""
            ),
            "state.packet.blank-field": baseline.replace(
                "  objective: Implement the current bounded packet.", "  objective: ''"
            ),
            "state.collection.malformed-entry": baseline.replace(
                "owner_gates: []", "owner_gates:\n  -"
            ),
        }

        emitted: set[str] = set()
        for finding_id, state in cases.items():
            with self.subTest(finding_id=finding_id):
                report = diagnose(state)
                self.assertFinding(
                    report,
                    finding_id,
                    Severity.WARNING
                    if finding_id in {
                        "state.schema.unknown-key",
                        "state.schema.missing-version",
                    }
                    else Severity.ERROR,
                )
                occurrences = [
                    finding
                    for finding in report.findings
                    if finding.id == finding_id
                ]
                self.assertEqual(len(occurrences), 1)
                emitted.add(occurrences[0].id)

        self.assertEqual(emitted, set(cases))

    def test_freshness_contract_covers_missing_placeholder_invalid_stale_and_future(self) -> None:
        cases = {
            "state.updated.missing": valid_state().replace(
                "updated: 2026-07-10\n", ""
            ),
            "state.updated.placeholder": valid_state(updated="YYYY-MM-DD"),
            "state.updated.invalid": valid_state(updated="2026-02-30"),
            "state.updated.stale": valid_state(updated="2026-06-09"),
            "state.updated.future": valid_state(updated="2026-07-12"),
        }
        for finding_id, state in cases.items():
            with self.subTest(finding_id=finding_id):
                report = diagnose(state)
                self.assertFinding(report, finding_id, Severity.WARNING)

    def test_freshness_uses_exact_thirty_day_and_one_day_future_boundaries(self) -> None:
        for updated in ("2026-06-10", "2026-07-10", "2026-07-11"):
            with self.subTest(updated=updated):
                report = diagnose(valid_state(updated=updated))
                self.assertNotFinding(report, "state.updated.stale")
                self.assertNotFinding(report, "state.updated.future")

        stale = diagnose(valid_state(updated="2026-06-09"))
        future = diagnose(valid_state(updated="2026-07-12"))
        self.assertFinding(stale, "state.updated.stale", Severity.WARNING)
        self.assertFinding(future, "state.updated.future", Severity.WARNING)

    def test_structurally_invalid_updated_value_does_not_cascade_to_missing(self) -> None:
        for updated_line in ("updated:", "updated: []"):
            with self.subTest(updated_line=updated_line):
                state = valid_state().replace("updated: 2026-07-10", updated_line)
                report = diagnose(state)

                self.assertFinding(report, "state.schema.wrong-kind", Severity.ERROR)
                self.assertNotFinding(report, "state.updated.missing")

    def test_invalid_active_and_routed_paths_are_not_inspected(self) -> None:
        invalid_paths = (
            "../secret.md",
            "C:/secret.md",
            "docs\\secret.md",
            "./docs/secret.md",
            "docs/",
        )
        for invalid_path in invalid_paths:
            with self.subTest(invalid_path=invalid_path):
                state = valid_state(
                    active_spec=invalid_path,
                    routed_docs=(invalid_path,),
                )
                view = make_view(state)

                report = DiagnosticEngine().diagnose(
                    view,
                    DoctorPolicy(today=date(2026, 7, 10)),
                )

                self.assertFinding(report, "path.invalid", Severity.ERROR)
                self.assertEqual(view.inspect_counts[invalid_path], 0)

    def test_active_spec_inspection_statuses_map_to_exact_path_findings(self) -> None:
        expected = {
            "outside_root": "path.outside-root",
            "missing": "path.missing",
            "not_file": "path.not-file",
            "unreadable": "path.unreadable",
        }
        for status, finding_id in expected.items():
            with self.subTest(status=status):
                report = diagnose(
                    valid_state(),
                    statuses={"SPEC/current.md": status},
                )
                self.assertFinding(report, finding_id, Severity.ERROR)

    def test_routed_targets_are_checked_once_and_duplicate_routes_warn(self) -> None:
        state = valid_state(
            routed_docs=(
                "docs/missing.md",
                "docs/not-file.md",
                "docs/outside.md",
                "docs/unreadable.md",
                "docs/missing.md",
            )
        )
        statuses = {
            "docs/missing.md": "missing",
            "docs/not-file.md": "not_file",
            "docs/outside.md": "outside_root",
            "docs/unreadable.md": "unreadable",
        }
        view = make_view(state, statuses=statuses)

        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(today=date(2026, 7, 10)),
        )

        for finding_id in (
            "path.missing",
            "path.not-file",
            "path.outside-root",
            "path.unreadable",
            "path.duplicate-route",
        ):
            self.assertFinding(report, finding_id)
        self.assertEqual(view.inspect_counts["docs/missing.md"], 1)
        self.assertEqual(
            len(
                [
                    finding
                    for finding in report.findings
                    if finding.id == "path.duplicate-route"
                ]
            ),
            1,
        )
        duplicate = next(
            finding
            for finding in report.findings
            if finding.id == "path.duplicate-route"
        )
        self.assertEqual(duplicate.severity, Severity.WARNING)

    def test_optional_control_document_encoding_and_size_are_path_findings(self) -> None:
        report = diagnose(
            valid_state(),
            files={
                "review-findings.md": b"\xff",
                "docs/TODO-Open-Items.md": b"x" * 9,
            },
            policy=DoctorPolicy(
                today=date(2026, 7, 10),
                max_control_document_bytes=8,
            ),
        )

        self.assertFinding(report, "path.encoding.invalid", Severity.ERROR)
        self.assertFinding(report, "path.too-large", Severity.WARNING)
        self.assertIn("review_state", report.checks_run)
        self.assertNotIn("review_state", report.checks_skipped)

    def test_active_spec_and_routes_are_bounded_utf8_reads_deduplicated_by_path(self) -> None:
        state = valid_state(
            routed_docs=(
                "SPEC/current.md",
                "docs/open-fails.md",
                "docs/invalid.md",
                "docs/large.md",
            )
        )
        view = make_view(
            state,
            files={
                "SPEC/current.md": "# Current spec\n",
                "docs/open-fails.md": "read attempt fails",
                "docs/invalid.md": b"\xff",
                "docs/large.md": b"x" * 9,
            },
            read_statuses={"docs/open-fails.md": "unreadable"},
        )

        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(
                today=date(2026, 7, 10),
                max_control_document_bytes=8,
            ),
        )

        self.assertFinding(report, "path.unreadable", Severity.ERROR)
        self.assertFinding(report, "path.encoding.invalid", Severity.ERROR)
        self.assertFinding(report, "path.too-large", Severity.WARNING)
        for path in (
            "SPEC/current.md",
            "docs/open-fails.md",
            "docs/invalid.md",
            "docs/large.md",
        ):
            with self.subTest(path=path):
                self.assertEqual(view.read_counts[path], 1)

    def test_optional_read_os_error_is_a_path_finding_not_internal_failure(self) -> None:
        view = make_view(
            valid_state(),
            files={
                "review-findings.md": (
                    "## Active Findings\n"
                    "None currently tracked.\n"
                )
            },
            read_exceptions={
                "review-findings.md": PermissionError("denied")
            },
        )
        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(today=date(2026, 7, 10)),
        )

        self.assertFinding(report, "path.unreadable", Severity.ERROR)
        self.assertNotFinding(report, "review.structure.missing-section")
        self.assertEqual(report.checks_run, FIXED_CHECKS)
        self.assertEqual(report.checks_skipped, ())
        self.assertEqual(view.read_counts["review-findings.md"], 1)

    def test_control_documents_use_one_cached_bounded_snapshot(self) -> None:
        review_versions = (
            (
                "## Active Findings\n"
                "- [High] [packet:WP-001] First review snapshot\n"
                "## Recently Closed\n"
            ).encode("utf-8"),
            (
                "## Active Findings\n"
                "None currently tracked.\n"
                "## Recently Closed\n"
            ).encode("utf-8"),
        )
        todo_versions = (
            (
                "## Active Work\n"
                "- [ ] [packet:WP-001] First TODO snapshot\n"
                "## Release / Production Readiness\n"
                "None currently tracked.\n"
            ).encode("utf-8"),
            (
                "## Active Work\n"
                "None currently tracked.\n"
                "## Release / Production Readiness\n"
                "None currently tracked.\n"
            ).encode("utf-8"),
        )

        class FlappingProjectView(InMemoryProjectView):
            def __init__(self) -> None:
                state = valid_state(
                    status="owner_accepted",
                    routed_docs=(
                        "review-findings.md",
                        "docs/TODO-Open-Items.md",
                    ),
                )
                super().__init__(
                    {
                        "sdad-state.yaml": state.encode("utf-8"),
                        "SPEC/current.md": b"# Current spec\n",
                        "review-findings.md": review_versions[0],
                        "docs/TODO-Open-Items.md": todo_versions[0],
                    }
                )
                self._versions = {
                    "review-findings.md": review_versions,
                    "docs/TODO-Open-Items.md": todo_versions,
                }

            def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult:
                versions = self._versions.get(relative_path)
                if versions is None:
                    return super().read_bytes(relative_path, max_bytes)
                self.read_counts[relative_path] += 1
                read_index = min(self.read_counts[relative_path] - 1, len(versions) - 1)
                data = versions[read_index]
                if len(data) > max_bytes:
                    return ReadResult("too_large", None)
                return ReadResult("ok", data)

        view = FlappingProjectView()
        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(today=date(2026, 7, 10)),
        )

        self.assertFinding(report, "packet.open-finding", Severity.ERROR)
        self.assertFinding(report, "packet.open-todo", Severity.ERROR)
        self.assertEqual(view.read_counts["review-findings.md"], 1)
        self.assertEqual(view.read_counts["docs/TODO-Open-Items.md"], 1)

    def test_state_file_can_be_active_spec_and_route_without_second_read(self) -> None:
        state = valid_state(
            active_spec="sdad-state.yaml",
            routed_docs=("sdad-state.yaml",),
        )
        state_size = len(state.encode("utf-8"))
        view = make_view(state)

        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(
                today=date(2026, 7, 10),
                max_state_bytes=state_size,
                max_control_document_bytes=state_size + 1,
            ),
        )

        self.assertEqual(view.read_counts["sdad-state.yaml"], 1)
        self.assertEqual(view.inspect_counts["sdad-state.yaml"], 1)
        self.assertEqual(report.checks_run, FIXED_CHECKS)
        self.assertEqual(report.checks_skipped, ())
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 0)

    def test_cached_state_bytes_apply_later_smaller_control_limit(self) -> None:
        state = valid_state(
            active_spec="sdad-state.yaml",
            routed_docs=("sdad-state.yaml",),
        )
        state_size = len(state.encode("utf-8"))
        view = make_view(state)

        report = DiagnosticEngine().diagnose(
            view,
            DoctorPolicy(
                today=date(2026, 7, 10),
                max_state_bytes=state_size,
                max_control_document_bytes=state_size - 1,
            ),
        )

        self.assertEqual(view.read_counts["sdad-state.yaml"], 1)
        self.assertFinding(report, "path.too-large", Severity.WARNING)
        self.assertEqual(report.checks_run, FIXED_CHECKS)
        self.assertEqual(report.checks_skipped, ())
        self.assertEqual(report.error_count, 0)
        self.assertEqual(report.warning_count, 1)

    def test_cached_view_rereads_too_large_only_for_a_larger_limit(self) -> None:
        view = InMemoryProjectView({"doc.md": b"12345678"})
        cached = _CachedProjectView(view)

        self.assertEqual(cached.read_bytes("doc.md", 4), ReadResult("too_large", None))
        self.assertEqual(cached.read_bytes("doc.md", 3), ReadResult("too_large", None))
        self.assertEqual(cached.read_bytes("doc.md", 4), ReadResult("too_large", None))
        self.assertEqual(cached.read_bytes("doc.md", 8), ReadResult("ok", b"12345678"))
        self.assertEqual(cached.read_bytes("doc.md", 6), ReadResult("too_large", None))
        self.assertEqual(cached.read_bytes("doc.md", 10), ReadResult("ok", b"12345678"))
        self.assertEqual(view.inspect_counts["doc.md"], 1)
        self.assertEqual(view.read_counts["doc.md"], 2)

    def test_findings_have_stable_check_path_line_id_order_and_exact_counts(self) -> None:
        state = valid_state(updated="2026-06-09", routed_docs=("docs/missing.md",))
        state = state.replace("version: 1\n", "") + "custom_key: value\n"

        report = diagnose(state)

        self.assertEqual(
            [finding.id for finding in report.findings],
            [
                "state.schema.missing-version",
                "state.updated.stale",
                "state.schema.unknown-key",
                "path.missing",
            ],
        )
        self.assertEqual(report.error_count, 1)
        self.assertEqual(report.warning_count, 3)
        self.assertEqual(report.checks_run, FIXED_CHECKS)
        self.assertEqual(report.checks_skipped, ())

    def test_state_and_path_scenarios_emit_every_allowed_family_id(self) -> None:
        baseline = valid_state()
        reports = [
            diagnose(False, statuses={"sdad-state.yaml": "missing"}),
            diagnose(
                b"version: 1\n" * 8,
                policy=DoctorPolicy(today=date(2026, 7, 10), max_state_bytes=8),
            ),
            diagnose(b"version: 1\n\xff"),
            diagnose("version: 1\nscale: &shared standard\n"),
            diagnose(baseline + "scale: standard\n"),
            diagnose(baseline.replace("intensity: medium\n", "")),
            diagnose(baseline + "custom_key: preserved\n"),
            diagnose(
                baseline.replace(
                    "owner_gates: []\n", "owner_gates:\n  gate: approval\n"
                )
            ),
            diagnose(baseline.replace("version: 1\n", "")),
            diagnose(baseline.replace("version: 1", "version: 99")),
            diagnose(baseline.replace("scale: standard", "scale: enormous")),
            diagnose(
                baseline.replace(
                    "  objective: Implement the current bounded packet.\n", ""
                )
            ),
            diagnose(
                baseline.replace(
                    "  objective: Implement the current bounded packet.",
                    "  objective: ''",
                )
            ),
            diagnose(
                baseline.replace("owner_gates: []", "owner_gates:\n  -")
            ),
            diagnose(baseline.replace("updated: 2026-07-10\n", "")),
            diagnose(valid_state(updated="YYYY-MM-DD")),
            diagnose(valid_state(updated="2026-02-30")),
            diagnose(valid_state(updated="2026-06-09")),
            diagnose(valid_state(updated="2026-07-12")),
            diagnose(valid_state(active_spec="../secret.md")),
            diagnose(baseline, statuses={"SPEC/current.md": "outside_root"}),
            diagnose(baseline, statuses={"SPEC/current.md": "missing"}),
            diagnose(baseline, statuses={"SPEC/current.md": "not_file"}),
            diagnose(baseline, statuses={"SPEC/current.md": "unreadable"}),
            diagnose(
                valid_state(routed_docs=("docs/repeated.md", "docs/repeated.md")),
                files={"docs/repeated.md": "ok"},
            ),
            diagnose(
                baseline,
                files={"review-findings.md": b"\xff"},
            ),
            diagnose(
                baseline,
                files={"review-findings.md": b"x" * 9},
                policy=DoctorPolicy(
                    today=date(2026, 7, 10),
                    max_control_document_bytes=8,
                ),
            ),
        ]
        emitted = {
            finding.id for report in reports for finding in report.findings
        }

        self.assertTrue(
            all(
                finding.id in ALL_SCHEMA_V1_FINDING_IDS
                for report in reports
                for finding in report.findings
            )
        )
        self.assertEqual(emitted & STATE_PATH_FINDING_IDS, STATE_PATH_FINDING_IDS)

    def test_schema_v1_finding_allowlist_is_exactly_the_documented_44_ids(self) -> None:
        self.assertEqual(len(ALL_SCHEMA_V1_FINDING_IDS), 44)
        self.assertEqual(ALLOWED_FINDING_IDS, ALL_SCHEMA_V1_FINDING_IDS)

    def test_engine_rejects_reordered_checks_and_fixed_severity_breaches(self) -> None:
        from sdad_validator import checks

        reordered = (checks.BUILT_IN_CHECKS[1], checks.BUILT_IN_CHECKS[0], *checks.BUILT_IN_CHECKS[2:])
        with patch.object(checks, "BUILT_IN_CHECKS", reordered):
            with self.assertRaises(DiagnosticError) as caught:
                diagnose(valid_state())
        self.assertEqual(caught.exception.kind, "internal_error")

        class WrongSeverityStateCheck:
            name = "state_schema"

            def run(self, context: object) -> tuple[Finding, ...]:
                return (
                    Finding(
                        id="state.missing",
                        severity=Severity.WARNING,
                        message="wrong severity",
                        path="sdad-state.yaml",
                        line=None,
                        evidence="test contract breach",
                        remediation="reject this finding",
                    ),
                )

        wrong_severity = (WrongSeverityStateCheck(), *checks.BUILT_IN_CHECKS[1:])
        with patch.object(checks, "BUILT_IN_CHECKS", wrong_severity):
            with self.assertRaises(DiagnosticError) as caught:
                diagnose(valid_state())
        self.assertEqual(caught.exception.kind, "internal_error")

    def test_engine_rejects_invalid_conditional_severity_contracts(self) -> None:
        from sdad_validator import checks

        validation_ids = (
            "validation.empty",
            "validation.missing-command",
            "validation.blank-command",
            "validation.missing-proves",
            "validation.blank-proves",
            "validation.placeholder",
        )
        check_slots = {
            "validation": (2, "packet_coherence"),
            "gate": (3, "owner_gates"),
            "packet": (4, "review_state"),
        }

        def assert_rejected(
            finding_id: str,
            severity: object,
            status: str,
        ) -> None:
            domain = finding_id.split(".", 1)[0]
            slot, check_name = check_slots[domain]

            class FakeCheck:
                name = check_name

                def run(self, context: object) -> tuple[Finding, ...]:
                    return (
                        Finding(
                            id=finding_id,
                            severity=severity,  # type: ignore[arg-type]
                            message="fake conditional finding",
                            path="sdad-state.yaml",
                            line=10,
                            evidence=f"status: {status}",
                            remediation="reject invalid runtime contract",
                        ),
                    )

            built_ins = list(checks.BUILT_IN_CHECKS)
            built_ins[slot] = FakeCheck()
            with patch.object(checks, "BUILT_IN_CHECKS", tuple(built_ins)):
                with self.assertRaises(DiagnosticError) as caught:
                    diagnose(valid_state(status=status))
            self.assertEqual(caught.exception.kind, "internal_error")

        assert_rejected("validation.empty", "warning", "in_progress")
        for finding_id in validation_ids:
            with self.subTest(finding_id=finding_id, status="software_verified"):
                assert_rejected(finding_id, Severity.WARNING, "software_verified")
            with self.subTest(finding_id=finding_id, status="in_progress"):
                assert_rejected(finding_id, Severity.ERROR, "in_progress")
            with self.subTest(finding_id=finding_id, status="invented"):
                assert_rejected(finding_id, Severity.WARNING, "invented")

        gate_cases = (
            (Severity.ERROR, "owner_accepted"),
            (Severity.WARNING, "production_ready"),
            (Severity.WARNING, "in_progress"),
            (Severity.WARNING, "invented"),
        )
        for severity, status in gate_cases:
            with self.subTest(finding_id="gate.pending-after-acceptance", status=status):
                assert_rejected(
                    "gate.pending-after-acceptance",
                    severity,
                    status,
                )

        for finding_id in ("packet.open-finding", "packet.open-todo"):
            packet_cases = (
                (Severity.ERROR, "software_verified"),
                (Severity.WARNING, "owner_accepted"),
                (Severity.WARNING, "in_progress"),
                (Severity.WARNING, "invented"),
            )
            for severity, status in packet_cases:
                with self.subTest(finding_id=finding_id, status=status):
                    assert_rejected(finding_id, severity, status)


class DoctorPacketAndGateTests(DoctorAssertions, unittest.TestCase):
    def test_validation_required_status_set_controls_empty_severity_exactly(self) -> None:
        all_statuses = (
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
        )
        for status in all_statuses:
            with self.subTest(status=status):
                report = diagnose(valid_state(status=status, validation=()))
                expected = (
                    Severity.ERROR
                    if status in VALIDATION_REQUIRED_STATUSES
                    else Severity.WARNING
                )
                self.assertFinding(report, "validation.empty", expected)
                occurrences = [
                    finding
                    for finding in report.findings
                    if finding.id == "validation.empty"
                ]
                self.assertEqual(len(occurrences), 1)
                self.assertEqual({finding.severity for finding in occurrences}, {expected})

    def test_validation_field_defects_change_severity_without_duplicates(self) -> None:
        cases = {
            "validation.missing-command": ({"proves": "Tests pass."},),
            "validation.blank-command": (
                {"command": "'   '", "proves": "Tests pass."},
            ),
            "validation.missing-proves": ({"command": "python tests.py"},),
            "validation.blank-proves": (
                {"command": "python tests.py", "proves": "''"},
            ),
            "validation.placeholder": (
                {
                    "command": "Replace with the project check.",
                    "proves": "Tests pass.",
                },
            ),
        }
        for finding_id, validation in cases.items():
            for status, severity in (
                ("in_progress", Severity.WARNING),
                ("software_verified", Severity.ERROR),
            ):
                with self.subTest(finding_id=finding_id, status=status):
                    report = diagnose(
                        valid_state(status=status, validation=validation)
                    )
                    matches = [
                        finding
                        for finding in report.findings
                        if finding.id == finding_id
                    ]
                    self.assertEqual(len(matches), 1)
                    self.assertEqual(matches[0].severity, severity)

    def test_unknown_validation_keys_are_packet_warnings(self) -> None:
        report = diagnose(
            valid_state(
                validation=(
                    {
                        "command": "python tests.py",
                        "proves": "Tests pass.",
                        "notes": "not part of schema v1",
                    },
                )
            )
        )

        self.assertFinding(report, "validation.unknown-key", Severity.WARNING)
        self.assertEqual(
            len(
                [
                    finding
                    for finding in report.findings
                    if finding.id == "validation.unknown-key"
                ]
            ),
            1,
        )

    def test_validation_schema_defects_suppress_coherence_cascades(self) -> None:
        baseline = valid_state(status="software_verified")
        states = (
            replace_validation_block(baseline, ""),
            replace_validation_block(baseline, "validation: wrong-kind"),
            replace_validation_block(baseline, "validation:\n  - malformed"),
            replace_validation_block(
                baseline,
                "validation:\n"
                "  - command:\n"
                "    proves: Tests pass.",
            ),
            replace_validation_block(
                baseline,
                "validation:\n"
                "  - command: python tests.py\n"
                "    command: ''\n"
                "    proves: Tests pass.",
            ),
        )
        validation_defect_ids = PACKET_GATE_FINDING_IDS & {
            "validation.empty",
            "validation.missing-command",
            "validation.blank-command",
            "validation.missing-proves",
            "validation.blank-proves",
            "validation.placeholder",
        }
        for state in states:
            with self.subTest(state=state):
                report = diagnose(state)
                self.assertFalse(
                    validation_defect_ids
                    & {finding.id for finding in report.findings},
                    report.findings,
                )

    def test_unusable_packet_status_suppresses_conditional_validation_findings(self) -> None:
        baseline = valid_state(status="software_verified", validation=())
        states = (
            baseline.replace("  status: software_verified\n", ""),
            baseline.replace("  status: software_verified", "  status: ''"),
            baseline.replace("  status: software_verified", "  status: []"),
            baseline.replace("  status: software_verified", "  status: invented"),
        )
        conditional_ids = {
            "validation.empty",
            "validation.missing-command",
            "validation.blank-command",
            "validation.missing-proves",
            "validation.blank-proves",
            "validation.placeholder",
        }
        for state in states:
            with self.subTest(state=state):
                report = diagnose(state)
                self.assertTrue(
                    any(finding.id.startswith("state.") for finding in report.findings),
                    report.findings,
                )
                self.assertFalse(
                    conditional_ids & {finding.id for finding in report.findings},
                    report.findings,
                )

    def test_invalid_field_suppression_is_limited_to_its_own_entry(self) -> None:
        state = replace_validation_block(
            valid_state(status="software_verified"),
            "validation:\n"
            "  - command:\n"
            "    proves: First entry proof.\n"
            "  - proves: Second entry proof.",
        )

        report = diagnose(state)

        matches = [
            finding
            for finding in report.findings
            if finding.id == "validation.missing-command"
        ]
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0].severity, Severity.ERROR)
        self.assertNotFinding(report, "validation.blank-command")

    def test_autonomy_four_requires_a_gate_only_in_the_exact_status_set(self) -> None:
        required = (
            "not_started",
            "in_progress",
            "ai_complete",
            "software_verified",
            "tester_ready",
            "hardware_evidence_received",
            "hardware_verified",
            "blocked",
        )
        excluded = (
            "deferred",
            "owner_accepted",
            "release_candidate",
            "production_ready",
        )
        for status in required:
            with self.subTest(status=status):
                report = diagnose(valid_state(autonomy="4", status=status))
                self.assertFinding(report, "gate.required", Severity.ERROR)
        for status in excluded:
            with self.subTest(status=status):
                report = diagnose(valid_state(autonomy="4", status=status))
                self.assertNotFinding(report, "gate.required")

        lower_autonomy = diagnose(valid_state(autonomy="3", status="blocked"))
        self.assertNotFinding(lower_autonomy, "gate.required")

    def test_pending_gate_changes_from_warning_to_error_at_terminal_status(self) -> None:
        warning = diagnose(
            valid_state(status="owner_accepted", owner_gates=("Approve release",))
        )
        error = diagnose(
            valid_state(status="production_ready", owner_gates=("Approve release",))
        )

        self.assertFinding(
            warning,
            "gate.pending-after-acceptance",
            Severity.WARNING,
        )
        self.assertFinding(
            error,
            "gate.pending-after-acceptance",
            Severity.ERROR,
        )

    def test_release_candidate_alone_has_no_owner_gate_invariant(self) -> None:
        without_gate = diagnose(valid_state(status="release_candidate"))
        with_gate = diagnose(
            valid_state(
                status="release_candidate",
                owner_gates=("Release review",),
            )
        )

        for report in (without_gate, with_gate):
            self.assertNotFinding(report, "gate.required")
            self.assertNotFinding(report, "gate.pending-after-acceptance")

    def test_full_scale_without_a_q5_term_does_not_require_a_gate(self) -> None:
        report = diagnose(
            valid_state(
                scale="full",
                autonomy="2",
                objective="Coordinate a long multi-agent documentation packet.",
            )
        )

        self.assertNotFinding(report, "gate.required")
        self.assertNotFinding(report, "gate.q5-review")

    def test_q5_matching_normalizes_separators_and_real_data_alias(self) -> None:
        matches = (
            ("Perform a DESTRUCTIVE-ACTION safely.", frozenset({"destructive action"})),
            ("Operate on REAL_DATA safely.", frozenset({"real user data"})),
            ("Operate on real-user-data safely.", frozenset({"real user data"})),
            ("Run the orbital_launch operation.", frozenset({"orbital launch"})),
        )
        for objective, q5_keywords in matches:
            with self.subTest(objective=objective):
                report = diagnose(
                    valid_state(objective=objective),
                    policy=DoctorPolicy(
                        today=date(2026, 7, 10),
                        q5_keywords=q5_keywords,
                    ),
                )
                self.assertFinding(report, "gate.q5-review", Severity.WARNING)

    def test_q5_matching_has_whole_token_boundaries_and_no_hidden_keywords(self) -> None:
        nonmatches = (
            ("Improve authentication handling.", frozenset({"auth"})),
            ("Clean up prerelease notes.", frozenset({"release"})),
            ("Review real user metadata.", frozenset({"real user data"})),
            ("Prepare a production release.", frozenset({"orbital launch"})),
        )
        for objective, q5_keywords in nonmatches:
            with self.subTest(objective=objective):
                report = diagnose(
                    valid_state(objective=objective),
                    policy=DoctorPolicy(
                        today=date(2026, 7, 10),
                        q5_keywords=q5_keywords,
                    ),
                )
                self.assertNotFinding(report, "gate.q5-review")

        injected_match = diagnose(
            valid_state(objective="Perform an orbital-launch operation."),
            policy=DoctorPolicy(
                today=date(2026, 7, 10),
                q5_keywords=frozenset({"orbital launch"}),
            ),
        )
        self.assertFinding(injected_match, "gate.q5-review", Severity.WARNING)

    def test_q5_phrase_rejects_unapproved_punctuation_separators(self) -> None:
        for separator in ("/", ".", "+"):
            with self.subTest(separator=separator):
                report = diagnose(
                    valid_state(
                        objective=f"Perform a destructive{separator}action safely."
                    ),
                    policy=DoctorPolicy(
                        today=date(2026, 7, 10),
                        q5_keywords=frozenset({"destructive action"}),
                    ),
                )
                self.assertNotFinding(report, "gate.q5-review")

    def test_malformed_owner_gate_collection_does_not_create_gate_cascades(self) -> None:
        state = valid_state(autonomy="4", status="in_progress").replace(
            "owner_gates: []",
            "owner_gates:\n  -",
        )

        report = diagnose(state)

        self.assertFinding(report, "state.collection.malformed-entry", Severity.ERROR)
        self.assertNotFinding(report, "gate.required")
        self.assertNotFinding(report, "gate.q5-review")

    def test_whitespace_only_owner_gate_does_not_satisfy_or_remain_as_a_gate(self) -> None:
        required = diagnose(
            valid_state(
                autonomy="4",
                status="in_progress",
                owner_gates=("'   '",),
            )
        )
        terminal = diagnose(
            valid_state(
                status="production_ready",
                owner_gates=("'   '",),
            )
        )

        self.assertFinding(
            required,
            "state.collection.malformed-entry",
            Severity.ERROR,
        )
        self.assertNotFinding(required, "gate.required")
        self.assertNotFinding(required, "gate.q5-review")
        self.assertFinding(
            terminal,
            "state.collection.malformed-entry",
            Severity.ERROR,
        )
        self.assertNotFinding(terminal, "gate.pending-after-acceptance")

    def test_parseable_state_keeps_checks_run_when_only_subrules_are_suppressed(self) -> None:
        states = (
            valid_state(status="invented"),
            valid_state().replace(
                "owner_gates: []",
                "owner_gates: wrong-kind",
            ),
        )
        for state in states:
            with self.subTest(state=state):
                report = diagnose(state)
                self.assertEqual(report.checks_run, FIXED_CHECKS)
                self.assertEqual(report.checks_skipped, ())

    def test_packet_and_gate_scenarios_emit_every_allowed_family_id(self) -> None:
        reports = [
            diagnose(valid_state(validation=())),
            diagnose(valid_state(validation=({"proves": "Tests pass."},))),
            diagnose(
                valid_state(
                    validation=({"command": "''", "proves": "Tests pass."},)
                )
            ),
            diagnose(valid_state(validation=({"command": "python tests.py"},))),
            diagnose(
                valid_state(
                    validation=(
                        {"command": "python tests.py", "proves": "''"},
                    )
                )
            ),
            diagnose(
                valid_state(
                    validation=(
                        {
                            "command": "Replace with the project check.",
                            "proves": "Tests pass.",
                        },
                    )
                )
            ),
            diagnose(
                valid_state(
                    validation=(
                        {
                            "command": "python tests.py",
                            "proves": "Tests pass.",
                            "notes": "extra",
                        },
                    )
                )
            ),
            diagnose(valid_state(autonomy="4")),
            diagnose(
                valid_state(objective="Perform a destructive action."),
                policy=DoctorPolicy(
                    today=date(2026, 7, 10),
                    q5_keywords=frozenset({"destructive action"}),
                ),
            ),
            diagnose(
                valid_state(
                    status="owner_accepted",
                    owner_gates=("Approval",),
                )
            ),
        ]
        emitted = {
            finding.id for report in reports for finding in report.findings
        }

        self.assertTrue(
            all(
                finding.id in ALL_SCHEMA_V1_FINDING_IDS
                for report in reports
                for finding in report.findings
            )
        )
        self.assertEqual(emitted & PACKET_GATE_FINDING_IDS, PACKET_GATE_FINDING_IDS)


class DoctorReviewStateTests(DoctorAssertions, unittest.TestCase):
    def test_missing_exact_sections_warn_and_skip_each_document(self) -> None:
        report = diagnose(
            valid_state(status="owner_accepted"),
            files={
                "review-findings.md": (
                    "# Review\n\n"
                    "## Active findings\n\n"
                    "- [High] [packet:WP-001] Wrong heading case\n"
                ),
                "docs/TODO-Open-Items.md": (
                    "# TODO\n\n"
                    "## Active Work \n\n"
                    "- [ ] [packet:WP-001] Trailing heading space\n\n"
                    "## Release / Production Readiness\n\n"
                    "None currently tracked.\n"
                ),
            },
        )

        self.assertFinding(
            report,
            "review.structure.missing-section",
            Severity.WARNING,
        )
        self.assertFinding(
            report,
            "todo.structure.missing-section",
            Severity.WARNING,
        )
        for finding_id in (
            "packet.open-finding",
            "packet.open-todo",
            "packet.unlinked-open-work",
        ):
            self.assertNotFinding(report, finding_id)

    def test_each_required_todo_heading_is_checked_independently(self) -> None:
        documents = (
            (
                "## Active Work\n"
                "- [ ] [packet:WP-001] Active work\n"
            ),
            (
                "## Release / Production Readiness\n"
                "- [ ] [packet:WP-001] Release work\n"
            ),
        )
        for document in documents:
            with self.subTest(document=document):
                report = diagnose(
                    valid_state(status="owner_accepted"),
                    files={"docs/TODO-Open-Items.md": document},
                )
                matches = [
                    finding
                    for finding in report.findings
                    if finding.id == "todo.structure.missing-section"
                ]
                self.assertEqual(len(matches), 1)
                self.assertEqual(matches[0].severity, Severity.WARNING)
                self.assertNotFinding(report, "packet.open-todo")
                self.assertNotFinding(report, "packet.unlinked-open-work")

    def test_structure_warnings_do_not_depend_on_usable_packet_id(self) -> None:
        state = valid_state().replace("  id: WP-001\n", "")

        report = diagnose(
            state,
            files={
                "review-findings.md": "# Missing active review section\n",
                "docs/TODO-Open-Items.md": "# Missing active TODO sections\n",
            },
        )

        self.assertFinding(
            report,
            "state.packet.missing-field",
            Severity.ERROR,
        )
        self.assertFinding(
            report,
            "review.structure.missing-section",
            Severity.WARNING,
        )
        self.assertFinding(
            report,
            "todo.structure.missing-section",
            Severity.WARNING,
        )
        self.assertNotFinding(report, "packet.unlinked-open-work")

    def test_whitespace_only_packet_id_does_not_drive_linkage_coherence(self) -> None:
        report = diagnose(
            valid_state(packet_id="'   '", status="owner_accepted"),
            files={
                "review-findings.md": (
                    "## Active Findings\n"
                    "- [High] Finding cannot be linked without a usable packet ID\n"
                    "## Recently Closed\n"
                )
            },
        )

        self.assertNotFinding(report, "packet.open-finding")
        self.assertNotFinding(report, "packet.unlinked-open-work")

    def test_sentinel_checked_deferred_and_closed_entries_are_inactive(self) -> None:
        report = diagnose(
            valid_state(status="production_ready"),
            files={
                "review-findings.md": (
                    "## Active Findings\n\n"
                    "- [x] [packet:WP-001] Checked review item\n"
                    "- [X] [packet:WP-001] Checked review item uppercase\n"
                    "None currently tracked.\n\n"
                    "## Recently Closed\n\n"
                    "- [Critical] [packet:WP-001] Already closed\n"
                ),
                "docs/TODO-Open-Items.md": (
                    "## Active Work\n\n"
                    "- [x] [packet:WP-001] Checked lower\n"
                    "- [X] [packet:WP-001] Checked upper\n"
                    "None currently tracked.\n\n"
                    "## Future / Deferred\n\n"
                    "- [ ] [packet:WP-001] Deferred work\n\n"
                    "## Release / Production Readiness\n\n"
                    "None currently tracked.\n"
                ),
            },
        )

        self.assertFalse(
            REVIEW_TODO_FINDING_IDS & {finding.id for finding in report.findings},
            report.findings,
        )

    def test_linked_review_findings_change_severity_with_status(self) -> None:
        review = (
            "## Active Findings\n\n"
            "- [High] [packet:WP-001] Classified finding\n"
            "- [packet:WP-001] Unclassified linked finding\n\n"
            "## Recently Closed\n"
        )
        for status, severity in (
            ("software_verified", Severity.WARNING),
            ("owner_accepted", Severity.ERROR),
        ):
            with self.subTest(status=status):
                report = diagnose(
                    valid_state(status=status),
                    files={"review-findings.md": review},
                )
                matches = [
                    finding
                    for finding in report.findings
                    if finding.id == "packet.open-finding"
                ]
                self.assertEqual(len(matches), 2)
                self.assertEqual({finding.severity for finding in matches}, {severity})

    def test_linked_todos_in_both_sections_change_severity_with_status(self) -> None:
        todo = (
            "## Active Work\n\n"
            "- [ ] [packet:WP-001] Active implementation\n\n"
            "## Future / Deferred\n\n"
            "- [ ] [packet:WP-001] Ignored deferred item\n\n"
            "## Release / Production Readiness\n\n"
            "- [ ] [packet:WP-001] Release evidence\n"
        )
        for status, severity in (
            ("hardware_verified", Severity.WARNING),
            ("production_ready", Severity.ERROR),
        ):
            with self.subTest(status=status):
                report = diagnose(
                    valid_state(status=status),
                    files={"docs/TODO-Open-Items.md": todo},
                )
                matches = [
                    finding
                    for finding in report.findings
                    if finding.id == "packet.open-todo"
                ]
                self.assertEqual(len(matches), 2)
                self.assertEqual({finding.severity for finding in matches}, {severity})

    def test_review_and_todo_status_sets_are_exact(self) -> None:
        review = (
            "## Active Findings\n"
            "- [High] [packet:WP-001] Open finding\n"
            "## Recently Closed\n"
        )
        todo = (
            "## Active Work\n"
            "- [ ] [packet:WP-001] Open TODO\n"
            "## Release / Production Readiness\n"
            "None currently tracked.\n"
        )
        sensitive = {
            "software_verified",
            "tester_ready",
            "hardware_evidence_received",
            "hardware_verified",
            "release_candidate",
        }
        terminal = {"owner_accepted", "production_ready"}
        inactive = {
            "not_started",
            "in_progress",
            "ai_complete",
            "blocked",
            "deferred",
        }
        for status in sensitive | terminal | inactive:
            with self.subTest(status=status):
                report = diagnose(
                    valid_state(status=status),
                    files={
                        "review-findings.md": review,
                        "docs/TODO-Open-Items.md": todo,
                    },
                )
                matches = [
                    finding
                    for finding in report.findings
                    if finding.id in {"packet.open-finding", "packet.open-todo"}
                ]
                if status in sensitive:
                    self.assertEqual(len(matches), 2)
                    self.assertEqual(
                        {finding.severity for finding in matches},
                        {Severity.WARNING},
                    )
                elif status in terminal:
                    self.assertEqual(len(matches), 2)
                    self.assertEqual(
                        {finding.severity for finding in matches},
                        {Severity.ERROR},
                    )
                else:
                    self.assertEqual(matches, [])

    def test_release_critical_finding_supersedes_general_open_finding(self) -> None:
        report = diagnose(
            valid_state(status="release_candidate"),
            files={
                "review-findings.md": (
                    "## Active Findings\n\n"
                    "- [Critical] [packet:WP-001] Release blocker\n\n"
                    "## Recently Closed\n"
                )
            },
        )

        self.assertFinding(
            report,
            "packet.open-critical-finding",
            Severity.ERROR,
        )
        self.assertNotFinding(report, "packet.open-finding")
        self.assertEqual(
            len(
                [
                    finding
                    for finding in report.findings
                    if finding.path == "review-findings.md" and finding.line == 3
                ]
            ),
            1,
        )

    def test_critical_specialization_applies_only_at_release_candidate(self) -> None:
        review = (
            "## Active Findings\n"
            "- [Critical] [packet:WP-001] Critical finding\n"
            "## Recently Closed\n"
        )
        sensitive = {
            "software_verified",
            "tester_ready",
            "hardware_evidence_received",
            "hardware_verified",
        }
        terminal = {"owner_accepted", "production_ready"}
        inactive = {
            "not_started",
            "in_progress",
            "ai_complete",
            "blocked",
            "deferred",
        }
        for status in sensitive | terminal | inactive | {"release_candidate"}:
            with self.subTest(status=status):
                report = diagnose(
                    valid_state(status=status),
                    files={"review-findings.md": review},
                )
                if status == "release_candidate":
                    self.assertFinding(
                        report,
                        "packet.open-critical-finding",
                        Severity.ERROR,
                    )
                    self.assertNotFinding(report, "packet.open-finding")
                elif status in sensitive:
                    self.assertFinding(
                        report,
                        "packet.open-finding",
                        Severity.WARNING,
                    )
                    self.assertNotFinding(report, "packet.open-critical-finding")
                elif status in terminal:
                    self.assertFinding(
                        report,
                        "packet.open-finding",
                        Severity.ERROR,
                    )
                    self.assertNotFinding(report, "packet.open-critical-finding")
                else:
                    self.assertNotFinding(report, "packet.open-finding")
                    self.assertNotFinding(report, "packet.open-critical-finding")

    def test_review_classifications_and_marker_placement_are_exact(self) -> None:
        review = (
            "## Active Findings\n"
            "- [Critical] [packet:WP-001] Exact Critical\n"
            "- [High] [packet:WP-001] Exact High\n"
            "- [Medium] [packet:WP-001] Exact Medium\n"
            "- [Low] [packet:WP-001] Exact Low\n"
            "- [packet:WP-001] Exact unclassified\n"
            "- [High] [packet: WP-001 ] Trimmed captured ID\n"
            "- [critical] [packet:WP-001] Wrong classification case\n"
            "- [Urgent] [packet:WP-001] Unsupported classification\n"
            "- [High] [Packet:WP-001] Wrong marker case\n"
            "- [High] [packet:wp-001] Wrong ID case\n"
            "- [High] Marker later [packet:WP-001]\n"
            "- Similar prose for WP-001 only\n"
            "## Recently Closed\n"
        )

        report = diagnose(
            valid_state(status="software_verified"),
            files={"review-findings.md": review},
        )

        matches = [
            finding
            for finding in report.findings
            if finding.id == "packet.open-finding"
        ]
        self.assertEqual(len(matches), 6)
        self.assertEqual([finding.line for finding in matches], [2, 3, 4, 5, 6, 7])

        terminal = diagnose(
            valid_state(status="owner_accepted"),
            files={"review-findings.md": review},
        )
        linked = [
            finding
            for finding in terminal.findings
            if finding.id == "packet.open-finding"
        ]
        unlinked = [
            finding
            for finding in terminal.findings
            if finding.id == "packet.unlinked-open-work"
        ]
        self.assertEqual([finding.line for finding in linked], [2, 3, 4, 5, 6, 7])
        self.assertEqual([finding.line for finding in unlinked], [8, 9, 10, 11, 12, 13])
        self.assertEqual({finding.severity for finding in linked}, {Severity.ERROR})
        self.assertEqual({finding.severity for finding in unlinked}, {Severity.WARNING})

    def test_todo_marker_checkbox_and_placement_grammar_are_exact(self) -> None:
        todo = (
            "## Active Work\n"
            "- [ ] [packet:WP-001] Exact marker\n"
            "- [ ] [packet: WP-001 ] Trimmed captured ID\n"
            "- [ ] [Packet:WP-001] Wrong marker case\n"
            "- [ ] [packet:wp-001] Wrong ID case\n"
            "- [ ] Marker later [packet:WP-001]\n"
            "- [ ]  [packet:WP-001] Double separator space\n"
            "- [x] [packet:WP-001] Checked\n"
            "## Release / Production Readiness\n"
            "None currently tracked.\n"
        )

        report = diagnose(
            valid_state(status="hardware_verified"),
            files={"docs/TODO-Open-Items.md": todo},
        )

        matches = [
            finding
            for finding in report.findings
            if finding.id == "packet.open-todo"
        ]
        self.assertEqual(len(matches), 2)
        self.assertEqual([finding.line for finding in matches], [2, 3])

        terminal = diagnose(
            valid_state(status="owner_accepted"),
            files={"docs/TODO-Open-Items.md": todo},
        )
        linked = [
            finding
            for finding in terminal.findings
            if finding.id == "packet.open-todo"
        ]
        unlinked = [
            finding
            for finding in terminal.findings
            if finding.id == "packet.unlinked-open-work"
        ]
        self.assertEqual([finding.line for finding in linked], [2, 3])
        self.assertEqual([finding.line for finding in unlinked], [4, 5, 6, 7])
        self.assertEqual({finding.severity for finding in linked}, {Severity.ERROR})
        self.assertEqual({finding.severity for finding in unlinked}, {Severity.WARNING})

    def test_terminal_unlinked_work_requests_manual_reconciliation(self) -> None:
        report = diagnose(
            valid_state(status="owner_accepted"),
            files={
                "review-findings.md": (
                    "## Active Findings\n"
                    "- [High] Finding without a packet marker\n"
                    "- [Low] [packet:WP-999] Explicitly linked to another packet\n"
                    "## Recently Closed\n"
                ),
                "docs/TODO-Open-Items.md": (
                    "## Active Work\n"
                    "- [ ] Work without a packet marker\n"
                    "## Release / Production Readiness\n"
                    "None currently tracked.\n"
                ),
            },
        )

        matches = [
            finding
            for finding in report.findings
            if finding.id == "packet.unlinked-open-work"
        ]
        self.assertEqual(len(matches), 3)
        self.assertEqual({finding.severity for finding in matches}, {Severity.WARNING})
        self.assertEqual(
            {finding.path for finding in matches},
            {"review-findings.md", "docs/TODO-Open-Items.md"},
        )

    def test_packet_id_containing_closing_bracket_is_unrepresentable(self) -> None:
        report = diagnose(valid_state(packet_id="WP]001"))

        self.assertFinding(
            report,
            "packet.marker.unrepresentable",
            Severity.WARNING,
        )

    def test_optional_document_failures_skip_only_that_documents_subrules(self) -> None:
        todo = (
            "## Active Work\n"
            "- [ ] [packet:WP-001] Still open\n"
            "## Release / Production Readiness\n"
            "None currently tracked.\n"
        )
        state = valid_state(
            status="owner_accepted",
            routed_docs=("review-findings.md", "docs/TODO-Open-Items.md"),
        )
        cases = (
            (
                "path.encoding.invalid",
                {"SPEC/current.md": "x", "review-findings.md": b"\xff", "docs/TODO-Open-Items.md": todo},
                {},
                DoctorPolicy(today=date(2026, 7, 10)),
            ),
            (
                "path.too-large",
                {"SPEC/current.md": "x", "review-findings.md": b"x" * 257, "docs/TODO-Open-Items.md": todo},
                {},
                DoctorPolicy(
                    today=date(2026, 7, 10),
                    max_control_document_bytes=256,
                ),
            ),
            (
                "path.unreadable",
                {"SPEC/current.md": "x", "review-findings.md": "present", "docs/TODO-Open-Items.md": todo},
                {"review-findings.md": "unreadable"},
                DoctorPolicy(today=date(2026, 7, 10)),
            ),
        )
        for finding_id, files, read_statuses, policy in cases:
            with self.subTest(finding_id=finding_id):
                report = diagnose(
                    state,
                    files=files,
                    read_statuses=read_statuses,
                    policy=policy,
                )
                self.assertFinding(report, finding_id)
                self.assertFinding(report, "packet.open-todo", Severity.ERROR)
                self.assertNotFinding(report, "review.structure.missing-section")
                self.assertNotFinding(report, "packet.open-finding")
                self.assertIn("review_state", report.checks_run)
                self.assertNotIn("review_state", report.checks_skipped)

    def test_missing_routed_document_does_not_block_other_document_rules(self) -> None:
        report = diagnose(
            valid_state(
                status="owner_accepted",
                routed_docs=("review-findings.md",),
            ),
            files={
                "docs/TODO-Open-Items.md": (
                    "## Active Work\n"
                    "- [ ] [packet:WP-001] Still open\n"
                    "## Release / Production Readiness\n"
                    "None currently tracked.\n"
                )
            },
        )

        self.assertFinding(report, "path.missing", Severity.ERROR)
        self.assertFinding(report, "packet.open-todo", Severity.ERROR)
        self.assertNotFinding(report, "review.structure.missing-section")

    def test_absent_undeclared_optional_documents_are_ignored(self) -> None:
        report = diagnose(valid_state(status="owner_accepted"))

        self.assertFalse(
            REVIEW_TODO_FINDING_IDS & {finding.id for finding in report.findings},
            report.findings,
        )
        self.assertIn("review_state", report.checks_run)

    def test_similarly_named_routed_document_is_not_inspected_for_coherence(self) -> None:
        report = diagnose(
            valid_state(
                status="owner_accepted",
                routed_docs=("docs/review-findings.md",),
            ),
            files={
                "docs/review-findings.md": (
                    "## Active Findings\n"
                    "- [Critical] [packet:WP-001] Wrong document path\n"
                )
            },
        )

        self.assertNotFinding(report, "packet.open-finding")
        self.assertNotFinding(report, "packet.open-critical-finding")

    def test_review_findings_sort_by_path_then_line_with_exact_counts(self) -> None:
        report = diagnose(
            valid_state(status="owner_accepted"),
            files={
                "review-findings.md": (
                    "## Active Findings\n"
                    "- [High] [packet:WP-001] Open review\n"
                    "## Recently Closed\n"
                ),
                "docs/TODO-Open-Items.md": (
                    "## Active Work\n"
                    "- [ ] [packet:WP-001] Open TODO\n"
                    "## Release / Production Readiness\n"
                    "None currently tracked.\n"
                ),
            },
        )
        coherence = [
            finding
            for finding in report.findings
            if finding.id in {"packet.open-finding", "packet.open-todo"}
        ]

        self.assertEqual(
            [(finding.id, finding.path, finding.line) for finding in coherence],
            [
                ("packet.open-todo", "docs/TODO-Open-Items.md", 2),
                ("packet.open-finding", "review-findings.md", 2),
            ],
        )
        self.assertEqual(report.error_count, 2)
        self.assertEqual(report.warning_count, 0)

    def test_review_scenarios_emit_every_allowed_family_id(self) -> None:
        linked_review = (
            "## Active Findings\n"
            "- [High] [packet:WP-001] Open finding\n"
            "## Recently Closed\n"
        )
        critical_review = linked_review.replace("[High]", "[Critical]")
        linked_todo = (
            "## Active Work\n"
            "- [ ] [packet:WP-001] Open TODO\n"
            "## Release / Production Readiness\n"
            "None currently tracked.\n"
        )
        reports = [
            diagnose(
                valid_state(),
                files={"review-findings.md": "# Missing section\n"},
            ),
            diagnose(
                valid_state(),
                files={"docs/TODO-Open-Items.md": "# Missing sections\n"},
            ),
            diagnose(
                valid_state(status="software_verified"),
                files={"review-findings.md": linked_review},
            ),
            diagnose(
                valid_state(status="release_candidate"),
                files={"review-findings.md": critical_review},
            ),
            diagnose(
                valid_state(status="software_verified"),
                files={"docs/TODO-Open-Items.md": linked_todo},
            ),
            diagnose(
                valid_state(status="owner_accepted"),
                files={
                    "review-findings.md": (
                        "## Active Findings\n"
                        "- Work without marker\n"
                        "## Recently Closed\n"
                    )
                },
            ),
            diagnose(valid_state(packet_id="WP]001")),
        ]
        emitted = {
            finding.id for report in reports for finding in report.findings
        }

        self.assertTrue(
            all(
                finding.id in ALL_SCHEMA_V1_FINDING_IDS
                for report in reports
                for finding in report.findings
            )
        )
        self.assertEqual(emitted & REVIEW_TODO_FINDING_IDS, REVIEW_TODO_FINDING_IDS)


if __name__ == "__main__":
    unittest.main()
