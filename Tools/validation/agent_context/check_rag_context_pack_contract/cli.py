#!/usr/bin/env python3
"""Validate RAG context-pack report shape and guardrails."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import read_json_report, resolve_output_path, write_json_report

ALLOWED_KINDS = {"rag_context_pack", "rag_query_context", "startup_unified_context_pack"}
REQUIRED_FLAGS = (
    "provider_execution_performed",
    "patch_application_performed",
    "source_writes_performed",
)


def validate_pack(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != 1:
        errors.append("schema_version must be 1")
    if data.get("kind") not in ALLOWED_KINDS:
        errors.append(f"kind must be one of {sorted(ALLOWED_KINDS)}")
    for flag in REQUIRED_FLAGS:
        if data.get(flag) is not False:
            errors.append(f"{flag} must be false")
    chunks = data.get("chunks")
    if chunks is None and isinstance(data.get("rag_context_pack"), dict):
        chunks = data["rag_context_pack"].get("chunks")
    if chunks is None:
        errors.append("chunks field is required")
        return errors
    if not isinstance(chunks, list):
        errors.append("chunks must be a list")
        return errors
    for index, chunk in enumerate(chunks):
        if not isinstance(chunk, dict):
            errors.append(f"chunks[{index}] must be an object")
            continue
        source = str(chunk.get("source_path") or "")
        if not source:
            errors.append(f"chunks[{index}] source_path is required")
        if Path(source).is_absolute():
            errors.append(f"chunks[{index}] source_path must be repo-relative")
        if "output/" in source.replace("\\", "/"):
            errors.append(f"chunks[{index}] must not point at output artifacts")
        if not chunk.get("chunk_id"):
            errors.append(f"chunks[{index}] chunk_id is required")
        if not chunk.get("text_hash"):
            errors.append(f"chunks[{index}] text_hash is required")
        start = chunk.get("char_start")
        end = chunk.get("char_end")
        if not isinstance(start, int) or start < 0:
            errors.append(f"chunks[{index}] char_start must be a non-negative integer")
        if not isinstance(end, int) or end < 0:
            errors.append(f"chunks[{index}] char_end must be a non-negative integer")
        if isinstance(start, int) and isinstance(end, int) and end < start:
            errors.append(f"chunks[{index}] char_end must be >= char_start")
    return errors


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# RAG Context Pack Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Pack: `{report.get('pack')}`",
        "",
        "## Errors",
        "",
    ]
    lines.extend(f"- {item}" for item in report.get("errors") or ["none"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--pack", required=True)
    parser.add_argument("--output", default="output/validation/rag_context_pack_contract.json")
    parser.add_argument("--markdown-output", default="output/validation/rag_context_pack_contract.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    pack_path = resolve_output_path(repo_root, args.pack)
    data = read_json_report(pack_path)
    errors = validate_pack(data)
    report = {
        "schema_version": 1,
        "kind": "rag_context_pack_contract",
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "pack": str(pack_path),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
