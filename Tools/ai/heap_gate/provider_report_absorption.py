"""Absorb completed provider lane reports into the same heap graph."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    append_unique,
    now_iso,
    provider_heap_lane,
    read_json,
    repo_rel,
    subprocess,
    terminate_process_tree,
    write_json_report,
)


def absorb_completed_provider_item(
    gate: Any,
    item: dict[str, Any],
    *,
    launch_manifest: Path,
    work_dir: Path,
    round_id: int,
    revision: int,
    timeout_seconds: int,
) -> bool:
    if item.get("absorbed"):
        return False
    spec = item["spec"]
    lane = str(item["lane"])
    requirement = str(item["requirement"])
    correlation = str(item["correlation"])
    command = list(item["command"])
    completed = _completed_process(item, command, timeout_seconds)
    report_data = read_json(Path(spec["output"]))
    provider_report = gate.summarize_provider_report(spec, completed, report_data)
    provider_report["started_at"] = item.get("started_at")
    provider_report["completed_at"] = item.get("completed_at")
    provider_report["elapsed_seconds"] = item.get("elapsed_seconds")
    provider_report["provider_process_id"] = item.get("pid")
    provider_report["launch_manifest"] = repo_rel(gate.repo_root, launch_manifest)
    provider_report["leader_packet"] = gate.provider_leader_packet_path
    provider_report = gate.enrich_provider_report_with_operational_peer_review(
        provider_report,
        lane,
        work_dir,
        revision,
        gate.read_events(),
    )
    provider_report.update(gate.provider_block_contract(lane, revision, provider_report))
    provider_report["execution_mode"] = "concurrent_provider_teamwork"
    provider_report["revision"] = revision
    if not provider_report.get("operational_provider_activity"):
        provider_report["passed"] = False
    provider_report["status"] = "ready" if provider_report.get("passed") else "degraded"
    normalized_output = dict(report_data) if isinstance(report_data, dict) else {}
    normalized_output.update(provider_report)
    write_json_report(normalized_output, Path(spec["output"]))
    gate.provider_reports.append(provider_report)
    append_unique(gate.state["provider_results"], provider_report, key="requirement")
    _publish_provider_report(gate, lane, requirement, correlation, provider_report, round_id, revision)
    item["absorbed"] = True
    return True


def refresh_peer_reports_after_provider_join(
    gate: Any,
    *,
    work_dir: Path,
    round_id: int,
    revision: int,
) -> None:
    """Rebind peer reports to the final GPU1 delta after all provider lanes join."""
    for provider_report in gate.provider_reports:
        lane = str(provider_report.get("lane") or "")
        if lane not in {"gpu0_peer", "npu_micro_task_auditor"}:
            continue
        was_operational = bool(provider_report.get("operational_provider_activity"))
        refreshed = gate.enrich_provider_report_with_operational_peer_review(
            dict(provider_report),
            lane,
            work_dir,
            revision,
            gate.read_events(),
        )
        refreshed.update(gate.provider_block_contract(lane, revision, refreshed))
        if not refreshed.get("operational_provider_activity"):
            refreshed["passed"] = False
        refreshed["status"] = "ready" if refreshed.get("passed") else "degraded"
        provider_report.clear()
        provider_report.update(refreshed)
        output = str(provider_report.get("output") or "")
        if output:
            output_path = gate.repo_root / output
            existing = read_json(output_path)
            merged = existing if isinstance(existing, dict) else {}
            merged.update(provider_report)
            write_json_report(merged, output_path)
        if provider_report.get("operational_provider_activity") and not was_operational:
            gate.publish(
                provider_heap_lane(lane),
                "provider_peer_block",
                _provider_peer_block_payload(lane, revision, provider_report),
                target="orchestrator",
                correlation_id=f"{gate.stamp}:provider:{lane}:refreshed-block",
                round_id=round_id,
            )
        gate.append_heap_exchange_event(
            {
                "kind": "provider_peer_rebound",
                "lane": lane,
                "round": round_id,
                "revision": revision,
                "provider_block_id": provider_report.get("provider_block_id"),
                "proposal_block_id": provider_report.get("proposal_block_id"),
                "refines_block_id": provider_report.get("refines_block_id"),
                "resume_from_block_id": provider_report.get("resume_from_block_id"),
                "operational_provider_activity": provider_report.get(
                    "operational_provider_activity"
                ),
                "summary": "peer report rebound against final GPU1 delta before proposal iteration",
            }
        )


def _completed_process(
    item: dict[str, Any],
    command: list[str],
    timeout_seconds: int,
) -> subprocess.CompletedProcess[str]:
    completed = item.get("completed")
    process = item.get("process")
    if completed is not None:
        return completed
    if process is not None:
        try:
            stdout, stderr = process.communicate(timeout=float(item.get("timeout_seconds") or timeout_seconds))
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(command, process.returncode, stdout or "", stderr or "")
        except subprocess.TimeoutExpired:
            terminate_process_tree(process)
            stdout, stderr = process.communicate()
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(command, 124, stdout or "", (stderr or "") + "\nprovider timeout")
    if completed is None:
        completed = subprocess.CompletedProcess(
            command,
            127,
            "",
            "provider process was not started and no completed process was recorded",
        )
    item["completed"] = completed
    return completed


def _publish_provider_report(
    gate: Any,
    lane: str,
    requirement: str,
    correlation: str,
    provider_report: dict[str, Any],
    round_id: int,
    revision: int,
) -> None:
    gate.publish(
        provider_heap_lane(lane),
        "telemetry_signal",
        provider_report,
        target="orchestrator",
        correlation_id=correlation,
        round_id=round_id,
    )
    if provider_report.get("operational_provider_activity"):
        gate.publish(
            provider_heap_lane(lane),
            "provider_peer_block",
            _provider_peer_block_payload(lane, revision, provider_report),
            target="orchestrator",
            correlation_id=f"{correlation}:block",
            round_id=round_id,
        )
    gate.append_heap_exchange_event(
        {
            "kind": "provider_output",
            "lane": lane,
            "round": round_id,
            "requirement": requirement,
            "revision": revision,
            "execution_mode": "concurrent_provider_teamwork",
            "started_at": provider_report.get("started_at"),
            "completed_at": provider_report.get("completed_at"),
            "elapsed_seconds": provider_report.get("elapsed_seconds"),
            "provider_process_id": provider_report.get("provider_process_id"),
            "provider_block_id": provider_report.get("provider_block_id"),
            "proposal_block_id": provider_report.get("proposal_block_id"),
            "block_type": provider_report.get("block_type"),
            "passed": provider_report.get("passed"),
            "operational_provider_activity": provider_report.get("operational_provider_activity"),
            "provider_activity_classification": provider_report.get("provider_activity_classification"),
            "source_file": provider_report.get("output"),
            "summary": str(provider_report.get("response_text") or "")[:500],
        }
    )
    _publish_claim(gate, lane, requirement, correlation, provider_report, round_id)


def _provider_peer_block_payload(
    lane: str,
    revision: int,
    provider_report: dict[str, Any],
) -> dict[str, Any]:
    return {
        "kind": "provider_peer_block",
        "lane": lane,
        "revision": revision,
        "provider_block_id": provider_report.get("provider_block_id"),
        "proposal_block_id": provider_report.get("proposal_block_id"),
        "role": provider_report.get("role"),
        "block_type": provider_report.get("block_type"),
        "pointer_action": provider_report.get("pointer_action"),
        "refines_block_id": provider_report.get("refines_block_id"),
        "resume_from_block_id": provider_report.get("resume_from_block_id"),
        "target_files": provider_report.get("target_files") or [],
        "decision": provider_report.get("decision"),
        "provider_report": provider_report.get("output"),
        "native_tool_call_count": provider_report.get("native_tool_call_count"),
        "semantic_provider_execution_performed": provider_report.get("semantic_provider_execution_performed"),
        "operational_provider_activity": provider_report.get("operational_provider_activity"),
    }


def _publish_claim(
    gate: Any,
    lane: str,
    requirement: str,
    correlation: str,
    provider_report: dict[str, Any],
    round_id: int,
) -> None:
    operational = bool(provider_report.get("operational_provider_activity"))
    claim = {
        "id": f"{requirement}_claim",
        "from": lane,
        "claim": (
            "provider lane contributed operational heap evidence"
            if operational
            else "provider lane produced diagnostic evidence only"
        ),
        "confidence": 0.88 if operational else 0.2,
        "requirement": requirement,
        "evidence_ref": provider_report.get("output"),
        "provider_execution_performed": provider_report.get("provider_execution_performed"),
        "semantic_provider_execution_performed": provider_report.get("semantic_provider_execution_performed"),
        "operational_provider_activity": operational,
        "provider_activity_classification": provider_report.get("provider_activity_classification"),
        "leader_packet": provider_report.get("leader_packet"),
        "observed_request": gate.request_text(),
        "observed_response": provider_report.get("response_text") or gate.response_text(),
        "execution_mode": "concurrent_provider_teamwork",
    }
    append_unique(gate.state["claims"], claim)
    gate.publish(
        provider_heap_lane(lane),
        "claim",
        claim,
        target="deterministic",
        correlation_id=f"{correlation}:claim",
        round_id=round_id,
    )
