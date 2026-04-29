"""Preflight checks for the AI artifact pipeline."""
from __future__ import annotations

import os
import platform
import sys
from pathlib import Path
from typing import Any

from .artifact_contracts import file_meta, planned_outputs, rel


def read_text_if_exists(path: Path, limit: int = 6000) -> str | None:
    """Read a bounded text preview from a file when it exists."""
    if not path.exists():
        return None
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def python_runtime() -> dict[str, Any]:
    """Return compact Python runtime information."""
    return {
        "executable": sys.executable,
        "version": sys.version.split()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
    }


def workstation_context(repo: Path) -> dict[str, Any]:
    """Return local workstation context summary when documented."""
    doc = repo / "docs" / "LOCAL_WORKSTATION_TARGET.md"
    text = read_text_if_exists(doc)
    return {"source": rel(doc, repo), "available": text is not None, "summary": text[:1200] if text else None}


def preflight(repo: Path, out: Path, args: Any) -> dict[str, Any]:
    """Run non-invasive preflight checks for a pipeline invocation."""
    warnings: list[str] = []
    errors: list[str] = []
    analysis = Path(args.analysis_json).resolve() if args.analysis_json else None

    if args.build_music_summary and not analysis:
        errors.append("--build-music-summary requires --analysis-json")
    if analysis and not analysis.exists():
        errors.append(f"Analysis JSON not found: {analysis}")
    if args.npu_workers > 4:
        warnings.append("npu_workers is greater than 4; local workstation policy recommends 4 or fewer.")
    if args.npu_guardrail and not args.smart_context:
        warnings.append("NPU guardrail works best with smart context; falling back to artifact directory review.")
    if args.guardrail_auto_remediate and not args.npu_guardrail:
        warnings.append("Guardrail auto-remediation was requested but npu_guardrail is disabled.")
    if args.review_wave_entrypoints and not (repo / "analyze_wav.py").exists():
        warnings.append("Wave entrypoint review enabled but analyze_wav.py was not found at repository root.")
    if args.gpu_command and "{brief}" not in args.gpu_command:
        warnings.append("GPU command does not include {brief}; planner may not receive ai_scene_brief.json.")
    if args.gpu_command and "{output}" not in args.gpu_command:
        warnings.append("GPU command does not include {output}; planner output may not be captured consistently.")

    blender_doc = repo / "docs" / "LOCAL_WORKSTATION_TARGET.md"
    if blender_doc.exists() and "blender command is not currently available in PATH" in blender_doc.read_text(encoding="utf-8", errors="replace"):
        warnings.append("Local workstation profile says blender is not in PATH; use full Blender executable path for CLI tests.")

    input_files = []
    if analysis:
        input_files.append(file_meta(analysis, repo))
    for item in [
        "analyze_wav.py",
        "build_track_summary.py",
        "docs/LOCAL_WORKSTATION_TARGET.md",
        "indexAI/task_capsules/blender_51_compat.json",
        "indexAI/task_capsules/resource_budget.json",
    ]:
        input_files.append(file_meta(repo / item, repo))

    return {
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "input_files": input_files,
        "planned_outputs": planned_outputs(repo, out, args),
        "python_runtime": python_runtime(),
        "workstation_context": workstation_context(repo),
        "environment": {"cwd": os.getcwd(), "dry_run": args.dry_run},
    }
