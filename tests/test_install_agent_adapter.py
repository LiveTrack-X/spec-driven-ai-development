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
    "gemini-cli": ("adapters/gemini-cli/GEMINI.md", "GEMINI.md"),
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
NESTED_ADAPTERS = {
    name: paths
    for name, paths in ADAPTERS.items()
    if len(Path(paths[1]).parts) > 1
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


def powershell_command(
    script: Path,
    adapter: str,
    target_root: Path,
    *extra: str,
) -> list[str]:
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


def _quote_powershell_path(value: Path) -> str:
    return "'" + str(value).replace("'", "''") + "'"


def create_directory_link(link: Path, target: Path) -> None:
    if os.name != "nt":
        link.symlink_to(target, target_is_directory=True)
        return

    powershell = find_powershell()
    if not powershell:
        raise unittest.SkipTest("PowerShell is required to create a Windows junction")

    command = (
        f"New-Item -ItemType Junction -Path {_quote_powershell_path(link)} "
        f"-Target {_quote_powershell_path(target)} | Out-Null"
    )
    subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
        check=True,
        text=True,
        capture_output=True,
    )


def create_file_link(link: Path, target: Path) -> None:
    try:
        link.symlink_to(target)
        return
    except OSError as error:
        if os.name != "nt":
            raise
        powershell = find_powershell()
        if not powershell:
            raise unittest.SkipTest(
                f"file symlinks are unavailable: {error}"
            ) from error

    command = (
        f"New-Item -ItemType SymbolicLink -Path {_quote_powershell_path(link)} "
        f"-Target {_quote_powershell_path(target)} | Out-Null"
    )
    result = subprocess.run(
        [powershell, "-NoLogo", "-NoProfile", "-NonInteractive", "-Command", command],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise unittest.SkipTest(
            "Windows file symlinks require an enabled developer mode or elevation"
        )


def prepare_isolated_installer(
    repo: Path,
    script_name: str,
    source_rel: str,
) -> Path:
    script = repo / "scripts" / script_name
    script.parent.mkdir(parents=True)
    shutil.copy2(ROOT / "scripts" / script_name, script)
    source = repo / source_rel
    source.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / source_rel, source)
    return script


class InstallAgentAdapterSmokeTests(unittest.TestCase):
    def assert_file_matches_source(self, target: Path, source_rel: str) -> None:
        source = ROOT / source_rel
        self.assertTrue(target.is_file(), f"missing target file: {target}")
        self.assertEqual(read(source), read(target))

    def assert_no_transaction_artifacts(self, target_root: Path) -> None:
        artifacts = sorted(
            str(path.relative_to(target_root))
            for path in target_root.rglob("*")
            if path.name.startswith(".sdad-adapter.stage.")
            or path.name.endswith(".previous")
        )
        self.assertEqual(artifacts, [])

    def require_file_symlinks(self, sandbox: Path) -> None:
        target = sandbox / "symlink-probe-target.txt"
        link = sandbox / "symlink-probe.txt"
        target.write_text("probe\n", encoding="utf-8")
        try:
            create_file_link(link, target)
        except unittest.SkipTest as error:
            self.skipTest(str(error))
        finally:
            if link.is_symlink():
                link.unlink()
            target.unlink(missing_ok=True)

    def test_bash_transactions_refuse_overwrite_force_replace_and_cleanup_every_adapter(
        self,
    ) -> None:
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
                    target = target_root / target_rel
                    command = [bash, str(script), adapter, str(target_root)]

                    subprocess.run(
                        command,
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

                    second = subprocess.run(
                        command,
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )
                    self.assertNotEqual(second.returncode, 0)
                    self.assertIn("Target exists", second.stderr)
                    self.assert_no_transaction_artifacts(target_root)

                    target.write_text("local change\n", encoding="utf-8")
                    subprocess.run(
                        [*command, "--force"],
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

    def test_powershell_transactions_refuse_overwrite_force_replace_and_cleanup_every_adapter(
        self,
    ) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target_root.mkdir()
                    target = target_root / target_rel
                    command = powershell_command(script, adapter, target_root)

                    subprocess.run(
                        command,
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

                    second = subprocess.run(
                        command,
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )
                    self.assertNotEqual(second.returncode, 0)
                    self.assertIn("Target exists", second.stderr + second.stdout)
                    self.assert_no_transaction_artifacts(target_root)

                    target.write_text("local change\n", encoding="utf-8")
                    subprocess.run(
                        powershell_command(script, adapter, target_root, "-Force"),
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

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
            self.assert_no_transaction_artifacts(target_root)

    def test_bash_rejects_linked_target_file_for_every_adapter(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            self.require_file_symlinks(sandbox)
            for adapter, (_source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target = target_root / target_rel
                    target.parent.mkdir(parents=True)
                    outside = sandbox / f"{adapter}-outside.txt"
                    outside.write_text("preserve me\n", encoding="utf-8")
                    create_file_link(target, outside)

                    result = subprocess.run(
                        [bash, str(script), adapter, str(target_root), "--force"],
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Refusing to install through linked path", result.stderr)
                    self.assertEqual(read(outside), "preserve me\n")
                    self.assert_no_transaction_artifacts(target_root)

    def test_powershell_rejects_linked_target_file_for_every_adapter(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            self.require_file_symlinks(sandbox)
            for adapter, (_source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target = target_root / target_rel
                    target.parent.mkdir(parents=True)
                    outside = sandbox / f"{adapter}-outside.txt"
                    outside.write_text("preserve me\n", encoding="utf-8")
                    create_file_link(target, outside)

                    result = subprocess.run(
                        powershell_command(script, adapter, target_root, "-Force"),
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "Refusing to install through linked path",
                        result.stderr + result.stdout,
                    )
                    self.assertEqual(read(outside), "preserve me\n")
                    self.assert_no_transaction_artifacts(target_root)

    def test_bash_rejects_linked_parent_for_every_nested_adapter(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (_source_rel, target_rel) in NESTED_ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    outside = sandbox / f"{adapter}-outside"
                    target_root.mkdir()
                    outside.mkdir()
                    first_parent = Path(target_rel).parts[0]
                    create_directory_link(target_root / first_parent, outside)

                    result = subprocess.run(
                        [bash, str(script), adapter, str(target_root), "--force"],
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("Refusing to install through linked path", result.stderr)
                    self.assertEqual(list(outside.iterdir()), [])
                    self.assert_no_transaction_artifacts(target_root)

    def test_powershell_rejects_linked_parent_for_every_nested_adapter(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (_source_rel, target_rel) in NESTED_ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    outside = sandbox / f"{adapter}-outside"
                    target_root.mkdir()
                    outside.mkdir()
                    first_parent = Path(target_rel).parts[0]
                    create_directory_link(target_root / first_parent, outside)

                    result = subprocess.run(
                        powershell_command(script, adapter, target_root, "-Force"),
                        cwd=ROOT,
                        text=True,
                        capture_output=True,
                    )

                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn(
                        "Refusing to install through linked path",
                        result.stderr + result.stdout,
                    )
                    self.assertEqual(list(outside.iterdir()), [])
                    self.assert_no_transaction_artifacts(target_root)

    def test_bash_force_replaces_hard_link_for_every_adapter(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        script = ROOT / "scripts" / "install-agent-adapter.sh"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target = target_root / target_rel
                    target.parent.mkdir(parents=True)
                    outside = sandbox / f"{adapter}-outside.txt"
                    outside.write_text("preserve me\n", encoding="utf-8")
                    os.link(outside, target)

                    subprocess.run(
                        [bash, str(script), adapter, str(target_root), "--force"],
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )

                    self.assertEqual(read(outside), "preserve me\n")
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

    def test_powershell_force_replaces_hard_link_for_every_adapter(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target = target_root / target_rel
                    target.parent.mkdir(parents=True)
                    outside = sandbox / f"{adapter}-outside.txt"
                    outside.write_text("preserve me\n", encoding="utf-8")
                    os.link(outside, target)

                    subprocess.run(
                        powershell_command(script, adapter, target_root, "-Force"),
                        cwd=ROOT,
                        check=True,
                        text=True,
                        capture_output=True,
                    )

                    self.assertEqual(read(outside), "preserve me\n")
                    self.assert_file_matches_source(target, source_rel)
                    self.assert_no_transaction_artifacts(target_root)

    def test_bash_publication_is_independent_from_source_for_every_adapter(self) -> None:
        bash = find_bash()
        if not bash:
            self.skipTest("bash is not available")

        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    repo = sandbox / adapter
                    script = prepare_isolated_installer(
                        repo,
                        "install-agent-adapter.sh",
                        source_rel,
                    )
                    target_root = repo / "target"
                    target_root.mkdir()
                    subprocess.run(
                        [bash, str(script), adapter, str(target_root)],
                        cwd=repo,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    target = target_root / target_rel
                    installed = read(target)

                    (repo / source_rel).write_text("mutated source\n", encoding="utf-8")

                    self.assertEqual(read(target), installed)
                    self.assertNotEqual(read(target), "mutated source\n")
                    self.assert_no_transaction_artifacts(target_root)

    def test_powershell_publication_is_independent_from_source_for_every_adapter(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    repo = sandbox / adapter
                    script = prepare_isolated_installer(
                        repo,
                        "install-agent-adapter.ps1",
                        source_rel,
                    )
                    target_root = repo / "target"
                    target_root.mkdir()
                    subprocess.run(
                        powershell_command(script, adapter, target_root),
                        cwd=repo,
                        check=True,
                        text=True,
                        capture_output=True,
                    )
                    target = target_root / target_rel
                    installed = read(target)

                    (repo / source_rel).write_text("mutated source\n", encoding="utf-8")

                    self.assertEqual(read(target), installed)
                    self.assertNotEqual(read(target), "mutated source\n")
                    self.assert_no_transaction_artifacts(target_root)

    @unittest.skipUnless(os.name == "nt", "Windows read-only semantics only")
    def test_powershell_force_replaces_read_only_target_for_every_adapter(self) -> None:
        script = ROOT / "scripts" / "install-agent-adapter.ps1"
        with tempfile.TemporaryDirectory() as tmp:
            sandbox = Path(tmp)
            for adapter, (source_rel, target_rel) in ADAPTERS.items():
                with self.subTest(adapter=adapter):
                    target_root = sandbox / adapter
                    target = target_root / target_rel
                    target.parent.mkdir(parents=True)
                    target.write_text("local change\n", encoding="utf-8")
                    target.chmod(0o444)
                    try:
                        subprocess.run(
                            powershell_command(script, adapter, target_root, "-Force"),
                            cwd=ROOT,
                            check=True,
                            text=True,
                            capture_output=True,
                        )
                        self.assert_file_matches_source(target, source_rel)
                        self.assert_no_transaction_artifacts(target_root)
                    finally:
                        if target.exists():
                            target.chmod(0o666)


if __name__ == "__main__":
    unittest.main()
