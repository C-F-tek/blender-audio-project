"""RuntimeGateProviderCommandsMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    Any,
    Path,
    repo_rel,
    subprocess,
)


class RuntimeGateProviderCommandsMixin:
    def provider_command_specs(self, work_dir: Path, revision: int = 0) -> list[dict[str, Any]]:
        suffix = f"_revision{revision}" if revision else ""
        gpu1_json = work_dir / f"gpu1_ollama_provider_probe{suffix}.json"
        gpu0_json = work_dir / f"gpu0_openvino_peer_workload{suffix}.json"
        gpu0_md = work_dir / f"gpu0_openvino_peer_workload{suffix}.md"
        npu_json = work_dir / f"npu_micro_task_auditor{suffix}.json"
        npu_md = work_dir / f"npu_micro_task_auditor{suffix}.md"
        leader_packet = str(getattr(self, "provider_leader_packet_path", "") or "")
        startup_manifest = str(getattr(self.args, "startup_manifest", "") or "")
        task_file = str(getattr(self.args, "task_file", "") or "")
        request_file = str(getattr(self.args, "request_file", "") or "")
        request_args = ["--request-file", request_file] if request_file else ["--request", self.request_text()]
        startup_args = (
            ["--startup-manifest", startup_manifest]
            if startup_manifest
            else (["--task-file", task_file] if task_file else [])
        )
        return [
            {
                "lane": "gpu1_planner",
                "requirement": "gpu1_provider_planner",
                "role": "primary_planner_cumulative_responder",
                "output": gpu1_json,
                "command": [
                    self.child_python(),
                    "-m",
                    "Tools.ai",
                    "run_local_provider_probe",
                    "--repo-root",
                    ".",
                    "--run-ollama",
                    "--model",
                    self.args.provider_model,
                    "--prompt",
                    "__GPU1_CUMULATIVE_PROMPT__",
                    "--timeout",
                    str(self.args.timeout_seconds),
                    "--max-new-tokens",
                    str(max(128, min(int(self.args.max_new_tokens), 4096))),
                    "--ollama-num-ctx",
                    str(max(4096, int(self.args.ollama_num_ctx))),
                    "--keep-alive",
                    str(self.args.keep_alive),
                    "--output",
                    repo_rel(self.repo_root, gpu1_json),
                ],
            },
            {
                "lane": "gpu0_peer",
                "requirement": "gpu0_provider_peer",
                "role": "diagnostic_peer_workload",
                "output": gpu0_json,
                "command": [
                    self.child_python(),
                    "-m",
                    "Tools.ai",
                    "build_openvino_gpu0_workload_report",
                    "--repo-root",
                    ".",
                    "--iterations",
                    str(self.args.gpu0_iterations),
                    "--min-seconds",
                    str(self.args.gpu0_min_seconds),
                    "--tool-loop-timeout-seconds",
                    str(min(max(int(self.args.timeout_seconds // 2), 60), 180)),
                    "--require-semantic-provider",
                    "--role",
                    "heap_runtime_diagnostic_peer",
                    *startup_args,
                    *(
                        ["--leader-packet", leader_packet]
                        if leader_packet
                        else []
                    ),
                    *request_args,
                    "--output",
                    repo_rel(self.repo_root, gpu0_json),
                    "--markdown-output",
                    repo_rel(self.repo_root, gpu0_md),
                ],
            },
            {
                "lane": "npu_micro_task_auditor",
                "requirement": "npu_micro_task_auditor",
                "role": "npu_micro_task_auditor",
                "output": npu_json,
                "command": [
                    self.child_python(),
                    "-m",
                    "Tools.ai",
                    "build_npu_micro_task_companion_report",
                    "--repo-root",
                    ".",
                    *startup_args,
                    *request_args,
                    *(
                        ["--leader-packet", leader_packet]
                        if leader_packet
                        else []
                    ),
                    "--python-exe",
                    self.child_python(),
                    "--timeout-seconds",
                    str(self.args.npu_micro_timeout_seconds),
                    "--max-context-chars",
                    str(self.args.npu_max_context_chars),
                    "--tool-loop-timeout-seconds",
                    str(min(max(int(self.args.timeout_seconds // 2), 60), 180)),
                    "--require-semantic-provider",
                    *(
                        [
                            "--run-device-workload",
                            "--device-workload-seconds",
                            str(self.args.npu_device_workload_seconds),
                            "--device-workload-iterations",
                            str(self.args.npu_device_workload_iterations),
                        ]
                        if self.args.allow_npu_device_workload
                        else []
                    ),
                    "--output",
                    repo_rel(self.repo_root, npu_json),
                    "--markdown-output",
                    repo_rel(self.repo_root, npu_md),
                ],
            },
        ]

    def summarize_provider_report(
        self,
        spec: dict[str, Any],
        completed: subprocess.CompletedProcess[str],
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        lane = str(spec["lane"])
        tool_calls: list[dict[str, Any]] = []
        textual_tool_calls: list[dict[str, Any]] = []
        native_tool_loop_requested = bool(report_data.get("native_tool_loop_requested"))
        native_tool_loop_supported = bool(report_data.get("native_tool_loop_supported"))
        native_tool_loop_performed = bool(report_data.get("native_tool_loop_performed"))

        def absorb_tool_loop(payload: dict[str, Any]) -> None:
            nonlocal native_tool_loop_requested
            nonlocal native_tool_loop_supported
            nonlocal native_tool_loop_performed
            native_tool_loop_requested = native_tool_loop_requested or bool(
                payload.get("native_tool_loop_requested")
            )
            native_tool_loop_supported = native_tool_loop_supported or bool(
                payload.get("native_tool_loop_supported")
            )
            native_tool_loop_performed = native_tool_loop_performed or bool(
                payload.get("native_tool_loop_performed")
            )
            calls = payload.get("tool_calls") if isinstance(payload.get("tool_calls"), list) else []
            for call in calls:
                if isinstance(call, dict):
                    tool_calls.append(call)
            text_calls = (
                payload.get("textual_tool_calls")
                if isinstance(payload.get("textual_tool_calls"), list)
                else []
            )
            for call in text_calls:
                if isinstance(call, dict):
                    textual_tool_calls.append(call)

        absorb_tool_loop(report_data)
        provider_execution = bool(
            report_data.get("provider_execution_performed")
            or report_data.get("openvino_gpu0_workload_performed")
            or report_data.get("openvino_gpu0_probe_performed")
            or report_data.get("npu_provider_execution_performed")
            or report_data.get("npu_device_workload_performed")
        )
        device_workload_execution = bool(
            report_data.get("device_workload_execution_performed")
            or report_data.get("openvino_gpu0_workload_performed")
            or report_data.get("openvino_gpu0_probe_performed")
            or report_data.get("npu_device_workload_performed")
        )
        semantic_provider_execution = bool(
            report_data.get("semantic_provider_execution_performed")
            or report_data.get("gpu0_semantic_provider_execution_performed")
            or report_data.get("npu_semantic_provider_execution_performed")
        )
        if provider_execution or semantic_provider_execution:
            self.provider_execution_performed = True
        errors = report_data.get("errors") if isinstance(report_data.get("errors"), list) else []
        warnings = (
            report_data.get("warnings") if isinstance(report_data.get("warnings"), list) else []
        )
        response_text = str(report_data.get("response_text") or "").strip()
        selected_model = str(report_data.get("selected_model") or "").strip()
        lane_reports = report_data.get("lane_reports")
        if isinstance(lane_reports, list):
            for lane_report in lane_reports:
                if isinstance(lane_report, dict):
                    absorb_tool_loop(lane_report)
                if isinstance(lane_report, dict) and lane_report.get("lane") == "ollama":
                    selected_model = str(
                        lane_report.get("selected_model")
                        or lane_report.get("model")
                        or selected_model
                    ).strip()
                    response_text = str(
                        lane_report.get("response_text")
                        or lane_report.get("text_preview")
                        or response_text
                    ).strip()
                    if not report_data.get("target_files") and lane_report.get("target_files"):
                        report_data["target_files"] = lane_report.get("target_files")
                    if (
                        not report_data.get("validation_commands")
                        and lane_report.get("validation_commands")
                    ):
                        report_data["validation_commands"] = lane_report.get(
                            "validation_commands"
                        )
                    if response_text:
                        break
        return {
            "lane": lane,
            "role": spec.get("role"),
            "requirement": spec.get("requirement"),
            "output": repo_rel(self.repo_root, Path(spec["output"])),
            "returncode": completed.returncode,
            "passed": completed.returncode == 0 and report_data.get("passed") is True,
            "provider_execution_performed": provider_execution,
            "device_workload_execution_performed": device_workload_execution,
            "semantic_provider_required": report_data.get("semantic_provider_required"),
            "semantic_provider_execution_performed": semantic_provider_execution,
            "semantic_provider_model_loaded": report_data.get("semantic_provider_model_loaded"),
            "semantic_provider_classification": report_data.get(
                "semantic_provider_classification"
            ),
            "report_kind": report_data.get("kind"),
            "response_text": response_text,
            "tool_calls": tool_calls,
            "textual_tool_calls": textual_tool_calls,
            "native_tool_loop_requested": native_tool_loop_requested,
            "native_tool_loop_supported": native_tool_loop_supported,
            "native_tool_loop_performed": native_tool_loop_performed,
            "native_tool_call_count": len(tool_calls),
            "textual_tool_call_count": len(textual_tool_calls),
            "role_decision": report_data.get("role_decision"),
            "selected_model": selected_model or report_data.get("selected_model"),
            "target_files": report_data.get("target_files") or report_data.get("TARGET_FILES") or [],
            "validation_commands": report_data.get("validation_commands")
            or report_data.get("VALIDATION_COMMANDS")
            or [],
            "npu_device_workload": report_data.get("npu_device_workload"),
            "npu_device_workload_requested": report_data.get("npu_device_workload_requested"),
            "npu_device_workload_performed": report_data.get("npu_device_workload_performed"),
            "npu_provider_execution_performed": report_data.get("npu_provider_execution_performed"),
            "errors": errors,
            "warnings": warnings,
            "stdout_tail": (completed.stdout or "")[-1000:],
            "stderr_tail": (completed.stderr or "")[-1000:],
        }

    def build_quality_failure_feedback(self, text: str, events: list[dict[str, Any]]) -> str:
        file_quality = self.response_file_reference_quality(text)
        implementation_quality = self.implementation_quality_report(text, events)
        candidates = self.real_source_file_candidates(events, limit=32)
        base_feedback = (
            "quality gate failure: la risposta precedente non è uscibile come prodotto heap. "
            f"output_artifact_refs={file_quality.get('output_artifact_refs')}; "
            f"unverified_source_file_refs={file_quality.get('unverified_source_file_refs')}; "
            f"no_source_file_refs={file_quality.get('no_source_file_refs')}; "
            f"implementation_quality_errors={implementation_quality.get('errors')}. "
            "Devi rigenerare usando solo file sorgente reali candidati, con proposte concrete agganciate a path repo esistenti. "
            "Se manca codice/patch/comandi, GPU0 deve considerare il blocco non soddisfacente. "
            f"source_candidates={candidates}"
        )
        iteration_feedback = self.proposal_iteration_feedback(events, file_quality)
        concrete_delta_feedback = self.force_concrete_delta_feedback(events)
        return "\n".join(
            part
            for part in (
                base_feedback,
                self.matrix_patch_candidate_feedback(events),
                iteration_feedback,
                concrete_delta_feedback,
            )
            if part
        )

    def force_concrete_delta_feedback(self, events: list[dict[str, Any]]) -> str:
        """Force GPU1 to produce a materially different concrete block after veto loops.

        This is intentionally feedback-only: it does not change provider calls,
        does not apply patches and does not alter the composer format. It raises
        the in-heap contract pressure when repeated proposal chunks are rejected
        for placeholder/stub markers or near-identical revisions.
        """
        report = self.latest_proposal_iteration_report()
        if not report:
            return ""

        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        progress = (
            report.get("proposal_progress")
            if isinstance(report.get("proposal_progress"), dict)
            else {}
        )
        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        veto = (
            report.get("cross_lane_veto") if isinstance(report.get("cross_lane_veto"), dict) else {}
        )

        def listify(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, tuple):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, str) and value.strip():
                return [value.strip()]
            return []

        def parse_similarity(value: Any) -> float:
            try:
                return float(str(value or "0").replace(",", "."))
            except ValueError:
                return 0.0

        placeholder_hits = listify(implementation.get("placeholder_hits"))
        implementation_errors = listify(implementation.get("errors"))
        progress_errors = listify(progress.get("errors"))
        unverified_refs = listify(
            quality.get("unverified_source_file_refs") or quality.get("unverified_file_refs")
        )
        veto_reasons = listify(veto.get("reasons"))
        similarity = parse_similarity(progress.get("similarity"))

        has_placeholder = bool(placeholder_hits) or any(
            marker in item.lower()
            for item in implementation_errors + veto_reasons
            for marker in ("placeholder", "todo", "fixme", "bare_pass", "stub")
        )
        repeated = similarity >= 0.95 or any(
            "similarity=" in item.lower() for item in progress_errors + veto_reasons
        )
        vetoed = veto.get("vetoed") is True

        if not (has_placeholder or repeated or vetoed):
            return ""

        candidates = self.real_source_file_candidates(events, limit=18)
        latest_revision = report.get("revision")
        latest_source = report.get("source")
        lines = [
            "FORCED CONCRETE DELTA REQUIRED:",
            f"- Previous proposal revision: {latest_revision}",
            f"- Previous proposal source: {latest_source}",
            f"- Similarity with previous proposal: {similarity:.3f}",
            "- The previous block was rejected by the same heap. Do not repeat it.",
            "- Treat candidate_response_preview as a negative example when prior flags include invented_source_path, unresolved_pointer_placeholder or unresolved_angle_bracket_token.",
            "- Produce a materially different proposal chunk, not a paraphrase.",
            "- Remove every TODO/FIXME/pass/placeholder/stub marker from the proposal text.",
            "- Use concrete repo-relative TARGET_FILES only from the allowed concrete source targets below.",
            "- Copy TARGET_FILES verbatim from the allowed concrete source targets; do not cite rejected refs anywhere in the next proposal.",
            "- Every diff header path must match an allowed concrete source target exactly.",
            "- If the only possible target is unverified or invented, return EXIT_DECISION=NO_PATCHABLE_TARGET instead of inventing a path.",
            "- Never output unresolved angle-bracket placeholders such as <id-or-empty>.",
            "- For each TARGET_FILE include PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, VALIDATION_COMMANDS, RISKS and EXIT_DECISION.",
            "- If no concrete target is patchable from current evidence, return EXIT_DECISION=NO_PATCHABLE_TARGET with explicit reason.",
            "- GPU1 may move backward on previous/refines/resume pointers to propagate imports, symbols, contracts and validation commands, then resume forward.",
            "- GPU0 and NPU vetoes are authoritative quality signals inside this heap loop.",
        ]
        if placeholder_hits:
            lines.append("- Placeholder hits to eliminate: " + ", ".join(placeholder_hits[:12]))
        if implementation_errors:
            lines.append(
                "- Implementation errors to resolve: " + " | ".join(implementation_errors[:8])
            )
        if progress_errors:
            lines.append("- Progress errors to resolve: " + " | ".join(progress_errors[:8]))
        if unverified_refs:
            lines.append(
                "- Rejected/non-allowlisted source refs blacklist: "
                + ", ".join(unverified_refs[:12])
            )
        if veto_reasons:
            lines.append("- Cross-lane veto reasons to resolve: " + " | ".join(veto_reasons[:8]))
        if candidates:
            lines.append("Allowed concrete source targets:")
            lines.extend(f"- {item}" for item in candidates[:18])
        return "\n".join(lines)
