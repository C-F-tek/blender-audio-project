from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

COMMON_VALIDATION_REPORT_KEYS = (
    "schema_version",
    "kind",
    "repo_root",
    "passed",
    "errors",
    "warnings",
    "checks",
)


@dataclass(frozen=True)
class RuntimeOutputManifestEntry:
    """One planned or observed runtime output path entry."""

    path: str
    kind: str
    policy_source: str
    allowed: bool
    legacy: bool = False
    generated: bool = False
    provider_execution_performed: bool = False
    reason: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "kind": self.kind,
            "policy_source": self.policy_source,
            "allowed": self.allowed,
            "legacy": self.legacy,
            "generated": self.generated,
            "provider_execution_performed": self.provider_execution_performed,
            "reason": self.reason,
        }


def build_validation_report(
    *,
    kind: str,
    repo_root: Path | str,
    passed: bool,
    errors: list[str] | None = None,
    warnings: list[str] | None = None,
    checks: dict[str, Any] | None = None,
    schema_version: int = 1,
) -> dict[str, Any]:
    """Build a common deterministic validation-report envelope."""

    return {
        "schema_version": schema_version,
        "kind": kind,
        "repo_root": str(repo_root),
        "passed": passed,
        "errors": list(errors or []),
        "warnings": list(warnings or []),
        "checks": dict(checks or {}),
    }


def validation_report_has_common_keys(report: dict[str, Any]) -> bool:
    """Return True when a report exposes the common validation-report keys."""

    return all(key in report for key in COMMON_VALIDATION_REPORT_KEYS)


def build_helper_boundary_report(
    *, package_name: str, modules: list[str], checks: dict[str, Any]
) -> dict[str, Any]:
    """Build a deterministic report for the app-agnostic helper boundary."""

    return {
        "schema_version": 1,
        "kind": "npu_pipeline_helper_boundary",
        "package": package_name,
        "module_count": len(modules),
        "modules": sorted(modules),
        "checks": checks,
    }


def helper_boundary_passed(report: dict[str, Any]) -> bool:
    """Return True when all boolean check values in a boundary report are true."""

    checks = report.get("checks") or {}
    for value in checks.values():
        if isinstance(value, bool) and value is not True:
            return False
    return True


def build_runtime_output_manifest(
    *,
    repo_root: Path | str,
    entries: list[RuntimeOutputManifestEntry],
    provider_execution_performed: bool = False,
    schema_version: int = 1,
) -> dict[str, Any]:
    """Build an additive runtime-output manifest without touching files."""

    entry_payload = [entry.to_dict() for entry in entries]
    blocked = [entry for entry in entry_payload if entry.get("allowed") is not True]
    return {
        "schema_version": schema_version,
        "kind": "npu_runtime_output_manifest",
        "repo_root": str(repo_root),
        "provider_execution_performed": provider_execution_performed,
        "output_count": len(entry_payload),
        "blocked_count": len(blocked),
        "passed": not blocked,
        "errors": [f"blocked runtime output: {entry.get('path')}" for entry in blocked],
        "warnings": [],
        "outputs": entry_payload,
    }


def runtime_output_manifest_passed(manifest: dict[str, Any]) -> bool:
    """Return True when a runtime-output manifest has no blocked entries."""

    return manifest.get("passed") is True and manifest.get("blocked_count") == 0
