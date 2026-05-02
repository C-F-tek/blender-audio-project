#!/usr/bin/env python3
"""Build a compact artifact pack for code patch-plan reports.

This tool summarizes the report-only code patch-plan lane and its documentation
follow-up bridge without embedding large raw artifacts. It is designed to be fed
into the existing GitHub evidence bundle builder as a normal compact report.

It does not apply code patches, edit documentation, execute providers, run
Blender or write outside the requested report outputs.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT_FOR_IMPORTS = Path(__file__).resolve().parents[2]
if str(REPO_ROOT_FOR_IMPORTS) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT_FOR_IMPORTS))

try:
    from Tools.validation.report_utils import resolve_output_path, write_json_report
except ImportError:  # pragma: no cover - fallback for direct package-local execution.
    from report_utils import resolve_output_path, write_json_report  # type: ignore


REPORT_KIND = "code_patch_artifact_pack"
DEFAULT_CODE_PATCH_PLAN = "output/patch_specs/agent_review_code_patch_plan_macro.json"
DEFAULT_DOCS_FOLLOWUP = "output/patch_specs/agent_review_code_docs_followup_macro.json"
DEFAULT_OUTPUT = "output/validation/code_patch_artifact_pack.json"
DEFAULT_MARKDOWN = "output/validation/code_patch_artifact_pack.md"
MAX_TEXT_CHARS = 700
MAX_ITEMS = 40


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def read_json_object(path: Path) -> tuple[dict[str, Any], list[str]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError:
        return {}, [f"missing file: {path}"]
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{type(exc).__name__}: {exc}"]
    if not isinstance(data, dict):
        return {}, ["root JSON value must be an object"]
    return data, []


def compact_text(value: Any, limit: int = MAX_TEXT_CHARS) -> str:
    text = str(value or "")
    return text if len(text) <= limit else text[:limit] + "...[truncated]"


def compact_list(value: Any, *, max_items: int = MAX_ITEMS, text_limit: int = MAX_TEXT_CHARS) -> list[Any]:
    if not isinstance(value, list):
        return []
    compacted: list[Any] = []
    for item in value[:max_items]:
        if isinstance(item, str):
            compacted.append(compact_text(item, text_limit))
        else:
            compacted.append(item)
    return compacted


def summarize_code_plan(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": plan.get("id"),
        "area": plan.get("area"),
        "risk": plan.get("risk"),
        "status": plan.get("status"),
        "target_files": compact_list(plan.get("target_files"), text_limit=250),
        "rationale": compact_text(plan.get("rationale")),
        "edit_strategy": compact_text(plan.get("edit_strategy")),
        "validation_commands": compact_list(plan.get("validation_commands"), text_limit=500),
        "stop_conditions": compact_list(plan.get("stop_conditions"), text_limit=500),
        "manual_review_required": plan.get("manual_review_required"),
        "source_evidence": {
            "contract": (plan.get("source_evidence") or {}).get("contract") if isinstance(plan.get("source_evidence"), dict) else None,
            "line_count_csv_hint": (plan.get("source_evidence") or {}).get("line_count_csv_hint") if isinstance(plan.get("source_evidence"), dict) else None,
        },
    }


def summarize_docs_followup(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": item.get("id"),
        "source_code_patch_plan_id": item.get("source_code_patch_plan_id"),
        "area": item.get("area"),
        "risk": item.get("risk"),
        "status": item.get("status"),
        "target_files": compact_list(item.get("target_files"), text_limit=250),
        "missing_candidate_docs": compact_list(item.get("missing_candidate_docs"), text_limit=250),
        "rationale": compact_text(item.get("rationale")),
        "edit_strategy": compact_text(item.get("edit_strategy")),
        "validation_commands": compact_list(item.get("validation_commands"), text_limit=500),
        "stop_conditions": compact_list(item.get("stop_conditions"), text_limit=500),
        "manual_review_required": item.get("manual_review_required"),
    }


def report_guardrail_errors(data: dict[str, Any], label: str) -> list[str]:
    errors: list[str] = []
    for field in ("provider_execution_performed", "patch_application_performed", "source_writes_performed"):
        if data.get(field) is not False:
            errors.append(f"{label}: {field} must be false")
    if data.get("manual_review_required") is not True:
        errors.append(f"{label}: manual_review_required must be true")
    return errors


def build_pack(repo_root: Path, code_plan_path: Path, docs_followup_path: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    code_plan, code_errors = read_json_object(code_plan_path)
    docs_followup, docs_errors = read_json_object(docs_followup_path)
    errors.extend(f"code patch plan: {error}" for error in code_errors)
    errors.extend(f"docs follow-up: {error}" for error in docs_errors)

    code_plan_items: list[dict[str, Any]] = []
    docs_followup_items: list[dict[str, Any]] = []

    if code_plan:
        if code_plan.get("kind") != "agent_review_code_patch_plan":
            errors.append("code patch plan kind must be agent_review_code_patch_plan")
        errors.extend(report_guardrail_errors(code_plan, "code patch plan"))
        raw_plans = code_plan.get("code_patch_plans", [])
        if not isinstance(raw_plans, list):
            errors.append("code patch plan code_patch_plans must be a list")
            raw_plans = []
        if code_plan.get("patch_plan_count") != len(raw_plans):
            errors.append("code patch plan patch_plan_count must match len(code_patch_plans)")
        code_plan_items = [summarize_code_plan(plan) for plan in raw_plans if isinstance(plan, dict)]

    if docs_followup:
        if docs_followup.get("kind") != "agent_review_code_docs_followup":
            errors.append("docs follow-up kind must be agent_review_code_docs_followup")
        errors.extend(report_guardrail_errors(docs_followup, "docs follow-up"))
        raw_suggestions = docs_followup.get("docs_followup_suggestions", [])
        if not isinstance(raw_suggestions, list):
            errors.append("docs follow-up docs_followup_suggestions must be a list")
            raw_suggestions = []
        if docs_followup.get("docs_followup_count") != len(raw_suggestions):
            errors.append("docs follow-up docs_followup_count must match len(docs_followup_suggestions)")
        docs_followup_items = [summarize_docs_followup(item) for item in raw_suggestions if isinstance(item, dict)]

    if code_plan and docs_followup:
        code_ids = {str(item.get("id")) for item in code_plan.get("code_patch_plans", []) if isinstance(item, dict)}
        docs_source_ids = {str(item.get("source_code_patch_plan_id")) for item in docs_followup.get("docs_followup_suggestions", []) if isinstance(item, dict)}
        missing_docs = sorted(code_ids - docs_source_ids)
        if missing_docs:
            warnings.append("code plans without docs follow-up suggestions: " + ", ".join(missing_docs))

    return {
        "schema_version": 1,
        "kind": REPORT_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "apply_mode": "report_only_compact_code_patch_artifact_pack",
        "inputs": {
            "code_patch_plan": repo_rel(repo_root, code_plan_path),
            "docs_followup": repo_rel(repo_root, docs_followup_path),
        },
        "summary": {
            "code_patch_plan_count": len(code_plan_items),
            "docs_followup_count": len(docs_followup_items),
            "code_patch_plan_ready": bool(code_plan_items) and not code_errors,
            "docs_followup_ready": bool(docs_followup_items) and not docs_errors,
        },
        "code_patch_plans": code_plan_items,
        "docs_followup_suggestions": docs_followup_items,
        "decision": {
            "ready_for_manual_code_review": bool(code_plan_items) and not errors,
            "ready_for_manual_docs_review": bool(docs_followup_items) and not errors,
            "manual_review_required": True,
            "recommended_next_layer": "review_code_and_docs_queues_together" if code_plan_items and docs_followup_items and not errors else "fix_or_collect_patch_plan_artifacts",
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "docs_written": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
            "raw_patch_content_embedded": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Code Patch Artifact Pack", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Manual review required: `{report['manual_review_required']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append(f"- Code patch plan count: `{report['summary']['code_patch_plan_count']}`")
    lines.append(f"- Docs follow-up count: `{report['summary']['docs_followup_count']}`")
    lines.append("")
    lines.append("## Code patch plans")
    lines.append("")
    if not report.get("code_patch_plans"):
        lines.append("- none")
    for plan in report.get("code_patch_plans", []):
        lines.append(f"### `{plan.get('id')}`")
        lines.append(f"- Area: `{plan.get('area')}`")
        lines.append(f"- Risk: `{plan.get('risk')}`")
        lines.append(f"- Status: `{plan.get('status')}`")
        lines.append(f"- Target files: `{plan.get('target_files')}`")
        lines.append(f"- Rationale: {plan.get('rationale')}")
        lines.append("")
    lines.append("## Docs follow-up suggestions")
    lines.append("")
    if not report.get("docs_followup_suggestions"):
        lines.append("- none")
    for item in report.get("docs_followup_suggestions", []):
        lines.append(f"### `{item.get('id')}`")
        lines.append(f"- Source code plan: `{item.get('source_code_patch_plan_id')}`")
        lines.append(f"- Target docs: `{item.get('target_files')}`")
        lines.append(f"- Rationale: {item.get('rationale')}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("This pack is compact evidence only. It is not a patch apply queue.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--code-patch-plan", default=DEFAULT_CODE_PATCH_PLAN)
    parser.add_argument("--docs-followup", default=DEFAULT_DOCS_FOLLOWUP)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    code_plan_path = resolve_output_path(repo_root, args.code_patch_plan)
    docs_followup_path = resolve_output_path(repo_root, args.docs_followup)
    report = build_pack(repo_root, code_plan_path, docs_followup_path)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    text = write_json_report(report, output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
