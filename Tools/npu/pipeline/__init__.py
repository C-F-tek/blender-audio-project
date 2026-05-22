"""Compatibility package for IA-Carmine NPU provider core."""

from __future__ import annotations

from pathlib import Path

_PACKAGE_DIR = Path(__file__).resolve().parent
_CORE_DIR = Path(__file__).resolve().parents[3] / "ia_carmine" / "providers" / "npu" / "pipeline"

__path__ = [str(_PACKAGE_DIR), str(_CORE_DIR)]