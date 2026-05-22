"""Generic-write follow-up rules for provider-native broker evidence."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, provider_heap_lane, read_json, safe_int

OPERATIVE_GENERIC_WRITE_LANES = {"gpu1_planner", "gpu0_peer"}
GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS = 3


def generic_write_results(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "broker_result":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if str(payload.get("tool") or "") != "generic_write":
            continue
        if str(payload.get("lane") or "") not in OPERATIVE_GENERIC_WRITE_LANES:
            continue
        results.append(payload)
    return results


def passed_generic_write_results(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    passed: list[dict[str, Any]] = []
    for payload in generic_write_results(events):
        errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
        if payload.get("blocked") or errors:
            continue
        if safe_int(payload.get("returncode"), default=1) != 0:
            continue
        summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
        if summary.get("passed") is False:
            continue
        passed.append(payload)
    return passed


def generic_write_refinement_count(events: list[dict[str, Any]]) -> int:
    return len(passed_generic_write_results(events))


def _latest_gpu1_revision(owner: Any) -> int:
    revisions = [
        safe_int(report.get("revision"), default=0)
        for report in getattr(owner, "provider_reports", [])
        if report.get("lane") == "gpu1_planner"
    ]
    return max(revisions) if revisions else -1


def generic_write_followup_pending(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if generic_write_refinement_count(events) >= GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
        return []
    latest_gpu1 = _latest_gpu1_revision(owner)
    pending: list[dict[str, Any]] = []
    for payload in passed_generic_write_results(events):
        source_revision = safe_int(payload.get("revision"), default=0)
        if latest_gpu1 <= source_revision:
            pending.append(payload)
    return pending


def generic_write_followup_pending_count(owner: Any, events: list[dict[str, Any]]) -> int:
    return len(generic_write_followup_pending(owner, events))


def _tool_outputs(payload: dict[str, Any]) -> dict[str, Any]:
    outputs = payload.get("outputs")
    return outputs if isinstance(outputs, dict) else {}


def _generic_write_report(owner: Any, payload: dict[str, Any]) -> dict[str, Any]:
    outputs = _tool_outputs(payload)
    report_ref = str(outputs.get("json_report") or "").strip()
    if not report_ref:
        return {}
    report_path = owner.repo_root / report_ref
    return read_json(report_path)


def generic_write_document_product_eligible(owner: Any, events: list[dict[str, Any]]) -> bool:
    if generic_write_refinement_count(events) < GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
        return False
    if generic_write_followup_pending_count(owner, events) > 0:
        return False
    return True


def generic_write_document_product(owner: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    results = passed_generic_write_results(events)
    latest = results[-1] if results else {}
    report = _generic_write_report(owner, latest) if latest else {}
    return {
        "eligible": generic_write_document_product_eligible(owner, events),
        "kind": "generic_write_document_product",
        "minimum_refinements": GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS,
        "refinement_count": len(results),
        "latest_outputs": _tool_outputs(latest) if latest else {},
        "latest_refined_request": str(report.get("refined_request") or "")[:6000],
        "code_product_allowed_after_three_refinements": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def maybe_run_generic_write_followup(
    owner: Any, round_id: int, events: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    pending = generic_write_followup_pending(owner, events)
    if not pending or getattr(owner, "provider_universe_blocked_reason", ""):
        return events
    attempted = getattr(owner, "_generic_write_followup_attempted", set())
    if not isinstance(attempted, set):
        attempted = set()
    payload = pending[0]
    digest = owner.broker_result_digest(payload)
    if digest in attempted:
        return events
    attempted.add(digest)
    owner._generic_write_followup_attempted = attempted

    source_lane = str(payload.get("lane") or "")
    source_revision = safe_int(payload.get("revision"), default=0)
    next_revision = max(safe_int(owner.provider_revision_count, default=0) + 1, source_revision + 1)
    owner.provider_revision_count = next_revision
    outputs = _tool_outputs(payload)
    report = _generic_write_report(owner, payload)
    owner.provider_revision_feedback = "\n".join(
        [
            "GENERIC_WRITE_NEXT_TURN_REQUIRED",
            f"source_lane={source_lane}",
            f"source_revision={source_revision}",
            f"generic_write_outputs={outputs}",
            f"refined_request_excerpt={str(report.get('refined_request') or '')[:2400]}",
            "GPU1 must consume this refined MD/JSON in a new revision; do not repeat the rejected block.",
            "After three consumed generic_write refinements this may close as a readable refined product, including code content, but not as applied source writes.",
        ]
    )
    owner.publish(
        "deterministic",
        "validation_signal",
        {
            "kind": "generic_write_next_turn_required",
            "source_lane": source_lane,
            "source_revision": source_revision,
            "next_gpu1_revision": next_revision,
            "generic_write_outputs": outputs,
            "validator_action": "generate_new_gpu1_revision_consuming_generic_write",
        },
        target="gpu1",
        correlation_id=f"{owner.stamp}:generic-write-followup:{digest}",
        round_id=round_id,
    )
    owner.append_heap_exchange_event(
        {
            "kind": "generic_write_followup",
            "lane": provider_heap_lane(source_lane),
            "round": round_id,
            "summary": "generic_write evidence requires a later GPU1 revision before final product",
            "source_revision": source_revision,
            "next_gpu1_revision": next_revision,
        }
    )
    owner.run_provider_teamwork(round_id, revision=next_revision)
    updated = owner.read_events()
    if getattr(owner, "provider_universe_blocked_reason", ""):
        return updated
    if owner.publish_provider_native_tool_calls(round_id, updated):
        if owner.heap.pending_broker_requests():
            owner.run_bridge()
        updated = owner.read_events()
    owner.publish_shared_evidence_facts(round_id, updated)
    if owner.detailed_output_expected() and owner.response_text():
        updated = owner.persist_current_gpu1_proposal_iteration(
            revision=next_revision,
            events=updated,
            source="gpu1_generic_write_followup",
        )
    return updated
