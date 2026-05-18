"""Revision context selection for heap runtime launcher commands."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .common import REQUIRED_COMPOSER_JSON, read_optional_json

def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )

def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any]]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}
    candidates = sorted(
        [
            path / "external_heap_revision_context.json"
            for path in validation_dir.iterdir()
            if is_complete_heap_run_dir(path)
            and (path / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}
    path = candidates[0].resolve()
    return path, read_optional_json(path)

def revision_context_from_profile(
    repo_root: Path, profile: dict[str, Any], explicit_path: str
) -> tuple[Path | None, dict[str, Any]]:
    mode = str(profile.get("revision_context_mode") or "off")
    if mode == "off":
        return None, {}
    if explicit_path.strip():
        path = Path(explicit_path)
        if not path.is_absolute():
            path = repo_root / path
        path = path.resolve()
        return path, read_optional_json(path)
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    return None, {}

def revision_context_prompt(payload: dict[str, Any], path: Path | None, max_tasks: int) -> str:
    if not payload:
        return ""
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    limit = max(0, max_tasks)
    selected = tasks[:limit]
    candidate_summary = (
        payload.get("candidate_applicability_summary")
        if isinstance(payload.get("candidate_applicability_summary"), dict)
        else {}
    )
    lines = [
        "",
        "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN:",
        f"- path: {path if path else ''}",
        f"- protocol: {payload.get('protocol')}",
        f"- product_acceptance_status: {payload.get('product_acceptance_status')}",
        f"- product_acceptance_passed: {payload.get('product_acceptance_passed')}",
        f"- requires_concrete_rewrite: {payload.get('requires_concrete_rewrite')}",
        f"- priority_next_action: {payload.get('priority_next_action')}",
        f"- candidate_applicability_summary: {json.dumps(candidate_summary, ensure_ascii=False)}",
        f"- resume_from_block_id: {payload.get('resume_from_block_id')}",
        f"- latest_block_id: {payload.get('latest_block_id')}",
        f"- task_count: {len(tasks)}",
        "- GPU1 must consume rewrite/propagation tasks before emitting new proposal blocks.",
        "- If requires_concrete_rewrite=true, GPU1 must first rewrite non-concrete candidates with real repo paths and concrete operations.",
        "- GPU1 must not propagate symbols from candidates marked non-concrete or from sketch/stub code.",
        "- GPU1 may move backward to propagate imports, variables, functions, classes and contracts, then resume forward.",
        "- GPU0 and NPU tasks are parallel recheck/audit work over old pointers.",
        "TASKS:",
    ]
    for idx, task in enumerate(selected, start=1):
        if not isinstance(task, dict):
            continue
        lines.append(
            f"{idx}. {task.get('task_id')} role={task.get('role')} type={task.get('task_type')} target={task.get('target_block_id')} resume={task.get('resume_from_block_id')}"
        )
        if task.get("candidate_applicability_flags"):
            lines.append(
                f"   candidate_applicability_flags={json.dumps(task.get('candidate_applicability_flags'), ensure_ascii=False)}"
            )
        if task.get("symbol_propagation_skipped"):
            lines.append(
                f"   symbol_propagation_skipped={task.get('symbol_propagation_skipped')} reason={task.get('symbol_propagation_skip_reason')}"
            )
        if task.get("discovered_symbols"):
            lines.append(
                f"   discovered_symbols={json.dumps(task.get('discovered_symbols'), ensure_ascii=False)}"
            )
        if task.get("rejection_reasons"):
            lines.append(
                f"   rejection_reasons={json.dumps(task.get('rejection_reasons'), ensure_ascii=False)}"
            )
        if task.get("instruction"):
            lines.append(f"   instruction={task.get('instruction')}")
    if len(tasks) > len(selected):
        lines.append(
            f"- omitted_tasks={len(tasks) - len(selected)}; read full revision context artifact for remaining tasks."
        )
    return "\n".join(lines)
