#!/usr/bin/env python3
"""Deterministic blackboard/teamwork runtime lab for IA-Carmine.

This is intentionally small and provider-free. It proves the control inversion:
roles read a shared heap, publish typed events, request one allowlisted broker
operation, evaluate the broker evidence, and close with an explicit product
state. It is a lab, not a patch applier.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
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

DEFAULT_OUTPUT = "output/validation/heap_team_runtime_lab_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/heap_team_runtime_lab_{stamp}.md"
DEFAULT_EVENTS = "output/heap_team_runtime_lab/{stamp}/events.jsonl"
DEFAULT_SNAPSHOT = "output/heap_team_runtime_lab/{stamp}/state.json"
DEFAULT_HEAP_MD = "output/heap_team_runtime_lab/{stamp}/state.md"
DEFAULT_BRIDGE_DIR = "output/heap_team_runtime_lab/{stamp}/broker_bridge"
DEFAULT_BRIDGE_JSON = "output/validation/heap_team_runtime_lab_broker_bridge_{stamp}.json"
DEFAULT_BRIDGE_MD = "output/validation/heap_team_runtime_lab_broker_bridge_{stamp}.md"


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


def make_state(objective: str) -> dict[str, Any]:
    return {
        "task": {"objective": objective, "status": "active"},
        "budget_governor": {},
        "invocation_contract": {},
        "facts": [],
        "needs": [],
        "tool_requests": [],
        "claims": [],
        "decisions": [],
        "candidate_operations": [],
        "product": {"required": True, "status": "not_ready", "reason": "loop has not evaluated broker evidence yet"},
    }


def append_unique(bucket: list[dict[str, Any]], item: dict[str, Any], key: str = "id") -> bool:
    value = item.get(key)
    if value and any(existing.get(key) == value for existing in bucket):
        return False
    bucket.append(item)
    return True


class HeapTeamLab:
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
        self.budget_governor = build_heap_provider_budget_governor(
            self.budget_config,
            requested_max_iterations=args.max_iterations,
        )
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
        self.decision_count = 0
        self.candidate_operation_count = 0
        self.bridge_reports: list[str] = []
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def read_events(self) -> list[dict[str, Any]]:
        self.heap_read_count += 1
        return self.heap.read_events()

    def publish(self, source: str, event_type: str, payload: dict[str, Any], *, target: str = "", correlation_id: str = "", round_id: int | None = None) -> None:
        self.heap.append_event(
            source=source,
            target=target or None,
            event_type=event_type,
            correlation_id=correlation_id or None,
            round_id=round_id,
            payload=payload,
        )
        self.heap_write_count += 1

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

    def planner_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        if not any(item.get("id") == "provider_budget_governor_loaded" for item in self.state["facts"]):
            budget_fact = {
                "id": "provider_budget_governor_loaded",
                "source": "heap_provider_budget_governor",
                "kind": "provider_budget",
                "value": self.budget_governor.get("decision"),
                "loop_budget": self.budget_governor.get("loop_budget"),
                "provider_lanes": sorted((self.budget_governor.get("provider_lanes") or {}).keys()),
            }
            if append_unique(self.state["facts"], budget_fact):
                self.publish("deterministic", "fact", budget_fact, target="gpu1", correlation_id=f"{self.stamp}:fact:budget", round_id=round_id)

        if not any(item.get("id") == "provider_invocation_contract_loaded" for item in self.state["facts"]):
            contract_fact = {
                "id": "provider_invocation_contract_loaded",
                "source": "heap_provider_invocation_contract",
                "kind": "provider_invocation_contract",
                "value": self.invocation_contract.get("real_run_gate", {}).get("decision"),
                "required_events": self.invocation_contract.get("expected_telemetry_contract", {}).get("events_required", []),
            }
            if append_unique(self.state["facts"], contract_fact):
                self.publish("deterministic", "fact", contract_fact, target="gpu1", correlation_id=f"{self.stamp}:fact:invocation_contract", round_id=round_id)

        if not any(item.get("id") == "repo_snapshot_loaded" for item in self.state["facts"]):
            fact = {
                "id": "repo_snapshot_loaded",
                "source": "repo_snapshot",
                "kind": "repo_state",
                "value": "repository snapshot readable; heap lab controls loop state through events",
            }
            if append_unique(self.state["facts"], fact):
                self.publish("gpu1", "fact", fact, target="orchestrator", correlation_id=f"{self.stamp}:fact:repo", round_id=round_id)
        has_request = any(event.get("event_type") == "broker_request" for event in events)
        if not has_request:
            request_id = f"{self.stamp}:syntax-contract-smoke"
            loop_budget = safe_dict(self.budget_governor.get("loop_budget"))
            need = {
                "id": "need_allowlisted_tool_evidence",
                "owner": "planner",
                "kind": "brokered_validation",
                "target": self.args.tool,
                "budget_ref": "provider_budget_governor_loaded",
                "max_iterations": loop_budget.get("max_iterations"),
            }
            append_unique(self.state["needs"], need)
            self.publish("gpu1", "need", need, target="broker", correlation_id=request_id, round_id=round_id)
            tool_request = {"id": request_id, "tool": self.args.tool, "args": {}, "reason": "prove heap-driven brokered tool execution before product decision"}
            append_unique(self.state["tool_requests"], tool_request)
            self.publish("gpu1", "broker_request", tool_request, target="broker", correlation_id=request_id, round_id=round_id)
            self.tool_request_count += 1

    def critic_step(self, round_id: int, events: list[dict[str, Any]]) -> None:
        broker_results = [event for event in events if event.get("event_type") == "broker_result"]
        if not broker_results or self.state["claims"]:
            return
        payloads = [safe_dict(event.get("payload")) for event in broker_results]
        failed = [payload for payload in payloads if payload.get("returncode") not in (0, None) or payload.get("errors")]
        claim = {
            "id": "brokered_tool_evidence_reviewed",
            "from": "critic",
            "claim": "broker produced executable evidence through the shared heap" if not failed else "broker evidence contains failures",
            "confidence": 0.91 if not failed else 0.72,
            "broker_result_count": len(broker_results),
            "failed_result_count": len(failed),
        }
        append_unique(self.state["claims"], claim)
        self.publish("npu", "claim", claim, target="gpu1", correlation_id=f"{self.stamp}:critic:broker", round_id=round_id)
        self.publish("deterministic", "validation_signal", claim, target="gpu1", correlation_id=f"{self.stamp}:validation:broker", round_id=round_id)

    def arbiter_step(self, round_id: int) -> None:
        if not self.state["claims"] or self.state["decisions"]:
            return
        claim = self.state["claims"][-1]
        passed = safe_int(claim.get("failed_result_count")) == 0 and self.tool_execution_count > 0
        decision = {
            "id": "heap_team_lab_decision",
            "from": "arbiter",
            "decision": "product_ready_no_source_write" if passed else "blocked_with_reason",
            "evidence_refs": ["heap:provider_budget_governor", "heap:broker_result", "heap:validation_signal", *self.bridge_reports[-1:]],
            "budget_decision": self.budget_governor.get("decision"),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
            "provider_generation_permit_allowed": self.budget_governor.get("permit_allowed"),
        }
        append_unique(self.state["decisions"], decision)
        self.decision_count += 1
        self.publish("deterministic", "decision", decision, target="orchestrator", correlation_id=f"{self.stamp}:decision", round_id=round_id)
        candidate = {
            "id": "candidate_heap_loop_driver_refactor",
            "kind": "design_operation",
            "path": "Tools/ai/run_heap_team_runtime_lab.py",
            "status": "ready_for_manual_review" if passed else "blocked",
            "rationale": "promote heap-read/write/tool/decision/product loop semantics before adding LLM providers",
            "budget_governor": self.budget_governor.get("decision"),
        }
        append_unique(self.state["candidate_operations"], candidate)
        self.candidate_operation_count += 1
        self.publish("deterministic", "candidate_operation", candidate, target="orchestrator", correlation_id=f"{self.stamp}:candidate", round_id=round_id)
        self.state["product"] = {
            "required": True,
            "status": "ready" if passed else "blocked_with_reason",
            "reason": "heap loop produced provider budget, broker evidence, validation, decision and candidate operation" if passed else "broker evidence failed or no tool execution occurred",
            "budget_governor": self.budget_governor.get("decision"),
        }
        self.publish("orchestrator", "product_signal", self.state["product"], correlation_id=f"{self.stamp}:product", round_id=round_id)

    def run(self) -> dict[str, Any]:
        self.publish("orchestrator", "task_state", self.state["task"], target="gpu1", correlation_id=f"{self.stamp}:task", round_id=0)
        self.heap.write_snapshot()
        self.publish("deterministic", "decision", self.budget_governor, target="orchestrator", correlation_id=f"{self.stamp}:budget", round_id=0)
        for round_id in range(1, self.max_iterations + 1):
            events = self.read_events()
            self.planner_step(round_id, events)
            if self.heap.pending_broker_requests():
                self.run_bridge()
            events = self.read_events()
            self.critic_step(round_id, events)
            self.arbiter_step(round_id)
            if self.state["product"].get("status") in {"ready", "blocked_with_reason"}:
                break
        snapshot = self.heap.write_snapshot()
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
            "invocation_contract_ready": bool(self.invocation_contract.get("passed")),
            "invocation_gate_decision": safe_dict(self.invocation_contract.get("real_run_gate")).get("decision"),
        }
        metric_errors = []
        for key in ("heap_read_count", "heap_write_count", "tool_request_count", "tool_execution_count", "decision_count", "candidate_operation_count"):
            if safe_int(metrics.get(key)) <= 0:
                metric_errors.append(f"{key} must be >0")
        if metrics["product_status"] not in {"ready", "blocked_with_reason"}:
            metric_errors.append("product_status must be ready or blocked_with_reason")
        self.errors.extend(metric_errors)
        return {
            "schema_version": 1,
            "kind": "heap_team_runtime_lab",
            "generated_at": now_iso(),
            "repo_root": self.repo_root.as_posix(),
            "stamp": self.stamp,
            "passed": not self.errors,
            "metrics": metrics,
            "state": self.state,
            "budget_governor": self.budget_governor,
            "heap_snapshot": {"event_count": snapshot.get("event_count"), "event_log": snapshot.get("event_log"), "pending_broker_request_count": snapshot.get("pending_broker_request_count")},
            "bridge_reports": self.bridge_reports,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "errors": self.errors,
            "warnings": self.warnings,
            "guardrails": {"deterministic_roles_only": True, "provider_execution_performed": False, "patch_application_performed": False, "source_writes_performed": False},
        }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Team Runtime Lab", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    metrics = safe_dict(report.get("metrics"))
    for key in ("heap_read_count", "heap_write_count", "tool_request_count", "tool_execution_count", "decision_count", "candidate_operation_count", "product_status", "budget_decision", "budget_max_iterations", "invocation_contract_ready", "invocation_gate_decision"):
        lines.append(f"- {key}: `{metrics.get(key)}`")
    product = safe_dict(safe_dict(report.get("state")).get("product"))
    lines.extend(["", "## Product", "", f"- Status: `{product.get('status')}`", f"- Reason: {product.get('reason')}"])
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--objective", default="prove heap-driven multi-role teamwork loop before provider/LLM integration")
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
    lab = HeapTeamLab(args)
    report = lab.run()
    output = resolve_output_path(lab.repo_root, args.output.format(stamp=lab.stamp))
    markdown = resolve_output_path(lab.repo_root, args.markdown_output.format(stamp=lab.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
