"""Report assembly for agent-review evidence sufficiency."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .evidence_analysis import analyze_code_code, analyze_doc_code, analyze_doc_doc, build_decision
from .evidence_common import (
    load_json_object,
    load_optional_report,
    now_iso,
    repo_rel,
    resolve_path,
)

def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    refined_path = resolve_path(repo_root, args.refined_review)
    proposals_path = resolve_path(repo_root, args.refined_proposals)
    if not refined_path.exists():
        missing = repo_rel(refined_path, repo_root)
        proposal_missing = not proposals_path.exists()
        return {
            "schema_version": 1,
            "kind": "agent_review_evidence_sufficiency",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": False,
            "errors": [f"blocked_missing_refined_review_input: {missing}"],
            "warnings": [
                "Evidence sufficiency input is missing; the heap runtime must classify this instead of raising a traceback.",
            ],
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "apply_mode": "report_only_evidence_sufficiency",
            "inputs": {
                "refined_review": missing,
                "refined_review_exists": False,
                "refined_proposals": repo_rel(proposals_path, repo_root),
                "refined_proposals_exists": not proposal_missing,
                "refined_proposal_count": None,
                "context_reports": [
                    load_optional_report(repo_root, value) for value in args.report_file
                ],
            },
            "areas": {
                "doc_code": {
                    "area": "doc_code",
                    "item_count": 0,
                    "ready_for_manual_patch_count": 0,
                    "needs_more_context_count": 0,
                    "items": [],
                },
                "doc_doc": {
                    "area": "doc_doc",
                    "item_count": 0,
                    "ready_for_manual_patch_count": 0,
                    "needs_more_context_count": 0,
                    "items": [],
                },
                "code_code": {
                    "area": "code_code",
                    "item_count": 0,
                    "ready_for_manual_patch_count": 0,
                    "needs_more_context_count": 0,
                    "items": [],
                },
            },
            "decision": {
                "ready_for_manual_patch_count": 0,
                "needs_more_context_count": 0,
                "recommended_mode": "blocked_missing_refined_review_input",
                "sufficient_for_real_pr": False,
                "next_steps": [
                    "Generate refined review/proposals or rewire this lane to current-run reports before acceptance."
                ],
            },
            "guardrails": {
                "report_only": True,
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "real_github_pr_created": False,
                "sqlite_write_performed": False,
                "persistent_memory_write_performed": False,
                "manual_review_required": True,
            },
        }
    refined = load_json_object(refined_path)
    proposals = load_json_object(proposals_path) if proposals_path.exists() else {}
    doc_code = analyze_doc_code(refined, repo_root)
    doc_doc = analyze_doc_doc(refined, repo_root)
    code_code = analyze_code_code(refined, repo_root)
    decision = build_decision(doc_code, doc_doc, code_code)
    context_reports = [load_optional_report(repo_root, value) for value in args.report_file]
    warnings = [
        f"context report missing/unreadable: {item['path']} ({item['error']})"
        for item in context_reports
        if item.get("error")
    ]
    return {
        "schema_version": 1,
        "kind": "agent_review_evidence_sufficiency",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_evidence_sufficiency",
        "inputs": {
            "refined_review": repo_rel(refined_path, repo_root),
            "refined_proposals": repo_rel(proposals_path, repo_root),
            "refined_proposal_count": proposals.get("proposal_count"),
            "context_reports": context_reports,
        },
        "areas": {
            "doc_code": doc_code,
            "doc_doc": doc_doc,
            "code_code": code_code,
        },
        "decision": decision,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "manual_review_required": True,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Evidence Sufficiency", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Recommended mode: `{report['decision']['recommended_mode']}`")
    lines.append(f"- Sufficient for real PR: `{report['decision']['sufficient_for_real_pr']}`")
    lines.append(
        f"- Ready patch candidates: `{report['decision']['ready_for_manual_patch_count']}`"
    )
    lines.append(f"- Needs more context: `{report['decision']['needs_more_context_count']}`")
    lines.append("")
    for step in report["decision"].get("next_steps", []):
        lines.append(f"- {step}")
    lines.append("")
    for area_name, area in report["areas"].items():
        lines.append(f"## {area_name}")
        lines.append("")
        lines.append(f"- Items: `{area['item_count']}`")
        lines.append(f"- Ready: `{area['ready_for_manual_patch_count']}`")
        lines.append(f"- Needs context: `{area['needs_more_context_count']}`")
        lines.append("")
        for item in area.get("items", [])[:20]:
            label = item.get("path") or item.get("doc") or item.get("symbol")
            lines.append(f"### {label}")
            lines.append(f"- Recommendation: `{item.get('recommendation')}`")
            lines.append(f"- Evidence sufficient: `{item.get('evidence_sufficient')}`")
            lines.append(f"- Confidence: `{item.get('confidence')}`")
            lines.append(f"- Reason: {item.get('reason')}")
            if item.get("reference"):
                lines.append(f"- Reference: `{item.get('reference')}`")
            if item.get("missing_terms"):
                lines.append(f"- Missing terms: `{item.get('missing_terms')}`")
            lines.append("")
    return "\n".join(lines) + "\n"
