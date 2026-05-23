"""Fallback report writer for incomplete heap runtime runs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import repo_rel, write_json
from .requesting import startup_artifact_refs


def write_fallback_heap_report(
    *,
    repo_root: Path,
    stamp: str,
    run_dir: Path,
    report_file: Path,
    markdown_file: Path,
    request: str,
    startup_payload: dict[str, Any],
    startup_result: dict[str, Any],
    heap_result: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    context_refs = startup_artifact_refs(startup_payload)
    blocking = [reason]
    if startup_payload.get("startup_reload_degraded"):
        blocking.append("startup_reload_degraded=True")
    blocking.extend(_startup_rag_blockers(startup_payload))
    for item in (
        startup_payload.get("blocking_requirements", [])
        if isinstance(startup_payload.get("blocking_requirements"), list)
        else []
    ):
        blocking.append(f"startup blocking requirement: {item}")
    report = {
        "schema_version": 1,
        "kind": "heap_runtime_completeness_gate",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "request": request,
        "passed": False,
        "fallback_heap_report": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": blocking,
        "warnings": (
            startup_payload.get("startup_warnings", [])
            if isinstance(startup_payload.get("startup_warnings"), list)
            else []
        ),
        "metrics": {
            "stamp": stamp,
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "provider_revision_count": 0,
            "startup_reload_degraded": bool(startup_payload.get("startup_reload_degraded")),
        },
        "real_run_output_contract": {
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "runtime_debug_lab_required": True,
            "runtime_debug_lab_passed": False,
            "context_artifact_refs": context_refs,
            "startup_manifest": repo_rel(
                repo_root,
                run_dir
                / "startup_context_memory_reload"
                / "heap_context_memory_reload_manifest.json",
            ),
            "startup_task_file": repo_rel(
                repo_root,
                run_dir / "startup_context_memory_reload" / "heap_startup_input_ready_context.md",
            ),
            "startup_reload_degraded": bool(startup_payload.get("startup_reload_degraded")),
            "fallback_reason": reason,
        },
        "startup_context_memory_reload": startup_payload,
        "command_results": {"startup": startup_result, "heap": heap_result},
    }
    write_json(report_file, report)
    _write_fallback_markdown(markdown_file, report, context_refs, blocking, reason, startup_payload)
    return report


def _write_fallback_markdown(
    markdown_file: Path,
    report: dict[str, Any],
    context_refs: list[str],
    blocking: list[str],
    reason: str,
    startup_payload: dict[str, Any],
) -> None:
    lines = [
        "# Heap Runtime Fallback Report",
        "",
        f"- Product status: `{report['metrics']['product_status']}`",
        f"- Quality output passed: `{report['metrics']['quality_output_passed']}`",
        f"- Fallback reason: `{reason}`",
        f"- Startup reload degraded: `{startup_payload.get('startup_reload_degraded')}`",
        "",
        "## Context artifacts",
        "",
    ]
    lines.extend(f"- `{ref}`" for ref in context_refs)
    lines.extend(["", "## Blocking issues", ""])
    lines.extend(f"- {item}" for item in blocking)
    markdown_file.parent.mkdir(parents=True, exist_ok=True)
    markdown_file.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _startup_rag_blockers(startup_payload: dict[str, Any]) -> list[str]:
    blockers: list[str] = []
    if startup_payload.get("rag_index_ready") is not False:
        return blockers
    missing = startup_payload.get("rag_missing_embedding_count_after")
    action = startup_payload.get("rag_index_action") or ""
    ingest_failed = startup_payload.get("rag_repo_ingest_passed") is False
    if ingest_failed:
        detail = f"rag_repo_ingest failed: missing embeddings after ingest: {missing}"
        if action:
            detail += f" (action={action})"
        blockers.append(detail)
    else:
        blockers.append("rag index not ready before provider runtime")
    return blockers
