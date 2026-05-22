"""Operator decision sidecar writer for final readable products."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def write_operator_decision(
    path: Path,
    *,
    final_document_status: str,
    product_kind: str,
    product_status: str,
    gpu1_reason: str,
    resume_from_block_id: str,
    soft_lock: dict[str, Any],
    provider_blocked_reason: str,
    provider_replight_reports: list[Any],
    open_pointer_count_final: int,
    blocked_continuation: bool,
    write_text: Any,
) -> None:
    replight_lines = [
        "provider_replight:",
        *[
            (
                f"- {_as_dict(item).get('lane')}: passed={_as_dict(item).get('replight_passed')} "
                f"loaded={_as_dict(item).get('provider_loaded')} model={_as_dict(item).get('provider_model')} "
                f"reason={_as_dict(item).get('replight_blocked_reason')}"
            )
            for item in provider_replight_reports
        ],
    ]
    lines = [
        f"final_document_status={final_document_status}",
        f"product_kind={product_kind}",
        f"product_status={product_status}",
        f"gpu1_blocked_reason={gpu1_reason}",
        f"resume_from_block_id={resume_from_block_id}",
        f"soft_lock_state={soft_lock.get('soft_lock_state') or ''}",
        f"closure_quorum_status={soft_lock.get('closure_quorum_status') or ''}",
        f"closure_quorum_reason={soft_lock.get('closure_quorum_reason') or ''}",
        f"gpu1_closure_decision={soft_lock.get('soft_lock_closure_owner_decision') or ''}",
        f"gpu0_closure_agreement={soft_lock.get('gpu0_closure_agreement') or ''}",
        f"npu_closure_advisory={soft_lock.get('npu_closure_advisory') or ''}",
        f"cpu_closure_validation={soft_lock.get('cpu_closure_validation') or ''}",
        f"provider_blocked_reason={provider_blocked_reason}",
        *replight_lines,
        f"open_pointer_count_final={open_pointer_count_final}",
        (
            "decision=do not apply patch; continue from the listed resume/pointer closure table."
            if blocked_continuation
            else "decision=review code product status before apply."
        ),
    ]
    write_text(path, "\n".join(lines))


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
