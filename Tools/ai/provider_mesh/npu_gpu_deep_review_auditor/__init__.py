"""NPU/GPU deep review auditor package."""

from .cli import main
from .runner import run_auditor

__all__ = ["main", "run_auditor"]
