#!/usr/bin/env python3
"""Smoke test for Markdown split shadow applier."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], repo_root: Path) -> dict[str, object]:
    proc = subprocess.run(cmd, cwd=repo_root, text=True, capture_output=True, check=False)
    if proc.stdout:
        print(proc.stdout)
    if proc.stderr:
        print(proc.stderr, file=sys.stderr)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)
    output = Path(cmd[cmd.index("--output") + 1])
    return json.loads(output.read_text(encoding="utf-8"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default="output/validation/full0to10_markdown_split_shadow_smoke")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    work_dir = repo_root / args.work_dir
    sample_root = work_dir / "repo"
    sample_root.mkdir(parents=True, exist_ok=True)
    long_title = "AI Context Pack Core AI Backend Generated At 2026 05 01 " * 8
    md = sample_root / "large.md"
    md.write_text(f"# Root\nintro\n\n## {long_title}\nalpha\n\n## B\nbeta\n", encoding="utf-8")
    specs = work_dir / "patch_specs.json"
    specs.write_text(json.dumps([
        {"candidate_kind": "markdown_split", "target_path": "large.md"},
        {"candidate_kind": "code_split_candidate", "target_path": "large.md"},
    ], indent=2), encoding="utf-8")

    cli = repo_root / "Tools/ai/apply_full0to10_markdown_split_patch_specs.py"
    dry = run([
        sys.executable, str(cli), "--repo-root", str(sample_root), "--patch-specs", str(specs),
        "--output", str(work_dir / "dry.json"), "--markdown-output", str(work_dir / "dry.md"),
    ], repo_root)
    applied = run([
        sys.executable, str(cli), "--repo-root", str(sample_root), "--patch-specs", str(specs), "--apply-shadow",
        "--output", str(work_dir / "apply.json"), "--markdown-output", str(work_dir / "apply.md"),
    ], repo_root)

    shadow = sample_root / "large.md.split" / "README.md"
    child_files = list((sample_root / "large.md.split").glob("*.md"))
    max_name = max(len(path.name) for path in child_files)
    summary = {
        "passed": dry["accepted_count"] == 1 and applied["written_file_count"] >= 2 and shadow.exists() and md.exists() and max_name <= 96,
        "dry_accepted": dry["accepted_count"],
        "written": applied["written_file_count"],
        "original_still_exists": md.exists(),
        "max_child_filename_length": max_name,
    }
    print(json.dumps(summary, indent=2))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
