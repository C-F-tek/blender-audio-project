#!/usr/bin/env python3
"""Provider-aware heap/team exchange lab for IA-Carmine.

This lab is the next step after the deterministic heap/team runtime lab. It keeps
all guardrails, but optionally lets a real GPU1/Ollama planner provider read the
shared heap and publish typed team events back into it.

Default mode is still deterministic and non-generative. Real provider generation
requires all of these flags:

- --execute-ollama-gpu1
- --allow-provider-generation
- --operator-intent

Even when the provider is enabled this script does not apply patches, does not
write source files, does not run Blender and does not run FFmpeg. Provider output
must become heap events before it can affect the arbiter decision.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.heap_provider_budget_governor import ProviderBudgetConfig, build_heap_provider_budget_governor, clamp_loop_iterations
    from Tools.ai.heap_provider_invocation_contract import build_heap_provider_invocation_contract
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict, safe_int
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.heap_provider_budget_governor import ProviderBudgetConfig, build_heap_provider_budget_governor, clamp_loop_iterations  # type: ignore
    from Tools.ai.heap_provider_invocation_contract import build_heap_provider_invocation_contract  # type: ignore
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap, safe_dict, safe_int  # type: ignore
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "output/validation/heap_provider_team_exchange_lab_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/heap_provider_team_exchange_lab_{stamp}.md"
DEFAULT_EVENTS = "output/heap_provider_team_exchange_lab/{stamp}/events.jsonl"
DEFAULT_SNAPSHOT = "output/heap_provider_team_exchange_lab/{stamp}/state.json"
DEFAULT_HEAP_MD = "output/heap_provider_team_exchange_lab/{stamp}/state.md"
DEFAULT_BRIDGE_DIR = "output/heap_provider_team_exchange_lab/{stamp}/broker_bridge"
DEFAULT_BRIDGE_JSON = "output/validation/heap_provider_team_exchange_lab_broker_bridge_{stamp}.json"
DEFAULT_BRIDGE_MD = "output/validation/heap_provider_team_exchange_lab_broker_bridge_{stamp}.md"


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
    except Exception:  # noqa: BLE001 - runtime reports may be partially written.
        return {}
    return data if isinstance(data, dict) else {}


def json_dumps_compact(value: Any, max_chars: int = 12000) -> str:
    text = json.dumps(value, indent=2, ensure_ascii=False, default=str)
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n...<truncated>"


def make_state(objective: str) -> dict[str, Any]:
    return {
        "task": {"objective": objective, "status": "active"},
        "budget_governor": {},
        "invocation_contract": {},
        "facts": [],
        "needs": [],
        "tool_requests": [],
        "provider_outputs": [],
        "claims": [],
        "decisions": [],
        "candidate_operations": [],
        "product": {"required": True, "status": "not_ready", "reason": "provider team loop has not reached arbiter"},
    }


def append_unique(bucket: list[dict[str, Any]], item: dict[str, Any], key: str = "id") -> bool:
    value = item.get(key)
    if value and any(existing.get(key) == value for existing in bucket):
        return False
    bucket.append(item)
    return True


def extract_json_object(text: str) -> dict[str, Any]:
    stripped = text.strip()
    if not stripped:
        return {}
    try:
        data = json.loads(stripped)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError:
        pass
    start = stripped.find("{")
    end = stripped.rfind("}")
    if start < 0 or end <= start:
        return {}
    try:
        data = json.loads(stripped[start : end + 1])
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


class OllamaProviderError(RuntimeError):
    pass


def call_ollama_generate(
    *,
    url: str,
    model: str,
    prompt: str,
    timeout_seconds: int,
    max_new_tokens: int,
    keep_alive: str,
) -> dict[str, Any]:
    endpoint = url.rstrip("/") + "/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "format": "json",
        "keep_alive": keep_alive,
        "options": {
            "temperature": 0,
            "num_predict": max_new_tokens,
        },
    }
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(endpoint, data=body, headers={"Content-Type": "application/json"}, method="POST")
    started = time.monotonic()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310 - local operator-controlled Ollama endpoint.
            raw = response.read().decode("utf-8", errors="replace")
            status = getattr(response, "status", 200)
    except urllib.error.URLError as exc:
        raise OllamaProviderError(f"ollama request failed: {type(exc).__name__}: {exc}") from exc
    duration_ms = int((time.monotonic() - started) * 1000)
    try:
        envelope = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise OllamaProviderError(f"ollama envelope JSON parse failed: {exc}; raw_preview={raw[:500]}") from exc
    if not isinstance(envelope, dict):
        raise OllamaProviderError("ollama envelope is not an object")
    response_text = str(envelope.get("response") or "")
    parsed = extract_json_object(response_text)
    return {
        "status": status,
        "duration_ms": duration_ms,
        "envelope": envelope,
        "response_text": response_text,
        "parsed": parsed,
        "json_ok": bool(parsed),
    }


def build_gpu1_prompt(state: dict[str, Any], event_summary: dict[str, Any]) -> str:
    return "\n".join(
        [
            "You are gpu1_planner inside the IA-Carmine heap/team runtime.",
            "Read the shared heap state and return ONLY a JSON object.",
            "Do not propose source writes unless they are candidate_operations for manual review.",
            "Do not claim that patches were applied. Do not run tools directly.",
            "Required JSON shape:",
            json.dumps(
                {
                    "role": "gpu1_planner",
                    "claims": [
                        {
                            "id": "gpu1_claim_1",
                            "claim": "short evidence-based claim",
                            "confidence": 0.0,
                            "evidence_refs": ["heap:event-or-report-ref"],
                        }
                    ],
                    "needs": [],
                    "candidate_operations": [
                        {
                            "id": "candidate_id",
                            "kind": "design_operation",
                            "path": "optional/path",
                            "status": "ready_for_manual_review|blocked",
                            "rationale": "why this follows from heap evidence",
                        }
                    ],
                    "product_signal": {
                        "status": "ready|blocked_with_reason",
                        "reason": "short reason grounded in heap evidence",
                    },
                    "blockers": [],
                },
                indent=2,
                ensure_ascii=False,
            ),
            "Current heap state:",
            json_dumps_compact(state, max_chars=10000),
            "Event summary:",
            json_dumps_compact(event_summary, max_chars=4000),
        ]
    )


class HeapProviderTeamExchangeLab:
    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        self.repo_root = Path(args.repo_root).resolve()
        self.stamp = args.stamp or datetime.now().strftime("%Y%m%d-%H%M%S")
        self.heap = ProviderRuntimeHeap.from_args(
            self.repo_root,
            self.stamp,
            args.events or DEFAULT_EVENTS,
            args.snapshot or DEFAULT_SNAPSHOT,
            args.heap_markdown or DEFAULT_HEAP_MD,
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
        self.state = make_state(args.objective)
        self.state["budget_governor"] = self.budget_governor
        self.state["invocation_contract"] = self.invocation_contract
        self.heap_read_count = 0
        self.heap_write_count = 0
        self.tool_request_count = 0
        self.tool_execution_count = 0
        self.provider_execution_requested = False
        self.provider_execution_performed = False
        self.provider_iteration_count = 0
        self.provider_output_count = 0
        self.decision_count = 0
        self.candidate_operation_count = 0
        self.bridge_reports: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def read_events(self) -> list[dict[str, Any]]:
        self.heap_read_count += 1
        return self.heap.read_events()

    def publish(self, source: str, event_type: str, payload: dict[str, Any], *, target: str = "", correlation_id: str = "", round_id: int | None = None) -> None:
        self.heap.append_event(source=source, target=target or None, event_type=event_type, correlation_id=correlation_id or None, round_id=round_id, payload=payload)
        self.heap_write_count += 1

    def event_summary(self, events: list[dict[str, Any]]) -> dict[str, Any]:
        by_type: dict[str, int] = {}
        by_source: dict[str, int] = {}
        for event in events:
            by_type[str(event.get("event_type") or "unknown")] = by_type.get(str(event.get("event_type") or "unknown"), 0) + 1
            by_source[str(event.get("source") or "unknown")] = by_source.get(str(event.get("source") or "unknown"), 0) + 1
        return {"event_count": len(events), "by_type": by_type, "by_source": by_source}

    def bootstrap(self) -> None:
        self.publish("orchestrator", "task_state", self.state["task"], target="gpu1", correlation_id=f"{self.stamp}:task", round_id=0)
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
        append_unique(self.state["facts"], budget_fact)
        append_unique(self.state["facts"], contract_fact)
        self.publish("deterministic", "fact", budget_fact, target="gpu1", correlation_id=f"{self.stamp}:fact:budget", round_id=0)
        self.publish("deterministic", "fact", contract_fact, target="gpu1", correlation_id=f"{self.stamp}:fact:contract", round_id=0)
        self.heap.write_snapshot()

    def planner_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if any(event.get("event_type") == "broker_request" for event in events):
            return
        request_id = f"{self.stamp}:team-tool-evidence"
        need = {
            "id": "need_brokered_team_evidence",
            "owner": "gpu1_planner",
            "kind": "brokered_validation",
            "target": self.args.tool,
            "reason": "provider team exchange must consume brokered evidence before arbiter decision",
        }
        append_unique(self.state["needs"], need)
        self.publish("gpu1", "need", need, target="broker", correlation_id=request_id, round_id=round_id)
        tool_request = {"id": request_id, "tool": self.args.tool, "args": {}, "reason": "heap team provider loop broker evidence"}
        append_unique(self.state["tool_requests"], tool_request)
        self.publish("gpu1", "broker_request", tool_request, target="broker", correlation_id=request_id, round_id=round_id)
        self.tool_request_count += 1

    def run_bridge(self) -> dict[str, Any]:
        bridge_json = resolve_output_path(self.repo_root, (self.args.bridge_output or DEFAULT_BRIDGE_JSON).format(stamp=self.stamp))
        bridge_md = resolve_output_path(self.repo_root, (self.args.bridge_markdown_output or DEFAULT_BRIDGE_MD).format(stamp=self.stamp))
        command = [
            sys.executable,
            "Tools/ai/provider_runtime_heap_broker_bridge.py",
            "--repo-root", ".",
            "--stamp", self.stamp,
            "--events", repo_rel(self.repo_root, self.heap.paths.events),
            "--snapshot", repo_rel(self.repo_root, self.heap.paths.snapshot),
            "--heap-markdown", repo_rel(self.repo_root, self.heap.paths.markdown),
            "--bridge-dir", self.args.bridge_dir or DEFAULT_BRIDGE_DIR,
            "--timeout-seconds", str(self.args.timeout_seconds),
            "--max-requests", "1",
            "--output", repo_rel(self.repo_root, bridge_json),
            "--markdown-output", repo_rel(self.repo_root, bridge_md),
        ]
        completed = subprocess.run(command, cwd=self.repo_root, capture_output=True, text=True, check=False, timeout=self.args.timeout_seconds + 30)
        report = read_json(bridge_json)
        self.bridge_reports.append(repo_rel(self.repo_root, bridge_json))
        if completed.returncode != 0:
            self.errors.append(f"broker bridge returned {completed.returncode}: {(completed.stderr or completed.stdout)[-1000:]}")
        self.tool_execution_count += safe_int(report.get("tool_execution_count"))
        return report

    def maybe_run_gpu1_provider(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if any(item.get("id") == "gpu1_provider_output" for item in self.state["provider_outputs"]):
            return
        gate_decision = safe_dict(self.invocation_contract.get("real_run_gate")).get("decision")
        allowed = gate_decision == "allow_future_real_run" and self.budget_governor.get("permit_allowed") is True
        if not self.args.execute_ollama_gpu1:
            if self.args.require_provider_output:
                self.warnings.append("provider output required but --execute-ollama-gpu1 was not supplied")
            return
        self.provider_execution_requested = True
        if not allowed:
            self.warnings.append("gpu1 provider execution requested but invocation gate did not allow future real run")
            self.publish(
                "gpu1",
                "claim",
                {
                    "id": "gpu1_provider_blocked_by_gate",
                    "claim": "gpu1 provider execution was requested but gate denied it",
                    "gate_decision": gate_decision,
                    "confidence": 1.0,
                },
                target="npu",
                correlation_id=f"{self.stamp}:gpu1:gate_block",
                round_id=round_id,
            )
            return
        prompt = build_gpu1_prompt(self.state, self.event_summary(events))
        telemetry = {
            "id": "gpu1_provider_invocation_started",
            "provider_lane": "gpu1_planner",
            "model_name": self.args.ollama_model,
            "ollama_url": self.args.ollama_url,
            "generation_enabled": True,
            "permit_decision": self.budget_governor.get("decision"),
        }
        self.publish("gpu1", "telemetry_signal", telemetry, target="orchestrator", correlation_id=f"{self.stamp}:gpu1:invoke", round_id=round_id)
        try:
            provider_result = call_ollama_generate(
                url=self.args.ollama_url,
                model=self.args.ollama_model,
                prompt=prompt,
                timeout_seconds=self.args.provider_timeout_seconds,
                max_new_tokens=self.args.provider_max_new_tokens,
                keep_alive=self.args.keep_alive,
            )
        except OllamaProviderError as exc:
            failure = {
                "id": "gpu1_provider_failure",
                "provider_lane": "gpu1_planner",
                "model_name": self.args.ollama_model,
                "error": str(exc),
                "recommendations_or_blockers": ["ollama provider unavailable or returned unusable output"],
            }
            self.publish("gpu1", "claim", {"id": "gpu1_provider_failure_claim", "claim": failure["recommendations_or_blockers"][0], "confidence": 1.0, "error": str(exc)}, target="npu", correlation_id=f"{self.stamp}:gpu1:failure", round_id=round_id)
            append_unique(self.state["provider_outputs"], failure)
            return
        self.provider_execution_performed = True
        self.provider_iteration_count += 1
        parsed = safe_dict(provider_result.get("parsed"))
        output = {
            "id": "gpu1_provider_output",
            "provider_lane": "gpu1_planner",
            "model_name": self.args.ollama_model,
            "json_ok": bool(provider_result.get("json_ok")),
            "duration_ms": provider_result.get("duration_ms"),
            "parsed": parsed,
            "response_preview": str(provider_result.get("response_text") or "")[:2000],
            "heap_event_refs": [f"heap:{self.stamp}:task", f"heap:{self.stamp}:team-tool-evidence"],
            "tool_request_refs": [item.get("id") for item in self.state["tool_requests"]],
        }
        append_unique(self.state["provider_outputs"], output)
        self.provider_output_count += 1
        self.publish("gpu1", "telemetry_signal", output, target="orchestrator", correlation_id=f"{self.stamp}:gpu1:result", round_id=round_id)
        for index, claim in enumerate(parsed.get("claims") if isinstance(parsed.get("claims"), list) else [], start=1):
            if not isinstance(claim, dict):
                continue
            item = {
                "id": str(claim.get("id") or f"gpu1_provider_claim_{index}"),
                "from": "gpu1_provider",
                "claim": str(claim.get("claim") or "provider emitted an empty claim"),
                "confidence": claim.get("confidence", 0.5),
                "evidence_refs": claim.get("evidence_refs") if isinstance(claim.get("evidence_refs"), list) else output["heap_event_refs"],
            }
            append_unique(self.state["claims"], item)
            self.publish("gpu1", "claim", item, target="npu", correlation_id=f"{self.stamp}:gpu1:claim:{index}", round_id=round_id)
        for index, candidate in enumerate(parsed.get("candidate_operations") if isinstance(parsed.get("candidate_operations"), list) else [], start=1):
            if not isinstance(candidate, dict):
                continue
            item = {
                "id": str(candidate.get("id") or f"gpu1_candidate_{index}"),
                "kind": str(candidate.get("kind") or "design_operation"),
                "path": str(candidate.get("path") or ""),
                "status": str(candidate.get("status") or "ready_for_manual_review"),
                "rationale": str(candidate.get("rationale") or "provider candidate derived from heap evidence"),
                "source": "gpu1_provider",
            }
            append_unique(self.state["candidate_operations"], item)
            self.candidate_operation_count += 1
            self.publish("gpu1", "candidate_operation", item, target="orchestrator", correlation_id=f"{self.stamp}:gpu1:candidate:{index}", round_id=round_id)

    def gpu0_peer_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if any(claim.get("id") == "gpu0_peer_topology_claim" for claim in self.state["claims"]):
            return
        claim = {
            "id": "gpu0_peer_topology_claim",
            "from": "gpu0_peer",
            "claim": "GPU0 remained a diagnostic peer and did not become implicit primary planner",
            "confidence": 0.99,
            "provider_output_seen": bool(self.state["provider_outputs"]),
            "event_count_seen": len(events),
        }
        append_unique(self.state["claims"], claim)
        self.publish("gpu0", "claim", claim, target="npu", correlation_id=f"{self.stamp}:gpu0:peer", round_id=round_id)

    def npu_critic_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if any(claim.get("id") == "npu_teamwork_audit_claim" for claim in self.state["claims"]):
            return
        broker_results = [event for event in events if event.get("event_type") == "broker_result"]
        provider_ok = bool(self.state["provider_outputs"])
        if self.args.require_provider_output and not provider_ok:
            claim_text = "provider output is required but missing"
            confidence = 0.98
        elif provider_ok:
            claim_text = "provider output was converted into heap-visible team evidence"
            confidence = 0.92
        else:
            claim_text = "deterministic team exchange is valid, provider generation was not required"
            confidence = 0.88
        claim = {
            "id": "npu_teamwork_audit_claim",
            "from": "npu_critic",
            "claim": claim_text,
            "confidence": confidence,
            "broker_result_count": len(broker_results),
            "provider_output_count": len(self.state["provider_outputs"]),
            "provider_execution_requested": self.provider_execution_requested,
            "provider_execution_performed": self.provider_execution_performed,
            "source_writes_performed": False,
            "patch_application_performed": False,
        }
        append_unique(self.state["claims"], claim)
        self.publish("npu", "claim", claim, target="orchestrator", correlation_id=f"{self.stamp}:npu:audit", round_id=round_id)
        self.publish("npu", "validation_signal", claim, target="orchestrator", correlation_id=f"{self.stamp}:npu:validation", round_id=round_id)

    def arbiter_step(self, round_id: int) -> None:
        if self.state["decisions"]:
            return
        provider_required_missing = self.args.require_provider_output and not self.provider_execution_performed
        broker_ok = self.tool_execution_count > 0
        ready = broker_ok and not provider_required_missing
        if not self.state["candidate_operations"]:
            candidate = {
                "id": "candidate_provider_team_exchange_next_step",
                "kind": "design_operation",
                "path": "Tools/ai/run_heap_provider_team_exchange_lab.py",
                "status": "ready_for_manual_review" if ready else "blocked",
                "rationale": "provider/team exchange should remain heap-mediated across planner, peer, critic and arbiter roles",
                "source": "arbiter",
            }
            append_unique(self.state["candidate_operations"], candidate)
            self.candidate_operation_count += 1
            self.publish("deterministic", "candidate_operation", candidate, target="orchestrator", correlation_id=f"{self.stamp}:candidate", round_id=round_id)
        decision = {
            "id": "heap_provider_team_exchange_decision",
            "from": "arbiter",
            "decision": "product_ready_with_provider_team_exchange" if ready else "blocked_with_reason",
            "evidence_refs": ["heap:task_state", "heap:broker_result", "heap:gpu0_claim", "heap:npu_claim", *self.bridge_reports[-1:]],
            "provider_required_missing": provider_required_missing,
            "provider_execution_requested": self.provider_execution_requested,
            "provider_execution_performed": self.provider_execution_performed,
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
        }
        append_unique(self.state["decisions"], decision)
        self.decision_count += 1
        self.publish("deterministic", "decision", decision, target="orchestrator", correlation_id=f"{self.stamp}:decision", round_id=round_id)
        self.state["product"] = {
            "required": True,
            "status": "ready" if ready else "blocked_with_reason",
            "reason": "heap/team loop produced broker evidence, peer/critic claims, provider telemetry state and arbiter decision" if ready else "provider output required but not available",
            "provider_execution_requested": self.provider_execution_requested,
            "provider_execution_performed": self.provider_execution_performed,
        }
        self.publish("orchestrator", "product_signal", self.state["product"], correlation_id=f"{self.stamp}:product", round_id=round_id)

    def run(self) -> dict[str, Any]:
        self.bootstrap()
        for round_id in range(1, self.max_iterations + 1):
            events = self.read_events()
            self.planner_step(round_id, events)
            if self.heap.pending_broker_requests():
                self.run_bridge()
            events = self.read_events()
            self.maybe_run_gpu1_provider(round_id, events)
            events = self.read_events()
            self.gpu0_peer_step(round_id, events)
            self.npu_critic_step(round_id, events)
            self.arbiter_step(round_id)
            if self.state["product"].get("status") in {"ready", "blocked_with_reason"}:
                break
        snapshot = self.heap.write_snapshot()
        metrics = {
            "heap_read_count": self.heap_read_count,
            "heap_write_count": self.heap_write_count,
            "tool_request_count": self.tool_request_count,
            "tool_execution_count": self.tool_execution_count,
            "provider_execution_requested": self.provider_execution_requested,
            "provider_execution_performed": self.provider_execution_performed,
            "provider_iteration_count": self.provider_iteration_count,
            "provider_output_count": self.provider_output_count,
            "decision_count": self.decision_count,
            "candidate_operation_count": self.candidate_operation_count,
            "product_status": self.state["product"].get("status"),
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "role_event_counts": safe_dict(snapshot.get("by_lane")),
        }
        metric_errors: list[str] = []
        for key in ("heap_read_count", "heap_write_count", "tool_request_count", "tool_execution_count", "decision_count", "candidate_operation_count"):
            if safe_int(metrics.get(key)) <= 0:
                metric_errors.append(f"{key} must be >0")
        if self.args.require_provider_output and not self.provider_execution_performed:
            metric_errors.append("provider output was required but provider_execution_performed is false")
        if metrics["product_status"] not in {"ready", "blocked_with_reason"}:
            metric_errors.append("product_status must be ready or blocked_with_reason")
        self.errors.extend(metric_errors)
        return {
            "schema_version": 1,
            "kind": "heap_provider_team_exchange_lab",
            "generated_at": now_iso(),
            "repo_root": self.repo_root.as_posix(),
            "stamp": self.stamp,
            "passed": not self.errors,
            "metrics": metrics,
            "state": self.state,
            "budget_governor": self.budget_governor,
            "invocation_contract": self.invocation_contract,
            "heap_snapshot": {"event_count": snapshot.get("event_count"), "event_log": snapshot.get("event_log"), "pending_broker_request_count": snapshot.get("pending_broker_request_count")},
            "bridge_reports": self.bridge_reports,
            "provider_execution_requested": self.provider_execution_requested,
            "provider_execution_performed": self.provider_execution_performed,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "persistent_memory_write_performed": False,
            "errors": self.errors,
            "warnings": self.warnings,
            "guardrails": {
                "heap_mediated_provider_exchange": True,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "persistent_memory_write_performed": False,
                "blender_runtime_performed": False,
                "ffmpeg_runtime_performed": False,
            },
        }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Provider Team Exchange Lab", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    metrics = safe_dict(report.get("metrics"))
    for key in (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "provider_execution_requested",
        "provider_execution_performed",
        "provider_iteration_count",
        "provider_output_count",
        "decision_count",
        "candidate_operation_count",
        "product_status",
        "budget_decision",
        "invocation_gate_decision",
    ):
        lines.append(f"- {key}: `{metrics.get(key)}`")
    product = safe_dict(safe_dict(report.get("state")).get("product"))
    lines.extend(["", "## Product", "", f"- Status: `{product.get('status')}`", f"- Reason: {product.get('reason')}"])
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report.get("warnings", []))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--objective", default="test heap-mediated provider teamwork iterations")
    parser.add_argument("--tool", default="run_gpu_planner_json_contract_smoke")
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
    parser.add_argument("--execute-ollama-gpu1", action="store_true")
    parser.add_argument("--require-provider-output", action="store_true")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--ollama-model", default="gpt-oss:20b")
    parser.add_argument("--provider-timeout-seconds", type=int, default=240)
    parser.add_argument("--provider-max-new-tokens", type=int, default=900)
    parser.add_argument("--timeout-seconds", type=int, default=180)
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
    lab = HeapProviderTeamExchangeLab(args)
    report = lab.run()
    output = resolve_output_path(lab.repo_root, args.output.format(stamp=lab.stamp))
    markdown = resolve_output_path(lab.repo_root, args.markdown_output.format(stamp=lab.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
