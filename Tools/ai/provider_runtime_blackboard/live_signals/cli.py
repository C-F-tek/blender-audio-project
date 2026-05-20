#!/usr/bin/env python3
"""Append live provider-runtime heap signals during full-toolbox execution.

This is an interstitial runtime blackboard bridge. It does not run providers,
execute tools, apply patches, or mutate source files. It only appends
coordination events to the provider runtime heap at the point where the
orchestrator already has the relevant report context.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap, safe_dict
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_runtime_blackboard import ProviderRuntimeHeap, safe_dict  # type: ignore
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path_text: str) -> dict[str, Any]:
    if not path_text:
        return {}
    path = Path(path_text)
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def existing(repo_root: Path, path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    return repo_rel(repo_root, path) if path.exists() else path_text


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.heap_markdown
    )

    events: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    if args.mode == "init":
        events.append(
            heap.append_event(
                source="orchestrator",
                event_type="provider_state",
                correlation_id=f"{args.stamp}:live-runtime-heap",
                payload={
                    "state": "live_runtime_heap_initialized",
                    "mode": args.mode,
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        )

    elif args.mode == "gpu1-request":
        gpu1 = read_json(args.gpu1_report)
        task_packet = read_json(args.gpu0_task_packet)
        if not gpu1:
            errors.append(f"missing or invalid gpu1 report: {args.gpu1_report}")
        if not task_packet:
            errors.append(f"missing or invalid gpu0 task packet: {args.gpu0_task_packet}")
        if not errors:
            events.append(
                heap.append_event(
                    source="gpu1",
                    target="gpu0",
                    event_type="evidence_request",
                    round_id=args.round,
                    correlation_id=f"{args.stamp}:gpu1-gpu0-live-evidence",
                    payload={
                        "objective": "GPU1 primary advisory requests live coworker evidence from GPU0 before GPU0 execution.",
                        "gpu1_report": existing(repo_root, args.gpu1_report),
                        "gpu0_task_packet": existing(repo_root, args.gpu0_task_packet),
                        "gpu1_passed": gpu1.get("passed"),
                        "gpu1_provider_execution_performed": gpu1.get(
                            "provider_execution_performed"
                        ),
                        "task_count": task_packet.get("task_count"),
                        "direct_execution": False,
                        "broker_required": True,
                    },
                )
            )

    elif args.mode == "broker-results":
        broker_report = read_json(args.broker_report)
        if not broker_report:
            errors.append(f"missing or invalid broker report: {args.broker_report}")
        else:
            results = safe_list(broker_report.get("tool_results"))
            if not results:
                events.append(
                    heap.append_event(
                        source="broker",
                        target="gpu0",
                        event_type="broker_result",
                        round_id=args.round,
                        correlation_id=f"{args.stamp}:gpu0-live-broker-summary",
                        payload={
                            "broker_report": existing(repo_root, args.broker_report),
                            "passed": broker_report.get("passed"),
                            "tool_request_count": broker_report.get("tool_request_count"),
                            "tool_execution_count": broker_report.get("tool_execution_count"),
                            "blocked_tool_count": broker_report.get("blocked_tool_count"),
                            "failed_tool_count": broker_report.get("failed_tool_count"),
                        },
                    )
                )
            for index, result in enumerate(results, start=1):
                if not isinstance(result, dict):
                    continue
                request_id = str(
                    result.get("id")
                    or result.get("request_id")
                    or f"gpu0-live-broker-result-{index:03d}"
                )
                events.append(
                    heap.append_event(
                        source="broker",
                        target="gpu0",
                        event_type="broker_result",
                        round_id=args.round,
                        correlation_id=request_id,
                        payload={
                            "request_id": request_id,
                            "tool": result.get("tool"),
                            "executed": result.get("executed"),
                            "blocked": result.get("blocked"),
                            "returncode": result.get("returncode"),
                            "outputs": result.get("outputs"),
                            "errors": result.get("errors", []),
                            "warnings": result.get("warnings", []),
                            "broker_report": existing(repo_root, args.broker_report),
                        },
                    )
                )

    elif args.mode == "npu-support":
        npu = read_json(args.npu_report)
        if not npu:
            errors.append(f"missing or invalid npu report: {args.npu_report}")
        else:
            events.append(
                heap.append_event(
                    source="npu",
                    target="gpu1",
                    event_type="evidence_response",
                    round_id=args.round,
                    correlation_id=f"{args.stamp}:npu-live-support",
                    payload={
                        "summary": "NPU micro/support lane published live support evidence to GPU1.",
                        "npu_report": existing(repo_root, args.npu_report),
                        "npu_passed": npu.get("passed"),
                        "provider_execution_requested": npu.get("provider_execution_requested"),
                        "provider_execution_performed": npu.get("provider_execution_performed"),
                        "non_blocking": npu.get("non_blocking"),
                        "tool_request_count": npu.get("tool_request_count"),
                        "product_pass_blocker": npu.get("product_pass_blocker"),
                        "direct_execution": False,
                        "broker_required": True,
                    },
                )
            )
    elif args.mode == "tool-catalog-complete":
        capability = read_json(args.runtime_capability)
        runtime_usage = read_json(args.runtime_usage)
        if not capability:
            errors.append(
                f"missing or invalid runtime capability report: {args.runtime_capability}"
            )
        if not runtime_usage:
            errors.append(f"missing or invalid runtime usage report: {args.runtime_usage}")
        if not errors:
            correlation_id = f"{args.stamp}:tool-catalog-exchange"
            catalog_payload = {
                "runtime_capability": existing(repo_root, args.runtime_capability),
                "runtime_usage": existing(repo_root, args.runtime_usage),
                "tool_count": capability.get("tool_count"),
                "broker_required": True,
                "direct_execution": False,
            }
            events.append(
                heap.append_event(
                    source="gpu1",
                    target="broker",
                    event_type="tool_catalog_request",
                    round_id=args.round,
                    correlation_id=correlation_id,
                    payload={
                        **catalog_payload,
                        "summary": "GPU1 requests the broker-controlled tool catalog before final product assembly.",
                    },
                )
            )
            events.append(
                heap.append_event(
                    source="broker",
                    target="gpu1",
                    event_type="tool_catalog_response",
                    round_id=args.round,
                    correlation_id=correlation_id,
                    payload={
                        **catalog_payload,
                        "summary": "Broker publishes the runtime tool capability catalog into the provider heap.",
                    },
                )
            )
    else:
        errors.append(f"unsupported mode: {args.mode}")

    snapshot = heap.write_snapshot()
    return {
        "schema_version": 1,
        "kind": "provider_runtime_live_signals",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "mode": args.mode,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "event_count": len(events),
        "events": events,
        "heap_snapshot": {
            "event_count": snapshot.get("event_count"),
            "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            "event_log": snapshot.get("event_log"),
        },
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Live Signals", ""]
    for key in ("passed", "stamp", "mode", "event_count"):
        lines.append(f"- {key}: `{report.get(key)}`")
    heap = safe_dict(report.get("heap_snapshot"))
    lines.append(f"- heap_event_count: `{heap.get('event_count')}`")
    lines.append(f"- pending_broker_request_count: `{heap.get('pending_broker_request_count')}`")
    lines.append(f"- event_log: `{heap.get('event_log')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument(
        "--mode",
        required=True,
        choices=[
            "init",
            "gpu1-request",
            "broker-results",
            "npu-support",
            "tool-catalog-complete",
        ],
    )
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--gpu1-report", default="")
    parser.add_argument("--gpu0-task-packet", default="")
    parser.add_argument("--broker-report", default="")
    parser.add_argument("--npu-report", default="")
    parser.add_argument("--runtime-usage", default="")
    parser.add_argument("--runtime-capability", default="")
    parser.add_argument("--round", type=int, default=1)
    parser.add_argument(
        "--output",
        default="output/validation/provider_runtime_live_signals_{mode}_{stamp}.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/provider_runtime_live_signals_{mode}_{stamp}.md",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp, mode=args.mode))
    markdown = resolve_output_path(
        repo_root, args.markdown_output.format(stamp=args.stamp, mode=args.mode)
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
