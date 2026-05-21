"""Priority heap and pointer graph for contractor tasks."""

from __future__ import annotations

import heapq
from pathlib import Path
from typing import Any

from Tools.ai.provider_runtime_blackboard.heap import ProviderRuntimeHeap

from .models import ContractorRole, HeapItem


class UniverseHeap:
    """Small heapq-backed scheduler backed by the provider runtime blackboard."""

    def __init__(self, repo_root: Path, stamp: str, output_dir: Path):
        self.repo_root = repo_root
        self.stamp = stamp
        self.output_dir = output_dir
        self._queue: list[HeapItem] = []
        self._sequence = 0
        self.pointer_graph: list[dict[str, Any]] = []
        self.blackboard = ProviderRuntimeHeap.from_args(
            repo_root=repo_root,
            stamp=stamp,
            events_path=str(output_dir / "events.jsonl"),
            snapshot_path=str(output_dir / "blackboard_snapshot.json"),
            markdown_path=str(output_dir / "blackboard_snapshot.md"),
        )

    def push(
        self,
        *,
        due_tick: int,
        priority: int,
        role: ContractorRole,
        kind: str,
        payload: dict[str, Any] | None = None,
        previous_block_id: str = "",
        refines_block_id: str = "",
        resume_from_block_id: str = "",
    ) -> HeapItem:
        self._sequence += 1
        item = HeapItem(
            due_tick=due_tick,
            priority=priority,
            sequence=self._sequence,
            role=role,
            kind=kind,
            payload=payload or {},
            previous_block_id=previous_block_id,
            refines_block_id=refines_block_id,
            resume_from_block_id=resume_from_block_id,
        )
        heapq.heappush(self._queue, item)
        return item

    def pending(self) -> bool:
        return bool(self._queue)

    def pop_ready(self, tick: int) -> HeapItem | None:
        if not self._queue or self._queue[0].due_tick > tick:
            return None
        return heapq.heappop(self._queue)

    def record_block(
        self,
        *,
        block_id: str,
        item: HeapItem,
        status: str,
        payload: dict[str, Any],
    ) -> None:
        node = {
            "block_id": block_id,
            "role": item.role.value,
            "kind": item.kind,
            "status": status,
            "previous_block_id": item.previous_block_id,
            "refines_block_id": item.refines_block_id,
            "resume_from_block_id": item.resume_from_block_id,
            "payload": payload,
        }
        self.pointer_graph.append(node)
