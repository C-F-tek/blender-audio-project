from __future__ import annotations

from .common import *  # noqa: F403

def build_proposals(review: dict[str, Any]) -> dict[str, Any]:
    proposals: list[dict[str, Any]] = []
    for finding in review.get("deterministic_findings", []):
        if finding.get("severity") in {"high", "medium", "low"}:
            proposals.append(
                {
                    "id": f"MEGA-{len(proposals) + 1:03d}",
                    "title": finding.get("title"),
                    "area": finding.get("area"),
                    "apply_mode": "manual_review_only",
                    "content_status": "proposal_only",
                    "details": finding.get("details", []),
                }
            )
    ollama_json = review.get("ollama_review", {}).get("response_json")
    if isinstance(ollama_json, dict):
        for item in ollama_json.get("patch_proposals", []) or []:
            if isinstance(item, dict):
                proposal = dict(item)
                proposal.setdefault("id", f"OLLAMA-MEGA-{len(proposals) + 1:03d}")
                proposal.setdefault("apply_mode", "manual_review_only")
                proposal.setdefault("content_status", "proposal_only")
                proposals.append(proposal)
    return {
        "schema_version": 1,
        "kind": "megalithic_repo_review_proposals",
        "repo_root": review["repo_root"],
        "passed": True,
        "errors": [],
        "warnings": [],
        "provider_execution_performed": review["provider_execution_performed"],
        "patch_application_performed": False,
        "apply_mode": "manual_review_only",
        "proposal_count": len(proposals),
        "proposals": proposals,
    }

def render_markdown(review: dict[str, Any], proposals: dict[str, Any]) -> str:
    lines = ["# Megalithic Repository Review", ""]
    lines.append(f"- Generated at: `{review['generated_at']}`")
    lines.append(f"- Provider execution performed: `{review['provider_execution_performed']}`")
    lines.append(f"- Ollama used: `{review['ollama_review']['used']}`")
    lines.append(f"- Docs scanned: `{review['summary']['doc_count']}`")
    lines.append(f"- Code files scanned: `{review['summary']['code_count']}`")
    lines.append(f"- RAW artifacts scanned: `{review['summary']['raw_artifact_count']}`")
    lines.append(f"- SQLite memory DBs scanned: `{review['summary']['sqlite_memory_count']}`")
    lines.append(f"- Proposal count: `{proposals['proposal_count']}`")
    lines.append("")
    lines.append("## Resource lanes")
    lines.append("")
    for lane, details in review["resource_lanes"].items():
        lines.append(f"- `{lane}`: {details}")
    lines.append("")
    lines.append("## Deterministic findings")
    lines.append("")
    for finding in review["deterministic_findings"]:
        lines.append(f"### {finding['severity']} — {finding['title']}")
        lines.append(f"- Area: `{finding['area']}`")
        for detail in finding.get("details", [])[:30]:
            lines.append(f"- {detail}")
        lines.append("")
    if review["ollama_review"].get("response_text"):
        lines.append("## Ollama semantic review")
        lines.append("")
        lines.append("```text")
        lines.append(review["ollama_review"]["response_text"][:16000])
        lines.append("```")
        lines.append("")
    lines.append("## Proposals")
    lines.append("")
    for proposal in proposals["proposals"]:
        lines.append(
            f"- `{proposal.get('id')}` {proposal.get('title')} ({proposal.get('apply_mode')})"
        )
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    for key, value in review["guardrails"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"

def write_outputs(
    review: dict[str, Any], proposals: dict[str, Any], args: argparse.Namespace
) -> None:
    output = Path(args.output)
    markdown_output = Path(args.markdown_output)
    proposal_output = Path(args.proposal_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    proposal_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(review, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    proposal_output.write_text(
        json.dumps(proposals, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    markdown_output.write_text(render_markdown(review, proposals), encoding="utf-8")
