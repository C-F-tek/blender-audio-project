#!/usr/bin/env python3
"""Provider hierarchy section helpers for final heap readable products."""

from __future__ import annotations

from typing import Any


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _device_identity_map_text(items: list[Any]) -> str:
    parts: list[str] = []
    for raw in items:
        item = _as_dict(raw)
        lane = str(item.get("logical_lane") or "")
        if not lane:
            continue
        backend = str(item.get("provider_backend_device_id") or item.get("provider_compute_device") or "")
        windows = str(item.get("windows_task_manager_device_hint") or "")
        vulkan = str(item.get("vulkan_visible_device") or "")
        name = str(item.get("vulkan_device_name") or "")
        detail = f"{lane}->{backend}"
        if vulkan or name:
            detail += f"->Vulkan {vulkan} {name}".rstrip()
        if windows:
            detail += f"->{windows}"
        detail += f" verified={item.get('device_identity_verified')}"
        parts.append(detail)
    return "; ".join(parts)


def provider_hierarchy_summary(metrics: dict[str, Any]) -> list[str]:
    lane_tiers = _as_dict(metrics.get("lane_tiers"))
    authority = _as_dict(metrics.get("lane_authority"))
    lane_budgets = _as_dict(metrics.get("lane_context_budgets"))
    consumed = _as_list(metrics.get("consumed_peer_block_ids"))
    device_map = _as_list(metrics.get("device_identity_map"))

    def budget(lane: str) -> str:
        data = _as_dict(lane_budgets.get(lane))
        if data.get("ollama_num_ctx"):
            return f"ctx={data.get('ollama_num_ctx')}, max_new_tokens={data.get('max_new_tokens')} source={data.get('max_new_tokens_source') or 'unknown'} override={data.get('max_new_tokens_override_path') or 'unknown'}"
        if data.get("max_prompt_chars"):
            return f"prompt_chars={data.get('max_prompt_chars')}, context_chars={data.get('max_context_chars')}, max_new_tokens={data.get('max_new_tokens')} source={data.get('max_new_tokens_source') or 'unknown'} override={data.get('max_new_tokens_override_path') or 'unknown'}"
        return ""

    return [
        f"Context budget hierarchy valid: `{metrics.get('context_hierarchy_valid')}`; scope=`{metrics.get('context_hierarchy_scope') or 'budget_only_not_workload_or_leadership'}`; operator effective config: `{metrics.get('operator_effective_provider_config') or {}}`.",
        f"GPU1/NVIDIA identity: `{metrics.get('gpu1_lane_identity') or 'GPU1/NVIDIA primary Ollama lane'}`.",
        f"GPU1 replight health/residency only: `{metrics.get('gpu1_replight_valid')}`; scope=`{metrics.get('gpu1_replight_scope') or 'health_residency_only'}`; mai leadership/prodotto.",
        f"GPU1 boot leader ready: `{metrics.get('gpu1_boot_leader_ready')}`; autorizza solo avvio sidecar.",
        f"GPU1 primary workload: `{metrics.get('gpu1_primary_workload_valid')}`; chars=`{metrics.get('gpu1_primary_workload_chars')}`, tokens=`{metrics.get('gpu1_primary_workload_tokens')}`.",
        f"GPU1 primary evidence: `{metrics.get('gpu1_primary_evidence_valid')}`; source=`{metrics.get('gpu1_primary_evidence_source')}`; leader_source=`{metrics.get('leader_source')}`; gpu1_native_tool_call_count=`{metrics.get('gpu1_native_tool_call_count')}`.",
        f"Parallel provider overlap / sidecar scope mode: `{metrics.get('sidecar_scope_mode')}`; start policy=`{metrics.get('sidecars_start_policy')}`; overlap=`{metrics.get('parallel_provider_overlap_seconds')}`; gpu1_idle_after_primary_seconds=`{metrics.get('gpu1_idle_after_primary_seconds')}`; sidecar_alone_after_gpu1_seconds=`{metrics.get('sidecar_alone_after_gpu1_seconds')}`.",
        f"GPU1 recovery/congruence: attempted=`{metrics.get('gpu1_recovery_attempted') or metrics.get('provider_recovery_attempted')}`; congruence_check=`{metrics.get('gpu1_congruence_check_performed')}`; sidecar_invalid=`{metrics.get('sidecar_invalid')}`; sidecar_incongruent=`{metrics.get('sidecar_incongruent')}`.",
        f"GPU1 leader valid: `{metrics.get('gpu1_leader_valid')}`; leader block id: `{metrics.get('gpu1_leader_block_id')}`.",
        f"GPU1/NVIDIA: lane_tier=`{lane_tiers.get('gpu1_planner') or 'primary'}`, authority=`{authority.get('gpu1_planner') or 'leader'}`, closure_owner=`gpu1_planner`, context_budget=`{budget('gpu1_planner')}`.",
        f"GPU0/Vulkan: lane_tier=`{lane_tiers.get('gpu0_peer') or 'coworker_medium'}`, authority=`{authority.get('gpu0_peer') or 'coworker'}`, closure_owner=`gpu1_planner`, context_budget=`{budget('gpu0_peer')}`.",
        f"NPU/OpenVINO: lane_tier=`{lane_tiers.get('npu_micro_task_auditor') or 'micro_fast'}`, authority=`{authority.get('npu_micro_task_auditor') or 'micro_tool'}`, closure_owner=`gpu1_planner`, context_budget=`{budget('npu_micro_task_auditor')}`.",
        f"Consumed peer block ids: `{consumed}`; roles observed/verified/invalid: `{metrics.get('roles_observed') or []}` / `{metrics.get('roles_verified') or []}` / `{metrics.get('roles_observed_invalid') or []}`.",
        f"GPU1 consumed GPU0 peer: `{metrics.get('gpu1_consumed_gpu0_peer')}`; GPU1 consumed NPU peer: `{metrics.get('gpu1_consumed_npu_peer')}`.",
        f"GPU1 consumed generic_write block ids: `{metrics.get('gpu1_consumed_generic_write_block_ids') or []}`.",
        "Device identity map: `" + _device_identity_map_text(device_map) + "`.",
        "Regola: GPU0 puo' produrre testo migliore o piu lungo, ma resta coworker_medium; non diventa primary e non chiude senza consumo GPU1.",
    ]
