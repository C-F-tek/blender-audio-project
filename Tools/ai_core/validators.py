from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass(slots=True)
class ValidationIssue:
    level: str
    message: str
    path: str | None = None


@dataclass(slots=True)
class ValidationReport:
    passed: bool = True
    issues: list[ValidationIssue] = field(default_factory=list)

    def add(self, level: str, message: str, path: str | None = None) -> None:
        issue = ValidationIssue(level=level, message=message, path=path)
        self.issues.append(issue)
        if level.lower() in {"error", "critical"}:
            self.passed = False

    def error(self, message: str, path: str | None = None) -> None:
        self.add("error", message, path)

    def warning(self, message: str, path: str | None = None) -> None:
        self.add("warning", message, path)

    def to_dict(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "issues": [
                {"level": issue.level, "message": issue.message, "path": issue.path}
                for issue in self.issues
            ],
        }


class Validator(Protocol):
    def validate(self, payload: Any) -> ValidationReport:
        ...


class AlwaysPassValidator:
    def validate(self, payload: Any) -> ValidationReport:
        return ValidationReport(passed=True)


class RequiredKeysValidator:
    def __init__(self, required_keys: list[str]) -> None:
        self.required_keys = required_keys

    def validate(self, payload: Any) -> ValidationReport:
        report = ValidationReport()
        if not isinstance(payload, dict):
            report.error(f"Expected dict payload, got {type(payload).__name__}")
            return report
        for key in self.required_keys:
            if key not in payload:
                report.error(f"Missing required key: {key}", path=key)
        return report
