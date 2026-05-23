"""RuntimeGateProviderExecutionMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

import time

from ia_carmine.runtime.heap_gate.provider_execution_checks import (
    gpu1_primary_evidence_status,
    gpu1_primary_workload_status,
    provider_overlap_seconds,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, now_iso, provider_heap_lane, read_json, repo_rel, subprocess, write_json_report
from ia_carmine.runtime.heap_gate.provider_block_contract import proposal_block_id_for_revision as make_proposal_block_id, provider_block_contract as build_provider_block_contract
from ia_carmine.runtime.heap_gate.provider_lane_policy import PRIMARY_LANE, lane_policy_payload, provider_lanes_for_revision
from ia_carmine.runtime.heap_gate.provider_coexistence_preflight import (
    enforce_provider_role_coexistence_preflight,
)
from ia_carmine.runtime.heap_gate.provider_lane_launch import start_provider_item, write_provider_launch_manifest
from ia_carmine.runtime.heap_gate.provider_process_collection import collect_provider_processes, terminate_pending_provider_processes
from ia_carmine._shared.provider_replight import provider_replight_failure_reason
from ia_carmine.runtime.heap_gate.provider_replight_gate import run_provider_replight_gate
from ia_carmine.runtime.heap_gate.provider_residency_preflight import wait_for_gpu1_residency_preflight
from ia_carmine.runtime.heap_gate.provider_report_absorption import absorb_completed_provider_item
from ia_carmine.runtime.heap_gate.provider_runtime_plan import write_provider_runtime_plan
from ia_carmine.runtime.heap_gate.provider_teamwork_packet import build_provider_teamwork_leader_packet
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import packet_from_report
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    publish_provider_report_native_tool_calls,
)
from ia_carmine.runtime.heap_gate.provider_universe_abort import (
    block_provider_universe_run,
    primary_provider_block_reason,
)


class RuntimeGateProviderExecutionMixin:
    def proposal_block_id_for_revision(self, revision: int) -> str:
        return make_proposal_block_id(self.stamp, revision)

    def provider_block_contract(
        self,
        lane: str,
        revision: int,
        provider_report: dict[str, Any],
    ) -> dict[str, Any]:
        return build_provider_block_contract(self.stamp, lane, revision, provider_report)

    def run_provider_teamwork(self, round_id: int, revision: int = 0) -> None:
        if self.provider_reports and revision <= 0:
            return

        work_dir = self.provider_work_dir()
        time_contract = self.provider_time_counter_contract()
        raw_watchdog = time_contract.get("watchdog_timeout_seconds")
        timeout_seconds = int(
            raw_watchdog if raw_watchdog not in ("", None) else max(30, self.args.timeout_seconds)
        )
        prepared: list[dict[str, Any]] = []
        suffix = f"_revision{revision}" if revision else ""
        launch_manifest = work_dir / f"provider_launch_manifest{suffix}.json"
        try:
            selected_lanes = provider_lanes_for_revision(self, revision)
            leader_prompt = self.gpu1_provider_prompt()
            leader_packet = work_dir / f"provider_teamwork_leader_packet{f'_revision{revision}' if revision else ''}.json"
            write_json_report(
                build_provider_teamwork_leader_packet(self, round_id, revision, leader_prompt),
                leader_packet,
            )
            self.provider_leader_packet_path = repo_rel(self.repo_root, leader_packet)
            self.provider_leader_prompt = leader_prompt
            write_provider_runtime_plan(
                self,
                work_dir,
                selected_lanes=selected_lanes,
                stage="provider_boot_gate_started",
            )
            if not enforce_provider_role_coexistence_preflight(
                self,
                work_dir,
                launch_manifest,
                prepared,
                round_id=round_id,
                revision=revision,
                selected_lanes=selected_lanes,
                time_contract=time_contract,
                reports=getattr(self, "provider_replight_reports", []),
            ):
                return
            write_provider_runtime_plan(
                self,
                work_dir,
                selected_lanes=selected_lanes,
                stage="before_gpu1_replight",
                reports=getattr(self, "provider_replight_reports", []),
            )
            replight_block_reason = run_provider_replight_gate(
                self,
                work_dir,
                round_id=round_id,
                revision=revision,
                selected_lanes=selected_lanes,
            )
            write_provider_runtime_plan(
                self,
                work_dir,
                selected_lanes=selected_lanes,
                stage="provider_replight_failed" if replight_block_reason else "provider_replight_passed",
                reports=getattr(self, "provider_replight_reports", []),
            )
            if replight_block_reason:
                block_provider_universe_run(self, replight_block_reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "provider_replight_failed_before_provider_loop",
                )
                return
            for spec in self.provider_command_specs(work_dir, revision=revision, selected_lanes=selected_lanes):
                lane = str(spec["lane"])
                requirement = str(spec["requirement"])
                correlation = f"{self.stamp}:provider:{requirement}"

                self.publish(
                    provider_heap_lane(lane),
                    "provider_state",
                    {
                        "id": correlation,
                        "lane": lane,
                        "role": spec.get("role"),
                        "requirement": requirement,
                        "revision": revision,
                        "provider_cycle_id": revision,
                        "revision_owner_lane": PRIMARY_LANE,
                        "gpu1_revision_owner": lane == PRIMARY_LANE,
                        "review_for_gpu1_cycle": revision if lane == "gpu0_peer" else None,
                        "audit_for_gpu1_cycle": revision
                        if lane == "npu_micro_task_auditor"
                        else None,
                        "cannot_open_revision": lane != PRIMARY_LANE,
                        "status": "preparing",
                        "output": repo_rel(self.repo_root, Path(spec["output"])),
                        "execution_mode": "provider_teamwork_unified_parallel",
                        "budget_counter_seconds": spec.get("budget_counter_seconds"),
                        "soft_close_after_seconds": spec.get("soft_close_after_seconds"),
                        "watchdog_timeout_seconds": spec.get("watchdog_timeout_seconds"),
                        "provider_backend": spec.get("provider_backend"),
                        "provider_compute_device": spec.get("provider_compute_device"),
                        "provider_device_policy": spec.get("provider_device_policy"),
                        "logical_lane": spec.get("logical_lane") or lane,
                        "provider_backend_device_id": spec.get("provider_backend_device_id"),
                        "windows_task_manager_device_hint": spec.get(
                            "windows_task_manager_device_hint"
                        ),
                        "vulkan_visible_device": spec.get("vulkan_visible_device"),
                        "vulkan_device_name": spec.get("vulkan_device_name"),
                        "vulkan_vendor_id": spec.get("vulkan_vendor_id"),
                        "device_identity_verified": spec.get("device_identity_verified"),
                        **lane_policy_payload(spec),
                    },
                    target="orchestrator",
                    correlation_id=correlation,
                    round_id=round_id,
                )

                command = [
                    (self.provider_leader_prompt if item == "__GPU1_CUMULATIVE_PROMPT__" else item)
                    for item in spec["command"]
                ]
                try:
                    command, provider_prompt_file = self.provider_command_with_prompt_file(
                        command, revision
                    )
                    if provider_prompt_file:
                        self.warnings.append(
                            f"provider GPU1 prompt written to prompt-file={provider_prompt_file}"
                        )

                    command, provider_command_wrapper = self.provider_command_for_windows(
                        command, revision
                    )
                    if provider_command_wrapper:
                        self.warnings.append(
                            f"provider command exceeded Windows argv limit; executed wrapper={provider_command_wrapper}"
                        )

                    prepared.append(
                        {
                            "spec": spec,
                            "lane": lane,
                            "requirement": requirement,
                            "correlation": correlation,
                            "command": command,
                            "revision": revision,
                            "review_for_gpu1_cycle": revision if lane == "gpu0_peer" else None,
                            "audit_for_gpu1_cycle": revision
                            if lane == "npu_micro_task_auditor"
                            else None,
                            "process": None,
                            "completed": None,
                            "prepare_error": "",
                            "started_at": "",
                            "completed_at": "",
                            "elapsed_seconds": None,
                            "timeout_seconds": spec.get("timeout_seconds", timeout_seconds),
                            "budget_counter_seconds": spec.get("budget_counter_seconds"),
                            "soft_close_after_seconds": spec.get("soft_close_after_seconds"),
                            "watchdog_timeout_seconds": spec.get("watchdog_timeout_seconds"),
                            **lane_policy_payload(spec),
                            "time_counter_contract": spec.get("time_counter_contract"),
                            "pid": None,
                        }
                    )
                except Exception as exc:  # noqa: BLE001 - provider lane failure becomes report evidence.
                    prepared.append(
                        {
                            "spec": spec,
                            "lane": lane,
                            "requirement": requirement,
                            "correlation": correlation,
                            "command": command,
                            "revision": revision,
                            "review_for_gpu1_cycle": revision if lane == "gpu0_peer" else None,
                            "audit_for_gpu1_cycle": revision
                            if lane == "npu_micro_task_auditor"
                            else None,
                            "process": None,
                            "completed": subprocess.CompletedProcess(
                                command,
                                returncode=127,
                                stdout="",
                                stderr=f"{type(exc).__name__}: {exc}",
                            ),
                            "prepare_error": f"{type(exc).__name__}: {exc}",
                            "started_at": "",
                            "completed_at": now_iso(),
                            "elapsed_seconds": 0.0,
                            "timeout_seconds": spec.get("timeout_seconds", timeout_seconds),
                            "budget_counter_seconds": spec.get("budget_counter_seconds"),
                            "soft_close_after_seconds": spec.get("soft_close_after_seconds"),
                            "watchdog_timeout_seconds": spec.get("watchdog_timeout_seconds"),
                            **lane_policy_payload(spec),
                            "time_counter_contract": spec.get("time_counter_contract"),
                            "pid": None,
                        }
                    )

            def absorb(item: dict[str, Any]) -> None:
                absorb_completed_provider_item(
                    self,
                    item,
                    launch_manifest=launch_manifest,
                    work_dir=work_dir,
                    round_id=round_id,
                    revision=revision,
                    timeout_seconds=timeout_seconds,
                )

            primary_items = [item for item in prepared if item.get("lane") == PRIMARY_LANE]
            sidecar_items = [item for item in prepared if item.get("lane") != PRIMARY_LANE]
            if not primary_items:
                reason = "provider_universe_primary_lane_not_prepared"
                block_provider_universe_run(self, reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "gpu1_manual_full_gpu_gate_missing",
                )
                return

            for item in primary_items:
                start_provider_item(self, item, round_id, revision)
            write_provider_launch_manifest(
                self,
                launch_manifest,
                prepared,
                round_id,
                revision,
                time_contract,
                "gpu1_leader_started_before_sidecars",
            )
            collect_provider_processes(
                self,
                primary_items,
                timeout_seconds,
                round_id,
                revision,
                on_completed=absorb,
            )
            for item in primary_items:
                if item.get("completed") is not None:
                    absorb(item)
            leader_report_for_packet = (
                primary_items[0].get("provider_report")
                if isinstance(primary_items[0].get("provider_report"), dict)
                else {}
            )
            self.current_gpu1_closure_decision_packet = packet_from_report(
                leader_report_for_packet,
                source="gpu1_provider_report_before_gpu0",
            )
            write_json_report(
                build_provider_teamwork_leader_packet(self, round_id, revision, leader_prompt),
                leader_packet,
            )
            self.sidecars_start_policy = "same_production_window_residency_checked_parallel"
            for item in sidecar_items:
                start_provider_item(self, item, round_id, revision)
            primary_start = primary_items[0].get("started_perf")
            if primary_start:
                self.provider_sidecars_start_after_gpu1_seconds = round(
                    time.perf_counter() - float(primary_start),
                    6,
                )
            write_provider_launch_manifest(
                self,
                launch_manifest,
                prepared,
                round_id,
                revision,
                time_contract,
                "production_provider_window_all_lanes_started_before_residency_result",
            )
            preflight = wait_for_gpu1_residency_preflight(self, primary_items[0])
            self.gpu1_residency_preflight = preflight
            write_provider_launch_manifest(
                self,
                launch_manifest,
                prepared,
                round_id,
                revision,
                time_contract,
                "gpu1_replight_preflight_passed"
                if preflight.get("passed")
                else "gpu1_replight_preflight_blocked_before_sidecars",
            )
            if not preflight.get("passed"):
                primary_block_reason = str(
                    preflight.get("replight_blocked_reason")
                    or preflight.get("product_blocked_reason")
                    or preflight.get("status")
                    or "provider_replight_failed:gpu1_planner"
                )
                terminate_pending_provider_processes(
                    self,
                    prepared,
                    round_id,
                    revision,
                    f"GPU1 residency preflight failed during production window: {primary_block_reason}",
                )
                for item in prepared:
                    if item.get("completed") is not None:
                        absorb(item)
                block_provider_universe_run(self, primary_block_reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "gpu1_replight_preflight_blocked_before_sidecars",
                )
                return

            self.gpu1_boot_leader_ready = True
            write_json_report(
                build_provider_teamwork_leader_packet(self, round_id, revision, leader_prompt),
                leader_packet,
            )
            write_provider_launch_manifest(
                self,
                launch_manifest,
                prepared,
                round_id,
                revision,
                time_contract,
                "parallel_sidecars_running_after_gpu1_residency_handshake",
            )
            for item in sidecar_items:
                if item.get("completed") is not None:
                    absorb(item)
            collect_provider_processes(
                self,
                prepared,
                timeout_seconds,
                round_id,
                revision,
                on_completed=absorb,
            )
            self.parallel_provider_overlap_seconds = provider_overlap_seconds(
                primary_items, sidecar_items
            )
            if (
                sidecar_items
                and self.parallel_provider_overlap_seconds <= 0
                and primary_items[0].get("completed_perf") is not None
            ):
                self.warnings.append("parallelism_lost_by_serial_leader_gate")
            missing_replight_lanes = [
                str(item.get("lane"))
                for item in prepared
                if not isinstance(item.get("provider_report"), dict)
            ]
            replight_block_reason = (
                f"provider_replight_failed:{missing_replight_lanes[0]}:missing_provider_report"
                if missing_replight_lanes
                else provider_replight_failure_reason(
                    [
                        item.get("provider_report")
                        for item in prepared
                        if isinstance(item.get("provider_report"), dict)
                    ]
                )
            )
            if replight_block_reason:
                block_provider_universe_run(self, replight_block_reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "provider_replight_failed",
                )
                return
            leader_report = (
                primary_items[0].get("provider_report")
                if isinstance(primary_items[0].get("provider_report"), dict)
                else {}
            )
            primary_status = self.capture_gpu1_primary_evidence_after_provider_join(
                leader_report, round_id
            )
            leader_valid = bool(primary_status.get("gpu1_primary_evidence_valid"))
            self.gpu1_leader_valid = leader_valid
            self.gpu1_leader_block_id = str(
                leader_report.get("provider_block_id")
                or leader_report.get("proposal_block_id")
                or ""
            )
            if not leader_valid:
                reason = str(
                    primary_status.get("block_reason")
                    or "gpu1_primary_evidence_missing"
                )
                block_provider_universe_run(self, reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "gpu1_primary_evidence_missing_after_provider_join",
                )
                return
            primary_block_reason = primary_provider_block_reason(primary_items)
            if primary_block_reason:
                block_provider_universe_run(self, primary_block_reason, round_id, revision)
                write_provider_launch_manifest(
                    self,
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "primary_blocked_after_parallel_provider_join",
                )
                return
            write_provider_launch_manifest(
                self,
                launch_manifest,
                prepared,
                round_id,
                revision,
                time_contract,
                "parallel_provider_joined_gpu1_evidence_captured",
            )
        except BaseException:
            terminate_pending_provider_processes(
                self,
                prepared,
                round_id,
                revision,
                "provider teamwork aborted before all child providers were joined",
            )
            raise

        for item in prepared:
            if not item.get("absorbed"):
                try:
                    absorb_completed_provider_item(
                        self,
                        item,
                        launch_manifest=launch_manifest,
                        work_dir=work_dir,
                        round_id=round_id,
                        revision=revision,
                        timeout_seconds=timeout_seconds,
                    )
                except BaseException as exc:  # noqa: BLE001 - preserve peer lane collection evidence.
                    self.warnings.append(
                        f"provider lane absorption failed for {item.get('lane')}: {type(exc).__name__}: {exc}"
                    )

    def capture_gpu1_primary_evidence_after_provider_join(
        self, leader_report: dict[str, Any], round_id: int
    ) -> dict[str, Any]:
        workload = gpu1_primary_workload_status(leader_report)
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
        if not self.gpu1_primary_workload_valid:
            block_reason = "gpu1_primary_workload_missing"
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

    def capture_gpu1_primary_evidence_before_sidecars(
        self, leader_report: dict[str, Any], round_id: int
    ) -> dict[str, Any]:
        return self.capture_gpu1_primary_evidence_after_provider_join(
            leader_report, round_id
        )
