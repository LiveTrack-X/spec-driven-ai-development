#!/usr/bin/env python3
"""Read-only context inventory and revision-pinned, bounded text pages.

This optional helper does not execute validation commands, archive files, infer
completion, or turn a context-size advisory into a Doctor failure.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Sequence, TextIO

from sdad_validator.project_view import FilesystemProjectView
from sdad_validator.diagnostics import DiagnosticError
from sdad_validator.state_contract import inspect_state

MAX_FILE_BYTES = 1_000_000
MAX_PAGE_BYTES = 50_000
MAX_PAGE_LINES = 500
CONTROL_PATHS = (
    "sdad-state.yaml", "docs/INDEX.md", "docs/TODO-Open-Items.md",
    "review-findings.md", "docs/implementation-notes.md",
)


class ContextError(ValueError):
    pass


def load_text(view: FilesystemProjectView, path: str) -> tuple[str, str, int]:
    result = view.read_bytes(path, MAX_FILE_BYTES)
    if result.status != "ok":
        raise ContextError(f"Cannot read {path}: {result.status}")
    assert result.data is not None
    try:
        text = result.data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise ContextError(f"Cannot read {path}: invalid UTF-8") from exc
    return text, hashlib.sha256(result.data).hexdigest(), len(result.data)


def headings(lines: list[str]) -> list[tuple[int, int, str]]:
    """Return ATX headings outside backtick/tilde fences, with one-based lines."""
    result = []
    fence_char = ""
    fence_length = 0
    for number, line in enumerate(lines, 1):
        fence = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            marker, tail = fence.groups()
            if not fence_char:
                fence_char, fence_length = marker[0], len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length and not tail.strip():
                fence_char = ""
            continue
        if fence_char:
            continue
        match = re.match(r"^ {0,3}(#{1,6})[ \t]+(.+?)\s*$", line)
        if match:
            title = re.sub(r"[ \t]+#+[ \t]*$", "", match.group(2))
            result.append((number, len(match.group(1)), title))
    return result


def read_page(view: FilesystemProjectView, path: str, *, start: int | None = None,
              count: int = 100, heading: str | None = None,
              expected_sha256: str | None = None) -> dict:
    if not 1 <= count <= MAX_PAGE_LINES:
        raise ContextError(f"lines must be between 1 and {MAX_PAGE_LINES}")
    text, digest, byte_count = load_text(view, path)
    if expected_sha256 is not None and expected_sha256 != digest:
        raise ContextError("Source changed; inspect the current revision before continuing")
    lines = text.splitlines()
    first, last = 1, len(lines)
    if heading is not None:
        entries = headings(lines)
        matches = [entry for entry in entries if entry[2] == heading]
        if len(matches) != 1:
            raise ContextError(f"Heading must match exactly once; found {len(matches)}")
        first, level, _ = matches[0]
        last = next((n - 1 for n, depth, _ in entries if n > first and depth <= level), last)
    position = first if start is None else start
    if position < first or position > last + 1:
        raise ContextError("start is outside the selected section")
    selected = []
    page_bytes = 0
    for line in lines[position - 1:min(last, position - 1 + count)]:
        size = len(line.encode("utf-8")) + 1
        if page_bytes + size > MAX_PAGE_BYTES:
            if not selected:
                raise ContextError("One line exceeds the page byte budget; use a more specific source or bounded search")
            break
        selected.append(line)
        page_bytes += size
    following = position + len(selected)
    payload = {
        "schema_version": 1, "path": path, "sha256": digest,
        "file_bytes": byte_count, "file_lines": len(lines),
        "heading": heading, "start": position, "end": following - 1,
        "page_bytes": page_bytes, "lines": selected,
        "truncated": following <= last,
        "next_start": following if following <= last else None,
        "continuation": "Use this sha256 with --expect-sha256 on the next page.",
    }
    # JSON escaping and metadata also consume the caller's context budget.
    while len(json.dumps(payload, ensure_ascii=False).encode("utf-8")) > MAX_PAGE_BYTES:
        if not selected:
            raise ContextError("Page metadata exceeds the output budget")
        removed = selected.pop()
        page_bytes -= len(removed.encode("utf-8")) + 1
        following = position + len(selected)
        payload.update(end=following - 1, page_bytes=page_bytes,
                       truncated=following <= last, next_start=following if following <= last else None)
        if not selected:
            raise ContextError("One line exceeds the serialized output budget; use bounded search")
    return payload


def inventory(view: FilesystemProjectView) -> dict:
    paths = list(CONTROL_PATHS)
    state, _, _ = load_text(view, "sdad-state.yaml")
    parsed = inspect_state(state)
    if parsed.snapshot is not None:
        for key in ("active_spec", "current_handoff"):
            pointer = parsed.snapshot.scalar(key)
            if pointer and pointer.value and pointer.value not in paths:
                paths.append(pointer.value)
    records = []
    for path in paths:
        try:
            text, digest, size = load_text(view, path)
            count = len(text.splitlines())
            action = "review_compaction" if size > 200_000 or count > 2_000 else "targeted_read" if size > 50_000 or count > 500 else "within_default_budget"
            records.append({"path": path, "status": "ok", "bytes": size,
                            "lines": count, "sha256": digest, "advice": action})
        except ContextError as exc:
            records.append({"path": path, "status": "unavailable", "detail": str(exc)})
    return {"schema_version": 1, "root": view.root.as_posix(), "files": records,
            "state_issue_count": len(parsed.issues),
            "limits": "Size advice only. No completion, acceptance or safe-to-archive inference. Run Doctor separately."}


def run_cli(arguments: Sequence[str] | None = None, *, stdout: TextIO | None = None) -> int:
    output = stdout if stdout is not None else sys.stdout
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".", help="explicit project directory")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("inspect", help="summarize active controls, the declared SPEC and handoff")
    read = sub.add_parser("read", help="read a bounded UTF-8 page; no writes")
    read.add_argument("path", help="normalized relative project path")
    read.add_argument("--heading", help="one exact Markdown ATX heading, without #")
    read.add_argument("--start", type=int, help="one-based file line, inside the selected section")
    read.add_argument("--lines", type=int, default=100)
    read.add_argument("--expect-sha256", help="refuse to combine different source revisions")
    args = parser.parse_args(arguments)
    try:
        view = FilesystemProjectView(Path(args.root).expanduser())
        payload = inventory(view) if args.command == "inspect" else read_page(
            view, args.path, start=args.start, count=args.lines, heading=args.heading,
            expected_sha256=args.expect_sha256)
    except (ContextError, DiagnosticError) as exc:
        output.write(json.dumps({"schema_version": 1, "error": str(exc)}, ensure_ascii=False) + "\n")
        return 2
    output.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_cli())
