"""Shared dependencies/constants for agent-review code patch plans."""

from __future__ import annotations

from Tools.ai._shared.code_patch_plan_common import (
    line_count_for,
    load_line_counts,
    normalize_repo_path,
    now_iso,
    read_json_object,
    repo_rel,
    report_only_guardrails,
    resolve_output_path,
    target_path_errors,
    write_json_and_markdown,
)

PLAN_KIND = "agent_review_code_patch_plan"
APPLY_MODE = "report_only_manual_review_code_patch_plan"
DEFAULT_CODE_DRIFT_REPORT = "output/validation/code_contract_drift.json"
DEFAULT_OUTPUT = "output/patch_specs/agent_review_code_patch_plan.json"
DEFAULT_MARKDOWN = "output/patch_specs/agent_review_code_patch_plan.md"
DEFAULT_LINE_COUNT_CSV = "docs/LOCAL_VALIDATION_EVIDENCE/python_line_count_20260501-215122.csv"
DEFAULT_VALIDATION_COMMANDS = [
    r"python -m Tools.validation check_python_syntax --repo-root . --output .\output\validation\python_syntax.json",
    r"python -m Tools.validation check_validation_report_contract --repo-root . --output .\output\validation\validation_report_contract.json",
    "git diff --check",
]
COMMON_STOP_CONDITIONS = [
    "Stop if the edit requires provider execution, Blender runtime execution, or patch auto-apply.",
    "Stop if the patch touches output/**, generated indexes, full analysis JSON, SQLite, secrets, permissions, billing, or repository visibility.",
    "Stop if local validation fails.",
]
MAX_STATIC_RECOMMENDATIONS = 30
