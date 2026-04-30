from __future__ import annotations

from typing import Any


def build_helper_boundary_report(*, package_name: str, modules: list[str], checks: dict[str, Any]) -> dict[str, Any]:
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
