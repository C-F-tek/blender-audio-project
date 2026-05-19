from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path

try:
    from Tools.docs._shared.large_markdown_splitter_core import (
        DEFAULT_MAX_LINES,
        DEFAULT_SCOPES,
        find_repo_root,
        git_status,
        iter_markdown_files,
        repo_relative,
        split_file,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script fallback
    from Tools.docs._shared.large_markdown_splitter_core import (
        DEFAULT_MAX_LINES,
        DEFAULT_SCOPES,
        find_repo_root,
        git_status,
        iter_markdown_files,
        repo_relative,
        split_file,
    )


def render_markdown_report(report: dict[str, object]) -> str:
    lines = [
        "# Markdown line budget report",
        "",
        f"- Kind: `{report['kind']}`",
        f"- Apply: `{report['apply']}`",
        f"- Max lines: `{report['max_lines']}`",
        f"- Scanned files: `{report['scanned_file_count']}`",
        f"- Oversized files: `{report['oversized_file_count']}`",
        f"- Split operations: `{report['split_operation_count']}`",
        "",
        "## Results",
        "",
    ]
    for item in report["results"]:  # type: ignore[index]
        lines.append(
            f"- `{item.get('path')}` action=`{item.get('action')}` lines=`{item.get('original_lines', item.get('line_count'))}`"
        )
    lines.append("")
    return "\n".join(lines)


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Split large Markdown files into bounded folders.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--include-evidence", action="store_true")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", default="output/validation/markdown_line_budget_report.json")
    parser.add_argument("--markdown-output", default="output/validation/markdown_line_budget_report.md")
    return parser


def main() -> int:
    args = build_arg_parser().parse_args()
    repo_root = find_repo_root(Path(args.repo_root))
    scopes = tuple(args.scope) if args.scope else DEFAULT_SCOPES
    files = iter_markdown_files(repo_root, scopes, args.include_evidence)
    oversized = [item for item in files if item.line_count > args.max_lines]
    results = [split_file(item, repo_root, args.max_lines, args.apply) for item in oversized]
    report = {
        "kind": "ia_carmine_markdown_line_budget_split",
        "repo_root": str(repo_root),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "apply": bool(args.apply),
        "max_lines": args.max_lines,
        "scopes": list(scopes),
        "include_evidence": bool(args.include_evidence),
        "scanned_file_count": len(files),
        "oversized_file_count": len(oversized),
        "split_operation_count": len(results),
        "results": results,
        "git_status_after": git_status(repo_root) if args.apply else [],
    }
    output = repo_root / args.output
    md_output = repo_root / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    md_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md_output.write_text(render_markdown_report(report), encoding="utf-8")
    print(f"[OK] Report: {repo_relative(output, repo_root)}")
    print(f"[OK] Markdown report: {repo_relative(md_output, repo_root)}")
    print(f"[OK] Scanned={len(files)} oversized={len(oversized)} apply={args.apply}")
    for result in results:
        print(f"[{result.get('action')}] {result.get('path')} -> {result.get('target_dir', '')}")
    return 0
