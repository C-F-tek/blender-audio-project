"""Preflight-specific broker tool argument policy."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import MAX_FILE_WINDOW_CHARS
from Tools.validation.heap_runtime.gpu1_native_tool_loop_preflight.context import (
    DEFAULT_MEMORY_QUERY,
    repair_runtime_file_window_args,
)

GPU1_LANE = "gpu1_planner"


def normalize_tool_args(
    tool: str,
    raw_args: dict[str, Any],
    *,
    runtime_args: Any,
    provider_report: Path,
    broker_report_paths: list[Path],
) -> dict[str, Any]:
    normalized = dict(raw_args)
    if tool == "runtime_file_window":
        startup = getattr(runtime_args, "startup_context", {})
        if isinstance(startup, dict):
            normalized = repair_runtime_file_window_args(normalized, Path(runtime_args.repo_root), startup)
        normalized.setdefault("offset", 0)
        requested = _positive_int(normalized.get("limit"), 0)
        configured = _positive_int(getattr(runtime_args, "file_window_limit", 16000), 16000)
        normalized["limit"] = min(MAX_FILE_WINDOW_CHARS, max(requested, configured))
    if tool == "runtime_file_refs":
        _normalize_runtime_file_refs(normalized)
    if tool == "runtime_sqlite_memory":
        normalized.setdefault("action", "status")
        normalized.setdefault("scope", "operational")
    if tool == "rag_context_pack":
        normalized.setdefault("query", DEFAULT_MEMORY_QUERY)
        normalized.setdefault("top_k", 12)
        normalized.setdefault("char_budget", 24000)
        normalized.setdefault("allow_missing_query_embedding", "true")
    if tool == "generic_write":
        _normalize_generic_write(normalized, runtime_args, provider_report, broker_report_paths)
    return normalized


def tool_argument_errors(tool: str, args: dict[str, Any]) -> list[str]:
    if tool == "check_python_syntax":
        return ["check_python_syntax_not_valid_for_gpu1_universe_preflight_without_code_delta"]
    if tool == "analyze_code_product_artifact":
        path = str(args.get("code_product_path") or args.get("path") or "").strip()
        if not path or "startup_context_memory_reload" in path.replace("\\", "/"):
            return ["analyze_code_product_artifact_requires_real_code_product_ref"]
    if tool == "generic_write":
        has_text = bool(str(args.get("proposal_text") or "").strip())
        has_file = bool(str(args.get("proposal_text_file") or "").strip())
        if not has_text and not has_file:
            return ["generic_write_requires_proposal_text_or_file"]
    if tool == "runtime_file_window" and _positive_int(args.get("limit"), 0) < 4000:
        return ["runtime_file_window_too_small_for_universe_preflight"]
    return []


def _normalize_runtime_file_refs(args: dict[str, Any]) -> None:
    path_value = args.pop("path", "")
    if not path_value:
        return
    path_values = path_value if isinstance(path_value, list) else [path_value]
    text_files = _as_list(args.get("text_file"))
    target_files = _as_list(args.get("target_file"))
    for item in path_values:
        value = str(item or "").strip()
        if not value:
            continue
        normalized_path = value.replace("\\", "/")
        if normalized_path.startswith(("ia_carmine/", "Tools/", "docs/", "AGENTS.md", "CHATGPT.md", "README.md")):
            target_files.append(value)
        else:
            text_files.append(value)
    if text_files:
        args["text_file"] = text_files
    if target_files:
        args["target_file"] = target_files


def _normalize_generic_write(
    args: dict[str, Any],
    runtime_args: Any,
    provider_report: Path,
    broker_report_paths: list[Path],
) -> None:
    if args.get("capture_mode") not in {"native_call", "no_tool_capture"}:
        args["capture_mode"] = "native_call"
    args.setdefault("provider_report", str(provider_report))
    args.setdefault("source_lane", GPU1_LANE)
    args.setdefault("source_revision", "0")
    args.setdefault("provider_role", "primary")
    args.setdefault("reason", "gpu1_requested_file_backed_write_refinement")
    prompt_file = str(getattr(runtime_args, "operator_prompt_file", "") or "")
    if prompt_file and not args.get("request_file"):
        args["request_file"] = prompt_file
    if broker_report_paths and not args.get("evidence_report"):
        args["evidence_report"] = [str(item) for item in broker_report_paths]


def _positive_int(value: Any, default: int) -> int:
    try:
        parsed = int(value)
    except Exception:
        return default
    return parsed if parsed > 0 else default


def _as_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item) for item in value if str(item or "").strip()]
    return [str(value)] if value else []
