"""Canonical ``python -m ia_carmine.cli runtime_tool_broker`` entrypoint."""

from __future__ import annotations

from ia_carmine.runtime.runtime_tool.agent_broker.cli import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
