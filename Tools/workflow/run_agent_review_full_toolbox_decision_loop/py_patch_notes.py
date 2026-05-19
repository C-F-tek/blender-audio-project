"""Patch-notes quality product phase for the Python workflow."""

from __future__ import annotations

from pathlib import Path

from py_mesh import existing
from py_support import WorkflowContext, git_output


def run_patch_notes_quality_product(ctx: WorkflowContext) -> None:
    extra_context = existing(
        ctx,
        "repo_consistency_md",
        "decision_md",
        "patch_plan_md",
        "patch_quality_md",
        "telemetry_md",
        "runtime_usage_md",
        "runtime_capability_md",
        "memory_bundle_md",
        "bundle_md",
    )
    args = [
        "-m",
        "Tools.ai",
        "build_patch_notes_quality_product",
        "--repo-root",
        ".",
        "--stamp",
        ctx.args.Stamp,
        "--task-markdown",
        ctx.args.TaskMarkdown,
        "--patch-plan",
        ctx.p("patch_plan_json"),
        "--patch-quality",
        ctx.p("patch_quality_json"),
        "--decision-loop",
        ctx.p("decision_json"),
        "--runtime-usage",
        ctx.p("runtime_usage_json"),
        "--runtime-capability",
        ctx.p("runtime_capability_json"),
        "--repository-consistency",
        ctx.p("repo_consistency_json"),
        "--memory-bundle",
        ctx.p("memory_bundle_json"),
        "--full-toolbox-telemetry",
        ctx.p("telemetry_json"),
        "--sqlite-fts-db",
        ctx.p("patch_notes_quality_fts_db"),
        "--branch",
        git_output(ctx.repo_root, "branch", "--show-current"),
        "--commit",
        git_output(ctx.repo_root, "rev-parse", "--short", "HEAD"),
        "--issue",
        str(getattr(ctx.args, "IssueNumber", "") or ""),
        "--request",
        f"Build manual-review patch notes quality product for {ctx.args.Stamp}.",
        "--max-patch-notes",
        str(max(1, int(getattr(ctx.args, "MaxPatchPlans", 20) or 20))),
        "--min-patch-notes",
        str(max(0, int(getattr(ctx.args, "MinPatchPlans", 0) or 0))),
        "--output",
        ctx.p("patch_notes_quality_json"),
        "--markdown-output",
        ctx.p("patch_notes_quality_md"),
    ]
    if Path(ctx.p("bundle_json")).exists():
        args += ["--github-evidence-bundle", ctx.p("bundle_json")]
    args += sum((["--extra-context", item] for item in extra_context), [])
    ctx.run_python("Patch notes quality product", args)
