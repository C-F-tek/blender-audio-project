"""Time counter contract for provider teamwork lanes."""

from __future__ import annotations

from typing import Any

from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import (
    CLOSURE_OWNER,
    GPU0_LANE,
    GPU1_LANE,
    NPU_LANE,
    lane_hierarchy,
)


def _int_value(value: Any, default: int, minimum: int = 0) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        parsed = default
    return max(minimum, parsed)


def _bounded_seconds(value: int, minimum: int, maximum: int) -> int:
    return max(minimum, min(maximum, int(value)))


def _soft_close_for_budget(seconds: int) -> int:
    lead = max(1, min(10, int(seconds) // 4))
    return max(1, int(seconds) - lead)


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
        "early_exit_when_product_ready_with_evidence": True,
        "soft_close_is_finalization_signal_only": True,
        "soft_close_must_not_truncate_pointer_recursion": True,
        "soft_lock_state_on_soft_close": "closing_open_pointers",
        "soft_lock_forbids_new_broad_exploration": True,
        "soft_lock_requires_explicit_pointer_closure": True,
        "provider_residency_lifecycle": "keep_gpu1_gpu0_loaded_across_provider_revisions_until_production_cycle_cleanup",
        "memory_release_policy": "per_revision_release_only_for_finished_child_processes; ollama_model_unload_only_at_provider_production_cycle_cleanup",
        "lane_start_failure_policy": "abort_universe",
        "active_lane_failure_policy": "block_universe_but_join_active_lanes",
        "closure_owner": CLOSURE_OWNER,
        "sidecar_lanes": [GPU0_LANE, NPU_LANE],
    }


def build_provider_lane_time_contracts(args: Any) -> dict[str, dict[str, Any]]:
    contract = build_provider_time_counter_contract(args)
    budget = int(contract["budget_counter_seconds"])
    npu_requested = _int_value(getattr(args, "npu_micro_timeout_seconds", budget), budget, minimum=1)
    npu_budget = _bounded_seconds(npu_requested, 5, max(5, min(90, budget)))
    gpu0_budget = _bounded_seconds(budget // 4, 20, max(20, min(90, budget)))
    gpu0_tool_timeout = _bounded_seconds(gpu0_budget // 2, 8, gpu0_budget)
    npu_tool_timeout = _bounded_seconds(npu_budget // 2, 5, npu_budget)
    gpu0_derived_config = [
        {
            "field": "gpu0.sidecar_budget_seconds",
            "effective_value": gpu0_budget,
            "source": "derived_from_budget_counter_seconds",
            "reason": "GPU0 sidecar watchdog is a bounded review budget, not an operator truncation knob.",
        },
        {
            "field": "gpu0.native_tool_timeout_seconds",
            "effective_value": gpu0_tool_timeout,
            "source": "derived_from_gpu0_sidecar_budget_seconds",
            "reason": "Native tool timeout follows the sidecar packet-review budget.",
        },
    ]
    npu_derived_config = [
        {
            "field": "npu.sidecar_budget_seconds",
            "effective_value": npu_budget,
            "source": "npu_micro_timeout_seconds_bounded_by_run_budget",
            "requested_value": npu_requested,
        },
        {
            "field": "npu.native_tool_timeout_seconds",
            "effective_value": npu_tool_timeout,
            "source": "derived_from_npu_sidecar_budget_seconds",
        },
    ]
    return {
        GPU1_LANE: {
            **contract,
            **lane_hierarchy(GPU1_LANE),
            "lane": GPU1_LANE,
            "lane_authority": "primary_open_review_close_synthesis",
            "lane_is_closure_owner": True,
            "primary_closer": True,
            "sidecar_lane": False,
            "lane_watchdog_seconds": 0,
            "timeout_seconds": 0,
            "native_tool_calling_policy": "gpu1_may_drive_broker_native_tool_calls_and_own_final_synthesis",
            "delta_context_mode": "full_startup_then_pointer_delta_revisions",
        },
        GPU0_LANE: {
            **contract,
            **lane_hierarchy(GPU0_LANE),
            "lane": GPU0_LANE,
            "budget_counter_seconds": gpu0_budget,
            "soft_close_after_seconds": _soft_close_for_budget(gpu0_budget),
            "soft_close_lead_seconds": max(1, gpu0_budget - _soft_close_for_budget(gpu0_budget)),
            "counter_tick_seconds": max(1, gpu0_budget // 10),
            "watchdog_timeout_seconds": gpu0_budget,
            "watchdog_semantics": "bounded_sidecar_watchdog_independent_of_primary",
            "lane_watchdog_seconds": gpu0_budget,
            "timeout_seconds": gpu0_budget,
            "native_tool_timeout_seconds": gpu0_tool_timeout,
            "sidecar_join_after_primary_seconds": 0,
            "lane_authority": "coworker_reviewer_refiner_not_primary_closer",
            "lane_is_closure_owner": False,
            "primary_closer": False,
            "sidecar_lane": True,
            "reviewer_refiner": True,
            "native_tool_calling_policy": "gpu0_same_schema_peer_only_requires_later_gpu1_consumption",
            "delta_context_mode": "pointer_delta_review",
            "started_lane_hard_kill_allowed": True,
            "derived_config": gpu0_derived_config,
        },
        NPU_LANE: {
            **contract,
            **lane_hierarchy(NPU_LANE),
            "lane": NPU_LANE,
            "budget_counter_seconds": npu_budget,
            "soft_close_after_seconds": _soft_close_for_budget(npu_budget),
            "soft_close_lead_seconds": max(1, npu_budget - _soft_close_for_budget(npu_budget)),
            "counter_tick_seconds": max(1, npu_budget // 10),
            "watchdog_timeout_seconds": npu_budget,
            "watchdog_semantics": "hard_micro_watchdog_from_npu_micro_timeout_seconds_independent_of_primary",
            "lane_watchdog_seconds": npu_budget,
            "timeout_seconds": npu_budget,
            "native_tool_timeout_seconds": npu_tool_timeout,
            "sidecar_join_after_primary_seconds": 0,
            "requested_npu_seconds": npu_requested,
            "npu_micro_timeout_enforced": True,
            "lane_authority": "microtask_tool_auditor_not_primary_closer",
            "lane_is_closure_owner": False,
            "primary_closer": False,
            "sidecar_lane": True,
            "micro_audit_only": True,
            "native_tool_calling_policy": "npu_may_call_native_tools_only_for_diagnostic_micro_audit",
            "delta_context_mode": "pointer_delta_micro_audit",
            "started_lane_hard_kill_allowed": True,
            "derived_config": npu_derived_config,
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
            "- GPU1/GPU0 Ollama residency stays alive across provider revisions so lanes can call back into each other.",
            "- Release short-lived child processes at lane boundaries when useful; unload Ollama models only at production-cycle provider cleanup.",
            "- If the pointer universe reaches a ready product with evidence before soft_close_after_seconds, exit through product_signal immediately.",
            "- Near soft_close_after_seconds, close coherently: emit HEAP_DELTA_PROPOSAL or EXIT_DECISION=NO_PATCHABLE_TARGET with pointers.",
            "- Soft close is not permission to truncate pointer recursion; continue propagation/refinement unless the heap has ready evidence or an explicit blocked reason.",
            "- At soft close enter SOFT_LOCK_STATE=closing_open_pointers: do not start broad exploration; close, merge, veto, refine, classify, or defer existing pointers.",
            "- Every open pointer must become merged_into_final_product, rejected_with_reason, superseded_by_pointer, deferred_to_resume, blocked_external_dependency, or requires_operator_input.",
            "- A unique run is not a one-way script row: it may BACKTRACK_PROPAGATE, let GPU0/NPU recheck old pointers, then RESUME_FORWARD.",
            "- Do not wait silently for a process cutoff; persist previous/refines/resume pointers and the final decision state.",
            f"- base watchdog_timeout_seconds={contract.get('watchdog_timeout_seconds')} applies to GPU1; lane_time_contracts define bounded GPU0/NPU sidecar watchdogs.",
            f"- closure_owner={contract.get('closure_owner')}; sidecar_lanes={contract.get('sidecar_lanes')}.",
        ]
    )
