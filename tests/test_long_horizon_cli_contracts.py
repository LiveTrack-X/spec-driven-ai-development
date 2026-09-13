from __future__ import annotations

import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad import run_cli  # noqa: E402
from sdad_validator.diagnostics import DoctorReport  # noqa: E402


class LongHorizonCliContractTests(unittest.TestCase):
    @staticmethod
    def _clean_report(root: str, state_version: int = 2) -> DoctorReport:
        return DoctorReport(
            root=root,
            findings=(),
            checks_run=(
                "state_schema",
                "path_integrity",
                "packet_coherence",
                "owner_gates",
                "review_state",
            ),
            checks_skipped=(),
            error_count=0,
            warning_count=0,
            state_version=state_version,
        )

    def test_tilde_roots_are_expanded_for_both_access_and_reporting(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home with spaces"
            project = home / "nested" / "project"
            project.mkdir(parents=True)
            captured_roots: list[str] = []

            def diagnose(view, _policy):
                captured_roots.append(view.root.as_posix())
                return self._clean_report(view.root.as_posix())

            environment = {
                "HOME": str(home),
                "USERPROFILE": str(home),
                "HOMEDRIVE": home.drive,
                "HOMEPATH": str(home)[len(home.drive) :],
            }
            with patch.dict(os.environ, environment, clear=False):
                stdout = io.StringIO()
                stderr = io.StringIO()
                exit_code = run_cli(
                    ["doctor", "~/nested/project", "--json"],
                    diagnose=diagnose,
                    stdout=stdout,
                    stderr=stderr,
                )

            expected = project.resolve().as_posix()
            self.assertEqual(exit_code, 0)
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(captured_roots, [expected])
            self.assertEqual(json.loads(stdout.getvalue())["root"], expected)

    def test_missing_tilde_root_reports_the_same_expanded_path_it_attempted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / "home~1"
            home.mkdir()
            environment = {
                "HOME": str(home),
                "USERPROFILE": str(home),
                "HOMEDRIVE": home.drive,
                "HOMEPATH": str(home)[len(home.drive) :],
            }
            with patch.dict(os.environ, environment, clear=False):
                stdout = io.StringIO()
                stderr = io.StringIO()
                exit_code = run_cli(
                    ["doctor", "~/missing", "--json"],
                    stdout=stdout,
                    stderr=stderr,
                )

            payload = json.loads(stdout.getvalue())
            self.assertEqual(exit_code, 2)
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(payload["root"], (home / "missing").resolve().as_posix())
            self.assertEqual(
                payload["diagnostic_error"]["kind"],
                "unusable_root",
            )
            # Windows short paths may legitimately contain a tilde. Reject the
            # unexpanded input, not a character in the expanded directory name.
            self.assertNotIn("~/missing", payload["diagnostic_error"]["message"])
            self.assertIn(str(home / "missing"), payload["diagnostic_error"]["message"])

    def test_repeated_mixed_root_invocations_do_not_reuse_prior_cli_state(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            roots = [Path(tmp) / f"project-{index:02d}" for index in range(32)]
            for root in roots:
                root.mkdir()

            observed: list[str] = []

            def diagnose(view, _policy):
                observed.append(view.root.as_posix())
                return self._clean_report(view.root.as_posix())

            for index, root in enumerate(roots):
                stdout = io.StringIO()
                stderr = io.StringIO()
                arguments = ["doctor", str(root)]
                if index % 2:
                    arguments.append("--json")
                exit_code = run_cli(
                    arguments,
                    diagnose=diagnose,
                    stdout=stdout,
                    stderr=stderr,
                )
                self.assertEqual(exit_code, 0)
                self.assertEqual(stderr.getvalue(), "")
                if index % 2:
                    self.assertEqual(
                        json.loads(stdout.getvalue())["root"],
                        root.resolve().as_posix(),
                    )
                else:
                    self.assertTrue(stdout.getvalue().startswith("Doctor: 0 errors"))

            self.assertEqual(observed, [root.resolve().as_posix() for root in roots])

    def test_repository_validator_rejects_unknown_arguments_before_validation(self) -> None:
        completed = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS / "validate_repo.py"),
                "--definitely-invalid",
                "value",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(completed.returncode, 1)
        self.assertEqual(completed.stdout, "")
        self.assertEqual(
            completed.stderr,
            "ERROR: validate_repo.py does not accept arguments: "
            "--definitely-invalid value\n",
        )
        self.assertNotIn("Traceback", completed.stderr)


if __name__ == "__main__":
    unittest.main()
