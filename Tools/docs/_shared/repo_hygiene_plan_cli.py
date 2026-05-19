from __future__ import annotations

import argparse
import json
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.docs._shared.repo_hygiene_plan_core import (
        build_bundle,
        classify_markdown,
        classify_split_dirs,
        iter_files,
        repo_root_from,
    )
except ModuleNotFoundError:  # pragma: no cover - direct script fallback
    from Tools.docs._shared.repo_hygiene_plan_core import (
        build_bundle,
        classify_markdown,
        classify_split_dirs,
        iter_files,
        repo_root_from,
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Repository Hygiene Plan",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Markdown items: `{report['summary']['item_count']}`",
        f"- PatchKit bundle: `{report.get('patchkit_bundle', {}).get('path', '')}`",
        "",
        "## Summary",
        "",
        f"- By classification: `{json.dumps(report['summary']['by_classification'], ensure_ascii=False)}`",
        f"- By action: `{json.dumps(report['summary']['by_action'], ensure_ascii=False)}`",
        "",
        "## High/medium priority items",
        "",
        "| Confidence | Classification | Action | Path | Delete marker | Reason | Lines |",
        "|---|---|---|---|---|---|---:|",
    ]
    rows = [item for item in report["items"] if item["confidence"] in {"high", "medium"}]
    for item in rows[:160]:
        lines.append(
            f"| {item['confidence']} | {item['classification']} | {item['recommended_action']} | `{item['path']}` | `{item.get('delete_marker', '')}` | {item['reason']} | {item['line_count']} |"
        )
    if len(rows) > 160:
        lines.append(f"\n_Truncated {len(rows) - 160} more items; see JSON._")
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "This report is advisory. Delete operations require a PatchKit bundle, explicit review branch and validators.",
        ]
    )
    return "\n".join(lines) + "\n"


def build_summary(items: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "item_count": len(items),
        "by_classification": dict(Counter(item["classification"] for item in items).most_common()),
        "by_action": dict(Counter(item["recommended_action"] for item in items).most_common()),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Build repo hygiene cleanup/refactor plan.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-lines", type=int, default=400)
    parser.add_argument("--output", default="output/validation/repo_hygiene_plan.json")
    parser.add_argument("--markdown-output", default="output/validation/repo_hygiene_plan.md")
    parser.add_argument("--emit-patchkit-bundle", default="")
    args = parser.parse_args()

    root = repo_root_from(Path(args.repo_root))
    items = [
        classify_markdown(root, path, args.max_lines)
        for path in iter_files(root, (".md",))
    ]
    items.extend(classify_split_dirs(root))
    items_dicts = [item.__dict__ for item in sorted(items, key=lambda i: (i.classification, i.path))]
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "repo_hygiene_plan",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "summary": build_summary(items_dicts),
        "items": items_dicts,
    }
    if args.emit_patchkit_bundle:
        report["patchkit_bundle"] = build_bundle(report, root, root / args.emit_patchkit_bundle)
    out = root / args.output
    md = root / args.markdown_output
    out.parent.mkdir(parents=True, exist_ok=True)
    md.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {"passed": True, "summary": report["summary"], "patchkit_bundle": report.get("patchkit_bundle")},
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0
