"""Deterministic MPC-lite governor for GPU1 tool-calling loops."""

from __future__ import annotations

import json
from typing import Any

from ia_carmine.runtime.heap_gate.final_product_delta_protocol import section_body
from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import (
    gpu1_tool_result_consumption_state,
)
from ia_carmine.runtime.heap_gate.runtime_common import safe_int
from ia_carmine.runtime.runtime_tool.tool_cycle_contract import normalize_tool_cycle_status


THRESHOLD = 100
GPU0_BLOCKING_DECISIONS = {"veto", "refine_required", "incongruent"}


def build_gpu1_tool_mpc_governor_report(
    owner: Any,
    events: list[dict[str, Any]],
    *,
    response_text: str,
    revision: int,
    final_product_protocol: dict[str, Any] | None = None,
    final_product_code_file_read_contract: dict[str, Any] | None = None,
    gpu1_tool_result_consumption: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic report; this never calls providers."""
    final_product_protocol = (
        final_product_protocol if isinstance(final_product_protocol, dict) else {}
    )
    final_product_code_file_read_contract = (
        final_product_code_file_read_contract
        if isinstance(final_product_code_file_read_contract, dict)
        else {}
    )
    consumption = (
        gpu1_tool_result_consumption
        if isinstance(gpu1_tool_result_consumption, dict)
        else gpu1_tool_result_consumption_state(owner, events, response_text=response_text)
    )
    cycle_statuses = _tool_cycle_statuses(consumption)
    loop_state = _tool_loop_state(consumption)
    signals: list[dict[str, Any]] = []
    _add_pending_tool_signal(signals, consumption)
    _add_same_tool_repeat_signal(signals, loop_state)
    _add_failed_tool_consumed_signal(signals, consumption)
    _add_code_delta_signal(signals, final_product_code_file_read_contract, consumption)
    gpu0_signal = _gpu0_signal(owner, response_text)
    npu_signal = _npu_signal(owner, response_text)
    if gpu0_signal.get("active"):
        signals.append(gpu0_signal)
    if npu_signal.get("active"):
        signals.append(npu_signal)
    _add_valid_final_delta_signal(signals, final_product_protocol)
    total_cost = sum(safe_int(item.get("cost"), default=0) for item in signals)
    decision, first_blocker, next_action = _decision(signals, total_cost)
    return {
        "schema_version": 1,
        "kind": "gpu1_tool_mpc_governor",
        "passed": True,
        "revision": int(revision),
        "decision": decision,
        "total_cost": total_cost,
        "threshold": THRESHOLD,
        "first_blocker": first_blocker,
        "required_next_action": next_action,
        "cost_signals": signals,
        "gpu0_cost_signal": gpu0_signal,
        "npu_cost_signal": npu_signal,
        "tool_loop_state": loop_state,
        "tool_cycle_statuses": cycle_statuses,
    }


def _add_pending_tool_signal(signals: list[dict[str, Any]], consumption: dict[str, Any]) -> None:
    pending = [
        *[str(item) for item in consumption.get("gpu1_pending_tool_result_ids") or []],
        *[str(item) for item in consumption.get("gpu1_unconsumed_tool_result_ids") or []],
    ]
    if pending or consumption.get("gpu1_resume_after_tool_result_required"):
        signals.append(
            _signal(
                "pending_tool_result",
                90,
                str(consumption.get("gpu1_tool_result_blocker") or "gpu1_requested_tool_result_not_consumed"),
                pending_tool_result_ids=list(dict.fromkeys(item for item in pending if item)),
            )
        )


def _add_same_tool_repeat_signal(signals: list[dict[str, Any]], loop_state: dict[str, Any]) -> None:
    if safe_int(loop_state.get("same_tool_repeat_count"), default=0) > 0:
        signals.append(
            _signal(
                "same_tool_repeat",
                100,
                "gpu1_repeated_same_tool_call_without_new_consumed_result",
                repeat_count=loop_state.get("same_tool_repeat_count"),
            )
        )


def _add_failed_tool_consumed_signal(signals: list[dict[str, Any]], consumption: dict[str, Any]) -> None:
    failed = [str(item) for item in consumption.get("gpu1_consumed_failed_tool_result_ids") or [] if str(item)]
    if failed:
        signals.append(
            _signal(
                "failed_tool_consumed",
                100,
                "gpu1_consumed_failed_tool_result_as_evidence",
                consumed_failed_tool_result_ids=failed,
            )
        )


def _add_code_delta_signal(
    signals: list[dict[str, Any]],
    file_read: dict[str, Any],
    consumption: dict[str, Any],
) -> None:
    if file_read.get("required") is True and file_read.get("verified") is not True:
        pending = bool(
            consumption.get("gpu1_pending_tool_result_ids")
            or consumption.get("gpu1_unconsumed_tool_result_ids")
        )
        signals.append(
            _signal(
                "code_delta_without_file_window",
                80,
                "gpu1_code_delta_without_verified_runtime_file_window",
                preferred_decision="force_consume_tool_result" if pending else "block_with_reason",
            )
        )


def _add_valid_final_delta_signal(
    signals: list[dict[str, Any]], protocol: dict[str, Any]
) -> None:
    if protocol.get("passed") is True:
        signals.append(_signal("valid_final_delta", -100, "final_product_delta_valid"))


def _gpu0_signal(owner: Any, response_text: str) -> dict[str, Any]:
    reports = getattr(owner, "provider_reports", []) or []
    consumed_text = response_text.lower()
    for report in reversed(reports):
        if str(report.get("lane") or "") != "gpu0_peer":
            continue
        decision = str(
            report.get("gpu0_effective_decision")
            or report.get("gpu0_decision")
            or report.get("role_decision")
            or ""
        ).strip().lower()
        block_id = str(report.get("provider_block_id") or report.get("block_id") or "")
        if decision in GPU0_BLOCKING_DECISIONS and block_id.lower() not in consumed_text:
            return _signal(
                "gpu0_veto_unconsumed",
                70,
                "gpu0_veto_or_refine_required_not_consumed_by_gpu1",
                provider_block_id=block_id,
                decision=decision,
                preferred_decision="force_gpu1_refine",
            )
    return {}


def _npu_signal(owner: Any, response_text: str) -> dict[str, Any]:
    reports = getattr(owner, "provider_reports", []) or []
    consumed_text = response_text.lower()
    issue_tokens = ("placeholder", "tool_loop", "source_write", "invalid", "blocked")
    for report in reversed(reports):
        if str(report.get("lane") or "") != "npu_micro_task_auditor":
            continue
        block_id = str(report.get("provider_block_id") or report.get("block_id") or "")
        body = json.dumps(report, ensure_ascii=False).lower()
        if any(token in body for token in issue_tokens) and block_id.lower() not in consumed_text:
            return _signal(
                "npu_audit_unconsumed",
                50,
                "npu_audit_issue_not_consumed_by_gpu1",
                provider_block_id=block_id,
            )
    return {}


def _tool_cycle_statuses(consumption: dict[str, Any]) -> list[dict[str, Any]]:
    raw = consumption.get("tool_cycle_statuses")
    if isinstance(raw, list) and raw:
        return [item for item in raw if isinstance(item, dict)]
    ledger = consumption.get("gpu1_tool_result_ledger")
    if isinstance(ledger, list):
        return [normalize_tool_cycle_status(item) for item in ledger if isinstance(item, dict)]
    return []


def _tool_loop_state(consumption: dict[str, Any]) -> dict[str, Any]:
    ledger = consumption.get("gpu1_tool_result_ledger")
    ledger = ledger if isinstance(ledger, list) else []
    keys: dict[str, int] = {}
    for item in ledger:
        if not isinstance(item, dict):
            continue
        tool = str(item.get("tool") or "")
        args = json.dumps(item.get("args_ref") or {}, sort_keys=True, default=str)
        key = f"{tool}:{args}"
        keys[key] = keys.get(key, 0) + 1
    repeat_count = sum(count - 1 for count in keys.values() if count > 1)
    if consumption.get("tool_result_consumed_by_gpu1"):
        repeat_count = 0
    return {
        "same_tool_repeat_count": repeat_count,
        "pending_tool_result_ids": [
            str(item) for item in consumption.get("gpu1_pending_tool_result_ids") or []
        ],
        "unconsumed_tool_result_ids": [
            str(item) for item in consumption.get("gpu1_unconsumed_tool_result_ids") or []
        ],
        "consumed_failed_tool_result_ids": [
            str(item) for item in consumption.get("gpu1_consumed_failed_tool_result_ids") or []
        ],
    }


def _decision(signals: list[dict[str, Any]], total_cost: int) -> tuple[str, str, str]:
    active = [item for item in signals if item.get("active")]
    by_name = {str(item.get("name")): item for item in active}
    if "failed_tool_consumed" in by_name:
        return "block_with_reason", str(by_name["failed_tool_consumed"].get("reason")), "Do not cite failed tool_result in CONSUMED_EVIDENCE."
    if "same_tool_repeat" in by_name:
        return "block_repeat_tool_call", str(by_name["same_tool_repeat"].get("reason")), "Change tool choice or consume the existing result before repeating."
    if "pending_tool_result" in by_name:
        return "force_consume_tool_result", str(by_name["pending_tool_result"].get("reason")), "Resume GPU1 and consume the pending tool_result."
    if "code_delta_without_file_window" in by_name:
        signal = by_name["code_delta_without_file_window"]
        preferred = str(signal.get("preferred_decision") or "block_with_reason")
        return preferred, str(signal.get("reason")), "Read source content with runtime_file_window before code delta."
    if "gpu0_veto_unconsumed" in by_name:
        return "force_gpu1_refine", str(by_name["gpu0_veto_unconsumed"].get("reason")), "Resume GPU1 and consume/refine against GPU0 sidecar evidence."
    blockers = [item for item in active if safe_int(item.get("cost"), default=0) > 0]
    if blockers and total_cost >= THRESHOLD:
        first = blockers[0]
        return "block_with_reason", str(first.get("reason") or first.get("name")), "Resolve the first active blocker."
    if by_name.get("valid_final_delta") and not blockers:
        return "emit_final_delta", "", "Emit/apply the valid FINAL_PRODUCT_DELTA."
    return "continue", "", "Continue GPU1 runtime loop."


def _signal(name: str, cost: int, reason: str, **extra: Any) -> dict[str, Any]:
    return {"name": name, "cost": cost, "active": True, "reason": reason, **extra}
