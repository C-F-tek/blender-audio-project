"""Smoke checks for GPU1 primary evidence gating."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def run_provider_loop_primary_evidence_checks(repo_root: Path) -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_execution_checks import (
        gpu1_primary_evidence_status,
        gpu1_primary_workload_status,
    )

    errors: list[str] = []
    replight_report = _gpu1_report(
        response_text='{"ok": true, "lane": "ollama"}',
        replight_mode=True,
        provider_stage="health_check_only",
    )
    if gpu1_primary_workload_status(replight_report)["gpu1_primary_workload_valid"]:
        errors.append("GPU1 replight/handshake report can still become primary workload")

    text_report = _gpu1_report(response_text="GPU1 primary text without native tools")
    missing = gpu1_primary_evidence_status(None, text_report, [])
    if missing["gpu1_primary_evidence_valid"]:
        errors.append("GPU1 text without broker evidence can still become primary evidence")

    generic_events = [
        _broker_result(
            tool="generic_write",
            lane="gpu1_planner",
            revision=0,
            returncode=0,
            summary={"passed": True},
            outputs={"json_report": "output/validation/gpu1_generic_write.json"},
        )
    ]
    generic = gpu1_primary_evidence_status(None, text_report, generic_events)
    if not generic["gpu1_primary_evidence_valid"]:
        errors.append("valid GPU1 generic_write is not counted as primary evidence")
    if generic["leader_source"] != "generic_write":
        errors.append("GPU1 generic_write evidence did not set leader_source=generic_write")

    native_events = [
        _broker_result(
            tool="runtime_file_refs",
            lane="gpu1_planner",
            revision=0,
            returncode=0,
            summary={"passed": True},
            provider_native_tool_call=True,
            provider_block_id="test:gpu1_planner:000",
        )
    ]
    native_report = dict(text_report)
    native_report["native_tool_call_count"] = 1
    native_report["provider_block_id"] = "test:gpu1_planner:000"
    native = gpu1_primary_evidence_status(None, native_report, native_events)
    if native["leader_source"] != "native_tool_result":
        errors.append("GPU1 native tool evidence did not set leader_source=native_tool_result")

    fake_native = gpu1_primary_evidence_status(None, text_report, native_events)
    if fake_native["leader_source"] == "native_tool_result":
        errors.append("GPU1 native_tool_result is still valid when native_tool_call_count is 0")

    failed_events = [
        _broker_result(
            tool="generic_write",
            lane="gpu1_planner",
            revision=0,
            returncode=2,
            errors=["generic_write: unsupported args"],
        )
    ]
    failed = gpu1_primary_evidence_status(None, text_report, failed_events)
    if not failed["gpu1_generic_write_capture_failed"]:
        errors.append("failed GPU1 generic_write capture is not exposed")

    execution_source = (
        repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py"
    ).read_text(encoding="utf-8", errors="replace")
    required = [
        "capture_gpu1_primary_evidence_after_provider_join",
        "capture_gpu1_primary_evidence_before_sidecars",
        "gpu1_primary_evidence_missing",
        "generic_write_capture_failed",
        "async_sidecars_started_after_gpu1_packet",
        "publish_provider_report_native_tool_calls",
    ]
    for marker in required:
        if marker not in execution_source:
            errors.append(f"provider execution is missing marker: {marker}")
    if "gpu1_leader_missing_before_sidecars" in execution_source:
        errors.append("provider execution still blocks sidecars on final GPU1 evidence")
    return {"name": "provider_loop_primary_evidence", "errors": errors}


def _gpu1_report(
    *,
    response_text: str,
    replight_mode: bool = False,
    provider_stage: str = "verified_provider_work",
) -> dict[str, Any]:
    return {
        "lane": "gpu1_planner",
        "revision": 0,
        "passed": True,
        "response_text": response_text,
        "replight_mode": replight_mode,
        "provider_stage": provider_stage,
        "provider_work_verified": True,
        "completion_token_count": 128,
        "provider_block_id": "test:gpu1_planner:000",
    }


def _broker_result(
    *,
    tool: str,
    lane: str,
    revision: int,
    returncode: int,
    summary: dict[str, Any] | None = None,
    errors: list[str] | None = None,
    outputs: dict[str, Any] | None = None,
    provider_native_tool_call: bool = False,
    provider_block_id: str = "test:gpu1_planner:000",
) -> dict[str, Any]:
    return {
        "event_type": "broker_result",
        "payload": {
            "tool": tool,
            "lane": lane,
            "revision": revision,
            "returncode": returncode,
            "executed": returncode == 0,
            "summary": summary or {},
            "errors": errors or [],
            "outputs": outputs or {},
            "provider_native_tool_call": provider_native_tool_call,
            "provider_block_id": provider_block_id,
        },
    }
