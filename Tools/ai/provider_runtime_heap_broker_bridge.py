#!/usr/bin/env python3
"""Bridge provider-runtime heap broker requests into the existing broker.

This adapter keeps provider lanes conversational through the shared heap while
preserving the existing rule: tools are executed only by
tools/ai/agent_runtime_tool_broker.py.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.ai.provider_mesh_runtime.python_runtime import (
        command_env,
        resolve_child_python,
    )
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
    from tools.ai.provider_mesh_runtime.python_runtime import (  # type: ignore
        command_env,
        resolve_child_python,
    )
    from tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict  # type: ignore
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

DEFAULT_OUTPUT = "output/validation/provider_runtime_heap_broker_bridge_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/provider_runtime_heap_broker_bridge_{stamp}.md"


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


def safe_id(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip()
    keep = []
    for char in text:
        keep.append(char if char.isalnum() or char in "._-" else "_")
    normalized = "".join(keep).strip("._-")
    return normalized[:96] or fallback


def event_to_tool_request(event: dict[str, Any], index: int) -> dict[str, Any]:
    payload = safe_dict(event.get("payload"))
    request_id = safe_id(
        event.get("correlation_id") or payload.get("request_id") or payload.get("id"),
        f"heap_request_{index:03d}",
    )
    return {
        "id": request_id,
        "tool": str(payload.get("tool") or ""),
        "args": safe_dict(payload.get("args")),
        "reason": str(payload.get("reason") or "Provider runtime heap broker request."),
        "requirement": str(payload.get("requirement") or ""),
        "source": str(event.get("source") or "provider_runtime_heap"),
        "heap_event": {
            "source": event.get("source"),
            "target": event.get("target"),
            "round": event.get("round"),
            "event_type": event.get("event_type"),
            "correlation_id": event.get("correlation_id"),
        },
    }


def build_request_packet(
    repo_root: Path, stamp: str, pending: list[dict[str, Any]], request_file: Path
) -> dict[str, Any]:
    tool_requests = [
        event_to_tool_request(event, index)
        for index, event in enumerate(pending, start=1)
    ]
    packet = {
        "schema_version": 1,
        "kind": "agent_runtime_tool_requests",
        "generated_at": now_iso(),
        "stamp": stamp,
        "source": "provider_runtime_heap",
        "source_classification": "provider_runtime_heap_broker_bridge",
        "tool_requests": tool_requests,
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    request_file.parent.mkdir(parents=True, exist_ok=True)
    request_file.write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return packet


def run_broker(
    *,
    repo_root: Path,
    stamp: str,
    request_file: Path,
    tool_output_dir: Path,
    broker_output: Path,
    broker_markdown: Path,
    timeout_seconds: int,
    dry_run: bool,
) -> tuple[int, str, str]:
    command = [
        resolve_child_python(repo_root),
        "tools/ai/agent_runtime_tool_broker.py",
        "--repo-root",
        ".",
        "--request-file",
        repo_rel(repo_root, request_file),
        "--tool-output-dir",
        repo_rel(repo_root, tool_output_dir),
        "--stamp",
        stamp,
        "--timeout-seconds",
        str(timeout_seconds),
        "--output",
        repo_rel(repo_root, broker_output),
        "--markdown-output",
        repo_rel(repo_root, broker_markdown),
    ]
    if dry_run:
        command.append("--dry-run")
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=command_env(repo_root),
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def broker_result_target_from_source(value: object) -> str:
    lane = str(value or "").strip().lower()
    if lane in {
        "gpu1",
        "gpu0",
        "npu",
        "broker",
        "deterministic",
        "telemetry",
        "orchestrator",
    }:
        return lane
    return "orchestrator"


def request_sources_by_id(broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report.get("tool_requests", []):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        if not request_id:
            continue
        heap_event = safe_dict(request.get("heap_event"))
        source = request.get("source") or heap_event.get("source") or "orchestrator"
        mapping[request_id] = broker_result_target_from_source(source)
    return mapping


def request_requirements_by_id(broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report.get("tool_requests", []):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        requirement = str(request.get("requirement") or "")
        if request_id and requirement:
            mapping[request_id] = requirement
    return mapping


def request_correlations_by_id(broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report.get("tool_requests", []):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        heap_event = safe_dict(request.get("heap_event"))
        correlation_id = str(heap_event.get("correlation_id") or "")
        if request_id and correlation_id:
            mapping[request_id] = correlation_id
    return mapping


def append_broker_results(
    heap: ProviderRuntimeHeap, broker_report: dict[str, Any]
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    source_by_request_id = request_sources_by_id(broker_report)
    correlation_by_request_id = request_correlations_by_id(broker_report)
    requirement_by_request_id = request_requirements_by_id(broker_report)
    for result in broker_report.get("tool_results", []):
        if not isinstance(result, dict):
            continue
        result_id = str(result.get("id") or result.get("request_id") or "")
        result_correlation_id = correlation_by_request_id.get(result_id, result_id)
        target_lane = source_by_request_id.get(result_id, "orchestrator")
        event = heap.append_event(
            source="broker",
            target=target_lane,
            event_type="broker_result",
            correlation_id=result_correlation_id,
            payload={
                "request_id": result_correlation_id,
                "normalized_request_id": result_id,
                "target_lane": target_lane,
                "tool": result.get("tool"),
                "requirement": result.get("requirement")
                or requirement_by_request_id.get(result_id, ""),
                "executed": result.get("executed"),
                "blocked": result.get("blocked"),
                "returncode": result.get("returncode"),
                "outputs": result.get("outputs"),
                "errors": result.get("errors", []),
                "warnings": result.get("warnings", []),
                "broker_report": broker_report.get("output") or "",
            },
        )
        events.append(event)
    return events


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.heap_markdown
    )
    pending = heap.pending_broker_requests()
    if args.max_requests > 0:
        pending = pending[: args.max_requests]

    bridge_dir = resolve_output_path(
        repo_root, args.bridge_dir.format(stamp=args.stamp)
    )
    request_file = bridge_dir / "broker_requests_from_heap.json"
    broker_output = bridge_dir / "agent_runtime_tool_broker.json"
    broker_markdown = bridge_dir / "agent_runtime_tool_broker.md"
    tool_output_dir = bridge_dir / "tool_outputs"

    packet = build_request_packet(repo_root, args.stamp, pending, request_file)
    returncode = 0
    stdout_tail = ""
    stderr_tail = ""
    broker_report: dict[str, Any] = {}
    broker_result_events: list[dict[str, Any]] = []

    if pending:
        returncode, stdout_tail, stderr_tail = run_broker(
            repo_root=repo_root,
            stamp=args.stamp,
            request_file=request_file,
            tool_output_dir=tool_output_dir,
            broker_output=broker_output,
            broker_markdown=broker_markdown,
            timeout_seconds=args.timeout_seconds,
            dry_run=args.dry_run,
        )
        broker_report = read_json(broker_output)
        if broker_report:
            broker_report["output"] = repo_rel(repo_root, broker_output)
            # The broker output may not echo the original request packet. Keep
            # the generated tool_requests attached here so broker_result events
            # can be routed back to the provider lane that created the request.
            broker_report.setdefault("tool_requests", packet.get("tool_requests", []))
            broker_result_events = append_broker_results(heap, broker_report)

    snapshot = heap.write_snapshot()
    errors: list[str] = []
    if returncode != 0:
        errors.append(f"agent_runtime_tool_broker returned {returncode}")
    if broker_report.get("errors"):
        errors.extend(str(item) for item in broker_report.get("errors", []))

    return {
        "schema_version": 1,
        "kind": "provider_runtime_heap_broker_bridge",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "dry_run": bool(args.dry_run),
        "pending_broker_request_count": len(pending),
        "broker_result_event_count": len(broker_result_events),
        "request_packet": repo_rel(repo_root, request_file),
        "broker_report": repo_rel(repo_root, broker_output),
        "broker_markdown": repo_rel(repo_root, broker_markdown),
        "tool_output_dir": repo_rel(repo_root, tool_output_dir),
        "broker_returncode": returncode,
        "broker_stdout_tail": stdout_tail,
        "broker_stderr_tail": stderr_tail,
        "broker_passed": broker_report.get("passed"),
        "tool_request_count": broker_report.get(
            "tool_request_count", len(packet.get("tool_requests", []))
        ),
        "tool_execution_count": broker_report.get("tool_execution_count", 0),
        "blocked_tool_count": broker_report.get("blocked_tool_count", 0),
        "failed_tool_count": broker_report.get("failed_tool_count", 0),
        "heap_snapshot": {
            "event_count": snapshot.get("event_count"),
            "pending_broker_request_count": snapshot.get(
                "pending_broker_request_count"
            ),
            "event_log": snapshot.get("event_log"),
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
    lines = ["# Provider Runtime Heap Broker Bridge", ""]
    for key in (
        "passed",
        "dry_run",
        "stamp",
        "pending_broker_request_count",
        "broker_result_event_count",
        "broker_returncode",
        "broker_passed",
        "tool_request_count",
        "tool_execution_count",
        "blocked_tool_count",
        "failed_tool_count",
        "request_packet",
        "broker_report",
        "tool_output_dir",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument(
        "--bridge-dir", default="output/ai_runtime_heap/{stamp}/broker_bridge"
    )
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--max-requests", type=int, default=0)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(
        repo_root, args.markdown_output.format(stamp=args.stamp)
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
