"""Artifact helpers for heap proposal cycles."""

from __future__ import annotations

from typing import Any
import re

from ia_carmine.runtime.heap_gate.proposal_prompt import build_refinement_prompt
from ia_carmine.runtime.heap_gate.runtime_common import repo_rel, write_json_report, write_text_report


def write_heap_parallel_cycle_artifact(
    owner: Any, revision: int, assessment: dict[str, Any]
) -> dict[str, str]:
    out_dir = owner.proposal_iteration_dir()
    basename = f"heap_parallel_cycle_{revision:03d}"
    json_path = out_dir / f"{basename}.json"
    md_path = out_dir / f"{basename}.md"
    write_json_report(assessment, json_path)
    md_lines = [
        "# Heap Parallel Cycle Assessment",
        "",
        f"- Revision: `{revision}`",
        f"- Passed: `{assessment.get('passed')}`",
        f"- GPU1 present: `{assessment.get('gpu1_present')}`",
        f"- GPU0 present: `{assessment.get('gpu0_present')}`",
        f"- NPU present: `{assessment.get('npu_present')}`",
        f"- NPU workload ok: `{assessment.get('npu_workload_ok')}`",
        "",
        "## Missing lanes",
        "",
        *[f"- `{item}`" for item in assessment.get("missing_lanes", [])],
        "",
        "## Provider report lanes",
        "",
        *[f"- `{item}`" for item in assessment.get("provider_report_lanes", [])],
        "",
    ]
    write_text_report("\n".join(md_lines), md_path)
    refs = {"json": repo_rel(owner.repo_root, json_path), "markdown": repo_rel(owner.repo_root, md_path)}
    owner.append_heap_exchange_event(
        {
            "kind": "heap_parallel_cycle_assessment",
            "lane": "arbiter",
            "round": revision,
            "path": refs["json"],
            "markdown": refs["markdown"],
            "passed": bool(assessment.get("passed")),
            "summary": "same-heap multi-lane participation assessed before proposal acceptance",
        }
    )
    return refs


def build_cross_lane_proposal_veto(
    owner: Any,
    *,
    response_text: str,
    implementation_quality: dict[str, Any],
    proposal_progress: dict[str, Any],
    deterministic_reviews: dict[str, Any],
    npu_audit: dict[str, Any],
    parallel_cycle: dict[str, Any],
    revision: int,
) -> dict[str, Any]:
    reasons: list[str] = []
    gpu0_review = deterministic_reviews.get("gpu0_review")
    npu_piece = deterministic_reviews.get("npu_micro_task_piece")
    placeholder_hits = implementation_quality.get("placeholder_hits") if isinstance(implementation_quality, dict) else []
    impl_errors = implementation_quality.get("errors") if isinstance(implementation_quality, dict) else []
    progress_errors = proposal_progress.get("errors") if isinstance(proposal_progress, dict) else []
    combined_gpu0 = "\n".join(str(item) for item in (gpu0_review or []))
    combined_npu = "\n".join(str(item) for item in (npu_piece or []))
    combined_response = str(response_text or "")
    if placeholder_hits:
        reasons.append(f"implementation_quality.placeholder_hits={placeholder_hits}")
    if impl_errors:
        reasons.append(f"implementation_quality.errors={impl_errors}")
    if progress_errors:
        reasons.append(f"proposal_progress.errors={progress_errors}")
    if parallel_cycle.get("passed") is not True:
        reasons.append(f"parallel_cycle_missing_lanes={parallel_cycle.get('missing_lanes')}")
    if re.search(r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b", combined_gpu0, re.IGNORECASE):
        reasons.append("GPU0 review contains placeholder/stub/TODO signal")
    if re.search(r"reject|reject_until|rifiut|non soddisfacente|non accett", combined_gpu0, re.IGNORECASE):
        reasons.append("GPU0 review contains reject signal")
    if re.search(r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b", combined_npu, re.IGNORECASE):
        reasons.append("NPU micro-task contains placeholder/stub/TODO signal")
    if re.search(r"reject|reject_until|rifiut|non soddisfacente|non accett", combined_npu, re.IGNORECASE):
        reasons.append("NPU micro-task contains reject signal")
    if re.search(r"\bTODO\b|\bFIXME\b|placeholder|stub|da implementare", combined_response, re.IGNORECASE):
        reasons.append("response_text contains TODO/FIXME/placeholder/stub marker")
    if npu_audit and npu_audit.get("requested") and not npu_audit.get("performed"):
        reasons.append("NPU workload requested but not performed")
    reasons = list(dict.fromkeys(str(item) for item in reasons if str(item).strip()))
    refinement_prompt = ""
    if reasons:
        refinement_prompt = build_refinement_prompt(
            revision=revision,
            reasons=reasons,
            source_candidates=owner.real_source_file_candidates(owner.read_events(), limit=24),
        )
    return {
        "vetoed": bool(reasons),
        "reasons": reasons,
        "gpu0_review": gpu0_review or [],
        "npu_micro_task_piece": npu_piece or [],
        "npu_workload_audit": npu_audit or {},
        "parallel_cycle": parallel_cycle,
        "refinement_prompt": refinement_prompt,
    }


def write_heap_refinement_task_artifact(
    owner: Any, revision: int, veto: dict[str, Any]
) -> dict[str, str]:
    out_dir = owner.proposal_iteration_dir()
    basename = f"heap_refinement_task_after_revision_{revision:03d}"
    json_path = out_dir / f"{basename}.json"
    md_path = out_dir / f"{basename}.md"
    payload = {
        "schema_version": 1,
        "kind": "heap_refinement_task",
        "stamp": owner.stamp,
        "after_revision": revision,
        "vetoed": bool(veto.get("vetoed")),
        "reasons": veto.get("reasons", []),
        "parallel_cycle": veto.get("parallel_cycle", {}),
        "refinement_prompt": veto.get("refinement_prompt", ""),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json_report(payload, json_path)
    md_lines = [
        "# Heap Refinement Task",
        "",
        f"- After revision: `{revision}`",
        f"- Vetoed: `{bool(veto.get('vetoed'))}`",
        "",
        "## Reasons",
        "",
        *[f"- {item}" for item in veto.get("reasons", [])],
        "",
        "## Refinement prompt",
        "",
        "```text",
        str(veto.get("refinement_prompt") or ""),
        "```",
        "",
    ]
    write_text_report("\n".join(md_lines), md_path)
    refs = {"json": repo_rel(owner.repo_root, json_path), "markdown": repo_rel(owner.repo_root, md_path)}
    owner.append_heap_exchange_event(
        {
            "kind": "heap_refinement_task",
            "lane": "arbiter",
            "round": revision,
            "path": refs["json"],
            "markdown": refs["markdown"],
            "summary": "cross-lane veto converted into next provider refinement task",
        }
    )
    return refs


def render_proposal_iteration_markdown(
    *,
    revision: int,
    block_id: str,
    source: str,
    quality_passed: bool,
    pointer_action: str,
    exit_decision: str,
    previous_block_id: str,
    data: dict[str, Any],
    provider_block_refs: dict[str, list[str]],
    deterministic_reviews: dict[str, Any],
    implementation_quality: dict[str, Any],
    proposal_progress: dict[str, Any],
    npu_audit: dict[str, Any],
    parallel_cycle: dict[str, Any],
    cross_lane_veto: dict[str, Any],
    anchored_sources: list[str],
    clipped: str,
) -> str:
    md = [
        "# Heap Proposal Iteration",
        "",
        f"- Revision: `{revision}`",
        f"- Block id: `{block_id}`",
        f"- Source: `{source}`",
        f"- Quality passed: `{quality_passed}`",
        f"- Pointer action: `{pointer_action}`",
        f"- Exit decision: `{exit_decision}`",
        f"- Previous block: `{previous_block_id}`",
        f"- Refines block: `{data['refines_block_id']}`",
        f"- Resume from: `{data['resume_from_block_id']}`",
        f"- Target files: `{data['target_files']}`",
        f"- GPU1 block ref: `{data['gpu1_block_ref']}`",
        f"- GPU0 review block refs: `{provider_block_refs['gpu0']}`",
        f"- NPU audit block refs: `{provider_block_refs['npu']}`",
        "",
        "## Deterministic lane reviews",
        "",
        "### GPU0 review",
        "",
        *[f"- {item}" for item in deterministic_reviews.get("gpu0_review", [])],
        "",
        "### NPU micro-task piece",
        "",
        *[f"- {item}" for item in deterministic_reviews.get("npu_micro_task_piece", [])],
        "",
        "### Implementation quality",
        "",
        f"- Passed: `{implementation_quality.get('passed')}`",
        f"- Errors: `{implementation_quality.get('errors')}`",
        "",
        "### Proposal progress",
        "",
        f"- Passed: `{proposal_progress.get('passed')}`",
        f"- Similarity: `{proposal_progress.get('similarity')}`",
        f"- Errors: `{proposal_progress.get('errors')}`",
        "",
        "### NPU workload audit",
        "",
        f"- Requested: `{npu_audit.get('requested')}`",
        f"- Performed: `{npu_audit.get('performed')}`",
        f"- Passed: `{npu_audit.get('passed')}`",
        f"- Iterations: `{npu_audit.get('iterations')}`",
        f"- Seconds: `{npu_audit.get('seconds')}`",
        f"- Python: `{npu_audit.get('python_exe')}`",
        "",
        "### Heap parallel cycle",
        "",
        f"- Passed: `{parallel_cycle.get('passed')}`",
        f"- Missing lanes: `{parallel_cycle.get('missing_lanes')}`",
        "",
        "### Cross-lane veto",
        "",
        f"- Vetoed: `{cross_lane_veto.get('vetoed')}`",
        f"- Reasons: `{cross_lane_veto.get('reasons')}`",
        "",
        "## GPU1 free text evidence",
        "",
        f"- Raw chars: `{data.get('gpu1_free_text_evidence_chars')}`",
        f"- Raw sha256: `{data.get('gpu1_free_text_evidence_sha256')}`",
        "- Stored in JSON field: `gpu1_free_text_evidence`.",
        f"- Visible even when invalid: `{data.get('gpu1_free_text_evidence_visible_even_when_invalid')}`",
        f"- Reject reason: `{data.get('reject_reason')}`",
        "",
        "## Anchored source candidates",
        "",
        *[f"- `{item}`" for item in anchored_sources[:20]],
        "",
        "## Proposal chunk",
        "",
        clipped,
        "",
    ]
    return "\n".join(md)
