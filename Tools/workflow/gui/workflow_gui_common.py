"""Common imports and helpers for the classic workflow GUI."""

from __future__ import annotations

import queue
import sys
from pathlib import Path

GUI_DIR = Path(__file__).resolve().parent
WORKFLOW_DIR = GUI_DIR.parent
for candidate in (GUI_DIR, WORKFLOW_DIR):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

try:
    import workflow_core as wf  # noqa: E402
except ImportError:
    from Tools.workflow import workflow_core as wf  # noqa: E402


class QueueWriter:
    def __init__(self, target_queue: queue.Queue[str]) -> None:
        self.target_queue = target_queue

    def write(self, text: str) -> int:
        if text:
            self.target_queue.put(text)
        return len(text)

    def flush(self) -> None:
        return None
