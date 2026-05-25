"""Brokered search-result refs for strict runtime_file_window follow-up."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from ia_carmine.runtime.runtime_tool.broker.common import repo_rel


def source_broker_request_id(args: dict[str, Any]) -> str:
    return str(
        args.get("source_broker_request_id")
        or args.get("broker_request_id")
        or ""
    ).strip()


def attach_broker_report_metadata(
    repo_root: Path, report: dict[str, Any], args: dict[str, Any], output: Path
) -> None:
    request_id = source_broker_request_id(args)
    report.setdefault("producer", "ia_carmine.runtime.runtime_tool.broker.concrete_tool_cli")
    report.setdefault("tool_report_ref", repo_rel(output, repo_root))
    report.setdefault("source_report_ref", repo_rel(output, repo_root))
    if request_id:
        report.setdefault("request_id", request_id)
        report.setdefault("broker_request_id", request_id)
        report.setdefault("source_broker_request_id", request_id)
        report.setdefault("broker_authorized", True)
    refs = report.get("runtime_file_window_authorized_refs")
    refs = refs if isinstance(refs, list) else []
    for item in refs:
        if not isinstance(item, dict):
            continue
        if request_id:
            item.setdefault("source_broker_request_id", request_id)
        item.setdefault("source_report_ref", repo_rel(output, repo_root))
    for match in (
        report.get("matches") if isinstance(report.get("matches"), list) else []
    ):
        if not isinstance(match, dict):
            continue
        hint = match.get("runtime_file_window_hint")
        if not isinstance(hint, dict):
            continue
        arguments = hint.get("arguments")
        if not isinstance(arguments, dict):
            arguments = {}
            hint["arguments"] = arguments
        arguments.setdefault("startup_manifest", repo_rel(output, repo_root))
        arguments.setdefault("source_report_ref", repo_rel(output, repo_root))
        if request_id:
            arguments.setdefault("source_broker_request_id", request_id)


def attach_runtime_file_window_search_refs(
    tool: str, matches: list[dict[str, Any]], source_request_id: str = ""
) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for index, match in enumerate(matches, start=1):
        path = str(match.get("repo_relative") or match.get("path") or "").strip()
        if not path:
            continue
        line = match.get("line") if isinstance(match.get("line"), int) else None
        ref_id = _search_ref_id(tool, path, line, index)
        ref = {
            "ref_id": ref_id,
            "kind": "runtime_file_window_search_ref",
            "path": path,
            "line": line,
            "source_tool": tool,
            "source": "brokered_search_result",
            "source_broker_request_id": source_request_id,
            "required": False,
        }
        match["runtime_file_window_ref_id"] = ref_id
        match["runtime_file_window_authorized_ref"] = ref
        match["runtime_file_window_hint"] = _runtime_file_window_hint(
            path, line, ref_id, source_request_id
        )
        refs.append(ref)
    return refs


def _runtime_file_window_hint(
    path: str,
    line: int | None = None,
    ref_id: str = "",
    source_request_id: str = "",
) -> dict[str, Any]:
    arguments: dict[str, Any] = {"offset": 0, "limit": 16000}
    if ref_id:
        arguments["ref_id"] = ref_id
    else:
        arguments["path"] = path
    if source_request_id:
        arguments["source_broker_request_id"] = source_request_id
    hint: dict[str, Any] = {"tool": "runtime_file_window", "arguments": arguments}
    if line and line > 1:
        hint["line_hint"] = line
    if ref_id:
        hint["path_hint"] = path
    return hint


def _search_ref_id(tool: str, path: str, line: int | None, index: int) -> str:
    digest = hashlib.sha256(
        f"{tool}:{path}:{line or ''}:{index}".encode("utf-8", errors="replace")
    ).hexdigest()[:16]
    return f"{tool}_match_{index}_{digest}"
