#!/usr/bin/env python3
"""Produce a request-refinement Markdown report for the next provider turn."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _read_text(repo_root: Path, value: str, *, limit: int = 12000) -> str:
    if not value:
        return ""
    path = _resolve(repo_root, value)
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8-sig", errors="replace")[:limit]


def _read_json(repo_root: Path, value: str) -> dict[str, Any]:
    if not value:
        return {}
    path = _resolve(repo_root, value)
    if not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig", errors="replace"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def _list_arg(values: list[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        for part in str(value).split(","):
            item = part.strip()
            if item:
                out.append(item)
    return out


def _compact(value: Any, limit: int = 1400) -> str:
    text = json.dumps(value, ensure_ascii=False, default=str) if not isinstance(value, str) else value
    text = text.replace("\r\n", "\n").strip()
    return text[:limit] + ("\n...[truncated]" if len(text) > limit else "")


def _truthy(value: Any) -> bool:
    return str(value or "").strip().lower() in {"1", "true", "yes", "on"}


def _provider_summary(report: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "lane",
        "revision",
        "role",
        "provider_role",
        "provider_block_id",
        "proposal_block_id",
        "response_text",
        "target_files",
        "validation_commands",
        "provider_rejection_reason",
        "native_tool_call_count",
        "errors",
        "warnings",
    )
    return {key: report.get(key) for key in keys if key in report}


def _tool_result_summary(result: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "id": result.get("id") or result.get("request_id"),
        "tool": result.get("tool"),
        "executed": result.get("executed"),
        "blocked": result.get("blocked"),
        "returncode": result.get("returncode"),
        "outputs": result.get("outputs"),
        "errors": result.get("errors") or [],
        "warnings": result.get("warnings") or [],
    }
    result_summary = result.get("summary")
    if result_summary:
        summary["summary_excerpt"] = _compact(result_summary, limit=900)
    return summary


def _evidence_summaries(repo_root: Path, refs: list[str]) -> list[dict[str, Any]]:
    summaries: list[dict[str, Any]] = []
    for ref in refs:
        data = _read_json(repo_root, ref)
        if not data:
            continue
        item: dict[str, Any] = {
            "path": ref,
            "kind": data.get("kind"),
            "passed": data.get("passed"),
            "errors": data.get("errors") or [],
            "warnings": data.get("warnings") or [],
        }
        if isinstance(data.get("provider_rejection_reasons"), list):
            item["provider_rejection_reasons"] = data.get("provider_rejection_reasons")
        if isinstance(data.get("tool_results"), list):
            item["tool_results"] = [
                _tool_result_summary(result)
                for result in data.get("tool_results", [])
                if isinstance(result, dict)
            ]
        if isinstance(data.get("tool_requests"), list):
            item["tool_requests"] = [
                {
                    "id": request.get("id") or request.get("request_id"),
                    "tool": request.get("tool"),
                    "lane": request.get("lane"),
                    "capture_mode": request.get("capture_mode")
                    or _compact(request.get("args", {}), limit=180),
                }
                for request in data.get("tool_requests", [])
                if isinstance(request, dict)
            ]
        summaries.append(item)
    return summaries


def _render_tool_evidence(evidence_summaries: list[dict[str, Any]]) -> str:
    if not evidence_summaries:
        return "- No broker/tool evidence report was available."
    lines: list[str] = []
    for item in evidence_summaries:
        lines.append(
            f"- `{item.get('path')}` kind=`{item.get('kind')}` passed=`{item.get('passed')}`"
        )
        for error in item.get("errors") or []:
            lines.append(f"  - error: {_compact(error, limit=260)}")
        for result in item.get("tool_results") or []:
            lines.append(
                "  - tool_result "
                f"id=`{result.get('id')}` tool=`{result.get('tool')}` "
                f"returncode=`{result.get('returncode')}` blocked=`{result.get('blocked')}`"
            )
            for error in result.get("errors") or []:
                lines.append(f"    - runtime error: {_compact(error, limit=260)}")
    return "\n".join(lines)


def _build_refined_request(
    *,
    request_text: str,
    capture_mode: str,
    reason: str,
    source_lane: str,
    provider_summary: dict[str, Any],
    evidence_reports: list[str],
    evidence_summaries: list[dict[str, Any]],
) -> str:
    target_files = provider_summary.get("target_files") or []
    target_text = ", ".join(str(item) for item in target_files) or "non verificati"
    provider_text = _compact(provider_summary.get("response_text") or "", limit=3600)
    native_tool_count = provider_summary.get("native_tool_call_count")
    tool_call_text = (
        "No native provider tool calls were emitted."
        if capture_mode == "no_tool_capture" or not native_tool_count
        else f"Native provider tool calls reported: {native_tool_count}."
    )
    return "\n".join(
        [
            "# Generic Write Request Refinement",
            "",
            f"Source lane: `{source_lane or 'unknown'}`",
            f"Capture mode: `{capture_mode or 'native_call'}`",
            f"Reason: {reason or 'provider requested a richer next-turn plan'}",
            "",
            "## Original Request",
            "",
            request_text.strip() or "No operator request text was available to the tool.",
            "",
            "## Current Provider State",
            "",
            f"- Provider block: `{provider_summary.get('provider_block_id') or ''}`",
            f"- Proposal block: `{provider_summary.get('proposal_block_id') or ''}`",
            f"- Revision: `{provider_summary.get('revision')}`",
            f"- Candidate targets: `{target_text}`",
            f"- Validation commands: `{provider_summary.get('validation_commands') or []}`",
            "",
            "## Captured Provider Response",
            "",
            provider_text or "No provider response text was available.",
            "",
            "## Tool Calls And Runtime Evidence",
            "",
            tool_call_text,
            "",
            _render_tool_evidence(evidence_summaries),
            "",
            "## Next Action Plan",
            "",
            "1. Resolve real repo-relative target files with `runtime_file_refs` if targets are absent or uncertain.",
            "2. If code targets are verified, request `run_heap_virtual_dev_environment` and `run_heap_code_execution_matrix` before claiming product readiness.",
            "3. If runtime behavior is unclear, request `agent_runtime_debug_lab` with the smallest concrete diagnostic request.",
            "4. If no verified target exists, return `EXIT_DECISION=NO_PATCHABLE_TARGET` with `BLOCKED_NO_VERIFIED_TARGET_REASON`.",
            "5. GPU1 must consume GPU0/NPU vetoes and this report in the next revision before final synthesis.",
            "",
            "## Evidence Reports",
            "",
            "\n".join(f"- `{item}`" for item in evidence_reports) or "- none",
        ]
    ).strip()


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    request_text = str(args.operator_request or "").strip()
    if not request_text and args.request_file:
        request_text = _read_text(repo_root, args.request_file)
    provider_report = _read_json(repo_root, args.provider_report)
    proposal_text = str(args.proposal_text or provider_report.get("response_text") or "").strip()
    evidence_reports = _list_arg(args.evidence_report)
    if args.provider_report and args.provider_report not in evidence_reports:
        evidence_reports.insert(0, args.provider_report)
    evidence_summaries = _evidence_summaries(repo_root, evidence_reports)
    provider_summary = _provider_summary(provider_report)
    if proposal_text and not provider_summary.get("response_text"):
        provider_summary["response_text"] = proposal_text
    capture_mode = str(args.capture_mode or "native_call")
    source_lane = str(args.source_lane or provider_summary.get("lane") or "")
    source_revision = str(getattr(args, "source_revision", "") or provider_summary.get("revision") or "")
    peer_followup_required = _truthy(getattr(args, "peer_followup_required", "")) or source_lane in {
        "gpu0_peer",
        "npu_micro_task_auditor",
    }
    gpu1_followup_required = _truthy(getattr(args, "gpu1_followup_required", "")) or peer_followup_required
    provider_role = str(
        getattr(args, "provider_role", "")
        or provider_summary.get("provider_role")
        or provider_summary.get("role")
        or ""
    )
    refined_request = _build_refined_request(
        request_text=request_text,
        capture_mode=capture_mode,
        reason=str(args.reason or ""),
        source_lane=source_lane,
        provider_summary=provider_summary,
        evidence_reports=evidence_reports,
        evidence_summaries=evidence_summaries,
    )
    try:
        native_tool_count = int(provider_summary.get("native_tool_call_count") or 0)
    except (TypeError, ValueError):
        native_tool_count = 0
    return {
        "schema_version": 1,
        "kind": "generic_write_md",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": True,
        "source_lane": source_lane,
        "source_revision": source_revision,
        "gpu1_followup_required": gpu1_followup_required,
        "peer_followup_required": peer_followup_required,
        "provider_role": provider_role,
        "capture_mode": capture_mode,
        "tool_calls_absent": capture_mode == "no_tool_capture" or native_tool_count == 0,
        "reason": str(args.reason or ""),
        "request_file": str(args.request_file or ""),
        "provider_report": str(args.provider_report or ""),
        "evidence_report": evidence_reports,
        "tool_evidence_summary": evidence_summaries,
        "provider_summary": provider_summary,
        "provider_response_excerpt": _compact(provider_summary.get("response_text") or ""),
        "refined_request": refined_request,
        "action_plan": [
            "resolve verified targets",
            "run virtual dev environment when code targets exist",
            "run code execution matrix before code product readiness",
            "run debug lab for runtime uncertainty",
            "produce NO_PATCHABLE_TARGET when no verified target exists",
        ],
        "next_turn_required": True,
        "product_after_min_refinements": 3,
        "product_semantics": (
            "After three consumed generic_write refinements, the heap may expose "
            "the refined request/action plan as a readable product, including code "
            "content, without claiming source writes or patch application."
        ),
        "source_writes_performed": False,
        "patch_application_performed": False,
        "provider_execution_performed": False,
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "source_writes_performed": False,
            "patch_application_performed": False,
            "provider_execution_performed": False,
            "git_write_performed": False,
        },
        "errors": [],
        "warnings": [],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Generic Write",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Source lane: `{report.get('source_lane')}`",
        f"- Capture mode: `{report.get('capture_mode')}`",
        f"- Tool calls absent: `{report.get('tool_calls_absent')}`",
        f"- Next turn required: `{report.get('next_turn_required')}`",
        f"- Provider report: `{report.get('provider_report')}`",
        "",
        str(report.get("refined_request") or ""),
        "",
        "## Guardrails",
        "",
    ]
    for key, value in (report.get("guardrails") or {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--operator-request", default="")
    parser.add_argument("--provider-report", default="")
    parser.add_argument("--proposal-text", default="")
    parser.add_argument("--capture-mode", choices=("native_call", "no_tool_capture"), default="native_call")
    parser.add_argument("--evidence-report", action="append", default=[])
    parser.add_argument("--source-lane", default="")
    parser.add_argument("--source-revision", default="")
    parser.add_argument("--gpu1-followup-required", default="")
    parser.add_argument("--peer-followup-required", default="")
    parser.add_argument("--provider-role", default="")
    parser.add_argument("--reason", default="")
    parser.add_argument("--output", default="output/validation/generic_write_md.json")
    parser.add_argument("--markdown-output", default="output/validation/generic_write_md.md")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = _resolve(repo_root, args.output)
    markdown = _resolve(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
