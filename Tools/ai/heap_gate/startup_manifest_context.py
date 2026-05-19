"""Startup manifest helpers for heap gate context ingestion."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from Tools.ai._shared.universo_utils import read_json, repo_rel


ARTIFACT_PRIORITY = (
    "tool_catalog_json",
    "shared_memory_json",
    "operational_memory_status_json",
    "operational_memory_write_json",
    "operational_memory_search_json",
    "shared_context_json",
    "semantic_code_chunks_json",
    "semantic_evidence_chunks_json",
    "ai_context_pack_json",
    "repo_docs_map_json",
    "required_context_files_json",
    "code_execution_matrix_json",
    "runtime_debug_lab_json",
    "heap_task_file",
)


def _resolve_path(repo_root: Path, raw: str) -> Path | None:
    value = str(raw or "").strip()
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def resolve_startup_task_file_path(repo_root: Path, args: Any) -> Path | None:
    return _resolve_path(repo_root, str(getattr(args, "task_file", "") or ""))


def resolve_startup_manifest_path(repo_root: Path, args: Any) -> Path | None:
    explicit = _resolve_path(repo_root, str(getattr(args, "startup_manifest", "") or ""))
    if explicit is not None:
        return explicit
    task_file = resolve_startup_task_file_path(repo_root, args)
    if task_file is None:
        return None
    return task_file.parent / "heap_context_memory_reload_manifest.json"


def load_startup_manifest(repo_root: Path, args: Any) -> tuple[Path | None, dict[str, Any]]:
    manifest_path = resolve_startup_manifest_path(repo_root, args)
    if manifest_path is None:
        return None, {}
    return manifest_path, read_json(manifest_path)


def _json_digest(payload: dict[str, Any]) -> tuple[str, int]:
    text = json.dumps(payload, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(), len(text)


def _compact_artifacts(artifacts: dict[str, Any], limit: int) -> dict[str, str]:
    selected: dict[str, str] = {}
    for key in ARTIFACT_PRIORITY:
        value = str(artifacts.get(key) or "").strip()
        if value:
            selected[key] = value.replace("\\", "/")
        if len(selected) >= limit:
            return selected
    for key in sorted(artifacts):
        if key in selected:
            continue
        value = str(artifacts.get(key) or "").strip()
        if value:
            selected[key] = value.replace("\\", "/")
        if len(selected) >= limit:
            break
    return selected


def compact_manifest_context(
    repo_root: Path,
    args: Any,
    *,
    artifact_limit: int = 32,
    execution_limit: int = 24,
    context_file_limit: int = 80,
) -> dict[str, Any]:
    manifest_path, manifest = load_startup_manifest(repo_root, args)
    if not manifest_path:
        return {"loaded": False, "reason": "startup manifest argument missing"}
    rel_manifest = repo_rel(repo_root, manifest_path)
    if not manifest:
        return {
            "loaded": False,
            "startup_manifest": rel_manifest,
            "reason": "startup manifest missing or unreadable",
        }
    artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
    context_files = [str(item).replace("\\", "/") for item in manifest.get("context_files") or []]
    executions = [item for item in manifest.get("tool_executions") or [] if isinstance(item, dict)]
    digest, json_chars = _json_digest(manifest)
    task_ref = str(manifest.get("heap_task_file") or artifacts.get("heap_task_file") or "")
    task_path = (repo_root / task_ref).resolve(strict=False) if task_ref else None
    task_size = task_path.stat().st_size if task_path and task_path.is_file() else 0
    return {
        "loaded": True,
        "source": "startup_manifest",
        "startup_manifest": rel_manifest,
        "startup_manifest_sha256": digest,
        "manifest_json_chars": json_chars,
        "task_file": task_ref.replace("\\", "/"),
        "task_file_mode": "artifact_reference_only_not_ingested",
        "task_file_size_bytes": task_size,
        "request_chars": manifest.get("request_chars", 0),
        "request_sha256": manifest.get("request_sha256", ""),
        "request_preview": str(manifest.get("request_preview") or "")[:1200],
        "passed": manifest.get("passed"),
        "input_ready_before_heap": manifest.get("input_ready_before_heap"),
        "startup_reload_degraded": manifest.get("startup_reload_degraded"),
        "blocking_requirements": manifest.get("blocking_requirements") or [],
        "degraded_requirements": manifest.get("degraded_requirements") or [],
        "context_file_count": manifest.get("context_file_count", len(context_files)),
        "context_files_sample": context_files[: max(0, int(context_file_limit))],
        "artifacts": _compact_artifacts(artifacts, max(1, int(artifact_limit))),
        "tool_executions": executions[: max(0, int(execution_limit))],
        "contract": manifest.get("contract") if isinstance(manifest.get("contract"), dict) else {},
    }


def compact_task_file_context(
    repo_root: Path,
    args: Any,
    *,
    max_preview_chars: int = 12000,
) -> dict[str, Any]:
    task_path = resolve_startup_task_file_path(repo_root, args)
    if task_path is None:
        return {
            "loaded": False,
            "task_file": "",
            "reason": "task file argument missing and startup manifest unavailable",
        }
    rel_path = repo_rel(repo_root, task_path)
    if not task_path.is_file():
        return {"loaded": False, "task_file": rel_path, "reason": "task file missing"}

    digest = hashlib.sha256()
    preview_bytes = bytearray()
    preview_limit = max(0, int(max_preview_chars)) * 4
    total_bytes = 0
    try:
        with task_path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                total_bytes += len(chunk)
                digest.update(chunk)
                if len(preview_bytes) < preview_limit:
                    preview_bytes.extend(chunk[: max(0, preview_limit - len(preview_bytes))])
    except Exception as exc:  # noqa: BLE001 - context ingestion must report, not crash.
        return {
            "loaded": False,
            "task_file": rel_path,
            "reason": f"task file unreadable: {type(exc).__name__}: {exc}",
        }

    preview = preview_bytes.decode("utf-8-sig", errors="replace")[: max(0, int(max_preview_chars))]
    return {
        "loaded": True,
        "source": "legacy_startup_task_file",
        "task_file": rel_path,
        "sha256": digest.hexdigest(),
        "char_count": len(preview),
        "size_bytes": total_bytes,
        "preview": preview,
        "preview_truncated": total_bytes > len(preview_bytes),
    }
