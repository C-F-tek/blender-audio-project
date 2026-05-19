"""NPU/GPU deep review auditor package."""

from .cli import main
from .provider import classify_npu_output
from .runner import run_auditor
from .tool_requests import (
    build_npu_deterministic_tool_fallback_requests,
    should_use_npu_deterministic_tool_fallback,
)

__all__ = [
    "build_npu_deterministic_tool_fallback_requests",
    "classify_npu_output",
    "main",
    "run_auditor",
    "should_use_npu_deterministic_tool_fallback",
]
