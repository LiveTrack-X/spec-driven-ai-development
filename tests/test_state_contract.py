from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.state_contract import (  # noqa: E402
    collect_template_state_violations,
    inspect_state,
    is_normalized_relative_posix_path,
)


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def valid_state() -> str:
    return read("templates/project-control-files/sdad-state.yaml")


class StateContractTests(unittest.TestCase):
    def test_parses_the_canonical_state_subset(self) -> None:
        result = inspect_state(valid_state())

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(result.snapshot.scalar("scale").value, "standard")
        self.assertEqual(result.snapshot.active_packet["status"].value, "not_started")
        self.assertEqual(result.snapshot.owner_gates, ())
        self.assertEqual(result.snapshot.validation[0].fields["command"].line, 22)
        self.assertEqual(
            [item.value for item in result.snapshot.routed_docs],
            ["docs/TODO-Open-Items.md", "review-findings.md"],
        )

    def test_rejects_unsupported_syntax_without_partial_state(self) -> None:
        result = inspect_state("scale: standard\nvalidation: &shared []\n")

        self.assertIsNone(result.snapshot)
        self.assertEqual(result.issues[0].id, "state.syntax.unsupported")
        self.assertEqual(result.issues[0].line, 2)
        self.assertIsNone(result.issues[0].legacy_message)

    def test_rejects_each_unsupported_yaml_form(self) -> None:
        cases = {
            "tab indentation": "active_packet:\n\tid: packet-1\n",
            "anchor": "validation: &shared []\n",
            "alias": "validation: *shared\n",
            "tag": "scale: !custom standard\n",
            "multiline literal": "active_packet:\n  objective: |\n    text\n",
            "multiline folded": "active_packet:\n  objective: >\n    text\n",
            "unsupported indentation": "active_packet:\n    id: packet-1\n",
            "flow list": "owner_gates: [owner-review]\n",
            "flow mapping": "active_packet: {}\n",
            "merge key": "active_packet:\n  <<: *shared\n",
        }

        for label, text in cases.items():
            with self.subTest(label=label):
                result = inspect_state(text)
                self.assertIsNone(result.snapshot)
                self.assertEqual(result.issues[0].id, "state.syntax.unsupported")

    def test_parses_plain_single_and_double_quoted_scalars_and_comments(self) -> None:
        text = (
            "version: 1\n"
            "updated: '2026-07-10' # outside comment\n"
            "scale: \"standard\"\n"
            "intensity: 'medium'\n"
            "autonomy: 2\n"
            "active_spec: 'SPEC/#draft.md' # keep hash in quotes\n"
            "active_packet:\n"
            "  id: plain-id # outside comment\n"
            "  objective: \"quoted # objective\" # outside comment\n"
            "  status: 'not_started'\n"
            "owner_gates: []\n"
            "validation: []\n"
            "routed_docs: []\n"
        )

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(result.snapshot.scalar("updated").value, "2026-07-10")
        self.assertEqual(result.snapshot.scalar("active_spec").value, "SPEC/#draft.md")
        self.assertEqual(
            result.snapshot.active_packet["objective"].value,
            "quoted # objective",
        )

    def test_parses_scalar_lists_and_validation_mapping_lists(self) -> None:
        text = valid_state().replace(
            "owner_gates: []",
            "owner_gates:\n"
            "  - owner approval\n"
            "  - 'hardware # review' # outside comment",
        )

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(
            [(value.value, value.line) for value in result.snapshot.owner_gates],
            [("owner approval", 19), ("hardware # review", 20)],
        )
        self.assertEqual(len(result.snapshot.validation), 1)
        self.assertEqual(result.snapshot.validation[0].line, 24)
        self.assertEqual(
            result.snapshot.validation[0].fields["proves"].value,
            "Replace with the claim this command supports.",
        )

    def test_parses_empty_list_form_for_each_supported_list(self) -> None:
        text = valid_state().replace(
            "validation:\n"
            "  - command: Replace with the project validation command.\n"
            "    proves: Replace with the claim this command supports.",
            "validation: []",
        ).replace(
            "routed_docs:\n"
            "  - docs/TODO-Open-Items.md\n"
            "  - review-findings.md",
            "routed_docs: []",
        )

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(result.snapshot.owner_gates, ())
        self.assertEqual(result.snapshot.validation, ())
        self.assertEqual(result.snapshot.routed_docs, ())

    def test_reports_duplicate_keys_at_the_duplicate_source_lines(self) -> None:
        text = (
            valid_state()
            .replace("scale: standard", "scale: standard\nscale: full")
            .replace(
                "  status: not_started",
                "  status: not_started\n  status: blocked",
            )
            .replace(
                "    proves: Replace with the claim this command supports.",
                "    proves: first\n    proves: second",
            )
        )

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        duplicates = [
            issue for issue in result.issues if issue.id == "state.schema.duplicate-key"
        ]
        self.assertEqual(
            [(issue.evidence, issue.line) for issue in duplicates],
            [("scale", 6), ("status", 17), ("proves", 26)],
        )

    def test_blank_top_level_value_keeps_the_key_source_line(self) -> None:
        result = inspect_state("scale:\n")

        scale_issue = next(
            issue
            for issue in result.issues
            if issue.legacy_message == "sdad-state.yaml missing scalar value: scale"
        )
        self.assertEqual(scale_issue.line, 1)

    def test_valid_subset_returns_a_snapshot_when_schema_is_invalid(self) -> None:
        result = inspect_state(valid_state().replace("scale: standard", "scale: huge"))

        self.assertIsNotNone(result.snapshot)
        unsupported = next(
            issue
            for issue in result.issues
            if issue.id == "state.schema.unsupported-value"
            and issue.evidence == "huge"
        )
        self.assertEqual(unsupported.line, 5)
        self.assertEqual(unsupported.legacy_message, "unsupported scale: huge")

    def test_only_existing_repository_contract_issues_have_legacy_messages(self) -> None:
        text = valid_state().replace("version: 1\n", "extra: value\n")

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        missing_version = next(
            issue
            for issue in result.issues
            if issue.id == "state.schema.missing-version"
        )
        unknown_key = next(
            issue
            for issue in result.issues
            if issue.id == "state.schema.unknown-key"
        )
        self.assertIsNone(missing_version.legacy_message)
        self.assertIsNone(unknown_key.legacy_message)

    def test_preserves_existing_violation_text(self) -> None:
        text = valid_state().replace("scale: standard", "scale: huge")

        self.assertIn(
            "unsupported scale: huge",
            collect_template_state_violations(text),
        )

    def test_empty_template_text_keeps_missing_file_compatibility(self) -> None:
        self.assertEqual(collect_template_state_violations(""), [])

    def test_preserves_existing_violation_order(self) -> None:
        text = (
            "scale: huge\n"
            "scale: huge\n"
            "autonomy: 9\n"
            "active_spec: ../outside.md\n"
            "active_packet:\n"
            "  id: packet-1\n"
            "  status: invented\n"
            "  status: invented\n"
            "owner_gates: disabled\n"
            "validation: true\n"
            "routed_docs: all\n"
        )

        self.assertEqual(
            collect_template_state_violations(text),
            [
                "sdad-state.yaml duplicate top-level key: scale",
                "sdad-state.yaml missing top-level key: intensity",
                "unsupported scale: huge",
                "unsupported autonomy: 9",
                "sdad-state.yaml active_spec must be a relative path: ../outside.md",
                "sdad-state.yaml owner_gates must be a list",
                "sdad-state.yaml validation must be a list",
                "sdad-state.yaml routed_docs must be a list",
                "sdad-state.yaml active_packet duplicate key: status",
                "sdad-state.yaml active_packet missing key: objective",
                "unsupported active_packet status: invented",
            ],
        )

    def test_normalized_relative_posix_path_contract(self) -> None:
        for value in (
            "SPEC/SPEC-COMPLETE.md",
            "docs/TODO-Open-Items.md",
            "unicode/\ud14c\uc2a4\ud2b8.md",
        ):
            with self.subTest(value=value):
                self.assertTrue(is_normalized_relative_posix_path(value))

        for value in (
            "",
            "/absolute.md",
            "C:/drive.md",
            "docs\\windows.md",
            "../outside.md",
            "docs/./file.md",
            "docs//file.md",
            "./file.md",
        ):
            with self.subTest(value=value):
                self.assertFalse(is_normalized_relative_posix_path(value))


if __name__ == "__main__":
    unittest.main()
