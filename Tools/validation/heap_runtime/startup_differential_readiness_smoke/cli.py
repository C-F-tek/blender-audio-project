#!/usr/bin/env python3
"""Validate differential startup scan, RAG ingest, and tool catalog cache."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from argparse import Namespace
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.heap_context_memory_reload.common import write_json
from ia_carmine.context.heap_context_memory_reload.runner import (
    _store_tool_catalog_cache,
    _try_restore_tool_catalog_cache,
)
from ia_carmine.context.heap_context_memory_reload.runner_state import ReloadRun
from ia_carmine.context.heap_context_memory_reload.startup_scan import build_startup_repo_scan_index

PROJECT_ROOT = Path(__file__).resolve().parents[4]


def _run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(PROJECT_ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def _make_repo(root: Path, file_count: int = 100) -> None:
    _run(["git", "init"], root)
    for index in range(file_count):
        path = root / "docs" / f"file_{index:03d}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# File {index}\n\nprovider context {index}\n", encoding="utf-8")
    (root / "Tools").mkdir(exist_ok=True)
    (root / "Tools" / "dispatch.py").write_text("TOOLS = []\n", encoding="utf-8")
    (root / "ia_carmine" / "demo").mkdir(parents=True, exist_ok=True)
    (root / "ia_carmine" / "demo" / "cli.py").write_text("def main(): return 0\n", encoding="utf-8")


def _ingest(repo: Path, scan_index: Path, output: Path) -> dict[str, Any]:
    completed = _run(
        [
            sys.executable,
            "-m",
            "ia_carmine.context.agent_context.rag_context.ingest_repo_cli",
            "--repo-root",
            str(repo),
            "--db",
            str(repo / "rag.sqlite"),
            "--skip-embeddings",
            "--allow-missing-embeddings",
            "--startup-scan-index",
            str(scan_index),
            "--output",
            str(output),
            "--markdown-output",
            str(output.with_suffix(".md")),
        ],
        repo,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr[-1200:] or completed.stdout[-1200:])
    return json.loads(output.read_text(encoding="utf-8"))


def _state(repo: Path, output_dir: Path, scan_index: dict[str, Any], stamp: str) -> ReloadRun:
    return ReloadRun(
        args=Namespace(rag_max_file_size=250000),
        repo_root=repo,
        stamp=stamp,
        project_python=sys.executable,
        output_dir=output_dir,
        request_text="startup differential smoke",
        repo_scan_index=scan_index,
    )


def run_smoke() -> dict[str, Any]:
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    errors: list[str] = []
    try:
        with tempfile.TemporaryDirectory(prefix="startup-delta-smoke-") as temp:
            repo = Path(temp) / "repo"
            repo.mkdir()
            _make_repo(repo)
            first_dir = repo / "output" / "first"
            second_dir = repo / "output" / "second"
            first_scan = build_startup_repo_scan_index(repo, first_dir, max_hash_size=250000)
            first_scan_path = first_dir / "startup_repo_scan_index.json"
            _ingest(repo, first_scan_path, first_dir / "rag_ingest.json")
            time.sleep(0.02)
            changed_path = repo / "docs" / "file_042.md"
            changed_path.write_text("# File 42\n\nprovider context changed\n", encoding="utf-8")
            second_scan = build_startup_repo_scan_index(repo, second_dir, max_hash_size=250000)
            second_scan_path = second_dir / "startup_repo_scan_index.json"
            second_ingest = _ingest(repo, second_scan_path, second_dir / "rag_ingest.json")
            checks["delta_scan_one_changed"] = (
                second_scan.get("changed_file_count") == 1
                and second_scan.get("unchanged_ref_only_count", 0) >= 100
                and second_scan.get("changed_files") == ["docs/file_042.md"]
            )
            checks["rag_reads_only_changed"] = (
                second_ingest.get("read_file_count") == 1
                and second_ingest.get("chunked_file_count") == 1
                and second_ingest.get("unchanged_ref_only_document_count", 0) >= 100
                and second_ingest.get("startup_repo_scan_index_used") is True
            )
            cache_source_dir = repo / "output" / "cache_source"
            cache_restore_dir = repo / "output" / "cache_restore"
            cache_source_dir.mkdir(parents=True)
            catalog_json = cache_source_dir / "startup_tool_catalog.json"
            catalog_md = cache_source_dir / "startup_tool_catalog.md"
            write_json(catalog_json, {"schema_version": 1, "kind": "tool_catalog", "passed": True})
            catalog_md.write_text("# Tool Catalog\n", encoding="utf-8")
            state = _state(repo, cache_source_dir, second_scan, "source-run")
            _store_tool_catalog_cache(
                state,
                catalog_json,
                catalog_md,
                {"effective_passed": True},
            )
            restore_state = _state(repo, cache_restore_dir, second_scan, "restore-run")
            restored = _try_restore_tool_catalog_cache(
                restore_state,
                cache_restore_dir / "startup_tool_catalog.json",
                cache_restore_dir / "startup_tool_catalog.md",
            )
            checks["tool_catalog_cache_hit"] = bool(restored and restored.get("cache_hit"))
            details = {
                "second_scan": {
                    "changed_file_count": second_scan.get("changed_file_count"),
                    "unchanged_ref_only_count": second_scan.get("unchanged_ref_only_count"),
                    "changed_files": second_scan.get("changed_files"),
                },
                "second_ingest": {
                    "read_file_count": second_ingest.get("read_file_count"),
                    "chunked_file_count": second_ingest.get("chunked_file_count"),
                    "unchanged_ref_only_document_count": second_ingest.get(
                        "unchanged_ref_only_document_count"
                    ),
                },
                "tool_catalog_cache": {
                    "cache_hit": restored.get("cache_hit") if restored else False,
                    "source_run": restored.get("source_run") if restored else "",
                },
            }
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{type(exc).__name__}: {exc}")
    errors.extend(name for name, passed in checks.items() if not passed)
    return {
        "schema_version": 1,
        "kind": "startup_differential_readiness_smoke",
        "passed": not errors,
        "checks": checks,
        "details": details,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/startup_differential_readiness_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke()
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
