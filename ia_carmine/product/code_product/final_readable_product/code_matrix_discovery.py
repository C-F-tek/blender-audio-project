"""Code execution matrix discovery for final readable product assembly."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_code_matrix(
    repo_root: Path,
    run_dir: Path,
    gate: dict[str, Any],
) -> tuple[dict[str, Any], str]:
    for path in discover_code_matrix_reports(repo_root, run_dir, gate):
        payload = _read_json(path)
        if payload.get("kind") == "heap_code_execution_tool":
            return payload, str(path)
    return {}, ""


def discover_code_matrix_reports(
    repo_root: Path,
    run_dir: Path,
    gate: dict[str, Any],
) -> list[Path]:
    paths: list[Path] = []
    for container in (gate.get("metrics"), gate.get("real_run_output_contract")):
        for value in _as_list(_as_dict(container).get("code_execution_matrix_reports")):
            raw = Path(str(value))
            if raw.is_absolute():
                paths.append(raw)
            elif str(value).replace("\\", "/").startswith("output/"):
                paths.append(repo_root / raw)
            else:
                paths.append(run_dir / raw)
    paths.extend(run_dir.glob("broker_bridge/tool_outputs/*heap_code_execution_tool.json"))
    paths.extend(run_dir.glob("**/*heap_code_execution_tool.json"))
    deduped: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve(strict=False))
        if key not in seen and path.exists():
            deduped.append(path.resolve(strict=False))
            seen.add(key)
    return deduped


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def _as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}
