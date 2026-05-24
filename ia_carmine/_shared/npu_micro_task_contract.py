from __future__ import annotations

import json
from pathlib import Path

from ia_carmine._shared.file_backed_transport import report_text_preview

NPU_MICRO_TASK_KINDS = (
    "section_presence_audit",
    "target_reference_audit",
    "validation_command_audit",
    "risk_guardrail_audit",
)
NPU_MICRO_DECISIONS = (
    "NPU_DONE",
    "NPU_REJECT",
    "NPU_NO_ACTION",
    "NPU_TIMEOUT_BOUNDARY",
)


def render_leader_peer_prompt(request: str, leader_packet: dict) -> str:
    if not leader_packet:
        return request
    contract = leader_packet.get("same_heap_teamwork_contract")
    contract_text = "; ".join(str(item) for item in contract[:4]) if isinstance(contract, list) else ""
    propagation = leader_packet.get("propagation_contract")
    propagation_text = "; ".join(str(item) for item in propagation[:4]) if isinstance(propagation, list) else ""
    pointer = leader_packet.get("pointer_contract") if isinstance(leader_packet.get("pointer_contract"), dict) else {}
    time_counter = leader_packet.get("time_counter_contract") if isinstance(leader_packet.get("time_counter_contract"), dict) else {}
    return "\n".join(
        part
        for part in (
            "NPU peer micro lane. Consume the GPU1 primary advisor leader packet.",
            "SIDECAR_SCOPE_MODE: packet_review_only",
            "SCOPE_RULE: audit only the current GPU1 packet; do not explore broadly, synthesize a final product, or propose a complete alternate plan.",
            "OPERATOR_REQUEST: omitted_when_leader_packet_present",
            f"GPU1_LEADER_ROLE: {leader_packet.get('role')}",
            f"SAME_HEAP_TEAMWORK_CONTRACT: {contract_text}",
            f"HEAP_UNIVERSE_CONTRACT: {leader_packet.get('heap_universe_contract')}",
            f"STARTUP_CONTEXT_PLANE: {leader_packet.get('startup_context_plane')}",
            f"POINTER_CONTRACT: {pointer}",
            f"TIME_COUNTER_CONTRACT: {time_counter}",
            f"PROPAGATION_CONTRACT: {propagation_text}",
            f"SOURCE_PATH_ALLOWLIST_CONTRACT: {str(leader_packet.get('source_allowlist_contract') or '')[:700]}",
            f"GPU1_REVISION_FEEDBACK: {str(leader_packet.get('revision_feedback') or '')[:300]}",
        )
        if part.strip()
    )


def select_npu_micro_task(request: str, leader_packet: dict, task_preview: str) -> str:
    if leader_packet:
        request = ""
        task_preview = ""
    text = "\n".join(
        (
            request or "",
            task_preview or "",
            json.dumps(leader_packet, ensure_ascii=False)[:2500] if leader_packet else "",
        )
    ).lower()
    if any(marker in text for marker in ("target_files", "target files", "repo-relative", "source path")):
        return "target_reference_audit"
    if any(marker in text for marker in ("validation_commands", "validation commands", "py_compile", "pytest")):
        return "validation_command_audit"
    if any(marker in text for marker in ("risks", "guardrail", "forbidden", "output/**")):
        return "risk_guardrail_audit"
    return "section_presence_audit"


def render_npu_micro_prompt(
    request: str,
    leader_packet: dict,
    task_preview: str,
    micro_task_kind: str,
) -> str:
    leader_context = render_leader_peer_prompt(request, leader_packet)
    request_context = "" if leader_packet else (request or "")[:900]
    task_context = "" if leader_packet else (task_preview or "")[:900]
    return "\n".join(
        [
            "IA-Carmine NPU bounded micro-task lane.",
            "You are not the primary planner and you do not write a patch.",
            "SIDECAR_SCOPE_MODE=packet_review_only",
            "Audit only the current GPU1 leader packet. Do not perform broad exploration, final synthesis, or alternate full planning.",
            "Perform exactly one closed textual micro-audit.",
            "Allowed MICRO_TASK values: " + ",".join(NPU_MICRO_TASK_KINDS),
            f"MICRO_TASK={micro_task_kind}",
            "Required output schema, exactly these keys on separate lines:",
            f"MICRO_TASK={micro_task_kind}",
            "CHECKED=<short item checked>",
            "FINDINGS=<0-5 compact findings>",
            "DECISION=NPU_DONE|NPU_REJECT|NPU_NO_ACTION|NPU_TIMEOUT_BOUNDARY",
            "REASON=<short reason>",
            "If context is insufficient, return DECISION=NPU_NO_ACTION immediately.",
            "Do not continue searching and do not produce long prose.",
            "REQUEST_CONTEXT:",
            request_context,
            "TASK_PREVIEW:",
            task_context,
            "LEADER_PACKET_CONTEXT:",
            leader_context[:1200],
        ]
    )


def infer_npu_decision(npu_tool_loop: dict, role_response: dict) -> str:
    response = _npu_findings_text(npu_tool_loop, role_response)
    parsed = _extract_npu_decision(response)
    if parsed:
        return parsed
    classification = str(npu_tool_loop.get("classification") or "").lower()
    if "timeout" in classification:
        return "NPU_TIMEOUT_BOUNDARY"
    if npu_tool_loop.get("native_tool_loop_performed"):
        return "NPU_DONE"
    if classification in {"openvino_native_tool_not_selected", "openvino_tool_loop_model_dir_unconfigured"}:
        return "NPU_NO_ACTION"
    if npu_tool_loop.get("errors"):
        return "NPU_REJECT"
    return "NPU_NO_ACTION"


def schema_response_text(
    micro_task_kind: str,
    decision: str,
    role_response: dict,
    device_workload: dict,
    npu_tool_loop: dict,
) -> str:
    findings = _npu_findings_text(npu_tool_loop, role_response).strip()
    if not findings:
        findings = "no actionable context available"
    reason = str(npu_tool_loop.get("classification") or role_response.get("role_decision") or "bounded_micro_audit")
    lines = [
        f"MICRO_TASK={micro_task_kind}",
        "CHECKED=leader_packet_or_gpu1_delta",
        "FINDINGS=" + findings[:700].replace("\n", " "),
        f"DECISION={decision}",
        f"REASON={reason[:240]}",
    ]
    if device_workload.get("requested"):
        lines.append(
            "NPU_DEVICE_WORKLOAD="
            f"performed={device_workload.get('performed')};passed={device_workload.get('passed')};"
            f"iterations={device_workload.get('iterations')};seconds={device_workload.get('seconds')}"
        )
    return "\n".join(lines)


def _npu_findings_text(npu_tool_loop: dict, role_response: dict) -> str:
    repo_root = Path(
        str(
            npu_tool_loop.get("repo_root")
            or role_response.get("repo_root")
            or "."
        )
    ).resolve(strict=False)
    text = str(
        report_text_preview(
            repo_root,
            npu_tool_loop,
            ("response_text", "provider_heap_delta_text"),
        ).get("text")
        or ""
    ).strip()
    if text:
        return text
    return str(
        role_response.get("micro_task_result_summary")
        or role_response.get("response_text")
        or ""
    )


def _extract_npu_decision(text: str) -> str:
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped.startswith("DECISION="):
            decision = stripped.split("=", 1)[1].strip()
            if decision in NPU_MICRO_DECISIONS:
                return decision
    return ""
