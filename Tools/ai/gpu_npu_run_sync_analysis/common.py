"""Shared helpers for GPU/NPU run sync analysis."""

from __future__ import annotations

import time
from datetime import datetime
from pathlib import Path
from typing import Any

GPU_ROUND_ELAPSED_SOURCE = "gpu_round_elapsed_seconds"
GPU_ROUND_ALIAS_SOURCE = "gpu_round_duration_fields"
GPU_ELAPSED_FALLBACK_SOURCE = "gpu_elapsed_divided_by_round_count"

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def elapsed_seconds(started: float) -> float:
    return round(time.perf_counter() - started, 3)

def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return (repo_root / path).resolve() if not path.is_absolute() else path.resolve()

def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)

def nested_dict(data: dict[str, Any], key: str) -> dict[str, Any]:
    value = data.get(key)
    return value if isinstance(value, dict) else {}

def list_of_dicts(value: Any) -> list[dict[str, Any]]:
    return [item for item in value if isinstance(item, dict)] if isinstance(value, list) else []

def safe_float(value: Any, default: float = 0.0) -> float:
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.replace(",", "."))
        except ValueError:
            return default
    return default

def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, int) and not isinstance(value, bool):
        return value
    if isinstance(value, float):
        return int(value)
    if isinstance(value, str):
        try:
            return int(value)
        except ValueError:
            return default
    return default

def first_int(default: int, *values: Any) -> int:
    for value in values:
        parsed = safe_int(value, default=-1)
        if parsed >= 0:
            return parsed
    return default

def parse_iso_seconds(value: Any) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None

def duration_from_timestamps(started: Any, finished: Any) -> float:
    start_dt = parse_iso_seconds(started)
    finish_dt = parse_iso_seconds(finished)
    if not start_dt or not finish_dt:
        return 0.0
    return max(0.0, (finish_dt - start_dt).total_seconds())

def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    index = min(len(ordered) - 1, max(0, round((pct / 100.0) * (len(ordered) - 1))))
    return ordered[index]

def rounded_sum(values: list[float]) -> float:
    return round(sum(values), 3) if values else 0.0

def numeric_round_field(round_item: dict[str, Any], key: str) -> float:
    value = safe_float(round_item.get(key))
    return value if value > 0 else 0.0

def collect_round_field_durations(rounds: list[dict[str, Any]], key: str) -> list[float]:
    durations: list[float] = []
    for item in rounds:
        value = numeric_round_field(item, key)
        if value > 0:
            durations.append(value)
    return durations

def extract_round_duration_alias(round_item: dict[str, Any]) -> float:
    for key in (
        "round_elapsed_seconds",
        "duration_seconds",
        "provider_elapsed_seconds",
    ):
        value = numeric_round_field(round_item, key)
        if value > 0:
            return value
    return duration_from_timestamps(round_item.get("started_at"), round_item.get("finished_at"))

def extract_gpu_round_durations(
    report: dict[str, Any],
    rounds: list[dict[str, Any]],
    round_count: int,
    gpu_elapsed: float,
) -> tuple[list[float], str]:
    """Prefer real ``rounds[*].elapsed_seconds`` over synthetic total/round timing."""
    elapsed_durations = collect_round_field_durations(rounds, "elapsed_seconds")
    if elapsed_durations:
        return elapsed_durations, GPU_ROUND_ELAPSED_SOURCE

    alias_durations = [extract_round_duration_alias(item) for item in rounds]
    alias_durations = [value for value in alias_durations if value > 0]
    if alias_durations:
        return alias_durations, GPU_ROUND_ALIAS_SOURCE

    if round_count > 0 and gpu_elapsed > 0:
        return [gpu_elapsed / round_count], GPU_ELAPSED_FALLBACK_SOURCE

    return [], "unavailable"

def audit_duration_seconds(audit: dict[str, Any]) -> float:
    explicit = safe_float(audit.get("elapsed_seconds"))
    if explicit > 0:
        return explicit
    return duration_from_timestamps(audit.get("started_at"), audit.get("finished_at"))

def compact_performance_source(data: dict[str, Any]) -> dict[str, Any]:
    performance = data.get("performance")
    if not isinstance(performance, dict):
        return {}
    return {
        str(key): value
        for key, value in performance.items()
        if isinstance(value, (int, float, str, bool)) or value is None
    }

def runtime_tool_counters(report: dict[str, Any]) -> dict[str, int]:
    keys = (
        "runtime_tool_request_count",
        "runtime_tool_execution_count",
        "runtime_tool_failed_count",
        "runtime_tool_blocked_count",
        "runtime_tool_provider_request_count",
        "runtime_tool_provider_request_execution_count",
        "deterministic_runtime_tool_fallback_request_count",
        "deterministic_runtime_tool_fallback_execution_count",
    )
    return {key: safe_int(report.get(key)) for key in keys}
