from __future__ import annotations

from .common import *  # noqa: F403

def build_report(
    *,
    repo_root: Path,
    args: argparse.Namespace,
    evidence: dict[str, Any],
    refined: dict[str, Any],
    context_reports: list[dict[str, Any]],
    context_file_count: int,
    rounds: list[dict[str, Any]],
    npu_audits: list[dict[str, Any]],
    model_used: str,
    errors: list[str],
    warnings: list[str],
    started_at: float,
    npu_auditor_disabled_reason: str = "",
) -> dict[str, Any]:
    recommendations = merge_recommendations(rounds)
    diagnostics = aggregate_recommendation_diagnostics(rounds, evidence)
    ready = [rec for rec in recommendations if rec.get("status") == "ready_for_patch_plan"]
    needs_context = [rec for rec in recommendations if rec.get("status") == "needs_more_context"]
    unusable_npu = [
        audit
        for audit in npu_audits
        if audit.get("classification") not in {"usable_audit_text", "not_executed", "metadata_only"}
    ]
    npu_success_count = sum(
        1
        for audit in npu_audits
        if audit.get("provider_execution_succeeded") is True
        or audit.get("classification") == "usable_audit_text"
    )
    npu_requested_count = sum(
        1 for audit in npu_audits if audit.get("provider_execution_requested") is True
    )
    fallback_recommended = (
        diagnostics["evidence_ready_for_manual_patch_count"] > 0
        and diagnostics["filtered_recommendation_count"] == 0
    )
    runtime_tool_bootstrap = getattr(args, "runtime_tool_bootstrap_result", {})
    runtime_brokers = [
        round_item.get("runtime_tool_broker", {})
        for round_item in rounds
        if round_item.get("runtime_tool_broker")
    ]
    provider_runtime_brokers = [
        item for item in runtime_brokers if item.get("source") != "deterministic_fallback"
    ]
    deterministic_runtime_brokers = [
        item for item in runtime_brokers if item.get("source") == "deterministic_fallback"
    ]
    runtime_tool_request_count = int(runtime_tool_bootstrap.get("requested_tool_count") or 0) + sum(
        int(item.get("requested_tool_count") or 0) for item in runtime_brokers
    )
    runtime_tool_execution_count = int(
        runtime_tool_bootstrap.get("tool_execution_count") or 0
    ) + sum(int(item.get("tool_execution_count") or 0) for item in runtime_brokers)
    runtime_tool_failed_count = int(runtime_tool_bootstrap.get("failed_tool_count") or 0) + sum(
        int(item.get("failed_tool_count") or 0) for item in runtime_brokers
    )
    runtime_tool_blocked_count = int(runtime_tool_bootstrap.get("blocked_tool_count") or 0) + sum(
        int(item.get("blocked_tool_count") or 0) for item in runtime_brokers
    )
    runtime_tool_result_count = len(runtime_tool_bootstrap.get("tool_results", [])) + sum(
        len(item.get("tool_results", [])) for item in runtime_brokers
    )
    runtime_tool_provider_request_count = sum(
        int(item.get("requested_tool_count") or 0) for item in provider_runtime_brokers
    )
    runtime_tool_provider_request_execution_count = sum(
        int(item.get("tool_execution_count") or 0) for item in provider_runtime_brokers
    )
    deterministic_runtime_tool_fallback_request_count = sum(
        int(item.get("requested_tool_count") or 0) for item in deterministic_runtime_brokers
    )
    deterministic_runtime_tool_fallback_execution_count = sum(
        int(item.get("tool_execution_count") or 0) for item in deterministic_runtime_brokers
    )
    deterministic_runtime_tool_fallback_failed_count = sum(
        int(item.get("failed_tool_count") or 0) for item in deterministic_runtime_brokers
    )
    deterministic_runtime_tool_fallback_blocked_count = sum(
        int(item.get("blocked_tool_count") or 0) for item in deterministic_runtime_brokers
    )
    provider_empty_response_count = sum(
        1 for round_item in rounds if round_item.get("provider_empty_response")
    )
    provider_error_count = sum(1 for round_item in rounds if round_item.get("provider_error"))
    schema_repair_retry_attempt_count = sum(
        1 for round_item in rounds if round_item.get("schema_repair_retry", {}).get("attempted")
    )
    schema_repair_retry_accept_count = sum(
        1 for round_item in rounds if round_item.get("schema_repair_retry", {}).get("accepted")
    )
    runtime_tool_feedback_context_report_count = sum(
        1
        for item in context_reports
        if isinstance(item, dict) and item.get("kind") == "runtime_tool_feedback_context"
    )
    report_errors = list(errors)
    runtime_tool_bootstrap_failed = bool(
        runtime_tool_bootstrap.get("executed") and runtime_tool_bootstrap.get("passed") is not True
    )
    if runtime_tool_bootstrap_failed:
        detail = (
            runtime_tool_bootstrap.get("error")
            or f"returncode={runtime_tool_bootstrap.get('returncode')} broker_output_exists={runtime_tool_bootstrap.get('broker_output_exists')}"
        )
        report_errors.append(f"runtime_tool_bootstrap_failed: {detail}")
    if provider_empty_response_count:
        diagnostics = dict(diagnostics)
        diagnostics["empty_recommendations_reason"] = "provider_empty_response"
        diagnostics["recommended_next_layer"] = "inspect_provider_empty_response"
        fallback_recommended = False
    return {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_supervised",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not report_errors,
        "errors": report_errors,
        "warnings": warnings,
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
        "model_used": model_used,
        "ollama_base_url": normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL),
        "budget_minutes": args.budget_minutes,
        "elapsed_seconds": round(time.perf_counter() - started_at, 3),
        "context_file_count": context_file_count,
        "round_count": len(rounds),
        "rounds": rounds,
        "npu_audit_count": len(npu_audits),
        "npu_audit_requested_count": npu_requested_count,
        "npu_audit_success_count": npu_success_count,
        "npu_auditor_disabled_reason": npu_auditor_disabled_reason,
        "npu_audits": npu_audits,
        "runtime_tool_broker_enabled": bool(args.enable_runtime_tool_broker),
        "runtime_tool_bootstrap_enabled": bool(
            args.enable_runtime_tool_broker and not args.disable_runtime_tool_bootstrap
        ),
        "runtime_tool_bootstrap_executed": bool(runtime_tool_bootstrap.get("executed")),
        "runtime_tool_bootstrap_passed": runtime_tool_bootstrap.get("passed"),
        "runtime_tool_bootstrap_request_count": int(
            runtime_tool_bootstrap.get("requested_tool_count") or 0
        ),
        "runtime_tool_bootstrap_execution_count": int(
            runtime_tool_bootstrap.get("tool_execution_count") or 0
        ),
        "runtime_tool_bootstrap_failed_count": int(
            runtime_tool_bootstrap.get("failed_tool_count") or 0
        ),
        "runtime_tool_bootstrap_blocked_count": int(
            runtime_tool_bootstrap.get("blocked_tool_count") or 0
        ),
        "runtime_tool_bootstrap_result_count": len(runtime_tool_bootstrap.get("tool_results", [])),
        "runtime_tool_bootstrap_output": runtime_tool_bootstrap.get("broker_output", ""),
        "runtime_tool_bootstrap": runtime_tool_bootstrap,
        "runtime_tool_request_count": runtime_tool_request_count,
        "runtime_tool_execution_count": runtime_tool_execution_count,
        "runtime_tool_failed_count": runtime_tool_failed_count,
        "runtime_tool_blocked_count": runtime_tool_blocked_count,
        "runtime_tool_result_count": runtime_tool_result_count,
        "runtime_tool_provider_request_count": runtime_tool_provider_request_count,
        "runtime_tool_provider_request_execution_count": runtime_tool_provider_request_execution_count,
        "runtime_tool_feedback_context_report_count": runtime_tool_feedback_context_report_count,
        "live_context_refresh_enabled": bool(args.refresh_live_context_each_round),
        "live_context_report_paths": list(args.live_context_report or []),
        "live_context_refresh_count": sum(
            int(round_item.get("live_context_report_count") or 0) for round_item in rounds
        ),
        "deterministic_runtime_tool_fallback_request_count": deterministic_runtime_tool_fallback_request_count,
        "deterministic_runtime_tool_fallback_execution_count": deterministic_runtime_tool_fallback_execution_count,
        "deterministic_runtime_tool_fallback_failed_count": deterministic_runtime_tool_fallback_failed_count,
        "deterministic_runtime_tool_fallback_blocked_count": deterministic_runtime_tool_fallback_blocked_count,
        "provider_empty_response_count": provider_empty_response_count,
        "provider_error_count": provider_error_count,
        "schema_repair_retry_attempt_count": schema_repair_retry_attempt_count,
        "schema_repair_retry_accept_count": schema_repair_retry_accept_count,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        **diagnostics,
        "decision": {
            "ready_for_patch_plan": bool(ready),
            "ready_count": len(ready),
            "needs_more_context_count": len(needs_context),
            "fallback_patch_plan_recommended": fallback_recommended,
            "npu_auditor_non_blocking": True,
            "npu_unusable_or_failed_count": len(unusable_npu),
            "npu_audit_success_count": npu_success_count,
            "npu_auditor_disabled_reason": npu_auditor_disabled_reason,
            "recommended_next_layer": diagnostics["recommended_next_layer"],
            "manual_review_required": True,
        },
        "inputs": {
            "evidence_kind": evidence.get("kind"),
            "refined_kind": refined.get("kind"),
            "context_report_count": len(context_reports),
        },
        "guardrails": {
            "provider_execution_requires_use_ollama": True,
            "npu_auditor_requires_include_npu_auditor": True,
            "npu_auditor_non_blocking": True,
            "npu_primary_advisory": False,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "runtime_tool_broker_report_only": True,
            "runtime_tool_broker_requires_enable_runtime_tool_broker": True,
            "manual_review_required": True,
        },
    }
