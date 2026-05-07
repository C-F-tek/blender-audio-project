"""Python production engine for the full-toolbox decision-loop workflow."""
from __future__ import annotations

from pathlib import Path
from typing import Any

from py_mesh import live_signal, run_peer_exchange, run_provider_mesh
from py_product import run_decision_and_bundle
from py_support import WorkflowContext, build_paths, read_json, resolve_python, write_line_inventory


COMPILE_TARGETS = [
    "Tools/ai/gpu_planner_json_contract.py",
    "Tools/ai/replay_gpu_planner_json_contract.py",
    "Tools/ai/analyze_gpu_npu_run_sync.py",
    "Tools/ai/build_deterministic_recommendations.py",
    "Tools/ai/build_agent_review_patch_plan.py",
    "Tools/ai/build_full_toolbox_run_telemetry_summary.py",
    "Tools/ai/build_runtime_tool_usage_telemetry.py",
    "Tools/ai/build_runtime_tool_capability_manifest.py",
    "Tools/ai/build_semantic_evidence_chunks.py",
    "Tools/ai/build_agent_review_evidence_sufficiency.py",
    "Tools/ai/build_openvino_hardware_governance_report.py",
    "Tools/ai/build_ai_peer_exchange_packet.py",
    "Tools/ai/provider_runtime_heap.py",
    "Tools/ai/provider_runtime_heap_live_signals.py",
    "Tools/ai/build_provider_runtime_heap_from_peer_reports.py",
    "Tools/ai/build_provider_runtime_heap_telemetry.py",
    "Tools/ai/run_provider_runtime_heap_gpu_peer_smoke.py",
    "Tools/ai/run_gpu0_peer_companion_worker.py",
    "Tools/ai/run_npu_gpu_deep_review_auditor.py",
    "Tools/ai/run_agent_review_decision_loop.py",
    "Tools/ai/build_repository_consistency_map.py",
    "Tools/validation/check_ai_peer_exchange_contract.py",
    "Tools/validation/run_repository_consistency_map_smoke.py",
    "Tools/validation/run_gpu_planner_json_contract_smoke.py",
    "Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py",
    "Tools/validation/run_agent_review_decision_loop_smoke.py",
    "Tools/validation/check_provider_evidence_contract.py",
]


def init_context(args: Any) -> WorkflowContext:
    repo_root = Path(args.RepoRoot).resolve()
    if not args.Stamp:
        raise ValueError("--Stamp is required for the Python full-toolbox engine")
    paths = build_paths(args.Stamp, args.EvidenceDir)
    return WorkflowContext(args=args, repo_root=repo_root, python_exe=resolve_python(repo_root), paths=paths)


def existing(ctx: WorkflowContext, *keys: str) -> list[str]:
    return [ctx.p(key) for key in keys if Path(ctx.p(key)).exists()]


def run_static_foundation(ctx: WorkflowContext) -> None:
    live_signal(ctx, "init", "Provider runtime heap live init", "heap_init_json", "heap_init_md")
    if not ctx.args.SkipMemoryReload:
        ctx.run_powershell(
            "Full memory/tool regeneration",
            "Tools/workflow/run_full_memory_tool_regeneration.ps1",
            {
                "RepoRoot": ".",
                "Stamp": ctx.p("artifact_stamp"),
                "Profile": "full_refactor",
                "Objective": "Reload IA-Carmine full toolbox context before agent review full toolbox decision-loop run.",
            },
        )
    else:
        ctx.warnings.append("memory/tool regeneration skipped by request")
    ctx.run_python("Full Python line-count inventory", ["Tools/validation/build_python_line_count_csv.py", "--repo-root", ".", "--timestamped", "--report-output", ctx.p("line_count_json"), "--markdown-output", ctx.p("line_count_md")])
    line_report = read_json(ctx.p("line_count_json")) or {}
    if line_report.get("csv_written"):
        ctx.paths["line_count_csv"] = str(line_report["csv_written"])
        write_line_inventory(ctx.paths["line_count_csv"], ctx.p("line_count_all_md"), ctx.args.Stamp)
    else:
        ctx.warnings.append(f"Unable to resolve line-count CSV from {ctx.p('line_count_json')}")
    ctx.run_python("Python syntax validation", ["-m", "Tools.validation.check_python_syntax", "--repo-root", ".", "--output", ctx.p("python_syntax_json")])
    ctx.run_python("Code interpreter/static report", ["-m", "Tools.ai.build_code_interpreter_report", "--repo-root", ".", "--input", "Tools/ai", "--input", "Tools/validation", "--input", "Tools/npu", "--input", "Tools/workflow", "--input", "Scripting/v61b", "--input", "Scripting/shared", "--output", ctx.p("code_interpreter_json"), "--markdown-output", ctx.p("code_interpreter_md")])
    ctx.run_python("Contract script compile", ["-m", "py_compile", *COMPILE_TARGETS])
    ctx.run_python("GPU planner JSON contract smoke", ["Tools/validation/run_gpu_planner_json_contract_smoke.py", "--repo-root", ".", "--output", ctx.p("gpu_contract_smoke_json"), "--markdown-output", ctx.p("gpu_contract_smoke_md")])
    ctx.run_python("Deterministic recommendation synthesizer smoke", ["Tools/validation/run_deterministic_recommendation_synthesizer_smoke.py", "--repo-root", ".", "--output", ctx.p("deterministic_smoke_json"), "--markdown-output", ctx.p("deterministic_smoke_md")])
    ctx.run_python("Agent review decision-loop smoke", ["Tools/validation/run_agent_review_decision_loop_smoke.py", "--repo-root", ".", "--output", ctx.p("decision_loop_smoke_json"), "--markdown-output", ctx.p("decision_loop_smoke_md")])
    ctx.run_python("NPU provider environment preflight", ["Tools/ai/check_npu_provider_environment.py", "--repo-root", ".", "--output", ctx.p("npu_env_json"), "--markdown-output", ctx.p("npu_env_md")])
    ctx.run_python("OpenVINO hardware governance report", ["Tools/ai/build_openvino_hardware_governance_report.py", "--repo-root", ".", "--npu-micro-start-mode", ctx.args.NpuMicroStartMode, "--output", ctx.p("openvino_governance_json"), "--markdown-output", ctx.p("openvino_governance_md")])
    ctx.run_python("Repository consistency map", ["Tools/ai/build_repository_consistency_map.py", "--repo-root", ".", "--output", ctx.p("repo_consistency_json"), "--markdown-output", ctx.p("repo_consistency_md"), "--workers", str(ctx.args.RepositoryConsistencyMapWorkers), "--worker-backend", ctx.args.RepositoryConsistencyMapWorkerBackend, "--worker-cpu-target", str(ctx.args.RepositoryConsistencyMapWorkerCpuTarget), "--max-auto-workers", str(ctx.args.RepositoryConsistencyMapMaxAutoWorkers)])
    ctx.run_python("Repository consistency map smoke", ["Tools/validation/run_repository_consistency_map_smoke.py", "--repo-root", ".", "--map-report", ctx.p("repo_consistency_json"), "--output", ctx.p("repo_consistency_smoke_json"), "--markdown-output", ctx.p("repo_consistency_smoke_md"), "--workers", str(ctx.args.RepositoryConsistencyMapWorkers)])
    ctx.run_python("Agent review evidence sufficiency", ["Tools/ai/build_agent_review_evidence_sufficiency.py", "--repo-root", ".", "--refined-review", ctx.p("refined_review"), *sum((["--report-file", p] for p in existing(ctx, "repo_consistency_json", "repo_consistency_smoke_json", "code_interpreter_json", "line_count_json", "python_syntax_json", "openvino_governance_json")), []), "--output", ctx.p("evidence"), "--markdown-output", ctx.p("evidence_md")])
    ctx.run_python("GPU0 companion worker task lane", ["Tools/ai/build_gpu0_companion_task_lane.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--output", ctx.p("gpu0_companion_json"), "--markdown-output", ctx.p("gpu0_companion_md"), "--tool-requests-output", ctx.p("gpu0_companion_tools_json"), *sum((["--source-report", p] for p in existing(ctx, "evidence", "repo_consistency_json", "repo_consistency_smoke_json", "code_interpreter_json", "line_count_json", "python_syntax_json", "npu_env_json", "openvino_governance_json")), [])])
    ctx.run_python("GPU0 companion worker contract", ["Tools/validation/check_gpu0_companion_contract.py", "--report", ctx.p("gpu0_companion_json"), "--output", ctx.p("gpu0_companion_contract_json"), "--markdown-output", ctx.p("gpu0_companion_contract_md")])


def run_workflow(args: Any) -> int:
    ctx = init_context(args)
    print("=== Agent Review Full Toolbox Decision Loop ===")
    print(f"Repo: {ctx.repo_root}")
    print(f"Stamp: {ctx.args.Stamp}")
    print(f"RunGpuNpuProvider: {ctx.args.RunGpuNpuProvider}")
    print(f"RequireProviderArtifacts: {ctx.args.RequireProviderArtifacts}")
    print(f"RunLegacyNpuAuditorProvider: {ctx.args.RunLegacyNpuAuditorProvider}")
    print(f"Python: {ctx.python_exe}")
    print("Guardrail: report-only decision loop; provider execution only when -RunGpuNpuProvider is explicitly supplied.")
    run_static_foundation(ctx)
    run_provider_mesh(ctx)
    run_peer_exchange(ctx)
    run_decision_and_bundle(ctx)
    workflow = read_json(ctx.p("workflow_json")) or {}
    return 0 if workflow.get("passed") else 2
