#!/usr/bin/env python3
"""Controlled report-only runtime debug lab for AI programming/debug tasks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ia_carmine._shared.file_backed_transport import INLINE_TEXT_MAX_CHARS
from .reporting import render_markdown, write_reports
from .runner import run_request


def load_request(path: Path) -> tuple[dict[str, object] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return None, f"request file not found: {path}"
    except json.JSONDecodeError as exc:
        return (
            None,
            f"invalid request JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}",
        )
    except OSError as exc:
        return None, f"unable to read request file: {type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "request JSON root must be an object"
    return data, None


def load_request_json(text: str) -> tuple[dict[str, object] | None, str | None]:
    if len(text) > INLINE_TEXT_MAX_CHARS:
        return None, "request_json_large_requires_request_file"
    try:
        data = json.loads(text)
    except json.JSONDecodeError as exc:
        return None, f"invalid request JSON at line {exc.lineno}, column {exc.colno}: {exc.msg}"
    if not isinstance(data, dict):
        return None, "request JSON root must be an object"
    return data, None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--request-json", default="")
    parser.add_argument("--output", default="output/validation/agent_runtime_debug_lab.json")
    parser.add_argument("--markdown-output", default="output/validation/agent_runtime_debug_lab.md")
    parser.add_argument("--timeout-seconds", type=int, default=300)
    parser.add_argument("--tail-chars", type=int, default=4000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    if args.request_json:
        request, load_error = load_request_json(args.request_json)
    elif args.request_file:
        request_path = Path(args.request_file)
        if not request_path.is_absolute():
            request_path = repo_root / request_path
        request, load_error = load_request(request_path)
    else:
        request, load_error = None, "--request-json or --request-file is required"
    if load_error:
        report = {
            "schema_version": 1,
            "kind": "agent_runtime_debug_lab",
            "repo_root": repo_root.as_posix(),
            "passed": False,
            "operation_count": 0,
            "failed_count": 1,
            "operations": [],
            "guardrails": {
                "free_shell_exposed": False,
                "allowlist_enforced": True,
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "git_write_performed": False,
                "blender_runtime_execution_performed": False,
                "ffmpeg_runtime_execution_performed": False,
            },
            "errors": [load_error],
            "warnings": [],
        }
    else:
        assert request is not None
        report = run_request(
            repo_root=repo_root,
            request=request,
            timeout_seconds=max(1, int(args.timeout_seconds)),
            tail_chars=max(256, int(args.tail_chars)),
        )

    write_reports(
        repo_root=repo_root,
        output=args.output,
        markdown_output=args.markdown_output,
        report=report,
        markdown=render_markdown(report),
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
