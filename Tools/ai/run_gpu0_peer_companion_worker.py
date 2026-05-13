#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, record_lane_diagnostic
from tools.ai.runtime_hardware_capability.workloads import run_openvino_gpu0_tensor_test
from tools.validation.report_utils import (
    resolve_output_path,
    write_json_report,
    write_text_report,
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def safe_int(value: Any) -> int:
    try:
        return int(value or 0)
    except (TypeError, ValueError):
        return 0


def classify_primary(primary: dict[str, Any]) -> list[str]:
    classifications: list[str] = []
    if not primary.get("passed"):
        classifications.append("gpu1_primary_advisory_not_proven")
    if primary.get("provider_empty_response"):
        classifications.append("gpu1_primary_advisory_empty_response")
    for item in safe_list(primary.get("classifications")):
        text = str(item)
        if text and text not in classifications:
            classifications.append(text)
    return classifications


def response_items(
    task_packet: dict[str, Any], primary: dict[str, Any], workload: dict[str, Any]
) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    for task in safe_list(task_packet.get("tasks")):
        if not isinstance(task, dict):
            continue
        task_id = str(task.get("id") or "unknown_task")
        objective = str(task.get("objective") or "")
        status = "ready"
        findings: list[str] = []
        if "primary_advisory" in task_id and not primary.get("passed"):
            status = "blocked"
            findings.append(
                "GPU1 primary advisory is not proven; heap runtime must classify degradation."
            )
        if workload.get("passed") is not True:
            status = "blocked"
            findings.append("GPU0 OpenVINO peer workload failed or was unavailable.")
        if not findings:
            findings.append(
                "Task can be handled with deterministic/broker evidence in this peer cycle."
            )
        items.append(
            {
                "task_id": task_id,
                "objective": objective,
                "status": status,
                "findings": findings,
                "requires_gpu1_followup": not primary.get("passed"),
                "requires_broker_context": "runtime_tool" in task_id
                or "patch_spec" in task_id,
            }
        )
    return items


def tool_requests(
    task_packet: dict[str, Any], response: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    templates = [
        item
        for item in safe_list(task_packet.get("tool_request_templates"))
        if isinstance(item, dict)
    ]
    task_ids = {
        str(item.get("task_id"))
        for item in response
        if item.get("requires_broker_context")
    }
    requests: list[dict[str, Any]] = []
    for index, template in enumerate(templates, start=1):
        request = dict(template)
        request.setdefault("id", f"gpu0_peer_tool_request_{index:03d}")
        request.setdefault(
            "reason",
            "GPU0 peer worker requested broker-controlled deterministic evidence.",
        )
        request["source"] = "gpu0_peer_companion"
        if task_ids:
            request["related_task_ids"] = sorted(task_ids)
        requests.append(request)
    return requests


def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], dict[str, Any]]:
    repo_root = Path(args.repo_root).resolve()
    task_path = resolve_output_path(repo_root, args.task_packet)
    primary_path = resolve_output_path(repo_root, args.primary_advisory)
    task_packet = read_json(task_path)
    primary = read_json(primary_path)
    model_dir = os.environ.get("IA_CARMINE_GPU0_COMPANION_MODEL_DIR", "").strip()
    workload = run_openvino_gpu0_tensor_test(
        iterations=args.iterations,
        min_seconds=args.min_seconds,
        role="peer_companion_worker",
        production_support=True,
    )
    semantic_mode = "semantic_model_unconfigured_numeric_tool_peer"
    classifications = classify_primary(primary)
    warnings: list[str] = []
    errors: list[str] = []
    if not model_dir:
        classifications.append("gpu0_peer_semantic_model_unconfigured")
        warnings.append(
            "IA_CARMINE_GPU0_COMPANION_MODEL_DIR not set; GPU0 peer emits numeric/tool evidence only."
        )
    else:
        semantic_mode = "semantic_model_configured_not_invoked_by_this_worker"
        warnings.append(
            "Semantic GPU0 model directory is configured; this worker currently keeps provider semantics in report-only numeric/tool mode."
        )
    if not task_packet:
        classifications.append("gpu0_peer_task_packet_missing")
        errors.append("GPU0 peer task packet missing or invalid.")
    if workload.get("passed") is not True:
        classifications.append("gpu0_peer_openvino_workload_failed")
        errors.append("GPU0 OpenVINO peer workload failed.")
    responses = response_items(task_packet, primary, workload)
    requests = tool_requests(task_packet, responses)
    if not responses:
        classifications.append("gpu0_peer_no_response_items")
        errors.append("GPU0 peer worker had no tasks to answer.")
    report = {
        "schema_version": 1,
        "kind": "gpu0_peer_response",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "repo_root": str(repo_root),
        "passed": not errors,
        "role": "companion_peer_worker",
        "lane": "GPU0/OpenVINO",
        "production_role": "tool_request_producing_companion",
        "provider_execution_performed": bool(
            workload.get("provider_execution_performed")
        ),
        "semantic_execution_mode": semantic_mode,
        "gpu0_model_dir_configured": bool(model_dir),
        "task_packet": repo_rel(repo_root, task_path),
        "primary_advisory": repo_rel(repo_root, primary_path),
        "task_count": safe_int(task_packet.get("task_count")),
        "response_count": len(responses),
        "tool_request_count": len(requests),
        "peer_visibility": {
            "gpu0_sees_gpu1_primary_advisory": bool(primary),
            "gpu0_sees_task_packet": bool(task_packet),
            "gpu0_produces_tool_requests_for_gpu1": bool(requests),
            "gpu1_followup_expected_after_broker": bool(requests),
        },
        "response_items": responses,
        "openvino_gpu0_workload": workload,
        "openvino_gpu0_workload_passed": bool(workload.get("passed")),
        "classifications": list(dict.fromkeys(classifications)),
        "errors": errors,
        "warnings": warnings,
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "openvino_gpu1_workload_allowed": False,
            "gpu1_reserved_for_ollama": True,
            "runtime_tool_broker_required_for_tool_requests": True,
        },
    }
    request_packet = {
        "schema_version": 1,
        "kind": "gpu0_peer_tool_requests",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "source": "gpu0_peer_companion",
        "tool_requests": requests,
        "guardrails": {
            "broker_allowlist_required": True,
            "provider_execution_allowed": False,
            "patch_application_allowed": False,
            "persistent_memory_write_allowed": False,
            "manual_review_required": True,
        },
    }
    return report, request_packet


def append_runtime_heap_events(
    args: argparse.Namespace,
    repo_root: Path,
    report: dict[str, Any],
    request_packet: dict[str, Any],
) -> list[dict[str, Any]]:
    if not getattr(args, "runtime_heap_stamp", ""):
        return []
    heap = ProviderRuntimeHeap.from_args(
        repo_root,
        args.runtime_heap_stamp,
        getattr(args, "runtime_heap_events", ""),
        getattr(args, "runtime_heap_snapshot", ""),
        getattr(args, "runtime_heap_markdown", ""),
    )
    events: list[dict[str, Any]] = []
    correlation_id = f"{args.runtime_heap_stamp}:gpu1-gpu0-live-evidence"
    events.append(
        record_lane_diagnostic(
            heap,
            "gpu0",
            "ready" if report.get("passed") else "degraded",
            "GPU0 peer companion worker completed.",
            {
                "passed": report.get("passed"),
                "provider_execution_performed": report.get(
                    "provider_execution_performed"
                ),
                "classifications": report.get("classifications", []),
                "errors": report.get("errors", []),
                "warnings": report.get("warnings", []),
            },
            correlation_id=f"{args.runtime_heap_stamp}:gpu0-peer-companion-diagnostic",
        )
    )
    events.append(
        heap.append_event(
            source="gpu0",
            target="gpu1",
            event_type="evidence_response",
            round_id=1,
            correlation_id=correlation_id,
            payload={
                "summary": "GPU0 coworker produced live response for GPU1 through runtime heap.",
                "gpu0_report": report.get("stamp"),
                "passed": report.get("passed"),
                "provider_execution_performed": report.get(
                    "provider_execution_performed"
                ),
                "response_count": report.get("response_count"),
                "tool_request_count": report.get("tool_request_count"),
                "classifications": report.get("classifications", []),
                "direct_execution": False,
                "broker_required": True,
            },
        )
    )
    for request in safe_list(request_packet.get("tool_requests")):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        events.append(
            heap.append_event(
                source="gpu0",
                target="broker",
                event_type="broker_request",
                round_id=1,
                correlation_id=request_id,
                payload={
                    "request_id": request_id,
                    "tool": request.get("tool"),
                    "args": request.get("args", {}),
                    "reason": request.get("reason"),
                    "source": "gpu0_peer_companion_live",
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        )
    snapshot = heap.write_snapshot()
    report["runtime_heap_live_event_count"] = len(events)
    report["runtime_heap_live_event_log"] = snapshot.get("event_log")
    return events


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# GPU0 Peer Companion Response",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Semantic mode: `{report.get('semantic_execution_mode')}`",
        f"- Task count: `{report.get('task_count')}`",
        f"- Response count: `{report.get('response_count')}`",
        f"- Tool request count: `{report.get('tool_request_count')}`",
        f"- Classifications: `{report.get('classifications')}`",
        "",
        "## Responses",
        "",
    ]
    for item in safe_list(report.get("response_items")):
        lines.append(
            f"- `{item.get('task_id')}` status=`{item.get('status')}` findings=`{item.get('findings')}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in safe_list(report.get("errors")))
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in safe_list(report.get("warnings")))
    lines.append("")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--task-packet", required=True)
    parser.add_argument("--primary-advisory", required=True)
    parser.add_argument(
        "--output", default="output/validation/gpu0_peer_response_{stamp}.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/gpu0_peer_response_{stamp}.md"
    )
    parser.add_argument(
        "--tool-requests-output",
        default="output/validation/gpu0_tool_requests_{stamp}.json",
    )
    parser.add_argument("--iterations", type=int, default=24)
    parser.add_argument("--min-seconds", type=float, default=1.0)
    parser.add_argument("--allow-degraded", action="store_true")
    parser.add_argument("--runtime-heap-stamp", default="")
    parser.add_argument("--runtime-heap-events", default="")
    parser.add_argument("--runtime-heap-snapshot", default="")
    parser.add_argument("--runtime-heap-markdown", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report, requests = build_report(args)
    append_runtime_heap_events(args, repo_root, report, requests)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(
        repo_root, args.markdown_output.format(stamp=args.stamp)
    )
    request_output = resolve_output_path(
        repo_root, args.tool_requests_output.format(stamp=args.stamp)
    )
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    write_json_report(requests, request_output)
    return 0 if report["passed"] or args.allow_degraded else 2


if __name__ == "__main__":
    raise SystemExit(main())
