#!/usr/bin/env python3
"""Static smoke for heap startup context ingestion wiring.

This validator is report-only. It does not execute providers, Blender, FFmpeg,
patch application, Git writes, or runtime output generation beyond its own JSON
report. Its purpose is to distinguish these two states:

1. startup context is merely produced and passed as a task-file path;
2. startup context/manifest/artifact refs become heap events/facts before the
   provider loop can make decisions.

A failing report is useful: it identifies exactly which wiring contract is not
proved yet.
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


SOURCE_FILES = {
    "launcher": "Tools/ai/heap_context_closure/cli.py",
    "gate": "Tools/ai/heap_runtime/completeness_gate/cli.py",
    "preload": "Tools/ai/heap_context_memory_reload/cli.py",
    "reconciler": "Tools/ai/heap_context_memory_reload/reconcile_report/cli.py",
    "composer": "Tools/ai/heap_final_proposals/cli.py",
}


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError:
        return ""


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.as_posix()


def def_body_call_count(source: str, name: str) -> int:
    """Return occurrences of a function/method call outside its own def line."""
    count = 0
    call_pattern = re.compile(rf"\b(?:self\.)?{re.escape(name)}\s*\(")
    def_pattern = re.compile(rf"^\s*def\s+{re.escape(name)}\s*\(")
    for line in source.splitlines():
        if def_pattern.search(line):
            continue
        if call_pattern.search(line):
            count += 1
    return count


def first_position(source: str, needle: str) -> int:
    position = source.find(needle)
    return position if position >= 0 else 10**12


def bool_check(
    checks: list[dict[str, Any]],
    *,
    check_id: str,
    passed: bool,
    severity: str,
    evidence: str,
    recommendation: str,
) -> None:
    checks.append(
        {
            "id": check_id,
            "passed": bool(passed),
            "severity": severity,
            "evidence": evidence,
            "recommendation": recommendation,
        }
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Startup Context Ingestion Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Critical failures: `{report.get('critical_failure_count')}`",
        f"- Warning failures: `{report.get('warning_failure_count')}`",
        f"- Provider execution performed: `{report.get('provider_execution_performed')}`",
        f"- Patch application performed: `{report.get('patch_application_performed')}`",
        "",
        "## Checks",
        "",
    ]
    for item in report.get("checks") or []:
        lines.extend(
            [
                f"### `{item.get('id')}`",
                "",
                f"- Passed: `{item.get('passed')}`",
                f"- Severity: `{item.get('severity')}`",
                f"- Evidence: {item.get('evidence')}",
                f"- Recommendation: {item.get('recommendation')}",
                "",
            ]
        )
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def build_report(repo_root: Path) -> dict[str, Any]:
    sources = {name: read_text(repo_root / rel_path) for name, rel_path in SOURCE_FILES.items()}
    checks: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []

    missing_sources = [rel_path for name, rel_path in SOURCE_FILES.items() if not sources.get(name)]
    for rel_path in missing_sources:
        errors.append(f"required source unreadable: {rel_path}")

    launcher = sources.get("launcher", "")
    gate = sources.get("gate", "")
    preload = sources.get("preload", "")
    reconciler = sources.get("reconciler", "")
    composer = sources.get("composer", "")

    bool_check(
        checks,
        check_id="launcher_passes_startup_task_file",
        passed="--task-file" in launcher and "startup_task_file" in launcher,
        severity="critical",
        evidence="launcher should pass heap_startup_input_ready_context.md into python -m Tools.ai run_heap_runtime_completeness_gate",
        recommendation="Keep --task-file forwarding in python -m Tools.ai heap_context_closure.",
    )

    bool_check(
        checks,
        check_id="gate_declares_task_file_argument",
        passed="--task-file" in gate,
        severity="critical",
        evidence="gate parser must accept --task-file if launcher passes it",
        recommendation="Add parser.add_argument('--task-file', ...) to python -m Tools.ai run_heap_runtime_completeness_gate if absent.",
    )

    task_file_read = bool(
        re.search(r"task_file[^\n]{0,120}read_text\s*\(", gate)
        or re.search(r"read_text\s*\([^\n]{0,120}task_file", gate)
        or re.search(r"Path\([^\n]{0,80}task_file[^\n]{0,160}\)\.read_text\s*\(", gate)
    )
    bool_check(
        checks,
        check_id="gate_reads_task_file_content",
        passed=task_file_read,
        severity="critical",
        evidence="passing a task-file path is not enough; gate should read it and emit heap facts/events from it",
        recommendation="Read task-file content during gate startup and append a bounded heap fact/telemetry event with path, hash, preview, and artifact refs.",
    )

    lifecycle_defined = "def publish_startup_memory_context_reload_events" in gate
    lifecycle_call_count = def_body_call_count(gate, "publish_startup_memory_context_reload_events")
    bool_check(
        checks,
        check_id="startup_reload_lifecycle_invoked",
        passed=lifecycle_defined and lifecycle_call_count > 0,
        severity="critical",
        evidence=f"defined={lifecycle_defined}; non-def call count={lifecycle_call_count}",
        recommendation="Invoke publish_startup_memory_context_reload_events() during heap initialization before provider rounds.",
    )

    bool_check(
        checks,
        check_id="memory_context_reload_payload_emitted",
        passed="memory_context_reload" in gate and "append_heap_exchange_event" in gate,
        severity="critical",
        evidence="gate should emit reload lifecycle as heap events/facts, not only report fields",
        recommendation="Emit payload.kind='memory_context_reload' as stable fact/telemetry_signal before provider rounds.",
    )

    bool_check(
        checks,
        check_id="startup_artifact_refs_named_in_gate",
        passed="artifact_refs" in gate
        or "context_artifact_refs" in gate
        or "startup_manifest" in gate,
        severity="critical",
        evidence="provider lanes need startup artifact refs available from heap state",
        recommendation="Propagate startup manifest/task-file/artifact refs into heap events and provider context.",
    )

    startup_publish_positions = [
        first_position(gate, "self.publish_startup_task_file_context()"),
        first_position(gate, "self.publish_startup_memory_context_reload_events()"),
        first_position(gate, "self.publish_startup_manifest_evidence()"),
    ]
    first_snapshot_position = first_position(gate, "self.heap.write_snapshot()")
    startup_before_snapshot = all(
        position < first_snapshot_position for position in startup_publish_positions
    )
    bool_check(
        checks,
        check_id="startup_context_published_before_initial_snapshot",
        passed=startup_before_snapshot,
        severity="critical",
        evidence="startup task-file/manifest/reload events must be published before the first heap snapshot",
        recommendation="Move startup preload publication before self.heap.write_snapshot() in bootstrap().",
    )

    bool_check(
        checks,
        check_id="reconciler_allows_degraded_startup_policy",
        passed=("allow-degraded" in reconciler or "allow_degraded" in reconciler)
        and "refusing to reconcile" not in reconciler,
        severity="warning",
        evidence="degradable startup policy requires using useful artifacts while preserving degraded warnings",
        recommendation="Add --allow-degraded-startup or equivalent artifact-useful policy to reconciler.",
    )

    shape_terms = (
        "useful_artifact_paths",
        "existing_artifact_paths",
        "artifact_summaries",
        "artifact_paths",
    )
    covered_terms = [term for term in shape_terms if term in reconciler]
    bool_check(
        checks,
        check_id="reconciler_reads_preload_tool_execution_artifact_shapes",
        passed=len(covered_terms) >= 3,
        severity="warning",
        evidence=f"covered artifact shape terms={covered_terms}",
        recommendation="Read execution.useful_artifact_paths, existing_artifact_paths, artifact_paths and artifact_summaries[].path.",
    )

    operational_write_signal = bool(
        "operational_memory_write" in preload
        and "runtime_sqlite_memory" in preload
        and "remember" in preload
    )
    bool_check(
        checks,
        check_id="startup_records_operational_memory_write",
        passed=operational_write_signal,
        severity="warning",
        evidence="BASE_REQUIREMENTS contains operational_memory_write; startup should prove a run-specific scratch write or gate should do it before provider loop",
        recommendation="Record startup manifest summary into operational SQLite memory under output/** with action=remember, scope=operational.",
    )

    bool_check(
        checks,
        check_id="composer_exposes_product_causality_flag",
        passed="product_causality_passed" in composer
        or "startup_context_seen_before_first_provider" in composer,
        severity="warning",
        evidence="composer packages reports after the fact; it should expose whether startup context was causally seen before provider output",
        recommendation="Add product_causality_passed plus startup/provider ordering flags to python -m Tools.ai heap_final_proposals.",
    )

    critical_failures = [
        item for item in checks if item["severity"] == "critical" and not item["passed"]
    ]
    warning_failures = [
        item for item in checks if item["severity"] == "warning" and not item["passed"]
    ]
    passed = not errors and not critical_failures
    if warning_failures:
        warnings.append(f"warning checks failed: {len(warning_failures)}")

    return {
        "schema_version": 1,
        "kind": "heap_startup_context_ingestion_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": passed,
        "critical_failure_count": len(critical_failures),
        "warning_failure_count": len(warning_failures),
        "checked_sources": {
            key: repo_rel(repo_root, repo_root / value) for key, value in SOURCE_FILES.items()
        },
        "checks": checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_touched": False,
        "ffmpeg_runtime_touched": False,
        "errors": errors,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_startup_context_ingestion_smoke.json"
    )
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(
        repo_root,
        args.markdown_output or str(Path(args.output).with_suffix(".md")),
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)
    print(
        json.dumps(
            {
                **report,
                "output": repo_rel(repo_root, output),
                "markdown_output": repo_rel(repo_root, markdown_output),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
