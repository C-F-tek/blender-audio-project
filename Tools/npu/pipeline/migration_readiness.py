from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MigrationReadinessCheck:
    """One deterministic readiness check for a future runtime wiring step."""

    name: str
    passed: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "passed": self.passed,
            "reason": self.reason,
        }


def build_migration_readiness_report(
    *,
    target_file: str,
    checks: list[MigrationReadinessCheck],
    allowed_to_modify_runtime: bool,
) -> dict[str, Any]:
    """Build a readiness report for a future runtime migration step."""

    check_payload = [check.to_dict() for check in checks]
    failed = [check for check in check_payload if check.get("passed") is not True]
    return {
        "schema_version": 1,
        "kind": "npu_pipeline_migration_readiness",
        "target_file": target_file,
        "allowed_to_modify_runtime": allowed_to_modify_runtime,
        "ready": bool(allowed_to_modify_runtime and not failed),
        "failed_count": len(failed),
        "checks": check_payload,
    }


def default_runtime_wiring_readiness(
    *, local_validation_passed: bool, indexes_regenerated: bool
) -> dict[str, Any]:
    """Return the default gate for wiring helpers into the legacy runtime file."""

    checks = [
        MigrationReadinessCheck(
            name="local_validation_passed",
            passed=local_validation_passed,
            reason="Full local validation must pass before runtime wiring.",
        ),
        MigrationReadinessCheck(
            name="indexes_regenerated",
            passed=indexes_regenerated,
            reason="AI/NPU indexes must be regenerated after structural helper changes.",
        ),
        MigrationReadinessCheck(
            name="runtime_not_modified_in_current_batch",
            passed=True,
            reason="Current batch must keep runtime behavior unchanged.",
        ),
    ]
    return build_migration_readiness_report(
        target_file="Tools/npu/dual_ai_pipeline/cli.py",
        checks=checks,
        allowed_to_modify_runtime=False,
    )
