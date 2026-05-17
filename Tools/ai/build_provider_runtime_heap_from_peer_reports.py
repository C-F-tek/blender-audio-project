#!/usr/bin/env python3
"""Build provider-runtime heap events from real peer-exchange reports.

This bridge converts already-produced full-toolbox provider artifacts into an
append-only runtime heap event stream. It does not run providers, execute tools,
apply patches, or mutate source files.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict  # type: ignore
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_OUTPUT = "output/validation/provider_runtime_heap_from_peer_reports_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/provider_runtime_heap_from_peer_reports_{stamp}.md"


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


def existing_report(repo_root: Path, path_text: str) -> str:
    if not path_text:
        return ""
    path = Path(path_text)
    return repo_rel(repo_root, path) if path.exists() else path_text


def first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return ""


def append_from_reports(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.heap_markdown
    )

    gpu1 = read_json(args.gpu1_report)
    gpu0 = read_json(args.gpu0_report)
    gpu0_tool_requests = read_json(args.gpu0_tool_requests)
    gpu0_broker = read_json(args.gpu0_broker_report)
    npu = read_json(args.npu_report)
    read_json(args.npu_broker_report)
    peer_contract = read_json(args.peer_contract_report)
    peer_exchange = read_json(args.peer_exchange_report)

    events: list[dict[str, Any]] = []
    warnings: list[str] = []
    correlation_gpu = f"{args.stamp}:gpu1-gpu0-peer-evidence"

    events.append(
        heap.append_event(
            source="orchestrator",
            event_type="provider_state",
            correlation_id=f"{args.stamp}:full-toolbox-runtime-heap",
            payload={
                "state": "full_toolbox_peer_reports_loaded",
                "peer_exchange_present": bool(peer_exchange),
                "reports": {
                    "gpu1": existing_report(repo_root, args.gpu1_report),
                    "gpu0": existing_report(repo_root, args.gpu0_report),
                    "gpu0_tool_requests": existing_report(repo_root, args.gpu0_tool_requests),
                    "gpu0_broker": existing_report(repo_root, args.gpu0_broker_report),
                    "npu": existing_report(repo_root, args.npu_report),
                    "npu_broker": existing_report(repo_root, args.npu_broker_report),
                    "peer_exchange": existing_report(repo_root, args.peer_exchange_report),
                    "peer_contract": existing_report(repo_root, args.peer_contract_report),
                },
                "direct_execution": False,
                "broker_required": True,
            },
        )
    )

    if gpu1 and gpu0:
        events.append(
            heap.append_event(
                source="gpu1",
                target="gpu0",
                event_type="evidence_request",
                round_id=1,
                correlation_id=correlation_gpu,
                payload={
                    "objective": "GPU1 primary planner requests coworker evidence from GPU0 through shared runtime heap.",
                    "gpu1_report": existing_report(repo_root, args.gpu1_report),
                    "gpu1_passed": gpu1.get("passed"),
                    "gpu1_provider_execution_performed": gpu1.get("provider_execution_performed"),
                    "recommendation_count": first_present(
                        gpu1.get("recommendation_count"),
                        (
                            len(gpu1.get("recommendations", []))
                            if isinstance(gpu1.get("recommendations"), list)
                            else ""
                        ),
                    ),
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        )
        events.append(
            heap.append_event(
                source="gpu0",
                target="gpu1",
                event_type="evidence_response",
                round_id=1,
                correlation_id=correlation_gpu,
                payload={
                    "summary": "GPU0 coworker response is available as provider peer evidence.",
                    "gpu0_report": existing_report(repo_root, args.gpu0_report),
                    "gpu0_passed": gpu0.get("passed"),
                    "gpu0_provider_execution_performed": gpu0.get("provider_execution_performed"),
                    "tool_request_count": first_present(
                        gpu0.get("tool_request_count"),
                        (
                            len(gpu0_tool_requests.get("tool_requests", []))
                            if isinstance(gpu0_tool_requests.get("tool_requests"), list)
                            else ""
                        ),
                    ),
                    "classifications": first_present(
                        gpu0.get("classifications"), gpu0.get("classification")
                    ),
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        )
    else:
        warnings.append("gpu1/gpu0 reports missing; GPU peer evidence exchange not emitted")

    tool_requests = gpu0_tool_requests.get("tool_requests", [])
    if isinstance(tool_requests, list):
        for index, request in enumerate(tool_requests, start=1):
            if not isinstance(request, dict):
                continue
            request_id = str(
                request.get("id") or request.get("request_id") or f"gpu0-tool-request-{index:03d}"
            )
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
                        "args": safe_dict(request.get("args")),
                        "reason": request.get("reason"),
                        "source_report": existing_report(repo_root, args.gpu0_tool_requests),
                        "direct_execution": False,
                        "broker_required": True,
                    },
                )
            )

    broker_results = gpu0_broker.get("tool_results", [])
    if isinstance(broker_results, list) and broker_results:
        for index, result in enumerate(broker_results, start=1):
            if not isinstance(result, dict):
                continue
            result_id = str(
                result.get("id") or result.get("request_id") or f"gpu0-broker-result-{index:03d}"
            )
            events.append(
                heap.append_event(
                    source="broker",
                    target="gpu0",
                    event_type="broker_result",
                    round_id=1,
                    correlation_id=result_id,
                    payload={
                        "request_id": result_id,
                        "tool": result.get("tool"),
                        "executed": result.get("executed"),
                        "blocked": result.get("blocked"),
                        "returncode": result.get("returncode"),
                        "outputs": result.get("outputs"),
                        "errors": result.get("errors", []),
                        "warnings": result.get("warnings", []),
                        "broker_report": existing_report(repo_root, args.gpu0_broker_report),
                    },
                )
            )
    elif gpu0_broker:
        events.append(
            heap.append_event(
                source="broker",
                target="gpu0",
                event_type="broker_result",
                round_id=1,
                correlation_id=f"{args.stamp}:gpu0-broker-summary",
                payload={
                    "broker_report": existing_report(repo_root, args.gpu0_broker_report),
                    "passed": gpu0_broker.get("passed"),
                    "tool_request_count": gpu0_broker.get("tool_request_count"),
                    "tool_execution_count": gpu0_broker.get("tool_execution_count"),
                    "blocked_tool_count": gpu0_broker.get("blocked_tool_count"),
                    "failed_tool_count": gpu0_broker.get("failed_tool_count"),
                },
            )
        )

    if npu:
        events.append(
            heap.append_event(
                source="npu",
                target="gpu1",
                event_type="evidence_response",
                round_id=1,
                correlation_id=f"{args.stamp}:npu-micro-support",
                payload={
                    "summary": "NPU microtask support report is available to GPU1 as non-blocking context.",
                    "npu_report": existing_report(repo_root, args.npu_report),
                    "npu_passed": npu.get("passed"),
                    "provider_execution_requested": npu.get("provider_execution_requested"),
                    "provider_execution_performed": npu.get("provider_execution_performed"),
                    "non_blocking": first_present(npu.get("non_blocking"), True),
                    "tool_request_count": npu.get("tool_request_count"),
                    "product_pass_blocker": npu.get("product_pass_blocker"),
                    "broker_report": existing_report(repo_root, args.npu_broker_report),
                    "direct_execution": False,
                    "broker_required": True,
                },
            )
        )

    if peer_contract:
        events.append(
            heap.append_event(
                source="deterministic",
                target="gpu1",
                event_type="validation_signal",
                round_id=1,
                correlation_id=f"{args.stamp}:ai-peer-contract",
                payload={
                    "peer_contract_report": existing_report(repo_root, args.peer_contract_report),
                    "peer_exchange_report": existing_report(repo_root, args.peer_exchange_report),
                    "passed": peer_contract.get("passed"),
                    "provider_broker_loop": safe_dict(peer_contract.get("provider_broker_loop")),
                    "errors": peer_contract.get("errors", []),
                    "warnings": peer_contract.get("warnings", []),
                },
            )
        )

    snapshot = heap.write_snapshot()
    errors: list[str] = []
    if not (gpu1 and gpu0):
        errors.append("GPU1/GPU0 peer reports were not both available")

    return {
        "schema_version": 1,
        "kind": "provider_runtime_heap_from_peer_reports",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "event_count": len(events),
        "heap_snapshot": {
            "event_count": snapshot.get("event_count"),
            "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            "event_log": snapshot.get("event_log"),
        },
        "reports": {
            "gpu1": existing_report(repo_root, args.gpu1_report),
            "gpu0": existing_report(repo_root, args.gpu0_report),
            "gpu0_tool_requests": existing_report(repo_root, args.gpu0_tool_requests),
            "gpu0_broker": existing_report(repo_root, args.gpu0_broker_report),
            "npu": existing_report(repo_root, args.npu_report),
            "npu_broker": existing_report(repo_root, args.npu_broker_report),
            "peer_exchange": existing_report(repo_root, args.peer_exchange_report),
            "peer_contract": existing_report(repo_root, args.peer_contract_report),
        },
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "git_write_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap From Peer Reports", ""]
    for key in ("passed", "stamp", "event_count"):
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
    lines.extend(["", "## Reports", ""])
    for key, value in safe_dict(report.get("reports")).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--gpu1-report", default="")
    parser.add_argument("--gpu0-report", default="")
    parser.add_argument("--gpu0-tool-requests", default="")
    parser.add_argument("--gpu0-broker-report", default="")
    parser.add_argument("--npu-report", default="")
    parser.add_argument("--npu-broker-report", default="")
    parser.add_argument("--peer-exchange-report", default="")
    parser.add_argument("--peer-contract-report", default="")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = append_from_reports(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(repo_root, args.markdown_output.format(stamp=args.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
