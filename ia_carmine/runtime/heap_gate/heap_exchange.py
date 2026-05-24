"""RuntimeGateHeapExchangeMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    command_env,
    json,
    now_iso,
    read_json,
    repo_rel,
    subprocess,
    write_json_report,
    write_text_report,
)


class RuntimeGateHeapExchangeMixin:
    def heap_exchange_paths(self) -> dict[str, Path]:
        """Return heap/exchange lifecycle artifact paths for this gate universe."""
        if self.output_dir:
            base = self.output_dir / "heap_exchange"
        else:
            base = self.repo_root / "output" / "ai_packets" / self.stamp
        base.mkdir(parents=True, exist_ok=True)
        return {
            "dir": base,
            "runtime_state": base / "heap_exchange_runtime_state.jsonl",
            "runtime_entry": base / "heap_exchange_runtime_entry.json",
            "runtime_entry_md": base / "heap_exchange_runtime_entry.md",
            "exit_output": base / "heap_runtime_exit_output.json",
            "exit_output_md": base / "heap_runtime_exit_output.md",
            "exit_product": base / "heap_exchange_runtime_exit_product.json",
            "exit_product_md": base / "heap_exchange_runtime_exit_product.md",
        }

    def append_heap_exchange_event(self, event: dict[str, Any]) -> None:
        """Publish a public heap/exchange event without exposing private reasoning."""
        paths = self.heap_exchange_paths()
        payload = dict(event)
        payload.setdefault("schema_version", 1)
        payload.setdefault("stamp", self.stamp)
        payload.setdefault("timestamp", now_iso())
        payload.setdefault("raw_thinking_exposed", False)
        payload.setdefault("source_of_knowledge", "heap_exchange")
        paths["runtime_state"].parent.mkdir(parents=True, exist_ok=True)
        with paths["runtime_state"].open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    def write_heap_exchange_entry(self) -> None:
        """Register the heap completeness gate as the dynamic heap/exchange universe."""
        paths = self.heap_exchange_paths()
        lanes = [
            {"name": "gpu1", "role": "primary_exit_coordinator", "available": True},
            {
                "name": "gpu0",
                "role": "diagnostic_peer_and_product_evidence_lane",
                "available": True,
            },
            {
                "name": "npu",
                "role": "micro_task_auditor_and_guardrail_peer",
                "available": True,
            },
            {"name": "broker", "role": "allowlisted_tool_executor", "available": True},
            {
                "name": "code_execution_matrix",
                "role": "allowlisted_compile_test_diff_evidence_lane",
                "available": True,
            },
            {
                "name": "virtual_dev_environment",
                "role": "controlled_script_load_debug_probe_environment",
                "available": True,
            },
            {
                "name": "context_memory",
                "role": "sqlite_fts_context_pack_semantic_chunks",
                "available": True,
            },
            {
                "name": "deterministic_audit",
                "role": "exit_quality_and_contract_lane",
                "available": True,
            },
        ]
        request_input_evidence = self.request_input_ref_or_tail()
        entry = {
            "schema_version": 1,
            "kind": "heap_exchange_runtime_entry",
            "generated_at": now_iso(),
            "stamp": self.stamp,
            "repo_root": self.repo_root.as_posix(),
            "source_of_knowledge": "heap_exchange",
            "center_is_dynamic": True,
            "dynamic_exchange_pipeline": True,
            "static_chain_invocation_performed": False,
            "entry_controls_inputs_only": True,
            "exit_must_produce_concrete_product": True,
            "task_file": self.args.task_file,
            **self.prefixed_text_evidence_fields("request", request_input_evidence),
            "runtime_state": repo_rel(self.repo_root, paths["runtime_state"]),
            "lanes": lanes,
            "available_lane_count": len([item for item in lanes if item.get("available")]),
            "knowledge_surface": {
                "source_of_knowledge": "heap_exchange",
                "knowledge_surface": "shared_runtime_heap_blackboard",
                "routing_model": "dynamic_exchange_not_static_chain",
                "lane_autonomy_model": "gpu1_gpu0_npu_provider_lanes_publish_and_consume_exchange_evidence",
                "deterministic_boundaries": {
                    "in_controlled": True,
                    "loop_dynamic": True,
                    "out_deterministic": True,
                },
            },
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "passed": True,
            "errors": [],
            "warnings": [],
        }
        write_json_report(entry, paths["runtime_entry"])
        lines = [
            "# Heap Exchange Runtime Entry",
            "",
            "- Passed: `True`",
            f"- Stamp: `{self.stamp}`",
            "- Routing model: `dynamic_exchange_not_static_chain`",
            "- Source of knowledge: `heap_exchange`",
            "",
            "GPU1, GPU0, NPU, broker and memory/context lanes publish into the same heap universe. Exit is deterministic and product-bound.",
        ]
        write_text_report("\n".join(lines) + "\n", paths["runtime_entry_md"])
        self.append_heap_exchange_event(
            {
                "kind": "heap_entry",
                "lane": "orchestrator",
                "summary": "heap completeness gate registered as dynamic heap/exchange universe",
                "entry": repo_rel(self.repo_root, paths["runtime_entry"]),
            }
        )

    def write_exit_output_product(
        self, response_text: str, events: list[dict[str, Any]], metrics: dict[str, Any]
    ) -> dict[str, Any]:
        """Write the operator-facing heap exit product assembled from all lane artifacts."""
        paths = self.heap_exchange_paths()
        product_status = str(
            self.state.get("product", {}).get("status")
            or metrics.get("product_status")
            or "blocked_with_reason"
        )
        file_quality = self.response_file_reference_quality(response_text)
        request_input_evidence = self.request_input_ref_or_tail()
        response_evidence = self.response_text_ref_or_tail(
            response_text,
            name="heap_exit_response_text",
            kind="heap_exit_response_text",
            producer="heap_exchange",
        )
        provider_raw_response_evidence = self.response_text_ref_or_tail(
            self.response_text(),
            name="heap_exit_provider_raw_response_text",
            kind="gpu1_raw_response_text",
            producer="gpu1_planner",
        )
        product = {
            "schema_version": 1,
            "kind": "heap_runtime_exit_output",
            "generated_at": now_iso(),
            "stamp": self.stamp,
            **self.prefixed_text_evidence_fields("request_input", request_input_evidence),
            "product_status": product_status,
            **self.prefixed_text_evidence_fields("response_text", response_evidence),
            **self.prefixed_text_evidence_fields(
                "provider_raw_response_text", provider_raw_response_evidence
            ),
            "source_of_knowledge": "heap_exchange",
            "assembled_by": "gpu1_exit_coordinator",
            "revealed_by": "heap_exchange_runtime_exit",
            "provider_contribution_refs_or_tails": self.provider_response_refs_or_tails(),
            "context_artifact_refs": self.broker_output_refs(events),
            "bridge_reports": self.bridge_report_refs(events),
            "quality_output_signals": self.quality_output_signals(response_text, events),
            "response_file_reference_quality": file_quality,
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": self.missing_requirements(events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(events),
            "runtime_debug_lab_required": self.runtime_debug_lab_required(),
            "runtime_debug_lab_passed": self.runtime_debug_lab_passed(events),
            "runtime_debug_lab_reports": self.runtime_debug_lab_reports(events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
        }
        write_json_report(product, paths["exit_output"])
        md = [
            "# Heap Runtime Exit Output",
            "",
            f"- Status: `{product_status}`",
            f"- Assembled by: `{product['assembled_by']}`",
            f"- Revealed by: `{product['revealed_by']}`",
            "",
            "## Response",
            "",
            response_text,
            "",
            "## File reference quality",
            "",
            f"- Passed: `{file_quality.get('passed')}`",
            f"- Unverified file refs: `{file_quality.get('unverified_file_refs')}`",
            "",
            "## Runtime debug lab",
            "",
            f"- Virtual dev environment required: `{product.get('virtual_dev_environment_required')}`",
            f"- Virtual dev environment passed: `{product.get('virtual_dev_environment_passed')}`",
            f"- Virtual dev environment reports: `{product.get('virtual_dev_environment_reports')}`",
            f"- Code execution matrix required: `{product.get('code_execution_matrix_required')}`",
            f"- Code execution matrix passed: `{product.get('code_execution_matrix_passed')}`",
            f"- Code execution matrix reports: `{product.get('code_execution_matrix_reports')}`",
            f"- Required: `{product.get('runtime_debug_lab_required')}`",
            f"- Passed: `{product.get('runtime_debug_lab_passed')}`",
            f"- Reports: `{product.get('runtime_debug_lab_reports')}`",
            "",
            "## Proposal iterations",
            "",
            f"- Artifacts: `{product.get('proposal_iteration_artifacts')}`",
        ]
        write_text_report("\n".join(md) + "\n", paths["exit_output_md"])
        self.append_heap_exchange_event(
            {
                "kind": "heap_exit_product",
                "lane": "gpu1",
                "summary": f"GPU1 composed heap exit output with status={product_status}",
                "operation": "write_file",
                "operation_count": 1,
                "path": repo_rel(self.repo_root, paths["exit_output"]),
                "source_file": repo_rel(self.repo_root, paths["exit_output"]),
                "product_status": product_status,
                "quality_passed": self.quality_output_passed(response_text, events),
            }
        )
        return product

    def build_heap_exchange_exit_product(self, require_concrete_product: bool) -> dict[str, Any]:
        """Reuse the existing deterministic heap/exchange exit boundary tool."""
        paths = self.heap_exchange_paths()
        command = [
            self.child_python(),
            "ia_carmine/runtime/heap_exchange/runtime_exit/cli.py",
            "--repo-root",
            ".",
            "--stamp",
            self.stamp,
            "--runtime-entry",
            repo_rel(self.repo_root, paths["runtime_entry"]),
            "--runtime-state",
            repo_rel(self.repo_root, paths["runtime_state"]),
            "--output",
            repo_rel(self.repo_root, paths["exit_product"]),
            "--markdown-output",
            repo_rel(self.repo_root, paths["exit_product_md"]),
        ]
        if require_concrete_product:
            command.append("--require-concrete-product")
        try:
            completed = subprocess.run(
                command,
                cwd=self.repo_root,
                env=command_env(self.repo_root),
                capture_output=True,
                text=True,
                check=False,
                timeout=max(30, int(self.args.timeout_seconds)),
            )
        except subprocess.TimeoutExpired as exc:
            self.warnings.append(f"heap exchange exit timed out: {exc}")
            return {
                "passed": False,
                "error": "timeout",
                "output": repo_rel(self.repo_root, paths["exit_product"]),
            }
        report = read_json(paths["exit_product"])
        if completed.returncode != 0:
            self.warnings.append(
                f"heap exchange exit returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}"
            )
        return report or {
            "passed": completed.returncode == 0,
            "output": repo_rel(self.repo_root, paths["exit_product"]),
        }
