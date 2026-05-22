from __future__ import annotations

import time
from typing import Any

from ia_carmine._shared.ollama_gpu_residency import ollama_ps_snapshot


def finalize_ollama_unload_snapshots(
    *,
    snapshots: list[dict[str, Any]],
    session_ollama_exe: Any,
    selected_model: str,
    base_url: str,
    unload_model: bool,
) -> tuple[bool, bool]:
    if unload_model:
        time.sleep(0.5)
        unload_snapshot = ollama_ps_snapshot(
            session_ollama_exe,
            selected_model,
            "after_unload",
            base_url=base_url,
        )
        snapshots.append(unload_snapshot)
        return True, not bool(unload_snapshot.get("model_line"))
    unload_snapshot = ollama_ps_snapshot(
        session_ollama_exe,
        selected_model,
        "unload_deferred",
        base_url=base_url,
    )
    snapshots.append(unload_snapshot)
    return False, False
