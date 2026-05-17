"""Shared helpers for agent memory routing policy."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

try:
    from tools.validation.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    import sys

    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.validation.report_utils import write_json_report

DEFAULT_OUTPUT = "output/validation/agent_memory_routing_policy.json"
DEFAULT_MARKDOWN = "output/validation/agent_memory_routing_policy.md"
DEFAULT_BROKER_REQUEST = "output/ai_runtime_tools/agent_memory_routing_policy_tool_requests.json"
SAFE_ID_RE = re.compile(r"[^A-Za-z0-9_.-]+")

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def safe_id(value: str, fallback: str = "memory_route") -> str:
    text = SAFE_ID_RE.sub("_", str(value or "").strip()).strip("._-")
    return text[:80] or fallback

def split_values(values: list[str]) -> list[str]:
    out: list[str] = []
    for value in values:
        for part in str(value).split(","):
            normalized = part.strip()
            if normalized and normalized not in out:
                out.append(normalized)
    return out
