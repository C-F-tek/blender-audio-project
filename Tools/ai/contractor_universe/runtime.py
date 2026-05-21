"""Contractor universe runtime orchestration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from Tools.ai._shared.report_io import write_json_report, write_text_report
from Tools.ai.runtime_universe.builder import RepoRuntimeUniverseBuilder

from .agents import AuditorAgent, DeterministicBackend, ReviewerAgent, StrategistAgent
from .clock import LogicalClock
from .heap import UniverseHeap
from .models import ContractorRole


class ContractorUniverseRuntime:
    """Small explicit runtime that compacts existing Universo IA semantics."""

    def __init__(
        self,
        *,
        repo_root: Path,
        output_dir: Path,
        stamp: str,
        request_text: str,
        args: Any,
    ):
        self.repo_root = repo_root
        self.output_dir = output_dir
        self.stamp = stamp
        self.request_text = request_text
        self.clock = LogicalClock.from_args(args)
        self.heap = UniverseHeap(repo_root, stamp, output_dir)
        backend = DeterministicBackend()
        self.agents = {
            ContractorRole.STRATEGIST: StrategistAgent(backend),
            ContractorRole.REVIEWER: ReviewerAgent(backend),
            ContractorRole.AUDITOR: AuditorAgent(backend),
        }

    def seed(self) -> None:
        self.heap.blackboard.add_event(
            "user_request",
            lane="orchestrator",
            payload={"request_chars": len(self.request_text), "request_preview": self.request_text[:500]},
        )
        self.heap.push(
            due_tick=0,
            priority=0,
            role=ContractorRole.STRATEGIST,
            kind="proposal",
            payload={"request": self.request_text},
        )

    def run(self) -> dict[str, Any]:
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.seed()
        blocked_reason = ""
        while self.heap.pending():
            item = self.heap.pop_ready(self.clock.tick)
            if item is None:
                self.clock.advance()
                continue
            result = self.agents[item.role].run_turn(item, self.heap, self.clock)
            for next_item in result.next_items:
                self.heap.push(
                    due_tick=next_item.due_tick,
                    priority=next_item.priority,
                    role=next_item.role,
                    kind=next_item.kind,
                    payload=next_item.payload,
                    previous_block_id=next_item.previous_block_id,
                    refines_block_id=next_item.refines_block_id,
                    resume_from_block_id=next_item.resume_from_block_id,
                )
            if result.blocked_reason:
                blocked_reason = result.blocked_reason
            self.clock.advance()

        universe = RepoRuntimeUniverseBuilder(
            self.repo_root, self.output_dir, include_validation=False
        ).build()
        blackboard_snapshot = self.heap.blackboard.write_snapshot()
        product_status = "blocked_with_reason" if blocked_reason else "ready"
        report = {
            "schema_version": 1,
            "kind": "contractor_universe_run",
            "stamp": self.stamp,
            "product_status": product_status,
            "blocked_reason": blocked_reason,
            "runtime_universe_summary": universe.summary(),
            "validation_index_included": False,
            "time": {
                "tick": self.clock.tick,
                "elapsed_seconds": round(self.clock.elapsed_seconds, 3),
                "soft_close_after_seconds": self.clock.soft_close_after_seconds,
            },
            "agents": [role.value for role in self.agents],
            "telemetry_enabled": False,
            "validation_enabled": False,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "pointer_graph": self.heap.pointer_graph,
            "blackboard_snapshot": str(self.output_dir / "blackboard_snapshot.json"),
        }
        write_json_report(report, self.output_dir / "run.json")
        write_json_report(self.heap.pointer_graph, self.output_dir / "pointer_graph.json")
        write_text_report(self._render_markdown(report, blackboard_snapshot), self.output_dir / "run.md")
        return report

    def _render_markdown(
        self, report: dict[str, Any], blackboard_snapshot: dict[str, Any]
    ) -> str:
        lines = [
            "# Contractor Universe Run",
            "",
            f"- Status: `{report['product_status']}`",
            f"- Blocked reason: `{report['blocked_reason']}`",
            f"- Provider execution performed: `{report['provider_execution_performed']}`",
            f"- Validation enabled: `{report['validation_enabled']}`",
            f"- Telemetry enabled: `{report['telemetry_enabled']}`",
            f"- Pointer blocks: `{len(report['pointer_graph'])}`",
            f"- Blackboard events: `{blackboard_snapshot.get('event_count', 0)}`",
            "",
            "This artifact is compact local evidence, not an apply boundary.",
            "",
        ]
        return "\n".join(lines)
