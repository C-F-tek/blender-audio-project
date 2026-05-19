"""Provider-universe abort helpers for heap runtime gate."""
from __future__ import annotations
from Tools.ai.heap_gate.runtime_common import Any, repo_rel


def provider_universe_abort_reason(prepared: list[dict[str, Any]]) -> str:
    for item in prepared:
        report = item.get("provider_report")
        if not isinstance(report, dict):
            continue
        status = str(report.get("status") or "")
        if status in {"failed", "non_operational"}:
            return f"provider_universe_lane_not_active:{item.get('lane')}:{status}"
    return ""


def block_provider_universe_run(gate: Any, reason: str, round_id: int, revision: int) -> None:
    if not reason:
        return
    gate.provider_universe_blocked_reason = reason
    if reason not in gate.errors:
        gate.errors.append(reason)
    decision = {
        "id": "provider_universe_blocked",
        "from": "provider_universe",
        "decision": "blocked_with_reason",
        "reason": reason,
        "revision": revision,
        "round": round_id,
    }
    if not any(item.get("id") == decision["id"] for item in gate.state.get("decisions", [])):
        gate.state["decisions"].append(decision)
        gate.decision_count += 1
        gate.publish(
            "deterministic",
            "decision",
            decision,
            target="orchestrator",
            correlation_id=f"{gate.stamp}:provider-universe-blocked",
            round_id=round_id,
        )
    product = {
        "required": True,
        "status": "blocked_with_reason",
        "request_input": gate.request_text(),
        "response_text": gate.build_final_response_text(gate.read_events()),
        "response_source": gate.response_source(),
        "heap_event_refs": [repo_rel(gate.repo_root, gate.heap.paths.events)],
        "provider_refs": gate.provider_refs(),
        "provider_response_texts": gate.provider_response_texts(),
        "provider_role_decisions": gate.provider_role_decisions(),
        "missing_requirements": [reason],
        "reason": reason,
        "provider_universe_blocked": True,
    }
    gate.state["product"] = product
    gate.publish(
        "orchestrator",
        "product_signal",
        product,
        correlation_id=f"{gate.stamp}:provider-universe-product-blocked",
        round_id=round_id,
    )
