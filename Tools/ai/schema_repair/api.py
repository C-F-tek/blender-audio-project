"""Public schema repair API."""

from __future__ import annotations

from .common import (
    RECOMMENDATION_TEMPLATE,
    REQUIRED_TOP_LEVEL_KEYS,
    SCHEMA_REPAIR_CONTEXT_KIND,
    SCHEMA_REPAIR_TRIGGER_REASONS,
    TOOL_REQUEST_TEMPLATE,
)
from .context import (
    build_schema_repair_context_report,
    build_schema_repair_context_stack,
    build_schema_repair_retry_prompt,
    should_attempt_schema_repair_retry,
    should_emit_schema_repair_context,
    summarize_schema_repair_retry,
)
from .evidence import collect_recent_runtime_tool_evidence, summarize_round_schema_failures

__all__ = [
    "RECOMMENDATION_TEMPLATE",
    "REQUIRED_TOP_LEVEL_KEYS",
    "SCHEMA_REPAIR_CONTEXT_KIND",
    "SCHEMA_REPAIR_TRIGGER_REASONS",
    "TOOL_REQUEST_TEMPLATE",
    "build_schema_repair_context_report",
    "build_schema_repair_context_stack",
    "build_schema_repair_retry_prompt",
    "collect_recent_runtime_tool_evidence",
    "should_attempt_schema_repair_retry",
    "should_emit_schema_repair_context",
    "summarize_round_schema_failures",
    "summarize_schema_repair_retry",
]
