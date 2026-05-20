"""RuntimeGateProviderExecutionMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

import time

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    command_env,
    now_iso,
    provider_heap_lane,
    repo_rel,
    subprocess,
    write_json_report,
)
from Tools.ai.heap_gate.provider_block_contract import (
    proposal_block_id_for_revision as make_proposal_block_id,
    provider_block_contract as build_provider_block_contract,
)
from Tools.ai.heap_gate.provider_process_collection import (
    collect_provider_processes,
    terminate_pending_provider_processes,
)
from Tools.ai.heap_gate.provider_report_absorption import absorb_completed_provider_item
from Tools.ai.heap_gate.provider_teamwork_packet import build_provider_teamwork_leader_packet
from Tools.ai.heap_gate.provider_universe_abort import block_provider_universe_run


PRIMARY_LANE = "gpu1_planner"


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

    def _write_provider_launch_manifest(
        self,
        path: Path,
        prepared: list[dict[str, Any]],
        round_id: int,
        revision: int,
        time_contract: dict[str, Any],
        stage: str,
    ) -> None:
        write_json_report(
            {
                "kind": "provider_launch_manifest",
                "execution_mode": "provider_teamwork_unified_parallel",
                "revision": revision,
                "round": round_id,
                "stage": stage,
                "created_at": now_iso(),
                "time_counter_contract": time_contract,
                "lanes": [
                    {
                        "lane": item.get("lane"),
                        "requirement": item.get("requirement"),
                        "role": item.get("spec", {}).get("role"),
                        "provider_model": (
                            self.args.provider_model
                            if item.get("lane") == PRIMARY_LANE
                            else ""
                        ),
                        "pid": item.get("pid"),
                        "started_at": item.get("started_at"),
                        "completed_at": item.get("completed_at"),
                        "elapsed_seconds": item.get("elapsed_seconds"),
                        "timeout_seconds": item.get("timeout_seconds"),
                        "budget_counter_seconds": item.get("budget_counter_seconds"),
                        "soft_close_after_seconds": item.get("soft_close_after_seconds"),
                        "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
                        "prepare_error": item.get("prepare_error"),
                        "blocked_reason": item.get("blocked_reason", ""),
                        "output": repo_rel(self.repo_root, Path(item["spec"]["output"])),
                        "leader_packet": self.provider_leader_packet_path,
                    }
                    for item in prepared
                ],
            },
            path,
        )

    def _start_provider_item(
        self,
        item: dict[str, Any],
        round_id: int,
        revision: int,
    ) -> None:
        if item.get("completed") is not None:
            return
        command = list(item["command"])
        started_at = now_iso()
        started_perf = time.perf_counter()
        try:
            process = subprocess.Popen(
                command,
                cwd=self.repo_root,
                env=command_env(self.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
            )
            item["process"] = process
            item["started_at"] = started_at
            item["started_perf"] = started_perf
            item["pid"] = process.pid
            self.publish(
                provider_heap_lane(str(item["lane"])),
                "provider_state",
                {
                    "id": str(item["correlation"]),
                    "lane": item["lane"],
                    "role": item["spec"].get("role"),
                    "requirement": item["requirement"],
                    "revision": revision,
                    "status": "running",
                    "pid": process.pid,
                    "started_at": started_at,
                    "output": repo_rel(self.repo_root, Path(item["spec"]["output"])),
                    "execution_mode": "provider_teamwork_unified_parallel",
                    "budget_counter_seconds": item.get("budget_counter_seconds"),
                    "soft_close_after_seconds": item.get("soft_close_after_seconds"),
                    "watchdog_timeout_seconds": item.get("watchdog_timeout_seconds"),
                },
                target="orchestrator",
                correlation_id=str(item["correlation"]),
                round_id=round_id,
            )
        except Exception as exc:  # noqa: BLE001 - provider lane failure becomes report evidence.
            item["start_attempted_at"] = started_at
            item["started_at"] = ""
            item["completed_at"] = now_iso()
            item["elapsed_seconds"] = round(time.perf_counter() - started_perf, 6)
            item["prepare_error"] = f"start_error:{type(exc).__name__}: {exc}"
            item["completed"] = subprocess.CompletedProcess(
                command,
                returncode=127,
                stdout="",
                stderr=f"{type(exc).__name__}: {exc}",
            )

    def _primary_provider_report(self, prepared: list[dict[str, Any]]) -> dict[str, Any]:
        for item in prepared:
            if item.get("lane") == PRIMARY_LANE and isinstance(item.get("provider_report"), dict):
                return item["provider_report"]
        return {}

    def _primary_provider_block_reason(self, prepared: list[dict[str, Any]]) -> str:
        report = self._primary_provider_report(prepared)
        if not report:
            return "provider_universe_primary_lane_missing_report"
        if report.get("status") != "ready":
            return f"provider_universe_primary_lane_not_ready:{report.get('status')}"
        if not report.get("operational_provider_activity"):
            classification = report.get("provider_activity_classification") or "unknown"
            return f"provider_universe_primary_lane_not_operational:{classification}"
        return ""

    def _block_unstarted_provider_items(
        self,
        items: list[dict[str, Any]],
        reason: str,
    ) -> None:
        for item in items:
            if item.get("completed") is not None or item.get("started_at"):
                continue
            item["blocked_reason"] = reason
            item["completed_at"] = now_iso()
            item["elapsed_seconds"] = 0.0
            item["completed"] = subprocess.CompletedProcess(
                list(item.get("command") or []),
                130,
                "",
                f"provider lane not started because primary lane blocked universe: {reason}",
            )

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
        try:
            leader_prompt = self.gpu1_provider_prompt()
            leader_packet = work_dir / f"provider_teamwork_leader_packet{f'_revision{revision}' if revision else ''}.json"
            write_json_report(
                build_provider_teamwork_leader_packet(self, round_id, revision, leader_prompt),
                leader_packet,
            )
            self.provider_leader_packet_path = repo_rel(self.repo_root, leader_packet)
            self.provider_leader_prompt = leader_prompt

            for spec in self.provider_command_specs(work_dir, revision=revision):
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
                            "time_counter_contract": spec.get("time_counter_contract"),
                            "pid": None,
                        }
                    )

            suffix = f"_revision{revision}" if revision else ""
            launch_manifest = work_dir / f"provider_launch_manifest{suffix}.json"
            for item in prepared:
                self._start_provider_item(item, round_id, revision)
            self._write_provider_launch_manifest(
                launch_manifest, prepared, round_id, revision, time_contract, "all_lanes_started"
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

            for item in prepared:
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
            primary_block_reason = self._primary_provider_block_reason(prepared)
            if primary_block_reason:
                block_provider_universe_run(self, primary_block_reason, round_id, revision)
                self._write_provider_launch_manifest(
                    launch_manifest,
                    prepared,
                    round_id,
                    revision,
                    time_contract,
                    "primary_blocked_after_parallel_join",
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
