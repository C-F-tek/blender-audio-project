"""Input evidence summarizers for selective execution plans."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from .common import read_json_object, read_text_file, repo_relative

def summarize_context_evidence(json_path: Path, md_path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize context-pack evidence from JSON when present, else Markdown."""
    data, error = read_json_object(json_path)
    if data is not None:
        decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
        return {
            "path": repo_relative(json_path, repo_root),
            "exists": True,
            "json_ok": True,
            "markdown_fallback": False,
            "kind": data.get("kind"),
            "passed": data.get("passed"),
            "provider_execution_performed": data.get("provider_execution_performed"),
            "included_file_count": data.get("included_file_count"),
            "forbidden_path_count": data.get("forbidden_path_count"),
            "source_writes_performed": decision.get("source_writes_performed"),
            "provider_execution_seen": decision.get("provider_execution_seen"),
            "errors": (data.get("errors") if isinstance(data.get("errors"), list) else []),
            "warnings": (data.get("warnings") if isinstance(data.get("warnings"), list) else []),
        }

    text, text_error, truncated = read_text_file(md_path)
    markdown_passed = text is not None and "- Passed: `True`" in text
    return {
        "path": repo_relative(json_path, repo_root),
        "exists": json_path.exists(),
        "json_ok": False,
        "json_error": error,
        "markdown_path": repo_relative(md_path, repo_root),
        "markdown_exists": md_path.exists(),
        "markdown_fallback": text is not None,
        "markdown_truncated": truncated,
        "kind": "ai_context_pack_evidence",
        "passed": markdown_passed if text is not None else None,
        "provider_execution_performed": (
            False if text and "Provider execution performed: `False`" in text else None
        ),
        "source_writes_performed": (
            False if text and "source_writes_performed`: `False`" in text else None
        ),
        "provider_execution_seen": (
            False if text and "provider_execution_seen`: `False`" in text else None
        ),
        "errors": [error] if error else [],
        "warnings": (
            [f"using Markdown fallback: {repo_relative(md_path, repo_root)}"]
            if text is not None
            else [text_error or "context evidence missing"]
        ),
    }

def summarize_dry_run_evidence(path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize dry-run matrix evidence."""
    data, error = read_json_object(path)
    if data is None:
        return {
            "path": repo_relative(path, repo_root),
            "exists": path.exists(),
            "json_ok": False,
            "passed": False,
            "error": error,
            "provider_execution_performed": None,
            "case_count": None,
            "matrix_workers": None,
            "repeat_cases": None,
            "all_steps_planned_only": None,
        }

    matrix = data.get("matrix") if isinstance(data.get("matrix"), dict) else {}
    summary = data.get("case_summary") if isinstance(data.get("case_summary"), dict) else {}
    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    return {
        "path": repo_relative(path, repo_root),
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "case_count": summary.get("case_count"),
        "matrix_workers": matrix.get("matrix_workers"),
        "repeat_cases": matrix.get("repeat_cases"),
        "all_cases_dry_run": decision.get("all_cases_dry_run"),
        "all_steps_planned_only": decision.get("all_steps_planned_only"),
        "gpu_npu_workloads_executed": decision.get("gpu_npu_workloads_executed"),
        "errors": data.get("errors") if isinstance(data.get("errors"), list) else [],
        "warnings": (data.get("warnings") if isinstance(data.get("warnings"), list) else []),
    }

def summarize_provider_evidence(path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize compact provider evidence."""
    data, error = read_json_object(path)
    if data is None:
        return {
            "path": repo_relative(path, repo_root),
            "exists": path.exists(),
            "json_ok": False,
            "passed": False,
            "error": error,
            "provider_execution_seen": False,
            "ollama_gpu_primary_advisory": False,
            "npu_excluded_when_unusable": False,
        }

    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    reports = data.get("reports") if isinstance(data.get("reports"), list) else []
    report_kinds = [
        str(item.get("kind")) for item in reports if isinstance(item, dict) and item.get("kind")
    ]
    report_pass_count = sum(
        1 for item in reports if isinstance(item, dict) and item.get("passed") is True
    )
    return {
        "path": repo_relative(path, repo_root),
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "generated_at": data.get("generated_at"),
        "report_count": len(reports),
        "report_pass_count": report_pass_count,
        "report_kinds": sorted(report_kinds),
        "ollama_gpu_primary_advisory": decision.get("ollama_gpu_primary_advisory"),
        "npu_excluded_when_unusable": decision.get("npu_excluded_when_unusable"),
        "provider_execution_seen": decision.get("provider_execution_seen"),
    }

def summarize_validation_contract(path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize validation report contract output if available."""
    data, error = read_json_object(path)
    if data is None:
        return {
            "path": repo_relative(path, repo_root),
            "exists": path.exists(),
            "json_ok": False,
            "passed": None,
            "error": error,
            "warnings": [
                "validation report contract output is local/ignored and may be absent on GitHub"
            ],
        }
    return {
        "path": repo_relative(path, repo_root),
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "errors": data.get("errors") if isinstance(data.get("errors"), list) else [],
        "warnings": (data.get("warnings") if isinstance(data.get("warnings"), list) else []),
    }

def summarize_execution_plans(plan_dir: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize active execution plans without validating their full contract."""
    plans: list[dict[str, Any]] = []
    if plan_dir.exists():
        for path in sorted(plan_dir.glob("*.md")):
            text, error, truncated = read_text_file(path, max_chars=8000)
            lowered = text.lower() if text else ""
            plans.append(
                {
                    "path": repo_relative(path, repo_root),
                    "exists": True,
                    "truncated": truncated,
                    "mentions_selective_planner": "selective planner" in lowered
                    or "selective_planner" in lowered,
                    "mentions_patch_spec": "patch spec" in lowered or "patch-spec" in lowered,
                    "mentions_context_pack": "context pack" in lowered,
                    "error": error,
                }
            )
    return {
        "path": repo_relative(plan_dir, repo_root),
        "exists": plan_dir.exists(),
        "active_plan_count": len(plans),
        "related_plan_count": sum(
            1 for item in plans if item["mentions_selective_planner"] or item["mentions_patch_spec"]
        ),
        "plans": plans,
    }

def summarize_tech_debt(path: Path, repo_root: Path) -> dict[str, Any]:
    """Summarize tech-debt markers relevant to this planner."""
    text, error, truncated = read_text_file(path, max_chars=16000)
    lowered = text.lower() if text else ""
    keywords = {
        "selective_planner": "selective planner" in lowered or "selective_planner" in lowered,
        "patch_spec": "patch spec" in lowered or "patch-spec" in lowered,
        "context_pack": "context pack" in lowered,
        "provider_quality_gate": "quality gate" in lowered
        and ("provider" in lowered or "gpu" in lowered or "npu" in lowered),
    }
    return {
        "path": repo_relative(path, repo_root),
        "exists": path.exists(),
        "read_ok": text is not None,
        "truncated": truncated,
        "keywords": keywords,
        "error": error,
    }
