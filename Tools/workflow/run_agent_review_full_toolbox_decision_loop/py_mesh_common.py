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

def live_signal(
    ctx: WorkflowContext,
    mode: str,
    label: str,
    json_key: str,
    md_key: str,
    extra: list[str] | None = None,
) -> None:
    ctx.run_python(
        label,
        [
            "-m",
            "Tools.ai",
            "provider_runtime_live_signals",
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
    missing = [
        key for key in ("evidence", "orch_json", "gpu_json") if not Path(ctx.p(key)).exists()
    ]
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
        "guardrails": {
            "report_only": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }
    if "orch_json" in missing:
        write_json(ctx.p("orch_json"), dict(fallback, kind="agent_gpu_npu_parallel_orchestrator"))
        write_text(
            ctx.p("orch_md"), ["# Required provider orchestrator fallback", "", "- Passed: `False`"]
        )
    if "gpu_json" in missing:
        write_json(
            ctx.p("gpu_json"),
            dict(
                fallback,
                kind="agent_gpu_parallel_report",
                provider_empty_response=True,
                recommendation_count=0,
                recommendations=[],
            ),
        )
        write_text(ctx.p("gpu_md"), ["# Required GPU provider fallback", "", "- Passed: `False`"])
    if "evidence" in missing:
        write_json(
            ctx.p("evidence"),
            dict(fallback, kind="agent_review_evidence_sufficiency", evidence_sufficient=False),
        )
