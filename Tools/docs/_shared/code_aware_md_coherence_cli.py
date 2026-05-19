from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from Tools.docs._shared.code_aware_md_coherence_core import (
        analyze_markdown,
        build_script_maps,
        repo_root_from,
        summarize,
    )
    from Tools.docs.docs_hygiene.code_aware_md_coherence_render import render_markdown
except ModuleNotFoundError:  # pragma: no cover - direct script fallback
    from Tools.docs._shared.code_aware_md_coherence_core import (
        analyze_markdown,
        build_script_maps,
        repo_root_from,
        summarize,
    )
    from code_aware_md_coherence_render import render_markdown


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo = repo_root_from(Path(args.repo_root))
    scripts = build_script_maps(repo)
    md = analyze_markdown(repo, scripts, args.max_lines)
    report: dict[str, Any] = {
        "kind": "md_code_coherence_report",
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "repo_root": str(repo),
        "max_lines": args.max_lines,
        "inventory": {
            "markdown_file_count": len(md["documents"]),
            "python_script_count": len(scripts["python"]),
            "powershell_script_count": len(scripts["powershell"]),
        },
        "scripts": scripts,
        "documents": md["documents"],
        "findings": md["findings"],
    }
    report["summary"] = summarize(report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a code-aware Markdown coherence report.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--max-lines", type=int, default=400)
    parser.add_argument("--output", default="output/validation/md_code_coherence_report.json")
    parser.add_argument("--markdown-output", default="output/validation/md_code_coherence_report.md")
    parser.add_argument("--max-markdown-finding-rows", type=int, default=120)
    args = parser.parse_args()

    report = build_report(args)
    repo = Path(report["repo_root"])
    out = repo / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_out = repo / args.markdown_output
    md_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.write_text(render_markdown(report, args.max_markdown_finding_rows), encoding="utf-8")
    print(f"[OK] Wrote {out.relative_to(repo)}")
    print(f"[OK] Wrote {md_out.relative_to(repo)}")
    print(json.dumps(report["summary"], indent=2, ensure_ascii=False))
    return 0
