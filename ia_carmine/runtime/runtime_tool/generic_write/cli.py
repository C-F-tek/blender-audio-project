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


def _provider_summary(report: dict[str, Any]) -> dict[str, Any]:
    keys = (
        "lane",
        "revision",
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


def _build_refined_request(
    *,
    request_text: str,
    reason: str,
    source_lane: str,
    provider_summary: dict[str, Any],
    evidence_reports: list[str],
) -> str:
    target_files = provider_summary.get("target_files") or []
    target_text = ", ".join(str(item) for item in target_files) or "non verificati"
    return "\n".join(
        [
            "# Generic Write Request Refinement",
            "",
            f"Source lane: `{source_lane or 'unknown'}`",
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
    provider_summary = _provider_summary(provider_report)
    if proposal_text and not provider_summary.get("response_text"):
        provider_summary["response_text"] = proposal_text
    refined_request = _build_refined_request(
        request_text=request_text,
        reason=str(args.reason or ""),
        source_lane=str(args.source_lane or ""),
        provider_summary=provider_summary,
        evidence_reports=evidence_reports,
    )
    return {
        "schema_version": 1,
        "kind": "generic_write_md",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": True,
        "source_lane": str(args.source_lane or ""),
        "reason": str(args.reason or ""),
        "request_file": str(args.request_file or ""),
        "provider_report": str(args.provider_report or ""),
        "evidence_report": evidence_reports,
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
    parser.add_argument("--evidence-report", action="append", default=[])
    parser.add_argument("--source-lane", default="")
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
