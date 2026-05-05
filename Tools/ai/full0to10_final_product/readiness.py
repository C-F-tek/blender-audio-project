"""Readiness scoring for Full0To10 final tool product."""
from __future__ import annotations

from typing import Any

from .constants import SAFETY_FLAGS


def contract_passed(record: dict[str, Any]) -> bool:
    data = record.get("json")
    return bool(isinstance(data, dict) and data.get("passed") is True)


def build_readiness(records: dict[str, Any], evidence_index: dict[str, Any]) -> dict[str, Any]:
    score = 100
    blockers: list[str] = []
    warnings: list[str] = []

    if not evidence_index["passed"]:
        score -= 35
        blockers.extend(evidence_index["missing_required_roles"])

    json_roles = (
        "effective_use_summary",
        "provider_hardening",
        "tool_telemetry",
        "optimization",
        "quality_gate",
        "accelerator_control",
        "provider_governor",
        "provider_run_permit",
        "provider_invocation_plan",
        "provider_workload_report_contract",
        "provider_expected_telemetry_contract",
    )
    for role in json_roles:
        record = records.get(role, {})
        if record.get("exists") and record.get("type") == "json" and not contract_passed(record):
            score -= 10
            warnings.append(f"{role}_not_passed")

    permit = records.get("provider_run_permit", {}).get("json") or {}
    if permit.get("provider_execution_performed") is True:
        score -= 40
        blockers.append("provider_governor_executed_provider")

    invocation = records.get("provider_invocation_plan", {}).get("json") or {}
    if invocation.get("generation_executes_now") is True:
        score -= 40
        blockers.append("provider_invocation_plan_executes_generation")
    if invocation.get("readiness", {}).get("ready_for_bundle_inclusion") is not True:
        score -= 10
        warnings.append("provider_invocation_plan_not_bundle_ready")

    score = max(0, score)
    report = {
        "kind": "full0to10_final_tool_product_readiness",
        "passed": not blockers,
        "score": score,
        "ready_for_tool_product_review": score >= 80 and not blockers,
        "ready_for_real_provider_run": False,
        "blockers": blockers,
        "warnings": warnings,
        "policy": "final_product_review_before_real_provider_run",
    }
    report.update(SAFETY_FLAGS)
    return report
