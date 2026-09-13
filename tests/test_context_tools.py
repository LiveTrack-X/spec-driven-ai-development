from __future__ import annotations

import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from sdad_context import ContextError, inventory, read_page, run_cli
from sdad_validator.project_view import FilesystemProjectView


class ContextToolsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.view = FilesystemProjectView(self.root)

    def put(self, path, text):
        target = self.root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")

    def test_heading_reads_include_children_but_not_next_section_or_fenced_examples(self):
        self.put("notes.md", "# Notes\n```md\n## Active\n```\n## Active\nkeep\n### Child\nchild\n## History\nold\n")
        result = read_page(self.view, "notes.md", heading="Active")
        self.assertEqual(result["lines"], ["## Active", "keep", "### Child", "child"])
        self.assertFalse(result["truncated"])

    def test_paging_uses_original_line_numbers_and_refuses_changed_sources(self):
        self.put("notes.md", "# Notes\none\ntwo\nthree\n")
        first = read_page(self.view, "notes.md", count=2)
        second = read_page(self.view, "notes.md", start=first["next_start"], expected_sha256=first["sha256"])
        self.assertEqual(second["lines"], ["two", "three"])
        self.put("notes.md", "changed\n")
        with self.assertRaisesRegex(ContextError, "Source changed"):
            read_page(self.view, "notes.md", expected_sha256=first["sha256"])

    def test_utf8_byte_budget_and_no_silent_long_line_truncation(self):
        self.put("large.md", ("한" * 1000 + "\n") * 30)
        result = read_page(self.view, "large.md", count=500)
        self.assertLessEqual(result["page_bytes"], 50_000)
        self.assertTrue(result["truncated"])
        self.put("one.md", "한" * 20_000)
        with self.assertRaisesRegex(ContextError, "One line"):
            read_page(self.view, "one.md")

    def test_ambiguous_missing_and_out_of_section_requests_fail(self):
        self.put("notes.md", "# Notes\n## Same\none\n## Same\ntwo\n")
        for heading in ("Same", "Missing"):
            with self.assertRaises(ContextError):
                read_page(self.view, "notes.md", heading=heading)
        with self.assertRaises(ContextError):
            read_page(self.view, "notes.md", start=999)
        with self.assertRaises(ContextError):
            read_page(self.view, "notes.md", count=501)

    def test_serialized_output_including_escaping_stays_bounded(self):
        self.put("escaped.md", ('\\"\t' * 1000 + '\n') * 20)
        result = read_page(self.view, "escaped.md", count=500)
        self.assertLessEqual(len(json.dumps(result, ensure_ascii=False).encode("utf-8")), 50_000)
        self.assertTrue(result["truncated"])
        reconstructed = list(result["lines"])
        for _ in range(20):
            if result["next_start"] is None:
                break
            result = read_page(self.view, "escaped.md", start=result["next_start"], expected_sha256=result["sha256"])
            self.assertLessEqual(len(json.dumps(result, ensure_ascii=False).encode("utf-8")), 50_000)
            reconstructed.extend(result["lines"])
        self.assertIsNone(result["next_start"])
        self.assertTrue(reconstructed == (self.root / "escaped.md").read_text(encoding="utf-8").splitlines(), "Bounded pages must reconstruct every line exactly once")

    def test_traversal_absolute_binary_and_oversize_are_rejected(self):
        for path in ("../outside", str(self.root / "x.md"), "docs/../x.md"):
            with self.assertRaises(ContextError): read_page(self.view, path)
        (self.root / "binary").write_bytes(b"\xff")
        with self.assertRaisesRegex(ContextError, "UTF-8"): read_page(self.view, "binary")
        (self.root / "huge").write_bytes(b"x" * 1_000_001)
        with self.assertRaisesRegex(ContextError, "too_large"): read_page(self.view, "huge")

    def test_inspect_is_fixed_surface_metadata_and_never_changes_or_dumps_history(self):
        state = (ROOT / "templates/project-control-files/sdad-state.yaml").read_text(encoding="utf-8")
        self.put("sdad-state.yaml", state)
        self.put("docs/TODO-Open-Items.md", "private historical body\n" * 501)
        self.put("docs/archive/old.md", "must not be inspected")
        before = {p:p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        result = inventory(self.view)
        todo = next(f for f in result["files"] if f["path"] == "docs/TODO-Open-Items.md")
        self.assertEqual(todo["advice"], "targeted_read")
        self.assertNotIn("private historical body", json.dumps(result))
        self.assertFalse(any("archive" in f["path"] for f in result["files"]))
        self.assertEqual(before, {p:p.read_bytes() for p in self.root.rglob("*") if p.is_file()})

    def test_empty_files_and_cli_error_are_explicit(self):
        self.put("empty.md", "")
        self.assertEqual(read_page(self.view, "empty.md")["lines"], [])
        out = io.StringIO()
        self.assertEqual(run_cli(["--root", str(self.root), "read", "absent.md"], stdout=out), 2)
        self.assertIn("error", json.loads(out.getvalue()))

    def test_inventory_follows_declared_spec_and_handoff_without_scanning_other_specs(self):
        state = (ROOT / "templates/project-control-files/sdad-state.yaml").read_text(encoding="utf-8")
        self.put("sdad-state.yaml", state + "\ncurrent_handoff: docs/checkpoint.md\n")
        self.put("SPEC/SPEC-COMPLETE.md", "requirement\n" * 2001)
        self.put("docs/checkpoint.md", "# Current checkpoint\n")
        self.put("SPEC/inactive.md", "unselected proposal")
        files = {f["path"]: f for f in inventory(self.view)["files"]}
        self.assertEqual(files["SPEC/SPEC-COMPLETE.md"]["advice"], "review_compaction")
        self.assertEqual(files["docs/checkpoint.md"]["status"], "ok")
        self.assertNotIn("SPEC/inactive.md", files)


if __name__ == "__main__": unittest.main()
