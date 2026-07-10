from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTERS = {
    "codex": ("adapters/codex/AGENTS.md", "AGENTS.md"),
    "claude-code": ("adapters/claude-code/CLAUDE.md", "CLAUDE.md"),
    "cursor": (
        "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
        ".cursor/rules/spec-driven-ai-development.mdc",
    ),
    "github-copilot": (
        "adapters/github-copilot/.github/copilot-instructions.md",
        ".github/copilot-instructions.md",
    ),
    "generic": (
        "adapters/generic/AI-SESSION-INSTRUCTIONS.md",
        "AI-SESSION-INSTRUCTIONS.md",
    ),
}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def find_bash() -> str | None:
    candidates: list[str | None] = []
    if os.name == "nt":
        candidates.extend(
            [
                r"C:\Program Files\Git\bin\bash.exe",
                r"C:\Program Files\Git\usr\bin\bash.exe",
            ]
        )
    candidates.append(shutil.which("bash"))

    for candidate in candidates:
        if not candidate:
            continue
        path = Path(candidate)
        if os.name == "nt" and "system32" in str(path).lower():
            continue
        if path.exists():
            return str(path)
    return None


def find_powershell() -> str | None:
    return shutil.which("pwsh") or shutil.which("powershell")


def powershell_command(script: Path, adapter: str, target_root: Path, *extra: str) -> list[str]:
    powershell = find_powershell()
    if not powershell:
        raise unittest.SkipTest("PowerShell is not available")

    command = [powershell, "-NoLogo", "-NoProfile", "-NonInteractive"]
    if os.name == "nt" or Path(powershell).name.lower() == "powershell.exe":
        command.extend(["-ExecutionPolicy", "Bypass"])
    command.extend(
        [
            "-File",
            str(script),
            "-Adapter",
            adapter,
            "-TargetPath",
            str(target_root),
            *extra,
        ]
    )
    return command


def create_directory_link(link: Path, target: Path) -> None:
    if os.name != "nt":
        link.symlink_to(target, target_is_directory=True)
        return

    powershell = find_powershell()
    if not powershell:
        raise unittest.SkipTest("PowerShell is required to create a Windows junction")

    def quote(value: Path) -> str:
        return "'" + str(value).replace("'", "''") + "'"

    command = (
        f"New-Item -ItemType Junction -Path {quote(link)} "
        f"-Target {quote(target)} | Out-Null"
    )
    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
        check=True,
        text=True,
        capture_output=True,
    )


class InstallAgentAdapterSmokeTests(unittest.TestCase):
    def assert_file_matches_source(self, target: Path, source_rel: str) -> None:
        source = ROOT / source_rel
        self.assertTrue(target.is_file(), f"missing target file: {target}")
        self.assertEqual(read(source), read(target))

    def test_bash_installer_places_nested_adapter_and_requires_force(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            target = target_root / ".cursor" / "rules" / "spec-driven-ai-development.mdc"
            command = [bash, str(script), "cursor", str(target_root)]

            subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
            self.assert_file_matches_source(
                target,
                "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            )

            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Target exists", second.stderr)

            target.write_text("local change\n", encoding="utf-8")
            subprocess.run(
                [*command, "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assert_file_matches_source(
                target,
                "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc",
            )

    def test_bash_installer_places_every_supported_adapter(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target_root.mkdir()
                    subprocess.run(
                        [bash, str(script), adapter, str(target_root)],
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target_root / target_rel, source_rel)

    def test_bash_installer_accepts_force_when_target_path_is_omitted(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            target = target_root / "AGENTS.md"

            result = subprocess.run(
                [bash, str(script), "codex", "--force"],
                cwd=target_root,
                text=True,
                capture_output=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assert_file_matches_source(target, "adapters/codex/AGENTS.md")

    def test_powershell_installer_places_adapter_and_requires_force(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            target = target_root / "CLAUDE.md"
            command = powershell_command(script, "claude-code", target_root)

            subprocess.run(command, cwd=ROOT, check=True, text=True, capture_output=True)
            self.assert_file_matches_source(target, "adapters/claude-code/CLAUDE.md")

            second = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Target exists", second.stderr + second.stdout)

            target.write_text("local change\n", encoding="utf-8")
            subprocess.run(
                powershell_command(script, "claude-code", target_root, "-Force"),
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assert_file_matches_source(target, "adapters/claude-code/CLAUDE.md")

    def test_powershell_installer_places_every_supported_adapter(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target_root.mkdir()
                    subprocess.run(
                        powershell_command(script, adapter, target_root),
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target_root / target_rel, source_rel)

    def test_bash_installer_rejects_linked_parent_that_escapes_target_root(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            target_root = sandbox / "project"
            outside = sandbox / "outside"
            target_root.mkdir()
            outside.mkdir()
            create_directory_link(target_root / ".cursor", outside)

            result = subprocess.run(
                [bash, str(script), "cursor", str(target_root), "--force"],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to install through linked path", result.stderr)
            self.assertFalse((outside / "rules" / "spec-driven-ai-development.mdc").exists())

    def test_powershell_installer_rejects_linked_parent_that_escapes_target_root(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            target_root = sandbox / "project"
            outside = sandbox / "outside"
            target_root.mkdir()
            outside.mkdir()
            create_directory_link(target_root / ".cursor", outside)

            result = subprocess.run(
                powershell_command(script, "cursor", target_root, "-Force"),
                cwd=ROOT,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Refusing to install through linked path",
                result.stderr + result.stdout,
            )
            self.assertFalse((outside / "rules" / "spec-driven-ai-development.mdc").exists())

    def test_bash_force_replaces_hard_link_without_mutating_other_name(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            target_root = sandbox / "project"
            target_root.mkdir()
            outside = sandbox / "outside.txt"
            outside.write_text("preserve me\n", encoding="utf-8")
            target = target_root / "AGENTS.md"
            os.link(outside, target)

            subprocess.run(
                [bash, str(script), "codex", str(target_root), "--force"],
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertEqual(outside.read_text(encoding="utf-8"), "preserve me\n")
            self.assert_file_matches_source(target, "adapters/codex/AGENTS.md")

    def test_powershell_force_replaces_hard_link_without_mutating_other_name(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            target_root = sandbox / "project"
            target_root.mkdir()
            outside = sandbox / "outside.txt"
            outside.write_text("preserve me\n", encoding="utf-8")
            target = target_root / "CLAUDE.md"
            os.link(outside, target)

            subprocess.run(
                powershell_command(script, "claude-code", target_root, "-Force"),
                cwd=ROOT,
                check=True,
                text=True,
                capture_output=True,
            )

            self.assertEqual(outside.read_text(encoding="utf-8"), "preserve me\n")
            self.assert_file_matches_source(target, "adapters/claude-code/CLAUDE.md")

    def test_powershell_force_replaces_read_only_target(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            target = target_root / "AGENTS.md"
            target.write_text("local change\n", encoding="utf-8")
            target.chmod(0o444)
            try:
                subprocess.run(
                    powershell_command(script, "codex", target_root, "-Force"),
                    cwd=ROOT,
                    check=True,
                    text=True,
                    capture_output=True,
                )
                self.assert_file_matches_source(target, "adapters/codex/AGENTS.md")
            finally:
                if target.exists():
                    target.chmod(0o666)


if __name__ == "__main__":
    unittest.main()
