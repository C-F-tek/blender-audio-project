from __future__ import annotations

from .common import *  # noqa: F403
from .parsing import aggregate_recommendation_diagnostics, parse_model_json_with_diagnostics, recommendation_diagnostics_for_round
from .prompt import build_prompt
from .reporting import merge_recommendations

def run_deep_review(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    evidence = read_json(resolve_path(repo_root, args.evidence))
    refined = (
        read_json(resolve_path(repo_root, args.refined_review))
        if resolve_path(repo_root, args.refined_review).exists()
        else {}
    )
    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    context_reports = []
    for report_file in args.report_file:
        path = resolve_path(repo_root, report_file)
        if path.exists():
            try:
                data = read_json(path)
                context_reports.append(
                    {
                        "path": repo_rel(path, repo_root),
                        "kind": data.get("kind"),
                        "passed": data.get("passed"),
                        "summary": data.get("summary", {}),
                        "decision": data.get("decision", {}),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                context_reports.append({"path": repo_rel(path, repo_root), "error": str(exc)})
        else:
            context_reports.append({"path": repo_rel(path, repo_root), "error": "missing"})

    evidence_paths = extract_evidence_files(evidence)
    context_roots = list(args.context_root or []) + evidence_paths
    if not context_roots:
        context_roots = ["docs", "tools/ai", "tools/validation", "tools/workflow"]
    context_files = collect_repo_context(
        repo_root, context_roots, args.max_context_files, args.max_chars_per_file
    )
    batches = split_batches(context_files, args.files_per_round)

    start = time.perf_counter()
    deadline = start + max(1, args.budget_minutes) * 60
    rounds: list[dict[str, Any]] = []
    model_used = args.ollama_model or ""
    errors: list[str] = []

    if not args.use_ollama:
        return {
            "schema_version": 1,
            "kind": "agent_gpu_deep_planning_review",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": False,
            "errors": ["--use-ollama is required for GPU deep planning review"],
            "warnings": [],
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "apply_mode": "report_only_gpu_deep_planning",
            "elapsed_seconds": 0,
            "round_count": 0,
            "recommendation_count": 0,
            "raw_recommendation_candidate_count": 0,
            "filtered_recommendation_count": 0,
            "tool_request_count": 0,
            "valid_tool_request_count": 0,
            "invalid_tool_request_count": 0,
            "json_parse_error_count": 0,
            "repair_attempt_count": 0,
            "empty_recommendations_reason": "valid_json_empty_recommendations",
            "evidence_ready_for_manual_patch_count": evidence_ready_count,
            "recommended_next_layer": "collect_more_evidence",
            "recommendations": [],
            "decision": {
                "ready_for_patch_plan": False,
                "reason": "provider execution not enabled",
            },
            "guardrails": {
                "provider_execution_requires_use_ollama": True,
                "patch_application_performed": False,
            },
        }

    base_url = normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL)
    with OllamaModelManager(
        base_url=base_url,
        keep_alive=args.keep_alive,
        shutdown_server=False,
        startup_timeout=args.startup_timeout,
    ) as manager:
        for index, batch in enumerate(batches, start=1):
            if index > args.max_rounds:
                break
            if time.perf_counter() >= deadline and rounds:
                break
            context_reports = build_schema_repair_context_stack(
                base_context_reports=context_reports,
                rounds=rounds,
                evidence_ready_for_manual_patch_count=evidence_ready_count,
                provider="gpu_ollama",
            )
            prompt = build_prompt(
                objective=args.objective,
                evidence=evidence,
                refined=refined,
                context_reports=context_reports,
                batch=batch,
                round_index=index,
                elapsed_seconds=time.perf_counter() - start,
            )
            round_start = time.perf_counter()
            try:
                response, model_used = manager.generate(
                    args.ollama_model,
                    prompt,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                )
                parsed, parse_diagnostics = parse_model_json_with_diagnostics(
                    response, evidence_ready_count
                )
            except Exception as exc:  # noqa: BLE001 - report-only provider diagnostics.
                response = ""
                parsed = {
                    "summary": "provider error",
                    "confidence": "low",
                    "recommendations": [],
                    "missing_evidence": [str(exc)],
                    "next_best_action": "inspect provider error",
                }
                parse_diagnostics = {
                    "json_ok": False,
                    "parse_error": f"{type(exc).__name__}: {exc}",
                    "repair_attempt_count": 0,
                    "model_output_missing_required_fields": False,
                }
                errors.append(f"round {index}: {type(exc).__name__}: {exc}")
            round_diagnostics = recommendation_diagnostics_for_round(
                parsed, parse_diagnostics, evidence_ready_count
            )
            rounds.append(
                {
                    "round": index,
                    "elapsed_seconds": round(time.perf_counter() - round_start, 3),
                    "file_count": len(batch),
                    "files": [item.path for item in batch],
                    "response_chars": len(response),
                    "raw_response_preview": response[:3000],
                    "parsed_response": parsed,
                    **round_diagnostics,
                }
            )

    recommendations = merge_recommendations(rounds)
    diagnostics = aggregate_recommendation_diagnostics(rounds, evidence)
    ready = [rec for rec in recommendations if rec.get("status") == "ready_for_patch_plan"]
    needs_context = [rec for rec in recommendations if rec.get("status") == "needs_more_context"]
    fallback_recommended = (
        diagnostics["evidence_ready_for_manual_patch_count"] > 0
        and diagnostics["filtered_recommendation_count"] == 0
    )
    decision = {
        "ready_for_patch_plan": bool(ready),
        "ready_count": len(ready),
        "needs_more_context_count": len(needs_context),
        "fallback_patch_plan_recommended": fallback_recommended,
        "recommended_next_layer": diagnostics["recommended_next_layer"],
        "manual_review_required": True,
    }
    return {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_review",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_gpu_deep_planning",
        "model_used": model_used,
        "ollama_base_url": base_url,
        "budget_minutes": args.budget_minutes,
        "elapsed_seconds": round(time.perf_counter() - start, 3),
        "context_file_count": len(context_files),
        "round_count": len(rounds),
        "rounds": rounds,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        **diagnostics,
        "decision": decision,
        "guardrails": {
            "provider_execution_requires_use_ollama": True,
            "provider_execution_performed": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "manual_review_required": True,
        },
    }
