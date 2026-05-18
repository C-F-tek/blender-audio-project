from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from Tools.ai._shared.code_patch_plan_common import read_json_object

LEVELS = {
    "tool",
    "app",
    "workflow",
    "ai",
    "provider",
    "validator",
    "evidence",
    "memory",
    "runtime",
}
FINAL_KINDS = {
    "agent_review_decision_loop",
    "agent_review_full_toolbox_decision_loop_integrated",
    "github_evidence_bundle_validation",
    "python_syntax",
    "validation_report_contract",
}
DEFAULT_OUTPUT = "output/validation/agent_review_warning_policy.json"
DEFAULT_MARKDOWN_OUTPUT = "output/validation/agent_review_warning_policy.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def as_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def load_report(
    repo_root: Path, value: str | Path, *, missing_is_error: bool = True
) -> tuple[Path, dict[str, Any], list[str]]:
    path = resolve_path(repo_root, value)
    data, errors = read_json_object(path, missing_is_error=missing_is_error)
    return path, data, [f"{repo_rel(path, repo_root)}: {error}" for error in errors]


def infer_level(path: str, report: dict[str, Any]) -> str:
    kind = str(report.get("kind") or "").lower()
    normalized_path = path.lower().replace("\\", "/")
    if "workflow" in kind:
        return "workflow"
    if "npu" in kind or "gpu" in kind or "provider" in kind or "parallel_gpu" in normalized_path:
        return "provider"
    if "broker" in kind or "runtime_tool" in kind:
        return "runtime"
    if "memory" in kind or "sqlite" in kind:
        return "memory"
    if "validation" in kind or "syntax" in kind or "/validation/" in normalized_path:
        return "validator"
    if "evidence" in kind or "/local_validation_evidence/" in normalized_path:
        return "evidence"
    if "decision_loop" in kind or "planner" in kind or "review" in kind or "ai" in kind:
        return "ai"
    if "app" in kind:
        return "app"
    return "tool"


def extract_reason(report: dict[str, Any]) -> str:
    for key in (
        "empty_recommendations_reason",
        "gpu_empty_recommendations_reason",
        "reason",
        "status_reason",
        "failure_reason",
    ):
        value = report.get(key)
        if value:
            return str(value)
    decision = report.get("decision")
    if isinstance(decision, dict):
        for key in ("gpu_empty_recommendations_reason", "reason", "failure_reason"):
            value = decision.get(key)
            if value:
                return str(value)
    errors = report.get("errors")
    if isinstance(errors, list) and errors:
        return "; ".join(str(item) for item in errors[:5])
    if isinstance(errors, dict) and errors:
        return json.dumps(errors, sort_keys=True, ensure_ascii=False)[:500]
    return "passed=false diagnostic report without explicit reason"


def extract_next_layer(report: dict[str, Any]) -> str:
    for key in ("recommended_next_layer", "next_best_action"):
        value = report.get(key)
        if value:
            return str(value)
    decision = report.get("decision")
    if isinstance(decision, dict):
        for key in ("recommended_next_layer", "next_best_action"):
            value = decision.get(key)
            if value:
                return str(value)
    return ""


def final_decision_recovered(
    decision_report: dict[str, Any], *, min_recommendations: int, min_patch_plans: int
) -> bool:
    if not decision_report or decision_report.get("passed") is not True:
        return False
    if as_int(decision_report.get("recommendation_count")) < min_recommendations:
        return False
    if as_int(decision_report.get("patch_plan_count")) < min_patch_plans:
        return False
    if decision_report.get("patch_application_performed") is not False:
        return False
    if decision_report.get("provider_execution_performed") not in (False, None):
        return False
    if decision_report.get("sqlite_write_performed") not in (False, None):
        return False
    if decision_report.get("persistent_memory_write_performed") not in (False, None):
        return False
    return True


def is_final_authoritative(path: str, report: dict[str, Any], final_report_paths: set[str]) -> bool:
    if path in final_report_paths:
        return True
    return str(report.get("kind") or "") in FINAL_KINDS
