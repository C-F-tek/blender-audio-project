#!/usr/bin/env python3
"""Compatibility entrypoint/API for provider runtime blackboard."""

from __future__ import annotations

from provider_runtime_blackboard.api import *  # noqa: F401,F403
from provider_runtime_blackboard.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
