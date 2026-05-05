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

    for role in ("effective_use_summary", "provider_hardening", "tool_telemetry", "optimization", "quality_gate"):
        record = records.get(role, {})
        if not record.get("exists"):
            continue
        if record.get("type") == "json" and not contract_passed(record):
            score -= 12
            warnings.append(f"{role}_not_passed")

    provider = records.get("provider_hardening", {}).get("json") or {}
    lanes = provider.get("lanes") or {}
    if "ollama_gpu" not in lanes:
        score -= 8
        warnings.append("ollama_gpu_contract_missing")
    if "openvino_npu" not in lanes:
        score -= 8
        warnings.append("openvino_npu_contract_missing")
    if "sqlite_fts5" not in lanes:
        score -= 8
        blockers.append("sqlite_fts5_contract_missing")

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
