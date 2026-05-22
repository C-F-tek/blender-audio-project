"""Canonical command surface for IA-Carmine Core Runtime."""

from __future__ import annotations

from .dispatch import TOOL_MAIN_TARGETS, available_tools, main, resolve_tool

__all__ = ["TOOL_MAIN_TARGETS", "available_tools", "main", "resolve_tool"]

if __name__ == "__main__":
    raise SystemExit(main())
