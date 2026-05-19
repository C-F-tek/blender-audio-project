"""RuntimeGateProviderExecutionMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

import time

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    append_unique,
    command_env,
    now_iso,
    provider_heap_lane,
    read_json,
    repo_rel,
    subprocess,
    terminate_process_tree,
    write_json_report,
)
from Tools.ai.heap_gate.provider_teamwork_packet import build_provider_teamwork_leader_packet


class RuntimeGateProviderExecutionMixin:
    def proposal_block_id_for_revision(self, revision: int) -> str:
        return f"{self.stamp}:proposal:{int(revision):03d}"

    def provider_block_contract(
        self,
        lane: str,
        revision: int,
        provider_report: dict[str, Any],
    ) -> dict[str, Any]:
        proposal_block_id = self.proposal_block_id_for_revision(revision)
        lane_key = str(lane or "provider").strip() or "provider"
        provider_block_id = f"{self.stamp}:{lane_key}:{int(revision):03d}"
        if lane_key == "gpu0_peer":
            role = "gpu0_reviewer_refiner"
            block_type = "review_refinement_block"
            pointer_action = "REFINE"
            refines = proposal_block_id
            resume = proposal_block_id
        elif lane_key == "npu_micro_task_auditor":
            role = "npu_auditor"
            block_type = "audit_block"
            pointer_action = "AUDIT"
            refines = proposal_block_id
            resume = proposal_block_id
        elif lane_key == "gpu1_planner":
            role = "gpu1_planner"
            block_type = "provider_proposal_block"
            pointer_action = "PROPOSE"
            refines = ""
            resume = proposal_block_id
        else:
            role = str(provider_report.get("role") or lane_key)
            block_type = "provider_evidence_block"
            pointer_action = "EVIDENCE"
            refines = ""
            resume = proposal_block_id
        target_files = provider_report.get("target_files")
        if not isinstance(target_files, list):
            target_files = []
        return {
            "heap_block": True,
            "block_id": provider_block_id,
            "provider_block_id": provider_block_id,
            "proposal_block_id": proposal_block_id,
            "revision": int(revision),
            "role": role,
            "block_type": block_type,
            "previous_block_id": "",
            "next_block_id": "",
            "refines_block_id": refines,
            "resume_from_block_id": resume,
            "pointer_action": pointer_action,
            "target_files": [str(item) for item in target_files if str(item).strip()],
            "decision": (
                "accept"
                if provider_report.get("passed")
                else "blocked"
            ),
            "exit_decision": (
                "PATCHABLE_TARGET"
                if target_files and provider_report.get("passed")
                else "BLOCKED"
            ),
        }

    def run_provider_teamwork(self, round_id: int, revision: int = 0) -> None:
        if self.provider_reports and revision <= 0:
            return

        work_dir = self.provider_work_dir()
        timeout_seconds = max(30, self.args.timeout_seconds)
        prepared: list[dict[str, Any]] = []
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
                        "pid": item.get("pid"),
                        "started_at": item.get("started_at"),
                        "completed_at": item.get("completed_at"),
                        "elapsed_seconds": item.get("elapsed_seconds"),
                        "prepare_error": item.get("prepare_error"),
                        "output": repo_rel(self.repo_root, Path(item["spec"]["output"])),
                        "leader_packet": self.provider_leader_packet_path,
                    }
                    for item in prepared
                ],
            },
            launch_manifest,
        )

        for item in prepared:
            spec = item["spec"]
            lane = str(item["lane"])
            requirement = str(item["requirement"])
            correlation = str(item["correlation"])
            command = list(item["command"])
            process = item.get("process")
            completed = item.get("completed")

            if completed is None and process is not None:
                try:
                    stdout, stderr = process.communicate(timeout=timeout_seconds)
                    item["completed_at"] = now_iso()
                    item["elapsed_seconds"] = round(
                        time.perf_counter() - float(item.get("started_perf") or 0.0), 6
                    )
                    completed = subprocess.CompletedProcess(
                        command,
                        returncode=process.returncode,
                        stdout=stdout or "",
                        stderr=stderr or "",
                    )
                except subprocess.TimeoutExpired:
                    terminate_process_tree(process)
                    stdout, stderr = process.communicate()
                    item["completed_at"] = now_iso()
                    item["elapsed_seconds"] = round(
                        time.perf_counter() - float(item.get("started_perf") or 0.0), 6
                    )
                    completed = subprocess.CompletedProcess(
                        command,
                        returncode=124,
                        stdout=stdout or "",
                        stderr=(stderr or "") + "\nprovider timeout",
                    )

            if completed is None:
                completed = subprocess.CompletedProcess(
                    command,
                    returncode=127,
                    stdout="",
                    stderr="provider process was not started and no completed process was recorded",
                )

            report_data = read_json(Path(spec["output"]))
            provider_report = self.summarize_provider_report(spec, completed, report_data)
            provider_report["status"] = "ready" if provider_report.get("passed") else "degraded"
            provider_report["started_at"] = item.get("started_at")
            provider_report["completed_at"] = item.get("completed_at")
            provider_report["elapsed_seconds"] = item.get("elapsed_seconds")
            provider_report["provider_process_id"] = item.get("pid")
            provider_report["launch_manifest"] = repo_rel(self.repo_root, launch_manifest)
            provider_report["leader_packet"] = self.provider_leader_packet_path
            events = self.read_events()
            provider_report = self.enrich_provider_report_with_operational_peer_review(
                provider_report,
                lane,
                work_dir,
                revision,
                events,
            )
            provider_report.update(
                self.provider_block_contract(lane, revision, provider_report)
            )
            provider_report["execution_mode"] = "concurrent_provider_teamwork"
            provider_report["revision"] = revision
            normalized_output = dict(report_data) if isinstance(report_data, dict) else {}
            normalized_output.update(provider_report)
            write_json_report(normalized_output, Path(spec["output"]))

            self.provider_reports.append(provider_report)
            append_unique(self.state["provider_results"], provider_report, key="requirement")
            self.publish(
                provider_heap_lane(lane),
                "telemetry_signal",
                provider_report,
                target="orchestrator",
                correlation_id=correlation,
                round_id=round_id,
            )
            self.publish(
                provider_heap_lane(lane),
                "provider_peer_block",
                {
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
                    "semantic_provider_execution_performed": provider_report.get(
                        "semantic_provider_execution_performed"
                    ),
                },
                target="orchestrator",
                correlation_id=f"{correlation}:block",
                round_id=round_id,
            )
            self.append_heap_exchange_event(
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
                    "leader_packet": provider_report.get("leader_packet"),
                    "provider_block_id": provider_report.get("provider_block_id"),
                    "proposal_block_id": provider_report.get("proposal_block_id"),
                    "block_type": provider_report.get("block_type"),
                    "pointer_action": provider_report.get("pointer_action"),
                    "refines_block_id": provider_report.get("refines_block_id"),
                    "resume_from_block_id": provider_report.get("resume_from_block_id"),
                    "passed": provider_report.get("passed"),
                    "provider_execution_performed": provider_report.get(
                        "provider_execution_performed"
                    ),
                    "semantic_provider_execution_performed": provider_report.get(
                        "semantic_provider_execution_performed"
                    ),
                    "source_file": provider_report.get("output"),
                    "summary": str(provider_report.get("response_text") or "")[:500],
                }
            )
            claim = {
                "id": f"{requirement}_claim",
                "from": lane,
                "claim": (
                    "provider lane contributed usable heap evidence"
                    if provider_report.get("passed")
                    else "provider lane did not produce usable heap evidence"
                ),
                "confidence": 0.88 if provider_report.get("passed") else 0.35,
                "requirement": requirement,
                "evidence_ref": provider_report.get("output"),
                "provider_execution_performed": provider_report.get("provider_execution_performed"),
                "semantic_provider_execution_performed": provider_report.get(
                    "semantic_provider_execution_performed"
                ),
                "leader_packet": provider_report.get("leader_packet"),
                "observed_request": self.request_text(),
                "observed_response": provider_report.get("response_text") or self.response_text(),
                "execution_mode": "concurrent_provider_teamwork",
            }
            append_unique(self.state["claims"], claim)
            self.publish(
                provider_heap_lane(lane),
                "claim",
                claim,
                target="deterministic",
                correlation_id=f"{correlation}:claim",
                round_id=round_id,
            )
