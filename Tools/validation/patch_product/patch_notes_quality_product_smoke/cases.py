"""Focused smoke cases for patch-notes quality behavior."""

from __future__ import annotations

from typing import Any

def area_diversity_smoke() -> dict[str, Any]:
    from Tools.ai.patch_product.patch_notes_quality_product.scoring import build_patch_notes

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
    import tempfile
    from pathlib import Path

    from Tools.ai.repository_product.repository_consistency_map.python_inventory import extract_local_import_findings

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        package = root / "Tools" / "ai"
        package.mkdir(parents=True)
        (root / "Tools" / "__init__.py").write_text("", encoding="utf-8")
        (package / "__init__.py").write_text("", encoding="utf-8")
        (package / "real_module.py").write_text(
            "def existing_symbol():\n    return True\n", encoding="utf-8"
        )
        tree = ast.parse("from Tools.ai.real_module import missing_symbol\n")
        findings = extract_local_import_findings(tree, "Tools/ai/consumer.py", root)
    kinds = [item.get("kind") for item in findings]
    return {
        "passed": "python_import_symbol_missing" in kinds,
        "kinds": kinds,
        "finding_count": len(findings),
    }


def patchable_availability_smoke() -> dict[str, Any]:
    from Tools.ai.patch_product.patch_notes_quality_product.scoring import build_product_sufficiency

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
        "full_toolbox_telemetry": {
            "workflow_summary": {"passed": True, "recommendation_count": 1, "patch_plan_count": 1}
        },
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
        "full_toolbox_telemetry": {
            "workflow_summary": {"passed": True, "recommendation_count": 1, "patch_plan_count": 1}
        },
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
    import tempfile
    from pathlib import Path

    from Tools.ai.deterministic_recommendations import (
        synthesize_from_repository_consistency_maps,
    )

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
