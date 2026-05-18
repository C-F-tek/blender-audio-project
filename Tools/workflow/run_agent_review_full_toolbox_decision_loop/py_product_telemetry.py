from __future__ import annotations

from py_mesh import existing, live_signal
from py_product_common import *  # noqa: F403

def run_runtime_telemetry(ctx: WorkflowContext, label: str) -> None:
    ctx.run_python(
        label,
        [
            "-m",
            "Tools.ai",
            "runtime_tool_usage_telemetry",
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
            "--decision-loop",
            ctx.p("decision_json"),
            "--broker-report",
            ctx.p("runtime_broker_json"),
            "--broker-report",
            ctx.p("gpu0_broker_json"),
            "--broker-report",
            ctx.p("npu_broker_json"),
            "--output",
            ctx.p("runtime_usage_json"),
            "--markdown-output",
            ctx.p("runtime_usage_md"),
        ],
    )
    ctx.run_python(
        "Runtime tool capability manifest",
        [
            "-m",
            "Tools.ai",
            "build_runtime_tool_capability_manifest",
            "--repo-root",
            ".",
            "--tool-usage",
            ctx.p("runtime_usage_json"),
            "--output",
            ctx.p("runtime_capability_json"),
            "--markdown-output",
            ctx.p("runtime_capability_md"),
        ],
    )
    live_signal(
        ctx,
        "tool-catalog-complete",
        "Provider runtime heap tool catalog exchange complete",
        "heap_catalog_json",
        "heap_catalog_md",
        [
            "--runtime-usage",
            ctx.p("runtime_usage_json"),
            "--runtime-capability",
            ctx.p("runtime_capability_json"),
            "--round",
            "1",
        ],
    )
    ctx.run_python(
        "Provider runtime heap telemetry refresh",
        [
            "-m",
            "Tools.ai",
            "build_provider_runtime_heap_telemetry",
            "--repo-root",
            ".",
            "--stamp",
            ctx.args.Stamp,
            "--output",
            ctx.p("heap_telemetry_json"),
            "--markdown-output",
            ctx.p("heap_telemetry_md"),
        ],
    )

def run_runtime_flow_map(ctx: WorkflowContext) -> None:
    report_keys = [
        "orch_json",
        "gpu_json",
        "gpu_npu_sync_json",
        "provider_contract_json",
        "peer_json",
        "peer_contract_json",
        "heap_snapshot_json",
        "heap_telemetry_json",
        "runtime_usage_json",
        "runtime_capability_json",
        "runtime_broker_json",
        "gpu0_broker_json",
        "npu_broker_json",
        "recommendations_json",
        "bridge_json",
        "decision_json",
        "patch_plan_json",
        "patch_quality_json",
        "patch_notes_quality_json",
        "repo_consistency_json",
        "repo_consistency_smoke_json",
        "final_product_json",
    ]
    args = [
        "-m",
        "Tools.ai",
        "runtime_flow_map",
        "--repo-root",
        ".",
        "--stamp",
        ctx.args.Stamp,
        "--entrypoint",
        "python -m Tools.workflow run_agent_review_full_toolbox_decision_loop",
        "--output",
        ctx.p("runtime_flow_json"),
        "--jsonl-output",
        ctx.p("runtime_flow_jsonl"),
        "--markdown-output",
        ctx.p("runtime_flow_md"),
        "--mermaid-output",
        ctx.p("runtime_flow_mmd"),
    ]
    args += sum((["--report", path] for path in existing(ctx, *report_keys)), [])
    ctx.run_python("Runtime flow map evidence", args)

def run_final_product(ctx: WorkflowContext) -> None:
    report_keys = [
        "orch_json",
        "gpu_json",
        "gpu_npu_sync_json",
        "provider_contract_json",
        "peer_json",
        "peer_contract_json",
        "heap_from_peer_json",
        "heap_telemetry_json",
        "heap_catalog_json",
        "heap_snapshot_json",
        "runtime_usage_json",
        "runtime_capability_json",
        "runtime_broker_json",
        "gpu0_broker_json",
        "npu_broker_json",
        "recommendations_json",
        "decision_json",
        "patch_plan_json",
        "patch_quality_json",
        "patch_notes_quality_json",
    ]
    artifact_keys = [
        "orch_md",
        "gpu_md",
        "gpu_npu_sync_md",
        "peer_md",
        "peer_contract_md",
        "heap_telemetry_md",
        "heap_catalog_md",
        "heap_snapshot_md",
        "runtime_usage_md",
        "runtime_capability_md",
        "patch_plan_md",
        "patch_quality_md",
        "patch_notes_quality_md",
    ]
    args = [
        "-m",
        "Tools.ai",
        "build_heap_runtime_product_package",
        "--repo-root",
        ".",
        "--output-dir",
        ctx.p("final_product_dir"),
        "--request",
        f"Build the final local AI product for stamp {ctx.args.Stamp} from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.",
        "--no-external-probes",
        "--timeout-seconds",
        "8",
        "--output",
        ctx.p("final_product_json"),
    ]
    args += sum((["--run-report", path] for path in existing(ctx, *report_keys)), [])
    args += sum((["--run-artifact", path] for path in existing(ctx, *artifact_keys)), [])
    ctx.run_python("Heap runtime final product", args)

def build_evidence_bundle(ctx: WorkflowContext) -> None:
    if not ctx.args.SkipSharedToolboxBundle:
        ctx.run_python(
            "Shared toolbox AI-to-AI bundle",
            [
                "-m",
                "Tools.ai.shared_toolbox_bundle",
                "--repo-root",
                ".",
                "--stamp",
                ctx.p("artifact_stamp"),
                "--output-dir",
                ctx.args.EvidenceDir,
                "--validate-bundle",
                "--recursive-max-files",
                "160",
                "--chunk-large-files-lines",
                "200",
            ],
        )
    else:
        ctx.warnings.append("shared toolbox bundle skipped by request")
    report_paths = existing(
        ctx,
        "orch_json",
        "gpu_json",
        *TOOL_REPORT_KEYS,
        "heap_from_peer_json",
        "patch_quality_json",
        "patch_notes_quality_json",
        "runtime_flow_json",
        "final_product_json",
        "final_product_manifest",
        "final_product_evidence",
        "final_product_readiness",
        "recommendations_json",
        "bridge_json",
        "decision_json",
        "patch_plan_json",
    )
    artifact_paths = existing(
        ctx,
        "repo_consistency_md",
        "repo_consistency_smoke_md",
        "line_count_all_md",
        "openvino_governance_md",
        "megalithic_review_md",
        "refined_review_md",
        "decision_md",
        "gpu1_primary_md",
        "gpu0_response_md",
        "npu_micro_md",
        "npu_broker_md",
        "peer_md",
        "peer_contract_md",
        "heap_from_peer_md",
        "heap_telemetry_md",
        "heap_init_md",
        "heap_gpu1_request_md",
        "heap_broker_md",
        "heap_npu_md",
        "heap_catalog_md",
        "heap_snapshot_md",
        "runtime_flow_jsonl",
        "runtime_flow_md",
        "runtime_flow_mmd",
        "final_product_md",
        "final_product_readme",
        "patch_plan_md",
        "patch_quality_md",
        "patch_notes_quality_md",
    )
    line_csv = ctx.paths.get("line_count_csv")
    if line_csv and Path(line_csv).exists():
        artifact_paths.append(line_csv)
    args = [
        "-m",
        "Tools.ai.repository_product.github_evidence_bundle",
        "--repo-root",
        ".",
        "--basename",
        ctx.p("bundle_base"),
        "--output-dir",
        ctx.args.EvidenceDir,
        "--report",
        ",".join(report_paths),
        "--max-included-artifact-chars",
        "16000",
        "--max-included-artifacts",
        "42",
    ]
    args += sum((["--artifact", path] for path in artifact_paths), [])
    ctx.run_python("Full toolbox GitHub evidence bundle", args)
    ctx.run_python(
        "Validate full toolbox GitHub evidence bundle",
        [
            "-m",
            "Tools.validation",
            "check_github_evidence_bundle",
            "--repo-root",
            ".",
            "--bundle",
            ctx.p("bundle_json"),
            "--output",
            ctx.p("bundle_validation_json"),
        ],
    )
