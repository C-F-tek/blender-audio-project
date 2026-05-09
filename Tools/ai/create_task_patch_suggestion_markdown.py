#!/usr/bin/env python3
"""Create task Markdown with a valid patch_suggestion fenced JSON block."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Tools.ai.patch_suggestion_bundle.operations import is_safe_target
from Tools.validation.report_utils import resolve_output_path, write_json_report

TASK_PREFIX = "docs/LOCAL_AI_TASKS/"


def normalize_task_path(repo_root: Path, raw: str) -> tuple[str, str | None]:
    path = Path(raw)
    full = path if path.is_absolute() else repo_root / path
    try:
        rel = full.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return raw, "task file must stay inside the repository"
    if not rel.startswith(TASK_PREFIX) or not rel.endswith(".md"):
        return rel, "task file must be a Markdown file under docs/LOCAL_AI_TASKS/"
    return rel, None


def load_content(args: argparse.Namespace) -> str:
    if args.content_file:
        return Path(args.content_file).read_text(encoding="utf-8-sig")
    return args.content


def build_payload(args: argparse.Namespace, target_path: str, content: str) -> dict[str, Any]:
    return {
        "schema_version": 1,
        "kind": "task_patch_suggestion",
        "suggestions": [
            {
                "id": args.suggestion_id,
                "title": args.suggestion_title,
                "risk": args.risk,
                "operation": args.operation,
                "path": target_path,
                "marker": args.marker,
                "content": content,
            }
        ],
    }


def render_markdown(args: argparse.Namespace, payload: dict[str, Any]) -> str:
    return "\n".join(
        [
            f"# {args.title}",
            "",
            args.goal,
            "",
            "Operator gate:",
            args.operator_gate,
            "",
            "```patch_suggestion",
            json.dumps(payload, indent=2, ensure_ascii=False),
            "```",
            "",
        ]
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--goal", required=True)
    parser.add_argument("--operator-gate", default="Continue only after explicit operator confirmation.")
    parser.add_argument("--suggestion-id", required=True)
    parser.add_argument("--suggestion-title", required=True)
    parser.add_argument("--risk", default="low")
    parser.add_argument(
        "--operation",
        default="append_once",
        choices=["append_once", "insert_after_once", "insert_before_once", "replace_once", "write_file"],
    )
    parser.add_argument("--target-path", required=True)
    parser.add_argument("--marker", default="")
    parser.add_argument("--content", default="")
    parser.add_argument("--content-file", default="")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    task_rel, task_error = normalize_task_path(repo_root, args.task_file)
    if task_error:
        errors.append(task_error)
    target_rel = args.target_path.replace("\\", "/").lstrip("/")
    safe, safe_error = is_safe_target(target_rel)
    if not safe:
        errors.append(f"unsafe target path: {safe_error}")
    content = load_content(args)
    if not content and args.operation != "write_file":
        errors.append("--content or --content-file is required")
    args.marker = args.marker or content

    report = {
        "schema_version": 1,
        "kind": "task_patch_suggestion_markdown_create",
        "repo_root": repo_root.as_posix(),
        "task_file": task_rel,
        "target_path": target_rel,
        "operation": args.operation,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "task_markdown_written": False,
        "errors": errors,
        "warnings": warnings,
        "passed": False,
    }
    if not errors:
        payload = build_payload(args, target_rel, content)
        task_path = repo_root / task_rel
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(render_markdown(args, payload), encoding="utf-8")
        report["task_markdown_written"] = True
        report["source_writes_performed"] = True
        report["passed"] = True
        report["suggestion_count"] = 1

    if args.output:
        output = resolve_output_path(repo_root, args.output)
        print(write_json_report(report, output), end="")
    else:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
