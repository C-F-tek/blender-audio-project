#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

from Tools.ai.patch_notes_quality_product.builder import build_report


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_fixture(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patch Notes Quality Product Smoke", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Positive passed: `{report['positive']['passed']}`")
    lines.append(f"- Positive quality gate: `{report['positive']['quality_gate_passed']}`")
    lines.append(f"- Negative passed: `{report['negative']['passed']}`")
    lines.append(f"- Negative quality gate: `{report['negative']['quality_gate_passed']}`")
    if report["errors"]:
        lines += ["", "## Errors", ""]
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


def build_fixtures(repo_root: Path, stamp: str) -> dict[str, str]:
    base = repo_root / "output/validation" / f"patch_notes_quality_product_smoke_{stamp}"
    base.mkdir(parents=True, exist_ok=True)
    task = base / "task.md"
    task.write_text("# Patch notes smoke task\n\nObjective: produce patch notes from a manual-review patch plan with telemetry evidence.\n", encoding="utf-8")
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
                    "target_files": ["Tools/ai/build_patch_plan_quality_product_report.py"],
                    "rationale": "Verify that generated patch notes can summarize an existing quality product lane.",
                    "edit_strategy": "Add report-only product evidence and keep patch application separate.",
                    "source_evidence": {"smoke": True},
                    "validation_commands": ["python Tools/validation/run_patch_notes_quality_product_smoke.py --repo-root ."],
                    "stop_conditions": ["manual review rejects evidence"],
                    "manual_review_required": True,
                }
            ],
        },
    )
    paths = {
        "patch_quality": base / "patch_quality.json",
        "decision_loop": base / "decision_loop.json",
        "runtime_usage": base / "runtime_usage.json",
        "runtime_capability": base / "runtime_capability.json",
        "repository_consistency": base / "repository_consistency.json",
        "memory_bundle": base / "memory_bundle.json",
        "full_toolbox_telemetry": base / "telemetry.json",
        "github_evidence_bundle": base / "bundle.json",
    }
    common = {"schema_version": 1, "passed": True, "errors": []}
    write_fixture(paths["patch_quality"], {**common, "kind": "patch_plan_quality_product_gate", "quality_gate_passed": True, "classification": "ready_for_manual_patch_review", "quality": {"average_plan_score": 100, "plan_scores": [{"id": "smoke_plan_001", "score": 100, "notes": []}]}})
    write_fixture(paths["decision_loop"], {**common, "kind": "agent_review_decision_loop", "patch_plan_count": 1})
    npu_final_review = {"classification": "gpu1_gpu0_npu_final_review", "npu_support_seen": True, "npu_self_check_only": False, "final_review_on_performant_lane": True, "reviewers": ["gpu1", "gpu0", "deterministic_validators"], "deterministic_validator_acceptance_required": True}
    write_fixture(paths["runtime_usage"], {**common, "kind": "runtime_tool_usage_telemetry", "provider_execution_performed": True, "summary": {"tool_call_entry_count": 2, "executed_count": 2}, "provider_evidence": {"provider_execution_performed": True, "gpu_provider_execution_performed": True, "gpu0_peer_support_provider_execution_performed": True, "npu_micro_tool_lane_performed": True, "npu_final_review": npu_final_review}})
    write_fixture(paths["runtime_capability"], {**common, "kind": "runtime_tool_capability_manifest", "tool_count": 2})
    write_fixture(paths["repository_consistency"], {**common, "kind": "repository_consistency_map", "finding_count": 0})
    write_fixture(paths["memory_bundle"], {**common, "kind": "full_memory_tool_regeneration_bundle"})
    write_fixture(paths["full_toolbox_telemetry"], {**common, "kind": "full_toolbox_run_telemetry_summary", "provider_execution_performed": True, "provider_evidence": {"provider_execution_performed": True, "gpu_provider_execution_performed": True, "gpu0_peer_support_provider_execution_performed": True, "npu_micro_tool_lane_performed": True, "npu_final_review": npu_final_review}})
    write_fixture(paths["github_evidence_bundle"], {**common, "kind": "github_validation_evidence_bundle", "reports": []})
    out = {"task": task, "patch_plan": patch_plan, **paths}
    return {key: value.relative_to(repo_root).as_posix() for key, value in out.items()}


def run_case(repo_root: Path, stamp: str, fixtures: dict[str, str], min_score: float) -> dict[str, Any]:
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


def area_diversity_smoke() -> dict[str, Any]:
    from Tools.ai.patch_notes_quality_product.scoring import build_patch_notes

    patch_plan = {
        "patch_plans": [
            {
                "id": f"doc_python_{index}",
                "area": "doc_python",
                "status": "ready_for_patch_plan",
                "target_files": ["docs/doc-python.md"],
                "rationale": "doc python mismatch requiring update",
                "edit_strategy": "update documented command to tracked path or mark as design-only",
                "validation_commands": ["git diff --check"],
                "stop_conditions": ["manual review"],
                "manual_review_required": True,
                "source_evidence": {},
            }
            for index in range(1, 8)
        ]
        + [
            {
                "id": "doc_doc_1",
                "area": "doc_doc",
                "status": "ready_for_patch_plan",
                "target_files": ["docs/doc-doc.md"],
                "rationale": "doc doc mismatch requiring update",
                "edit_strategy": "align stale doc reference with canonical doc",
                "validation_commands": ["git diff --check"],
                "stop_conditions": ["manual review"],
                "manual_review_required": True,
                "source_evidence": {},
            },
            {
                "id": "python_doc_1",
                "area": "python_doc",
                "status": "ready_for_patch_plan",
                "target_files": ["docs/python-doc.md"],
                "rationale": "document tracked python behavior",
                "edit_strategy": "add missing operator documentation for existing python tool",
                "validation_commands": ["git diff --check"],
                "stop_conditions": ["manual review"],
                "manual_review_required": True,
                "source_evidence": {},
            },
        ]
    }
    notes = build_patch_notes(patch_plan, {}, limit=5)
    areas = [note.get("area") for note in notes]
    return {
        "passed": "doc_doc" in areas and "python_doc" in areas and areas.count("doc_python") < 5,
        "areas": areas,
        "note_count": len(notes),
    }


def python_python_symbol_smoke() -> dict[str, Any]:
    import ast
    from pathlib import Path
    import tempfile

    from Tools.ai.repository_consistency_map.python_inventory import extract_local_import_findings

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        package = root / "Tools" / "ai"
        package.mkdir(parents=True)
        (root / "Tools" / "__init__.py").write_text("", encoding="utf-8")
        (package / "__init__.py").write_text("", encoding="utf-8")
        (package / "real_module.py").write_text("def existing_symbol():\n    return True\n", encoding="utf-8")
        tree = ast.parse("from Tools.ai.real_module import missing_symbol\n")
        findings = extract_local_import_findings(tree, "Tools/ai/consumer.py", root)
    kinds = [item.get("kind") for item in findings]
    return {
        "passed": "python_import_symbol_missing" in kinds,
        "kinds": kinds,
        "finding_count": len(findings),
    }



def patchable_availability_smoke() -> dict[str, Any]:
    from Tools.ai.patch_notes_quality_product.scoring import build_product_sufficiency

    task = {
        "title": "ALL_ALL patchable availability smoke",
        "objective_hint": "ALL_ALL doc_python doc_doc python_doc python_python",
    }
    report = {"patch_notes": []}
    loaded_unpatchable_only = {
        "repository_consistency": {
            "finding_kind_counts": {"md_mentions_missing_python_path": 1},
            "findings": [
                {
                    "kind": "md_mentions_missing_python_path",
                    "source": "docs/LOCAL_VALIDATION_EVIDENCE/generated.md",
                    "target": "missing_tool.py",
                }
            ],
        },
        "full_toolbox_telemetry": {"workflow_summary": {"passed": True, "recommendation_count": 1, "patch_plan_count": 1}},
    }
    unpatchable = build_product_sufficiency(
        report,
        loaded_unpatchable_only,
        task,
        patch_note_limit=10,
        requested_min_patch_notes=1,
    )
    loaded_patchable = {
        "repository_consistency": {
            "finding_kind_counts": {"md_mentions_missing_python_path": 2},
            "findings": [
                {
                    "kind": "md_mentions_missing_python_path",
                    "source": "docs/LOCAL_VALIDATION_EVIDENCE/generated.md",
                    "target": "missing_tool.py",
                },
                {
                    "kind": "md_mentions_missing_python_path",
                    "source": "AGENTS.md",
                    "target": "missing_tool.py",
                },
            ],
        },
        "full_toolbox_telemetry": {"workflow_summary": {"passed": True, "recommendation_count": 1, "patch_plan_count": 1}},
    }
    patchable = build_product_sufficiency(
        report,
        loaded_patchable,
        task,
        patch_note_limit=10,
        requested_min_patch_notes=1,
    )
    return {
        "passed": (
            "doc_python" not in unpatchable.get("available_requested_areas", [])
            and patchable.get("repository_area_counts", {}).get("doc_python") == 1
            and patchable.get("raw_repository_area_counts", {}).get("doc_python") == 2
            and patchable.get("unpatchable_repository_area_counts", {}).get("doc_python") == 1
        ),
        "unpatchable_available_requested_areas": unpatchable.get("available_requested_areas"),
        "patchable_repository_area_counts": patchable.get("repository_area_counts"),
        "raw_repository_area_counts": patchable.get("raw_repository_area_counts"),
        "unpatchable_repository_area_counts": patchable.get("unpatchable_repository_area_counts"),
    }


def deterministic_doc_python_patchable_smoke() -> dict[str, Any]:
    from pathlib import Path
    import tempfile

    from Tools.ai.build_deterministic_recommendations import synthesize_from_repository_consistency_maps

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        docs = root / "docs"
        generated = docs / "LOCAL_VALIDATION_EVIDENCE"
        docs.mkdir(parents=True)
        generated.mkdir(parents=True)
        (root / "AGENTS.md").write_text("# agents\n", encoding="utf-8")
        (generated / "generated.md").write_text("# generated\n", encoding="utf-8")
        repository_map = {
            "kind": "repository_consistency_map",
            "findings": [
                {
                    "kind": "md_mentions_missing_python_path",
                    "severity": "high",
                    "source": "docs/LOCAL_VALIDATION_EVIDENCE/generated.md",
                    "target": "missing_generated.py",
                    "line": 1,
                    "recommendation": "Update generated evidence reference.",
                },
                {
                    "kind": "md_mentions_missing_python_path",
                    "severity": "high",
                    "source": "AGENTS.md",
                    "target": "missing_patchable.py",
                    "line": 2,
                    "recommendation": "Update patchable documentation reference.",
                },
            ],
        }
        recommendations, skipped = synthesize_from_repository_consistency_maps(
            repository_maps=[repository_map],
            repo_root=root,
            npu_refs=[],
            tool_refs=[],
            max_recommendations=10,
        )
    areas = [item.get("area") for item in recommendations]
    targets = [item.get("target_files") for item in recommendations]
    return {
        "passed": areas == ["doc_python"] and targets == [["AGENTS.md"]],
        "areas": areas,
        "targets": targets,
        "skipped_count": len(skipped),
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    fixtures = build_fixtures(repo_root, stamp)
    positive = run_case(repo_root, stamp, fixtures, 72.0)
    negative = run_case(repo_root, stamp + "_forced_false", fixtures, 101.0)
    all_all_task_path = repo_root / fixtures["task"]
    all_all_task_path.write_text(
        "# ALL_ALL smoke task\n\n"
        "Objective: ALL_ALL repository progression. Required areas: "
        "doc_doc, doc_python, python_doc, python_python, policy_violation, "
        "refactor_candidate, telemetry_gap, evidence_gap.\n",
        encoding="utf-8",
    )
    all_all_insufficient = run_case(repo_root, stamp + "_all_all_insufficient", fixtures, 72.0)
    errors: list[str] = []
    if not positive.get("passed") or not positive.get("quality_gate_passed") or not positive.get("patch_notes"):
        errors.append("positive case did not produce passing patch notes")
    if not positive.get("success_cases"):
        errors.append("positive case did not produce structured success cases")
    if not negative.get("passed") or negative.get("quality_gate_passed") or not negative.get("fallback_path_notes"):
        errors.append("negative non-blocking fallback case did not behave as expected")
    if not negative.get("fallback_cases"):
        errors.append("negative non-blocking fallback case did not produce structured fallback cases")
    if all_all_insufficient.get("quality_gate_passed"):
        errors.append("ALL_ALL insufficient case incorrectly passed quality gate")
    if all_all_insufficient.get("classification") != "completed_with_insufficient_all_all_patch_notes":
        errors.append("ALL_ALL insufficient case did not receive insufficient classification")
    area_diversity = area_diversity_smoke()
    if not area_diversity.get("passed"):
        errors.append("area diversity smoke failed to include doc_doc/python_doc alongside doc_python")
    python_python_symbol = python_python_symbol_smoke()
    if not python_python_symbol.get("passed"):
        errors.append("python_python symbol import smoke failed")
    patchable_availability = patchable_availability_smoke()
    if not patchable_availability.get("passed"):
        errors.append("patchable availability smoke failed")
    deterministic_doc_python_patchable = deterministic_doc_python_patchable_smoke()
    if not deterministic_doc_python_patchable.get("passed"):
        errors.append("deterministic doc_python patchable smoke failed")
    report = {
        "schema_version": 1,
        "kind": "patch_notes_quality_product_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "positive": {"passed": positive.get("passed"), "quality_gate_passed": positive.get("quality_gate_passed"), "classification": positive.get("classification"), "patch_note_count": len(positive.get("patch_notes", [])), "success_case_count": len(positive.get("success_cases", []))},
        "negative": {"passed": negative.get("passed"), "quality_gate_passed": negative.get("quality_gate_passed"), "classification": negative.get("classification"), "fallback_path_note_count": len(negative.get("fallback_path_notes", [])), "fallback_case_count": len(negative.get("fallback_cases", []))},
        "all_all_insufficient": {"passed": all_all_insufficient.get("passed"), "quality_gate_passed": all_all_insufficient.get("quality_gate_passed"), "classification": all_all_insufficient.get("classification"), "product_sufficiency": all_all_insufficient.get("product_sufficiency")},
        "area_diversity": area_diversity,
        "python_python_symbol": python_python_symbol,
        "patchable_availability": patchable_availability,
        "deterministic_doc_python_patchable": deterministic_doc_python_patchable,
        "guardrails": {"report_only": True, "patch_application_performed": False, "source_writes_performed": False},
    }
    output = resolve_output_path(repo_root, args.output or f"output/validation/patch_notes_quality_product_smoke_{stamp}.json")
    markdown = resolve_output_path(repo_root, args.markdown_output or f"output/validation/patch_notes_quality_product_smoke_{stamp}.md")
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
