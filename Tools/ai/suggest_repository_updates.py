#!/usr/bin/env python3
"""Build an advisory post-validation AI work packet.

The packet is intentionally app-agnostic and non-destructive:

- no source files are modified;
- no patches are applied;
- no provider/model call is made unless `--use-ollama` is explicitly passed;
- inputs and outputs are configurable;
- defaults are only a convenient profile for this repository.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/ai_pipeline"
DEFAULT_PACKET_BASENAME = "repository_update_suggestions"
DEFAULT_MAX_CHARS = 6000
IGNORED_PLAN_FILENAMES = {"README.md"}

PROFILE_CONTEXT_FILES: dict[str, tuple[str, ...]] = {
    "core": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/TECH_DEBT_TRACKER.md",
        "docs/REFACTORING_AND_REUSE_PLAN.md",
        "docs/JSON_SCHEMAS.md",
        "docs/AI_ARTIFACT_SCHEMAS.md",
        "Tools/npu/pipeline/README.md",
        "Tools/validation/README.md",
    ),
    "npu": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/TECH_DEBT_TRACKER.md",
        "docs/REFACTORING_AND_REUSE_PLAN.md",
        "docs/DATA_FLOW.md",
        "docs/JSON_SCHEMAS.md",
        "Tools/npu/pipeline/README.md",
        "Tools/validation/README.md",
        "Tools/npu/run_dual_ai_pipeline.py",
        "Tools/npu/build_runtime_output_manifest.py",
        "Tools/npu/build_provider_result_report.py",
        "Tools/ai/run_local_provider_probe.py",
        "Tools/validation/check_ai_workload_report_quality.py",
    ),
    "docs": (
        "AGENTS.md",
        "WORKFLOW.md",
        "docs/README.md",
        "docs/AI_DOCS_ENTRYPOINT.md",
        "docs/PROJECT_STATUS_POINT.md",
        "docs/GITHUB_ONLY_AI_CONTINUATION_GUIDE.md",
        "docs/GITHUB_LOCAL_VALIDATION_WORKFLOW.md",
        "docs/TECH_DEBT_TRACKER.md",
    ),
}

PROFILE_REPORTS: dict[str, tuple[str, ...]] = {
    "core": (
        "output/validation/python_syntax.json",
        "output/validation/ai_pipeline_modules.json",
        "output/validation/npu_pipeline_modules.json",
        "output/validation/npu_pipeline_helper_tests.json",
        "output/validation/npu_pipeline_docs.json",
        "output/validation/provider_result_parsing.json",
        "output/validation/provider_result_report.json",
        "output/validation/ai_workload_report_quality.json",
        "output/validation/npu_runtime_output_manifest.json",
        "output/validation/local_ai_resource_lanes.json",
        "output/validation/local_provider_probe.json",
        "output/validation/execution_plan_status.json",
        "output/validation/validation_report_contract.json",
        "output/validation/docs_links.json",
    ),
    "npu": (
        "output/validation/python_syntax.json",
        "output/validation/npu_pipeline_modules.json",
        "output/validation/npu_pipeline_helper_tests.json",
        "output/validation/npu_pipeline_docs.json",
        "output/validation/provider_result_parsing.json",
        "output/validation/provider_result_report.json",
        "output/validation/ai_workload_report_quality.json",
        "output/validation/npu_runtime_output_manifest.json",
        "output/validation/local_ai_resource_lanes.json",
        "output/validation/local_provider_probe.json",
        "output/validation/execution_plan_status.json",
        "output/validation/validation_report_contract.json",
    ),
    "docs": (
        "output/validation/docs_links.json",
        "output/validation/execution_plan_status.json",
        "output/validation/json_artifacts.json",
        "output/validation/validation_report_contract.json",
    ),
}


def split_path_values(items: list[str]) -> list[str]:
    """Accept repeated args and comma-separated PowerShell values."""

    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def unique_items(items: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for item in split_path_values(items):
        normalized = item.replace("\\", "/")
        if normalized in seen:
            continue
        seen.add(normalized)
        out.append(normalized)
    return out


def read_text_if_exists(path: Path, *, max_chars: int) -> dict[str, Any]:
    rel = str(path)
    if not path.exists():
        return {"path": rel, "exists": False, "text": "", "chars": 0, "truncated": False}
    text = path.read_text(encoding="utf-8", errors="replace")
    original_len = len(text)
    truncated = original_len > max_chars
    if truncated:
        text = text[:max_chars] + "\n...[truncated]"
    return {"path": rel, "exists": True, "text": text, "chars": original_len, "truncated": truncated}


def read_json_if_exists(path: Path) -> dict[str, Any]:
    rel = str(path)
    if not path.exists():
        return {"path": rel, "exists": False, "data": None, "error": "missing"}
    try:
        return {"path": rel, "exists": True, "data": json.loads(path.read_text(encoding="utf-8-sig")), "error": ""}
    except Exception as exc:  # noqa: BLE001 - report-only tool.
        return {"path": rel, "exists": True, "data": None, "error": f"{type(exc).__name__}: {exc}"}


def compact_report_summary(report: dict[str, Any]) -> dict[str, Any]:
    data = report.get("data")
    if not isinstance(data, dict):
        return {"path": report["path"], "exists": report["exists"], "passed": None, "error": report.get("error")}
    return {
        "path": report["path"],
        "exists": report["exists"],
        "kind": data.get("kind"),
        "schema_version": data.get("schema_version"),
        "passed": data.get("passed"),
        "errors": data.get("errors", [])[:10] if isinstance(data.get("errors"), list) else data.get("errors"),
        "warnings": data.get("warnings", [])[:10] if isinstance(data.get("warnings"), list) else data.get("warnings"),
        "checks_keys": sorted((data.get("checks") or {}).keys())[:30] if isinstance(data.get("checks"), dict) else [],
    }


def collect_context(
    repo_root: Path,
    *,
    profile: str,
    context_files: list[str],
    report_files: list[str],
    extra_context: list[str],
    extra_reports: list[str],
    max_chars: int,
) -> dict[str, Any]:
    all_context_files = unique_items(list(PROFILE_CONTEXT_FILES.get(profile, ())) + context_files + extra_context)
    all_report_files = unique_items(list(PROFILE_REPORTS.get(profile, ())) + report_files + extra_reports)

    docs = [read_text_if_exists(repo_root / rel, max_chars=max_chars) for rel in all_context_files]
    reports_raw = [read_json_if_exists(repo_root / rel) for rel in all_report_files]

    active_dir = repo_root / "docs" / "EXECUTION_PLANS" / "active"
    completed_dir = repo_root / "docs" / "EXECUTION_PLANS" / "completed"
    active_plans = [
        path
        for path in sorted(active_dir.glob("*.md"))
        if path.name not in IGNORED_PLAN_FILENAMES
    ] if active_dir.exists() else []
    completed_plans = [
        path
        for path in sorted(completed_dir.glob("*.md"))
        if path.name not in IGNORED_PLAN_FILENAMES
    ] if completed_dir.exists() else []

    return {
        "schema_version": 1,
        "kind": "post_validation_ai_work_packet_context",
        "profile": profile,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "context_files": all_context_files,
        "report_files": all_report_files,
        "docs": docs,
        "validation_reports": [compact_report_summary(report) for report in reports_raw],
        "execution_plans": {
            "active": [path.relative_to(repo_root).as_posix() for path in active_plans],
            "completed_tail": [path.relative_to(repo_root).as_posix() for path in completed_plans[-30:]],
        },
    }


def deterministic_suggestions(context: dict[str, Any]) -> list[dict[str, str]]:
    suggestions: list[dict[str, str]] = []
    reports = context.get("validation_reports", [])
    failed_reports = [r for r in reports if r.get("passed") is False]
    missing_reports = [r for r in reports if not r.get("exists")]
    active_plans = context.get("execution_plans", {}).get("active", [])

    if failed_reports:
        suggestions.append(
            {
                "priority": "P1",
                "area": "validation",
                "title": "Fix failing validation reports before new runtime work",
                "details": "; ".join(f"{r.get('path')}: {r.get('errors')}" for r in failed_reports[:5]),
            }
        )
    if missing_reports:
        suggestions.append(
            {
                "priority": "P2",
                "area": "validation",
                "title": "Run or review missing validation reports before strict follow-up work",
                "details": "; ".join(str(r.get("path")) for r in missing_reports[:8]),
            }
        )
    if active_plans:
        suggestions.append(
            {
                "priority": "P2",
                "area": "execution_plans",
                "title": "Review active execution plans before opening the next milestone",
                "details": "; ".join(active_plans[:10]),
            }
        )
    suggestions.append(
        {
            "priority": "P2",
            "area": "agnostic_core",
            "title": "Prefer additive observability before provider or Blender runtime changes",
            "details": "Safe next steps: report contract consistency, runtime-output manifest emission, provider-result parsing/reporting without changing provider execution.",
        }
    )
    return suggestions


def build_ollama_prompt(context: dict[str, Any], deterministic: list[dict[str, str]]) -> str:
    compact = {
        "profile": context.get("profile"),
        "repo_root": context.get("repo_root"),
        "validation_reports": context.get("validation_reports"),
        "execution_plans": context.get("execution_plans"),
        "deterministic_suggestions": deterministic,
    }
    return (
        "You are a local repository maintenance assistant for blender-audio-project.\n"
        "Return concise Markdown only. Do not propose Blender runtime, Ready To Jazz, "
        "provider execution, full analysis JSON edits, or generated index hand edits.\n"
        "Prioritize app-agnostic core/backend/AI/NPU/multistep/guardrail/memory.\n\n"
        "Context JSON:\n"
        + json.dumps(compact, indent=2, ensure_ascii=False)
        + "\n\nProduce: 1) next safe milestone, 2) files to inspect, 3) validation commands, 4) stop conditions."
    )


def maybe_run_ollama(repo_root: Path, prompt: str, *, model: str | None) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.npu.ollama_runtime import OllamaSession  # noqa: PLC0415

    with OllamaSession(model=model, shutdown_server=False, unload_model=True) as session:
        text = session.generate(prompt, max_new_tokens=1200, temperature=0.1)
    return {"used": True, "model": model, "text": text, "error": ""}


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Post-Validation AI Work Packet", ""]
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Repo: `{report['repo_root']}`")
    lines.append(f"- Profile: `{report['profile']}`")
    lines.append(f"- Ollama used: `{report['ollama']['used']}`")
    lines.append(f"- Packet manifest: `{report['packet_manifest']['path']}`")
    lines.append("")
    lines.append("## Deterministic suggestions")
    lines.append("")
    for item in report["suggestions"]:
        lines.append(f"### {item['priority']} — {item['title']}")
        lines.append("")
        lines.append(f"- Area: `{item['area']}`")
        lines.append(f"- Details: {item['details']}")
        lines.append("")
    if report["ollama"].get("text"):
        lines.append("## Local Ollama draft")
        lines.append("")
        lines.append(report["ollama"]["text"].strip())
        lines.append("")
    lines.append("## Inputs")
    lines.append("")
    lines.append("### Context files")
    for path in report["context"]["context_files"]:
        lines.append(f"- `{path}`")
    lines.append("")
    lines.append("### Report files")
    for path in report["context"]["report_files"]:
        lines.append(f"- `{path}`")
    lines.append("")
    lines.append("## Guardrails")
    lines.append("")
    lines.extend(
        [
            "- Advisory only: do not auto-apply edits from this packet.",
            "- Output/input paths are configurable; defaults are not part of the architecture boundary.",
            "- Validate locally before committing generated indexes.",
            "- Keep provider execution changes in a separate explicitly scoped milestone.",
        ]
    )
    return "\n".join(lines) + "\n"


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
    parser.add_argument("--context-file", action="append", default=[], help="Additional context file to include. Repeatable.")
    parser.add_argument("--report-file", action="append", default=[], help="Additional validation/report JSON file to include. Repeatable.")
    parser.add_argument("--extra-context", action="append", default=[], help="Alias for --context-file. Repeatable.")
    parser.add_argument("--extra-report", action="append", default=[], help="Alias for --report-file. Repeatable.")
    parser.add_argument("--max-context-chars", type=int, default=DEFAULT_MAX_CHARS)
    parser.add_argument("--use-ollama", action="store_true", help="Use local Ollama for advisory drafting.")
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
            ollama = maybe_run_ollama(repo_root, build_ollama_prompt(context, suggestions), model=args.model)
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            ollama = {"used": False, "model": args.model, "text": "", "error": f"{type(exc).__name__}: {exc}"}

    output_json, output_md, output_manifest = build_output_paths(repo_root, args.output_dir, args.basename)
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
        "context_files": context["context_files"],
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
    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    output_manifest.write_text(json.dumps(packet_manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"passed": True, "json": str(output_json), "markdown": str(output_md), "manifest": str(output_manifest), "ollama_used": ollama["used"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
