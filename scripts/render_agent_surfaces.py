from __future__ import annotations

import argparse
import errno
import os
import shutil
import stat
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = "templates/project-control-files/AGENTS.md"
CANONICAL_TITLE = "# SDAD Protocol Agent Kernel"
CANONICAL_SCOPE = (
    "Scope: Required, always-loaded instructions for AI agents and maintainers"
)

CURSOR_PREFIX = """---
description: Route Cursor through the compact, evidence-based SDAD Protocol kernel.
globs:
alwaysApply: true
---

"""

SURFACES = {
    "adapters/codex/AGENTS.md": (
        "# SDAD Protocol",
        "Scope: Codex project instructions",
        "",
    ),
    "adapters/claude-code/CLAUDE.md": (
        "# SDAD Protocol",
        "Scope: Claude Code project memory",
        "",
    ),
    "adapters/gemini-cli/GEMINI.md": (
        "# SDAD Protocol",
        "Scope: Gemini CLI project context",
        "",
    ),
    "adapters/cursor/.cursor/rules/spec-driven-ai-development.mdc": (
        "# SDAD Protocol",
        "Scope: Cursor project rule",
        CURSOR_PREFIX,
    ),
    "adapters/github-copilot/.github/copilot-instructions.md": (
        "# SDAD Protocol",
        "Scope: GitHub Copilot project instructions",
        "",
    ),
    "adapters/generic/AI-SESSION-INSTRUCTIONS.md": (
        "# SDAD Protocol",
        "Scope: Generic AI coding-agent instructions",
        "",
    ),
}


class _StagedSurface:
    def __init__(
        self,
        *,
        target: Path,
        staged: Path,
        backup: Path | None,
        had_original: bool,
        payload: bytes,
    ) -> None:
        self.target = target
        self.staged = staged
        self.backup = backup
        self.had_original = had_original
        self.payload = payload
        self.original_moved = False
        self.published = False
        self.publication_complete = False
        self.published_identity: tuple[int, int] | None = None


def _read_canonical(root: Path) -> str:
    path = root / CANONICAL_PATH
    content = path.read_text(encoding="utf-8")
    if content.count(CANONICAL_TITLE) != 1:
        raise ValueError(f"canonical title must appear once in {CANONICAL_PATH}")
    if content.count(CANONICAL_SCOPE) != 1:
        raise ValueError(f"canonical scope must appear once in {CANONICAL_PATH}")
    return content.replace("\r\n", "\n")


def _temporary_file(parent: Path, target_name: str, purpose: str) -> Path:
    descriptor, raw_path = tempfile.mkstemp(
        dir=parent,
        prefix=f".{target_name}.sdad-{purpose}-",
        suffix=".tmp",
    )
    os.close(descriptor)
    return Path(raw_path)


def _write_staged_file(path: Path, content: str) -> None:
    payload = content.encode("utf-8")
    with path.open("wb") as stream:
        written = stream.write(payload)
        if written != len(payload):
            raise OSError(
                f"short write while staging {path.name}: {written}/{len(payload)} bytes"
            )
        stream.flush()
        os.fsync(stream.fileno())


def _file_identity_from_stat(result: os.stat_result) -> tuple[int, int]:
    return result.st_dev, result.st_ino


def _published_target_is_owned(surface: _StagedSurface) -> bool:
    if surface.published_identity is None:
        return False
    try:
        target_stat = surface.target.stat(follow_symlinks=False)
    except OSError:
        return False
    if not stat.S_ISREG(target_stat.st_mode):
        return False
    identity = _file_identity_from_stat(target_stat)
    if identity != surface.published_identity:
        return False
    return not surface.publication_complete or surface.target.read_bytes() == surface.payload


def _write_all(descriptor: int, payload: bytes) -> None:
    view = memoryview(payload)
    while view:
        written = os.write(descriptor, view)
        if written <= 0:
            raise OSError("short write while publishing an agent surface")
        view = view[written:]


def _copy_exclusively(surface: _StagedSurface) -> None:
    mode = stat.S_IMODE(surface.staged.stat().st_mode)
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    flags |= getattr(os, "O_BINARY", 0)
    descriptor = os.open(surface.target, flags, mode)
    try:
        surface.published = True
        surface.published_identity = _file_identity_from_stat(os.fstat(descriptor))
        _write_all(descriptor, surface.payload)
        if hasattr(os, "fchmod"):
            os.fchmod(descriptor, mode)
        os.fsync(descriptor)
        surface.publication_complete = True
    finally:
        os.close(descriptor)

    if not _published_target_is_owned(surface):
        raise OSError(f"concurrent change while publishing: {surface.target}")
    surface.staged.unlink()


_HARD_LINK_FALLBACK_ERRNOS = frozenset(
    {
        errno.EACCES,
        errno.EPERM,
        errno.EXDEV,
        errno.ENOSYS,
        getattr(errno, "ENOTSUP", errno.EPERM),
        getattr(errno, "EOPNOTSUPP", errno.EPERM),
    }
)
_HARD_LINK_FALLBACK_WINERRORS = frozenset({1, 50})


def _hard_link_fallback_allowed(error: OSError) -> bool:
    return (
        error.errno in _HARD_LINK_FALLBACK_ERRNOS
        or getattr(error, "winerror", None) in _HARD_LINK_FALLBACK_WINERRORS
    )


def _publish_without_clobber(surface: _StagedSurface) -> None:
    staged_identity = _file_identity_from_stat(surface.staged.stat())
    try:
        os.link(surface.staged, surface.target)
    except OSError as exc:
        if (
            isinstance(exc, FileExistsError)
            or surface.target.exists()
            or surface.target.is_symlink()
        ):
            raise
        if not _hard_link_fallback_allowed(exc):
            raise
        _copy_exclusively(surface)
        return

    surface.published = True
    surface.published_identity = staged_identity
    surface.publication_complete = True
    if not _published_target_is_owned(surface):
        raise OSError(f"concurrent change while publishing: {surface.target}")
    surface.staged.unlink()


def _created_parent_directories(parent: Path) -> list[Path]:
    missing: list[Path] = []
    candidate = parent
    while not candidate.exists():
        missing.append(candidate)
        candidate = candidate.parent
    parent.mkdir(parents=True, exist_ok=True)
    return missing


def _cleanup_paths(paths: list[Path]) -> list[OSError]:
    errors: list[OSError] = []
    for path in paths:
        try:
            path.unlink(missing_ok=True)
        except OSError as exc:
            errors.append(exc)
    return errors


def _cleanup_created_directories(paths: list[Path]) -> None:
    for path in sorted(
        set(paths),
        key=lambda candidate: (-len(candidate.parts), candidate.as_posix()),
    ):
        try:
            path.rmdir()
        except OSError:
            # A concurrent writer may have populated a directory that this run
            # created. Never remove non-empty directories during rollback.
            pass


def render_surfaces(root: Path) -> dict[str, str]:
    canonical = _read_canonical(root)
    rendered: dict[str, str] = {}
    for relative_path, (title, scope, prefix) in SURFACES.items():
        rendered[relative_path] = prefix + canonical.replace(
            CANONICAL_TITLE,
            title,
            1,
        ).replace(
            CANONICAL_SCOPE,
            scope,
            1,
        )
    return rendered


def collect_surface_drift(root: Path) -> list[str]:
    violations: list[str] = []
    for relative_path, expected in render_surfaces(root).items():
        path = root / relative_path
        if not path.is_file():
            violations.append(f"missing rendered agent surface: {relative_path}")
            continue
        actual = path.read_text(encoding="utf-8").replace("\r\n", "\n")
        if actual != expected:
            violations.append(f"rendered agent surface drift: {relative_path}")
    return violations


def write_surfaces(root: Path) -> None:
    rendered = render_surfaces(root)
    staged: list[_StagedSurface] = []
    created_directories: list[Path] = []

    try:
        for relative_path, content in rendered.items():
            target = root / relative_path
            created_directories.extend(_created_parent_directories(target.parent))

            had_original = target.exists() or target.is_symlink()
            if had_original and not target.is_file():
                raise OSError(f"rendered agent surface is not a file: {relative_path}")

            payload = content.encode("utf-8")
            if had_original and target.read_bytes() == payload:
                continue

            staged_path = _temporary_file(target.parent, target.name, "stage")
            backup_path: Path | None = None
            try:
                _write_staged_file(staged_path, content)
                if had_original:
                    shutil.copymode(target, staged_path)
                    backup_path = _temporary_file(
                        target.parent,
                        target.name,
                        "backup",
                    )
                else:
                    shutil.copymode(root / CANONICAL_PATH, staged_path)
            except Exception:
                _cleanup_paths(
                    [
                        path
                        for path in (staged_path, backup_path)
                        if path is not None
                    ]
                )
                raise

            staged.append(
                _StagedSurface(
                    target=target,
                    staged=staged_path,
                    backup=backup_path,
                    had_original=had_original,
                    payload=payload,
                )
            )
    except Exception:
        cleanup_errors = _cleanup_paths(
            [
                path
                for surface in staged
                for path in (surface.staged, surface.backup)
                if path is not None
            ]
        )
        _cleanup_created_directories(created_directories)
        if cleanup_errors:
            raise RuntimeError(
                "failed to clean staged agent surfaces after a staging failure"
            ) from cleanup_errors[0]
        raise

    try:
        for surface in staged:
            if surface.had_original:
                assert surface.backup is not None
                os.replace(surface.target, surface.backup)
                surface.original_moved = True
                _publish_without_clobber(surface)
            else:
                # Prefer an atomic hard-link publication.  Filesystems without
                # hard-link support fall back to exclusive creation, which is
                # still no-clobber and preserves the staged file mode.
                _publish_without_clobber(surface)
    except Exception:
        rollback_errors: list[OSError] = []
        for surface in reversed(staged):
            try:
                if surface.original_moved:
                    assert surface.backup is not None
                    if surface.published and not _published_target_is_owned(surface):
                        raise OSError(
                            f"concurrent change prevents rollback: {surface.target}"
                        )
                    if not surface.published and (
                        surface.target.exists() or surface.target.is_symlink()
                    ):
                        raise OSError(
                            f"concurrent target prevents rollback: {surface.target}"
                        )
                    os.replace(surface.backup, surface.target)
                    surface.original_moved = False
                    surface.published = False
                elif surface.published:
                    if not _published_target_is_owned(surface):
                        raise OSError(
                            f"concurrent change prevents cleanup: {surface.target}"
                        )
                    surface.target.unlink(missing_ok=True)
                    surface.published = False
            except OSError as exc:
                rollback_errors.append(exc)

        cleanup_errors = _cleanup_paths(
            [
                path
                for surface in staged
                for path in (surface.staged, surface.backup)
                if path is not None and not surface.original_moved
            ]
        )
        _cleanup_created_directories(created_directories)
        if rollback_errors or cleanup_errors:
            raise RuntimeError(
                "agent surface publication failed and rollback was incomplete"
            ) from (rollback_errors + cleanup_errors)[0]
        raise

    cleanup_errors = _cleanup_paths(
        [surface.backup for surface in staged if surface.backup is not None]
    )
    if cleanup_errors:
        raise RuntimeError(
            "agent surfaces were published but transaction cleanup failed"
        ) from cleanup_errors[0]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render self-contained tool adapters from the canonical agent kernel."
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--write", action="store_true", help="regenerate committed adapters")
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args()

    root = args.root.resolve()
    if args.check:
        violations = collect_surface_drift(root)
        for violation in violations:
            print(f"ERROR: {violation}")
        if violations:
            return 1
        print("Agent surfaces match the canonical runtime kernel.")
        return 0

    write_surfaces(root)
    print(f"Rendered {len(SURFACES)} agent surfaces.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
