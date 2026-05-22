"""RuntimeGateProviderExecutionMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

import time

from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, now_iso, provider_heap_lane, repo_rel, subprocess, write_json_report
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
from ia_carmine.runtime.heap_gate.provider_universe_abort import (
    block_provider_universe_run,
    block_unstarted_provider_items,
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
                stage="before_provider_replight",
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
                        "status": "preparing",
                        "output": repo_rel(self.repo_root, Path(spec["output"])),
                        "execution_mode": "provider_teamwork_unified_parallel",
                        "budget_counter_seconds": spec.get("budget_counter_seconds"),
                        "soft_close_after_seconds": spec.get("soft_close_after_seconds"),
                        "watchdog_timeout_seconds": spec.get("watchdog_timeout_seconds"),
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
                "gpu1_manual_full_gpu_gate_started",
            )
            for item in primary_items:
                if item.get("completed") is not None:
                    absorb(item)
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
                    primary_items,
                    round_id,
                    revision,
                    f"GPU1 replight preflight failed before sidecar start: {primary_block_reason}",
                )
                for item in primary_items:
                    if item.get("completed") is not None:
                        absorb(item)
                block_unstarted_provider_items(sidecar_items, primary_block_reason)
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
                "parallel_lanes_started_after_gpu1_replight_preflight",
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
                    "primary_blocked_after_sidecar_join",
                )
                return
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
