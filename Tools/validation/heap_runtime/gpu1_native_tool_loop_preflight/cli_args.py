"""Argument validation for the GPU1 native tool-loop preflight."""

from __future__ import annotations

import argparse
from typing import Any


def validate_explicit_preflight_args(
    args: Any,
    parser: argparse.ArgumentParser,
) -> None:
    model = str(getattr(args, "model", "") or "").strip()
    if not model or model.lower() == "auto":
        parser.error("--model must be an explicit model name; auto/fallback is not allowed")

    missing = [
        name
        for name, value in (
            ("--base-url", getattr(args, "base_url", "")),
            ("--keep-alive", getattr(args, "keep_alive", "")),
            ("--memory-query", getattr(args, "memory_query", "")),
            ("--startup-required-context-profile", getattr(args, "startup_required_context_profile", "")),
            ("--ai-context-pack-profile", getattr(args, "ai_context_pack_profile", "")),
            ("--rag-db", getattr(args, "rag_db", "")),
            ("--rag-profile", getattr(args, "rag_profile", "")),
            ("--rag-index-policy", getattr(args, "rag_index_policy", "")),
            ("--rag-embedding-model", getattr(args, "rag_embedding_model", "")),
        )
        if not str(value or "").strip()
    ]
    for name, value in (
        ("--num-ctx", getattr(args, "num_ctx", 0)),
        ("--max-new-tokens", getattr(args, "max_new_tokens", 0)),
        ("--timeout-seconds", getattr(args, "timeout_seconds", 0)),
        ("--max-subturns", getattr(args, "max_subturns", 0)),
        ("--file-window-limit", getattr(args, "file_window_limit", 0)),
        ("--startup-provider-input-workers", getattr(args, "startup_provider_input_workers", 0)),
        ("--startup-operational-memory-limit", getattr(args, "startup_operational_memory_limit", 0)),
        ("--rag-top-k", getattr(args, "rag_top_k", 0)),
        ("--rag-char-budget", getattr(args, "rag_char_budget", 0)),
    ):
        if int(value or 0) <= 0:
            missing.append(name)
    if missing:
        parser.error("missing explicit GPU1 preflight parameter(s): " + ", ".join(missing))
