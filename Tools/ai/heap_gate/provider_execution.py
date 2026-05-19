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
        timeout_seconds = max(30, self.args.timeout_seconds)
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
                        "execution_mode": "concurrent_provider_teamwork",
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
                            "pid": None,
                        }
                    )

            for item in prepared:
                if item.get("completed") is not None:
                    continue
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
                            "execution_mode": "concurrent_provider_teamwork",
                        },
                        target="orchestrator",
                        correlation_id=str(item["correlation"]),
                        round_id=round_id,
                    )
                except Exception as exc:  # noqa: BLE001 - provider lane failure becomes report evidence.
                    item["started_at"] = started_at
                    item["completed_at"] = now_iso()
                    item["elapsed_seconds"] = round(time.perf_counter() - started_perf, 6)
                    item["completed"] = subprocess.CompletedProcess(
                        command,
                        returncode=127,
                        stdout="",
                        stderr=f"{type(exc).__name__}: {exc}",
                    )

            suffix = f"_revision{revision}" if revision else ""
            launch_manifest = work_dir / f"provider_launch_manifest{suffix}.json"
            write_json_report(
                {
                    "kind": "provider_launch_manifest",
                    "execution_mode": "concurrent_provider_teamwork",
                    "revision": revision,
                    "round": round_id,
                    "created_at": now_iso(),
                    "lanes": [
                        {
                            "lane": item.get("lane"),
                            "requirement": item.get("requirement"),
                            "role": item.get("spec", {}).get("role"),
                            "provider_model": (
                                self.args.provider_model
                                if item.get("lane") == "gpu1_planner"
                                else ""
                            ),
                            "pid": item.get("pid"),
                            "started_at": item.get("started_at"),
                            "completed_at": item.get("completed_at"),
                            "elapsed_seconds": item.get("elapsed_seconds"),
                            "timeout_seconds": item.get("timeout_seconds"),
                            "prepare_error": item.get("prepare_error"),
                            "output": repo_rel(self.repo_root, Path(item["spec"]["output"])),
                            "leader_packet": self.provider_leader_packet_path,
                        }
                        for item in prepared
                    ],
                },
                launch_manifest,
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
