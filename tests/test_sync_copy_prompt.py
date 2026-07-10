from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "sync_copy_prompt_under_test",
    ROOT / "scripts" / "sync_copy_prompt.py",
)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError("Could not load scripts/sync_copy_prompt.py")
SYNC_COPY_PROMPT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(SYNC_COPY_PROMPT)


class CopyPromptSyncTests(unittest.TestCase):
    def test_builds_readme_with_exact_option_one_prompt(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs").mkdir()
            (root / "docs/no-clone-quick-install.md").write_text(
                "## Option 1: Give This To Your AI Agent\n\n"
                "```text\ncanonical\nprompt\n```\n\n"
                "## Option 2: Installer\n",
                encoding="utf-8",
            )
            (root / "README.md").write_text(
                "## Copy-Paste Start Prompt\n\n"
                "```text\nstale\n```\n\n"
                "## What SDAD Gives You\n",
                encoding="utf-8",
            )

            current, expected = SYNC_COPY_PROMPT.synchronized_readme(root)

            self.assertNotEqual(current, expected)
            self.assertEqual(
                SYNC_COPY_PROMPT.prompt_content(
                    expected,
                    "## Copy-Paste Start Prompt",
                ),
                "canonical\nprompt\n",
            )

    def test_rejects_a_heading_without_a_text_fence(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing text fence"):
            SYNC_COPY_PROMPT.prompt_content(
                "## Copy-Paste Start Prompt\n\nNo prompt here.\n",
                "## Copy-Paste Start Prompt",
            )


if __name__ == "__main__":
    unittest.main()
