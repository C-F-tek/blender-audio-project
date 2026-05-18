"""Report assembly for megalithic review refinement."""

from __future__ import annotations

from typing import Any

from .common import now_iso, refine_validation_reports
from .doc_refs import refine_doc_code, refine_doc_doc
from .duplicates import refine_code_code

def build_proposals(findings: list[dict[str, Any]], review: dict[str, Any]) -> dict[str, Any]:
    proposals = []
    for finding in findings:
        if finding.get("severity") in {"high", "medium", "low"}:
            proposals.append(
                {
                    "id": f"REFINED-MEGA-{len(proposals) + 1:03d}",
                    "title": finding.get("title"),
                    "area": finding.get("area"),
                    "apply_mode": "manual_review_only",
                    "content_status": "proposal_only",
                    "details": finding.get("details", []),
                }
            )
    return {
        "schema_version": 1,
        "kind": "megalithic_refined_review_proposals",
        "repo_root": review.get("repo_root"),
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": bool(review.get("provider_execution_performed")),
        "patch_application_performed": False,
        "apply_mode": "manual_review_only",
        "proposal_count": len(proposals),
        "proposals": proposals,
    }

def refine_review(review: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    validation_findings, validation_info = refine_validation_reports(review)
    doc_code_findings, doc_code_meta = refine_doc_code(review)
    doc_doc_findings, doc_doc_meta = refine_doc_doc(review)
    code_code_findings, code_code_meta = refine_code_code(review)
    findings = validation_findings + doc_code_findings + doc_doc_findings + code_code_findings
    informational = validation_info
    if not findings:
        findings.append(
            {
                "severity": "info",
                "area": "baseline",
                "title": "No high-confidence actionable discrepancy after signal refinement",
                "details": [
                    "The wide megalithic scan produced only expected guardrails or low-signal findings."
                ],
            }
        )
    refined = {
        "schema_version": 1,
        "kind": "megalithic_refined_review",
        "generated_at": now_iso(),
        "repo_root": review.get("repo_root"),
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": bool(review.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_manual_review_only",
        "original_review_kind": review.get("kind"),
        "original_summary": review.get("summary", {}),
        "refined_findings": findings,
        "informational_findings": informational,
        "refinement": {
            "doc_code": doc_code_meta,
            "doc_doc": doc_doc_meta,
            "code_code": code_code_meta,
        },
        "guardrails": {
            "report_only": True,
            "provider_execution_explicit_only": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "output_artifacts_should_not_be_committed": True,
            "sqlite_db_should_not_be_committed": True,
        },
    }
    proposals = build_proposals(findings, review)
    return refined, proposals

def render_markdown(refined: dict[str, Any], proposals: dict[str, Any]) -> str:
    lines = ["# Megalithic Review Signal Refinement", ""]
    lines.append(
        f"- Provider execution performed upstream: `{refined['provider_execution_performed']}`"
    )
    lines.append(f"- Proposal count: `{proposals['proposal_count']}`")
    lines.append("")
    lines.append("## Refined findings")
    lines.append("")
    for finding in refined["refined_findings"]:
        lines.append(f"### {finding.get('severity')} — {finding.get('title')}")
        lines.append(f"- Area: `{finding.get('area')}`")
        for detail in finding.get("details", [])[:30]:
            lines.append(f"- {detail}")
        lines.append("")
    if refined.get("informational_findings"):
        lines.append("## Informational / expected guardrails")
        lines.append("")
        for finding in refined["informational_findings"]:
            lines.append(f"### {finding.get('title')}")
            for detail in finding.get("details", [])[:20]:
                lines.append(f"- {detail}")
            lines.append("")
    lines.append("## Refinement counters")
    lines.append("")
    lines.append(
        f"- Resolved doc/code refs: `{refined['refinement']['doc_code'].get('resolved_count', 0)}`"
    )
    lines.append(f"- Ignored doc/code refs: `{refined['refinement']['doc_code']['ignored_count']}`")
    lines.append(
        f"- Ignored code/code duplicates: `{refined['refinement']['code_code']['ignored_count']}`"
    )
    return "\n".join(lines) + "\n"
