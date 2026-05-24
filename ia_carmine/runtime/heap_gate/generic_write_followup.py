"""Generic-write follow-up rules for provider-native broker evidence."""

from __future__ import annotations

from ia_carmine._shared.file_backed_transport import read_text_windows_safe, resolve_path
from ia_carmine.runtime.heap_gate.runtime_common import Any, provider_heap_lane, read_json, safe_int

GENERIC_WRITE_CAPTURE_LANES = {"gpu1_planner"}
OPERATIVE_GENERIC_WRITE_LANES = GENERIC_WRITE_CAPTURE_LANES
PEER_GENERIC_WRITE_LANES: set[str] = set()
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
        if owner is not None and not _generic_write_source_verified(owner, payload):
            continue
        passed.append(payload)
    return passed


def generic_write_refinement_count(events: list[dict[str, Any]], owner: Any | None = None) -> int:
    if owner is None:
        return len(passed_generic_write_results(events, owner=owner))
    return generic_write_consumed_round_count(owner, events)


def generic_write_consumed_round_count(owner: Any, events: list[dict[str, Any]]) -> int:
    del events
    refs = getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or []
    return len({str(item) for item in refs if str(item).strip()})


def failed_generic_write_results(
    events: list[dict[str, Any]], owner: Any | None = None
) -> list[dict[str, Any]]:
    failed: list[dict[str, Any]] = []
    for payload in generic_write_results(events, owner=owner):
        errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
        summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
        returncode = payload.get("returncode")
        if (
            payload.get("blocked")
            or errors
            or (returncode is not None and safe_int(returncode, default=1) != 0)
            or summary.get("passed") is False
        ):
            failed.append(payload)
    return failed


def generic_write_capture_failed_count(
    events: list[dict[str, Any]], owner: Any | None = None
) -> int:
    return len(failed_generic_write_results(events, owner=owner))


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
        if not payload.get("gpu1_followup_required"):
            continue
        if _generic_write_ref_id(owner, payload) in _consumed_generic_write_refs(owner):
            continue
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
        if _generic_write_ref_id(owner, payload) in _consumed_generic_write_refs(owner):
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


def _generic_write_report_text(owner: Any, report: dict[str, Any], prefix: str) -> str:
    text = str(report.get(prefix) or "").strip()
    if text:
        return text
    ref = report.get(f"{prefix}_ref") if isinstance(report.get(f"{prefix}_ref"), dict) else {}
    ref_path = str(ref.get("path") or "").strip()
    if ref_path:
        try:
            return read_text_windows_safe(resolve_path(owner.repo_root, ref_path)).strip()
        except Exception:
            pass
    return str(report.get(f"{prefix}_tail") or "").strip()


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
    source_provider_passed = report.get("source_provider_passed")
    source_provider_execution = report.get("source_provider_execution_performed")
    source_provider_work = report.get("source_provider_work_verified")
    provider_summary = (
        report.get("provider_summary")
        if isinstance(report.get("provider_summary"), dict)
        else {}
    )
    hydrated = dict(payload)
    hydrated.update(
        {
            "lane": lane,
            "revision": revision,
            "provider_report": payload.get("provider_report") or report.get("provider_report"),
            "source_provider_passed": source_provider_passed
            if source_provider_passed is not None
            else provider_summary.get("passed"),
            "source_provider_execution_performed": source_provider_execution
            if source_provider_execution is not None
            else bool(
                provider_summary.get("provider_execution_performed")
                or provider_summary.get("operational_provider_activity")
            ),
            "source_provider_work_verified": source_provider_work
            if source_provider_work is not None
            else bool(
                provider_summary.get("provider_work_verified")
                or provider_summary.get("gpu1_primary_workload_valid")
            ),
            "source_provider_block_id": report.get("source_provider_block_id")
            or provider_summary.get("provider_block_id"),
            "source_proposal_block_id": report.get("source_proposal_block_id")
            or provider_summary.get("proposal_block_id"),
            "gpu1_followup_required": bool(followup),
            "peer_followup_required": bool(
                report.get("peer_followup_required") or lane in PEER_GENERIC_WRITE_LANES
            ),
            "capture_mode": payload.get("capture_mode") or report.get("capture_mode"),
        }
    )
    return hydrated


def _generic_write_source_verified(owner: Any, payload: dict[str, Any]) -> bool:
    hydrated = _hydrate_generic_write_payload(owner, payload)
    return bool(
        hydrated.get("source_provider_passed") is True
        and hydrated.get("source_provider_execution_performed") is True
        and hydrated.get("source_provider_work_verified") is True
    )


def _generic_write_ref_id(owner: Any, payload: dict[str, Any]) -> str:
    hydrated = _hydrate_generic_write_payload(owner, payload)
    for key in ("source_provider_block_id", "provider_block_id", "source_proposal_block_id"):
        value = str(hydrated.get(key) or "").strip()
        if value:
            return value
    outputs = _tool_outputs(hydrated)
    if outputs.get("json_report"):
        return str(outputs.get("json_report"))
    return owner.broker_result_digest(hydrated)


def _consumed_generic_write_refs(owner: Any) -> set[str]:
    return {
        str(item)
        for item in (getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or [])
        if str(item).strip()
    }


def generic_write_document_product_eligible(owner: Any, events: list[dict[str, Any]]) -> bool:
    results = passed_generic_write_results(events, owner=owner)
    if len(results) < GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
        return False
    consumed_refs = _consumed_generic_write_refs(owner)
    matched_refs = {
        _generic_write_ref_id(owner, payload)
        for payload in results
        if _generic_write_ref_id(owner, payload) in consumed_refs
    }
    if len(matched_refs) < GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
        return False
    if generic_write_consumed_round_count(owner, events) < GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS:
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
    failed_results = failed_generic_write_results(events, owner=owner)
    latest = _latest_verified_gpu1_result(results)
    report = _generic_write_report(owner, latest) if latest else {}
    latest_gpu1 = _latest_gpu1_revision(owner)
    latest_source_revision = safe_int(latest.get("revision"), default=-1) if latest else -1
    lanes = [str(payload.get("lane") or "") for payload in results]
    captures = [_capture_summary(owner, payload) for payload in results]
    consumed_count = generic_write_consumed_round_count(owner, events)
    return {
        "eligible": generic_write_document_product_eligible(owner, events),
        "kind": "generic_write_refined_product",
        "minimum_refinements": GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS,
        "refinement_count": consumed_count,
        "generic_write_consumed_round_count": consumed_count,
        "capture_count": len(results),
        "generic_write_source_unverified_count": len(generic_write_results(events, owner=owner))
        - len(results),
        "generic_write_capture_failed_count": len(failed_results),
        "generic_write_capture_failures": [
            _failed_capture_summary(payload) for payload in failed_results[:8]
        ],
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
        "latest_refined_request": _generic_write_report_text(
            owner, report, "refined_request"
        )[:6000],
        "captures": captures,
        "peer_review_refs": [
            item for item in captures if item.get("lane") in PEER_GENERIC_WRITE_LANES
        ],
        "gpu1_consumed_generic_write_block_ids": list(
            getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or []
        ),
        "code_product_allowed_after_three_refinements": True,
        "product_includes_provider_communication": True,
        "readable_code_content_allowed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def _latest_verified_gpu1_result(results: list[dict[str, Any]]) -> dict[str, Any]:
    for payload in reversed(results):
        if str(payload.get("lane") or "") == "gpu1_planner":
            return payload
    return {}


def _capture_summary(owner: Any, payload: dict[str, Any]) -> dict[str, Any]:
    report = _generic_write_report(owner, payload)
    hydrated = _hydrate_generic_write_payload(owner, payload)
    return {
        "lane": str(hydrated.get("lane") or report.get("source_lane") or ""),
        "revision": hydrated.get("revision")
        if hydrated.get("revision") is not None
        else report.get("source_revision"),
        "capture_mode": str(report.get("capture_mode") or payload.get("capture_mode") or ""),
        "gpu1_followup_required": bool(
            hydrated.get("gpu1_followup_required") or report.get("gpu1_followup_required")
        ),
        "peer_followup_required": bool(
            hydrated.get("peer_followup_required") or report.get("peer_followup_required")
        ),
        "source_provider_passed": hydrated.get("source_provider_passed"),
        "source_provider_execution_performed": hydrated.get(
            "source_provider_execution_performed"
        ),
        "source_provider_work_verified": hydrated.get("source_provider_work_verified"),
        "source_provider_block_id": hydrated.get("source_provider_block_id"),
        "outputs": _tool_outputs(payload),
        "provider_report": str(report.get("provider_report") or payload.get("provider_report") or ""),
        "provider_response_excerpt": str(report.get("provider_response_excerpt") or "")[:1200],
    }


def _failed_capture_summary(payload: dict[str, Any]) -> dict[str, Any]:
    return {
        "lane": str(payload.get("lane") or ""),
        "revision": payload.get("revision"),
        "capture_mode": str(payload.get("capture_mode") or ""),
        "request_id": str(payload.get("request_id") or payload.get("id") or ""),
        "errors": payload.get("errors") if isinstance(payload.get("errors"), list) else [],
        "returncode": payload.get("returncode"),
        "blocked": bool(payload.get("blocked")),
        "outputs": _tool_outputs(payload),
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
            f"refined_request_excerpt={_generic_write_report_text(owner, report, 'refined_request')[:2400]}",
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
    _mark_generic_write_consumed_by_gpu1(owner, payload, next_revision)
    consumed_refs = list(getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or [])
    owner.append_heap_exchange_event(
        {
            "kind": "generic_write_consumed_by_gpu1",
            "lane": provider_heap_lane("gpu1_planner"),
            "round": round_id,
            "source_lane": source_lane,
            "source_revision": source_revision,
            "gpu1_revision": next_revision,
            "consumed_generic_write_refs": consumed_refs,
        }
    )
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


def _mark_generic_write_consumed_by_gpu1(
    owner: Any, payload: dict[str, Any], next_revision: int
) -> None:
    gpu1_report = next(
        (
            report
            for report in reversed(getattr(owner, "provider_reports", []) or [])
            if str(report.get("lane") or "") == "gpu1_planner"
            and safe_int(report.get("revision"), default=-1) >= next_revision
            and report.get("passed") is True
            and bool(report.get("provider_work_verified") or report.get("gpu1_primary_workload_valid"))
        ),
        {},
    )
    if not gpu1_report:
        return
    refs = list(getattr(owner, "gpu1_consumed_generic_write_block_ids", []) or [])
    ref_id = _generic_write_ref_id(owner, payload)
    if ref_id and ref_id not in refs:
        refs.append(ref_id)
    owner.gpu1_consumed_generic_write_block_ids = refs
    gpu1_report["consumed_generic_write_refs"] = refs
