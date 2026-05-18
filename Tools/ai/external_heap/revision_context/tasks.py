"""Revision task construction for GPU1/GPU0/NPU lanes."""

from __future__ import annotations

from typing import Any

from .applicability import (
    block_is_terminal_no_patchable_target,
    candidate_applicability_flags_from_block,
    candidate_block_concrete_enough,
    candidate_symbol_text_from_block,
    sanitize_revision_context_text,
)
from .common import REVISION_TASK_PREVIEW_CHARS, as_list, compact_text
from .symbols import extract_symbols, rejection_reasons

def no_patchable_target_preview(block: dict[str, Any], flags: list[str], preview_limit: int) -> str:
    previous_block_id = str(block.get("previous_block_id") or "")
    refines_block_id = str(block.get("refines_block_id") or "")
    resume_from_block_id = str(block.get("resume_from_block_id") or previous_block_id or "")
    reason = ", ".join(flags) if flags else "candidate_not_concrete_enough"
    text = (
        "# HEAP_DELTA_PROPOSAL\n"
        "EXIT_DECISION=NO_PATCHABLE_TARGET\n"
        "POINTER_ACTION=STAY_FORWARD\n"
        "CURRENT_POINTER:\n"
        f"- previous_block_id={previous_block_id}\n"
        f"- refines_block_id={refines_block_id}\n"
        f"- resume_from_block_id={resume_from_block_id}\n"
        "\n"
        "TARGET_FILES:\n"
        "- none_verified\n"
        "\n"
        "BLOCKED_NO_VERIFIED_TARGET_REASON:\n"
        f"- rejected candidate cannot be reused as operational input: {reason}\n"
        "- no verified/allowlisted repo-relative patch target is available from this block.\n"
        "\n"
        "PATCH_SKETCH:\n"
        "- omitted because emitting a diff without a verified target would create a fake patch.\n"
    )
    return compact_text(text, preview_limit)

def task_block_context(
    block: dict[str, Any], preview_limit: int = REVISION_TASK_PREVIEW_CHARS
) -> dict[str, Any]:
    candidate_flags = candidate_applicability_flags_from_block(block)
    raw_diagnostic_preview = compact_text(block.get("diagnostic_preview"), preview_limit)

    if candidate_flags:
        source_preview = no_patchable_target_preview(block, candidate_flags, preview_limit)
        candidate_preview = source_preview
        diagnostic_preview = sanitize_revision_context_text(raw_diagnostic_preview)
    else:
        source_preview = compact_text(block.get("preview"), preview_limit)
        candidate_preview = compact_text(block.get("candidate_response_preview"), preview_limit)
        diagnostic_preview = raw_diagnostic_preview

    return {
        "source_path": str(block.get("source_path") or ""),
        "markdown_path": str(block.get("markdown_path") or ""),
        "previous_block_id": str(block.get("previous_block_id") or ""),
        "next_block_id": str(block.get("next_block_id") or ""),
        "refines_block_id": str(block.get("refines_block_id") or ""),
        "block_quality_passed": block.get("quality_passed"),
        "block_accepted": block.get("accepted"),
        "preview_source": str(block.get("preview_source") or ""),
        "source_preview": source_preview,
        "candidate_response_preview": candidate_preview,
        "diagnostic_preview": diagnostic_preview,
        "rejected_candidate_preview_omitted": bool(candidate_flags),
        "rejected_candidate_preview_reason": (
            "candidate_not_concrete_enough" if candidate_flags else ""
        ),
        "candidate_response_available": bool(candidate_preview.strip()),
        "diagnostic_preview_available": bool(diagnostic_preview.strip()),
        "candidate_applicability_flags": candidate_flags,
        "candidate_concrete_enough": not candidate_flags,
    }

def build_gpu1_tasks(
    proposals: list[dict[str, Any]], composer: dict[str, Any]
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    previous_symbols: dict[str, set[str]] = {
        "imports": set(),
        "defs": set(),
        "classes": set(),
        "assignments": set(),
    }
    for block in proposals:
        block_id = str(block.get("block_id") or "")
        if block_is_terminal_no_patchable_target(block):
            continue
        symbol_text = candidate_symbol_text_from_block(block)
        concrete_candidate = candidate_block_concrete_enough(block)
        symbols = (
            extract_symbols(symbol_text)
            if concrete_candidate
            else {"imports": [], "defs": [], "classes": [], "assignments": []}
        )
        discovered: dict[str, list[str]] = {}
        for key, values in symbols.items():
            new_values = [value for value in values if value not in previous_symbols[key]]
            if new_values:
                discovered[key] = new_values
            previous_symbols[key].update(values)
        reasons = rejection_reasons(composer, block)
        if candidate_applicability_flags_from_block(block):
            reasons = [sanitize_revision_context_text(reason) for reason in reasons]
        if discovered and block.get("previous_block_id"):
            tasks.append(
                {
                    "task_id": f"gpu1_propagate_symbols_{block_id}",
                    "role": "gpu1_planner",
                    "task_type": "backpropagate_symbol_contract",
                    "source_block_id": block_id,
                    "target_block_id": block.get("previous_block_id"),
                    "resume_from_block_id": block_id,
                    "discovered_symbols": discovered,
                    "symbol_propagation_source_concrete": True,
                    "instruction": "Propaga import/variabili/classi/funzioni scoperte nel candidate_response_preview ai blocchi precedenti compatibili, poi riprendi dal source_block_id senza perdere il cursore forward.",
                    **task_block_context(block),
                }
            )
        if reasons:
            tasks.append(
                {
                    "task_id": f"gpu1_rewrite_rejected_{block_id}",
                    "role": "gpu1_planner",
                    "task_type": "rewrite_rejected_block",
                    "source_block_id": block_id,
                    "target_block_id": block_id,
                    "resume_from_block_id": block.get("resume_from_block_id")
                    or block.get("previous_block_id")
                    or block_id,
                    "rejection_reasons": reasons,
                    "symbol_propagation_skipped": not concrete_candidate,
                    "symbol_propagation_skip_reason": (
                        "candidate_not_concrete_enough" if not concrete_candidate else ""
                    ),
                    "instruction": "Riscrivi il blocco senza copiare candidate_response_preview se il blocco contiene invented_source_path, unresolved_pointer_placeholder, unresolved_angle_bracket_token, placeholder/stub o source refs non verificati. In quei casi tratta candidate_response_preview come esempio negativo/blacklist e usa diagnostic_preview solo per capire i motivi di rigetto. Genera una proposta nuova con soli source path repo-relative verificati/allowlisted; se nessun target e' verificabile, produci EXIT_DECISION=NO_PATCHABLE_TARGET con BLOCKED_NO_VERIFIED_TARGET_REASON, senza fake diff. Mantieni i pointer previous/next/refines/resume usando valori vuoti o block id reali; non usare placeholder <id-or-empty>.",
                    **task_block_context(block),
                }
            )
    return tasks

def build_peer_tasks(
    proposals: list[dict[str, Any]],
    gpu0: list[dict[str, Any]],
    npu: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    gpu0_available = bool(gpu0)
    npu_available = bool(npu)
    for block in proposals:
        block_id = str(block.get("block_id") or "")
        if block_is_terminal_no_patchable_target(block):
            continue
        if block.get("accepted") is True:
            continue
        if gpu0_available:
            tasks.append(
                {
                    "task_id": f"gpu0_parallel_recheck_{block_id}",
                    "role": "gpu0_reviewer_refiner",
                    "task_type": "parallel_recheck_old_pointer",
                    "target_block_id": block_id,
                    "can_edit_pointer": True,
                    "instruction": "Rivaluta il candidate_response_preview anche se il blocco non e' l'ultimo. Usa diagnostic_preview solo come diagnosi. Se candidate_applicability_flags non e' vuoto, proponi refines_block_id e resume_from_block_id per una riscrittura concreta.",
                    **task_block_context(block),
                }
            )
        if npu_available:
            tasks.append(
                {
                    "task_id": f"npu_parallel_audit_{block_id}",
                    "role": "npu_auditor",
                    "task_type": "parallel_guardrail_audit_old_pointer",
                    "target_block_id": block_id,
                    "can_edit_pointer": False,
                    "instruction": "Audita candidate_response_preview per placeholder/stub, path inventati, source writes non dichiarati, ripetizioni e candidate_applicability_flags. Usa diagnostic_preview come contesto secondario. Restituisci decisione accept/reject e motivi.",
                    **task_block_context(block),
                }
            )
    return tasks

def choose_resume_block(proposals: list[dict[str, Any]]) -> str:
    accepted = [block for block in proposals if block.get("accepted") is True]
    if accepted:
        return str(accepted[-1].get("block_id") or "")
    if proposals:
        latest = proposals[-1]
        return str(
            latest.get("resume_from_block_id")
            or latest.get("previous_block_id")
            or latest.get("block_id")
            or ""
        )
    return ""

def candidate_applicability_summary(tasks: list[dict[str, Any]]) -> dict[str, Any]:
    flag_counts: dict[str, int] = {}
    non_concrete_task_ids: list[str] = []
    concrete_task_ids: list[str] = []
    symbol_skipped_task_ids: list[str] = []
    for task in tasks:
        if task.get("task_type") != "rewrite_rejected_block":
            continue
        if task.get("candidate_concrete_enough") is True:
            concrete_task_ids.append(str(task.get("task_id") or ""))
        else:
            non_concrete_task_ids.append(str(task.get("task_id") or ""))
        if task.get("symbol_propagation_skipped") is True:
            symbol_skipped_task_ids.append(str(task.get("task_id") or ""))
        for flag in as_list(task.get("candidate_applicability_flags")):
            flag_text = str(flag)
            flag_counts[flag_text] = flag_counts.get(flag_text, 0) + 1
    return {
        "rewrite_task_count": len(non_concrete_task_ids) + len(concrete_task_ids),
        "non_concrete_candidate_task_count": len(non_concrete_task_ids),
        "concrete_candidate_task_count": len(concrete_task_ids),
        "symbol_propagation_skipped_task_count": len(symbol_skipped_task_ids),
        "flag_counts": dict(sorted(flag_counts.items())),
        "non_concrete_task_ids": non_concrete_task_ids,
        "symbol_propagation_skipped_task_ids": symbol_skipped_task_ids,
        "requires_concrete_rewrite": bool(non_concrete_task_ids),
        "priority_next_action": (
            "rewrite_non_concrete_candidates" if non_concrete_task_ids else "review_or_continue"
        ),
    }
