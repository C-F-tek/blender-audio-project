from __future__ import annotations

from typing import Any


def safe_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _bool_at(data: dict[str, Any], *path: str) -> bool:
    current: Any = data
    for key in path:
        current = safe_dict(current).get(key)
    return bool(current)


def build_telemetry_quality(loaded: dict[str, dict[str, Any]]) -> dict[str, Any]:
    runtime_usage = safe_dict(loaded.get("runtime_usage"))
    capability = safe_dict(loaded.get("runtime_capability"))
    run_summary = safe_dict(loaded.get("full_toolbox_telemetry"))
    provider_evidence = safe_dict(
        run_summary.get("provider_evidence") or runtime_usage.get("provider_evidence")
    )
    npu_final_review = safe_dict(
        provider_evidence.get("npu_final_review")
        or safe_dict(safe_dict(run_summary.get("gpu_npu")).get("npu_final_review"))
    )
    usage_summary = safe_dict(runtime_usage.get("summary"))
    tool_calls = safe_list(runtime_usage.get("tool_calls"))
    required = {
        "runtime_usage_seen": bool(runtime_usage),
        "runtime_capability_seen": bool(capability),
        "tool_call_entries_seen": bool(
            tool_calls or usage_summary.get("tool_call_entry_count")
        ),
        "provider_execution_observed": bool(
            provider_evidence.get("provider_execution_performed")
            or runtime_usage.get("provider_execution_performed")
            or run_summary.get("provider_execution_performed")
        ),
        "gpu1_primary_observed": bool(
            provider_evidence.get("gpu_provider_execution_performed")
            or _bool_at(run_summary, "guardrails", "gpu_provider_execution_performed")
        ),
        "gpu0_companion_observed": bool(
            provider_evidence.get("gpu0_peer_support_provider_execution_performed")
            or _bool_at(
                run_summary, "guardrails", "gpu0_peer_provider_execution_performed"
            )
        ),
        "npu_micro_or_tool_observed": bool(
            provider_evidence.get("npu_provider_execution_performed")
            or provider_evidence.get("npu_micro_tool_lane_performed")
            or _bool_at(run_summary, "guardrails", "npu_micro_non_blocking")
        ),
        "npu_final_review_observed": bool(
            npu_final_review.get("final_review_on_performant_lane")
            and npu_final_review.get("deterministic_validator_acceptance_required")
            and not npu_final_review.get("npu_self_check_only")
        ),
    }
    missing = [key for key, ok in required.items() if not ok]
    score = round(100.0 * (len(required) - len(missing)) / len(required), 2)
    return {
        "score": score,
        "required_signals": required,
        "missing_signals": missing,
        "tool_call_entry_count": usage_summary.get("tool_call_entry_count")
        or len(tool_calls),
        "executed_count": usage_summary.get("executed_count"),
        "failed_count": usage_summary.get("failed_count"),
        "blocked_count": usage_summary.get("blocked_count"),
        "provider_evidence": provider_evidence,
        "npu_final_review": npu_final_review,
    }


def build_evidence_coverage(
    loaded: dict[str, dict[str, Any]], input_status: dict[str, str]
) -> dict[str, Any]:
    expected = [
        "patch_quality",
        "decision_loop",
        "runtime_usage",
        "runtime_capability",
        "repository_consistency",
        "memory_bundle",
        "full_toolbox_telemetry",
        "github_evidence_bundle",
    ]
    coverage = {key: bool(loaded.get(key)) for key in expected}
    missing = [key for key in expected if not coverage[key]]
    score = round(100.0 * (len(expected) - len(missing)) / len(expected), 2)
    return {
        "score": score,
        "coverage": coverage,
        "missing_evidence": missing,
        "input_status": input_status,
    }


def build_success_cases(
    report: dict[str, Any], loaded: dict[str, dict[str, Any]]
) -> list[dict[str, Any]]:
    telemetry = safe_dict(report.get("telemetry_quality"))
    coverage = safe_dict(report.get("evidence_coverage"))
    patch_summary = safe_dict(report.get("patch_plan_summary"))
    runtime_usage = safe_dict(loaded.get("runtime_usage"))
    usage_summary = safe_dict(runtime_usage.get("summary"))
    npu_final_review = safe_dict(telemetry.get("npu_final_review"))
    return [
        {
            "case": "patch_notes_quality_product",
            "quality_gate_passed": report.get("quality_gate_passed"),
            "score": report.get("quality_score"),
            "telemetry_quality_score": telemetry.get("score"),
            "evidence_coverage_score": coverage.get("score"),
            "manual_review_required": report.get("manual_review_required"),
        },
        {
            "case": "patch_plan_quality_product",
            "quality_gate_passed": patch_summary.get("patch_quality_gate_passed"),
            "score": patch_summary.get("average_plan_score"),
            "patch_plan_count": patch_summary.get("patch_plan_count"),
        },
        {
            "case": "runtime_tool_broker",
            "tool_call_entry_count": usage_summary.get("tool_call_entry_count"),
            "executed_count": usage_summary.get("executed_count"),
            "failed_count": usage_summary.get("failed_count"),
            "blocked_count": usage_summary.get("blocked_count"),
            "telemetry_quality": safe_dict(usage_summary.get("telemetry_quality")),
        },
        {
            "case": "npu_final_review",
            "classification": npu_final_review.get("classification"),
            "npu_support_seen": npu_final_review.get("npu_support_seen"),
            "final_review_on_performant_lane": npu_final_review.get(
                "final_review_on_performant_lane"
            ),
            "reviewers": safe_list(npu_final_review.get("reviewers")),
            "deterministic_validator_acceptance_required": npu_final_review.get(
                "deterministic_validator_acceptance_required"
            ),
        },
    ]


def build_fallback_cases(
    report: dict[str, Any], loaded: dict[str, dict[str, Any]], min_quality_score: float
) -> list[dict[str, Any]]:
    cases: list[dict[str, Any]] = []
    runtime_usage = safe_dict(loaded.get("runtime_usage"))
    provider = safe_dict(
        safe_dict(report.get("telemetry_quality")).get("provider_evidence")
    )
    npu_final_review = safe_dict(
        safe_dict(report.get("telemetry_quality")).get("npu_final_review")
    )
    evidence_paths = (
        safe_dict(report.get("inputs")).get("paths")
        if isinstance(report.get("inputs"), dict)
        else {}
    )

    if report.get("quality_score", 0) < min_quality_score or not report.get(
        "quality_gate_passed"
    ):
        cases.append(
            {
                "fallback_type": "patch_notes_quality_gate_fallback",
                "trigger": "quality_gate_passed_false_or_score_below_threshold",
                "primary_lane": "patch_notes_quality_product",
                "fallback_lane": "manual_review_patch_notes_fallback",
                "provider_requested": runtime_usage.get("provider_execution_performed"),
                "provider_performed": runtime_usage.get("provider_execution_performed"),
                "recovered": bool(report.get("patch_notes")),
                "product_blocker": False,
                "evidence_paths": safe_dict(evidence_paths),
            }
        )

    npu_semantic = provider.get("npu_provider_execution_performed")
    npu_tool = provider.get("npu_micro_support_performed") or provider.get(
        "npu_micro_tool_lane_performed"
    )
    if npu_semantic is False and npu_tool:
        cases.append(
            {
                "fallback_type": "npu_provider_empty_or_timeout",
                "trigger": "npu_semantic_provider_not_confirmed_but_micro_tool_lane_recovered",
                "primary_lane": "npu_semantic_provider",
                "fallback_lane": "npu_brokered_tool_support",
                "provider_requested": True,
                "provider_performed": False,
                "recovered": True,
                "product_blocker": False,
                "evidence_paths": {
                    "runtime_usage": safe_dict(evidence_paths).get("runtime_usage"),
                    "full_toolbox_telemetry": safe_dict(evidence_paths).get(
                        "full_toolbox_telemetry"
                    ),
                },
            }
        )

    if npu_final_review and not npu_final_review.get("final_review_on_performant_lane"):
        cases.append(
            {
                "fallback_type": "npu_final_review_missing_gpu_peer",
                "trigger": npu_final_review.get("classification"),
                "primary_lane": "npu_final_state",
                "fallback_lane": "deterministic_validator_acceptance",
                "provider_requested": True,
                "provider_performed": provider.get("npu_provider_execution_performed"),
                "recovered": bool(
                    npu_final_review.get("deterministic_validator_acceptance_required")
                ),
                "product_blocker": bool(npu_final_review.get("product_blocker")),
                "evidence_paths": {
                    "full_toolbox_telemetry": safe_dict(evidence_paths).get(
                        "full_toolbox_telemetry"
                    ),
                },
            }
        )

    for reason in safe_list(provider.get("provider_degraded_reasons")):
        text = str(reason)
        if "GPU0" in text or "gpu0" in text or "COMPANION_MODEL_DIR" in text:
            cases.append(
                {
                    "fallback_type": "gpu0_semantic_companion_unconfigured",
                    "trigger": text[:500],
                    "primary_lane": "gpu0_openvino_semantic_companion",
                    "fallback_lane": "gpu0_numeric_static_tool_peer",
                    "provider_requested": True,
                    "provider_performed": provider.get(
                        "gpu0_peer_support_provider_execution_performed"
                    ),
                    "recovered": True,
                    "product_blocker": False,
                    "evidence_paths": {
                        "runtime_usage": safe_dict(evidence_paths).get("runtime_usage")
                    },
                }
            )
    return cases
