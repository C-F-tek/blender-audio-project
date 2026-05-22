"""Report assembly for external heap revision context."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from .applicability import terminal_no_patchable_target_summary
from .common import as_list, normalize_bool
from .symbols import latest_block, peer_blocks, proposal_blocks
from .tasks import (
    build_gpu1_tasks,
    build_peer_tasks,
    candidate_applicability_summary,
    choose_resume_block,
)


def _provider_evidence_blocks(pointer: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = []
    for block in as_list(pointer.get("blocks")):
        if not isinstance(block, dict):
            continue
        if str(block.get("block_type") or "") == "proposal_chunk":
            continue
        blocks.append(block)
    return blocks


def _latest_provider_block(pointer: dict[str, Any], role: str = "") -> dict[str, Any]:
    blocks = _provider_evidence_blocks(pointer)
    if role:
        blocks = [block for block in blocks if str(block.get("role") or "") == role]
    if not blocks:
        return {}
    return blocks[-1]


def _closure_provider_block(pointer: dict[str, Any]) -> dict[str, Any]:
    return (
        _latest_provider_block(pointer, "gpu1_planner")
        or _latest_provider_block(pointer, "gpu0_reviewer_refiner")
        or {}
    )


def _provider_recovery_tasks(
    pointer: dict[str, Any],
    linked_gpu0: list[dict[str, Any]],
    linked_npu: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    gpu1 = _latest_provider_block(pointer, "gpu1_planner")
    if not gpu1:
        return []
    source_id = str(gpu1.get("block_id") or "")
    tasks: list[dict[str, Any]] = [
        {
            "task_id": f"recover_missing_proposal_from_{source_id}",
            "role": "gpu1_planner",
            "task_type": "recover_missing_proposal_chunk",
            "source_block_id": source_id,
            "target_block_id": source_id,
            "resume_from_block_id": source_id,
            "first_turn_plan_allowed": True,
            "accepted_first_turn_output_types": [
                "PLAN_THEN_PROPOSAL",
                "HEAP_DELTA_PROPOSAL",
                "NO_PATCHABLE_TARGET",
            ],
            "plan_is_not_final_product": True,
            "instruction": (
                "Resume from the provider evidence block, consume startup chunks/memory/tool "
                "refs and emit a real HEAP_DELTA_PROPOSAL or NO_PATCHABLE_TARGET. The first "
                "turn may be PLAN_THEN_PROPOSAL only when it explains the complete steps needed "
                "before code, but that plan is evidence, not final product. Do not discard the "
                "full operator request and do not invent a code product."
            ),
        }
    ]
    for role, linked in (
        ("gpu0_reviewer_refiner", linked_gpu0),
        ("npu_auditor", linked_npu),
    ):
        for block in linked[:1]:
            block_id = str(block.get("block_id") or "")
            can_add_pointer_information = role == "gpu0_reviewer_refiner"
            tasks.append(
                {
                    "task_id": f"recheck_{role}_{block_id}",
                    "role": role,
                    "task_type": "peer_recheck_provider_failure",
                    "source_block_id": block_id,
                    "target_block_id": source_id,
                    "resume_from_block_id": source_id,
                    "can_add_pointer_information": can_add_pointer_information,
                    "pointer_update_scope": [
                        "previous_block_id",
                        "refines_block_id",
                        "resume_from_block_id",
                        "pointer_action",
                        "propagation_notes",
                        "script_or_text_delta_refs",
                    ]
                    if can_add_pointer_information
                    else [],
                    "return_to_main_block_id": source_id if can_add_pointer_information else "",
                    "restart_on_rejected_partial": True,
                    "rejected_partial_evidence_policy": (
                        "Attach the wrong/partial answer evidence to the pointer graph and "
                        "request a response typology change before GPU1 retries."
                    ),
                    "instruction": (
                        "Re-evaluate the GPU1 recovery block as the same heap consciousness. "
                        "GPU0 may add coherent pointer information, propagation notes or "
                        "script/text delta refs, then return to the main GPU1 block. Keep "
                        "refines/resume pointers and report operational vetoes."
                    ),
                }
            )
    return tasks


def build_report(
    pointer: dict[str, Any], composer: dict[str, Any], causality: dict[str, Any]
) -> dict[str, Any]:
    proposals = proposal_blocks(pointer)
    gpu0 = peer_blocks(pointer, "gpu0_reviewer_refiner")
    npu = peer_blocks(pointer, "npu_auditor")
    linked_gpu0 = [block for block in gpu0 if block.get("refines_block_id")]
    linked_npu = [block for block in npu if block.get("refines_block_id")]
    gpu1_tasks = build_gpu1_tasks(proposals, composer)
    peer_tasks = build_peer_tasks(proposals, linked_gpu0, linked_npu)
    provider_recovery_tasks = (
        [] if proposals else _provider_recovery_tasks(pointer, linked_gpu0, linked_npu)
    )
    all_tasks = gpu1_tasks + peer_tasks + provider_recovery_tasks
    candidate_summary = candidate_applicability_summary(all_tasks)
    if provider_recovery_tasks:
        candidate_summary = dict(candidate_summary)
        candidate_summary["requires_concrete_rewrite"] = False
        candidate_summary["priority_next_action"] = "recover_missing_proposal_chunk"
    terminal_no_patchable = terminal_no_patchable_target_summary(proposals)
    if terminal_no_patchable.get("all_proposals_terminal_no_patchable_target"):
        candidate_summary = dict(candidate_summary)
        candidate_summary["requires_concrete_rewrite"] = False
        candidate_summary["priority_next_action"] = "blocked_no_verified_target"
    latest = latest_block(proposals)
    latest_provider = _closure_provider_block(pointer)
    latest_id = str(latest.get("block_id") or latest_provider.get("block_id") or "")
    resume_block = choose_resume_block(proposals) or latest_id
    closure_owner_block = _latest_provider_block(pointer, "gpu1_planner")
    npu_sidecar_status = (
        "evidence_ready_non_closer" if npu else "missing_or_not_selected"
    )
    open_pointer_count = int(
        pointer.get("open_pointer_count_final") or pointer.get("open_pointer_count") or 0
    )
    pointer_limited = bool(pointer.get("max_blocks_applied"))
    source_run_was_fallback = (
        bool(composer.get("fallback_heap_report_used"))
        or str(composer.get("product_status") or "") == "blocked_with_reason"
        and not proposals
    )
    provider_rejections = as_list(pointer.get("provider_rejections"))
    provider_rejection_reasons = as_list(pointer.get("provider_rejection_reasons"))
    proposal_graph_operational = bool(
        proposals
        and linked_gpu0
        and linked_npu
        and normalize_bool(pointer.get("provider_execution_performed"))
        and normalize_bool(causality.get("causal_chain_passed"))
    )
    provider_graph_operational = bool(
        not proposals
        and normalize_bool(pointer.get("provider_execution_performed"))
        and int(pointer.get("edge_count") or 0) > 0
        and linked_gpu0
        and linked_npu
        and _latest_provider_block(pointer, "gpu1_planner")
    )
    operational_revision_context = proposal_graph_operational or provider_graph_operational
    warnings: list[str] = []
    if pointer_limited:
        warnings.append(
            "pointer manifest was limited by max_blocks; revision tasks are based on exposed blocks only"
        )
    if candidate_summary.get("requires_concrete_rewrite"):
        warnings.append(
            "non-concrete candidate proposals require rewrite before symbol propagation or product acceptance"
        )
    if provider_graph_operational and not proposals:
        warnings.append(
            "provider graph is resumable but produced no proposal chunk; GPU1 recovery task required"
        )
    elif provider_rejection_reasons:
        warnings.append(
            "provider graph is non-operational because provider work was rejected: "
            + ",".join(str(item) for item in provider_rejection_reasons)
        )
    elif not operational_revision_context:
        warnings.append(
            "revision context is non-operational: source run had no linked provider/pointer blocks"
        )
    return {
        "schema_version": 1,
        "kind": "external_heap_revision_context",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "protocol": "external_heap_revision_context_v1",
        "passed": True,
        "operational_revision_context": operational_revision_context,
        "proposal_graph_operational": proposal_graph_operational,
        "provider_graph_operational": provider_graph_operational,
        "source_run_was_fallback": source_run_was_fallback,
        "can_resume_universe": operational_revision_context or open_pointer_count > 0,
        "source_pointer_protocol": pointer.get("protocol"),
        "pointer_product_contract": pointer.get("pointer_product_contract"),
        "pointer_contract_role": pointer.get("pointer_contract_role"),
        "provider_execution_semantics": pointer.get("provider_execution_semantics"),
        "causal_chain_status": causality.get("causal_chain_status"),
        "causal_chain_passed": causality.get("causal_chain_passed"),
        "product_acceptance_status": causality.get("product_acceptance_status"),
        "product_acceptance_passed": causality.get("product_acceptance_passed"),
        "proposal_block_count": len(proposals),
        "source_block_count": pointer.get("source_block_count"),
        "pointer_block_count": pointer.get("block_count"),
        "pointer_max_blocks_applied": pointer_limited,
        "roles_present": pointer.get("roles_present"),
        "all_roles_present": pointer.get("all_roles_present", pointer.get("roles_present")),
        "provider_verified_count": pointer.get("provider_verified_count"),
        "provider_rejected_count": pointer.get("provider_rejected_count"),
        "provider_rejections": provider_rejections,
        "provider_rejection_reasons": provider_rejection_reasons,
        "gpu0_block_count": len(gpu0),
        "npu_block_count": len(npu),
        "linked_gpu0_block_count": len(linked_gpu0),
        "linked_npu_block_count": len(linked_npu),
        "closure_owner": "gpu1_planner",
        "closure_owner_block_id": str(closure_owner_block.get("block_id") or ""),
        "npu_sidecar_status": npu_sidecar_status,
        "npu_is_primary_closer": False,
        "soft_lock_closure_owner_decision": pointer.get(
            "soft_lock_closure_owner_decision", ""
        ),
        "gpu0_closure_agreement": pointer.get("gpu0_closure_agreement", ""),
        "npu_closure_advisory": pointer.get(
            "npu_closure_advisory", npu_sidecar_status
        ),
        "cpu_closure_validation": pointer.get("cpu_closure_validation", ""),
        "closure_quorum_status": pointer.get("closure_quorum_status", ""),
        "closure_quorum_reason": pointer.get("closure_quorum_reason", ""),
        "soft_lock_targeted_refine_used": pointer.get(
            "soft_lock_targeted_refine_used", False
        ),
        "soft_lock_state": (
            "closed" if open_pointer_count == 0 else "closing_open_pointers"
        ),
        "open_pointer_count_final": open_pointer_count,
        "pointer_closure_table": pointer.get("pointer_closure_table", []),
        "resume_from_block_id": resume_block,
        "latest_block_id": latest_id,
        "parallel_task_count": len(all_tasks),
        "gpu1_task_count": len(gpu1_tasks),
        "provider_recovery_task_count": len(provider_recovery_tasks),
        "gpu0_task_count": len(
            [task for task in peer_tasks if task.get("role") == "gpu0_reviewer_refiner"]
        ),
        "npu_task_count": len([task for task in peer_tasks if task.get("role") == "npu_auditor"]),
        "candidate_applicability_summary": candidate_summary,
        "terminal_no_patchable_target": terminal_no_patchable.get(
            "all_proposals_terminal_no_patchable_target"
        ),
        "terminal_no_patchable_target_count": terminal_no_patchable.get("count"),
        "terminal_no_patchable_target_block_ids": terminal_no_patchable.get("block_ids"),
        "requires_concrete_rewrite": candidate_summary.get("requires_concrete_rewrite"),
        "priority_next_action": candidate_summary.get("priority_next_action"),
        "tasks": all_tasks,
        "runtime_instruction": (
            "GPU1 puo' avanzare o tornare indietro sui pointer. Se scopre un import, variabile, classe o contratto "
            "necessario, deve generare un task di propagazione sui blocchi precedenti, far rivalutare in parallelo GPU0/NPU, "
            "poi riprendere dal resume_from_block_id mantenendo la catena next/previous/refines. Se requires_concrete_rewrite=true, "
            "prima deve riscrivere i candidati non concreti e non propagare simboli da sketch o stub. "
            "GPU0 puo' aggiungere informazioni coerenti ai pointer, proporre salti di propagazione per testo/script/modifiche "
            "e poi tornare al blocco principale. Se una risposta parziale viene bocciata, il ciclo riparte con evidenza "
            "della risposta sbagliata e richiesta esplicita di cambiare tipologia. Il primo giro GPU1 puo' essere PLAN_THEN_PROPOSAL "
            "quando serve spiegare i passi completi, ma resta evidenza e non prodotto. "
            "La riscrittura deve usare solo source path repo-relative verificati/allowlisted; se il target non e' verificabile, "
            "deve produrre EXIT_DECISION=NO_PATCHABLE_TARGET invece di inventare path. Non usare placeholder <id-or-empty>."
        ),
        "provider_execution_performed": normalize_bool(pointer.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": warnings,
    }
