"""Provider-native tool-call handling for the heap broker."""

from __future__ import annotations

from ia_carmine._shared.file_backed_transport import (
    report_text,
    report_text_required_full,
    write_json_artifact,
)
from ia_carmine._shared.provider_work_rejections import role_for
from ia_carmine._shared.provider_tool_schemas import is_api_native_tool_call
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    append_unique,
    provider_heap_lane,
    provider_patch_synthesis_plan,
)
from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS

PRIMARY_NATIVE_TOOL_CALL_LANES = {"gpu1_planner"}
PEER_NATIVE_TOOL_CALL_LANES = {"gpu0_peer"}
OPERATIVE_NATIVE_TOOL_CALL_LANES = PRIMARY_NATIVE_TOOL_CALL_LANES | PEER_NATIVE_TOOL_CALL_LANES
DIAGNOSTIC_NATIVE_TOOL_CALL_LANES = {"npu_micro_task_auditor"}
SIDECAR_NATIVE_TOOL_CALL_LANES = PEER_NATIVE_TOOL_CALL_LANES | DIAGNOSTIC_NATIVE_TOOL_CALL_LANES
NO_TOOL_GENERIC_WRITE_CAPTURE_LANES: set[str] = set()
EVIDENCE_ENRICHED_TOOLS = {
    "generic_write",
    "run_heap_code_execution_matrix",
    "synthesize_patch_candidates",
}


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
        fallback_requirement = (
            "generic_write_refinement"
            if tool_name == "generic_write"
            else f"provider_native_{tool_name}"
        )
        return {
            "stage": 99,
            "requirement": requirement or fallback_requirement,
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


def publish_provider_report_native_tool_calls(
    owner: Any, report: dict[str, Any], round_id: int, events: list[dict[str, Any]]
) -> int:
    return _publish_report_native_tool_calls(owner, report, round_id, events)


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
        if not is_api_native_tool_call(call, lane=lane):
            _publish_non_native_tool_call_diagnostic(owner, source, lane, output, call, unique_id, round_id)
            continue
        if tool_name == "generic_write" and lane in SIDECAR_NATIVE_TOOL_CALL_LANES:
            _publish_sidecar_generic_write_non_decision(
                owner, source, lane, output, call, unique_id, round_id
            )
            continue
        if lane not in OPERATIVE_NATIVE_TOOL_CALL_LANES:
            _publish_peer_native_call_diagnostic(
                owner, source, lane, output, call, unique_id, round_id
            )
            continue
        plan_item = owner.provider_plan_item_for_tool_call(call, events)
        if not plan_item:
            _publish_unmapped_native_call(owner, source, lane, output, call, unique_id, round_id)
            continue
        _enrich_provider_native_tool_args(owner, report, output, call, plan_item)
        request_id = f"{owner.stamp}:provider-native:{call_id}:{plan_item['tool']}"
        _publish_need_and_request(owner, report, call, plan_item, request_id, round_id)
        published += 1
    if (
        not calls
        and lane in PRIMARY_NATIVE_TOOL_CALL_LANES
        and str(report_text(getattr(owner, "repo_root", None), report).get("text") or "").strip()
    ):
        _publish_primary_free_text_raw_evidence(owner, report, output, round_id)
    elif (
        not calls
        and lane in SIDECAR_NATIVE_TOOL_CALL_LANES
        and str(report_text(getattr(owner, "repo_root", None), report).get("text") or "").strip()
    ):
        _publish_sidecar_free_text_raw_evidence(owner, report, output, round_id)
    return published


def _lane_tool_authority(lane: str) -> dict[str, Any]:
    if lane in PRIMARY_NATIVE_TOOL_CALL_LANES:
        return {
            "native_tool_call_authority": "primary_broker_authority",
            "tool_result_scope": "primary_product_evidence",
            "gpu1_followup_required": False,
            "cannot_close_product": False,
            "peer_only": False,
        }
    if lane in PEER_NATIVE_TOOL_CALL_LANES:
        return {
            "native_tool_call_authority": "peer_broker_authority",
            "tool_result_scope": "gpu0_peer_evidence_only",
            "gpu1_followup_required": True,
            "cannot_close_product": True,
            "peer_only": True,
        }
    return {
        "native_tool_call_authority": "diagnostic_only",
        "tool_result_scope": "diagnostic_veto_evidence",
        "gpu1_followup_required": True,
        "cannot_close_product": True,
        "peer_only": True,
    }


def _report_has_useful_no_tool_text(report: dict[str, Any]) -> bool:
    lane = str(report.get("lane") or "")
    if lane not in NO_TOOL_GENERIC_WRITE_CAPTURE_LANES:
        return False
    if str(report_text(report.get("repo_root"), report).get("text") or "").strip() == "":
        return False
    if isinstance(report.get("tool_calls"), list) and report.get("tool_calls"):
        return False
    npu_peer_evidence = bool(
        lane == "npu_micro_task_auditor"
        and (
            report.get("npu_peer_evidence_verified")
            or (
                report.get("provider_device_verified")
                and report.get("npu_device_workload_performed")
                and report.get("npu_micro_audit_performed")
            )
        )
    )
    useful_evidence = bool(
        report.get("provider_work_verified")
        or report.get("operational_provider_activity")
        or report.get("useful_output_produced")
        or npu_peer_evidence
    )
    provider_stage = str(report.get("provider_stage") or "").strip()
    if provider_stage == "health_check_only" and not npu_peer_evidence:
        return False
    if report.get("provider_work_verified") is False and not useful_evidence:
        return False
    if report.get("replight_passed") is not None and not useful_evidence:
        return False
    return True


def _publish_no_tool_generic_write_capture(
    owner: Any,
    report: dict[str, Any],
    output: str,
    round_id: int,
    events: list[dict[str, Any]],
) -> int:
    lane = str(report.get("lane") or "provider")
    revision = str(report.get("revision") or "000")
    call = {
        "id": f"{lane}_no_tool_capture_{revision}",
        "tool": "generic_write",
        "args": {"capture_mode": "no_tool_capture"},
        "reason": (
            "Provider lane produced useful text without native tool calls; capture it "
            "as generic_write primary communication evidence."
        ),
    }
    unique_id = f"{output}:{call['id']}:generic_write"
    if unique_id in owner.provider_native_tool_call_ids:
        return 0
    owner.provider_native_tool_call_ids.add(unique_id)
    plan_item = owner.provider_plan_item_for_tool_call(call, events)
    if not plan_item:
        _publish_unmapped_native_call(
            owner,
            provider_heap_lane(lane),
            lane,
            output,
            call,
            unique_id,
            round_id,
        )
        return 0
    _enrich_provider_native_tool_args(owner, report, output, call, plan_item)
    request_id = f"{owner.stamp}:provider-no-tool-capture:{lane}:{revision}:generic_write"
    _publish_need_and_request(owner, report, call, plan_item, request_id, round_id)
    return 1


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
            "diagnostic_tool_call_lane": lane in DIAGNOSTIC_NATIVE_TOOL_CALL_LANES,
            "policy": (
                "GPU1 is the primary native-tool lane. GPU0 uses the same tool schema "
                "as peer evidence that must be consumed by a later GPU1 turn. NPU "
                "native tool calls remain diagnostic/veto evidence and do not drive "
                "broker work."
            ),
        },
        target="deterministic",
        correlation_id=unique_id,
        round_id=round_id,
    )


def _publish_sidecar_generic_write_non_decision(
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
            "kind": "sidecar_generic_write_non_decision",
            "lane": lane,
            "tool_call": call,
            "provider_report": output,
            "sidecar_scope_mode": "packet_review_only",
            "raw_evidence_non_decision": True,
            "gpu1_followup_required": True,
            "policy": (
                "GPU0/NPU sidecars cannot promote free-form generic_write as an "
                "operative product channel. They must emit packet-bound review, "
                "veto or evidence_request data for GPU1 to consume."
            ),
        },
        target="deterministic",
        correlation_id=unique_id,
        round_id=round_id,
    )


def _publish_sidecar_free_text_raw_evidence(
    owner: Any,
    report: dict[str, Any],
    output: str,
    round_id: int,
) -> None:
    lane = str(report.get("lane") or "provider")
    owner.publish(
        provider_heap_lane(lane),
        "validation_signal",
        {
            "kind": "sidecar_free_text_raw_evidence_non_decision",
            "lane": lane,
            "provider_report": output,
            "provider_block_id": report.get("provider_block_id"),
            "proposal_block_id": report.get("proposal_block_id"),
            "revision": report.get("revision"),
            "sidecar_scope_mode": "packet_review_only",
            "raw_evidence_non_decision": True,
            "gpu1_followup_required": True,
        },
        target="deterministic",
        correlation_id=f"{output}:{lane}:free-text-non-decision",
        round_id=round_id,
    )


def _publish_non_native_tool_call_diagnostic(
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
            "kind": "provider_textual_tool_call_not_executable",
            "lane": lane,
            "tool_call": call,
            "provider_report": output,
            "raw_evidence_non_decision": True,
            "policy": (
                "Only provider API-native tool_calls are broker executable. "
                "Markdown, JSON-in-text and structured prose tool requests remain diagnostic."
            ),
        },
        target="deterministic",
        correlation_id=unique_id,
        round_id=round_id,
    )


def _publish_primary_free_text_raw_evidence(
    owner: Any,
    report: dict[str, Any],
    output: str,
    round_id: int,
) -> None:
    lane = str(report.get("lane") or "provider")
    owner.publish(
        provider_heap_lane(lane),
        "validation_signal",
        {
            "kind": "primary_free_text_without_native_tool_call",
            "lane": lane,
            "provider_report": output,
            "provider_block_id": report.get("provider_block_id"),
            "proposal_block_id": report.get("proposal_block_id"),
            "revision": report.get("revision"),
            "raw_evidence_non_decision": True,
            "provider_textual_tool_call_not_executable": bool(report.get("textual_tool_calls")),
            "native_tool_call_required": bool(report.get("provider_native_tool_call_required")),
            "policy": (
                "GPU1 prose without a native provider tool_call is retained as raw "
                "text evidence only. It does not create broker requests and cannot "
                "verify lab, matrix, patch, workload or product status."
            ),
        },
        target="deterministic",
        correlation_id=f"{output}:{lane}:free-text-no-native-tool",
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


def _enrich_provider_native_tool_args(
    owner: Any,
    report: dict[str, Any],
    output: str,
    call: dict[str, Any],
    plan_item: dict[str, Any],
) -> None:
    tool = str(plan_item.get("tool") or "")
    if tool not in EVIDENCE_ENRICHED_TOOLS:
        return
    args = dict(plan_item.get("args") or {})
    refs = args.get("evidence_report")
    evidence_reports = list(refs if isinstance(refs, list) else ([refs] if refs else []))
    bridge_reports = list(getattr(owner, "bridge_reports", []) or [])
    for ref in [output, *owner.proposal_iteration_artifacts(), *bridge_reports]:
        if ref and ref not in evidence_reports:
            evidence_reports.append(ref)
    args["evidence_report"] = evidence_reports
    if tool == "generic_write":
        call_args = call.get("args") if isinstance(call.get("args"), dict) else {}
        args.setdefault("capture_mode", str(call_args.get("capture_mode") or "native_call"))
        args.setdefault("provider_report", output)
        lane = str(report.get("lane") or "")
        peer_followup_required = lane in {"gpu0_peer", "npu_micro_task_auditor"}
        revision = report.get("revision")
        args.setdefault("source_lane", lane)
        args.setdefault("source_revision", "" if revision is None else str(revision))
        args.setdefault("gpu1_followup_required", str(peer_followup_required).lower())
        args.setdefault("peer_followup_required", str(peer_followup_required).lower())
        args.setdefault(
            "provider_role",
            role_for(
                lane,
                report,
                str(report.get("provider_role") or report.get("role") or ""),
            ),
        )
        args.setdefault(
            "proposal_text",
            str(report_text_required_full(getattr(owner, "repo_root", None), report).get("text") or ""),
        )
        args.setdefault("request_file", str(getattr(owner.args, "request_file", "") or ""))
        if not args.get("request_file"):
            args.setdefault("operator_request", owner.request_text()[:5000])
        args.setdefault(
            "reason",
            call.get("reason")
            or "Provider lane requested generic_write to refine the next GPU1 turn.",
        )
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
    authority = _lane_tool_authority(lane)
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
        **authority,
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
        **authority,
    }
    if plan_item.get("nonblocking"):
        tool_request["nonblocking"] = True
    append_unique(owner.state["tool_requests"], tool_request)
    request_ref = write_json_artifact(
        owner.repo_root,
        owner.provider_work_dir() / "broker_request_payloads",
        name=request_id.replace(":", "_"),
        payload=tool_request,
        kind="provider_native_broker_request",
        producer="tool_broker_native_calls",
    )
    event_payload = {
        "id": request_id,
        "request_id": request_id,
        "tool": tool_request["tool"],
        "args_keys": sorted(str(key) for key in (tool_request.get("args") or {}))[:32],
        "lane": lane,
        "provider_native_tool_call": True,
        "payload_file_backed": True,
        "payload_ref": request_ref,
        "payload_kind": "provider_native_broker_request",
    }
    owner.publish(
        source,
        "broker_request",
        event_payload,
        target="broker",
        correlation_id=request_id,
        round_id=round_id,
    )
    owner.tool_request_count += 1
