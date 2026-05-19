from __future__ import annotations

from py_mesh_common import *  # noqa: F403

def run_provider_mesh(ctx: WorkflowContext) -> None:
    if not ctx.args.RunGpuNpuProvider:
        ctx.warnings.append(
            "GPU/NPU provider orchestrator skipped; rerun with -RunGpuNpuProvider for full provider execution."
        )
        return
    if not ctx.args.RunLegacyNpuAuditorProvider:
        ctx.warnings.append(
            "legacy NPU auditor provider disabled; production NPU execution uses the micro peer support lane."
        )
    provider_args = [
        "-m",
        "Tools.ai",
        "gpu_npu_parallel_orchestrator",
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
        *sum(
            (
                ["--report-file", p]
                for p in existing(
                    ctx,
                    "repo_consistency_json",
                    "repo_consistency_smoke_json",
                    "code_interpreter_json",
                    "line_count_json",
                    "python_syntax_json",
                    "gpu_contract_smoke_json",
                    "deterministic_smoke_json",
                    "decision_loop_smoke_json",
                    "npu_env_json",
                    "openvino_governance_json",
                    "gpu0_companion_json",
                    "gpu0_companion_contract_json",
                    "memory_workflow",
                )
            ),
            [],
        ),
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
    npu_mesh_mode = normalized_npu_micro_start_mode(ctx)
    if not ctx.args.SkipNpuMicroProvider and npu_mesh_mode == "startup":
        provider_args.append("--run-npu-micro-support-provider")
    elif npu_mesh_mode == "final-provider":
        ctx.warnings.append(
            "NPU micro provider will run as a final peer pass; live provider mesh still requires GPU1/GPU0 heap events."
        )
    elif npu_mesh_mode in {"deferred", "live-seed-only"}:
        ctx.warnings.append(
            f"NPU micro provider is {npu_mesh_mode}; provider mesh keeps NPU off the live GPU1/GPU0 critical path. "
            "The post-GPU peer-exchange NPU assistant and brokered telemetry remain available."
        )
    else:
        ctx.warnings.append(
            f"NPU micro provider disabled/degraded by workflow option: {npu_mesh_mode}"
        )

    if ctx.args.RunLegacyNpuAuditorProvider:
        provider_args += [
            "--run-npu-auditor-provider",
            "--npu-auditor-every-rounds",
            str(ctx.args.NpuAuditorEveryRounds),
            "--max-concurrent-npu-audits",
            "1",
            "--npu-auditor-timeout-seconds",
            str(ctx.args.NpuAuditorTimeoutSeconds),
            "--npu-max-context-chars",
            str(ctx.args.NpuMaxContextChars),
            "--npu-max-prompt-chars",
            str(ctx.args.NpuMaxPromptChars),
            "--npu-max-new-tokens",
            str(ctx.args.NpuMaxNewTokens),
            "--npu-final-wait-seconds",
            str(ctx.args.NpuFinalWaitSeconds),
        ]
    ctx.run_python(
        "GPU1 primary advisory orchestrator",
        provider_args,
        timeout=max(120, ctx.args.BudgetMinutes * 90),
    )
    ensure_required_provider_artifacts(ctx)
    if Path(ctx.p("gpu_json")).exists():
        ctx.run_python(
            "Replay GPU planner JSON contract",
            [
                "-m",
                "Tools.ai",
                "replay_gpu_planner_json_contract",
                "--repo-root",
                ".",
                "--gpu-report",
                ctx.p("gpu_json"),
                "--output",
                ctx.p("gpu_replay_json"),
                "--markdown-output",
                ctx.p("gpu_replay_md"),
            ],
        )
    if Path(ctx.p("orch_json")).exists():
        ctx.run_python(
            "Analyze GPU/NPU run sync",
            [
                "-m",
                "Tools.ai",
                "gpu_npu_run_sync_analysis",
                "--repo-root",
                ".",
                "--orchestrator",
                ctx.p("orch_json"),
                "--output",
                ctx.p("gpu_npu_sync_json"),
                "--markdown-output",
                ctx.p("gpu_npu_sync_md"),
            ],
        )

def normalized_npu_micro_start_mode(ctx: WorkflowContext) -> str:
    raw = str(getattr(ctx.args, "NpuMicroStartMode", "startup") or "startup").strip().lower()
    if raw == "peer":
        return "startup"
    if raw == "post-gpu-provider":
        return "final-provider"
    return raw

def npu_peer_provider_enabled(ctx: WorkflowContext) -> bool:
    return normalized_npu_micro_start_mode(ctx) == "final-provider"

def write_npu_peer_nonblocking_placeholder(
    ctx: WorkflowContext,
    reason: str,
    classification: str = "npu_peer_provider_deferred_to_avoid_openvino_contention",
) -> None:
    mode = str(getattr(ctx.args, "NpuMicroStartMode", "deferred") or "deferred")
    npu_payload = {
        "schema_version": 1,
        "kind": "npu_micro_peer_assistant",
        "generated_at": now_iso(),
        "stamp": ctx.args.Stamp,
        "passed": True,
        "classification": classification,
        "provider_execution_requested": False,
        "provider_execution_performed": False,
        "provider_execution_succeeded": False,
        "provider_empty_response": False,
        "non_blocking": True,
        "deferred_to_avoid_openvino_contention": True,
        "npu_micro_start_mode": mode,
        "reason": reason,
        "tool_request_count": 0,
        "tool_requests": [],
        "npu_deterministic_tool_fallback_used": False,
        "npu_deterministic_tool_fallback_count": 0,
        "runtime_tool_context_seen": True,
        "runtime_tool_context_report_count": len(
            existing(
                ctx,
                "gpu0_broker_json",
                "gpu0_response_json",
                "heap_snapshot_json",
                "heap_broker_json",
            )
        ),
        "warnings": [reason],
        "errors": [],
        "decision": {
            "npu_primary_advisory": False,
            "manual_review_required": True,
            "product_pass_blocker": False,
            "deferred_to_avoid_openvino_contention": True,
        },
        "guardrails": {
            "report_only": True,
            "npu_micro_lane_non_blocking": True,
            "npu_primary_advisory": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
    broker_payload = {
        "schema_version": 1,
        "kind": "agent_runtime_tool_broker",
        "generated_at": now_iso(),
        "stamp": ctx.args.Stamp,
        "passed": True,
        "executed": False,
        "classification": "npu_peer_provider_deferred_noop_broker",
        "enabled": False,
        "requested_tool_count": 0,
        "tool_request_count": 0,
        "tool_execution_count": 0,
        "failed_tool_count": 0,
        "blocked_tool_count": 0,
        "tool_results": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "persistent_memory_write_performed": False,
        "warnings": [reason],
        "errors": [],
        "guardrails": {
            "report_only": True,
            "noop_broker_for_deferred_npu_peer": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
    write_json(ctx.p("npu_micro_json"), npu_payload)
    write_text(
        ctx.p("npu_micro_md"),
        [
            "# NPU Micro Peer Assistant",
            "",
            "- Passed: `True`",
            "- Provider execution requested: `False`",
            "- Provider execution performed: `False`",
            "- Non-blocking: `True`",
            f"- Mode: `{mode}`",
            f"- Classification: `{npu_payload['classification']}`",
            f"- Reason: {reason}",
        ],
    )
    write_json(ctx.p("npu_broker_json"), broker_payload)
    write_text(
        ctx.p("npu_broker_md"),
        [
            "# NPU Micro Runtime Tool Broker",
            "",
            "- Passed: `True`",
            "- Executed: `False`",
            "- Tool execution count: `0`",
            f"- Classification: `{broker_payload['classification']}`",
            f"- Reason: {reason}",
        ],
    )
