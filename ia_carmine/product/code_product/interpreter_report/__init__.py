"""Static code interpreter report package."""

from __future__ import annotations

from ia_carmine.product.code_product.interpreter_report.builder import build_report
from ia_carmine.product.code_product.interpreter_report.render import render_markdown

__all__ = ["build_report", "render_markdown"]
