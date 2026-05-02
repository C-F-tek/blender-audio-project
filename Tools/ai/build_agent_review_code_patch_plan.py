#!/usr/bin/env python3
"""Build a report-only code patch plan from contract-drift evidence.

This builder turns `code_contract_drift` reports into small, manual-review code
patch plan entries. It does not apply patches, execute providers, run Blender,
write source files, write SQLite databases or touch runtime output artifacts.
"""
from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report  # type: ignore


PLAN_KIND = "agent_review_code_patch_plan"
APPLY_MODE = "report_only_manual_review_code_patch_plan"
DEFAULT_CODE_DRIFT_REPORT = "output/validation/code_contract_drift.json"
DEFAULT_OUTPUT = "output/patch_specs/agent_review_code_patch_plan.json"
DEFAULT_MARKDOWN = "output/patch_specs/agent_review_code_patch_plan.md"
DEFAULT_LINE_COUNT_CSV = "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv"

CODE_EXTENSIONS = {".py", ".ps1", ".psm1", ".psd1", ".yml", ".yaml"}
FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)
FORBIDDEN_TARGET_SUFFIXES = (
    ".db",
    ".sqlite",
    ".sqlite3",
)
FORBIDDEN_TARGET_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
)
DEFAULT_VALIDATION_COMMANDS = [
    "python .\\Tools\\validation\\check_python_syntax.py --repo-root . --output .\\output\\validation\\python_syntax.json",
    "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
    "git diff --check",
]


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
    except (OSError, json.JSONDecodeError) as exc:
        return {}, [f"{type(exc).__name__}: {exc}"]
    if not isinstance(data, dict):
        return {}, ["root JSON value must be an object"]
    return data, []


def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/").lstrip("./")


def is_code_like_path(path_value: str) -> bool:
    return Path(path_value).suffix.lower() in CODE_EXTENSIONS


def target_errors(repo_root: Path, path_value: str) -> list[str]:
    path = normalize_repo_path(path_value)
    errors: list[str] = []
    if not path:
        return ["empty target path"]
    if Path(path).is_absolute():
        errors.append("absolute target paths are not allowed")
    full = (repo_root / path).resolve(strict=False)
    try:
        full.relative_to(repo_root.resolve(strict=False))
    except ValueError:
        errors.append("target path escapes repository root")
    for prefix in FORBIDDEN_TARGET_PREFIXES:
        if path.startswith(prefix):
            errors.append(f"forbidden target prefix: {prefix}")
    for suffix in FORBIDDEN_TARGET_SUFFIXES:
        if path.lower().endswith(suffix):
            errors.append(f"forbidden target suffix: {suffix}")
    for fragment in FORBIDDEN_TARGET_FRAGMENTS:
        if fragment in path.lower():
            errors.append(f"forbidden target fragment: {fragment}")
    if not is_code_like_path(path):
        errors.append("target is not a code/config script path for the code patch-plan lane")
    if not full.is_file():
        errors.append("target file does not exist")
    return errors


def load_line_counts(repo_root: Path, csv_path: Path) -> tuple[dict[str, int], list[str]]:
    warnings: list[str] = []
    counts: dict[str, int] = {}
    if not csv_path.exists():
        warnings.append(f"line-count CSV missing: {repo_rel(repo_root, csv_path)}")
        return counts, warnings
    try:
        with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
            reader = csv.DictReader(handle)
            for row in reader:
                path = normalize_repo_path(row.get("Path") or row.get("File"))
                raw_lines = row.get("Lines") or row.get("lines")
                if not path or raw_lines is None:
                    continue
                try:
                    counts[path] = int(str(raw_lines).strip())
                except ValueError:
                    continue
    except OSError as exc:
        warnings.append(f"unable to read line-count CSV: {type(exc).__name__}: {exc}")
    return counts, warnings


def line_count_for(path_value: str, counts: dict[str, int]) -> int | None:
    normalized = normalize_repo_path(path_value)
    if normalized in counts:
        return counts[normalized]
    # Some older CSV exports may contain absolute paths. Use suffix matching as a fallback.
    matches = [lines for path, lines in counts.items() if normalize_repo_path(path).endswith(normalized)]
    if len(matches) == 1:
        return matches[0]
    return None


def risk_for(path_value: str, check: dict[str, Any], counts: dict[str, int]) -> str:
    lines = line_count_for(path_value, counts)
    error_count = len(check.get("errors", []) if isinstance(check.get("errors"), list) else [])
    warning_count = len(check.get("warnings", []) if isinstance(check.get("warnings"), list) else [])
    missing_required = len(check.get("missing_required_terms", []) if isinstance(check.get("missing_required_terms"), list) else [])
    if missing_required or error_count:
        base = "medium"
    else:
        base = "low"
    if lines is not None and lines >= 600:
        return "high" if base == "medium" else "medium"
    if warning_count >= 5 and base == "low":
        return "medium"
    return base


def status_for(check: dict[str, Any]) -> str:
    if check.get("ok") is False:
        return "ready_for_manual_review"
    missing_recommended = check.get("missing_recommended_terms", [])
    warnings = check.get("warnings", [])
    if missing_recommended or warnings:
        return "candidate_for_manual_review"
    return "informational"


def rationale_for(check: dict[str, Any]) -> str:
    contract = check.get("contract") or "code contract"
    missing_required = check.get("missing_required_terms", []) if isinstance(check.get("missing_required_terms"), list) else []
    missing_recommended = check.get("missing_recommended_terms", []) if isinstance(check.get("missing_recommended_terms"), list) else []
    forbidden = check.get("forbidden_terms_present", []) if isinstance(check.get("forbidden_terms_present"), list) else []
    parts = [f"Contract drift check `{contract}` reported a code-review candidate."]
    if missing_required:
        parts.append("Missing required terms: " + ", ".join(f"`{term}`" for term in missing_required[:8]) + ".")
    if missing_recommended:
        parts.append("Missing recommended terms: " + ", ".join(f"`{term}`" for term in missing_recommended[:8]) + ".")
    if forbidden:
        parts.append("Forbidden terms present: " + ", ".join(f"`{term}`" for term in forbidden[:8]) + ".")
    return " ".join(parts)


def edit_strategy_for(path_value: str, check: dict[str, Any], counts: dict[str, int]) -> str:
    hint = ""
    safe_actions = check.get("safe_actions", []) if isinstance(check.get("safe_actions"), list) else []
    for action in safe_actions:
        if isinstance(action, dict) and action.get("hint"):
            hint = str(action["hint"])
            break
    lines = line_count_for(path_value, counts)
    size_note = ""
    if lines is not None:
        size_note = f" Current CSV sizing hint: {lines} lines; verify current count locally before editing."
    return (
        (hint or "Apply the smallest targeted code/config change that restores the documented contract terms.")
        + size_note
        + " Do not apply this plan automatically."
    )


def validation_commands_for(path_value: str) -> list[str]:
    commands = list(DEFAULT_VALIDATION_COMMANDS)
    suffix = Path(path_value).suffix.lower()
    if suffix == ".py":
        commands.insert(0, f"python -m py_compile .\\{path_value.replace('/', '\\\\')}")
    return commands


def plan_from_check(index: int, repo_root: Path, check: dict[str, Any], counts: dict[str, int]) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    path_value = normalize_repo_path(check.get("path"))
    if not path_value:
        return None, {"id": f"code_contract_{index:03d}", "reason": "check has no path"}
    errors = target_errors(repo_root, path_value)
    if errors:
        return None, {"id": f"code_contract_{index:03d}", "path": path_value, "reason": "; ".join(errors)}

    missing_required = check.get("missing_required_terms", []) if isinstance(check.get("missing_required_terms"), list) else []
    missing_recommended = check.get("missing_recommended_terms", []) if isinstance(check.get("missing_recommended_terms"), list) else []
    check_errors = check.get("errors", []) if isinstance(check.get("errors"), list) else []
    check_warnings = check.get("warnings", []) if isinstance(check.get("warnings"), list) else []
    if not missing_required and not missing_recommended and not check_errors and not check_warnings and check.get("ok") is not False:
        return None, {"id": f"code_contract_{index:03d}", "path": path_value, "reason": "check is already clean"}

    return (
        {
            "id": f"code_contract_{index:03d}",
            "area": str(check.get("owner_lane") or check.get("contract") or "validation"),
            "risk": risk_for(path_value, check, counts),
            "status": status_for(check),
            "target_files": [path_value],
            "rationale": rationale_for(check),
            "edit_strategy": edit_strategy_for(path_value, check, counts),
            "proposed_patch": "",
            "validation_commands": validation_commands_for(path_value),
            "stop_conditions": [
                "Stop if the target file changed since the drift report was generated.",
                "Stop if the edit requires provider execution, Blender runtime execution, or patch auto-apply.",
                "Stop if the patch touches output/**, generated indexes, full analysis JSON, SQLite, secrets, permissions, billing, or repository visibility.",
                "Stop if local validation fails.",
            ],
            "manual_review_required": True,
            "source_evidence": {
                "contract": check.get("contract"),
                "owner_lane": check.get("owner_lane"),
                "consumed_by_lanes": check.get("consumed_by_lanes", []),
                "missing_required_terms": missing_required,
                "missing_recommended_terms": missing_recommended,
                "errors": check_errors,
                "warnings": check_warnings,
                "line_count_csv_hint": line_count_for(path_value, counts),
            },
        },
        None,
    )


def should_consider_check(check: Any) -> bool:
    if not isinstance(check, dict):
        return False
    if check.get("ok") is False:
        return True
    for field in ("missing_required_terms", "missing_recommended_terms", "errors", "warnings"):
        value = check.get(field)
        if isinstance(value, list) and value:
            return True
    return False


def build_code_patch_plan(repo_root: Path, code_drift_path: Path, line_count_csv: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    code_drift, load_errors = read_json_object(code_drift_path)
    errors.extend(f"code drift report: {error}" for error in load_errors)
    counts, count_warnings = load_line_counts(repo_root, line_count_csv)
    warnings.extend(count_warnings)

    plans: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    if code_drift:
        if code_drift.get("kind") != "code_contract_drift":
            errors.append("code drift report kind must be code_contract_drift")
        for field in ("provider_execution_performed", "patch_application_performed", "source_writes_performed"):
            if code_drift.get(field) is not False:
                errors.append(f"code drift report {field} must be false")
        checks = code_drift.get("checks", [])
        if not isinstance(checks, list):
            errors.append("code drift report checks must be a list")
            checks = []
        for index, check in enumerate(checks, start=1):
            if not should_consider_check(check):
                continue
            plan, skip = plan_from_check(index, repo_root, check, counts)
            if plan:
                plans.append(plan)
            if skip:
                skipped.append(skip)

    if code_drift and not plans:
        warnings.append("no code patch plans were produced from code_contract_drift checks")

    return {
        "schema_version": 1,
        "kind": PLAN_KIND,
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "apply_mode": APPLY_MODE,
        "inputs": {
            "code_contract_drift_report": repo_rel(repo_root, code_drift_path),
            "line_count_csv": repo_rel(repo_root, line_count_csv),
            "line_count_csv_loaded": bool(counts),
        },
        "patch_plan_count": len(plans),
        "code_patch_plans": plans,
        "skipped_candidate_count": len(skipped),
        "skipped_candidates": skipped,
        "decision": {
            "ready_for_manual_review": bool(plans) and not errors,
            "patch_plan_count": len(plans),
            "manual_review_required": True,
            "recommended_next_layer": "manual_review_then_targeted_code_pr" if plans and not errors else "collect_or_fix_code_contract_evidence",
        },
        "guardrails": {
            "report_only": True,
            "manual_review_required": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "sqlite_write_performed": False,
            "npu_primary_advisory": False,
            "openvino_gpu_primary_lane": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Code Patch Plan", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Manual review required: `{report['manual_review_required']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Source writes performed: `{report['source_writes_performed']}`")
    lines.append(f"- Patch plan count: `{report['patch_plan_count']}`")
    lines.append("")
    lines.append("## Inputs")
    lines.append("")
    for key, value in report.get("inputs", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Plans")
    lines.append("")
    if not report.get("code_patch_plans"):
        lines.append("- none")
    for plan in report.get("code_patch_plans", []):
        lines.append(f"### `{plan['id']}`")
        lines.append("")
        lines.append(f"- Area: `{plan['area']}`")
        lines.append(f"- Risk: `{plan['risk']}`")
        lines.append(f"- Status: `{plan['status']}`")
        lines.append(f"- Target files: `{', '.join(plan['target_files'])}`")
        lines.append(f"- Rationale: {plan['rationale']}")
        lines.append(f"- Strategy: {plan['edit_strategy']}")
        lines.append("")
    if report.get("skipped_candidates"):
        lines.append("## Skipped candidates")
        lines.append("")
        for item in report["skipped_candidates"]:
            lines.append(f"- `{item.get('id')}` `{item.get('path', '')}`: {item.get('reason')}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("This artifact is a code patch plan only. It contains no replacements and must not be treated as an apply queue.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--code-contract-drift-report", default=DEFAULT_CODE_DRIFT_REPORT)
    parser.add_argument("--line-count-csv", default=DEFAULT_LINE_COUNT_CSV)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    code_drift_path = resolve_output_path(repo_root, args.code_contract_drift_report)
    line_count_csv = resolve_output_path(repo_root, args.line_count_csv)
    report = build_code_patch_plan(repo_root, code_drift_path, line_count_csv)

    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    text = write_json_report(report, output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
