"""Provider execution evidence checks kept out of the provider runner."""

from __future__ import annotations

from ia_carmine._shared.file_backed_transport import report_text_required_full
from ia_carmine._shared.provider_work_rejections import looks_like_handshake, normalize_bool
from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
from ia_carmine.runtime.heap_gate.generic_write_followup import failed_generic_write_results
from ia_carmine.runtime.heap_gate.final_product_delta_protocol import (
    code_file_read_contract,
    final_product_protocol,
)
from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import (
    gpu1_tool_result_consumption_state,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, safe_int


def gpu1_primary_workload_status(
    report: dict[str, Any],
    *,
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    response_text = str(report_text_required_full(repo_root, report).get("text") or "").strip()
    token_count = safe_int(
        report.get("eval_count") or report.get("completion_token_count"),
        default=0,
    )
    provider_stage = str(report.get("provider_stage") or "").strip()
    non_replight = (
        not normalize_bool(report.get("replight_mode"))
        and provider_stage != "health_check_only"
    )
    workload_valid = bool(
        report.get("passed") is True
        and non_replight
        and response_text
        and not looks_like_handshake(response_text)
        and (
            report.get("provider_work_verified")
            or report.get("semantic_provider_execution_performed")
            or report.get("operational_provider_activity")
            or report.get("useful_output_produced")
        )
    )
    return {
        "gpu1_primary_workload_valid": workload_valid,
        "gpu1_primary_workload_chars": len(response_text),
        "gpu1_primary_workload_tokens": token_count,
        "gpu1_primary_workload_stage": provider_stage,
    }


def gpu1_primary_evidence_status(
    owner: Any | None, report: dict[str, Any], events: list[dict[str, Any]]
) -> dict[str, Any]:
    generic_failed = [
        payload
        for payload in failed_generic_write_results(events, owner=owner)
        if _same_gpu1_revision(payload, report)
    ]
    tool_state = (
        gpu1_tool_result_consumption_state(owner, events, report=report)
        if owner is not None
        else {}
    )
    response_text = _report_text(owner, report) if owner is not None else ""
    consumed_ids = [
        str(item)
        for item in (tool_state.get("gpu1_consumed_tool_result_ids") or [])
        if str(item).strip()
    ]
    consumed_passed_ids = [
        str(item)
        for item in (tool_state.get("gpu1_consumed_passed_tool_result_ids") or [])
        if str(item).strip()
    ]
    source = "native_tool_result_consumed_by_gpu1" if consumed_passed_ids else ""
    if tool_state.get("gpu1_resume_after_tool_result_required"):
        source = ""
    elif owner is not None and response_text:
        protocol = final_product_protocol(response_text)
        code_read = code_file_read_contract(
            owner,
            response_text=response_text,
            protocol=protocol,
            target_files=[
                str(item)
                for item in (report.get("target_files") or [])
                if str(item).strip()
            ],
            events=events,
        )
        if protocol.get("passed") and (
            not code_read.get("required") or code_read.get("verified")
        ):
            source = source or "gpu1_final_product_delta"
    return {
        "gpu1_primary_evidence_valid": bool(source),
        "gpu1_primary_evidence_source": source,
        "leader_source": source or "none",
        "gpu1_generic_write_capture_valid": False,
        "gpu1_generic_write_capture_failed": bool(generic_failed),
        **tool_state,
    }


def provider_overlap_seconds(
    primary_items: list[dict[str, Any]], sidecar_items: list[dict[str, Any]]
) -> float:
    if not primary_items:
        return 0.0
    primary_start = primary_items[0].get("started_perf")
    primary_end = primary_items[0].get("completed_perf")
    if primary_start is None or primary_end is None:
        return 0.0
    best = 0.0
    for item in sidecar_items:
        side_start = item.get("started_perf")
        side_end = item.get("completed_perf")
        if side_start is None or side_end is None:
            continue
        overlap = min(float(primary_end), float(side_end)) - max(
            float(primary_start), float(side_start)
        )
        best = max(best, overlap)
    return round(max(0.0, best), 6)


def _same_gpu1_revision(payload: dict[str, Any], report: dict[str, Any]) -> bool:
    if str(payload.get("lane") or "") != "gpu1_planner":
        return False
    payload_revision = payload.get("revision")
    report_revision = report.get("revision")
    if payload_revision is not None and report_revision is not None:
        return safe_int(payload_revision, default=-1) == safe_int(report_revision, default=-2)
    for key in ("provider_block_id", "proposal_block_id"):
        payload_id = str(payload.get(key) or "").strip()
        report_id = str(report.get(key) or "").strip()
        if payload_id and report_id:
            return payload_id == report_id
    return False


def _provider_native_tool_result_valid(payload: dict[str, Any], report: dict[str, Any]) -> bool:
    if str(payload.get("tool") or "") == "generic_write":
        return False
    if not payload.get("provider_native_tool_call"):
        return False
    if safe_int(report.get("native_tool_call_count"), default=0) <= 0:
        return False
    if not _same_gpu1_revision(payload, report):
        return False
    for key in ("provider_block_id", "proposal_block_id"):
        payload_id = str(payload.get(key) or "").strip()
        report_id = str(report.get(key) or "").strip()
        if report_id and payload_id != report_id:
            return False
    return broker_result_passed(payload)
