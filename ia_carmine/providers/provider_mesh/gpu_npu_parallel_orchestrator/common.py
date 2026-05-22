#!/usr/bin/env python3
"""Run GPU deep planning and NPU checkpoint audits in parallel.

This is the non-blocking orchestration prototype:

- GPU/Ollama planner runs continuously in its own process;
- checkpoint files are monitored as they appear;
- GPU0/OpenVINO support micro-work is launched as a peer subprocess while
  GPU1/Ollama keeps planning;
- legacy NPU audits are launched as separate best-effort subprocesses only
  when explicitly requested;
- GPU planning does not wait for GPU0/NPU support completion;
- NPU audit concurrency is capped to avoid overloading the NPU/runtime;
- final report joins GPU output plus all completed NPU audits.

No patches are applied and no PR is created.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_npu_parallel_orchestrator.md"
DEFAULT_GPU_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.json"
DEFAULT_GPU_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_parallel_gpu.md"
DEFAULT_CHECKPOINT_DIR = "output/ai_pipeline/gpu_deep_planning_parallel_checkpoints"
DEFAULT_GPU0_PEER_SUPPORT_DIR = "output/ai_pipeline/gpu0_peer_support_parallel"
DEFAULT_NPU_MICRO_SUPPORT_DIR = "output/ai_pipeline/npu_micro_support_parallel"
ROUND_RE = re.compile(r"round_(\d{3})\.json$")

try:
    from ia_carmine.product.deterministic_recommendations.evidence_to_recommendation import write_recommendation_event
    from ia_carmine.product.patch_product.patch_plan_generator import write_patch_plan_event
    from ia_carmine.runtime.provider_runtime_blackboard import ProviderRuntimeHeap
    from ia_carmine._shared.runtime_tool_guidance import deterministic_fallback_tool_requests
    from ia_carmine.product.pipeline.validation_step import write_validation_event
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.product.deterministic_recommendations.evidence_to_recommendation import write_recommendation_event  # type: ignore
    from ia_carmine.product.patch_product.patch_plan_generator import write_patch_plan_event  # type: ignore
    from ia_carmine.runtime.provider_runtime_blackboard import ProviderRuntimeHeap  # type: ignore
    from ia_carmine._shared.runtime_tool_guidance import deterministic_fallback_tool_requests  # type: ignore
    from ia_carmine.product.pipeline.validation_step import write_validation_event  # type: ignore

try:
    from ia_carmine.providers.provider_mesh.runtime.gpu0_peer import (
        build_gpu0_peer_support_command,
        gpu0_peer_support_output_path,
        should_launch_gpu0_peer_support,
    )
    from ia_carmine.providers.provider_mesh.runtime.npu_micro import (
        build_npu_micro_support_command,
        collect_runtime_tool_context_reports,
        npu_micro_support_output_path,
    )
    from ia_carmine.providers.provider_mesh.runtime.python_runtime import (
        command_env,
        resolve_child_python,
    )
    from ia_carmine.providers.provider_mesh.runtime.runtime_heap import (
        append_runtime_heap_event,
        record_runtime_lane_diagnostic,
        write_runtime_heap_snapshot,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.providers.provider_mesh.runtime.gpu0_peer import (  # type: ignore
        build_gpu0_peer_support_command,
        gpu0_peer_support_output_path,
        should_launch_gpu0_peer_support,
    )
    from ia_carmine.providers.provider_mesh.runtime.npu_micro import (  # type: ignore
        build_npu_micro_support_command,
        collect_runtime_tool_context_reports,
        npu_micro_support_output_path,
    )
    from ia_carmine.providers.provider_mesh.runtime.python_runtime import (  # type: ignore
        command_env,
        resolve_child_python,
    )
    from ia_carmine.providers.provider_mesh.runtime.runtime_heap import (  # type: ignore
        append_runtime_heap_event,
        record_runtime_lane_diagnostic,
        write_runtime_heap_snapshot,
    )

ORCHESTRATOR_RUNTIME_TOOL_BOOTSTRAP_REQUESTS: list[dict[str, object]] = [
    {
        "id": "orchestrator_bootstrap_tool_inventory",
        "tool": "build_agent_agnostic_tool_inventory",
        "reason": "Bootstrap shared runtime tool inventory before GPU/NPU orchestration.",
        "args": {},
    },
    {
        "id": "orchestrator_bootstrap_memory_inventory",
        "tool": "build_agent_memory_inventory",
        "reason": "Bootstrap durable project memory inventory before GPU/NPU orchestration.",
        "args": {},
    },
    {
        "id": "orchestrator_bootstrap_persistent_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap persistent memory status in read-only mode before GPU/NPU orchestration.",
        "args": {"action": "status", "scope": "persistent"},
    },
    {
        "id": "orchestrator_bootstrap_operational_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap operational scratch memory status before GPU/NPU orchestration.",
        "args": {"action": "status", "scope": "operational"},
    },
    {
        "id": "orchestrator_bootstrap_python_line_count",
        "tool": "build_python_line_count_csv",
        "reason": "Bootstrap Python inventory before orchestration.",
        "args": {},
    },
    {
        "id": "orchestrator_bootstrap_python_syntax",
        "tool": "check_python_syntax",
        "reason": "Bootstrap Python syntax baseline before orchestration.",
        "args": {},
    },
    {
        "id": "orchestrator_bootstrap_gpu_contract_smoke",
        "tool": "run_gpu_planner_json_contract_smoke",
        "reason": "Bootstrap GPU JSON contract validation before orchestration.",
        "args": {},
    },
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def terminate_process(process: subprocess.Popen[str], timeout_seconds: float = 3.0) -> None:
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=timeout_seconds)
    except subprocess.TimeoutExpired:
        process.kill()
        try:
            process.wait(timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            pass

def run_command_async(command: list[str], repo_root: Path) -> subprocess.Popen[str]:
    return subprocess.Popen(
        command,
        cwd=repo_root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=command_env(repo_root),
    )

def run_command_sync(
    command: list[str], repo_root: Path, timeout_seconds: int
) -> tuple[int, str, str, str]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env=command_env(repo_root),
        )
        return (
            completed.returncode,
            completed.stdout[-12000:],
            completed.stderr[-12000:],
            "",
        )
    except subprocess.TimeoutExpired as exc:
        return (
            124,
            exc.stdout or "",
            exc.stderr or "",
            f"TimeoutExpired: {timeout_seconds}s",
        )
    except Exception as exc:  # noqa: BLE001 - report-only runtime broker execution must be captured.
        return 1, "", "", f"{type(exc).__name__}: {exc}"

def checkpoint_round(path: Path) -> int | None:
    match = ROUND_RE.search(path.name)
    if not match:
        return None
    return int(match.group(1))

def collect_stdout_stderr(process: subprocess.Popen[str]) -> tuple[str, str]:
    stdout = ""
    stderr = ""
    try:
        out, err = process.communicate(timeout=1)
        stdout = out or ""
        stderr = err or ""
    except subprocess.TimeoutExpired:
        return "", ""
    return stdout[-12000:], stderr[-12000:]

def record_round_id(record: dict[str, Any]) -> int:
    value = record.get("round")
    if value in (None, ""):
        return -1
    try:
        return int(value)
    except (TypeError, ValueError):
        return -1

def lane_status_from_success(enabled: bool, success: bool) -> str:
    if not enabled:
        return "disabled"
    return "ready" if success else "degraded"

def runtime_state_gate(lane_status: dict[str, str], max_degraded_lanes: int) -> dict[str, Any]:
    degraded = sorted(
        lane
        for lane, status in lane_status.items()
        if str(status).lower() in {"degraded", "failed"}
    )
    return {
        "passed": len(degraded) <= max(0, int(max_degraded_lanes)),
        "max_degraded_lanes": max(0, int(max_degraded_lanes)),
        "degraded_lanes": degraded,
        "degraded_lane_count": len(degraded),
        "lane_status": dict(sorted(lane_status.items())),
    }

def safe_int(value: Any, default: int = 0) -> int:
    try:
        if value is None or value == "":
            return default
        return int(value)
    except (TypeError, ValueError):
        return default

def parse_iso_seconds(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None

def audit_elapsed_seconds(audit_record: dict[str, Any]) -> float | None:
    explicit = audit_record.get("elapsed_seconds")
    if explicit is not None:
        try:
            return float(explicit)
        except (TypeError, ValueError):
            pass
    start = parse_iso_seconds(audit_record.get("started_at"))
    finish = parse_iso_seconds(audit_record.get("finished_at"))
    if not start or not finish:
        return None
    return max(0.0, (finish - start).total_seconds())
