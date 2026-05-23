"""Provider lane status helpers for live flow rendering."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


PROVIDER_LANES = {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}


def support_provider_payload(lane: str, payload: dict[str, Any]) -> bool:
    role = str(payload.get("role") or "").strip()
    return lane == "orchestrator" or role == "support" or (lane and lane not in PROVIDER_LANES)


def lane_details(run_status: dict[str, Any]) -> str:
    providers = run_status.get("provider_lane_statuses") or []
    parts = []
    for item in providers[:4]:
        lane = str(item.get("lane") or "").strip()
        if not lane or support_provider_payload(lane, item):
            continue
        status = item.get("status") or item.get("passed") or "?"
        role_text = f",role={lane_role(lane)}"
        tier = str(item.get("lane_tier") or "").strip()
        tier_text = f",tier={_short_label(tier, 18)}" if tier else ""
        authority = str(item.get("authority") or "").strip()
        authority_text = f",auth={_short_label(authority, 14)}" if authority else ""
        context_budget = item.get("context_budget") if isinstance(item.get("context_budget"), dict) else {}
        context_text = _context_budget_text(context_budget)
        owner = str(item.get("closure_owner") or "").strip()
        owner_text = f",owner={_short_label(owner, 18)}" if owner else ""
        model = str(item.get("selected_model") or "").strip()
        model_text = f",model={_short_label(model, 28)}" if model else ""
        device = str(item.get("provider_compute_device") or "").strip()
        device_text = f",dev={_short_label(device, 24)}" if device else ""
        verified = item.get("provider_device_verified")
        verified_text = f",devok={_bool_marker(verified)}" if verified not in ("", None) else ""
        identity = item.get("device_identity_verified")
        identity_text = (
            f",idok={_bool_marker(identity)}" if identity not in ("", None) else ""
        )
        backend_device = str(item.get("provider_backend_device_id") or "").strip()
        backend_text = f",backend_dev={_short_label(backend_device, 18)}" if backend_device else ""
        windows_hint = str(item.get("windows_task_manager_device_hint") or "").strip()
        windows_text = f",win={_short_label(windows_hint, 24)}" if windows_hint else ""
        elapsed = item.get("elapsed_seconds")
        elapsed_text = f",t={elapsed}s" if elapsed not in ("", None) else ""
        budget = item.get("budget_counter_seconds")
        budget_text = f",budget={budget}s" if budget not in ("", None) else ""
        soft_close = item.get("soft_close_after_seconds")
        soft_text = f",soft={soft_close}s" if soft_close not in ("", None) else ""
        watchdog = item.get("watchdog_timeout_seconds")
        watchdog_text = f",watchdog={watchdog}s" if watchdog not in ("", None) else ""
        pid = item.get("pid")
        pid_text = f",pid={pid}" if pid not in ("", None) else ""
        semantic = item.get("semantic_provider_execution_performed")
        semantic_text = f",semantic={_bool_marker(semantic)}" if semantic not in ("", None) else ""
        operational = item.get("operational_provider_activity")
        operational_text = f",op={_bool_marker(operational)}" if operational not in ("", None) else ""
        primary_evidence = item.get("gpu1_primary_evidence_valid")
        primary_evidence_text = (
            f",primary_ev={_bool_marker(primary_evidence)}"
            if primary_evidence not in ("", None)
            else ""
        )
        leader_source = str(item.get("leader_source") or "").strip()
        leader_source_text = (
            f",leader={_short_label(leader_source, 18)}" if leader_source else ""
        )
        diagnostic = item.get("diagnostic_only")
        diagnostic_text = f",diag={_bool_marker(diagnostic)}" if diagnostic not in ("", None) else ""
        replight = item.get("replight_passed")
        replight_text = f",replight={_bool_marker(replight)}" if replight not in ("", None) else ""
        loaded = item.get("provider_loaded")
        loaded_text = f",loaded={_bool_marker(loaded)}" if loaded not in ("", None) else ""
        completion_tokens = item.get("completion_token_count")
        token_text = f",tok={completion_tokens}" if completion_tokens not in ("", None) else ""
        native = item.get("native_tool_call_count")
        native_text = f",native={native}" if native not in ("", None) else ""
        partial = item.get("partial_response_chars")
        partial_text = f",partial={partial}ch" if partial not in ("", None) else ""
        response = item.get("response_chars")
        response_text = f",resp={response}ch" if response not in ("", None) else ""
        classification = str(item.get("provider_activity_classification") or "").split(":", 1)[-1]
        class_text = f",class={_short_label(classification, 32)}" if classification else ""
        output = str(item.get("output") or "").replace("\\", "/").rsplit("/", 1)[-1]
        output_text = f",out={output}" if output else ""
        parts.append(
            f"{lane}[{status}{role_text}{tier_text}{authority_text}{context_text}{owner_text}"
            f"{model_text}{device_text}{verified_text}{elapsed_text}{budget_text}{soft_text}"
            f"{watchdog_text}{pid_text}{identity_text}{backend_text}{windows_text}{semantic_text}"
            f"{operational_text}{primary_evidence_text}{leader_source_text}"
            f"{diagnostic_text}{replight_text}{loaded_text}{token_text}"
            f"{native_text}{partial_text}{response_text}"
            f"{class_text}{output_text}]"
        )
    return ",".join(parts) or "-"


def lane_role(lane: str) -> str:
    return {
        "gpu1_planner": "primary",
        "gpu0_peer": "peer",
        "npu_micro_task_auditor": "micro",
    }.get(lane, "support")


def provider_status(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    result: list[dict[str, Any]] = []
    for item in sorted(path.glob("*.json")):
        if item.name.startswith(("provider_launch_manifest", "provider_teamwork_leader_packet")):
            continue
        try:
            data = json.loads(item.read_text(encoding="utf-8-sig", errors="replace"))
        except Exception:
            data = {}
        data = data if isinstance(data, dict) else {}
        lane = str(data.get("provider_id") or data.get("lane") or lane_from_name(item.name))
        if support_provider_payload(lane, data):
            continue
        result.append(
            {
                "lane": lane,
                "status": data.get("status") or ("written" if data else "pending"),
                "passed": data.get("passed"),
                "selected_model": data.get("provider_model") or data.get("selected_model") or data.get("model"),
                "semantic_provider_execution_performed": data.get("semantic_provider_execution_performed"),
                "lane_tier": data.get("lane_tier"),
                "authority": data.get("authority"),
                "closure_owner": data.get("closure_owner"),
                "context_budget": data.get("context_budget"),
                "provider_backend": data.get("provider_backend"),
                "provider_compute_device": data.get("provider_compute_device"),
                "provider_device_verified": data.get("provider_device_verified"),
                "logical_lane": data.get("logical_lane"),
                "provider_backend_device_id": data.get("provider_backend_device_id"),
                "windows_task_manager_device_hint": data.get(
                    "windows_task_manager_device_hint"
                ),
                "vulkan_visible_device": data.get("vulkan_visible_device"),
                "vulkan_device_name": data.get("vulkan_device_name"),
                "vulkan_vendor_id": data.get("vulkan_vendor_id"),
                "device_identity_verified": data.get("device_identity_verified"),
                "cpu_provider_fallback_performed": data.get("cpu_provider_fallback_performed"),
                "operational_provider_activity": data.get("operational_provider_activity"),
                "gpu1_primary_workload_valid": data.get("gpu1_primary_workload_valid"),
                "gpu1_primary_evidence_valid": data.get("gpu1_primary_evidence_valid"),
                "gpu1_primary_evidence_source": data.get("gpu1_primary_evidence_source"),
                "leader_source": data.get("leader_source"),
                "diagnostic_only": data.get("diagnostic_only"),
                "replight_passed": data.get("replight_passed"),
                "provider_loaded": data.get("provider_loaded"),
                "generated_phrase": data.get("generated_phrase"),
                "completion_token_count": data.get("completion_token_count"),
                "provider_activity_classification": data.get("provider_activity_classification"),
                "native_tool_call_count": data.get("native_tool_call_count"),
                "partial_response_chars": data.get("partial_response_chars"),
                "response_chars": response_chars(data),
                "budget_counter_seconds": data.get("budget_counter_seconds"),
                "soft_close_after_seconds": data.get("soft_close_after_seconds"),
                "watchdog_timeout_seconds": data.get("watchdog_timeout_seconds"),
                "output": str(item),
            }
        )
    return result


def merge_provider_statuses(
    event_statuses: list[dict[str, Any]], file_statuses: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in event_statuses + file_statuses:
        lane = str(item.get("lane") or "").strip()
        if not lane or support_provider_payload(lane, item):
            continue
        current = merged.get(lane, {})
        current.update({key: value for key, value in item.items() if value not in ("", None)})
        current["source"] = "heap_event+artifact" if lane in merged else item.get("source", "artifact")
        merged[lane] = current
    return [merged[key] for key in sorted(merged)]


def lane_from_name(name: str) -> str:
    if name.startswith("gpu1_"):
        return "gpu1_planner"
    if name.startswith("gpu0_"):
        return "gpu0_peer"
    if name.startswith("npu_"):
        return "npu_micro_task_auditor"
    return name.rsplit(".", 1)[0]


def response_chars(data: dict[str, Any]) -> int | None:
    text = str(data.get("response_text") or data.get("provider_heap_delta_text") or "")
    return len(text) if text else None


def _short_label(value: str, limit: int) -> str:
    text = value.replace(" ", "_").replace(",", "_")
    return text if len(text) <= limit else text[: max(0, limit - 1)] + "~"


def _bool_marker(value: Any) -> str:
    return "yes" if value is True else ("no" if value is False else str(value))


def _context_budget_text(value: dict[str, Any]) -> str:
    if not isinstance(value, dict) or not value:
        return ""
    for key in ("ollama_num_ctx", "max_context_chars", "max_prompt_chars"):
        data = value.get(key)
        if data not in ("", None):
            return f",ctx={data}"
    return ""
