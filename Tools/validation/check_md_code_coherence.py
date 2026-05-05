#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root_from(start: Path) -> Path:
    cur = start.resolve()
    for candidate in [cur, *cur.parents]:
        if (candidate / ".git").exists():
            return candidate
    raise SystemExit(f"Repository root not found from {start}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate code-aware Markdown coherence report thresholds.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", default="output/validation/md_code_coherence_report.json")
    parser.add_argument("--max-high", type=int, default=0)
    parser.add_argument("--max-medium", type=int, default=999999)
    parser.add_argument("--output", default="output/validation/md_code_coherence_check.json")
    args = parser.parse_args()

    repo = repo_root_from(Path(args.repo_root))
    report_path = repo / args.report
    if not report_path.exists():
        builder = repo / "Tools" / "docs" / "build_code_aware_md_coherence.py"
        if not builder.exists():
            raise SystemExit(f"[FAIL] Missing report and builder: {report_path}")
        subprocess.run([
            sys.executable, str(builder),
            "--repo-root", str(repo),
            "--output", str(report_path.relative_to(repo)),
            "--markdown-output", "output/validation/md_code_coherence_report.md",
        ], cwd=repo, check=True)

    data = json.loads(report_path.read_text(encoding="utf-8-sig"))
    severities = data.get("summary", {}).get("by_severity", {})
    high = int(severities.get("high", 0))
    medium = int(severities.get("medium", 0))
    passed = high <= args.max_high and medium <= args.max_medium
    result = {
        "kind": "md_code_coherence_check",
        "passed": passed,
        "report": str(report_path.relative_to(repo)),
        "max_high": args.max_high,
        "actual_high": high,
        "max_medium": args.max_medium,
        "actual_medium": medium,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [] if passed else ["Markdown/code coherence thresholds exceeded."],
        "warnings": [],
    }
    out = repo / args.output
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8", newline="\
")
    print(f"[OK] Wrote {out}")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if passed else 2


if __name__ == "__main__":
    raise SystemExit(main())
