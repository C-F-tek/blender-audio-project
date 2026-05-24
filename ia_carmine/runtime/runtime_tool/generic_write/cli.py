#!/usr/bin/env python3
"""Produce a request-refinement Markdown report for the next provider turn."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import (
    read_text_evidence,
    read_text_windows_safe,
    resolve_path,
    write_large_text_evidence,
)

def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def _read_text(repo_root: Path, value: str, *, limit: int | None = None) -> str:
    if not value:
        return ""
    path = _resolve(repo_root, value)
    if not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8-sig", errors="replace")
    return text if limit is None else text[:limit]


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
        "provider_cycle_id",
        "role",
        "provider_role",
        "passed",
        "provider_execution_performed",
        "provider_work_verified",
        "operational_provider_activity",
        "useful_output_produced",
        "gpu1_primary_workload_valid",
        "lane_is_closure_owner",
        "closure_owner",
        "review_for_gpu1_cycle",
        "audit_for_gpu1_cycle",
        "cannot_open_revision",
        "provider_block_id",
        "proposal_block_id",
        "refines_block_id",
        "response_text_ref",
        "response_text_chars",
        "response_text_sha256",
        "response_text_tail",
        "target_files",
        "validation_commands",
        "provider_compute_device",
        "windows_task_manager_device_hint",
        "elapsed_seconds",
        "prompt_eval_count",
        "eval_count",
        "prompt_token_count",
        "completion_token_count",
        "provider_rejection_reason",
        "native_tool_call_count",
        "errors",
        "warnings",
    )
    return {key: report.get(key) for key in keys if key in report}


def _provider_response_text(repo_root: Path, report: dict[str, Any]) -> str:
    return str(read_text_evidence(repo_root, report, "response_text").get("text") or "").strip()


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
    output_path = _resolve(repo_root, str(getattr(args, "output", "output/validation/generic_write_md.json")))
    request_text = str(args.operator_request or "").strip()
    if not request_text and args.request_file:
        request_text = _read_text(repo_root, args.request_file)
    provider_report = _read_json(repo_root, args.provider_report)
    proposal_text = str(args.proposal_text or provider_report.get("response_text") or "").strip()
    if not proposal_text and getattr(args, "proposal_text_file", ""):
        proposal_text = _read_text(repo_root, args.proposal_text_file)
    evidence_reports = _list_arg(args.evidence_report)
    if args.provider_report and args.provider_report not in evidence_reports:
        evidence_reports.insert(0, args.provider_report)
    evidence_summaries = _evidence_summaries(repo_root, evidence_reports)
    provider_summary = _provider_summary(provider_report)
    provider_response_full = _provider_response_text(repo_root, provider_report)
    if provider_response_full:
        provider_summary["response_text"] = provider_response_full
    if proposal_text and not provider_summary.get("response_text"):
        provider_summary["response_text"] = proposal_text
    capture_mode = str(args.capture_mode or "native_call")
    source_lane = str(args.source_lane or provider_summary.get("lane") or "")
    raw_source_revision = getattr(args, "source_revision", "")
    if raw_source_revision in ("", None):
        raw_source_revision = provider_summary.get("revision")
    source_revision = "" if raw_source_revision is None else str(raw_source_revision)
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
    refined_request_evidence = write_large_text_evidence(
        repo_root,
        output_path.parent / "generic_write_artifacts",
        name=f"refined_request_{source_lane or 'unknown'}_{source_revision or '0'}",
        text=refined_request,
        kind="generic_write_refined_request",
        producer="generic_write",
        suffix=".md",
    )
    provider_response = str(provider_summary.get("response_text") or "")
    provider_summary_report = dict(provider_summary)
    provider_summary_report.pop("response_text", None)
    provider_summary_report.setdefault("response_text_chars", len(provider_response))
    provider_summary_report.setdefault(
        "response_text_sha256",
        hashlib.sha256(provider_response.encode("utf-8", errors="replace")).hexdigest(),
    )
    provider_summary_report.setdefault("response_text_tail", provider_response[-4000:])
    try:
        native_tool_count = int(provider_summary.get("native_tool_call_count") or 0)
    except (TypeError, ValueError):
        native_tool_count = 0
    source_provider_passed = provider_summary.get("passed") is True
    source_provider_execution_performed = bool(
        provider_summary.get("provider_execution_performed")
        or provider_summary.get("operational_provider_activity")
    )
    source_provider_work_verified = bool(
        provider_summary.get("provider_work_verified")
        or provider_summary.get("gpu1_primary_workload_valid")
    )
    return {
        "schema_version": 1,
        "kind": "generic_write_md",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": True,
        "source_lane": source_lane,
        "source_revision": source_revision,
        "source_provider_passed": source_provider_passed,
        "source_provider_execution_performed": source_provider_execution_performed,
        "source_provider_work_verified": source_provider_work_verified,
        "source_provider_block_id": str(provider_summary.get("provider_block_id") or ""),
        "source_proposal_block_id": str(provider_summary.get("proposal_block_id") or ""),
        "source_provider_cycle_id": provider_summary.get("provider_cycle_id")
        if provider_summary.get("provider_cycle_id") is not None
        else source_revision,
        "gpu1_followup_required": gpu1_followup_required,
        "peer_followup_required": peer_followup_required,
        "provider_role": provider_role,
        "capture_mode": capture_mode,
        "tool_calls_absent": capture_mode == "no_tool_capture" or native_tool_count == 0,
        "reason": str(args.reason or ""),
        "request_file": str(args.request_file or ""),
        "proposal_text_file": str(getattr(args, "proposal_text_file", "") or ""),
        "provider_report": str(args.provider_report or ""),
        "evidence_report": evidence_reports,
        "tool_evidence_summary": evidence_summaries,
        "provider_summary": provider_summary_report,
        "provider_response_excerpt": _compact(provider_response),
        "provider_response_sha256": hashlib.sha256(
            provider_response.encode("utf-8", errors="replace")
        ).hexdigest(),
        "refined_request_ref": refined_request_evidence.get("ref") or {},
        "refined_request_chars": refined_request_evidence.get("chars", 0),
        "refined_request_sha256": refined_request_evidence.get("sha256", ""),
        "refined_request_tail": refined_request_evidence.get("tail", ""),
        "refined_request_tail_chars": refined_request_evidence.get("tail_chars", 0),
        "refined_request_full_text_in_json": False,
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
    refined_request = _read_ref_text_from_report(report, "refined_request")
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
        refined_request or str(report.get("refined_request_tail") or ""),
        "",
        "## Guardrails",
        "",
    ]
    for key, value in (report.get("guardrails") or {}).items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def _read_ref_text_from_report(report: dict[str, Any], prefix: str) -> str:
    repo_root = Path(str(report.get("repo_root") or ".")).resolve()
    ref = report.get(f"{prefix}_ref") if isinstance(report.get(f"{prefix}_ref"), dict) else {}
    ref_path = str(ref.get("path") or "").strip()
    if not ref_path:
        return ""
    try:
        return read_text_windows_safe(resolve_path(repo_root, ref_path))
    except Exception:
        return ""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request-file", default="")
    parser.add_argument("--operator-request", default="")
    parser.add_argument("--provider-report", default="")
    parser.add_argument("--proposal-text", default="")
    parser.add_argument("--proposal-text-file", default="")
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
