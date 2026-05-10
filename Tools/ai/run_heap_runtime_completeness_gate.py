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
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.heap_provider_budget_governor import ProviderBudgetConfig, build_heap_provider_budget_governor, clamp_loop_iterations
    from Tools.ai.heap_provider_invocation_contract import build_heap_provider_invocation_contract
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict, safe_int
    from Tools.ai.provider_mesh_runtime.python_runtime import command_env, resolve_child_python
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.heap_provider_budget_governor import ProviderBudgetConfig, build_heap_provider_budget_governor, clamp_loop_iterations  # type: ignore
    from Tools.ai.heap_provider_invocation_contract import build_heap_provider_invocation_contract  # type: ignore
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict, safe_int  # type: ignore
    from Tools.ai.provider_mesh_runtime.python_runtime import command_env, resolve_child_python  # type: ignore
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

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
    "shared_context_chunks",
    "validation_evidence",
    "gpu1_provider_planner",
    "gpu0_provider_peer",
    "npu_micro_task_auditor",
)

BASE_REQUIREMENTS = (
    "tool_catalog",
    "shared_memory",
    "shared_context_chunks",
    "validation_evidence",
)

PROVIDER_REQUIREMENTS = (
    "gpu1_provider_planner",
    "gpu0_provider_peer",
    "npu_micro_task_auditor",
)


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:  # noqa: BLE001 - report summarizer must not crash on partial artifacts.
        return {}
    return data if isinstance(data, dict) else {}



def make_state(objective: str, request: str = "") -> dict[str, Any]:
    return {
        "task": {"objective": objective, "status": "active"},
        "request": {"text": request.strip(), "status": "received" if request.strip() else "not_requested"},
        "budget_governor": {},
        "invocation_contract": {},
        "facts": [],
        "needs": [],
        "tool_requests": [],
        "shared_evidence": [],
        "provider_results": [],
        "claims": [],
        "decisions": [],
        "candidate_operations": [],
        "product": {"required": True, "status": "not_ready", "reason": "heap runtime completeness gate has not converged"},
    }


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


class HeapRuntimeCompletenessGate:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.repo_root = Path(args.repo_root).resolve()
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
        self.budget_governor = build_heap_provider_budget_governor(self.budget_config, requested_max_iterations=args.max_iterations)
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

    def tool_plan(self) -> list[dict[str, Any]]:
        return [
            {
                "requirement": "tool_catalog",
                "id": "tool-catalog-inventory",
                "tool": "build_agent_agnostic_tool_inventory",
                "args": {"root": ["Tools/ai", "Tools/validation", "Tools/workflow"]},
                "reason": "discover allowlisted project tools before deciding product readiness",
            },
            {
                "requirement": "shared_memory",
                "id": "shared-memory-inventory",
                "tool": "build_agent_memory_inventory",
                "args": {"objective": self.args.objective},
                "reason": "load read-only shared memory state into heap-visible evidence",
            },
            {
                "requirement": "shared_context_chunks",
                "id": "shared-request-context",
                "tool": "build_agent_transient_request_context",
                "args": {
                    "objective": self.args.objective,
                    "memory_note": [
                        "heap runtime completeness gate must prove tool, memory, context and validation evidence before product signal",
                        "budget/iterations define convergence and prevent endless repository loops",
                    ],
                    "raw_file": ["AGENTS.md", "README.md"],
                },
                "reason": "materialize request-scoped shared context/chunks from repository policy documents",
            },
            {
                "requirement": "validation_evidence",
                "id": "planner-json-contract-validation",
                "tool": "run_gpu_planner_json_contract_smoke",
                "args": {},
                "reason": "prove validation tool evidence is consumed before arbiter decision",
            },
        ]

    def read_events(self) -> list[dict[str, Any]]:
        self.heap_read_count += 1
        return self.heap.read_events()

    def publish(self, source: str, event_type: str, payload: dict[str, Any], *, target: str = "", correlation_id: str = "", round_id: int | None = None) -> None:
        self.heap.append_event(source=source, target=target or None, event_type=event_type, correlation_id=correlation_id or None, round_id=round_id, payload=payload)
        self.heap_write_count += 1

    def broker_results(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return event_payloads_by_type(events, "broker_result")

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
            requirement = self.requirement_for_tool(tool)
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
            requirement = self.requirement_for_tool(str(payload.get("tool") or ""))
            if requirement != "unknown":
                attempted.add(requirement)
        for provider_report in self.provider_reports:
            requirement = str(provider_report.get("requirement") or "")
            if requirement in PROVIDER_REQUIREMENTS:
                attempted.add(requirement)
        return attempted

    def missing_requirements(self, events: list[dict[str, Any]]) -> list[str]:
        completed = self.completed_requirements(events)
        return [item for item in REQUIREMENT_ORDER if item not in completed]

    def next_unattempted_plan_item(self, events: list[dict[str, Any]]) -> dict[str, Any] | None:
        attempted = self.attempted_requirements(events)
        for item in self.tool_plan():
            if item["requirement"] not in attempted:
                return item
        return None

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
            self.publish("deterministic", "fact", evidence, target="gpu1", correlation_id=f"{self.stamp}:shared:{requirement}", round_id=round_id)

    def bootstrap(self) -> None:
        self.publish("orchestrator", "task_state", self.state["task"], target="gpu1", correlation_id=f"{self.stamp}:task", round_id=0)
        if self.request_text():
            request_payload = {
                "id": f"{self.stamp}:user_request",
                "text": self.request_text(),
                "objective": self.args.objective,
                "expected_output": ["response_text", "response_source", "heap_event_refs", "provider_refs", "product_status"],
            }
            self.publish("orchestrator", "user_request", request_payload, target="gpu1", correlation_id=f"{self.stamp}:user_request", round_id=0)
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
            "required_events": safe_dict(self.invocation_contract.get("expected_telemetry_contract")).get("events_required", []),
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
            self.publish("deterministic", "fact", fact, target="gpu1", correlation_id=f"{self.stamp}:fact:{fact['id']}", round_id=0)
        self.heap.write_snapshot()

    def planner_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.heap.pending_broker_requests():
            return
        plan_item = self.next_unattempted_plan_item(events)
        if not plan_item:
            return
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
        self.publish("gpu1", "need", need, target="broker", correlation_id=request_id, round_id=round_id)
        tool_request = {
            "id": request_id,
            "tool": plan_item["tool"],
            "args": plan_item.get("args") or {},
            "reason": plan_item["reason"],
            "requirement": plan_item["requirement"],
        }
        append_unique(self.state["tool_requests"], tool_request)
        self.publish("gpu1", "broker_request", tool_request, target="broker", correlation_id=request_id, round_id=round_id)
        self.tool_request_count += 1

    def run_bridge(self) -> dict[str, Any]:
        bridge_json = resolve_output_path(self.repo_root, self.path_arg(self.args.bridge_output, DEFAULT_BRIDGE_JSON).format(stamp=self.stamp))
        bridge_md = resolve_output_path(self.repo_root, self.path_arg(self.args.bridge_markdown_output, DEFAULT_BRIDGE_MD).format(stamp=self.stamp))
        command = [
            resolve_child_python(self.repo_root),
            "Tools/ai/provider_runtime_heap_broker_bridge.py",
            "--repo-root", ".",
            "--stamp", self.stamp,
            "--events", repo_rel(self.repo_root, self.heap.paths.events),
            "--snapshot", repo_rel(self.repo_root, self.heap.paths.snapshot),
            "--heap-markdown", repo_rel(self.repo_root, self.heap.paths.markdown),
            "--bridge-dir", self.path_arg(self.args.bridge_dir, DEFAULT_BRIDGE_DIR),
            "--timeout-seconds", str(self.args.timeout_seconds),
            "--max-requests", "1",
            "--output", repo_rel(self.repo_root, bridge_json),
            "--markdown-output", repo_rel(self.repo_root, bridge_md),
        ]
        completed = subprocess.run(command, cwd=self.repo_root, env=command_env(self.repo_root), capture_output=True, text=True, check=False, timeout=self.args.timeout_seconds + 30)
        report = read_json(bridge_json)
        self.bridge_reports.append(repo_rel(self.repo_root, bridge_json))
        if completed.returncode != 0:
            self.errors.append(f"broker bridge returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}")
        self.tool_execution_count += safe_int(report.get("tool_execution_count"))
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
            "claim": "heap evidence complete" if not missing else "heap evidence still incomplete",
            "confidence": 0.95 if not missing else 0.78,
            "completed_requirements": completed,
            "missing_requirements": missing,
            "broker_result_count": len(broker_results),
            "tool_execution_count": self.tool_execution_count,
        }
        append_unique(self.state["claims"], claim)
        self.publish("npu", "claim", claim, target="gpu1", correlation_id=f"{self.stamp}:critic:{round_id}", round_id=round_id)
        self.publish("deterministic", "validation_signal", claim, target="gpu1", correlation_id=f"{self.stamp}:validation:{round_id}", round_id=round_id)

    def arbiter_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if self.state["decisions"]:
            return
        missing = self.missing_requirements(events)
        unattempted = self.next_unattempted_plan_item(events)
        ready = not missing
        if ready and self.request_text() and not self.response_text():
            missing = [*missing, "gpu1_request_response"]
            ready = False
        budget_exhausted = round_id >= self.max_iterations
        no_more_progress = unattempted is None and bool(missing)
        if not ready and not budget_exhausted and not no_more_progress:
            return
        status = "ready" if ready else "blocked_with_reason"
        decision = {
            "id": "heap_completeness_gate_decision",
            "from": "arbiter",
            "decision": "product_ready_heap_complete" if ready else "blocked_with_reason",
            "evidence_refs": ["heap:task_state", "heap:broker_result", "heap:shared_evidence", "heap:validation_signal", *self.bridge_reports[-4:]],
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "provider_generation_permit_allowed": self.budget_governor.get("permit_allowed"),
        }
        append_unique(self.state["decisions"], decision)
        self.decision_count += 1
        self.publish("deterministic", "decision", decision, target="orchestrator", correlation_id=f"{self.stamp}:decision", round_id=round_id)
        candidate = {
            "id": "candidate_heap_runtime_product_flow",
            "kind": "design_operation",
            "path": "Tools/workflow/run_unified_real_product_pr.ps1",
            "status": "ready_for_manual_review" if ready else "blocked",
            "rationale": "gate proves heap/tool/memory/context/validation convergence before product readiness" if ready else "gate blocked because heap completeness requirements were not all satisfied within budget",
            "missing_requirements": missing,
        }
        append_unique(self.state["candidate_operations"], candidate)
        self.candidate_operation_count += 1
        self.publish("deterministic", "candidate_operation", candidate, target="orchestrator", correlation_id=f"{self.stamp}:candidate", round_id=round_id)
        self.state["product"] = {
            "required": True,
            "status": status,
            "request_input": self.request_text(),
            "response_text": self.response_text(),
            "response_source": self.response_source(),
            "heap_event_refs": [repo_rel(self.repo_root, self.heap.paths.events)],
            "provider_refs": self.provider_refs(),
            "toolused": self.tool_execution_count > 0,
            "shared_memory_written_and_used": "shared_memory" in self.completed_requirements(events),
            "gpu0_audit": "observed response; no extra action required for casual request" if self.request_text() else "",
            "npu_audit": "no micro action needed for casual request" if self.request_text() else "",
            "reason": "heap loop consumed tool catalog, memory, context/chunks and validation evidence" if ready else "heap loop stopped by budget/failed requirement before readiness",
            "completed_requirements": sorted(self.completed_requirements(events)),
            "missing_requirements": missing,
            "budget_exhausted": budget_exhausted,
            "budget_governor": self.budget_governor.get("decision"),
        }
        self.publish("orchestrator", "product_signal", self.state["product"], correlation_id=f"{self.stamp}:product", round_id=round_id)


    def base_requirements_complete(self, events: list[dict[str, Any]]) -> bool:
        completed = self.completed_requirements(events)
        return all(requirement in completed for requirement in BASE_REQUIREMENTS)

    def provider_work_dir(self) -> Path:
        if self.output_dir:
            path = self.output_dir / "provider_teamwork"
        else:
            path = self.repo_root / "output" / "validation" / f"heap_runtime_provider_teamwork_{self.stamp}"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def request_text(self) -> str:
        return str(getattr(self.args, "request", "") or "").strip()

    def gpu1_request_prompt(self) -> str:
        request = self.request_text()
        if not request:
            return "Return exactly this JSON object and no prose: {\"ok\": true, \"lane\": \"ollama\"}"
        return (
            "Sei GPU1 planner nel runtime heap IA-Carmine. "
            "Rispondi direttamente alla richiesta utente in italiano, in modo breve. "
            "Non generare patch, non usare markdown, non descrivere il sistema. "
            f"Richiesta utente: {request}"
        )

    def response_text(self) -> str:
        for report in self.provider_reports:
            if report.get("lane") != "gpu1_planner":
                continue
            text = str(report.get("response_text") or "").strip()
            if text:
                return text
        return ""

    def response_source(self) -> str:
        return "gpu1_planner" if self.response_text() else ""

    def provider_refs(self) -> list[str]:
        refs: list[str] = []
        for report in self.provider_reports:
            output = str(report.get("output") or "")
            if output:
                refs.append(output)
        return refs

    def provider_command_specs(self, work_dir: Path) -> list[dict[str, Any]]:
        gpu1_json = work_dir / "gpu1_ollama_provider_probe.json"
        gpu0_json = work_dir / "gpu0_openvino_peer_workload.json"
        gpu0_md = work_dir / "gpu0_openvino_peer_workload.md"
        npu_json = work_dir / "npu_micro_task_auditor.json"
        npu_md = work_dir / "npu_micro_task_auditor.md"
        return [
            {
                "lane": "gpu1_planner",
                "requirement": "gpu1_provider_planner",
                "role": "primary_planner",
                "output": gpu1_json,
                "command": [
                    resolve_child_python(self.repo_root),
                    "Tools/ai/run_local_provider_probe.py",
                    "--repo-root", ".",
                    "--run-ollama",
                    "--model", self.args.provider_model,
                    "--prompt", self.gpu1_request_prompt(),
                    "--timeout", str(self.args.timeout_seconds),
                    "--output", repo_rel(self.repo_root, gpu1_json),
                ],
            },
            {
                "lane": "gpu0_peer",
                "requirement": "gpu0_provider_peer",
                "role": "diagnostic_peer_workload",
                "output": gpu0_json,
                "command": [
                    resolve_child_python(self.repo_root),
                    "Tools/ai/build_openvino_gpu0_workload_report.py",
                    "--repo-root", ".",
                    "--iterations", str(self.args.gpu0_iterations),
                    "--min-seconds", str(self.args.gpu0_min_seconds),
                    "--role", "heap_runtime_diagnostic_peer",
                    "--output", repo_rel(self.repo_root, gpu0_json),
                    "--markdown-output", repo_rel(self.repo_root, gpu0_md),
                ],
            },
            {
                "lane": "npu_micro_task_auditor",
                "requirement": "npu_micro_task_auditor",
                "role": "static_micro_task_auditor",
                "output": npu_json,
                "command": [
                    resolve_child_python(self.repo_root),
                    "Tools/ai/build_npu_micro_task_companion_report.py",
                    "--repo-root", ".",
                    "--task-file", self.args.task_file,
                    "--timeout-seconds", str(self.args.npu_micro_timeout_seconds),
                    "--max-context-chars", str(self.args.npu_max_context_chars),
                    "--output", repo_rel(self.repo_root, npu_json),
                    "--markdown-output", repo_rel(self.repo_root, npu_md),
                ],
            },
        ]

    def summarize_provider_report(self, spec: dict[str, Any], completed: subprocess.CompletedProcess[str], report_data: dict[str, Any]) -> dict[str, Any]:
        lane = str(spec["lane"])
        provider_execution = bool(
            report_data.get("provider_execution_performed")
            or report_data.get("openvino_gpu0_workload_performed")
            or report_data.get("openvino_gpu0_probe_performed")
        )
        if provider_execution:
            self.provider_execution_performed = True
        errors = report_data.get("errors") if isinstance(report_data.get("errors"), list) else []
        warnings = report_data.get("warnings") if isinstance(report_data.get("warnings"), list) else []
        response_text = ""
        lane_reports = report_data.get("lane_reports")
        if isinstance(lane_reports, list):
            for lane_report in lane_reports:
                if isinstance(lane_report, dict) and lane_report.get("lane") == "ollama":
                    response_text = str(lane_report.get("response_text") or lane_report.get("text_preview") or "").strip()
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
            "errors": errors,
            "warnings": warnings,
            "stdout_tail": (completed.stdout or "")[-1000:],
            "stderr_tail": (completed.stderr or "")[-1000:],
        }

    def run_provider_teamwork(self, round_id: int) -> None:
        if self.provider_reports:
            return
        work_dir = self.provider_work_dir()
        for spec in self.provider_command_specs(work_dir):
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
                    "output": repo_rel(self.repo_root, Path(spec["output"])),
                },
                target="orchestrator",
                correlation_id=correlation,
                round_id=round_id,
            )
            try:
                completed = subprocess.run(
                    spec["command"],
                    cwd=self.repo_root,
                    env=command_env(self.repo_root),
                    capture_output=True,
                    text=True,
                    check=False,
                    timeout=max(30, self.args.timeout_seconds),
                )
            except subprocess.TimeoutExpired as exc:
                completed = subprocess.CompletedProcess(spec["command"], returncode=124, stdout=exc.stdout or "", stderr=exc.stderr or "provider timeout")
            report_data = read_json(Path(spec["output"]))
            provider_report = self.summarize_provider_report(spec, completed, report_data)
            self.provider_reports.append(provider_report)
            append_unique(self.state["provider_results"], provider_report, key="requirement")
            self.publish(provider_heap_lane(lane), "telemetry_signal", provider_report, target="orchestrator", correlation_id=correlation, round_id=round_id)
            claim = {
                "id": f"{requirement}_claim",
                "from": lane,
                "claim": "provider lane contributed usable heap evidence" if provider_report.get("passed") else "provider lane did not produce usable heap evidence",
                "confidence": 0.88 if provider_report.get("passed") else 0.35,
                "requirement": requirement,
                "evidence_ref": provider_report.get("output"),
                "provider_execution_performed": provider_report.get("provider_execution_performed"),
                "observed_request": self.request_text(),
                "observed_response": self.response_text(),
            }
            append_unique(self.state["claims"], claim)
            self.publish(provider_heap_lane(lane), "claim", claim, target="deterministic", correlation_id=f"{correlation}:claim", round_id=round_id)

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
            self.critic_step(round_id, events)
            self.arbiter_step(round_id, events)
            if self.state["product"].get("status") in {"ready", "blocked_with_reason"}:
                break
        if self.state["product"].get("status") == "not_ready":
            events = self.read_events()
            self.arbiter_step(last_round or self.max_iterations, events)
        snapshot = self.heap.write_snapshot()
        final_events = self.read_events()
        completed = sorted(self.completed_requirements(final_events))
        missing = self.missing_requirements(final_events)
        metrics = {
            "heap_read_count": self.heap_read_count,
            "heap_write_count": self.heap_write_count,
            "tool_request_count": self.tool_request_count,
            "tool_execution_count": self.tool_execution_count,
            "decision_count": self.decision_count,
            "candidate_operation_count": self.candidate_operation_count,
            "product_status": self.state["product"].get("status"),
            "budget_decision": self.budget_governor.get("decision"),
            "budget_max_iterations": self.max_iterations,
            "completed_requirement_count": len(completed),
            "required_requirement_count": len(REQUIREMENT_ORDER),
            "completed_requirements": completed,
            "missing_requirements": missing,
            "request_input": self.request_text(),
            "response_text": self.response_text(),
            "response_source": self.response_source(),
            "response_text_present": bool(self.response_text()),
            "provider_refs": self.provider_refs(),
            "shared_evidence_count": len(self.state["shared_evidence"]),
            "shared_memory_evidence_count": 1 if "shared_memory" in completed else 0,
            "shared_context_chunk_evidence_count": 1 if "shared_context_chunks" in completed else 0,
            "tool_catalog_evidence_count": 1 if "tool_catalog" in completed else 0,
            "validation_evidence_count": 1 if "validation_evidence" in completed else 0,
            "gpu1_provider_evidence_count": 1 if "gpu1_provider_planner" in completed else 0,
            "gpu0_provider_evidence_count": 1 if "gpu0_provider_peer" in completed else 0,
            "npu_micro_task_evidence_count": 1 if "npu_micro_task_auditor" in completed else 0,
            "provider_result_count": len(self.provider_reports),
            "provider_lane_count": len({item.get("lane") for item in self.provider_reports}),
            "provider_execution_performed": self.provider_execution_performed,
            "provider_teamwork_required": True,
            "budget_exhausted": bool(missing and (last_round >= self.max_iterations)),
            "invocation_contract_ready": bool(self.invocation_contract.get("passed")),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
        }
        metric_errors = []
        for key in ("heap_read_count", "heap_write_count", "tool_request_count", "tool_execution_count", "decision_count", "candidate_operation_count"):
            if safe_int(metrics.get(key)) <= 0:
                metric_errors.append(f"{key} must be >0")
        if metrics["product_status"] not in {"ready", "blocked_with_reason"}:
            metric_errors.append("product_status must be ready or blocked_with_reason")
        if metrics["product_status"] == "ready" and missing:
            metric_errors.append("ready product_status is forbidden while requirements are missing")
        if metrics["product_status"] == "ready" and safe_int(metrics.get("provider_lane_count")) < 3:
            metric_errors.append("ready product_status requires all three provider lanes")
        if metrics["product_status"] == "ready" and not self.provider_execution_performed:
            metric_errors.append("ready product_status requires observable provider execution")
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
            "heap_snapshot": {"event_count": snapshot.get("event_count"), "event_log": snapshot.get("event_log"), "pending_broker_request_count": snapshot.get("pending_broker_request_count")},
            "bridge_reports": self.bridge_reports,
            "provider_reports": self.provider_reports,
            "real_run_input_contract": {
                "kind": "heap_runtime_completeness_gate_input_contract",
                "task_file": self.args.task_file,
                "objective": self.args.objective,
                "request": self.request_text(),
                "stamp": self.stamp,
                "budget_minutes": self.args.budget_minutes,
                "max_iterations": self.max_iterations,
                "entry_files": ["AGENTS.md", "README.md"],
            },
            "real_run_output_contract": {
                "kind": "heap_runtime_completeness_gate_output_contract",
                "heap_event_log": snapshot.get("event_log"),
                "heap_snapshot": snapshot.get("snapshot"),
                "bridge_reports": self.bridge_reports,
                "provider_report_outputs": [item.get("output") for item in self.provider_reports],
                "request_input": self.request_text(),
                "response_text": self.response_text(),
                "response_source": self.response_source(),
                "provider_refs": self.provider_refs(),
                "product_status": self.state["product"].get("status"),
                "completed_requirements": completed,
                "missing_requirements": missing,
            },
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "errors": self.errors,
            "warnings": self.warnings,
            "guardrails": {"heap_completeness_gate": True, "provider_teamwork_universe_required": True, "provider_execution_performed": self.provider_execution_performed, "patch_application_performed": False, "source_writes_performed": False},
        }


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
    ):
        lines.append(f"- {key}: `{metrics.get(key)}`")
    product = safe_dict(safe_dict(report.get("state")).get("product"))
    lines.extend(["", "## Product", "", f"- Status: `{product.get('status')}`", f"- Request: `{product.get('request_input')}`", f"- Response source: `{product.get('response_source')}`", f"- Response text: {product.get('response_text')}", f"- Reason: {product.get('reason')}"])
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
    parser.add_argument("--objective", default="prove complete heap-driven teamwork loop over repository context, shared memory, brokered tools and all provider lanes")
    parser.add_argument("--request", default="", help="Optional real user request for heap heartbeat, e.g. ciao.")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--tool", default="run_gpu_planner_json_contract_smoke", help="Compatibility flag; complete gate uses its internal readiness tool plan.")
    parser.add_argument("--max-iterations", type=int, default=4)
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
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--operator-intent", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--provider-model", default="")
    parser.add_argument("--gpu0-iterations", type=int, default=16)
    parser.add_argument("--gpu0-min-seconds", type=float, default=0.1)
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
    output = resolve_output_path(gate.repo_root, gate.path_arg(args.output, DEFAULT_OUTPUT).format(stamp=gate.stamp))
    markdown = resolve_output_path(gate.repo_root, gate.path_arg(args.markdown_output, DEFAULT_MARKDOWN).format(stamp=gate.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
