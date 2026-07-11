from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
RESEARCH_SOURCE_URLS = (
    "https://developers.openai.com/api/docs/guides/latest-model?model=gpt-5.6",
    "https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/",
    "https://www.anthropic.com/engineering/building-effective-agents",
    "https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents",
    "https://www.anthropic.com/research/trustworthy-agents",
    "https://code.claude.com/docs/en/best-practices",
    "https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents",
    "https://geminicli.com/docs/cli/gemini-md/",
    "https://ai.google.dev/gemini-api/docs/prompting-strategies",
    "https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions",
    "https://docs.github.com/en/copilot/concepts/agents/cloud-agent/risks-and-mitigations",
    "https://cursor.com/docs/rules",
    "https://cursor.com/blog/agent-best-practices",
    "https://airc.nist.gov/airmf-resources/airmf/5-sec-core/",
    "https://openreview.net/forum?id=VTF8yNQM66",
    "https://papers.nips.cc/paper_files/paper/2024/hash/5a7c947568c1b1328ccc5230172e1e7c-Abstract-Conference.html",
    "https://arxiv.org/abs/2210.03629",
    "https://papers.neurips.cc/paper_files/paper/2023/hash/1b44b878bb782e6954cd888628510e90-Abstract-Conference.html",
    "https://arxiv.org/abs/2407.01489",
    "https://arxiv.org/abs/2307.03172",
    "https://arxiv.org/abs/2507.09089",
    "https://pubsonline.informs.org/doi/abs/10.1287/mnsc.2025.00535",
    "https://papers.ssrn.com/sol3/papers.cfm?abstract_id=5713646",
    "https://arxiv.org/abs/2505.23419",
    "https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/",
)
SPEC = importlib.util.spec_from_file_location(
    "validate_repo_under_test",
    ROOT / "scripts" / "validate_repo.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load scripts/validate_repo.py")
VALIDATE_REPO = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATE_REPO)


class ResearchFoundationsContractTests(unittest.TestCase):
    HEADER = (
        "| Primary source | Last verified | Paraphrased principle | "
        "Adopted SDAD decision | Limitation or non-transferable detail | "
        "Control type |"
    )

    def write_fixture(
        self,
        root: Path,
        *,
        urls: tuple[str, ...] = RESEARCH_SOURCE_URLS,
        verified: str = "2026-07-10",
        control_type: str = "Guidance",
        linked: bool = True,
    ) -> None:
        docs = root / "docs"
        docs.mkdir()
        rows = [
            self.HEADER,
            "| --- | --- | --- | --- | --- | --- |",
        ]
        rows.extend(
            f"| [Source {index}]({url}) | {verified} | Principle {index} | "
            f"Decision {index} | Limitation {index} | {control_type} |"
            for index, url in enumerate(urls, start=1)
        )
        boundaries = (
            "Sources inform bounded design decisions; they do not establish SDAD "
            "effectiveness. Mixed productivity results are not consensus. No reported "
            "percentage or benchmark score is an SDAD effectiveness claim.\n\n"
        )
        (docs / "research-foundations.md").write_text(
            "# Research Foundations\n\n" + boundaries + "\n".join(rows) + "\n",
            encoding="utf-8",
        )
        (docs / "tool-adapters.md").write_text(
            "See [research](research-foundations.md).\n" if linked else "# Adapters\n",
            encoding="utf-8",
        )

    def validate(self, root: Path) -> None:
        validator = getattr(VALIDATE_REPO, "validate_research_foundations", None)
        self.assertIsNotNone(validator, "research-foundations validator is missing")
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            validator()

    def test_accepts_exact_source_set_and_matrix_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.validate(root)

    def test_rejects_missing_or_unapproved_source(self) -> None:
        cases = (
            RESEARCH_SOURCE_URLS[:-1],
            RESEARCH_SOURCE_URLS[:-1] + ("https://example.com/not-approved",),
        )
        for urls in cases:
            with self.subTest(urls=urls[-1]), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_fixture(root, urls=urls)
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.validate(root)

    def test_rejects_wrong_verification_date_or_control_type(self) -> None:
        cases = (
            {"verified": "2026-07-11"},
            {"control_type": "Marketing claim"},
        )
        for overrides in cases:
            with self.subTest(overrides=overrides), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_fixture(root, **overrides)
                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.validate(root)

    def test_rejects_unrouted_research_document(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root, linked=False)
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)


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

    def test_accepts_equivalent_noncanonical_root_spelling(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "alias").mkdir()
            (root / "README.md").write_text("[Guide](guide.md)\n", encoding="utf-8")
            (root / "guide.md").write_text("# Guide\n", encoding="utf-8")

            self.validate(root / "alias" / "..")

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


class DoctorGeminiDocumentationContractTests(unittest.TestCase):
    CONTRACT_PATHS = {
        "README.md",
        "adapters/README.md",
        "docs/getting-started.md",
        "docs/user-guide.md",
        "docs/tool-adapters.md",
        "docs/known-limitations.md",
    }

    def write_current_contract_fixture(self, root: Path) -> None:
        for relative_path in self.CONTRACT_PATHS:
            source = ROOT / relative_path
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def validate(self, root: Path) -> None:
        validator = getattr(
            VALIDATE_REPO,
            "validate_doctor_gemini_documentation_contract",
            None,
        )
        self.assertIsNotNone(
            validator,
            "doctor/Gemini documentation validator is missing",
        )
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            validator()

    def test_contract_mapping_covers_only_the_public_documentation_routes(self) -> None:
        contracts = getattr(VALIDATE_REPO, "DOCTOR_GEMINI_DOC_CONTRACTS", None)
        self.assertIsNotNone(contracts, "doctor/Gemini contract mapping is missing")
        self.assertEqual(set(contracts), self.CONTRACT_PATHS)

    def test_current_documentation_satisfies_the_contract(self) -> None:
        self.validate(ROOT)

    def test_rejects_a_full_exit_table_in_the_compact_readme_section(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_current_contract_fixture(root)
            readme_path = root / "README.md"
            readme = readme_path.read_text(encoding="utf-8")
            readme_path.write_text(
                readme.replace(
                    "## What SDAD Gives You",
                    "| Exit | Meaning |\n| --- | --- |\n| 0 | Clean |\n\n"
                    "## What SDAD Gives You",
                    1,
                ),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_an_incomplete_getting_started_exit_contract(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_current_contract_fixture(root)
            guide_path = root / "docs/getting-started.md"
            guide = guide_path.read_text(encoding="utf-8")
            guide_path.write_text(
                re.sub(r"(?m)^\| 1 \|.*\n", "", guide, count=1),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_wrong_getting_started_exit_meanings(self) -> None:
        def replace_exit_rows(guide: str, replacements: dict[str, str]) -> str:
            return re.sub(
                r"(?m)^\| ([012]) \| ([^\n]+) \|$",
                lambda match: (
                    f"| {match.group(1)} | "
                    f"{replacements.get(match.group(1), match.group(2))} |"
                ),
                guide,
            )

        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            self.write_current_contract_fixture(fixture)
            original = (fixture / "docs/getting-started.md").read_text(
                encoding="utf-8"
            )
            meanings = dict(
                re.findall(r"(?m)^\| ([012]) \| ([^\n]+) \|$", original)
            )
            cases = (
                {"0": meanings["2"], "2": meanings["0"]},
                {"1": "Arbitrary text that does not define completed findings."},
            )

            for replacements in cases:
                with self.subTest(replacements=replacements):
                    root = fixture / next(iter(replacements))
                    self.write_current_contract_fixture(root)
                    guide_path = root / "docs/getting-started.md"
                    guide_path.write_text(
                        replace_exit_rows(original, replacements),
                        encoding="utf-8",
                    )
                    with contextlib.redirect_stderr(io.StringIO()):
                        with self.assertRaises(SystemExit):
                            self.validate(root)

    def test_rejects_a_contradictory_duplicate_exit_row(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_current_contract_fixture(root)
            guide_path = root / "docs/getting-started.md"
            guide = guide_path.read_text(encoding="utf-8")
            correct_zero_row = re.search(r"(?m)^\| 0 \| [^\n]+ \|$", guide)
            self.assertIsNotNone(correct_zero_row)
            guide_path.write_text(
                guide.replace(
                    correct_zero_row.group(0),
                    "| 0 | Diagnosis did not complete because the root failed. |\n"
                    + correct_zero_row.group(0),
                    1,
                ),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_an_unstable_gemini_memory_command(self) -> None:
        for unstable_command in ("/memory reload", "/memory show --refresh"):
            with self.subTest(command=unstable_command), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_current_contract_fixture(root)
                guide_path = root / "docs/tool-adapters.md"
                guide = guide_path.read_text(encoding="utf-8")
                guide_path.write_text(
                    guide + f"\nUnstable alias: `{unstable_command}`\n",
                    encoding="utf-8",
                )

                with contextlib.redirect_stderr(io.StringIO()):
                    with self.assertRaises(SystemExit):
                        self.validate(root)

    def test_checkout_only_doctor_stays_out_of_distribution_surfaces(self) -> None:
        for relative_path in (
            "scripts/install-agent-adapter.ps1",
            "scripts/install-agent-adapter.sh",
            "docs/no-clone-quick-install.md",
        ):
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIsNone(
                    re.search(r"\bdoctor\b|scripts[/\\]sdad\.py", content, flags=re.I)
                )

    def test_owner_artwork_and_expanded_copy_prompt_are_unchanged(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        no_clone = (ROOT / "docs/no-clone-quick-install.md").read_text(
            encoding="utf-8"
        )
        self.assertEqual(
            VALIDATE_REPO.prompt_content(readme, VALIDATE_REPO.README_HEADING),
            VALIDATE_REPO.prompt_content(no_clone, VALIDATE_REPO.CANONICAL_HEADING),
        )
        self.assertNotIn("<details", readme)
        self.assertEqual(
            hashlib.sha256(
                (ROOT / "assets/spec-driven-ai-development-infographic.png").read_bytes()
            ).hexdigest(),
            "5c5a53a8973599839a83cefa8ea787277cbe580c98d04eb608b597a84b540793",
        )


class DoctorSourceVersionContractTests(unittest.TestCase):
    def test_doctor_source_uses_three_exact_named_version_domains(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        self.assertRegex(source, r'(?m)^DOCTOR_VERSION = "3\.2\.0"$')
        self.assertRegex(source, r"(?m)^LEGACY_REPORT_SCHEMA_VERSION = 1$")
        self.assertRegex(source, r"(?m)^REPORT_SCHEMA_VERSION = 2$")
        self.assertNotRegex(source, r"(?m)^SCHEMA_VERSION\s*=")

    def test_report_schema_selection_owns_the_only_state_v2_mapping(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        self.assertIn("def _select_report_schema(", source)
        self.assertEqual(source.count("state_version == 2"), 1)

    def test_current_doctor_source_satisfies_checkout_contract(self) -> None:
        VALIDATE_REPO.validate_doctor_checkout_contract()


class StableReleaseContractTests(unittest.TestCase):
    EXPECTED_SOURCES = {
        "mini": {
            "path": "templates/mini-sdad/MINI-SDAD.md",
            "sha256": "f5370ba6539ab55b88fc10a7589ca7f42fa6714072830620aad7dab60d21f669",
        },
        "codex": {
            "path": "adapters/codex/AGENTS.md",
            "target": "AGENTS.md",
            "sha256": "fc1ecaf1d373c26784d5e1c6113531a16de295c1177bd2ee5ebcb7ba7b4d2bba",
        },
        "claude-code": {
            "path": "adapters/claude-code/CLAUDE.md",
            "target": "CLAUDE.md",
            "sha256": "dc14598dee6645801ca04b3802216a38c87f5ae64fefaa0275daa01e88c865f5",
        },
        "gemini-cli": {
            "path": "adapters/gemini-cli/GEMINI.md",
            "target": "GEMINI.md",
            "sha256": "a35f1210bd5f8ed688b2c7ee82d29c505b29632a8da8295fa639a6f799f1ab23",
        },
        "cursor": {
            "path": "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            "target": ".cursor/rules/spec-driven-ai-development.mdc",
            "sha256": "371ee47e6d0712e37ce8381696cc0a5c1660d9a770157f9034ac9f2a150a0c68",
        },
        "github-copilot": {
            "path": "adapters/github-copilot/.github/copilot-instructions.md",
            "target": ".github/copilot-instructions.md",
            "sha256": "335209bcfee60dbb9ddce7a6c92def0d173d793680dec2e58b7f1757e788b3b4",
        },
        "generic": {
            "path": "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
            "target": "AI-SESSION-INSTRUCTIONS.md",
            "sha256": "9664f9c868e19a585fd3e64c96d79eac717ae6696c02c721d29233d287f90e75",
        },
    }

    def test_manifest_has_exact_v3_1_0_identity_and_baseline_sources(self) -> None:
        manifest = json.loads((ROOT / "install-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["label"], "v3.1.0 stable baseline")
        self.assertEqual(
            manifest["revision"],
            "1741b72a51bb4eb0711e8c0f188c3ddcf922eaaa",
        )
        self.assertEqual(
            manifest["capabilities"],
            {"progressive_control_plane": True},
        )
        self.assertEqual(manifest["sources"], self.EXPECTED_SOURCES)
        self.assertEqual(VALIDATE_REPO.STABLE_RELEASE_SOURCES, self.EXPECTED_SOURCES)

    def test_current_stable_release_surfaces_satisfy_contract(self) -> None:
        manifest = json.loads((ROOT / "install-sources.json").read_text(encoding="utf-8"))
        VALIDATE_REPO.validate_stable_release_contract(manifest)

    def test_option_one_and_readme_prompt_include_gemini_and_stay_expanded(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        no_clone = (ROOT / "docs/no-clone-quick-install.md").read_text(
            encoding="utf-8"
        )
        canonical = VALIDATE_REPO.prompt_content(
            no_clone,
            VALIDATE_REPO.CANONICAL_HEADING,
        )
        mirrored = VALIDATE_REPO.prompt_content(readme, VALIDATE_REPO.README_HEADING)
        self.assertEqual(mirrored, canonical)
        self.assertIn("Gemini CLI -> ./GEMINI.md", canonical)
        self.assertIn("adapters/gemini-cli/GEMINI.md", canonical)
        self.assertNotIn("<details", readme)
        self.assertNotIn("<summary", readme)


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
    def test_readme_inherits_pins_through_canonical_option_one_parity(self) -> None:
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
