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
        model = str(item.get("selected_model") or "").strip()
        model_text = f",model={_short_label(model, 28)}" if model else ""
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
        diagnostic = item.get("diagnostic_only")
        diagnostic_text = f",diag={_bool_marker(diagnostic)}" if diagnostic not in ("", None) else ""
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
            f"{lane}[{status}{role_text}{model_text}{elapsed_text}{budget_text}{soft_text}"
            f"{watchdog_text}{pid_text}{semantic_text}"
            f"{operational_text}{diagnostic_text}{native_text}{partial_text}{response_text}"
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
        lane = str(data.get("lane") or lane_from_name(item.name))
        if support_provider_payload(lane, data):
            continue
        result.append(
            {
                "lane": lane,
                "status": data.get("status") or ("written" if data else "pending"),
                "passed": data.get("passed"),
                "selected_model": data.get("selected_model") or data.get("model"),
                "semantic_provider_execution_performed": data.get("semantic_provider_execution_performed"),
                "operational_provider_activity": data.get("operational_provider_activity"),
                "diagnostic_only": data.get("diagnostic_only"),
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
