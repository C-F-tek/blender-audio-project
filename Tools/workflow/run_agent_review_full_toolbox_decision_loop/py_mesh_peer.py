from __future__ import annotations

from py_mesh_common import *  # noqa: F403
from py_mesh_provider import normalized_npu_micro_start_mode, npu_peer_provider_enabled, write_npu_peer_nonblocking_placeholder

def run_peer_exchange(ctx: WorkflowContext) -> None:
    if not ctx.args.RunGpuNpuProvider or not Path(ctx.p("gpu_json")).exists():
        if ctx.args.RunGpuNpuProvider:
            ctx.warnings.append(
                f"AI peer-exchange skipped because GPU primary report is missing: {ctx.p('gpu_json')}"
            )
        return
    common = [
        "--repo-root",
        ".",
        "--stamp",
        ctx.args.Stamp,
        "--gpu-report",
        ctx.p("gpu_json"),
        "--gpu-markdown",
        ctx.p("gpu_md"),
    ]
    ctx.run_python(
        "Build AI peer-exchange packet",
        [
            "-m",
            "Tools.ai",
            "peer_exchange_packet",
            *common,
            *sum(
                (
                    ["--source-report", p]
                    for p in existing(
                        ctx,
                        "evidence",
                        "repo_consistency_json",
                        "repo_consistency_smoke_json",
                        "code_interpreter_json",
                        "line_count_json",
                        "python_syntax_json",
                        "npu_env_json",
                        "openvino_governance_json",
                        "gpu0_companion_json",
                        "gpu0_companion_contract_json",
                    )
                ),
                [],
            ),
            "--primary-output",
            ctx.p("gpu1_primary_json"),
            "--primary-markdown-output",
            ctx.p("gpu1_primary_md"),
            "--task-output",
            ctx.p("gpu0_task_json"),
            "--exchange-output",
            ctx.p("peer_json"),
            "--exchange-markdown-output",
            ctx.p("peer_md"),
        ],
    )
    live_signal(
        ctx,
        "gpu1-request",
        "Provider runtime heap GPU1 to GPU0 live request",
        "heap_gpu1_request_json",
        "heap_gpu1_request_md",
        [
            "--gpu1-report",
            ctx.p("gpu1_primary_json"),
            "--gpu0-task-packet",
            ctx.p("gpu0_task_json"),
            "--round",
            "1",
        ],
    )
    ctx.run_python(
            "GPU0 peer companion worker",
            [
            "-m",
            "Tools.ai",
            "run_gpu0_peer_companion_worker",
            "--repo-root",
            ".",
            "--stamp",
            ctx.args.Stamp,
            "--task-packet",
            ctx.p("gpu0_task_json"),
            "--primary-advisory",
            ctx.p("gpu1_primary_json"),
            "--output",
            ctx.p("gpu0_response_json"),
            "--markdown-output",
            ctx.p("gpu0_response_md"),
            "--tool-requests-output",
            ctx.p("gpu0_tools_json"),
            "--runtime-heap-stamp",
            ctx.args.Stamp,
            "--runtime-heap-events",
            ctx.p("heap_events"),
            "--runtime-heap-snapshot",
            ctx.p("heap_snapshot_json"),
            "--runtime-heap-markdown",
            ctx.p("heap_snapshot_md"),
            "--iterations",
            "32",
            "--min-seconds",
            "1",
            "--allow-degraded",
        ],
    )
    ctx.run_python(
            "GPU0 peer runtime tool broker",
            [
            "-m",
            "Tools.ai",
            "agent_runtime_tool_broker",
            "--repo-root",
            ".",
            "--request-file",
            ctx.p("gpu0_tools_json"),
            "--tool-output-dir",
            f"{ctx.p('runtime_tool_dir')}/gpu0_peer",
            "--stamp",
            ctx.args.Stamp,
            "--timeout-seconds",
            "240",
            "--output",
            ctx.p("gpu0_broker_json"),
            "--markdown-output",
            ctx.p("gpu0_broker_md"),
        ],
    )
    live_signal(
        ctx,
        "broker-results",
        "Provider runtime heap GPU0 broker live results",
        "heap_broker_json",
        "heap_broker_md",
        ["--broker-report", ctx.p("gpu0_broker_json"), "--round", "1"],
    )
    if npu_peer_provider_enabled(ctx):
        ctx.run_python(
            "NPU micro peer assistant",
            [
                "-m",
                "Tools.ai",
                "npu_gpu_deep_review_auditor",
                "--repo-root",
                ".",
                "--gpu-review",
                ctx.p("gpu_json"),
                "--run-npu",
                "--runtime-tool-context-report",
                ctx.p("gpu0_broker_json"),
                "--runtime-tool-context-report",
                ctx.p("gpu0_response_json"),
                "--runtime-tool-context-report",
                ctx.p("heap_snapshot_json"),
                "--runtime-tool-context-report",
                ctx.p("heap_broker_json"),
                "--context-output",
                ctx.p("npu_context_md"),
                "--npu-output",
                ctx.p("npu_output_md"),
                "--npu-notes-output",
                ctx.p("npu_notes_md"),
                "--npu-metadata-output",
                ctx.p("npu_metadata_json"),
                "--output",
                ctx.p("npu_micro_json"),
                "--markdown-output",
                ctx.p("npu_micro_md"),
                "--timeout-seconds",
                str(ctx.args.NpuMicroTimeoutSeconds),
                "--max-context-chars",
                str(ctx.args.NpuMaxContextChars),
                "--max-prompt-chars",
                str(ctx.args.NpuMaxPromptChars),
                "--max-new-tokens",
                str(ctx.args.NpuMaxNewTokens),
                "--max-runtime-tool-context-chars",
                "6000",
                "--max-npu-tool-requests",
                "4",
            ],
        )
        live_signal(
            ctx,
            "npu-support",
            "Provider runtime heap NPU live support",
            "heap_npu_json",
            "heap_npu_md",
            ["--npu-report", ctx.p("npu_micro_json"), "--round", "1"],
        )
        ctx.run_python(
            "NPU micro runtime tool broker",
            [
                "-m",
                "Tools.ai",
                "agent_runtime_tool_broker",
                "--repo-root",
                ".",
                "--request-file",
                ctx.p("npu_micro_json"),
                "--tool-output-dir",
                f"{ctx.p('runtime_tool_dir')}/npu_micro",
                "--stamp",
                ctx.args.Stamp,
                "--timeout-seconds",
                str(ctx.args.NpuMicroBrokerTimeoutSeconds),
                "--output",
                ctx.p("npu_broker_json"),
                "--markdown-output",
                ctx.p("npu_broker_md"),
            ],
        )
    else:
        npu_mesh_mode = normalized_npu_micro_start_mode(ctx)
        if npu_mesh_mode == "startup":
            reason = "Final NPU provider pass moved off the performance path; startup NPU support and broker seed evidence are reviewed by GPU1/GPU0 plus deterministic validators."
            classification = "npu_final_provider_moved_to_gpu_peer_review"
        else:
            reason = f"NPU peer provider mode {npu_mesh_mode} did not run as final-provider; startup provider mesh remains the default real-product lane."
            classification = "npu_peer_provider_not_final_provider"
        write_npu_peer_nonblocking_placeholder(ctx, reason, classification)
        live_signal(
            ctx,
            "npu-support",
            "Provider runtime heap NPU deferred support placeholder",
            "heap_npu_json",
            "heap_npu_md",
            ["--npu-report", ctx.p("npu_micro_json"), "--round", "1"],
        )
    ctx.run_python(
        "Finalize AI peer-exchange packet",
        [
            "-m",
            "Tools.ai",
            "peer_exchange_packet",
            *common,
            *sum(
                (
                    ["--source-report", p]
                    for p in existing(
                        ctx,
                        "evidence",
                        "repo_consistency_json",
                        "code_interpreter_json",
                        "gpu0_response_json",
                        "npu_micro_json",
                    )
                ),
                [],
            ),
            "--response-report",
            ctx.p("gpu0_response_json"),
            "--broker-report",
            ctx.p("gpu0_broker_json"),
            "--npu-report",
            ctx.p("npu_micro_json"),
            "--npu-broker-report",
            ctx.p("npu_broker_json"),
            "--primary-output",
            ctx.p("gpu1_primary_json"),
            "--primary-markdown-output",
            ctx.p("gpu1_primary_md"),
            "--task-output",
            ctx.p("gpu0_task_json"),
            "--exchange-output",
            ctx.p("peer_json"),
            "--exchange-markdown-output",
            ctx.p("peer_md"),
        ],
    )
    ctx.run_python(
        "AI peer-exchange contract",
        [
            "-m",
            "Tools.validation",
            "ai_peer_exchange_contract",
            "--repo-root",
            ".",
            "--stamp",
            ctx.args.Stamp,
            "--broker-report",
            ctx.p("gpu0_broker_json"),
            "--npu-response",
            ctx.p("npu_micro_json"),
            "--npu-broker-report",
            ctx.p("npu_broker_json"),
            "--require-broker-execution",
            "--allow-degraded",
            "--output",
            ctx.p("peer_contract_json"),
            "--markdown-output",
            ctx.p("peer_contract_md"),
        ],
    )
    ctx.run_python(
        "Provider runtime heap from peer reports",
        [
            "-m",
            "Tools.ai",
            "build_provider_runtime_heap_from_peer_reports",
            "--repo-root",
            ".",
            "--stamp",
            ctx.args.Stamp,
            "--gpu1-report",
            ctx.p("gpu1_primary_json"),
            "--gpu0-report",
            ctx.p("gpu0_response_json"),
            "--gpu0-tool-requests",
            ctx.p("gpu0_tools_json"),
            "--gpu0-broker-report",
            ctx.p("gpu0_broker_json"),
            "--npu-report",
            ctx.p("npu_micro_json"),
            "--npu-broker-report",
            ctx.p("npu_broker_json"),
            "--peer-exchange-report",
            ctx.p("peer_json"),
            "--peer-contract-report",
            ctx.p("peer_contract_json"),
            "--output",
            ctx.p("heap_from_peer_json"),
            "--markdown-output",
            ctx.p("heap_from_peer_md"),
        ],
    )
    contract = [
        "-m",
        "Tools.validation",
        "provider_evidence_contract",
        "--repo-root",
        ".",
        "--stamp",
        ctx.args.Stamp,
        "--orchestrator",
        ctx.p("orch_json"),
        "--gpu-report",
        ctx.p("gpu_json"),
        "--gpu-npu-sync",
        ctx.p("gpu_npu_sync_json"),
        "--local-provider-probe",
        "output/validation/local_provider_probe.json",
        "--openvino-gpu0-workload",
        ctx.p("gpu0_support_bootstrap"),
        "--output",
        ctx.p("provider_contract_json"),
        "--markdown-output",
        ctx.p("provider_contract_md"),
    ]
    if ctx.args.RequireProviderArtifacts:
        contract += ["--require-gpu-provider", "--require-openvino-gpu0-secondary"]
        if ctx.args.RunLegacyNpuAuditorProvider:
            contract.append("--require-npu-auditor")
    ctx.run_python("Strict provider evidence contract", contract)
