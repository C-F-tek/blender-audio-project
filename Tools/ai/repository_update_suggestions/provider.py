"""Optional local Ollama drafting."""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

def maybe_run_ollama(repo_root: Path, prompt: str, *, model: str | None) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from Tools.npu._shared.ollama_runtime import OllamaSession  # noqa: PLC0415

    with OllamaSession(model=model, shutdown_server=False, unload_model=True) as session:
        text = session.generate(prompt, max_new_tokens=1200, temperature=0.1)
    return {"used": True, "model": model, "text": text, "error": ""}
