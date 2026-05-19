from __future__ import annotations

from .common import *  # noqa: F403
from .proposal_models import proposal_concrete_operation_count, proposals_concrete_operation_count

def all_provider_observability_green(by_kind: dict[str, dict[str, Any]]) -> bool:
    resource_lanes = by_kind.get("local_ai_resource_lanes")
    npu_manifest = by_kind.get("npu_runtime_output_manifest")
    provider_parsing = by_kind.get("provider_result_parsing")
    provider_probe = by_kind.get("local_provider_probe")

    ready_lanes = (
        set(resource_lanes.get("ready_lanes") or []) if isinstance(resource_lanes, dict) else set()
    )
    return (
        report_passed(resource_lanes)
        and {"gpu", "npu", "ollama"}.issubset(ready_lanes)
        and report_passed(npu_manifest)
        and int(npu_manifest.get("blocked_count") or 0) == 0
        and report_passed(provider_parsing)
        and report_passed(provider_probe)
        and provider_probe.get("provider_execution_performed") is True
    )

def provider_report_adoption_green(by_kind: dict[str, dict[str, Any]]) -> bool:
    provider_result_report = by_kind.get("provider_result_report")
    provider_probe = by_kind.get("local_provider_probe")
    return (
        all_provider_observability_green(by_kind)
        and report_passed(provider_result_report)
        and provider_result_report.get("provider_execution_performed") is False
        and provider_result_report.get("mode") == "runtime_safe_report_only"
        and provider_probe.get("provider_execution_performed") is True
    )

def workload_quality_decision(by_kind: dict[str, dict[str, Any]]) -> dict[str, Any]:
    report = by_kind.get("ai_workload_report_quality")
    if not isinstance(report, dict):
        return {
            "quality_report_present": False,
            "usable_lanes": [],
            "unusable_lanes": [],
            "ollama_gpu_primary_advisory_allowed": False,
            "npu_excluded_from_primary_advisory": True,
        }
    decision = report.get("decision") if isinstance(report.get("decision"), dict) else {}
    return {
        "quality_report_present": True,
        "usable_lanes": report.get("usable_lanes") or [],
        "unusable_lanes": report.get("unusable_lanes") or [],
        "ollama_gpu_primary_advisory_allowed": decision.get("ollama_gpu_primary_advisory_allowed")
        is True,
        "npu_excluded_from_primary_advisory": decision.get("npu_excluded_from_primary_advisory")
        is not False,
        "routing_policy": decision.get("routing_policy") or report.get("policy"),
    }

def ai_workload_quality_has_unusable_output(by_kind: dict[str, dict[str, Any]]) -> bool:
    report = by_kind.get("ai_workload_report_quality")
    return isinstance(report, dict) and bool(report.get("unusable_lanes"))
