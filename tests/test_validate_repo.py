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


class SkillMigrationRepositoryContractTests(unittest.TestCase):
    def assert_skill_mutation_rejected(self, mutate) -> str:
        original_read = VALIDATE_REPO.read
        skill_path = "skills/ai-spec-project-start/SKILL.md"

        def read_with_mutation(candidate: str) -> str:
            content = original_read(candidate)
            return mutate(content) if candidate == skill_path else content

        error_output = io.StringIO()
        with mock.patch.object(VALIDATE_REPO, "read", side_effect=read_with_mutation):
            with contextlib.redirect_stderr(error_output):
                with self.assertRaises(SystemExit):
                    VALIDATE_REPO.validate_skill()
        return error_output.getvalue()

    def assert_skill_mutation_accepted(self, mutate) -> None:
        original_read = VALIDATE_REPO.read
        skill_path = "skills/ai-spec-project-start/SKILL.md"

        def read_with_mutation(candidate: str) -> str:
            content = original_read(candidate)
            return mutate(content) if candidate == skill_path else content

        error_output = io.StringIO()
        with mock.patch.object(VALIDATE_REPO, "read", side_effect=read_with_mutation):
            with contextlib.redirect_stderr(error_output):
                try:
                    VALIDATE_REPO.validate_skill()
                except SystemExit as exc:
                    self.fail(
                        "Narrative-only rewording was rejected: "
                        f"{error_output.getvalue().strip()} ({exc})"
                    )

    def test_rejects_preview_that_no_longer_precedes_writes(self) -> None:
        output = self.assert_skill_mutation_rejected(
            lambda text: text.replace(
                "apply the proposed control-file changes",
                "apply the proposed file changes",
                1,
            )
        )
        self.assertIn("migration preview", output)

    def test_rejects_a_broad_generic_trigger(self) -> None:
        old_generic_trigger = (
            "  Start, adopt, review, implement, reorganize, release, or hand off "
            "a project.\n"
        )
        output = self.assert_skill_mutation_rejected(
            lambda text: text.replace(
                "description: >-\n",
                "description: >-\n" + old_generic_trigger,
                1,
            )
        )
        self.assertIn(
            "Skill frontmatter has broad generic trigger: ordinary project workflow",
            output,
        )

    def test_accepts_narrative_rewording_when_section_concepts_remain(self) -> None:
        def reword(text: str) -> str:
            return text.replace(
                "Inspect the request and repository first.",
                "Begin by inspecting repository evidence and the request.",
                1,
            ).replace(
                "because parent context is not assumed.",
                "because parent context cannot be assumed.",
                1,
            )

        self.assert_skill_mutation_accepted(reword)


class CanonicalTemplateRepositoryContractTests(unittest.TestCase):
    def validator(self):
        validator = getattr(
            VALIDATE_REPO,
            "validate_canonical_template_contract",
            None,
        )
        self.assertIsNotNone(validator, "canonical template validator is missing")
        return validator

    def test_current_canonical_templates_satisfy_contract(self) -> None:
        self.validator()()

    def test_rejects_duplicate_current_handoff_source(self) -> None:
        validator = self.validator()
        original_read = VALIDATE_REPO.read
        index_path = "templates/project-control-files/docs/INDEX.md"
        source = (
            "- Current handoff: use "
            "`../sdad-state.yaml#current_handoff` when declared."
        )

        def read_with_duplicate(path: str) -> str:
            content = original_read(path)
            if path == index_path:
                return content + "\n" + source + "\n"
            return content

        error_output = io.StringIO()
        with mock.patch.object(VALIDATE_REPO, "read", side_effect=read_with_duplicate):
            with contextlib.redirect_stderr(error_output):
                with self.assertRaises(SystemExit):
                    validator()

        self.assertIn(
            "Canonical INDEX must contain exactly one current-handoff source line",
            error_output.getvalue(),
        )

    def assert_mutation_rejected(self, path: str, mutate) -> str:
        validator = self.validator()
        original_read = VALIDATE_REPO.read

        def read_with_mutation(candidate: str) -> str:
            content = original_read(candidate)
            return mutate(content) if candidate == path else content

        error_output = io.StringIO()
        with mock.patch.object(VALIDATE_REPO, "read", side_effect=read_with_mutation):
            with contextlib.redirect_stderr(error_output):
                with self.assertRaises(SystemExit):
                    validator()
        return error_output.getvalue()

    def test_state_templates_reject_prefix_and_comment_identity_decoys(self) -> None:
        cases = (
            (
                "templates/project-control-files/sdad-state.yaml",
                lambda text: text.replace("bootstrap", "bootstrap-old"),
            ),
            (
                "skills/ai-spec-project-start/references/starter-templates.md",
                lambda text: text.replace("  id: bootstrap", "  id: bootstrap-old", 1)
                .replace("validation_for: bootstrap", "validation_for: bootstrap-old", 1),
            ),
            (
                "skills/ai-spec-project-start/references/starter-templates.md",
                lambda text: text.replace("  id: bootstrap", "#   id: bootstrap", 1),
            ),
        )
        for path, mutate in cases:
            with self.subTest(path=path, mutate=mutate):
                self.assertIn("state-v2 identity", self.assert_mutation_rejected(path, mutate))

    def test_state_identity_rejects_structural_parser_issues(self) -> None:
        cases = (
            (
                "examples/minimal-project/sdad-state.yaml",
                lambda text: text.replace(
                    "scale: standard",
                    "scale: standard\nscale: standard",
                    1,
                ),
            ),
            (
                "skills/ai-spec-project-start/references/starter-templates.md",
                lambda text: text.replace("owner_gates: []\n", "", 1),
            ),
        )
        for path, mutate in cases:
            with self.subTest(path=path):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn("state-v2 identity", output)

    def test_starter_blocks_must_be_visible_in_their_sections(self) -> None:
        path = "skills/ai-spec-project-start/references/starter-templates.md"

        def hide_state_section(text: str, opener: str, closer: str) -> str:
            start = text.index("## Active State Schema")
            end = text.index("## INDEX Schema", start)
            section = text[start:end]
            return text[:start] + f"{opener}\n{section}{closer}\n" + text[end:]

        finding_block = (
            "```markdown\n"
            "- [High] [packet:bootstrap] Replace with a classified finding.\n"
            "- [packet:bootstrap] Replace with an unclassified finding.\n"
            "```"
        )
        handoff_block = (
            "```markdown\n"
            "## 1. Session Identity\n\n"
            "- Handoff ID: H0001\n"
            "- Active packet: [packet:bootstrap]\n"
            "```"
        )
        cases = (
            (
                "Active State Schema",
                lambda text: hide_state_section(text, "~~~~markdown", "~~~~"),
            ),
            (
                "Active State Schema",
                lambda text: hide_state_section(text, "<!--", "-->"),
            ),
            (
                "open-finding wire forms",
                lambda text: text.replace(
                    finding_block,
                    f"~~~~markdown\n{finding_block}\n~~~~",
                    1,
                ),
            ),
            (
                "open-finding wire forms",
                lambda text: text.replace(
                    finding_block,
                    f"<!--\n{finding_block}\n-->",
                    1,
                ),
            ),
            (
                "Optional Current Handoff",
                lambda text: text.replace(
                    handoff_block,
                    f"~~~~markdown\n{handoff_block}\n~~~~",
                    1,
                ),
            ),
            (
                "Optional Current Handoff",
                lambda text: text.replace(
                    handoff_block,
                    f"<!--\n{handoff_block}\n-->",
                    1,
                ),
            ),
        )
        for expected, mutate in cases:
            with self.subTest(expected=expected, mutate=mutate):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn(expected, output)

    def test_starter_fenced_block_content_preserves_inline_html_comments(self) -> None:
        path = "skills/ai-spec-project-start/references/starter-templates.md"
        cases = (
            (
                "state-v2 identity",
                lambda text: text.replace(
                    "version: 2\n",
                    "<!--decoy-->version: 2\n",
                    1,
                ),
            ),
            (
                "open-finding wire forms",
                lambda text: text.replace(
                    "- [High] [packet:bootstrap] Replace with a classified finding.\n",
                    "<!--decoy-->- [High] [packet:bootstrap] "
                    "Replace with a classified finding.\n",
                    1,
                ),
            ),
            (
                "Optional Current Handoff",
                lambda text: text.replace(
                    "- Active packet: [packet:bootstrap]\n",
                    "<!--decoy-->- Active packet: [packet:bootstrap]\n",
                    1,
                ),
            ),
        )
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn(expected, output)

    def test_starter_fence_lines_preserve_inline_html_comments(self) -> None:
        path = "skills/ai-spec-project-start/references/starter-templates.md"
        cases = (
            (
                "Active State Schema",
                lambda text: text.replace(
                    "```yaml\nversion: 2\n",
                    "```yaml<!--decoy-->\nversion: 2\n",
                    1,
                ),
            ),
            (
                "state-v2 identity",
                lambda text: text.replace(
                    "  - review-findings.md\n```\n",
                    "  - review-findings.md\n```<!--decoy-->\n",
                    1,
                ),
            ),
        )
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn(expected, output)

    def test_handoff_rejects_comment_fence_and_wrong_section_decoys(self) -> None:
        path = (
            "templates/project-control-files/docs/sdad/handoffs/"
            "YYYY-MM-DD-HNNNN-topic.md"
        )
        identity = (
            "## 1. Session Identity\n\n"
            "- Handoff ID: H0001\n"
            "- Active packet: [packet:bootstrap]\n"
        )
        replacements = (
            f"```markdown\n{identity}```\n",
            f"<!--\n{identity}-->\n",
            (
                "## 1. Session Identity\n\nNo marker.\n\n"
                "## 2. Notes\n\n- Active packet: [packet:bootstrap]\n\n"
                f"```markdown\n{identity}```\n"
            ),
        )
        for replacement in replacements:
            with self.subTest(replacement=replacement):
                output = self.assert_mutation_rejected(
                    path,
                    lambda text, replacement=replacement: replacement,
                )
                self.assertIn("first Session Identity section", output)

    def test_handoff_rejects_identity_and_authorization_pointer_drift(self) -> None:
        path = (
            "templates/project-control-files/docs/sdad/handoffs/"
            "YYYY-MM-DD-HNNNN-topic.md"
        )
        mutations = (
            lambda text: text.replace(
                "- Handoff ID: H0001",
                "- Handoff ID: H0002",
                1,
            ),
            lambda text: text.replace(
                "- Handoff ID: H0001",
                "- Handoff ID: H0001\n- Handoff ID: H0001",
                1,
            ),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn("H0001 identity and bootstrap marker", output)

        for field in (
            "- Authoritative authorization record, if any:\n",
            "- Last-observed authorization status:\n",
        ):
            with self.subTest(field=field):
                output = self.assert_mutation_rejected(
                    path,
                    lambda text, field=field: text.replace(field, "", 1),
                )
                self.assertIn("authorization field exactly once", output)

    def test_starter_handoff_requires_the_optional_subsection_block(self) -> None:
        path = "skills/ai-spec-project-start/references/starter-templates.md"
        identity = (
            "## 1. Session Identity\n\n"
            "- Handoff ID: H0001\n"
            "- Active packet: [packet:bootstrap]\n"
        )
        block = f"```markdown\n{identity}```"
        mutations = (
            lambda text: text.replace(block, "```markdown\nNo marker.\n```", 1)
            + f"\n<!--\n{identity}-->\n",
            lambda text: text.replace(block, "No current handoff example.", 1)
            + f"\n## Decoy Example\n\n{block}\n",
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn("Optional Current Handoff", output)

    def test_starter_requires_both_open_finding_forms(self) -> None:
        path = "skills/ai-spec-project-start/references/starter-templates.md"
        output = self.assert_mutation_rejected(
            path,
            lambda text: text.replace(
                "- [High] [packet:bootstrap] Replace with a classified finding.\n",
                "",
                1,
            ),
        )
        self.assertIn("open-finding wire forms", output)

    def test_packet_switch_validation_is_scoped_and_numbered(self) -> None:
        path = "templates/project-control-files/docs/sdad/playbooks/work-packets.md"
        ordered_decoy = (
            "```text\nselect next leaf\nclassify\nreview validation\nupdate state\n"
            "remove or replace\ndoctor strict\nproject checks\nadvance\nrerun doctor\n```\n\n"
        )
        mutations = (
            lambda text: text.replace(
                "8. Run project checks separately and record their bounded evidence.\n",
                "Project checks remain relevant.\n",
                1,
            ),
            lambda text: text.replace(
                "8. Run project checks separately and record their bounded evidence.\n"
                "9. Advance status only after the required evidence exists.\n",
                "9. Run project checks separately and record their bounded evidence.\n"
                "8. Advance status only after the required evidence exists.\n",
                1,
            ),
            lambda text: ordered_decoy
            + text.replace("## Packet Switch Transaction", "## Packet Transition Notes", 1),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate):
                output = self.assert_mutation_rejected(path, mutate)
                self.assertIn("Packet Switch Transaction", output)


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
                guide.replace(
                    "the completed `state.missing` finding and\nexit `1`",
                    "a completed `state.missing` finding",
                    1,
                ),
                encoding="utf-8",
            )

            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_rejects_wrong_getting_started_exit_meanings(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            fixture = Path(tmp)
            self.write_current_contract_fixture(fixture)
            original = (fixture / "docs/getting-started.md").read_text(
                encoding="utf-8"
            )
            cases = (
                (
                    "the completed `state.missing` finding and\nexit `1`",
                    "the completed `state.missing` finding and\nexit `2`",
                ),
                (
                    "fatal invocation or report-construction failure uses exit `2`",
                    "fatal invocation or report-construction failure uses exit `1`",
                ),
            )

            for index, (old, new) in enumerate(cases):
                with self.subTest(new=new):
                    root = fixture / str(index)
                    self.write_current_contract_fixture(root)
                    guide_path = root / "docs/getting-started.md"
                    guide_path.write_text(
                        original.replace(old, new, 1),
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
            guide_path.write_text(
                guide.replace(
                    "Doctor never executes validation commands.",
                    "Contradictory note: `state.missing` uses exit `2`.\n\n"
                    "Doctor never executes validation commands.",
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
        ):
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIsNone(
                    re.search(r"\bdoctor\b|scripts[/\\]sdad\.py", content, flags=re.I)
                )

    def test_v3_2_artwork_and_expanded_copy_prompt_are_canonical(self) -> None:
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
            "915eec2f2bc257897483c2616a0d08506f96db138d3f41c2bf827e039018f9c8",
        )


class PublicV32DocumentationContractTests(unittest.TestCase):
    CONTRACT_PATHS = (
        "README.md",
        "docs/no-clone-quick-install.md",
        "docs/getting-started.md",
        "docs/user-guide.md",
        "docs/owners-guide.md",
        "docs/ai-work-loop.md",
        "docs/session-handoff.md",
        "docs/known-limitations.md",
        "docs/pattern-catalog.md",
        "prompts/handoff-prompt.md",
        "templates/project-control-files/AGENTS.md",
    )

    def write_fixture(self, root: Path) -> None:
        for relative_path in self.CONTRACT_PATHS:
            source = ROOT / relative_path
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def validate(self, root: Path) -> None:
        validator = getattr(
            VALIDATE_REPO,
            "validate_public_v3_2_documentation_contract",
            None,
        )
        self.assertIsNotNone(validator, "public v3.2 documentation validator is missing")
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            validator()

    def mutate(self, root: Path, path: str, old: str, new: str) -> None:
        target = root / path
        content = target.read_text(encoding="utf-8")
        mutated = content.replace(old, new, 1)
        self.assertNotEqual(mutated, content, f"fixture mutation did not match {path}")
        target.write_text(mutated, encoding="utf-8")

    def assert_mutation_rejected(
        self,
        path: str,
        old: str,
        new: str,
        *,
        mirror_prompt: bool = False,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            self.mutate(root, path, old, new)
            if mirror_prompt:
                other = (
                    "README.md"
                    if path == "docs/no-clone-quick-install.md"
                    else "docs/no-clone-quick-install.md"
                )
                self.mutate(root, other, old, new)
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_current_public_v3_2_docs_satisfy_the_semantic_contract(self) -> None:
        self.validate(ROOT)

    def test_rejects_reintroduced_fixed_five_question_ritual(self) -> None:
        self.assert_mutation_rejected(
            "docs/no-clone-quick-install.md",
            "Do not make me answer a fixed questionnaire.",
            "Ask me Q1 through Q5 before inspecting the repository.",
            mirror_prompt=True,
        )

    def test_rejects_removed_no_clone_overwrite_guard(self) -> None:
        self.assert_mutation_rejected(
            "docs/no-clone-quick-install.md",
            "$targetItem = Get-Item -Force -LiteralPath $targetPath -ErrorAction SilentlyContinue\n"
            "if ($targetItem) {\n"
            "  if (($targetItem.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {\n"
            "    throw \"Refusing to install through linked path: $targetPath\"\n"
            "  }\n"
            "  throw \"Target already exists: $targetPath\"\n"
            "}",
            "$targetItem = $null\n# Existing targets may be replaced.",
        )

    def test_rejects_removed_no_clone_staging_or_atomic_publication(self) -> None:
        cases = (
            (
                "$tempPath = Join-Path $targetDir (\".sdad-download.\" + "
                "[guid]::NewGuid().ToString(\"N\") + \".tmp\")",
                "$tempPath = $targetPath",
            ),
            (
                "[IO.File]::Move($tempPath, $targetPath)",
                "Copy-Item -LiteralPath $tempPath -Destination $targetPath -Force",
            ),
        )
        for old, new in cases:
            with self.subTest(new=new):
                self.assert_mutation_rejected(
                    "docs/no-clone-quick-install.md",
                    old,
                    new,
                )

    def test_rejects_removed_no_clone_exact_target_postcondition(self) -> None:
        self.assert_mutation_rejected(
            "docs/no-clone-quick-install.md",
            "if [[ ! -f \"$target_path\" ]]; then\n"
            "  nested_temp=\"$target_path/$(basename \"$temp_path\")\"\n"
            "  if [[ -f \"$nested_temp\" ]]; then rm -- \"$nested_temp\"; fi\n"
            "  echo \"Publication did not create the exact target file: $target_path\" >&2\n"
            "  exit 1\n"
            "fi",
            "# Exact-target postcondition removed.",
        )

    def test_rejects_removed_handoff_pointer_marker_lifecycle(self) -> None:
        self.assert_mutation_rejected(
            "docs/session-handoff.md",
            "7. On packet switch, completion, archive, or replacement, remove or replace the\n"
            "   state pointer in the same coherence update. A handoff for another packet\n"
            "   cannot remain current.",
            "7. Keep the previous pointer for later reference.",
        )

    def test_rejects_removed_one_time_bootstrap_boundary(self) -> None:
        self.assert_mutation_rejected(
            "docs/user-guide.md",
            "The large copy-paste bootstrap prompt is for one-time install, upgrade,\n"
            "migration, or repair. Once installed, use the repository adapter and current\n"
            "state; do not paste the bootstrap prompt into every session.",
            "Paste the large bootstrap prompt into every session.",
        )

    def test_rejects_removed_authorization_action_reuse_and_expiry(self) -> None:
        self.assert_mutation_rejected(
            "docs/user-guide.md",
            "Authorized action:\nPacket:\nConditions:\nSource/artifact identity:\nExpires when:\n"
            "Evidence required before action:",
            "Packet:\nConditions:\nSource/artifact identity:\n"
            "Evidence required before action:",
        )

    def test_rejects_collapsed_or_divergent_readme_copy_prompt(self) -> None:
        cases = (
            ("## Copy-Paste Start Prompt", "<details>\n## Copy-Paste Start Prompt"),
            (
                "Use the SDAD Protocol (SPEC-Directed AI Development)",
                "Use a modified SDAD Protocol (SPEC-Directed AI Development)",
            ),
        )
        for old, new in cases:
            with self.subTest(new=new):
                self.assert_mutation_rejected("README.md", old, new)

    def test_rejects_current_positioning_drift(self) -> None:
        cases = (
            (
                "README.md",
                "SPEC-Directed AI Development: a repository-local operating protocol",
                "SPEC-Driven AI Development: a development methodology",
            ),
            (
                "docs/known-limitations.md",
                "method-agnostic,\ntool- and model-neutral",
                "model-specific,\ntool-dependent",
            ),
            (
                "docs/ai-work-loop.md",
                "not a prescribed implementation method",
                "the prescribed implementation method",
            ),
        )
        for path, old, new in cases:
            with self.subTest(path=path):
                self.assert_mutation_rejected(path, old, new)

    def test_rejects_current_legacy_vocabulary_before_migration(self) -> None:
        self.assert_mutation_rejected(
            "docs/user-guide.md",
            "## Migrating From SDAD 3.1",
            "Use Level 4 Release-gated Autonomy for release.\n\n"
            "## Migrating From SDAD 3.1",
        )


class PublicRelationshipHelperTests(unittest.TestCase):
    def assert_rejected(self, helper: object, content: str, label: str) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                helper(content, label)

    def test_accepts_positive_report_schema_relationship(self) -> None:
        helper = VALIDATE_REPO._require_report_schema_relationship
        helper(
            "Existing v1 calls use report schema 1. State v2 calls use report schema 2.",
            "positive schema relation",
        )

    def test_accepts_negative_report_schema_clarification(self) -> None:
        helper = VALIDATE_REPO._require_report_schema_relationship
        helper(
            "V1 does not use report schema 2 and remains on report schema 1. "
            "State v2 does not use report schema 1 and uses report schema 2.",
            "negative schema clarification",
        )

    def test_rejects_reversed_report_schema_relationship(self) -> None:
        helper = VALIDATE_REPO._require_report_schema_relationship
        self.assert_rejected(
            helper,
            "V1 uses report schema 2 and does not use report schema 1. "
            "State v2 uses report schema 1 and does not use report schema 2.",
            "reversed schema relation",
        )

    def test_accepts_positive_three_control_relationship(self) -> None:
        helper = VALIDATE_REPO._require_three_control_relationship
        helper(
            "Execution scope determines how far work proceeds now. Owner gates "
            "determine which protected actions require the owner.",
            "positive three-control relation",
        )

    def test_accepts_negative_execution_scope_clarification(self) -> None:
        helper = VALIDATE_REPO._require_three_control_relationship
        helper(
            "Execution scope determines how far work proceeds and does not authorize "
            "protected actions. Owner gates require owner authorization for protected actions.",
            "negative scope clarification",
        )

    def test_rejects_reversed_owner_gate_relationship(self) -> None:
        helper = VALIDATE_REPO._require_three_control_relationship
        self.assert_rejected(
            helper,
            "Execution scope determines how far work proceeds and authorizes protected "
            "actions. Owner gates do not require the owner for protected actions.",
            "reversed owner-gate relation",
        )

    def test_accepts_positive_routed_docs_relationship(self) -> None:
        helper = VALIDATE_REPO._require_routed_docs_selection_relationship
        helper(
            "routed_docs is an eligible selection set, not an instruction to read every file.",
            "positive routed-docs relation",
        )

    def test_accepts_negative_routed_docs_clarification(self) -> None:
        helper = VALIDATE_REPO._require_routed_docs_selection_relationship
        helper(
            "routed_docs is an eligible selection set and is not a read-all route.",
            "negative routed-docs clarification",
        )

    def test_rejects_reversed_routed_docs_relationship(self) -> None:
        helper = VALIDATE_REPO._require_routed_docs_selection_relationship
        self.assert_rejected(
            helper,
            "routed_docs is an eligible selection set that requires reading every file "
            "as a read-all route.",
            "reversed routed-docs relation",
        )


class LongRunningLifecycleContractTests(unittest.TestCase):
    CONTRACT_PATHS = (
        "templates/project-control-files/sdad-state.yaml",
        "templates/project-control-files/AGENTS.md",
        "templates/project-control-files/SPEC/SPEC-COMPLETE.md",
        "templates/project-control-files/SPEC/adr/ADR-0001-template.md",
        "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
        "templates/project-control-files/docs/sdad/playbooks/documentation-and-handoff.md",
        "templates/project-control-files/docs/sdad/playbooks/evidence-and-risk-gates.md",
        "templates/project-control-files/docs/implementation-notes.md",
        "templates/project-control-files/docs/TODO-Open-Items.md",
        "templates/project-control-files/review-findings.md",
        "templates/project-control-files/docs/evidence-matrix.md",
        "templates/project-control-files/docs/claim-registry.md",
        "templates/project-control-files/docs/work-packet-state.md",
        "templates/project-control-files/docs/INDEX.md",
        "docs/ai-work-loop.md",
        "docs/implicit-rules.md",
        "docs/known-limitations.md",
        "docs/session-handoff.md",
    )

    def write_fixture(self, root: Path) -> None:
        for relative_path in self.CONTRACT_PATHS:
            source = ROOT / relative_path
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source.read_text(encoding="utf-8"), encoding="utf-8")

    def validate(self, root: Path) -> None:
        validator = getattr(
            VALIDATE_REPO,
            "validate_long_running_lifecycle_contract",
            None,
        )
        self.assertIsNotNone(validator, "long-running lifecycle validator is missing")
        with mock.patch.object(VALIDATE_REPO, "ROOT", root):
            validator()

    def assert_mutation_rejected(
        self,
        path: str,
        old: str,
        new: str,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_fixture(root)
            target = root / path
            content = target.read_text(encoding="utf-8")
            mutated = content.replace(old, new, 1)
            self.assertNotEqual(mutated, content, f"fixture mutation did not match {path}")
            target.write_text(mutated, encoding="utf-8")
            with contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    self.validate(root)

    def test_current_long_running_contract_is_coherent(self) -> None:
        self.validate(ROOT)

    def test_rejects_loss_of_the_single_active_spec_entrypoint(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/AGENTS.md",
            "single normative SPEC entrypoint",
            "one optional SPEC hint",
        )

    def test_rejects_reuse_of_an_accepted_packet_for_material_change(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/SPEC/SPEC-COMPLETE.md",
            "new, never-reused packet ID",
            "existing accepted packet ID",
        )

    def test_rejects_cyclic_or_implicit_spec_precedence(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/SPEC/SPEC-COMPLETE.md",
            "Keep lineage acyclic",
            "Allow lineage cycles",
        )

    def test_rejects_line_count_as_the_only_packet_split_rule(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "Line count alone",
            "Line count",
        )

    def test_rejects_child_only_closure_of_a_split_parent(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "After the children finish, reconcile",
            "After one child finishes, close",
        )

    def test_rejects_split_without_a_durable_parent_envelope(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "parent packet ID, objective, active SPEC path and revision",
            "parent summary",
        )

    def test_rejects_inactive_split_parent_in_active_work(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "under `Future / Deferred`",
            "under `Active Work`",
        )

    def test_rejects_loss_of_deferred_finding_lane(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/review-findings.md",
            "## Future / Deferred Findings",
            "## Recently Hidden Findings",
        )

    def test_rejects_release_without_deferred_finding_scan(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/evidence-and-risk-gates.md",
            "## Deferred Finding Gate",
            "## Deferred Finding Notes",
        )

    def test_rejects_loss_of_terminal_revision_bound_decision(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "## Terminal Packet Decision Record",
            "## Optional Historical Note",
        )

    def test_rejects_overwriting_a_revised_terminal_decision(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "- Revises/supersedes decisions:\n  - None | path/URL/ID",
            "- Replace prior decision in place: yes",
        )

    def test_rejects_automatic_winner_for_parallel_owner_decisions(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "neither is\nautomatically current: hold the affected claim",
            "the newest is\nautomatically current: release the affected claim",
        )

    def test_rejects_deleting_expired_authorization_history(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "retain the immutable record in history",
            "delete the record permanently",
        )

    def test_rejects_authorization_without_source_identity(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "- Source/artifact identity:\n- Expires when:",
            "- Expires when:",
        )

    def test_rejects_revocation_without_authorization_predecessor(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "- Revises/supersedes authorizations:\n  - None | path/URL/ID",
            "- Prior authorization was overwritten: yes",
        )

    def test_rejects_revocation_that_leaves_the_gate_satisfied(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/work-packet-state.md",
            "Keep or restore the affected\ngate in state `owner_gates` as unsatisfied",
            "Keep the affected\ngate satisfied",
        )

    def test_rejects_global_handoff_sequence_instead_of_date_scoped_ids(self) -> None:
        self.assert_mutation_rejected(
            "docs/session-handoff.md",
            "Start a\n   new date at `H0001`",
            "Continue the\n   global sequence across every date",
        )

    def test_rejects_handoff_next_action_before_current_owner_redirect(self) -> None:
        self.assert_mutation_rejected(
            "docs/session-handoff.md",
            "Apply any\n   current owner redirect before the recorded next action",
            "Follow the recorded next action before any\n   current owner redirect",
        )

    def test_rejects_rule5_without_enforcement_and_regression_evidence(self) -> None:
        self.assert_mutation_rejected(
            "docs/implicit-rules.md",
            "-> enforcement plus regression evidence",
            "-> another reminder in chat",
        )

    def test_rejects_rule5_without_retirement_route(self) -> None:
        self.assert_mutation_rejected(
            "docs/implicit-rules.md",
            "-> Keep / Refine / Merge / Retire",
            "-> Keep forever",
        )

    def test_rejects_continuing_old_work_after_owner_spec_adoption(self) -> None:
        self.assert_mutation_rejected(
            "docs/ai-work-loop.md",
            "treat it as a current change request; hold affected work",
            "treat it as a current change request; continue old work",
        )

    def test_rejects_implementing_a_review_only_spec(self) -> None:
        self.assert_mutation_rejected(
            "docs/ai-work-loop.md",
            "keep the request read-only; report conflicts without incorporating",
            "implement the request; report conflicts after incorporating",
        )

    def test_rejects_automatic_authority_for_a_discovered_spec(self) -> None:
        self.assert_mutation_rejected(
            "docs/ai-work-loop.md",
            "it gains no authority from filename, date, or status",
            "it becomes authoritative from filename, date, or status",
        )

    def test_rejects_ignoring_a_current_owner_redirect(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "Stop affected local and delegated work",
            "Continue affected local and delegated work",
        )

    def test_rejects_packet_switch_when_an_existing_gate_is_satisfied(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "Continue the same packet when action",
            "Create a new packet when action",
        )

    def test_rejects_reopening_terminal_history_under_the_same_packet(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "Never move a terminal",
            "Move a terminal",
        )

    def test_rejects_shared_write_leaf_across_independent_worktrees(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "use distinct child leaf packet IDs",
            "share one leaf packet ID",
        )

    def test_rejects_rewriting_acceptance_for_a_post_acceptance_defect(self) -> None:
        self.assert_mutation_rejected(
            "docs/ai-work-loop.md",
            "do not rewrite acceptance",
            "rewrite acceptance",
        )

    def test_rejects_new_packet_for_matching_current_background_result(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "keep the packet only if identity/acceptance/gates match",
            "create a new packet even if identity/acceptance/gates match",
        )

    def test_rejects_owner_deferral_as_recently_closed(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/TODO-Open-Items.md",
            "owner resolution/acceptance decision",
            "owner deferral decision",
        )

    def test_rejects_closure_without_evidence_decision_or_supersession(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/documentation-and-handoff.md",
            "bounded completion evidence",
            "text relocation",
        )

    def test_rejects_duplicated_owner_acceptance_in_evidence_ledgers(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/evidence-matrix.md",
            "## Owner Decision References",
            "## Local Owner Acceptance Copy",
        )

    def test_rejects_undefined_owner_decision_authority(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/documentation-and-handoff.md",
            "one authority per decision",
            "one mutable copy per ledger",
        )

    def test_rejects_pre_integration_release_evidence(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/sdad/playbooks/evidence-and-risk-gates.md",
            "final integrated",
            "pre-merge",
        )

    def test_rejects_age_only_implementation_note_compaction(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/implementation-notes.md",
            "current effect rather than age",
            "file age alone",
        )

    def test_rejects_forcing_implement_into_read_only_packets(self) -> None:
        self.assert_mutation_rejected(
            "docs/ai-work-loop.md",
            "not applicable",
            "mandatory",
        )

    def test_rejects_missing_phase_skip_rule_from_installed_kernel(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/AGENTS.md",
            "phase N/A",
            "phase mandatory",
        )

    def test_rejects_missing_blocked_packet_route_without_handoff(self) -> None:
        self.assert_mutation_rejected(
            "templates/project-control-files/docs/INDEX.md",
            "blocked/deferred",
            "unrelated status",
        )


class DoctorSourceVersionContractTests(unittest.TestCase):
    def validate_source(self, source: str) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "scripts").mkdir()
            (root / "docs").mkdir()
            (root / "scripts" / "sdad.py").write_text(source, encoding="utf-8")
            for relative_path in (
                "scripts/install-agent-adapter.ps1",
                "scripts/install-agent-adapter.sh",
                "docs/no-clone-quick-install.md",
            ):
                (root / relative_path).write_text(
                    "Adapter-only installation surface.\n",
                    encoding="utf-8",
                )
            with mock.patch.object(VALIDATE_REPO, "ROOT", root):
                VALIDATE_REPO.validate_doctor_checkout_contract()

    def assert_source_rejected(self, source: str) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                self.validate_source(source)

    def test_doctor_source_uses_three_exact_named_version_domains(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        self.assertRegex(source, r'(?m)^DOCTOR_VERSION = "3\.2\.2"$')
        self.assertRegex(source, r"(?m)^LEGACY_REPORT_SCHEMA_VERSION = 1$")
        self.assertRegex(source, r"(?m)^REPORT_SCHEMA_VERSION = 2$")
        self.assertNotRegex(source, r"(?m)^SCHEMA_VERSION\s*=")

    def test_report_schema_selection_owns_the_only_state_v2_mapping(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        self.assertIn("def _select_report_schema(", source)
        self.assertEqual(source.count("state_version == 2"), 1)

    def test_current_doctor_source_satisfies_checkout_contract(self) -> None:
        VALIDATE_REPO.validate_doctor_checkout_contract()

    def test_rejects_computed_doctor_version_hidden_by_literal_decoy(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            'DOCTOR_VERSION = "3.2.2"',
            '# DOCTOR_VERSION = "3.2.2"\nDOCTOR_VERSION = "3." + "2.2"',
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_version_reassignment_after_correct_literal(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            'DOCTOR_VERSION = "3.2.2"',
            'DOCTOR_VERSION = "3.2.2"\nDOCTOR_VERSION = "3.2.3"',
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_augmented_version_reassignment(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            'DOCTOR_VERSION = "3.2.2"',
            'DOCTOR_VERSION = "3.2.2"\nDOCTOR_VERSION += ".1"',
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_named_expression_version_reassignment(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            'DOCTOR_VERSION = "3.2.2"',
            'DOCTOR_VERSION = "3.2.2"\n(DOCTOR_VERSION := "3.2.3")',
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_starred_version_reassignment(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            'DOCTOR_VERSION = "3.2.2"',
            'DOCTOR_VERSION = "3.2.2"\n*DOCTOR_VERSION, = ["3.2.3"]',
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_deleting_required_version_constants(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        for name in (
            "DOCTOR_VERSION",
            "LEGACY_REPORT_SCHEMA_VERSION",
            "REPORT_SCHEMA_VERSION",
        ):
            with self.subTest(name=name):
                self.assert_source_rejected(source + f"\ndel {name}\n")

    def test_rejects_annotated_generic_schema_version(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            "REPORT_SCHEMA_VERSION = 2",
            "REPORT_SCHEMA_VERSION = 2\nSCHEMA_VERSION: int = 1",
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_named_expression_generic_schema_version(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        mutated = source.replace(
            "REPORT_SCHEMA_VERSION = 2",
            "REPORT_SCHEMA_VERSION = 2\n(SCHEMA_VERSION := 1)",
            1,
        )
        self.assertNotEqual(mutated, source)
        self.assert_source_rejected(mutated)

    def test_rejects_other_common_python_bindings(self) -> None:
        source = (ROOT / "scripts" / "sdad.py").read_text(encoding="utf-8")
        cases = {
            "for-target": "for DOCTOR_VERSION in ():\n    pass",
            "with-target": "with context() as DOCTOR_VERSION:\n    pass",
            "comprehension-target": "[None for DOCTOR_VERSION in ()]",
            "function-name": "def DOCTOR_VERSION():\n    pass",
            "class-name": "class DOCTOR_VERSION:\n    pass",
            "import-alias": "import package as DOCTOR_VERSION",
            "from-import-alias": "from package import value as DOCTOR_VERSION",
            "wildcard-import": "from package import *",
            "except-name": (
                "try:\n    pass\n"
                "except Exception as DOCTOR_VERSION:\n    pass"
            ),
            "pattern-capture": (
                "match {}:\n"
                '    case {"key": DOCTOR_VERSION}:\n'
                "        pass"
            ),
            "argument": "def helper(DOCTOR_VERSION):\n    pass",
        }
        for name, binding in cases.items():
            with self.subTest(name=name):
                self.assert_source_rejected(source + "\n" + binding + "\n")


class InternalWorkspaceIgnoreContractTests(unittest.TestCase):
    def test_internal_superpowers_workspaces_are_root_ignored(self) -> None:
        entries = {
            line.strip()
            for line in (ROOT / ".gitignore").read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        self.assertIn("/.superpowers/", entries)
        self.assertIn("/docs/superpowers/", entries)


class StableReleaseContractTests(unittest.TestCase):
    EXPECTED_BASELINE_REVISION = "adfd40afd4e1d3fcaba64cc3f5be936c5feb51fd"
    EXPECTED_SOURCES = {
        "mini": {
            "path": "templates/mini-sdad/MINI-SDAD.md",
            "sha256": "0bd02d52289bf92607520bec6ef3e08715ec91f586350ba31dda5cdb1d1db7b6",
        },
        "codex": {
            "path": "adapters/codex/AGENTS.md",
            "target": "AGENTS.md",
            "sha256": "8237f7905ba8ce0db95e77b5d40e54200062d2654adae45e667f04743f342e08",
        },
        "claude-code": {
            "path": "adapters/claude-code/CLAUDE.md",
            "target": "CLAUDE.md",
            "sha256": "57a9431eecc5d8e2dfdfe71eb59ad673ff230db5c320197291a8a7a129f875ce",
        },
        "gemini-cli": {
            "path": "adapters/gemini-cli/GEMINI.md",
            "target": "GEMINI.md",
            "sha256": "b3a6e16c21e14e594bdc5560838c664e3116ef1ee1366724a6b39a19a9e2e76b",
        },
        "cursor": {
            "path": "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            "target": ".cursor/rules/spec-driven-ai-development.mdc",
            "sha256": "789d378813f7b32f0e677265fa23c7908cf6b52342fc54e92455d05293038bfc",
        },
        "github-copilot": {
            "path": "adapters/github-copilot/.github/copilot-instructions.md",
            "target": ".github/copilot-instructions.md",
            "sha256": "ee914a5ebaa5413c7bfd43d21b48e6919fc3e373afed5707bc6076acf5a573b3",
        },
        "generic": {
            "path": "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
            "target": "AI-SESSION-INSTRUCTIONS.md",
            "sha256": "15e02a42c32e46b332dc217ac43abad958d35e5a153f0f9746be42a32eee5ec2",
        },
    }

    def test_manifest_has_exact_v3_2_2_identity_and_baseline_sources(self) -> None:
        manifest = json.loads((ROOT / "install-sources.json").read_text(encoding="utf-8"))
        self.assertEqual(manifest["schema_version"], 1)
        self.assertEqual(manifest["label"], "v3.2.2 stable baseline")
        self.assertEqual(manifest["revision"], self.EXPECTED_BASELINE_REVISION)
        self.assertEqual(
            manifest["capabilities"],
            {"progressive_control_plane": True},
        )
        self.assertEqual(manifest["sources"], self.EXPECTED_SOURCES)
        self.assertEqual(set(manifest["sources"]), VALIDATE_REPO.INSTALL_SOURCE_KEYS)
        self.assertNotIn("doctor", manifest["sources"])
        self.assertEqual(VALIDATE_REPO.STABLE_RELEASE_SOURCES, self.EXPECTED_SOURCES)

    def test_v3_2_2_release_identity_surfaces_are_present(self) -> None:
        release = (ROOT / "docs/releases/v3.2.2.md").read_text(encoding="utf-8")
        self.assertIn("# SDAD v3.2.2", release)
        self.assertIn("Release date: 2026-07-15", release)
        self.assertIn("Tag: `v3.2.2`", release)
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        self.assertRegex(
            changelog,
            r"(?s)\A# Changelog\n\n## Unreleased\n\n.+?\n\n"
            r"## 3\.2\.2 - 2026-07-15\n",
        )
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/releases/v3.2.2.md", readme)
        self.assertNotIn("<details", readme)
        self.assertNotIn("<summary", readme)

    def test_v3_2_2_release_counts_distinguish_run_from_skipped(self) -> None:
        expected = "ran 443 tests, with three"
        overclaim = "passed 443 tests with three"
        for relative_path in (
            "docs/releases/v3.2.2.md",
            "docs/known-limitations.md",
        ):
            with self.subTest(path=relative_path):
                content = (ROOT / relative_path).read_text(encoding="utf-8")
                self.assertIn(expected, content)
                self.assertNotIn(overclaim, content)

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
