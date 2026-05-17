"""Models and profile key maps for operator product launcher."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

PROFILE_FILE = "Tools/ai/runtime_profiles/heap_runtime_launcher_profiles.json"
DEFAULT_PROFILE = "balanced_external_heap"

CLI_VALUE_KEYS = {
    "budget_minutes": "--budget-minutes",
    "max_iterations": "--max-iterations",
    "min_runtime_rounds": "--min-runtime-rounds",
    "min_proposal_iterations": "--min-proposal-iterations",
    "max_rounds": "--max-rounds",
    "max_provider_revisions": "--max-provider-revisions",
    "timeout_seconds": "--timeout-seconds",
    "preflight_timeout_seconds": "--preflight-timeout-seconds",
    "npu_device_workload_seconds": "--npu-device-workload-seconds",
    "npu_device_workload_iterations": "--npu-device-workload-iterations",
    "startup_max_memory_chars": "--startup-max-memory-chars",
    "startup_max_context_files": "--startup-max-context-files",
    "startup_scan_context_files": "--startup-scan-context-files",
    "startup_max_chars_per_file": "--startup-max-chars-per-file",
    "revision_context_max_tasks": "--revision-context-max-tasks",
}

CLI_FLAG_KEYS = {
    "allow_provider_generation": "--allow-provider-generation",
    "skip_preflight": "--skip-preflight",
    "skip_startup_reload": "--skip-startup-reload",
    "strict_startup_reload": "--strict-startup-reload",
    "no_documents": "--no-documents",
}


@dataclass
class LauncherConfig:
    repo_root: Path
    request_file: Path
    intermediate_root: Path
    final_root: Path
    profile_name: str = DEFAULT_PROFILE
    python_exe: str = ""
    stamp: str = ""
    revision_context: str = ""
    profiles_file: Path | None = None
    profile_overrides: dict[str, Any] | None = None
