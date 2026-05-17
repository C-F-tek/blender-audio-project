from __future__ import annotations

from .common import *  # noqa: F403

def provider_recommendations(
    gpu_report: dict[str, Any], repo_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    recommendations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    raw = gpu_report.get("recommendations")
    if not isinstance(raw, list):
        return recommendations, skipped
    for index, item in enumerate(raw, start=1):
        if not isinstance(item, dict):
            skipped.append(
                {
                    "id": f"provider_{index:03d}",
                    "reason": "recommendation is not an object",
                }
            )
            continue
        if item.get("status") != "ready_for_patch_plan":
            continue
        rec = dict(item)
        rec.setdefault("source", "gpu_provider")
        errors = recommendation_schema_errors(rec, len(recommendations), repo_root)
        if errors:
            skipped.append(
                {
                    "id": str(item.get("id") or f"provider_{index:03d}"),
                    "reason": "; ".join(errors),
                }
            )
            continue
        recommendations.append(rec)
    return recommendations, skipped

def doc_code_recommendation(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    doc = normalize_repo_path(item.get("doc"))
    if not doc:
        return None, {
            "id": f"det_doc_code_{index:03d}",
            "reason": "doc_code item has no doc target",
        }
    error = target_path_error(doc, repo_root)
    if error:
        return None, {"id": f"det_doc_code_{index:03d}", "reason": f"{doc}: {error}"}

    reference = normalize_repo_path(item.get("reference"))
    existing_candidate = normalize_repo_path(item.get("existing_candidate"))
    candidates = unique_strings(item.get("candidate_references"))
    evidence_paths = compact_evidence_files(item)
    strategy_parts = [
        "Create a narrow manual-review patch plan for the documentation/code reference mismatch.",
        f"Inspect `{reference}` and update `{doc}` only if the reference is stale or should point at an existing artifact.",
    ]
    if existing_candidate:
        strategy_parts.append(
            f"Prefer existing candidate `{existing_candidate}` over inventing a new runtime artifact."
        )
    if candidates:
        strategy_parts.append(
            f"Candidate references observed: {', '.join(f'`{candidate}`' for candidate in candidates[:6])}."
        )

    return (
        {
            "id": f"det_doc_code_{index:03d}",
            "area": "doc_code",
            "status": "ready_for_patch_plan",
            "target_files": [doc],
            "rationale": item.get("reason")
            or "Evidence and runtime tool reports are sufficient to build a manual-review patch plan for this doc/code reference.",
            "proposed_strategy": " ".join(strategy_parts),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the referenced file exists after refreshing master.",
                "Stop if the fix requires creating runtime code instead of correcting documentation or references.",
                "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.",
            ],
            "source": "deterministic_evidence_synthesizer",
            "evidence": evidence_paths,
            "tool_evidence": tool_refs,
            "npu_audit_refs": npu_refs,
            "guardrails": {
                "patch_application_performed": False,
                "manual_review_required": True,
            },
        },
        None,
    )

def doc_doc_recommendation(
    *,
    item: dict[str, Any],
    index: int,
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    path = normalize_repo_path(item.get("path"))
    if not path:
        return None, {
            "id": f"det_doc_doc_{index:03d}",
            "reason": "doc_doc item has no path target",
        }
    error = target_path_error(path, repo_root)
    if error:
        return None, {"id": f"det_doc_doc_{index:03d}", "reason": f"{path}: {error}"}
    missing_terms = (
        [str(term) for term in item.get("missing_terms", []) if str(term).strip()]
        if isinstance(item.get("missing_terms"), list)
        else []
    )
    terms_text = (
        ", ".join(f"`{term}`" for term in missing_terms[:10]) or "the missing cross-reference terms"
    )
    return (
        {
            "id": f"det_doc_doc_{index:03d}",
            "area": "doc_doc",
            "status": "ready_for_patch_plan",
            "target_files": [path],
            "rationale": item.get("reason")
            or "Evidence and runtime tool reports are sufficient to build a manual-review documentation cross-reference patch plan.",
            "proposed_strategy": (
                f"Add a compact cross-reference for {terms_text}. "
                "Link or summarize the canonical source instead of duplicating large contract sections."
            ),
            "risk": "low",
            "validation_commands": DEFAULT_VALIDATION_COMMANDS,
            "stop_conditions": [
                "Stop if the missing terms are already present after refreshing master.",
                "Stop if the edit would duplicate large generated artifacts.",
                "Stop if the patch would touch output/**, generated indexes, SQLite, full analysis JSON, provider settings or Blender runtime.",
            ],
            "source": "deterministic_evidence_synthesizer",
            "evidence": compact_evidence_files(item),
            "tool_evidence": tool_refs,
            "npu_audit_refs": npu_refs,
            "guardrails": {
                "patch_application_performed": False,
                "manual_review_required": True,
            },
        },
        None,
    )

def synthesize_from_evidence(
    *,
    evidence: dict[str, Any],
    repo_root: Path,
    npu_refs: list[dict[str, Any]],
    tool_refs: list[dict[str, Any]],
    max_recommendations: int,
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    recommendations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    areas = evidence.get("areas") if isinstance(evidence.get("areas"), dict) else {}

    doc_code = areas.get("doc_code") if isinstance(areas.get("doc_code"), dict) else {}
    for index, item in enumerate(
        doc_code.get("items", []) if isinstance(doc_code.get("items"), list) else [],
        start=1,
    ):
        if len(recommendations) >= max_recommendations:
            break
        if not isinstance(item, dict) or item.get("evidence_sufficient") is not True:
            continue
        rec, skip = doc_code_recommendation(
            item=item,
            index=index,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
        )
        if rec:
            recommendations.append(rec)
        if skip:
            skipped.append(skip)

    doc_doc = areas.get("doc_doc") if isinstance(areas.get("doc_doc"), dict) else {}
    for index, item in enumerate(
        doc_doc.get("items", []) if isinstance(doc_doc.get("items"), list) else [],
        start=1,
    ):
        if len(recommendations) >= max_recommendations:
            break
        if not isinstance(item, dict) or item.get("evidence_sufficient") is not True:
            continue
        rec, skip = doc_doc_recommendation(
            item=item,
            index=index,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
        )
        if rec:
            recommendations.append(rec)
        if skip:
            skipped.append(skip)

    validated: list[dict[str, Any]] = []
    for rec in recommendations:
        errors = recommendation_schema_errors(rec, len(validated), repo_root)
        if errors:
            skipped.append({"id": str(rec.get("id")), "reason": "; ".join(errors)})
            continue
        validated.append(rec)
    return validated, skipped
