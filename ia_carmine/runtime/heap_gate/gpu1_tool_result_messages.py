"""GPU1-facing broker tool-result message payloads."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import artifact_ref
from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_passed


def gpu1_tool_result_payload(
    repo_root: Path,
    result: dict[str, Any],
    *,
    tool_call_id: str = "",
    max_text_chars: int = 16000,
    max_ref_items: int = 24,
) -> dict[str, Any]:
    """Build the content GPU1 receives in the next chat subturn."""
    outputs = result.get("outputs") if isinstance(result.get("outputs"), dict) else {}
    report_path = _resolve_report_path(repo_root, outputs)
    report = _read_json(report_path) if report_path else {}
    payload: dict[str, Any] = {
        "request_id": result.get("request_id") or result.get("id"),
        "tool_call_id": tool_call_id,
        "tool": result.get("tool"),
        "returncode": result.get("returncode"),
        "passed": broker_result_passed(result, repo_root=repo_root),
        "executed": result.get("executed"),
        "blocked": result.get("blocked"),
        "errors": result.get("errors") if isinstance(result.get("errors"), list) else [],
        "warnings": result.get("warnings") if isinstance(result.get("warnings"), list) else [],
        "outputs": outputs,
        "stdout_tail": str(result.get("stdout_tail") or ""),
        "stderr_tail": str(result.get("stderr_tail") or ""),
        "stdout_ref": result.get("stdout_ref") if isinstance(result.get("stdout_ref"), dict) else {},
        "stderr_ref": result.get("stderr_ref") if isinstance(result.get("stderr_ref"), dict) else {},
        "summary": result.get("summary") if isinstance(result.get("summary"), dict) else result.get("summary"),
        "tool_report_ref": artifact_ref(report_path, repo_root, kind="broker_tool_result")
        if report_path and report_path.exists()
        else {},
        "tool_report_compact": _compact_report(report, max_ref_items=max_ref_items),
        "gpu1_next_step_hint": _next_step_hint(str(result.get("tool") or ""), report),
    }
    _add_text_window_payload(payload, report, max_text_chars=max_text_chars)
    _add_concrete_tool_result_payload(payload, report, max_text_chars=max_text_chars)
    _add_runtime_file_refs_payload(payload, report, max_ref_items=max_ref_items)
    return payload


def gpu1_tool_result_text(payload: dict[str, Any]) -> str:
    """Render the payload as readable tool message content."""
    lines = [
        "TOOL_RESULT",
        f"request_id: {payload.get('request_id') or ''}",
        f"tool_call_id: {payload.get('tool_call_id') or ''}",
        f"tool: {payload.get('tool') or ''}",
        f"returncode: {payload.get('returncode')}",
        f"passed: {str(bool(payload.get('passed'))).lower()}",
        f"executed: {str(bool(payload.get('executed'))).lower()}",
        f"blocked: {str(bool(payload.get('blocked'))).lower()}",
        "errors: " + json.dumps(payload.get("errors") or [], ensure_ascii=False),
        "warnings: " + json.dumps(payload.get("warnings") or [], ensure_ascii=False),
        "outputs: " + json.dumps(payload.get("outputs") or {}, ensure_ascii=False, sort_keys=True),
        "tool_report_ref: "
        + json.dumps(payload.get("tool_report_ref") or {}, ensure_ascii=False, sort_keys=True),
        "tool_report_compact: "
        + json.dumps(payload.get("tool_report_compact") or {}, ensure_ascii=False, sort_keys=True),
        "gpu1_next_step_hint: " + str(payload.get("gpu1_next_step_hint") or ""),
    ]
    if payload.get("runtime_file_refs_compact"):
        lines.extend(
            [
                "RUNTIME_FILE_REFS_COMPACT_BEGIN",
                json.dumps(payload["runtime_file_refs_compact"], indent=2, ensure_ascii=False),
                "RUNTIME_FILE_REFS_COMPACT_END",
            ]
        )
    if payload.get("runtime_file_window_text") is not None:
        lines.extend(
            [
                f"runtime_file_window_text_chars: {payload.get('runtime_file_window_text_chars')}",
                "RUNTIME_FILE_WINDOW_TEXT_BEGIN",
                str(payload.get("runtime_file_window_text") or ""),
                "RUNTIME_FILE_WINDOW_TEXT_END",
            ]
        )
    if payload.get("concrete_tool_result_text") is not None:
        lines.extend(
            [
                f"concrete_tool_result_text_chars: {payload.get('concrete_tool_result_text_chars')}",
                "CONCRETE_TOOL_RESULT_TEXT_BEGIN",
                str(payload.get("concrete_tool_result_text") or ""),
                "CONCRETE_TOOL_RESULT_TEXT_END",
            ]
        )
    return "\n".join(lines)


def _resolve_report_path(repo_root: Path, outputs: dict[str, Any]) -> Path | None:
    report = str(outputs.get("json_report") or outputs.get("evidence_json") or "").strip()
    if not report:
        return None
    path = Path(report)
    return path if path.is_absolute() else repo_root / path


def _read_json(path: Path | None) -> dict[str, Any]:
    if not path or not path.exists():
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def _compact_report(report: dict[str, Any], *, max_ref_items: int) -> dict[str, Any]:
    if not report:
        return {}
    compact: dict[str, Any] = {}
    for key in (
        "schema_version",
        "kind",
        "passed",
        "path",
        "offset",
        "limit",
        "next_offset",
        "eof",
        "ref_count",
        "verified_count",
        "target_count",
        "verified_target_count",
        "candidate_count",
        "product_status",
        "decision",
        "errors",
        "warnings",
    ):
        if key in report:
            compact[key] = report.get(key)
    if isinstance(report.get("source_ref"), dict):
        compact["source_ref"] = report["source_ref"]
    if isinstance(report.get("refs"), list):
        compact["refs_sample_count"] = min(len(report["refs"]), max_ref_items)
    return compact


def _add_text_window_payload(
    payload: dict[str, Any], report: dict[str, Any], *, max_text_chars: int
) -> None:
    text = str(report.get("text") or "")
    if not text:
        return
    payload["runtime_file_window_text"] = text[:max_text_chars]
    payload["runtime_file_window_text_chars"] = len(text)
    payload["runtime_file_window_text_delivered_chars"] = min(len(text), max_text_chars)
    payload["runtime_file_window_source_ref"] = report.get("source_ref")
    payload["runtime_file_window_next_offset"] = report.get("next_offset")
    payload["runtime_file_window_eof"] = report.get("eof")


def _add_concrete_tool_result_payload(
    payload: dict[str, Any], report: dict[str, Any], *, max_text_chars: int
) -> None:
    if str(report.get("kind") or "") not in {
        "repo_toolchain_probe",
        "repo_toolchain_command",
        "repo_search_rg",
        "repo_search_git_grep",
        "repo_find_fd",
        "repo_json_query_jq",
        "repo_powershell_readonly",
    }:
        return
    text = str(report.get("result_text") or "")
    payload["concrete_tool_result_text"] = text[:max_text_chars]
    payload["concrete_tool_result_text_chars"] = int(report.get("result_text_chars") or len(text))
    payload["concrete_tool_command"] = report.get("command")


def _add_runtime_file_refs_payload(
    payload: dict[str, Any], report: dict[str, Any], *, max_ref_items: int
) -> None:
    refs = report.get("refs") if isinstance(report.get("refs"), list) else []
    if not refs:
        return
    sample: list[dict[str, Any]] = []
    for item in refs:
        if not isinstance(item, dict):
            continue
        sample.append(
            {
                "repo_relative": item.get("repo_relative"),
                "raw": item.get("raw"),
                "kind": item.get("kind"),
                "status": item.get("status"),
                "exists": item.get("exists"),
                "patchable": item.get("patchable"),
                "reason": item.get("reason"),
            }
        )
        if len(sample) >= max_ref_items:
            break
    payload["runtime_file_refs_compact"] = {
        "ref_count": report.get("ref_count"),
        "verified_count": report.get("verified_count"),
        "sample": sample,
        "instruction": (
            "Use a repo_relative value from sample with runtime_file_window when you need real "
            "file content; runtime_file_refs proves paths, not contents."
        ),
    }


def _next_step_hint(tool: str, report: dict[str, Any]) -> str:
    if tool == "runtime_file_refs":
        return "Choose verified repo_relative refs and call runtime_file_window for real content."
    if tool == "runtime_file_window":
        if report.get("eof") is False:
            return "You may continue reading with next_offset, or produce/consume a delta if enough evidence exists."
        return "Consume this file content in CONSUMED_EVIDENCE and produce the next delta if sufficient."
    return "Consume this result explicitly in CONSUMED_EVIDENCE before using it as product evidence."
