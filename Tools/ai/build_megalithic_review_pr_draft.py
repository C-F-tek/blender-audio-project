#!/usr/bin/env python3
"""Build a PR draft artifact from a megalithic repository review.

This tool does not create a GitHub pull request. It converts review/proposal
artifacts into a PR-ready JSON/Markdown package so a human or a separate GitHub
step can decide whether to create a real PR.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REVIEW = "output/ai_pipeline/megalithic_repo_review.json"
DEFAULT_PROPOSALS = "output/ai_pipeline/megalithic_repo_review_proposals.json"
DEFAULT_OUTPUT = "output/ai_pipeline/megalithic_repo_review_pr_draft.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/megalithic_repo_review_pr_draft.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug[:72] or "megalithic-review-followup"


def proposal_titles(proposals: dict[str, Any]) -> list[str]:
    items = proposals.get("proposals", [])
    titles = []
    for item in items:
        if isinstance(item, dict):
            title = str(item.get("title") or item.get("id") or "review proposal").strip()
            if title:
                titles.append(title)
    return titles


def top_findings(review: dict[str, Any], *, limit: int = 12) -> list[str]:
    out = []
    for finding in review.get("deterministic_findings", [])[:limit]:
        if not isinstance(finding, dict):
            continue
        severity = finding.get("severity", "unknown")
        area = finding.get("area", "unknown")
        title = finding.get("title", "untitled finding")
        out.append(f"[{severity}] {area}: {title}")
    return out


def build_pr_body(review: dict[str, Any], proposals: dict[str, Any], *, branch_name: str) -> str:
    summary = review.get("summary", {})
    proposal_count = int(proposals.get("proposal_count") or 0)
    provider_execution = bool(review.get("provider_execution_performed"))
    lines = [
        "Generated from megalithic repository review artifacts.",
        "",
        "This is a review PR draft. It is intended for manual evaluation before any commit or real PR creation.",
        "",
        "Scope reviewed:",
        "",
        f"- Docs scanned: {summary.get('doc_count')}",
        f"- Code files scanned: {summary.get('code_count')}",
        f"- RAW artifacts scanned: {summary.get('raw_artifact_count')}",
        f"- SQLite memory DBs scanned read-only: {summary.get('sqlite_memory_count')}",
        f"- Validation reports ingested: {summary.get('validation_report_count')}",
        f"- Provider execution performed: {provider_execution}",
        f"- Proposal count: {proposal_count}",
        "",
        "Findings:",
        "",
    ]
    findings = top_findings(review)
    if findings:
        lines.extend(f"- {item}" for item in findings)
    else:
        lines.append("- No deterministic findings recorded.")
    lines.extend(["", "Proposed follow-up:", ""])
    titles = proposal_titles(proposals)
    if titles:
        lines.extend(f"- {title}" for title in titles[:20])
    else:
        lines.append("- No patch/doc proposal is currently necessary.")
    lines.extend(
        [
            "",
            "Suggested branch:",
            "",
            f"```text\n{branch_name}\n```",
            "",
            "Validation checklist:",
            "",
            "- [ ] Review megalithic_repo_review.md",
            "- [ ] Review megalithic_repo_review_proposals.json",
            "- [ ] Apply only selected manual-review proposals",
            "- [ ] Do not commit output/** artifacts",
            "- [ ] Do not commit SQLite memory DB files",
            "- [ ] Run python syntax validation",
            "- [ ] Run validation report contract",
            "- [ ] Run git diff --check",
            "",
            "Guardrails:",
            "",
            "- no automatic patch application",
            "- no Blender runtime execution",
            "- no full analysis JSON changes",
            "- no SQLite DB commit",
            "- no NPU advisory promotion",
            "- no OpenVINO GPU primary lane",
        ]
    )
    return "\n".join(lines) + "\n"


def build_pr_draft(review: dict[str, Any], proposals: dict[str, Any], *, base_branch: str, title_prefix: str) -> dict[str, Any]:
    proposal_count = int(proposals.get("proposal_count") or 0)
    first_title = proposal_titles(proposals)[:1]
    title_suffix = first_title[0] if first_title else "megalithic review follow-up"
    title = f"{title_prefix}: {title_suffix}"
    branch_name = f"codex/{slugify(title_suffix)}"
    body = build_pr_body(review, proposals, branch_name=branch_name)
    return {
        "schema_version": 1,
        "kind": "megalithic_repo_review_pr_draft",
        "generated_at": now_iso(),
        "repo_root": review.get("repo_root"),
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": bool(review.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "manual_review_only_pr_draft",
        "needs_real_pr": proposal_count > 0,
        "proposal_count": proposal_count,
        "base_branch": base_branch,
        "suggested_branch": branch_name,
        "title": title,
        "body": body,
        "review_artifact": review.get("kind"),
        "proposal_artifact": proposals.get("kind"),
        "commands": {
            "create_branch": f"git switch -c {branch_name}",
            "status": "git status --short",
            "validate_python": "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
            "validate_reports": "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
            "diff_check": "git diff --check",
        },
        "guardrails": {
            "real_github_pr_created": False,
            "patch_application_performed": False,
            "output_artifacts_should_not_be_committed": True,
            "sqlite_db_should_not_be_committed": True,
            "manual_review_required": True,
        },
    }


def render_markdown(draft: dict[str, Any]) -> str:
    lines = ["# Megalithic Review PR Draft", ""]
    lines.append(f"- Needs real PR: `{draft['needs_real_pr']}`")
    lines.append(f"- Proposal count: `{draft['proposal_count']}`")
    lines.append(f"- Suggested branch: `{draft['suggested_branch']}`")
    lines.append(f"- Title: `{draft['title']}`")
    lines.append("")
    lines.append("## PR Body")
    lines.append("")
    lines.append(draft["body"])
    lines.append("## Commands")
    lines.append("")
    for name, command in draft["commands"].items():
        lines.append(f"- `{name}`: `{command}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default=DEFAULT_REVIEW)
    parser.add_argument("--proposals", default=DEFAULT_PROPOSALS)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--base-branch", default="master")
    parser.add_argument("--title-prefix", default="review")
    args = parser.parse_args()

    review = read_json(Path(args.review))
    proposals = read_json(Path(args.proposals))
    draft = build_pr_draft(review, proposals, base_branch=args.base_branch, title_prefix=args.title_prefix)

    output = Path(args.output)
    markdown_output = Path(args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(draft, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(draft), encoding="utf-8")

    print(json.dumps({
        "passed": draft["passed"],
        "needs_real_pr": draft["needs_real_pr"],
        "proposal_count": draft["proposal_count"],
        "output": args.output,
        "markdown": args.markdown_output,
        "real_github_pr_created": False,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
