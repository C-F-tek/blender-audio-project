"""Repository consistency map package."""

from __future__ import annotations

from ia_carmine.product.repository_product.repository_consistency_map.builder import build_report
from ia_carmine.product.repository_product.repository_consistency_map.render import render_markdown

__all__ = ["build_report", "render_markdown"]
