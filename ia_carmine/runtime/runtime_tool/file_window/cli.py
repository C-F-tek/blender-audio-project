"""Read a bounded window from a file-backed runtime artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from ia_carmine._shared.file_backed_transport import (
    MAX_FILE_WINDOW_CHARS,
    artifact_ref,
    is_allowed_runtime_artifact_path,
    read_text_window_bytes,
    resolve_path,
)


def render_markdown(report: dict[str, object]) -> str:
    return "\n".join(
        [
            "# Runtime Artifact File Window",
            "",
            f"- Passed: `{report.get('passed')}`",
            f"- Path: `{report.get('path')}`",
            f"- Offset: `{report.get('offset')}`",
            f"- Limit: `{report.get('limit')}`",
            f"- Next offset: `{report.get('next_offset')}`",
            f"- EOF: `{report.get('eof')}`",
            "",
            "## Errors",
            "",
            *[f"- {item}" for item in report.get("errors", [])],
        ]
    ).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--path", required=True)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--limit", type=int, default=16000)
    parser.add_argument("--output", default="output/validation/runtime_file_window.json")
    parser.add_argument("--markdown-output", default="output/validation/runtime_file_window.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    target = resolve_path(repo_root, args.path)
    errors: list[str] = []
    text = ""
    offset = max(0, int(args.offset))
    limit = int(args.limit)
    next_offset = offset
    eof = True
    path_allowed = is_allowed_runtime_artifact_path(repo_root, args.path)
    if not path_allowed:
        errors.append("runtime_file_window_path_outside_repo_root")
    elif limit <= 0:
        errors.append("runtime_file_window_limit_must_be_positive")
    elif limit > MAX_FILE_WINDOW_CHARS:
        errors.append(f"runtime_file_window_limit_exceeds_max:{MAX_FILE_WINDOW_CHARS}")
    elif not target.is_file():
        errors.append(f"file not found: {args.path}")
    else:
        text, next_offset, eof = read_text_window_bytes(target, offset=offset, limit=limit)
    ref = (
        artifact_ref(target, repo_root, kind="runtime_file_window_source", required=True)
        if path_allowed
        else {
            "ref_id": "rejected_runtime_file_window_source",
            "path": str(args.path),
            "kind": "runtime_file_window_source",
            "required": True,
            "producer": "runtime_file_window",
            "source": "rejected_outside_repo_root",
            "content_type": "",
            "exists": False,
            "bytes": 0,
            "sha256": "",
        }
    )
    report = {
        "schema_version": 1,
        "kind": "runtime_file_window",
        "repo_root": str(repo_root),
        "passed": not errors,
        "path": ref.get("path"),
        "source_ref": ref,
        "offset": offset,
        "offset_units": "bytes",
        "limit": limit,
        "max_limit": MAX_FILE_WINDOW_CHARS,
        "next_offset": next_offset,
        "eof": eof,
        "text": text,
        "text_chars": len(text),
        "errors": errors,
        "warnings": [],
        "source_writes_performed": False,
        "patch_application_performed": False,
        "provider_execution_performed": False,
        "git_write_performed": False,
    }
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
