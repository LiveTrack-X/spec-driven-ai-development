from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import unittest
from dataclasses import FrozenInstanceError, fields
from datetime import date
from pathlib import Path, PurePosixPath
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.diagnostics import (  # noqa: E402
    DEFAULT_Q5_KEYWORDS,
    DIAGNOSTIC_ERROR_KINDS,
    DiagnosticError,
    DoctorPolicy,
    DoctorReport,
    Finding,
    Severity,
)
from sdad_validator.project_view import (  # noqa: E402
    FilesystemProjectView,
    PathInspection,
    ProjectView,
    ReadResult,
)


EXPECTED_Q5_KEYWORDS = frozenset(
    {
        "release",
        "production",
        "migration",
        "destructive action",
        "real user data",
        "auth",
        "money",
        "security",
        "rollback",
    }
)


class DiagnosticRecordTests(unittest.TestCase):
    def test_severity_values_and_finding_are_exact_and_immutable(self) -> None:
        finding = Finding(
            id="path.invalid",
            severity=Severity.ERROR,
            message="The path is invalid.",
            path="SPEC/current.md",
            line=4,
            evidence="../outside.md",
            remediation="Use a normalized repository-relative POSIX path.",
        )

        self.assertEqual(Severity.ERROR.value, "error")
        self.assertEqual(Severity.WARNING.value, "warning")
        self.assertEqual(tuple(Severity), (Severity.ERROR, Severity.WARNING))
        self.assertEqual(finding.path, "SPEC/current.md")
        with self.assertRaises(FrozenInstanceError):
            finding.message = "changed"  # type: ignore[misc]

    def test_diagnostic_record_field_names_are_exact_and_ordered(self) -> None:
        expected_fields = (
            (
                Finding,
                (
                    "id",
                    "severity",
                    "message",
                    "path",
                    "line",
                    "evidence",
                    "remediation",
                ),
            ),
            (
                DoctorPolicy,
                (
                    "today",
                    "stale_after_days",
                    "max_state_bytes",
                    "max_control_document_bytes",
                    "q5_keywords",
                ),
            ),
            (
                DoctorReport,
                (
                    "root",
                    "findings",
                    "checks_run",
                    "checks_skipped",
                    "error_count",
                    "warning_count",
                ),
            ),
            (PathInspection, ("status", "resolved_path")),
            (ReadResult, ("status", "data")),
        )

        for record_type, expected in expected_fields:
            with self.subTest(record_type=record_type.__name__):
                self.assertEqual(
                    tuple(field.name for field in fields(record_type)),
                    expected,
                )

    def test_policy_has_exact_defaults_and_stores_injected_values(self) -> None:
        policy = DoctorPolicy(today=date(2026, 7, 10))

        self.assertEqual(DEFAULT_Q5_KEYWORDS, EXPECTED_Q5_KEYWORDS)
        self.assertEqual(policy.stale_after_days, 30)
        self.assertEqual(policy.max_state_bytes, 65_536)
        self.assertEqual(policy.max_control_document_bytes, 1_048_576)
        self.assertEqual(policy.q5_keywords, EXPECTED_Q5_KEYWORDS)
        with self.assertRaises(FrozenInstanceError):
            policy.stale_after_days = 31  # type: ignore[misc]

        injected = DoctorPolicy(
            today=date(2030, 1, 2),
            stale_after_days=7,
            max_state_bytes=123,
            max_control_document_bytes=456,
            q5_keywords=frozenset({"custom gate"}),
        )
        self.assertEqual(
            injected,
            DoctorPolicy(
                today=date(2030, 1, 2),
                stale_after_days=7,
                max_state_bytes=123,
                max_control_document_bytes=456,
                q5_keywords=frozenset({"custom gate"}),
            ),
        )

    def test_report_and_error_store_diagnostic_data(self) -> None:
        finding = Finding(
            id="state.missing",
            severity=Severity.WARNING,
            message="State is missing.",
            path=None,
            line=None,
            evidence="sdad-state.yaml",
            remediation="Install the project control files.",
        )
        report = DoctorReport(
            root="C:/project",
            findings=(finding,),
            checks_run=("state-schema",),
            checks_skipped=("path-integrity",),
            error_count=0,
            warning_count=1,
        )
        self.assertEqual(report.findings, (finding,))
        self.assertEqual(report.warning_count, 1)
        with self.assertRaises(FrozenInstanceError):
            report.root = "changed"  # type: ignore[misc]

    def test_diagnostic_error_accepts_only_the_four_stable_kinds(self) -> None:
        expected_kinds = frozenset(
            {
                "invalid_invocation",
                "unusable_root",
                "unreadable_state",
                "internal_error",
            }
        )

        self.assertEqual(DIAGNOSTIC_ERROR_KINDS, expected_kinds)
        self.assertIsInstance(DIAGNOSTIC_ERROR_KINDS, frozenset)
        for kind in expected_kinds:
            with self.subTest(kind=kind):
                error = DiagnosticError(kind, "diagnostic failed")
                self.assertEqual(error.kind, kind)
                self.assertEqual(str(error), "diagnostic failed")

        with self.assertRaisesRegex(ValueError, "unsupported diagnostic error kind"):
            DiagnosticError("usage", "bad invocation")

    def test_path_and_read_results_are_immutable(self) -> None:
        inspection = PathInspection("missing", None)
        result = ReadResult("too_large", None)

        with self.assertRaises(FrozenInstanceError):
            inspection.status = "ok"  # type: ignore[misc]
        with self.assertRaises(FrozenInstanceError):
            result.data = b"partial"  # type: ignore[misc]


class FilesystemProjectViewTests(unittest.TestCase):
    def project_root(self, files: dict[str, bytes] | None = None) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name) / "project"
        root.mkdir()
        for relative_path, data in (files or {}).items():
            target = root.joinpath(*PurePosixPath(relative_path).parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        return root

    def test_rejects_invalid_path_matrix_before_any_candidate_access(self) -> None:
        view: ProjectView = FilesystemProjectView(self.project_root())
        invalid_paths = (
            "",
            "/absolute.md",
            "C:/drive-qualified.md",
            "C:drive-relative.md",
            "//server/share/file.md",
            "\\\\server\\share\\file.md",
            "//?/C:/device.md",
            "//./C:/device.md",
            "\\\\?\\C:\\device.md",
            "\\\\.\\C:\\device.md",
            "folder\\windows.md",
            "file.md:alternate-stream",
            ".",
            "./file.md",
            "folder/./file.md",
            "..",
            "../file.md",
            "folder/../file.md",
            "folder//file.md",
            "folder/",
        )

        with (
            patch.object(
                Path,
                "resolve",
                side_effect=AssertionError("invalid path was resolved"),
            ),
            patch.object(
                Path,
                "stat",
                side_effect=AssertionError("invalid path was inspected"),
            ),
            patch.object(
                Path,
                "open",
                side_effect=AssertionError("invalid path was opened"),
            ),
        ):
            for relative_path in invalid_paths:
                with self.subTest(relative_path=relative_path):
                    inspection = view.inspect(relative_path)
                    result = view.read_bytes(relative_path, max_bytes=8)
                    self.assertEqual(inspection, PathInspection("invalid", None))
                    self.assertEqual(result, ReadResult("invalid", None))

    def test_reads_in_root_unicode_path_as_raw_bytes(self) -> None:
        payload = b"\xffraw bytes are not classified here"
        root = self.project_root({"\ubb38\uc11c/\uacc4\ud68d.md": payload})
        view = FilesystemProjectView(root)

        inspection = view.inspect("\ubb38\uc11c/\uacc4\ud68d.md")
        result = view.read_bytes("\ubb38\uc11c/\uacc4\ud68d.md", max_bytes=len(payload))

        self.assertEqual(inspection.status, "ok")
        self.assertEqual(
            inspection.resolved_path,
            (root / "\ubb38\uc11c/\uacc4\ud68d.md").resolve(),
        )
        self.assertEqual(result, ReadResult("ok", payload))

    def test_reports_missing_files_and_directories_without_data(self) -> None:
        root = self.project_root()
        (root / "docs").mkdir()
        view = FilesystemProjectView(root)

        self.assertEqual(view.inspect("missing.md").status, "missing")
        self.assertEqual(
            view.read_bytes("missing.md", max_bytes=8),
            ReadResult("missing", None),
        )
        self.assertEqual(view.inspect("docs").status, "not_file")
        self.assertEqual(
            view.read_bytes("docs", max_bytes=8),
            ReadResult("not_file", None),
        )

    def test_maps_resolution_stat_and_open_os_errors_to_unreadable(self) -> None:
        view = FilesystemProjectView(self.project_root({"state.md": b"state"}))

        with patch.object(Path, "resolve", side_effect=PermissionError("denied")):
            self.assertEqual(view.inspect("state.md"), PathInspection("unreadable", None))

        with patch.object(Path, "stat", side_effect=PermissionError("denied")):
            inspection = view.inspect("state.md")
            self.assertEqual(inspection.status, "unreadable")
            self.assertIsNotNone(inspection.resolved_path)

        with patch.object(Path, "open", side_effect=PermissionError("denied")):
            self.assertEqual(
                view.read_bytes("state.md", max_bytes=8),
                ReadResult("unreadable", None),
            )

    def test_read_limit_never_returns_partial_data(self) -> None:
        view = FilesystemProjectView(
            self.project_root({"exact.md": b"x" * 8, "large.md": b"x" * 9})
        )

        self.assertEqual(
            view.read_bytes("exact.md", max_bytes=8),
            ReadResult("ok", b"x" * 8),
        )
        self.assertEqual(
            view.read_bytes("large.md", max_bytes=8),
            ReadResult("too_large", None),
        )

    def test_rejects_symlink_or_junction_escape_when_host_permits(self) -> None:
        root = self.project_root()
        outside = root.parent / "outside"
        outside.mkdir()
        (outside / "secret.md").write_bytes(b"secret")
        link = root / "escape"

        if os.name == "nt":
            completed = subprocess.run(
                ["cmd.exe", "/d", "/c", "mklink", "/J", str(link), str(outside)],
                check=False,
                capture_output=True,
                text=True,
            )
            if completed.returncode != 0:
                self.skipTest("Windows junction creation was denied by the host")
            self.addCleanup(lambda: link.rmdir() if link.exists() else None)
        else:
            try:
                link.symlink_to(outside, target_is_directory=True)
            except (NotImplementedError, OSError) as exc:
                self.skipTest(f"symlink creation was denied by the host: {exc}")

        view = FilesystemProjectView(root)

        inspection = view.inspect("escape/secret.md")
        result = view.read_bytes("escape/secret.md", max_bytes=8)

        self.assertEqual(inspection.status, "outside_root")
        self.assertEqual(inspection.resolved_path, (outside / "secret.md").resolve())
        self.assertEqual(result, ReadResult("outside_root", None))

    def test_uses_path_ancestry_not_a_shared_string_prefix(self) -> None:
        root = self.project_root()
        prefix_sibling = root.parent / f"{root.name}-outside"
        prefix_sibling.mkdir()
        outside_file = prefix_sibling / "secret.md"
        outside_file.write_bytes(b"secret")
        link = root / "escape.md"
        try:
            link.symlink_to(outside_file)
        except (NotImplementedError, OSError) as exc:
            self.skipTest(f"symlink creation was denied by the host: {exc}")

        inspection = FilesystemProjectView(root).inspect("escape.md")

        self.assertEqual(inspection.status, "outside_root")

    def test_rejects_negative_read_limits(self) -> None:
        view = FilesystemProjectView(self.project_root({"state.md": b"state"}))

        with self.assertRaises(ValueError):
            view.read_bytes("state.md", max_bytes=-1)


if __name__ == "__main__":
    unittest.main()
