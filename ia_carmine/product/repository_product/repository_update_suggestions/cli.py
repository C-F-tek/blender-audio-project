"""CLI entrypoint for repository update suggestion packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import DEFAULT_MAX_CHARS, DEFAULT_OUTPUT_DIR, DEFAULT_PACKET_BASENAME, PROFILE_CONTEXT_FILES
from .context import collect_context
from .markdown import render_markdown
from .provider import maybe_run_ollama
from .suggestions import build_ollama_prompt, deterministic_suggestions

def build_output_paths(repo_root: Path, output_dir: str, basename: str) -> tuple[Path, Path, Path]:
    directory = repo_root / output_dir
    return (
        directory / f"{basename}.json",
        directory / f"{basename}.md",
        directory / f"{basename}_manifest.json",
    )

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--profile", default="core", choices=sorted(PROFILE_CONTEXT_FILES.keys()))
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_PACKET_BASENAME)
    parser.add_argument(
        "--context-file",
        action="append",
        default=[],
        help="Additional context file to include. Repeatable.",
    )
    parser.add_argument(
        "--report-file",
        action="append",
        default=[],
        help="Additional validation/report JSON file to include. Repeatable.",
    )
    parser.add_argument(
        "--extra-context",
        action="append",
        default=[],
        help="Alias for --context-file. Repeatable.",
    )
    parser.add_argument(
        "--extra-report",
        action="append",
        default=[],
        help="Alias for --report-file. Repeatable.",
    )
    parser.add_argument("--max-context-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument(
        "--use-ollama",
        action="store_true",
        help="Use local Ollama for advisory drafting.",
    )
    parser.add_argument("--model", help="Optional Ollama model name.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    context = collect_context(
        repo_root,
        profile=args.profile,
        context_files=args.context_file,
        report_files=args.report_file,
        extra_context=args.extra_context,
        extra_reports=args.extra_report,
        max_chars=args.max_context_chars,
    )
    suggestions = deterministic_suggestions(context)
    ollama = {"used": False, "model": args.model, "text": "", "error": ""}

    if args.use_ollama:
        try:
            ollama = maybe_run_ollama(
                repo_root, build_ollama_prompt(context, suggestions), model=args.model
            )
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            ollama = {
                "used": False,
                "model": args.model,
                "text": "",
                "error": f"{type(exc).__name__}: {exc}",
            }

    output_json, output_md, output_manifest = build_output_paths(
        repo_root, args.output_dir, args.basename
    )
    packet_manifest = {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet_manifest",
        "path": str(output_manifest),
        "outputs": {
            "json": str(output_json),
            "markdown": str(output_md),
        },
        "profile": args.profile,
        "input_count": len(context["context_files"]) + len(context["report_files"]),
        "requested_context_files": context["requested_context_files"],
        "context_files": context["context_files"],
        "excluded_context_files": context["excluded_context_files"],
        "advisory_context_routing": context["advisory_context_routing"],
        "report_files": context["report_files"],
    }

    report = {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet",
        "generated_at": context["generated_at"],
        "repo_root": str(repo_root),
        "profile": args.profile,
        "passed": True,
        "errors": [],
        "warnings": [ollama["error"]] if ollama.get("error") else [],
        "packet_manifest": packet_manifest,
        "context": context,
        "suggestions": suggestions,
        "ollama": ollama,
    }

    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_manifest.write_text(
        json.dumps(packet_manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "passed": True,
                "json": str(output_json),
                "markdown": str(output_md),
                "manifest": str(output_manifest),
                "ollama_used": ollama["used"],
            },
            indent=2,
        )
    )
    return 0
