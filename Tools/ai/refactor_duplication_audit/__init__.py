"""Refactor duplication audit package."""

from .cli import main
from .report import build_report

__all__ = ["build_report", "main"]
