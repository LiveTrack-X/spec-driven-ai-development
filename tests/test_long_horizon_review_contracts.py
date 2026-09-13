from __future__ import annotations

import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.checks.review_state import (  # noqa: E402
    _parse_v2_review_records,
    _parse_v2_todo_records,
    _review_items,
    _todo_items,
)
from sdad_validator.diagnostics import DoctorPolicy, DoctorReport  # noqa: E402
from sdad_validator.doctor import DiagnosticEngine  # noqa: E402
from sdad_validator.project_view import FilesystemProjectView  # noqa: E402


PACKET_ID = "WP-LONG"
TODAY = date(2026, 7, 15)
INDEX_TEXT = """# Project Documentation Router

## Active Catalog

- Current handoff: use `../sdad-state.yaml#current_handoff` when declared.
"""


def _state(*, version: int, status: str, routed_doc: str) -> str:
    version_specific = (
        ["intensity: medium", "autonomy: 2"]
        if version == 1
        else ["execution_scope: packet"]
    )
    lines = [
        f"version: {version}",
        f"updated: {TODAY.isoformat()}",
        "scale: standard",
        *version_specific,
        "active_spec: SPEC/current.md",
        "active_packet:",
        f"  id: {PACKET_ID}",
        "  objective: Exercise duplicate active ledger sections.",
        f"  status: {status}",
    ]
    if version == 2:
        lines.append(f"validation_for: {PACKET_ID}")
    lines.extend(
        (
            "owner_gates: []",
            "validation:",
            "  - command: python -m unittest discover -s tests",
            "    proves: The project unit tests pass.",
            "routed_docs:",
            f"  - {routed_doc}",
        )
    )
    return "\n".join(lines) + "\n"


def _line_number(text: str, exact_line: str) -> int:
    return text.splitlines().index(exact_line) + 1


class LongHorizonReviewContractTests(unittest.TestCase):
    def diagnose(
        self,
        *,
        version: int,
        status: str,
        document_path: str,
        document: str,
    ) -> DoctorReport:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            files = {
                "sdad-state.yaml": _state(
                    version=version,
                    status=status,
                    routed_doc=document_path,
                ),
                "SPEC/current.md": "# Current SPEC\n",
                document_path: document,
            }
            if version == 2:
                files["docs/INDEX.md"] = INDEX_TEXT
            for relative_path, content in files.items():
                target = root / relative_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")

            return DiagnosticEngine().diagnose(
                FilesystemProjectView(root),
                DoctorPolicy(today=TODAY),
            )

    def assert_finding_lines(
        self,
        report: DoctorReport,
        *,
        finding_id: str,
        path: str,
        lines: list[int],
    ) -> None:
        matches = [
            finding
            for finding in report.findings
            if finding.id == finding_id and finding.path == path
        ]
        self.assertEqual([finding.line for finding in matches], lines)

    def test_duplicate_review_sections_detect_blocker_at_every_position(
        self,
    ) -> None:
        blocker = f"- [Critical] [packet:{PACKET_ID}] release blocker"
        for version in (1, 2):
            for blocker_position in range(3):
                with self.subTest(
                    version=version,
                    blocker_position=blocker_position,
                ):
                    bodies = ["None currently tracked."] * 3
                    bodies[blocker_position] = blocker
                    document = "# Review Findings\n\n" + "\n\n".join(
                        f"## Active Findings\n\n{body}" for body in bodies
                    )
                    document += "\n\n## Recently Closed\n\nNone.\n"

                    report = self.diagnose(
                        version=version,
                        status="release_candidate",
                        document_path="review-findings.md",
                        document=document,
                    )

                    self.assert_finding_lines(
                        report,
                        finding_id="packet.open-critical-finding",
                        path="review-findings.md",
                        lines=[_line_number(document, blocker)],
                    )

    def test_duplicate_todo_sections_detect_blocker_at_every_position(
        self,
    ) -> None:
        blocker = f"- [ ] [packet:{PACKET_ID}] pending verification"
        for version in (1, 2):
            for blocker_position in range(3):
                with self.subTest(
                    version=version,
                    blocker_position=blocker_position,
                ):
                    bodies = ["None currently tracked."] * 3
                    bodies[blocker_position] = blocker
                    document = "# TODO\n\n" + "\n\n".join(
                        f"## Active Work\n\n{body}" for body in bodies
                    )
                    document += (
                        "\n\n## Release / Production Readiness\n\n"
                        "None currently tracked.\n"
                    )

                    report = self.diagnose(
                        version=version,
                        status="software_verified",
                        document_path="docs/TODO-Open-Items.md",
                        document=document,
                    )

                    self.assert_finding_lines(
                        report,
                        finding_id="packet.open-todo",
                        path="docs/TODO-Open-Items.md",
                        lines=[_line_number(document, blocker)],
                    )

    def test_all_visible_duplicate_sections_preserve_source_line_order(
        self,
    ) -> None:
        review_lines = [
            f"- [High] [packet:{PACKET_ID}] finding {index}"
            for index in range(3)
        ]
        review = "# Review Findings\n\n" + "\n\n".join(
            f"## Active Findings\n\n{line}" for line in review_lines
        )
        review += "\n\n## Recently Closed\n\nNone.\n"

        todo_lines = [
            f"- [ ] [packet:{PACKET_ID}] todo {index}"
            for index in range(3)
        ]
        todo = (
            "# TODO\n\n"
            f"## Release / Production Readiness\n\n{todo_lines[0]}\n\n"
            f"## Active Work\n\n{todo_lines[1]}\n\n"
            f"## Release / Production Readiness\n\n{todo_lines[2]}\n"
        )

        for version in (1, 2):
            with self.subTest(version=version, ledger="review"):
                records = (
                    _review_items(review, PACKET_ID)
                    if version == 1
                    else _parse_v2_review_records(review)
                )
                self.assertIsNotNone(records)
                assert records is not None
                self.assertEqual(
                    [record.line for record in records],
                    [_line_number(review, line) for line in review_lines],
                )

            with self.subTest(version=version, ledger="todo"):
                records = (
                    _todo_items(todo, PACKET_ID)
                    if version == 1
                    else _parse_v2_todo_records(todo)
                )
                self.assertIsNotNone(records)
                assert records is not None
                self.assertEqual(
                    [record.line for record in records],
                    [_line_number(todo, line) for line in todo_lines],
                )

    def test_fenced_duplicate_section_decoys_are_ignored(self) -> None:
        cases = (
            (
                "review-findings.md",
                "packet.open-finding",
                "## Active Findings",
                f"- [High] [packet:{PACKET_ID}] visible first",
                f"- [Critical] [packet:{PACKET_ID}] fenced decoy",
                f"- [Low] [packet:{PACKET_ID}] visible last",
                "\n\n## Recently Closed\n\nNone.\n",
                "```markdown",
                "```",
            ),
            (
                "docs/TODO-Open-Items.md",
                "packet.open-todo",
                "## Active Work",
                f"- [ ] [packet:{PACKET_ID}] visible first",
                f"- [ ] [packet:{PACKET_ID}] fenced decoy",
                f"- [ ] [packet:{PACKET_ID}] visible last",
                (
                    "\n\n## Release / Production Readiness\n\n"
                    "None currently tracked.\n"
                ),
                "~~~markdown",
                "~~~",
            ),
        )
        for version in (1, 2):
            for (
                path,
                finding_id,
                heading,
                first,
                decoy,
                last,
                suffix,
                fence_open,
                fence_close,
            ) in cases:
                with self.subTest(version=version, path=path):
                    document = (
                        f"# Ledger\n\n{heading}\n\n{first}\n\n"
                        f"{fence_open}\n{heading}\n\n{decoy}\n{fence_close}\n\n"
                        f"{heading}\n\n{last}{suffix}"
                    )

                    report = self.diagnose(
                        version=version,
                        status="software_verified",
                        document_path=path,
                        document=document,
                    )

                    self.assert_finding_lines(
                        report,
                        finding_id=finding_id,
                        path=path,
                        lines=[
                            _line_number(document, first),
                            _line_number(document, last),
                        ],
                    )
                    self.assertFalse(
                        any(
                            finding.path == path
                            and finding.line == _line_number(document, decoy)
                            for finding in report.findings
                        ),
                        report.findings,
                    )


if __name__ == "__main__":
    unittest.main()
