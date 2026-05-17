"""Report processing for runtime flow-map evidence."""

from __future__ import annotations

from collections import Counter
from pathlib import Path
from typing import Any

from .common import (
    add_edge,
    add_node,
    append_event,
    as_dict,
    as_list,
    compact_report_summary,
    component_from_report,
    repo_rel,
    safe_int,
)

def process_report(
    *,
    repo_root: Path,
    path: Path,
    data: dict[str, Any],
    parse_error: str,
    nodes: dict[str, dict[str, Any]],
    edges: dict[tuple[str, str, str], dict[str, Any]],
    events: list[dict[str, Any]],
    counters: Counter[str],
) -> dict[str, Any]:
    rel = repo_rel(path, repo_root)
    component = component_from_report(rel, data)
    report_node = f"report:{rel}"
    add_node(nodes, report_node, "report", rel, path=rel, kind=data.get("kind"))
    add_edge(edges, component, report_node, "emits_report", 1)
    append_event(
        events,
        component=component,
        action="report_observed",
        status="error" if parse_error else "ok",
        span=rel,
        report_path=rel,
        kind=data.get("kind"),
    )

    if parse_error:
        counters["parse_error_count"] += 1
        return compact_report_summary(rel, data, parse_error)

    counters["report_count"] += 1
    if data.get("passed") is False:
        counters["failed_report_count"] += 1

    round_count = safe_int(
        data.get("round_count") or data.get("gpu_round_count") or len(as_list(data.get("rounds")))
    )
    if round_count:
        counters["round_count"] = max(counters["round_count"], round_count)
        add_edge(edges, "orchestrator", "gpu_planner", "round_loop", round_count)

    recommendation_count = safe_int(
        data.get("recommendation_count")
        or data.get("gpu_recommendation_count")
        or data.get("proposal_count")
    )
    if recommendation_count:
        counters["recommendation_count"] += recommendation_count
        add_edge(edges, component, "recommendations", "produces", recommendation_count)
        append_event(
            events,
            component=component,
            action="recommendation",
            status="observed",
            span=rel,
            count=recommendation_count,
        )

    patch_plan_count = safe_int(
        data.get("patch_plan_count") or len(as_list(data.get("patch_plans")))
    )
    if patch_plan_count:
        counters["patch_plan_count"] += patch_plan_count
        add_edge(edges, component, "patch_plan", "produces", patch_plan_count)
        append_event(
            events,
            component=component,
            action="patch_plan",
            status="observed",
            span=rel,
            count=patch_plan_count,
        )

    tool_request_count = safe_int(
        data.get("tool_request_count") or data.get("requested_tool_count")
    )
    tool_execution_count = safe_int(data.get("tool_execution_count"))
    if tool_request_count:
        counters["tool_request_count"] += tool_request_count
        add_edge(edges, component, "broker", "tool_request", tool_request_count)
        append_event(
            events,
            component=component,
            action="tool_request",
            status="observed",
            span=rel,
            count=tool_request_count,
        )
    if tool_execution_count:
        counters["tool_execution_count"] += tool_execution_count
        add_edge(edges, "broker", component, "tool_result", tool_execution_count)
        append_event(
            events,
            component="broker",
            action="tool_execution",
            status="observed",
            span=rel,
            count=tool_execution_count,
        )

    if data.get("provider_execution_performed") is True:
        counters["provider_call_count"] += 1
        append_event(events, component=component, action="provider_call", status="ok", span=rel)

    heap_event_count = safe_int(data.get("event_count"))
    by_lane = as_dict(data.get("by_lane"))
    if heap_event_count or by_lane:
        counters["heap_event_count"] += heap_event_count
        for lane, lane_data in by_lane.items():
            lane_component = {
                "gpu1": "gpu_planner",
                "gpu0": "gpu0_peer",
                "npu": "npu_peer",
                "broker": "broker",
                "orchestrator": "orchestrator",
                "deterministic": "validation",
            }.get(str(lane), str(lane))
            event_count = safe_int(as_dict(lane_data).get("event_count"), 1)
            add_edge(edges, lane_component, "heap", "heap_write", event_count)
            counters["heap_write_count"] += event_count
        append_event(
            events,
            component="heap",
            action="heap_snapshot",
            status="observed",
            span=rel,
            count=heap_event_count,
        )

    for round_item in as_list(data.get("rounds"))[:200]:
        if not isinstance(round_item, dict):
            continue
        round_id = safe_int(round_item.get("round"))
        span = f"round_{round_id:03d}" if round_id >= 0 else rel
        json_ok = round_item.get("json_ok")
        status = "ok" if json_ok is True or json_ok is None else "error"
        append_event(events, component=component, action="round", status=status, span=span)

    return compact_report_summary(rel, data, parse_error)
