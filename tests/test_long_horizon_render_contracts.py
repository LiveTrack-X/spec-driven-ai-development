from __future__ import annotations

import errno
import importlib.util
import os
import stat
import sys
import tempfile
import unittest
from contextlib import nullcontext
from pathlib import Path
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "render_agent_surfaces.py"
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from sdad_validator.agent_experience import (  # noqa: E402
    STARTUP_SURFACES,
    SURFACE_BUDGETS,
)
from validate_repo import (  # noqa: E402
    CROSS_MODEL_AGENT_SURFACES,
    REQUIRED_FILES,
)


class LongHorizonRenderContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        spec = importlib.util.spec_from_file_location(
            "long_horizon_render_agent_surfaces_under_test",
            SCRIPT,
        )
        if spec is None or spec.loader is None:
            raise RuntimeError("could not import render_agent_surfaces.py")
        cls.module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.module)

    def seed_canonical(self, root: Path) -> None:
        canonical = root / self.module.CANONICAL_PATH
        canonical.parent.mkdir(parents=True)
        canonical.write_bytes(
            (
                "# SDAD Protocol Agent Kernel\r\n"
                "\r\n"
                "Status: Active\r\n"
                "Scope: Required, always-loaded instructions for AI agents and maintainers\r\n"
                "\r\n"
                "## Fast Start\r\n"
                "Read sdad-state.yaml first.\r\n"
            ).encode("utf-8")
        )

    def seed_tree(self, root: Path) -> dict[str, bytes]:
        self.seed_canonical(root)

        originals: dict[str, bytes] = {}
        for index, relative_path in enumerate(self.module.SURFACES, start=1):
            target = root / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            originals[relative_path] = (
                f"original-{index}:{relative_path}\r\n".encode("utf-8")
            )
            target.write_bytes(originals[relative_path])
        return originals

    def transaction_artifacts(self, root: Path) -> list[Path]:
        return sorted(
            path
            for path in root.rglob("*")
            if ".sdad-stage-" in path.name or ".sdad-backup-" in path.name
        )

    def test_each_existing_target_backup_move_failure_restores_every_original(
        self,
    ) -> None:
        surface_count = len(self.module.SURFACES)
        for fail_at in range(1, surface_count + 1):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                originals = self.seed_tree(root)
                targets = {
                    root / relative_path for relative_path in self.module.SURFACES
                }
                real_replace = os.replace
                forward_attempts = 0
                failure_injected = False

                def fail_selected_commit(
                    source: object,
                    destination: object,
                ) -> None:
                    nonlocal forward_attempts, failure_injected
                    source_path = Path(source)
                    destination_path = Path(destination)
                    is_forward_move = (
                        source_path in targets
                        and ".sdad-backup-" in destination_path.name
                    )
                    if is_forward_move:
                        forward_attempts += 1
                        if forward_attempts == fail_at and not failure_injected:
                            failure_injected = True
                            raise OSError(f"injected commit failure {fail_at}")
                    real_replace(source, destination)

                with mock.patch.object(
                    self.module.os,
                    "replace",
                    side_effect=fail_selected_commit,
                ):
                    with self.assertRaisesRegex(
                        OSError,
                        f"injected commit failure {fail_at}",
                    ):
                        self.module.write_surfaces(root)

                self.assertTrue(failure_injected)
                for relative_path, original in originals.items():
                    self.assertEqual((root / relative_path).read_bytes(), original)
                self.assertEqual(self.transaction_artifacts(root), [])

    def test_each_existing_target_publish_conflict_restores_every_original(
        self,
    ) -> None:
        surface_count = len(self.module.SURFACES)
        for fail_at in range(1, surface_count + 1):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                originals = self.seed_tree(root)
                real_link = os.link
                attempts = 0

                def fail_selected_link(source: object, destination: object) -> None:
                    nonlocal attempts
                    attempts += 1
                    if attempts == fail_at:
                        raise FileExistsError(
                            f"injected existing-target conflict {fail_at}"
                        )
                    real_link(source, destination)

                with mock.patch.object(
                    self.module.os,
                    "link",
                    side_effect=fail_selected_link,
                ):
                    with self.assertRaisesRegex(
                        FileExistsError,
                        f"injected existing-target conflict {fail_at}",
                    ):
                        self.module.write_surfaces(root)

                for relative_path, original in originals.items():
                    self.assertEqual((root / relative_path).read_bytes(), original)
                self.assertEqual(self.transaction_artifacts(root), [])

    def test_each_missing_target_publication_failure_rolls_back_cleanly(self) -> None:
        surface_count = len(self.module.SURFACES)
        for fail_at in range(1, surface_count + 1):
            with self.subTest(fail_at=fail_at), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.seed_canonical(root)
                real_link = os.link
                attempts = 0

                def fail_selected_link(source: object, destination: object) -> None:
                    nonlocal attempts
                    attempts += 1
                    if attempts == fail_at:
                        raise FileExistsError(
                            f"injected no-clobber conflict {fail_at}"
                        )
                    real_link(source, destination)

                with mock.patch.object(
                    self.module.os,
                    "link",
                    side_effect=fail_selected_link,
                ):
                    with self.assertRaisesRegex(
                        FileExistsError,
                        f"injected no-clobber conflict {fail_at}",
                    ):
                        self.module.write_surfaces(root)

                for relative_path in self.module.SURFACES:
                    self.assertFalse((root / relative_path).exists())
                self.assertEqual(self.transaction_artifacts(root), [])
                self.assertFalse((root / "adapters").exists())

    def test_concurrently_created_missing_target_is_preserved(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)
            targets = [root / relative_path for relative_path in self.module.SURFACES]
            real_link = os.link
            attempts = 0
            concurrent_payload = b"concurrent writer owns this file\n"

            def create_before_second_link(source: object, destination: object) -> None:
                nonlocal attempts
                attempts += 1
                target = Path(destination)
                if attempts == 2:
                    target.write_bytes(concurrent_payload)
                real_link(source, destination)

            with mock.patch.object(
                self.module.os,
                "link",
                side_effect=create_before_second_link,
            ):
                with self.assertRaises(FileExistsError):
                    self.module.write_surfaces(root)

            self.assertFalse(targets[0].exists())
            self.assertEqual(targets[1].read_bytes(), concurrent_payload)
            for target in targets[2:]:
                self.assertFalse(target.exists())
            self.assertEqual(self.transaction_artifacts(root), [])

    def test_missing_target_replaced_before_link_returns_is_not_claimed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)
            targets = [root / relative_path for relative_path in self.module.SURFACES]
            first_target = targets[0]
            real_link = os.link
            real_replace = os.replace
            replacement_identity: tuple[int, int] | None = None

            def link_then_replace(source: object, destination: object) -> None:
                nonlocal replacement_identity
                real_link(source, destination)
                if Path(destination) == first_target:
                    replacement = first_target.with_name("concurrent-inside-link.tmp")
                    replacement.write_bytes(first_target.read_bytes())
                    real_replace(replacement, first_target)
                    current = first_target.stat()
                    replacement_identity = (current.st_dev, current.st_ino)

            with mock.patch.object(
                self.module.os,
                "link",
                side_effect=link_then_replace,
            ):
                with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                    self.module.write_surfaces(root)

            self.assertIsNotNone(replacement_identity)
            current = first_target.stat()
            self.assertEqual((current.st_dev, current.st_ino), replacement_identity)
            for target in targets[1:]:
                self.assertFalse(target.exists())

    def test_existing_target_created_after_backup_is_preserved_with_backup(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            originals = self.seed_tree(root)
            first_relative = next(iter(self.module.SURFACES))
            first_target = root / first_relative
            concurrent_payload = b"concurrent writer after backup\n"
            real_link = os.link

            def create_before_link(source: object, destination: object) -> None:
                target = Path(destination)
                if target == first_target:
                    target.write_bytes(concurrent_payload)
                real_link(source, destination)

            with mock.patch.object(
                self.module.os,
                "link",
                side_effect=create_before_link,
            ):
                with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                    self.module.write_surfaces(root)

            self.assertEqual(first_target.read_bytes(), concurrent_payload)
            backups = [
                path
                for path in self.transaction_artifacts(root)
                if ".sdad-backup-" in path.name
            ]
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), originals[first_relative])

    def test_dangling_symlink_created_after_backup_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            probe = root / "symlink-capability-probe"
            try:
                probe.symlink_to("missing-probe-target")
            except OSError:
                symlink_available = False
            else:
                symlink_available = True
                probe.unlink()

            originals = self.seed_tree(root)
            first_relative = next(iter(self.module.SURFACES))
            first_target = root / first_relative
            link_value = "concurrent-missing-target"
            real_link = os.link

            def create_symlink_before_link(
                source: object,
                destination: object,
            ) -> None:
                target = Path(destination)
                if target == first_target:
                    if symlink_available:
                        target.symlink_to(link_value)
                    else:
                        raise FileExistsError("simulated dangling symlink conflict")
                real_link(source, destination)

            real_is_symlink = Path.is_symlink

            def selective_is_symlink(path: Path) -> bool:
                if path == first_target:
                    return True
                return real_is_symlink(path)

            symlink_contract = (
                nullcontext()
                if symlink_available
                else mock.patch.object(Path, "is_symlink", new=selective_is_symlink)
            )
            with symlink_contract, mock.patch.object(
                self.module.os,
                "link",
                side_effect=create_symlink_before_link,
            ):
                with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                    self.module.write_surfaces(root)

            if symlink_available:
                self.assertTrue(first_target.is_symlink())
                self.assertEqual(os.readlink(first_target), link_value)
            else:
                self.assertFalse(first_target.exists())
            backups = [
                path
                for path in self.transaction_artifacts(root)
                if ".sdad-backup-" in path.name
            ]
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_bytes(), originals[first_relative])

    def test_same_byte_aba_replacement_is_not_deleted_during_rollback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)
            targets = [root / relative_path for relative_path in self.module.SURFACES]
            real_link = os.link
            real_replace = os.replace
            attempts = 0
            replacement_identity: tuple[int, int] | None = None

            def replace_first_before_second_link(
                source: object,
                destination: object,
            ) -> None:
                nonlocal attempts, replacement_identity
                attempts += 1
                if attempts == 2:
                    replacement = targets[0].with_name("concurrent-replacement.tmp")
                    replacement.write_bytes(targets[0].read_bytes())
                    real_replace(replacement, targets[0])
                    current = targets[0].stat()
                    replacement_identity = (current.st_dev, current.st_ino)
                    raise FileExistsError("injected later publication conflict")
                real_link(source, destination)

            with mock.patch.object(
                self.module.os,
                "link",
                side_effect=replace_first_before_second_link,
            ):
                with self.assertRaisesRegex(RuntimeError, "rollback was incomplete"):
                    self.module.write_surfaces(root)

            self.assertIsNotNone(replacement_identity)
            current = targets[0].stat()
            self.assertEqual((current.st_dev, current.st_ino), replacement_identity)
            self.assertEqual(
                targets[0].read_bytes(),
                self.module.render_surfaces(root)[next(iter(self.module.SURFACES))].encode(
                    "utf-8"
                ),
            )
            for target in targets[1:]:
                self.assertFalse(target.exists())

    def test_hard_link_unsupported_falls_back_without_mode_or_content_drift(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)
            canonical = root / self.module.CANONICAL_PATH
            expected_mode = stat.S_IMODE(canonical.stat().st_mode)

            with mock.patch.object(
                self.module.os,
                "link",
                side_effect=OSError(errno.EOPNOTSUPP, "hard links unsupported"),
            ):
                self.module.write_surfaces(root)

            expected = self.module.render_surfaces(root)
            for relative_path, content in expected.items():
                target = root / relative_path
                self.assertEqual(target.read_bytes(), content.encode("utf-8"))
                self.assertEqual(stat.S_IMODE(target.stat().st_mode), expected_mode)
            self.assertEqual(self.transaction_artifacts(root), [])

    def test_unexpected_hard_link_io_error_is_not_masked_by_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)

            with (
                mock.patch.object(
                    self.module.os,
                    "link",
                    side_effect=OSError(errno.EIO, "injected storage failure"),
                ),
                mock.patch.object(
                    self.module,
                    "_copy_exclusively",
                    wraps=self.module._copy_exclusively,
                ) as fallback,
            ):
                with self.assertRaisesRegex(OSError, "injected storage failure"):
                    self.module.write_surfaces(root)

            fallback.assert_not_called()
            for relative_path in self.module.SURFACES:
                self.assertFalse((root / relative_path).exists())
            self.assertEqual(self.transaction_artifacts(root), [])
            self.assertFalse((root / "adapters").exists())

    def test_exclusive_copy_failure_removes_partial_file_and_new_directories(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_canonical(root)
            real_write = os.write
            writes = 0

            def partial_then_fail(descriptor: int, payload: object) -> int:
                nonlocal writes
                writes += 1
                if writes == 1:
                    data = bytes(payload)
                    return real_write(descriptor, data[: max(1, len(data) // 2)])
                raise OSError("injected exclusive copy failure")

            with (
                mock.patch.object(
                    self.module.os,
                    "link",
                    side_effect=OSError(errno.EOPNOTSUPP, "hard links unsupported"),
                ),
                mock.patch.object(
                    self.module.os,
                    "write",
                    side_effect=partial_then_fail,
                ),
            ):
                with self.assertRaisesRegex(
                    OSError,
                    "injected exclusive copy failure",
                ):
                    self.module.write_surfaces(root)

            for relative_path in self.module.SURFACES:
                self.assertFalse((root / relative_path).exists())
            self.assertEqual(self.transaction_artifacts(root), [])
            self.assertFalse((root / "adapters").exists())

    def test_surface_registries_cannot_silently_drop_a_renderer_target(self) -> None:
        rendered = set(self.module.SURFACES)
        canonical = {self.module.CANONICAL_PATH}

        self.assertEqual(set(STARTUP_SURFACES), canonical | rendered)
        self.assertEqual(set(CROSS_MODEL_AGENT_SURFACES), canonical | rendered)
        self.assertTrue(rendered <= set(SURFACE_BUDGETS))
        self.assertTrue(rendered <= set(REQUIRED_FILES))

    def test_success_is_lf_utf8_and_repeated_write_is_a_noop(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.seed_tree(root)

            self.module.write_surfaces(root)

            expected = self.module.render_surfaces(root)
            first_snapshot: dict[str, tuple[bytes, int]] = {}
            for relative_path, content in expected.items():
                target = root / relative_path
                payload = target.read_bytes()
                self.assertEqual(payload, content.encode("utf-8"))
                self.assertNotIn(b"\r", payload)
                first_snapshot[relative_path] = (payload, target.stat().st_mtime_ns)
            self.assertEqual(self.module.collect_surface_drift(root), [])
            self.assertEqual(self.transaction_artifacts(root), [])

            real_replace = os.replace
            with mock.patch.object(
                self.module.os,
                "replace",
                wraps=real_replace,
            ) as replace:
                self.module.write_surfaces(root)

            replace.assert_not_called()
            for relative_path, snapshot in first_snapshot.items():
                target = root / relative_path
                self.assertEqual(
                    (target.read_bytes(), target.stat().st_mtime_ns),
                    snapshot,
                )
            self.assertEqual(self.module.collect_surface_drift(root), [])
            self.assertEqual(self.transaction_artifacts(root), [])


if __name__ == "__main__":
    unittest.main()
