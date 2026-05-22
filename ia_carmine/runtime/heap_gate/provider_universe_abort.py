"""Provider-universe abort helpers for heap runtime gate."""
from __future__ import annotations
from ia_carmine.runtime.heap_gate.runtime_common import Any, now_iso, repo_rel, subprocess


def provider_universe_abort_reason(prepared: list[dict[str, Any]]) -> str:
    for item in prepared:
        report = item.get("provider_report")
        if not isinstance(report, dict):
            continue
        status = str(report.get("status") or "")
        if status in {"failed", "non_operational"}:
            exact = str(
                report.get("product_blocked_reason")
                or report.get("provider_activity_classification")
                or ""
            )
            if exact:
                return exact
            return f"provider_universe_lane_not_active:{item.get('lane')}:{status}"
    return ""


def primary_provider_report(prepared: list[dict[str, Any]]) -> dict[str, Any]:
    for item in prepared:
        if item.get("lane") == "gpu1_planner" and isinstance(item.get("provider_report"), dict):
            return item["provider_report"]
    return {}


def primary_provider_block_reason(prepared: list[dict[str, Any]]) -> str:
    report = primary_provider_report(prepared)
    if not report:
        return "provider_universe_primary_lane_missing_report"
    exact = str(
        report.get("product_blocked_reason")
        or report.get("provider_activity_classification")
        or ""
    )
    if report.get("status") != "ready":
        return exact or f"provider_universe_primary_lane_not_ready:{report.get('status')}"
    if not report.get("operational_provider_activity"):
        classification = report.get("provider_activity_classification") or "unknown"
        return f"provider_universe_primary_lane_not_operational:{classification}"
    return ""


def block_unstarted_provider_items(items: list[dict[str, Any]], reason: str) -> None:
    for item in items:
        if item.get("completed") is not None or item.get("started_at"):
            continue
        item["blocked_reason"] = reason
        item["completed_at"] = now_iso()
        item["elapsed_seconds"] = 0.0
        item["completed"] = subprocess.CompletedProcess(
            list(item.get("command") or []),
            130,
            "",
            f"provider lane not started because primary lane blocked universe: {reason}",
        )


def block_provider_universe_run(gate: Any, reason: str, round_id: int, revision: int) -> None:
    if not reason:
        return
    gate.provider_universe_blocked_reason = reason
    if reason not in gate.errors:
        gate.errors.append(reason)
    decision = {
        "id": "provider_universe_blocked",
        "from": "provider_universe",
        "decision": "blocked_with_reason",
        "reason": reason,
        "revision": revision,
        "round": round_id,
    }
    if not any(item.get("id") == decision["id"] for item in gate.state.get("decisions", [])):
        gate.state["decisions"].append(decision)
        gate.decision_count += 1
        gate.publish(
            "deterministic",
            "decision",
            decision,
            target="orchestrator",
            correlation_id=f"{gate.stamp}:provider-universe-blocked",
            round_id=round_id,
        )
    product = {
        "required": True,
        "product_kind": "blocked_continuation_product",
        "status": "blocked_with_reason",
        "product_status": "blocked_with_reason",
        "product_blocked_reason": reason,
        "failed_provider": _failed_provider_from_reason(reason),
        "request_input": gate.request_text(),
        "response_text": gate.build_final_response_text(gate.read_events()),
        "response_source": gate.response_source(),
        "heap_event_refs": [repo_rel(gate.repo_root, gate.heap.paths.events)],
        "provider_refs": gate.provider_refs(),
        "provider_replight_required": True,
        "provider_replight_reports": _provider_replight_reports(gate),
        "provider_response_texts": gate.provider_response_texts(),
        "provider_role_decisions": gate.provider_role_decisions(),
        "missing_requirements": [reason],
        "reason": reason,
        "provider_universe_blocked": True,
        "continuation_required": True,
        "soft_close_reason": reason,
    }
    gate.state["product"] = product
    gate.publish(
        "orchestrator",
        "product_signal",
        product,
        correlation_id=f"{gate.stamp}:provider-universe-product-blocked",
        round_id=round_id,
    )


def _failed_provider_from_reason(reason: str) -> str:
    parts = str(reason or "").split(":")
    if len(parts) >= 2 and parts[0] == "provider_replight_failed":
        return parts[1]
    for lane in ("gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"):
        if lane in str(reason or ""):
            return lane
    return ""


def _provider_replight_reports(gate: Any) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for report in (
        list(getattr(gate, "provider_replight_reports", []) or [])
        + list(getattr(gate, "provider_reports", []) or [])
    ):
        if not isinstance(report, dict):
            continue
        reports.append(
            {
                "provider_id": report.get("provider_id") or report.get("lane"),
                "provider_role": report.get("provider_role") or report.get("role"),
                "provider_model": report.get("provider_model") or report.get("selected_model"),
                "requested_provider_model": report.get("requested_provider_model"),
                "selected_provider_model": report.get("selected_provider_model") or report.get("selected_model"),
                "model_switch_reason": report.get("model_switch_reason"),
                "provider_backend": report.get("provider_backend"),
                "provider_compute_device": report.get("provider_compute_device"),
                "full_gpu_residency_required": report.get("full_gpu_residency_required"),
                "full_gpu_residency_verified": report.get("full_gpu_residency_verified"),
                "device_workload_performed": report.get("device_workload_execution_performed")
                or report.get("npu_device_workload_performed"),
                "semantic_provider_model_loaded": report.get("semantic_provider_model_loaded")
                or report.get("npu_micro_provider_model_loaded"),
                "provider_loaded": report.get("provider_loaded"),
                "generated_phrase": report.get("generated_phrase"),
                "prompt_token_count": report.get("prompt_token_count"),
                "completion_token_count": report.get("completion_token_count"),
                "tokens_per_second": report.get("tokens_per_second"),
                "native_tool_calling_supported": report.get(
                    "native_tool_calling_supported"
                ),
                "broker_tools_available_count": report.get(
                    "broker_tools_available_count"
                ),
                "available_tool_names": report.get("available_tool_names") or [],
                "functionalities": report.get("functionalities") or [],
                "replight_passed": report.get("replight_passed"),
                "replight_blocked_reason": report.get("replight_blocked_reason"),
            }
        )
    return reports
