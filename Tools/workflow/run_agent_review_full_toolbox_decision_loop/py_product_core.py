from __future__ import annotations

from py_product_common import *  # noqa: F403

def run_decision_loop(ctx: WorkflowContext) -> None:
    args = [
        "-m",
        "ia_carmine",
        "run_agent_review_decision_loop",
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
        "Tools/workflow/_powershell/run_post_validation_ai_packet.ps1",
        {
            "Profile": "core",
            "ContextFile": existing(
                ctx,
                "repo_consistency_md",
                "repo_consistency_smoke_md",
                "line_count_all_md",
                "code_interpreter_md",
                "gpu_replay_md",
                "gpu_npu_sync_md",
                "provider_contract_md",
                "peer_md",
                "peer_contract_md",
                "decision_md",
                "patch_plan_md",
            ),
            "ReportFile": existing(
                ctx,
                "orch_json",
                "gpu_json",
                *TOOL_REPORT_KEYS,
                "recommendations_json",
                "bridge_json",
                "decision_json",
                "patch_plan_json",
            ),
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
            {
                "id": "full_toolbox_bootstrap_python_syntax",
                "tool": "check_python_syntax",
                "reason": "Brokered Python syntax validation.",
                "args": {},
            },
            {
                "id": "full_toolbox_bootstrap_python_line_count",
                "tool": "build_python_line_count_csv",
                "reason": "Brokered Python inventory.",
                "args": {"exclude_dir": ".venv,venv,__pycache__"},
            },
            {
                "id": "full_toolbox_bootstrap_validation_contract",
                "tool": "check_validation_report_contract",
                "reason": "Brokered validation report contract check.",
                "args": {"report_file": f"{ctx.p('decision_json')},{ctx.p('patch_plan_json')}"},
            },
        ],
    }
    write_json(ctx.p("runtime_bootstrap_json"), payload)
    ctx.run_python(
        "Runtime tool broker bootstrap activation",
        [
            "-m",
            "ia_carmine",
            "agent_runtime_tool_broker",
            "--repo-root",
            ".",
            "--request-file",
            ctx.p("runtime_bootstrap_json"),
            "--tool-output-dir",
            ctx.p("runtime_tool_dir"),
            "--stamp",
            ctx.args.Stamp,
            "--timeout-seconds",
            "240",
            "--output",
            ctx.p("runtime_broker_json"),
            "--markdown-output",
            ctx.p("runtime_broker_md"),
        ],
    )

def run_patch_plan_quality_product_gate(ctx: WorkflowContext) -> None:
    # Write non-blocking patch-plan quality and fallback diagnostics.
    extra_context = existing(
        ctx,
        "repo_consistency_md",
        "decision_md",
        "patch_plan_md",
        "runtime_capability_md",
        "memory_bundle_md",
    )
    args = [
        "-m",
        "ia_carmine",
        "build_patch_plan_quality_product_report",
        "--repo-root",
        ".",
        "--patch-plan",
        ctx.p("patch_plan_json"),
        "--decision-loop",
        ctx.p("decision_json"),
        "--recommendations",
        ctx.p("recommendations_json"),
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
