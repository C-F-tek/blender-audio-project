from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import DEFAULT_REPORT_JSON, PROJECT_DIR
from .report import build_report, format_report, save_report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Spaziotempo startup service check")
    parser.add_argument(
        "--project", default=str(PROJECT_DIR), help="Project/repository directory to inspect."
    )
    parser.add_argument(
        "--repo-root",
        default="",
        help="Compatibility alias used by IA-Carmine launchers. Maps to the project/repository directory.",
    )
    parser.add_argument(
        "--root",
        default="",
        help="Workspace root. Defaults to the parent of the selected project/repository directory.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_REPORT_JSON),
        help="JSON report output path. Defaults to output/workflow_logs/startup_check.json.",
    )
    parser.add_argument(
        "--text-output",
        default="",
        help="Optional text report output path. Defaults to the JSON output path with .txt suffix.",
    )
    parser.add_argument("--json", action="store_true", help="Print the JSON report to stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.repo_root or args.project).resolve(strict=False)
    workspace_root = Path(args.root).resolve(strict=False) if args.root else project.parent
    output_path = Path(args.output).resolve(strict=False)
    text_output_path = (
        Path(args.text_output).resolve(strict=False)
        if args.text_output
        else output_path.with_suffix(".txt")
    )
    report = build_report(project, workspace_root)
    save_report(report, output_path, text_output_path)
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(format_report(report, output_path))
    return 0
