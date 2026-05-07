"""Provider mesh phases for the Python full-toolbox workflow engine."""
from __future__ import annotations

from pathlib import Path

from py_support import WorkflowContext, add_existing, now_iso, write_json, write_text


def existing(ctx: WorkflowContext, *keys: str) -> list[str]:
    return [ctx.p(key) for key in keys if Path(ctx.p(key)).exists()]


def add_reports(ctx: WorkflowContext, *keys: str) -> None:
    for key in keys:
        add_existing(ctx.reports, ctx.p(key))


def add_artifacts(ctx: WorkflowContext, *keys: str) -> None:
    for key in keys:
        add_existing(ctx.artifacts, ctx.p(key))


def live_signal(ctx: WorkflowContext, mode: str, label: str, json_key: str, md_key: str, extra: list[str] | None = None) -> None:
    ctx.run_python(
        label,
        [
            "Tools/ai/provider_runtime_heap_live_signals.py",
            "--repo-root",
            ".",
            "--stamp",
            ctx.args.Stamp,
            "--mode",
            mode,
            "--events",
            ctx.p("heap_events"),
            "--snapshot",
            ctx.p("heap_snapshot_json"),
            "--heap-markdown",
            ctx.p("heap_snapshot_md"),
            "--output",
            ctx.p(json_key),
            "--markdown-output",
            ctx.p(md_key),
            *(extra or []),
        ],
    )
    add_reports(ctx, json_key, "heap_snapshot_json")
    add_artifacts(ctx, md_key, "heap_snapshot_md", "heap_events")


def ensure_required_provider_artifacts(ctx: WorkflowContext) -> None:
    if not ctx.args.RunGpuNpuProvider or not ctx.args.RequireProviderArtifacts:
        return
    missing = [key for key in ("evidence", "orch_json", "gpu_json") if not Path(ctx.p(key)).exists()]
    if not missing:
        return
    for key in missing:
        ctx.errors.append(f"required provider artifact missing: {ctx.p(key)}")
    fallback = {
        "schema_version": 1,
        "generated_at": now_iso(),
        "stamp": ctx.args.Stamp,
        "passed": False,
        "provider_execution_requested": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "classification": "required_provider_artifact_missing",
        "guardrails": {"report_only": True, "patch_application_performed": False, "source_writes_performed": False},
    }
    if "orch_json" in missing:
        write_json(ctx.p("orch_json"), dict(fallback, kind="agent_gpu_npu_parallel_orchestrator"))
        write_text(ctx.p("orch_md"), ["# Required provider orchestrator fallback", "", "- Passed: `False`"])
    if "gpu_json" in missing:
        write_json(ctx.p("gpu_json"), dict(fallback, kind="agent_gpu_parallel_report", provider_empty_response=True, recommendation_count=0, recommendations=[]))
        write_text(ctx.p("gpu_md"), ["# Required GPU provider fallback", "", "- Passed: `False`"])
    if "evidence" in missing:
        write_json(ctx.p("evidence"), dict(fallback, kind="agent_review_evidence_sufficiency", evidence_sufficient=False))


def run_provider_mesh(ctx: WorkflowContext) -> None:
    if not ctx.args.RunGpuNpuProvider:
        ctx.warnings.append("GPU/NPU provider orchestrator skipped; rerun with -RunGpuNpuProvider for full provider execution.")
        return
    if not ctx.args.RunLegacyNpuAuditorProvider:
        ctx.warnings.append("legacy NPU auditor provider disabled; production NPU execution uses the micro peer support lane.")
    provider_args = [
        "Tools/ai/run_agent_gpu_npu_parallel_orchestrator.py",
        "--repo-root",
        ".",
        "--budget-minutes",
        str(ctx.args.BudgetMinutes),
        "--max-rounds",
        str(ctx.args.MaxRounds),
        "--files-per-round",
        str(ctx.args.FilesPerRound),
        "--max-context-files",
        str(ctx.args.MaxContextFiles),
        "--max-chars-per-file",
        str(ctx.args.MaxCharsPerFile),
        "--max-new-tokens",
        str(ctx.args.MaxNewTokens),
        "--keep-alive",
        ctx.args.KeepAlive,
        "--evidence",
        ctx.p("evidence"),
        "--refined-review",
        ctx.p("refined_review"),
        *sum((["--report-file", p] for p in existing(ctx, "repo_consistency_json", "repo_consistency_smoke_json", "code_interpreter_json", "line_count_json", "python_syntax_json", "gpu_contract_smoke_json", "deterministic_smoke_json", "decision_loop_smoke_json", "npu_env_json", "gpu0_companion_json", "gpu0_companion_contract_json", "memory_workflow")), []),
        "--enable-runtime-tool-broker",
        "--run-gpu0-peer-support-provider",
        "--gpu0-peer-support-dir",
        ctx.p("gpu0_support_dir"),
        "--gpu0-peer-support-every-rounds",
        "1",
        "--gpu0-peer-support-iterations",
        "24",
        "--gpu0-peer-support-min-seconds",
        "1",
        "--run-npu-micro-support-provider",
        "--npu-micro-support-dir",
        ctx.p("npu_support_dir"),
        "--npu-micro-support-every-rounds",
        "1",
        "--npu-micro-support-timeout-seconds",
        str(ctx.args.NpuMicroTimeoutSeconds),
        "--npu-micro-support-final-wait-seconds",
        str(ctx.args.NpuFinalWaitSeconds),
        "--npu-micro-support-max-context-chars",
        str(ctx.args.NpuMaxContextChars),
        "--npu-micro-support-max-prompt-chars",
        str(ctx.args.NpuMaxPromptChars),
        "--npu-micro-support-max-new-tokens",
        str(ctx.args.NpuMaxNewTokens),
        "--runtime-heap-stamp",
        ctx.args.Stamp,
        "--runtime-heap-events",
        ctx.p("heap_events"),
        "--runtime-heap-snapshot",
        ctx.p("heap_snapshot_json"),
        "--runtime-heap-markdown",
        ctx.p("heap_snapshot_md"),
        "--runtime-tool-output-dir",
        ctx.p("runtime_tool_dir"),
        "--runtime-tool-timeout-seconds",
        "300",
        "--context-root",
        "docs",
        "--context-root",
        "Tools/ai",
        "--context-root",
        "Tools/validation",
        "--context-root",
        "Tools/workflow",
        "--context-root",
        "Tools/npu",
        "--context-root",
        ctx.p("line_count_all_md"),
        "--checkpoint-dir",
        ctx.p("checkpoint_dir"),
        "--gpu-output",
        ctx.p("gpu_json"),
        "--gpu-markdown-output",
        ctx.p("gpu_md"),
        "--output",
        ctx.p("orch_json"),
        "--markdown-output",
        ctx.p("orch_md"),
    ]
    if ctx.args.RunLegacyNpuAuditorProvider:
        provider_args += ["--run-npu-auditor-provider", "--npu-auditor-every-rounds", str(ctx.args.NpuAuditorEveryRounds), "--max-concurrent-npu-audits", "1", "--npu-auditor-timeout-seconds", str(ctx.args.NpuAuditorTimeoutSeconds), "--npu-max-context-chars", str(ctx.args.NpuMaxContextChars), "--npu-max-prompt-chars", str(ctx.args.NpuMaxPromptChars), "--npu-max-new-tokens", str(ctx.args.NpuMaxNewTokens), "--npu-final-wait-seconds", str(ctx.args.NpuFinalWaitSeconds)]
    ctx.run_python("GPU1 primary advisory orchestrator", provider_args, timeout=max(120, ctx.args.BudgetMinutes * 90))
    ensure_required_provider_artifacts(ctx)
    if Path(ctx.p("gpu_json")).exists():
        ctx.run_python("Replay GPU planner JSON contract", ["Tools/ai/replay_gpu_planner_json_contract.py", "--repo-root", ".", "--gpu-report", ctx.p("gpu_json"), "--output", ctx.p("gpu_replay_json"), "--markdown-output", ctx.p("gpu_replay_md")])
    if Path(ctx.p("orch_json")).exists():
        ctx.run_python("Analyze GPU/NPU run sync", ["Tools/ai/analyze_gpu_npu_run_sync.py", "--repo-root", ".", "--orchestrator", ctx.p("orch_json"), "--output", ctx.p("gpu_npu_sync_json"), "--markdown-output", ctx.p("gpu_npu_sync_md")])


def run_peer_exchange(ctx: WorkflowContext) -> None:
    if not ctx.args.RunGpuNpuProvider or not Path(ctx.p("gpu_json")).exists():
        if ctx.args.RunGpuNpuProvider:
            ctx.warnings.append(f"AI peer-exchange skipped because GPU primary report is missing: {ctx.p('gpu_json')}")
        return
    common = ["--repo-root", ".", "--stamp", ctx.args.Stamp, "--gpu-report", ctx.p("gpu_json"), "--gpu-markdown", ctx.p("gpu_md")]
    ctx.run_python("Build AI peer-exchange packet", ["Tools/ai/build_ai_peer_exchange_packet.py", *common, *sum((["--source-report", p] for p in existing(ctx, "evidence", "repo_consistency_json", "repo_consistency_smoke_json", "code_interpreter_json", "line_count_json", "python_syntax_json", "npu_env_json", "gpu0_companion_json", "gpu0_companion_contract_json")), []), "--primary-output", ctx.p("gpu1_primary_json"), "--primary-markdown-output", ctx.p("gpu1_primary_md"), "--task-output", ctx.p("gpu0_task_json"), "--exchange-output", ctx.p("peer_json"), "--exchange-markdown-output", ctx.p("peer_md")])
    live_signal(ctx, "gpu1-request", "Provider runtime heap GPU1 to GPU0 live request", "heap_gpu1_request_json", "heap_gpu1_request_md", ["--gpu1-report", ctx.p("gpu1_primary_json"), "--gpu0-task-packet", ctx.p("gpu0_task_json"), "--round", "1"])
    ctx.run_python("GPU0 peer companion worker", ["Tools/ai/run_gpu0_peer_companion_worker.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--task-packet", ctx.p("gpu0_task_json"), "--primary-advisory", ctx.p("gpu1_primary_json"), "--output", ctx.p("gpu0_response_json"), "--markdown-output", ctx.p("gpu0_response_md"), "--tool-requests-output", ctx.p("gpu0_tools_json"), "--runtime-heap-stamp", ctx.args.Stamp, "--runtime-heap-events", ctx.p("heap_events"), "--runtime-heap-snapshot", ctx.p("heap_snapshot_json"), "--runtime-heap-markdown", ctx.p("heap_snapshot_md"), "--iterations", "32", "--min-seconds", "1", "--allow-degraded"])
    ctx.run_python("GPU0 peer runtime tool broker", ["Tools/ai/agent_runtime_tool_broker.py", "--repo-root", ".", "--request-file", ctx.p("gpu0_tools_json"), "--tool-output-dir", f"{ctx.p('runtime_tool_dir')}/gpu0_peer", "--stamp", ctx.args.Stamp, "--timeout-seconds", "240", "--output", ctx.p("gpu0_broker_json"), "--markdown-output", ctx.p("gpu0_broker_md")])
    live_signal(ctx, "broker-results", "Provider runtime heap GPU0 broker live results", "heap_broker_json", "heap_broker_md", ["--broker-report", ctx.p("gpu0_broker_json"), "--round", "1"])
    ctx.run_python("NPU micro peer assistant", ["Tools/ai/run_npu_gpu_deep_review_auditor.py", "--repo-root", ".", "--gpu-review", ctx.p("gpu_json"), "--run-npu", "--runtime-tool-context-report", ctx.p("gpu0_broker_json"), "--runtime-tool-context-report", ctx.p("gpu0_response_json"), "--runtime-tool-context-report", ctx.p("heap_snapshot_json"), "--runtime-tool-context-report", ctx.p("heap_broker_json"), "--context-output", ctx.p("npu_context_md"), "--npu-output", ctx.p("npu_output_md"), "--npu-notes-output", ctx.p("npu_notes_md"), "--npu-metadata-output", ctx.p("npu_metadata_json"), "--output", ctx.p("npu_micro_json"), "--markdown-output", ctx.p("npu_micro_md"), "--timeout-seconds", str(ctx.args.NpuMicroTimeoutSeconds), "--max-context-chars", str(ctx.args.NpuMaxContextChars), "--max-prompt-chars", str(ctx.args.NpuMaxPromptChars), "--max-new-tokens", str(ctx.args.NpuMaxNewTokens), "--max-runtime-tool-context-chars", "6000", "--max-npu-tool-requests", "4"])
    live_signal(ctx, "npu-support", "Provider runtime heap NPU live support", "heap_npu_json", "heap_npu_md", ["--npu-report", ctx.p("npu_micro_json"), "--round", "1"])
    ctx.run_python("NPU micro runtime tool broker", ["Tools/ai/agent_runtime_tool_broker.py", "--repo-root", ".", "--request-file", ctx.p("npu_micro_json"), "--tool-output-dir", f"{ctx.p('runtime_tool_dir')}/npu_micro", "--stamp", ctx.args.Stamp, "--timeout-seconds", str(ctx.args.NpuMicroBrokerTimeoutSeconds), "--output", ctx.p("npu_broker_json"), "--markdown-output", ctx.p("npu_broker_md")])
    ctx.run_python("Finalize AI peer-exchange packet", ["Tools/ai/build_ai_peer_exchange_packet.py", *common, *sum((["--source-report", p] for p in existing(ctx, "evidence", "repo_consistency_json", "code_interpreter_json", "gpu0_response_json", "npu_micro_json")), []), "--response-report", ctx.p("gpu0_response_json"), "--broker-report", ctx.p("gpu0_broker_json"), "--npu-report", ctx.p("npu_micro_json"), "--npu-broker-report", ctx.p("npu_broker_json"), "--primary-output", ctx.p("gpu1_primary_json"), "--primary-markdown-output", ctx.p("gpu1_primary_md"), "--task-output", ctx.p("gpu0_task_json"), "--exchange-output", ctx.p("peer_json"), "--exchange-markdown-output", ctx.p("peer_md")])
    ctx.run_python("AI peer-exchange contract", ["Tools/validation/check_ai_peer_exchange_contract.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--broker-report", ctx.p("gpu0_broker_json"), "--npu-response", ctx.p("npu_micro_json"), "--npu-broker-report", ctx.p("npu_broker_json"), "--require-broker-execution", "--allow-degraded", "--output", ctx.p("peer_contract_json"), "--markdown-output", ctx.p("peer_contract_md")])
    ctx.run_python("Provider runtime heap from peer reports", ["Tools/ai/build_provider_runtime_heap_from_peer_reports.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--gpu1-report", ctx.p("gpu1_primary_json"), "--gpu0-report", ctx.p("gpu0_response_json"), "--gpu0-tool-requests", ctx.p("gpu0_tools_json"), "--gpu0-broker-report", ctx.p("gpu0_broker_json"), "--npu-report", ctx.p("npu_micro_json"), "--npu-broker-report", ctx.p("npu_broker_json"), "--peer-exchange-report", ctx.p("peer_json"), "--peer-contract-report", ctx.p("peer_contract_json"), "--output", ctx.p("heap_from_peer_json"), "--markdown-output", ctx.p("heap_from_peer_md")])
    ctx.run_python("Provider runtime heap telemetry", ["Tools/ai/build_provider_runtime_heap_telemetry.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--output", ctx.p("heap_telemetry_json"), "--markdown-output", ctx.p("heap_telemetry_md")])
    contract = ["Tools/validation/check_provider_evidence_contract.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--orchestrator", ctx.p("orch_json"), "--gpu-report", ctx.p("gpu_json"), "--gpu-npu-sync", ctx.p("gpu_npu_sync_json"), "--local-provider-probe", "output/validation/local_provider_probe.json", "--openvino-gpu0-workload", ctx.p("gpu0_support_bootstrap"), "--output", ctx.p("provider_contract_json"), "--markdown-output", ctx.p("provider_contract_md")]
    if ctx.args.RequireProviderArtifacts:
        contract += ["--require-gpu-provider", "--require-openvino-gpu0-secondary"]
        if ctx.args.RunLegacyNpuAuditorProvider:
            contract.append("--require-npu-auditor")
    ctx.run_python("Strict provider evidence contract", contract)
