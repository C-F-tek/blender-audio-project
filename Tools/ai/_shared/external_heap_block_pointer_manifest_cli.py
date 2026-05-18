from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from build_external_heap_block_pointer_manifest import build_report
except ModuleNotFoundError:
    from Tools.ai.external_heap.block_pointer_manifest import build_report


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Block Pointer Manifest",
        "",
        f"- Protocol: `{report.get('protocol')}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Pointer product contract: `{report.get('pointer_product_contract')}`",
        f"- Pointer contract role: `{report.get('pointer_contract_role')}`",
        f"- Provider execution semantics: `{report.get('provider_execution_semantics')}`",
        f"- Block count: `{report.get('block_count')}`",
        f"- Source block count: `{report.get('source_block_count')}`",
        f"- Max blocks applied: `{report.get('max_blocks_applied')}`",
        f"- Edge count: `{report.get('edge_count')}`",
        f"- Roles present: `{report.get('roles_present')}`",
        f"- All roles present: `{report.get('all_roles_present')}`",
        f"- Forward pointers: `{report.get('has_forward_pointers')}`",
        f"- Back-refinement pointers: `{report.get('has_backrefinement_pointers')}`",
        f"- Resume pointers: `{report.get('has_resume_pointers')}`",
        "",
        "## Blocks",
        "",
    ]
    for block in report.get("blocks") or []:
        lines.extend(
            [
                f"### `{block.get('block_id')}`",
                "",
                f"- Type: `{block.get('block_type')}`",
                f"- Role: `{block.get('role')}`",
                f"- Source: `{block.get('source_path')}`",
                f"- Previous: `{block.get('previous_block_id')}`",
                f"- Next: `{block.get('next_block_id')}`",
                f"- Refines: `{block.get('refines_block_id')}`",
                f"- Resume from: `{block.get('resume_from_block_id')}`",
                f"- Accepted: `{block.get('accepted')}`",
                f"- Preview source: `{block.get('preview_source')}`",
                f"- Pointer contract: `{block.get('pointer_contract')}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--max-block-chars", type=int, default=9000)
    parser.add_argument("--max-blocks", type=int, default=0)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_dir = Path(args.run_dir).resolve()
    output = Path(args.output).resolve() if args.output else run_dir / "external_heap_block_pointer_manifest.json"
    markdown_output = (
        Path(args.markdown_output).resolve() if args.markdown_output else output.with_suffix(".md")
    )
    report = build_report(repo_root, run_dir, args.max_block_chars, args.max_blocks)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0
