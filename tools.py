"""Compatibility package alias for the repository's ``Tools`` directory.

Most IA-Carmine scripts import modules through the lowercase ``tools`` package
name while the checked-in directory is named ``Tools``.  This module makes
``import tools.ai...`` resolve to that directory without duplicating files.
"""

from __future__ import annotations

from pathlib import Path

__path__ = [str(Path(__file__).resolve().with_name("Tools"))]
