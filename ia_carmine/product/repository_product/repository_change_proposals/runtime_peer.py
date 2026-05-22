from __future__ import annotations

from .common import *  # noqa: F403
from .proposal_models import proposal

def runtime_peer_evidence_summary(
    by_kind_multi: dict[str, list[dict[str, Any]]], reports: list[dict[str, Any]]
) -> dict[str, Any]:
    kinds = {kind: len(items) for kind, items in by_kind_multi.items()}
    gpu0_reports = (
        by_kind_multi.get("ollama_gpu0_peer_report", [])
        + by_kind_multi.get("gpu0_ollama_vulkan_peer", [])
        + by_kind_multi.get("openvino_gpu0_workload", [])
        + by_kind_multi.get("openvino_gpu0_secondary_workload", [])
    )
    npu_reports = (
        by_kind_multi.get("npu_micro_peer", [])
        + by_kind_multi.get("npu_micro_task_companion_report", [])
        + by_kind_multi.get("npu_gpu_deep_review_audit", [])
    )
    heap_entry_reports = by_kind_multi.get("heap_exchange_runtime_entry", [])
    heap_manifest_reports = by_kind_multi.get("heap_peer_runtime_manifest", [])
    closure_reports = by_kind_multi.get("heap_exchange_closure_audit", [])
    exit_reports = by_kind_multi.get("heap_exchange_runtime_exit_product", [])
    lifecycle_reports = by_kind_multi.get("heap_exchange_runtime_lifecycle", [])
    chain_contract_reports = by_kind_multi.get("unified_chain_contract", [])
    correlation_reports = by_kind_multi.get("runtime_evidence_correlation", [])
    apply_reports = by_kind_multi.get("patch_suggestion_bundle_apply", []) + by_kind_multi.get(
        "generated_patch_specs_review_pr_apply", []
    )

    latest_apply = latest_report(apply_reports)
    manual_items = latest_apply.get("manual_review_items") if isinstance(latest_apply, dict) else []
    if not isinstance(manual_items, list):
        manual_items = []

    metadata_only_count = sum(
        1
        for item in manual_items
        if isinstance(item, dict) and "metadata-only" in str(item.get("reason") or "")
    )
    operation_count = (
        int(latest_apply.get("operation_count") or 0) if isinstance(latest_apply, dict) else 0
    )
    changed_count = (
        int(latest_apply.get("changed_count") or 0) if isinstance(latest_apply, dict) else 0
    )

    return {
        "report_kinds_seen": kinds,
        "runtime_report_paths": [
            repo_path
            for report in reports
            for repo_path in [str(report.get("path") or "")]
            if "output/" in repo_path.replace("\\", "/")
        ],
        "heap_entry_present": bool(heap_entry_reports),
        "heap_peer_runtime_manifest_present": bool(heap_manifest_reports),
        "heap_closure_audit_present": bool(closure_reports),
        "heap_exit_product_present": bool(exit_reports),
        "heap_lifecycle_present": bool(lifecycle_reports),
        "unified_chain_contract_present": bool(chain_contract_reports),
        "latest_apply_report_path": (
            latest_apply.get("_source_path") if isinstance(latest_apply, dict) else ""
        ),
        "gpu0_workload_present": bool(gpu0_reports),
        "gpu0_observable": any(
            report.get("gpu0_vulkan_workload_verified") is True
            or report.get("provider_work_verified") is True
            or report.get("openvino_gpu0_observable_workload_passed") is True
            or report.get("passed") is True
            for report in gpu0_reports
        ),
        "npu_micro_peer_present": bool(npu_reports),
        "npu_peer_activity_requested": any(
            report.get("npu_peer_activity_requested") is True
            or report.get("provider_execution_requested") is True
            or report.get("npu_activity_classification") == "diagnostic_report_only"
            for report in npu_reports
        ),
        "runtime_evidence_correlation_present": bool(correlation_reports),
        "patch_apply_report_present": bool(apply_reports),
        "patch_apply_operation_count": operation_count,
        "patch_apply_changed_count": changed_count,
        "metadata_only_manual_review_count": metadata_only_count,
        "needs_concrete_generated_product": bool(apply_reports) and operation_count == 0,
    }

def runtime_peer_evidence_ready(summary: dict[str, Any]) -> bool:
    return (
        summary.get("heap_entry_present") is True
        and summary.get("heap_peer_runtime_manifest_present") is True
        and summary.get("gpu0_workload_present") is True
        and summary.get("npu_micro_peer_present") is True
        and summary.get("runtime_evidence_correlation_present") is True
    )

def runtime_peer_evidence_proposal(summary: dict[str, Any]) -> dict[str, Any]:
    marker = "<!-- IA-CARMINE-RUNTIME-PEER-EVIDENCE-PROPOSAL -->"
    content = (
        "\n\n"
        f"{marker}\n"
        "## Runtime peer evidence proposal path\n\n"
        "The repository-change proposal builder can consume current-stamp heap/exchange, GPU0, "
        "NPU peer, runtime correlation and generated patch-spec apply reports. This keeps the "
        "GPU1/Ollama advisory lane grounded in the active heap instead of falling back to "
        "static validation-only context.\n\n"
        "When generated patch specs are metadata-only, the proposal path must expose that as "
        "a concrete product gap and prefer deterministic, reviewable operations over "
        "evidence-only success.\n"
    )
    return proposal(
        proposal_id="P-RUNTIME-PEER-EVIDENCE-FEED",
        priority="P1",
        area="heap_exchange_product",
        title="Feed current runtime peer evidence into repository proposals",
        rationale=(
            "Current heap/GPU0/NPU/runtime-correlation evidence is available, but generated patch "
            "specs can still collapse into metadata-only proposals. The proposal builder must "
            "surface current runtime evidence and emit a concrete, reviewable product lane."
        ),
        target_files=[
            "ia_carmine/product/repository_product/repository_change_proposals/cli.py",
            "ia_carmine/product/generated_patch_specs/proposal_cli.py",
            "Tools/validation/README.md",
        ],
        change_type="runtime_evidence_proposal_feed",
        evidence_summary={"runtime_peer_evidence": summary},
        sketch=[
            "Discover current-stamp heap, GPU0, NPU and runtime-correlation reports.",
            "Carry runtime peer evidence into repository_change_proposals evidence_summary.",
            "Allow reviewed proposals to provide concrete deterministic operations for patch-spec generation.",
            "Fail if runtime evidence exists but no concrete generated product can be produced.",
        ],
        concrete_operations=[
            {
                "operation": "append_once",
                "path": "Tools/validation/README.md",
                "content": content,
                "source_id": "P-RUNTIME-PEER-EVIDENCE-FEED",
                "family": "runtime_peer_evidence",
                "description": "document runtime peer evidence proposal path",
            }
        ],
        validation=[
            "python -m Tools.validation run_repository_change_proposals_runtime_evidence_smoke --repo-root .",
            "python -m Tools.validation run_generated_patch_specs_empty_product_smoke --repo-root .",
            "python -m py_compile .\\Tools\\ai\\build_repository_change_proposals.py .\\Tools\\ai\\generated_patch_specs_from_proposals.py",
            "git diff --check",
        ],
        stop_conditions=[
            "Any change would execute providers from the proposal builder.",
            "Any change would fabricate source changes without runtime evidence.",
            "Any change would write under output/**, indexAI/code_chunks/** or docs/LOCAL_VALIDATION_EVIDENCE/** as final product.",
        ],
    )
