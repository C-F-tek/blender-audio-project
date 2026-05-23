"""CLI for the heap final proposal composer."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from ia_carmine.product.heap_final_proposals.artifacts import (
    build_action_list,
    collect_gpu0_reviews,
    collect_npu_audits,
    compute_product_causality,
    flatten_quality_blockers,
    list_proposals,
    list_provider_reports,
)
from ia_carmine.product.heap_final_proposals.common import (
    discover_run_dir,
    documents_root,
    load_startup_manifest,
    load_startup_reconciliation,
    now_stamp,
    read_json,
    repo_rel,
    resolve_path,
)
from ia_carmine.product.heap_final_proposals.documents import write_documents_package
from ia_carmine.product.heap_final_proposals.rendering import render_markdown
from ia_carmine._shared.report_io import print_json_report

try:
    from ia_carmine._shared.heap_proposal_gate import build_operator_decision, gate_proposals, load_allowlist
except ImportError:  # pragma: no cover
    from ia_carmine._shared.heap_proposal_gate import (  # type: ignore
        build_operator_decision,
        gate_proposals,
        load_allowlist,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", default="")
    parser.add_argument("--report-file", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--write-documents", action="store_true")
    parser.add_argument("--max-proposal-chars", type=int, default=18000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    run_dir = discover_run_dir(repo_root, args.report_file, args.run_dir)
    report_file = (
        resolve_path(repo_root, args.report_file)
        if args.report_file
        else run_dir / "heap_runtime_completeness_gate_report.json"
    )
    report = read_json(report_file)
    startup_manifest = load_startup_manifest(run_dir)
    startup_reconciliation = load_startup_reconciliation(run_dir)
    stamp = str(
        report.get("stamp")
        or startup_manifest.get("stamp")
        or (report.get("metrics") or {}).get("stamp")
        or now_stamp()
    )
    proposals = _load_gated_proposals(repo_root, run_dir)
    provider_reports = list_provider_reports(run_dir)
    blockers = flatten_quality_blockers(report, proposals, startup_manifest)
    gpu0_reviews = collect_gpu0_reviews(proposals, provider_reports)
    npu_audits = collect_npu_audits(proposals, provider_reports)
    action_list = build_action_list(blockers, proposals, startup_manifest)
    product_causality = compute_product_causality(
        report=report,
        startup_manifest=startup_manifest,
        startup_reconciliation=startup_reconciliation,
        proposals=proposals,
        provider_reports=provider_reports,
    )
    operator_decision = _build_operator_decision(repo_root, proposals)
    markdown = render_markdown(
        decision_block=operator_decision,
        repo_root=repo_root,
        run_dir=run_dir,
        report=report,
        startup_manifest=startup_manifest,
        proposals=proposals,
        provider_reports=provider_reports,
        blockers=blockers,
        gpu0_reviews=gpu0_reviews,
        npu_audits=npu_audits,
        action_list=action_list,
        product_causality=product_causality,
        max_proposal_chars=max(2000, int(args.max_proposal_chars)),
    )
    result = _build_result(
        stamp=stamp,
        repo_root=repo_root,
        run_dir=run_dir,
        report_file=report_file,
        report=report,
        startup_manifest=startup_manifest,
        startup_reconciliation=startup_reconciliation,
        proposals=proposals,
        provider_reports=provider_reports,
        blockers=blockers,
        gpu0_reviews=gpu0_reviews,
        npu_audits=npu_audits,
        action_list=action_list,
        product_causality=product_causality,
        operator_decision=operator_decision,
    )
    output = resolve_path(repo_root, args.output) if args.output else run_dir / "heap_final_proposal_composer.json"
    markdown_output = (
        resolve_path(repo_root, args.markdown_output)
        if args.markdown_output
        else run_dir / "heap_final_proposal_composer.md"
    )
    _write_outputs(output, markdown_output, result, markdown, repo_root)
    if args.write_documents:
        document_package = write_documents_package(
            stamp=stamp,
            doc_dir=documents_root(args.documents_root, stamp),
            markdown=markdown,
            json_data=result,
            proposals=proposals,
        )
        result.update(document_package)
        result["download_hint"] = (
            f"Apri o copia il file TXT principale: {document_package['primary_txt']}"
        )
        _write_outputs(output, markdown_output, result, markdown, repo_root)
    print_json_report(result, default=str)
    return 0 if not blockers else 2


def _load_gated_proposals(repo_root: Path, run_dir: Path) -> list[dict[str, Any]]:
    raw_proposals = list_proposals(run_dir)
    try:
        similarity_threshold = float(os.getenv("PROPOSAL_SIMILARITY_THRESHOLD", "0.95"))
    except ValueError:
        similarity_threshold = 0.95
    allowlist_path = os.getenv("PROPOSAL_ALLOWLIST_PATH", "config/allowlist.json")
    allowed_sources, allowlist_enforced, _resolved_allowlist_path = load_allowlist(
        allowlist_path,
        repo_root,
    )
    return gate_proposals(
        proposals=raw_proposals,
        allowed_sources=allowed_sources,
        allowlist_enforced=allowlist_enforced,
        similarity_threshold=similarity_threshold,
    )


def _build_operator_decision(repo_root: Path, proposals: list[dict[str, Any]]) -> dict[str, Any]:
    allowlist_path = os.getenv("PROPOSAL_ALLOWLIST_PATH", "config/allowlist.json")
    _allowed_sources, allowlist_enforced, resolved_allowlist_path = load_allowlist(
        allowlist_path,
        repo_root,
    )
    return build_operator_decision(
        proposals=proposals,
        allowlist_enforced=allowlist_enforced,
        allowlist_path=resolved_allowlist_path if allowlist_enforced else "",
    )


def _build_result(
    *,
    stamp: str,
    repo_root: Path,
    run_dir: Path,
    report_file: Path,
    report: dict[str, Any],
    startup_manifest: dict[str, Any],
    startup_reconciliation: dict[str, Any],
    proposals: list[dict[str, Any]],
    provider_reports: list[dict[str, Any]],
    blockers: list[str],
    gpu0_reviews: list[dict[str, Any]],
    npu_audits: list[dict[str, Any]],
    action_list: list[str],
    product_causality: dict[str, Any],
    operator_decision: dict[str, Any],
) -> dict[str, Any]:
    accepted = [item for item in proposals if item.get("accepted")]
    rejected = [item for item in proposals if not item.get("accepted")]
    return {
        "schema_version": 1,
        "kind": "heap_final_proposal_composer",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "run_dir": repo_rel(repo_root, run_dir),
        "report_file": repo_rel(repo_root, report_file),
        "startup_manifest": startup_manifest,
        "startup_reload_degraded": bool(startup_manifest.get("startup_reload_degraded")),
        "proposal_count": len(proposals),
        "accepted_proposal_count": len(accepted),
        "rejected_proposal_count": len(rejected),
        "provider_report_count": len(provider_reports),
        "gpu0_review_count": len(gpu0_reviews),
        "npu_audit_count": len(npu_audits),
        "blocking_issue_count": len(blockers),
        "blocking_issues": blockers,
        "action_list": action_list,
        "product_status": (report.get("metrics") or {}).get("product_status")
        or (report.get("real_run_output_contract") or {}).get("product_status"),
        "quality_output_passed": (report.get("metrics") or {}).get("quality_output_passed"),
        "operator_decision": operator_decision,
        "product_causality": product_causality,
        "product_causality_status": product_causality.get("product_causality_status"),
        "product_causality_passed": product_causality.get("product_causality_passed"),
        "startup_reconciliation": startup_reconciliation,
        "proposals": [_proposal_summary(item) for item in proposals],
        "accepted_proposals": [item.get("name") for item in accepted],
        "rejected_proposals": [
            {"name": item.get("name"), "reason": item.get("reject_reason")} for item in rejected
        ],
        "gpu0_reviews": gpu0_reviews,
        "npu_audits": npu_audits,
        "provider_reports": [_provider_summary(repo_root, item) for item in provider_reports],
    }


def _proposal_summary(item: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "name",
        "block_id",
        "revision",
        "source",
        "quality_passed",
        "accepted",
        "reject_reason",
        "target_files",
        "declared_target_files",
        "verified_declared_target_files",
        "allowlist_candidate_files",
        "rejected_unverified_refs",
        "validation_commands",
        "rejected_validation_refs",
        "provider_execution_performed",
        "implementation_quality",
        "proposal_progress",
        "operator_gate_passed",
        "operator_gate_reasons",
        "operator_gate_targets",
        "gpu0_review",
        "npu_micro_task_piece",
        "npu_workload_audit",
        "anchored_source_candidates",
    )
    return {key: item.get(key) for key in keys}


def _provider_summary(repo_root: Path, item: dict[str, Any]) -> dict[str, Any]:
    path = repo_rel(repo_root, item["path"]) if isinstance(item.get("path"), Path) else ""
    return {
        "path": path,
        "kind": item.get("kind"),
        "lane": item.get("lane"),
        "passed": item.get("passed"),
        "provider_execution_performed": item.get("provider_execution_performed"),
        "npu_device_workload": item.get("npu_device_workload"),
        "errors": item.get("errors"),
        "warnings": item.get("warnings"),
    }


def _write_outputs(
    output: Path,
    markdown_output: Path,
    result: dict[str, Any],
    markdown: str,
    repo_root: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    result["output"] = repo_rel(repo_root, output)
    result["markdown_output"] = repo_rel(repo_root, markdown_output)
    output.write_text(
        json.dumps(result, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    markdown_output.write_text(markdown, encoding="utf-8")
