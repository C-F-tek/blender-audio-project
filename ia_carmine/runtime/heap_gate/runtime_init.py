"""RuntimeGateInitMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from time import monotonic

from ia_carmine.runtime.heap_gate.provider_time import build_provider_time_counter_contract
from ia_carmine.runtime.heap_gate.runtime_common import (
    DEFAULT_BRIDGE_DIR,
    DEFAULT_BRIDGE_JSON,
    DEFAULT_BRIDGE_MD,
    DEFAULT_EVENTS,
    DEFAULT_HEAP_MD,
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    DEFAULT_SNAPSHOT,
    HISTORICAL_TOOL_CONTEXT_FILES,
    Any,
    Path,
    ProviderBudgetConfig,
    ProviderRuntimeHeap,
    RepoRuntimeUniverseBuilder,
    RuntimeFileRefResolver,
    argparse,
    build_heap_provider_budget_governor,
    build_heap_provider_invocation_contract,
    clamp_loop_iterations,
    datetime,
    json,
    make_state,
    read_request_file,
    render_universe_markdown,
    repo_rel,
    resolve_child_python,
)
from ia_carmine.runtime.heap_gate.target_planner import filter_source_candidates_for_request


class RuntimeGateInitMixin:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.repo_root = Path(args.repo_root).resolve()
        derived_runtime_config: list[dict[str, Any]] = []
        if bool(getattr(args, "allow_provider_generation", False)):
            keep_alive = str(getattr(args, "keep_alive", "") or "").strip().lower()
            if keep_alive in {"", "0", "0s", "0m", "0h"}:
                args.keep_alive = "120s"
                derived_runtime_config.append(
                    {
                        "field": "keep_alive",
                        "effective_value": "120s",
                        "source": "derived_runtime_default",
                        "reason": "provider_generation_requires_nonzero_keep_alive",
                    }
                )
        setattr(args, "_derived_runtime_config", derived_runtime_config)
        if getattr(args, "request_file", ""):
            args.request = read_request_file(self.repo_root, args.request_file)
        self.stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_dir = Path(args.output_dir).resolve() if args.output_dir else None
        self.heap = ProviderRuntimeHeap.from_args(
            self.repo_root,
            self.stamp,
            self.path_arg(args.events, DEFAULT_EVENTS),
            self.path_arg(args.snapshot, DEFAULT_SNAPSHOT),
            self.path_arg(args.heap_markdown, DEFAULT_HEAP_MD),
        )
        self.budget_config = ProviderBudgetConfig(
            objective=args.objective,
            budget_minutes=args.budget_minutes,
            max_rounds=args.max_rounds,
            files_per_round=args.files_per_round,
            max_context_files=args.max_context_files,
            max_chars_per_file=args.max_chars_per_file,
            max_new_tokens=args.max_new_tokens,
            keep_alive=args.keep_alive,
            npu_micro_start_mode=args.npu_micro_start_mode,
            npu_micro_timeout_seconds=args.npu_micro_timeout_seconds,
            npu_final_wait_seconds=args.npu_final_wait_seconds,
            npu_max_context_chars=args.npu_max_context_chars,
            npu_max_prompt_chars=args.npu_max_prompt_chars,
            npu_max_new_tokens=args.npu_max_new_tokens,
            allow_provider_generation=args.allow_provider_generation,
            operator_intent=args.operator_intent,
        )
        self.budget_governor = build_heap_provider_budget_governor(
            self.budget_config, requested_max_iterations=args.max_iterations
        )
        self.time_counter_contract = build_provider_time_counter_contract(args)
        self.runtime_loop_started_at = monotonic()
        self.invocation_contract = build_heap_provider_invocation_contract(
            self.budget_governor,
            allow_provider_generation=args.allow_provider_generation,
            operator_intent=args.operator_intent,
        )
        self.max_iterations = clamp_loop_iterations(self.budget_config, args.max_iterations)
        self.state = make_state(args.objective, getattr(args, "request", ""))
        self.derived_runtime_config = list(getattr(args, "_derived_runtime_config", []) or [])
        self.state["derived_runtime_config"] = self.derived_runtime_config
        self.state["budget_governor"] = self.budget_governor
        self.state["invocation_contract"] = self.invocation_contract
        self.state["time_counter_contract"] = self.time_counter_contract
        self.heap_read_count = 0
        self.heap_write_count = 0
        self.tool_request_count = 0
        self.tool_execution_count = 0
        self.decision_count = 0
        self.candidate_operation_count = 0
        self.bridge_reports: list[str] = []
        self.provider_reports: list[dict[str, Any]] = []
        self.provider_execution_performed = False
        self.provider_revision_count = 0
        self.provider_revision_feedback = ""
        self.provider_recovery_attempt_count = 0
        self.provider_recovery_last_status: dict[str, Any] = {}
        self.provider_universe_blocked_reason = ""
        self.provider_universe_deferred_block_reason = ""
        self.gpu1_replight_valid = False
        self.gpu1_boot_leader_ready = False
        self.gpu1_primary_workload_valid = False
        self.gpu1_primary_evidence_valid = False
        self.gpu1_primary_evidence_source = ""
        self.gpu1_primary_workload_chars = 0
        self.gpu1_primary_workload_tokens = 0
        self.leader_source = "none"
        self.sidecars_start_policy = ""
        self.parallel_provider_overlap_seconds = 0.0
        self.gpu1_idle_after_primary_seconds = 0.0
        self.sidecar_alone_after_gpu1_seconds = 0.0
        self.provider_sidecar_scope_mode = "packet_review_only"
        self.provider_native_tool_call_ids: set[str] = set()
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.file_ref_resolver = RuntimeFileRefResolver(self.repo_root)
        self.repo_runtime_universe = RepoRuntimeUniverseBuilder(
            self.repo_root, self.output_dir
        ).build()
        self.runtime_universe_report_refs: dict[str, str] = {}
        self._code_execution_matrix_targets_cache: list[str] | None = None

    def runtime_elapsed_seconds(self) -> float:
        return max(0.0, monotonic() - self.runtime_loop_started_at)

    def runtime_soft_close_reached(self) -> bool:
        soft_close = int(self.time_counter_contract.get("soft_close_after_seconds") or 0)
        return bool(soft_close > 0 and self.runtime_elapsed_seconds() >= soft_close)

    def path_arg(self, explicit: str, default: str) -> str:
        # With --output-dir, parser defaults such as DEFAULT_OUTPUT/DEFAULT_MARKDOWN
        # are not operator-supplied explicit paths. They must resolve inside the
        # single run directory, otherwise the universe test writes the exit report
        # to the global default while the preflight/smoke reads the run_dir product.
        if explicit and not (self.output_dir and explicit == default):
            return explicit
        if not self.output_dir:
            return default
        mapping = {
            DEFAULT_EVENTS: "events.jsonl",
            DEFAULT_SNAPSHOT: "state.json",
            DEFAULT_HEAP_MD: "state.md",
            DEFAULT_BRIDGE_DIR: "broker_bridge",
            DEFAULT_BRIDGE_JSON: "broker_bridge.json",
            DEFAULT_BRIDGE_MD: "broker_bridge.md",
            DEFAULT_OUTPUT: "heap_runtime_completeness_gate_report.json",
            DEFAULT_MARKDOWN: "heap_runtime_completeness_gate_report.md",
        }
        filename = mapping.get(default)
        if not filename:
            return default
        return str(self.output_dir / filename)

    def child_python(self) -> str:
        """Return the project Python executable used for child tools.

        Policy: explicit --python-exe > repo .venv resolver. No system env/PATH
        fallback is introduced here.
        """
        explicit = str(getattr(self.args, "python_exe", "") or "").strip()
        if explicit:
            return str(Path(explicit).resolve())
        return resolve_child_python(self.repo_root)

    def runtime_context_dir(self) -> Path:
        if self.output_dir:
            path = self.output_dir / "team_context"
        else:
            path = (
                self.repo_root / "output" / "validation" / f"heap_runtime_team_context_{self.stamp}"
            )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def write_runtime_universe_report(self) -> dict[str, str]:
        if self.runtime_universe_report_refs:
            return self.runtime_universe_report_refs
        context_dir = self.runtime_context_dir()
        json_path = context_dir / "repo_runtime_universe.json"
        md_path = context_dir / "repo_runtime_universe.md"
        json_path.write_text(
            json.dumps(self.repo_runtime_universe.as_dict(), indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        md_path.write_text(render_universe_markdown(self.repo_runtime_universe), encoding="utf-8")
        self.runtime_universe_report_refs = {
            "json_report": repo_rel(self.repo_root, json_path),
            "markdown_report": repo_rel(self.repo_root, md_path),
        }
        return self.runtime_universe_report_refs

    def runtime_universe_prompt_summary(self, limit: int = 24) -> str:
        summary = self.repo_runtime_universe.summary()
        sources = "\n".join(
            f"- {item}"
            for item in filter_source_candidates_for_request(
                self.repo_runtime_universe.source_index,
                self.request_text(),
                limit=limit,
            )
        )
        tools = "\n".join(
            f"- {item.get('name')} args={item.get('allowed_args')}"
            for item in self.repo_runtime_universe.tool_catalog[:limit]
        )
        return (
            "RUNTIME_FILE_UNIVERSE:\n"
            f"- source_count={summary.get('source_count')} validation_count={summary.get('validation_count')} "
            f"tool_catalog_count={summary.get('tool_catalog_count')} "
            f"startup_artifact_ref_count={summary.get('startup_artifact_ref_count')}\n"
            "Broker-owned real tools available to request through tool_requests only:\n"
            f"{tools or '- none'}\n"
            "Verified source target examples from local filesystem:\n"
            f"{sources or '- none'}"
        )

    def historical_tool_context_files(self) -> list[str]:
        """Return existing canonical/historical maps that help choose reusable tools."""
        refs: list[str] = []
        for rel_path in HISTORICAL_TOOL_CONTEXT_FILES:
            if (self.repo_root / rel_path).exists():
                refs.append(rel_path)
        return refs
