from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def line_count(text: str) -> int:
    return len(text.splitlines())


def fenced_prompt(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^{re.escape(heading)}\s+.*?^```text\s*\n(.*?)^```\s*$",
        text,
    )
    if match is None:
        raise AssertionError(f"Missing fenced prompt under {heading}")
    return match.group(1)


def substantive_lines(text: str) -> set[str]:
    return {
        line.strip()
        for line in text.splitlines()
        if len(line.strip()) >= 30
    }


class AgentExperienceSurfaceTests(unittest.TestCase):
    def test_always_loaded_control_plane_stays_small(self) -> None:
        agents = read("templates/project-control-files/AGENTS.md")
        index = read("templates/project-control-files/docs/INDEX.md")
        state_path = ROOT / "templates/project-control-files/sdad-state.yaml"

        self.assertTrue(state_path.is_file(), "sdad-state.yaml must be the first-read state")
        state = state_path.read_text(encoding="utf-8")
        self.assertLessEqual(line_count(agents), 120)
        self.assertLessEqual(line_count(index), 80)
        self.assertLessEqual(line_count(state), 80)
        self.assertLessEqual(
            len(agents) + len(index) + len(state),
            12_000,
            "the fixed startup control plane should stay below ~3k rough tokens",
        )

    def test_active_state_exposes_the_minimum_routing_contract(self) -> None:
        state = read("templates/project-control-files/sdad-state.yaml")

        self.assertIn(
            "intensity: medium",
            state,
            "the active-state template must use the official Low/Medium/High taxonomy",
        )

        for key in (
            "scale:",
            "intensity:",
            "autonomy:",
            "active_spec:",
            "active_packet:",
            "owner_gates:",
            "validation:",
            "routed_docs:",
        ):
            with self.subTest(key=key):
                self.assertIn(key, state)

        self.assertIn("0 = ask-first", state)
        self.assertIn("3 = session", state)

    def test_project_templates_route_the_installed_tool_adapter(self) -> None:
        surfaces = (
            "templates/project-control-files/README.md",
            "templates/project-control-files/docs/INDEX.md",
            "templates/project-control-files/docs/Repository-Operating-Rules.md",
            "templates/project-control-files/docs/sdad/handoffs/YYYY-MM-DD-topic.md",
        )

        for path in surfaces:
            with self.subTest(path=path):
                self.assertIn("installed tool adapter", read(path).lower())

        handoff = read(
            "templates/project-control-files/docs/sdad/handoffs/YYYY-MM-DD-topic.md"
        )
        self.assertIn("Change type and routed documentation surfaces", handoff)
        self.assertNotIn("Minimum update-set row", handoff)
        self.assertLess(
            handoff.find("First, load the installed tool adapter"),
            handoff.find("Then read this current handoff only as deeply as needed"),
        )
        self.assertIn("authorized private data", handoff)

        for path in (
            "docs/field-notes/documentation-governance-method.md",
            "docs/anti-patterns.md",
        ):
            with self.subTest(path=path):
                content = read(path)
                self.assertIn("installed tool adapter", content)
                self.assertIn("authorized private data", content)

    def test_mini_escalation_does_not_reject_its_own_scale_gate(self) -> None:
        mini = read("templates/mini-sdad/MINI-SDAD.md")
        cursor = read("templates/mini-sdad/cursor-mini-sdad.mdc")

        self.assertNotIn("the work spans multiple AI sessions", mini)
        self.assertNotIn("the owner will return to the project later", mini)
        self.assertIn("three or more persistence/evidence signals", mini)
        self.assertIn("another owner-controlled gate", mini)
        self.assertTrue(cursor.rstrip().endswith(mini.rstrip()))

    def test_kickoff_keeps_readme_triggered_instead_of_mandatory(self) -> None:
        kickoff = read("prompts/kickoff-prompt.md")

        self.assertIn("Create or update `README.md` only when", kickoff)

    def test_readme_has_one_start_and_the_canonical_option_one_prompt(self) -> None:
        readme = read("README.md")
        no_clone = read("docs/no-clone-quick-install.md")
        start_headings = re.findall(r"^## Start Here(?:\:.*)?$", readme, re.MULTILINE)

        self.assertEqual(start_headings, ["## Start Here"])
        prompt_section = re.search(
            r"^## Copy-Paste Start Prompt\s+(.*?)(?=^## |\Z)",
            readme,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(prompt_section)
        self.assertNotRegex(prompt_section.group(1), r"(?i)<\s*(?:details|summary)\b")
        prompt_match = re.search(
            r"^## Copy-Paste Start Prompt\s+.*?^```(?:text)?\s*\n(.*?)^```",
            readme,
            re.MULTILINE | re.DOTALL,
        )
        self.assertIsNotNone(prompt_match, "README must keep one copy-paste start prompt")
        self.assertEqual(
            fenced_prompt(readme, "## Copy-Paste Start Prompt"),
            fenced_prompt(no_clone, "## Option 1: Give This To Your AI Agent"),
        )

    def test_always_loaded_rules_do_not_duplicate_the_full_rulebook(self) -> None:
        agents = read("templates/project-control-files/AGENTS.md")
        rules = read("templates/project-control-files/docs/Repository-Operating-Rules.md")
        overlap = substantive_lines(agents) & substantive_lines(rules)

        self.assertLessEqual(
            len(overlap),
            30,
            f"always-loaded AGENTS duplicates {len(overlap)} full-rulebook lines",
        )
        self.assertIn("progressive", agents.lower())
        self.assertIn("on demand", agents.lower())

    def test_tool_adapters_stay_bounded_and_route_progressively(self) -> None:
        adapters = (
            "adapters/codex/AGENTS.md",
            "adapters/claude-code/CLAUDE.md",
            "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            "adapters/github-copilot/.github/copilot-instructions.md",
            "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
        )

        for path in adapters:
            with self.subTest(path=path):
                content = read(path)
                self.assertLessEqual(line_count(content), 120)
                self.assertIn("docs/INDEX.md", content)
                self.assertIn("Sensitive Data", content)
                self.assertIn("owner", content.lower())
                self.assertIn("on demand", content.lower())

    def test_bootstrap_skill_uses_progressive_disclosure(self) -> None:
        skill = read("skills/ai-spec-project-start/SKILL.md")

        self.assertLessEqual(line_count(skill), 500)
        self.assertLessEqual(len(skill), 25_000)
        for route in (
            "references/runtime-contract.md",
            "references/starter-templates.md",
            "references/field-patterns.md",
            "references/implicit-rules.md",
        ):
            with self.subTest(route=route):
                self.assertIn(route, skill)
                self.assertTrue((ROOT / "skills/ai-spec-project-start" / route).is_file())

    def test_scale_contract_is_consistent_across_active_surfaces(self) -> None:
        surfaces = (
            "templates/project-control-files/AGENTS.md",
            "templates/project-control-files/docs/sdad/playbooks/work-packets.md",
            "skills/ai-spec-project-start/SKILL.md",
            "skills/ai-spec-project-start/references/runtime-contract.md",
            "README.md",
            "docs/getting-started.md",
            "docs/fit-assessment.md",
            "docs/no-clone-quick-install.md",
            "prompts/kickoff-prompt.md",
        )

        for path in surfaces:
            contract = read(path).lower()
            with self.subTest(path=path):
                self.assertIn("inspects, documents, or tests", contract)
                self.assertIn("changes, accepts, or executes", contract)

    def test_current_spec_sections_override_historical_material(self) -> None:
        surfaces = (
            "templates/project-control-files/AGENTS.md",
            "templates/project-control-files/docs/Repository-Operating-Rules.md",
            "skills/ai-spec-project-start/references/runtime-contract.md",
        )

        for path in surfaces:
            with self.subTest(path=path):
                self.assertIn(
                    "current active sections override older",
                    read(path).lower(),
                )


class AgentExperienceValidatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        module_path = ROOT / "scripts" / "sdad_validator" / "agent_experience.py"
        if not module_path.is_file():
            raise AssertionError("agent experience validator module is missing")

        spec = importlib.util.spec_from_file_location(
            "agent_experience_under_test",
            module_path,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("could not import agent experience validator")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def build_valid_tree(self, root: Path) -> None:
        adapter_paths = (
            "templates/project-control-files/AGENTS.md",
            "adapters/codex/AGENTS.md",
            "adapters/claude-code/CLAUDE.md",
            "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            "adapters/github-copilot/.github/copilot-instructions.md",
            "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
        )
        adapter = (
            "# Agent\n"
            "sdad-state.yaml\n"
            "docs/INDEX.md\n"
            "current source and tests\n"
            "one routed path, then load optional policy on demand\n"
            "docs/Repository-Operating-Rules.md\n"
            "## Sensitive Data\nowner gate; load rules on demand\n"
        )
        for relative_path in adapter_paths:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(adapter, encoding="utf-8")

        rules = root / "templates/project-control-files/docs/Repository-Operating-Rules.md"
        rules.parent.mkdir(parents=True, exist_ok=True)
        rules.write_text("# Rules\n", encoding="utf-8")

        (root / "templates/project-control-files/docs/INDEX.md").write_text(
            "# Index\n"
            "sdad-state.yaml\n"
            "SPEC/SPEC-COMPLETE.md\n"
            "TODO-Open-Items.md\n"
            "review-findings.md\n"
            "implementation-notes.md\n"
            "save-state.md\n"
            "sdad/playbooks/context-and-data.md\n"
            "sdad/playbooks/work-packets.md\n"
            "sdad/playbooks/evidence-and-risk-gates.md\n"
            "sdad/playbooks/documentation-and-handoff.md\n"
            "sdad/playbooks/advanced-extensions.md\n",
            encoding="utf-8",
        )
        (root / "templates/project-control-files/sdad-state.yaml").write_text(
            "scale: standard\n"
            "intensity: medium\n"
            "autonomy: 2\n"
            "active_spec: SPEC/SPEC-COMPLETE.md\n"
            "active_packet:\n"
            "  id: packet-1\n"
            "  objective: Validate the compact control plane.\n"
            "  status: not_started\n"
            "owner_gates: []\n"
            "validation: []\n"
            "routed_docs: []\n",
            encoding="utf-8",
        )
        (root / "README.md").write_text(
            "## Start Here\n"
            "[User guide](docs/user-guide.md)\n"
            "[Getting started](docs/getting-started.md)\n\n"
            "## Copy-Paste Start Prompt\n\n"
            "```text\nstart\n```\n",
            encoding="utf-8",
        )

    def collect(self, root: Path) -> list[str]:
        return self.module.collect_agent_experience_violations(root)

    def test_accepts_a_complete_compact_control_plane(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)

            self.assertEqual(self.collect(root), [])

    def test_readme_copy_prompt_cannot_be_collapsed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            readme = root / "README.md"
            readme.write_text(
                readme.read_text(encoding="utf-8").replace(
                    "```text\nstart\n```",
                    "<details>\n<summary>Show prompt</summary>\n\n"
                    "```text\nstart\n```\n</details>",
                ),
                encoding="utf-8",
            )

            self.assertIn(
                "README copy-paste start prompt must remain expanded",
                self.collect(root),
            )

    def test_reports_line_budget_violation_without_fixture_noise(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            path = root / "templates/project-control-files/AGENTS.md"
            current = path.read_text(encoding="utf-8").splitlines()
            path.write_text(
                "\n".join(current + ["# filler"] * (121 - len(current))) + "\n",
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                [
                    "templates/project-control-files/AGENTS.md exceeds 120 lines: 121"
                ],
            )

    def test_reports_single_line_character_budget_violation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            required_routes = (
                "sdad-state.yaml SPEC/SPEC-COMPLETE.md TODO-Open-Items.md "
                "review-findings.md implementation-notes.md save-state.md "
                "sdad/playbooks/context-and-data.md "
                "sdad/playbooks/work-packets.md "
                "sdad/playbooks/evidence-and-risk-gates.md "
                "sdad/playbooks/documentation-and-handoff.md "
                "sdad/playbooks/advanced-extensions.md "
            )
            (root / "templates/project-control-files/docs/INDEX.md").write_text(
                required_routes + "x" * (4_001 - len(required_routes)),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                [
                    "templates/project-control-files/docs/INDEX.md exceeds "
                    "4000 characters: 4001"
                ],
            )

    def test_state_keys_must_be_top_level_not_comments(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            state_path = root / "templates/project-control-files/sdad-state.yaml"
            state_path.write_text(
                state_path.read_text(encoding="utf-8").replace(
                    "scale: standard",
                    "# scale: standard",
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                ["sdad-state.yaml missing top-level key: scale"],
            )

    def test_state_rejects_unknown_routing_values(self) -> None:
        cases = (
            ("scale: standard", "scale: huge", "unsupported scale: huge"),
            (
                "intensity: medium",
                "intensity: normal",
                "unsupported intensity: normal",
            ),
            ("autonomy: 2", "autonomy: 9", "unsupported autonomy: 9"),
        )

        for old, new, expected in cases:
            with self.subTest(value=new), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.build_valid_tree(root)
                path = root / "templates/project-control-files/sdad-state.yaml"
                state = path.read_text(encoding="utf-8").replace(old, new)
                path.write_text(state, encoding="utf-8")

                self.assertIn(expected, self.collect(root))

    def test_state_accepts_every_documented_autonomy_level(self) -> None:
        for level in ("0", "1", "2", "3", "4"):
            with self.subTest(level=level), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.build_valid_tree(root)
                path = root / "templates/project-control-files/sdad-state.yaml"
                state = path.read_text(encoding="utf-8").replace(
                    "autonomy: 2",
                    f"autonomy: {level}",
                )
                path.write_text(state, encoding="utf-8")

                self.assertNotIn(f"unsupported autonomy: {level}", self.collect(root))

    def test_state_rejects_duplicate_keys_and_invalid_packet_contract(self) -> None:
        cases = (
            (
                "scale: standard",
                "scale: standard\nscale: full",
                "sdad-state.yaml duplicate top-level key: scale",
            ),
            (
                "  status: not_started",
                "  status: invented",
                "unsupported active_packet status: invented",
            ),
            (
                "  objective: Validate the compact control plane.\n",
                "",
                "sdad-state.yaml active_packet missing key: objective",
            ),
            (
                "active_spec: SPEC/SPEC-COMPLETE.md",
                "active_spec: ../outside.md",
                "sdad-state.yaml active_spec must be a relative path: ../outside.md",
            ),
        )

        for old, new, expected in cases:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.build_valid_tree(root)
                path = root / "templates/project-control-files/sdad-state.yaml"
                path.write_text(
                    path.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8",
                )

                self.assertIn(expected, self.collect(root))

    def test_state_rejects_malformed_control_collections(self) -> None:
        cases = (
            (
                "active_packet:\n"
                "  id: packet-1\n"
                "  objective: Validate the compact control plane.\n"
                "  status: not_started",
                "active_packet: nope",
                "sdad-state.yaml active_packet must be a mapping",
            ),
            (
                "owner_gates: []",
                "owner_gates: disabled",
                "sdad-state.yaml owner_gates must be a list",
            ),
            (
                "validation: []",
                "validation: true",
                "sdad-state.yaml validation must be a list",
            ),
            (
                "routed_docs: []",
                "routed_docs: all",
                "sdad-state.yaml routed_docs must be a list",
            ),
        )

        for old, new, expected in cases:
            with self.subTest(value=new), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.build_valid_tree(root)
                path = root / "templates/project-control-files/sdad-state.yaml"
                state = path.read_text(encoding="utf-8").replace(old, new)
                path.write_text(state, encoding="utf-8")

                self.assertIn(expected, self.collect(root))

    def test_startup_surfaces_require_the_ordered_progressive_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            path = root / "adapters/codex/AGENTS.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace("docs/INDEX.md\n", ""),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                ["adapters/codex/AGENTS.md missing ordered route: docs/INDEX.md"],
            )

    def test_startup_route_cannot_skip_source_tests_and_the_routed_path(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            path = root / "adapters/codex/AGENTS.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "current source and tests\n"
                    "one routed path, then load optional policy on demand\n",
                    "",
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                ["adapters/codex/AGENTS.md missing ordered route: current source"],
            )

    def test_index_requires_each_current_state_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            path = root / "templates/project-control-files/docs/INDEX.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace("save-state.md\n", ""),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                [
                    "templates/project-control-files/docs/INDEX.md missing route: "
                    "save-state.md"
                ],
            )

    def test_index_requires_each_on_demand_playbook_route(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.build_valid_tree(root)
            path = root / "templates/project-control-files/docs/INDEX.md"
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "sdad/playbooks/advanced-extensions.md\n",
                    "",
                ),
                encoding="utf-8",
            )

            self.assertEqual(
                self.collect(root),
                [
                    "templates/project-control-files/docs/INDEX.md missing route: "
                    "sdad/playbooks/advanced-extensions.md"
                ],
            )


if __name__ == "__main__":
    unittest.main()
