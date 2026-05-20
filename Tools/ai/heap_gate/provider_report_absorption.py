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
    provider_report["budget_counter_seconds"] = item.get("budget_counter_seconds")
    provider_report["soft_close_after_seconds"] = item.get("soft_close_after_seconds")
    provider_report["watchdog_timeout_seconds"] = item.get("watchdog_timeout_seconds")
    provider_report["time_counter_contract"] = item.get("time_counter_contract")
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
    provider_report["execution_mode"] = "provider_teamwork_unified_parallel"
    provider_report["revision"] = revision
    provider_report["report_passed"] = bool(provider_report.get("passed"))
    provider_report["diagnostic_only"] = not bool(
        provider_report.get("operational_provider_activity")
    )
    provider_report["status"] = "ready" if completed.returncode == 0 else "failed"
    normalized_output = dict(report_data) if isinstance(report_data, dict) else {}
    normalized_output.update(provider_report)
    write_json_report(normalized_output, Path(spec["output"]))
    item["provider_report"] = provider_report
    gate.provider_reports.append(provider_report)
    append_unique(gate.state["provider_results"], provider_report, key="requirement")
    _publish_provider_report(gate, lane, requirement, correlation, provider_report, round_id, revision)
    item["absorbed"] = True
    return True


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
            watchdog = float(
                item.get("watchdog_timeout_seconds")
                or item.get("timeout_seconds")
                or timeout_seconds
            )
            stdout, stderr = process.communicate(timeout=None if watchdog <= 0 else watchdog)
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(command, process.returncode, stdout or "", stderr or "")
        except subprocess.TimeoutExpired:
            terminate_process_tree(process)
            stdout, stderr = process.communicate()
            item["completed_at"] = now_iso()
            completed = subprocess.CompletedProcess(
                command, 124, stdout or "", (stderr or "") + "\nprovider watchdog timeout"
            )
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
        "provider_evidence",
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
            "execution_mode": "provider_teamwork_unified_parallel",
            "started_at": provider_report.get("started_at"),
            "completed_at": provider_report.get("completed_at"),
            "elapsed_seconds": provider_report.get("elapsed_seconds"),
            "budget_counter_seconds": provider_report.get("budget_counter_seconds"),
            "soft_close_after_seconds": provider_report.get("soft_close_after_seconds"),
            "watchdog_timeout_seconds": provider_report.get("watchdog_timeout_seconds"),
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
    payload = {
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
        "operational_provider_activity": provider_report.get("operational_provider_activity"),
    }
    if lane == "npu_micro_task_auditor":
        payload["npu_micro_provider_execution_performed"] = provider_report.get(
            "npu_micro_provider_execution_performed"
        )
    else:
        payload["semantic_provider_execution_performed"] = provider_report.get(
            "semantic_provider_execution_performed"
        )
    return payload


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
            else "provider lane produced non-operational evidence only"
        ),
        "confidence": 0.88 if operational else 0.2,
        "requirement": requirement,
        "evidence_ref": provider_report.get("output"),
        "provider_execution_performed": provider_report.get("provider_execution_performed"),
        "operational_provider_activity": operational,
        "provider_activity_classification": provider_report.get("provider_activity_classification"),
        "leader_packet": provider_report.get("leader_packet"),
        "observed_request": gate.request_text(),
        "observed_response": provider_report.get("response_text") or gate.response_text(),
        "execution_mode": "provider_teamwork_unified_parallel",
    }
    if lane == "npu_micro_task_auditor":
        claim["npu_micro_provider_execution_performed"] = provider_report.get(
            "npu_micro_provider_execution_performed"
        )
    else:
        claim["semantic_provider_execution_performed"] = provider_report.get(
            "semantic_provider_execution_performed"
        )
    append_unique(gate.state["claims"], claim)
    gate.publish(
        provider_heap_lane(lane),
        "claim",
        claim,
        target="deterministic",
        correlation_id=f"{correlation}:claim",
        round_id=round_id,
    )
