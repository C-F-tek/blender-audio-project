"""Manifest construction for heap startup reload."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai.heap_context_memory_reload.common import repo_rel, sha256_text


def requirement_status(
    commands: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[str], list[str], list[str]]:
    required = [item for item in commands if item.get("required")]
    optional = [item for item in commands if not item.get("required")]
    blocking = [str(item.get("requirement")) for item in required if not item.get("effective_passed")]
    degraded = [str(item.get("requirement")) for item in commands if item.get("degraded")]
    optional_failed = [
        str(item.get("requirement")) for item in optional if not item.get("effective_passed")
    ]
    return required, optional, blocking, degraded, optional_failed


def build_manifest(
    *,
    stamp: str,
    repo_root: Path,
    project_python: str,
    request_text: str,
    context_files: list[str],
    artifacts: dict[str, str],
    commands: list[dict[str, Any]],
    warnings: list[str],
    task_file: Path,
    context_pack_result: dict[str, Any],
    strict_ai_context_pack: bool,
    strict_startup_reload: bool,
) -> dict[str, Any]:
    required, optional, blocking, degraded, optional_failed = requirement_status(commands)
    startup_reload_degraded = bool(degraded or optional_failed)
    required_passed = not blocking
    optional_passed = all(bool(item.get("effective_passed")) for item in optional)
    input_ready_before_heap = required_passed and bool(context_files)
    strict_startup = bool(strict_startup_reload or strict_ai_context_pack)
    passed = bool(input_ready_before_heap and (not strict_startup or not startup_reload_degraded))
    return {
        "schema_version": 1,
        "kind": "heap_context_memory_reload_manifest",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "request_file": artifacts.get("startup_request_file", ""),
        "request_chars": len(request_text),
        "request_sha256": sha256_text(request_text),
        "request_preview": request_text[:4000],
        "passed": passed,
        "input_ready_before_heap": input_ready_before_heap,
        "load_context_into_heap": True,
        "startup_reload_degraded": startup_reload_degraded,
        "strict_startup_reload": strict_startup,
        "required_reload_passed": required_passed,
        "optional_reload_passed": optional_passed,
        "blocking_requirements": blocking,
        "degraded_requirements": degraded,
        "optional_failed_requirements": optional_failed,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "context_file_count": len(context_files),
        "context_files": context_files,
        "artifacts": artifacts,
        "tool_executions": commands,
        "startup_warnings": warnings,
        "required_requirements": [item["requirement"] for item in required],
        "optional_requirements": [item["requirement"] for item in optional],
        "heap_task_file": artifacts["heap_task_file"],
        "contract": {
            "input_ready_before_heap": input_ready_before_heap,
            "load_context_into_heap": True,
            "tool_catalog_loaded": bool(artifacts.get("tool_catalog_json")),
            "shared_memory_loaded": bool(artifacts.get("shared_memory_json")),
            "operational_memory_loaded": bool(artifacts.get("operational_memory_status_json")),
            "operational_memory_write_recorded": bool(
                artifacts.get("operational_memory_write_json")
            ),
            "repo_docs_loaded": bool(artifacts.get("repo_docs_map_json")),
            "semantic_code_chunks_loaded": bool(artifacts.get("semantic_code_chunks_json")),
            "ai_context_pack_loaded": bool(artifacts.get("ai_context_pack_json"))
            and context_pack_result.get("artifact_useful"),
            "semantic_evidence_chunks_loaded": bool(artifacts.get("semantic_evidence_chunks_json")),
            "heap_task_file_written": task_file.exists(),
            "advisory_context_pack_non_blocking": not bool(strict_ai_context_pack),
            "final_composer_required": True,
        },
    }


def build_print_payload(manifest: dict[str, Any], repo_root: Path, manifest_path: Path, manifest_md: Path) -> dict[str, Any]:
    return {
        "schema_version": manifest["schema_version"],
        "kind": manifest["kind"],
        "stamp": manifest["stamp"],
        "passed": manifest["passed"],
        "input_ready_before_heap": manifest["input_ready_before_heap"],
        "startup_reload_degraded": manifest["startup_reload_degraded"],
        "required_reload_passed": manifest["required_reload_passed"],
        "optional_reload_passed": manifest["optional_reload_passed"],
        "request_file": manifest.get("request_file", ""),
        "request_chars": manifest.get("request_chars", 0),
        "request_sha256": manifest.get("request_sha256", ""),
        "context_file_count": manifest.get("context_file_count", 0),
        "artifact_count": len(manifest.get("artifacts", {})),
        "tool_execution_count": len(manifest.get("tool_executions", [])),
        "blocking_requirements": manifest.get("blocking_requirements", []),
        "degraded_requirements": manifest.get("degraded_requirements", []),
        "optional_failed_requirements": manifest.get("optional_failed_requirements", []),
        "manifest": repo_rel(repo_root, manifest_path),
        "markdown": repo_rel(repo_root, manifest_md),
        "heap_task_file": manifest.get("heap_task_file", ""),
    }
