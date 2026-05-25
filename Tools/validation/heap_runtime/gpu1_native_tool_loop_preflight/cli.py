#!/usr/bin/env python3
"""Live preflight for GPU1 prompt -> native tool -> broker -> resume."""

from __future__ import annotations

import argparse, json, sys
from datetime import datetime
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[4]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from ia_carmine._shared.file_backed_transport import (
    artifact_ref,
    read_text_windows_safe,
    report_text_preview,
    write_text_artifact,
)
from ia_carmine._shared.provider_ollama_probe import run_ollama_probe
from ia_carmine.runtime.heap_gate.final_product_delta_protocol import final_product_protocol
from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed
from ia_carmine.runtime.heap_gate.gpu1_tool_result_messages import gpu1_tool_result_payload, gpu1_tool_result_text
from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import (
    gpu1_tool_result_consumption_state,
)
from ia_carmine.runtime.runtime_tool.broker.executor import build_report
from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.context import DEFAULT_MEMORY_QUERY, build_preflight_prompt, native_tool_required_retry_message, startup_context, tool_loop_soft_stop_message
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.export import export_documents_copy
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.invalid_delta import invalid_delta_text
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.operator_delta import invalid_operator_delta_text, operator_delta_report
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.readable import assistant_after_tool, render_delta_readable
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.review import run_delta_review_tool
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.tool_policy import normalize_tool_args, tool_argument_errors

GPU1_LANE = "gpu1_planner"

def _json_write(payload: Any, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
def _load_operator_prompt(args: argparse.Namespace, repo_root: Path) -> str:
    prompt_file = str(getattr(args, "operator_prompt_file", "") or "").strip()
    if prompt_file:
        path = Path(prompt_file)
        if not path.is_absolute():
            path = repo_root / path
        return read_text_windows_safe(path)
    return str(getattr(args, "operator_prompt", "") or "")

def _operator_prompt_ref(args: argparse.Namespace, repo_root: Path) -> dict[str, Any]:
    prompt_file = str(getattr(args, "operator_prompt_file", "") or "").strip()
    if not prompt_file:
        return {}
    path = Path(prompt_file)
    if not path.is_absolute():
        path = repo_root / path
    return artifact_ref(path, repo_root, kind="operator_prompt")

def _assistant_history_message(report: dict[str, Any]) -> dict[str, Any]:
    message = report.get("assistant_message") if isinstance(report.get("assistant_message"), dict) else {}
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    if message:
        out = {key: value for key, value in message.items() if key in {"role", "content", "tool_calls"}}
        if calls and not out.get("tool_calls"):
            out["tool_calls"] = calls
        if calls or out.get("tool_calls"):
            out["content"] = ""
        return out
    if calls:
        return {"role": "assistant", "content": "", "tool_calls": calls}
    return {"role": "assistant", "content": str(report.get("response_text") or "")}

def _tool_result_message(repo_root: Path, result: dict[str, Any], tool_call_id: str) -> dict[str, Any]:
    payload = gpu1_tool_result_payload(repo_root, result, tool_call_id=tool_call_id)
    return {
        "role": "tool",
        "tool_name": str(result.get("tool") or ""),
        "content": gpu1_tool_result_text(payload),
    }

def _broker_args(
    repo_root: Path,
    request_file: Path,
    tool_output_dir: Path,
    broker_output: Path,
    stamp: str,
    timeout_seconds: int,
) -> argparse.Namespace:
    return argparse.Namespace(
        repo_root=str(repo_root),
        request_file=str(request_file),
        request_json="",
        payload_file="",
        job_id=stamp,
        tool_output_dir=str(tool_output_dir),
        stamp=stamp,
        timeout_seconds=timeout_seconds,
        dry_run=False,
        output=str(broker_output),
        markdown_output=str(broker_output.with_suffix(".md")),
    )
class _ConsumptionOwner:
    def __init__(self, repo_root: Path, results: list[dict[str, Any]]) -> None:
        self.repo_root = repo_root
        self._results = results

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            event.get("payload")
            for event in events
            if event.get("event_type") == "broker_result" and isinstance(event.get("payload"), dict)
        ] or self._results

    def provider_report_response_text(self, report: dict[str, Any]) -> str:
        return str(report.get("response_text") or "")
def _has_history_shape(history: list[dict[str, Any]]) -> bool:
    assistant_tool = any(
        item.get("role") == "assistant" and isinstance(item.get("tool_calls"), list) and item.get("tool_calls")
        for item in history
    )
    tool_message = any(item.get("role") == "tool" for item in history)
    assistant_after_tool = False
    seen_tool = False
    for item in history:
        if item.get("role") == "tool":
            seen_tool = True
        elif seen_tool and item.get("role") == "assistant":
            assistant_after_tool = True
            break
    return bool(assistant_tool and tool_message and assistant_after_tool)
def _assistant_after_tool(history: list[dict[str, Any]]) -> dict[str, Any]:
    return assistant_after_tool(history)
def _tool_calls(report: dict[str, Any]) -> list[dict[str, Any]]:
    calls = report.get("tool_calls") if isinstance(report.get("tool_calls"), list) else []
    return [item for item in calls if isinstance(item, dict) and str(item.get("tool") or "")]
def _run(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    output = resolve_output_path(repo_root, args.output)
    work_dir = output.parent / "gpu1_native_tool_loop_preflight"
    work_dir.mkdir(parents=True, exist_ok=True)
    stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S"); args.stamp = stamp
    history_path = work_dir / "gpu1_chat_history.json"
    args.operator_prompt = _load_operator_prompt(args, repo_root)
    startup = startup_context(args, repo_root, work_dir, stamp)
    args.startup_context = startup
    args.repo_root = str(repo_root)
    prompt = build_preflight_prompt(
        startup,
        args.operator_prompt,
        args.max_subturns,
        args.model,
        _operator_prompt_ref(args, repo_root),
    )
    history: list[dict[str, Any]] = [{"role": "user", "content": prompt}]
    _json_write(history, history_path)
    history_ref = artifact_ref(history_path, repo_root, kind="gpu1_native_tool_chat_history")
    errors: list[str] = []
    warnings: list[str] = []

    reports: list[dict[str, Any]] = []
    report_paths: list[Path] = []
    broker_reports: list[dict[str, Any]] = []
    broker_report_paths: list[Path] = []
    all_results: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    final_report: dict[str, Any] = {}
    final_report_path = work_dir / "gpu1_subturn_final_report.json"
    final_subturn = -1

    for subturn in range(max(1, int(args.max_subturns))):
        subturn_output = work_dir / f"gpu1_subturn{subturn}_report.json"
        report = run_ollama_probe(
            repo_root=repo_root,
            model=args.model,
            messages=history,
            max_new_tokens=args.max_new_tokens,
            num_ctx=args.num_ctx,
            keep_alive=args.keep_alive,
            partial_output=subturn_output,
            require_gpu_residency=False,
            base_url=args.base_url,
            unload_model=False,
            chat_history_ref=history_ref,
            gpu1_tool_loop_subturn=subturn,
        )
        write_json_report(report, subturn_output)
        reports.append(report)
        report_paths.append(subturn_output)
        history.append(_assistant_history_message(report))
        calls = _tool_calls(report)
        if not calls:
            candidate_text = str(report_text_preview(repo_root, report).get("text") or "")
            candidate_protocol = final_product_protocol(candidate_text)
            candidate_consumption = gpu1_tool_result_consumption_state(
                _ConsumptionOwner(repo_root, all_results),
                events,
                response_text=candidate_text,
                report={**report, "revision": 0, "gpu1_tool_loop_subturn": subturn},
            )
            if (
                all_results
                and candidate_protocol.get("passed")
                and int(candidate_consumption.get("tool_result_consumed_passed_by_gpu1_count") or 0) > 0
            ):
                final_report = report
                final_report_path = subturn_output
                final_subturn = subturn
                break
            if all_results and report.get("provider_textual_tool_call_not_executable"):
                final_report = report
                final_report_path = subturn_output
                final_subturn = subturn
                break
            if subturn + 1 < max(1, int(args.max_subturns)):
                history.append(native_tool_required_retry_message(candidate_text, subturn, startup, args.model))
                _json_write(history, history_path)
                continue
            final_report = report
            final_report_path = subturn_output
            final_subturn = subturn
            break

        requests: list[dict[str, Any]] = []
        for index, call in enumerate(calls, start=1):
            tool = str(call.get("tool") or "")
            call_id = str(call.get("id") or f"gpu1_preflight_tool_call_{subturn}_{index}")
            raw_args = call.get("args") if isinstance(call.get("args"), dict) else {}
            normalized_args = normalize_tool_args(
                tool,
                raw_args,
                runtime_args=args,
                provider_report=subturn_output,
                broker_report_paths=broker_report_paths,
            )
            argument_errors = tool_argument_errors(tool, normalized_args)
            request_id = f"gpu1_preflight_{stamp}_subturn{subturn}_call{index:03d}_{tool}"
            requests.append(
                {
                    "id": request_id,
                    "request_id": request_id,
                    "tool": tool,
                    "args": normalized_args,
                    "source": "gpu1_native_tool_loop_preflight",
                    "lane": GPU1_LANE,
                    "provider_native_tool_call": True,
                    "provider_report": str(subturn_output),
                    "provider_block_id": f"{stamp}:gpu1_preflight:{subturn:03d}",
                    "revision": 0,
                    "gpu1_tool_loop_subturn": subturn,
                    "tool_call_id": call_id,
                    "tool_call_index": index,
                    "argument_errors": argument_errors,
                    "chat_history_ref": history_ref,
                }
            )
        packet = {
            "schema_version": 1,
            "kind": "agent_runtime_tool_requests",
            "source": "gpu1_native_tool_loop_preflight",
            "tool_requests": requests,
        }
        request_file = work_dir / f"broker_request_packet_subturn{subturn}.json"
        broker_output = work_dir / f"broker_report_subturn{subturn}.json"
        _json_write(packet, request_file)
        broker = build_report(
            _broker_args(
                repo_root,
                request_file,
                work_dir / "broker_tools",
                broker_output,
                f"{stamp}_subturn{subturn}",
                args.timeout_seconds,
            )
        )
        write_json_report(broker, broker_output)
        broker_reports.append(broker)
        broker_report_paths.append(broker_output)
        results = broker.get("tool_results") if isinstance(broker.get("tool_results"), list) else []
        for index, request in enumerate(requests):
            result = results[index] if index < len(results) and isinstance(results[index], dict) else {}
            result.update(
                {
                    "request_id": request["request_id"],
                    "normalized_request_id": request["request_id"],
                    "provider_native_tool_call": True,
                    "lane": GPU1_LANE,
                    "provider_report": str(subturn_output),
                    "provider_block_id": request["provider_block_id"],
                    "revision": 0,
                    "gpu1_tool_loop_subturn": subturn,
                    "tool_call_id": request["tool_call_id"],
                    "tool_call_index": request["tool_call_index"],
                    "chat_history_ref": history_ref,
                    "broker_report": str(broker_output),
                }
            )
            if request.get("argument_errors"):
                result["returncode"] = 2
                result["errors"] = [
                    *[str(item) for item in result.get("errors", []) if item],
                    *[str(item) for item in request.get("argument_errors", [])],
                ]
            events.extend(
                [
                    {"event_type": "broker_request", "payload": request},
                    {"event_type": "broker_result", "payload": result},
                ]
            )
            all_results.append(result)
            history.append(_tool_result_message(repo_root, result, str(request["tool_call_id"])))
        _json_write(history, history_path)
    else:
        warnings.append("gpu1_tool_budget_exhausted_soft_stop_finalization")

    final_report_text = str(report_text_preview(repo_root, final_report).get("text") or "") if final_report else ""
    final_report_protocol = final_product_protocol(final_report_text) if final_report else {}
    if all_results and (
        not final_report
        or _tool_calls(final_report)
        or final_report.get("provider_textual_tool_call_not_executable")
        or final_report_protocol.get("passed") is not True
    ):
        passed_ids = [
            str(item.get("request_id") or "")
            for item in all_results
            if broker_result_passed(item, repo_root=repo_root)
        ]
        failed_ids = [
            str(item.get("request_id") or "")
            for item in all_results
            if not broker_result_passed(item, repo_root=repo_root)
        ]
        final_subturn = max(1, int(args.max_subturns))
        history.append(
            tool_loop_soft_stop_message(
                subturn=final_subturn,
                max_subturns=max(1, int(args.max_subturns)),
                consumed_ids=passed_ids,
                failed_ids=failed_ids,
                model=args.model,
            )
        )
        _json_write(history, history_path)
        final_report_path = work_dir / f"gpu1_subturn{final_subturn}_finalize_report.json"
        final_report = run_ollama_probe(
            repo_root=repo_root,
            model=args.model,
            messages=history,
            max_new_tokens=args.max_new_tokens,
            num_ctx=args.num_ctx,
            keep_alive=args.keep_alive,
            partial_output=final_report_path,
            require_gpu_residency=False,
            base_url=args.base_url,
            unload_model=False,
            chat_history_ref=history_ref,
            gpu1_tool_loop_subturn=final_subturn,
            native_tool_chat_tools_enabled=False,
        )
        write_json_report(final_report, final_report_path)
        reports.append(final_report)
        report_paths.append(final_report_path)
        history.append(_assistant_history_message(final_report))
        _json_write(history, history_path)
    elif final_report and history and history[-1].get("role") != "assistant":
        history.append(_assistant_history_message(final_report))
        _json_write(history, history_path)

    if not all_results:
        errors.append("provider_native_tool_call_required_unmet")
    if any(report.get("provider_textual_tool_call_not_executable") for report in reports):
        errors.append("provider_textual_tool_call_not_executable")

    final_text = str(report_text_preview(repo_root, final_report).get("text") or "")
    protocol = final_product_protocol(final_text)
    consumption = gpu1_tool_result_consumption_state(
        _ConsumptionOwner(repo_root, all_results),
        events,
        response_text=final_text,
        report={
            **final_report,
            "revision": 0,
            "gpu1_tool_loop_subturn": final_subturn,
            "chat_history_ref": history_ref,
        },
    )
    combined_broker = {
        "passed": bool(broker_reports and any(item.get("passed") for item in broker_reports)),
        "all_tool_reports_passed": bool(broker_reports and all(item.get("passed") for item in broker_reports)),
        "failed_tool_report_count": sum(1 for item in broker_reports if not item.get("passed")),
        "tool_request_count": sum(int(item.get("tool_request_count") or 0) for item in broker_reports),
        "tool_execution_count": sum(int(item.get("tool_execution_count") or 0) for item in broker_reports),
        "tool_result_written_count": len(all_results),
        "tool_result_passed_count": sum(
            1 for item in all_results if broker_result_passed(item, repo_root=repo_root)
        ),
        "tool_result_failed_count": sum(
            1 for item in all_results if not broker_result_passed(item, repo_root=repo_root)
        ),
        "broker_report_refs": [
            artifact_ref(path, repo_root, kind="gpu1_native_tool_broker_report")
            for path in broker_report_paths
        ],
    }
    combined_broker_path = work_dir / "broker_report.json"
    write_json_report(combined_broker, combined_broker_path)
    delta_review: dict[str, Any] = {}
    if broker_reports and not combined_broker.get("passed"):
        errors.append("broker_tool_call_failed")
    if not consumption.get("tool_result_consumed_by_gpu1"):
        errors.append("gpu1_requested_tool_result_not_consumed")
    if consumption.get("gpu1_unconsumed_tool_result_ids"):
        errors.append("gpu1_requested_tool_result_not_consumed")
    if int(consumption.get("tool_result_consumed_failed_by_gpu1_count") or 0) > 0:
        errors.append("gpu1_consumed_failed_tool_result_as_final_product_evidence")
    if not protocol.get("passed"):
        missing_delta = invalid_delta_text(
            final_text=final_text,
            final_report_path=final_report_path,
            protocol=protocol,
            unconsumed_ids=consumption.get("gpu1_unconsumed_tool_result_ids", []),
        )
        delta_ref = write_text_artifact(repo_root, work_dir / "delta_review", name="gpu1_final_product_delta", text=missing_delta, kind="gpu1_final_product_delta_missing_or_invalid", producer="gpu1_native_tool_loop_preflight", suffix=".md")
        delta_review = {"passed": False, "delta_ref": delta_ref, "invalid": True}
        errors.extend(str(item) for item in protocol.get("errors", []))
    else:
        operator_delta = operator_delta_report(protocol, response_text=final_text)
        if not operator_delta.get("passed"):
            operator_errors = [str(item) for item in operator_delta.get("errors", []) if item]
            errors.extend(operator_errors)
            delta_ref = write_text_artifact(
                repo_root,
                work_dir / "delta_review",
                name="gpu1_final_product_delta",
                text=invalid_operator_delta_text(
                    delta=str(protocol.get("delta") or ""),
                    errors=operator_errors,
                    protocol=protocol,
                    provider_report_path=str(final_report_path),
                ),
                kind="gpu1_final_product_delta_invalid_operator_product",
                producer="gpu1_native_tool_loop_preflight",
                suffix=".md",
            )
            delta_review = {
                "passed": False,
                "delta_ref": delta_ref,
                "invalid": True,
                "operator_delta_valid": False,
                "operator_delta_errors": operator_errors,
            }
        else:
            delta_review = run_delta_review_tool(
                repo_root=repo_root,
                work_dir=work_dir,
                stamp=stamp,
                request_id=str((all_results[-1] if all_results else {}).get("request_id") or f"gpu1_preflight_{stamp}"),
                delta_text=str(protocol.get("delta") or ""),
                provider_report=final_report_path,
                evidence_report=combined_broker_path,
                timeout_seconds=args.timeout_seconds,
            )
            if not delta_review.get("passed"):
                errors.append("gpu1_final_product_delta_review_tool_failed")
    return _report(
        args,
        repo_root,
        output,
        history_path,
        history,
        reports[0] if reports else {},
        combined_broker,
        final_report,
        {
            "protocol": protocol,
            "operator_delta": operator_delta_report(protocol, response_text=final_text),
            "consumption": consumption,
            "request_id": str((all_results[-1] if all_results else {}).get("request_id") or ""),
            "delta_review": delta_review,
            "startup_context": startup,
            "subturn_report_paths": report_paths,
            "subturn_reports": reports,
            "broker_report_paths": broker_report_paths,
            "final_subturn": final_subturn,
        },
        errors,
        warnings,
    )

def _report(
    args: argparse.Namespace,
    repo_root: Path,
    output: Path,
    history_path: Path,
    history: list[dict[str, Any]],
    subturn0: dict[str, Any],
    broker_report: dict[str, Any],
    subturn1: dict[str, Any],
    evidence: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    history_ref = artifact_ref(history_path, repo_root, kind="gpu1_native_tool_chat_history")
    consumption = evidence.get("consumption") if isinstance(evidence.get("consumption"), dict) else {}
    protocol = evidence.get("protocol") if isinstance(evidence.get("protocol"), dict) else {}
    operator_delta = evidence.get("operator_delta") if isinstance(evidence.get("operator_delta"), dict) else {}
    delta_review = evidence.get("delta_review") if isinstance(evidence.get("delta_review"), dict) else {}
    startup = evidence.get("startup_context") if isinstance(evidence.get("startup_context"), dict) else {}
    startup_refs = startup.get("refs") if isinstance(startup.get("refs"), dict) else {}
    subturn_report_paths = [
        path for path in evidence.get("subturn_report_paths", []) if isinstance(path, Path)
    ]
    broker_report_paths = [
        path for path in evidence.get("broker_report_paths", []) if isinstance(path, Path)
    ]
    subturn_reports = [
        report for report in evidence.get("subturn_reports", []) if isinstance(report, dict)
    ] or [item for item in (subturn0, subturn1) if isinstance(item, dict) and item]
    total_native_tool_calls = sum(
        int(report.get("native_tool_call_count") or 0) for report in subturn_reports
    )
    provider_textual_tool_call_not_executable = any(
        bool(report.get("provider_textual_tool_call_not_executable")) for report in subturn_reports
    )
    final_native_tool_calls = int(subturn1.get("native_tool_call_count") or 0) if subturn1 else 0
    operator_delta_valid = bool(operator_delta.get("passed"))
    tool_loop_closed = bool(
        subturn1
        and final_native_tool_calls == 0
        and operator_delta_valid
        and not consumption.get("gpu1_waiting_for_tool_result")
        and not consumption.get("gpu1_unconsumed_tool_result_ids")
    )
    assistant_text_ref = write_text_artifact(
        repo_root,
        output.parent / "gpu1_native_tool_loop_preflight",
        name="gpu1_text_after_tool_result",
        text=str(_assistant_after_tool(history).get("content") or ""),
        kind="gpu1_text_after_consumed_tool_result",
        producer="gpu1_native_tool_loop_preflight",
        suffix=".md",
    )
    readable_path = output.parent / "gpu1_native_tool_loop_preflight" / "gpu1_delta_readable.md"
    readable_text = render_delta_readable(
        request_id=str(evidence.get("request_id") or ""),
        history=history,
        protocol=protocol,
        operator_delta=operator_delta,
        consumption=consumption,
        delta_review=delta_review,
    )
    readable_path.parent.mkdir(parents=True, exist_ok=True)
    readable_path.write_text(readable_text, encoding="utf-8")
    passed = bool(
        not errors
        and total_native_tool_calls > 0
        and int(broker_report.get("tool_execution_count") or 0) > 0
        and consumption.get("tool_result_consumed_by_gpu1") is True
        and final_native_tool_calls == 0
        and operator_delta_valid
        and delta_review.get("passed") is True
        and _has_history_shape(history)
    )
    report = {
        "schema_version": 1,
        "kind": "gpu1_native_tool_loop_preflight",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "model": args.model,
        "base_url": args.base_url,
        "context_source": startup.get("context_source") or "",
        "startup_context_refs": startup_refs,
        "passed": passed,
        "provider_execution_performed": bool(subturn0 or subturn1),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "gpu0_npu_started_before_gpu1_tool_loop_closed": False,
        "native_tool_call_count": total_native_tool_calls,
        "provider_textual_tool_call_not_executable": provider_textual_tool_call_not_executable,
        "broker_request_count": int(broker_report.get("tool_request_count") or 0),
        "broker_result_count": int(broker_report.get("tool_execution_count") or 0),
        "broker_result_written_count": int(
            broker_report.get("tool_result_written_count")
            or broker_report.get("tool_execution_count")
            or 0
        ),
        "broker_result_passed_count": int(broker_report.get("tool_result_passed_count") or 0),
        "broker_result_failed_count": int(broker_report.get("tool_result_failed_count") or 0),
        "chat_history_ref": history_ref,
        "chat_history_message_count": len(history),
        "chat_history_has_assistant_tool_call_tool_and_resume": _has_history_shape(history),
        "tool_result_consumed_by_gpu1": bool(consumption.get("tool_result_consumed_by_gpu1")),
        "tool_result_consumed_passed_by_gpu1_count": int(
            consumption.get("tool_result_consumed_passed_by_gpu1_count") or 0
        ),
        "gpu1_tool_loop_closed": tool_loop_closed,
        "final_product_protocol_valid": bool(protocol.get("passed")),
        "operator_delta_valid": operator_delta_valid,
        "operator_delta_errors": operator_delta.get("errors") or [],
        "final_product_delta_valid": operator_delta_valid,
        "gpu1_text_after_tool_result_ref": assistant_text_ref,
        "delta_readable_ref": artifact_ref(
            readable_path,
            repo_root,
            kind="gpu1_native_tool_loop_delta_readable",
            producer="gpu1_native_tool_loop_preflight",
        ),
        "delta_review_tool": "generic_write",
        "delta_review_tool_result_written": bool(delta_review.get("tool_result")),
        "delta_review_tool_passed": bool(delta_review.get("passed")),
        "delta_review_broker_report_ref": delta_review.get("broker_report_ref") or {},
        "delta_review_input_ref": delta_review.get("delta_ref") or {},
        "final_product_delta_ref": delta_review.get("delta_ref") or {},
        "request_id": evidence.get("request_id") or "",
        "gpu1_tool_loop_subturn_count": len(subturn_report_paths),
        "final_subturn": evidence.get("final_subturn"),
        "subturn_report_refs": [
            artifact_ref(path, repo_root, kind="gpu1_native_tool_subturn_report")
            for path in subturn_report_paths
        ],
        "broker_report_refs": [
            artifact_ref(path, repo_root, kind="gpu1_native_tool_broker_report")
            for path in broker_report_paths
        ],
        "subturn0_report_ref": artifact_ref(
            output.parent / "gpu1_native_tool_loop_preflight" / "gpu1_subturn0_report.json",
            repo_root,
            kind="gpu1_native_tool_subturn_report",
        ),
        "broker_report_ref": artifact_ref(
            output.parent / "gpu1_native_tool_loop_preflight" / "broker_report.json",
            repo_root,
            kind="gpu1_native_tool_broker_report",
        ),
        "subturn1_report_ref": artifact_ref(
            output.parent / "gpu1_native_tool_loop_preflight" / "gpu1_subturn1_report.json",
            repo_root,
            kind="gpu1_native_tool_subturn_report",
        ),
        "final_product_protocol": protocol,
        "gpu1_tool_result_consumption": consumption,
        "errors": sorted(set(errors)),
        "warnings": warnings,
    }
    write_json_report(report, output)
    report["documents_export"] = export_documents_copy(
        repo_root,
        output,
        output.parent / "gpu1_native_tool_loop_preflight",
        str(args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")),
    )
    write_json_report(report, output)
    return report

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/gpu1_native_tool_loop_preflight.json")
    parser.add_argument("--model", default="qwen2.5-coder:14b")
    parser.add_argument("--base-url", default="http://127.0.0.1:11434")
    parser.add_argument("--num-ctx", type=int, default=8192)
    parser.add_argument("--max-new-tokens", type=int, default=700)
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--timeout-seconds", type=int, default=90)
    parser.add_argument("--max-subturns", type=int, default=5)
    parser.add_argument("--startup-manifest", default="")
    parser.add_argument("--startup-output-dir", default="")
    parser.add_argument("--refresh-startup-context", action="store_true")
    parser.add_argument("--memory-query", default=DEFAULT_MEMORY_QUERY)
    parser.add_argument("--rag-embedding-model", default="bge-m3")
    parser.add_argument("--file-window-limit", type=int, default=16000)
    parser.add_argument("--operator-prompt", default="")
    parser.add_argument("--operator-prompt-file", default="")
    parser.add_argument("--stamp", default="")
    args = parser.parse_args()
    report = _run(args)
    print(write_json_report(report), end="")
    return 0 if report.get("passed") else 2

if __name__ == "__main__":
    raise SystemExit(main())
