from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.docs.markdown_split_tool_guide import write_root_tool_guide
    from Tools.docs._shared.markdown_splits_refactor_core import (
        DEFAULT_MAX_LINES,
        DEFAULT_SCOPES,
        find_legacy_split_dirs,
        git_status,
        migrate_legacy_dir,
        prune_obsolete,
        rel,
        repo_root,
        skipped,
        split_monolithic_file,
        write,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script fallback
    from markdown_split_tool_guide import write_root_tool_guide
    from Tools.docs._shared.markdown_splits_refactor_core import (
        DEFAULT_MAX_LINES,
        DEFAULT_SCOPES,
        find_legacy_split_dirs,
        git_status,
        migrate_legacy_dir,
        prune_obsolete,
        rel,
        repo_root,
        skipped,
        split_monolithic_file,
        write,
    )


def collect_results(args: argparse.Namespace, root: Path, scopes: list[str]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    if args.migrate_legacy_splits:
        for old in find_legacy_split_dirs(root, scopes):
            results.append(migrate_legacy_dir(old, root, args.max_lines, args.apply))
    if args.split_monolithic:
        for scope in scopes:
            base = (root / scope).resolve()
            files = (
                [base]
                if base.is_file()
                else [p for p in base.rglob("*.md") if p.is_file()]
                if base.exists()
                else []
            )
            for path in sorted(files):
                if not skipped(path, root) and path.suffix == ".md" and path.exists():
                    item = split_monolithic_file(path, root, args.max_lines, args.apply)
                    if item.get("action") != "skip":
                        results.append(item)
    if args.prune_obsolete_snapshots:
        results.extend(prune_obsolete(root, args.apply))
    if args.write_root_tool_guide:
        results.append(write_root_tool_guide(root, args.apply, write, rel))
    return results


def render_md(report: dict[str, Any]) -> str:
    lines = [
        "# Markdown refactor report",
        "",
        f"- Apply: `{report['apply']}`",
        f"- Max lines: `{report['max_lines']}`",
        f"- Results: `{len(report['results'])}`",
        "",
        "## Results",
        "",
    ]
    for item in report["results"]:
        lines.append(
            f"- `{item.get('path')}` action=`{item.get('action')}` target=`{item.get('target_dir', '')}`"
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES)
    ap.add_argument("--scope", action="append", default=[])
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--migrate-legacy-splits", action="store_true")
    ap.add_argument("--split-monolithic", action="store_true")
    ap.add_argument("--prune-obsolete-snapshots", action="store_true")
    ap.add_argument("--write-root-tool-guide", action="store_true")
    ap.add_argument("--output", default="output/validation/markdown_refactor_report.json")
    ap.add_argument("--markdown-output", default="output/validation/markdown_refactor_report.md")
    args = ap.parse_args()

    root = repo_root(Path(args.repo_root))
    results = collect_results(args, root, args.scope or list(DEFAULT_SCOPES))
    report = {
        "kind": "ia_carmine_markdown_refactor",
        "apply": bool(args.apply),
        "max_lines": args.max_lines,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "results": results,
        "git_status_after": git_status(root) if args.apply else [],
    }
    out = root / args.output
    md = root / args.markdown_output
    out.parent.mkdir(parents=True, exist_ok=True)
    md.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    md.write_text(render_md(report), encoding="utf-8")
    print(f"[OK] report={rel(out, root)} results={len(results)} apply={args.apply}")
    for item in results:
        print(f"[{item.get('action')}] {item.get('path')} -> {item.get('target_dir', '')}")
    return 0
