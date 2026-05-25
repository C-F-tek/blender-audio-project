#!/usr/bin/env python3
"""Optional smoke for Ollama /api/embed with bge-m3 batch input."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.agent_context.rag_context.embedding import embed_batch, validate_vector


def render_markdown(report: dict) -> str:
    lines = [
        "# RAG Ollama Embed Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Endpoint: `{report.get('endpoint')}`",
        f"- Model: `{report.get('model')}`",
        f"- RAG profile: `{report.get('rag_profile')}`",
        f"- Probe performed: `{report.get('probe_performed')}`",
        f"- Embedding count: `{report.get('embedding_count')}`",
    ]
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--endpoint", default="")
    parser.add_argument("--model", default="")
    parser.add_argument("--rag-profile", default="")
    parser.add_argument("--batch-size", type=int, default=0)
    parser.add_argument("--require-ollama", action=argparse.BooleanOptionalAction, default=None)
    parser.add_argument("--allow-missing-ollama", action="store_true")
    parser.add_argument("--output", default="output/validation/rag_ollama_embed_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/rag_ollama_embed_smoke.md")
    args = parser.parse_args()
    missing = []
    if not str(args.endpoint or "").strip():
        missing.append("--endpoint")
    if not str(args.model or "").strip():
        missing.append("--model")
    if not str(args.rag_profile or "").strip():
        missing.append("--rag-profile")
    if int(args.batch_size or 0) <= 0:
        missing.append("--batch-size")
    if args.require_ollama is None:
        missing.append("--require-ollama/--no-require-ollama")
    if missing:
        parser.error("missing explicit RAG Ollama embed smoke parameter(s): " + ", ".join(missing))
    repo_root = Path(args.repo_root).resolve()
    inputs = [f"rag smoke input {index}" for index in range(max(1, int(args.batch_size)))]
    vectors, errors = embed_batch(
        endpoint=args.endpoint,
        model=args.model,
        texts=inputs,
        timeout_seconds=20,
        retries=0,
    )
    warnings: list[str] = []
    hard_errors: list[str] = []
    require_ollama = bool(args.require_ollama and not args.allow_missing_ollama)
    provider_execution_attempted = True
    if errors and require_ollama:
        hard_errors.extend(errors)
    elif errors:
        warnings.extend(f"optional Ollama probe skipped/unavailable: {item}" for item in errors)
    dimensions = []
    for vector in vectors:
        values, _norm, error = validate_vector(vector)
        if error:
            hard_errors.append(error)
        else:
            dimensions.append(len(values))
    report = {
        "schema_version": 1,
        "kind": "rag_ollama_embed_smoke",
        "passed": not hard_errors,
        "errors": hard_errors,
        "warnings": warnings,
        "endpoint": args.endpoint,
        "model": args.model,
        "rag_profile": args.rag_profile,
        "batch_size": args.batch_size,
        "require_ollama": require_ollama,
        "probe_performed": provider_execution_attempted,
        "embedding_count": len(vectors),
        "dimensions": sorted(set(dimensions)),
        "provider_execution_performed": provider_execution_attempted,
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
