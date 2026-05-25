"""GPU1 primary evidence capture helpers."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.provider_execution_checks import (
    gpu1_primary_evidence_status,
    gpu1_primary_workload_status,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, read_json, write_json_report
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    publish_provider_report_native_tool_calls,
)


def capture_gpu1_primary_evidence_after_provider_join(
    self, leader_report: dict[str, Any], round_id: int
) -> dict[str, Any]:
    workload = gpu1_primary_workload_status(leader_report, repo_root=self.repo_root)
    self.gpu1_primary_workload_valid = bool(
        workload.get("gpu1_primary_workload_valid")
    )
    self.gpu1_primary_workload_chars = int(
        workload.get("gpu1_primary_workload_chars") or 0
    )
    self.gpu1_primary_workload_tokens = int(
        workload.get("gpu1_primary_workload_tokens") or 0
    )
    replight_reports = list(getattr(self, "provider_replight_reports", []) or [])
    self.gpu1_replight_valid = any(
        str(report.get("lane") or report.get("provider_id") or "") == "gpu1_planner"
        and report.get("replight_passed") is True
        for report in replight_reports
        if isinstance(report, dict)
    )
    events = self.read_events()
    if self.gpu1_primary_workload_valid:
        published = publish_provider_report_native_tool_calls(
            self, leader_report, round_id, events
        )
        if published and self.heap.pending_broker_requests():
            self.run_bridge()
            events = self.read_events()
    evidence = gpu1_primary_evidence_status(self, leader_report, events)
    self.gpu1_primary_evidence_valid = bool(
        evidence.get("gpu1_primary_evidence_valid")
    )
    self.gpu1_primary_evidence_source = str(
        evidence.get("gpu1_primary_evidence_source") or ""
    )
    self.leader_source = str(evidence.get("leader_source") or "none")
    self.gpu1_waiting_for_tool_result = bool(
        evidence.get("gpu1_waiting_for_tool_result")
    )
    self.gpu1_requested_tool_call_id = str(
        evidence.get("gpu1_requested_tool_call_id") or ""
    )
    self.gpu1_requested_tool_name = str(
        evidence.get("gpu1_requested_tool_name") or ""
    )
    self.gpu1_resume_after_tool_result_required = bool(
        evidence.get("gpu1_resume_after_tool_result_required")
    )
    self.gpu1_consumed_tool_result_ids = [
        str(item)
        for item in (evidence.get("gpu1_consumed_tool_result_ids") or [])
        if str(item).strip()
    ]
    self.gpu1_tool_result_pending_ids = [
        str(item)
        for item in (evidence.get("gpu1_tool_result_pending_ids") or [])
        if str(item).strip()
    ]
    self.gpu1_unconsumed_tool_result_ids = [
        str(item)
        for item in (evidence.get("gpu1_unconsumed_tool_result_ids") or [])
        if str(item).strip()
    ]
    if not self.gpu1_primary_workload_valid:
        block_reason = "gpu1_primary_workload_missing"
    elif evidence.get("gpu1_resume_after_tool_result_required"):
        block_reason = str(
            evidence.get("gpu1_tool_result_blocker")
            or "gpu1_requested_tool_result_not_consumed"
        )
    elif evidence.get("gpu1_generic_write_capture_failed"):
        block_reason = "generic_write_capture_failed"
    elif not self.gpu1_primary_evidence_valid:
        block_reason = "gpu1_primary_evidence_missing"
    else:
        block_reason = ""
    leader_report.update(
        {
            **workload,
            **evidence,
            "gpu1_replight_valid": self.gpu1_replight_valid,
            "gpu1_boot_leader_ready": bool(
                getattr(self, "gpu1_boot_leader_ready", False)
            ),
            "sidecars_start_policy": str(
                getattr(self, "sidecars_start_policy", "") or ""
            ),
            "parallel_provider_overlap_seconds": getattr(
                self, "parallel_provider_overlap_seconds", 0.0
            ),
            "gpu1_primary_block_reason": block_reason,
        }
    )
    output_ref = str(leader_report.get("output") or "")
    if output_ref:
        output_path = Path(output_ref)
        if not output_path.is_absolute():
            output_path = self.repo_root / output_path
        if output_path.exists():
            persisted = read_json(output_path)
            persisted.update(leader_report)
            write_json_report(persisted, output_path)
    self.publish(
        "gpu1",
        "validation_signal",
        {
            "kind": "gpu1_primary_evidence_gate",
            "provider_block_id": leader_report.get("provider_block_id"),
            "proposal_block_id": leader_report.get("proposal_block_id"),
            "revision": leader_report.get("revision"),
            **workload,
            **evidence,
            "gpu1_replight_valid": self.gpu1_replight_valid,
            "gpu1_boot_leader_ready": bool(
                getattr(self, "gpu1_boot_leader_ready", False)
            ),
            "sidecars_start_policy": str(
                getattr(self, "sidecars_start_policy", "") or ""
            ),
            "parallel_provider_overlap_seconds": getattr(
                self, "parallel_provider_overlap_seconds", 0.0
            ),
            "block_reason": block_reason,
        },
        target="orchestrator",
        correlation_id=f"{self.stamp}:gpu1-primary-evidence:{leader_report.get('revision')}",
        round_id=round_id,
    )
    return {**workload, **evidence, "block_reason": block_reason}
