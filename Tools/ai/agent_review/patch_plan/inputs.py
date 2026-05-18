"""Input report helpers for agent review patch plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import load_json_object, repo_rel, resolve_path

def load_gpu_report(
    repo_root: Path, orchestrator: dict[str, Any], warnings: list[str]
) -> dict[str, Any]:
    gpu_output = orchestrator.get("gpu_output")
    if not gpu_output:
        return {}
    path = resolve_path(repo_root, str(gpu_output))
    if not path.exists():
        warnings.append(
            f"GPU report referenced by orchestrator is missing: {repo_rel(path, repo_root)}"
        )
        return {}
    try:
        return load_json_object(path)
    except Exception as exc:  # noqa: BLE001 - report-only diagnostic.
        warnings.append(
            f"Unable to read GPU report {repo_rel(path, repo_root)}: {type(exc).__name__}: {exc}"
        )
        return {}

def npu_audit_refs(orchestrator: dict[str, Any]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for audit in (
        orchestrator.get("npu_audits", [])
        if isinstance(orchestrator.get("npu_audits"), list)
        else []
    ):
        if not isinstance(audit, dict):
            continue
        refs.append(
            {
                "round": audit.get("round"),
                "status": audit.get("status"),
                "classification": audit.get("classification"),
                "provider_execution_requested": audit.get("provider_execution_requested"),
                "provider_load_attempted": audit.get("provider_load_attempted"),
                "provider_execution_succeeded": audit.get("provider_execution_succeeded"),
                "provider_execution_performed": audit.get("provider_execution_performed"),
                "dependency_missing": audit.get("dependency_missing"),
                "gpu_review_blocked": audit.get("gpu_review_blocked"),
                "audit_output": audit.get("audit_output"),
            }
        )
    return refs
