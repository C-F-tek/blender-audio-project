"""Repository consistency report builder."""

from __future__ import annotations

import os
import time
from collections import Counter
from pathlib import Path
from typing import Any

from Tools.ai.repository_consistency_map.constants import DOC_EXTENSIONS
from Tools.ai.repository_consistency_map.findings import (
    build_findings,
    build_provider_hints,
)
from Tools.ai.repository_consistency_map.markdown import extract_markdown_references
from Tools.ai.repository_consistency_map.paths import (
    bounded_worker_count,
    build_existing_path_index,
    build_repo_file_manifest,
    build_repo_file_records,
    elapsed_seconds,
    filter_manifest_by_extensions,
    now_iso,
)
from Tools.ai.repository_consistency_map.python_inventory import (
    extract_python_inventory,
)


def build_report(
    *,
    repo_root: Path,
    max_detail_items: int,
    max_snippet_chars: int,
    workers: int,
    worker_backend: str = "process",
    worker_cpu_target: float = 0.40,
    max_auto_workers: int | None = 8,
) -> dict[str, Any]:
    total_started = time.perf_counter()
    timings: dict[str, float] = {}

    phase_started = time.perf_counter()
    all_files = build_repo_file_manifest(repo_root)
    markdown_files = filter_manifest_by_extensions(all_files, DOC_EXTENSIONS)
    python_files = filter_manifest_by_extensions(all_files, {".py"})
    file_records = build_repo_file_records(repo_root, all_files)
    counted_file_records = [item for item in file_records if item.get("line_count_available")]
    markdown_file_count = len(markdown_files)
    python_file_count = len(python_files)
    timings["file_discovery_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    path_index = build_existing_path_index(repo_root, files=all_files)
    timings["path_index_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    md_refs, md_commands, md_warnings = extract_markdown_references(
        repo_root,
        path_index,
        max_snippet_chars=max_snippet_chars,
        workers=workers,
        markdown_files=markdown_files,
        worker_backend=worker_backend,
        worker_cpu_target=worker_cpu_target,
        max_auto_workers=max_auto_workers,
    )
    timings["markdown_scan_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    py_inventory, import_findings, py_warnings = extract_python_inventory(
        repo_root,
        workers=workers,
        python_files=python_files,
        worker_backend=worker_backend,
        worker_cpu_target=worker_cpu_target,
        max_auto_workers=max_auto_workers,
    )
    timings["python_inventory_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    findings = build_findings(
        md_refs=md_refs,
        md_commands=md_commands,
        py_inventory=py_inventory,
        import_findings=import_findings,
    )
    severity_counts = Counter(str(item.get("severity")) for item in findings)
    kind_counts = Counter(str(item.get("kind")) for item in findings)
    references_by_kind = Counter(str(item.get("kind")) for item in md_refs)
    provider_hints = build_provider_hints(findings)
    timings["findings_build_seconds"] = elapsed_seconds(phase_started)

    phase_started = time.perf_counter()
    scope = {
        "repository_file_count": len(all_files),
        "repository_file_metadata_count": len(file_records),
        "repository_line_count_available_count": len(counted_file_records),
        "repository_text_line_count_total": sum(
            int(item.get("line_count") or 0) for item in counted_file_records
        ),
        "markdown_file_count": markdown_file_count,
        "python_file_count": python_file_count,
        "markdown_reference_count": len(md_refs),
        "markdown_python_command_count": len(md_commands),
        "python_inventory_count": len(py_inventory),
    }
    performance = {
        "workers_requested": workers,
        "worker_backend_requested": worker_backend,
        "worker_cpu_target": worker_cpu_target,
        "max_auto_workers": max_auto_workers,
        "adaptive_worker_mode": workers <= 0,
        "cpu_count": os.cpu_count() or 1,
        "cpu_process_worker_backend_enabled": worker_backend
        in {"process", "auto", "cpu", "multiprocessing"},
        "repo_file_count": len(all_files),
        "single_file_discovery_manifest_enabled": True,
        "file_metadata_enabled": True,
        "markdown_scan_workers": bounded_worker_count(
            workers,
            markdown_file_count,
            cpu_target=worker_cpu_target,
            max_auto_workers=max_auto_workers,
        ),
        "python_scan_workers": bounded_worker_count(
            workers,
            python_file_count,
            cpu_target=worker_cpu_target,
            max_auto_workers=max_auto_workers,
        ),
        **timings,
    }
    performance["report_assembly_seconds"] = elapsed_seconds(phase_started)
    performance["total_build_report_seconds"] = elapsed_seconds(total_started)

    return {
        "schema_version": 1,
        "kind": "repository_consistency_map",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": md_warnings + py_warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "scope": {
            **scope,
            "generated_evidence_chunk_exclusion_enabled": True,
        },
        "finding_count": len(findings),
        "severity_counts": dict(sorted(severity_counts.items())),
        "finding_kind_counts": dict(sorted(kind_counts.items())),
        "markdown_reference_kind_counts": dict(sorted(references_by_kind.items())),
        "findings": findings,
        "markdown_references": (md_refs[:max_detail_items] if max_detail_items else md_refs),
        "markdown_python_commands": (
            md_commands[:max_detail_items] if max_detail_items else md_commands
        ),
        "python_inventory": py_inventory,
        "repository_file_metadata": (
            file_records[:max_detail_items] if max_detail_items else file_records
        ),
        "provider_hints_for_gpu_planner": provider_hints,
        "performance": performance,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "do_not_commit_output": True,
            "generated_evidence_chunk_dirs_excluded": True,
            "repository_file_metadata_enabled": True,
            "repository_file_line_count_enabled": True,
            "repository_file_modified_at_enabled": True,
        },
    }
