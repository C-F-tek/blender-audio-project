#!/usr/bin/env python3
"""Build compact Git-trackable evidence from local generated reports.

The repository ignores ``output/`` by design, so long local validation/provider
reports should not be pasted into chat or committed directly. This helper reads
selected local reports and writes a compact evidence bundle under a normal docs
path that can be reviewed and pushed with Git CLI.

It does not execute providers and does not modify runtime outputs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REPORTS = (
    "output/validation/ai_workload_report_quality.json",
    "output/validation/ai_workload_quality_lane_routing.json",
    "output/validation/npu_decode_quality_remediation.json",
    "output/validation/npu_decode_smoke_diagnostic.json",
    "output/validation/local_provider_probe.json",
    "output/validation/npu_runtime_output_manifest.json",
    "output/validation/provider_result_report.json",
)

DEFAULT_SELECTED_CHUNKS_EVIDENCE = (
    "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json",
)

MAX_ARTIFACT_PREVIEW_CHARS = 1500
MAX_PATCH_PLAN_TEXT_CHARS = 1200
DEFAULT_INCLUDED_ARTIFACT_CHARS = 6000
DEFAULT_MAX_INCLUDED_ARTIFACTS = 40
CONTENT_EXTENSION_ALLOWLIST = {".json", ".md", ".txt", ".csv", ".yml", ".yaml", ".toml", ".ini", ".cfg", ".py", ".ps1"}

RAW_ARTIFACT_DENY_PREFIXES = (
    "output/ai_context_packs/",
    "output/ai_pipeline/gpu_deep_planning_parallel_checkpoints/",
    "output/ai_pipeline/gpu_planner_nonempty_diagnostics_checkpoints",
    "output/ai_pipeline/gpu_planner_fallback_verify_checkpoints",
    "output/ai_pipeline/gpu_planner_full_after_fallback_fix_checkpoints",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "renders/",
)

RAW_ARTIFACT_DENY_FRAGMENTS = (
    "full_analysis",
    "analysis_full",
    ".sqlite",
    ".db",
    "_npu_async_audit_context",
    "_npu_async_audit_npu",
    "_npu_async_audit_npu_notes",
)


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def read_text(path: Path) -> tuple[str, str | None]:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace"), None
    except Exception as exc:
        return "", f"{type(exc).__name__}: {exc}"


def sha256_file(path: Path) -> str | None:
    if not path.exists() or not path.is_file():
        return None
    digest = hashlib.sha256()
    try:
        with path.open("rb") as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                digest.update(chunk)
    except OSError:
        return None
    return digest.hexdigest()


def line_count(text: str) -> int:
    if not text:
        return 0
    return text.count("\n") + (0 if text.endswith("\n") else 1)


def compact_value(value: Any, *, max_string: int = 500) -> Any:
    if isinstance(value, str):
        return value if len(value) <= max_string else value[:max_string] + "...[truncated]"
    if isinstance(value, list):
        return [compact_value(item, max_string=max_string) for item in value[:20]]
    if isinstance(value, dict):
        return {str(key): compact_value(item, max_string=max_string) for key, item in value.items()}
    return value


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def list_contains(value: Any, expected: str) -> bool:
    return any(str(item).lower() == expected.lower() for item in as_list(value))


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def repo_relative(path: Path, repo_root: Path) -> str:
    if path.is_absolute() and path.is_relative_to(repo_root):
        return path.relative_to(repo_root).as_posix()
    return str(path).replace("\\", "/")


def normalize_manifest_path(path: Path, repo_root: Path) -> str:
    return repo_relative(path, repo_root).replace("\\", "/")


def raw_artifact_content_allowed(rel_path: str) -> bool:
    lower = rel_path.lower().replace("\\", "/")
    if any(lower.startswith(prefix.lower()) for prefix in RAW_ARTIFACT_DENY_PREFIXES):
        return False
    if any(fragment.lower() in lower for fragment in RAW_ARTIFACT_DENY_FRAGMENTS):
        return False
    return True


def compact_patch_plan(plan: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": plan.get("id"),
        "area": plan.get("area"),
        "source": plan.get("source"),
        "risk": plan.get("risk"),
        "status": plan.get("status"),
        "target_files": compact_value(plan.get("target_files") or [], max_string=300),
        "rationale": compact_value(plan.get("rationale") or "", max_string=MAX_PATCH_PLAN_TEXT_CHARS),
        "edit_strategy": compact_value(plan.get("edit_strategy") or "", max_string=MAX_PATCH_PLAN_TEXT_CHARS),
        "validation_commands": compact_value(plan.get("validation_commands") or [], max_string=500),
        "stop_conditions": compact_value(plan.get("stop_conditions") or [], max_string=500),
        "manual_review_required": plan.get("manual_review_required"),
    }


def summarize_patch_plan_report(data: dict[str, Any]) -> dict[str, Any] | None:
    if data.get("kind") != "agent_review_patch_plan":
        return None

    decision = data.get("decision") if isinstance(data.get("decision"), dict) else {}
    patch_plans = data.get("patch_plans") if isinstance(data.get("patch_plans"), list) else []

    return {
        "patch_plan_count": data.get("patch_plan_count", len(patch_plans)),
        "fallback_used": decision.get("fallback_used"),
        "manual_review_required": decision.get("manual_review_required"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "plans": [compact_patch_plan(plan) for plan in patch_plans if isinstance(plan, dict)],
    }


def summarize_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    rel = normalize_manifest_path(path, repo_root)
    item: dict[str, Any] = {
        "path": rel,
        "exists": path.exists(),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        "sha256": sha256_file(path),
        "content_included": False,
        "role": "local_artifact_reference",
    }

    if not path.exists() or not path.is_file():
        return item

    if path.suffix.lower() in CONTENT_EXTENSION_ALLOWLIST and raw_artifact_content_allowed(rel):
        text, error = read_text(path)
        if error:
            item["read_error"] = error
            return item
        item["preview"] = text[:MAX_ARTIFACT_PREVIEW_CHARS]
        item["preview_chars"] = min(len(text), MAX_ARTIFACT_PREVIEW_CHARS)
        item["line_count"] = line_count(text)
        item["content_included"] = bool(item["preview"])

    return item


def build_included_artifact(path: Path, repo_root: Path, *, max_chars: int, role: str) -> dict[str, Any]:
    rel = normalize_manifest_path(path, repo_root)
    item: dict[str, Any] = {
        "path": rel,
        "exists": path.exists(),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
        "sha256": sha256_file(path),
        "role": role,
        "content_included": False,
        "content_truncated": False,
    }
    if not path.exists() or not path.is_file():
        return item
    if path.suffix.lower() not in CONTENT_EXTENSION_ALLOWLIST:
        item["skip_reason"] = "suffix_not_text_allowlisted"
        return item
    if not raw_artifact_content_allowed(rel):
        item["skip_reason"] = "raw_artifact_content_denied_by_policy"
        return item
    text, error = read_text(path)
    if error:
        item["read_error"] = error
        return item
    item["line_count"] = line_count(text)
    item["raw_chars"] = len(text)
    item["included_chars"] = min(len(text), max_chars)
    item["content"] = text[:max_chars]
    item["content_truncated"] = len(text) > max_chars
    item["content_included"] = True
    return item


def discover_related_artifacts(repo_root: Path, report_paths: list[Path]) -> list[Path]:
    """Discover useful sibling artifacts for bundle output.

    The input model stays report/MD driven. This discovery only enriches the
    output bundle with bounded contents that the tool can infer are relevant.
    """
    discovered: list[Path] = []
    for report in report_paths:
        if report.suffix.lower() == ".json":
            sibling_md = report.with_suffix(".md")
            if sibling_md.exists():
                discovered.append(sibling_md)
        data = read_json(report)
        if not data:
            continue
        for key in ("markdown_output", "markdown_report", "csv_written"):
            value = data.get(key)
            if isinstance(value, str):
                discovered.append(resolve_repo_path(repo_root, value))
        inputs = data.get("inputs") if isinstance(data.get("inputs"), dict) else {}
        for value in inputs.values():
            if isinstance(value, str) and value:
                path = resolve_repo_path(repo_root, value)
                if path.exists() and path.is_file():
                    discovered.append(path)
    unique: dict[str, Path] = {}
    for path in discovered:
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        unique[key] = path
    return sorted(unique.values(), key=lambda item: normalize_manifest_path(item, repo_root).lower())


def summarize_report(path: Path, repo_root: Path) -> dict[str, Any]:
    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {"path": rel, "exists": path.exists(), "json_ok": False, "kind": None, "passed": None, "summary": {}}

    summary: dict[str, Any] = {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "patch_application_performed": data.get("patch_application_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }
    for key in (
        "usable_lanes", "unusable_lanes", "primary_advisory_provider", "policy", "mode", "provider", "python_exe", "device",
        "model_dir", "proposal_count", "patch_plan_count", "fallback_used", "manual_review_required", "recommendation_count",
        "round_count", "empty_recommendations_reason", "evidence_ready_for_manual_patch_count", "recommended_next_layer",
    ):
        if key in data:
            summary[key] = compact_value(data.get(key))
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    if checks:
        summary["checks"] = compact_value({key: checks.get(key) for key in ("classification", "usable_for_advisory", "npu_usable_for_advisory", "npu_classification", "metrics", "npu_metrics", "provider_envelope", "promotion_gate", "required_promotion_gate") if key in checks}, max_string=350)
    routing = data.get("routing") if isinstance(data.get("routing"), dict) else {}
    if routing:
        summary["routing"] = compact_value({"advisory_lanes": routing.get("advisory_lanes"), "excluded_advisory_lanes": routing.get("excluded_advisory_lanes"), "primary_advisory_provider": routing.get("primary_advisory_provider"), "trusted_context_files": routing.get("trusted_context_files"), "excluded_context_files": routing.get("excluded_context_files")}, max_string=350)
    context = data.get("context") if isinstance(data.get("context"), dict) else {}
    if context:
        summary["context"] = compact_value({"context_files": context.get("context_files"), "excluded_context_files": context.get("excluded_context_files"), "advisory_context_routing": context.get("advisory_context_routing")}, max_string=350)
    ollama = data.get("ollama") if isinstance(data.get("ollama"), dict) else {}
    if ollama:
        summary["ollama"] = compact_value({"used": ollama.get("used"), "model": ollama.get("model"), "error": ollama.get("error"), "text_preview": (ollama.get("text") or "")[:500]}, max_string=500)

    patch_plan_summary = summarize_patch_plan_report(data)
    if patch_plan_summary:
        summary["patch_plan_summary"] = patch_plan_summary

    return {"path": rel, "exists": True, "json_ok": True, "kind": data.get("kind"), "passed": data.get("passed"), "summary": summary}


def summarize_selected_chunks_evidence(path: Path, repo_root: Path) -> dict[str, Any]:
    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {"path": rel, "exists": path.exists(), "json_ok": False, "kind": None, "passed": None, "summary": {}}

    summary: dict[str, Any] = {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "selected_count": data.get("selected_count"),
        "total_selected_chars": data.get("total_selected_chars"),
        "max_chunks": data.get("max_chunks"),
        "max_total_chars": data.get("max_total_chars"),
        "source_bundle": data.get("source_bundle"),
        "source_chunks": data.get("source_chunks"),
        "decision": compact_value(data.get("decision") or {}),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }
    return {"path": rel, "exists": True, "json_ok": True, "kind": data.get("kind"), "passed": data.get("passed"), "summary": summary}


def discover_selected_chunks_evidence(repo_root: Path, explicit_paths: list[str]) -> list[Path]:
    candidates = split_path_values(explicit_paths)
    if not candidates:
        candidates = list(DEFAULT_SELECTED_CHUNKS_EVIDENCE)
        evidence_dir = repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE"
        if evidence_dir.exists():
            for path in sorted(evidence_dir.glob("*selected_chunks_evidence.json")):
                rel = repo_relative(path, repo_root)
                if rel not in candidates:
                    candidates.append(rel)
    resolved: list[Path] = []
    seen: set[str] = set()
    for raw in candidates:
        path = resolve_repo_path(repo_root, raw)
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        if key not in seen and path.exists():
            resolved.append(path)
            seen.add(key)
    return resolved


def report_summaries(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item.get("summary", {}) for item in reports if isinstance(item.get("summary"), dict)]


def selected_chunks_evidence_seen(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    return any(item.get("exists") is True and item.get("json_ok") is True for item in selected_chunks_evidence)


def selected_chunks_built(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(selected_chunks_evidence):
        decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
        if decision.get("selected_chunks_built") is True:
            return True
        if isinstance(summary.get("selected_count"), int) and summary.get("selected_count", 0) > 0:
            return True
    return False


def selected_chunks_budget_respected(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(selected_chunks_evidence):
        decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
        if decision.get("budget_respected") is True:
            return True
        total_chars = summary.get("total_selected_chars")
        max_total_chars = summary.get("max_total_chars")
        if isinstance(total_chars, int) and isinstance(max_total_chars, int) and total_chars <= max_total_chars:
            return True
    return False


def npu_marked_unusable(reports: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(reports):
        if list_contains(summary.get("unusable_lanes"), "npu"):
            return True
        checks = summary.get("checks") if isinstance(summary.get("checks"), dict) else {}
        if checks.get("npu_usable_for_advisory") is False:
            return True
        if str(checks.get("npu_classification") or "").lower() in {"unusable_output", "unusable"}:
            return True
    return False


def npu_marked_excluded_from_advisory(reports: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(reports):
        routing = summary.get("routing") if isinstance(summary.get("routing"), dict) else {}
        if list_contains(routing.get("excluded_advisory_lanes"), "npu"):
            return True
        for ctx in as_list(routing.get("excluded_context_files")):
            if isinstance(ctx, dict) and ctx.get("lane") == "npu" and ctx.get("trusted") is False:
                return True
        context = summary.get("context") if isinstance(summary.get("context"), dict) else {}
        excluded_context = context.get("excluded_context_files") or []
        if "output/ai_packets/npu_real_workload_report.md" in excluded_context:
            return True
        advisory_routing = context.get("advisory_context_routing") if isinstance(context.get("advisory_context_routing"), dict) else {}
        if list_contains(advisory_routing.get("excluded_advisory_lanes"), "npu"):
            return True
    return False


def npu_excluded_when_unusable(reports: list[dict[str, Any]]) -> bool:
    return npu_marked_unusable(reports) and npu_marked_excluded_from_advisory(reports)


def build_bundle(
    repo_root: Path,
    report_paths: list[str],
    basename: str,
    output_dir: Path,
    selected_chunks_paths: list[str],
    artifact_paths: list[str],
    auto_include_related: bool,
    max_included_artifact_chars: int,
    max_included_artifacts: int,
) -> tuple[dict[str, Any], str]:
    resolved = [resolve_repo_path(repo_root, raw) for raw in report_paths]
    reports = [summarize_report(path, repo_root) for path in resolved]
    artifact_manifest = [summarize_artifact(path, repo_root) for path in resolved]
    selected_paths = discover_selected_chunks_evidence(repo_root, selected_chunks_paths)
    selected_chunks_evidence = [summarize_selected_chunks_evidence(path, repo_root) for path in selected_paths]

    explicit_artifacts = [resolve_repo_path(repo_root, raw) for raw in split_path_values(artifact_paths)]
    auto_artifacts = discover_related_artifacts(repo_root, resolved) if auto_include_related else []
    included_candidates: list[tuple[Path, str]] = [(path, "explicit_artifact") for path in explicit_artifacts]
    included_candidates.extend((path, "auto_related_artifact") for path in auto_artifacts)
    deduped: dict[str, tuple[Path, str]] = {}
    for path, role in included_candidates:
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        deduped[key] = (path, role)
    included_artifacts = [
        build_included_artifact(path, repo_root, max_chars=max_included_artifact_chars, role=role)
        for path, role in list(deduped.values())[:max_included_artifacts]
    ]

    bundle = {
        "schema_version": 1,
        "kind": "github_validation_evidence_bundle",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_reports": [item["path"] for item in reports],
        "source_selected_chunks_evidence": [item["path"] for item in selected_chunks_evidence],
        "source_included_artifacts": [item["path"] for item in included_artifacts],
        "reports": reports,
        "selected_chunks_evidence": selected_chunks_evidence,
        "artifact_manifest": artifact_manifest,
        "included_artifacts": included_artifacts,
        "included_artifact_policy": {
            "auto_include_related_artifacts": auto_include_related,
            "max_included_artifact_chars": max_included_artifact_chars,
            "max_included_artifacts": max_included_artifacts,
            "content_extension_allowlist": sorted(CONTENT_EXTENSION_ALLOWLIST),
            "raw_artifact_deny_prefixes": list(RAW_ARTIFACT_DENY_PREFIXES),
            "raw_artifact_deny_fragments": list(RAW_ARTIFACT_DENY_FRAGMENTS),
        },
        "decision": {
            "ollama_gpu_primary_advisory": any((item.get("summary", {}).get("primary_advisory_provider", {}) or {}).get("provider") == "ollama" or (item.get("summary", {}).get("routing", {}).get("primary_advisory_provider", {}) or {}).get("provider") == "ollama" or (item.get("summary", {}).get("ollama", {}) or {}).get("used") is True for item in reports),
            "npu_excluded_when_unusable": npu_excluded_when_unusable(reports),
            "provider_execution_seen": any(item.get("summary", {}).get("provider_execution_performed") is True for item in reports),
            "npu_decode_smoke_passed": any(item.get("kind") == "npu_decode_smoke_diagnostic" and item.get("passed") is True and item.get("summary", {}).get("provider_execution_performed") is True for item in reports),
            "selected_chunks_evidence_seen": selected_chunks_evidence_seen(selected_chunks_evidence),
            "selected_chunks_built": selected_chunks_built(selected_chunks_evidence),
            "budget_respected": selected_chunks_budget_respected(selected_chunks_evidence),
            "artifact_manifest_built": bool(artifact_manifest),
            "included_artifacts_built": bool(included_artifacts),
            "included_artifact_count": len(included_artifacts),
            "patch_plan_summary_seen": any(bool(item.get("summary", {}).get("patch_plan_summary")) for item in reports),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    md_path = output_dir / f"{basename}.md"
    json_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(bundle), encoding="utf-8")
    return bundle, f"{json_path}\n{md_path}"


def render_report_entry(lines: list[str], item: dict[str, Any]) -> None:
    summary = item.get("summary", {})
    lines.append(f"### `{item['path']}`")
    lines.append("")
    lines.append(f"- Exists: `{item['exists']}`")
    lines.append(f"- JSON OK: `{item['json_ok']}`")
    lines.append(f"- Kind: `{item.get('kind')}`")
    lines.append(f"- Passed: `{item.get('passed')}`")
    for field, label in (
        ("provider_execution_performed", "Provider execution performed"),
        ("patch_application_performed", "Patch application performed"),
        ("source_writes_performed", "Source writes performed"),
        ("patch_plan_count", "Patch plan count"),
        ("recommendation_count", "Recommendation count"),
        ("recommended_next_layer", "Recommended next layer"),
        ("selected_count", "Selected count"),
        ("total_selected_chars", "Total selected chars"),
        ("max_total_chars", "Max total chars"),
        ("usable_lanes", "Usable lanes"),
        ("unusable_lanes", "Unusable lanes"),
        ("primary_advisory_provider", "Primary advisory provider"),
        ("python_exe", "Python executable"),
    ):
        if summary.get(field) is not None:
            lines.append(f"- {label}: `{summary.get(field)}`")
    for field, label in (("errors", "Errors"), ("warnings", "Warnings"), ("routing", "Routing"), ("decision", "Decision"), ("ollama", "Ollama")):
        if summary.get(field):
            lines.append(f"- {label}: `{summary.get(field)}`")
    patch_plan_summary = summary.get("patch_plan_summary") or {}
    if patch_plan_summary:
        lines.append(f"- Patch plan summary count: `{patch_plan_summary.get('patch_plan_count')}`")
        lines.append(f"- Fallback used: `{patch_plan_summary.get('fallback_used')}`")
        lines.append(f"- Manual review required: `{patch_plan_summary.get('manual_review_required')}`")
    lines.append("")


def render_patch_plan_summary(lines: list[str], bundle: dict[str, Any]) -> None:
    entries: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for item in bundle.get("reports", []):
        summary = item.get("summary", {}) if isinstance(item.get("summary"), dict) else {}
        patch_plan_summary = summary.get("patch_plan_summary") if isinstance(summary.get("patch_plan_summary"), dict) else {}
        if patch_plan_summary:
            entries.append((item, patch_plan_summary))
    if not entries:
        return
    lines.append("## Patch plan summary")
    lines.append("")
    for item, patch_plan_summary in entries:
        lines.append(f"### `{item.get('path')}`")
        lines.append("")
        lines.append(f"- Patch plan count: `{patch_plan_summary.get('patch_plan_count')}`")
        lines.append(f"- Fallback used: `{patch_plan_summary.get('fallback_used')}`")
        lines.append(f"- Manual review required: `{patch_plan_summary.get('manual_review_required')}`")
        lines.append(f"- Provider execution performed: `{patch_plan_summary.get('provider_execution_performed')}`")
        lines.append(f"- Patch application performed: `{patch_plan_summary.get('patch_application_performed')}`")
        lines.append(f"- Source writes performed: `{patch_plan_summary.get('source_writes_performed')}`")
        lines.append("")
        for plan in patch_plan_summary.get("plans", []):
            if not isinstance(plan, dict):
                continue
            lines.append(f"#### {plan.get('id')} — {plan.get('area')}")
            lines.append(f"- Source: `{plan.get('source')}`")
            lines.append(f"- Risk: `{plan.get('risk')}`")
            lines.append(f"- Status: `{plan.get('status')}`")
            lines.append(f"- Target files: `{plan.get('target_files')}`")
            lines.append(f"- Rationale: {plan.get('rationale')}")
            lines.append(f"- Strategy: {plan.get('edit_strategy')}")
            lines.append("")
        lines.append("")


def render_artifact_manifest(lines: list[str], bundle: dict[str, Any]) -> None:
    manifest = bundle.get("artifact_manifest") or []
    if not manifest:
        return
    lines.append("## Artifact manifest")
    lines.append("")
    for item in manifest:
        if isinstance(item, dict):
            lines.append(f"- `{item.get('path')}` exists=`{item.get('exists')}` size=`{item.get('size_bytes')}` suffix=`{item.get('suffix')}` preview_chars=`{item.get('preview_chars')}`")
    lines.append("")


def render_included_artifacts(lines: list[str], bundle: dict[str, Any]) -> None:
    artifacts = bundle.get("included_artifacts") or []
    if not artifacts:
        return
    lines.append("## Included artifact contents")
    lines.append("")
    for item in artifacts:
        if not isinstance(item, dict):
            continue
        lines.append(f"### `{item.get('path')}`")
        lines.append("")
        lines.append(f"- Role: `{item.get('role')}`")
        lines.append(f"- Exists: `{item.get('exists')}`")
        lines.append(f"- Suffix: `{item.get('suffix')}`")
        lines.append(f"- Size bytes: `{item.get('size_bytes')}`")
        lines.append(f"- SHA-256: `{item.get('sha256')}`")
        lines.append(f"- Content included: `{item.get('content_included')}`")
        lines.append(f"- Content truncated: `{item.get('content_truncated')}`")
        if item.get("skip_reason"):
            lines.append(f"- Skip reason: `{item.get('skip_reason')}`")
        if item.get("content"):
            lines.append("")
            lines.append("```text")
            lines.append(str(item.get("content")))
            lines.append("```")
        lines.append("")


def render_markdown(bundle: dict[str, Any]) -> str:
    lines = ["# Local Validation Evidence Bundle", ""]
    lines.append(f"- Generated at: `{bundle['generated_at']}`")
    lines.append(f"- Kind: `{bundle['kind']}`")
    lines.append("")
    lines.append("## Decision summary")
    for key, value in bundle["decision"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Reports")
    lines.append("")
    for item in bundle["reports"]:
        render_report_entry(lines, item)
    render_patch_plan_summary(lines, bundle)
    render_artifact_manifest(lines, bundle)
    render_included_artifacts(lines, bundle)
    selected = bundle.get("selected_chunks_evidence") or []
    if selected:
        lines.append("## Selected chunks evidence")
        lines.append("")
        for item in selected:
            render_report_entry(lines, item)
    lines.append("## Git push helper")
    lines.append("")
    lines.append("```powershell")
    lines.append("git add docs/LOCAL_VALIDATION_EVIDENCE/")
    lines.append('git commit -m "test: add local ai workflow evidence bundle"')
    lines.append("git push")
    lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--basename", default="latest_ai_workflow_evidence")
    parser.add_argument("--output-dir", default="docs/LOCAL_VALIDATION_EVIDENCE")
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument("--artifact", action="append", default=[], help="Extra artifact file to include with bounded content; repeatable or comma-separated.")
    parser.add_argument("--no-auto-include-related-artifacts", action="store_true", help="Disable automatic inclusion of sibling/declared related artifacts.")
    parser.add_argument("--max-included-artifact-chars", type=int, default=DEFAULT_INCLUDED_ARTIFACT_CHARS)
    parser.add_argument("--max-included-artifacts", type=int, default=DEFAULT_MAX_INCLUDED_ARTIFACTS)
    parser.add_argument(
        "--selected-chunks-evidence",
        action="append",
        default=[],
        help="Compact selected-chunks evidence JSON path. Repeatable or comma-separated. If omitted, docs/LOCAL_VALIDATION_EVIDENCE/*selected_chunks_evidence.json is discovered when present.",
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir
    report_paths = split_path_values(args.report) or list(DEFAULT_REPORTS)
    bundle, outputs = build_bundle(
        repo_root,
        report_paths,
        args.basename,
        output_dir,
        list(args.selected_chunks_evidence or []),
        list(args.artifact or []),
        not args.no_auto_include_related_artifacts,
        args.max_included_artifact_chars,
        args.max_included_artifacts,
    )
    print(json.dumps({"passed": True, "outputs": outputs.splitlines(), "decision": bundle["decision"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
