"""Fixture builders for patch-notes quality smoke."""

from __future__ import annotations

from pathlib import Path

from .common import write_fixture

def build_fixtures(repo_root: Path, stamp: str) -> dict[str, str]:
    base = repo_root / "output/validation" / f"patch_notes_quality_product_smoke_{stamp}"
    base.mkdir(parents=True, exist_ok=True)
    task = base / "task.md"
    task.write_text(
        "# Patch notes smoke task\n\nObjective: produce patch notes from a manual-review patch plan with product evidence.\n",
        encoding="utf-8",
    )
    patch_plan = base / "patch_plan.json"
    write_fixture(
        patch_plan,
        {
            "schema_version": 1,
            "kind": "agent_review_patch_plan",
            "passed": True,
            "patch_plans": [
                {
                    "id": "smoke_plan_001",
                    "area": "ai-quality",
                    "status": "ready_for_manual_review",
                    "target_files": ["ia_carmine/product/patch_product/patch_plan_quality_product_report/cli.py"],
                    "rationale": "Verify that generated patch notes can summarize an existing quality product lane.",
                    "edit_strategy": "Add report-only product evidence and keep patch application separate.",
                    "source_evidence": {"smoke": True},
                    "validation_commands": [
                        "python -m Tools.validation patch_notes_quality_product_smoke --repo-root ."
                    ],
                    "stop_conditions": ["manual review rejects evidence"],
                    "manual_review_required": True,
                }
            ],
        },
    )
    paths = {
        "patch_quality": base / "patch_quality.json",
        "decision_loop": base / "decision_loop.json",
        "runtime_capability": base / "runtime_capability.json",
        "repository_consistency": base / "repository_consistency.json",
        "memory_bundle": base / "memory_bundle.json",
        "github_evidence_bundle": base / "bundle.json",
    }
    common = {"schema_version": 1, "passed": True, "errors": []}
    write_fixture(
        paths["patch_quality"],
        {
            **common,
            "kind": "patch_plan_quality_product_gate",
            "quality_gate_passed": True,
            "classification": "ready_for_manual_patch_review",
            "quality": {
                "average_plan_score": 100,
                "plan_scores": [{"id": "smoke_plan_001", "score": 100, "notes": []}],
            },
        },
    )
    write_fixture(
        paths["decision_loop"],
        {**common, "kind": "agent_review_decision_loop", "patch_plan_count": 1},
    )
    npu_final_review = {
        "classification": "gpu1_gpu0_npu_final_review",
        "npu_support_seen": True,
        "npu_self_check_only": False,
        "final_review_on_performant_lane": True,
        "reviewers": ["gpu1", "gpu0", "deterministic_validators"],
        "deterministic_validator_acceptance_required": True,
    }
    write_fixture(
        paths["runtime_capability"],
        {**common, "kind": "runtime_tool_capability_manifest", "tool_count": 2},
    )
    write_fixture(
        paths["repository_consistency"],
        {**common, "kind": "repository_consistency_map", "finding_count": 0},
    )
    write_fixture(
        paths["memory_bundle"], {**common, "kind": "full_memory_tool_regeneration_bundle"}
    )
    write_fixture(
        paths["github_evidence_bundle"],
        {**common, "kind": "github_validation_evidence_bundle", "reports": []},
    )
    out = {"task": task, "patch_plan": patch_plan, **paths}
    return {key: value.relative_to(repo_root).as_posix() for key, value in out.items()}
