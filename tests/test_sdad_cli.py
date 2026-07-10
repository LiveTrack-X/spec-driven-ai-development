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
    spec.loader.exec_module(module)
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
    (root / "sdad-state.yaml").write_text(
        "version: 1\n"
        f"updated: {updated_value}\n"
        "scale: standard\n"
        "intensity: low\n"
        "autonomy: 2\n"
        "active_spec: SPEC/SPEC-COMPLETE.md\n"
        "active_packet:\n"
        "  id: cli-contract\n"
        "  objective: Keep the control plane coherent.\n"
        "  status: in_progress\n"
        "owner_gates: []\n"
        "validation:\n"
        "  - command: python -m unittest discover -s tests -v\n"
        "    proves: The repository test suite passes.\n"
        "routed_docs:\n"
        f"{route_lines}\n",
        encoding="utf-8",
    )


class DoctorCliSubprocessTests(unittest.TestCase):
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
            "SCHEMA_VERSION = 1\n",
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
