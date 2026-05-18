#!/usr/bin/env python3
"""Run GPU/Ollama deep planning with non-blocking intermediate NPU audits.

This supervised runner is the long-running IA-Carmine planning mode:

- GPU/Ollama performs multi-round reasoning over repository evidence;
- each round writes an intermediate checkpoint JSON/Markdown artifact;
- optional NPU auditor inspects checkpoints as a non-blocking guardrail;
- NPU failures, unusable text or missing OpenVINO are warnings only;
- repeated deterministic NPU dependency failures are circuit-broken;
- no patch is applied and no GitHub PR is created.
"""

from __future__ import annotations

from pathlib import Path

try:
    from Tools.ai.schema_repair_context import build_schema_repair_context_stack
except ImportError:
    import sys as _schema_repair_sys

    _schema_repair_repo_root = Path(__file__).resolve().parents[2]
    if str(_schema_repair_repo_root) not in _schema_repair_sys.path:
        _schema_repair_sys.path.insert(0, str(_schema_repair_repo_root))
    from Tools.ai.schema_repair_context import build_schema_repair_context_stack  # type: ignore

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.gpu_deep_planning_review import (
        DEFAULT_EVIDENCE,
        DEFAULT_REFINED,
        aggregate_recommendation_diagnostics,
        build_markdown,
        build_prompt,
        collect_repo_context,
        evidence_ready_for_manual_patch_count,
        extract_evidence_files,
        extract_valid_tool_requests,
        merge_recommendations,
        parse_model_json_with_diagnostics,
        read_json,
        recommendation_diagnostics_for_round,
        repo_rel,
        resolve_path,
        split_batches,
    )
    from Tools.ai._shared.runtime_tool_guidance import deterministic_fallback_tool_requests
    from Tools.npu._shared.ollama_runtime import (
        DEFAULT_BASE_URL,
        OllamaModelManager,
        normalize_base_url,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.gpu_deep_planning_review import (  # type: ignore
        DEFAULT_EVIDENCE,
        DEFAULT_REFINED,
        aggregate_recommendation_diagnostics,
        build_markdown,
        build_prompt,
        collect_repo_context,
        evidence_ready_for_manual_patch_count,
        extract_evidence_files,
        extract_valid_tool_requests,
        merge_recommendations,
        parse_model_json_with_diagnostics,
        read_json,
        recommendation_diagnostics_for_round,
        repo_rel,
        resolve_path,
        split_batches,
    )
    from Tools.ai._shared.runtime_tool_guidance import deterministic_fallback_tool_requests  # type: ignore
    from Tools.npu._shared.ollama_runtime import (  # type: ignore
        DEFAULT_BASE_URL,
        OllamaModelManager,
        normalize_base_url,
    )


from Tools.ai.schema_repair import (
    build_schema_repair_retry_prompt,
    should_attempt_schema_repair_retry,
    summarize_schema_repair_retry,
)

DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_supervised.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_supervised.md"
DEFAULT_CHECKPOINT_DIR = "output/ai_pipeline/gpu_deep_planning_checkpoints"
TERMINAL_NPU_AUDIT_CLASSIFICATIONS = {"dependency_missing_openvino_genai"}

DEFAULT_RUNTIME_TOOL_BOOTSTRAP_REQUESTS: list[dict[str, Any]] = [
    {
        "id": "bootstrap_tool_inventory",
        "tool": "build_agent_agnostic_tool_inventory",
        "reason": "Bootstrap available runtime tools, capabilities and guardrails before GPU planning.",
        "args": {},
    },
    {
        "id": "bootstrap_memory_inventory",
        "tool": "build_agent_memory_inventory",
        "reason": "Bootstrap durable project memory inventory before GPU planning.",
        "args": {},
    },
    {
        "id": "bootstrap_persistent_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap persistent memory status in read-only mode before GPU planning.",
        "args": {"action": "status", "scope": "persistent"},
    },
    {
        "id": "bootstrap_operational_memory_status",
        "tool": "runtime_sqlite_memory",
        "reason": "Bootstrap operational scratch memory status before GPU planning.",
        "args": {"action": "status", "scope": "operational"},
    },
    {
        "id": "bootstrap_python_line_count",
        "tool": "build_python_line_count_csv",
        "reason": "Bootstrap full Python inventory before refactor planning.",
        "args": {},
    },
    {
        "id": "bootstrap_python_syntax",
        "tool": "check_python_syntax",
        "reason": "Bootstrap Python syntax baseline before code planning.",
        "args": {},
    },
    {
        "id": "bootstrap_gpu_contract_smoke",
        "tool": "run_gpu_planner_json_contract_smoke",
        "reason": "Bootstrap GPU JSON contract validation, including runtime tool request support.",
        "args": {},
    },
]


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def run_command(
    command: list[str], repo_root: Path, timeout_seconds: int
) -> tuple[int, str, str, str | None]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return (
            completed.returncode,
            completed.stdout[-12000:],
            completed.stderr[-12000:],
            None,
        )
    except subprocess.TimeoutExpired as exc:
        return (
            124,
            exc.stdout or "",
            exc.stderr or "",
            f"TimeoutExpired: {timeout_seconds}s",
        )
    except Exception as exc:  # noqa: BLE001 - non-blocking auditor runner.
        return 1, "", "", f"{type(exc).__name__}: {exc}"

def compact_tool_results_for_context(
    tool_results: list[dict[str, Any]], *, max_items: int = 8
) -> list[dict[str, Any]]:
    compact: list[dict[str, Any]] = []
    for item in tool_results[:max_items]:
        compact.append(
            {
                "id": item.get("id"),
                "tool": item.get("tool"),
                "executed": item.get("executed"),
                "blocked": item.get("blocked"),
                "returncode": item.get("returncode"),
                "outputs": item.get("outputs", {}),
                "summary": item.get("summary", {}),
                "guardrails": item.get("guardrails", {}),
                "errors": item.get("errors", []),
            }
        )
    return compact
