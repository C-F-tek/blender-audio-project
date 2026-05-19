from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from build_full_context_golden_proposals import (
        build_payload,
        repo_relative,
        resolve_repo_path,
    )
except ModuleNotFoundError:
    from Tools.ai.agent_context.full_context_golden_proposals import (
        build_payload,
        repo_relative,
        resolve_repo_path,
    )


def render_markdown(payload: dict[str, Any]) -> str:
    lines = [
        "# Full-Context Golden Proposals",
        "",
        f"- Generated at: `{payload['generated_at']}`",
        f"- Proposal count: `{len(payload['proposals'])}`",
        f"- Apply mode: `{payload['apply_mode']}`",
        f"- Provider execution performed: `{payload['provider_execution_performed']}`",
        "",
    ]
    for proposal in payload["proposals"]:
        lines.extend(_proposal_lines(proposal))
    return "\n".join(lines).rstrip() + "\n"


def _proposal_lines(proposal: dict[str, Any]) -> list[str]:
    lines = [
        f"## {proposal['id']}: {proposal['title']}",
        "",
        f"- Priority: `{proposal['priority']}`",
        f"- Area: `{proposal['area']}`",
        f"- Change type: `{proposal['change_type']}`",
        f"- Risk: `{proposal['risk_level']}`",
        f"- Apply allowed now: `{proposal['apply_allowed_now']}`",
        f"- Requires manual review: `{proposal['requires_manual_review']}`",
        "",
        proposal["rationale"],
        "",
        "Target files:",
    ]
    lines.extend(f"- `{target}`" for target in proposal["target_files"])
    lines.extend(["", "Patch sketch:"])
    lines.extend(f"- {item}" for item in proposal["patch_sketch"])
    lines.extend(["", "Validation commands:"])
    lines.extend(f"- `{command}`" for command in proposal["validation_commands"])
    lines.append("")
    return lines


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--source-report", default="", help="Optional source proposal/report JSON")
    parser.add_argument("--output", default="output/ai_pipeline/full_context_golden_proposals.json")
    parser.add_argument(
        "--markdown-output",
        default="output/ai_pipeline/full_context_golden_proposals.md",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output = resolve_repo_path(repo_root, args.output)
    markdown_output = resolve_repo_path(repo_root, args.markdown_output)
    payload = build_payload(repo_root, args.source_report)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(payload), encoding="utf-8")
    print(json.dumps(_summary(payload, output, markdown_output, repo_root), indent=2, ensure_ascii=False))
    return 0


def _summary(payload: dict[str, Any], output: Path, markdown_output: Path, repo_root: Path) -> dict[str, Any]:
    return {
        "passed": payload["passed"],
        "kind": payload["kind"],
        "proposal_count": len(payload["proposals"]),
        "output": repo_relative(output, repo_root),
        "markdown_output": repo_relative(markdown_output, repo_root),
    }
