from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.state_contract import (  # noqa: E402
    KNOWN_TOP_LEVEL_KEYS_BY_VERSION,
    REQUIRED_TOP_LEVEL_KEYS_BY_VERSION,
    STATE_ENUMS_BY_VERSION,
    V1_STATE_KEYS,
    V2_STATE_KEYS,
    collect_template_state_violations,
    inspect_state,
    is_normalized_relative_posix_path,
    is_valid_v2_packet_id,
)


V1_STATE = """version: 1
updated: YYYY-MM-DD

# one-shot | mini | standard | full
scale: standard
# low | medium | high
intensity: medium
# 0 = ask-first, 1 = unit, 2 = work packet, 3 = session, 4 = owner-gated risk
autonomy: 2

active_spec: SPEC/SPEC-COMPLETE.md
active_packet:
  id: bootstrap
  objective: Replace with the current evidence-ready objective.
  status: not_started

# Keep only gates that can stop the current packet.
owner_gates: []

# Keep commands short and runnable from the repository root.
validation:
  - command: Replace with the project validation command.
    proves: Replace with the claim this command supports.

# List only documents needed by the current packet.
routed_docs:
  - docs/TODO-Open-Items.md
  - review-findings.md
"""

V2_STATE = """version: 2
updated: YYYY-MM-DD

# state v2: standard | full
scale: standard
# unit | packet
execution_scope: packet

active_spec: SPEC/SPEC-COMPLETE.md
active_packet:
  id: bootstrap
  objective: Replace with the current evidence-ready objective.
  status: not_started
validation_for: bootstrap

# Keep only gates that can stop the current packet.
owner_gates: []

# Keep commands short and runnable from the repository root.
validation:
  - command: Replace with the project validation command.
    proves: Replace with the claim this command supports.

# List only documents needed by the current packet.
routed_docs:
  - docs/TODO-Open-Items.md
  - review-findings.md
"""


def valid_v1_state() -> str:
    return V1_STATE


def valid_v2_state() -> str:
    return V2_STATE


class StateContractTests(unittest.TestCase):
    def test_parses_the_canonical_state_subset(self) -> None:
        result = inspect_state(valid_v1_state())

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

    def test_missing_version_is_effective_v1_and_declared_versions_dispatch(self) -> None:
        missing = inspect_state(valid_v1_state().replace("version: 1\n", ""))
        self.assertEqual(missing.state_version, 1)
        self.assertIn("state.schema.missing-version", [issue.id for issue in missing.issues])

        self.assertEqual(inspect_state(valid_v1_state()).state_version, 1)
        self.assertEqual(inspect_state(valid_v2_state()).state_version, 2)

        future = inspect_state(valid_v1_state().replace("version: 1", "version: 99"))
        self.assertIsNone(future.state_version)
        self.assertIn("state.schema.unsupported-version", [issue.id for issue in future.issues])

    def test_v2_requires_validation_owner_and_rejects_stateless_scales(self) -> None:
        baseline = valid_v2_state()
        cases = {
            "state.schema.missing-key": baseline.replace(
                "validation_for: bootstrap\n", ""
            ),
            "state.schema.wrong-kind": baseline.replace(
                "validation_for: bootstrap", "validation_for:\n  nested: value"
            ),
            "state.schema.unsupported-value": baseline.replace(
                "validation_for: bootstrap", "validation_for: ''"
            ),
        }
        for expected, text in cases.items():
            with self.subTest(expected=expected):
                self.assertIn(expected, [issue.id for issue in inspect_state(text).issues])

        for scale in ("standard", "full"):
            with self.subTest(scale=scale):
                result = inspect_state(
                    baseline.replace("scale: standard", f"scale: {scale}")
                )
                self.assertEqual(result.issues, ())

        for scale in ("one-shot", "mini", "huge", "2"):
            with self.subTest(scale=scale):
                result = inspect_state(
                    baseline.replace("scale: standard", f"scale: {scale}")
                )
                self.assertIn(
                    "state.schema.unsupported-value",
                    [issue.id for issue in result.issues],
                )

    def test_v1_and_v2_controls_are_explicit_and_non_inheriting(self) -> None:
        self.assertEqual(
            V1_STATE_KEYS,
            (
                "scale",
                "intensity",
                "autonomy",
                "active_spec",
                "active_packet",
                "owner_gates",
                "validation",
                "routed_docs",
            ),
        )
        self.assertEqual(
            V2_STATE_KEYS,
            (
                "scale",
                "execution_scope",
                "active_spec",
                "active_packet",
                "owner_gates",
                "validation",
                "routed_docs",
                "validation_for",
                "current_handoff",
            ),
        )
        self.assertEqual(
            REQUIRED_TOP_LEVEL_KEYS_BY_VERSION[2],
            frozenset(V2_STATE_KEYS[:-1]),
        )
        self.assertEqual(
            KNOWN_TOP_LEVEL_KEYS_BY_VERSION[2],
            frozenset(("version", "updated", *V2_STATE_KEYS)),
        )
        self.assertEqual(
            STATE_ENUMS_BY_VERSION,
            {
                1: {
                    "scale": frozenset(
                        {"one-shot", "mini", "standard", "full"}
                    ),
                    "intensity": frozenset({"low", "medium", "high"}),
                    "autonomy": frozenset({"0", "1", "2", "3", "4"}),
                },
                2: {
                    "scale": frozenset({"standard", "full"}),
                    "execution_scope": frozenset({"unit", "packet"}),
                },
            },
        )

    def test_v1_accepts_every_legacy_control_enum(self) -> None:
        cases = (
            (
                "scale",
                "standard",
                ("one-shot", "mini", "standard", "full"),
            ),
            ("intensity", "medium", ("low", "medium", "high")),
            ("autonomy", "2", ("0", "1", "2", "3", "4")),
        )
        for key, baseline, accepted_values in cases:
            for value in accepted_values:
                with self.subTest(key=key, value=value):
                    result = inspect_state(
                        valid_v1_state().replace(
                            f"{key}: {baseline}",
                            f"{key}: {value}",
                            1,
                        )
                    )
                    self.assertEqual(result.issues, ())

    def test_v2_execution_scope_accepts_only_unit_or_packet_scalars(self) -> None:
        baseline = valid_v2_state()
        for scope in ("unit", "packet"):
            with self.subTest(scope=scope):
                result = inspect_state(
                    baseline.replace(
                        "execution_scope: packet",
                        f"execution_scope: {scope}",
                    )
                )
                self.assertEqual(result.issues, ())

        cases = (
            (
                baseline.replace("execution_scope: packet\n", ""),
                "state.schema.missing-key",
            ),
            (
                baseline.replace(
                    "execution_scope: packet",
                    "execution_scope:\n  nested: value",
                ),
                "state.schema.wrong-kind",
            ),
            (
                baseline.replace("execution_scope: packet", "execution_scope: ''"),
                "state.schema.unsupported-value",
            ),
            (
                baseline.replace("execution_scope: packet", "execution_scope: 2"),
                "state.schema.unsupported-value",
            ),
            (
                baseline.replace(
                    "execution_scope: packet",
                    "execution_scope: ask_first",
                ),
                "state.schema.unsupported-value",
            ),
            (
                baseline.replace(
                    "execution_scope: packet",
                    "execution_scope: session",
                ),
                "state.schema.unsupported-value",
            ),
        )
        for text, expected in cases:
            with self.subTest(expected=expected, text=text):
                issues = [
                    issue
                    for issue in inspect_state(text).issues
                    if issue.evidence == "execution_scope"
                    or "execution_scope" in issue.message
                ]
                self.assertEqual([issue.id for issue in issues], [expected])

    def test_v2_treats_intensity_and_autonomy_as_unknown_legacy_keys(self) -> None:
        for key, value in (("intensity", "medium"), ("autonomy", "4")):
            with self.subTest(key=key):
                result = inspect_state(valid_v2_state() + f"{key}: {value}\n")
                unknown = [
                    issue
                    for issue in result.issues
                    if issue.id == "state.schema.unknown-key"
                ]
                self.assertEqual(
                    [(issue.evidence, issue.severity) for issue in unknown],
                    [(key, "warning")],
                )

    def test_v2_packet_identity_grammar_is_exact(self) -> None:
        self.assertTrue(is_valid_v2_packet_id("A"))
        self.assertTrue(is_valid_v2_packet_id("WP_https.edge-01"))
        self.assertTrue(is_valid_v2_packet_id("A" * 64))
        for value in (
            "",
            "_A",
            "-A",
            ".A",
            " A",
            "A ",
            "A/B",
            "A\\B",
            "A:B",
            "A]B",
            "A\nB",
            "A" * 65,
            "한글",
        ):
            with self.subTest(value=value):
                self.assertFalse(is_valid_v2_packet_id(value))

    def test_v2_packet_identity_fields_use_the_exact_grammar(self) -> None:
        baseline = valid_v2_state()
        for text in (
            baseline.replace("validation_for: bootstrap", "validation_for: _bootstrap"),
            baseline.replace("  id: bootstrap", "  id: bootstrap/child"),
        ):
            with self.subTest(text=text):
                issues = inspect_state(text).issues
                invalid = [
                    issue
                    for issue in issues
                    if issue.id == "state.schema.unsupported-value"
                ]
                self.assertEqual(len(invalid), 1)
                self.assertIsNone(invalid[0].legacy_message)

    def test_v2_current_handoff_is_optional_but_must_be_a_normalized_scalar(self) -> None:
        baseline = valid_v2_state()
        self.assertNotIn("current_handoff", baseline)
        valid = baseline + "current_handoff: docs/sdad/handoffs/current.md\n"
        valid_snapshot = inspect_state(valid).snapshot
        self.assertIsNotNone(valid_snapshot)
        assert valid_snapshot is not None
        self.assertEqual(
            valid_snapshot.scalar("current_handoff").value,
            "docs/sdad/handoffs/current.md",
        )
        for replacement, expected in (
            ("current_handoff: ''", "path.invalid"),
            ("current_handoff: ../outside.md", "path.invalid"),
            ("current_handoff:\n  nested: value", "state.schema.wrong-kind"),
        ):
            with self.subTest(replacement=replacement):
                result = inspect_state(baseline + replacement + "\n")
                self.assertIn(expected, [issue.id for issue in result.issues])

    def test_v2_template_validation_returns_every_error_message(self) -> None:
        text = (
            valid_v2_state()
            .replace("scale: standard", "scale: one-shot")
            .replace("validation_for: bootstrap\n", "")
            + "current_handoff: ../outside.md\n"
        )
        result = inspect_state(text)
        expected = [
            issue.message for issue in result.issues if issue.severity == "error"
        ]

        self.assertGreaterEqual(len(expected), 3)
        self.assertTrue(all(issue.legacy_message is None for issue in result.issues))
        self.assertEqual(collect_template_state_violations(text), expected)

    def test_unsupported_version_preserves_all_duplicate_key_findings(self) -> None:
        text = (
            valid_v1_state()
            .replace("version: 1", "version: 99")
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
        duplicates = [
            issue for issue in result.issues if issue.id == "state.schema.duplicate-key"
        ]
        self.assertIsNone(result.state_version)
        self.assertEqual([issue.evidence for issue in duplicates], ["scale", "status", "proves"])
        self.assertTrue(all(issue.legacy_message is None for issue in duplicates))

    def test_rejects_unsupported_syntax_without_partial_state(self) -> None:
        result = inspect_state("scale: standard\nvalidation: &shared []\n")

        self.assertIsNone(result.snapshot)
        self.assertEqual(result.issues[0].id, "state.syntax.unsupported")
        self.assertEqual(result.issues[0].line, 2)
        self.assertIsNone(result.issues[0].legacy_message)

    def test_rejects_mapping_colons_without_separation(self) -> None:
        result = inspect_state("scale:standard\n")

        self.assertIsNone(result.snapshot)
        self.assertEqual(result.issues[0].id, "state.syntax.unsupported")
        self.assertEqual(result.issues[0].line, 1)

    def test_rejects_quoted_comments_without_separation(self) -> None:
        result = inspect_state("scale: 'standard'#comment\n")

        self.assertIsNone(result.snapshot)
        self.assertEqual(result.issues[0].id, "state.syntax.unsupported")
        self.assertEqual(result.issues[0].line, 1)

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
        text = valid_v1_state().replace(
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
        text = valid_v1_state().replace(
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
            valid_v1_state()
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

    def test_reports_every_top_level_duplicate_but_only_one_legacy_message(self) -> None:
        text = "scale: standard\nscale: full\nscale: mini\n"

        result = inspect_state(text)
        duplicates = [
            issue
            for issue in result.issues
            if issue.id == "state.schema.duplicate-key"
            and issue.evidence == "scale"
        ]

        self.assertEqual([issue.line for issue in duplicates], [2, 3])
        self.assertEqual(
            [issue.legacy_message for issue in duplicates],
            ["sdad-state.yaml duplicate top-level key: scale", None],
        )
        self.assertEqual(
            collect_template_state_violations(text).count(
                "sdad-state.yaml duplicate top-level key: scale"
            ),
            1,
        )

    def test_reports_every_packet_duplicate_but_only_one_legacy_message(self) -> None:
        text = (
            "active_packet:\n"
            "  status: not_started\n"
            "  status: blocked\n"
            "  status: deferred\n"
        )

        result = inspect_state(text)
        duplicates = [
            issue
            for issue in result.issues
            if issue.id == "state.schema.duplicate-key"
            and issue.evidence == "status"
        ]

        self.assertEqual([issue.line for issue in duplicates], [3, 4])
        self.assertEqual(
            [issue.legacy_message for issue in duplicates],
            ["sdad-state.yaml active_packet duplicate key: status", None],
        )
        self.assertEqual(
            collect_template_state_violations(text).count(
                "sdad-state.yaml active_packet duplicate key: status"
            ),
            1,
        )

    def test_reports_every_validation_entry_duplicate(self) -> None:
        text = (
            "validation:\n"
            "  - command: first\n"
            "    command: second\n"
            "    command: third\n"
        )

        result = inspect_state(text)
        duplicates = [
            issue
            for issue in result.issues
            if issue.id == "state.schema.duplicate-key"
            and issue.evidence == "command"
        ]

        self.assertEqual([issue.line for issue in duplicates], [3, 4])
        self.assertEqual(
            [issue.legacy_message for issue in duplicates],
            [None, None],
        )

    def test_last_top_level_occurrence_controls_the_snapshot(self) -> None:
        for replacement in (
            "scale: standard\nscale:",
            "scale: standard\nscale: []",
        ):
            with self.subTest(replacement=replacement):
                result = inspect_state(
                    valid_v1_state().replace("scale: standard", replacement)
                )
                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                self.assertIsNone(result.snapshot.scalar("scale"))

    def test_last_packet_occurrence_controls_the_snapshot(self) -> None:
        for replacement in (
            "  status: not_started\n  status:",
            "  status: not_started\n  status: []",
        ):
            with self.subTest(replacement=replacement):
                result = inspect_state(
                    valid_v1_state().replace("  status: not_started", replacement)
                )
                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                self.assertNotIn("status", result.snapshot.active_packet)

    def test_last_validation_field_occurrence_controls_the_snapshot(self) -> None:
        original = "  - command: Replace with the project validation command."
        for replacement in (
            f"{original}\n    command:",
            f"{original}\n    command: []",
        ):
            with self.subTest(replacement=replacement):
                result = inspect_state(valid_v1_state().replace(original, replacement))
                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                self.assertNotIn("command", result.snapshot.validation[0].fields)

    def test_bare_validation_item_is_malformed_and_not_snapshotted(self) -> None:
        original = (
            "validation:\n"
            "  - command: Replace with the project validation command.\n"
            "    proves: Replace with the claim this command supports."
        )
        result = inspect_state(valid_v1_state().replace(original, "validation:\n  -"))

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(result.snapshot.validation, ())
        self.assertTrue(
            any(
                issue.id == "state.collection.malformed-entry"
                for issue in result.issues
            )
        )

    def test_blank_packet_fields_emit_one_modern_issue(self) -> None:
        cases = (
            ("  id: bootstrap", "  id:", "sdad-state.yaml active_packet missing key: id"),
            ("  id: bootstrap", "  id: ''", None),
        )

        for old, new, expected_legacy in cases:
            with self.subTest(value=new):
                result = inspect_state(valid_v1_state().replace(old, new))
                packet_issues = [
                    issue
                    for issue in result.issues
                    if issue.line == 13
                    and issue.id
                    in {
                        "state.packet.missing-field",
                        "state.packet.blank-field",
                        "state.schema.wrong-kind",
                    }
                ]
                self.assertEqual(len(packet_issues), 1)
                self.assertEqual(packet_issues[0].id, "state.packet.blank-field")
                self.assertEqual(packet_issues[0].legacy_message, expected_legacy)

    def test_quoted_empty_packet_status_emits_one_blank_issue(self) -> None:
        legacy = "unsupported active_packet status: "
        for quoted_empty in ("''", '\"\"'):
            with self.subTest(value=quoted_empty):
                text = valid_v1_state().replace(
                    "  status: not_started",
                    f"  status: {quoted_empty}",
                )
                result = inspect_state(text)
                status_issues = [
                    issue
                    for issue in result.issues
                    if issue.line == 15
                    and issue.id
                    in {
                        "state.packet.blank-field",
                        "state.schema.unsupported-value",
                    }
                ]

                self.assertEqual(len(status_issues), 1)
                self.assertEqual(status_issues[0].id, "state.packet.blank-field")
                self.assertEqual(status_issues[0].legacy_message, legacy)
                self.assertEqual(collect_template_state_violations(text), [legacy])

    def test_empty_and_whitespace_active_spec_keep_distinct_legacy_output(self) -> None:
        cases = (
            ("''", "", "sdad-state.yaml active_spec must be a relative path: "),
            ("'   '", "   ", None),
        )
        for source, value, expected_legacy in cases:
            with self.subTest(source=source):
                text = valid_v1_state().replace(
                    "active_spec: SPEC/SPEC-COMPLETE.md",
                    f"active_spec: {source}",
                )

                result = inspect_state(text)

                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                self.assertEqual(result.snapshot.scalar("active_spec").value, value)
                path_issues = [
                    issue for issue in result.issues if issue.id == "path.invalid"
                ]
                self.assertEqual(len(result.issues), 1)
                self.assertEqual(len(path_issues), 1)
                self.assertEqual(path_issues[0].severity, "error")
                self.assertEqual(path_issues[0].evidence, value)
                self.assertEqual(path_issues[0].legacy_message, expected_legacy)
                self.assertEqual(
                    collect_template_state_violations(text),
                    [] if expected_legacy is None else [expected_legacy],
                )

    def test_quoted_whitespace_packet_text_fields_are_blank(self) -> None:
        for key, original in (
            ("id", "bootstrap"),
            ("objective", "Replace with the current evidence-ready objective."),
        ):
            with self.subTest(key=key):
                text = valid_v1_state().replace(
                    f"  {key}: {original}",
                    f"  {key}: '   '",
                )
                result = inspect_state(text)

                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                self.assertEqual(result.snapshot.active_packet[key].value, "   ")
                field_issues = [
                    issue
                    for issue in result.issues
                    if issue.id == "state.packet.blank-field"
                    and issue.evidence == key
                ]
                self.assertEqual(len(result.issues), 1)
                self.assertEqual(len(field_issues), 1)
                self.assertEqual(field_issues[0].severity, "error")
                self.assertIsNone(field_issues[0].legacy_message)
                self.assertEqual(collect_template_state_violations(text), [])

    def test_quoted_whitespace_packet_status_is_one_blank_issue(self) -> None:
        text = valid_v1_state().replace(
            "  status: not_started",
            "  status: '   '",
        )

        result = inspect_state(text)

        self.assertIsNotNone(result.snapshot)
        assert result.snapshot is not None
        self.assertEqual(result.snapshot.active_packet["status"].value, "   ")
        status_issues = [
            issue
            for issue in result.issues
            if issue.id
            in {"state.packet.blank-field", "state.schema.unsupported-value"}
            and issue.line == 15
        ]
        self.assertEqual(len(result.issues), 1)
        self.assertEqual(len(status_issues), 1)
        self.assertEqual(status_issues[0].id, "state.packet.blank-field")
        self.assertEqual(status_issues[0].severity, "error")
        self.assertEqual(
            status_issues[0].legacy_message,
            "unsupported active_packet status:    ",
        )
        self.assertEqual(
            collect_template_state_violations(text),
            ["unsupported active_packet status:    "],
        )

    def test_quoted_whitespace_collection_entries_are_malformed_but_retained(self) -> None:
        cases = (
            (
                "owner_gates",
                valid_v1_state().replace(
                    "owner_gates: []",
                    "owner_gates:\n  - '   '",
                ),
            ),
            (
                "routed_docs",
                valid_v1_state().replace(
                    "  - docs/TODO-Open-Items.md",
                    "  - '   '",
                ),
            ),
        )

        for key, text in cases:
            with self.subTest(key=key):
                result = inspect_state(text)

                self.assertIsNotNone(result.snapshot)
                assert result.snapshot is not None
                values = getattr(result.snapshot, key)
                self.assertEqual(values[0].value, "   ")
                collection_issues = [
                    issue
                    for issue in result.issues
                    if issue.id == "state.collection.malformed-entry"
                    and issue.message.startswith(f"{key} entries ")
                ]
                self.assertEqual(len(result.issues), 1)
                self.assertEqual(len(collection_issues), 1)
                self.assertEqual(collection_issues[0].severity, "error")
                self.assertEqual(collection_issues[0].evidence, "blank")
                self.assertIsNone(collection_issues[0].legacy_message)
                self.assertFalse(
                    any(
                        issue.id == "path.invalid" and issue.evidence == "   "
                        for issue in result.issues
                    )
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
        result = inspect_state(
            valid_v1_state().replace("scale: standard", "scale: huge")
        )

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
        text = valid_v1_state().replace("version: 1\n", "extra: value\n")

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

    def test_v1_only_recognizes_v1_top_level_keys(self) -> None:
        for key, value in (
            ("validation_for", "bootstrap"),
            ("current_handoff", "docs/sdad/handoffs/current.md"),
        ):
            with self.subTest(key=key):
                result = inspect_state(valid_v1_state() + f"{key}: {value}\n")
                unknown = [
                    issue
                    for issue in result.issues
                    if issue.id == "state.schema.unknown-key"
                ]
                self.assertEqual(
                    [
                        (
                            issue.id,
                            issue.severity,
                            issue.evidence,
                            issue.legacy_message,
                        )
                        for issue in unknown
                    ],
                    [("state.schema.unknown-key", "warning", key, None)],
                )

    def test_v1_issue_ids_legacy_messages_and_order_are_stable(self) -> None:
        text = (
            valid_v1_state()
            .replace("scale: standard", "scale: huge\nscale: huge")
            .replace("intensity: medium\n", "")
            .replace("autonomy: 2", "autonomy:\n  nested: value")
            .replace("active_spec: SPEC/SPEC-COMPLETE.md", "active_spec: ../outside.md")
            .replace(
                "  objective: Replace with the current evidence-ready objective.\n",
                "",
            )
            .replace("owner_gates: []", "owner_gates:\n  -")
            + "custom_key: preserved\n"
        )

        self.assertEqual(
            [(issue.id, issue.legacy_message) for issue in inspect_state(text).issues],
            [
                (
                    "state.schema.duplicate-key",
                    "sdad-state.yaml duplicate top-level key: scale",
                ),
                (
                    "state.schema.missing-key",
                    "sdad-state.yaml missing top-level key: intensity",
                ),
                ("state.schema.unsupported-value", "unsupported scale: huge"),
                (
                    "state.schema.wrong-kind",
                    "sdad-state.yaml missing scalar value: autonomy",
                ),
                (
                    "path.invalid",
                    "sdad-state.yaml active_spec must be a relative path: ../outside.md",
                ),
                (
                    "state.packet.missing-field",
                    "sdad-state.yaml active_packet missing key: objective",
                ),
                ("state.schema.unknown-key", None),
                ("state.collection.malformed-entry", None),
            ],
        )

    def test_preserves_existing_violation_text(self) -> None:
        text = valid_v1_state().replace("scale: standard", "scale: huge")

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
            "   ",
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
