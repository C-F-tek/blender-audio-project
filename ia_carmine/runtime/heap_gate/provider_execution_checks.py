"""Provider execution evidence checks kept out of the provider runner."""

from __future__ import annotations

from ia_carmine._shared.provider_work_rejections import looks_like_handshake, normalize_bool
from ia_carmine.runtime.heap_gate.generic_write_followup import failed_generic_write_results
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, safe_int


def gpu1_primary_workload_status(report: dict[str, Any]) -> dict[str, Any]:
    response_text = str(report.get("response_text") or "").strip()
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
    native_passed = [
        payload
        for event in events
        if event.get("event_type") == "broker_result"
        for payload in [event.get("payload") if isinstance(event.get("payload"), dict) else {}]
        if _provider_native_tool_result_valid(payload, report)
    ]
    source = "native_tool_result" if native_passed else ""
    return {
        "gpu1_primary_evidence_valid": bool(source),
        "gpu1_primary_evidence_source": source,
        "leader_source": source or "none",
        "gpu1_generic_write_capture_valid": False,
        "gpu1_generic_write_capture_failed": bool(generic_failed),
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


def _broker_result_passed(payload: dict[str, Any]) -> bool:
    errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
    summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
    returncode = payload.get("returncode")
    executed = payload.get("executed")
    execution_ok = (
        (returncode is not None and safe_int(returncode, default=1) == 0)
        or executed is True
    )
    return bool(
        not payload.get("blocked")
        and not errors
        and execution_ok
        and summary.get("passed") is not False
    )


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
    return _broker_result_passed(payload)
