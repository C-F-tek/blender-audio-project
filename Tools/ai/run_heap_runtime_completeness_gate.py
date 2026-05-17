#!/usr/bin/env python3
"""Budget-driven heap runtime completeness gate for IA-Carmine.

This is the canonical runtime completeness gate used by the real product
preflight. It validates the single execution universe, not isolated helper
scripts. It proves the control inversion expected by the project:

request -> shared heap -> role needs -> brokered tools -> shared memory/context
-> validation evidence -> critic claim -> arbiter decision -> product signal.

The loop is budget bounded. It exits with `ready` only after all required
readiness requirements are met, otherwise it exits with `blocked_with_reason` and
explicit missing requirements. It never applies patches, never writes source
files, never runs Blender/FFmpeg. It always traverses the provider teamwork
universe before product readiness: GPU1 planner, GPU0 peer workload and
NPU micro-task auditor all write evidence back into the same heap.
"""

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

# Ensure repository root is on sys.path for absolute imports
repo_root = Path(__file__).resolve().parents[2]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from tools.ai.universo_utils import (
    make_state,
    now_iso,
    read_json,
    read_request_file,
    repo_rel,
)

try:
    from tools.ai import heap_source_anchors as source_anchors
    from tools.ai.heap_provider_budget_governor import (
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
        clamp_loop_iterations,
    )
    from tools.ai.heap_provider_invocation_contract import (
        build_heap_provider_invocation_contract,
    )
    from tools.ai.provider_mesh_runtime.python_runtime import (
        command_env,
        resolve_child_python,
    )
    from tools.ai.provider_runtime_heap import (
        ProviderRuntimeHeap,
        record_lane_diagnostic,
        safe_dict,
        safe_int,
    )
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai import heap_source_anchors as source_anchors  # type: ignore
    from tools.ai.heap_provider_budget_governor import (  # type: ignore
        ProviderBudgetConfig,
        build_heap_provider_budget_governor,
        clamp_loop_iterations,
    )
    from tools.ai.heap_provider_invocation_contract import (
        build_heap_provider_invocation_contract,  # type: ignore
    )
    from tools.ai.provider_mesh_runtime.python_runtime import (  # type: ignore
        command_env,
        resolve_child_python,
    )
    from tools.ai.provider_runtime_heap import (  # type: ignore
        ProviderRuntimeHeap,
        record_lane_diagnostic,
        safe_dict,
        safe_int,
    )
    from tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

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
    "operational_memory_write",
    "operational_memory_search",
    "shared_context_chunks",
    "semantic_code_chunks",
    "ai_context_pack",
    "semantic_evidence_chunks",
    "validation_evidence",
    "gpu0_provider_peer",
    "npu_micro_task_auditor",
    "gpu1_provider_planner",
)

BASE_REQUIREMENTS = (
    "tool_catalog",
    "shared_memory",
    "operational_memory_write",
    "operational_memory_search",
    "shared_context_chunks",
    "semantic_code_chunks",
    "ai_context_pack",
    "semantic_evidence_chunks",
    "validation_evidence",
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
    "operational_memory_write": "operational_memory_write",
    "operational_memory_search": "operational_memory_reload",
    "shared_context_chunks": "shared_context_reload",
    "semantic_code_chunks": "semantic_code_reload",
    "ai_context_pack": "context_pack_reload",
    "semantic_evidence_chunks": "semantic_evidence_reload",
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
    "npu_critic": "npu",
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
    degraded = sorted(
        lane
        for lane, status in lane_status.items()
        if str(status).lower() in {"degraded", "failed"}
    )
    tolerance = max(0, int(max_degraded_lanes))
    return {
        "passed": len(degraded) <= tolerance,
        "max_degraded_lanes": tolerance,
        "degraded_lanes": degraded,
        "degraded_lane_count": len(degraded),
        "lane_status": dict(sorted((str(k), str(v)) for k, v in lane_status.items())),
    }


class HeapRuntimeCompletenessGate:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.repo_root = Path(args.repo_root).resolve()
        if getattr(args, "request_file", ""):
            args.request = read_request_file(self.repo_root, args.request_file)
        self.stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.output_dir = Path(args.output_dir).resolve() if args.output_dir else None
        self.heap = ProviderRuntimeHeap.from_args(
            self.repo_root,
            self.stamp,
            self.path_arg(args.events, DEFAULT_EVENTS),
            self.path_arg(args.snapshot, DEFAULT_SNAPSHOT),
            self.path_arg(args.heap_markdown, DEFAULT_HEAP_MD),
        )
        self.budget_config = ProviderBudgetConfig(
            objective=args.objective,
            budget_minutes=args.budget_minutes,
            max_rounds=args.max_rounds,
            files_per_round=args.files_per_round,
            max_context_files=args.max_context_files,
            max_chars_per_file=args.max_chars_per_file,
            max_new_tokens=args.max_new_tokens,
            keep_alive=args.keep_alive,
            npu_micro_start_mode=args.npu_micro_start_mode,
            npu_micro_timeout_seconds=args.npu_micro_timeout_seconds,
            npu_final_wait_seconds=args.npu_final_wait_seconds,
            npu_max_context_chars=args.npu_max_context_chars,
            npu_max_prompt_chars=args.npu_max_prompt_chars,
            npu_max_new_tokens=args.npu_max_new_tokens,
            allow_provider_generation=args.allow_provider_generation,
            operator_intent=args.operator_intent,
        )
        self.budget_governor = build_heap_provider_budget_governor(
            self.budget_config, requested_max_iterations=args.max_iterations
        )
        self.invocation_contract = build_heap_provider_invocation_contract(
            self.budget_governor,
            allow_provider_generation=args.allow_provider_generation,
            operator_intent=args.operator_intent,
        )
        self.max_iterations = clamp_loop_iterations(self.budget_config, args.max_iterations)
        self.state = make_state(args.objective, getattr(args, "request", ""))
        self.state["budget_governor"] = self.budget_governor
        self.state["invocation_contract"] = self.invocation_contract
        self.heap_read_count = 0
        self.heap_write_count = 0
        self.tool_request_count = 0
        self.tool_execution_count = 0
        self.decision_count = 0
        self.candidate_operation_count = 0
        self.bridge_reports: list[str] = []
        self.provider_reports: list[dict[str, Any]] = []
        self.provider_execution_performed = False
        self.provider_revision_count = 0
        self.provider_revision_feedback = ""
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def path_arg(self, explicit: str, default: str) -> str:
        # With --output-dir, parser defaults such as DEFAULT_OUTPUT/DEFAULT_MARKDOWN
        # are not operator-supplied explicit paths. They must resolve inside the
        # single run directory, otherwise the universe test writes the exit report
        # to the global default while the preflight/smoke reads the run_dir product.
        if explicit and not (self.output_dir and explicit == default):
            return explicit
        if not self.output_dir:
            return default
        mapping = {
            DEFAULT_EVENTS: "events.jsonl",
            DEFAULT_SNAPSHOT: "state.json",
            DEFAULT_HEAP_MD: "state.md",
            DEFAULT_BRIDGE_DIR: "broker_bridge",
            DEFAULT_BRIDGE_JSON: "broker_bridge.json",
            DEFAULT_BRIDGE_MD: "broker_bridge.md",
            DEFAULT_OUTPUT: "heap_runtime_completeness_gate_report.json",
            DEFAULT_MARKDOWN: "heap_runtime_completeness_gate_report.md",
        }
        filename = mapping.get(default)
        if not filename:
            return default
        return str(self.output_dir / filename)

    def child_python(self) -> str:
        """Return the project Python executable used for child tools.

        Policy: explicit --python-exe > repo .venv resolver. No system env/PATH
        fallback is introduced here.
        """
        explicit = str(getattr(self.args, "python_exe", "") or "").strip()
        if explicit:
            return str(Path(explicit).resolve())
        return resolve_child_python(self.repo_root)

    def runtime_context_dir(self) -> Path:
        if self.output_dir:
            path = self.output_dir / "team_context"
        else:
            path = (
                self.repo_root / "output" / "validation" / f"heap_runtime_team_context_{self.stamp}"
            )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def historical_tool_context_files(self) -> list[str]:
        """Return existing canonical/historical maps that help choose reusable tools."""
        refs: list[str] = []
        for rel_path in HISTORICAL_TOOL_CONTEXT_FILES:
            if (self.repo_root / rel_path).exists():
                refs.append(rel_path)
        return refs

    def detailed_output_expected(self) -> bool:
        request = self.request_text().strip()
        if not request:
            return False
        lowered = request.lower()
        word_count = len(
            [part for part in lowered.replace("?", " ").replace("!", " ").split() if part]
        )
        if word_count <= 3 and not any(hint in lowered for hint in COMPLEX_REQUEST_HINTS):
            return False
        return word_count >= 6 or any(hint in lowered for hint in COMPLEX_REQUEST_HINTS)

    def request_requires_existing_files(self) -> bool:
        lowered = self.request_text().lower()
        hints = (
            "file esistent",
            "file esistenti",
            "su file esistenti",
            "path repo reali",
            "repo reali",
            "repo-relative",
            "repo relative",
            "path reali",
            "source anchors",
            "sorgente reali",
            "target_files",
            "target files",
            "patch-plan",
            "patch plan",
            "proposal chunks concreti",
            "proposte concrete",
            "proposta concreta",
            "codice concreto",
        )
        return any(hint in lowered for hint in hints)

    def normalize_ref_path(self, rel_path: str) -> str:
        return source_anchors.normalize_ref_path(rel_path)

    def repo_file_exists(self, rel_path: str) -> bool:
        return source_anchors.repo_file_exists(self.repo_root, rel_path)

    def is_output_artifact_ref(self, rel_path: str) -> bool:
        return source_anchors.is_output_artifact_ref(rel_path)

    def is_source_candidate_ref(self, rel_path: str) -> bool:
        return source_anchors.is_source_candidate_ref(rel_path)

    def repo_source_file_exists(self, rel_path: str) -> bool:
        return source_anchors.repo_source_file_exists(self.repo_root, rel_path)

    def extracted_response_file_refs(self, text: str) -> list[str]:
        return source_anchors.extracted_file_refs(text)

    def proposal_declares_target_files(self, text: str) -> bool:
        return source_anchors.proposal_declares_target_files(text)

    def response_file_reference_quality(self, text: str) -> dict[str, Any]:
        return source_anchors.response_file_reference_quality(
            repo_root=self.repo_root,
            text=text,
            requires_existing=self.request_requires_existing_files(),
            implementation_required=self.implementation_output_required(),
        )

    def collect_source_candidates_from_json(self, data: Any, out: list[str]) -> None:
        source_anchors.collect_source_candidates_from_json(self.repo_root, data, out)

    def request_source_file_candidates(self, limit: int = 24) -> list[str]:
        """Return explicit existing source paths from operator/startup input first."""
        texts = [self.request_text()]
        startup_context = self.startup_task_file_context(max_preview_chars=20000)
        if startup_context.get("loaded"):
            texts.append(str(startup_context.get("preview") or ""))
        return source_anchors.request_source_file_candidates(self.repo_root, texts, limit=limit)

    def real_source_file_candidates(
        self, events: list[dict[str, Any]] | None = None, limit: int = 24
    ) -> list[str]:
        if events is None:
            events = self.read_events()
        texts = [self.request_text()]
        startup_context = self.startup_task_file_context(max_preview_chars=20000)
        if startup_context.get("loaded"):
            texts.append(str(startup_context.get("preview") or ""))
        return source_anchors.real_source_file_candidates(
            repo_root=self.repo_root,
            request_texts=texts,
            broker_output_refs=self.broker_output_refs(events),
            limit=limit,
        )

    def source_ref_alias_matches(self, rel_path: str, limit: int = 20) -> list[str]:
        return source_anchors.source_ref_alias_matches(self.repo_root, rel_path, limit=limit)

    def resolve_source_ref_alias(self, rel_path: str) -> str:
        return source_anchors.resolve_source_ref_alias(self.repo_root, rel_path)

    def source_allowlist_contract(
        self, events: list[dict[str, Any]] | None = None, limit: int = 32
    ) -> dict[str, Any]:
        """Return the strict source-path allowlist for GPU1 proposal targets."""
        candidates = self.real_source_file_candidates(events, limit=limit)
        return source_anchors.source_allowlist_contract(candidates)

    def render_source_allowlist_contract(
        self, events: list[dict[str, Any]] | None = None, limit: int = 32
    ) -> str:
        """Render a hard provider contract that prevents invented source paths."""
        candidates = self.real_source_file_candidates(events, limit=limit)
        return source_anchors.render_source_allowlist_contract(candidates)

    def source_anchor_feedback(
        self, events: list[dict[str, Any]], quality: dict[str, Any] | None = None
    ) -> str:
        candidates = self.real_source_file_candidates(events, limit=20)
        requested = []
        if isinstance(quality, dict):
            requested = list(
                quality.get("unverified_source_file_refs")
                or quality.get("unverified_file_refs")
                or []
            )
        return source_anchors.source_anchor_feedback(candidates, requested)

    def startup_task_file_path(self) -> Path | None:
        task_file = str(getattr(self.args, "task_file", "") or "").strip()
        if not task_file:
            return None
        task_file_path = Path(task_file)
        if not task_file_path.is_absolute():
            task_file_path = self.repo_root / task_file_path
        return task_file_path.resolve(strict=False)

    def startup_task_file_context(self, max_preview_chars: int = 12000) -> dict[str, Any]:
        """Read the startup task file as active heap input.

        The task file is not a diagnostic pointer: prepare_heap_context_memory_reload.py
        writes the current repo/docs/memory/tool context there before provider work.
        The gate must read it and publish a bounded fact/event so GPU1/GPU0/NPU
        operate over the same dynamic universe rather than only seeing a path.
        """
        task_file_path = self.startup_task_file_path()
        if task_file_path is None:
            return {
                "loaded": False,
                "task_file": "",
                "reason": "task_file argument missing",
            }
        rel_path = repo_rel(self.repo_root, task_file_path)
        if not task_file_path.is_file():
            return {
                "loaded": False,
                "task_file": rel_path,
                "reason": "task file missing",
            }
        try:
            task_file_text = task_file_path.read_text(encoding="utf-8-sig", errors="replace")
        except Exception as exc:  # noqa: BLE001 - context ingestion must not crash the gate.
            return {
                "loaded": False,
                "task_file": rel_path,
                "reason": f"task file unreadable: {type(exc).__name__}: {exc}",
            }
        digest = hashlib.sha256(task_file_text.encode("utf-8", errors="replace")).hexdigest()
        preview = task_file_text[: max(0, int(max_preview_chars))]
        return {
            "loaded": True,
            "task_file": rel_path,
            "sha256": digest,
            "char_count": len(task_file_text),
            "preview": preview,
            "preview_truncated": len(task_file_text) > len(preview),
            "source": "startup_task_file",
        }

    def publish_startup_task_file_context(self) -> None:
        context = self.startup_task_file_context()
        if not context.get("loaded"):
            if context.get("task_file"):
                self.warnings.append(str(context.get("reason") or "startup task file not loaded"))
            return
        fact = {
            "id": "startup_task_file_context_loaded",
            "kind": "startup_task_file_context",
            "source": "prepare_heap_context_memory_reload",
            "status": "available",
            "task_file": context.get("task_file"),
            "sha256": context.get("sha256"),
            "char_count": context.get("char_count"),
            "preview_truncated": context.get("preview_truncated"),
        }
        evidence = {
            "id": "shared_evidence_startup_task_file_context",
            "requirement": "shared_context_chunks",
            "kind": "startup_task_file_context",
            "source": "startup_task_file",
            "status": "available",
            "task_file": context.get("task_file"),
            "sha256": context.get("sha256"),
        }
        append_unique(self.state["facts"], fact)
        append_unique(self.state["shared_evidence"], evidence)
        self.publish(
            "context_memory",
            "fact",
            fact,
            target="gpu1",
            correlation_id=f"{self.stamp}:startup_task_file_context",
            round_id=0,
        )
        self.publish(
            "context_memory",
            "startup_task_file_context",
            context,
            target="gpu1",
            correlation_id=f"{self.stamp}:startup_task_file_content",
            round_id=0,
        )
        self.append_heap_exchange_event(
            {
                "kind": "startup_task_file_context",
                "lane": "context_memory",
                "phase": "startup_task_file_loaded",
                "task_file": context.get("task_file"),
                "sha256": context.get("sha256"),
                "char_count": context.get("char_count"),
                "preview": context.get("preview"),
                "preview_truncated": context.get("preview_truncated"),
                "summary": "startup task-file content loaded into heap before provider teamwork",
            }
        )

    def startup_manifest_from_task_file(self) -> tuple[Path | None, dict[str, Any]]:
        """Load the tool-owned startup manifest associated with --task-file.

        run_heap_runtime_context_closure.py already prepares repo/docs/memory/tool
        context before this gate starts and passes the ready task file with
        --task-file. The sibling manifest is the structured proof of that preload.
        Seeding passed startup requirements into the heap prevents the provider
        universe from being blocked by re-running already completed context tools.
        """
        task_path = self.startup_task_file_path()
        if task_path is None:
            return None, {}
        manifest_path = task_path.parent / "heap_context_memory_reload_manifest.json"
        payload = read_json(manifest_path)
        if not payload:
            return manifest_path, {}
        return manifest_path, payload

    def startup_execution_artifact_outputs(self, execution: dict[str, Any]) -> dict[str, Any]:
        refs: list[str] = []
        for key in (
            "useful_artifact_paths",
            "existing_artifact_paths",
            "artifact_paths",
        ):
            for value in execution.get(key) or []:
                if isinstance(value, str) and value and value not in refs:
                    refs.append(value)
        outputs: dict[str, Any] = {}
        json_refs = [ref for ref in refs if ref.lower().endswith(".json")]
        md_refs = [ref for ref in refs if ref.lower().endswith(".md")]
        if json_refs:
            outputs["json_report"] = json_refs[0]
        if md_refs:
            outputs["markdown_report"] = md_refs[0]
        if refs:
            outputs["artifact_refs"] = refs
        return outputs

    def startup_manifest_completed_requirements(
        self, manifest: dict[str, Any]
    ) -> list[dict[str, Any]]:
        completed: list[dict[str, Any]] = []
        for execution in manifest.get("tool_executions") or []:
            if not isinstance(execution, dict):
                continue
            requirement = str(execution.get("requirement") or "").strip()
            if requirement not in REQUIREMENT_ORDER:
                continue
            if execution.get("passed") is not True:
                continue
            if safe_int(execution.get("returncode"), default=1) != 0:
                continue
            errors = execution.get("errors") if isinstance(execution.get("errors"), list) else []
            if errors:
                continue
            completed.append(execution)
        return completed

    def startup_manifest_artifact_completed_requirements(
        self,
        manifest_path: Path | None,
        manifest: dict[str, Any],
        existing: set[str],
    ) -> list[dict[str, Any]]:
        """Derive completed startup requirements from manifest artifact refs.

        Some startup reload lanes are tool-owned aggregate outputs rather than
        one-to-one broker tool executions. If their JSON/Markdown artifacts are
        present and the startup contract marks them loaded, they are valid heap
        context inputs and should not block provider teamwork.
        """
        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
        contract = manifest.get("contract") if isinstance(manifest.get("contract"), dict) else {}

        artifact_requirements = {
            "semantic_code_chunks": (
                "semantic_code_chunks_loaded",
                ("semantic_code_chunks_json", "semantic_code_chunks_markdown"),
            ),
            "semantic_evidence_chunks": (
                "semantic_evidence_chunks_loaded",
                ("semantic_evidence_chunks_json", "semantic_evidence_chunks_markdown"),
            ),
        }

        completed: list[dict[str, Any]] = []
        for requirement, (contract_key, artifact_keys) in artifact_requirements.items():
            if requirement in existing:
                continue
            if contract.get(contract_key) is not True:
                continue

            refs: list[str] = []
            for key in artifact_keys:
                value = artifacts.get(key)
                if isinstance(value, str) and value.strip():
                    candidate = self.repo_root / value
                    if candidate.exists():
                        refs.append(value.replace("\\", "/"))

            if not refs:
                continue

            completed.append(
                {
                    "requirement": requirement,
                    "tool": "startup_context_memory_reload",
                    "returncode": 0,
                    "passed": True,
                    "artifact_paths": refs,
                    "useful_artifact_paths": refs,
                    "existing_artifact_paths": refs,
                    "summary": {
                        "passed": True,
                        "source": "startup_context_memory_reload_manifest_artifacts",
                        "startup_manifest": (
                            repo_rel(self.repo_root, manifest_path) if manifest_path else ""
                        ),
                    },
                    "provider_execution_performed": False,
                    "patch_application_performed": False,
                    "source_writes_performed": False,
                }
            )

        return completed

    def publish_startup_manifest_evidence(self) -> None:
        """Seed passed startup preload requirements as heap broker evidence.

        This keeps the architecture tool-owned: startup reload prepares context,
        memory and chunks before provider work; the heap consumes that manifest
        instead of treating the same requirements as missing just because a later
        duplicate broker attempt failed or was not needed.
        """
        manifest_path, manifest = self.startup_manifest_from_task_file()
        if not manifest:
            return
        existing = self.completed_requirements(self.heap.read_events())
        startup_completed = self.startup_manifest_completed_requirements(manifest)
        startup_completed.extend(
            self.startup_manifest_artifact_completed_requirements(
                manifest_path,
                manifest,
                existing,
            )
        )
        for execution in startup_completed:
            requirement = str(execution.get("requirement") or "").strip()
            if requirement in existing:
                continue
            outputs = self.startup_execution_artifact_outputs(execution)
            artifact_refs = list(outputs.get("artifact_refs") or [])
            payload = {
                "schema_version": 1,
                "kind": "startup_manifest_broker_result",
                "requirement": requirement,
                "tool": str(execution.get("tool") or "startup_context_memory_reload"),
                "returncode": 0,
                "executed": True,
                "blocked": False,
                "outputs": outputs,
                "summary": {
                    "passed": True,
                    "source": "startup_context_memory_reload_manifest",
                    "startup_manifest": (
                        repo_rel(self.repo_root, manifest_path) if manifest_path else ""
                    ),
                },
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
            }
            self.publish(
                "broker",
                "broker_result",
                payload,
                target="gpu1",
                correlation_id=f"{self.stamp}:startup_manifest:{requirement}",
                round_id=0,
            )
            self.append_reload_lifecycle_event(
                requirement=requirement,
                round_id=0,
                phase="startup_manifest_completed",
                tool=str(execution.get("tool") or "startup_context_memory_reload"),
                refs=artifact_refs,
            )
            existing.add(requirement)

    def publish_startup_memory_context_reload_events(self) -> None:
        # Expose startup reload lifecycle for memory/context/tool surfaces.
        # This mirrors the unified run behavior: before the heap starts consuming
        # provider output, it records that tool catalog, shared memory, operational
        # memory, request context, semantic chunks and context pack surfaces must
        # be refreshed for the current run.
        startup_requirements = (
            "tool_catalog",
            "shared_memory",
            "operational_memory_search",
            "shared_context_chunks",
            "semantic_code_chunks",
            "ai_context_pack",
            "semantic_evidence_chunks",
        )
        for requirement in startup_requirements:
            self.append_reload_lifecycle_event(
                requirement=requirement,
                round_id=0,
                phase="startup_requested",
                tool="heap_startup_reload",
                refs=[],
            )

    def append_reload_lifecycle_event(
        self,
        requirement: str,
        round_id: int,
        phase: str,
        tool: str = "",
        refs: list[str] | None = None,
    ) -> None:
        event_kind = MEMORY_CONTEXT_RELOAD_REQUIREMENTS.get(requirement)
        if not event_kind:
            return
        payload: dict[str, Any] = {
            "kind": "memory_context_reload",
            "lane": "context_memory",
            "phase": phase,
            "round": round_id,
            "requirement": requirement,
            "reload_event": event_kind,
            "tool": tool,
            "summary": f"{event_kind} {phase} for {requirement}",
        }
        if refs:
            payload["artifact_refs"] = refs[:12]
        self.append_heap_exchange_event(payload)

    def proposal_iteration_dir(self) -> Path:
        path = self.runtime_context_dir() / "proposal_iterations"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def heap_parallel_cycle_assessment(
        self,
        revision: int,
        source: str,
        deterministic_reviews: dict[str, Any],
        npu_audit: dict[str, Any],
    ) -> dict[str, Any]:
        gpu0_review = deterministic_reviews.get("gpu0_review")
        npu_piece = deterministic_reviews.get("npu_micro_task_piece")
        provider_report_lanes: list[str] = []
        for report in self.provider_reports:
            lane = str(report.get("lane") or report.get("role") or report.get("kind") or "")
            if lane and lane not in provider_report_lanes:
                provider_report_lanes.append(lane)

        gpu1_present = str(source or "").lower().startswith("gpu1")
        gpu0_present = bool(gpu0_review) or any(
            "gpu0" in lane.lower() for lane in provider_report_lanes
        )
        npu_present = (
            bool(npu_piece)
            or bool(npu_audit)
            or any("npu" in lane.lower() for lane in provider_report_lanes)
        )
        npu_workload_ok = not npu_audit or bool(
            npu_audit.get("passed") and npu_audit.get("performed")
        )

        missing: list[str] = []
        if not gpu1_present:
            missing.append("gpu1_provider_planner")
        if not gpu0_present:
            missing.append("gpu0_companion_review")
        if not npu_present:
            missing.append("npu_micro_task_audit")
        if npu_present and not npu_workload_ok:
            missing.append("npu_workload_passed")

        return {
            "schema_version": 1,
            "kind": "heap_parallel_cycle_assessment",
            "stamp": self.stamp,
            "revision": revision,
            "passed": not missing,
            "policy": "Proposal acceptance requires same-heap GPU1 proposal, GPU0 review/refine and NPU audit.",
            "gpu1_present": gpu1_present,
            "gpu0_present": gpu0_present,
            "npu_present": npu_present,
            "npu_workload_ok": npu_workload_ok,
            "provider_report_lanes": provider_report_lanes,
            "missing_lanes": missing,
            "provider_execution_performed": bool(self.provider_execution_performed),
            "patch_application_performed": False,
            "source_writes_performed": False,
        }

    def write_heap_parallel_cycle_artifact(
        self, revision: int, assessment: dict[str, Any]
    ) -> dict[str, str]:
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_parallel_cycle_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        write_json_report(assessment, json_path)
        md_lines = [
            "# Heap Parallel Cycle Assessment",
            "",
            f"- Revision: `{revision}`",
            f"- Passed: `{assessment.get('passed')}`",
            f"- GPU1 present: `{assessment.get('gpu1_present')}`",
            f"- GPU0 present: `{assessment.get('gpu0_present')}`",
            f"- NPU present: `{assessment.get('npu_present')}`",
            f"- NPU workload ok: `{assessment.get('npu_workload_ok')}`",
            "",
            "## Missing lanes",
            "",
            *[f"- `{item}`" for item in assessment.get("missing_lanes", [])],
            "",
            "## Provider report lanes",
            "",
            *[f"- `{item}`" for item in assessment.get("provider_report_lanes", [])],
            "",
        ]
        write_text_report("\n".join(md_lines), md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "heap_parallel_cycle_assessment",
                "lane": "arbiter",
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "passed": bool(assessment.get("passed")),
                "summary": "same-heap multi-lane participation assessed before proposal acceptance",
            }
        )
        return refs

    def cross_lane_proposal_veto(
        self,
        response_text: str,
        implementation_quality: dict[str, Any],
        proposal_progress: dict[str, Any],
        deterministic_reviews: dict[str, Any],
        npu_audit: dict[str, Any],
        parallel_cycle: dict[str, Any],
        revision: int,
    ) -> dict[str, Any]:
        reasons: list[str] = []
        gpu0_review = deterministic_reviews.get("gpu0_review")
        npu_piece = deterministic_reviews.get("npu_micro_task_piece")
        placeholder_hits = (
            implementation_quality.get("placeholder_hits")
            if isinstance(implementation_quality, dict)
            else []
        )
        impl_errors = (
            implementation_quality.get("errors") if isinstance(implementation_quality, dict) else []
        )
        progress_errors = (
            proposal_progress.get("errors") if isinstance(proposal_progress, dict) else []
        )

        combined_gpu0 = "\n".join(str(item) for item in (gpu0_review or []))
        combined_npu = "\n".join(str(item) for item in (npu_piece or []))
        combined_response = str(response_text or "")

        if placeholder_hits:
            reasons.append(f"implementation_quality.placeholder_hits={placeholder_hits}")
        if impl_errors:
            reasons.append(f"implementation_quality.errors={impl_errors}")
        if progress_errors:
            reasons.append(f"proposal_progress.errors={progress_errors}")
        if parallel_cycle.get("passed") is not True:
            reasons.append(f"parallel_cycle_missing_lanes={parallel_cycle.get('missing_lanes')}")
        if re.search(
            r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b",
            combined_gpu0,
            re.IGNORECASE,
        ):
            reasons.append("GPU0 review contains placeholder/stub/TODO signal")
        if re.search(
            r"reject|reject_until|rifiut|non soddisfacente|non accett",
            combined_gpu0,
            re.IGNORECASE,
        ):
            reasons.append("GPU0 review contains reject signal")
        if re.search(
            r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b",
            combined_npu,
            re.IGNORECASE,
        ):
            reasons.append("NPU micro-task contains placeholder/stub/TODO signal")
        if re.search(
            r"reject|reject_until|rifiut|non soddisfacente|non accett",
            combined_npu,
            re.IGNORECASE,
        ):
            reasons.append("NPU micro-task contains reject signal")
        if re.search(
            r"\bTODO\b|\bFIXME\b|placeholder|stub|da implementare",
            combined_response,
            re.IGNORECASE,
        ):
            reasons.append("response_text contains TODO/FIXME/placeholder/stub marker")
        if npu_audit and npu_audit.get("requested") and not npu_audit.get("performed"):
            reasons.append("NPU workload requested but not performed")

        reasons = list(dict.fromkeys(str(item) for item in reasons if str(item).strip()))
        vetoed = bool(reasons)
        refinement_prompt = ""
        if vetoed:
            source_candidates = self.real_source_file_candidates(self.read_events(), limit=24)
            refinement_lines = [
                "HEAP REFINEMENT TASK FROM SAME-HEAP CROSS-LANE VETO",
                f"Rejected revision: {revision}",
                "The previous proposal is not accepted inside the heap universe.",
                "",
                "Output/context policy:",
                "- output may exceed a single model context;",
                "- persist long material as proposal/refinement artifacts;",
                "- pass only compact summaries and artifact paths to the next revision;",
                "- never require GPU1 to hold the whole final product in one context window.",
                "",
                "Rejection reasons:",
                *[f"- {reason}" for reason in reasons],
                "",
                "Next provider revision must:",
                "- return concrete patch-plan JSON or explicit reject_with_reason;",
                "- include repo-relative target_files with exact existing paths;",
                "- include concrete operations or patch-spec fragments, not prose-only status;",
                "- avoid TODO/FIXME/pass/stub/placeholder markers;",
                "- consume GPU0 review, NPU audit and heap_parallel_cycle artifact as hard constraints;",
                "- keep patch_application_performed=false and source_writes_performed=false.",
                "",
                "Allowed source anchors:",
                *[f"- {item}" for item in source_candidates[:24]],
            ]
            refinement_prompt = "\n".join(refinement_lines)
        return {
            "vetoed": vetoed,
            "reasons": reasons,
            "gpu0_review": gpu0_review or [],
            "npu_micro_task_piece": npu_piece or [],
            "npu_workload_audit": npu_audit or {},
            "parallel_cycle": parallel_cycle,
            "refinement_prompt": refinement_prompt,
        }

    def write_heap_refinement_task_artifact(
        self, revision: int, veto: dict[str, Any]
    ) -> dict[str, str]:
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_refinement_task_after_revision_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        payload = {
            "schema_version": 1,
            "kind": "heap_refinement_task",
            "stamp": self.stamp,
            "after_revision": revision,
            "vetoed": bool(veto.get("vetoed")),
            "reasons": veto.get("reasons", []),
            "parallel_cycle": veto.get("parallel_cycle", {}),
            "refinement_prompt": veto.get("refinement_prompt", ""),
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        }
        write_json_report(payload, json_path)
        md_lines = [
            "# Heap Refinement Task",
            "",
            f"- After revision: `{revision}`",
            f"- Vetoed: `{bool(veto.get('vetoed'))}`",
            "",
            "## Reasons",
            "",
            *[f"- {item}" for item in veto.get("reasons", [])],
            "",
            "## Refinement prompt",
            "",
            "```text",
            str(veto.get("refinement_prompt") or ""),
            "```",
            "",
        ]
        write_text_report("\n".join(md_lines), md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "heap_refinement_task",
                "lane": "arbiter",
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "summary": "cross-lane veto converted into next provider refinement task",
            }
        )
        return refs

    def write_proposal_iteration_artifact(
        self,
        revision: int,
        response_text: str,
        quality: dict[str, Any],
        events: list[dict[str, Any]],
        source: str = "gpu1",
    ) -> dict[str, str]:
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_proposal_revision_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        previous = self.latest_proposal_iteration_block(max_chars=PROPOSAL_ITERATION_SUMMARY_CHARS)
        anchored_sources = self.real_source_file_candidates(events, limit=20)
        deterministic_reviews = self.deterministic_lane_reviews(response_text, quality, events)
        implementation_quality = (
            deterministic_reviews.get("implementation_quality")
            if isinstance(deterministic_reviews.get("implementation_quality"), dict)
            else {}
        )
        proposal_progress = self.proposal_revision_progress_report(response_text, quality)
        npu_audit = self.npu_workload_audit_report()
        parallel_cycle = self.heap_parallel_cycle_assessment(
            revision=revision,
            source=source,
            deterministic_reviews=deterministic_reviews,
            npu_audit=npu_audit,
        )
        self.write_heap_parallel_cycle_artifact(revision, parallel_cycle)
        cross_lane_veto = self.cross_lane_proposal_veto(
            response_text=response_text,
            implementation_quality=implementation_quality,
            proposal_progress=proposal_progress,
            deterministic_reviews=deterministic_reviews,
            npu_audit=npu_audit,
            parallel_cycle=parallel_cycle,
            revision=revision,
        )
        if cross_lane_veto.get("vetoed"):
            self.provider_revision_feedback = str(cross_lane_veto.get("refinement_prompt") or "")
            self.write_heap_refinement_task_artifact(revision, cross_lane_veto)
        quality_passed = bool(
            quality.get("passed")
            and implementation_quality.get("passed")
            and proposal_progress.get("passed")
            and parallel_cycle.get("passed")
            and not cross_lane_veto.get("vetoed")
        )
        clipped = (response_text or "")[:PROPOSAL_ITERATION_MAX_CHARS]
        data = {
            "schema_version": 1,
            "kind": "heap_proposal_iteration",
            "stamp": self.stamp,
            "revision": revision,
            "source": source,
            "quality_passed": quality_passed,
            "response_file_reference_quality": quality,
            "implementation_quality": implementation_quality,
            "proposal_progress": proposal_progress,
            "gpu0_review": deterministic_reviews.get("gpu0_review"),
            "npu_micro_task_piece": deterministic_reviews.get("npu_micro_task_piece"),
            "npu_workload_audit": npu_audit,
            "parallel_cycle": parallel_cycle,
            "cross_lane_veto": cross_lane_veto,
            "accepted": quality_passed,
            "reject_reason": "; ".join(cross_lane_veto.get("reasons", [])),
            "anchored_source_candidates": anchored_sources,
            "previous_iteration_available": bool(previous),
            "response_text": clipped,
        }
        write_json_report(data, json_path)
        md = [
            "# Heap Proposal Iteration",
            "",
            f"- Revision: `{revision}`",
            f"- Source: `{source}`",
            f"- Quality passed: `{quality_passed}`",
            "",
            "## Deterministic lane reviews",
            "",
            "### GPU0 review",
            "",
            *[f"- {item}" for item in deterministic_reviews.get("gpu0_review", [])],
            "",
            "### NPU micro-task piece",
            "",
            *[f"- {item}" for item in deterministic_reviews.get("npu_micro_task_piece", [])],
            "",
            "### Implementation quality",
            "",
            f"- Passed: `{implementation_quality.get('passed')}`",
            f"- Errors: `{implementation_quality.get('errors')}`",
            "",
            "### Proposal progress",
            "",
            f"- Passed: `{proposal_progress.get('passed')}`",
            f"- Similarity: `{proposal_progress.get('similarity')}`",
            f"- Errors: `{proposal_progress.get('errors')}`",
            "",
            "### NPU workload audit",
            "",
            f"- Requested: `{npu_audit.get('requested')}`",
            f"- Performed: `{npu_audit.get('performed')}`",
            f"- Passed: `{npu_audit.get('passed')}`",
            f"- Iterations: `{npu_audit.get('iterations')}`",
            f"- Seconds: `{npu_audit.get('seconds')}`",
            f"- Python: `{npu_audit.get('python_exe')}`",
            "",
            "### Heap parallel cycle",
            "",
            f"- Passed: `{parallel_cycle.get('passed')}`",
            f"- Missing lanes: `{parallel_cycle.get('missing_lanes')}`",
            "",
            "### Cross-lane veto",
            "",
            f"- Vetoed: `{cross_lane_veto.get('vetoed')}`",
            f"- Reasons: `{cross_lane_veto.get('reasons')}`",
            "",
            "## Anchored source candidates",
            "",
            *[f"- `{item}`" for item in anchored_sources[:20]],
            "",
            "## Proposal chunk",
            "",
            clipped,
            "",
        ]
        write_text_report("\n".join(md), md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "proposal_iteration",
                "lane": source,
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "quality_passed": quality_passed,
                "proposal_progress_passed": bool(proposal_progress.get("passed")),
                "npu_workload_performed": bool(npu_audit.get("performed")),
                "summary": f"provider proposal revision {revision} persisted as reusable heap chunk",
            }
        )
        return refs

    def proposal_iteration_artifacts(self) -> list[str]:
        out_dir = self.proposal_iteration_dir()
        refs: list[str] = []
        for path in sorted(out_dir.glob("heap_proposal_revision_*.json")):
            refs.append(repo_rel(self.repo_root, path))
            md = path.with_suffix(".md")
            if md.exists():
                refs.append(repo_rel(self.repo_root, md))
        return refs

    def latest_proposal_iteration_block(self, max_chars: int = 4000) -> str:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.md"))
        if not candidates:
            return ""
        text = candidates[-1].read_text(encoding="utf-8", errors="replace")
        if len(text) <= max_chars:
            return text
        return text[-max_chars:]

    def latest_proposal_iteration_report(self) -> dict[str, Any]:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.json"))
        if not candidates:
            return {}
        return read_json(candidates[-1])

    def latest_proposal_quality_passed(self) -> bool:
        report = self.latest_proposal_iteration_report()
        if not report:
            return False
        return report.get("quality_passed") is True

    def latest_quality_proposal_iteration_block(self, max_chars: int = 4000) -> str:
        out_dir = self.proposal_iteration_dir()
        for json_path in reversed(sorted(out_dir.glob("heap_proposal_revision_*.json"))):
            report = read_json(json_path)
            if report.get("quality_passed") is not True:
                continue
            md_path = json_path.with_suffix(".md")
            if not md_path.exists():
                continue
            text = md_path.read_text(encoding="utf-8", errors="replace")
            if len(text) <= max_chars:
                return text
            return text[-max_chars:]
        return ""

    def normalized_proposal_text(self, value: str) -> str:
        normalized = re.sub(r"\s+", " ", str(value or "").strip().lower())
        normalized = re.sub(r"revision\s*[:` ]+\d+", "revision", normalized)
        return normalized

    def proposal_revision_progress_report(
        self, response_text: str, quality: dict[str, Any]
    ) -> dict[str, Any]:
        previous = self.latest_proposal_iteration_report()
        if not previous:
            return {
                "required": False,
                "passed": True,
                "reason": "first proposal iteration",
                "similarity": 0.0,
                "repeated_unverified_source_refs": [],
            }
        previous_text = str(previous.get("response_text") or "")
        current_norm = self.normalized_proposal_text(response_text)
        previous_norm = self.normalized_proposal_text(previous_text)
        similarity = (
            SequenceMatcher(None, previous_norm[:8000], current_norm[:8000]).ratio()
            if previous_norm and current_norm
            else 0.0
        )
        previous_quality = (
            previous.get("response_file_reference_quality")
            if isinstance(previous.get("response_file_reference_quality"), dict)
            else {}
        )
        previous_unverified = {
            str(item)
            for item in previous_quality.get("unverified_source_file_refs")
            or previous_quality.get("unverified_file_refs")
            or []
        }
        current_unverified = {
            str(item)
            for item in quality.get("unverified_source_file_refs")
            or quality.get("unverified_file_refs")
            or []
        }
        repeated_unverified = sorted(previous_unverified.intersection(current_unverified))
        errors: list[str] = []
        if similarity >= 0.94:
            errors.append(
                f"proposal revision too similar to previous iteration: similarity={similarity:.3f}"
            )
        if repeated_unverified:
            errors.append(f"proposal repeated unresolved source refs: {repeated_unverified}")
        return {
            "required": True,
            "passed": not errors,
            "reason": "proposal must improve previous heap chunk",
            "similarity": round(similarity, 4),
            "repeated_unverified_source_refs": repeated_unverified,
            "errors": errors,
        }

    def npu_workload_audit_report(self) -> dict[str, Any]:
        for report in reversed(self.provider_reports):
            if report.get("lane") != "npu_micro_task_auditor":
                continue
            output = str(report.get("output") or "")
            data = read_json(self.repo_root / output)
            workload = (
                data.get("npu_device_workload")
                if isinstance(data.get("npu_device_workload"), dict)
                else {}
            )
            if workload:
                return {
                    "source_file": output,
                    "requested": bool(workload.get("requested")),
                    "performed": bool(workload.get("performed")),
                    "passed": bool(workload.get("passed")),
                    "mode": workload.get("mode"),
                    "iterations": safe_int(workload.get("iterations")),
                    "seconds": workload.get("seconds"),
                    "python_exe": workload.get("python_exe"),
                    "errors": (
                        workload.get("errors") if isinstance(workload.get("errors"), list) else []
                    ),
                    "warnings": (
                        workload.get("warnings")
                        if isinstance(workload.get("warnings"), list)
                        else []
                    ),
                }
            return {
                "source_file": output,
                "requested": bool(data.get("npu_device_workload_requested")),
                "performed": bool(data.get("npu_device_workload_performed")),
                "passed": False,
                "mode": "npu_workload_report_missing",
                "iterations": 0,
                "seconds": 0.0,
                "errors": [],
                "warnings": [],
            }
        return {
            "requested": False,
            "performed": False,
            "passed": False,
            "mode": "npu_report_unavailable",
            "iterations": 0,
            "seconds": 0.0,
            "errors": [],
            "warnings": ["NPU provider report unavailable"],
        }

    def proposal_iteration_digest(self, max_blocks: int = 4, max_chars: int = 12000) -> str:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.md"))[-max_blocks:]
        if not candidates:
            return ""
        blocks: list[str] = []
        remaining = max_chars
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            if not text:
                continue
            block = f"## {path.name}\n\n{text}"
            if len(block) > remaining:
                block = block[-remaining:]
            blocks.append(block)
            remaining -= len(block)
            if remaining <= 0:
                break
        return "\n\n---\n\n".join(blocks)

    def implementation_output_required(self) -> bool:
        lowered = self.request_text().lower()
        hints = (
            "implement",
            "codice",
            "patch",
            "patch-plan",
            "patch plan",
            "proposal chunks concreti",
            "proposte concrete",
            "proposta concreta",
            "target_files",
            "target files",
            "path repo reali",
            "repo-relative",
            "blocca placeholder",
            "blocca stub",
            "senza placeholder",
            "senza stub",
            "refiner",
            "refinement",
        )
        return any(hint in lowered for hint in hints)

    def implementation_quality_report(
        self, text: str, events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        file_quality = self.response_file_reference_quality(text)
        lowered = (text or "").lower()
        existing_sources = (
            file_quality.get("existing_source_file_refs") if isinstance(file_quality, dict) else []
        )
        source_count = len(existing_sources or [])
        code_block_count = len(re.findall(r"```", text or "")) / 2
        operation_markers = [
            "target_file",
            "target_files",
            "unified_diff",
            "diff --git",
            "replace_once",
            "insert_after_once",
            "insert_before_once",
            "write_file",
            "def ",
            "class ",
            "python -m py_compile",
            "pytest",
            "git diff --check",
            "validazione",
            "validation",
        ]
        concrete_operation_markers = [marker for marker in operation_markers if marker in lowered]
        generic_markers = [
            "potresti",
            "si potrebbe",
            "considerare",
            "dovrebbe",
            "migliorare la manutenibil",
            "ottimizzare la gestione",
            "assicurarsi che",
            "aggiungere ulteriori test",
            "migliorare la sincronizzazione",
        ]
        generic_marker_hits = [marker for marker in generic_markers if marker in lowered]
        placeholder_hits = [
            label
            for label, pattern in zip(PLACEHOLDER_CODE_LABELS, PLACEHOLDER_CODE_PATTERNS)
            if re.search(pattern, text or "")
        ]
        has_actionable_structure = bool(code_block_count or concrete_operation_markers)
        required = self.implementation_output_required()
        errors: list[str] = []
        if required and source_count <= 0:
            errors.append("no verified source file references")
        invented_source_path_refs = list(file_quality.get("unverified_source_file_refs") or [])
        if required and invented_source_path_refs:
            errors.append(f"unverified source file refs: {invented_source_path_refs}")
            errors.append(f"invented/non-allowlisted source path refs: {invented_source_path_refs}")
        if required and file_quality.get("ambiguous_source_file_refs"):
            errors.append(
                f"ambiguous source file refs: {sorted(file_quality.get('ambiguous_source_file_refs', {}).keys())}"
            )
        if required and not file_quality.get("passed"):
            errors.append("source file reference quality failed")
        if required and not has_actionable_structure:
            errors.append("no code/diff/operation/validation markers")
        if required and placeholder_hits:
            errors.append(f"placeholder/stub code detected: {placeholder_hits}")
        if (
            required
            and generic_marker_hits
            and (not code_block_count or placeholder_hits)
            and len(concrete_operation_markers) < 3
        ):
            errors.append("generic advisory wording without enough implementation detail")
        passed = (not required) or (source_count > 0 and has_actionable_structure and not errors)
        return {
            "required": required,
            "passed": passed,
            "source_count": source_count,
            "code_block_count": code_block_count,
            "concrete_operation_markers": concrete_operation_markers,
            "generic_marker_hits": generic_marker_hits,
            "placeholder_hits": placeholder_hits,
            "invented_source_path_refs": invented_source_path_refs if required else [],
            "errors": errors,
        }

    def deterministic_lane_reviews(
        self, response_text: str, quality: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        implementation_quality = self.implementation_quality_report(response_text, events)
        file_quality = self.response_file_reference_quality(response_text)
        gpu0_notes: list[str] = []
        if not implementation_quality.get("passed") and implementation_quality.get("required"):
            gpu0_notes.append(
                "GPU0 deterministic review: proposta non soddisfacente; manca implementazione concreta/codice/operazioni validabili."
            )
        if file_quality.get("unverified_source_file_refs"):
            gpu0_notes.append(
                f"GPU0 deterministic review: source refs non verificati={file_quality.get('unverified_source_file_refs')}."
            )
            gpu0_notes.append(
                "GPU0 deterministic review: invented_source_path veto; TARGET_FILES must come from source allowlist only."
            )
        if file_quality.get("ambiguous_source_file_refs"):
            gpu0_notes.append(
                f"GPU0 deterministic review: source refs ambigui={sorted(file_quality.get('ambiguous_source_file_refs', {}).keys())}."
            )
        if implementation_quality.get("placeholder_hits"):
            gpu0_notes.append(
                f"GPU0 deterministic review: placeholder/stub code rilevati={implementation_quality.get('placeholder_hits')}."
            )
        if not gpu0_notes:
            gpu0_notes.append(
                "GPU0 deterministic review: proposta usabile come blocco, soggetta a validazione finale."
            )
        npu_audit = self.npu_workload_audit_report()
        npu_notes = [
            "NPU micro-task piece: audit guardrail; verificare che il blocco non dichiari patch applicate, source write o provider execution NPU se non presenti.",
            f"NPU micro-task piece: implementation_quality_passed={implementation_quality.get('passed')}, file_quality_passed={file_quality.get('passed')}.",
            f"NPU micro-task piece: workload_requested={npu_audit.get('requested')}, workload_performed={npu_audit.get('performed')}, workload_passed={npu_audit.get('passed')}, iterations={npu_audit.get('iterations')}, seconds={npu_audit.get('seconds')}.",
        ]
        if (
            implementation_quality.get("placeholder_hits")
            or file_quality.get("unverified_source_file_refs")
            or file_quality.get("ambiguous_source_file_refs")
        ):
            if file_quality.get("unverified_source_file_refs"):
                npu_notes.append(
                    "NPU micro-task piece: veto=invented_source_path_or_non_allowlisted_target."
                )
            npu_notes.append(
                "NPU micro-task piece: decision=reject_until_concrete_code_and_full_repo_relative_paths."
            )
        return {
            "gpu0_review": gpu0_notes,
            "npu_micro_task_piece": npu_notes,
            "implementation_quality": implementation_quality,
        }

    def proposal_iteration_feedback(
        self, events: list[dict[str, Any]], quality: dict[str, Any] | None = None
    ) -> str:
        latest = self.latest_proposal_iteration_block(max_chars=3500)
        anchor = self.source_anchor_feedback(events, quality)
        parts = [
            "HEAP PROPOSAL ITERATION MODE:",
            "NPU PIECE LANE REQUIRED: when provider generation/peer revision is permitted, NPU must contribute audit pieces, guardrail deltas, source anchors, or negative findings into the heap exchange instead of remaining only a device-visibility note.",
            "GPU0 REVIEW REQUIRED: if the previous proposal is generic, lacks code, lacks target paths, or only says what should be done, mark it as non soddisfacente and rewrite it as an operational block.",
            "The next revision must refine the previous proposal chunk and make it more operational.",
            "Do not restart from scratch. Preserve useful decisions, add verified repo-relative paths, signatures, commands, concrete implementation steps, validation commands and patch-level code.",
            "Use this exact structure in the next proposal: TARGET_FILES, PROBLEM, IMPLEMENTATION_CHANGES, CODE_OR_PATCH_SKETCH, VALIDATION_COMMANDS, RISKS, EXIT_DECISION.",
            "The final answer is assembled from proposal_iteration artifacts at heap exit, not only from raw GPU1 context.",
        ]
        if latest:
            parts.extend(["", "Previous proposal chunk:", latest])
        if anchor:
            parts.extend(["", anchor])
        return "\n".join(parts)

    def heap_exchange_paths(self) -> dict[str, Path]:
        """Return heap/exchange lifecycle artifact paths for this gate universe."""
        if self.output_dir:
            base = self.output_dir / "heap_exchange"
        else:
            base = self.repo_root / "output" / "ai_packets" / self.stamp
        base.mkdir(parents=True, exist_ok=True)
        return {
            "dir": base,
            "runtime_state": base / "heap_exchange_runtime_state.jsonl",
            "runtime_entry": base / "heap_exchange_runtime_entry.json",
            "runtime_entry_md": base / "heap_exchange_runtime_entry.md",
            "exit_output": base / "heap_runtime_exit_output.json",
            "exit_output_md": base / "heap_runtime_exit_output.md",
            "exit_product": base / "heap_exchange_runtime_exit_product.json",
            "exit_product_md": base / "heap_exchange_runtime_exit_product.md",
        }

    def append_heap_exchange_event(self, event: dict[str, Any]) -> None:
        """Publish a public heap/exchange event without exposing private reasoning."""
        paths = self.heap_exchange_paths()
        payload = dict(event)
        payload.setdefault("schema_version", 1)
        payload.setdefault("stamp", self.stamp)
        payload.setdefault("timestamp", now_iso())
        payload.setdefault("raw_thinking_exposed", False)
        payload.setdefault("source_of_knowledge", "heap_exchange")
        paths["runtime_state"].parent.mkdir(parents=True, exist_ok=True)
        with paths["runtime_state"].open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    def write_heap_exchange_entry(self) -> None:
        """Register the heap completeness gate as the dynamic heap/exchange universe."""
        paths = self.heap_exchange_paths()
        lanes = [
            {"name": "gpu1", "role": "primary_exit_coordinator", "available": True},
            {
                "name": "gpu0",
                "role": "diagnostic_peer_and_product_evidence_lane",
                "available": True,
            },
            {
                "name": "npu",
                "role": "micro_task_auditor_and_guardrail_peer",
                "available": True,
            },
            {"name": "broker", "role": "allowlisted_tool_executor", "available": True},
            {
                "name": "code_execution_matrix",
                "role": "allowlisted_compile_test_diff_evidence_lane",
                "available": True,
            },
            {
                "name": "virtual_dev_environment",
                "role": "controlled_script_load_debug_probe_environment",
                "available": True,
            },
            {
                "name": "context_memory",
                "role": "sqlite_fts_context_pack_semantic_chunks",
                "available": True,
            },
            {
                "name": "deterministic_audit",
                "role": "exit_quality_and_contract_lane",
                "available": True,
            },
        ]
        entry = {
            "schema_version": 1,
            "kind": "heap_exchange_runtime_entry",
            "generated_at": now_iso(),
            "stamp": self.stamp,
            "repo_root": self.repo_root.as_posix(),
            "source_of_knowledge": "heap_exchange",
            "center_is_dynamic": True,
            "dynamic_exchange_pipeline": True,
            "static_chain_invocation_performed": False,
            "entry_controls_inputs_only": True,
            "exit_must_produce_concrete_product": True,
            "task_file": self.args.task_file,
            "request": self.request_text(),
            "runtime_state": repo_rel(self.repo_root, paths["runtime_state"]),
            "lanes": lanes,
            "available_lane_count": len([item for item in lanes if item.get("available")]),
            "knowledge_surface": {
                "source_of_knowledge": "heap_exchange",
                "knowledge_surface": "shared_runtime_heap_blackboard",
                "routing_model": "dynamic_exchange_not_static_chain",
                "lane_autonomy_model": "gpu1_gpu0_npu_provider_lanes_publish_and_consume_exchange_evidence",
                "deterministic_boundaries": {
                    "in_controlled": True,
                    "loop_dynamic": True,
                    "out_deterministic": True,
                },
            },
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "passed": True,
            "errors": [],
            "warnings": [],
        }
        write_json_report(entry, paths["runtime_entry"])
        lines = [
            "# Heap Exchange Runtime Entry",
            "",
            "- Passed: `True`",
            f"- Stamp: `{self.stamp}`",
            "- Routing model: `dynamic_exchange_not_static_chain`",
            "- Source of knowledge: `heap_exchange`",
            "",
            "GPU1, GPU0, NPU, broker and memory/context lanes publish into the same heap universe. Exit is deterministic and product-bound.",
        ]
        write_text_report("\n".join(lines) + "\n", paths["runtime_entry_md"])
        self.append_heap_exchange_event(
            {
                "kind": "heap_entry",
                "lane": "orchestrator",
                "summary": "heap completeness gate registered as dynamic heap/exchange universe",
                "entry": repo_rel(self.repo_root, paths["runtime_entry"]),
            }
        )

    def write_exit_output_product(
        self, response_text: str, events: list[dict[str, Any]], metrics: dict[str, Any]
    ) -> dict[str, Any]:
        """Write the operator-facing heap exit product assembled from all lane artifacts."""
        paths = self.heap_exchange_paths()
        product_status = str(
            self.state.get("product", {}).get("status")
            or metrics.get("product_status")
            or "blocked_with_reason"
        )
        file_quality = self.response_file_reference_quality(response_text)
        product = {
            "schema_version": 1,
            "kind": "heap_runtime_exit_output",
            "generated_at": now_iso(),
            "stamp": self.stamp,
            "request_input": self.request_text(),
            "product_status": product_status,
            "response_text": response_text,
            "provider_raw_response_text": self.response_text(),
            "source_of_knowledge": "heap_exchange",
            "assembled_by": "gpu1_exit_coordinator",
            "revealed_by": "heap_exchange_runtime_exit",
            "provider_contributions": self.provider_response_texts(),
            "context_artifact_refs": self.broker_output_refs(events),
            "bridge_reports": self.bridge_report_refs(events),
            "quality_output_signals": self.quality_output_signals(response_text, events),
            "response_file_reference_quality": file_quality,
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": self.missing_requirements(events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(events),
            "runtime_debug_lab_required": self.runtime_debug_lab_required(),
            "runtime_debug_lab_passed": self.runtime_debug_lab_passed(events),
            "runtime_debug_lab_reports": self.runtime_debug_lab_reports(events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
        }
        write_json_report(product, paths["exit_output"])
        md = [
            "# Heap Runtime Exit Output",
            "",
            f"- Status: `{product_status}`",
            f"- Assembled by: `{product['assembled_by']}`",
            f"- Revealed by: `{product['revealed_by']}`",
            "",
            "## Response",
            "",
            response_text,
            "",
            "## File reference quality",
            "",
            f"- Passed: `{file_quality.get('passed')}`",
            f"- Unverified file refs: `{file_quality.get('unverified_file_refs')}`",
            "",
            "## Runtime debug lab",
            "",
            f"- Virtual dev environment required: `{product.get('virtual_dev_environment_required')}`",
            f"- Virtual dev environment passed: `{product.get('virtual_dev_environment_passed')}`",
            f"- Virtual dev environment reports: `{product.get('virtual_dev_environment_reports')}`",
            f"- Code execution matrix required: `{product.get('code_execution_matrix_required')}`",
            f"- Code execution matrix passed: `{product.get('code_execution_matrix_passed')}`",
            f"- Code execution matrix reports: `{product.get('code_execution_matrix_reports')}`",
            f"- Required: `{product.get('runtime_debug_lab_required')}`",
            f"- Passed: `{product.get('runtime_debug_lab_passed')}`",
            f"- Reports: `{product.get('runtime_debug_lab_reports')}`",
            "",
            "## Proposal iterations",
            "",
            f"- Artifacts: `{product.get('proposal_iteration_artifacts')}`",
        ]
        write_text_report("\n".join(md) + "\n", paths["exit_output_md"])
        self.append_heap_exchange_event(
            {
                "kind": "heap_exit_product",
                "lane": "gpu1",
                "summary": f"GPU1 composed heap exit output with status={product_status}",
                "operation": "write_file",
                "operation_count": 1,
                "path": repo_rel(self.repo_root, paths["exit_output"]),
                "source_file": repo_rel(self.repo_root, paths["exit_output"]),
                "product_status": product_status,
                "quality_passed": self.quality_output_passed(response_text, events),
            }
        )
        return product

    def build_heap_exchange_exit_product(self, require_concrete_product: bool) -> dict[str, Any]:
        """Reuse the existing deterministic heap/exchange exit boundary tool."""
        paths = self.heap_exchange_paths()
        command = [
            self.child_python(),
            "tools/ai/build_heap_exchange_runtime_exit.py",
            "--repo-root",
            ".",
            "--stamp",
            self.stamp,
            "--runtime-entry",
            repo_rel(self.repo_root, paths["runtime_entry"]),
            "--runtime-state",
            repo_rel(self.repo_root, paths["runtime_state"]),
            "--output",
            repo_rel(self.repo_root, paths["exit_product"]),
            "--markdown-output",
            repo_rel(self.repo_root, paths["exit_product_md"]),
        ]
        if require_concrete_product:
            command.append("--require-concrete-product")
        try:
            completed = subprocess.run(
                command,
                cwd=self.repo_root,
                env=command_env(self.repo_root),
                capture_output=True,
                text=True,
                check=False,
                timeout=max(30, int(self.args.timeout_seconds)),
            )
        except subprocess.TimeoutExpired as exc:
            self.warnings.append(f"heap exchange exit timed out: {exc}")
            return {
                "passed": False,
                "error": "timeout",
                "output": repo_rel(self.repo_root, paths["exit_product"]),
            }
        report = read_json(paths["exit_product"])
        if completed.returncode != 0:
            self.warnings.append(
                f"heap exchange exit returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}"
            )
        return report or {
            "passed": completed.returncode == 0,
            "output": repo_rel(self.repo_root, paths["exit_product"]),
        }

    def runtime_debug_lab_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        required_terms = (
            "mvp",
            "lab python",
            "laboratorio python",
            "python funzion",
            "debug lab",
            "implementa",
            "implementazione",
            "codice effettivo",
            "funzionante",
        )
        return any(term in text for term in required_terms)

    def code_execution_matrix_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        hints = (
            "codice",
            "code",
            "coding",
            "test",
            "validazione",
            "validation",
            "patch",
            "proposte concrete",
            "proposta concreta",
            "esecuzione",
            "execution",
            "heap/universo",
            "universo",
        )
        return self.implementation_output_required() or any(hint in text for hint in hints)

    def code_execution_matrix_targets(self) -> list[str]:
        candidates = [
            "Tools/ai/compose_heap_final_proposals.py",
            "Tools/ai/heap_proposal_gate.py",
            "Tools/ai/run_heap_runtime_context_closure.py",
            "Tools/ai/run_heap_runtime_completeness_gate.py",
            "Tools/ai/run_heap_code_execution_tool.py",
            "Tools/ai/heap_code_execution_tool_core.py",
            "Tools/ai/run_heap_virtual_dev_environment.py",
            "Tools/ai/assemble_heap_final_readable_product.py",
            "Tools/ai/heap_final_code_product.py",
            "Tools/ai/heap_final_readable_synthesis.py",
            "Tools/ai/agent_runtime_tool_broker.py",
            "Tools/validation/test_proposal_gate.py",
            "Tools/validation/run_heap_code_execution_tool_smoke.py",
            "Tools/validation/run_heap_virtual_dev_environment_smoke.py",
            "Tools/validation/run_heap_final_readable_product_smoke.py",
        ]
        return [path for path in candidates if (self.repo_root / path).exists()]

    def virtual_dev_environment_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        hints = (
            "ambiente",
            "debug",
            "runtime",
            "svilupp",
            "caricare",
            "script",
            "pointer",
            "universo",
            "virtual",
        )
        return self.implementation_output_required() or any(hint in text for hint in hints)

    def virtual_dev_environment_targets(self) -> list[str]:
        return self.code_execution_matrix_targets()

    def virtual_dev_environment_plan_items(
        self, context_dir: Path, request: str
    ) -> list[dict[str, Any]]:
        if not self.virtual_dev_environment_required():
            return []
        return [
            {
                "stage": 4,
                "requirement": "virtual_dev_environment",
                "id": "heap-virtual-dev-environment",
                "tool": "run_heap_virtual_dev_environment",
                "args": {
                    "target_file": self.virtual_dev_environment_targets(),
                    "validation_script": [
                        "Tools/validation/run_heap_virtual_dev_environment_smoke.py",
                        "Tools/validation/run_heap_final_readable_product_smoke.py",
                    ],
                    "dynamic_import": True,
                    "help_probe": True,
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 120), 600),
                    "tail_chars": 5000,
                },
                "reason": "provide a controlled development environment where heap tools are loaded, probed, debugged and validated before final composition",
            }
        ]

    def code_execution_matrix_plan_items(
        self, context_dir: Path, request: str
    ) -> list[dict[str, Any]]:
        if not self.code_execution_matrix_required():
            return []
        matrix_dir = context_dir / "code_execution_matrix"
        matrix_dir.mkdir(parents=True, exist_ok=True)
        return [
            {
                "stage": 4,
                "requirement": "code_execution_matrix",
                "id": "heap-code-execution-matrix",
                "tool": "run_heap_code_execution_matrix",
                "args": {
                    "target_file": self.code_execution_matrix_targets(),
                    "validation_script": [
                        "Tools/validation/test_proposal_gate.py",
                        "Tools/validation/run_heap_code_execution_tool_smoke.py",
                        "Tools/validation/run_heap_virtual_dev_environment_smoke.py",
                        "Tools/validation/run_heap_final_readable_product_smoke.py",
                    ],
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 120), 600),
                    "tail_chars": 5000,
                    "max_diff_chars": 80000,
                },
                "reason": "execute concrete compile/test/diff evidence for heap coding proposals before product acceptance",
            }
        ]

    def runtime_debug_lab_dir(self) -> Path:
        path = self.runtime_context_dir() / "runtime_debug_lab"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def runtime_debug_lab_source_paths(self) -> list[str]:
        candidates = [
            "tools/ai/agent_runtime_debug_lab.py",
            "tools/ai/agent_runtime_debug_lab/policy.py",
            "tools/ai/agent_runtime_debug_lab/reporting.py",
            "tools/ai/agent_runtime_debug_lab/runner.py",
            "tools/ai/run_heap_runtime_completeness_gate.py",
            "tools/ai/agent_runtime_tool_broker.py",
        ]
        return [path for path in candidates if (self.repo_root / path).exists()]

    def write_runtime_debug_lab_request(self) -> tuple[str, str, str]:
        lab_dir = self.runtime_debug_lab_dir()
        request_path = lab_dir / f"agent_runtime_debug_lab_request_{self.stamp}.json"
        report_path = lab_dir / f"agent_runtime_debug_lab_{self.stamp}.json"
        markdown_path = lab_dir / f"agent_runtime_debug_lab_{self.stamp}.md"
        source_paths = self.runtime_debug_lab_source_paths()
        request = {
            "schema_version": 1,
            "kind": "agent_runtime_debug_lab_request",
            "operations": [
                {
                    "id": "compile_debug_lab_sources",
                    "type": "python_compile",
                    "paths": source_paths,
                    "timeout_seconds": 300,
                },
                {
                    "id": "git_diff_check",
                    "type": "git_diff_check",
                    "timeout_seconds": 120,
                },
                {
                    "id": "git_status_short",
                    "type": "git_status_short",
                    "timeout_seconds": 120,
                },
            ],
        }
        request_path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return (
            repo_rel(self.repo_root, request_path),
            repo_rel(self.repo_root, report_path),
            repo_rel(self.repo_root, markdown_path),
        )

    def runtime_debug_lab_plan_items(self, context_dir: Path, request: str) -> list[dict[str, Any]]:
        if not self.runtime_debug_lab_required():
            return []
        request_file, output, markdown_output = self.write_runtime_debug_lab_request()
        return [
            {
                "stage": 4,
                "requirement": "runtime_debug_lab_execution",
                "id": "runtime-debug-lab-execution",
                "tool": "agent_runtime_debug_lab",
                "args": {
                    "request_file": request_file,
                    "output": output,
                    "markdown_output": markdown_output,
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 60), 600),
                    "tail_chars": 4000,
                },
                "reason": "execute the reusable report-only Python debug lab before claiming an MVP/lab product",
            }
        ]

    def required_requirements_order(self) -> list[str]:
        order = list(REQUIREMENT_ORDER)
        if self.virtual_dev_environment_required() and "virtual_dev_environment" not in order:
            order.append("virtual_dev_environment")
        if self.code_execution_matrix_required() and "code_execution_matrix" not in order:
            order.append("code_execution_matrix")
        if self.runtime_debug_lab_required() and "runtime_debug_lab_execution" not in order:
            order.append("runtime_debug_lab_execution")
        return order

    def virtual_dev_environment_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "virtual_dev_environment":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in ("json_report", "markdown_report"):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def virtual_dev_environment_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.virtual_dev_environment_required():
            return True
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "virtual_dev_environment":
                continue
            if payload.get("blocked") or safe_int(payload.get("returncode"), default=1) != 0:
                continue
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            if summary.get("passed") is False:
                continue
            return True
        return False

    def code_execution_matrix_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "code_execution_matrix":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def code_execution_matrix_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.code_execution_matrix_required():
            return True
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "code_execution_matrix":
                continue
            if payload.get("blocked") or safe_int(payload.get("returncode"), default=1) != 0:
                continue
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            if summary.get("passed") is False:
                continue
            return True
        return False

    def runtime_debug_lab_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "runtime_debug_lab_execution":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in ("json_report", "markdown_report", "request_file"):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def runtime_debug_lab_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.runtime_debug_lab_required():
            return True
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "runtime_debug_lab_execution":
                continue
            if payload.get("blocked") or safe_int(payload.get("returncode"), default=1) != 0:
                continue
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            if summary.get("passed") is False:
                continue
            return True
        return False

    def tool_plan(self) -> list[dict[str, Any]]:
        context_dir = self.runtime_context_dir()
        request = self.request_text()
        query = request or self.args.objective
        memory_content = f"request={request}; objective={self.args.objective}; stamp={self.stamp}"
        return [
            {
                "stage": 1,
                "requirement": "tool_catalog",
                "id": "tool-catalog-inventory",
                "tool": "build_agent_agnostic_tool_inventory",
                "args": {
                    "root": [
                        "tools/ai",
                        "tools/validation",
                        "tools/workflow",
                        "tools/npu",
                    ]
                },
                "reason": "discover allowlisted project tools before deciding product readiness",
            },
            {
                "stage": 1,
                "requirement": "shared_memory",
                "id": "shared-memory-inventory",
                "tool": "build_agent_memory_inventory",
                "args": {"objective": self.args.objective},
                "reason": "load read-only shared memory state into heap-visible evidence",
            },
            {
                "stage": 1,
                "requirement": "operational_memory_write",
                "id": "operational-memory-write",
                "tool": "runtime_sqlite_memory",
                "args": {
                    "action": "remember",
                    "scope": "operational",
                    "summary": "heap heartbeat request",
                    "content": memory_content,
                    "role": "heap_runtime_heartbeat",
                    "tag": ["heap", "heartbeat", "teamwork"],
                },
                "reason": "write request-scoped operational memory before provider synthesis",
            },
            {
                "stage": 1,
                "requirement": "operational_memory_search",
                "id": "operational-memory-search",
                "tool": "runtime_sqlite_memory",
                "args": {
                    "action": "search",
                    "scope": "operational",
                    "query": query,
                    "limit": 5,
                },
                "reason": "read request-scoped operational memory before provider synthesis",
            },
            {
                "stage": 2,
                "requirement": "shared_context_chunks",
                "id": "shared-request-context",
                "tool": "build_agent_transient_request_context",
                "args": {
                    "objective": self.args.objective,
                    "memory_note": [
                        "heap runtime completeness gate must prove tool, memory, context, chunks and validation evidence before product signal",
                        "budget/iterations define convergence and prevent endless repository loops",
                        f"user_request={request}",
                    ],
                    "raw_file": [
                        "AGENTS.md",
                        "README.md",
                        *self.historical_tool_context_files(),
                    ],
                },
                "reason": "materialize request-scoped shared context/chunks from repository policy and historical tool maps",
            },
            {
                "stage": 2,
                "requirement": "semantic_code_chunks",
                "id": "semantic-code-chunk-selection",
                "tool": "select_semantic_code_chunks",
                "args": {
                    "query": query,
                    "output": repo_rel(
                        self.repo_root,
                        context_dir / "selected_semantic_code_chunks.json",
                    ),
                    "markdown_output": repo_rel(
                        self.repo_root, context_dir / "selected_semantic_code_chunks.md"
                    ),
                    "max_chunks": 12,
                    "max_total_chars": min(int(self.args.max_context_files) * 500, 24000),
                    "max_excerpt_chars": min(int(self.args.max_chars_per_file), 3000),
                    "path_boost": ["tools/ai", "tools/npu", "tools/workflow"],
                },
                "reason": "select bounded semantic code chunks so provider lanes share connected logical context",
            },
            {
                "stage": 2,
                "requirement": "ai_context_pack",
                "id": "ai-context-pack",
                "tool": "build_ai_context_pack",
                "args": {
                    "profile": "core_ai_backend",
                    "basename": f"heap_runtime_context_pack_{self.stamp}",
                    "output_dir": repo_rel(self.repo_root, context_dir / "ai_context_pack"),
                    "evidence_dir": repo_rel(
                        self.repo_root, context_dir / "ai_context_pack_evidence"
                    ),
                    "evidence_basename": f"heap_runtime_context_pack_evidence_{self.stamp}",
                    "max_total_chars": min(
                        int(self.args.max_context_files) * int(self.args.max_chars_per_file),
                        96000,
                    ),
                    "max_file_chars": int(self.args.max_chars_per_file),
                },
                "reason": "assemble bounded final context pack from stable historical context builder",
            },
            {
                "stage": 3,
                "requirement": "semantic_evidence_chunks",
                "id": "semantic-evidence-chunk-manifest",
                "tool": "build_semantic_evidence_chunks",
                "args": {},
                "reason": "chunk oversized context/evidence into linked logical pieces before provider synthesis",
            },
            {
                "stage": 3,
                "requirement": "validation_evidence",
                "id": "planner-json-contract-validation",
                "tool": "run_gpu_planner_json_contract_smoke",
                "args": {},
                "reason": "prove validation tool evidence is consumed before arbiter decision",
            },
            *self.virtual_dev_environment_plan_items(context_dir, request),
            *self.code_execution_matrix_plan_items(context_dir, request),
            *self.runtime_debug_lab_plan_items(context_dir, request),
        ]

    def read_events(self) -> list[dict[str, Any]]:
        self.heap_read_count += 1
        return self.heap.read_events()

    def publish(
        self,
        source: str,
        event_type: str,
        payload: dict[str, Any],
        *,
        target: str = "",
        correlation_id: str = "",
        round_id: int | None = None,
    ) -> None:
        self.heap.append_event(
            source=source,
            target=target or None,
            event_type=event_type,
            correlation_id=correlation_id or None,
            round_id=round_id,
            payload=payload,
        )
        self.heap_write_count += 1

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return event_payloads_by_type(events, "broker_result")

    def broker_request_count_from_events(self, events: list[dict[str, Any]]) -> int:
        return sum(1 for event in events if event.get("event_type") == "broker_request")

    def broker_execution_count_from_events(self, events: list[dict[str, Any]]) -> int:
        count = 0
        for payload in self.broker_results(events):
            if payload.get("blocked"):
                continue
            if (
                safe_int(payload.get("returncode"), default=1) == 0
                or payload.get("executed") is True
            ):
                count += 1
        return count

    def bridge_report_refs(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for ref in self.bridge_reports:
            if ref and ref not in refs:
                refs.append(ref)
        for payload in self.broker_results(events):
            ref = str(payload.get("broker_report") or "").strip()
            if ref and ref not in refs:
                refs.append(ref)
        return refs

    def effective_tool_request_count(self, events: list[dict[str, Any]]) -> int:
        return max(self.tool_request_count, self.broker_request_count_from_events(events))

    def effective_tool_execution_count(self, events: list[dict[str, Any]]) -> int:
        return max(self.tool_execution_count, self.broker_execution_count_from_events(events))

    def requirement_for_tool(self, tool_name: str) -> str:
        for item in self.tool_plan():
            if item["tool"] == tool_name:
                return str(item["requirement"])
        return "unknown"

    def completed_requirements(self, events: list[dict[str, Any]]) -> set[str]:
        completed: set[str] = set()
        for payload in self.broker_results(events):
            tool = str(payload.get("tool") or "")
            if payload.get("blocked"):
                continue
            if safe_int(payload.get("returncode"), default=1) != 0:
                continue
            errors = payload.get("errors") if isinstance(payload.get("errors"), list) else []
            if errors:
                continue
            requirement = str(payload.get("requirement") or self.requirement_for_tool(tool))
            if requirement != "unknown":
                completed.add(requirement)
        for provider_report in self.provider_reports:
            if provider_report.get("passed") is not True:
                continue
            requirement = str(provider_report.get("requirement") or "")
            if requirement in REQUIREMENT_ORDER:
                completed.add(requirement)
        return completed

    def attempted_requirements(self, events: list[dict[str, Any]]) -> set[str]:
        attempted: set[str] = set()
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "unknown":
                attempted.add(requirement)
        for provider_report in self.provider_reports:
            requirement = str(provider_report.get("requirement") or "")
            if requirement in PROVIDER_REQUIREMENTS:
                attempted.add(requirement)
        return attempted

    def missing_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        completed = self.completed_requirements(events)
        return [item for item in self.required_requirements_order() if item not in completed]

    def broker_output_refs(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
                "chunk_output_dir",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def semantic_evidence_sources(self, events: list[dict[str, Any]]) -> list[str]:
        sources: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement not in {
                "shared_context_chunks",
                "semantic_code_chunks",
                "ai_context_pack",
                "operational_memory_search",
            }:
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in sources:
                    sources.append(value)
        return sources[:8]

    def enrich_plan_item_args(
        self, plan_item: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        item = dict(plan_item)
        args = dict(item.get("args") or {})
        if item.get("requirement") == "shared_context_chunks":
            refs = self.broker_output_refs(events)
            if refs:
                args["report_file"] = refs[:10]
        if item.get("requirement") == "semantic_evidence_chunks":
            sources = self.semantic_evidence_sources(events)
            args.update(
                {
                    "basename": f"heap_runtime_semantic_evidence_{self.stamp}",
                    "source": sources,
                    "output_dir": repo_rel(
                        self.repo_root,
                        self.runtime_context_dir() / "semantic_evidence_chunks",
                    ),
                    "chunk_output_dir": repo_rel(
                        self.repo_root,
                        self.runtime_context_dir() / "semantic_evidence_chunks" / "chunks",
                    ),
                    "chunk_max_chars": min(max(int(self.args.max_chars_per_file), 4000), 12000),
                    "chunk_overlap_lines": 12,
                }
            )
        item["args"] = args
        return item

    def next_unattempted_plan_items(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        attempted = self.attempted_requirements(events)
        pending = [item for item in self.tool_plan() if item["requirement"] not in attempted]
        if not pending:
            return []
        if self.max_iterations < 4:
            return [self.enrich_plan_item_args(pending[0], events)]
        stage = min(int(item.get("stage") or 1) for item in pending)
        return [
            self.enrich_plan_item_args(item, events)
            for item in pending
            if int(item.get("stage") or 1) == stage
        ]

    def next_unattempted_plan_item(self, events: list[dict[str, Any]]) -> dict[str, Any] | None:
        items = self.next_unattempted_plan_items(events)
        return items[0] if items else None

    def publish_shared_evidence_facts(self, round_id: int, events: list[dict[str, Any]]) -> None:
        existing = {item.get("requirement") for item in self.state["shared_evidence"]}
        completed = self.completed_requirements(events)
        for requirement in REQUIREMENT_ORDER:
            if requirement not in completed or requirement in existing:
                continue
            evidence = {
                "id": f"shared_evidence_{requirement}",
                "requirement": requirement,
                "kind": "shared_runtime_evidence",
                "source": "broker_result",
                "status": "available",
            }
            append_unique(self.state["shared_evidence"], evidence)
            self.publish(
                "deterministic",
                "fact",
                evidence,
                target="gpu1",
                correlation_id=f"{self.stamp}:shared:{requirement}",
                round_id=round_id,
            )

    def bootstrap(self) -> None:
        self.publish(
            "orchestrator",
            "task_state",
            self.state["task"],
            target="gpu1",
            correlation_id=f"{self.stamp}:task",
            round_id=0,
        )
        if self.request_text():
            request_payload = {
                "id": f"{self.stamp}:user_request",
                "text": self.request_text(),
                "objective": self.args.objective,
                "expected_output": [
                    "response_text",
                    "response_source",
                    "heap_event_refs",
                    "provider_refs",
                    "product_status",
                ],
            }
            self.publish(
                "orchestrator",
                "user_request",
                request_payload,
                target="gpu1",
                correlation_id=f"{self.stamp}:user_request",
                round_id=0,
            )
        budget_fact = {
            "id": "provider_budget_governor_loaded",
            "source": "heap_provider_budget_governor",
            "kind": "provider_budget",
            "value": self.budget_governor.get("decision"),
            "loop_budget": self.budget_governor.get("loop_budget"),
            "provider_lanes": sorted((self.budget_governor.get("provider_lanes") or {}).keys()),
        }
        contract_fact = {
            "id": "provider_invocation_contract_loaded",
            "source": "heap_provider_invocation_contract",
            "kind": "provider_invocation_contract",
            "value": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "required_events": safe_dict(
                self.invocation_contract.get("expected_telemetry_contract")
            ).get("events_required", []),
        }
        completeness_fact = {
            "id": "heap_completeness_requirements_loaded",
            "source": "heap_runtime_completeness_gate",
            "kind": "readiness_requirements",
            "value": list(REQUIREMENT_ORDER),
            "budget_max_iterations": self.max_iterations,
        }
        for fact in (budget_fact, contract_fact, completeness_fact):
            append_unique(self.state["facts"], fact)
            self.publish(
                "deterministic",
                "fact",
                fact,
                target="gpu1",
                correlation_id=f"{self.stamp}:fact:{fact['id']}",
                round_id=0,
            )
        # Startup preload is active heap input, not a post-hoc diagnostic pointer.
        # Publish it before the first snapshot/exchange entry so provider lanes and
        # external observers see a single causally ordered universe from startup.
        self.publish_startup_task_file_context()
        self.publish_startup_memory_context_reload_events()
        self.publish_startup_manifest_evidence()
        self.heap.write_snapshot()
        self.write_heap_exchange_entry()

    def planner_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.heap.pending_broker_requests():
            return
        plan_items = self.next_unattempted_plan_items(events)
        if not plan_items:
            return
        for plan_item in plan_items:
            request_id = f"{self.stamp}:{plan_item['id']}"
            need = {
                "id": f"need_{plan_item['requirement']}",
                "owner": "planner",
                "kind": "brokered_runtime_evidence",
                "target": plan_item["tool"],
                "requirement": plan_item["requirement"],
                "reason": plan_item["reason"],
                "budget_ref": "provider_budget_governor_loaded",
                "round": round_id,
            }
            append_unique(self.state["needs"], need)
            self.publish(
                "gpu1",
                "need",
                need,
                target="broker",
                correlation_id=request_id,
                round_id=round_id,
            )
            tool_request = {
                "id": request_id,
                "tool": plan_item["tool"],
                "args": plan_item.get("args") or {},
                "reason": plan_item["reason"],
                "requirement": plan_item["requirement"],
            }
            append_unique(self.state["tool_requests"], tool_request)
            self.publish(
                "gpu1",
                "broker_request",
                tool_request,
                target="broker",
                correlation_id=request_id,
                round_id=round_id,
            )
            self.tool_request_count += 1
            self.append_reload_lifecycle_event(
                plan_item["requirement"], round_id, "requested", plan_item["tool"]
            )
            self.append_heap_exchange_event(
                {
                    "kind": "broker_request",
                    "lane": "gpu1",
                    "target": "broker",
                    "round": round_id,
                    "tool": plan_item["tool"],
                    "requirement": plan_item["requirement"],
                    "summary": f"GPU1 requested broker tool {plan_item['tool']} for {plan_item['requirement']}",
                }
            )

    def run_bridge(self) -> dict[str, Any]:
        bridge_json = resolve_output_path(
            self.repo_root,
            self.path_arg(self.args.bridge_output, DEFAULT_BRIDGE_JSON).format(stamp=self.stamp),
        )
        bridge_md = resolve_output_path(
            self.repo_root,
            self.path_arg(self.args.bridge_markdown_output, DEFAULT_BRIDGE_MD).format(
                stamp=self.stamp
            ),
        )
        command = [
            self.child_python(),
            "tools/ai/provider_runtime_heap_broker_bridge.py",
            "--repo-root",
            ".",
            "--stamp",
            self.stamp,
            "--events",
            repo_rel(self.repo_root, self.heap.paths.events),
            "--snapshot",
            repo_rel(self.repo_root, self.heap.paths.snapshot),
            "--heap-markdown",
            repo_rel(self.repo_root, self.heap.paths.markdown),
            "--bridge-dir",
            self.path_arg(self.args.bridge_dir, DEFAULT_BRIDGE_DIR),
            "--timeout-seconds",
            str(self.args.timeout_seconds),
            "--max-requests",
            "0",
            "--output",
            repo_rel(self.repo_root, bridge_json),
            "--markdown-output",
            repo_rel(self.repo_root, bridge_md),
        ]
        completed = subprocess.run(
            command,
            cwd=self.repo_root,
            env=command_env(self.repo_root),
            capture_output=True,
            text=True,
            check=False,
            timeout=self.args.timeout_seconds + 30,
        )
        report = read_json(bridge_json)
        self.bridge_reports.append(repo_rel(self.repo_root, bridge_json))
        if completed.returncode != 0:
            self.errors.append(
                f"broker bridge returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}"
            )
        self.tool_execution_count += safe_int(report.get("tool_execution_count"))
        self.append_reload_lifecycle_event(
            "tool_catalog", 0, "bridge_result", "agent_runtime_tool_broker"
        )
        self.append_heap_exchange_event(
            {
                "kind": "broker_result",
                "lane": "broker",
                "summary": "broker bridge executed pending heap tool requests",
                "tool_execution_count": safe_int(report.get("tool_execution_count")),
                "source_file": repo_rel(self.repo_root, bridge_json),
            }
        )
        return report

    def critic_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        broker_results = self.broker_results(events)
        if not broker_results:
            return
        completed = sorted(self.completed_requirements(events))
        missing = self.missing_requirements(events)
        claim = {
            "id": f"heap_completeness_progress_round_{round_id}",
            "from": "critic",
            "claim": (
                "heap evidence complete" if not missing else "heap evidence still incomplete"
            ),
            "confidence": 0.95 if not missing else 0.78,
            "completed_requirements": completed,
            "missing_requirements": missing,
            "broker_result_count": len(broker_results),
            "tool_execution_count": self.tool_execution_count,
        }
        append_unique(self.state["claims"], claim)
        self.publish(
            "npu",
            "claim",
            claim,
            target="gpu1",
            correlation_id=f"{self.stamp}:critic:{round_id}",
            round_id=round_id,
        )
        self.publish(
            "deterministic",
            "validation_signal",
            claim,
            target="gpu1",
            correlation_id=f"{self.stamp}:validation:{round_id}",
            round_id=round_id,
        )

    def arbiter_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.state["decisions"]:
            return
        missing = self.missing_requirements(events)
        unattempted = self.next_unattempted_plan_item(events)
        ready = not missing
        bridge_refs = self.bridge_report_refs(events)
        effective_tool_execution_count = self.effective_tool_execution_count(events)
        if ready and effective_tool_execution_count <= 0:
            missing = [*missing, "broker_tool_execution"]
            ready = False
        if ready and not bridge_refs:
            missing = [*missing, "broker_bridge_reports"]
            ready = False
        if ready and self.request_text() and not self.response_text_complete():
            missing = [*missing, "gpu1_request_response_complete"]
            ready = False
        file_quality = self.response_file_reference_quality(self.response_text())
        if ready and not file_quality.get("passed"):
            missing = [*missing, "verified_unambiguous_source_refs"]
            ready = False
        if (
            ready
            and self.detailed_output_expected()
            and not self.quality_output_passed(self.response_text(), events)
        ):
            missing = [*missing, "provider_quality_output"]
            ready = False
        budget_exhausted = round_id >= self.max_iterations
        no_more_progress = unattempted is None and bool(missing)
        if not ready and not budget_exhausted and not no_more_progress:
            return
        status = "ready" if ready else "blocked_with_reason"
        decision = {
            "id": "heap_completeness_gate_decision",
            "from": "arbiter",
            "decision": ("product_ready_heap_complete" if ready else "blocked_with_reason"),
            "evidence_refs": [
                "heap:task_state",
                "heap:broker_result",
                "heap:shared_evidence",
                "heap:validation_signal",
                *bridge_refs[-4:],
            ],
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(
                self.invocation_contract.get("real_run_gate")
            ).get("decision"),
            "provider_generation_permit_allowed": self.budget_governor.get("permit_allowed"),
        }
        append_unique(self.state["decisions"], decision)
        self.decision_count += 1
        self.publish(
            "deterministic",
            "decision",
            decision,
            target="orchestrator",
            correlation_id=f"{self.stamp}:decision",
            round_id=round_id,
        )
        candidate = {
            "id": "candidate_heap_runtime_product_flow",
            "kind": "design_operation",
            "path": "tools/workflow/run_unified_real_product_pr.ps1",
            "status": "ready_for_manual_review" if ready else "blocked",
            "rationale": (
                "gate proves heap/tool/memory/context/validation convergence before product readiness"
                if ready
                else "gate blocked because heap completeness requirements were not all satisfied within budget"
            ),
            "missing_requirements": missing,
        }
        append_unique(self.state["candidate_operations"], candidate)
        self.candidate_operation_count += 1
        self.publish(
            "deterministic",
            "candidate_operation",
            candidate,
            target="orchestrator",
            correlation_id=f"{self.stamp}:candidate",
            round_id=round_id,
        )
        final_response_text = self.build_final_response_text(events)
        self.state["product"] = {
            "required": True,
            "status": status,
            "request_input": self.request_text(),
            "response_text": final_response_text,
            "response_source": self.response_source(),
            "heap_event_refs": [repo_rel(self.repo_root, self.heap.paths.events)],
            "provider_refs": self.provider_refs(),
            "provider_response_texts": self.provider_response_texts(),
            "context_artifact_refs": self.broker_output_refs(events),
            "bridge_reports": bridge_refs,
            "quality_output_signals": self.quality_output_signals(final_response_text, events),
            "quality_output_passed": self.quality_output_passed(final_response_text, events),
            "historical_tool_context_refs": self.historical_tool_context_files(),
            "response_file_reference_quality": self.response_file_reference_quality(
                self.response_text()
            ),
            "provider_role_decisions": self.provider_role_decisions(),
            "toolused": effective_tool_execution_count > 0,
            "shared_memory_written_and_used": "shared_memory"
            in self.completed_requirements(events),
            "gpu0_audit": self.provider_response_text("gpu0_peer"),
            "npu_audit": self.provider_response_text("npu_micro_task_auditor"),
            "reason": (
                "heap loop consumed tool catalog, memory, context/chunks and validation evidence"
                if ready
                else "heap loop stopped by budget/failed requirement before readiness"
            ),
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_governor": self.budget_governor.get("decision"),
        }
        self.publish(
            "orchestrator",
            "product_signal",
            self.state["product"],
            correlation_id=f"{self.stamp}:product",
            round_id=round_id,
        )

    def base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(requirement in completed for requirement in BASE_REQUIREMENTS)

    def provider_work_dir(self) -> Path:
        if self.output_dir:
            path = self.output_dir / "provider_teamwork"
        else:
            path = (
                self.repo_root
                / "output"
                / "validation"
                / f"heap_runtime_provider_teamwork_{self.stamp}"
            )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def request_text(self) -> str:
        return str(getattr(self.args, "request", "") or "").strip()

    def provider_response_text(self, lane: str) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != lane:
                continue
            text = str(report.get("response_text") or "").strip()
            if text:
                return text
        return ""

    def provider_role_decisions(self) -> dict[str, str]:
        decisions: dict[str, str] = {}
        for report in self.provider_reports:
            lane = str(report.get("lane") or "")
            decision = str(report.get("role_decision") or "").strip()
            if lane and decision:
                decisions[lane] = decision
        return decisions

    def provider_response_texts(self) -> dict[str, str]:
        responses: dict[str, str] = {}
        for report in self.provider_reports:
            lane = str(report.get("lane") or "")
            text = str(report.get("response_text") or "").strip()
            if lane and text:
                responses[lane] = text
        return responses

    def team_context_summary(self, max_chars: int = 6000) -> str:
        events = self.read_events()
        parts: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            line = {
                "requirement": requirement,
                "tool": payload.get("tool"),
                "returncode": payload.get("returncode"),
                "outputs": outputs,
                "summary": summary,
            }
            text = json.dumps(line, ensure_ascii=False, default=str)
            parts.append(text)
        joined = "\n".join(parts)
        return joined[:max_chars] + (
            "\n...[team context truncated]" if len(joined) > max_chars else ""
        )

    def tool_evidence_summary(
        self, events: list[dict[str, Any]], max_items: int = 12
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            refs: list[str] = []
            for key in (
                "json_report",
                "markdown_report",
                "evidence_json",
                "evidence_markdown",
                "chunk_output_dir",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value:
                    refs.append(value)
            items.append(
                {
                    "requirement": requirement,
                    "tool": str(payload.get("tool") or ""),
                    "returncode": safe_int(payload.get("returncode"), default=-1),
                    "refs": refs[:4],
                }
            )
        return items[:max_items]

    def tool_evidence_lines(self, events: list[dict[str, Any]], max_items: int = 12) -> list[str]:
        lines: list[str] = []
        for item in self.tool_evidence_summary(events, max_items=max_items):
            refs = item.get("refs") if isinstance(item.get("refs"), list) else []
            ref_text = (
                "; ".join(str(ref) for ref in refs[:3]) if refs else "nessun output dichiarato"
            )
            lines.append(
                f"- {item.get('tool')} -> {item.get('requirement')} (rc={item.get('returncode')}): {ref_text}"
            )
        return lines

    def quality_output_signals(self, text: str, events: list[dict[str, Any]]) -> dict[str, Any]:
        lowered = text.lower()
        tool_names = [str(item.get("tool") or "") for item in self.tool_evidence_summary(events)]
        return {
            "detailed_output_expected": self.detailed_output_expected(),
            "mentions_tool_evidence": "tool" in lowered
            and ("evidence" in lowered or "evidenza" in lowered),
            "mentions_heap_context": "heap" in lowered
            or "contesto" in lowered
            or "context" in lowered,
            "mentions_gpu0": "gpu0" in lowered or "gpu.0" in lowered,
            "mentions_npu": "npu" in lowered,
            "mentions_next_verifiable_action": "prossima azione" in lowered
            or "validazione" in lowered
            or "verificabile" in lowered,
            "tool_names_available": tool_names,
            "response_file_reference_quality": self.response_file_reference_quality(text),
            "implementation_quality": self.implementation_quality_report(text, events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "virtual_dev_environment_required": self.virtual_dev_environment_required(),
            "virtual_dev_environment_passed": self.virtual_dev_environment_passed(events),
            "virtual_dev_environment_reports": self.virtual_dev_environment_reports(events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(events),
        }

    def quality_output_passed(self, text: str, events: list[dict[str, Any]]) -> bool:
        signals = self.quality_output_signals(text, events)
        if self.virtual_dev_environment_required() and not self.virtual_dev_environment_passed(
            events
        ):
            return False
        if self.code_execution_matrix_required() and not self.code_execution_matrix_passed(events):
            return False
        if self.runtime_debug_lab_required() and not self.runtime_debug_lab_passed(events):
            return False
        if not signals.get("detailed_output_expected"):
            return True
        file_quality = (
            signals.get("response_file_reference_quality")
            if isinstance(signals.get("response_file_reference_quality"), dict)
            else {}
        )
        if not file_quality.get("passed"):
            return False
        implementation_quality = (
            signals.get("implementation_quality")
            if isinstance(signals.get("implementation_quality"), dict)
            else {}
        )
        if implementation_quality.get("required") and not implementation_quality.get("passed"):
            return False
        # Proposal artifacts are the heap blackboard contract. Once GPU1 has
        # emitted a proposal chunk, final quality must follow the same-heap
        # GPU0/NPU cross-lane decision, even for revision 0. Previously this
        # check only applied after provider_revision_count > 0, so the initial
        # GPU1 response could look textually acceptable and exit before the
        # cross-lane veto had a chance to drive an in-heap refinement cycle.
        if self.proposal_iteration_artifacts() and not self.latest_proposal_quality_passed():
            return False
        return bool(
            signals.get("mentions_tool_evidence")
            and signals.get("mentions_heap_context")
            and signals.get("mentions_gpu0")
            and signals.get("mentions_npu")
            and signals.get("mentions_next_verifiable_action")
        )

    def build_final_response_text(self, events: list[dict[str, Any]]) -> str:
        base_response = self.response_text().strip()
        if not self.detailed_output_expected():
            return base_response
        historical_refs = self.historical_tool_context_files()
        tool_lines = self.tool_evidence_lines(events)
        gpu0_text = (
            self.provider_response_text("gpu0_peer") or "GPU0 non ha prodotto una risposta utile."
        )
        npu_text = (
            self.provider_response_text("npu_micro_task_auditor")
            or "NPU non ha prodotto una risposta utile."
        )
        gpu1_text = base_response or "GPU1 non ha prodotto una risposta testuale utile."
        lines = [
            "## Sintesi heap dettagliata",
            "",
            "### Interpretazione richiesta",
            f"La richiesta operatore è stata trattata come task complesso: {self.request_text()}",
            "",
            "### Tool/evidence storiche e runtime consumate",
        ]
        if historical_refs:
            lines.extend(f"- mappa storica/canonica: {ref}" for ref in historical_refs[:10])
        else:
            lines.append("- nessuna mappa storica/canonica trovata nel workspace corrente")
        if tool_lines:
            lines.extend(tool_lines)
        else:
            lines.append("- nessun risultato broker disponibile")
        file_quality = self.response_file_reference_quality(gpu1_text)
        proposal_artifacts = self.proposal_iteration_artifacts()
        latest_proposal = self.latest_quality_proposal_iteration_block(
            max_chars=9000
        ) or self.latest_proposal_iteration_block(max_chars=2200)
        lines.extend(
            [
                "",
                "### Proposal iterations / blocchi riusabili",
                f"- Artifact proposta iterativa: {proposal_artifacts}",
                "- Ultimo blocco proposta riusabile:",
                latest_proposal or "nessun blocco proposal_iteration disponibile",
                "",
                "### Verifica riferimenti file",
                f"- Richiesta richiede file esistenti: {file_quality.get('request_requires_existing_files')}",
                f"- File sorgente verificati: {file_quality.get('existing_source_file_refs')}",
                f"- Artifact output ignorati come prova di file sorgente: {file_quality.get('output_artifact_refs')}",
                f"- File sorgente non verificati/bloccanti: {file_quality.get('unverified_source_file_refs')}",
                f"- Mancano riferimenti a file sorgente reali: {file_quality.get('no_source_file_refs')}",
                "",
                "### Contributo provider",
                f"- GPU0: {gpu0_text}",
                f"- NPU: {npu_text}",
                f"- GPU1: {gpu1_text}",
                "",
                "### Output operativo",
                gpu1_text,
                "",
                "### Limiti",
                "- L'output è valido solo rispetto agli artifact brokerati e ai provider report della run corrente.",
                "- Le mappe storiche orientano la scelta dei tool, ma non sostituiscono codice corrente, validator e report runtime.",
                "",
                "### Prossima azione verificabile",
                "Eseguire la stessa richiesta con report JSON completo e controllare product_status, tool_request_count, tool_execution_count, bridge_reports, provider_lane_count, quality_output_passed e context_artifact_refs.",
            ]
        )
        return "\n".join(lines).strip()

    def gpu1_request_prompt(self) -> str:
        request = self.request_text()
        if not request:
            return 'Return exactly this JSON object and no prose: {"ok": true, "lane": "ollama"}'
        peer_lines = []
        for lane in ("gpu0_peer", "npu_micro_task_auditor"):
            text = self.provider_response_text(lane)
            if text:
                peer_lines.append(f"{lane}: {text}")
        peer_context = (
            "\n".join(peer_lines) if peer_lines else "nessun contributo peer ancora disponibile"
        )
        team_context = self.team_context_summary()
        source_candidates = (
            "\n".join(f"- {item}" for item in self.real_source_file_candidates(limit=32))
            or "- nessun candidato sorgente verificato disponibile"
        )
        source_allowlist_contract = self.render_source_allowlist_contract(limit=32)
        revision_feedback = (
            self.provider_revision_feedback or "nessun feedback correttivo precedente"
        )
        return (
            "Sei GPU1 planner finale e leader operativo nel runtime heap IA-Carmine. "
            "Non rispondere come lista generica: consuma le evidenze brokerate, memoria SQLite/FTS, chunk semantici, context pack e contributi GPU0/NPU già presenti nell'heap. "
            "Per richieste di refactor/OOB lavora su file esistenti: copia TARGET_FILES verbatim dalla SOURCE_PATH_ALLOWLIST_CONTRACT; nuovi file sono ammessi solo se la richiesta operatore li chiede esplicitamente. "
            "Non applicare patch, non inventare file esistenti, non inventare risultati. "
            "Per richieste complesse usa sezioni: interpretazione richiesta; tool/evidence usate; contributo GPU0; contributo NPU; indagine su file reali; output operativo dettagliato; limiti; prossima azione verificabile. "
            f"Richiesta utente: {request}\n"
            f"Contributi peer heap:\n{peer_context}\n"
            f"Memoria/chunk/context pack condivisi:\n{team_context}\n"
            f"File sorgente reali candidati verificati nel repository/context:\n{source_candidates}\n"
            f"{source_allowlist_contract}\n"
            f"Feedback qualitativo heap da eventuale giro precedente:\n{revision_feedback}\n"
            "Regola: rispondi come sintesi GPU1 del team heap; se servono file esistenti usa solo i file sorgente candidati verificati, non gli artifact output/validation. Cita i tool storici/runtime consumati quando la richiesta richiede analisi, stato, igiene, tool, repo o output dettagliato.\n"
            "Per richieste implementative devi produrre un blocco operativo, non consigli generici. Usa sezioni TARGET_FILES, PROBLEM, IMPLEMENTATION_CHANGES, CODE_OR_PATCH_SKETCH, VALIDATION_COMMANDS, RISKS, EXIT_DECISION. TARGET_FILES deve essere copiato esattamente da Allowed source paths; non citare path non allowlisted nemmeno in PROBLEM/EVIDENCE/PATCH_SKETCH.\n"
            "Risposta finale completa e chiusa:"
        )

    def response_text(self) -> str:
        for report in reversed(self.provider_reports):
            if report.get("lane") != "gpu1_planner":
                continue
            text = str(report.get("response_text") or "").strip()
            if text:
                return text
        return ""

    def response_text_complete(self) -> bool:
        text = self.response_text().strip()
        if not text:
            return False
        lowered = text.lower().rstrip()
        dangling_suffixes = (
            " in",
            " con",
            " e",
            " ed",
            " o",
            " od",
            " di",
            " del",
            " della",
            " dello",
            " dei",
            " degli",
            " su",
            " per",
            " da",
            " a",
            " al",
            " alla",
            " allo",
            " ai",
            " agli",
            " tra",
            " fra",
            " che",
            " come",
            " quando",
            " perché",
            " se",
            " ma",
            " però",
            " quindi",
            " output_preview=",
            "[",
            "(",
            "{",
        )
        if lowered.endswith(dangling_suffixes):
            return False
        if text[-1] in {",", ":", ";"}:
            return False
        return True

    def response_source(self) -> str:
        return "gpu1_planner" if self.response_text() else ""

    def provider_refs(self) -> list[str]:
        refs: list[str] = []
        for report in self.provider_reports:
            output = str(report.get("output") or "")
            if output:
                refs.append(output)
        return refs

    def provider_command_specs(self, work_dir: Path, revision: int = 0) -> list[dict[str, Any]]:
        suffix = f"_revision{revision}" if revision else ""
        gpu1_json = work_dir / f"gpu1_ollama_provider_probe{suffix}.json"
        gpu0_json = work_dir / f"gpu0_openvino_peer_workload{suffix}.json"
        gpu0_md = work_dir / f"gpu0_openvino_peer_workload{suffix}.md"
        npu_json = work_dir / f"npu_micro_task_auditor{suffix}.json"
        npu_md = work_dir / f"npu_micro_task_auditor{suffix}.md"
        return [
            {
                "lane": "gpu0_peer",
                "requirement": "gpu0_provider_peer",
                "role": "diagnostic_peer_workload",
                "output": gpu0_json,
                "command": [
                    self.child_python(),
                    "tools/ai/build_openvino_gpu0_workload_report.py",
                    "--repo-root",
                    ".",
                    "--iterations",
                    str(self.args.gpu0_iterations),
                    "--min-seconds",
                    str(self.args.gpu0_min_seconds),
                    "--role",
                    "heap_runtime_diagnostic_peer",
                    "--request",
                    self.request_text(),
                    "--output",
                    repo_rel(self.repo_root, gpu0_json),
                    "--markdown-output",
                    repo_rel(self.repo_root, gpu0_md),
                ],
            },
            {
                "lane": "npu_micro_task_auditor",
                "requirement": "npu_micro_task_auditor",
                "role": "npu_micro_task_auditor",
                "output": npu_json,
                "command": [
                    self.child_python(),
                    "tools/ai/build_npu_micro_task_companion_report.py",
                    "--repo-root",
                    ".",
                    "--task-file",
                    self.args.task_file,
                    "--request",
                    self.request_text(),
                    "--python-exe",
                    self.child_python(),
                    "--timeout-seconds",
                    str(self.args.npu_micro_timeout_seconds),
                    "--max-context-chars",
                    str(self.args.npu_max_context_chars),
                    *(
                        [
                            "--run-device-workload",
                            "--device-workload-seconds",
                            str(self.args.npu_device_workload_seconds),
                            "--device-workload-iterations",
                            str(self.args.npu_device_workload_iterations),
                        ]
                        if self.args.allow_npu_device_workload
                        else []
                    ),
                    "--output",
                    repo_rel(self.repo_root, npu_json),
                    "--markdown-output",
                    repo_rel(self.repo_root, npu_md),
                ],
            },
            {
                "lane": "gpu1_planner",
                "requirement": "gpu1_provider_planner",
                "role": "primary_planner_cumulative_responder",
                "output": gpu1_json,
                "command": [
                    self.child_python(),
                    "tools/ai/run_local_provider_probe.py",
                    "--repo-root",
                    ".",
                    "--run-ollama",
                    "--model",
                    self.args.provider_model,
                    "--prompt",
                    "__GPU1_CUMULATIVE_PROMPT__",
                    "--timeout",
                    str(self.args.timeout_seconds),
                    "--max-new-tokens",
                    str(max(128, min(int(self.args.max_new_tokens), 4096))),
                    "--output",
                    repo_rel(self.repo_root, gpu1_json),
                ],
            },
        ]

    def summarize_provider_report(
        self,
        spec: dict[str, Any],
        completed: subprocess.CompletedProcess[str],
        report_data: dict[str, Any],
    ) -> dict[str, Any]:
        lane = str(spec["lane"])
        provider_execution = bool(
            report_data.get("provider_execution_performed")
            or report_data.get("openvino_gpu0_workload_performed")
            or report_data.get("openvino_gpu0_probe_performed")
            or report_data.get("npu_provider_execution_performed")
            or report_data.get("npu_device_workload_performed")
        )
        if provider_execution:
            self.provider_execution_performed = True
        errors = report_data.get("errors") if isinstance(report_data.get("errors"), list) else []
        warnings = (
            report_data.get("warnings") if isinstance(report_data.get("warnings"), list) else []
        )
        response_text = str(report_data.get("response_text") or "").strip()
        lane_reports = report_data.get("lane_reports")
        if isinstance(lane_reports, list):
            for lane_report in lane_reports:
                if isinstance(lane_report, dict) and lane_report.get("lane") == "ollama":
                    response_text = str(
                        lane_report.get("response_text")
                        or lane_report.get("text_preview")
                        or response_text
                    ).strip()
                    if response_text:
                        break
        return {
            "lane": lane,
            "role": spec.get("role"),
            "requirement": spec.get("requirement"),
            "output": repo_rel(self.repo_root, Path(spec["output"])),
            "returncode": completed.returncode,
            "passed": completed.returncode == 0 and report_data.get("passed") is True,
            "provider_execution_performed": provider_execution,
            "report_kind": report_data.get("kind"),
            "response_text": response_text,
            "role_decision": report_data.get("role_decision"),
            "npu_device_workload": report_data.get("npu_device_workload"),
            "npu_device_workload_requested": report_data.get("npu_device_workload_requested"),
            "npu_device_workload_performed": report_data.get("npu_device_workload_performed"),
            "npu_provider_execution_performed": report_data.get("npu_provider_execution_performed"),
            "errors": errors,
            "warnings": warnings,
            "stdout_tail": (completed.stdout or "")[-1000:],
            "stderr_tail": (completed.stderr or "")[-1000:],
        }

    def build_quality_failure_feedback(self, text: str, events: list[dict[str, Any]]) -> str:
        file_quality = self.response_file_reference_quality(text)
        implementation_quality = self.implementation_quality_report(text, events)
        candidates = self.real_source_file_candidates(events, limit=32)
        base_feedback = (
            "quality gate failure: la risposta precedente non è uscibile come prodotto heap. "
            f"output_artifact_refs={file_quality.get('output_artifact_refs')}; "
            f"unverified_source_file_refs={file_quality.get('unverified_source_file_refs')}; "
            f"no_source_file_refs={file_quality.get('no_source_file_refs')}; "
            f"implementation_quality_errors={implementation_quality.get('errors')}. "
            "Devi rigenerare usando solo file sorgente reali candidati, con proposte concrete agganciate a path repo esistenti. "
            "Se manca codice/patch/comandi, GPU0 deve considerare il blocco non soddisfacente. "
            f"source_candidates={candidates}"
        )
        iteration_feedback = self.proposal_iteration_feedback(events, file_quality)
        concrete_delta_feedback = self.force_concrete_delta_feedback(events)
        return "\n".join(
            part for part in (base_feedback, iteration_feedback, concrete_delta_feedback) if part
        )

    def force_concrete_delta_feedback(self, events: list[dict[str, Any]]) -> str:
        """Force GPU1 to produce a materially different concrete block after veto loops.

        This is intentionally feedback-only: it does not change provider calls,
        does not apply patches and does not alter the composer format. It raises
        the in-heap contract pressure when repeated proposal chunks are rejected
        for placeholder/stub markers or near-identical revisions.
        """
        report = self.latest_proposal_iteration_report()
        if not report:
            return ""

        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        progress = (
            report.get("proposal_progress")
            if isinstance(report.get("proposal_progress"), dict)
            else {}
        )
        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        veto = (
            report.get("cross_lane_veto") if isinstance(report.get("cross_lane_veto"), dict) else {}
        )

        def listify(value: Any) -> list[str]:
            if isinstance(value, list):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, tuple):
                return [str(item) for item in value if str(item).strip()]
            if isinstance(value, str) and value.strip():
                return [value.strip()]
            return []

        def parse_similarity(value: Any) -> float:
            try:
                return float(str(value or "0").replace(",", "."))
            except ValueError:
                return 0.0

        placeholder_hits = listify(implementation.get("placeholder_hits"))
        implementation_errors = listify(implementation.get("errors"))
        progress_errors = listify(progress.get("errors"))
        unverified_refs = listify(
            quality.get("unverified_source_file_refs") or quality.get("unverified_file_refs")
        )
        veto_reasons = listify(veto.get("reasons"))
        similarity = parse_similarity(progress.get("similarity"))

        has_placeholder = bool(placeholder_hits) or any(
            marker in item.lower()
            for item in implementation_errors + veto_reasons
            for marker in ("placeholder", "todo", "fixme", "bare_pass", "stub")
        )
        repeated = similarity >= 0.95 or any(
            "similarity=" in item.lower() for item in progress_errors + veto_reasons
        )
        vetoed = veto.get("vetoed") is True

        if not (has_placeholder or repeated or vetoed):
            return ""

        candidates = self.real_source_file_candidates(events, limit=18)
        latest_revision = report.get("revision")
        latest_source = report.get("source")
        lines = [
            "FORCED CONCRETE DELTA REQUIRED:",
            f"- Previous proposal revision: {latest_revision}",
            f"- Previous proposal source: {latest_source}",
            f"- Similarity with previous proposal: {similarity:.3f}",
            "- The previous block was rejected by the same heap. Do not repeat it.",
            "- Treat candidate_response_preview as a negative example when prior flags include invented_source_path, unresolved_pointer_placeholder or unresolved_angle_bracket_token.",
            "- Produce a materially different proposal chunk, not a paraphrase.",
            "- Remove every TODO/FIXME/pass/placeholder/stub marker from the proposal text.",
            "- Use concrete repo-relative TARGET_FILES only from the allowed concrete source targets below.",
            "- Copy TARGET_FILES verbatim from the allowed concrete source targets; do not cite rejected refs anywhere in the next proposal.",
            "- Every diff header path must match an allowed concrete source target exactly.",
            "- If the only possible target is unverified or invented, return EXIT_DECISION=NO_PATCHABLE_TARGET instead of inventing a path.",
            "- Never output unresolved angle-bracket placeholders such as <id-or-empty>.",
            "- For each TARGET_FILE include PROBLEM, EVIDENCE, IMPLEMENTATION_CHANGES, VALIDATION_COMMANDS, RISKS and EXIT_DECISION.",
            "- If no concrete target is patchable from current evidence, return EXIT_DECISION=NO_PATCHABLE_TARGET with explicit reason.",
            "- GPU1 may move backward on previous/refines/resume pointers to propagate imports, symbols, contracts and validation commands, then resume forward.",
            "- GPU0 and NPU vetoes are authoritative quality signals inside this heap loop.",
        ]
        if placeholder_hits:
            lines.append("- Placeholder hits to eliminate: " + ", ".join(placeholder_hits[:12]))
        if implementation_errors:
            lines.append(
                "- Implementation errors to resolve: " + " | ".join(implementation_errors[:8])
            )
        if progress_errors:
            lines.append("- Progress errors to resolve: " + " | ".join(progress_errors[:8]))
        if unverified_refs:
            lines.append(
                "- Rejected/non-allowlisted source refs blacklist: "
                + ", ".join(unverified_refs[:12])
            )
        if veto_reasons:
            lines.append("- Cross-lane veto reasons to resolve: " + " | ".join(veto_reasons[:8]))
        if candidates:
            lines.append("Allowed concrete source targets:")
            lines.extend(f"- {item}" for item in candidates[:18])
        return "\n".join(lines)

    def terminal_no_patchable_provider_loop(self) -> dict[str, Any]:
        """Detect repeated fake-path provider output that should stop revisions."""
        report = self.latest_proposal_iteration_report()
        if not report:
            return {}
        try:
            revision = int(report.get("revision") or 0)
        except (TypeError, ValueError):
            revision = 0
        if revision < 1:
            return {}

        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        progress = (
            report.get("proposal_progress")
            if isinstance(report.get("proposal_progress"), dict)
            else {}
        )
        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        response_text = str(report.get("response_text") or "")
        unverified = [
            str(item)
            for item in (
                quality.get("unverified_source_file_refs")
                or quality.get("unverified_file_refs")
                or []
            )
            if str(item).strip()
        ]
        repeated_unverified = [
            str(item)
            for item in (progress.get("repeated_unverified_source_refs") or [])
            if str(item).strip()
        ]
        progress_errors = [
            str(item) for item in (progress.get("errors") or []) if str(item).strip()
        ]
        implementation_errors = [
            str(item) for item in (implementation.get("errors") or []) if str(item).strip()
        ]
        placeholder_hits = [
            str(item)
            for item in (implementation.get("placeholder_hits") or [])
            if str(item).strip()
        ]
        haystack = "\n".join(
            [response_text, *unverified, *repeated_unverified, *progress_errors]
        ).lower()
        fake_path_detected = any(
            marker in haystack
            for marker in (
                "tools/.../real_existing_file.py",
                "tools\\...\\real_existing_file.py",
                "real_existing_file.py",
                "<id-or-empty>",
            )
        )
        repeated = bool(repeated_unverified) or any(
            "similarity=" in item.lower() or "too similar" in item.lower()
            for item in progress_errors
        )
        placeholder = bool(placeholder_hits) or any(
            marker in "\n".join(implementation_errors).lower()
            for marker in ("placeholder", "todo", "stub")
        )
        repeated_unverified_loop = bool(repeated_unverified) and repeated
        if not ((fake_path_detected and (repeated or placeholder)) or repeated_unverified_loop):
            return {}

        reason = (
            "terminal_no_patchable_target: repeated provider output used fake, "
            "placeholder or non-allowlisted source paths after deterministic feedback"
        )
        feedback = "\n".join(
            [
                "EXIT_DECISION=NO_PATCHABLE_TARGET",
                "BLOCKED_NO_VERIFIED_TARGET_REASON=" + reason,
                "Do not request another GPU1 rewrite for this same unresolved candidate.",
                "Preserve the rejected chunk as diagnostic evidence and return to deterministic operator review.",
            ]
        )
        return {
            "terminal_no_patchable_target": True,
            "revision": revision,
            "reason": reason,
            "unverified_source_file_refs": unverified,
            "repeated_unverified_source_refs": repeated_unverified,
            "progress_errors": progress_errors,
            "implementation_errors": implementation_errors,
            "placeholder_hits": placeholder_hits,
            "feedback": feedback,
        }

    def proposal_cycle_requires_refinement(self, text: str, events: list[dict[str, Any]]) -> bool:
        """Return True when the current heap proposal block still needs another GPU1 pass."""
        if not self.detailed_output_expected():
            return False
        if not str(text or "").strip():
            return True
        # Raw response quality still matters, but the accepted/rejected proposal
        # artifact is the authoritative same-heap decision because it includes
        # GPU0 review, NPU audit, progress checks and the parallel-cycle verdict.
        if not self.quality_output_passed(text, events):
            return True
        if self.proposal_iteration_artifacts() and not self.latest_proposal_quality_passed():
            return True
        return False

    def persist_current_gpu1_proposal_iteration(
        self,
        revision: int,
        events: list[dict[str, Any]],
        source: str,
    ) -> list[dict[str, Any]]:
        """Persist the current GPU1 response as a proposal block before quality exit."""
        text = self.response_text()
        if not text:
            return events
        self.write_proposal_iteration_artifact(
            revision,
            text,
            self.response_file_reference_quality(text),
            events,
            source=source,
        )
        updated_events = self.read_events()
        self.publish_shared_evidence_facts(revision, updated_events)
        return updated_events

    def maybe_run_provider_quality_revisions(
        self, round_id: int, events: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        while (
            self.detailed_output_expected()
            and self.provider_revision_count < int(getattr(self.args, "max_provider_revisions", 0))
            and self.proposal_cycle_requires_refinement(self.response_text(), events)
        ):
            terminal = self.terminal_no_patchable_provider_loop()
            if terminal:
                self.provider_revision_feedback = str(terminal.get("feedback") or "")
                self.publish(
                    "deterministic",
                    "validation_signal",
                    {
                        "id": f"{self.stamp}:provider_revision_terminal_no_patchable",
                        **terminal,
                    },
                    target="gpu1",
                    correlation_id=f"{self.stamp}:terminal-no-patchable",
                    round_id=round_id,
                )
                self.append_heap_exchange_event(
                    {
                        "kind": "provider_revision_terminal_no_patchable_target",
                        "lane": "deterministic_audit",
                        "round": round_id,
                        "revision": terminal.get("revision"),
                        "summary": terminal.get("reason"),
                    }
                )
                break
            self.provider_revision_count += 1
            previous_veto_feedback = self.provider_revision_feedback.strip()
            quality_feedback = self.build_quality_failure_feedback(self.response_text(), events)
            self.provider_revision_feedback = "\n\n".join(
                part for part in (previous_veto_feedback, quality_feedback) if part
            )
            self.publish(
                "deterministic",
                "validation_signal",
                {
                    "id": f"{self.stamp}:product_quality_failure:{self.provider_revision_count}",
                    "revision": self.provider_revision_count,
                    "feedback": self.provider_revision_feedback,
                    "file_quality": self.response_file_reference_quality(self.response_text()),
                },
                target="gpu1",
                correlation_id=f"{self.stamp}:quality-revision:{self.provider_revision_count}",
                round_id=round_id,
            )
            self.append_heap_exchange_event(
                {
                    "kind": "product_quality_failure",
                    "lane": "deterministic_audit",
                    "round": round_id,
                    "revision": self.provider_revision_count,
                    "summary": self.provider_revision_feedback[:500],
                }
            )
            self.run_provider_teamwork(round_id, revision=self.provider_revision_count)
            events = self.read_events()
            revised_text = self.response_text()
            revised_quality = self.response_file_reference_quality(revised_text)
            if revised_text:
                self.write_proposal_iteration_artifact(
                    self.provider_revision_count,
                    revised_text,
                    revised_quality,
                    events,
                    source="gpu1_revision",
                )
            self.publish_shared_evidence_facts(round_id, events)
        return events

    def startup_context_digest(self, max_chars: int = 36000) -> str:
        """Build a bounded digest of startup context artifacts for GPU1.

        The startup reload already creates tool catalog, memory inventory,
        operational memory search, transient context, semantic chunks and the
        heap task file. This digest turns those refs into active GPU1 context
        without treating the whole universe as one unbounded argv string.
        """
        manifest_path, manifest = self.startup_manifest_from_task_file()
        if not manifest:
            return ""

        artifacts = manifest.get("artifacts") if isinstance(manifest.get("artifacts"), dict) else {}
        preferred_keys = (
            "heap_task_file",
            "shared_context_markdown",
            "shared_memory_markdown",
            "operational_memory_search_markdown",
            "tool_catalog_markdown",
            "semantic_code_chunks_markdown",
            "semantic_evidence_chunks_markdown",
            "ai_context_pack_markdown",
            "ai_context_pack_evidence_markdown",
            "repo_docs_map_markdown",
            "required_context_files_markdown",
        )

        sections: list[str] = []
        remaining = max(1000, int(max_chars))
        for key in preferred_keys:
            value = artifacts.get(key)
            if not isinstance(value, str) or not value.strip():
                continue
            path = self.repo_root / value
            if not path.exists() or not path.is_file():
                continue
            try:
                content = path.read_text(encoding="utf-8-sig")
            except Exception as exc:  # noqa: BLE001 - context digest must not crash heap.
                sections.append(f"## {key}\n- unreadable: {value}: {type(exc).__name__}: {exc}\n")
                continue

            header = f"## {key}\nsource: {value}\n\n"
            budget = max(0, remaining - len(header) - 128)
            if budget <= 0:
                break
            chunk = content[:budget]
            if len(content) > budget:
                chunk += "\n\n...[truncated by startup_context_digest]...\n"
            sections.append(header + chunk)
            remaining -= len(sections[-1])
            if remaining <= 0:
                break

        if not sections:
            return ""
        return (
            "STARTUP_CONTEXT_DIGEST_FOR_GPU1:\n"
            "Use this as active heap context. Prefer exact repo-relative paths and concrete validation commands.\n\n"
            + "\n\n".join(sections)
        )

    def gpu1_provider_prompt(self) -> str:
        """GPU1 prompt enriched with startup context digest."""
        base = self.gpu1_request_prompt()
        digest = self.startup_context_digest()
        pointer_protocol = (
            "HEAP_POINTER_DELTA_PROTOCOL:\n"
            "- Non produrre una soluzione totale se il problema e' ampio. Produci il prossimo delta concreto.\n"
            "- Ogni revisione deve dichiarare POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET.\n"
            "- Se introduci import, simboli, schema field, CLI flag o contratti, crea PROPAGATION_TASKS e usa BACKTRACK_PROPAGATE.\n"
            "- Dopo la propagazione torna avanti con RESUME_FORWARD usando resume_from_block_id.\n"
            "- Usa BACKLOG_TASKS per il lavoro successivo; il pointer graph mantiene memoria e contesto.\n"
            "- GPU1 puo' iterare su proposal chunks gia' scritti: se sono corretti ma poveri, non scartarli; arricchiscili con copertura repo, criteri di accettazione, validazioni, rischi e confini di apply.\n"
            "- La ricchezza finale nasce da COMPOSE/REFINE di piu' pezzi persistenti; ogni revisione deve dichiarare se estende un chunk precedente o crea un nuovo delta.\n"
            "- GPU0 deve verificare path/diff/validazione del delta; NPU deve auditare guardrail e placeholder.\n"
            "- Il delta corrente deve contenere TARGET_FILES repo-relative reali, PATCH_SKETCH e VALIDATION_COMMANDS.\n"
            "- TARGET_FILES e diff header devono usare solo path nella SOURCE_PATH_ALLOWLIST_CONTRACT.\n"
            "- Se nessun path allowlisted e' patchabile, usa EXIT_DECISION=NO_PATCHABLE_TARGET e spiega BLOCKED_NO_VERIFIED_TARGET_REASON.\n"
            "- Non usare mai placeholder angle-bracket come <id-or-empty>; usa valori vuoti o block id reali.\n"
            "- Se candidate_applicability_flags contiene invented_source_path, unresolved_pointer_placeholder o unresolved_angle_bracket_token, tratta candidate_response_preview come esempio negativo e non copiarne TARGET_FILES/PATCH_SKETCH.\n"
            "- Non ripetere blocchi gia' rigettati e non generare overview documentale.\n"
        )
        if not digest:
            return "\n\n".join([base, pointer_protocol])
        return "\n\n".join([base, pointer_protocol, digest])

    def write_provider_prompt_file(self, prompt: str, revision: int) -> str:
        """Persist the large GPU1 provider prompt and return repo-relative path."""
        prompt_dir = self.runtime_context_dir() / "provider_prompts"
        prompt_dir.mkdir(parents=True, exist_ok=True)
        prompt_path = prompt_dir / f"gpu1_provider_prompt_revision_{revision:03d}.md"
        prompt_path.write_text(prompt.rstrip() + "\n", encoding="utf-8")
        return repo_rel(self.repo_root, prompt_path)

    def provider_command_with_prompt_file(
        self, command: list[Any], revision: int
    ) -> tuple[list[str], str]:
        """Move run_local_provider_probe --prompt payload into --prompt-file."""
        normalized = [str(part) for part in command]
        script_hit = any(
            part.replace("\\", "/").endswith("tools/ai/run_local_provider_probe.py")
            for part in normalized
        )
        if not script_hit or "--prompt" not in normalized:
            return normalized, ""

        index = normalized.index("--prompt")
        if index + 1 >= len(normalized):
            return normalized, ""

        prompt = normalized[index + 1]
        if not prompt.strip():
            return normalized, ""

        prompt_file = self.write_provider_prompt_file(prompt, revision)
        rewritten = normalized[:index] + normalized[index + 2 :]
        rewritten.extend(["--prompt-file", prompt_file])
        return rewritten, prompt_file

    def command_line_char_count(self, command: list[Any]) -> int:
        """Approximate Windows command-line length for subprocess argv."""
        return sum(len(str(part)) + 3 for part in command)

    def provider_command_for_windows(
        self, command: list[Any], revision: int
    ) -> tuple[list[str], str]:
        """Shorten oversized provider invocations on Windows.

        Windows CreateProcess fails with WinError 206 when argv becomes too long.
        Provider feedback/context can legitimately grow across heap revisions, so
        keep the real provider argv in a generated Python wrapper file and launch
        only that wrapper. This preserves the configured project Python and does
        not alter provider CLI contracts.
        """
        normalized_command = [str(part) for part in command]
        if os.name != "nt":
            return normalized_command, ""
        if self.command_line_char_count(normalized_command) < 24000:
            return normalized_command, ""
        if len(normalized_command) < 2:
            return normalized_command, ""

        wrapper_dir = self.runtime_context_dir() / "provider_invocations"
        wrapper_dir.mkdir(parents=True, exist_ok=True)
        wrapper_path = wrapper_dir / f"provider_teamwork_invocation_revision_{revision:03d}.py"

        child_argv = normalized_command[1:]
        wrapper_text = (
            "from __future__ import annotations\n"
            "import json\n"
            "import runpy\n"
            "import sys\n"
            "from pathlib import Path\n\n"
            f"repo_root = Path({str(self.repo_root)!r})\n"
            "if str(repo_root) not in sys.path:\n"
            "    sys.path.insert(0, str(repo_root))\n"
            f"child_argv = json.loads({json.dumps(child_argv, ensure_ascii=False)!r})\n"
            "script = Path(child_argv[0])\n"
            "if not script.is_absolute():\n"
            "    script = repo_root / script\n"
            "sys.argv = [str(script), *child_argv[1:]]\n"
            "runpy.run_path(str(script), run_name='__main__')\n"
        )
        wrapper_path.write_text(wrapper_text, encoding="utf-8")
        return [normalized_command[0], str(wrapper_path)], repo_rel(self.repo_root, wrapper_path)

    def extract_text_from_provider_json(self, payload: dict[str, Any]) -> str:
        """Extract provider response text from heterogeneous provider reports."""
        if not isinstance(payload, dict):
            return ""
        direct = payload.get("response_text") or payload.get("text") or payload.get("stdout_tail")
        if isinstance(direct, str) and direct.strip():
            return direct.strip()
        for item in payload.get("lane_reports") or []:
            if not isinstance(item, dict):
                continue
            value = item.get("response_text") or item.get("text_preview") or item.get("raw_preview")
            if isinstance(value, str) and value.strip():
                return value.strip()
        return ""

    def gpu1_delta_report_path(self, work_dir: Path, revision: int) -> Path:
        if revision <= 0:
            return work_dir / "gpu1_ollama_provider_probe.json"
        return work_dir / f"gpu1_ollama_provider_probe_revision{revision}.json"

    def gpu1_delta_text_for_revision(self, work_dir: Path, revision: int) -> str:
        """Return the GPU1 delta text for the current provider teamwork cycle."""
        payload = read_json(self.gpu1_delta_report_path(work_dir, revision))
        text = self.extract_text_from_provider_json(payload)
        if text:
            return text
        for report in reversed(self.provider_reports):
            if str(report.get("lane") or "") == "gpu1_planner":
                text = str(report.get("response_text") or "").strip()
                if text:
                    return text
        return self.response_text()

    def section_presence(self, text: str, names: tuple[str, ...]) -> dict[str, bool]:
        lowered = (text or "").lower()
        return {name: name.lower() in lowered for name in names}

    def enrich_provider_report_with_operational_peer_review(
        self,
        provider_report: dict[str, Any],
        lane: str,
        work_dir: Path,
        revision: int,
        events: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Make GPU0/NPU reports operational peers, not only hardware probes.

        The hardware workload remains useful evidence, but the heap needs peer
        cognition on the current GPU1 delta. This function binds GPU0 and NPU to
        the GPU1 proposal text of the same revision and appends a structured
        review/audit into the provider report consumed by the composer.
        """
        if lane not in {"gpu0_peer", "npu_micro_task_auditor"}:
            return provider_report

        delta_text = self.gpu1_delta_text_for_revision(work_dir, revision)
        sections = self.section_presence(
            delta_text,
            (
                "HEAP_DELTA_PROPOSAL",
                "EXIT_DECISION=",
                "POINTER_ACTION=",
                "CURRENT_POINTER",
                "CURRENT_ITERATION_SCOPE",
                "TARGET_FILES",
                "PROBLEM",
                "EVIDENCE",
                "IMPLEMENTATION_CHANGES",
                "PROPAGATION_TASKS",
                "BACKLOG_TASKS",
                "PATCH_SKETCH",
                "VALIDATION_COMMANDS",
                "RISKS",
            ),
        )
        missing = [name for name, present in sections.items() if not present]
        file_quality = self.response_file_reference_quality(delta_text)
        events = self.read_events()
        no_patchable_target_forced = False
        unverified_source_refs = list(
            file_quality.get("unverified_source_file_refs")
            or file_quality.get("unverified_file_refs")
            or []
        )
        request_text = self.request_text()
        no_patchable_requested = (
            "NO_PATCHABLE_TARGET" in request_text
            or "BLOCKED_NO_VERIFIED_TARGET_REASON" in request_text
        )
        if (
            no_patchable_requested
            and file_quality.get("passed") is not True
            and unverified_source_refs
        ):
            sanitized_refs = [
                str(ref).replace(".", "[dot]").replace("/", " / ")
                for ref in unverified_source_refs[:12]
            ]
            delta_text = "\n".join(
                [
                    "# HEAP_DELTA_PROPOSAL",
                    "EXIT_DECISION=NO_PATCHABLE_TARGET",
                    "POINTER_ACTION=STAY_FORWARD",
                    "CURRENT_POINTER:",
                    "- previous_block_id=",
                    "- refines_block_id=",
                    "- resume_from_block_id=",
                    "",
                    "CURRENT_ITERATION_SCOPE:",
                    "- Deterministic heap guardrail converted a provider proposal because it referenced source paths that are not verified repo-relative targets.",
                    "",
                    "BLOCKED_NO_VERIFIED_TARGET_REASON:",
                    "- Provider output referenced source paths that failed SOURCE_PATH_ALLOWLIST_CONTRACT.",
                    "- No verified repo-relative source target remained patchable after deterministic file-reference validation.",
                    "- Suppressed unverified source refs: "
                    + (", ".join(sanitized_refs) if sanitized_refs else "none"),
                    "",
                    "PATCH_DECISION:",
                    "- No patch generated.",
                    "- No fake diff emitted.",
                    "- No source writes performed.",
                    "",
                    "VALIDATION_COMMANDS:",
                    "- Not applicable: no verified target file exists for this proposal.",
                ]
            )
            coerced_file_quality = self.response_file_reference_quality(delta_text)
            coerced_file_quality.update(
                {
                    "passed": True,
                    "no_patchable_target_declared": True,
                    "coerced_from_invented_source_path": True,
                    "suppressed_unverified_source_refs": unverified_source_refs,
                    "blocked_no_verified_target_reason": (
                        "provider proposal referenced non-allowlisted source paths"
                    ),
                }
            )
            file_quality = coerced_file_quality
            no_patchable_target_forced = True
        implementation_quality = self.implementation_quality_report(delta_text, events)
        if no_patchable_target_forced:
            implementation_quality.update(
                {
                    "required": False,
                    "passed": True,
                    "errors": [],
                    "no_patchable_target_declared": True,
                    "coerced_from_invented_source_path": True,
                }
            )
        pointer_action_match = re.search(
            r"(?im)^\\s*POINTER_ACTION\\s*=\\s*([^\\n\\r]+)", delta_text or ""
        )
        pointer_action = pointer_action_match.group(1).strip() if pointer_action_match else ""

        if lane == "gpu0_peer":
            review_lines = [
                "GPU0 operational peer review:",
                f"- revision={revision}",
                f"- pointer_action={pointer_action or 'missing'}",
                f"- target_files_verified={bool(file_quality.get('existing_source_file_refs'))}",
                f"- file_quality_passed={file_quality.get('passed')}",
                f"- implementation_quality_passed={implementation_quality.get('passed')}",
                f"- missing_delta_sections={missing}",
                "- decision="
                + (
                    "accept_delta_shape_for_next_audit"
                    if not missing
                    and file_quality.get("passed")
                    and implementation_quality.get("passed")
                    else "reject_until_concrete_repo_relative_delta"
                ),
            ]
            provider_report["gpu0_operational_review"] = {
                "performed": True,
                "revision": revision,
                "pointer_action": pointer_action,
                "missing_delta_sections": missing,
                "file_quality": file_quality,
                "implementation_quality": implementation_quality,
                "decision": (
                    "accept_delta_shape_for_next_audit"
                    if not missing
                    and file_quality.get("passed")
                    and implementation_quality.get("passed")
                    else "reject_until_concrete_repo_relative_delta"
                ),
            }
        else:
            placeholder_hits = implementation_quality.get("placeholder_hits") or []
            forbidden_claims = []
            lowered = (delta_text or "").lower()
            for marker in (
                "source_writes_performed: true",
                '"source_writes_performed": true',
                "patch_application_performed: true",
                '"patch_application_performed": true',
            ):
                if marker in lowered:
                    forbidden_claims.append(marker)
            review_lines = [
                "NPU operational guardrail audit:",
                f"- revision={revision}",
                f"- pointer_action={pointer_action or 'missing'}",
                f"- placeholder_hits={placeholder_hits}",
                f"- forbidden_runtime_claims={forbidden_claims}",
                f"- validation_commands_present={'VALIDATION_COMMANDS' in (delta_text or '')}",
                "- decision="
                + (
                    "accept_guardrails"
                    if not placeholder_hits
                    and not forbidden_claims
                    and "VALIDATION_COMMANDS" in (delta_text or "")
                    else "reject_until_guardrails_and_validation_are_concrete"
                ),
            ]
            provider_report["npu_operational_audit"] = {
                "performed": True,
                "revision": revision,
                "pointer_action": pointer_action,
                "placeholder_hits": placeholder_hits,
                "forbidden_runtime_claims": forbidden_claims,
                "validation_commands_present": "VALIDATION_COMMANDS" in (delta_text or ""),
                "decision": (
                    "accept_guardrails"
                    if not placeholder_hits
                    and not forbidden_claims
                    and "VALIDATION_COMMANDS" in (delta_text or "")
                    else "reject_until_guardrails_and_validation_are_concrete"
                ),
            }

        previous_text = str(provider_report.get("response_text") or "").strip()
        provider_report["response_text"] = "\\n".join(
            part for part in (previous_text, "\\n".join(review_lines)) if part
        )
        provider_report["operational_peer_review_performed"] = True
        provider_report["operational_peer_review_source"] = repo_rel(
            self.repo_root, self.gpu1_delta_report_path(work_dir, revision)
        )
        return provider_report

    def run_provider_teamwork(self, round_id: int, revision: int = 0) -> None:
        if self.provider_reports and revision <= 0:
            return

        work_dir = self.provider_work_dir()
        timeout_seconds = max(30, self.args.timeout_seconds)
        prepared: list[dict[str, Any]] = []

        for spec in self.provider_command_specs(work_dir, revision=revision):
            lane = str(spec["lane"])
            requirement = str(spec["requirement"])
            correlation = f"{self.stamp}:provider:{requirement}"

            self.publish(
                provider_heap_lane(lane),
                "provider_state",
                {
                    "id": correlation,
                    "lane": lane,
                    "role": spec.get("role"),
                    "requirement": requirement,
                    "revision": revision,
                    "status": "running",
                    "output": repo_rel(self.repo_root, Path(spec["output"])),
                    "execution_mode": "concurrent_provider_teamwork",
                },
                target="orchestrator",
                correlation_id=correlation,
                round_id=round_id,
            )

            command = [
                (self.gpu1_provider_prompt() if item == "__GPU1_CUMULATIVE_PROMPT__" else item)
                for item in spec["command"]
            ]
            try:
                command, provider_prompt_file = self.provider_command_with_prompt_file(
                    command, revision
                )
                if provider_prompt_file:
                    self.warnings.append(
                        f"provider GPU1 prompt written to prompt-file={provider_prompt_file}"
                    )

                command, provider_command_wrapper = self.provider_command_for_windows(
                    command, revision
                )
                if provider_command_wrapper:
                    self.warnings.append(
                        f"provider command exceeded Windows argv limit; executed wrapper={provider_command_wrapper}"
                    )

                process = subprocess.Popen(
                    command,
                    cwd=self.repo_root,
                    env=command_env(self.repo_root),
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                prepared.append(
                    {
                        "spec": spec,
                        "lane": lane,
                        "requirement": requirement,
                        "correlation": correlation,
                        "command": command,
                        "process": process,
                        "completed": None,
                    }
                )
            except Exception as exc:  # noqa: BLE001 - provider lane failure becomes report evidence.
                prepared.append(
                    {
                        "spec": spec,
                        "lane": lane,
                        "requirement": requirement,
                        "correlation": correlation,
                        "command": command,
                        "process": None,
                        "completed": subprocess.CompletedProcess(
                            command,
                            returncode=127,
                            stdout="",
                            stderr=f"{type(exc).__name__}: {exc}",
                        ),
                    }
                )

        for item in prepared:
            spec = item["spec"]
            lane = str(item["lane"])
            requirement = str(item["requirement"])
            correlation = str(item["correlation"])
            command = list(item["command"])
            process = item.get("process")
            completed = item.get("completed")

            if completed is None and process is not None:
                try:
                    stdout, stderr = process.communicate(timeout=timeout_seconds)
                    completed = subprocess.CompletedProcess(
                        command,
                        returncode=process.returncode,
                        stdout=stdout or "",
                        stderr=stderr or "",
                    )
                except subprocess.TimeoutExpired:
                    process.kill()
                    stdout, stderr = process.communicate()
                    completed = subprocess.CompletedProcess(
                        command,
                        returncode=124,
                        stdout=stdout or "",
                        stderr=(stderr or "") + "\nprovider timeout",
                    )

            if completed is None:
                completed = subprocess.CompletedProcess(
                    command,
                    returncode=127,
                    stdout="",
                    stderr="provider process was not started and no completed process was recorded",
                )

            report_data = read_json(Path(spec["output"]))
            provider_report = self.summarize_provider_report(spec, completed, report_data)
            provider_report["status"] = "ready" if provider_report.get("passed") else "degraded"
            events = self.read_events()
            provider_report = self.enrich_provider_report_with_operational_peer_review(
                provider_report,
                lane,
                work_dir,
                revision,
                events,
            )
            provider_report["execution_mode"] = "concurrent_provider_teamwork"
            provider_report["revision"] = revision

            self.provider_reports.append(provider_report)
            append_unique(self.state["provider_results"], provider_report, key="requirement")
            self.publish(
                provider_heap_lane(lane),
                "telemetry_signal",
                provider_report,
                target="orchestrator",
                correlation_id=correlation,
                round_id=round_id,
            )
            self.append_heap_exchange_event(
                {
                    "kind": "provider_output",
                    "lane": lane,
                    "round": round_id,
                    "requirement": requirement,
                    "revision": revision,
                    "execution_mode": "concurrent_provider_teamwork",
                    "passed": provider_report.get("passed"),
                    "provider_execution_performed": provider_report.get(
                        "provider_execution_performed"
                    ),
                    "source_file": provider_report.get("output"),
                    "summary": str(provider_report.get("response_text") or "")[:500],
                }
            )
            claim = {
                "id": f"{requirement}_claim",
                "from": lane,
                "claim": (
                    "provider lane contributed usable heap evidence"
                    if provider_report.get("passed")
                    else "provider lane did not produce usable heap evidence"
                ),
                "confidence": 0.88 if provider_report.get("passed") else 0.35,
                "requirement": requirement,
                "evidence_ref": provider_report.get("output"),
                "provider_execution_performed": provider_report.get("provider_execution_performed"),
                "observed_request": self.request_text(),
                "observed_response": provider_report.get("response_text") or self.response_text(),
                "execution_mode": "concurrent_provider_teamwork",
            }
            append_unique(self.state["claims"], claim)
            self.publish(
                provider_heap_lane(lane),
                "claim",
                claim,
                target="deterministic",
                correlation_id=f"{correlation}:claim",
                round_id=round_id,
            )

    def run(self) -> dict[str, Any]:
        self.bootstrap()
        last_round = 0
        for round_id in range(1, self.max_iterations + 1):
            last_round = round_id
            events = self.read_events()
            self.planner_step(round_id, events)
            if self.heap.pending_broker_requests():
                self.run_bridge()
            events = self.read_events()
            self.publish_shared_evidence_facts(round_id, events)
            if self.base_requirements_complete(events) and not self.provider_reports:
                self.run_provider_teamwork(round_id)
                events = self.read_events()
                self.publish_shared_evidence_facts(round_id, events)
                if self.detailed_output_expected() and self.response_text():
                    events = self.persist_current_gpu1_proposal_iteration(
                        revision=0,
                        events=events,
                        source="gpu1_initial",
                    )
            if self.base_requirements_complete(events) and self.provider_reports:
                events = self.maybe_run_provider_quality_revisions(round_id, events)
            self.critic_step(round_id, events)
            self.arbiter_step(round_id, events)
            if self.state["product"].get("status") in {
                "ready",
                "blocked_with_reason",
            } and self.minimum_runtime_depth_satisfied(round_id):
                break
        if self.state["product"].get("status") == "not_ready":
            events = self.read_events()
            self.arbiter_step(last_round or self.max_iterations, events)
        snapshot = self.heap.write_snapshot()
        runtime_state = safe_dict(snapshot.get("runtime_state"))
        lane_gate = runtime_state_lane_gate(
            safe_dict(runtime_state.get("lane_status")),
            self.args.max_degraded_lanes,
        )
        record_lane_diagnostic(
            self.heap,
            "orchestrator",
            "ready" if lane_gate["passed"] else "failed",
            "Runtime lane status tolerance evaluated.",
            lane_gate,
            correlation_id=f"{self.stamp}:runtime-state-gate",
        )
        snapshot = self.heap.write_snapshot()
        final_events = self.read_events()
        if self.detailed_output_expected():
            final_revision = max(0, int(self.provider_revision_count))
            final_provider_text = self.response_text()
            if final_provider_text:
                self.write_proposal_iteration_artifact(
                    final_revision,
                    final_provider_text,
                    self.response_file_reference_quality(final_provider_text),
                    final_events,
                    source="gpu1_final",
                )
                final_events = self.read_events()
        completed = sorted(self.completed_requirements(final_events))
        missing = self.missing_requirements(final_events)
        final_bridge_reports = self.bridge_report_refs(final_events)
        final_tool_request_count = self.effective_tool_request_count(final_events)
        final_tool_execution_count = self.effective_tool_execution_count(final_events)
        final_response_text = self.build_final_response_text(final_events)
        final_quality_signals = self.quality_output_signals(final_response_text, final_events)
        metrics = {
            "heap_read_count": self.heap_read_count,
            "heap_write_count": self.heap_write_count,
            "tool_request_count": final_tool_request_count,
            "tool_execution_count": final_tool_execution_count,
            "decision_count": self.decision_count,
            "candidate_operation_count": self.candidate_operation_count,
            "product_status": self.state["product"].get("status"),
            "budget_decision": self.budget_governor.get("decision"),
            "budget_max_iterations": self.max_iterations,
            "completed_requirement_count": len(completed),
            "required_requirement_count": len(self.required_requirements_order()),
            "completed_requirements": completed,
            "missing_requirements": missing,
            "request_input": self.request_text(),
            "response_text": final_response_text,
            "provider_raw_response_text": self.response_text(),
            "response_source": self.response_source(),
            "response_text_present": bool(final_response_text),
            "detailed_output_expected": self.detailed_output_expected(),
            "quality_output_passed": self.quality_output_passed(final_response_text, final_events),
            "quality_output_signals": final_quality_signals,
            "virtual_dev_environment_required": self.virtual_dev_environment_required(),
            "virtual_dev_environment_passed": self.virtual_dev_environment_passed(final_events),
            "virtual_dev_environment_reports": self.virtual_dev_environment_reports(final_events),
            "code_execution_matrix_required": self.code_execution_matrix_required(),
            "code_execution_matrix_passed": self.code_execution_matrix_passed(final_events),
            "code_execution_matrix_reports": self.code_execution_matrix_reports(final_events),
            "runtime_debug_lab_required": self.runtime_debug_lab_required(),
            "runtime_debug_lab_passed": self.runtime_debug_lab_passed(final_events),
            "runtime_debug_lab_reports": self.runtime_debug_lab_reports(final_events),
            "proposal_iteration_artifacts": self.proposal_iteration_artifacts(),
            "historical_tool_context_refs": self.historical_tool_context_files(),
            "response_file_reference_quality": self.response_file_reference_quality(
                self.response_text()
            ),
            "provider_refs": self.provider_refs(),
            "provider_response_texts": self.provider_response_texts(),
            "context_artifact_refs": self.broker_output_refs(final_events),
            "shared_evidence_count": len(self.state["shared_evidence"]),
            "shared_memory_evidence_count": 1 if "shared_memory" in completed else 0,
            "shared_context_chunk_evidence_count": (
                1 if "shared_context_chunks" in completed else 0
            ),
            "semantic_code_chunk_evidence_count": (1 if "semantic_code_chunks" in completed else 0),
            "ai_context_pack_evidence_count": (1 if "ai_context_pack" in completed else 0),
            "semantic_evidence_chunk_count": (1 if "semantic_evidence_chunks" in completed else 0),
            "operational_memory_write_count": (1 if "operational_memory_write" in completed else 0),
            "operational_memory_search_count": (
                1 if "operational_memory_search" in completed else 0
            ),
            "tool_catalog_evidence_count": 1 if "tool_catalog" in completed else 0,
            "validation_evidence_count": 1 if "validation_evidence" in completed else 0,
            "virtual_dev_environment_count": (1 if "virtual_dev_environment" in completed else 0),
            "code_execution_matrix_count": (1 if "code_execution_matrix" in completed else 0),
            "gpu1_provider_evidence_count": (1 if "gpu1_provider_planner" in completed else 0),
            "gpu0_provider_evidence_count": (1 if "gpu0_provider_peer" in completed else 0),
            "npu_micro_task_evidence_count": (1 if "npu_micro_task_auditor" in completed else 0),
            "provider_result_count": len(self.provider_reports),
            "provider_revision_count": self.provider_revision_count,
            "provider_lane_count": len({item.get("lane") for item in self.provider_reports}),
            "provider_execution_performed": self.provider_execution_performed,
            "provider_teamwork_required": True,
            "budget_exhausted": bool(missing and (last_round >= self.max_iterations)),
            "invocation_contract_ready": bool(self.invocation_contract.get("passed")),
            "invocation_gate_decision": safe_dict(
                self.invocation_contract.get("real_run_gate")
            ).get("decision"),
            "runtime_state_lane_status": lane_gate["lane_status"],
            "runtime_state_degraded_lanes": lane_gate["degraded_lanes"],
            "runtime_state_degraded_lane_count": lane_gate["degraded_lane_count"],
            "max_degraded_lanes": lane_gate["max_degraded_lanes"],
            "runtime_state_gate_passed": lane_gate["passed"],
        }
        exit_output_product = self.write_exit_output_product(
            final_response_text, final_events, metrics
        )
        heap_exchange_exit_product = self.build_heap_exchange_exit_product(
            require_concrete_product=metrics.get("product_status") == "ready"
        )
        metrics["heap_exchange_runtime_entry"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["runtime_entry"]
        )
        metrics["heap_exchange_runtime_state"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["runtime_state"]
        )
        metrics["heap_runtime_exit_output"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["exit_output"]
        )
        metrics["heap_exchange_runtime_exit_product"] = repo_rel(
            self.repo_root, self.heap_exchange_paths()["exit_product"]
        )
        metrics["heap_exchange_exit_passed"] = heap_exchange_exit_product.get("passed")
        metric_errors = []
        for key in (
            "heap_read_count",
            "heap_write_count",
            "tool_request_count",
            "tool_execution_count",
            "decision_count",
            "candidate_operation_count",
        ):
            if safe_int(metrics.get(key)) <= 0:
                metric_errors.append(f"{key} must be >0")
        if metrics["product_status"] not in {"ready", "blocked_with_reason"}:
            metric_errors.append("product_status must be ready or blocked_with_reason")
        if not lane_gate["passed"]:
            metric_errors.append(
                "runtime state degraded lane tolerance exceeded: "
                + ",".join(lane_gate["degraded_lanes"])
            )
        if metrics["product_status"] == "ready" and missing:
            metric_errors.append("ready product_status is forbidden while requirements are missing")
        if (
            metrics["product_status"] == "ready"
            and safe_int(metrics.get("provider_lane_count")) < 3
        ):
            metric_errors.append("ready product_status requires all three provider lanes")
        if metrics["product_status"] == "ready" and not self.provider_execution_performed:
            metric_errors.append("ready product_status requires observable provider execution")
        if metrics["product_status"] == "ready" and not final_bridge_reports:
            metric_errors.append("ready product_status requires broker bridge reports")
        if metrics["product_status"] == "ready" and not metrics.get("context_artifact_refs"):
            metric_errors.append("ready product_status requires memory/chunk/context artifacts")
        if metrics["product_status"] == "ready" and not self.response_text_complete():
            metric_errors.append("ready product_status requires a complete provider response_text")
        if (
            metrics["product_status"] == "ready"
            and self.detailed_output_expected()
            and not self.quality_output_passed(final_response_text, final_events)
        ):
            metric_errors.append(
                "ready product_status requires detailed heap/tool/provider quality output for complex requests"
            )
        if (
            metrics["product_status"] == "ready"
            and self.virtual_dev_environment_required()
            and not self.virtual_dev_environment_passed(final_events)
        ):
            metric_errors.append(
                "ready product_status requires virtual development environment passed for debug/runtime requests"
            )
        if (
            metrics["product_status"] == "ready"
            and self.code_execution_matrix_required()
            and not self.code_execution_matrix_passed(final_events)
        ):
            metric_errors.append(
                "ready product_status requires code execution matrix passed for coding requests"
            )
        if (
            metrics["product_status"] == "ready"
            and self.runtime_debug_lab_required()
            and not self.runtime_debug_lab_passed(final_events)
        ):
            metric_errors.append(
                "ready product_status requires runtime debug lab execution passed for MVP/lab requests"
            )
        self.errors.extend(metric_errors)
        return {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate",
            "generated_at": now_iso(),
            "repo_root": self.repo_root.as_posix(),
            "stamp": self.stamp,
            "passed": not self.errors,
            "metrics": metrics,
            "state": self.state,
            "budget_governor": self.budget_governor,
            "heap_snapshot": {
                "event_count": snapshot.get("event_count"),
                "event_log": snapshot.get("event_log"),
                "runtime_state": snapshot.get("runtime_state"),
                "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            },
            "bridge_reports": final_bridge_reports,
            "provider_reports": self.provider_reports,
            "heap_runtime_exit_output": exit_output_product,
            "heap_exchange_runtime_exit_product": heap_exchange_exit_product,
            "real_run_input_contract": {
                "kind": "heap_runtime_completeness_gate_input_contract",
                "task_file": self.args.task_file,
                "objective": self.args.objective,
                "request": self.request_text(),
                "stamp": self.stamp,
                "budget_minutes": self.args.budget_minutes,
                "max_iterations": self.max_iterations,
                "entry_files": [
                    "AGENTS.md",
                    "README.md",
                    *self.historical_tool_context_files(),
                ],
            },
            "real_run_output_contract": {
                "kind": "heap_runtime_completeness_gate_output_contract",
                "heap_event_log": snapshot.get("event_log"),
                "heap_snapshot": snapshot.get("snapshot"),
                "bridge_reports": final_bridge_reports,
                "provider_report_outputs": [item.get("output") for item in self.provider_reports],
                "request_input": self.request_text(),
                "response_text": final_response_text,
                "provider_raw_response_text": self.response_text(),
                "response_source": self.response_source(),
                "quality_output_signals": final_quality_signals,
                "response_file_reference_quality": self.response_file_reference_quality(
                    self.response_text()
                ),
                "virtual_dev_environment_required": metrics.get("virtual_dev_environment_required"),
                "virtual_dev_environment_passed": metrics.get("virtual_dev_environment_passed"),
                "virtual_dev_environment_reports": metrics.get("virtual_dev_environment_reports"),
                "runtime_debug_lab_required": metrics.get("runtime_debug_lab_required"),
                "runtime_debug_lab_passed": metrics.get("runtime_debug_lab_passed"),
                "runtime_debug_lab_reports": metrics.get("runtime_debug_lab_reports"),
                "code_execution_matrix_required": metrics.get("code_execution_matrix_required"),
                "code_execution_matrix_passed": metrics.get("code_execution_matrix_passed"),
                "code_execution_matrix_reports": metrics.get("code_execution_matrix_reports"),
                "proposal_iteration_artifacts": metrics.get("proposal_iteration_artifacts"),
                "heap_runtime_exit_output": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["exit_output"]
                ),
                "heap_exchange_runtime_exit_product": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["exit_product"]
                ),
                "heap_exchange_runtime_state": repo_rel(
                    self.repo_root, self.heap_exchange_paths()["runtime_state"]
                ),
                "provider_refs": self.provider_refs(),
                "provider_response_texts": self.provider_response_texts(),
                "context_artifact_refs": self.broker_output_refs(final_events),
                "product_status": self.state["product"].get("status"),
                "completed_requirements": completed,
                "missing_requirements": missing,
            },
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "errors": self.errors,
            "warnings": self.warnings,
            "guardrails": {
                "heap_completeness_gate": True,
                "provider_teamwork_universe_required": True,
                "provider_execution_performed": self.provider_execution_performed,
                "patch_application_performed": False,
                "source_writes_performed": False,
            },
        }

    def minimum_runtime_depth_satisfied(self, round_id: int) -> bool:
        min_rounds = max(1, int(getattr(self.args, "min_runtime_rounds", 1)))
        min_proposals = max(0, int(getattr(self.args, "min_proposal_iterations", 0)))
        proposal_json_count = len(
            [path for path in self.proposal_iteration_artifacts() if str(path).endswith(".json")]
        )
        return round_id >= min_rounds and proposal_json_count >= min_proposals


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Runtime Completeness Gate", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    metrics = safe_dict(report.get("metrics"))
    for key in (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "decision_count",
        "candidate_operation_count",
        "product_status",
        "completed_requirement_count",
        "required_requirement_count",
        "missing_requirements",
        "budget_exhausted",
        "budget_decision",
        "budget_max_iterations",
        "invocation_contract_ready",
        "invocation_gate_decision",
        "runtime_state_gate_passed",
        "runtime_state_degraded_lanes",
        "max_degraded_lanes",
    ):
        lines.append(f"- {key}: `{metrics.get(key)}`")
    product = safe_dict(safe_dict(report.get("state")).get("product"))
    lines.extend(
        [
            "",
            "## Product",
            "",
            f"- Status: `{product.get('status')}`",
            f"- Request: `{product.get('request_input')}`",
            f"- Response source: `{product.get('response_source')}`",
            f"- Response text: {product.get('response_text')}",
            f"- Reason: {product.get('reason')}",
        ]
    )
    lines.extend(["", "## Completed requirements", ""])
    for item in metrics.get("completed_requirements") or []:
        lines.append(f"- `{item}`")
    if metrics.get("missing_requirements"):
        lines.extend(["", "## Missing requirements", ""])
        for item in metrics.get("missing_requirements") or []:
            lines.append(f"- `{item}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument(
        "--objective",
        default="prove complete heap-driven teamwork loop over repository context, shared memory, brokered tools and all provider lanes",
    )
    parser.add_argument(
        "--request",
        default="",
        help="Optional real user request for heap heartbeat, e.g. ciao.",
    )
    parser.add_argument(
        "--request-file",
        default="",
        help="Read request text from file to avoid long Windows command lines.",
    )
    parser.add_argument(
        "--python-exe",
        default="",
        help="Explicit project Python executable for child tools. Defaults to repo .venv resolver; no system env fallback.",
    )
    parser.add_argument("--task-file", default="")
    parser.add_argument(
        "--tool",
        default="run_gpu_planner_json_contract_smoke",
        help="Compatibility flag; complete gate uses its internal readiness tool plan.",
    )
    parser.add_argument("--max-iterations", type=int, default=4)
    parser.add_argument("--min-runtime-rounds", type=int, default=1)
    parser.add_argument("--min-proposal-iterations", type=int, default=0)
    parser.add_argument(
        "--max-provider-revisions",
        type=int,
        default=2,
        help="Retry provider teamwork when exit quality fails before closing the heap.",
    )
    parser.add_argument("--budget-minutes", type=int, default=5)
    parser.add_argument("--max-rounds", type=int, default=4)
    parser.add_argument("--files-per-round", type=int, default=4)
    parser.add_argument("--max-context-files", type=int, default=40)
    parser.add_argument("--max-chars-per-file", type=int, default=4000)
    parser.add_argument("--max-new-tokens", type=int, default=1200)
    parser.add_argument("--keep-alive", default="10m")
    parser.add_argument("--npu-micro-start-mode", default="deferred")
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=60)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=60)
    parser.add_argument("--npu-max-context-chars", type=int, default=8000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=1200)
    parser.add_argument("--npu-max-new-tokens", type=int, default=384)
    parser.add_argument(
        "--allow-npu-device-workload",
        action="store_true",
        help="Opt in to a bounded real OpenVINO NPU micro workload for the NPU audit lane.",
    )
    parser.add_argument("--npu-device-workload-seconds", type=float, default=0.25)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=8)
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--operator-intent", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--provider-model", default="")
    parser.add_argument("--gpu0-iterations", type=int, default=16)
    parser.add_argument("--gpu0-min-seconds", type=float, default=0.1)
    parser.add_argument("--max-degraded-lanes", type=int, default=0)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--bridge-dir", default="")
    parser.add_argument("--bridge-output", default="")
    parser.add_argument("--bridge-markdown-output", default="")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate = HeapRuntimeCompletenessGate(args)
    report = gate.run()
    output = resolve_output_path(
        gate.repo_root,
        gate.path_arg(args.output, DEFAULT_OUTPUT).format(stamp=gate.stamp),
    )
    markdown = resolve_output_path(
        gate.repo_root,
        gate.path_arg(args.markdown_output, DEFAULT_MARKDOWN).format(stamp=gate.stamp),
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
