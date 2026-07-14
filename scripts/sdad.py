#!/usr/bin/env python3
"""Checkout-only, read-only command line interface for SDAD diagnostics.

This entry point reports existing control-plane evidence. It does not execute
validation commands, mutate project files, contact a network, or accept work
on the owner's behalf.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass
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


DOCTOR_VERSION = "3.2.1"
LEGACY_REPORT_SCHEMA_VERSION = 1
REPORT_SCHEMA_VERSION = 2
_CORE_VERSION = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$"
)
_INTERNAL_ERROR_MESSAGE = "The diagnostic could not be completed."
Diagnose = Callable[[ProjectView, DoctorPolicy], DoctorReport]


class _HelpRequested(Exception):
    pass


class _InvalidInvocation(Exception):
    def __init__(self, message: str, project_root: str | None = None) -> None:
        super().__init__(message)
        self.project_root = project_root


@dataclass(frozen=True)
class _VersionRequirementProbe:
    present: bool
    value: str | None
    error: str | None


class _ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args: object, stdout: TextIO | None = None, **kwargs: object) -> None:
        self._stdout = stdout if stdout is not None else sys.stdout
        super().__init__(*args, **kwargs)

    def _print_message(self, message: str | None, file: TextIO | None = None) -> None:
        if message:
            (file or self._stdout).write(message)

    def print_help(self, file: TextIO | None = None) -> None:
        self._print_message(
            self.format_help(),
            file if file is not None else self._stdout,
        )

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
    doctor.add_argument(
        "--require-version",
        action="append",
        metavar="VERSION",
        help="require one exact Doctor core version",
    )
    return parser


def _explicit_flag(arguments: Sequence[str], flag: str) -> bool:
    for value in arguments:
        if value == "--":
            break
        if value == flag or value.startswith(flag + "="):
            return True
    return False


def _probe_version_requirement(
    arguments: Sequence[str],
) -> _VersionRequirementProbe:
    if not arguments or arguments[0] != "doctor":
        return _VersionRequirementProbe(False, None, None)
    values: list[str] = []
    index = 1
    while index < len(arguments):
        token = arguments[index]
        if token == "--":
            break
        if token == "--require-version":
            if index + 1 >= len(arguments) or arguments[index + 1].startswith("-"):
                return _VersionRequirementProbe(
                    True,
                    None,
                    "--require-version requires one value",
                )
            values.append(arguments[index + 1])
            index += 2
            continue
        if token.startswith("--require-version="):
            values.append(token.split("=", 1)[1])
        index += 1
    if not values:
        return _VersionRequirementProbe(False, None, None)
    if len(values) != 1:
        return _VersionRequirementProbe(
            True,
            None,
            "--require-version may appear once",
        )
    if _CORE_VERSION.fullmatch(values[0]) is None:
        return _VersionRequirementProbe(
            True,
            values[0],
            "--require-version requires core X.Y.Z",
        )
    return _VersionRequirementProbe(True, values[0], None)


def _doctor_help_requested(arguments: Sequence[str]) -> bool:
    if not arguments or arguments[0] != "doctor":
        return False
    for token in arguments[1:]:
        if token == "--":
            return False
        if token in {"-h", "--help"}:
            return True
    return False


def _select_report_schema(
    *,
    guard_present: bool,
    state_version: int | None,
) -> int:
    return (
        REPORT_SCHEMA_VERSION
        if guard_present or state_version == 2
        else LEGACY_REPORT_SCHEMA_VERSION
    )


def _probe_project_root(arguments: Sequence[str]) -> str | None:
    prefix: list[str] = []
    options_enabled = True
    for value in arguments:
        if options_enabled and (
            value.startswith("--json=")
            or value.startswith("--strict=")
        ):
            break
        prefix.append(value)
        if value == "--":
            options_enabled = False

    try:
        namespace, _unknown = _parser(io.StringIO()).parse_known_args(prefix)
    except (_HelpRequested, _InvalidInvocation):
        return None
    return namespace.project_root


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


def _completed_payload(
    report: DoctorReport,
    strict: bool,
    report_schema: int,
) -> dict[str, object]:
    if report_schema == LEGACY_REPORT_SCHEMA_VERSION:
        return {
            "schema_version": LEGACY_REPORT_SCHEMA_VERSION,
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
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "doctor_version": DOCTOR_VERSION,
        "state_version": report.state_version,
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
    root: str | None,
    strict: bool,
    error: DiagnosticError,
    report_schema: int,
) -> dict[str, object]:
    if report_schema == LEGACY_REPORT_SCHEMA_VERSION:
        return {
            "schema_version": LEGACY_REPORT_SCHEMA_VERSION,
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
    return {
        "schema_version": REPORT_SCHEMA_VERSION,
        "doctor_version": DOCTOR_VERSION,
        "state_version": error.state_version,
        "root": root.replace("\\", "/") if root is not None else None,
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
    root: str | None,
    strict: bool,
    json_mode: bool,
    guard_present: bool,
    stdout: TextIO,
    stderr: TextIO,
) -> int:
    safe_error = DiagnosticError(
        error.kind,
        _message(error, _INTERNAL_ERROR_MESSAGE),
        state_version=error.state_version,
    )
    if json_mode:
        report_schema = _select_report_schema(
            guard_present=guard_present,
            state_version=safe_error.state_version,
        )
        stdout.write(
            _json_text(
                _error_payload(
                    root=root,
                    strict=strict,
                    error=safe_error,
                    report_schema=report_schema,
                )
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
    output = stdout if stdout is not None else sys.stdout
    errors = stderr if stderr is not None else sys.stderr
    json_mode = _explicit_flag(raw_arguments, "--json")
    strict = _explicit_flag(raw_arguments, "--strict")

    if raw_arguments == ["--version"]:
        output.write(DOCTOR_VERSION + "\n")
        return 0

    if _explicit_flag(raw_arguments, "--version"):
        return _emit_error(
            DiagnosticError(
                "invalid_invocation",
                "--version must be used as a standalone operation",
            ),
            root=_path_text(Path.cwd()),
            strict=strict,
            json_mode=json_mode,
            guard_present=False,
            stdout=output,
            stderr=errors,
        )

    if _doctor_help_requested(raw_arguments):
        try:
            _parser(output).parse_args(["doctor", "--help"])
        except _HelpRequested:
            return 0

    version_probe = _probe_version_requirement(raw_arguments)
    if (
        not raw_arguments
        or raw_arguments[0] != "doctor"
    ) and _explicit_flag(raw_arguments, "--require-version"):
        return _emit_error(
            DiagnosticError(
                "invalid_invocation",
                "--require-version is only valid with the doctor command",
            ),
            root=_path_text(Path.cwd()),
            strict=strict,
            json_mode=json_mode,
            guard_present=False,
            stdout=output,
            stderr=errors,
        )

    if version_probe.error is not None:
        return _emit_error(
            DiagnosticError("invalid_invocation", version_probe.error),
            root=None,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )

    if version_probe.present and version_probe.value != DOCTOR_VERSION:
        return _emit_error(
            DiagnosticError(
                "version_mismatch",
                "Required Doctor version "
                f"{version_probe.value} does not match {DOCTOR_VERSION}.",
            ),
            root=None,
            strict=strict,
            json_mode=json_mode,
            guard_present=True,
            stdout=output,
            stderr=errors,
        )

    current_root = _path_text(Path.cwd())
    probed_root = _probe_project_root(raw_arguments)

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
        invalid_root = (
            exc.project_root
            if exc.project_root is not None
            else probed_root
        )
        return _emit_error(
            DiagnosticError(
                "invalid_invocation",
                _message(exc, "The command invocation is invalid."),
            ),
            root=(
                None
                if version_probe.present
                else (
                    _path_text(invalid_root)
                    if invalid_root is not None
                    else current_root
                )
            ),
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )

    json_mode = bool(namespace.json_mode)
    strict = bool(namespace.strict)
    root_input = namespace.project_root or Path.cwd()
    attempted_root = _path_text(root_input)
    pre_acceptance_root = None if version_probe.present else attempted_root

    try:
        view = FilesystemProjectView(root_input)
    except DiagnosticError as exc:
        return _emit_error(
            exc,
            root=pre_acceptance_root,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )
    except (OSError, RuntimeError, ValueError) as exc:
        return _emit_error(
            DiagnosticError(
                "unusable_root",
                _message(exc, "The project root cannot be inspected."),
            ),
            root=pre_acceptance_root,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )
    except Exception:
        return _emit_error(
            DiagnosticError("internal_error", _INTERNAL_ERROR_MESSAGE),
            root=pre_acceptance_root,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
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
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )
    except Exception:
        return _emit_error(
            DiagnosticError("internal_error", _INTERNAL_ERROR_MESSAGE),
            root=accepted_root,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )

    report_state_version = (
        report.state_version if isinstance(report, DoctorReport) else None
    )
    try:
        if not isinstance(report, DoctorReport):
            raise TypeError("diagnostic engine returned an invalid report")
        exit_code = int(
            report.error_count > 0
            or (strict and report.warning_count > 0)
        )
        report_schema = _select_report_schema(
            guard_present=version_probe.present,
            state_version=report.state_version,
        )
        rendered = (
            _json_text(_completed_payload(report, strict, report_schema))
            if json_mode
            else _render_human(report)
        )
    except Exception:
        return _emit_error(
            DiagnosticError(
                "internal_error",
                _INTERNAL_ERROR_MESSAGE,
                state_version=report_state_version,
            ),
            root=accepted_root,
            strict=strict,
            json_mode=json_mode,
            guard_present=version_probe.present,
            stdout=output,
            stderr=errors,
        )

    output.write(rendered)
    return exit_code


if __name__ == "__main__":
    raise SystemExit(run_cli())
