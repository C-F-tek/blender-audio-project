"""Provider-native tool-call handling for the heap broker."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    append_unique,
    provider_heap_lane,
    provider_patch_synthesis_plan,
)
from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS


def provider_plan_item_for_tool_call(
    owner: Any, call: dict[str, Any], events: list[dict[str, Any]]
) -> dict[str, Any] | None:
    tool_name = str(call.get("tool") or "").strip()
    requirement = str(call.get("requirement") or "").strip()
    for item in owner.tool_plan():
        if item["tool"] == tool_name or (requirement and item["requirement"] == requirement):
            return owner.enrich_plan_item_args(item, events)
    if tool_name == "synthesize_patch_candidates":
        return provider_patch_synthesis_plan(
            call=call,
            target_files=owner.code_execution_matrix_targets(),
            operator_request=owner.request_text(),
            operator_request_file=str(getattr(owner.args, "request_file", "") or ""),
            files_per_round=int(owner.args.files_per_round),
            timeout_seconds=int(owner.args.timeout_seconds),
        )
    if tool_name in TOOL_SPECS:
        return {
            "stage": 99,
            "requirement": requirement or f"provider_native_{tool_name}",
            "id": f"provider-native-{tool_name}",
            "tool": tool_name,
            "args": dict(call.get("args") or {}),
            "reason": call.get("reason")
            or f"provider native tool_call requested allowlisted tool {tool_name}",
        }
    return None


def publish_provider_native_tool_calls(
    owner: Any, round_id: int, events: list[dict[str, Any]]
) -> int:
    published = 0
    for report in owner.provider_reports:
        published += _publish_report_native_tool_calls(owner, report, round_id, events)
    return published


def _publish_report_native_tool_calls(
    owner: Any, report: dict[str, Any], round_id: int, events: list[dict[str, Any]]
) -> int:
    published = 0
    lane = str(report.get("lane") or "provider")
    source = provider_heap_lane(lane)
    output = str(report.get("output") or "")
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    for index, call in enumerate(calls, start=1):
        if not isinstance(call, dict):
            continue
        tool_name = str(call.get("tool") or "").strip()
        call_id = str(call.get("id") or f"{tool_name}_{index:03d}")
        unique_id = f"{output}:{call_id}:{tool_name}"
        if unique_id in owner.provider_native_tool_call_ids:
            continue
        owner.provider_native_tool_call_ids.add(unique_id)
        if lane != "gpu1_planner":
            _publish_peer_native_call_diagnostic(
                owner, source, lane, output, call, unique_id, round_id
            )
            continue
        plan_item = owner.provider_plan_item_for_tool_call(call, events)
        if not plan_item:
            _publish_unmapped_native_call(owner, source, lane, output, call, unique_id, round_id)
            continue
        _add_evidence_reports(owner, output, plan_item)
        request_id = f"{owner.stamp}:provider-native:{call_id}:{plan_item['tool']}"
        _publish_need_and_request(owner, report, call, plan_item, request_id, round_id)
        published += 1
    return published


def _publish_peer_native_call_diagnostic(
    owner: Any,
    source: str,
    lane: str,
    output: str,
    call: dict[str, Any],
    unique_id: str,
    round_id: int,
) -> None:
    owner.publish(
        source,
        "validation_signal",
        {
            "kind": "provider_peer_native_tool_call_diagnostic_only",
            "lane": lane,
            "tool_call": call,
            "provider_report": output,
            "policy": (
                "GPU1 is the cognitive center. GPU0/NPU native tool calls are "
                "peer evidence and must not become broker-driving work."
            ),
        },
        target="deterministic",
        correlation_id=unique_id,
        round_id=round_id,
    )


def _publish_unmapped_native_call(
    owner: Any,
    source: str,
    lane: str,
    output: str,
    call: dict[str, Any],
    unique_id: str,
    round_id: int,
) -> None:
    tool_name = str(call.get("tool") or "").strip()
    owner.errors.append(f"provider_native_tool_call_unmapped:{lane}:{tool_name or '<empty>'}")
    owner.publish(
        source,
        "validation_signal",
        {
            "kind": "provider_native_tool_call_unmapped",
            "lane": lane,
            "tool_call": call,
            "provider_report": output,
        },
        target="deterministic",
        correlation_id=unique_id,
        round_id=round_id,
    )


def _add_evidence_reports(owner: Any, output: str, plan_item: dict[str, Any]) -> None:
    if plan_item.get("tool") not in {"synthesize_patch_candidates", "run_heap_code_execution_matrix"}:
        return
    args = dict(plan_item.get("args") or {})
    refs = args.get("evidence_report")
    evidence_reports = list(refs if isinstance(refs, list) else ([refs] if refs else []))
    for ref in [output, *owner.proposal_iteration_artifacts()]:
        if ref and ref not in evidence_reports:
            evidence_reports.append(ref)
    args["evidence_report"] = evidence_reports
    plan_item["args"] = args


def _publish_need_and_request(
    owner: Any,
    report: dict[str, Any],
    call: dict[str, Any],
    plan_item: dict[str, Any],
    request_id: str,
    round_id: int,
) -> None:
    lane = str(report.get("lane") or "provider")
    source = provider_heap_lane(lane)
    output = str(report.get("output") or "")
    call_id = str(call.get("id") or f"{plan_item['tool']}_001")
    need = {
        "id": f"need_provider_native_{plan_item['requirement']}_{call_id}",
        "owner": lane,
        "kind": "provider_native_tool_call",
        "target": plan_item["tool"],
        "requirement": plan_item["requirement"],
        "reason": call.get("reason")
        or plan_item.get("reason")
        or "provider native tool call requested broker evidence",
        "provider_report": output,
        "provider_block_id": report.get("provider_block_id"),
        "proposal_block_id": report.get("proposal_block_id"),
        "revision": report.get("revision"),
        "round": round_id,
    }
    append_unique(owner.state["needs"], need)
    owner.publish(
        source,
        "need",
        need,
        target="broker",
        correlation_id=request_id,
        round_id=round_id,
    )
    tool_request = {
        "id": request_id,
        "tool": plan_item["tool"],
        "args": plan_item.get("args") or {},
        "reason": need["reason"],
        "requirement": plan_item["requirement"],
        "provider_native_tool_call": True,
        "provider_report": output,
        "lane": lane,
        "revision": report.get("revision"),
        "provider_block_id": report.get("provider_block_id"),
        "proposal_block_id": report.get("proposal_block_id"),
    }
    if plan_item.get("nonblocking"):
        tool_request["nonblocking"] = True
    append_unique(owner.state["tool_requests"], tool_request)
    owner.publish(
        source,
        "broker_request",
        tool_request,
        target="broker",
        correlation_id=request_id,
        round_id=round_id,
    )
    owner.tool_request_count += 1
