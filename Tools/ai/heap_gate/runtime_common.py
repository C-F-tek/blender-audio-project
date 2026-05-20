"""Shared imports, constants and helpers for heap runtime gate modules."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

# Ensure repository root is on sys.path for absolute imports.
repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from Tools.ai._shared import heap_source_anchors as source_anchors
from Tools.ai.heap_gate.provider_tool_scheduler import provider_patch_synthesis_plan
from Tools.ai.heap_gate.target_planner import RuntimeTargetPlanner, request_focus_text, tokenize
from Tools.ai.heap_gate.terminal_invariants import evaluate_terminal_invariants
from Tools.ai.heap_provider.budget_governor import (
    ProviderBudgetConfig,
    build_heap_provider_budget_governor,
    clamp_loop_iterations,
)
from Tools.ai.heap_provider.invocation_contract import build_heap_provider_invocation_contract
from Tools.ai.provider_mesh.runtime.python_runtime import command_env, resolve_child_python
from Tools.ai.provider_runtime_blackboard import (
    ProviderRuntimeHeap,
    record_lane_diagnostic,
    safe_dict,
    safe_int,
)
from Tools.ai.runtime_tool.file_refs import RuntimeFileRefResolver
from Tools.ai.runtime_universe import RepoRuntimeUniverseBuilder
from Tools.ai.runtime_universe.report import render_universe_markdown
from Tools.ai._shared.universo_utils import (
    make_state,
    now_iso,
    read_json,
    read_request_file,
    repo_rel,
)
from Tools.ai._shared.process_tree import terminate_process_tree
from Tools.validation._shared.report_utils import (
    resolve_output_path,
    write_json_report,
    write_text_report,
)

__all__ = [
    "Any",
    "BASE_REQUIREMENTS",
    "COMPLEX_REQUEST_HINTS",
    "DEFAULT_BRIDGE_DIR",
    "DEFAULT_BRIDGE_JSON",
    "DEFAULT_BRIDGE_MD",
    "DEFAULT_EVENTS",
    "DEFAULT_HEAP_MD",
    "DEFAULT_MARKDOWN",
    "DEFAULT_OUTPUT",
    "DEFAULT_SNAPSHOT",
    "HISTORICAL_TOOL_CONTEXT_FILES",
    "MEMORY_CONTEXT_RELOAD_REQUIREMENTS",
    "PLACEHOLDER_CODE_LABELS",
    "PLACEHOLDER_CODE_PATTERNS",
    "PROPOSAL_ITERATION_MAX_CHARS",
    "PROPOSAL_ITERATION_SUMMARY_CHARS",
    "PROVIDER_START_REQUIREMENTS",
    "PROVIDER_REQUIREMENTS",
    "ProviderBudgetConfig",
    "ProviderRuntimeHeap",
    "REQUIREMENT_ORDER",
    "RepoRuntimeUniverseBuilder",
    "RuntimeFileRefResolver",
    "RuntimeTargetPlanner",
    "SequenceMatcher",
    "argparse",
    "append_unique",
    "build_heap_provider_budget_governor",
    "build_heap_provider_invocation_contract",
    "clamp_loop_iterations",
    "command_env",
    "datetime",
    "evaluate_terminal_invariants",
    "event_payloads_by_type",
    "hashlib",
    "json",
    "make_state",
    "now_iso",
    "os",
    "provider_heap_lane",
    "provider_patch_synthesis_plan",
    "re",
    "read_json",
    "read_request_file",
    "record_lane_diagnostic",
    "render_universe_markdown",
    "repo_rel",
    "request_focus_text",
    "resolve_child_python",
    "resolve_output_path",
    "runtime_state_lane_gate",
    "safe_dict",
    "safe_int",
    "source_anchors",
    "subprocess",
    "terminate_process_tree",
    "tokenize",
    "write_json_report",
    "write_text_report",
]

DEFAULT_OUTPUT = "output/validation/heap_runtime_completeness_gate_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/heap_runtime_completeness_gate_{stamp}.md"
DEFAULT_EVENTS = "output/heap_runtime_completeness_gate/{stamp}/events.jsonl"
DEFAULT_SNAPSHOT = "output/heap_runtime_completeness_gate/{stamp}/state.json"
DEFAULT_HEAP_MD = "output/heap_runtime_completeness_gate/{stamp}/state.md"
DEFAULT_BRIDGE_DIR = "output/heap_runtime_completeness_gate/{stamp}/broker_bridge"
DEFAULT_BRIDGE_JSON = "output/validation/heap_runtime_completeness_gate_broker_bridge_{stamp}.json"
DEFAULT_BRIDGE_MD = "output/validation/heap_runtime_completeness_gate_broker_bridge_{stamp}.md"

REQUIREMENT_ORDER = (
    "tool_catalog",
    "shared_memory",
    "persistent_memory_status",
    "persistent_memory_search",
    "operational_memory_write",
    "operational_memory_search",
    "shared_context_chunks",
    "semantic_code_chunks",
    "ai_context_pack",
    "semantic_evidence_chunks",
    "runtime_file_refs",
    "validation_evidence",
    "gpu0_provider_peer",
    "npu_micro_task_auditor",
    "gpu1_provider_planner",
)

BASE_REQUIREMENTS = (
    "tool_catalog",
    "shared_memory",
    "persistent_memory_status",
    "persistent_memory_search",
    "operational_memory_write",
    "operational_memory_search",
    "shared_context_chunks",
    "semantic_code_chunks",
    "ai_context_pack",
    "semantic_evidence_chunks",
    "runtime_file_refs",
    "validation_evidence",
)

PROVIDER_START_REQUIREMENTS = (
    "operational_memory_write",
    "semantic_code_chunks",
    "runtime_file_refs",
)

PROVIDER_REQUIREMENTS = (
    "gpu1_provider_planner",
    "gpu0_provider_peer",
    "npu_micro_task_auditor",
)

HISTORICAL_TOOL_CONTEXT_FILES = (
    "docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/project-tool-registry.md",
    "docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md",
    "docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md",
    "tools/ai/README.md",
    "tools/workflow/README.md",
)

COMPLEX_REQUEST_HINTS = (
    "analizza",
    "analysis",
    "audit",
    "compless",
    "concreto",
    "contesto",
    "context",
    "dettagli",
    "evidence",
    "file",
    "heap",
    "igiene",
    "implement",
    "iter",
    "memoria",
    "output",
    "repo",
    "runtime",
    "sql",
    "stato",
    "tool",
    "universo",
    "verifica",
)

MEMORY_CONTEXT_RELOAD_REQUIREMENTS = {
    "tool_catalog": "tool_catalog_reload",
    "shared_memory": "shared_memory_reload",
    "persistent_memory_status": "persistent_memory_status_reload",
    "persistent_memory_search": "persistent_memory_reload",
    "operational_memory_write": "operational_memory_write",
    "operational_memory_search": "operational_memory_reload",
    "shared_context_chunks": "shared_context_reload",
    "semantic_code_chunks": "semantic_code_reload",
    "ai_context_pack": "context_pack_reload",
    "semantic_evidence_chunks": "semantic_evidence_reload",
    "runtime_file_refs": "runtime_file_refs_reload",
    "virtual_dev_environment": "virtual_dev_environment_reload",
    "code_execution_matrix": "code_execution_matrix_reload",
    "runtime_debug_lab_execution": "runtime_debug_lab_reload",
}
PROPOSAL_ITERATION_MAX_CHARS = 12000
PROPOSAL_ITERATION_SUMMARY_CHARS = 1200
PLACEHOLDER_CODE_PATTERNS = (
    r"(?m)^\s*pass\s*(?:#.*)?$",
    r"(?is)def\s+[A-Za-z_][A-Za-z0-9_]*\([^)]*\):\s*(?:#[^\n]*\n\s*)*pass\b",
    r"(?i)\bTODO\b|\bFIXME\b|\bplaceholder\b|implement here|da implementare",
    r"(?i)#\s*(aggiornamento della politica|generazione (?:del|di) report|esecuzione delle (?:operazioni|attività)|implementazione della politica)",
)
PLACEHOLDER_CODE_LABELS = (
    "bare_pass",
    "comment_only_function_stub",
    "todo_or_placeholder_marker",
    "italian_comment_only_stub",
)


# now_iso moved to universo_utils


# repo_rel moved to universo_utils


def append_unique(bucket: list[dict[str, Any]], item: dict[str, Any], key: str = "id") -> bool:
    value = item.get(key)
    if value and any(existing.get(key) == value for existing in bucket):
        return False
    bucket.append(item)
    return True


def event_payloads_by_type(events: list[dict[str, Any]], event_type: str) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for event in events:
        if event.get("event_type") != event_type:
            continue
        payload = safe_dict(event.get("payload"))
        if payload:
            payloads.append(payload)
    return payloads


PROVIDER_ROLE_TO_HEAP_LANE = {
    "gpu1_planner": "gpu1",
    "gpu1_primary_advisory": "gpu1",
    "gpu0_peer": "gpu0",
    "gpu0_diagnostic_peer": "gpu0",
    "npu_micro_task": "npu",
    "npu_micro_task_auditor": "npu",
}


def provider_heap_lane(value: str) -> str:
    """Map logical provider roles to physical heap lanes.

    provider_runtime_heap accepts physical lanes only: gpu1/gpu0/npu/broker/
    deterministic/telemetry/orchestrator. Logical roles stay in payloads and
    reports so the runtime can prove who contributed without inventing heap
    lanes.
    """
    lane = str(value or "").strip().lower()
    return PROVIDER_ROLE_TO_HEAP_LANE.get(lane, lane)


def runtime_state_lane_gate(lane_status: dict[str, Any], max_degraded_lanes: int) -> dict[str, Any]:
    """Evaluate lane viability for the heap runtime gate.

    ``max_degraded_lanes`` is kept for CLI/report compatibility, but degraded
    and failed lanes are always unviable in complete/full mode.
    """
    unviable = sorted(
        lane
        for lane, status in lane_status.items()
        if str(status).lower() in {"degraded", "failed", "unavailable"}
    )
    configured_tolerance = max(0, int(max_degraded_lanes))
    return {
        "passed": not unviable,
        "max_degraded_lanes": 0,
        "configured_max_degraded_lanes": configured_tolerance,
        "degraded_lanes": unviable,
        "unviable_lanes": unviable,
        "degraded_lane_count": len(unviable),
        "unviable_lane_count": len(unviable),
        "lane_status": dict(sorted((str(k), str(v)) for k, v in lane_status.items())),
    }
