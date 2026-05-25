"""GPU1 native tool result wait/consume state.

GPU1 can request broker tools, but the broker result is not product evidence
until a later GPU1 turn consumes it in CONSUMED_EVIDENCE.
"""

from __future__ import annotations

import json
import re
from typing import Any

from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
from ia_carmine.runtime.heap_gate.final_product_delta_protocol import section_body
from ia_carmine.runtime.heap_gate.runtime_common import safe_int


GPU1_LANE = "gpu1_planner"


def gpu1_tool_result_consumption_state(
    owner: Any,
    events: list[dict[str, Any]],
    *,
    response_text: str = "",
    report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    report = report if isinstance(report, dict) else {}
    if not response_text:
        response_text = _report_text(owner, report)
    requests = _records_for_report(_gpu1_native_tool_requests(events), report)
    results = _records_for_report(_gpu1_native_tool_results(owner, events), report)
    request_ids = _unique([item["request_id"] for item in requests])
    result_ids = _unique([item["request_id"] for item in results])
    report_subturn = safe_int(report.get("gpu1_tool_loop_subturn"), default=-1)
    consumed = _consumed_results(response_text, results, report_subturn=report_subturn)
    consumed_ids = _unique([item["request_id"] for item in consumed])
    consumed_passed = [item for item in consumed if item.get("passed")]
    consumed_passed_ids = _unique([item["request_id"] for item in consumed_passed])
    consumed_failed = [item for item in consumed if not item.get("passed")]
    consumed_failed_ids = _unique([item["request_id"] for item in consumed_failed])
    diagnostic_failed = _diagnostic_failed_results(
        response_text,
        results,
        report_subturn=report_subturn,
    )
    diagnostic_failed_ids = _unique([item["request_id"] for item in diagnostic_failed])
    pending_ids = [item for item in request_ids if item not in result_ids]
    accounted_ids = _unique([*consumed_ids, *diagnostic_failed_ids])
    unconsumed_ids = [item for item in result_ids if item not in accounted_ids]
    first_pending = _first_by_id(requests, pending_ids) or _first_by_id(results, unconsumed_ids)
    blocker = ""
    if pending_ids:
        blocker = "gpu1_tool_result_pending"
    elif unconsumed_ids:
        blocker = "gpu1_requested_tool_result_not_consumed"
    return {
        "gpu1_waiting_for_tool_result": bool(pending_ids or unconsumed_ids),
        "gpu1_requested_tool_call_id": str((first_pending or {}).get("request_id") or ""),
        "gpu1_requested_tool_name": str((first_pending or {}).get("tool") or ""),
        "gpu1_resume_after_tool_result_required": bool(pending_ids or unconsumed_ids),
        "gpu1_consumed_tool_result_ids": consumed_ids,
        "gpu1_consumed_passed_tool_result_ids": consumed_passed_ids,
        "gpu1_requested_tool_call_ids": request_ids,
        "gpu1_tool_result_written_ids": result_ids,
        "gpu1_pending_tool_result_ids": pending_ids,
        "gpu1_tool_result_pending_ids": pending_ids,
        "gpu1_unconsumed_tool_result_ids": unconsumed_ids,
        "gpu1_tool_result_blocker": blocker,
        "tool_result_written": bool(result_ids),
        "tool_result_consumed_by_gpu1": bool(consumed_ids),
        "tool_result_written_count": len(result_ids),
        "tool_result_consumed_by_gpu1_count": len(consumed_ids),
        "tool_result_consumed_passed_by_gpu1_count": len(consumed_passed_ids),
        "tool_result_consumed_failed_by_gpu1_count": len(consumed_failed_ids),
        "gpu1_consumed_failed_tool_result_ids": consumed_failed_ids,
        "tool_result_diagnostic_failed_by_gpu1_count": len(diagnostic_failed_ids),
        "gpu1_diagnostic_failed_tool_result_ids": diagnostic_failed_ids,
        "consumer_text_has_consumed_evidence_section": bool(
            section_body(response_text, "CONSUMED_EVIDENCE").strip()
        ),
        "gpu1_tool_result_consumption": {
            "requested": requests,
            "results": results,
            "consumed": consumed,
            "consumed_passed": consumed_passed,
            "consumed_failed": consumed_failed,
            "diagnostic_failed": diagnostic_failed,
            "pending_ids": pending_ids,
            "unconsumed_ids": unconsumed_ids,
            "blocker": blocker,
        },
    }


def gpu1_tool_result_resume_prompt_block(owner: Any, events: list[dict[str, Any]]) -> str:
    state = gpu1_tool_result_consumption_state(owner, events)
    results = state.get("gpu1_tool_result_consumption", {}).get("results", [])
    if not state.get("gpu1_resume_after_tool_result_required"):
        return "GPU1_TOOL_RESULT_RESUME: nessun tool_result GPU1 pending."
    lines = [
        "GPU1_TOOL_RESULT_RESUME_REQUIRED:",
        "- Se hai chiesto un tool, devi consumare il tool_result nello stesso ruolo GPU1 prima di produrre un packet reviewable.",
        "- Cita gli id/ref sotto in CONSUMED_EVIDENCE/tool_or_matrix_refs.",
        "- GPU0/NPU aspettano finche' questo consumo non e' avvenuto.",
        f"- blocker={state.get('gpu1_tool_result_blocker') or 'none'}",
        f"- pending_request_ids={','.join(state.get('gpu1_pending_tool_result_ids') or [])}",
        f"- unconsumed_result_ids={','.join(state.get('gpu1_unconsumed_tool_result_ids') or [])}",
    ]
    for item in results[:12]:
        refs = ",".join(item.get("refs") or [])
        lines.append(
            f"- tool_result id={item.get('request_id')} tool={item.get('tool')} "
            f"rc={item.get('returncode')} refs={refs}"
        )
    return "\n".join(lines)


def _gpu1_native_tool_requests(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    requests: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "broker_request":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if payload.get("provider_native_tool_call") is not True:
            continue
        if str(payload.get("lane") or "") != GPU1_LANE:
            continue
        request_id = _request_id(payload)
        if not request_id:
            continue
        requests.append(
            {
                "request_id": request_id,
                "tool": str(payload.get("tool") or ""),
                "lane": GPU1_LANE,
                "payload_ref": payload.get("payload_ref") if isinstance(payload.get("payload_ref"), dict) else {},
                "provider_report": str(payload.get("provider_report") or ""),
                "provider_block_id": str(payload.get("provider_block_id") or ""),
                "proposal_block_id": str(payload.get("proposal_block_id") or ""),
                "revision": payload.get("revision"),
                "gpu1_tool_loop_subturn": safe_int(payload.get("gpu1_tool_loop_subturn"), default=-1),
                "tool_call_id": str(payload.get("tool_call_id") or ""),
                "tool_call_index": payload.get("tool_call_index"),
                "chat_history_ref": payload.get("chat_history_ref") if isinstance(payload.get("chat_history_ref"), dict) else {},
            }
        )
    return _dedupe_records(requests)


def _gpu1_native_tool_results(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for payload in owner.broker_results(events):
        if payload.get("provider_native_tool_call") is not True:
            continue
        if str(payload.get("lane") or "") != GPU1_LANE:
            continue
        request_id = _request_id(payload)
        if not request_id:
            continue
        refs = _result_refs(payload)
        results.append(
            {
                "request_id": request_id,
                "tool": str(payload.get("tool") or ""),
                "lane": GPU1_LANE,
                "returncode": safe_int(payload.get("returncode"), default=1),
                "passed": broker_result_passed(
                    payload,
                    repo_root=getattr(owner, "repo_root", None),
                ),
                "refs": refs,
                "outputs": payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {},
                "provider_report": str(payload.get("provider_report") or ""),
                "provider_block_id": str(payload.get("provider_block_id") or ""),
                "proposal_block_id": str(payload.get("proposal_block_id") or ""),
                "revision": payload.get("revision"),
                "gpu1_tool_loop_subturn": safe_int(payload.get("gpu1_tool_loop_subturn"), default=-1),
                "tool_call_id": str(payload.get("tool_call_id") or ""),
                "tool_call_index": payload.get("tool_call_index"),
                "chat_history_ref": payload.get("chat_history_ref") if isinstance(payload.get("chat_history_ref"), dict) else {},
            }
        )
    return _dedupe_records(results)


def _consumed_results(
    response_text: str,
    results: list[dict[str, Any]],
    *,
    report_subturn: int,
) -> list[dict[str, Any]]:
    consumed_text = _consumed_evidence_text(response_text).lower()
    if not consumed_text:
        return []
    consumed: list[dict[str, Any]] = []
    for result in results:
        result_subturn = safe_int(result.get("gpu1_tool_loop_subturn"), default=-1)
        if report_subturn >= 0 and result_subturn >= report_subturn:
            continue
        refs = [str(result.get("request_id") or ""), *[str(item) for item in result.get("refs", [])]]
        if any(ref and ref.lower() in consumed_text for ref in refs):
            consumed.append(result)
    return consumed


def _diagnostic_failed_results(
    response_text: str,
    results: list[dict[str, Any]],
    *,
    report_subturn: int,
) -> list[dict[str, Any]]:
    diagnostic_text = _diagnostic_tool_failure_text(response_text).lower()
    if not diagnostic_text:
        return []
    accounted: list[dict[str, Any]] = []
    for result in results:
        if result.get("passed"):
            continue
        result_subturn = safe_int(result.get("gpu1_tool_loop_subturn"), default=-1)
        if report_subturn >= 0 and result_subturn >= report_subturn:
            continue
        refs = [str(result.get("request_id") or ""), *[str(item) for item in result.get("refs", [])]]
        if any(ref and ref.lower() in diagnostic_text for ref in refs):
            accounted.append(result)
    return accounted


def _consumed_evidence_text(response_text: str) -> str:
    section = section_body(response_text, "CONSUMED_EVIDENCE").strip()
    if section:
        return section
    payload = _json_payload(response_text)
    value = payload.get("CONSUMED_EVIDENCE") if isinstance(payload, dict) else None
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value or "")


def _diagnostic_tool_failure_text(response_text: str) -> str:
    sections = [
        section_body(response_text, "DIAGNOSTIC_TOOL_FAILURES").strip(),
        section_body(response_text, "FINAL_PRODUCT_DELTA").strip(),
    ]
    text = "\n".join(section for section in sections if section)
    if text:
        return text
    payload = _json_payload(response_text)
    value = payload.get("DIAGNOSTIC_TOOL_FAILURES") if isinstance(payload, dict) else None
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value or "")


def _json_payload(response_text: str) -> dict[str, Any]:
    text = (response_text or "").strip()
    fence = re.fullmatch(r"(?is)```(?:json)?\s*(.*?)\s*```", text)
    if fence:
        text = fence.group(1).strip()
    try:
        value = json.loads(text)
    except Exception:
        return {}
    return value if isinstance(value, dict) else {}


def _result_refs(payload: dict[str, Any]) -> list[str]:
    outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
    refs = [
        str(payload.get("request_id") or ""),
        str(payload.get("normalized_request_id") or ""),
        str(payload.get("id") or ""),
        str(payload.get("broker_report") or ""),
    ]
    for key in (
        "json_report",
        "markdown_report",
        "evidence_json",
        "evidence_markdown",
        "debug_lab_report",
        "debug_lab_markdown",
        "stdout_path",
        "stderr_path",
    ):
        value = str(outputs.get(key) or "")
        if value:
            refs.append(value)
    return _unique(refs)


def _request_id(payload: dict[str, Any]) -> str:
    return str(
        payload.get("request_id")
        or payload.get("id")
        or payload.get("normalized_request_id")
        or ""
    ).strip()


def _report_text(owner: Any, report: dict[str, Any]) -> str:
    if not report:
        return ""
    try:
        return str(owner.provider_report_response_text(report) or "")
    except Exception:
        return ""


def _records_for_report(items: list[dict[str, Any]], report: dict[str, Any]) -> list[dict[str, Any]]:
    if not report:
        return items
    return [item for item in items if _same_gpu1_loop(item, report)]


def _same_gpu1_loop(item: dict[str, Any], report: dict[str, Any]) -> bool:
    report_revision = report.get("revision")
    item_revision = item.get("revision")
    if report_revision is not None and item_revision is not None:
        if safe_int(item_revision, default=-1) != safe_int(report_revision, default=-2):
            return False

    report_history = _ref_path(report.get("chat_history_ref"))
    item_history = _ref_path(item.get("chat_history_ref"))
    if report_history and item_history and report_history != item_history:
        return False

    return True


def _ref_path(value: Any) -> str:
    if isinstance(value, dict):
        return str(value.get("path") or value.get("ref_id") or "").strip().lower()
    return ""


def _first_by_id(items: list[dict[str, Any]], ids: list[str]) -> dict[str, Any]:
    wanted = set(ids)
    for item in items:
        if item.get("request_id") in wanted:
            return item
    return {}


def _dedupe_records(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        key = str(item.get("request_id") or "")
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(item)
    return out


def _unique(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in out:
            out.append(value)
    return out
