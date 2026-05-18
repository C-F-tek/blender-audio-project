"""Duplication candidate builders."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from .common import HELPER_RULES, safe_id
from .scanner import files_involved

def build_rule_candidates(functions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for rule in HELPER_RULES:
        matched = [item for item in functions if rule["name_pattern"].match(str(item["name"]))]
        if rule["candidate_id"] == "dup_line_count_helpers":
            matched = [item for item in matched if not item.get("uses_shared_line_count_helper")]
        distinct_files = sorted({str(item["path"]) for item in matched})
        if len(matched) < 2 or len(distinct_files) < 2:
            continue
        candidate_id = str(rule["candidate_id"])
        candidates.append(
            {
                "candidate_id": candidate_id,
                "repeated_logic": rule["repeated_logic"],
                "files_involved": files_involved(matched),
                "function_names": sorted({str(item["name"]) for item in matched}),
                "occurrence_count": len(matched),
                "distinct_file_count": len(distinct_files),
                "existing_helper_available": bool(rule["existing_helper_available"]),
                "preferred_existing_helper_or_module": rule["preferred_existing_helper_or_module"],
                "recommendation_type": rule["recommendation_type"],
                "risk": rule["risk"],
                "schema_or_cli_impact": rule["schema_or_cli_impact"],
                "validation_required": validation_for_candidate(candidate_id),
                "manual_review_required": True,
            }
        )
    return candidates

def build_exact_name_candidates(
    functions: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    by_name: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in functions:
        name = str(item["name"])
        if name.startswith("_"):
            continue
        by_name[name].append(item)
    candidates: list[dict[str, Any]] = []
    helper_rule_ids = {str(rule["candidate_id"]) for rule in HELPER_RULES}
    for name, items in sorted(by_name.items()):
        distinct_files = sorted({str(item["path"]) for item in items})
        if len(items) < 2 or len(distinct_files) < 2:
            continue
        if any(rule["name_pattern"].match(name) for rule in HELPER_RULES):
            continue
        candidate_id = safe_id(f"dup_function_{name}")
        if candidate_id in helper_rule_ids:
            continue
        recommendation = "needs_more_context"
        preferred = (
            "Review whether same-name helper semantics are intentionally local before extracting."
        )
        risk = "medium"
        if name in {"main", "parse_args"}:
            recommendation = "keep_local_by_design"
            preferred = "CLI entrypoints should generally remain local."
            risk = "low"
        candidates.append(
            {
                "candidate_id": candidate_id,
                "repeated_logic": f"Same public function name appears in multiple files: {name}",
                "files_involved": files_involved(items),
                "function_names": [name],
                "occurrence_count": len(items),
                "distinct_file_count": len(distinct_files),
                "existing_helper_available": False,
                "preferred_existing_helper_or_module": preferred,
                "recommendation_type": recommendation,
                "risk": risk,
                "schema_or_cli_impact": "unknown until bodies are compared; manual review required.",
                "validation_required": [
                    "python -m py_compile touched files",
                    "check_python_syntax",
                ],
                "manual_review_required": True,
            }
        )
    return candidates

def validation_for_candidate(candidate_id: str) -> list[str]:
    if "tool_request" in candidate_id:
        return [
            "python -m Tools.validation run_agent_runtime_tool_broker_smoke --repo-root .",
            "python -m Tools.validation run_orchestrator_gpu_runtime_tool_routing_smoke --repo-root .",
            "python -m Tools.validation run_npu_runtime_tool_execution_smoke --repo-root .",
        ]
    if "artifact" in candidate_id or "chunk" in candidate_id:
        return [
            "python -m Tools.validation run_shared_toolbox_ai_to_ai_bundle_smoke --repo-root .",
            "python -m Tools.validation._shared.github_evidence_bundle_cli --repo-root . --bundle <bundle>",
        ]
    return [
        "python -m py_compile touched files",
        "python -m Tools.validation.check_python_syntax --repo-root .",
    ]

def dedupe_candidates(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for item in candidates:
        key = str(item.get("candidate_id") or item.get("repeated_logic") or len(deduped))
        if key not in deduped:
            deduped[key] = item
            continue
        current = deduped[key]
        current_files = list(current.get("files_involved") or [])
        for path in item.get("files_involved") or []:
            if path not in current_files:
                current_files.append(path)
        current["files_involved"] = current_files[:20]
        current["occurrence_count"] = max(
            int(current.get("occurrence_count") or 0),
            int(item.get("occurrence_count") or 0),
        )
    return list(deduped.values())

def build_manual_review_patch_plan_candidates(
    candidates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    plans: list[dict[str, Any]] = []
    for item in candidates:
        if item.get("recommendation_type") not in {
            "reuse_existing_helper",
            "promote_existing_function",
        }:
            continue
        if item.get("risk") not in {"low", "medium"}:
            continue
        plans.append(
            {
                "candidate_id": f"patch_plan_{item.get('candidate_id')}",
                "title": f"Manual-review refactor for {item.get('candidate_id')}",
                "recommendation_type": (
                    "ready_for_patch_plan" if item.get("risk") == "low" else "needs_more_context"
                ),
                "source_candidate_id": item.get("candidate_id"),
                "target_files": sorted(
                    {str(value).split("#L", 1)[0] for value in item.get("files_involved", [])}
                )[:8],
                "preferred_existing_helper_or_module": item.get(
                    "preferred_existing_helper_or_module"
                ),
                "validation": item.get("validation_required", []),
                "manual_review_required": True,
            }
        )
    return plans[:8]
