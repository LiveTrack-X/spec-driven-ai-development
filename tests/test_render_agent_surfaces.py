from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_agent_surfaces.py"


class RenderAgentSurfacesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        if not SCRIPT.is_file():
            raise AssertionError("scripts/render_agent_surfaces.py is missing")
        spec = importlib.util.spec_from_file_location(
            "render_agent_surfaces_under_test",
            SCRIPT,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("could not import render_agent_surfaces.py")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def test_committed_adapters_match_the_canonical_runtime_kernel(self) -> None:
        self.assertEqual(self.module.collect_surface_drift(ROOT), [])

    def test_reports_a_drifted_surface_without_rewriting_it(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            template = root / "templates/project-control-files/AGENTS.md"
            template.parent.mkdir(parents=True)
            template.write_text(
                "# Project Agent Control Plane\n\n"
                "Status: Active\n"
                "Scope: Required, always-loaded instructions for AI agents and maintainers\n"
                "\n## Fast Start\ncore\n",
                encoding="utf-8",
            )
            for relative_path in self.module.SURFACES:
                path = root / relative_path
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("drift\n", encoding="utf-8")

            violations = self.module.collect_surface_drift(root)

            self.assertEqual(len(violations), len(self.module.SURFACES))
            self.assertEqual(
                (root / "adapters/codex/AGENTS.md").read_text(encoding="utf-8"),
                "drift\n",
            )


if __name__ == "__main__":
    unittest.main()
