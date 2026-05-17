"""Shared helpers for heap final proposal composition."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

EXECUTION_TRUE_PATTERNS = (
    re.compile(
        r"\b(provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)\b\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"[\"'](provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)[\"']\s*:\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(NPU|GPU|provider|workload)[^\n]{0,120}\bperformed\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bperformed\s*=\s*true\b", re.IGNORECASE),
)
EXECUTION_BOOL_KEYS = {
    "provider_execution_performed",
    "gpu0_provider_execution_performed",
    "gpu1_provider_execution_performed",
    "npu_provider_execution_performed",
    "workload_performed",
}
WORKLOAD_CONTAINER_KEYS = {
    "npu_device_workload",
    "gpu_device_workload",
    "device_workload",
    "workload",
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path, limit: int | None = None) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit is not None and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def mapping_has_execution_evidence(value: Any, parent_key: str = "") -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in EXECUTION_BOOL_KEYS and normalize_bool(item):
                return True
            if (
                key_lower == "performed"
                and parent_key.lower() in WORKLOAD_CONTAINER_KEYS
                and normalize_bool(item)
            ):
                return True
            if mapping_has_execution_evidence(item, key_text):
                return True
    elif isinstance(value, list):
        return any(mapping_has_execution_evidence(item, parent_key) for item in value)
    return False


def text_has_execution_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in EXECUTION_TRUE_PATTERNS)


def provider_report_execution_performed(data: dict[str, Any]) -> bool:
    return mapping_has_execution_evidence(data) or text_has_execution_evidence(
        str(data.get("response_text") or "")
    )


def discover_run_dir(repo_root: Path, report_file: str, run_dir: str) -> Path:
    if run_dir:
        return resolve_path(repo_root, run_dir)
    if report_file:
        report = resolve_path(repo_root, report_file)
        if report.name == "heap_runtime_completeness_gate_report.json":
            return report.parent
    validation = repo_root / "output" / "validation"
    candidates = sorted(
        [
            path
            for path in validation.glob("*")
            if path.is_dir() and (path / "heap_runtime_completeness_gate_report.json").exists()
        ],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    if candidates:
        return candidates[0]
    raise SystemExit("unable to discover run dir; provide --run-dir or --report-file")


def documents_root(custom_root: str, stamp: str) -> Path:
    base = Path(custom_root).expanduser() if custom_root else Path.home() / "Documents"
    return (base / f"aicarmine_heap_final_proposals_{stamp}").resolve()


def load_startup_manifest(run_dir: Path) -> dict[str, Any]:
    return read_json(
        run_dir / "startup_context_memory_reload" / "heap_context_memory_reload_manifest.json"
    )


def load_startup_reconciliation(run_dir: Path) -> dict[str, Any]:
    return read_json(run_dir / "heap_startup_context_reconciliation.json")
