"""Runtime tool catalog backed by the broker registry."""

from __future__ import annotations

from typing import Any


def broker_tool_catalog() -> list[dict[str, Any]]:
    try:
        from Tools.ai.runtime_tool_broker.registry import TOOL_SPECS
    except Exception:
        return []
    rows: list[dict[str, Any]] = []
    for name, spec in sorted(TOOL_SPECS.items()):
        rows.append(
            {
                "name": name,
                "description": getattr(spec, "description", ""),
                "allowed_args": list(getattr(spec, "allowed_args", ())),
                "broker_owned_execution": True,
            }
        )
    return rows
