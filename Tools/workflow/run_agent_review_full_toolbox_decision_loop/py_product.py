"""Decision, product, bundle and telemetry phases for the Python workflow."""
from __future__ import annotations

from pathlib import Path

from py_mesh import add_artifacts, add_reports, existing, live_signal
from py_patch_notes import run_patch_notes_quality_product
from py_support import WorkflowContext, add_existing, now_iso, read_json, write_json, write_text


TOOL_REPORT_KEYS = [
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
    "megalithic_review_json",
    "megalithic_proposals_json",
    "refined_review",
    "refined_proposals",
    "gpu_replay_json",
    "gpu_npu_sync_json",
    "provider_contract_json",
    "gpu0_companion_json",
    "gpu0_companion_contract_json",
    "gpu0_support_bootstrap",
    "npu_support_bootstrap",
    "gpu1_primary_json",
    "gpu0_task_json",
    "gpu0_response_json",
    "gpu0_tools_json",
    "gpu0_broker_json",
    "npu_micro_json",
    "npu_broker_json",
    "peer_json",
    "peer_contract_json",
    "heap_init_json",
    "heap_gpu1_request_json",
    "heap_broker_json",
    "heap_npu_json",
    "heap_catalog_json",
    "heap_snapshot_json",
    "heap_telemetry_json",
    "memory_workflow",
]


def run_decision_loop(ctx: WorkflowContext) -> None:
    args = [
        "Tools/ai/run_agent_review_decision_loop.py",
        "--repo-root",
        ".",
        "--evidence",
        ctx.p("evidence"),
        "--orchestrator",
        ctx.p("orch_json"),
        "--gpu-report",
        ctx.p("gpu_json"),
        "--recommendations-output",
        ctx.p("recommendations_json"),
        "--recommendations-markdown",
        ctx.p("recommendations_md"),
        "--bridge-orchestrator-output",
        ctx.p("bridge_json"),
        "--patch-plan-output",
        ctx.p("patch_plan_json"),
        "--patch-plan-markdown",
        ctx.p("patch_plan_md"),
        "--output",
        ctx.p("decision_json"),
        "--markdown-output",
        ctx.p("decision_md"),
        "--min-recommendations",
        str(ctx.args.MinRecommendations),
        "--min-patch-plans",
        str(ctx.args.MinPatchPlans),
        "--max-recommendations",
        str(ctx.args.MaxRecommendations),
        "--max-patch-plans",
        str(ctx.args.MaxPatchPlans),
    ]
    args += sum((["--tool-report", path] for path in existing(ctx, *TOOL_REPORT_KEYS)), [])
    ctx.run_python("Agent review decision loop", args)


def run_post_validation_packet(ctx: WorkflowContext) -> None:
    if ctx.args.SkipPostValidationPacket:
        ctx.warnings.append("post-validation AI packet skipped by request")
        return
    ctx.run_powershell(
        "Post-validation AI packet",
        "Tools/workflow/run_post_validation_ai_packet.ps1",
        {
            "Profile": "core",
            "ContextFile": existing(ctx, "repo_consistency_md", "repo_consistency_smoke_md", "line_count_all_md", "code_interpreter_md", "gpu_replay_md", "gpu_npu_sync_md", "provider_contract_md", "peer_md", "peer_contract_md", "decision_md", "patch_plan_md"),
            "ReportFile": existing(ctx, "orch_json", "gpu_json", *TOOL_REPORT_KEYS, "recommendations_json", "bridge_json", "decision_json", "patch_plan_json"),
        },
    )


def run_runtime_bootstrap(ctx: WorkflowContext) -> None:
    payload = {
        "schema_version": 1,
        "kind": "runtime_tool_bootstrap_requests",
        "generated_at": now_iso(),
        "stamp": ctx.args.Stamp,
        "purpose": "Exercise minimal report-only runtime tool broker activation during full-toolbox runs.",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "tool_requests": [
            {"id": "full_toolbox_bootstrap_python_syntax", "tool": "check_python_syntax", "reason": "Brokered Python syntax validation.", "args": {}},
            {"id": "full_toolbox_bootstrap_python_line_count", "tool": "build_python_line_count_csv", "reason": "Brokered Python inventory.", "args": {"exclude_dir": ".venv,venv,__pycache__"}},
            {"id": "full_toolbox_bootstrap_validation_contract", "tool": "check_validation_report_contract", "reason": "Brokered validation report contract check.", "args": {"report_file": f"{ctx.p('decision_json')},{ctx.p('patch_plan_json')}"}},
        ],
    }
    write_json(ctx.p("runtime_bootstrap_json"), payload)
    ctx.run_python("Runtime tool broker bootstrap activation", ["Tools/ai/agent_runtime_tool_broker.py", "--repo-root", ".", "--request-file", ctx.p("runtime_bootstrap_json"), "--tool-output-dir", ctx.p("runtime_tool_dir"), "--stamp", ctx.args.Stamp, "--timeout-seconds", "240", "--output", ctx.p("runtime_broker_json"), "--markdown-output", ctx.p("runtime_broker_md")])


def run_patch_plan_quality_product_gate(ctx: WorkflowContext) -> None:
    # Write non-blocking patch-plan quality and fallback diagnostics.
    extra_context = existing(
        ctx,
        "repo_consistency_md",
        "decision_md",
        "patch_plan_md",
        "telemetry_md",
        "runtime_usage_md",
        "runtime_capability_md",
        "memory_bundle_md",
    )
    args = [
        "Tools/ai/build_patch_plan_quality_product_report.py",
        "--repo-root",
        ".",
        "--patch-plan",
        ctx.p("patch_plan_json"),
        "--decision-loop",
        ctx.p("decision_json"),
        "--recommendations",
        ctx.p("recommendations_json"),
        "--runtime-usage",
        ctx.p("runtime_usage_json"),
        "--runtime-capability",
        ctx.p("runtime_capability_json"),
        "--repository-consistency",
        ctx.p("repo_consistency_json"),
        "--memory-bundle",
        ctx.p("memory_bundle_json"),
        "--sqlite-fts-db",
        ctx.p("patch_quality_fts_db"),
        "--request",
        f"Validate patch notes/patch plan quality for stamp {ctx.args.Stamp}; keep run non-blocking and explain fallback path notes.",
        "--output",
        ctx.p("patch_quality_json"),
        "--markdown-output",
        ctx.p("patch_quality_md"),
    ]
    args += sum((["--extra-context", item] for item in extra_context), [])
    ctx.run_python("Patch plan quality product gate", args)

def run_runtime_telemetry(ctx: WorkflowContext, label: str) -> None:
    ctx.run_python(
        label,
        [
            "Tools/ai/build_runtime_tool_usage_telemetry.py",
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
    ctx.run_python("Runtime tool capability manifest", ["Tools/ai/build_runtime_tool_capability_manifest.py", "--repo-root", ".", "--tool-usage", ctx.p("runtime_usage_json"), "--output", ctx.p("runtime_capability_json"), "--markdown-output", ctx.p("runtime_capability_md")])
    live_signal(ctx, "tool-catalog-complete", "Provider runtime heap tool catalog exchange complete", "heap_catalog_json", "heap_catalog_md", ["--runtime-usage", ctx.p("runtime_usage_json"), "--runtime-capability", ctx.p("runtime_capability_json"), "--round", "1"])
    ctx.run_python("Provider runtime heap telemetry refresh", ["Tools/ai/build_provider_runtime_heap_telemetry.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--output", ctx.p("heap_telemetry_json"), "--markdown-output", ctx.p("heap_telemetry_md")])


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
        "Tools/ai/build_runtime_flow_map.py",
        "--repo-root",
        ".",
        "--stamp",
        ctx.args.Stamp,
        "--entrypoint",
        "Tools/workflow/run_agent_review_full_toolbox_decision_loop.py",
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
    report_keys = ["orch_json", "gpu_json", "gpu_npu_sync_json", "provider_contract_json", "peer_json", "peer_contract_json", "heap_from_peer_json", "heap_telemetry_json", "heap_catalog_json", "heap_snapshot_json", "runtime_usage_json", "runtime_capability_json", "runtime_broker_json", "gpu0_broker_json", "npu_broker_json", "recommendations_json", "decision_json", "patch_plan_json", "patch_quality_json", "patch_notes_quality_json"]
    artifact_keys = ["orch_md", "gpu_md", "gpu_npu_sync_md", "peer_md", "peer_contract_md", "heap_telemetry_md", "heap_catalog_md", "heap_snapshot_md", "runtime_usage_md", "runtime_capability_md", "patch_plan_md", "patch_quality_md", "patch_notes_quality_md"]
    args = ["Tools/ai/build_heap_runtime_product_package.py", "--repo-root", ".", "--output-dir", ctx.p("final_product_dir"), "--request", f"Build the final local AI product for stamp {ctx.args.Stamp} from the live provider mesh, runtime broker evidence, telemetry, patch specs and validation bundle.", "--no-external-probes", "--timeout-seconds", "8", "--output", ctx.p("final_product_json")]
    args += sum((["--run-report", path] for path in existing(ctx, *report_keys)), [])
    args += sum((["--run-artifact", path] for path in existing(ctx, *artifact_keys)), [])
    ctx.run_python("Heap runtime final product", args)


def build_evidence_bundle(ctx: WorkflowContext) -> None:
    if not ctx.args.SkipSharedToolboxBundle:
        ctx.run_python("Shared toolbox AI-to-AI bundle", ["-m", "Tools.ai.build_shared_toolbox_ai_to_ai_bundle", "--repo-root", ".", "--stamp", ctx.p("artifact_stamp"), "--output-dir", ctx.args.EvidenceDir, "--validate-bundle", "--recursive-max-files", "160", "--chunk-large-files-lines", "200"])
    else:
        ctx.warnings.append("shared toolbox bundle skipped by request")
    report_paths = existing(ctx, "orch_json", "gpu_json", *TOOL_REPORT_KEYS, "heap_from_peer_json", "patch_quality_json", "patch_notes_quality_json", "runtime_flow_json", "final_product_json", "final_product_manifest", "final_product_evidence", "final_product_readiness", "recommendations_json", "bridge_json", "decision_json", "patch_plan_json")
    artifact_paths = existing(ctx, "repo_consistency_md", "repo_consistency_smoke_md", "line_count_all_md", "openvino_governance_md", "megalithic_review_md", "refined_review_md", "decision_md", "gpu1_primary_md", "gpu0_response_md", "npu_micro_md", "npu_broker_md", "peer_md", "peer_contract_md", "heap_from_peer_md", "heap_telemetry_md", "heap_init_md", "heap_gpu1_request_md", "heap_broker_md", "heap_npu_md", "heap_catalog_md", "heap_snapshot_md", "runtime_flow_jsonl", "runtime_flow_md", "runtime_flow_mmd", "final_product_md", "final_product_readme", "patch_plan_md", "patch_quality_md", "patch_notes_quality_md")
    line_csv = ctx.paths.get("line_count_csv")
    if line_csv and Path(line_csv).exists():
        artifact_paths.append(line_csv)
    args = ["-m", "Tools.ai.build_github_evidence_bundle", "--repo-root", ".", "--basename", ctx.p("bundle_base"), "--output-dir", ctx.args.EvidenceDir, "--report", ",".join(report_paths), "--max-included-artifact-chars", "16000", "--max-included-artifacts", "42"]
    args += sum((["--artifact", path] for path in artifact_paths), [])
    ctx.run_python("Full toolbox GitHub evidence bundle", args)
    ctx.run_python("Validate full toolbox GitHub evidence bundle", ["-m", "Tools.validation.check_github_evidence_bundle", "--repo-root", ".", "--bundle", ctx.p("bundle_json"), "--output", ctx.p("bundle_validation_json")])


def run_run_telemetry(ctx: WorkflowContext) -> None:
    args = ["Tools/ai/build_full_toolbox_run_telemetry_summary.py", "--repo-root", ".", "--stamp", ctx.args.Stamp, "--decision-loop", ctx.p("decision_json"), "--recommendations", ctx.p("recommendations_json"), "--patch-plan", ctx.p("patch_plan_json"), "--repository-consistency", ctx.p("repo_consistency_json"), "--repository-consistency-smoke", ctx.p("repo_consistency_smoke_json"), "--gpu-npu-sync", ctx.p("gpu_npu_sync_json"), "--orchestrator", ctx.p("orch_json"), "--gpu-report", ctx.p("gpu_json"), "--peer-exchange", ctx.p("peer_json"), "--peer-contract", ctx.p("peer_contract_json"), "--provider-runtime-heap-telemetry", ctx.p("heap_telemetry_json"), "--provider-runtime-heap-snapshot", ctx.p("heap_snapshot_json"), "--line-count-csv", ctx.paths.get("line_count_csv", ""), "--budget-minutes", str(ctx.args.BudgetMinutes), "--max-rounds", str(ctx.args.MaxRounds), "--files-per-round", str(ctx.args.FilesPerRound), "--max-context-files", str(ctx.args.MaxContextFiles), "--max-chars-per-file", str(ctx.args.MaxCharsPerFile), "--max-new-tokens", str(ctx.args.MaxNewTokens), "--npu-auditor-every-rounds", str(ctx.args.NpuAuditorEveryRounds), "--repository-consistency-map-workers", str(ctx.args.RepositoryConsistencyMapWorkers), "--output", ctx.p("telemetry_json"), "--markdown-output", ctx.p("telemetry_md")]
    for key in ("heap_init_json", "heap_gpu1_request_json", "heap_broker_json", "heap_npu_json", "heap_catalog_json"):
        if Path(ctx.p(key)).exists():
            args += ["--provider-runtime-heap-live-signal", ctx.p(key)]
    for path in evidence_to_commit(ctx):
        args += ["--evidence-to-commit", path]
    if (read_json(ctx.p("bundle_validation_json")) or {}).get("passed"):
        args.append("--bundle-validation-passed")
    ctx.run_python("Full toolbox run telemetry summary", args)


def run_semantic_chunks(ctx: WorkflowContext) -> None:
    sources = existing(ctx, "bundle_json", "bundle_md", "telemetry_json", "telemetry_md", "runtime_usage_json", "runtime_usage_md", "runtime_capability_json", "runtime_capability_md", "runtime_flow_json", "runtime_flow_md", "runtime_flow_mmd", "heap_telemetry_json", "heap_telemetry_md", "heap_catalog_json", "heap_catalog_md", "heap_snapshot_json", "heap_snapshot_md", "final_product_json", "final_product_md", "peer_json", "peer_md", "npu_micro_json", "npu_micro_md", "npu_broker_json", "npu_broker_md", "peer_contract_json", "peer_contract_md")
    if not sources:
        ctx.warnings.append("semantic evidence chunking skipped; no source reports found")
        return
    args = ["Tools/ai/build_semantic_evidence_chunks.py", "--repo-root", ".", "--basename", ctx.p("chunk_base"), "--output-dir", ctx.args.EvidenceDir, "--chunk-output-dir", ctx.p("chunk_dir"), "--chunk-max-chars", "12000", "--chunk-overlap-lines", "12", "--zip-output", ctx.p("chunk_zip"), "--no-ollama"]
    args += sum((["--source", path] for path in sources), [])
    ctx.run_python("Semantic evidence chunking for cloud handoff", args)


def run_artifact_path_policy(ctx: WorkflowContext) -> None:
    paths = list(dict.fromkeys([*evidence_to_commit(ctx), *ctx.reports, *ctx.artifacts]))
    args = [
        "Tools/validation/check_generated_artifact_path_policy.py",
        "--repo-root",
        ".",
        "--max-repo-relative-path-chars",
        "210",
        "--max-filename-chars",
        "150",
        "--allowed-prefix",
        "docs/LOCAL_VALIDATION_EVIDENCE/",
        "--output",
        ctx.p("artifact_path_policy_json"),
        "--markdown-output",
        ctx.p("artifact_path_policy_md"),
    ]
    args += sum((["--path", path] for path in paths if path), [])
    ctx.run_python("Generated artifact path-length policy", args)


def evidence_to_commit(ctx: WorkflowContext) -> list[str]:
    keys = ["memory_bundle_json", "memory_bundle_md", "memory_line_count_csv", "bundle_json", "bundle_md", "telemetry_json", "telemetry_md", "runtime_usage_json", "runtime_usage_md", "runtime_capability_json", "runtime_capability_md", "runtime_flow_json", "runtime_flow_jsonl", "runtime_flow_md", "runtime_flow_mmd", "patch_quality_json", "patch_quality_md", "patch_notes_quality_json", "patch_notes_quality_md", "heap_telemetry_json", "heap_telemetry_md", "artifact_path_policy_json", "artifact_path_policy_md", "chunk_manifest_json", "chunk_manifest_md"]
    paths = [ctx.p(key) for key in keys if Path(ctx.p(key)).exists()]
    line_csv = ctx.paths.get("line_count_csv")
    if line_csv and Path(line_csv).exists():
        paths.append(line_csv)
    return paths


def write_workflow(ctx: WorkflowContext) -> None:
    report_keys = ["memory_workflow", "evidence", "provider_contract_json", *TOOL_REPORT_KEYS, "orch_json", "gpu_json", "gpu_replay_json", "gpu_npu_sync_json", "recommendations_json", "bridge_json", "decision_json", "patch_plan_json", "patch_quality_json", "patch_notes_quality_json", "runtime_flow_json", "heap_from_peer_json", "heap_telemetry_json", "final_product_json", "final_product_manifest", "final_product_evidence", "final_product_readiness", "artifact_path_policy_json", "bundle_validation_json", "final_python_syntax_json", "final_contract_json"]
    artifact_keys = ["memory_bundle_json", "memory_bundle_md", "memory_line_count_csv", "evidence_md", "provider_contract_md", "repo_consistency_md", "repo_consistency_smoke_md", "line_count_all_md", "code_interpreter_md", "gpu_contract_smoke_md", "deterministic_smoke_md", "decision_loop_smoke_md", "npu_env_md", "openvino_governance_md", "megalithic_review_md", "refined_review_md", "orch_md", "gpu_md", "gpu_replay_md", "gpu_npu_sync_md", "recommendations_md", "decision_md", "patch_plan_md", "patch_quality_md", "patch_notes_quality_md", "telemetry_json", "telemetry_md", "runtime_usage_json", "runtime_usage_md", "runtime_capability_json", "runtime_capability_md", "runtime_flow_jsonl", "runtime_flow_md", "runtime_flow_mmd", "gpu1_primary_md", "gpu0_response_md", "gpu0_broker_md", "npu_micro_md", "npu_broker_md", "peer_md", "peer_contract_md", "heap_from_peer_md", "heap_telemetry_md", "heap_catalog_md", "heap_snapshot_md", "heap_events", "final_product_md", "final_product_readme", "artifact_path_policy_md", "chunk_manifest_json", "chunk_manifest_md", "bundle_json", "bundle_md"]
    for key in report_keys:
        add_existing(ctx.reports, ctx.p(key))
    for key in artifact_keys:
        add_existing(ctx.artifacts, ctx.p(key))
    bad_reports: list[str] = []
    for path in ctx.reports:
        data = read_json(path)
        if data and data.get("passed") is False:
            bad_reports.append(path)
    decision = read_json(ctx.p("decision_json")) or {}
    bundle_validation = read_json(ctx.p("bundle_validation_json")) or {}
    passed = not ctx.errors and not bad_reports
    report = {
        "schema_version": 1,
        "kind": "agent_review_full_toolbox_decision_loop_workflow",
        "generated_at": now_iso(),
        "repo_root": str(ctx.repo_root),
        "stamp": ctx.args.Stamp,
        "passed": passed,
        "errors": [*ctx.errors, *[f"{path}: passed=false" for path in bad_reports]],
        "warnings": ctx.warnings,
        "provider_execution_performed": bool(ctx.args.RunGpuNpuProvider),
        "legacy_npu_auditor_provider_requested": bool(ctx.args.RunLegacyNpuAuditorProvider),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "recommendation_count": decision.get("recommendation_count"),
        "patch_plan_count": decision.get("patch_plan_count"),
        "bundle_validation_passed": bundle_validation.get("passed"),
        "final_local_ai_product_built": Path(ctx.p("final_product_json")).exists(),
        "final_local_ai_product": ctx.p("final_product_json"),
        "reports": ctx.reports,
        "artifacts": ctx.artifacts,
        "evidence_to_commit": evidence_to_commit(ctx),
        "guardrails": {"provider_execution_requires_explicit_flag": True, "patch_application_performed": False, "source_writes_performed": False, "raw_output_commit_allowed": False, "final_tool_product_external_probes_disabled": True},
    }
    write_json(ctx.p("workflow_json"), report)
    lines = ["# Agent Review Full Toolbox Decision Loop Workflow", "", f"- Passed: `{passed}`", f"- Stamp: `{ctx.args.Stamp}`", f"- Provider execution performed: `{bool(ctx.args.RunGpuNpuProvider)}`", "- Patch application performed: `False`", f"- Recommendation count: `{report.get('recommendation_count')}`", f"- Patch plan count: `{report.get('patch_plan_count')}`", f"- Final local AI product built: `{report.get('final_local_ai_product_built')}`", "", "## Evidence to commit", ""]
    lines += [f"- `{path}`" for path in report["evidence_to_commit"]]
    write_text(ctx.p("workflow_md"), lines)
    print("\n=== Full toolbox decision loop summary ===")
    print(f"Workflow: {ctx.p('workflow_json')}")
    print(f"Markdown: {ctx.p('workflow_md')}")
    print(f"Evidence bundle: {ctx.p('bundle_json')}")
    print(f"Passed: {passed}")

def run_decision_and_bundle(ctx: WorkflowContext) -> None:
    run_decision_loop(ctx)
    run_post_validation_packet(ctx)
    run_runtime_bootstrap(ctx)
    run_runtime_telemetry(ctx, "Runtime tool usage telemetry pre-bundle")
    run_patch_plan_quality_product_gate(ctx)
    run_patch_notes_quality_product(ctx)
    run_final_product(ctx)
    run_runtime_flow_map(ctx)
    build_evidence_bundle(ctx)
    ctx.run_python("Final Python syntax validation", ["-m", "Tools.validation.check_python_syntax", "--repo-root", ".", "--output", ctx.p("final_python_syntax_json")])
    ctx.run_python("Final scoped validation report contract", ["Tools/validation/check_validation_report_contract.py", "--repo-root", ".", "--report-file", ctx.p("decision_loop_smoke_json"), "--report-file", ctx.p("repo_consistency_smoke_json"), "--report-file", ctx.p("patch_notes_quality_json"), "--report-file", ctx.p("final_python_syntax_json"), "--report-file", ctx.p("bundle_validation_json"), "--output", ctx.p("final_contract_json")])
    run_run_telemetry(ctx)
    run_runtime_telemetry(ctx, "Runtime tool usage telemetry")
    run_patch_notes_quality_product(ctx)
    run_semantic_chunks(ctx)
    run_artifact_path_policy(ctx)
    write_workflow(ctx)
