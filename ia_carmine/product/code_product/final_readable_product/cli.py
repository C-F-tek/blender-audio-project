#!/usr/bin/env python3
"""Assemble the run-owned final readable product for heap context closure."""
from __future__ import annotations
import argparse
import json
import sys
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Any
try:
    from ia_carmine._shared.heap_final_code_product import code_product_items, code_product_status, lab_status_summary, matrix_has_reviewable_targets, render_full_code_product_markdown
    from ia_carmine._shared.heap_final_readable_synthesis import closure_display_values, render_markdown
    from ia_carmine._shared.heap_plan_product_full_patch import render_plan_product_full_patch
    from ia_carmine.product.code_product.final_readable_product.code_matrix_discovery import load_code_matrix
    from ia_carmine.product.code_product.final_readable_product.operator_decision import write_operator_decision
    from ia_carmine.product.code_product.final_readable_product.product_contract import code_product_markdown_metrics, final_product_blockers, real_code_product_ready
    from ia_carmine.product.code_product.final_readable_product.pointer_reconstruction import build_pointer_reconstruction
    from ia_carmine.runtime.heap_gate.pointer_soft_lock import gpu1_blocked_reason_from_gate, soft_lock_state_from_reports
    from ia_carmine.runtime.heap_gate.gpu1_one_turn_gate import ONE_TURN_SUMMARY_FIELDS
    from ia_carmine._shared.report_io import print_json_report
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine._shared.heap_final_code_product import code_product_items, code_product_status, lab_status_summary, matrix_has_reviewable_targets, render_full_code_product_markdown  # type: ignore
    from ia_carmine._shared.heap_final_readable_synthesis import closure_display_values, render_markdown  # type: ignore
    from ia_carmine._shared.heap_plan_product_full_patch import render_plan_product_full_patch  # type: ignore
    from ia_carmine.product.code_product.final_readable_product.code_matrix_discovery import load_code_matrix  # type: ignore
    from ia_carmine.product.code_product.final_readable_product.operator_decision import write_operator_decision  # type: ignore
    from ia_carmine.product.code_product.final_readable_product.product_contract import code_product_markdown_metrics, final_product_blockers, real_code_product_ready  # type: ignore
    from ia_carmine.product.code_product.final_readable_product.pointer_reconstruction import build_pointer_reconstruction  # type: ignore
    from ia_carmine.runtime.heap_gate.pointer_soft_lock import gpu1_blocked_reason_from_gate, soft_lock_state_from_reports  # type: ignore
    from ia_carmine.runtime.heap_gate.gpu1_one_turn_gate import ONE_TURN_SUMMARY_FIELDS  # type: ignore
    from ia_carmine._shared.report_io import print_json_report  # type: ignore
def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")
def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}
def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
def resolve_path(root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    return path.resolve(strict=False)
def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
def count_from_decision(decision: dict[str, Any], key: str, items: list[Any]) -> int:
    try:
        return max(len(items), int(decision.get(key) or 0))
    except (TypeError, ValueError):
        return len(items)


def one_turn_fields_from_metrics(metrics: dict[str, Any]) -> dict[str, Any]:
    fields = {
        key: metrics.get(key)
        for key in ONE_TURN_SUMMARY_FIELDS
        if key in metrics
    }
    fields.setdefault("gpu1_one_turn_runtime_gate_present", False)
    fields.setdefault("gpu1_one_turn_runtime_gate_passed", False)
    fields.setdefault("gpu1_one_turn_blocker", "")
    fields.setdefault("gpu1_one_turn_errors", [])
    return fields


def one_turn_gate_required(
    *,
    gate: dict[str, Any],
    metrics: dict[str, Any],
    composer: dict[str, Any],
    pointer: dict[str, Any],
    revision: dict[str, Any],
) -> bool:
    sources = (gate, metrics, composer, pointer, revision)
    for source in sources:
        if source.get("provider_execution_performed") is True:
            return True
        if source.get("allow_provider_generation") is True:
            return True
        if source.get("provider_generation_enabled") is True:
            return True
    if int(composer.get("provider_report_count") or 0) > 0:
        return True
    if as_list(composer.get("provider_reports")):
        return True
    if int(metrics.get("provider_lane_count") or 0) > 0:
        return True
    return False


def product_kind_from_surfaces(
    *,
    provider_runtime_blocked: bool,
    blocked_continuation: bool,
    code_product_ready: bool,
    text_product_ready: bool,
) -> str:
    if provider_runtime_blocked:
        return "provider_runtime_blocked_product"
    if blocked_continuation:
        return "blocked_continuation_product"
    if code_product_ready and text_product_ready:
        return "text_and_code_product"
    if code_product_ready:
        return "code_patch_product"
    if text_product_ready:
        return "text_product"
    return "diagnostic_decision_product"


def append_download_manifest(manifest_path: Path, paths: list[Path]) -> None:
    if not manifest_path:
        return
    try:
        lines = manifest_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    except Exception:
        lines = []
    existing = set(lines)
    additions = ["", "Final readable product:"]
    for path in paths:
        line = f"- {path}"
        if line not in existing:
            additions.append(line)
    if len(additions) > 2:
        write_text(manifest_path, "\n".join(lines + additions))
def zip_documents_dir(documents_dir: Path, zip_path: Path) -> int:
    members: list[Path] = [
        path for path in documents_dir.rglob("*") if path.is_file() and path != zip_path
    ]
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(members):
            archive.write(path, path.relative_to(documents_dir).as_posix())
    return len(members)
def build_report(args: argparse.Namespace) -> tuple[dict[str, Any], str]:
    repo_root = Path(args.repo_root).resolve()
    run_dir = resolve_path(repo_root, args.run_dir)
    composer_path = resolve_path(
        repo_root, args.composer_json or run_dir / "heap_final_proposal_composer.json"
    )
    gate_path = resolve_path(
        repo_root, args.gate_report or run_dir / "heap_runtime_completeness_gate_report.json"
    )
    composer = read_json(composer_path)
    gate = read_json(gate_path)
    postrun = read_json(run_dir / "external_heap_postrun_package.json")
    revision = read_json(run_dir / "external_heap_revision_context.json")
    pointer = read_json(run_dir / "external_heap_block_pointer_manifest.json")
    causality_path_value = str(postrun.get("causality_json") or "")
    causality_path = (
        resolve_path(repo_root, causality_path_value)
        if causality_path_value
        else run_dir / "heap_final_causality_normalized.json"
    )
    causality = read_json(causality_path)
    causal_chain_passed = (
        postrun.get("causality_passed")
        if "causality_passed" in postrun
        else causality.get("causal_chain_passed")
    )
    product_acceptance_passed = (
        postrun.get("product_acceptance_passed")
        if "product_acceptance_passed" in postrun
        else causality.get("product_acceptance_passed")
    )
    matrix, matrix_path = load_code_matrix(repo_root, run_dir, gate)
    pointer_reconstruction = build_pointer_reconstruction(pointer, revision)
    decision = as_dict(composer.get("operator_decision"))
    metrics = as_dict(gate.get("metrics"))
    gpu1_one_turn = one_turn_fields_from_metrics(metrics)
    gpu1_one_turn_required = one_turn_gate_required(
        gate=gate,
        metrics=metrics,
        composer=composer,
        pointer=pointer,
        revision=revision,
    )
    gate_product_status = str(metrics.get("product_status") or "")
    gate_state_product = as_dict(as_dict(gate.get("state")).get("product"))
    provider_rejection_reasons = as_list(pointer.get("provider_rejection_reasons")) or as_list(
        revision.get("provider_rejection_reasons")
    )
    provider_runtime_reason = ",".join(str(item) for item in provider_rejection_reasons if str(item).strip())
    provider_runtime_blocked = bool(provider_runtime_reason)
    provider_blocked_reason = str(
        provider_runtime_reason
        or gate_state_product.get("product_blocked_reason")
        or metrics.get("soft_close_reason")
        or ""
    )
    markdown = render_markdown(
        run_dir=run_dir,
        composer=composer,
        gate=gate,
        postrun=postrun,
        revision=revision,
        pointer=pointer,
        matrix=matrix,
        matrix_path=matrix_path,
    )
    full_code_product = render_full_code_product_markdown(
        matrix,
        matrix_path,
        gate_product_status,
        blocked_reason=provider_blocked_reason,
    )
    plan_product_full_patch = render_plan_product_full_patch(
        run_dir=run_dir,
        gate=gate,
        revision=revision,
        pointer=pointer,
        matrix=matrix,
        matrix_path=matrix_path,
    )
    output = resolve_path(repo_root, args.output or run_dir / "heap_final_readable_product.json")
    markdown_output = resolve_path(
        repo_root, args.markdown_output or run_dir / "heap_final_readable_product.md"
    )
    text_output = resolve_path(
        repo_root, args.text_output or run_dir / "heap_final_readable_product.txt"
    )
    full_code_product_output = run_dir / "CODE_PRODUCT_FULL_PATCH.md"
    plan_product_full_patch_output = run_dir / "PLAN_PRODUCT_FULL_PATCH.md"
    write_text(markdown_output, markdown)
    write_text(text_output, markdown)
    write_text(full_code_product_output, full_code_product)
    write_text(plan_product_full_patch_output, plan_product_full_patch)
    documents_outputs: dict[str, str] = {}
    documents_zip = ""
    zip_member_count = 0
    zip_path_for_later: Path | None = None
    documents_dir_for_later: Path | None = None
    documents_json_path: Path | None = None
    documents_dir_value = args.documents_dir or str(composer.get("documents_dir") or "")
    if documents_dir_value:
        documents_dir = Path(documents_dir_value).expanduser().resolve()
        documents_dir_for_later = documents_dir
        documents_md = documents_dir / "FINAL_READABLE_PRODUCT.md"
        documents_txt = documents_dir / "FINAL_READABLE_PRODUCT.txt"
        documents_json = documents_dir / "FINAL_READABLE_PRODUCT.json"
        documents_code_product = documents_dir / "CODE_PRODUCT_FULL_PATCH.md"
        documents_plan_product_full_patch = documents_dir / "PLAN_PRODUCT_FULL_PATCH.md"
        documents_json_path = documents_json
        write_text(documents_md, markdown)
        write_text(documents_txt, markdown)
        write_text(documents_code_product, full_code_product)
        write_text(documents_plan_product_full_patch, plan_product_full_patch)
        documents_outputs = {
            "documents_markdown": str(documents_md),
            "documents_text": str(documents_txt),
            "documents_json": str(documents_json),
            "documents_code_product": str(documents_code_product),
            "documents_plan_product_full_patch": str(documents_plan_product_full_patch),
        }
        manifest = str(composer.get("download_manifest_txt") or "")
        if manifest:
            append_download_manifest(
                Path(manifest).expanduser().resolve(),
                [
                    documents_md,
                    documents_txt,
                    documents_json,
                    documents_code_product,
                    documents_plan_product_full_patch,
                ],
            )
        if args.zip_documents:
            zip_path_for_later = (
                Path(args.zip_output).expanduser().resolve()
                if args.zip_output
                else Path(str(documents_dir) + ".zip")
            )
            documents_zip = str(zip_path_for_later)
    reviewable_matrix_targets = matrix_has_reviewable_targets(matrix)
    matrix_items = code_product_items(matrix) if reviewable_matrix_targets else []
    code_product_state = code_product_status(matrix, gate_product_status)
    matrix_target_count = int(matrix.get("target_count") or 0)
    verified_target_count = int(matrix.get("verified_target_count") or 0)
    lab = lab_status_summary(
        run_dir=run_dir,
        gate=gate,
        matrix=matrix,
        matrix_path=matrix_path,
    )
    lab_evidence_written = bool(lab.get("lab_evidence_written"))
    lab_status = str(lab.get("lab_status") or "not_run")
    provider_decision = str(decision.get("decision") or "")
    concrete_code_proposal_count = len(matrix_items)
    resume_from_block_id = str(revision.get("resume_from_block_id") or "")
    gpu1_reason = gpu1_blocked_reason_from_gate(gate)
    soft_lock = soft_lock_state_from_reports(gate, pointer, revision)
    pointer_closure_table = as_list(soft_lock.get("pointer_closure_table"))
    open_pointer_count_final = int(soft_lock.get("open_pointer_count_final") or 0)
    soft_lock_state = str(soft_lock.get("soft_lock_state") or "")
    closure_quorum_status = str(soft_lock.get("closure_quorum_status") or "")
    closure_quorum_reason = str(soft_lock.get("closure_quorum_reason") or "")
    gpu1_closure_display, gpu0_closure_display = closure_display_values(
        soft_lock,
        metrics,
        revision,
    )
    if gpu1_closure_display == "gpu1_decision_missing":
        closure_quorum_status = closure_quorum_status or "blocked_with_reason"
        closure_quorum_reason = (
            closure_quorum_reason or "gpu0_veto_not_allowed_without_gpu1_decision"
        )
        soft_lock["closure_quorum_status"] = closure_quorum_status
        soft_lock["closure_quorum_reason"] = closure_quorum_reason
        soft_lock["cpu_closure_validation"] = (
            soft_lock.get("cpu_closure_validation") or "blocked_provider_or_pointer"
        )
    soft_lock["soft_lock_closure_owner_decision"] = gpu1_closure_display
    soft_lock["gpu0_closure_agreement"] = gpu0_closure_display
    pointer_closure_blocked = open_pointer_count_final > 0
    targeted_refine_pending = bool(
        open_pointer_count_final > 0
        and closure_quorum_status == "targeted_refine_allowed"
        and not bool(metrics.get("provider_revision_budget_exhausted"))
    )
    blocked_continuation = bool(
        targeted_refine_pending
        or (
        not provider_runtime_blocked
        and (
        closure_quorum_status == "blocked_continuation_ready"
        or
        pointer_closure_blocked
        or (
            concrete_code_proposal_count == 0
            and (
                resume_from_block_id
                or gate_product_status == "blocked_with_reason"
                or gpu1_reason
            )
        )
        )
        )
    )
    if pointer_closure_blocked and concrete_code_proposal_count > 0:
        final_document_status = "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
    elif gate_product_status and gate_product_status != "ready":
        final_document_status = (
            "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
            if concrete_code_proposal_count > 0
            else "BLOCKED_CONTINUATION_PRODUCT"
        )
    elif concrete_code_proposal_count > 0:
        final_document_status = code_product_state
    elif provider_runtime_blocked:
        final_document_status = "BLOCKED_PROVIDER_RUNTIME"
    elif blocked_continuation:
        final_document_status = "BLOCKED_CONTINUATION_PRODUCT"
    elif provider_decision in {
        "DIAGNOSTIC_ONLY",
        "BLOCKED_PROVIDER_REVIEW",
        "BLOCKED_NO_VERIFIED_TARGET",
        "NO CONCRETE PATCHABLE PROPOSAL",
    }:
        final_document_status = "DIAGNOSTIC_REVIEW_READY"
    else:
        final_document_status = "NO_APPLICABLE_CODE_PRODUCT"
    code_product_report = code_product_markdown_metrics(full_code_product)
    truncation_marker = bool(code_product_report.get("truncation_marker"))
    code_product_ready = real_code_product_ready(
        final_document_status=final_document_status,
        concrete_code_proposal_count=concrete_code_proposal_count,
        code_product_metrics=code_product_report,
    )
    final_product_delta_applied_count = plan_product_full_patch.count("### Applied Delta ")
    text_product_ready = bool(
        "Text surface status: `FINAL_PRODUCT_TEXT_SURFACE_AVAILABLE`" in plan_product_full_patch
        and final_product_delta_applied_count > 0
    )
    final_product_surface_ready = bool(code_product_ready or text_product_ready)
    latest_final_product_kind = str(metrics.get("latest_final_product_kind") or "").strip()
    code_surface_required = bool(
        latest_final_product_kind in {"code", "text_and_code"}
        or code_product_ready
        or concrete_code_proposal_count > 0
    )
    report_product_kind = product_kind_from_surfaces(
        provider_runtime_blocked=provider_runtime_blocked,
        blocked_continuation=blocked_continuation,
        code_product_ready=code_product_ready,
        text_product_ready=text_product_ready,
    )
    blockers = final_product_blockers(
        markdown_output=markdown_output,
        final_document_status=final_document_status,
        concrete_code_proposal_count=concrete_code_proposal_count,
        code_product_metrics=code_product_report,
        code_product_ready=code_product_ready,
        text_product_ready=text_product_ready,
        final_product_kind=latest_final_product_kind or report_product_kind,
        code_surface_required=code_surface_required,
        pointer=pointer,
        revision=revision,
        matrix=matrix,
        gate=gate,
        product_acceptance_passed=(
            product_acceptance_passed if isinstance(product_acceptance_passed, bool) else None
        ),
    )
    if (
        gpu1_one_turn_required
        and gpu1_one_turn.get("gpu1_one_turn_runtime_gate_passed") is not True
    ):
        blockers.append(
            "gpu1_one_turn_runtime_gate_failed:"
            + str(
                gpu1_one_turn.get("gpu1_one_turn_blocker")
                or "gpu1_one_turn_runtime_gate_missing"
            )
        )
    blockers.extend(str(item) for item in pointer_reconstruction.get("errors", []))
    if open_pointer_count_final > 0:
        blockers.append("pointer closure has open pointers")
    generic_product = as_dict(
        metrics.get("generic_write_refined_request")
        or metrics.get("compat_legacy_generic_write_refined_product")
        or metrics.get("compat_legacy_generic_write_document_product")
        or metrics.get("generic_write_refined_product")
        or metrics.get("generic_write_document_product")
    )
    peer_pending_reasons = []
    if int(generic_product.get("gpu0_peer_followup_pending_count") or metrics.get("gpu0_peer_followup_pending_count") or 0) > 0:
        peer_pending_reasons.append("gpu0_peer_followup_pending")
    if int(generic_product.get("npu_peer_followup_pending_count") or metrics.get("npu_peer_followup_pending_count") or 0) > 0:
        peer_pending_reasons.append("npu_peer_followup_pending")
    if int(generic_product.get("generic_write_capture_failed_count") or metrics.get("generic_write_capture_failed_count") or 0) > 0:
        peer_pending_reasons.append("generic_write_capture_failed")
    if metrics.get("context_hierarchy_valid") is False:
        peer_pending_reasons.append("context_hierarchy_invalid")
    if metrics.get("gpu1_primary_workload_valid") is False:
        peer_pending_reasons.append("gpu1_primary_workload_missing")
    if metrics.get("gpu1_primary_evidence_valid") is False:
        peer_pending_reasons.append("gpu1_primary_evidence_missing")
    if metrics.get("gpu1_leader_valid") is False:
        peer_pending_reasons.append("gpu1_leader_missing")
    if (
        gpu1_one_turn_required
        and gpu1_one_turn.get("gpu1_one_turn_runtime_gate_passed") is not True
    ):
        peer_pending_reasons.append(
            "gpu1_one_turn_runtime_gate_failed:"
            + str(
                gpu1_one_turn.get("gpu1_one_turn_blocker")
                or "gpu1_one_turn_runtime_gate_missing"
            )
        )
    if (
        metrics.get("leader_source") == "native_tool_result"
        and int(metrics.get("gpu1_native_tool_call_count") or 0) <= 0
    ):
        peer_pending_reasons.append("gpu1_native_tool_result_invalid")
    if (
        metrics.get("gpu1_boot_leader_ready") is True
        and metrics.get("sidecars_start_policy") == "after_gpu1_residency_handshake"
        and float(metrics.get("parallel_provider_overlap_seconds") or 0.0) <= 0.0
    ):
        peer_pending_reasons.append("parallelism_lost_by_serial_leader_gate")
    peer_pending_reason = ",".join(peer_pending_reasons)
    final_soft_close_reason = (
        peer_pending_reason
        or closure_quorum_reason
        or gpu1_reason
        or gate_product_status
        or provider_decision
        or soft_lock_state
    )
    if peer_pending_reason and not provider_blocked_reason:
        provider_blocked_reason = peer_pending_reason
    if documents_dir_for_later:
        operator_decision_path = documents_dir_for_later / "OPERATOR_DECISION.txt"
        write_operator_decision(
            operator_decision_path,
            final_document_status=final_document_status,
            product_kind=report_product_kind,
            product_status=gate_product_status,
            gpu1_reason=gpu1_reason,
            resume_from_block_id=resume_from_block_id,
            soft_lock=soft_lock,
            provider_blocked_reason=provider_blocked_reason,
            provider_replight_reports=as_list(metrics.get("provider_replight_reports")),
            gpu1_one_turn=gpu1_one_turn,
            open_pointer_count_final=open_pointer_count_final,
            blocked_continuation=blocked_continuation,
            write_text=write_text,
        )
        documents_outputs["operator_decision"] = str(operator_decision_path)
    report_passed = bool(
        markdown.strip()
        and markdown_output.exists()
        and final_product_surface_ready
        and not blockers
    )
    product_blocked_reason = ""
    if not report_passed:
        product_blocked_reason = str(
            (blockers[0] if blockers else "") or final_soft_close_reason
        )
    report = {
        "schema_version": 1,
        "kind": "heap_final_readable_product",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "run_dir": str(run_dir),
        "passed": report_passed,
        "final_document_status": final_document_status,
        "decision": decision.get("decision"),
        "product_kind": report_product_kind,
        "product_status": gate_product_status,
        "product_approval_status": "blocked" if blocked_continuation else code_product_state,
        "resume_from_block_id": resume_from_block_id,
        "continuation_required": blocked_continuation,
        "soft_close_reason": final_soft_close_reason,
        "product_blocked_reason": product_blocked_reason,
        "causal_chain_passed": causal_chain_passed,
        "product_acceptance_passed": product_acceptance_passed,
        "causality_json": str(causality_path) if causality_path.exists() else "",
        "soft_lock_state": soft_lock_state,
        "soft_lock_closure_owner_decision": gpu1_closure_display,
        "gpu0_closure_agreement": gpu0_closure_display,
        "npu_closure_advisory": soft_lock.get("npu_closure_advisory", ""),
        "cpu_closure_validation": soft_lock.get("cpu_closure_validation", ""),
        "closure_quorum_status": closure_quorum_status,
        "closure_quorum_reason": closure_quorum_reason,
        "targeted_refine_pending": targeted_refine_pending,
        "provider_revision_budget_exhausted": metrics.get("provider_revision_budget_exhausted"),
        "soft_lock_targeted_refine_used": soft_lock.get(
            "soft_lock_targeted_refine_used", False
        ),
        "soft_lock_extension_count": soft_lock.get("soft_lock_extension_count", 0),
        "open_pointer_count_before_soft_lock": soft_lock.get("open_pointer_count_before_soft_lock"),
        "open_pointer_count_after_each_extension": soft_lock.get("open_pointer_count_after_each_extension", []),
        "open_pointer_count_final": open_pointer_count_final,
        "pointer_closure_table": pointer_closure_table,
        "gpu1_blocked_reason": gpu1_reason,
        "provider_rejected_count": pointer.get("provider_rejected_count"),
        "provider_rejection_reasons": provider_rejection_reasons,
        "provider_rejections": pointer.get("provider_rejections", []),
        "npu_sidecar_status": revision.get("npu_sidecar_status") or (
            "evidence_ready_non_closer" if revision.get("npu_block_count") else ""
        ),
        "lane_tiers": metrics.get("lane_tiers", {}),
        "lane_authority": metrics.get("lane_authority", {}),
        "lane_context_budgets": metrics.get("lane_context_budgets", {}),
        "gpu1_context_budget": metrics.get("gpu1_context_budget", {}),
        "gpu0_context_budget": metrics.get("gpu0_context_budget", {}),
        "npu_context_budget": metrics.get("npu_context_budget", {}),
        "context_hierarchy_valid": metrics.get("context_hierarchy_valid"),
        "gpu1_replight_valid": metrics.get("gpu1_replight_valid"),
        "gpu1_boot_leader_ready": metrics.get("gpu1_boot_leader_ready"),
        "gpu1_primary_workload_valid": metrics.get("gpu1_primary_workload_valid"),
        "gpu1_primary_evidence_valid": metrics.get("gpu1_primary_evidence_valid"),
        "gpu1_primary_evidence_source": metrics.get("gpu1_primary_evidence_source", ""),
        "gpu1_primary_workload_chars": metrics.get("gpu1_primary_workload_chars"),
        "gpu1_primary_workload_tokens": metrics.get("gpu1_primary_workload_tokens"),
        "leader_source": metrics.get("leader_source", ""),
        "gpu1_native_tool_call_count": metrics.get("gpu1_native_tool_call_count"),
        "gpu1_one_turn_runtime_gate_present": gpu1_one_turn.get("gpu1_one_turn_runtime_gate_present"),
        "gpu1_one_turn_runtime_gate_path": gpu1_one_turn.get("gpu1_one_turn_runtime_gate_path"),
        "gpu1_one_turn_runtime_gate_passed": gpu1_one_turn.get("gpu1_one_turn_runtime_gate_passed"),
        "gpu1_one_turn_native_tool_call_count": gpu1_one_turn.get("gpu1_one_turn_native_tool_call_count"),
        "gpu1_one_turn_broker_result_passed_count": gpu1_one_turn.get("gpu1_one_turn_broker_result_passed_count"),
        "gpu1_one_turn_role_tool_reinjected": gpu1_one_turn.get("gpu1_one_turn_role_tool_reinjected"),
        "gpu1_one_turn_tool_result_consumed": gpu1_one_turn.get("gpu1_one_turn_tool_result_consumed"),
        "gpu1_one_turn_final_product_delta_valid": gpu1_one_turn.get("gpu1_one_turn_final_product_delta_valid"),
        "gpu1_one_turn_blocker": gpu1_one_turn.get("gpu1_one_turn_blocker"),
        "gpu1_one_turn_errors": gpu1_one_turn.get("gpu1_one_turn_errors"),
        "sidecars_start_policy": metrics.get("sidecars_start_policy", ""),
        "parallel_provider_overlap_seconds": metrics.get(
            "parallel_provider_overlap_seconds"
        ),
        "device_identity_map": metrics.get("device_identity_map", []),
        "gpu1_leader_valid": metrics.get("gpu1_leader_valid"),
        "gpu1_leader_block_id": metrics.get("gpu1_leader_block_id", ""),
        "gpu1_consumed_generic_write_block_ids": metrics.get(
            "gpu1_consumed_generic_write_block_ids", []
        ),
        "consumed_peer_block_ids": metrics.get("consumed_peer_block_ids", []),
        "gpu1_consumed_gpu0_peer": metrics.get("gpu1_consumed_gpu0_peer"),
        "gpu1_consumed_npu_peer": metrics.get("gpu1_consumed_npu_peer"),
        "code_product_status": code_product_state,
        "real_code_product_ready": code_product_ready,
        "text_product_ready": text_product_ready,
        "final_product_surface_ready": final_product_surface_ready,
        "final_product_delta_applied_count": final_product_delta_applied_count,
        "code_product_metrics": code_product_report,
        "truncation_marker": truncation_marker,
        "blocking_reasons": blockers,
        "accepted_provider_proposal_count": count_from_decision(
            decision, "accepted_count", as_list(decision.get("accepted_proposals"))
        ),
        "rejected_provider_proposal_count": count_from_decision(
            decision, "rejected_count", as_list(decision.get("rejected_proposals"))
        ),
        "code_execution_matrix_passed": matrix.get("passed"),
        "pointer_manifest_passed": pointer.get("passed"),
        "pointer_reconstruction": pointer_reconstruction,
        "pointer_reconstruction_performed": pointer_reconstruction.get("performed"),
        "pointer_reconstruction_passed": pointer_reconstruction.get("passed"),
        "pointer_edge_count": pointer.get("edge_count"),
        "pointer_roles_present": pointer.get("all_roles_present", pointer.get("roles_present")),
        "linked_gpu0_block_count": revision.get("linked_gpu0_block_count")
        or revision.get("gpu0_block_count"),
        "linked_npu_block_count": revision.get("linked_npu_block_count")
        or revision.get("npu_block_count"),
        "concrete_code_proposal_count": concrete_code_proposal_count,
        "applicable_code_product": bool(matrix_items),
        "evidence_product_status": (
            "CODE_PRODUCT_APPLICABLE" if matrix_items else "NO_APPLICABLE_CODE_PRODUCT"
        ),
        "lab_status": lab_status,
        "lab_called": lab.get("lab_called"),
        "lab_evidence_written": lab_evidence_written,
        "lab_report_written": lab.get("lab_report_written"),
        "lab_usable": lab.get("lab_usable"),
        "lab_pass_values": lab.get("lab_pass_values"),
        "lab_required_missing": lab.get("lab_required_missing"),
        "tool_request_count": lab.get("tool_request_count"),
        "tool_execution_count": lab.get("tool_execution_count"),
        "provider_native_tool_call_count": lab.get("provider_native_tool_call_count"),
        "provider_textual_tool_call_count": lab.get("provider_textual_tool_call_count"),
        "matrix_target_count": matrix.get("target_count"),
        "verified_target_count": matrix.get("verified_target_count"),
        "matrix_report": matrix_path,
        "markdown_output": str(markdown_output),
        "text_output": str(text_output),
        "full_code_product_output": str(full_code_product_output),
        "plan_product_full_patch_output": str(plan_product_full_patch_output),
        "json_output": str(output),
        "documents_outputs": documents_outputs,
        "documents_zip": documents_zip,
        "zip_member_count": zip_member_count,
        "plan_product_full_patch_ready": text_product_ready,
        "plan_product_kind": "final_product_text_surface",
        "provider_execution_performed": pointer.get("provider_execution_performed"),
        "patch_application_performed": gate.get("patch_application_performed"),
        "source_writes_performed": gate.get("source_writes_performed"),
    }
    write_json(output, report)
    if documents_json_path:
        write_json(documents_json_path, report)
    if zip_path_for_later and documents_dir_for_later:
        zip_member_count = zip_documents_dir(documents_dir_for_later, zip_path_for_later)
        report["zip_member_count"] = zip_member_count
        write_json(output, report)
        if documents_json_path:
            write_json(documents_json_path, report)
    return report, markdown
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--composer-json", default="")
    parser.add_argument("--gate-report", default="")
    parser.add_argument("--documents-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--text-output", default="")
    parser.add_argument("--zip-output", default="")
    parser.add_argument("--zip-documents", action="store_true")
    return parser.parse_args()
def main() -> int:
    report, _markdown = build_report(parse_args())
    print_json_report(report)
    return 0 if report.get("passed") else 2
if __name__ == "__main__":
    raise SystemExit(main())
