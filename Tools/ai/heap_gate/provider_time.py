"""Time counter contract for provider teamwork lanes."""

from __future__ import annotations

from typing import Any


def _int_value(value: Any, default: int, minimum: int = 0) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, parsed)


def build_provider_time_counter_contract(args: Any) -> dict[str, Any]:
    budget_minutes = _int_value(getattr(args, "budget_minutes", 0), 0)
    operator_timeout = _int_value(getattr(args, "timeout_seconds", 0), 0)
    budget_seconds = budget_minutes * 60 if budget_minutes > 0 else operator_timeout
    budget_seconds = max(1, budget_seconds)
    close_lead = max(1, budget_seconds // 5)
    soft_close = max(1, budget_seconds - close_lead)
    return {
        "kind": "provider_time_counter_contract",
        "budget_minutes": budget_minutes,
        "budget_counter_seconds": budget_seconds,
        "soft_close_after_seconds": soft_close,
        "soft_close_lead_seconds": close_lead,
        "counter_tick_seconds": max(1, budget_seconds // 20),
        "watchdog_timeout_seconds": 0,
        "watchdog_semantics": "disabled_for_started_provider_lanes",
        "operational_semantics": "budget_counter_with_coordinated_soft_close",
        "hard_block_on_budget_expiry": False,
        "lane_start_failure_policy": "abort_universe",
        "active_lane_failure_policy": "block_universe_but_join_active_lanes",
    }


def build_provider_lane_time_contracts(args: Any) -> dict[str, dict[str, Any]]:
    contract = build_provider_time_counter_contract(args)
    budget = int(contract["budget_counter_seconds"])
    npu_requested = _int_value(getattr(args, "npu_micro_timeout_seconds", budget), budget, minimum=1)
    return {
        "gpu1_planner": {**contract, "lane_watchdog_seconds": 0},
        "gpu0_peer": {**contract, "lane_watchdog_seconds": 0},
        "npu_micro_task_auditor": {
            **contract,
            "lane_watchdog_seconds": 0,
            "requested_npu_seconds": npu_requested,
        },
    }


def provider_time_counter_prompt_text(contract: dict[str, Any]) -> str:
    if not contract:
        return ""
    return "\n".join(
        [
            "TIME_COUNTER_CONTRACT:",
            f"- budget_counter_seconds={contract.get('budget_counter_seconds')}",
            f"- soft_close_after_seconds={contract.get('soft_close_after_seconds')}",
            f"- counter_tick_seconds={contract.get('counter_tick_seconds')}",
            "- The time input is a heap orchestration counter, not a lane truncation boundary.",
            "- Near soft_close_after_seconds, close coherently: emit HEAP_DELTA_PROPOSAL or EXIT_DECISION=NO_PATCHABLE_TARGET with pointers.",
            "- Do not wait silently for a process cutoff; persist previous/refines/resume pointers and the final decision state.",
            f"- watchdog_timeout_seconds={contract.get('watchdog_timeout_seconds')} means the provider lane collector does not hard-kill started lanes by elapsed time.",
        ]
    )
