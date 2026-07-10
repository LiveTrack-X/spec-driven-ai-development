from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "validate_repo_under_test",
    ROOT / "scripts" / "validate_repo.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load scripts/validate_repo.py")
VALIDATE_REPO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE_REPO)


class MarkdownLinkValidationTests(unittest.TestCase):
    def validate(self, root: Path) -> None:
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            VALIDATE_REPO.validate_local_markdown_links()

    def test_accepts_local_link_with_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                '[Guide](guide.md "Open the guide")\n',
                encoding="utf-8",
            )
            (root / "guide.md").write_text("# Real Heading\n", encoding="utf-8")

            self.validate(root)

    def test_accepts_destination_with_balanced_parentheses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[Draft](guide_(draft).md)\n",
                encoding="utf-8",
            )
            (root / "guide_(draft).md").write_text("# Draft\n", encoding="utf-8")

            self.validate(root)

    def test_accepts_link_title_with_parentheses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                '[Guide](guide.md "Title (draft)")\n',
                encoding="utf-8",
            )
            (root / "guide.md").write_text("# Guide\n", encoding="utf-8")

            self.validate(root)

    def test_accepts_existing_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[Guide](guide.md#real-heading)\n",
                encoding="utf-8",
            )
            (root / "guide.md").write_text("# Real Heading\n", encoding="utf-8")

            self.validate(root)

    def test_rejects_missing_fragment_in_existing_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "[Missing](guide.md#missing-heading)\n",
                encoding="utf-8",
            )
            (root / "guide.md").write_text("# Real Heading\n", encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_missing_fragment_in_same_markdown_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text(
                "# Real Heading\n\n[Missing](#missing-heading)\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_broken_link_from_cursor_mdc_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            rule = root / ".cursor" / "rules" / "project.mdc"
            rule.parent.mkdir(parents=True)
            rule.write_text("[Missing](../../missing.md)\n", encoding="utf-8")

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)


class TestDiscoveryContractTests(unittest.TestCase):
    def test_accepts_discoverable_unittest_case(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "tests" / "test_real_case.py"
            path.parent.mkdir()
            path.write_text(
                "import unittest\n\n"
                "class RenamedTests(unittest.TestCase):\n"
                "    def test_behavior(self):\n"
                "        self.assertTrue(True)\n",
                encoding="utf-8",
            )

            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                self.assertEqual(VALIDATE_REPO.require_discovered_tests(), 1)

    def test_rejects_names_that_unittest_will_not_discover(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "tests" / "test_no_cases.py"
            path.parent.mkdir()
            path.write_text(
                "if False:\n"
                "    def test_disabled():\n"
                "        pass\n\n"
                "class NotATestCase:\n"
                "    def test_method(self):\n"
                "        pass\n\n"
                "def helper():\n"
                "    def test_nested():\n"
                "        pass\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.require_discovered_tests()

    def test_rejects_an_empty_test_module_even_when_other_tests_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_other_real_case.py").write_text(
                "import unittest\n\n"
                "class RealTests(unittest.TestCase):\n"
                "    def test_behavior(self):\n"
                "        self.assertTrue(True)\n",
                encoding="utf-8",
            )
            (tests_dir / "test_empty_contract.py").write_text(
                "HELPER = True\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.require_discovered_tests()

    def test_rejects_a_test_module_that_fails_to_import(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tests_dir = root / "tests"
            tests_dir.mkdir()
            (tests_dir / "test_broken.py").write_text(
                "raise RuntimeError('broken import')\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.require_discovered_tests()


class RequiredPhraseContractTests(unittest.TestCase):
    def test_returns_content_when_all_phrases_exist(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.txt").write_text("alpha\nbeta\n", encoding="utf-8")

            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                content = VALIDATE_REPO.require_phrases(
                    "config.txt",
                    "Config",
                    ["alpha", "beta"],
                )

            self.assertEqual(content, "alpha\nbeta\n")

    def test_rejects_missing_phrase_with_surface_name(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "config.txt").write_text("alpha\n", encoding="utf-8")

            error_output = io.StringIO()
            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                with contextlib.redirect_stderr(error_output):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.require_phrases(
                            "config.txt",
                            "Config",
                            ["alpha", "beta"],
                        )

            self.assertIn("Config missing: beta", error_output.getvalue())


class WorkflowActionPinContractTests(unittest.TestCase):
    def validate(self, root: Path) -> None:
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            VALIDATE_REPO.require_pinned_workflow_actions(
                "workflow.yml",
                {"actions/checkout", "actions/setup-python"},
            )

    def test_accepts_full_action_commit_pins(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workflow.yml").write_text(
                "steps:\n"
                "  - uses: actions/checkout@" + "a" * 40 + "\n"
                "  - uses: actions/setup-python@" + "B" * 40 + " # version\n",
                encoding="utf-8",
            )

            self.validate(root)

    def test_rejects_mutable_action_tag(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workflow.yml").write_text(
                "steps:\n"
                "  - uses: actions/checkout@v6\n"
                "  - uses: actions/setup-python@" + "b" * 40 + "\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_mutable_action_in_a_named_step(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workflow.yml").write_text(
                "steps:\n"
                "  - uses: actions/checkout@" + "a" * 40 + "\n"
                "  - uses: actions/setup-python@" + "b" * 40 + "\n"
                "  - name: unsafe extra action\n"
                "    uses: third-party/action@main\n",
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)


class InstallSourceManifestContractTests(unittest.TestCase):
    def test_readme_delegates_pinned_source_details_to_the_manifest(self) -> None:
        self.assertNotIn("README.md", VALIDATE_REPO.INSTALL_SOURCE_SURFACES)
        self.assertEqual(
            VALIDATE_REPO.INSTALL_SOURCE_SURFACES["docs/no-clone-quick-install.md"],
            VALIDATE_REPO.INSTALL_SOURCE_KEYS,
        )

    def test_rejects_ambiguous_or_absolute_manifest_paths(self) -> None:
        for value in (
            "/absolute/file.md",
            "C:/absolute/file.md",
            "folder\\file.md",
            "folder//file.md",
            "folder/../file.md",
            "./file.md",
        ):
            with self.subTest(value=value):
                self.assertFalse(VALIDATE_REPO.is_normalized_relative_posix_path(value))
        self.assertTrue(
            VALIDATE_REPO.is_normalized_relative_posix_path("folder/file.md")
        )

    def write_manifest(
        self,
        root: Path,
        sha256: str,
        progressive_control_plane: object = False,
        schema_version: object = 1,
        label: object = "v9.9.9 stable baseline",
    ) -> None:
        (root / "install-sources.json").write_text(
            json.dumps(
                {
                    "schema_version": schema_version,
                    "label": label,
                    "revision": "a" * 40,
                    "capabilities": {
                        "progressive_control_plane": progressive_control_plane,
                    },
                    "sources": {
                        "mini": {
                            "path": "templates/mini.md",
                            "sha256": sha256,
                        }
                    },
                }
            ),
            encoding="utf-8",
        )

    def validate(self, root: Path, blob: bytes) -> None:
        completed = subprocess.CompletedProcess([], 0, stdout=blob, stderr=b"")
        with (
            mock.patch.object(VALIDATE_REPO, "ROOT", root),
            mock.patch.object(VALIDATE_REPO, "INSTALL_SOURCE_KEYS", {"mini"}),
            mock.patch.object(VALIDATE_REPO, "INSTALL_SOURCE_SURFACES", {}),
            mock.patch.object(VALIDATE_REPO.subprocess, "run", return_value=completed),
        ):
            VALIDATE_REPO.validate_install_source_manifest()

    def test_accepts_hash_of_pinned_git_blob(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blob = b"pinned content\n"
            self.write_manifest(root, hashlib.sha256(blob).hexdigest())

            self.validate(root, blob)

    def test_rejects_hash_that_does_not_match_pinned_git_blob(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root, "0" * 64)

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root, b"different content\n")

    def test_rejects_non_boolean_progressive_capability(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            blob = b"pinned content\n"
            self.write_manifest(
                root,
                hashlib.sha256(blob).hexdigest(),
                progressive_control_plane="unknown",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root, blob)

    def test_rejects_invalid_schema_version_or_label(self) -> None:
        cases = (
            {"schema_version": 2},
            {"label": "latest"},
            {"label": ""},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                blob = b"pinned content\n"
                self.write_manifest(
                    root,
                    hashlib.sha256(blob).hexdigest(),
                    **overrides,
                )

                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.validate(root, blob)


class ContentSecurityPolicyContractTests(unittest.TestCase):
    def validate(self, root: Path) -> None:
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            VALIDATE_REPO.require_local_only_csp("diagram.html")

    def test_accepts_local_only_policy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "diagram.html").write_text(
                '<meta http-equiv="Content-Security-Policy" '
                'content="default-src \'none\'; script-src \'unsafe-inline\'; '
                "style-src 'unsafe-inline'; font-src 'self' data:; "
                "connect-src 'none'\">",
                encoding="utf-8",
            )

            self.validate(root)

    def test_rejects_remote_default_and_connect_sources(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "diagram.html").write_text(
                '<meta http-equiv="Content-Security-Policy" '
                'content="default-src *; connect-src https:">',
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_remote_image_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "diagram.html").write_text(
                '<meta http-equiv="Content-Security-Policy" '
                'content="default-src \'none\'; connect-src \'none\'; '
                'img-src data: https:">',
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)


class WorkflowDiagramCopyParityTests(unittest.TestCase):
    def test_rejects_html_that_drops_workflow_copy(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "workflow.json").write_text(
                json.dumps({"nodes": [{"label": "Active state"}]}),
                encoding="utf-8",
            )
            (root / "diagram.html").write_text("<p>Old state</p>", encoding="utf-8")

            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.validate_workflow_copy_parity(
                            "workflow.json",
                            "diagram.html",
                        )

    def test_rejects_mermaid_node_id_reused_for_different_labels(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "diagrams.md").write_text(
                "```mermaid\n"
                'flowchart TD\nA["Adapter"] --> B["State"]\n'
                'B --> A["ADR"]\n'
                "```\n",
                encoding="utf-8",
            )

            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        VALIDATE_REPO.validate_mermaid_node_id_consistency(
                            "diagrams.md"
                        )


class AgentExperienceIntegrationTests(unittest.TestCase):
    def test_converts_first_agent_experience_violation_to_cli_error(self) -> None:
        error_output = io.StringIO()
        with mock.patch.object(
            VALIDATE_REPO,
            "collect_agent_experience_violations",
            return_value=["control plane drift", "secondary drift"],
            create=True,
        ):
            with contextlib.redirect_stderr(error_output):
                with self.assertRaises(SystemExit):
                    VALIDATE_REPO.validate_agent_experience_contract()

        self.assertIn("ERROR: control plane drift", error_output.getvalue())

    def test_accepts_agent_experience_contract_without_violations(self) -> None:
        with mock.patch.object(
            VALIDATE_REPO,
            "collect_agent_experience_violations",
            return_value=[],
            create=True,
        ):
            VALIDATE_REPO.validate_agent_experience_contract()


class AgentSurfaceRenderIntegrationTests(unittest.TestCase):
    def test_converts_first_render_drift_to_cli_error(self) -> None:
        error_output = io.StringIO()
        with mock.patch.object(
            VALIDATE_REPO,
            "collect_surface_drift",
            return_value=["adapter drift"],
            create=True,
        ):
            with contextlib.redirect_stderr(error_output):
                with self.assertRaises(SystemExit):
                    VALIDATE_REPO.validate_rendered_agent_surfaces()

        self.assertIn("ERROR: adapter drift", error_output.getvalue())

    def test_accepts_rendered_agent_surfaces_without_drift(self) -> None:
        with mock.patch.object(
            VALIDATE_REPO,
            "collect_surface_drift",
            return_value=[],
            create=True,
        ):
            VALIDATE_REPO.validate_rendered_agent_surfaces()


if __name__ == "__main__":
    unittest.main()
