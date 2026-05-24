"""GPU1 closure decision packet helpers.

GPU1 is the only closure owner. GPU0 may review only the current packet
identified by GPU1 block id and revision; generic provider prose remains
evidence and never becomes a closure decision.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from ia_carmine._shared.file_backed_transport import report_text
from ia_carmine.runtime.heap_gate.runtime_common import Any

GPU1_PACKET_KIND = "gpu1_closure_decision_packet"
GPU1_CLOSURE_DECISIONS = {
    "finalize_product",
    "needs_refine",
    "blocked_continuation",
    "no_patchable_target",
}
GPU1_DECISION_MISSING = "gpu1_decision_missing"


def normalize_gpu1_decision(value: Any) -> str:
    raw = str(value or "").strip().lower().replace("-", "_")
    if raw in {"finalize_product", "finalize", "final_product_approved", "ready"}:
        return "finalize_product"
    if raw in {"needs_refine", "needs_gpu0_refine", "gpu0_refine_required", "refine"}:
        return "needs_refine"
    if raw in {"blocked_continuation", "deferred_to_resume", "continuation_required"}:
        return "blocked_continuation"
    if raw in {"no_patchable_target", "no_more_action", "no_patchable"}:
        return "no_patchable_target"
    if raw == GPU1_DECISION_MISSING:
        return GPU1_DECISION_MISSING
    return ""


def derive_gpu1_decision(
    *,
    quality_passed: bool,
    exit_decision: str = "",
    pointer_action: str = "",
    reject_reasons: list[str] | tuple[str, ...] | None = None,
    response_text: str = "",
) -> str:
    haystack = "\n".join(
        [
            str(exit_decision or ""),
            str(pointer_action or ""),
            "\n".join(str(item) for item in (reject_reasons or [])),
            str(response_text or ""),
        ]
    ).upper()
    if quality_passed:
        return "finalize_product"
    if "NO_PATCHABLE_TARGET" in haystack or "NO PATCHABLE TARGET" in haystack:
        return "no_patchable_target"
    if any(
        marker in haystack
        for marker in ("BLOCKED_CONTINUATION", "DEFERRED_TO_RESUME", "CONTINUATION_REQUIRED")
    ):
        return "blocked_continuation"
    return "needs_refine"


def build_gpu1_closure_decision_packet(
    *,
    gpu1_block_id: str,
    gpu1_revision: Any,
    gpu1_decision: str,
    target_files: list[Any] | tuple[Any, ...] | None = None,
    quality_passed: bool = False,
    reject_reasons: list[Any] | tuple[Any, ...] | None = None,
    evidence_refs: list[Any] | tuple[Any, ...] | None = None,
    generic_write_refs: list[Any] | tuple[Any, ...] | None = None,
    consumed_generic_write_refs: list[Any] | tuple[Any, ...] | None = None,
    exit_decision: str = "",
    pointer_action: str = "",
    refines_block_id: str = "",
    consumed_gpu0_block_id: str = "",
    consumed_gpu0_block_ids: list[Any] | tuple[Any, ...] | None = None,
    consumed_npu_block_ids: list[Any] | tuple[Any, ...] | None = None,
    response_text: str = "",
    source: str = "",
) -> dict[str, Any]:
    decision = normalize_gpu1_decision(gpu1_decision)
    if decision == GPU1_DECISION_MISSING:
        decision = ""
    payload = {
        "schema_version": 1,
        "kind": GPU1_PACKET_KIND,
        "gpu1_decision": decision,
        "gpu1_block_id": str(gpu1_block_id or ""),
        "gpu1_revision": str(gpu1_revision if gpu1_revision is not None else ""),
        "target_files": _string_list(target_files),
        "quality_passed": bool(quality_passed),
        "reject_reasons": _unique_strings(reject_reasons),
        "evidence_refs": _unique_strings(evidence_refs),
        "generic_write_refs": _unique_strings(generic_write_refs),
        "consumed_generic_write_refs": _unique_strings(consumed_generic_write_refs),
        "generic_write_used_as_decision": False,
        "exit_decision": str(exit_decision or ""),
        "pointer_action": str(pointer_action or ""),
        "refines_block_id": str(refines_block_id or ""),
        "consumed_gpu0_block_id": str(consumed_gpu0_block_id or ""),
        "consumed_gpu0_block_ids": _unique_strings(consumed_gpu0_block_ids),
        "consumed_npu_block_ids": _unique_strings(consumed_npu_block_ids),
        "response_text_sha256": _sha256(response_text),
        "source": str(source or ""),
    }
    payload["packet_fingerprint"] = gpu1_packet_fingerprint(payload)
    payload["valid"] = gpu1_decision_packet_valid(payload)
    if not payload["valid"]:
        payload["packet_errors"] = gpu1_decision_packet_errors(payload)
    return payload


def packet_from_report(
    report: dict[str, Any],
    *,
    source: str = "",
    repo_root: Path | str | None = None,
) -> dict[str, Any]:
    text = str(report_text(repo_root, report).get("text") or "")
    target_files = report.get("target_files") if isinstance(report.get("target_files"), list) else []
    reject_reasons = [
        report.get("gpu1_primary_block_reason"),
        report.get("provider_activity_classification"),
        report.get("provider_rejection_reason"),
        report.get("product_blocked_reason"),
    ]
    quality_passed = bool(
        report.get("passed")
        and report.get("operational_provider_activity")
        and target_files
        and "EXIT_DECISION=NO_PATCHABLE_TARGET" not in text.upper()
    )
    decision = derive_gpu1_decision(
        quality_passed=quality_passed,
        exit_decision=str(report.get("exit_decision") or ""),
        pointer_action=str(report.get("pointer_action") or ""),
        reject_reasons=[str(item) for item in reject_reasons if str(item or "").strip()],
        response_text=text,
    )
    evidence_refs = [
        report.get("output"),
        report.get("provider_block_id"),
        report.get("proposal_block_id"),
    ]
    generic_refs = []
    if str(report.get("leader_source") or "") == "generic_write":
        generic_refs.append(report.get("output"))
    return build_gpu1_closure_decision_packet(
        gpu1_block_id=str(
            report.get("proposal_block_id")
            or report.get("block_id")
            or report.get("provider_block_id")
            or ""
        ),
        gpu1_revision=report.get("revision") if report.get("revision") is not None else "",
        gpu1_decision=decision,
        target_files=target_files,
        quality_passed=quality_passed,
        reject_reasons=[item for item in reject_reasons if str(item or "").strip()],
        evidence_refs=evidence_refs,
        generic_write_refs=generic_refs,
        consumed_generic_write_refs=report.get("consumed_generic_write_refs")
        if isinstance(report.get("consumed_generic_write_refs"), list)
        else [],
        exit_decision=str(report.get("exit_decision") or ""),
        pointer_action=str(report.get("pointer_action") or ""),
        refines_block_id=str(report.get("refines_block_id") or ""),
        response_text=text,
        source=source or "provider_report",
    )


def extract_gpu1_closure_decision_packet(payload: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(payload, dict):
        return {}
    packet = payload.get("gpu1_closure_decision_packet")
    if isinstance(packet, dict):
        return packet
    if str(payload.get("kind") or "") == GPU1_PACKET_KIND:
        return payload
    return {}


def gpu1_decision_packet_valid(packet: dict[str, Any] | None) -> bool:
    return not gpu1_decision_packet_errors(packet)


def gpu1_decision_packet_errors(packet: dict[str, Any] | None) -> list[str]:
    if not isinstance(packet, dict):
        return ["gpu1_closure_decision_packet_missing"]
    errors: list[str] = []
    if str(packet.get("kind") or "") != GPU1_PACKET_KIND:
        errors.append("gpu1_closure_decision_packet_kind_invalid")
    if normalize_gpu1_decision(packet.get("gpu1_decision")) not in GPU1_CLOSURE_DECISIONS:
        errors.append("gpu1_decision_invalid")
    if not str(packet.get("gpu1_block_id") or "").strip():
        errors.append("gpu1_block_id_missing")
    if not str(packet.get("gpu1_revision") or "").strip():
        errors.append("gpu1_revision_missing")
    if packet.get("generic_write_used_as_decision") is True:
        errors.append("generic_write_used_as_gpu1_decision")
    return errors


def gpu1_packet_fingerprint(packet: dict[str, Any] | None) -> str:
    if not isinstance(packet, dict):
        return ""
    payload = {
        "gpu1_decision": normalize_gpu1_decision(packet.get("gpu1_decision")),
        "gpu1_block_id": str(packet.get("gpu1_block_id") or ""),
        "gpu1_revision": str(packet.get("gpu1_revision") or ""),
        "target_files": _unique_strings(packet.get("target_files")),
        "quality_passed": packet.get("quality_passed") is True,
        "reject_reasons": _unique_strings(packet.get("reject_reasons")),
        "evidence_refs": _unique_strings(packet.get("evidence_refs")),
        "generic_write_refs": _unique_strings(packet.get("generic_write_refs")),
        "consumed_generic_write_refs": _unique_strings(packet.get("consumed_generic_write_refs")),
        "exit_decision": str(packet.get("exit_decision") or ""),
        "pointer_action": str(packet.get("pointer_action") or ""),
        "refines_block_id": str(packet.get("refines_block_id") or ""),
        "consumed_gpu0_block_id": str(packet.get("consumed_gpu0_block_id") or ""),
        "consumed_gpu0_block_ids": _unique_strings(packet.get("consumed_gpu0_block_ids")),
        "consumed_npu_block_ids": _unique_strings(packet.get("consumed_npu_block_ids")),
        "response_text_sha256": str(packet.get("response_text_sha256") or ""),
        "source": str(packet.get("source") or ""),
    }
    encoded = json.dumps(payload, ensure_ascii=True, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(encoded.encode("utf-8", errors="replace")).hexdigest()


def gpu1_packets_equivalent(
    left: dict[str, Any] | None,
    right: dict[str, Any] | None,
) -> bool:
    left_fingerprint = gpu1_packet_fingerprint(left)
    right_fingerprint = gpu1_packet_fingerprint(right)
    return bool(left_fingerprint and right_fingerprint and left_fingerprint == right_fingerprint)


def _string_list(value: list[Any] | tuple[Any, ...] | None) -> list[str]:
    if not isinstance(value, (list, tuple)):
        return []
    return [str(item).strip() for item in value if str(item).strip()]


def _unique_strings(value: list[Any] | tuple[Any, ...] | None) -> list[str]:
    out: list[str] = []
    for item in _string_list(value):
        if item not in out:
            out.append(item)
    return out


def _sha256(text: str) -> str:
    if not text:
        return ""
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
