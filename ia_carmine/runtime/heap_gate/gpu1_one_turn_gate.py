"""Production GPU1 one-turn runtime gate.

This module is runtime-owned. It must not import validation/preflight runners.
"""

from __future__ import annotations

from ia_carmine._shared.file_backed_transport import artifact_ref
from ia_carmine._shared.provider_tool_schemas import is_api_native_tool_call
from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
from ia_carmine.runtime.heap_gate.final_product_delta_protocol import (
    final_product_delta_runtime_classification,
    final_product_protocol,
)
from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import (
    gpu1_tool_result_consumption_state,
)
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    json,
    read_json,
    repo_rel,
    safe_int,
    write_json_report,
)
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    provider_native_tool_request_id,
)


GATE_KIND = "gpu1_one_turn_runtime_gate"

ONE_TURN_SUMMARY_FIELDS = (
    "gpu1_one_turn_runtime_gate_path",
    "gpu1_one_turn_runtime_gate_present",
    "gpu1_one_turn_runtime_gate_passed",
    "gpu1_one_turn_native_tool_call_count",
    "gpu1_one_turn_broker_request_count",
    "gpu1_one_turn_broker_result_count",
    "gpu1_one_turn_broker_result_passed_count",
    "gpu1_one_turn_role_tool_reinjected",
    "gpu1_one_turn_tool_result_consumed",
    "gpu1_one_turn_final_product_protocol_valid",
    "gpu1_one_turn_operator_delta_valid",
    "gpu1_one_turn_final_product_delta_valid",
    "gpu1_one_turn_blocker",
    "gpu1_one_turn_errors",
)


def build_gpu1_one_turn_runtime_gate(
    gate: Any,
    *,
    revision: int,
    final_report: dict[str, Any],
    subturn_reports: list[dict[str, Any]],
    events: list[dict[str, Any]],
    history_path: Path,
    output_path: Path,
) -> dict[str, Any]:
    """Build and write the production one-turn gate report."""
    final_report = final_report if isinstance(final_report, dict) else {}
    selected_reports = [
        item
        for item in subturn_reports
        if isinstance(item, dict)
        and str(item.get("lane") or "") == "gpu1_planner"
        and safe_int(item.get("revision"), default=0) == int(revision)
    ]
    if final_report and final_report not in selected_reports:
        selected_reports.append(final_report)

    turn0_report, native_calls, textual_call_seen = _first_native_tool_turn(
        selected_reports
    )
    turn0_subturn = safe_int(turn0_report.get("gpu1_tool_loop_subturn"), default=-1)
    request_ids = _request_ids_for_calls(gate, turn0_report, native_calls)
    broker_requests = _matching_broker_requests(
        events, revision=revision, subturn=turn0_subturn, request_ids=request_ids
    )
    broker_results = _matching_broker_results(gate, events, request_ids)
    broker_results_passed = [
        item
        for item in broker_results
        if broker_result_passed(item, repo_root=getattr(gate, "repo_root", None))
    ]

    response_text = _provider_response_text(gate, final_report)
    protocol = final_product_protocol(response_text)
    consumption = gpu1_tool_result_consumption_state(
        gate,
        events,
        response_text=response_text,
        report=final_report,
    )
    runtime_delta = final_product_delta_runtime_classification(
        response_text,
        protocol=protocol,
        consumption=consumption,
    )
    operator_delta = _operator_delta_contract(protocol, runtime_delta)
    role_tool_reinjected = _role_tool_reinjected(history_path, request_ids)
    errors: list[str] = []
    if not selected_reports:
        errors.append("gpu1_one_turn_runtime_gate_missing")
    if textual_call_seen and not native_calls:
        errors.append("gpu1_one_turn_textual_tool_call_not_executable")
    if not native_calls:
        errors.append("gpu1_one_turn_native_tool_call_missing")
    if native_calls and not broker_requests:
        errors.append("gpu1_one_turn_broker_request_missing")
    if native_calls and not broker_results:
        errors.append("gpu1_one_turn_broker_result_missing")
    if native_calls and not broker_results_passed:
        errors.append("gpu1_one_turn_broker_result_missing")
    if native_calls and not role_tool_reinjected:
        errors.append("gpu1_one_turn_role_tool_reinjection_missing")
    if broker_results_passed and consumption.get("tool_result_consumed_by_gpu1") is not True:
        errors.append("gpu1_one_turn_tool_result_not_consumed")
    if not protocol.get("passed"):
        errors.append("gpu1_one_turn_final_product_protocol_invalid")
    if not str(protocol.get("delta") or "").strip():
        errors.append("gpu1_one_turn_final_product_delta_empty")
    if operator_delta.get("operator_delta_valid") is not True:
        errors.append("gpu1_one_turn_operator_delta_invalid")

    errors = list(dict.fromkeys(errors))
    passed = bool(
        native_calls
        and broker_results_passed
        and role_tool_reinjected
        and consumption.get("tool_result_consumed_by_gpu1") is True
        and protocol.get("passed") is True
        and operator_delta.get("operator_delta_valid") is True
        and not errors
    )
    report = {
        "schema_version": 1,
        "kind": GATE_KIND,
        "revision": revision,
        "passed": passed,
        "provider_execution_performed": bool(
            final_report.get("provider_execution_performed")
            or final_report.get("provider_work_verified")
            or response_text
        ),
        "gpu1_turn0_provider_performed": bool(turn0_report),
        "gpu1_turn0_native_tool_call_count": len(native_calls),
        "broker_request_count": len(broker_requests),
        "broker_result_count": len(broker_results),
        "broker_result_passed_count": len(broker_results_passed),
        "role_tool_reinjected": role_tool_reinjected,
        "gpu1_turn1_provider_performed": bool(final_report and response_text),
        "tool_result_consumed_by_gpu1": bool(
            consumption.get("tool_result_consumed_by_gpu1")
        ),
        "tool_result_consumed_by_gpu1_count": safe_int(
            consumption.get("tool_result_consumed_by_gpu1_count")
        ),
        "final_product_protocol_valid": bool(protocol.get("passed")),
        "operator_delta_valid": bool(operator_delta.get("operator_delta_valid")),
        "final_product_delta_valid": bool(
            protocol.get("passed") and operator_delta.get("operator_delta_valid")
        ),
        "gpu0_npu_started_before_gpu1_one_turn_closed": False,
        "gpu1_one_turn_blocker": errors[0] if errors else "",
        "blocker": errors[0] if errors else "",
        "errors": errors,
        "warnings": [],
        "native_tool_request_ids": request_ids,
        "broker_result_passed_ids": _unique(
            [
                str(item.get("request_id") or item.get("normalized_request_id") or "")
                for item in broker_results_passed
            ]
        ),
        "operator_delta_errors": operator_delta.get("operator_delta_errors", []),
        "operator_delta_classification": runtime_delta.get("classification", ""),
        "final_product_delta_runtime_classification": runtime_delta,
        "final_product_protocol": {key: value for key, value in protocol.items() if key != "delta"},
        "gpu1_tool_result_consumption": consumption,
        "tool_cycle_statuses": consumption.get("tool_cycle_statuses", []),
        "history_ref": artifact_ref(
            history_path,
            getattr(gate, "repo_root", None),
            kind="gpu1_native_tool_chat_history",
            producer="gpu1_one_turn_runtime_gate",
        ),
    }
    report.update(_summary_fields(report, output_path, getattr(gate, "repo_root", None)))
    write_json_report(report, output_path)
    return report


def one_turn_gate_summary(report: dict[str, Any], repo_root: Path | None = None) -> dict[str, Any]:
    report = report if isinstance(report, dict) else {}
    path = str(report.get("gpu1_one_turn_runtime_gate_path") or report.get("output") or "").strip()
    summary = {
        "gpu1_one_turn_runtime_gate_path": path,
        "gpu1_one_turn_runtime_gate_present": bool(report),
        "gpu1_one_turn_runtime_gate_passed": bool(report.get("passed")),
        "gpu1_one_turn_native_tool_call_count": safe_int(
            report.get("gpu1_turn0_native_tool_call_count")
            or report.get("gpu1_one_turn_native_tool_call_count")
        ),
        "gpu1_one_turn_broker_request_count": safe_int(
            report.get("broker_request_count")
            or report.get("gpu1_one_turn_broker_request_count")
        ),
        "gpu1_one_turn_broker_result_count": safe_int(
            report.get("broker_result_count")
            or report.get("gpu1_one_turn_broker_result_count")
        ),
        "gpu1_one_turn_broker_result_passed_count": safe_int(
            report.get("broker_result_passed_count")
            or report.get("gpu1_one_turn_broker_result_passed_count")
        ),
        "gpu1_one_turn_role_tool_reinjected": bool(
            report.get("role_tool_reinjected")
            or report.get("gpu1_one_turn_role_tool_reinjected")
        ),
        "gpu1_one_turn_tool_result_consumed": bool(
            report.get("tool_result_consumed_by_gpu1")
            or report.get("gpu1_one_turn_tool_result_consumed")
        ),
        "gpu1_one_turn_final_product_protocol_valid": bool(
            report.get("final_product_protocol_valid")
            or report.get("gpu1_one_turn_final_product_protocol_valid")
        ),
        "gpu1_one_turn_operator_delta_valid": bool(
            report.get("operator_delta_valid")
            or report.get("gpu1_one_turn_operator_delta_valid")
        ),
        "gpu1_one_turn_final_product_delta_valid": bool(
            report.get("final_product_delta_valid")
            or report.get("gpu1_one_turn_final_product_delta_valid")
        ),
        "gpu1_one_turn_blocker": str(
            report.get("gpu1_one_turn_blocker") or report.get("blocker") or ""
        ),
        "gpu1_one_turn_errors": [
            str(item) for item in (report.get("errors") or []) if str(item).strip()
        ],
    }
    if not summary["gpu1_one_turn_runtime_gate_path"] and report.get("path"):
        summary["gpu1_one_turn_runtime_gate_path"] = str(report.get("path"))
    if repo_root and summary["gpu1_one_turn_runtime_gate_path"]:
        summary["gpu1_one_turn_runtime_gate_path"] = repo_rel(
            repo_root, Path(summary["gpu1_one_turn_runtime_gate_path"])
        )
    return summary


def strict_one_turn_gate_passed(source: dict[str, Any]) -> bool:
    source = source if isinstance(source, dict) else {}
    errors = source.get("gpu1_one_turn_errors")
    if not isinstance(errors, list):
        errors = []
    return bool(
        source.get("gpu1_one_turn_runtime_gate_passed") is True
        and safe_int(source.get("gpu1_one_turn_native_tool_call_count")) > 0
        and safe_int(source.get("gpu1_one_turn_broker_request_count")) > 0
        and safe_int(source.get("gpu1_one_turn_broker_result_passed_count")) > 0
        and source.get("gpu1_one_turn_role_tool_reinjected") is True
        and source.get("gpu1_one_turn_tool_result_consumed") is True
        and source.get("gpu1_one_turn_final_product_delta_valid") is True
        and not errors
    )


def copy_one_turn_summary(source: dict[str, Any], target: dict[str, Any]) -> None:
    for key in ONE_TURN_SUMMARY_FIELDS:
        if key in source:
            target[key] = source.get(key)


def _summary_fields(report: dict[str, Any], output_path: Path, repo_root: Path | None) -> dict[str, Any]:
    report = dict(report)
    report["output"] = repo_rel(repo_root, output_path) if repo_root else str(output_path)
    return one_turn_gate_summary(report, repo_root)


def _first_native_tool_turn(
    reports: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], bool]:
    textual_seen = False
    for report in reports:
        calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
        lane = str(report.get("lane") or "gpu1_planner")
        model = str(report.get("selected_model") or report.get("model") or "")
        native_calls = [
            call
            for call in calls
            if isinstance(call, dict) and is_api_native_tool_call(call, lane=lane, model=model)
        ]
        textual_seen = textual_seen or bool(
            report.get("textual_tool_calls") or report.get("rejected_non_native_tool_calls")
        )
        textual_seen = textual_seen or bool(calls and not native_calls)
        if native_calls:
            return report, native_calls, textual_seen
    return {}, [], textual_seen


def _request_ids_for_calls(
    gate: Any, report: dict[str, Any], calls: list[dict[str, Any]]
) -> list[str]:
    values: list[str] = []
    for index, call in enumerate(calls, start=1):
        tool = str(call.get("tool") or "").strip()
        if not tool:
            continue
        values.append(
            provider_native_tool_request_id(
                str(getattr(gate, "stamp", "")),
                report,
                call,
                tool=tool,
                call_index=index,
            )
        )
    return _unique(values)


def _matching_broker_requests(
    events: list[dict[str, Any]],
    *,
    revision: int,
    subturn: int,
    request_ids: list[str],
) -> list[dict[str, Any]]:
    wanted = set(request_ids)
    results: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "broker_request":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        request_id = str(payload.get("request_id") or payload.get("id") or "").strip()
        if wanted and request_id not in wanted:
            continue
        if str(payload.get("lane") or "") != "gpu1_planner":
            continue
        if payload.get("provider_native_tool_call") is not True:
            continue
        if safe_int(payload.get("revision"), default=-1) != int(revision):
            continue
        if subturn >= 0 and safe_int(payload.get("gpu1_tool_loop_subturn"), default=-1) != subturn:
            continue
        results.append(payload)
    return results


def _matching_broker_results(
    gate: Any, events: list[dict[str, Any]], request_ids: list[str]
) -> list[dict[str, Any]]:
    wanted = set(request_ids)
    results: list[dict[str, Any]] = []
    for payload in gate.broker_results(events):
        request_id = str(
            payload.get("request_id") or payload.get("normalized_request_id") or ""
        ).strip()
        if wanted and request_id not in wanted:
            continue
        if payload.get("provider_native_tool_call") is not True:
            continue
        if str(payload.get("lane") or "") != "gpu1_planner":
            continue
        results.append(payload)
    return results


def _role_tool_reinjected(history_path: Path, request_ids: list[str]) -> bool:
    history = read_json(history_path)
    if not isinstance(history, list):
        try:
            history = json.loads(history_path.read_text(encoding="utf-8-sig"))
        except Exception:
            history = []
    if not isinstance(history, list):
        return False
    assistant_with_tool = False
    wanted = set(request_ids)
    for message in history:
        if not isinstance(message, dict):
            continue
        if message.get("role") == "assistant" and message.get("tool_calls"):
            assistant_with_tool = True
            continue
        if not assistant_with_tool or message.get("role") != "tool":
            continue
        if not wanted:
            return True
        content = str(message.get("content") or "")
        if any(request_id and request_id in content for request_id in wanted):
            return True
    return False


def _provider_response_text(gate: Any, report: dict[str, Any]) -> str:
    if not report:
        return ""
    try:
        return str(gate.provider_report_response_text(report) or "")
    except Exception:
        return str(report.get("response_text_tail") or report.get("text_preview") or "")


def _operator_delta_contract(
    protocol: dict[str, Any],
    runtime_delta: dict[str, Any] | None = None,
) -> dict[str, Any]:
    delta = str(protocol.get("delta") or "").strip()
    errors: list[str] = []
    lowered = delta.lower()
    blocked_phrases = (
        "tool loop has reached its soft stop",
        "tool loop has reached its subturn budget",
        "following findings have been made",
        "summary of the tool loop execution",
        "this final product provides a summary of the tool loop execution",
    )
    if any(phrase in lowered for phrase in blocked_phrases):
        errors.append("gpu1_delta_tool_loop_summary_not_operator_product")
    section_markers = (
        "toolchain probe",
        "runtime file window",
        "diagnostic tool failures",
        "next steps",
        "broker result",
    )
    marker_count = sum(1 for marker in section_markers if marker in lowered)
    concrete_markers = (
        "target_files",
        "target file",
        "implementation_changes",
        "validation_commands",
        "blocker",
        "patch",
        "fix",
        "correction",
    )
    if marker_count >= 3 and not any(marker in lowered for marker in concrete_markers):
        errors.append("gpu1_delta_tool_loop_summary_not_operator_product")
    if not delta:
        errors.append("gpu1_final_product_delta_missing")
    if isinstance(runtime_delta, dict):
        errors.extend(str(item) for item in runtime_delta.get("errors") or [])
    return {
        "operator_delta_valid": not errors,
        "operator_delta_errors": list(dict.fromkeys(errors)),
    }


def _unique(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        value = str(value or "").strip()
        if value and value not in out:
            out.append(value)
    return out
