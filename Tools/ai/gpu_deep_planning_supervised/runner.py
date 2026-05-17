from __future__ import annotations

from .audit import checkpoint_paths, refresh_live_context_reports, run_npu_audit_for_checkpoint
from .common import *  # noqa: F403
from .reporting import build_report
from .runtime_tools import (
    append_runtime_tool_feedback_context,
    run_runtime_tool_bootstrap,
    run_runtime_tool_broker_for_round,
    runtime_tool_context_report,
    run_schema_repair_retry_for_round,
)
def run_supervised(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    started_at = time.perf_counter()
    evidence = read_json(resolve_path(repo_root, args.evidence))
    refined = (
        read_json(resolve_path(repo_root, args.refined_review))
        if resolve_path(repo_root, args.refined_review).exists()
        else {}
    )
    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    context_reports = []
    runtime_tool_bootstrap = run_runtime_tool_bootstrap(repo_root, args)
    args.runtime_tool_bootstrap_result = runtime_tool_bootstrap
    if runtime_tool_bootstrap.get("executed"):
        context_reports.append(runtime_tool_context_report(0, runtime_tool_bootstrap))
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
                provider_error = f"{type(exc).__name__}: {exc}"
                context_reports.append({"path": repo_rel(path, repo_root), "error": str(exc)})
        else:
            context_reports.append({"path": repo_rel(path, repo_root), "error": "missing"})

    if not args.use_ollama:
        return {
            "schema_version": 1,
            "kind": "agent_gpu_deep_planning_supervised",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": False,
            "errors": ["--use-ollama is required"],
            "warnings": [],
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
            "elapsed_seconds": 0,
            "round_count": 0,
            "npu_audit_count": 0,
            "npu_audit_requested_count": 0,
            "npu_audit_success_count": 0,
            "npu_auditor_disabled_reason": "",
            "recommendation_count": 0,
            "raw_recommendation_candidate_count": 0,
            "filtered_recommendation_count": 0,
            "tool_request_count": 0,
            "valid_tool_request_count": 0,
            "invalid_tool_request_count": 0,
            "provider_empty_response_count": 0,
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
            "runtime_tool_bootstrap_result_count": len(
                runtime_tool_bootstrap.get("tool_results", [])
            ),
            "runtime_tool_bootstrap_output": runtime_tool_bootstrap.get("broker_output", ""),
            "runtime_tool_bootstrap": runtime_tool_bootstrap,
            "runtime_tool_request_count": int(
                runtime_tool_bootstrap.get("requested_tool_count") or 0
            ),
            "runtime_tool_execution_count": int(
                runtime_tool_bootstrap.get("tool_execution_count") or 0
            ),
            "runtime_tool_failed_count": int(runtime_tool_bootstrap.get("failed_tool_count") or 0),
            "runtime_tool_blocked_count": int(
                runtime_tool_bootstrap.get("blocked_tool_count") or 0
            ),
            "runtime_tool_result_count": len(runtime_tool_bootstrap.get("tool_results", [])),
            "runtime_tool_provider_request_count": 0,
            "runtime_tool_provider_request_execution_count": 0,
            "deterministic_runtime_tool_fallback_request_count": 0,
            "deterministic_runtime_tool_fallback_execution_count": 0,
            "deterministic_runtime_tool_fallback_failed_count": 0,
            "deterministic_runtime_tool_fallback_blocked_count": 0,
            "json_parse_error_count": 0,
            "repair_attempt_count": 0,
            "empty_recommendations_reason": "valid_json_empty_recommendations",
            "evidence_ready_for_manual_patch_count": evidence_ready_count,
            "recommended_next_layer": "collect_more_evidence",
            "decision": {"ready_for_patch_plan": False, "manual_review_required": True},
            "guardrails": {
                "provider_execution_requires_use_ollama": True,
                "patch_application_performed": False,
                "runtime_tool_bootstrap_report_only": True,
                "runtime_tool_bootstrap_requires_enable_runtime_tool_broker": True,
                "persistent_memory_write_performed": False,
            },
        }

    evidence_paths = extract_evidence_files(evidence)
    context_roots = list(args.context_root or []) + evidence_paths
    if not context_roots:
        context_roots = ["docs", "tools/ai", "tools/validation", "tools/workflow"]
    context_files = collect_repo_context(
        repo_root, context_roots, args.max_context_files, args.max_chars_per_file
    )
    batches = split_batches(context_files, args.files_per_round)
    checkpoint_dir = resolve_path(repo_root, args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    deadline = started_at + max(1, args.budget_minutes) * 60
    rounds: list[dict[str, Any]] = []
    npu_audits: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    model_used = args.ollama_model or ""
    base_url = normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL)
    npu_auditor_disabled_reason = ""

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
            live_context_report_count = 0
            if args.refresh_live_context_each_round or (index == 1 and args.live_context_report):
                live_context_report_count = refresh_live_context_reports(
                    context_reports,
                    repo_root,
                    args.live_context_report or [],
                )
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
                elapsed_seconds=time.perf_counter() - started_at,
            )
            round_start = time.perf_counter()
            schema_repair_retry: dict[str, Any] = {
                "attempted": False,
                "accepted": False,
                "reason": "not_attempted",
            }
            raw_response = ""
            provider_error = ""
            model_used_for_round = model_used if "model_used" in locals() else model
            try:
                response, model_used = manager.generate(
                    args.ollama_model,
                    prompt,
                    max_new_tokens=args.max_new_tokens,
                    temperature=args.temperature,
                    response_format="json",
                )
                raw_response = response
                model_used_for_round = model_used
                if not str(response or "").strip():
                    parsed = {
                        "summary": "provider returned an empty response",
                        "confidence": "low",
                        "recommendations": [],
                        "tool_requests": [],
                        "missing_evidence": ["provider_empty_response"],
                        "next_best_action": "inspect provider runtime, prompt budget and model output settings",
                    }
                    parse_diagnostics = {
                        "json_ok": False,
                        "parse_error": "ProviderEmptyResponse: model returned an empty response",
                        "repair_attempt_count": 0,
                        "model_output_missing_required_fields": False,
                        "provider_empty_response": True,
                        "provider_error": provider_error,
                    }
                    errors.append(f"round {index}: provider_empty_response")
                else:
                    parsed, parse_diagnostics = parse_model_json_with_diagnostics(
                        response, evidence_ready_count
                    )
                    schema_repair_retry = run_schema_repair_retry_for_round(
                        manager=manager,
                        model=model_used,
                        args=args,
                        round_index=index,
                        objective=args.objective,
                        raw_response=raw_response,
                        parsed_response=parsed,
                        parse_diagnostics=parse_diagnostics,
                        context_reports=context_reports,
                        rounds=rounds,
                        evidence_ready_for_manual_patch_count=evidence_ready_count,
                    )
                    if schema_repair_retry.get("accepted"):
                        raw_response = str(schema_repair_retry.get("raw_response") or raw_response)
                        parsed = dict(schema_repair_retry.get("parsed_response") or parsed)
                        parse_diagnostics = dict(
                            schema_repair_retry.get("parse_diagnostics") or parse_diagnostics
                        )
            except Exception as exc:  # noqa: BLE001
                provider_error = f"{type(exc).__name__}: {exc}"
                response = ""
                raw_response = response
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
                    "provider_empty_response": False,
                }
                errors.append(f"round {index}: {type(exc).__name__}: {exc}")
            round_diagnostics = recommendation_diagnostics_for_round(
                parsed, parse_diagnostics, evidence_ready_count
            )
            if parse_diagnostics.get("provider_empty_response"):
                round_diagnostics["empty_recommendations_reason"] = "provider_empty_response"
            valid_tool_requests, invalid_tool_request_errors = extract_valid_tool_requests(
                parsed,
                max_requests=args.runtime_tool_max_requests_per_round,
            )
            deterministic_fallback_used = False
            deterministic_fallback_reason = ""
            deterministic_fallback_requests: list[dict[str, Any]] = []
            broker_tool_requests = valid_tool_requests
            if invalid_tool_request_errors:
                warnings.append(
                    f"round {index}: invalid tool requests: {invalid_tool_request_errors}"
                )
            if not valid_tool_requests and args.enable_runtime_tool_broker:
                fallback_reason = str(round_diagnostics.get("empty_recommendations_reason") or "")
                if fallback_reason in {
                    "context_echo_detected",
                    "json_parse_failure",
                    "model_output_schema_mismatch",
                    "evidence_ready_but_no_tool_requests",
                    "valid_json_empty_recommendations",
                }:
                    deterministic_fallback_requests = deterministic_fallback_tool_requests(
                        fallback_reason,
                        max_requests=args.runtime_tool_max_requests_per_round,
                    )
                    if deterministic_fallback_requests:
                        deterministic_fallback_used = True
                        deterministic_fallback_reason = fallback_reason
                        broker_tool_requests = deterministic_fallback_requests
            runtime_broker = run_runtime_tool_broker_for_round(
                repo_root=repo_root,
                args=args,
                round_index=index,
                tool_requests=broker_tool_requests,
            )
            runtime_tool_feedback_context_appended = append_runtime_tool_feedback_context(
                context_reports,
                index,
                runtime_broker,
            )
            if deterministic_fallback_used:
                runtime_broker["source"] = "deterministic_fallback"
                runtime_broker["provider_generated_tool_requests"] = False
                runtime_broker["deterministic_fallback_reason"] = deterministic_fallback_reason
            elif valid_tool_requests:
                runtime_broker["source"] = "provider_tool_requests"
                runtime_broker["provider_generated_tool_requests"] = True
            if runtime_broker.get("error"):
                warnings.append(f"runtime tool broker round {index}: {runtime_broker.get('error')}")
            if runtime_broker.get("returncode") not in (None, 0):
                warnings.append(
                    f"runtime tool broker round {index}: returncode={runtime_broker.get('returncode')}"
                )
            if runtime_broker.get("executed"):
                context_reports.append(runtime_tool_context_report(index, runtime_broker))
            round_data = {
                "round": index,
                "elapsed_seconds": round(time.perf_counter() - round_start, 3),
                "file_count": len(batch),
                "files": [item.path for item in batch],
                "live_context_report_count": live_context_report_count,
                "live_context_refresh_performed": bool(live_context_report_count),
                "response_chars": len(response),
                "raw_response_preview": response[:3000],
                "parsed_response": parsed,
                "schema_repair_retry": summarize_schema_repair_retry(schema_repair_retry),
                "provider_empty_response": bool(parse_diagnostics.get("provider_empty_response")),
                "tool_requests": valid_tool_requests,
                "invalid_tool_request_errors": invalid_tool_request_errors,
                "runtime_tool_broker": runtime_broker,
                "provider_tool_request_count": len(valid_tool_requests),
                "deterministic_runtime_tool_fallback_used": deterministic_fallback_used,
                "deterministic_runtime_tool_fallback_reason": deterministic_fallback_reason,
                "deterministic_runtime_tool_fallback_request_count": len(
                    deterministic_fallback_requests
                ),
                **round_diagnostics,
            }
            rounds.append(round_data)
            interim_report = build_report(
                repo_root=repo_root,
                args=args,
                evidence=evidence,
                refined=refined,
                context_reports=context_reports,
                context_file_count=len(context_files),
                rounds=rounds,
                npu_audits=npu_audits,
                model_used=model_used,
                errors=errors,
                warnings=warnings,
                started_at=started_at,
                npu_auditor_disabled_reason=npu_auditor_disabled_reason,
            )
            checkpoint_json, checkpoint_md, audit_json = checkpoint_paths(checkpoint_dir, index)
            write_json(checkpoint_json, interim_report)
            checkpoint_md.write_text(build_markdown(interim_report), encoding="utf-8")
            should_audit = (
                args.include_npu_auditor
                and not npu_auditor_disabled_reason
                and index % max(1, args.npu_auditor_every_rounds) == 0
            )
            if should_audit:
                audit = run_npu_audit_for_checkpoint(repo_root, checkpoint_json, audit_json, args)
                npu_audits.append(audit)
                if audit.get("error"):
                    warnings.append(f"NPU audit round {index}: {audit.get('error')}")
                classification = str(audit.get("classification") or "")
                if classification not in {
                    "usable_audit_text",
                    "metadata_only",
                    "not_executed",
                }:
                    warnings.append(f"NPU audit round {index}: classification={classification}")
                if classification in TERMINAL_NPU_AUDIT_CLASSIFICATIONS:
                    npu_auditor_disabled_reason = classification
                    warnings.append(
                        f"NPU auditor circuit breaker enabled after round {index}: {classification}"
                    )

    return build_report(
        repo_root=repo_root,
        args=args,
        evidence=evidence,
        refined=refined,
        context_reports=context_reports,
        context_file_count=len(context_files),
        rounds=rounds,
        npu_audits=npu_audits,
        model_used=model_used,
        errors=errors,
        warnings=warnings,
        started_at=started_at,
        npu_auditor_disabled_reason=npu_auditor_disabled_reason,
    )
