"""Dry-run policy fields for the canonical ia_carmine run preview."""

from __future__ import annotations

from typing import Any


def dry_run_contract_policy(
    *,
    gpu1_base_url: str | None,
    gpu0_base_url: str | None,
    keep_alive: str | None,
    field_sources: dict[str, str] | None = None,
) -> dict[str, Any]:
    sources = field_sources or {}

    def source_for(*fields: str) -> str:
        values = [
            str(sources.get(field) or "").strip()
            for field in fields
            if str(sources.get(field) or "").strip()
            and str(sources.get(field) or "").strip() != "optional_unset"
        ]
        unique = sorted(set(values))
        if not unique:
            return "unknown"
        if len(unique) == 1:
            return unique[0]
        return "mixed:" + ",".join(unique)

    return {
        "provider_role_policy": {
            "closure_owner": "gpu1_planner",
            "gpu0_peer": "reviewer_refiner_not_primary_closer",
            "npu_micro_task_auditor": "micro_audit_only_not_primary_closer",
        },
        "provider_parallel_policy": {
            "provider_boot_gate": "gpu1_gpu0_npu_alive_in_same_window_before_replight_or_pointer_loop",
            "gpu1_start": "brief_ollama_gpu_residency_handshake_after_boot_gate",
            "gpu0_npu_start": "parallel_after_gpu1_residency_proven",
            "gpu1_wait_for_full_completion_before_sidecars": False,
        },
        "provider_replight_required": True,
        "provider_replight_policy": {
            "required_lanes": ["gpu1_planner"],
            "required_fields": [
                "provider_model",
                "provider_loaded",
                "generated_phrase",
                "prompt_token_count",
                "completion_token_count",
                "available_tool_names",
                "functionalities",
                "replight_passed",
            ],
            "failure_exit": "blocked_with_reason",
            "failure_product_kind": "blocked_continuation_product",
            "cpu_provider_fallback_allowed": False,
        },
        "provider_boot_gate_policy": {
            "required_lanes": ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
            "gpu1": {
                "backend": "ollama",
                "base_url": gpu1_base_url,
                "keep_alive": keep_alive,
                "source": source_for("gpu1_base_url", "keep_alive"),
                "config_sources": {
                    "base_url": source_for("gpu1_base_url"),
                    "keep_alive": source_for("keep_alive"),
                },
            },
            "gpu0": {
                "backend": "ollama_vulkan",
                "base_url": gpu0_base_url,
                "keep_alive": keep_alive,
                "source": source_for("gpu0_base_url", "gpu0_model", "keep_alive"),
                "config_sources": {
                    "base_url": source_for("gpu0_base_url"),
                    "model": source_for("gpu0_model"),
                    "keep_alive": source_for("keep_alive"),
                },
            },
            "npu": {
                "backend": "openvino_NPU",
                "source": source_for(
                    "npu_model_dir",
                    "npu_micro_start_mode",
                    "allow_npu_device_workload",
                ),
                "config_sources": {
                    "model_dir": source_for("npu_model_dir"),
                    "start_mode": source_for("npu_micro_start_mode"),
                    "device_workload": source_for("allow_npu_device_workload"),
                },
            },
            "workload_verified_at_boot": False,
            "failure_exit": "provider_boot_gate_failed",
        },
        "soft_lock_closure_quorum_policy": {
            "gpu1_closure_owner": True,
            "gpu0_required_for_close": True,
            "npu_closure_role": "advisory_only",
            "exit_rule": (
                "GPU1 no_more_action/blocked_continuation plus GPU0 agree_close "
                "closes automatically; GPU0 veto allows one targeted GPU1 refine"
            ),
        },
        "gpu1_closure_owner": True,
        "gpu0_required_for_close": True,
        "npu_closure_role": "advisory_only",
        "native_tool_calling_policy": {
            "gpu1_planner": "open_revision_drive_broker_tools_and_own_final_synthesis",
            "gpu0_peer": "same_tool_schema_peer_only_refinement_veto_evidence_requires_later_gpu1_consumption",
            "npu_micro_task_auditor": "micro_audit_native_tools_diagnostic_only",
        },
        "soft_lock_policy": {
            "soft_lock_state": "closing_open_pointers",
            "new_broad_exploration_allowed": False,
            "extensions_until": "open_pointer_count_zero_or_unresolvable_blocker",
            "soft_lock_closure_quorum_policy": {
                "gpu1_closure_owner": True,
                "gpu0_required_for_close": True,
                "npu_closure_role": "advisory_only",
                "valid_gpu1_decisions": [
                    "finalize_product",
                    "blocked_continuation",
                    "no_more_action",
                    "needs_gpu0_refine",
                ],
                "valid_gpu0_decisions": [
                    "agree_close",
                    "veto_with_reason",
                    "refine_once",
                ],
                "valid_quorum_statuses": [
                    "ready_to_close",
                    "targeted_refine_allowed",
                    "blocked_continuation_ready",
                    "blocked_with_reason",
                ],
            },
            "required_pointer_closure_statuses": [
                "merged_into_final_product",
                "rejected_with_reason",
                "superseded_by_pointer",
                "deferred_to_resume",
                "blocked_external_dependency",
                "requires_operator_input",
            ],
        },
        "delta_context_mode": "startup_full_once_then_pointer_delta_revisions",
        "required_provider_roles": ["gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor"],
    }
