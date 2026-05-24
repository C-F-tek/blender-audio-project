#!/usr/bin/env python3
"""Bridge provider-runtime heap broker requests into the existing broker.

This adapter keeps provider lanes conversational through the shared heap while
preserving the existing rule: tools are executed only by
the runtime broker executor.
"""

from __future__ import annotations

import argparse
import json
import sys
from argparse import Namespace
from datetime import datetime
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from ia_carmine.runtime.provider_runtime_blackboard import ProviderRuntimeHeap, safe_dict
from ia_carmine.runtime.provider_runtime_blackboard.common import resolve_output_path
from ia_carmine.runtime.runtime_tool.broker.executor import build_report as build_broker_report
from ia_carmine.runtime.runtime_tool.broker.markdown import render_markdown as render_broker_markdown
from ia_carmine._shared.file_backed_transport import (
    artifact_ref,
    file_sha256,
    read_json_windows_safe,
    resolve_path as resolve_transport_path,
    write_json_artifact,
    write_transport_manifest,
)
from Tools.validation._shared.report_utils import write_json_report, write_text_report

DEFAULT_OUTPUT = "output/validation/provider_runtime_broker_bridge_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/provider_runtime_broker_bridge_{stamp}.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def safe_id(value: Any, fallback: str) -> str:
    text = str(value or fallback).strip()
    keep = []
    for char in text:
        keep.append(char if char.isalnum() or char in "._-" else "_")
    normalized = "".join(keep).strip("._-")
    return normalized[:96] or fallback


def _payload_from_ref(repo_root: Path, event: dict[str, Any]) -> dict[str, Any]:
    payload = safe_dict(event.get("payload"))
    payload_ref = safe_dict(event.get("payload_ref")) or safe_dict(payload.get("payload_ref"))
    ref_path = str(payload_ref.get("path") or "").strip()
    if not ref_path:
        return payload
    try:
        target = resolve_transport_path(repo_root, ref_path)
        if not target.is_file():
            return {**payload, "_payload_ref_error": f"payload_ref_missing:{ref_path}"}
        expected_bytes = int(payload_ref.get("bytes") or 0)
        expected_sha = str(payload_ref.get("sha256") or "").strip()
        actual_bytes = target.stat().st_size
        actual_sha = file_sha256(target)
        if expected_bytes and actual_bytes != expected_bytes:
            return {**payload, "_payload_ref_error": f"payload_ref_bytes_mismatch:{ref_path}"}
        if expected_sha and actual_sha != expected_sha:
            return {**payload, "_payload_ref_error": f"payload_ref_sha256_mismatch:{ref_path}"}
        hydrated = read_json_windows_safe(target)
    except Exception as exc:  # noqa: BLE001 - bridge report preserves typed failure.
        return {
            **payload,
            "_payload_ref_error": f"payload_ref_unreadable:{ref_path}:{type(exc).__name__}:{exc}",
        }
    return {**payload, **hydrated, "payload_ref": payload_ref}


def event_to_tool_request(repo_root: Path, event: dict[str, Any], index: int) -> dict[str, Any]:
    payload = _payload_from_ref(repo_root, event)
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
        "nonblocking": bool(payload.get("nonblocking") or payload.get("optional")),
        "source": str(event.get("source") or "provider_runtime_blackboard"),
        "lane": str(payload.get("lane") or payload.get("owner") or event.get("source") or ""),
        "revision": payload.get("revision"),
        "provider_native_tool_call": bool(payload.get("provider_native_tool_call")),
        "provider_report": str(payload.get("provider_report") or ""),
        "provider_block_id": str(payload.get("provider_block_id") or ""),
        "proposal_block_id": str(payload.get("proposal_block_id") or ""),
        "native_tool_call_authority": str(payload.get("native_tool_call_authority") or ""),
        "tool_result_scope": str(payload.get("tool_result_scope") or ""),
        "payload_ref_error": str(payload.get("_payload_ref_error") or ""),
        "gpu1_followup_required": bool(payload.get("gpu1_followup_required")),
        "cannot_close_product": bool(payload.get("cannot_close_product")),
        "peer_only": bool(payload.get("peer_only")),
        "capture_mode": str(safe_dict(payload.get("args")).get("capture_mode") or ""),
        "heap_event": {
            "source": event.get("source"),
            "target": event.get("target"),
            "round": event.get("round"),
            "event_type": event.get("event_type"),
            "correlation_id": event.get("correlation_id"),
        },
    }


def build_request_packet(
    repo_root: Path, stamp: str, pending: list[dict[str, Any]]
) -> dict[str, Any]:
    tool_requests = [
        event_to_tool_request(repo_root, event, index)
        for index, event in enumerate(pending, start=1)
    ]
    packet = {
        "schema_version": 1,
        "kind": "agent_runtime_tool_requests",
        "generated_at": now_iso(),
        "stamp": stamp,
        "source": "provider_runtime_blackboard",
        "source_classification": "provider_runtime_broker_bridge",
        "tool_requests": tool_requests,
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    return packet


def run_broker(
    *,
    repo_root: Path,
    stamp: str,
    payload_file: Path,
    tool_output_dir: Path,
    broker_output: Path,
    broker_markdown: Path,
    timeout_seconds: int,
    dry_run: bool,
) -> tuple[int, str, str, dict[str, Any]]:
    broker_args = Namespace(
        repo_root=str(repo_root),
        request_data=None,
        request_packet=None,
        request_file="",
        request_json="",
        payload_file=repo_rel(repo_root, payload_file),
        job_id=stamp,
        tool_output_dir=repo_rel(repo_root, tool_output_dir),
        stamp=stamp,
        timeout_seconds=timeout_seconds,
        dry_run=dry_run,
    )
    broker_report = build_broker_report(broker_args)
    write_json_report(broker_report, broker_output)
    write_text_report(render_broker_markdown(broker_report), broker_markdown)
    stdout_tail = json.dumps(
        {
            "passed": broker_report.get("passed"),
            "tool_request_count": broker_report.get("tool_request_count"),
            "tool_execution_count": broker_report.get("tool_execution_count"),
            "blocked_tool_count": broker_report.get("blocked_tool_count"),
            "failed_tool_count": broker_report.get("failed_tool_count"),
        },
        ensure_ascii=False,
    )
    return 0 if broker_report.get("passed") else 2, stdout_tail, "", broker_report


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def broker_result_target_from_source(value: object) -> str:
    lane = str(value or "").strip().lower()
    if lane in {
        "gpu1",
        "gpu0",
        "npu",
        "broker",
        "deterministic",
        "orchestrator",
    }:
        return lane
    return "orchestrator"


def broker_report_tool_requests(repo_root: Path, broker_report: dict[str, Any]) -> list[dict[str, Any]]:
    requests = broker_report.get("tool_requests")
    if isinstance(requests, list):
        return [item for item in requests if isinstance(item, dict)]
    ref = safe_dict(broker_report.get("tool_requests_ref"))
    ref_path = str(ref.get("path") or "").strip()
    if ref_path:
        try:
            payload = read_json_windows_safe(resolve_transport_path(repo_root, ref_path))
            requests = payload.get("tool_requests")
            if isinstance(requests, list):
                return [item for item in requests if isinstance(item, dict)]
        except Exception:
            return []
    return []


def request_sources_by_id(repo_root: Path, broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report_tool_requests(repo_root, broker_report):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        if not request_id:
            continue
        heap_event = safe_dict(request.get("heap_event"))
        source = request.get("source") or heap_event.get("source") or "orchestrator"
        mapping[request_id] = broker_result_target_from_source(source)
    return mapping


def request_requirements_by_id(repo_root: Path, broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report_tool_requests(repo_root, broker_report):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        requirement = str(request.get("requirement") or "")
        if request_id and requirement:
            mapping[request_id] = requirement
    return mapping


def request_correlations_by_id(repo_root: Path, broker_report: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for request in broker_report_tool_requests(repo_root, broker_report):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        heap_event = safe_dict(request.get("heap_event"))
        correlation_id = str(heap_event.get("correlation_id") or "")
        if request_id and correlation_id:
            mapping[request_id] = correlation_id
    return mapping


def request_payloads_by_id(repo_root: Path, broker_report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    mapping: dict[str, dict[str, Any]] = {}
    for request in broker_report_tool_requests(repo_root, broker_report):
        if not isinstance(request, dict):
            continue
        request_id = str(request.get("id") or request.get("request_id") or "")
        if request_id:
            mapping[request_id] = request
    return mapping


def mapped_request_value(mapping: dict[str, str], result_id: str, default: str = "") -> str:
    if result_id in mapping:
        return mapping[result_id]
    for request_id, value in mapping.items():
        if request_id.startswith(result_id) or result_id.startswith(request_id):
            return value
    return default


def mapped_request_payload(
    mapping: dict[str, dict[str, Any]], result_id: str
) -> dict[str, Any]:
    if result_id in mapping:
        return mapping[result_id]
    for request_id, payload in mapping.items():
        if request_id.startswith(result_id) or result_id.startswith(request_id):
            return payload
    return {}


def resolve_ref(repo_root: Path, value: object) -> Path:
    path = Path(str(value or ""))
    return path if path.is_absolute() else repo_root / path


def read_output_report(repo_root: Path, outputs: object) -> dict[str, Any]:
    data = safe_dict(outputs)
    report_ref = str(data.get("json_report") or "")
    if not report_ref:
        return {}
    return read_json(resolve_ref(repo_root, report_ref))


def hydrate_generic_write_payload(
    repo_root: Path,
    result: dict[str, Any],
    request_payload: dict[str, Any],
) -> dict[str, Any]:
    outputs = safe_dict(result.get("outputs"))
    report = read_output_report(repo_root, outputs)
    provider_summary = safe_dict(report.get("provider_summary"))
    provider_report_ref = (
        request_payload.get("provider_report")
        or report.get("provider_report")
        or provider_summary.get("provider_report")
    )
    provider_report = read_json(resolve_ref(repo_root, provider_report_ref))
    lane = (
        request_payload.get("lane")
        or report.get("source_lane")
        or provider_summary.get("lane")
        or provider_report.get("lane")
    )
    revision = request_payload.get("revision")
    if revision is None:
        revision = (
            report.get("source_revision")
            or provider_summary.get("revision")
            or provider_report.get("revision")
        )
    followup = request_payload.get("gpu1_followup_required")
    if followup is None:
        followup = report.get("gpu1_followup_required")
    if followup is None:
        followup = str(lane or "") in {"gpu0_peer", "npu_micro_task_auditor"}
    return {
        **request_payload,
        "lane": lane,
        "revision": revision,
        "provider_report": provider_report_ref or request_payload.get("provider_report"),
        "provider_block_id": request_payload.get("provider_block_id")
        or provider_summary.get("provider_block_id")
        or provider_report.get("provider_block_id"),
        "proposal_block_id": request_payload.get("proposal_block_id")
        or provider_summary.get("proposal_block_id")
        or provider_report.get("proposal_block_id"),
        "gpu1_followup_required": bool(followup),
        "peer_only": request_payload.get("peer_only")
        if request_payload.get("peer_only") is not None
        else str(lane or "") in {"gpu0_peer", "npu_micro_task_auditor"},
        "capture_mode": request_payload.get("capture_mode") or report.get("capture_mode"),
    }


def append_broker_results(
    heap: ProviderRuntimeHeap, broker_report: dict[str, Any], repo_root: Path
) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    source_by_request_id = request_sources_by_id(repo_root, broker_report)
    correlation_by_request_id = request_correlations_by_id(repo_root, broker_report)
    requirement_by_request_id = request_requirements_by_id(repo_root, broker_report)
    payload_by_request_id = request_payloads_by_id(repo_root, broker_report)
    for result in broker_report.get("tool_results", []):
        if not isinstance(result, dict):
            continue
        result_id = str(result.get("id") or result.get("request_id") or "")
        result_correlation_id = mapped_request_value(
            correlation_by_request_id, result_id, result_id
        )
        target_lane = mapped_request_value(source_by_request_id, result_id, "orchestrator")
        requirement = str(
            result.get("requirement")
            or mapped_request_value(requirement_by_request_id, result_id, "")
        )
        request_payload = mapped_request_payload(payload_by_request_id, result_id)
        if str(result.get("tool") or "") == "generic_write":
            request_payload = hydrate_generic_write_payload(
                repo_root, result, request_payload
            )
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
                "requirement": requirement,
                "lane": request_payload.get("lane"),
                "revision": request_payload.get("revision"),
                "provider_native_tool_call": request_payload.get("provider_native_tool_call"),
                "provider_report": request_payload.get("provider_report"),
                "provider_block_id": request_payload.get("provider_block_id"),
                "proposal_block_id": request_payload.get("proposal_block_id"),
                "native_tool_call_authority": request_payload.get("native_tool_call_authority"),
                "tool_result_scope": request_payload.get("tool_result_scope"),
                "gpu1_followup_required": request_payload.get("gpu1_followup_required"),
                "cannot_close_product": request_payload.get("cannot_close_product"),
                "peer_only": request_payload.get("peer_only"),
                "capture_mode": request_payload.get("capture_mode"),
                "executed": result.get("executed"),
                "blocked": result.get("blocked"),
                "returncode": result.get("returncode"),
                "outputs": result.get("outputs"),
                "summary": result.get("summary"),
                "guardrails": result.get("guardrails"),
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

    bridge_dir = resolve_output_path(repo_root, args.bridge_dir.format(stamp=args.stamp))
    broker_output = bridge_dir / "agent_runtime_tool_broker.json"
    broker_markdown = bridge_dir / "agent_runtime_tool_broker.md"
    tool_output_dir = bridge_dir / "tool_outputs"

    packet = build_request_packet(repo_root, args.stamp, pending)
    packet_ref = write_json_artifact(
        repo_root,
        bridge_dir,
        name="request_packet",
        payload=packet,
        kind="provider_runtime_broker_request_packet",
        producer="provider_runtime_broker_bridge",
    )
    packet_file = resolve_transport_path(repo_root, str(packet_ref.get("path") or ""))
    manifest_path = bridge_dir / "request_payload_manifest.json"
    write_transport_manifest(
        repo_root,
        manifest_path,
        job_id=args.stamp,
        run_dir=bridge_dir,
        refs=[packet_ref],
        extra={
            "input": {"request_packet_path": packet_ref.get("path")},
            "broker": {"request_packet_ref": packet_ref},
            "read_order": ["request_packet"],
        },
    )
    manifest_ref = artifact_ref(
        manifest_path,
        repo_root,
        kind="ia_carmine_runtime_payload_manifest",
        producer="provider_runtime_broker_bridge",
        ref_id="provider_runtime_broker_payload_manifest",
    )
    returncode = 0
    stdout_tail = ""
    stderr_tail = ""
    broker_report: dict[str, Any] = {}
    broker_result_events: list[dict[str, Any]] = []

    if pending:
        returncode, stdout_tail, stderr_tail, broker_report = run_broker(
            repo_root=repo_root,
            stamp=args.stamp,
            payload_file=manifest_path,
            tool_output_dir=tool_output_dir,
            broker_output=broker_output,
            broker_markdown=broker_markdown,
            timeout_seconds=args.timeout_seconds,
            dry_run=args.dry_run,
        )
        if broker_report:
            broker_report["output"] = repo_rel(repo_root, broker_output)
            broker_result_events = append_broker_results(heap, broker_report, repo_root)

    snapshot = heap.write_snapshot()
    errors: list[str] = []
    if returncode != 0:
        errors.append(f"agent_runtime_tool_broker returned {returncode}")
    if broker_report.get("errors"):
        errors.extend(str(item) for item in broker_report.get("errors", []))

    return {
        "schema_version": 1,
        "kind": "provider_runtime_broker_bridge",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "job_id": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "dry_run": bool(args.dry_run),
        "pending_broker_request_count": len(pending),
        "broker_result_event_count": len(broker_result_events),
        "request_packet": packet_ref.get("path") or "",
        "request_packet_ref": packet_ref,
        "request_payload_manifest": manifest_ref.get("path") or "",
        "request_payload_manifest_ref": manifest_ref,
        "payload_file": manifest_ref.get("path") or "",
        "request_transport": "payload_file",
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
            "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
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


def main() -> int:
    try:
        from ia_carmine._shared.provider_runtime_broker_bridge_cli import main as cli_main
    except ModuleNotFoundError:
        from ia_carmine._shared.provider_runtime_broker_bridge_cli import main as cli_main
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())
