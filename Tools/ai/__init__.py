"""Compatibility package for the IA-Carmine command surface."""

from __future__ import annotations

from pathlib import Path

from ia_carmine.cli import available_tools, main, resolve_tool

_PACKAGE_DIR = Path(__file__).resolve().parent
_CORE_DIR = Path(__file__).resolve().parents[2] / "ia_carmine"
_CORE_COMPAT_DIRS = [
    _CORE_DIR,
    _CORE_DIR / "runtime",
    _CORE_DIR / "memory",
    _CORE_DIR / "context",
    _CORE_DIR / "providers",
    _CORE_DIR / "product",
    _CORE_DIR / "validation_contracts",
]

__path__ = [str(_PACKAGE_DIR), *(str(path) for path in _CORE_COMPAT_DIRS)]
__all__ = ["available_tools", "main", "resolve_tool"]
