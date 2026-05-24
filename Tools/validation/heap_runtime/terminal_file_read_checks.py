"""Terminal invariant fixtures for code-delta file-read evidence."""

from __future__ import annotations

from typing import Any, Callable


def run_file_read_terminal_fixtures(
    ready_metrics: Callable[[], dict[str, Any]],
    evaluate_terminal_invariants: Callable[..., list[str]],
) -> dict[str, list[str]]:
    code_delta_without_file_read = ready_metrics()
    code_delta_without_file_read["latest_final_product_file_read_verified"] = False
    code_delta_without_file_read["latest_final_product_file_read_refs"] = []
    code_delta_without_file_read["latest_final_product_file_read_errors"] = [
        "gpu1_code_delta_without_file_read"
    ]
    code_delta_without_file_read["latest_final_product_file_read_result_count"] = 0
    code_delta_without_file_read["latest_final_product_consumed_file_read_result_count"] = 0
    code_errors = evaluate_terminal_invariants(
        metrics=code_delta_without_file_read,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    text_only_without_file_read = ready_metrics()
    text_only_without_file_read["latest_final_product_kind"] = "text"
    text_only_without_file_read["latest_final_product_requires_file_read"] = False
    text_only_without_file_read["latest_final_product_file_read_verified"] = False
    text_only_without_file_read["latest_final_product_file_read_refs"] = []
    text_only_without_file_read["latest_final_product_file_read_result_count"] = 0
    text_only_without_file_read["latest_final_product_consumed_file_read_result_count"] = 0
    text_only_without_file_read["latest_final_product_diff_present"] = False
    text_errors = evaluate_terminal_invariants(
        metrics=text_only_without_file_read,
        missing_requirements=[],
        lane_gate_passed=True,
        degraded_lanes=[],
        final_bridge_reports=["output/validation/broker.json"],
        allow_provider_generation=True,
        provider_execution_performed=True,
        detailed_output_expected=True,
    )
    return {
        "code_delta_without_file_read_errors": code_errors,
        "text_only_without_file_read_errors": text_errors,
    }
