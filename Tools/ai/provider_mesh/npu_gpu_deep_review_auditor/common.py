"""Common helpers for the NPU/GPU deep review auditor."""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.npu.provider_mesh._shared.npu_runtime import DEFAULT_NPU_PYTHON
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    DEFAULT_NPU_PYTHON = Path(
        os.environ.get(
            "SPAZIOTEMPO_NPU_PYTHON",
            Path.home() / "blender" / "venvs" / "blender-npu-ai" / "Scripts" / "python.exe",
        )
    )

DEFAULT_GPU_REVIEW = "output/ai_pipeline/agent_gpu_deep_planning_review.json"
DEFAULT_CONTEXT = "output/ai_pipeline/npu_gpu_deep_review_audit_context.md"
DEFAULT_NPU_OUT = "output/ai_pipeline/npu_gpu_deep_review_audit.md"
DEFAULT_NPU_NOTES = "output/ai_pipeline/npu_gpu_deep_review_audit_notes.md"
DEFAULT_NPU_METADATA = "output/validation/npu_gpu_deep_review_audit_metadata.json"
DEFAULT_OUTPUT = "output/validation/npu_gpu_deep_review_audit.json"
DEFAULT_MARKDOWN = "output/validation/npu_gpu_deep_review_audit.md"
OPENVINO_GENAI_MISSING = "ModuleNotFoundError: No module named 'openvino_genai'"

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def compact_json(data: Any, max_chars: int) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text

def npu_python_path(value: str | None) -> Path:
    if value:
        return Path(value).expanduser()
    return Path(os.environ.get("SPAZIOTEMPO_NPU_PYTHON", str(DEFAULT_NPU_PYTHON))).expanduser()
