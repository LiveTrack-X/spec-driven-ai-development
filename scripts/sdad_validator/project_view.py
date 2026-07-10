from __future__ import annotations

import stat
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Protocol

from .diagnostics import DiagnosticError
from .state_contract import is_normalized_relative_posix_path


@dataclass(frozen=True)
class PathInspection:
    status: str
    resolved_path: Path | None


@dataclass(frozen=True)
class ReadResult:
    status: str
    data: bytes | None


class ProjectView(Protocol):
    @property
    def root(self) -> Path: ...

    def inspect(self, relative_path: str) -> PathInspection: ...

    def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult: ...


class FilesystemProjectView:
    def __init__(self, project_root: str | Path) -> None:
        try:
            resolved_root = Path(project_root).resolve(strict=True)
            root_mode = resolved_root.stat().st_mode
        except (OSError, RuntimeError) as exc:
            raise DiagnosticError(
                "unusable_root",
                f"Project root is not accessible: {project_root}",
            ) from exc
        if not stat.S_ISDIR(root_mode):
            raise DiagnosticError(
                "unusable_root",
                f"Project root is not a directory: {project_root}",
            )
        self._root = resolved_root

    @property
    def root(self) -> Path:
        return self._root

    @staticmethod
    def _is_lexically_valid(relative_path: str) -> bool:
        return (
            isinstance(relative_path, str)
            and relative_path != "."
            and "\x00" not in relative_path
            and is_normalized_relative_posix_path(relative_path)
        )

    def inspect(self, relative_path: str) -> PathInspection:
        if not self._is_lexically_valid(relative_path):
            return PathInspection("invalid", None)

        candidate = self._root.joinpath(*PurePosixPath(relative_path).parts)
        try:
            resolved_path = candidate.resolve(strict=False)
        except (OSError, RuntimeError):
            return PathInspection("unreadable", None)

        try:
            resolved_path.relative_to(self._root)
        except ValueError:
            return PathInspection("outside_root", resolved_path)

        try:
            mode = resolved_path.stat().st_mode
        except FileNotFoundError:
            return PathInspection("missing", resolved_path)
        except OSError:
            return PathInspection("unreadable", resolved_path)

        if not stat.S_ISREG(mode):
            return PathInspection("not_file", resolved_path)
        return PathInspection("ok", resolved_path)

    def read_bytes(self, relative_path: str, max_bytes: int) -> ReadResult:
        if max_bytes < 0:
            raise ValueError("max_bytes must be non-negative")

        inspection = self.inspect(relative_path)
        if inspection.status != "ok":
            return ReadResult(inspection.status, None)
        assert inspection.resolved_path is not None

        try:
            with inspection.resolved_path.open("rb") as source:
                data = source.read(max_bytes + 1)
        except OSError:
            return ReadResult("unreadable", None)

        if len(data) > max_bytes:
            return ReadResult("too_large", None)
        return ReadResult("ok", data)
