#!/usr/bin/env python3
"""Compatibility entrypoint for provider evidence contract validation."""

from __future__ import annotations

from provider_evidence_contract.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
