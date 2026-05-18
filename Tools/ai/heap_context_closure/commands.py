"""Command builders for heap context closure."""

from __future__ import annotations

from typing import Any


def startup_command(args: Any, state: dict[str, Any]) -> list[str]:
    return [
        state["project_python"],
        "-m",
        "Tools.ai",
        "heap_context_memory_reload",
        "--repo-root",
        ".",
        "--request-file",
        str(state["heap_request_file"]),
        "--stamp",
        state["stamp"],
        "--python-exe",
        state["project_python"],
        "--output-dir",
        str(state["startup_dir"]),
        "--max-memory-chars",
        str(args.startup_max_memory_chars),
        "--max-context-files",
        str(args.startup_max_context_files),
        "--startup-scan-context-files",
        str(args.startup_scan_context_files),
        "--max-chars-per-file",
        str(args.startup_max_chars_per_file),
    ]


def heap_command(args: Any, state: dict[str, Any]) -> list[str]:
    return [
        state["project_python"],
        "-m",
        "Tools.ai",
        "run_heap_runtime_completeness_gate",
        "--repo-root",
        ".",
        "--request-file",
        str(state["heap_request_file"]),
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-iterations",
        str(args.max_iterations),
        "--min-runtime-rounds",
        str(args.min_runtime_rounds),
        "--min-proposal-iterations",
        str(args.min_proposal_iterations),
        "--max-rounds",
        str(args.max_rounds),
        "--max-provider-revisions",
        str(args.max_provider_revisions),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--allow-npu-device-workload",
        "--npu-device-workload-seconds",
        str(args.npu_device_workload_seconds),
        "--npu-device-workload-iterations",
        str(args.npu_device_workload_iterations),
        "--output-dir",
        str(state["run_dir"]),
        "--output",
        str(state["report_file"]),
        "--markdown-output",
        str(state["markdown_file"]),
    ]
