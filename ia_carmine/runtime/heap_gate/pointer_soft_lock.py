"""Pointer closure and elastic soft-lock helpers for run-unica."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.pointer_closure_quorum import (
    GPU0_CLOSURE_AGREEMENTS,
    GPU1_CLOSURE_DECISIONS,
    QUORUM_STATUSES,
    closure_quorum_state,
    gpu1_closure_decision_from_text,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, read_json

POINTER_CLOSURE_STATUSES = {
    "merged_into_final_product",
    "rejected_with_reason",
    "superseded_by_pointer",
    "deferred_to_resume",
    "blocked_external_dependency",
    "requires_operator_input",
    "open",
}
PEER_POINTER_ROLES = {"gpu0_reviewer_refiner", "npu_auditor"}

def pointer_closure_table(
    blocks: list[dict[str, Any]],
    *,
    semantic_defer_open: bool = False,
    resume_from_block_id: str = "",
    closure_evidence_block_id: str = "",
) -> list[dict[str, Any]]:
    return [
        _closure_entry(
            block,
            blocks,
            semantic_defer_open=semantic_defer_open,
            resume_from_block_id=resume_from_block_id,
            closure_evidence_block_id=closure_evidence_block_id,
        )
        for block in blocks
        if str(block.get("id") or block.get("block_id") or "")
    ]


def pointer_closure_summary(
    blocks: list[dict[str, Any]],
    *,
    semantic_defer_open: bool = False,
    resume_from_block_id: str = "",
    closure_evidence_block_id: str = "",
) -> dict[str, Any]:
    table = pointer_closure_table(
        blocks,
        semantic_defer_open=semantic_defer_open,
        resume_from_block_id=resume_from_block_id,
        closure_evidence_block_id=closure_evidence_block_id,
    )
    open_rows = [row for row in table if row.get("closure_status") == "open"]
    return {
        "pointer_closure_table": table,
        "open_pointer_count": len(open_rows),
        "open_pointer_count_final": len(open_rows),
        "all_pointers_closed": not open_rows,
        "soft_lock_state": "closed" if not open_rows else "closing_open_pointers",
    }


def runtime_soft_lock_state(owner: Any, events: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    blocks = _runtime_pointer_blocks(owner)
    raw_summary = pointer_closure_summary(blocks)
    quorum = closure_quorum_state(owner, events, raw_summary=raw_summary)
    semantic_defer_open = quorum.get("closure_quorum_status") == "blocked_continuation_ready"
    summary = pointer_closure_summary(
        blocks,
        semantic_defer_open=semantic_defer_open,
        resume_from_block_id=str(quorum.get("resume_from_block_id") or ""),
        closure_evidence_block_id=str(quorum.get("closure_evidence_block_id") or ""),
    )
    extension_count = int(getattr(owner, "soft_lock_extension_count", 0) or 0)
    before = getattr(owner, "open_pointer_count_before_soft_lock", None)
    after = list(getattr(owner, "open_pointer_count_after_each_extension", []) or [])
    if before is None:
        before = summary["open_pointer_count_final"]
    return {
        "soft_lock_state": (
            "closing_open_pointers"
            if extension_count
            or raw_summary["open_pointer_count_final"]
            or quorum.get("closure_quorum_status")
            else "not_entered"
        ),
        "soft_lock_issued": bool(
            extension_count
            or raw_summary["open_pointer_count_final"]
            or quorum.get("closure_quorum_status")
        ),
        "soft_lock_extension_count": extension_count,
        "open_pointer_count_before_soft_lock": before,
        "open_pointer_count_after_each_extension": after,
        "open_pointer_count_raw": raw_summary["open_pointer_count_final"],
        "open_pointer_count_final": summary["open_pointer_count_final"],
        "pointer_closure_table": summary["pointer_closure_table"],
        **quorum,
    }


def register_soft_lock_extension(owner: Any) -> dict[str, Any]:
    state = runtime_soft_lock_state(owner)
    if not hasattr(owner, "soft_lock_extension_count"):
        owner.soft_lock_extension_count = 0
    if getattr(owner, "open_pointer_count_before_soft_lock", None) is None:
        owner.open_pointer_count_before_soft_lock = state["open_pointer_count_final"]
    owner.soft_lock_extension_count = int(owner.soft_lock_extension_count or 0) + 1
    after = list(getattr(owner, "open_pointer_count_after_each_extension", []) or [])
    after.append(state["open_pointer_count_final"])
    owner.open_pointer_count_after_each_extension = after
    return runtime_soft_lock_state(owner)


def soft_lock_feedback_text(state: dict[str, Any]) -> str:
    return "\n".join(
        [
            "SOFT_LOCK_STATE=closing_open_pointers",
            f"OPEN_POINTER_COUNT={state.get('open_pointer_count_final', 0)}",
            "The soft lock is an elastic finalization phase, not permission to truncate.",
            "Do not start broad exploration. Close only existing pointers by merge, veto, refine, classify, or resume decision.",
            "GPU1 is the closure owner. GPU0 reviews/refines. NPU may only micro-audit specific risks.",
            "Every pointer must end as merged_into_final_product, rejected_with_reason, superseded_by_pointer, deferred_to_resume, blocked_external_dependency, or requires_operator_input.",
        ]
    )


def render_pointer_closure_markdown_lines(state: dict[str, Any]) -> list[str]:
    rows = list(state.get("pointer_closure_table") or [])
    lines = [
        "## Pointer closure",
        "",
        f"- Soft lock state: `{state.get('soft_lock_state', '')}`.",
        f"- Soft lock extensions: `{state.get('soft_lock_extension_count', 0)}`.",
        f"- Open pointer count final: `{state.get('open_pointer_count_final', 0)}`.",
        "",
        "| pointer_id | source_role | closure_status | closure_owner | evidence | included | resume_from |",
        "|---|---|---|---|---|---|---|",
    ]
    if not rows:
        lines.append(
            "| pointer_graph_missing | deterministic | blocked_external_dependency | "
            "gpu1_planner |  | False |  |"
        )
        return lines
    for row in rows:
        lines.append(
            "| {pointer_id} | {source_role} | {closure_status} | {closure_owner} | "
            "{closure_evidence_block_id} | {included_in_product} | {resume_from_block_id} |".format(
                pointer_id=_md(row.get("pointer_id")),
                source_role=_md(row.get("source_role")),
                closure_status=_md(row.get("closure_status")),
                closure_owner=_md(row.get("closure_owner")),
                closure_evidence_block_id=_md(row.get("closure_evidence_block_id")),
                included_in_product=_md(row.get("included_in_product")),
                resume_from_block_id=_md(row.get("resume_from_block_id")),
            )
        )
    return lines


def gpu1_blocked_reason_from_gate(gate: dict[str, Any]) -> str:
    for report in _as_list(gate.get("provider_reports")):
        item = _as_dict(report)
        if str(item.get("lane") or "") != "gpu1_planner":
            continue
        blocked = str(item.get("product_blocked_reason") or "")
        if blocked:
            return blocked
        if item.get("status") != "ready" and not item.get("provider_device_verified"):
            return str(item.get("provider_activity_classification") or "")
        return ""
    metrics = _as_dict(gate.get("metrics"))
    for reason in _as_list(metrics.get("missing_requirements")):
        text = str(reason)
        if "ollama" in text or "gpu1" in text:
            return text
    return ""


def soft_lock_state_from_reports(
    gate: dict[str, Any],
    pointer: dict[str, Any],
    revision: dict[str, Any],
) -> dict[str, Any]:
    metrics = _as_dict(gate.get("metrics"))
    table = _as_list(
        revision.get("pointer_closure_table")
        or pointer.get("pointer_closure_table")
        or metrics.get("pointer_closure_table")
    )
    open_count = int(
        revision.get("open_pointer_count_final")
        or pointer.get("open_pointer_count_final")
        or metrics.get("open_pointer_count_final")
        or 0
    )
    return {
        "soft_lock_state": revision.get("soft_lock_state")
        or pointer.get("soft_lock_state")
        or metrics.get("soft_lock_state")
        or ("closing_open_pointers" if open_count else "closed"),
        "soft_lock_extension_count": metrics.get("soft_lock_extension_count", 0),
        "open_pointer_count_before_soft_lock": metrics.get("open_pointer_count_before_soft_lock"),
        "open_pointer_count_after_each_extension": metrics.get(
            "open_pointer_count_after_each_extension", []
        ),
        "open_pointer_count_final": open_count,
        "pointer_closure_table": table,
        "soft_lock_closure_owner_decision": revision.get(
            "soft_lock_closure_owner_decision"
        )
        or pointer.get("soft_lock_closure_owner_decision")
        or metrics.get("soft_lock_closure_owner_decision", ""),
        "gpu0_closure_agreement": revision.get("gpu0_closure_agreement")
        or pointer.get("gpu0_closure_agreement")
        or metrics.get("gpu0_closure_agreement", ""),
        "npu_closure_advisory": revision.get("npu_closure_advisory")
        or pointer.get("npu_closure_advisory")
        or metrics.get("npu_closure_advisory", ""),
        "cpu_closure_validation": revision.get("cpu_closure_validation")
        or pointer.get("cpu_closure_validation")
        or metrics.get("cpu_closure_validation", ""),
        "closure_quorum_status": revision.get("closure_quorum_status")
        or pointer.get("closure_quorum_status")
        or metrics.get("closure_quorum_status", ""),
        "closure_quorum_reason": revision.get("closure_quorum_reason")
        or pointer.get("closure_quorum_reason")
        or metrics.get("closure_quorum_reason", ""),
        "soft_lock_targeted_refine_used": revision.get("soft_lock_targeted_refine_used")
        or pointer.get("soft_lock_targeted_refine_used")
        or metrics.get("soft_lock_targeted_refine_used", False),
    }


def _runtime_pointer_blocks(owner: Any) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    for path in getattr(owner, "proposal_iteration_artifacts", lambda: [])():
        if not str(path).endswith(".json"):
            continue
        data = read_json(owner.repo_root / str(path))
        if data:
            blocks.append(
                {
                    "id": data.get("block_id")
                    or data.get("proposal_block_id")
                    or f"proposal_revision_{data.get('revision', 0)}",
                    "role": "gpu1_planner",
                    "accepted": data.get("accepted"),
                    "quality_passed": data.get("quality_passed"),
                    "reject_reason": data.get("reject_reason", ""),
                    "exit_decision": data.get("exit_decision", ""),
                    "resume_from_block_id": data.get("resume_from_block_id", ""),
                    "blocked_reason": data.get("closure_quorum_reason", ""),
                }
            )
    return blocks


def _closure_entry(
    block: dict[str, Any],
    blocks: list[dict[str, Any]],
    *,
    semantic_defer_open: bool = False,
    resume_from_block_id: str = "",
    closure_evidence_block_id: str = "",
) -> dict[str, Any]:
    pointer_id = str(block.get("id") or block.get("block_id") or "")
    role = str(block.get("role") or block.get("source_role") or "")
    resume = str(block.get("resume_from_block_id") or resume_from_block_id or "")
    accepted = bool(block.get("accepted") or block.get("quality_passed"))
    reason = str(block.get("reject_reason") or block.get("blocked_reason") or "")
    exit_decision = str(block.get("exit_decision") or "").upper()
    superseded = _superseded_by(pointer_id, blocks)
    peer_needs_gpu1_consumption = bool(
        accepted and role in PEER_POINTER_ROLES and not _peer_consumed_by_gpu1(pointer_id, blocks)
    )
    if peer_needs_gpu1_consumption:
        status = "deferred_to_resume"
        included = False
        resume = resume or pointer_id
        reason = reason or f"{role}_followup_pending_gpu1_consumption"
    elif accepted:
        status = "merged_into_final_product"
        included = True
    elif superseded:
        status = "superseded_by_pointer"
        included = False
    elif exit_decision in {"REQUIRES_OPERATOR_INPUT", "OPERATOR_INPUT_REQUIRED"}:
        status = "requires_operator_input"
        included = False
    elif exit_decision in {"BLOCKED_EXTERNAL_DEPENDENCY", "EXTERNAL_DEPENDENCY_BLOCKED"}:
        status = "blocked_external_dependency"
        included = False
    elif exit_decision in {"BLOCKED_CONTINUATION", "DEFERRED_TO_RESUME"}:
        status = "deferred_to_resume"
        included = False
    elif resume:
        status = "deferred_to_resume"
        included = False
    elif reason or exit_decision in {"NO_PATCHABLE_TARGET", "NO_MORE_ACTION"}:
        status = "rejected_with_reason"
        included = False
    elif semantic_defer_open:
        status = "deferred_to_resume"
        included = False
        if not resume:
            resume = resume_from_block_id or pointer_id
    else:
        status = "open"
        included = False
    return {
        "pointer_id": pointer_id,
        "source_role": role,
        "closure_status": status,
        "closure_owner": "gpu1_planner",
        "closure_evidence_block_id": (
            pointer_id if status != "open" else closure_evidence_block_id
        ),
        "included_in_product": included,
        "resume_from_block_id": resume,
        "closure_reason": reason or exit_decision,
    }


def _superseded_by(pointer_id: str, blocks: list[dict[str, Any]]) -> str:
    for block in blocks:
        if str(block.get("refines_block_id") or "") == pointer_id:
            return str(block.get("id") or block.get("block_id") or "")
    return ""


def _peer_consumed_by_gpu1(pointer_id: str, blocks: list[dict[str, Any]]) -> bool:
    if not pointer_id:
        return False
    peer_index = next(
        (
            index
            for index, block in enumerate(blocks)
            if str(block.get("id") or block.get("block_id") or "") == pointer_id
        ),
        -1,
    )
    candidate_blocks = blocks[peer_index + 1 :] if peer_index >= 0 else []
    for block in candidate_blocks:
        role = str(block.get("role") or block.get("source_role") or "")
        if role != "gpu1_planner":
            continue
        related = {
            str(block.get("previous_block_id") or ""),
            str(block.get("refines_block_id") or ""),
            str(block.get("resume_from_block_id") or ""),
        }
        consumed = block.get("consumed_block_ids") or block.get("consumes_block_ids") or []
        if isinstance(consumed, list):
            related.update(str(item) for item in consumed)
        if pointer_id in related:
            return True
    return False


def _md(value: Any) -> str:
    return str(value if value is not None else "").replace("|", "\\|").replace("\n", " ")


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
