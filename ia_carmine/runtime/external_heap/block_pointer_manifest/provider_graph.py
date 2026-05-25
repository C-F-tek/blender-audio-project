"""Provider evidence block graph helpers for external heap manifests."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import report_text_preview
from ia_carmine._shared.provider_work_verification import (
    provider_rejection_record,
    provider_work_status,
)

ROLE_ORDER = {
    "gpu1_planner": 0,
    "gpu0_reviewer_refiner": 1,
    "npu_auditor": 2,
}
EXECUTION_TRUE_PATTERNS = (
    re.compile(
        r"\b(provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)\b\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"[\"'](provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)[\"']\s*:\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(NPU|GPU|provider|workload)[^\n]{0,120}\bperformed\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bperformed\s*=\s*true\b", re.IGNORECASE),
)
EXECUTION_BOOL_KEYS = {
    "provider_execution_performed",
    "gpu0_provider_execution_performed",
    "gpu1_provider_execution_performed",
    "npu_provider_execution_performed",
    "workload_performed",
}
WORKLOAD_CONTAINER_KEYS = {
    "npu_device_workload",
    "gpu_device_workload",
    "device_workload",
    "workload",
}
RESOURCE_MECHANICS_BOOL_KEYS = {
    "resource_mechanics_performed",
    "resource_probe_performed",
    "mechanical_not_static_read",
}
SKIP_KINDS = {
    "gpu1_one_turn_runtime_gate",
    "provider_launch_manifest",
    "provider_role_coexistence",
    "provider_runtime_plan",
    "provider_teamwork_leader_packet",
}
GENERIC_REPORT_ROLES = {"primary", "peer", "micro", "provider", "worker", "auditor"}
PROVIDER_OBSERVED_STATUS_KEYS = (
    "device_detected",
    "model_loaded",
    "health_check_passed",
    "workload_performed",
    "useful_output_produced",
    "provider_work_verified",
)


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def _stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def _normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def _mapping_has_execution_evidence(value: Any, parent_key: str = "") -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in EXECUTION_BOOL_KEYS and _normalize_bool(item):
                return True
            if (
                key_lower == "performed"
                and parent_key.lower() in WORKLOAD_CONTAINER_KEYS
                and _normalize_bool(item)
            ):
                return True
            if _mapping_has_execution_evidence(item, key_text):
                return True
    elif isinstance(value, list):
        return any(_mapping_has_execution_evidence(item, parent_key) for item in value)
    return False


def _provider_execution_evidence(data: dict[str, Any], preview: str) -> bool:
    if "provider_work_verified" in data:
        return _normalize_bool(data.get("provider_work_verified"))
    return _mapping_has_execution_evidence(data) or any(
        pattern.search(preview) for pattern in EXECUTION_TRUE_PATTERNS
    )


def _mapping_has_resource_mechanics(value: Any) -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            if str(key).lower() in RESOURCE_MECHANICS_BOOL_KEYS and _normalize_bool(item):
                return True
            if _mapping_has_resource_mechanics(item):
                return True
    elif isinstance(value, list):
        return any(_mapping_has_resource_mechanics(item) for item in value)
    return False


def _canonical_role(data: dict[str, Any], path: Path) -> tuple[str, str]:
    lane = str(
        data.get("lane")
        or data.get("requirement")
        or data.get("report_kind")
        or data.get("kind")
        or path.stem
    ).lower()
    if "gpu0" in lane:
        role = "gpu0_reviewer_refiner"
        block_type = "review_refinement_block"
    elif "npu" in lane:
        role = "npu_auditor"
        block_type = "audit_block"
    else:
        role = "gpu1_planner"
        block_type = "provider_evidence_block"
    explicit_role = str(data.get("role") or "").strip()
    if explicit_role and explicit_role not in GENERIC_REPORT_ROLES:
        role = explicit_role
    explicit_block_type = str(data.get("block_type") or "").strip()
    if explicit_block_type:
        block_type = explicit_block_type
    return role, block_type


def _provider_sort_key(item: tuple[Path, dict[str, Any]]) -> tuple[int, str]:
    path, data = item
    role, _block_type = _canonical_role(data, path)
    return (ROLE_ORDER.get(role, 99), path.name)


def _provider_items(provider_dir: Path) -> list[tuple[Path, dict[str, Any]]]:
    if not provider_dir.exists():
        return []
    items: list[tuple[Path, dict[str, Any]]] = []
    for path in provider_dir.glob("*.json"):
        data = _read_json(path)
        if _skip_provider_item(path, data):
            continue
        items.append((path, data))
    return sorted(items, key=_provider_sort_key)


def _skip_provider_item(path: Path, data: dict[str, Any]) -> bool:
    name = path.name
    if str(data.get("kind") or "") in SKIP_KINDS:
        return True
    if name.startswith(("provider_launch_manifest", "provider_runtime_plan")):
        return True
    if name.startswith("provider_teamwork_leader_packet"):
        return True
    if "provider_replight" in name or _normalize_bool(data.get("replight_mode")):
        return True
    return False


def _preview_text(repo_root: Path, data: dict[str, Any], max_block_chars: int) -> str:
    text = str(report_text_preview(repo_root, data).get("text") or "")
    if not text:
        text = json.dumps(data, indent=2, ensure_ascii=False)
    if max_block_chars > 0 and len(text) > max_block_chars:
        return text[:max_block_chars] + "\n...[truncated]\n"
    return text


def _append_block(blocks: list[dict[str, Any]], block: dict[str, Any]) -> None:
    if not any(existing.get("block_id") == block.get("block_id") for existing in blocks):
        blocks.append(block)


def _provider_role_observed(status: dict[str, Any]) -> bool:
    return any(_normalize_bool(status.get(key)) for key in PROVIDER_OBSERVED_STATUS_KEYS)


def provider_blocks(repo_root: Path, run_dir: Path, max_block_chars: int) -> list[dict[str, Any]]:
    """Build provider evidence blocks as a navigable GPU1 -> GPU0 -> NPU graph.

    Proposal chunks remain the product path. When a run stops before producing a
    proposal, provider reports still need pointer edges so the next heap run can
    resume from the failed evidence chain instead of treating the heap as linear
    stdout.
    """
    blocks: list[dict[str, Any]] = []
    previous_id = ""
    latest_gpu1_id = ""
    provider_dir = run_dir / "provider_teamwork"
    for index, (path, data) in enumerate(_provider_items(provider_dir), start=1):
        role, block_type = _canonical_role(data, path)
        lane = _lane_for_role(role)
        work_status = provider_work_status(lane=lane, report=data, default_role=role)
        verified = bool(work_status["provider_work_verified"])
        observed = _provider_role_observed(work_status)
        sidecar_role = role in {"gpu0_reviewer_refiner", "npu_auditor"}
        if not verified and not (sidecar_role and observed):
            continue
        if not verified and sidecar_role:
            block_type = "observed_invalid_provider_evidence"
        text = _preview_text(repo_root, data, max_block_chars)
        block_id = str(data.get("provider_block_id") or data.get("block_id") or "").strip()
        if not block_id:
            block_id = _stable_id("provider", f"{_repo_rel(repo_root, path)}:{role}:{index}")
        proposal_block_id = str(data.get("proposal_block_id") or "")
        refines_id = str(data.get("refines_block_id") or proposal_block_id)
        if role in {"gpu0_reviewer_refiner", "npu_auditor"} and not refines_id:
            refines_id = str(
                data.get("review_target_pointer")
                or data.get("checked_block_id")
                or data.get("reviewed_gpu1_block_id")
                or latest_gpu1_id
                or previous_id
            )
        resume_id = str(data.get("resume_from_block_id") or proposal_block_id or refines_id)
        if not resume_id and role != "gpu1_planner":
            resume_id = latest_gpu1_id or previous_id
        block = {
            "block_id": block_id,
            "block_type": block_type,
            "role": role,
            "step_index": index,
            "source_path": _repo_rel(repo_root, path),
            "proposal_block_id": proposal_block_id,
            "previous_block_id": str(data.get("previous_block_id") or previous_id),
            "next_block_id": str(data.get("next_block_id") or ""),
            "refines_block_id": refines_id,
            "resume_from_block_id": resume_id,
            "pointer_action": data.get("pointer_action"),
            "target_files": data.get("target_files") if isinstance(data.get("target_files"), list) else [],
            "decision": data.get("decision"),
            "exit_decision": data.get("exit_decision"),
            "quality_passed": data.get("passed"),
            "provider_execution_performed": bool(verified),
            "provider_stage": work_status["provider_stage"],
            "device_detected": work_status["device_detected"],
            "model_loaded": work_status["model_loaded"],
            "health_check_passed": work_status["health_check_passed"],
            "workload_performed": work_status["workload_performed"],
            "useful_output_produced": work_status["useful_output_produced"],
            "provider_work_verified": verified,
            "provider_role_counted": verified,
            "provider_role_observed": observed or verified,
            "provider_role_observation_status": "verified" if verified else "observed_invalid",
            "provider_rejection_reason": "" if verified else work_status["provider_rejection_reason"],
            "role_rejection_reason": "" if verified else work_status["role_rejection_reason"],
            "invalid_role": bool(not verified and observed),
            "sidecar_invalid": bool(not verified and sidecar_role),
            "sidecar_incongruent": bool(
                str(
                    data.get("gpu0_effective_decision")
                    or data.get("gpu0_decision")
                    or ""
                ).lower()
                == "incongruent"
            ),
            "gpu0_review_not_required": role == "gpu1_planner",
            "gpu0_secondary_schema_valid": data.get("gpu0_secondary_schema_valid"),
            "gpu0_checked_current_packet": data.get("gpu0_checked_current_packet"),
            "role_decision": data.get("role_decision"),
            "gpu0_decision": data.get("gpu0_decision"),
            "gpu0_effective_decision": data.get("gpu0_effective_decision"),
            "checked_block_id": data.get("checked_block_id"),
            "checked_gpu1_revision": data.get("checked_gpu1_revision"),
            "reviewed_gpu1_block_id": data.get("reviewed_gpu1_block_id"),
            "reviewed_revision": data.get("reviewed_revision"),
            "review_target_pointer": data.get("review_target_pointer") or refines_id,
            "gpu1_closure_decision_packet_fingerprint": data.get(
                "gpu1_closure_decision_packet_fingerprint"
            ),
            "expected_packet_fingerprint": data.get("expected_packet_fingerprint"),
            "reviewed_packet_fingerprint": data.get("reviewed_packet_fingerprint"),
            "gpu0_review_invalid_requires_gpu1_retry": data.get(
                "gpu0_review_invalid_requires_gpu1_retry"
            ),
            "native_tool_call_count": data.get("native_tool_call_count", 0),
            "npu_peer_evidence_verified": data.get("npu_peer_evidence_verified"),
            "npu_native_tool_loop_error": data.get("npu_native_tool_loop_error"),
            "npu_native_tool_loop_required": data.get("npu_native_tool_loop_required"),
            "npu_peer_followup_required": data.get("npu_peer_followup_required"),
            "resource_mechanics_performed": _mapping_has_resource_mechanics(data),
            "resource_probe_performed": _normalize_bool(data.get("resource_probe_performed")),
            "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if text else "",
            "preview": text,
            "pointer_contract": {
                "product_contract": True,
                "decision_recovery": True,
                "navigation_role": (
                    "sidecar_audit_not_closer"
                    if role == "npu_auditor"
                    else "provider_evidence_chain"
                ),
                "closure_owner": role == "gpu1_planner",
                "primary_closer": role == "gpu1_planner",
                "sidecar_evidence": role in {"gpu0_reviewer_refiner", "npu_auditor"},
                "npu_sidecar_status": (
                    "evidence_ready_non_closer" if role == "npu_auditor" else ""
                ),
                "can_continue_to_next": True,
                "can_backrefine": role in {"gpu0_reviewer_refiner", "npu_auditor"},
                "requires_review": role != "gpu0_reviewer_refiner",
            },
        }
        if previous_id:
            for existing in blocks:
                if existing.get("block_id") == previous_id and not existing.get("next_block_id"):
                    existing["next_block_id"] = block_id
        _append_block(blocks, block)
        if role == "gpu1_planner":
            latest_gpu1_id = block_id
        previous_id = block_id
    return blocks


def provider_rejections(repo_root: Path, run_dir: Path) -> list[dict[str, Any]]:
    provider_dir = run_dir / "provider_teamwork"
    rejections: list[dict[str, Any]] = []
    for path, data in _provider_items(provider_dir):
        role, _block_type = _canonical_role(data, path)
        lane = _lane_for_role(role)
        status = provider_work_status(lane=lane, report=data, default_role=role)
        if status["provider_work_verified"]:
            continue
        record = provider_rejection_record(
            path=_repo_rel(repo_root, path),
            lane=lane,
            report=data,
            default_role=role,
        )
        observed = _provider_role_observed(status)
        record["provider_role_observed"] = observed
        record["provider_role_observation_status"] = (
            "observed_invalid" if observed else "not_observed"
        )
        record["invalid_role"] = observed
        rejections.append(record)
    return rejections


def _lane_for_role(role: str) -> str:
    if role == "gpu0_reviewer_refiner":
        return "gpu0_peer"
    if role == "npu_auditor":
        return "npu_micro_task_auditor"
    return "gpu1_planner"
