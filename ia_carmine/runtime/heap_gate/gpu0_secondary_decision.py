from __future__ import annotations

import json
from typing import Any

from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    extract_gpu1_closure_decision_packet,
    gpu1_decision_packet_valid,
    gpu1_packet_fingerprint,
)

GPU0_ROLE = "secondary_congruence_veto"
GPU0_DECISIONS = {"congruent", "veto", "refine_required", "incongruent"}


def normalize_gpu0_decision(value: Any) -> str:
    raw = str(value or "").strip().lower().replace("-", "_")
    if raw in {"congruent", "agree", "agree_close", "accept", "accepted", "pass"}:
        return "congruent"
    if raw in {"veto", "veto_with_reason", "blocked", "block"}:
        return "veto"
    if raw in {
        "refine",
        "refine_once",
        "refine_required",
        "evidence_request",
        "needs_refine",
        "requires_refine",
        "reject_until_concrete_repo_relative_delta",
    }:
        return "refine_required"
    if raw in {"incongruent", "incongruence", "congruence_check_failed", "mismatch"}:
        return "incongruent"
    return ""


def gpu0_role_decision(decision: str) -> str:
    normalized = normalize_gpu0_decision(decision)
    if normalized == "congruent":
        return "agree_close"
    if normalized == "veto":
        return "veto_with_reason"
    if normalized in {"refine_required", "incongruent"}:
        return "refine_once"
    return ""


def parse_gpu0_secondary_response(
    text: str,
    *,
    fallback_block_id: str = "",
    fallback_revision: str = "",
) -> dict[str, Any]:
    raw_text = str(text or "").strip()
    parsed = _parse_json_object(raw_text)
    if not isinstance(parsed, dict):
        return invalid_gpu0_secondary_decision(
            raw_text,
            fallback_block_id=fallback_block_id,
            fallback_revision=fallback_revision,
            reason="gpu0_secondary_schema_invalid",
        )

    decision = normalize_gpu0_decision(parsed.get("gpu0_decision") or parsed.get("decision"))
    if decision not in GPU0_DECISIONS:
        return invalid_gpu0_secondary_decision(
            raw_text,
            fallback_block_id=fallback_block_id,
            fallback_revision=fallback_revision,
            reason="gpu0_secondary_decision_invalid",
        )

    veto_reasons = _string_list(parsed.get("veto_reasons"))
    incongruence_reasons = _string_list(
        parsed.get("incongruence_reasons") or parsed.get("congruence_failures")
    )
    if decision == "veto" and not veto_reasons:
        veto_reasons = ["gpu0_veto_without_reasons"]
    if decision == "incongruent" and not incongruence_reasons:
        incongruence_reasons = ["gpu0_incongruent_without_reasons"]

    payload = {
        "gpu0_secondary_schema_valid": True,
        "gpu0_role": GPU0_ROLE,
        "gpu0_decision": decision,
        "gpu0_model_decision": decision,
        "gpu0_effective_decision": decision,
        "role_decision": gpu0_role_decision(decision),
        "checked_block_id": str(
            parsed.get("checked_block_id")
            or parsed.get("reviewed_gpu1_block_id")
            or parsed.get("refines_block_id")
            or fallback_block_id
            or ""
        ),
        "checked_gpu1_revision": str(
            parsed.get("checked_gpu1_revision")
            or parsed.get("review_for_gpu1_cycle")
            or fallback_revision
            or ""
        ),
        "missing_required_sections": _string_list(
            parsed.get("missing_required_sections") or parsed.get("missing_delta_sections")
        ),
        "incongruence_reasons": incongruence_reasons,
        "veto_reasons": veto_reasons,
        "required_gpu1_next_action": str(
            parsed.get("required_gpu1_next_action")
            or parsed.get("next_gpu1_action")
            or _default_next_action(decision)
        ),
        "free_text_evidence": raw_text,
        "free_text_used_as_product": False,
        "free_text_used_as_decision": False,
    }
    return payload


def bind_gpu0_secondary_to_gpu1_packet(
    payload: dict[str, Any],
    packet_source: dict[str, Any] | None,
) -> dict[str, Any]:
    """Bind a GPU0 decision to the current GPU1 closure packet.

    GPU0 may veto/refine only the packet identified by `gpu1_block_id` and
    `gpu1_revision`. Reasons that are not present in the packet evidence are
    retained as evidence but cannot become a final veto.
    """
    packet = extract_gpu1_closure_decision_packet(packet_source or {})
    result = dict(payload)
    result["gpu1_closure_decision_packet_present"] = bool(packet)
    result["gpu1_closure_decision_packet_valid"] = gpu1_decision_packet_valid(packet)
    result["gpu1_closure_decision_packet_fingerprint"] = gpu1_packet_fingerprint(packet)
    result["expected_gpu1_block_id"] = str(packet.get("gpu1_block_id") or "")
    result["expected_gpu1_revision"] = str(packet.get("gpu1_revision") or "")
    if not packet or not result["gpu1_closure_decision_packet_valid"]:
        return _invalidate_bound_decision(
            result,
            "gpu0_veto_not_allowed_without_gpu1_decision",
        )

    checked_block = str(result.get("checked_block_id") or "")
    checked_revision = str(result.get("checked_gpu1_revision") or "")
    if checked_block != result["expected_gpu1_block_id"] or checked_revision != result["expected_gpu1_revision"]:
        return _invalidate_bound_decision(result, "gpu0_checked_wrong_gpu1_packet")

    result["gpu0_checked_current_packet"] = True
    model_decision = normalize_gpu0_decision(
        result.get("gpu0_model_decision") or result.get("gpu0_decision")
    )
    result["gpu0_model_decision"] = model_decision
    if model_decision in {"veto", "refine_required", "incongruent"}:
        unanchored = _unanchored_reasons(result, packet)
        result["gpu0_unanchored_reasons"] = unanchored
        if unanchored and not _has_anchored_blocking_reason(result, packet):
            result["gpu0_decision_override_reason"] = "gpu0_unanchored_reason"
            result["gpu0_effective_decision"] = "congruent"
            result["gpu0_decision"] = "congruent"
            result["role_decision"] = "agree_close"
            result["required_gpu1_next_action"] = (
                "GPU0 raised only unanchored reasons; CPU ignores them as final veto."
            )
            veto = _string_list(result.get("veto_reasons"))
            if "gpu0_unanchored_reason" not in veto:
                veto.append("gpu0_unanchored_reason")
            result["veto_reasons"] = veto
            return result
    result["gpu0_effective_decision"] = normalize_gpu0_decision(result.get("gpu0_decision"))
    result["role_decision"] = gpu0_role_decision(str(result.get("gpu0_effective_decision") or ""))
    return result


def invalid_gpu0_secondary_decision(
    raw_text: str,
    *,
    fallback_block_id: str = "",
    fallback_revision: str = "",
    reason: str,
) -> dict[str, Any]:
    return {
        "gpu0_secondary_schema_valid": False,
        "gpu0_role": GPU0_ROLE,
        "gpu0_decision": "refine_required",
        "gpu0_model_decision": "",
        "gpu0_effective_decision": "refine_required",
        "role_decision": "refine_once",
        "checked_block_id": str(fallback_block_id or ""),
        "checked_gpu1_revision": str(fallback_revision or ""),
        "missing_required_sections": [],
        "incongruence_reasons": [],
        "veto_reasons": [reason],
        "required_gpu1_next_action": "GPU1 must request a valid structured GPU0 congruence/veto decision.",
        "free_text_evidence": str(raw_text or "").strip(),
        "free_text_used_as_product": False,
        "free_text_used_as_decision": False,
    }


def gpu0_secondary_decision_text(payload: dict[str, Any]) -> str:
    compact = {
        "gpu0_role": payload.get("gpu0_role") or GPU0_ROLE,
        "gpu0_secondary_schema_valid": payload.get("gpu0_secondary_schema_valid") is True,
        "gpu0_decision": payload.get("gpu0_decision") or "",
        "gpu0_model_decision": payload.get("gpu0_model_decision") or "",
        "gpu0_effective_decision": payload.get("gpu0_effective_decision") or payload.get("gpu0_decision") or "",
        "role_decision": payload.get("role_decision") or "",
        "checked_block_id": payload.get("checked_block_id") or "",
        "checked_gpu1_revision": payload.get("checked_gpu1_revision") or "",
        "expected_gpu1_block_id": payload.get("expected_gpu1_block_id") or "",
        "expected_gpu1_revision": payload.get("expected_gpu1_revision") or "",
        "gpu1_closure_decision_packet_present": payload.get(
            "gpu1_closure_decision_packet_present"
        ) is True,
        "gpu1_closure_decision_packet_valid": payload.get(
            "gpu1_closure_decision_packet_valid"
        ) is True,
        "gpu0_checked_current_packet": payload.get("gpu0_checked_current_packet") is True,
        "gpu0_unanchored_reasons": payload.get("gpu0_unanchored_reasons") or [],
        "missing_required_sections": payload.get("missing_required_sections") or [],
        "incongruence_reasons": payload.get("incongruence_reasons") or [],
        "veto_reasons": payload.get("veto_reasons") or [],
        "required_gpu1_next_action": payload.get("required_gpu1_next_action") or "",
        "free_text_used_as_product": False,
        "free_text_used_as_decision": False,
    }
    return "GPU0_SECONDARY_DECISION:\n" + json.dumps(compact, ensure_ascii=False, indent=2)


def gpu0_secondary_reason(payload: dict[str, Any]) -> str:
    for key in ("veto_reasons", "incongruence_reasons", "missing_required_sections"):
        values = _string_list(payload.get(key))
        if values:
            return "; ".join(values[:4])
    return str(payload.get("required_gpu1_next_action") or "").strip()


def _invalidate_bound_decision(payload: dict[str, Any], reason: str) -> dict[str, Any]:
    result = dict(payload)
    result["gpu0_secondary_schema_valid"] = False
    result["gpu0_decision_override_reason"] = reason
    result["gpu0_effective_decision"] = "refine_required"
    result["gpu0_decision"] = "refine_required"
    result["role_decision"] = "refine_once"
    result["gpu0_checked_current_packet"] = False
    veto = _string_list(result.get("veto_reasons"))
    if reason not in veto:
        veto.append(reason)
    result["veto_reasons"] = veto
    result["required_gpu1_next_action"] = (
        "GPU1 must publish a valid current gpu1_closure_decision_packet before GPU0 can evaluate."
    )
    return result


def _unanchored_reasons(payload: dict[str, Any], packet: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    for key in ("veto_reasons", "incongruence_reasons", "missing_required_sections"):
        reasons.extend(_string_list(payload.get(key)))
    anchors = _packet_anchor_texts(packet)
    unanchored: list[str] = []
    for reason in reasons:
        if not _reason_is_anchored(reason, anchors) and reason not in unanchored:
            unanchored.append(reason)
    return unanchored


def _has_anchored_blocking_reason(payload: dict[str, Any], packet: dict[str, Any]) -> bool:
    anchors = _packet_anchor_texts(packet)
    for key in ("veto_reasons", "incongruence_reasons", "missing_required_sections"):
        for reason in _string_list(payload.get(key)):
            if _reason_is_anchored(reason, anchors):
                return True
    return False


def _packet_anchor_texts(packet: dict[str, Any]) -> list[str]:
    anchors = [
        str(packet.get("gpu1_block_id") or ""),
        str(packet.get("gpu1_revision") or ""),
        str(packet.get("gpu1_decision") or ""),
        str(packet.get("exit_decision") or ""),
        str(packet.get("pointer_action") or ""),
    ]
    for key in ("target_files", "reject_reasons", "evidence_refs", "generic_write_refs"):
        anchors.extend(_string_list(packet.get(key)))
    return [item.lower() for item in anchors if item.strip()]


def _reason_is_anchored(reason: str, anchors: list[str]) -> bool:
    lowered = str(reason or "").strip().lower()
    if not lowered:
        return True
    return any(lowered == anchor or lowered in anchor or anchor in lowered for anchor in anchors)


def _default_next_action(decision: str) -> str:
    if decision == "congruent":
        return "GPU1 may continue only if CPU validators and product gates pass."
    if decision == "veto":
        return "GPU1 must stop this candidate and produce a new concrete proposal."
    if decision == "incongruent":
        return "GPU1 must reconcile the incongruence before closure."
    return "GPU1 must refine the current proposal before closure."


def _string_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return []


def _parse_json_object(text: str) -> dict[str, Any] | None:
    stripped = text.strip()
    if not stripped:
        return None
    if stripped.startswith("```"):
        stripped = _strip_fence(stripped)
    try:
        parsed = json.loads(stripped)
        return parsed if isinstance(parsed, dict) else None
    except json.JSONDecodeError:
        pass
    decoder = json.JSONDecoder()
    for index, char in enumerate(stripped):
        if char != "{":
            continue
        try:
            parsed, _end = decoder.raw_decode(stripped[index:])
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            return parsed
    return None


def _strip_fence(text: str) -> str:
    lines = text.strip().splitlines()
    if lines and lines[0].strip().startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()
