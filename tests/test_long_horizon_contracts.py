from __future__ import annotations

import random
import sys
import unittest
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from dataclasses import FrozenInstanceError
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.checks.state_schema import StateSchemaCheck  # noqa: E402
from sdad_validator.diagnostics import DoctorPolicy, Severity  # noqa: E402
from sdad_validator.doctor import DoctorContext, DiagnosticEngine  # noqa: E402
from sdad_validator.project_view import PathInspection, ReadResult  # noqa: E402
from sdad_validator.state_contract import (  # noqa: E402
    ACTIVE_PACKET_STATUSES,
    collect_template_state_violations,
    inspect_state,
    is_normalized_relative_posix_path,
)


INDEX_TEXT = """# Project Documentation Router

## Active Catalog

- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.
"""


def _state_blocks(
    *,
    status: str = "in_progress",
    updated: str = "2026-07-15",
    owner_entries: tuple[str, ...] = (),
    validation_empty: bool = False,
    routed_docs: tuple[str, ...] = (),
) -> tuple[tuple[str, str], ...]:
    owner_block = (
        "owner_gates: []"
        if not owner_entries
        else "owner_gates:\n" + "\n".join(
            "  -" if entry == "" else f"  - {entry}"
            for entry in owner_entries
        )
    )
    validation_block = (
        "validation: []"
        if validation_empty
        else (
            "validation:\n"
            "  - command: python -m unittest discover -s tests\n"
            "    proves: The repository tests pass."
        )
    )
    routed_block = (
        "routed_docs: []"
        if not routed_docs
        else "routed_docs:\n" + "\n".join(
            f"  - {path}" for path in routed_docs
        )
    )
    return (
        ("version", "version: 2"),
        ("updated", f"updated: {updated}"),
        ("scale", "scale: standard"),
        ("execution_scope", "execution_scope: packet"),
        ("active_spec", "active_spec: SPEC/current.md"),
        (
            "active_packet",
            "active_packet:\n"
            "  id: WP-LONG\n"
            "  objective: Implement the bounded packet.\n"
            f"  status: {status}",
        ),
        ("validation_for", "validation_for: WP-LONG"),
        ("owner_gates", owner_block),
        ("validation", validation_block),
        ("routed_docs", routed_block),
    )


def _render_blocks(blocks: tuple[tuple[str, str], ...]) -> str:
    return "\n".join(block for _key, block in blocks) + "\n"


def _valid_v2_state(**kwargs: object) -> str:
    return _render_blocks(_state_blocks(**kwargs))


def _valid_v1_state(
    *,
    status: str = "in_progress",
    objective: str = "Implement the bounded packet.",
    autonomy: str = "2",
    owner_entries: tuple[str, ...] = (),
) -> str:
    owner_block = (
        "owner_gates: []"
        if not owner_entries
        else "owner_gates:\n" + "\n".join(
            "  -" if entry == "" else f"  - {entry}"
            for entry in owner_entries
        )
    )
    return (
        "version: 1\n"
        "updated: 2026-07-15\n"
        "scale: standard\n"
        "intensity: medium\n"
        f"autonomy: {autonomy}\n"
        "active_spec: SPEC/current.md\n"
        "active_packet:\n"
        "  id: WP-LONG\n"
        f"  objective: {objective}\n"
        f"  status: {status}\n"
        f"{owner_block}\n"
        "validation:\n"
        "  - command: python -m unittest discover -s tests\n"
        "    proves: The repository tests pass.\n"
        "routed_docs: []\n"
    )


def _snapshot_values(text: str) -> tuple[object, ...]:
    result = inspect_state(text)
    if result.snapshot is None:
        raise AssertionError(result.issues)
    snapshot = result.snapshot
    return (
        result.state_version,
        tuple(sorted((key, value.value) for key, value in snapshot.scalars.items())),
        tuple(sorted((key, value.value) for key, value in snapshot.active_packet.items())),
        tuple(value.value for value in snapshot.owner_gates),
        tuple(
            tuple(sorted((key, value.value) for key, value in entry.fields.items()))
            for entry in snapshot.validation
        ),
        tuple(value.value for value in snapshot.routed_docs),
    )


class MutableProjectView:
    def __init__(self, state: str | bytes, files: dict[str, str] | None = None) -> None:
        self._root = Path("C:/long-horizon-project")
        self.files: dict[str, bytes] = {
            "sdad-state.yaml": (
                state.encode("utf-8") if isinstance(state, str) else state
            ),
            "SPEC/current.md": b"# Current specification\n",
            "docs/INDEX.md": INDEX_TEXT.encode("utf-8"),
        }
        for path, content in (files or {}).items():
            self.files[path] = content.encode("utf-8")
        self.read_counts: Counter[str] = Counter()
        self.inspect_counts: Counter[str] = Counter()

    @property
    def root(self) -> Path:
        return self._root

    def inspect(self, relative_path: str) -> PathInspection:
        self.inspect_counts[relative_path] += 1
        status = "ok" if relative_path in self.files else "missing"
        return PathInspection(status, self._root / relative_path)

    def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult:
        self.read_counts[relative_path] += 1
        data = self.files.get(relative_path)
        if data is None:
            return ReadResult("missing", None)
        if len(data) > max_bytes:
            return ReadResult("too_large", None)
        return ReadResult("ok", data)


def _diagnose(view: MutableProjectView, *, today: date = date(2026, 7, 15)):
    return DiagnosticEngine().diagnose(view, DoctorPolicy(today=today))


def _report_signature(report: object) -> tuple[object, ...]:
    return (
        report.root,
        report.state_version,
        report.checks_run,
        report.checks_skipped,
        report.error_count,
        report.warning_count,
        tuple(
            (
                finding.id,
                finding.severity.value,
                finding.path,
                finding.line,
                finding.evidence,
            )
            for finding in report.findings
        ),
    )


class StateTransportAndEvolutionContractTests(unittest.TestCase):
    def test_all_statuses_survive_common_text_transports(self) -> None:
        for status in sorted(ACTIVE_PACKET_STATUSES):
            canonical = _valid_v2_state(status=status)
            expected = inspect_state(canonical)
            self.assertEqual(expected.issues, ())
            variants = {
                "lf": canonical,
                "crlf": canonical.replace("\n", "\r\n"),
                "cr": canonical.replace("\n", "\r"),
                "no-final-newline": canonical.rstrip("\n"),
                "utf8-bom": "\ufeff" + canonical,
            }
            for transport, text in variants.items():
                with self.subTest(status=status, transport=transport):
                    self.assertEqual(inspect_state(text), expected)

        embedded_bom = _valid_v2_state().replace(
            "scale: standard",
            "\ufeffscale: standard",
        )
        self.assertEqual(
            [issue.id for issue in inspect_state(embedded_bom).issues],
            ["state.syntax.unsupported"],
        )

    def test_top_level_order_is_semantically_stable_across_many_arrangements(
        self,
    ) -> None:
        blocks = _state_blocks(
            owner_entries=("Approve release",),
            routed_docs=("review-findings.md", "docs/TODO-Open-Items.md"),
        )
        expected = _snapshot_values(_render_blocks(blocks))
        orders: set[tuple[str, ...]] = set()
        keys = tuple(key for key, _block in blocks)
        orders.add(keys)
        orders.add(tuple(reversed(keys)))
        for offset in range(len(keys)):
            orders.add(keys[offset:] + keys[:offset])
        for left in range(len(keys)):
            for right in range(left + 1, len(keys)):
                swapped = list(keys)
                swapped[left], swapped[right] = swapped[right], swapped[left]
                orders.add(tuple(swapped))
        generator = random.Random(20260715)
        for _ in range(128):
            shuffled = list(keys)
            generator.shuffle(shuffled)
            orders.add(tuple(shuffled))

        by_key = dict(blocks)
        for order in sorted(orders):
            with self.subTest(order=order):
                text = _render_blocks(tuple((key, by_key[key]) for key in order))
                result = inspect_state(text)
                self.assertEqual(result.issues, ())
                self.assertEqual(_snapshot_values(text), expected)

    def test_every_top_level_block_duplicate_is_reported_deterministically(self) -> None:
        blocks = _state_blocks()
        for index, (key, block) in enumerate(blocks):
            duplicated = blocks[: index + 1] + ((key, block),) + blocks[index + 1 :]
            with self.subTest(key=key):
                first = inspect_state(_render_blocks(duplicated))
                second = inspect_state(_render_blocks(duplicated))
                duplicates = [
                    issue
                    for issue in first.issues
                    if issue.id == "state.schema.duplicate-key"
                ]
                self.assertEqual(first, second)
                self.assertEqual(len(duplicates), 1)
                self.assertEqual(duplicates[0].evidence, key)
                self.assertEqual(first.state_version, 2)

    def test_future_and_malformed_versions_are_semantically_quarantined(self) -> None:
        cases = {
            "future-missing-updated": "version: 99\nscale: standard\n",
            "future-placeholder": "version: 99\nupdated: TBD\n",
            "future-mapping-updated": "version: 99\nupdated:\n  nested: value\n",
            "empty-version": "version:\nupdated: TBD\n",
            "list-version": "version: []\nupdated: TBD\n",
            "mapping-version": "version:\n  nested: 2\nupdated: TBD\n",
            "numeric-looking-02": "version: 02\nupdated: TBD\n",
            "numeric-looking-2.0": "version: 2.0\nupdated: TBD\n",
            "yaml-looking-true": "version: true\nupdated: TBD\n",
            "yaml-looking-null": "version: null\nupdated: TBD\n",
        }
        for name, state in cases.items():
            with self.subTest(name=name):
                report = _diagnose(MutableProjectView(state))
                self.assertIsNone(report.state_version)
                self.assertEqual(report.checks_run, ("state_schema",))
                self.assertFalse(
                    any(finding.id.startswith("state.updated.") for finding in report.findings),
                    report.findings,
                )
                self.assertTrue(
                    any(
                        finding.id
                        in {
                            "state.schema.unsupported-version",
                            "state.schema.wrong-kind",
                        }
                        for finding in report.findings
                    ),
                    report.findings,
                )

        for quoted in ("'2'", '"2"'):
            with self.subTest(quoted=quoted):
                state = _valid_v2_state().replace("version: 2", f"version: {quoted}")
                self.assertEqual(inspect_state(state).state_version, 2)
                self.assertEqual(inspect_state(state).issues, ())

    def test_path_sentinels_and_nul_are_rejected_before_project_inspection(self) -> None:
        for value in (".", "a\x00b"):
            with self.subTest(value=repr(value)):
                self.assertFalse(is_normalized_relative_posix_path(value))
                for field in ("active_spec", "current_handoff", "routed_docs"):
                    state = _valid_v2_state()
                    if field == "active_spec":
                        state = state.replace("active_spec: SPEC/current.md", f"active_spec: {value}")
                    elif field == "current_handoff":
                        state += f"current_handoff: {value}\n"
                    else:
                        state = state.replace("routed_docs: []", f"routed_docs:\n  - {value}")
                    result = inspect_state(state)
                    self.assertTrue(
                        any(issue.id == "path.invalid" and issue.evidence == value for issue in result.issues),
                        result.issues,
                    )

                state = _valid_v2_state().replace(
                    "active_spec: SPEC/current.md",
                    f"active_spec: {value}",
                )
                view = MutableProjectView(state)
                report = _diagnose(view)
                self.assertTrue(any(finding.id == "path.invalid" for finding in report.findings))
                self.assertNotIn(value, view.inspect_counts)

    def test_state_results_are_deeply_immutable_and_repeatable(self) -> None:
        state = _valid_v2_state(
            owner_entries=("Approve release",),
            routed_docs=("review-findings.md",),
        )
        first = inspect_state(state)
        second = inspect_state(state)
        self.assertEqual(first, second)
        assert first.snapshot is not None

        with self.assertRaises(TypeError):
            first.snapshot.scalars["scale"] = first.snapshot.scalars["scale"]
        with self.assertRaises(TypeError):
            first.snapshot.active_packet["status"] = first.snapshot.active_packet["status"]
        with self.assertRaises(TypeError):
            first.snapshot.validation[0].fields["command"] = first.snapshot.validation[0].fields["command"]
        with self.assertRaises(FrozenInstanceError):
            first.snapshot.owner_gates[0].value = "Changed"
        with self.assertRaises(AttributeError):
            first.snapshot.routed_docs.append("docs/other.md")

        invalid = state.replace("scale: standard", "scale: impossible")
        violations = collect_template_state_violations(invalid)
        violations.append("caller-owned mutation")
        self.assertNotIn(
            "caller-owned mutation",
            collect_template_state_violations(invalid),
        )


class LongRunningDiagnosticContractTests(unittest.TestCase):
    def test_utf8_bom_state_bytes_are_accepted_by_the_full_engine(self) -> None:
        state = _valid_v2_state().encode("utf-8-sig")
        report = _diagnose(MutableProjectView(state))
        self.assertEqual(report.state_version, 2)
        self.assertFalse(
            any(finding.id == "state.syntax.unsupported" for finding in report.findings)
        )

    def test_repeated_status_transitions_do_not_leak_cached_severity(self) -> None:
        engine = DiagnosticEngine()
        state = _valid_v2_state(status="in_progress", validation_empty=True)
        view = MutableProjectView(state)
        observed: list[Severity] = []
        for status in ("in_progress", "production_ready", "in_progress"):
            view.files["sdad-state.yaml"] = _valid_v2_state(
                status=status,
                validation_empty=True,
            ).encode("utf-8")
            report = engine.diagnose(view, DoctorPolicy(today=date(2026, 7, 15)))
            matching = [
                finding
                for finding in report.findings
                if finding.id == "validation.empty"
            ]
            self.assertEqual(len(matching), 1)
            observed.append(matching[0].severity)

        self.assertEqual(
            observed,
            [Severity.WARNING, Severity.ERROR, Severity.WARNING],
        )
        self.assertEqual(view.read_counts["sdad-state.yaml"], 3)

    def test_one_engine_matches_fresh_engines_across_every_status_transition(self) -> None:
        review = (
            "## Active Findings\n"
            "- [High] [packet:WP-LONG] Keep this active blocker visible.\n"
        )
        shared = DiagnosticEngine()
        view = MutableProjectView(
            _valid_v2_state(
                validation_empty=True,
                routed_docs=("review-findings.md",),
            ),
            {"review-findings.md": review},
        )
        statuses = tuple(sorted(ACTIVE_PACKET_STATUSES))
        for previous in statuses:
            view.files["sdad-state.yaml"] = _valid_v2_state(
                status=previous,
                validation_empty=True,
                routed_docs=("review-findings.md",),
            ).encode("utf-8")
            shared.diagnose(view, DoctorPolicy(today=date(2026, 7, 15)))
            for current in statuses:
                with self.subTest(previous=previous, current=current):
                    current_state = _valid_v2_state(
                        status=current,
                        validation_empty=True,
                        routed_docs=("review-findings.md",),
                    )
                    view.files["sdad-state.yaml"] = current_state.encode("utf-8")
                    actual = shared.diagnose(
                        view,
                        DoctorPolicy(today=date(2026, 7, 15)),
                    )
                    expected = _diagnose(
                        MutableProjectView(
                            current_state,
                            {"review-findings.md": review},
                        )
                    )
                    self.assertEqual(
                        _report_signature(actual),
                        _report_signature(expected),
                    )

    def test_parallel_diagnoses_are_deterministic_and_context_isolated(self) -> None:
        statuses = tuple(sorted(ACTIVE_PACKET_STATUSES))
        policy = DoctorPolicy(today=date(2026, 7, 15))
        engine = DiagnosticEngine()
        expected = {
            status: _report_signature(
                DiagnosticEngine().diagnose(
                    MutableProjectView(
                        _valid_v2_state(status=status, validation_empty=True)
                    ),
                    policy,
                )
            )
            for status in statuses
        }

        workload = statuses * 8
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [
                pool.submit(
                    engine.diagnose,
                    MutableProjectView(
                        _valid_v2_state(status=status, validation_empty=True)
                    ),
                    policy,
                )
                for status in workload
            ]
        for status, future in zip(workload, futures, strict=True):
            with self.subTest(status=status):
                self.assertEqual(
                    _report_signature(future.result()),
                    expected[status],
                )

    def test_freshness_boundaries_hold_across_centuries_and_calendar_rollovers(self) -> None:
        safe_dates = (
            date(1900, 3, 1),
            date(2000, 3, 1),
            date(2027, 1, 1),
            date(2100, 3, 1),
            date(2400, 3, 1),
        )
        offsets = {
            -2: "state.updated.future",
            -1: None,
            0: None,
            30: None,
            31: "state.updated.stale",
        }
        for today in safe_dates:
            for age_days, expected in offsets.items():
                with self.subTest(today=today, age_days=age_days):
                    declared = today - timedelta(days=age_days)
                    context = DoctorContext(
                        view=None,
                        policy=DoctorPolicy(today=today),
                        state_result=inspect_state(
                            _valid_v2_state(updated=declared.isoformat())
                        ),
                    )
                    ids = {
                        finding.id
                        for finding in StateSchemaCheck().run(context)
                        if finding.id.startswith("state.updated.")
                    }
                    self.assertEqual(ids, set() if expected is None else {expected})

        extremes = (
            (date.max, date.min, "state.updated.stale"),
            (date.min, date.max, "state.updated.future"),
        )
        for today, declared, expected in extremes:
            with self.subTest(today=today, declared=declared):
                context = DoctorContext(
                    view=None,
                    policy=DoctorPolicy(today=today),
                    state_result=inspect_state(
                        _valid_v2_state(updated=declared.isoformat())
                    ),
                )
                ids = {finding.id for finding in StateSchemaCheck().run(context)}
                self.assertIn(expected, ids)


class PartialOwnerGateCorruptionContractTests(unittest.TestCase):
    def test_valid_terminal_gate_cannot_be_hidden_by_a_malformed_sibling(self) -> None:
        malformed_entries = ("", "''", "decision: pending")
        for status, expected_severity in (
            ("owner_accepted", Severity.WARNING),
            ("production_ready", Severity.ERROR),
        ):
            for malformed in malformed_entries:
                for entries in (
                    ("Approve release", malformed),
                    (malformed, "Approve release"),
                ):
                    with self.subTest(status=status, entries=entries):
                        report = _diagnose(
                            MutableProjectView(
                                _valid_v2_state(
                                    status=status,
                                    owner_entries=entries,
                                )
                            )
                        )
                        pending = [
                            finding
                            for finding in report.findings
                            if finding.id == "gate.pending-after-acceptance"
                        ]
                        malformed_findings = [
                            finding
                            for finding in report.findings
                            if finding.id == "state.collection.malformed-entry"
                            and finding.message.startswith("owner_gates entries ")
                        ]
                        self.assertEqual(len(pending), 1)
                        self.assertIs(pending[0].severity, expected_severity)
                        self.assertEqual(len(malformed_findings), 1)

    def test_only_malformed_gate_entries_still_suppress_absence_based_inference(self) -> None:
        for malformed in ("", "''", "decision: pending"):
            with self.subTest(version=1, malformed=malformed):
                report = _diagnose(
                    MutableProjectView(
                        _valid_v1_state(
                            autonomy="4",
                            objective="Release production data.",
                            owner_entries=(malformed,),
                        )
                    )
                )
                self.assertFalse(
                    any(
                        finding.id in {"gate.required", "gate.q5-review"}
                        for finding in report.findings
                    ),
                    report.findings,
                )


if __name__ == "__main__":
    unittest.main()
