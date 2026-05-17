"""GPU0 task packet construction."""

from __future__ import annotations

from typing import Any

def build_tasks(primary: dict[str, Any], sources: list[dict[str, Any]]) -> list[dict[str, Any]]:
    failed_sources = [item for item in sources if item.get("passed") is False]
    tasks = [
        {
            "id": "gpu0_peer_primary_advisory_quality",
            "role": "companion_peer_worker",
            "objective": "Verify whether GPU1/Ollama planned and worked on usable primary advisory evidence.",
            "requires_semantic_model": False,
        },
        {
            "id": "gpu0_peer_runtime_tool_context",
            "role": "companion_peer_worker",
            "objective": "Request broker-controlled deterministic tool evidence for GPU1 planner follow-up.",
            "requires_semantic_model": False,
        },
        {
            "id": "gpu0_peer_patch_spec_readiness",
            "role": "companion_peer_worker",
            "objective": "Check whether recommendations, patch specs and validation evidence can support a review-only patch proposal.",
            "requires_semantic_model": False,
        },
    ]
    if not primary.get("passed"):
        tasks.append(
            {
                "id": "gpu0_peer_gpu1_degradation_root_cause",
                "role": "companion_peer_worker",
                "objective": "Summarize why GPU1 primary advisory is degraded before the run is accepted.",
                "requires_semantic_model": False,
            }
        )
    if failed_sources:
        tasks.append(
            {
                "id": "gpu0_peer_failed_report_triage",
                "role": "companion_peer_worker",
                "objective": "Triage failed deterministic reports and return compact blockers for GPU1.",
                "requires_semantic_model": False,
            }
        )
    return tasks

def tool_request_templates(
    source_paths: list[str], audit_source_paths: list[str]
) -> list[dict[str, Any]]:
    joined_reports = ",".join(source_paths[:8])
    audit_reports = ",".join(audit_source_paths[:8])
    return [
        {
            "id": "gpu0_peer_code_interpreter_context",
            "tool": "build_code_interpreter_report",
            "reason": "GPU0 peer worker needs current code-structure context through the broker allowlist.",
            "args": {"input": "tools/ai,tools/validation,tools/workflow,tools/npu"},
            "source": "gpu0_peer_companion",
        },
        {
            "id": "gpu0_peer_report_contract_context",
            "tool": "check_validation_report_contract",
            "reason": "GPU0 peer worker needs report-contract status for the evidence it received.",
            "args": {"report_file": joined_reports} if joined_reports else {},
            "source": "gpu0_peer_companion",
        },
        {
            "id": "gpu0_peer_refactor_duplication_context",
            "tool": "build_refactor_duplication_audit",
            "reason": "GPU0 peer worker needs deterministic reuse/refactor overlap evidence.",
            "args": (
                {
                    "root": "tools/ai,tools/validation,tools/workflow,tools/npu",
                    "report": audit_reports,
                }
                if audit_reports
                else {"root": "tools/ai,tools/validation,tools/workflow,tools/npu"}
            ),
            "source": "gpu0_peer_companion",
        },
    ]
