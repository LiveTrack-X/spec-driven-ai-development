"""Deletion regressions for routing guidance; live behavior is evaluated separately."""
from __future__ import annotations

import contextlib
import io
from pathlib import Path
import sys
import unittest
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import validate_repo as validator


class WorkflowClarityTests(unittest.TestCase):
    def test_current_guidance_contract(self):
        validator.validate_workflow_clarity_contract()

    def test_missing_safety_and_reuse_boundaries_fail(self):
        cases = (
            ("docs/INDEX.md", "Repairs cannot\nbypass gates.", "Repairs may bypass gates."),
            ("docs/INDEX.md", "Questions permit no writes.", "Questions permit writes."),
            ("docs/Repository-Operating-Rules.md", "keep that criterion incomplete", "ignore that criterion"),
            ("docs/Repository-Operating-Rules.md", "Never narrow acceptance", "Narrow acceptance"),
            ("docs/sdad/playbooks/documentation-and-handoff.md", "Do not label a reused result as a new run.", "Label reused results as new runs."),
            ("docs/sdad/playbooks/documentation-and-handoff.md", "dirty work needs", "all work needs"),
            ("docs/sdad/playbooks/evidence-and-risk-gates.md", "do not assume no impact", "assume no impact"),
            ("docs/sdad/playbooks/evidence-and-risk-gates.md", "never waives", "waives"),
        )
        original_read = validator.read
        for suffix, old, new in cases:
            path = "templates/project-control-files/" + suffix
            content = original_read(path)
            self.assertIn(old, content)
            with self.subTest(boundary=old):
                with mock.patch.object(validator, "read", side_effect=lambda p: content.replace(old, new) if p == path else original_read(p)):
                    with contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                        validator.validate_workflow_clarity_contract()

    def test_reporting_omits_ritual_without_omitting_evidence_limits(self):
        content = validator.read("templates/project-control-files/AGENTS.md")
        self.assertIn("omit phase N/A lists", content)
        self.assertIn("never claim evidence from skipped work", content)
        self.assertIn("not in every reply", content)


if __name__ == "__main__":
    unittest.main()
