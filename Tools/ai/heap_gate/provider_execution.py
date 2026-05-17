"""RuntimeGateProviderExecutionMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    append_unique,
    command_env,
    provider_heap_lane,
    read_json,
    repo_rel,
    subprocess,
)


class RuntimeGateProviderExecutionMixin:
    def run_provider_teamwork(self, round_id: int, revision: int = 0) -> None:
        if self.provider_reports and revision <= 0:
            return

        work_dir = self.provider_work_dir()
        timeout_seconds = max(30, self.args.timeout_seconds)
        prepared: list[dict[str, Any]] = []

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
                    "status": "running",
                    "output": repo_rel(self.repo_root, Path(spec["output"])),
                    "execution_mode": "concurrent_provider_teamwork",
                },
                target="orchestrator",
                correlation_id=correlation,
                round_id=round_id,
            )

            command = [
                (self.gpu1_provider_prompt() if item == "__GPU1_CUMULATIVE_PROMPT__" else item)
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

                process = subprocess.Popen(
                    command,
                    cwd=self.repo_root,
                    env=command_env(self.repo_root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                prepared.append(
                    {
                        "spec": spec,
                        "lane": lane,
                        "requirement": requirement,
                        "correlation": correlation,
                        "command": command,
                        "process": process,
                        "completed": None,
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
                    }
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
                    completed = subprocess.CompletedProcess(
                        command,
                        returncode=process.returncode,
                        stdout=stdout or "",
                        stderr=stderr or "",
                    )
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
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
            events = self.read_events()
            provider_report = self.enrich_provider_report_with_operational_peer_review(
                provider_report,
                lane,
                work_dir,
                revision,
                events,
            )
            provider_report["execution_mode"] = "concurrent_provider_teamwork"
            provider_report["revision"] = revision

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
            self.append_heap_exchange_event(
                {
                    "kind": "provider_output",
                    "lane": lane,
                    "round": round_id,
                    "requirement": requirement,
                    "revision": revision,
                    "execution_mode": "concurrent_provider_teamwork",
                    "passed": provider_report.get("passed"),
                    "provider_execution_performed": provider_report.get(
                        "provider_execution_performed"
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
