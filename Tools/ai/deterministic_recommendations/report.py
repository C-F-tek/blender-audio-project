from __future__ import annotations

from .common import *  # noqa: F403
from .consistency import area_diverse_items, synthesize_from_repository_consistency_maps
from .provider import provider_recommendations, synthesize_from_evidence

def load_gpu_report(
    repo_root: Path, orchestrator: dict[str, Any], explicit_gpu_report: str
) -> tuple[dict[str, Any], list[str]]:
    warnings: list[str] = []
    if explicit_gpu_report:
        data, errors = load_report_at(repo_root, explicit_gpu_report, missing_is_error=True)
        return data, errors

    gpu_output = normalize_repo_path(orchestrator.get("gpu_output"))
    if gpu_output:
        data, errors = load_report_at(repo_root, gpu_output, missing_is_error=True)
        warnings.extend(errors)
        return data, warnings

    default_path = resolve_path(
        repo_root, "output/ai_pipeline/agent_gpu_deep_planning_supervised.json"
    )
    if default_path.exists():
        data, errors = load_report_at(repo_root, default_path, missing_is_error=False)
        warnings.extend(errors)
        return data, warnings
    return {}, warnings

def build_recommendation_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    evidence, evidence_errors = load_report_at(repo_root, args.evidence, missing_is_error=True)
    errors.extend(evidence_errors)

    orchestrator: dict[str, Any] = {}
    if args.orchestrator:
        orchestrator_path = resolve_path(repo_root, args.orchestrator)
        if orchestrator_path.exists():
            orchestrator, orchestrator_errors = load_report_at(
                repo_root, args.orchestrator, missing_is_error=False
            )
            warnings.extend(orchestrator_errors)
        else:
            warnings.append(
                f"orchestrator report missing: {repo_rel(orchestrator_path, repo_root)}"
            )

    gpu_report, gpu_warnings = load_gpu_report(repo_root, orchestrator, args.gpu_report)
    warnings.extend(gpu_warnings)

    tool_refs: list[dict[str, Any]] = []
    repository_consistency_maps: list[dict[str, Any]] = []
    for value in args.tool_report:
        path = resolve_path(repo_root, value)
        data, tool_errors = load_report_at(repo_root, value, missing_is_error=False)
        warnings.extend(tool_errors)
        if data:
            tool_refs.append(summarize_tool_report(path, repo_root, data))
            if data.get("kind") == "repository_consistency_map":
                repository_consistency_maps.append(data)

    npu_refs = npu_audit_refs(orchestrator)
    provider_recs, provider_skipped = provider_recommendations(gpu_report, repo_root)
    recommendations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = list(provider_skipped)
    seen: set[str] = set()

    for rec in provider_recs:
        key = recommendation_key(rec)
        if key not in seen:
            seen.add(key)
            recommendations.append(rec)

    deterministic_used = False
    consistency_recommendation_count = 0
    if repository_consistency_maps:
        consistency_synthesized, consistency_skipped = synthesize_from_repository_consistency_maps(
            repository_maps=repository_consistency_maps,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
            max_recommendations=args.max_recommendations,
        )
        skipped.extend(consistency_skipped)
        consistency_recommendation_count = len(consistency_synthesized)
        if consistency_synthesized:
            deterministic_used = True
            combined: list[dict[str, Any]] = []
            combined_seen: set[str] = set()
            for rec in [*recommendations, *consistency_synthesized]:
                key = recommendation_key(rec)
                if key in combined_seen:
                    continue
                combined_seen.add(key)
                combined.append(rec)
            recommendations = area_diverse_items(combined, limit=args.max_recommendations)
            seen = {recommendation_key(rec) for rec in recommendations}

    if not recommendations and evidence:
        deterministic_used = True
        synthesized, synthesized_skipped = synthesize_from_evidence(
            evidence=evidence,
            repo_root=repo_root,
            npu_refs=npu_refs,
            tool_refs=tool_refs,
            max_recommendations=args.max_recommendations,
        )
        skipped.extend(synthesized_skipped)
        for rec in synthesized:
            key = recommendation_key(rec)
            if key not in seen:
                seen.add(key)
                recommendations.append(rec)

    if not recommendations and not errors:
        errors.append("no schema-valid recommendations were produced")

    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    empty_reason = (
        gpu_report.get("empty_recommendations_reason")
        or orchestrator.get("gpu_empty_recommendations_reason")
        or ""
    )
    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        "missing_evidence": (
            [] if recommendations else ["no evidence-sufficient items with safe existing targets"]
        ),
        "next_best_action": (
            "python -m Tools.ai agent_review_patch_plan" if recommendations else "collect_more_evidence"
        ),
        "skipped_candidate_count": len(skipped),
        "skipped_candidates": skipped,
        "decision": {
            "deterministic_synthesizer_used": deterministic_used,
            "provider_recommendation_count": len(provider_recs),
            "schema_valid_recommendation_count": len(recommendations),
            "evidence_ready_for_manual_patch_count": evidence_ready_count,
            "gpu_empty_recommendations_reason": empty_reason,
            "ready_for_patch_plan": bool(recommendations),
            "repository_consistency_map_count": len(repository_consistency_maps),
            "substantive_consistency_recommendation_count": consistency_recommendation_count,
            "cosmetic_patch_suppression_enabled": True,
            "recommended_next_layer": (
                "python -m Tools.ai agent_review_patch_plan" if recommendations else "collect_more_evidence"
            ),
            "manual_review_required": True,
        },
        "inputs": {
            "evidence": normalize_repo_path(args.evidence),
            "orchestrator": normalize_repo_path(args.orchestrator),
            "gpu_report": normalize_repo_path(args.gpu_report)
            or normalize_repo_path(orchestrator.get("gpu_output")),
            "tool_report_count": len(args.tool_report),
            "repository_consistency_map_count": len(repository_consistency_maps),
            "evidence_kind": evidence.get("kind"),
            "orchestrator_kind": orchestrator.get("kind"),
            "gpu_kind": gpu_report.get("kind"),
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "real_github_pr_created": False,
            "npu_primary_advisory": False,
            "openvino_gpu_primary_lane": False,
        },
    }

def build_patch_plan_bridge_orchestrator(
    *,
    repo_root: Path,
    recommendation_report: dict[str, Any],
    recommendation_output: Path,
    source_orchestrator: dict[str, Any] | None = None,
) -> dict[str, Any]:
    source_orchestrator = source_orchestrator if isinstance(source_orchestrator, dict) else {}
    return {
        "schema_version": 1,
        "kind": "deterministic_recommendation_patch_plan_bridge_orchestrator",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": recommendation_report.get("passed"),
        "errors": list(recommendation_report.get("errors") or []),
        "warnings": list(recommendation_report.get("warnings") or []),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "gpu_output": repo_rel(recommendation_output, repo_root),
        "gpu_recommendation_count": recommendation_report.get("recommendation_count", 0),
        "gpu_empty_recommendations_reason": "",
        "gpu_recommended_next_layer": "python -m Tools.ai agent_review_patch_plan",
        "npu_audits": source_orchestrator.get("npu_audits", []),
        "decision": {
            "deterministic_recommendation_bridge": True,
            "manual_review_required": True,
            "recommended_next_layer": "python -m Tools.ai agent_review_patch_plan",
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "real_github_pr_created": False,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Deterministic Recommendation Synthesizer", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Recommendation count: `{report['recommendation_count']}`")
    lines.append(
        f"- Deterministic synthesizer used: `{report['decision']['deterministic_synthesizer_used']}`"
    )
    lines.append(
        f"- GPU empty recommendations reason: `{report['decision']['gpu_empty_recommendations_reason']}`"
    )
    lines.append(
        f"- Evidence ready for manual patch count: `{report['decision']['evidence_ready_for_manual_patch_count']}`"
    )
    lines.append(f"- Next best action: `{report['next_best_action']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    if not report.get("recommendations"):
        lines.append("- none")
    for rec in report.get("recommendations", []):
        lines.append(f"### {rec.get('id')} — {rec.get('area')}")
        lines.append(f"- Source: `{rec.get('source')}`")
        lines.append(f"- Status: `{rec.get('status')}`")
        lines.append(f"- Risk: `{rec.get('risk')}`")
        lines.append(f"- Target files: `{rec.get('target_files')}`")
        lines.append(f"- Rationale: {rec.get('rationale')}")
        lines.append(f"- Strategy: {rec.get('proposed_strategy')}")
        lines.append("")
    if report.get("skipped_candidates"):
        lines.append("## Skipped candidates")
        lines.append("")
        for item in report["skipped_candidates"]:
            lines.append(f"- `{item.get('id')}`: {item.get('reason')}")
        lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.append("This report is deterministic and report-only. It is not a patch queue.")
    return "\n".join(lines) + "\n"
