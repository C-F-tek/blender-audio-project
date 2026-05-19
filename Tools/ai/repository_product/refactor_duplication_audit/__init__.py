"""Refactor duplication audit package."""

from .cli import main
from .markdown import render_markdown
from .report import build_report

__all__ = ["build_report", "main", "render_markdown"]
