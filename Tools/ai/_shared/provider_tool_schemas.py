"""Broker tool schema helpers shared by provider lanes."""

from __future__ import annotations

from typing import Any


def broker_tool_schemas(
    tool_names: list[str] | tuple[str, ...] | None = None,
    *,
    compact: bool = False,
) -> list[dict[str, Any]]:
    try:
        from Tools.ai.runtime_tool.broker.registry import TOOL_SPECS
    except ImportError:  # pragma: no cover
        from Tools.ai.runtime_tool.broker.registry import TOOL_SPECS  # type: ignore

    allowed = set(tool_names or [])
    schemas: list[dict[str, Any]] = []
    for name, spec in sorted(TOOL_SPECS.items()):
        if allowed and name not in allowed:
            continue
        properties: dict[str, Any] = {}
        if not compact:
            properties = {
                arg: {
                    "type": ["string", "number", "boolean", "array", "object"],
                    "description": f"Broker-validated argument `{arg}`.",
                }
                for arg in spec.allowed_args
            }
        schemas.append(
            {
                "type": "function",
                "function": {
                    "name": name,
                    "description": "IA-Carmine broker tool." if compact else spec.description,
                    "parameters": {
                        "type": "object",
                        "properties": properties,
                        "additionalProperties": False,
                    },
                },
            }
        )
    return schemas
