"""Canonical ``python -m Tools.ai runtime_tool_broker`` entrypoint."""

from __future__ import annotations

from Tools.ai.runtime_tool.agent_broker.cli import main

__all__ = ["main"]


if __name__ == "__main__":
    raise SystemExit(main())
