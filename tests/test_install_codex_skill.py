from __future__ import annotations

import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


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


def powershell_command(script: Path, *extra: str) -> list[str]:
    powershell = find_powershell()
    if not powershell:
        raise unittest.SkipTest("PowerShell is not available")

    command = [powershell, "-NoLogo", "-NoProfile", "-NonInteractive"]
    if os.name == "nt" or Path(powershell).name.lower() == "powershell.exe":
        command.extend(["-ExecutionPolicy", "Bypass"])
    command.extend(["-File", str(script), *extra])
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


class InstallCodexSkillSmokeTests(unittest.TestCase):
    def assert_no_transaction_artifacts(self, skills_root: Path) -> None:
        leftovers = sorted(
            path.name for path in skills_root.glob(".ai-spec-project-start.*")
        )
        self.assertEqual([], leftovers)

    def assert_installed_skill_matches_source(self, target: Path) -> None:
        source = ROOT / "skills" / "ai-spec-project-start"
        source_files = sorted(
            path.relative_to(source) for path in source.rglob("*") if path.is_file()
        )
        installed_files = sorted(
            path.relative_to(target) for path in target.rglob("*") if path.is_file()
        )
        self.assertEqual(source_files, installed_files)
        for relative_path in source_files:
            with self.subTest(path=relative_path):
                self.assertEqual(
                    (source / relative_path).read_bytes(),
                    (target / relative_path).read_bytes(),
                )

        updated_contracts = {
            Path("SKILL.md"): "read-only migration preview",
            Path("references/runtime-contract.md"): "Steady-State V2 Invariants",
            Path("references/field-patterns.md"): "Mature-Project Migration Evidence",
        }
        for relative_path, phrase in updated_contracts.items():
            with self.subTest(updated_contract=relative_path):
                self.assertEqual(
                    (source / relative_path).read_bytes(),
                    (target / relative_path).read_bytes(),
                )
                self.assertIn(
                    phrase,
                    (target / relative_path).read_text(encoding="utf-8"),
                )

        fallback = (
            target / "references" / "starter-templates.md"
        ).read_text(encoding="utf-8")
        for phrase in (
            "version: 2",
            "execution_scope: packet",
            "validation_for: bootstrap",
            "# current_handoff: docs/sdad/handoffs/YYYY-MM-DD-topic.md",
            "## Optional Current Handoff",
            "## 1. Session Identity\n\n"
            "- Active packet: [packet:bootstrap]",
        ):
            with self.subTest(fallback_phrase=phrase):
                self.assertIn(phrase, fallback)

    def test_bash_installer_requires_force_before_replacing_existing_skill(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-codex-skill.sh"
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex-home"
            target = codex_home / "skills" / "ai-spec-project-start"
            env = {**os.environ, "CODEX_HOME": str(codex_home)}
            command = [bash, str(script)]

            subprocess.run(command, cwd=ROOT, env=env, check=True, capture_output=True)
            self.assert_installed_skill_matches_source(target)
            marker = target / "local-change.txt"
            marker.write_text("preserve me\n", encoding="utf-8")

            second = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Target exists", second.stderr)
            self.assertTrue(marker.is_file())

            subprocess.run(
                [*command, "--force"],
                cwd=ROOT,
                env=env,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assert_installed_skill_matches_source(target)
            self.assertFalse(marker.exists())
            self.assert_no_transaction_artifacts(codex_home / "skills")

    def test_powershell_installer_requires_force_before_replacing_existing_skill(self) -> None:
        script = ROOT / "scripts" / "install-codex-skill.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            codex_home = Path(tmp) / "codex-home"
            target = codex_home / "skills" / "ai-spec-project-start"
            env = {**os.environ, "CODEX_HOME": str(codex_home)}
            command = powershell_command(script)

            subprocess.run(command, cwd=ROOT, env=env, check=True, capture_output=True)
            self.assert_installed_skill_matches_source(target)
            marker = target / "local-change.txt"
            marker.write_text("preserve me\n", encoding="utf-8")

            second = subprocess.run(command, cwd=ROOT, env=env, text=True, capture_output=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertIn("Target exists", second.stderr + second.stdout)
            self.assertTrue(marker.is_file())

            subprocess.run(
                powershell_command(script, "-Force"),
                cwd=ROOT,
                env=env,
                check=True,
                text=True,
                capture_output=True,
            )
            self.assert_installed_skill_matches_source(target)
            self.assertFalse(marker.exists())
            self.assert_no_transaction_artifacts(codex_home / "skills")

    def test_bash_installer_refuses_linked_skill_target(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-codex-skill.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            codex_home = sandbox / "codex-home"
            skills_root = codex_home / "skills"
            outside = sandbox / "outside"
            skills_root.mkdir(parents=True)
            outside.mkdir()
            marker = outside / "keep.txt"
            marker.write_text("preserve me\n", encoding="utf-8")
            create_directory_link(skills_root / "ai-spec-project-start", outside)
            env = {**os.environ, "CODEX_HOME": str(codex_home)}

            result = subprocess.run(
                [bash, str(script), "--force"],
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Refusing to replace linked skill target", result.stderr)
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve me\n")

    def test_powershell_installer_refuses_linked_skill_target(self) -> None:
        script = ROOT / "scripts" / "install-codex-skill.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            codex_home = sandbox / "codex-home"
            skills_root = codex_home / "skills"
            outside = sandbox / "outside"
            skills_root.mkdir(parents=True)
            outside.mkdir()
            marker = outside / "keep.txt"
            marker.write_text("preserve me\n", encoding="utf-8")
            create_directory_link(skills_root / "ai-spec-project-start", outside)
            env = {**os.environ, "CODEX_HOME": str(codex_home)}

            result = subprocess.run(
                powershell_command(script, "-Force"),
                cwd=ROOT,
                env=env,
                text=True,
                capture_output=True,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn(
                "Refusing to replace linked skill target",
                result.stderr + result.stdout,
            )
            self.assertEqual(marker.read_text(encoding="utf-8"), "preserve me\n")


if __name__ == "__main__":
    unittest.main()
