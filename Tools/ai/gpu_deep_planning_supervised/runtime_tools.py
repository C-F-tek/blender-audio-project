from __future__ import annotations

from .common import *  # noqa: F403

def run_runtime_tool_broker_for_round(
    *,
    repo_root: Path,
    args: argparse.Namespace,
    round_index: int,
    tool_requests: list[dict[str, Any]],
) -> dict[str, Any]:
    """Execute valid planner tool requests through the report-only broker."""

    if not args.enable_runtime_tool_broker:
        return {
            "enabled": False,
            "requested_tool_count": len(tool_requests),
            "executed": False,
            "tool_results": [],
            "guardrails": {
                "broker_execution_requires_enable_runtime_tool_broker": True,
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }
    if not tool_requests:
        return {
            "enabled": True,
            "requested_tool_count": 0,
            "executed": False,
            "tool_results": [],
            "guardrails": {
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }

    request_sources = {
        str(item.get("source") or "provider") for item in tool_requests if isinstance(item, dict)
    }
    request_source = (
        "deterministic_fallback" if request_sources == {"deterministic_fallback"} else "provider"
    )

    output_root = resolve_path(repo_root, args.runtime_tool_output_dir)
    round_dir = output_root / f"round_{round_index:03d}"
    round_dir.mkdir(parents=True, exist_ok=True)
    request_file = round_dir / f"round_{round_index:03d}_tool_requests.json"
    broker_output = round_dir / f"round_{round_index:03d}_runtime_tool_broker.json"
    broker_markdown = round_dir / f"round_{round_index:03d}_runtime_tool_broker.md"
    request_packet = {
        "schema_version": 1,
        "kind": "gpu_planner_runtime_tool_requests",
        "repo_root": str(repo_root),
        "round": round_index,
        "tool_requests": tool_requests,
        "guardrails": {
            "free_shell_allowed": False,
            "broker_allowlist_required": True,
            "patch_application_allowed": False,
            "persistent_memory_write_allowed": False,
            "manual_review_required": True,
        },
    }
    write_json(request_file, request_packet)
    command = [
        sys.executable,
        "tools/ai/agent_runtime_tool_broker.py",
        "--repo-root",
        ".",
        "--request-file",
        str(request_file),
        "--tool-output-dir",
        str(round_dir),
        "--timeout-seconds",
        str(args.runtime_tool_timeout_seconds),
        "--output",
        str(broker_output),
        "--markdown-output",
        str(broker_markdown),
    ]
    returncode, stdout, stderr, error = run_command(
        command, repo_root, args.runtime_tool_timeout_seconds + 30
    )
    broker_report: dict[str, Any] = {}
    broker_output_exists = broker_output.exists()
    if broker_output_exists:
        try:
            broker_report = read_json(broker_output)
        except Exception as exc:  # noqa: BLE001
            error = f"{error or ''} {type(exc).__name__}: {exc}".strip()
    elif not error:
        error = "runtime_tool_broker_output_missing"

    return {
        "enabled": True,
        "source": request_source,
        "deterministic_fallback": request_source == "deterministic_fallback",
        "executed": True,
        "requested_tool_count": len(tool_requests),
        "command": command,
        "returncode": returncode,
        "stdout_tail": stdout,
        "stderr_tail": stderr,
        "error": error or "",
        "request_file": repo_rel(request_file, repo_root),
        "broker_output": repo_rel(broker_output, repo_root),
        "broker_markdown": repo_rel(broker_markdown, repo_root),
        "broker_output_exists": broker_output_exists,
        "passed": broker_report.get("passed"),
        "tool_request_count": broker_report.get("tool_request_count", len(tool_requests)),
        "tool_execution_count": broker_report.get("tool_execution_count", 0),
        "blocked_tool_count": broker_report.get("blocked_tool_count", 0),
        "failed_tool_count": broker_report.get("failed_tool_count", 0),
        "operational_sqlite_write_performed": broker_report.get(
            "operational_sqlite_write_performed", False
        ),
        "provider_execution_performed": broker_report.get("provider_execution_performed", False),
        "patch_application_performed": broker_report.get("patch_application_performed", False),
        "sqlite_write_performed": broker_report.get("sqlite_write_performed", False),
        "persistent_memory_write_performed": broker_report.get(
            "persistent_memory_write_performed", False
        ),
        "tool_results": compact_tool_results_for_context(broker_report.get("tool_results", [])),
        "guardrails": broker_report.get("guardrails", {}),
    }

def runtime_tool_context_report(round_index: int, broker_result: dict[str, Any]) -> dict[str, Any]:
    return {
        "path": broker_result.get("broker_output"),
        "kind": "agent_runtime_tool_broker",
        "passed": broker_result.get("passed"),
        "summary": {
            "round": round_index,
            "bootstrap": bool(broker_result.get("bootstrap")),
            "tool_request_count": broker_result.get("tool_request_count"),
            "tool_execution_count": broker_result.get("tool_execution_count"),
            "blocked_tool_count": broker_result.get("blocked_tool_count"),
            "failed_tool_count": broker_result.get("failed_tool_count"),
            "operational_sqlite_write_performed": broker_result.get(
                "operational_sqlite_write_performed"
            ),
        },
        "decision": {
            "runtime_tool_results_available": bool(broker_result.get("tool_results")),
            "manual_review_required": True,
        },
        "tool_results": broker_result.get("tool_results", []),
    }

def runtime_tool_feedback_context_report(
    round_index: int, broker_result: dict[str, Any]
) -> dict[str, Any]:
    """Build compact closed-loop context from a runtime broker result."""

    source = str(broker_result.get("source") or "provider")
    tool_results = broker_result.get("tool_results", [])
    if not isinstance(tool_results, list):
        tool_results = []
    return {
        "path": broker_result.get("broker_output"),
        "kind": "runtime_tool_feedback_context",
        "source": source,
        "round": round_index,
        "passed": broker_result.get("passed"),
        "summary": {
            "tool_request_count": broker_result.get("tool_request_count"),
            "requested_tool_count": broker_result.get("requested_tool_count"),
            "tool_execution_count": broker_result.get("tool_execution_count"),
            "blocked_tool_count": broker_result.get("blocked_tool_count"),
            "failed_tool_count": broker_result.get("failed_tool_count"),
            "deterministic_fallback": bool(broker_result.get("deterministic_fallback")),
            "provider_execution_performed": broker_result.get("provider_execution_performed"),
            "patch_application_performed": broker_result.get("patch_application_performed"),
            "sqlite_write_performed": broker_result.get("sqlite_write_performed"),
            "persistent_memory_write_performed": broker_result.get(
                "persistent_memory_write_performed"
            ),
            "operational_sqlite_write_performed": broker_result.get(
                "operational_sqlite_write_performed"
            ),
        },
        "decision": {
            "runtime_tool_results_available": bool(tool_results),
            "feed_into_next_provider_round": True,
            "manual_review_required": True,
            "do_not_treat_fallback_as_provider_emitted": source == "deterministic_fallback",
        },
        "tool_results": tool_results,
        "guardrails": {
            "report_only": True,
            "provider_must_not_execute_tools_directly": True,
            "patch_application_performed": False,
            "persistent_memory_write_performed": False,
        },
    }

def append_runtime_tool_feedback_context(
    context_reports: list[dict[str, Any]],
    round_index: int,
    broker_result: dict[str, Any],
    *,
    max_feedback_reports: int = 24,
) -> bool:
    """Append broker feedback context for subsequent provider rounds."""

    if not isinstance(broker_result, dict):
        return False
    if not broker_result.get("executed"):
        return False
    if broker_result.get("broker_output_exists") is False and not broker_result.get("tool_results"):
        return False

    feedback = runtime_tool_feedback_context_report(round_index, broker_result)
    existing = [
        item
        for item in context_reports
        if isinstance(item, dict) and item.get("kind") == "runtime_tool_feedback_context"
    ]

    if len(existing) >= max_feedback_reports:
        removed = 0
        trimmed: list[dict[str, Any]] = []
        for item in context_reports:
            if (
                isinstance(item, dict)
                and item.get("kind") == "runtime_tool_feedback_context"
                and removed < len(existing) - max_feedback_reports + 1
            ):
                removed += 1
                continue
            trimmed.append(item)
        context_reports[:] = trimmed

    context_reports.append(feedback)
    return True

def run_schema_repair_retry_for_round(
    *,
    manager: Any,
    model: str,
    args: argparse.Namespace,
    round_index: int,
    objective: str,
    raw_response: str,
    parsed_response: dict[str, Any],
    parse_diagnostics: dict[str, Any],
    context_reports: list[dict[str, Any]],
    rounds: list[dict[str, Any]],
    evidence_ready_for_manual_patch_count: int,
) -> dict[str, Any]:
    """Run one JSON-only schema repair pass for a bad provider response."""

    if not raw_response or not raw_response.strip():
        return {
            "attempted": False,
            "accepted": False,
            "reason": "empty_or_missing_raw_response",
        }

    valid_tool_count = int(parse_diagnostics.get("valid_tool_request_count") or 0)
    if not should_attempt_schema_repair_retry(
        parsed_response=parsed_response,
        parse_diagnostics=parse_diagnostics,
        evidence_ready_for_manual_patch_count=evidence_ready_for_manual_patch_count,
        valid_tool_request_count=valid_tool_count,
    ):
        return {"attempted": False, "accepted": False, "reason": "not_needed"}

    repair_prompt = build_schema_repair_retry_prompt(
        provider="gpu_ollama",
        round_index=round_index,
        objective=objective,
        raw_response=raw_response,
        parsed_response=parsed_response,
        parse_diagnostics=parse_diagnostics,
        context_reports=context_reports,
        rounds=rounds,
        evidence_ready_for_manual_patch_count=evidence_ready_for_manual_patch_count,
    )
    repair_max_tokens = min(max(int(getattr(args, "max_new_tokens", 1600) or 1600), 900), 2200)
    try:
        repair_raw_response, repair_model_used = manager.generate(
            model,
            repair_prompt,
            max_new_tokens=repair_max_tokens,
            temperature=0.03,
            num_thread=getattr(args, "ollama_num_thread", None),
            response_format="json",
        )
    except Exception as exc:  # noqa: BLE001 - provider repair is best-effort.
        return {
            "attempted": True,
            "accepted": False,
            "reason": "repair_provider_error",
            "error": f"{type(exc).__name__}: {exc}",
        }

    repair_parsed, repair_diagnostics = parse_model_json_with_diagnostics(
        repair_raw_response,
        evidence_ready_for_manual_patch_count,
    )
    repair_tool_requests, repair_tool_errors = extract_valid_tool_requests(
        repair_parsed,
        max_requests=getattr(args, "runtime_tool_max_requests_per_round", 8),
    )
    repair_diagnostics["valid_tool_request_count"] = len(repair_tool_requests)
    repair_diagnostics["invalid_tool_request_count"] = len(repair_tool_errors)
    repair_recommendation_diagnostics = recommendation_diagnostics_for_round(
        repair_parsed,
        repair_diagnostics,
        evidence_ready_for_manual_patch_count,
    )
    accepted = bool(
        repair_diagnostics.get("schema_ok")
        and (
            int(repair_recommendation_diagnostics.get("filtered_recommendation_count") or 0) > 0
            or len(repair_tool_requests) > 0
        )
    )
    return {
        "attempted": True,
        "accepted": accepted,
        "reason": ("schema_repair_retry_accepted" if accepted else "schema_repair_retry_rejected"),
        "model_used": repair_model_used,
        "raw_response_preview": repair_raw_response[:3000],
        "raw_response": repair_raw_response,
        "parsed_response": repair_parsed,
        "parse_diagnostics": repair_diagnostics,
        "tool_requests": repair_tool_requests,
        "tool_request_errors": repair_tool_errors,
        "recommendation_diagnostics": repair_recommendation_diagnostics,
    }

def run_runtime_tool_bootstrap(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    # Run deterministic broker bootstrap before the first GPU planner prompt.
    if not args.enable_runtime_tool_broker:
        return {
            "enabled": False,
            "executed": False,
            "bootstrap": True,
            "requested_tool_count": 0,
            "tool_results": [],
            "guardrails": {
                "bootstrap_requires_enable_runtime_tool_broker": True,
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }
    if args.disable_runtime_tool_bootstrap:
        return {
            "enabled": True,
            "executed": False,
            "bootstrap": True,
            "disabled": True,
            "requested_tool_count": 0,
            "tool_results": [],
            "guardrails": {
                "bootstrap_disabled_by_flag": True,
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }
    result = run_runtime_tool_broker_for_round(
        repo_root=repo_root,
        args=args,
        round_index=0,
        tool_requests=[dict(item) for item in DEFAULT_RUNTIME_TOOL_BOOTSTRAP_REQUESTS],
    )
    result["bootstrap"] = True
    result["bootstrap_tool_ids"] = [item["id"] for item in DEFAULT_RUNTIME_TOOL_BOOTSTRAP_REQUESTS]
    return result
