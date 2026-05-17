"""Shared helpers and constants for megalithic review refinement."""

from __future__ import annotations

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REVIEW = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_repo_review.json"
DEFAULT_PROPOSALS = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_repo_review_proposals.json"
DEFAULT_OUTPUT = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review.json"
DEFAULT_PROPOSALS_OUTPUT = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_proposals.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review.md"
KNOWN_TOP_LEVELS = {
    ".github",
    "docs",
    "Tools",
    "Scripting",
    "patch_specs",
    "EXECUTION_PLANS",
    "old script legacy",
    "indexAI",
    "output",
}
KNOWN_ROOT_FILES = {"AGENTS.md", "WORKFLOW.md", "CONTRIBUTING.md", "README.md"}
LOW_SIGNAL_DOCS = {".aider.chat.history.md"}
BACKUP_OR_GENERATED_SEGMENTS = {
    "old script legacy",
    "v61b_backgood",
    "indexAI",
}
PLACEHOLDER_PATH_REFERENCES = {
    "Scripting/package_name",
    "Tools/validation/fixtures",
    "patch_specs/inbox",
    "Tools/npu/npu_preflight_report.json",
}
GENERATED_REFERENCE_PREFIXES = ("output/", "indexAI/")
PATH_ALIAS_PREFIXES = (
    ("EXECUTION_PLANS/", "docs/EXECUTION_PLANS/"),
    ("github/workflows/", ".github/workflows/"),
    (".github/workflows/", ".github/workflows/"),
)
ALLOW_DUPLICATE_SYMBOLS = {
    "__init__",
    "main",
    "execute",
    "draw",
    "add",
    "add_error",
    "add_item",
    "append_output",
    "apply_filter",
    "artifact_extra_roots",
    "ask_bool",
    "build_inventory",
    "build_layout",
    "build_ollama_prompt",
    "build_packet",
    "build_plan",
    "build_proposals",
    "build_report",
    "build_steps",
    "check_policy",
    "classify_path",
    "cleanup_intermediates",
    "cleanup_render_frames",
    "compact",
    "compact_text",
    "configure_headings",
    "copy_selected_path",
    "dry_run_spec",
    "ensure_repo_imports",
    "extract_symbols",
    "file_meta",
    "file_record",
    "format_symbol_summary",
    "from_mapping",
    "Get-RepoRelativePath",
    "Invoke-Step",
    "Resolve-ExistingPath",
    "Resolve-RepoRoot",
    "Write-Step",
}
CONCEPTUAL_SLASH_RE = re.compile(r"^[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)+$")

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))

def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

def repo_root_from_review(review: dict[str, Any]) -> Path:
    raw = review.get("repo_root") or "."
    return Path(str(raw)).resolve()

def normalize_reference(reference: str) -> str:
    return reference.strip().strip('`.,:)];"').replace("\\", "/").lstrip("/")

def candidate_references(reference: str) -> list[str]:
    ref = normalize_reference(reference)
    candidates = [ref]
    if ref in KNOWN_ROOT_FILES:
        candidates.append(ref)
    for prefix, replacement in PATH_ALIAS_PREFIXES:
        if ref.startswith(prefix):
            candidates.append(replacement + ref[len(prefix) :])
    if ref.startswith("docs/") is False and ref.startswith("EXECUTION_PLANS/"):
        candidates.append("docs/" + ref)
    return list(dict.fromkeys(item for item in candidates if item))

def existing_candidate(reference: str, repo_root: Path) -> str | None:
    for candidate in candidate_references(reference):
        path = repo_root / candidate
        if path.exists():
            return candidate
    return None

def has_path_intent(reference: str) -> bool:
    ref = normalize_reference(reference)
    if not ref or ref.startswith(("http://", "https://")):
        return False
    if ref in KNOWN_ROOT_FILES:
        return True
    first = ref.split("/", 1)[0]
    if first in KNOWN_TOP_LEVELS:
        return True
    suffix = Path(ref).suffix.lower()
    return suffix in {".py", ".ps1", ".sh", ".md", ".json", ".yaml", ".yml", ".txt"}

def is_conceptual_slash_term(reference: str) -> bool:
    ref = normalize_reference(reference)
    if has_path_intent(ref):
        return False
    if "." in ref and "/" not in ref:
        return False
    return bool(CONCEPTUAL_SLASH_RE.match(ref))

def is_placeholder_reference(reference: str) -> bool:
    ref = normalize_reference(reference)
    return ref in PLACEHOLDER_PATH_REFERENCES or any(
        ref.startswith(prefix) for prefix in GENERATED_REFERENCE_PREFIXES
    )

def classify_ai_workload_failure(report: dict[str, Any]) -> dict[str, Any]:
    errors = report.get("errors") or []
    npu_only = bool(errors) and all(str(item).lower().startswith("npu:") for item in errors)
    if report.get("kind") == "ai_workload_report_quality" and npu_only:
        return {
            "classification": "expected_guardrail",
            "severity": "info",
            "area": "advisory_quality_gate",
            "title": "NPU report excluded by AI workload quality gate",
            "details": [
                "The ai_workload_report_quality report failed because the NPU workload text is unusable.",
                "This is expected fail-closed behavior when Ollama/GPU remains the usable advisory lane.",
                *[str(item) for item in errors],
            ],
        }
    return {
        "classification": "actionable_failure",
        "severity": "high",
        "area": "validation_reports",
        "title": "Validation report failure requires review",
        "details": [f"{report.get('path')}: {errors}"],
    }

def refine_validation_reports(
    review: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    actionable: list[dict[str, Any]] = []
    informational: list[dict[str, Any]] = []
    for report in review.get("validation_reports", []):
        if not report.get("exists"):
            actionable.append(
                {
                    "severity": "medium",
                    "area": "validation_reports",
                    "title": "Expected validation report is missing",
                    "details": [str(report.get("path"))],
                }
            )
            continue
        if report.get("passed") is False:
            classified = classify_ai_workload_failure(report)
            if classified["classification"] == "expected_guardrail":
                informational.append(classified)
            else:
                actionable.append(classified)
    return actionable, informational
