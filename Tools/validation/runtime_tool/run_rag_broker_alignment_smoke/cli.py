#!/usr/bin/env python3
"""Validate RAG runtime broker allowlist and command builder wiring."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.runtime.runtime_tool.broker.context_builders import build_rag_context_pack_tool
from ia_carmine.runtime.runtime_tool.broker.registry import TOOL_SPECS


REQUIRED_ARGS = {
    "query",
    "task_file",
    "db",
    "top_k",
    "char_budget",
    "embedding_endpoint",
    "embedding_model",
    "skip_query_embedding",
}


def render_markdown(report: dict) -> str:
    lines = [
        "# RAG Broker Alignment Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Tool registered: `{report.get('tool_registered')}`",
        f"- Command contains rag_build_context_pack: `{report.get('command_contains_cli')}`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/rag_broker_alignment_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/rag_broker_alignment_smoke.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    spec = TOOL_SPECS.get("rag_context_pack")
    if spec is None:
        errors.append("rag_context_pack ToolSpec missing")
        allowed = set()
    else:
        allowed = set(spec.allowed_args)
    missing = sorted(REQUIRED_ARGS - allowed)
    if missing:
        errors.append(f"missing allowed args: {missing}")
    command, outputs = build_rag_context_pack_tool(
        repo_root,
        repo_root / "output" / "validation" / "rag_broker_alignment",
        "smoke-rag",
        {
            "query": "generic_write evidence",
            "top_k": 3,
            "char_budget": 2000,
            "skip_query_embedding": True,
        },
    )
    command_contains = "rag_build_context_pack" in command
    if not command_contains:
        errors.append("builder command does not call rag_build_context_pack")
    if sorted(outputs) != ["json_report", "markdown_report"]:
        errors.append(f"unexpected output keys: {sorted(outputs)}")
    report = {
        "schema_version": 1,
        "kind": "rag_broker_alignment_smoke",
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "tool_registered": spec is not None,
        "allowed_args": sorted(allowed),
        "command": command,
        "command_contains_cli": command_contains,
        "outputs": outputs,
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

