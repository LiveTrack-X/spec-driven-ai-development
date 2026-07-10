#!/usr/bin/env python3
"""Checkout-only, read-only command line interface for SDAD diagnostics.

This entry point reports existing control-plane evidence. It does not execute
validation commands, mutate project files, contact a network, or accept work
on the owner's behalf.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Callable, Sequence
from datetime import date
from pathlib import Path
from typing import TextIO


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from sdad_validator.diagnostics import (  # noqa: E402
    DiagnosticError,
    DoctorPolicy,
    DoctorReport,
    Finding,
)
from sdad_validator.doctor import DiagnosticEngine  # noqa: E402
from sdad_validator.project_view import (  # noqa: E402
    FilesystemProjectView,
    ProjectView,
)


SCHEMA_VERSION = 1
_INTERNAL_ERROR_MESSAGE = "The diagnostic could not be completed."
Diagnose = Callable[[ProjectView, DoctorPolicy], DoctorReport]


class _HelpRequested(Exception):
    pass


class _InvalidInvocation(Exception):
    def __init__(self, message: str, project_root: str | None = None) -> None:
        super().__init__(message)
        self.project_root = project_root


class _ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: object, stdout: TextIO | None = None, **kwargs: object) -> None:
        self._stdout = stdout or sys.stdout
        super().__init__(*args, **kwargs)

    def _print_message(self, message: str | None, file: TextIO | None = None) -> None:
        if message:
            (file or self._stdout).write(message)

    def error(self, message: str) -> None:
        raise _InvalidInvocation(message)

    def exit(self, status: int = 0, message: str | None = None) -> None:
        if status == 0:
            if message:
                self._print_message(message)
            raise _HelpRequested
        raise _InvalidInvocation(message or "invalid invocation")


def _parser(stdout: TextIO) -> _ArgumentParser:
    parser = _ArgumentParser(
        prog="sdad.py",
        description="Inspect an SDAD project without changing it.",
        allow_abbrev=False,
        stdout=stdout,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    doctor = commands.add_parser(
        "doctor",
        help="diagnose a stateful SDAD control plane",
        allow_abbrev=False,
        stdout=stdout,
    )
    doctor.add_argument(
        "project_root",
        nargs="?",
        metavar="PROJECT_ROOT",
        help="project to inspect (default: current directory)",
    )
    doctor.add_argument(
        "--json",
        action="store_true",
        dest="json_mode",
        help="emit one versioned JSON document",
    )
    doctor.add_argument(
        "--strict",
        action="store_true",
        help="make warnings fail without reclassifying them",
    )
    return parser


def _explicit_flag(arguments: Sequence[str], flag: str) -> bool:
    return any(value == flag or value.startswith(flag + "=") for value in arguments)


def _path_text(value: str | Path) -> str:
    try:
        return Path(value).expanduser().resolve(strict=False).as_posix()
    except (OSError, RuntimeError, ValueError):
        return str(value).replace("\\", "/")


def _message(value: object, fallback: str) -> str:
    normalized = " ".join(str(value).split())
    return normalized or fallback


def _finding_payload(finding: Finding) -> dict[str, object]:
    return {
        "id": finding.id,
        "severity": finding.severity.value,
        "path": finding.path.replace("\\", "/") if finding.path is not None else None,
        "line": finding.line,
        "message": finding.message,
        "evidence": finding.evidence,
        "remediation": finding.remediation,
    }


def _completed_payload(report: DoctorReport, strict: bool) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "root": report.root.replace("\\", "/"),
        "strict": strict,
        "summary": {
            "errors": report.error_count,
            "warnings": report.warning_count,
        },
        "checks": {
            "run": list(report.checks_run),
            "skipped": list(report.checks_skipped),
        },
        "findings": [_finding_payload(finding) for finding in report.findings],
    }


def _error_payload(
    *,
    root: str,
    strict: bool,
    error: DiagnosticError,
) -> dict[str, object]:
    return {
        "schema_version": SCHEMA_VERSION,
        "root": root.replace("\\", "/"),
        "strict": strict,
        "summary": {"errors": 0, "warnings": 0},
        "checks": {"run": [], "skipped": []},
        "findings": [],
        "diagnostic_error": {
            "kind": error.kind,
            "message": _message(error, _INTERNAL_ERROR_MESSAGE),
        },
    }


def _json_text(payload: dict[str, object]) -> str:
    return json.dumps(payload, ensure_ascii=False, indent=2) + "\n"


def _quantity(value: int, singular: str) -> str:
    noun = singular if value == 1 else singular + "s"
    return f"{value} {noun}"


def _summary(report: DoctorReport) -> str:
    return (
        "Doctor: "
        f"{_quantity(report.error_count, 'error')}, "
        f"{_quantity(report.warning_count, 'warning')}, "
        f"{_quantity(len(report.checks_run), 'check')} run, "
        f"{len(report.checks_skipped)} skipped"
    )


def _render_human(report: DoctorReport) -> str:
    lines: list[str] = []
    for finding in report.findings:
        header = f"{finding.severity.value.upper()} {finding.id}"
        if finding.path is not None:
            location = finding.path.replace("\\", "/")
            if finding.line is not None:
                location += f":{finding.line}"
            header += f" {location}"
        lines.extend(
            [
                header,
                f"  Observed: {finding.evidence}",
                f"  Fix: {finding.remediation}",
                "",
            ]
        )
    lines.append(_summary(report))
    return "\n".join(lines) + "\n"


def _emit_error(
    error: DiagnosticError,
    *,
    root: str,
    strict: bool,
    json_mode: bool,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    safe_error = DiagnosticError(
        error.kind,
        _message(error, _INTERNAL_ERROR_MESSAGE),
    )
    if json_mode:
        stdout.write(
            _json_text(
                _error_payload(root=root, strict=strict, error=safe_error)
            )
        )
    else:
        stderr.write(f"Doctor error [{safe_error.kind}]: {safe_error}\n")
    return 2


def run_cli(
    arguments: Sequence[str] | None = None,
    *,
    diagnose: Diagnose | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run one diagnosis and render its result to the selected streams."""

    raw_arguments = list(sys.argv[1:] if arguments is None else arguments)
    output = stdout or sys.stdout
    errors = stderr or sys.stderr
    json_mode = _explicit_flag(raw_arguments, "--json")
    strict = _explicit_flag(raw_arguments, "--strict")
    current_root = _path_text(Path.cwd())

    try:
        namespace, unknown = _parser(output).parse_known_args(raw_arguments)
        if unknown:
            raise _InvalidInvocation(
                "unrecognized arguments: " + " ".join(unknown),
                project_root=namespace.project_root,
            )
    except _HelpRequested:
        return 0
    except _InvalidInvocation as exc:
        return _emit_error(
            DiagnosticError(
                "invalid_invocation",
                _message(exc, "The command invocation is invalid."),
            ),
            root=(
                _path_text(exc.project_root)
                if exc.project_root is not None
                else current_root
            ),
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )

    json_mode = bool(namespace.json_mode)
    strict = bool(namespace.strict)
    root_input = namespace.project_root or Path.cwd()
    attempted_root = _path_text(root_input)

    try:
        view = FilesystemProjectView(root_input)
    except DiagnosticError as exc:
        return _emit_error(
            exc,
            root=attempted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return _emit_error(
            DiagnosticError(
                "unusable_root",
                _message(exc, "The project root cannot be inspected."),
            ),
            root=attempted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )
    except Exception:
        return _emit_error(
            DiagnosticError("internal_error", _INTERNAL_ERROR_MESSAGE),
            root=attempted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )

    accepted_root = view.root.as_posix()
    diagnose_once = diagnose or DiagnosticEngine().diagnose
    try:
        report = diagnose_once(view, DoctorPolicy(today=date.today()))
    except DiagnosticError as exc:
        return _emit_error(
            exc,
            root=accepted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )
    except Exception:
        return _emit_error(
            DiagnosticError("internal_error", _INTERNAL_ERROR_MESSAGE),
            root=accepted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )

    try:
        if not isinstance(report, DoctorReport):
            raise TypeError("diagnostic engine returned an invalid report")
        exit_code = int(
            report.error_count > 0
            or (strict and report.warning_count > 0)
        )
        rendered = (
            _json_text(_completed_payload(report, strict))
            if json_mode
            else _render_human(report)
        )
    except Exception:
        return _emit_error(
            DiagnosticError("internal_error", _INTERNAL_ERROR_MESSAGE),
            root=accepted_root,
            strict=strict,
            json_mode=json_mode,
            stdout=output,
            stderr=errors,
        )

    output.write(rendered)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_cli())
