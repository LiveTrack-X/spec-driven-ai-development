from __future__ import annotations

import contextlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "sdad.py"


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    try:
        spec.loader.exec_module(module)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return module


def _run(
    *arguments: str,
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT), *arguments],
        cwd=cwd or ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def _write_project(
    root: Path,
    *,
    updated: str | None = None,
    state_version: int | None = 1,
    routed_docs: tuple[str, ...] = (
        "docs/TODO-Open-Items.md",
        "review-findings.md",
    ),
) -> None:
    updated_value = updated or date.today().isoformat()
    (root / "SPEC").mkdir(parents=True, exist_ok=True)
    (root / "docs").mkdir(parents=True, exist_ok=True)
    (root / "SPEC" / "SPEC-COMPLETE.md").write_text(
        "# Specification\n",
        encoding="utf-8",
    )
    (root / "review-findings.md").write_text(
        "# Review Findings\n\n## Active Findings\n\nNo active findings.\n",
        encoding="utf-8",
    )
    (root / "docs" / "TODO-Open-Items.md").write_text(
        "# TODO\n\n## Active Work\n\nNo active work.\n\n"
        "## Release / Production Readiness\n\nNo release work.\n",
        encoding="utf-8",
    )
    route_lines = "\n".join(f"  - {path}" for path in routed_docs)
    version_line = "" if state_version is None else f"version: {state_version}\n"
    state_controls = (
        "scale: standard\nexecution_scope: packet\n"
        if state_version == 2
        else "scale: standard\nintensity: low\nautonomy: 2\n"
    )
    version_two_fields = (
        "validation_for: cli-contract\n" if state_version == 2 else ""
    )
    (root / "sdad-state.yaml").write_text(
        version_line + f"updated: {updated_value}\n"
        f"{state_controls}"
        "active_spec: SPEC/SPEC-COMPLETE.md\n"
        "active_packet:\n"
        "  id: cli-contract\n"
        "  objective: Keep the control plane coherent.\n"
        "  status: in_progress\n"
        f"{version_two_fields}"
        "owner_gates: []\n"
        "validation:\n"
        "  - command: python -m unittest discover -s tests -v\n"
        "    proves: The repository test suite passes.\n"
        "routed_docs:\n"
        f"{route_lines}\n",
        encoding="utf-8",
    )


class DoctorCliSubprocessTests(unittest.TestCase):
    def test_split_and_equals_version_requirements_are_equivalent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            for arguments in (
                ("doctor", str(project), "--require-version", "3.2.1", "--json"),
                ("doctor", str(project), "--require-version=3.2.1", "--json"),
            ):
                with self.subTest(arguments=arguments):
                    result = _run(*arguments)
                    payload = json.loads(result.stdout)
                    self.assertIn(result.returncode, (0, 1))
                    self.assertEqual(result.stderr, "")
                    self.assertEqual(payload["schema_version"], 2)
                    self.assertEqual(payload["doctor_version"], "3.2.1")
                    self.assertEqual(payload["state_version"], 1)

    def test_version_requirement_is_accepted_before_or_after_project_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            cases = (
                (
                    "doctor",
                    "--require-version",
                    "3.2.1",
                    str(project),
                    "--json",
                ),
                (
                    "doctor",
                    "--require-version=3.2.1",
                    str(project),
                    "--json",
                ),
                (
                    "doctor",
                    str(project),
                    "--require-version",
                    "3.2.1",
                    "--json",
                ),
                (
                    "doctor",
                    str(project),
                    "--require-version=3.2.1",
                    "--json",
                ),
            )
            for arguments in cases:
                with self.subTest(arguments=arguments):
                    result = _run(*arguments)
                    payload = json.loads(result.stdout)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(payload["schema_version"], 2)
                    self.assertEqual(payload["root"], project.resolve().as_posix())
                    self.assertEqual(result.stderr, "")

    def test_matching_guard_preserves_human_and_strict_behavior(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, updated="2000-01-01")

            human = _run(
                "doctor",
                str(project),
                "--require-version",
                "3.2.1",
            )
            strict_json = _run(
                "doctor",
                str(project),
                "--strict",
                "--require-version=3.2.1",
                "--json",
            )

        self.assertEqual(human.returncode, 0)
        self.assertTrue(
            human.stdout.endswith(
                "Doctor: 0 errors, 1 warning, 5 checks run, 0 skipped\n"
            )
        )
        self.assertEqual(human.stderr, "")
        payload = json.loads(strict_json.stdout)
        self.assertEqual(strict_json.returncode, 1)
        self.assertTrue(payload["strict"])
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 1})
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertEqual(strict_json.stderr, "")

    def test_unknown_arguments_with_matching_guard_use_schema_two(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            cases = (
                (
                    "doctor",
                    str(project),
                    "--require-version",
                    "3.2.1",
                    "--json",
                    "--unknown",
                ),
                (
                    "doctor",
                    "--require-version=3.2.1",
                    "--unknown",
                    str(project),
                    "--json",
                ),
            )
            for arguments in cases:
                with self.subTest(arguments=arguments):
                    result = _run(*arguments)
                    payload = json.loads(result.stdout)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(payload["schema_version"], 2)
                    self.assertIsNone(payload["root"])
                    self.assertIsNone(payload["state_version"])
                    self.assertEqual(
                        payload["diagnostic_error"]["kind"],
                        "invalid_invocation",
                    )
                    self.assertEqual(result.stderr, "")

    def test_effective_state_v2_selects_schema_two_without_a_guard(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, state_version=2)

            result = _run("doctor", str(project), "--json")

        payload = json.loads(result.stdout)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["doctor_version"], "3.2.1")
        self.assertEqual(payload["state_version"], 2)
        self.assertFalse(
            {"state.schema.missing-key", "state.schema.unknown-key"}
            & {finding["id"] for finding in payload["findings"]},
            payload["findings"],
        )
        self.assertEqual(result.stderr, "")

    def test_guarded_missing_declared_version_reports_effective_v1(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, state_version=None)

            result = _run(
                "doctor",
                str(project),
                "--require-version",
                "3.2.1",
                "--json",
            )

        payload = json.loads(result.stdout)
        self.assertIn(result.returncode, (0, 1), result.stderr)
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["state_version"], 1)
        self.assertEqual(result.stderr, "")

    def test_guarded_missing_or_unsupported_state_reports_null_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            missing = base / "missing"
            unsupported = base / "unsupported"
            missing.mkdir()
            unsupported.mkdir()
            _write_project(unsupported, state_version=99)

            for project in (missing, unsupported):
                with self.subTest(project=project):
                    result = _run(
                        "doctor",
                        str(project),
                        "--require-version=3.2.1",
                        "--json",
                    )
                    payload = json.loads(result.stdout)
                    self.assertEqual(result.returncode, 1, result.stderr)
                    self.assertEqual(payload["schema_version"], 2)
                    self.assertIsNone(payload["state_version"])
                    self.assertEqual(result.stderr, "")

    def test_no_guard_legacy_and_pre_version_lanes_remain_schema_one(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            projects = {
                "declared-v1": base / "declared-v1",
                "missing-version": base / "missing-version",
                "missing-state": base / "missing-state",
                "unsupported": base / "unsupported",
            }
            for project in projects.values():
                project.mkdir()
            _write_project(projects["declared-v1"])
            _write_project(projects["missing-version"], state_version=None)
            _write_project(projects["unsupported"], state_version=99)

            for lane, project in projects.items():
                with self.subTest(lane=lane):
                    result = _run("doctor", str(project), "--json")
                    payload = json.loads(result.stdout)
                    self.assertIn(result.returncode, (0, 1), result.stderr)
                    self.assertEqual(payload["schema_version"], 1)
                    self.assertEqual(
                        list(payload),
                        [
                            "schema_version",
                            "root",
                            "strict",
                            "summary",
                            "checks",
                            "findings",
                        ],
                    )
                    self.assertEqual(result.stderr, "")

    def test_json_mode_emits_one_versioned_completed_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)

            result = _run("doctor", str(project), "--json")

        self.assertEqual(result.returncode, 0, result.stderr)
        payload = json.loads(result.stdout)
        self.assertEqual(
            list(payload),
            ["schema_version", "root", "strict", "summary", "checks", "findings"],
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["root"], project.resolve().as_posix())
        self.assertFalse(payload["strict"])
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
        self.assertEqual(
            payload["checks"],
            {
                "run": [
                    "state_schema",
                    "path_integrity",
                    "packet_coherence",
                    "owner_gates",
                    "review_state",
                ],
                "skipped": [],
            },
        )
        self.assertEqual(payload["findings"], [])
        self.assertNotIn("diagnostic_error", payload)
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.count("\n{") + result.stdout.startswith("{"),
            1,
        )

    def test_default_project_root_is_current_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)

            result = _run("doctor", "--json", cwd=project)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["root"], project.resolve().as_posix())
        self.assertEqual(result.stderr, "")

    def test_human_clean_output_is_explicit_and_uses_stdout_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)

            result = _run("doctor", str(project))

        self.assertEqual(result.returncode, 0)
        self.assertEqual(
            result.stdout,
            "Doctor: 0 errors, 0 warnings, 5 checks run, 0 skipped\n",
        )
        self.assertEqual(result.stderr, "")
        self.assertNotIn("\x1b", result.stdout)

    def test_human_finding_contains_location_observation_fix_and_summary(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, updated="2000-01-01")

            result = _run("doctor", str(project))

        self.assertEqual(result.returncode, 0)
        lines = result.stdout.splitlines()
        self.assertTrue(lines[0].startswith("WARNING state.updated.stale sdad-state.yaml:2"))
        self.assertTrue(lines[1].startswith("  Observed: "))
        self.assertTrue(lines[2].startswith("  Fix: "))
        self.assertEqual(
            lines[-1],
            "Doctor: 0 errors, 1 warning, 5 checks run, 0 skipped",
        )
        self.assertEqual(result.stderr, "")

    def test_human_error_report_exits_one_on_stdout_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, routed_docs=("docs/missing.md",))

            result = _run("doctor", str(project))

        self.assertEqual(result.returncode, 1)
        self.assertTrue(result.stdout.startswith("ERROR path.missing docs/missing.md\n"))
        self.assertTrue(
            result.stdout.endswith(
                "Doctor: 1 error, 0 warnings, 5 checks run, 0 skipped\n"
            )
        )
        self.assertEqual(result.stderr, "")

    def test_strict_fails_warning_without_reclassifying_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, updated="2000-01-01")

            result = _run("doctor", str(project), "--json", "--strict")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertTrue(payload["strict"])
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 1})
        self.assertEqual(payload["findings"][0]["severity"], "warning")
        self.assertNotIn("diagnostic_error", payload)
        self.assertEqual(result.stderr, "")

    def test_error_fails_without_strict_and_finding_shape_is_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project, routed_docs=("docs/z.md", "docs/a.md"))

            result = _run("doctor", str(project), "--json")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(payload["strict"])
        self.assertEqual(payload["summary"], {"errors": 2, "warnings": 0})
        self.assertNotIn("diagnostic_error", payload)
        self.assertEqual(
            [finding["path"] for finding in payload["findings"]],
            ["docs/a.md", "docs/z.md"],
        )
        for finding in payload["findings"]:
            self.assertEqual(
                list(finding),
                [
                    "id",
                    "severity",
                    "path",
                    "line",
                    "message",
                    "evidence",
                    "remediation",
                ],
            )
            self.assertEqual(finding["severity"], "error")
            self.assertNotIn("\\", finding["path"])
            self.assertFalse(Path(finding["path"]).is_absolute())
            self.assertIsNone(finding["line"])
            self.assertTrue(finding["message"])
            self.assertTrue(finding["evidence"])
            self.assertTrue(finding["remediation"])
        self.assertEqual(result.stderr, "")

    def test_missing_state_is_completed_exit_one_not_diagnostic_error(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run("doctor", str(project), "--json")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(payload["summary"], {"errors": 1, "warnings": 0})
        self.assertEqual(payload["findings"][0]["id"], "state.missing")
        self.assertEqual(payload["checks"]["run"], ["state_schema"])
        self.assertEqual(
            payload["checks"]["skipped"],
            ["path_integrity", "packet_coherence", "owner_gates", "review_state"],
        )
        self.assertNotIn("diagnostic_error", payload)
        self.assertEqual(result.stderr, "")

    def test_bad_root_is_exit_two_json_with_common_empty_fields(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "not-a-project"

            result = _run("doctor", str(missing), "--json")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            list(payload),
            [
                "schema_version",
                "root",
                "strict",
                "summary",
                "checks",
                "findings",
                "diagnostic_error",
            ],
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["root"], missing.resolve().as_posix())
        self.assertFalse(payload["strict"])
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
        self.assertEqual(payload["checks"], {"run": [], "skipped": []})
        self.assertEqual(payload["findings"], [])
        self.assertEqual(payload["diagnostic_error"]["kind"], "unusable_root")
        self.assertTrue(payload["diagnostic_error"]["message"])
        self.assertEqual(result.stderr, "")

    def test_invalid_json_invocation_uses_current_root_and_explicit_strict(self) -> None:
        result = _run("doctor", "--json", "--strict", "--unknown")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], ROOT.resolve().as_posix())
        self.assertTrue(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertTrue(payload["diagnostic_error"]["message"])
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
        self.assertEqual(payload["checks"], {"run": [], "skipped": []})
        self.assertEqual(payload["findings"], [])
        self.assertEqual(result.stderr, "")

    def test_invalid_option_after_explicit_root_preserves_attempted_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run(
                "doctor",
                str(project),
                "--json",
                "--strict",
                "--unknown",
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], project.resolve().as_posix())
        self.assertTrue(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")

    def test_invalid_option_before_explicit_root_preserves_attempted_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run(
                "doctor",
                "--unknown",
                str(project),
                "--json",
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], project.resolve().as_posix())
        self.assertFalse(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")

    def test_malformed_json_flag_after_root_preserves_attempted_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run("doctor", str(project), "--json=false")

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], project.resolve().as_posix())
        self.assertFalse(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.count("\n{") + result.stdout.startswith("{"),
            1,
        )

    def test_malformed_json_flag_before_root_uses_current_directory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run("doctor", "--json=false", str(project))

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], ROOT.resolve().as_posix())
        self.assertFalse(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.count("\n{") + result.stdout.startswith("{"),
            1,
        )

    def test_malformed_strict_flag_after_root_preserves_root_and_explicit_flag(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run(
                "doctor",
                str(project),
                "--json",
                "--strict=false",
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], project.resolve().as_posix())
        self.assertTrue(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.count("\n{") + result.stdout.startswith("{"),
            1,
        )

    def test_malformed_strict_flag_before_root_uses_cwd_and_stays_explicit(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            result = _run(
                "doctor",
                "--strict=false",
                str(project),
                "--json",
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(payload["root"], ROOT.resolve().as_posix())
        self.assertTrue(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")
        self.assertEqual(
            result.stdout.count("\n{") + result.stdout.startswith("{"),
            1,
        )

    def test_double_dash_json_like_root_does_not_select_json_error_output(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)

            result = _run(
                "doctor",
                "--",
                "--json=false",
                "extra",
                cwd=cwd,
            )

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertRegex(
            result.stderr,
            r"^Doctor error \[invalid_invocation\]: .+\n$",
        )

    def test_double_dash_strict_like_root_is_not_an_explicit_strict_flag(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            cwd = Path(tmp)

            result = _run(
                "doctor",
                "--json",
                "--",
                "--strict=false",
                "extra",
                cwd=cwd,
            )

        payload = json.loads(result.stdout)
        self.assertEqual(result.returncode, 2)
        self.assertEqual(
            payload["root"],
            (cwd / "--strict=false").resolve().as_posix(),
        )
        self.assertFalse(payload["strict"])
        self.assertEqual(
            payload["diagnostic_error"]["kind"],
            "invalid_invocation",
        )
        self.assertEqual(result.stderr, "")

    def test_invalid_human_invocation_uses_only_one_fatal_stderr_line(self) -> None:
        result = _run("doctor", "--unknown")

        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, "")
        self.assertRegex(
            result.stderr,
            r"^Doctor error \[invalid_invocation\]: .+\n$",
        )
        self.assertNotIn("Traceback", result.stderr)

    def test_help_is_normal_success_on_stdout(self) -> None:
        result = _run("doctor", "--help")

        self.assertEqual(result.returncode, 0)
        self.assertIn("usage:", result.stdout)
        self.assertIn("PROJECT_ROOT", result.stdout)
        self.assertIn("--require-version", result.stdout)
        self.assertEqual(result.stderr, "")


class DoctorCliBoundaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.sdad = _load_module(SCRIPT, "sdad_cli_under_test")

    def run_injected(self, project: Path, diagnose, *arguments: str):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = self.sdad.run_cli(
            ["doctor", str(project), *arguments],
            diagnose=diagnose,
            stdout=stdout,
            stderr=stderr,
        )
        return code, stdout.getvalue(), stderr.getvalue()

    def run_raw(self, *arguments: str):
        stdout = io.StringIO()
        stderr = io.StringIO()
        code = self.sdad.run_cli(
            list(arguments),
            stdout=stdout,
            stderr=stderr,
        )
        return code, stdout.getvalue(), stderr.getvalue()

    def test_version_domains_are_separate_named_constants(self) -> None:
        from sdad_validator.state_contract import SUPPORTED_STATE_VERSIONS

        self.assertEqual(self.sdad.DOCTOR_VERSION, "3.2.1")
        self.assertEqual(self.sdad.LEGACY_REPORT_SCHEMA_VERSION, 1)
        self.assertEqual(self.sdad.REPORT_SCHEMA_VERSION, 2)
        self.assertEqual(SUPPORTED_STATE_VERSIONS, frozenset({1, 2}))
        self.assertFalse(hasattr(self.sdad, "SCHEMA_VERSION"))

    def test_top_level_version_is_exact_and_never_constructs_a_project_view(
        self,
    ) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            mock.patch.object(self.sdad, "FilesystemProjectView") as view,
            mock.patch.object(
                self.sdad,
                "_path_text",
                wraps=self.sdad._path_text,
            ) as path_text,
        ):
            code = self.sdad.run_cli(["--version"], stdout=stdout, stderr=stderr)
        self.assertEqual(code, 0)
        self.assertEqual(stdout.getvalue(), "3.2.1\n")
        self.assertEqual(stderr.getvalue(), "")
        view.assert_not_called()
        path_text.assert_not_called()

    def test_mismatch_precedes_bad_root_and_never_constructs_a_view(self) -> None:
        stdout = io.StringIO()
        with (
            mock.patch.object(self.sdad, "FilesystemProjectView") as view,
            mock.patch.object(
                self.sdad,
                "_path_text",
                wraps=self.sdad._path_text,
            ) as path_text,
        ):
            code = self.sdad.run_cli(
                [
                    "doctor",
                    "Z:/does-not-exist",
                    "--json",
                    "--require-version",
                    "3.2.2",
                ],
                stdout=stdout,
                stderr=io.StringIO(),
            )
        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(payload["schema_version"], 2)
        self.assertIsNone(payload["root"])
        self.assertIsNone(payload["state_version"])
        self.assertEqual(payload["diagnostic_error"]["kind"], "version_mismatch")
        view.assert_not_called()
        path_text.assert_not_called()

    def test_malformed_and_duplicate_guards_fail_before_project_access(self) -> None:
        cases = (
            ("missing", ("--require-version",)),
            (
                "duplicate-split",
                (
                    "--require-version",
                    "3.2.1",
                    "--require-version",
                    "3.2.1",
                ),
            ),
            (
                "duplicate-equals",
                ("--require-version=3.2.1", "--require-version=3.2.1"),
            ),
            ("major-leading-zero", ("--require-version", "01.2.3")),
            ("minor-leading-zero", ("--require-version", "3.02.0")),
            ("leading-whitespace", ("--require-version", " 3.2.1")),
            ("trailing-whitespace", ("--require-version", "3.2.1 ")),
            ("range", ("--require-version", ">=3.2.1")),
            ("prerelease", ("--require-version", "3.2.1-rc.1")),
            ("build", ("--require-version", "3.2.1+build.1")),
        )
        for name, guard in cases:
            with self.subTest(name=name):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    mock.patch.object(self.sdad, "FilesystemProjectView") as view,
                    mock.patch.object(
                        self.sdad,
                        "_path_text",
                        wraps=self.sdad._path_text,
                    ) as path_text,
                ):
                    code = self.sdad.run_cli(
                        [
                            "doctor",
                            "Z:/does-not-exist",
                            *guard,
                            "--json",
                            "--strict",
                        ],
                        stdout=stdout,
                        stderr=stderr,
                    )
                payload = json.loads(stdout.getvalue())
                self.assertEqual(code, 2)
                self.assertEqual(stderr.getvalue(), "")
                self.assertEqual(payload["schema_version"], 2)
                self.assertIsNone(payload["root"])
                self.assertIsNone(payload["state_version"])
                self.assertTrue(payload["strict"])
                self.assertEqual(
                    payload["diagnostic_error"]["kind"],
                    "invalid_invocation",
                )
                view.assert_not_called()
                path_text.assert_not_called()

    def test_malformed_guard_human_output_is_one_exact_error_line(self) -> None:
        code, stdout, stderr = self.run_raw(
            "doctor",
            "--require-version",
            "3.2.1-rc.1",
        )
        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(
            stderr,
            "Doctor error [invalid_invocation]: "
            "--require-version requires core X.Y.Z\n",
        )

    def test_doctor_help_precedes_guard_validation_and_project_access(self) -> None:
        canonical_code, canonical_stdout, canonical_stderr = self.run_raw(
            "doctor",
            "--help",
        )
        self.assertEqual(canonical_code, 0)
        self.assertEqual(canonical_stderr, "")
        self.assertIn("--require-version", canonical_stdout)

        cases = (
            ("doctor", "--require-version", "--help"),
            ("doctor", "--require-version", "--json", "--help"),
            ("doctor", "--require-version", "bad", "--help"),
            ("doctor", "--help", "--require-version=bad"),
            ("doctor", "--require-version=bad", "--json", "--help"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    mock.patch.object(self.sdad, "FilesystemProjectView") as view,
                    mock.patch.object(
                        self.sdad,
                        "_path_text",
                        wraps=self.sdad._path_text,
                    ) as path_text,
                ):
                    code = self.sdad.run_cli(
                        list(arguments),
                        stdout=stdout,
                        stderr=stderr,
                    )
                self.assertEqual(code, 0)
                self.assertEqual(stdout.getvalue(), canonical_stdout)
                self.assertEqual(stderr.getvalue(), "")
                view.assert_not_called()
                path_text.assert_not_called()

    def test_double_dash_stops_doctor_help_priority(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        error = self.sdad.DiagnosticError(
            "unusable_root",
            "The project root does not exist.",
        )
        with mock.patch.object(
            self.sdad,
            "FilesystemProjectView",
            side_effect=error,
        ) as view:
            code = self.sdad.run_cli(
                ["doctor", "--", "--help"],
                stdout=stdout,
                stderr=stderr,
            )
        self.assertEqual(code, 2)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            stderr.getvalue(),
            "Doctor error [unusable_root]: The project root does not exist.\n",
        )
        view.assert_called_once_with("--help")

    def test_version_token_combinations_are_invalid_before_help(self) -> None:
        cases = (
            ("--version", "--help"),
            ("--version", "doctor"),
            ("doctor", "--version"),
            ("doctor", "--version", "--help"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with mock.patch.object(self.sdad, "FilesystemProjectView") as view:
                    code = self.sdad.run_cli(
                        list(arguments),
                        stdout=stdout,
                        stderr=stderr,
                    )
                self.assertEqual(code, 2)
                self.assertEqual(stdout.getvalue(), "")
                self.assertRegex(
                    stderr.getvalue(),
                    r"^Doctor error \[invalid_invocation\]: .+\n$",
                )
                view.assert_not_called()

    def test_guard_outside_doctor_lane_is_never_a_version_mismatch(self) -> None:
        cases = (
            ("--require-version", "3.2.1", "--json"),
            ("--require-version=3.2.1", "--json"),
            ("--require-version", "3.2.1", "doctor", "--json"),
            ("--help", "--require-version=3.2.1", "--json"),
        )
        for arguments in cases:
            with self.subTest(arguments=arguments):
                stdout = io.StringIO()
                stderr = io.StringIO()
                with mock.patch.object(self.sdad, "FilesystemProjectView") as view:
                    code = self.sdad.run_cli(
                        list(arguments),
                        stdout=stdout,
                        stderr=stderr,
                    )
                payload = json.loads(stdout.getvalue())
                self.assertEqual(code, 2)
                self.assertEqual(stderr.getvalue(), "")
                self.assertEqual(payload["schema_version"], 1)
                self.assertEqual(
                    payload["diagnostic_error"]["kind"],
                    "invalid_invocation",
                )
                view.assert_not_called()

    def test_report_schema_selection_matrix_is_exact(self) -> None:
        cases = (
            (False, None, 1),
            (False, 1, 1),
            (False, 2, 2),
            (True, None, 2),
            (True, 1, 2),
            (True, 2, 2),
        )
        for guard_present, state_version, expected in cases:
            with self.subTest(
                guard_present=guard_present,
                state_version=state_version,
            ):
                self.assertEqual(
                    self.sdad._select_report_schema(
                        guard_present=guard_present,
                        state_version=state_version,
                    ),
                    expected,
                )

    def test_schema_one_completed_shape_and_key_order_remain_exact(self) -> None:
        report = self.sdad.DoctorReport(
            root="C:/project",
            findings=(),
            checks_run=("state_schema",),
            checks_skipped=(),
            error_count=0,
            warning_count=0,
            state_version=1,
        )
        payload = self.sdad._completed_payload(report, False, 1)
        self.assertEqual(
            list(payload),
            ["schema_version", "root", "strict", "summary", "checks", "findings"],
        )
        self.assertEqual(payload["schema_version"], 1)
        self.assertNotIn("doctor_version", payload)
        self.assertNotIn("state_version", payload)

    def test_schema_two_completed_shape_and_key_order_are_exact(self) -> None:
        report = self.sdad.DoctorReport(
            root="C:/project",
            findings=(),
            checks_run=("state_schema",),
            checks_skipped=(),
            error_count=0,
            warning_count=0,
            state_version=2,
        )
        payload = self.sdad._completed_payload(report, False, 2)
        self.assertEqual(
            list(payload),
            [
                "schema_version",
                "doctor_version",
                "state_version",
                "root",
                "strict",
                "summary",
                "checks",
                "findings",
            ],
        )
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["doctor_version"], "3.2.1")
        self.assertEqual(payload["state_version"], 2)

    def test_no_guard_error_after_effective_v2_uses_schema_two(self) -> None:
        def fail_after_state(_view: object, _policy: object):
            raise self.sdad.DiagnosticError(
                "internal_error",
                "failed",
                state_version=2,
            )

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            code, stdout, stderr = self.run_injected(
                project,
                fail_after_state,
                "--json",
            )
        payload = json.loads(stdout)
        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["state_version"], 2)
        self.assertEqual(payload["root"], project.resolve().as_posix())

    def test_no_guard_error_before_v2_remains_schema_one(self) -> None:
        for state_version in (None, 1):
            with self.subTest(state_version=state_version):
                def fail_before_v2(
                    _view: object,
                    _policy: object,
                    *,
                    _state_version=state_version,
                ):
                    raise self.sdad.DiagnosticError(
                        "internal_error",
                        "failed",
                        state_version=_state_version,
                    )

                with tempfile.TemporaryDirectory() as tmp:
                    project = Path(tmp)
                    _write_project(project)
                    code, stdout, stderr = self.run_injected(
                        project,
                        fail_before_v2,
                        "--json",
                    )
                payload = json.loads(stdout)
                self.assertEqual(code, 2)
                self.assertEqual(stderr, "")
                self.assertEqual(payload["schema_version"], 1)
                self.assertEqual(
                    list(payload),
                    [
                        "schema_version",
                        "root",
                        "strict",
                        "summary",
                        "checks",
                        "findings",
                        "diagnostic_error",
                    ],
                )

    def test_explicit_guard_selects_schema_two_for_v1_post_acceptance_error(
        self,
    ) -> None:
        def fail(_view: object, _policy: object):
            raise self.sdad.DiagnosticError(
                "unreadable_state",
                "failed",
                state_version=1,
            )

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            code, stdout, stderr = self.run_injected(
                project,
                fail,
                "--json",
                "--require-version",
                "3.2.1",
            )
        payload = json.loads(stdout)
        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        self.assertEqual(payload["schema_version"], 2)
        self.assertEqual(payload["state_version"], 1)
        self.assertEqual(payload["root"], project.resolve().as_posix())

    def test_schema_two_exit_two_shape_and_nested_order_are_exact(self) -> None:
        def fail(_view: object, _policy: object):
            raise self.sdad.DiagnosticError(
                "internal_error",
                "failed",
                state_version=2,
            )

        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            code, stdout, stderr = self.run_injected(project, fail, "--json")
        payload = json.loads(stdout)
        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        self.assertEqual(
            list(payload),
            [
                "schema_version",
                "doctor_version",
                "state_version",
                "root",
                "strict",
                "summary",
                "checks",
                "findings",
                "diagnostic_error",
            ],
        )
        self.assertEqual(
            list(payload["diagnostic_error"]),
            ["kind", "message"],
        )
        self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
        self.assertEqual(payload["checks"], {"run": [], "skipped": []})
        self.assertEqual(payload["findings"], [])

    def test_guarded_unusable_root_uses_null_pre_acceptance_fields(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        error = self.sdad.DiagnosticError(
            "unusable_root",
            "The project root does not exist.",
        )
        with mock.patch.object(
            self.sdad,
            "FilesystemProjectView",
            side_effect=error,
        ):
            code = self.sdad.run_cli(
                [
                    "doctor",
                    "Z:/does-not-exist",
                    "--require-version=3.2.1",
                    "--json",
                ],
                stdout=stdout,
                stderr=stderr,
            )
        payload = json.loads(stdout.getvalue())
        self.assertEqual(code, 2)
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(payload["schema_version"], 2)
        self.assertIsNone(payload["root"])
        self.assertIsNone(payload["state_version"])
        self.assertEqual(payload["diagnostic_error"]["kind"], "unusable_root")

    def test_injected_permitted_diagnostic_errors_have_exact_json_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)
            for kind in (
                "invalid_invocation",
                "unusable_root",
                "unreadable_state",
                "internal_error",
            ):
                with self.subTest(kind=kind):
                    message = f"Injected {kind} boundary."

                    def diagnose(_view, _policy, *, _kind=kind, _message=message):
                        raise self.sdad.DiagnosticError(_kind, _message)

                    code, stdout, stderr = self.run_injected(
                        project,
                        diagnose,
                        "--json",
                        "--strict",
                    )

                    payload = json.loads(stdout)
                    self.assertEqual(code, 2)
                    self.assertEqual(stderr, "")
                    self.assertEqual(payload["root"], project.resolve().as_posix())
                    self.assertTrue(payload["strict"])
                    self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
                    self.assertEqual(payload["checks"], {"run": [], "skipped": []})
                    self.assertEqual(payload["findings"], [])
                    self.assertEqual(
                        payload["diagnostic_error"],
                        {"kind": kind, "message": message},
                    )

    def test_unexpected_boundary_exception_is_internal_error_without_traceback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            _write_project(project)

            def explode(_view, _policy):
                raise RuntimeError("sensitive implementation detail")

            code, stdout, stderr = self.run_injected(project, explode, "--json")

        payload = json.loads(stdout)
        self.assertEqual(code, 2)
        self.assertEqual(stderr, "")
        self.assertEqual(payload["diagnostic_error"]["kind"], "internal_error")
        self.assertTrue(payload["diagnostic_error"]["message"])
        self.assertNotIn("sensitive implementation detail", stdout)
        self.assertNotIn("Traceback", stdout)

    def test_diagnosis_runs_exactly_once_for_human_and_json_rendering(self) -> None:
        for arguments in ((), ("--json",)):
            with self.subTest(arguments=arguments):
                calls = 0

                def diagnose(view, _policy):
                    nonlocal calls
                    calls += 1
                    return self.sdad.DoctorReport(
                        root=view.root.as_posix(),
                        findings=(),
                        checks_run=("state_schema",),
                        checks_skipped=("path_integrity",),
                        error_count=0,
                        warning_count=0,
                    )

                with tempfile.TemporaryDirectory() as tmp:
                    project = Path(tmp)
                    code, stdout, stderr = self.run_injected(
                        project,
                        diagnose,
                        *arguments,
                    )

                self.assertEqual(code, 0)
                self.assertEqual(calls, 1)
                self.assertEqual(stderr, "")
                if arguments:
                    self.assertEqual(
                        json.loads(stdout)["summary"],
                        {"errors": 0, "warnings": 0},
                    )
                else:
                    self.assertEqual(
                        stdout,
                        "Doctor: 0 errors, 0 warnings, 1 check run, 1 skipped\n",
                    )

    def test_json_render_or_exit_failure_becomes_one_internal_error_document(
        self,
    ) -> None:
        for failure in ("payload", "exit"):
            with (
                self.subTest(failure=failure),
                tempfile.TemporaryDirectory() as tmp,
            ):
                project = Path(tmp)

                def malformed(view, _policy):
                    return self.sdad.DoctorReport(
                        root=(
                            None
                            if failure == "payload"
                            else view.root.as_posix()
                        ),
                        findings=(),
                        checks_run=("state_schema",),
                        checks_skipped=(),
                        error_count=(None if failure == "exit" else 0),
                        warning_count=0,
                    )

                code, stdout, stderr = self.run_injected(
                    project,
                    malformed,
                    "--json",
                )

                payload = json.loads(stdout)
                self.assertEqual(code, 2)
                self.assertEqual(stderr, "")
                self.assertEqual(payload["summary"], {"errors": 0, "warnings": 0})
                self.assertEqual(payload["checks"], {"run": [], "skipped": []})
                self.assertEqual(payload["findings"], [])
                self.assertEqual(
                    payload["diagnostic_error"]["kind"],
                    "internal_error",
                )
                self.assertNotIn('"errors": null', stdout)
                self.assertEqual(
                    stdout.count("\n{") + stdout.startswith("{"),
                    1,
                )

    def test_human_render_or_exit_failure_is_fatal_without_partial_report(
        self,
    ) -> None:
        for failure in ("render", "exit"):
            with (
                self.subTest(failure=failure),
                tempfile.TemporaryDirectory() as tmp,
            ):
                project = Path(tmp)

                def malformed(view, _policy):
                    return self.sdad.DoctorReport(
                        root=view.root.as_posix(),
                        findings=((object(),) if failure == "render" else ()),
                        checks_run=("state_schema",),
                        checks_skipped=(),
                        error_count=(None if failure == "exit" else 0),
                        warning_count=0,
                    )

                code, stdout, stderr = self.run_injected(project, malformed)

                self.assertEqual(code, 2)
                self.assertEqual(stdout, "")
                self.assertEqual(
                    stderr,
                    "Doctor error [internal_error]: "
                    "The diagnostic could not be completed.\n",
                )
                self.assertNotIn("Doctor: None errors", stderr)

    def test_human_exit_two_is_one_exact_fatal_line(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)

            def diagnose(_view, _policy):
                raise self.sdad.DiagnosticError(
                    "unreadable_state",
                    "The state file cannot be opened.",
                )

            code, stdout, stderr = self.run_injected(project, diagnose)

        self.assertEqual(code, 2)
        self.assertEqual(stdout, "")
        self.assertEqual(
            stderr,
            "Doctor error [unreadable_state]: The state file cannot be opened.\n",
        )


class DoctorRepositoryContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.validator = _load_module(
            ROOT / "scripts" / "validate_repo.py",
            "validate_repo_for_doctor_contract",
        )

    def test_required_files_register_every_task_one_through_four_artifact(self) -> None:
        expected = {
            "scripts/sdad.py",
            "scripts/sdad_validator/__init__.py",
            "scripts/sdad_validator/agent_experience.py",
            "scripts/sdad_validator/state_contract.py",
            "scripts/sdad_validator/diagnostics.py",
            "scripts/sdad_validator/project_view.py",
            "scripts/sdad_validator/doctor.py",
            "scripts/sdad_validator/checks/__init__.py",
            "scripts/sdad_validator/checks/state_schema.py",
            "scripts/sdad_validator/checks/path_integrity.py",
            "scripts/sdad_validator/checks/packet_coherence.py",
            "scripts/sdad_validator/checks/owner_gates.py",
            "scripts/sdad_validator/checks/review_state.py",
            "tests/test_agent_experience_contracts.py",
            "tests/test_state_contract.py",
            "tests/test_project_view.py",
            "tests/test_doctor_checks.py",
            "tests/test_sdad_cli.py",
        }
        self.assertEqual(expected - set(self.validator.REQUIRED_FILES), set())

    def write_contract_surfaces(
        self,
        root: Path,
        *,
        advertised_path: str | None = None,
        marker: str | None = None,
    ) -> None:
        (root / "scripts").mkdir(parents=True)
        (root / "docs").mkdir(parents=True)
        (root / "scripts" / "sdad.py").write_text(
            '"""Checkout-only, read-only SDAD doctor."""\n'
            'DOCTOR_VERSION = "3.2.1"\n'
            "LEGACY_REPORT_SCHEMA_VERSION = 1\n"
            "REPORT_SCHEMA_VERSION = 2\n",
            encoding="utf-8",
        )
        surfaces = {
            "scripts/install-agent-adapter.ps1": "Install adapter only.\n",
            "scripts/install-agent-adapter.sh": "Install adapter only.\n",
            "docs/no-clone-quick-install.md": "# No-Clone\n\nInstall adapters only.\n",
        }
        if advertised_path is not None:
            surfaces[advertised_path] = marker or "Run sdad doctor now.\n"
        for path, content in surfaces.items():
            (root / path).write_text(content, encoding="utf-8")

    def test_checkout_only_contract_accepts_unadvertised_read_only_cli(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_contract_surfaces(root)
            with mock.patch.object(self.validator, "ROOT", root):
                self.validator.validate_doctor_checkout_contract()

    def test_checkout_only_contract_rejects_missing_or_generic_version_domains(
        self,
    ) -> None:
        replacements = (
            ('DOCTOR_VERSION = "3.2.1"', 'DOCTOR_VERSION = "3.2.2"'),
            ("LEGACY_REPORT_SCHEMA_VERSION = 1", "LEGACY_REPORT_SCHEMA_VERSION = 2"),
            ("REPORT_SCHEMA_VERSION = 2", "REPORT_SCHEMA_VERSION = 1"),
            (
                "REPORT_SCHEMA_VERSION = 2",
                "REPORT_SCHEMA_VERSION = 2\nSCHEMA_VERSION = 1",
            ),
        )
        for old, new in replacements:
            with self.subTest(replacement=new), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_contract_surfaces(root)
                cli = root / "scripts" / "sdad.py"
                cli.write_text(
                    cli.read_text(encoding="utf-8").replace(old, new, 1),
                    encoding="utf-8",
                )
                with mock.patch.object(self.validator, "ROOT", root):
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            self.validator.validate_doctor_checkout_contract()

    def test_checkout_only_contract_rejects_every_surface_and_marker(self) -> None:
        for path in (
            "scripts/install-agent-adapter.ps1",
            "scripts/install-agent-adapter.sh",
            "docs/no-clone-quick-install.md",
        ):
            for marker in ("Run sdad doctor now.\n", "Install scripts/sdad.py.\n"):
                with (
                    self.subTest(path=path, marker=marker),
                    tempfile.TemporaryDirectory() as tmp,
                ):
                    root = Path(tmp)
                    self.write_contract_surfaces(
                        root,
                        advertised_path=path,
                        marker=marker,
                    )
                    with mock.patch.object(self.validator, "ROOT", root):
                        with contextlib.redirect_stderr(io.StringIO()):
                            with self.assertRaises(SystemExit):
                                self.validator.validate_doctor_checkout_contract()


if __name__ == "__main__":
    unittest.main()
