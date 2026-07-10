from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from enum import Enum


DEFAULT_Q5_KEYWORDS = frozenset(
    {
        "release",
        "production",
        "migration",
        "destructive action",
        "real user data",
        "auth",
        "money",
        "security",
        "rollback",
    }
)

DIAGNOSTIC_ERROR_KINDS = frozenset(
    {
        "invalid_invocation",
        "unusable_root",
        "unreadable_state",
        "internal_error",
    }
)


class Severity(str, Enum):
    ERROR = "error"
    WARNING = "warning"


@dataclass(frozen=True)
class Finding:
    id: str
    severity: Severity
    message: str
    path: str | None
    line: int | None
    evidence: str
    remediation: str


@dataclass(frozen=True)
class DoctorPolicy:
    today: date
    stale_after_days: int = 30
    max_state_bytes: int = 65_536
    max_control_document_bytes: int = 1_048_576
    q5_keywords: frozenset[str] = DEFAULT_Q5_KEYWORDS


@dataclass(frozen=True)
class DoctorReport:
    root: str
    findings: tuple[Finding, ...]
    checks_run: tuple[str, ...]
    checks_skipped: tuple[str, ...]
    error_count: int
    warning_count: int


class DiagnosticError(RuntimeError):
    def __init__(self, kind: str, message: str) -> None:
        if kind not in DIAGNOSTIC_ERROR_KINDS:
            raise ValueError(f"unsupported diagnostic error kind: {kind}")
        super().__init__(message)
        self.kind = kind
