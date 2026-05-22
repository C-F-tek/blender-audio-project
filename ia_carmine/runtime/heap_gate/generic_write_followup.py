"""Generic-write follow-up rules for provider-native broker evidence."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import Any, provider_heap_lane, read_json, safe_int

GENERIC_WRITE_CAPTURE_LANES = {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}
OPERATIVE_GENERIC_WRITE_LANES = GENERIC_WRITE_CAPTURE_LANES
PEER_GENERIC_WRITE_LANES = {"gpu0_peer", "npu_micro_task_auditor"}
GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS = 3


def generic_write_results(
    events: list[dict[str, Any]], owner: Any | None = None
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "broker_result":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if str(payload.get("tool") or "") != "generic_write":
            continue
        payload = _hydrate_generic_write_payload(owner, payload) if owner is not None else payload
        if str(payload.get("lane") or "") not in OPERATIVE_GENERIC_WRITE_LANES:
            continue
        results.append(payload)
    return results


def passed_generic_write_results(
    events: list[dict[str, Any]], owner: Any | None = None
) -> list[dict[str, Any]]:
    passed: list[dict[str, Any]] = []
    for payload in generic_write_results(events, owner=owner):
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


def generic_write_refinement_count(events: list[dict[str, Any]], owner: Any | None = None) -> int:
    return len(passed_generic_write_results(events, owner=owner))


def _latest_gpu1_revision(owner: Any) -> int:
    revisions = [
        safe_int(report.get("revision"), default=0)
        for report in getattr(owner, "provider_reports", [])
        if report.get("lane") == "gpu1_planner"
    ]
    return max(revisions) if revisions else -1


def generic_write_followup_pending(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    latest_gpu1 = _latest_gpu1_revision(owner)
    pending: list[dict[str, Any]] = []
    for payload in passed_generic_write_results(events, owner=owner):
        source_revision = safe_int(payload.get("revision"), default=0)
        if latest_gpu1 <= source_revision:
            pending.append(payload)
    return pending


def generic_write_followup_pending_count(owner: Any, events: list[dict[str, Any]]) -> int:
    return len(generic_write_followup_pending(owner, events))


def gpu0_peer_followup_pending(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _peer_followup_pending(owner, events, "gpu0_peer")


def gpu0_peer_followup_pending_count(owner: Any, events: list[dict[str, Any]]) -> int:
    return len(gpu0_peer_followup_pending(owner, events))


def npu_peer_followup_pending(owner: Any, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return _peer_followup_pending(owner, events, "npu_micro_task_auditor")


def npu_peer_followup_pending_count(owner: Any, events: list[dict[str, Any]]) -> int:
    return len(npu_peer_followup_pending(owner, events))


def _peer_followup_pending(
    owner: Any, events: list[dict[str, Any]], lane: str
) -> list[dict[str, Any]]:
    latest_gpu1 = _latest_gpu1_revision(owner)
    pending: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != "broker_result":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if str(payload.get("tool") or "") == "generic_write":
            payload = _hydrate_generic_write_payload(owner, payload)
        if str(payload.get("lane") or "") != lane:
            continue
        if not payload.get("gpu1_followup_required"):
            continue
        source_revision = safe_int(payload.get("revision"), default=0)
        if latest_gpu1 <= source_revision:
            pending.append(payload)
    return pending


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


def _hydrate_generic_write_payload(owner: Any | None, payload: dict[str, Any]) -> dict[str, Any]:
    if owner is None:
        return payload
    report = _generic_write_report(owner, payload)
    if not report:
        return payload
    provider_summary = (
        report.get("provider_summary")
        if isinstance(report.get("provider_summary"), dict)
        else {}
    )
    lane = str(
        payload.get("lane")
        or report.get("source_lane")
        or provider_summary.get("lane")
        or ""
    )
    revision = payload.get("revision")
    if revision is None:
        revision = report.get("source_revision") or provider_summary.get("revision")
    followup = payload.get("gpu1_followup_required")
    if followup is None:
        followup = report.get("gpu1_followup_required")
    if followup is None:
        followup = lane in PEER_GENERIC_WRITE_LANES
    hydrated = dict(payload)
    hydrated.update(
        {
            "lane": lane,
            "revision": revision,
            "provider_report": payload.get("provider_report") or report.get("provider_report"),
            "gpu1_followup_required": bool(followup),
            "peer_followup_required": bool(
                report.get("peer_followup_required") or lane in PEER_GENERIC_WRITE_LANES
            ),
            "capture_mode": payload.get("capture_mode") or report.get("capture_mode"),
        }
    )
    return hydrated


def generic_write_document_product_eligible(owner: Any, events: list[dict[str, Any]]) -> bool:
    if generic_write_refinement_count(events, owner) < GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
        return False
    if generic_write_followup_pending_count(owner, events) > 0:
        return False
    if gpu0_peer_followup_pending_count(owner, events) > 0:
        return False
    if npu_peer_followup_pending_count(owner, events) > 0:
        return False
    return True


def generic_write_document_product(owner: Any, events: list[dict[str, Any]]) -> dict[str, Any]:
    results = passed_generic_write_results(events, owner=owner)
    latest = results[-1] if results else {}
    report = _generic_write_report(owner, latest) if latest else {}
    latest_gpu1 = _latest_gpu1_revision(owner)
    latest_source_revision = safe_int(latest.get("revision"), default=-1) if latest else -1
    lanes = [str(payload.get("lane") or "") for payload in results]
    captures = [_capture_summary(owner, payload) for payload in results]
    return {
        "eligible": generic_write_document_product_eligible(owner, events),
        "kind": "generic_write_refined_product",
        "minimum_refinements": GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS,
        "refinement_count": len(results),
        "capture_count": len(results),
        "generic_write_no_tool_capture_count": sum(
            1
            for payload in results
            if str(_generic_write_report(owner, payload).get("capture_mode") or payload.get("capture_mode") or "")
            == "no_tool_capture"
        ),
        "generic_write_lanes": sorted(set(lane for lane in lanes if lane)),
        "gpu0_peer_followup_pending_count": gpu0_peer_followup_pending_count(owner, events),
        "npu_peer_followup_pending_count": npu_peer_followup_pending_count(owner, events),
        "capture_modes": [
            str(_generic_write_report(owner, payload).get("capture_mode") or payload.get("capture_mode") or "")
            for payload in results
        ],
        "latest_source_lane": str(latest.get("lane") or "") if latest else "",
        "latest_source_revision": latest_source_revision,
        "latest_consumed_by_gpu1": latest_gpu1 > latest_source_revision,
        "latest_outputs": _tool_outputs(latest) if latest else {},
        "latest_refined_request": str(report.get("refined_request") or "")[:6000],
        "captures": captures,
        "code_product_allowed_after_three_refinements": True,
        "product_includes_provider_communication": True,
        "readable_code_content_allowed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def _capture_summary(owner: Any, payload: dict[str, Any]) -> dict[str, Any]:
    report = _generic_write_report(owner, payload)
    return {
        "lane": str(payload.get("lane") or report.get("source_lane") or ""),
        "revision": payload.get("revision") if payload.get("revision") is not None else report.get("source_revision"),
        "capture_mode": str(report.get("capture_mode") or payload.get("capture_mode") or ""),
        "gpu1_followup_required": bool(
            payload.get("gpu1_followup_required") or report.get("gpu1_followup_required")
        ),
        "peer_followup_required": bool(
            payload.get("peer_followup_required") or report.get("peer_followup_required")
        ),
        "outputs": _tool_outputs(payload),
        "provider_report": str(report.get("provider_report") or payload.get("provider_report") or ""),
        "provider_response_excerpt": str(report.get("provider_response_excerpt") or "")[:1200],
    }


def maybe_run_generic_write_followup(
    owner: Any, round_id: int, events: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    pending = generic_write_followup_pending(owner, events)
    if not pending:
        pending = gpu0_peer_followup_pending(owner, events)
    if not pending:
        pending = npu_peer_followup_pending(owner, events)
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
    tool_name = str(payload.get("tool") or "")
    source_revision = safe_int(payload.get("revision"), default=0)
    next_revision = max(safe_int(owner.provider_revision_count, default=0) + 1, source_revision + 1)
    owner.provider_revision_count = next_revision
    outputs = _tool_outputs(payload)
    report = _generic_write_report(owner, payload) if tool_name == "generic_write" else {}
    owner.provider_revision_feedback = "\n".join(
        [
            "GENERIC_WRITE_NEXT_TURN_REQUIRED",
            f"source_lane={source_lane}",
            f"source_tool={tool_name}",
            f"source_revision={source_revision}",
            f"generic_write_outputs={outputs}",
            f"refined_request_excerpt={str(report.get('refined_request') or '')[:2400]}",
            "GPU1 must consume this peer/tool evidence in a new revision; do not repeat the rejected block.",
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
    if getattr(owner, "provider_universe_blocked_reason", ""):
        return owner.read_events()
    return updated
