"""Patch-notes quality report runner helper."""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace
from typing import Any

from Tools.ai.patch_notes_quality_product.builder import build_report

def run_case(
    repo_root: Path, stamp: str, fixtures: dict[str, str], min_score: float
) -> dict[str, Any]:
    args = SimpleNamespace(
        repo_root=str(repo_root),
        stamp=stamp,
        task_markdown=fixtures["task"],
        patch_plan=fixtures["patch_plan"],
        patch_quality=fixtures["patch_quality"],
        decision_loop=fixtures["decision_loop"],
        runtime_usage=fixtures["runtime_usage"],
        runtime_capability=fixtures["runtime_capability"],
        repository_consistency=fixtures["repository_consistency"],
        memory_bundle=fixtures["memory_bundle"],
        full_toolbox_telemetry=fixtures["full_toolbox_telemetry"],
        github_evidence_bundle=fixtures["github_evidence_bundle"],
        branch="smoke",
        commit="",
        issue="",
        request="patch notes quality smoke",
        extra_context=[],
        sqlite_fts_db=f"output/validation/patch_notes_quality_product_smoke_{stamp}/product.sqlite",
        min_quality_score=min_score,
        strict_patch_notes_quality_gate=False,
    )
    return build_report(args)
