#!/usr/bin/env python3
"""Run an explicit Ollama/GPU deep planning review over repository evidence.

This is the first long-running deliberative layer for IA-Carmine. Unlike smoke
validators, it is intended to keep a local Ollama model active while repeatedly
reviewing Markdown, code and previously generated agnostic artifacts.

It is still non-destructive:

- provider execution only with --use-ollama;
- no patch application;
- no GitHub PR creation;
- no SQLite writes;
- no persistent memory promotion;
- no Blender runtime execution.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.npu.ollama_runtime import DEFAULT_BASE_URL, OllamaModelManager, normalize_base_url
except ImportError:  # Script-style execution from Tools/ai.
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.npu.ollama_runtime import DEFAULT_BASE_URL, OllamaModelManager, normalize_base_url  # type: ignore

DEFAULT_EVIDENCE = "output/ai_pipeline/agent_review_evidence_sufficiency.json"
DEFAULT_REFINED = "output/ai_pipeline/local_ai_core_tool_activation_megalithic_refined_review.json"
DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_review.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_review.md"
TEXT_EXTENSIONS = {".md", ".py", ".ps1", ".sh", ".json", ".yaml", ".yml", ".txt"}
EXCLUDED_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "renders"}
EMPTY_RECOMMENDATION_REASONS = {
    "json_parse_failure",
    "valid_json_empty_recommendations",
    "recommendations_filtered_out",
    "evidence_ready_but_no_gpu_plan",
    "model_output_missing_required_fields",
    "repair_attempt_failed",
}


@dataclass(frozen=True)
class ContextFile:
    path: str
    exists: bool
    chars: int
    lines: int
    preview: str


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def safe_read_text(path: Path, max_chars: int) -> tuple[str, bool, str | None]:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as exc:
        return "", False, f"{type(exc).__name__}: {exc}"
    truncated = max_chars > 0 and len(text) > max_chars
    if truncated:
        text = text[:max_chars]
    return text, truncated, None


def context_file(repo_root: Path, path_value: str, max_chars: int) -> ContextFile:
    path = resolve_path(repo_root, path_value)
    if not path.exists() or not path.is_file():
        return ContextFile(path=repo_rel(path, repo_root), exists=False, chars=0, lines=0, preview="")
    text, truncated, error = safe_read_text(path, max_chars)
    suffix = "\n...[truncated]" if truncated else ""
    if error:
        suffix = f"\n...[read error: {error}]"
    return ContextFile(path=repo_rel(path, repo_root), exists=True, chars=len(text), lines=len(text.splitlines()), preview=text + suffix)


def context_to_dict(item: ContextFile) -> dict[str, Any]:
    return {
        "path": item.path,
        "exists": item.exists,
        "chars": item.chars,
        "lines": item.lines,
        "preview": item.preview,
    }


def should_include(path: Path, repo_root: Path) -> bool:
    try:
        rel_parts = path.relative_to(repo_root).parts
    except ValueError:
        return False
    if any(part in EXCLUDED_DIRS for part in rel_parts):
        return False
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return False
    return path.is_file()


def collect_repo_context(repo_root: Path, roots: list[str], max_files: int, max_chars_per_file: int) -> list[ContextFile]:
    results: list[ContextFile] = []
    seen: set[str] = set()
    for root_value in roots:
        root = resolve_path(repo_root, root_value)
        if root.is_file() and should_include(root, repo_root):
            rel = repo_rel(root, repo_root)
            if rel not in seen:
                seen.add(rel)
                results.append(context_file(repo_root, rel, max_chars_per_file))
            continue
        if not root.exists() or not root.is_dir():
            continue
        for path in sorted(root.rglob("*")):
            if len(results) >= max_files:
                return results
            if not should_include(path, repo_root):
                continue
            rel = repo_rel(path, repo_root)
            if rel in seen:
                continue
            seen.add(rel)
            results.append(context_file(repo_root, rel, max_chars_per_file))
    return results


def extract_evidence_files(evidence: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for area in evidence.get("areas", {}).values():
        for item in area.get("items", []) if isinstance(area, dict) else []:
            for file_info in item.get("evidence_files", []):
                path = file_info.get("path") if isinstance(file_info, dict) else None
                if path and path not in paths:
                    paths.append(str(path))
    return paths


def evidence_ready_for_manual_patch_count(evidence: dict[str, Any]) -> int:
    """Return an evidence-ready count without assuming a single report shape.

    Historical evidence reports have used both a root/summary integer and per-item
    readiness markers. The GPU planner should not invent recommendations, but it
    must know whether another deterministic layer already has ready candidates.
    """

    explicit_counts: list[int] = []
    ready_items = 0

    def visit(value: Any) -> None:
        nonlocal ready_items
        if isinstance(value, dict):
            for key, child in value.items():
                if key == "ready_for_manual_patch_count" and isinstance(child, int):
                    explicit_counts.append(child)
                elif key == "ready_count" and isinstance(child, int) and value.get("kind") == "agent_review_evidence_sufficiency":
                    explicit_counts.append(child)
                visit(child)
            status = value.get("status") or value.get("classification")
            if isinstance(status, str) and status in {"ready_for_manual_patch", "ready_for_patch_plan"}:
                ready_items += 1
            decision = value.get("decision")
            if isinstance(decision, str) and decision in {"ready_for_manual_patch", "ready_for_patch_plan"}:
                ready_items += 1
            elif isinstance(decision, dict):
                ready = decision.get("ready_for_manual_patch") or decision.get("ready_for_patch_plan")
                if ready is True:
                    ready_items += 1
        elif isinstance(value, list):
            for child in value:
                visit(child)

    visit(evidence)
    if explicit_counts:
        return max(explicit_counts)
    return ready_items


def compact_json(data: Any, max_chars: int) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text


def split_batches(items: list[ContextFile], batch_size: int) -> list[list[ContextFile]]:
    if batch_size <= 0:
        return [items]
    return [items[index : index + batch_size] for index in range(0, len(items), batch_size)]


def build_prompt(
    *,
    objective: str,
    evidence: dict[str, Any],
    refined: dict[str, Any],
    context_reports: list[dict[str, Any]],
    batch: list[ContextFile],
    round_index: int,
    elapsed_seconds: float,
) -> str:
    files_block = []
    for item in batch:
        files_block.append(
            {
                "path": item.path,
                "exists": item.exists,
                "lines": item.lines,
                "chars": item.chars,
                "content_preview": item.preview,
            }
        )
    instruction = {
        "role": "IA-Carmine GPU deep planning reviewer",
        "objective": objective,
        "round_index": round_index,
        "elapsed_seconds": round(elapsed_seconds, 2),
        "rules": [
            "Do not propose automatic patch application.",
            "Use only evidence from supplied files and reports.",
            "Classify each recommendation as ready_for_patch_plan, needs_more_context, or advisory_only.",
            "Prefer small manual-review docs/code patch plans over broad rewrites.",
            "Call out missing evidence explicitly.",
            "Return valid JSON only.",
        ],
        "expected_json_schema": {
            "summary": "short technical summary",
            "confidence": "low|medium|high",
            "recommendations": [
                {
                    "id": "string",
                    "area": "doc_code|doc_doc|code_code|workflow|validation|other",
                    "status": "ready_for_patch_plan|needs_more_context|advisory_only",
                    "target_files": ["path"],
                    "rationale": "string",
                    "proposed_strategy": "string",
                    "risk": "low|medium|high",
                    "validation_commands": ["command"],
                    "stop_conditions": ["condition"],
                }
            ],
            "missing_evidence": ["string"],
            "next_best_action": "string",
        },
    }
    return "\n\n".join(
        [
            "You are reviewing a complex repository using explicit local GPU/Ollama reasoning.",
            "INSTRUCTIONS JSON:\n" + compact_json(instruction, 6000),
            "EVIDENCE SUFFICIENCY REPORT:\n" + compact_json(evidence, 18000),
            "REFINED MEGALITHIC REVIEW:\n" + compact_json(refined, 18000),
            "OPTIONAL CONTEXT REPORTS:\n" + compact_json(context_reports, 14000),
            "REPOSITORY FILE BATCH:\n" + compact_json(files_block, 36000),
        ]
    )


def parse_model_json_with_diagnostics(text: str) -> tuple[dict[str, Any], dict[str, Any]]:
    stripped = text.strip()
    repair_attempt_count = 0

    if stripped.startswith("```"):
        repair_attempt_count += 1
        stripped = stripped.strip("`")
        if stripped.lower().startswith("json"):
            stripped = stripped[4:].strip()

    start = stripped.find("{")
    end = stripped.rfind("}")
    if start >= 0 and end >= start and (start > 0 or end < len(stripped) - 1):
        repair_attempt_count += 1
        stripped = stripped[start : end + 1]

    diagnostics: dict[str, Any] = {
        "json_ok": False,
        "parse_error": "",
        "repair_attempt_count": repair_attempt_count,
        "model_output_missing_required_fields": False,
    }

    try:
        parsed_any = json.loads(stripped)
    except json.JSONDecodeError as exc:
        diagnostics["parse_error"] = f"{type(exc).__name__}: {exc}"
        return (
            {
                "summary": text[:2000],
                "confidence": "low",
                "recommendations": [],
                "missing_evidence": ["model_response_not_valid_json"],
                "next_best_action": "review raw model response",
            },
            diagnostics,
        )

    diagnostics["json_ok"] = True
    if not isinstance(parsed_any, dict):
        diagnostics["model_output_missing_required_fields"] = True
        return (
            {
                "summary": str(parsed_any)[:2000],
                "confidence": "low",
                "recommendations": [],
                "missing_evidence": ["model_response_not_json_object"],
                "next_best_action": "review raw model response",
            },
            diagnostics,
        )

    parsed = parsed_any
    if "recommendations" not in parsed:
        diagnostics["model_output_missing_required_fields"] = True
        parsed["recommendations"] = []
    elif not isinstance(parsed.get("recommendations"), list):
        diagnostics["model_output_missing_required_fields"] = True
        parsed["recommendations"] = []

    parsed.setdefault("missing_evidence", [])
    parsed.setdefault("next_best_action", "")
    return parsed, diagnostics


def parse_model_json(text: str) -> dict[str, Any]:
    parsed, _diagnostics = parse_model_json_with_diagnostics(text)
    return parsed


def _raw_recommendations(parsed: dict[str, Any]) -> list[Any]:
    recommendations = parsed.get("recommendations", [])
    return recommendations if isinstance(recommendations, list) else []


def classify_empty_recommendations(
    *,
    json_ok: bool,
    parse_error: str,
    repair_attempt_count: int,
    model_output_missing_required_fields: bool,
    raw_recommendation_candidate_count: int,
    filtered_recommendation_count: int,
    evidence_ready_for_manual_patch_count_value: int,
) -> str:
    if filtered_recommendation_count > 0:
        return ""
    if not json_ok and repair_attempt_count > 0 and parse_error:
        return "repair_attempt_failed"
    if not json_ok:
        return "json_parse_failure"
    if model_output_missing_required_fields:
        return "model_output_missing_required_fields"
    if raw_recommendation_candidate_count > 0 and filtered_recommendation_count == 0:
        return "recommendations_filtered_out"
    if evidence_ready_for_manual_patch_count_value > 0:
        return "evidence_ready_but_no_gpu_plan"
    return "valid_json_empty_recommendations"


def recommendation_diagnostics_for_round(
    parsed: dict[str, Any],
    parse_diagnostics: dict[str, Any],
    evidence_ready_for_manual_patch_count_value: int,
) -> dict[str, Any]:
    raw_recommendations = _raw_recommendations(parsed)
    raw_count = len(raw_recommendations)
    filtered_count = sum(1 for rec in raw_recommendations if isinstance(rec, dict))
    reason = classify_empty_recommendations(
        json_ok=bool(parse_diagnostics.get("json_ok")),
        parse_error=str(parse_diagnostics.get("parse_error") or ""),
        repair_attempt_count=int(parse_diagnostics.get("repair_attempt_count") or 0),
        model_output_missing_required_fields=bool(parse_diagnostics.get("model_output_missing_required_fields")),
        raw_recommendation_candidate_count=raw_count,
        filtered_recommendation_count=filtered_count,
        evidence_ready_for_manual_patch_count_value=evidence_ready_for_manual_patch_count_value,
    )
    return {
        "json_ok": bool(parse_diagnostics.get("json_ok")),
        "parse_error": str(parse_diagnostics.get("parse_error") or ""),
        "repair_attempt_count": int(parse_diagnostics.get("repair_attempt_count") or 0),
        "raw_recommendation_candidate_count": raw_count,
        "filtered_recommendation_count": filtered_count,
        "recommendation_count": filtered_count,
        "empty_recommendations_reason": reason,
        "evidence_ready_for_manual_patch_count": evidence_ready_for_manual_patch_count_value,
        "recommended_next_layer": "build_agent_review_patch_plan.py"
        if reason == "evidence_ready_but_no_gpu_plan"
        else "",
    }


def aggregate_recommendation_diagnostics(rounds: list[dict[str, Any]], evidence: dict[str, Any]) -> dict[str, Any]:
    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    raw_count = sum(int(round_result.get("raw_recommendation_candidate_count") or 0) for round_result in rounds)
    filtered_count = len(merge_recommendations(rounds))
    repair_attempt_count = sum(int(round_result.get("repair_attempt_count") or 0) for round_result in rounds)
    json_parse_error_count = sum(1 for round_result in rounds if not round_result.get("json_ok", True))
    missing_required_count = sum(1 for round_result in rounds if round_result.get("empty_recommendations_reason") == "model_output_missing_required_fields")
    parse_errors = [str(round_result.get("parse_error")) for round_result in rounds if round_result.get("parse_error")]

    reason = ""
    if filtered_count == 0:
        if any(round_result.get("empty_recommendations_reason") == "repair_attempt_failed" for round_result in rounds):
            reason = "repair_attempt_failed"
        elif json_parse_error_count:
            reason = "json_parse_failure"
        elif missing_required_count:
            reason = "model_output_missing_required_fields"
        elif raw_count > 0:
            reason = "recommendations_filtered_out"
        elif evidence_ready_count > 0:
            reason = "evidence_ready_but_no_gpu_plan"
        else:
            reason = "valid_json_empty_recommendations"

    return {
        "json_parse_error_count": json_parse_error_count,
        "parse_error": parse_errors[0] if parse_errors else "",
        "repair_attempt_count": repair_attempt_count,
        "raw_recommendation_candidate_count": raw_count,
        "filtered_recommendation_count": filtered_count,
        "empty_recommendations_reason": reason,
        "evidence_ready_for_manual_patch_count": evidence_ready_count,
        "recommended_next_layer": "build_agent_review_patch_plan.py"
        if reason == "evidence_ready_but_no_gpu_plan" or filtered_count > 0
        else "collect_more_evidence",
    }


def merge_recommendations(rounds: list[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    seen: set[str] = set()
    for round_result in rounds:
        parsed = round_result.get("parsed_response") or {}
        for rec in parsed.get("recommendations", []) if isinstance(parsed, dict) else []:
            if not isinstance(rec, dict):
                continue
            key = json.dumps([rec.get("area"), rec.get("status"), rec.get("target_files"), rec.get("proposed_strategy")], sort_keys=True, ensure_ascii=False)
            if key in seen:
                continue
            seen.add(key)
            merged.append(rec)
    return merged


def build_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent GPU Deep Planning Review", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Model: `{report.get('model_used')}`")
    lines.append(f"- Elapsed seconds: `{report['elapsed_seconds']}`")
    lines.append(f"- Round count: `{report['round_count']}`")
    lines.append(f"- Recommendation count: `{report['recommendation_count']}`")
    lines.append(f"- Raw recommendation candidates: `{report.get('raw_recommendation_candidate_count')}`")
    lines.append(f"- Filtered recommendation count: `{report.get('filtered_recommendation_count')}`")
    lines.append(f"- JSON parse error count: `{report.get('json_parse_error_count')}`")
    lines.append(f"- Empty recommendations reason: `{report.get('empty_recommendations_reason')}`")
    lines.append(f"- Evidence ready for manual patch count: `{report.get('evidence_ready_for_manual_patch_count')}`")
    lines.append("")
    lines.append("## Decision")
    lines.append("")
    for key, value in report.get("decision", {}).items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Recommendations")
    lines.append("")
    for rec in report.get("recommendations", []):
        lines.append(f"### {rec.get('id', 'recommendation')} â€” {rec.get('area')}")
        lines.append(f"- Status: `{rec.get('status')}`")
        lines.append(f"- Risk: `{rec.get('risk')}`")
        lines.append(f"- Target files: `{rec.get('target_files')}`")
        lines.append(f"- Rationale: {rec.get('rationale')}")
        lines.append(f"- Strategy: {rec.get('proposed_strategy')}")
        lines.append("")
    return "\n".join(lines) + "\n"


def run_deep_review(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    evidence = read_json(resolve_path(repo_root, args.evidence))
    refined = read_json(resolve_path(repo_root, args.refined_review)) if resolve_path(repo_root, args.refined_review).exists() else {}
    evidence_ready_count = evidence_ready_for_manual_patch_count(evidence)
    context_reports = []
    for report_file in args.report_file:
        path = resolve_path(repo_root, report_file)
        if path.exists():
            try:
                data = read_json(path)
                context_reports.append({"path": repo_rel(path, repo_root), "kind": data.get("kind"), "passed": data.get("passed"), "summary": data.get("summary", {}), "decision": data.get("decision", {})})
            except Exception as exc:  # noqa: BLE001
                context_reports.append({"path": repo_rel(path, repo_root), "error": str(exc)})
        else:
            context_reports.append({"path": repo_rel(path, repo_root), "error": "missing"})

    evidence_paths = extract_evidence_files(evidence)
    context_roots = list(args.context_root or []) + evidence_paths
    if not context_roots:
        context_roots = ["docs", "Tools/ai", "Tools/validation", "Tools/workflow"]
    context_files = collect_repo_context(repo_root, context_roots, args.max_context_files, args.max_chars_per_file)
    batches = split_batches(context_files, args.files_per_round)

    start = time.perf_counter()
    deadline = start + max(1, args.budget_minutes) * 60
    rounds: list[dict[str, Any]] = []
    model_used = args.ollama_model or ""
    errors: list[str] = []

    if not args.use_ollama:
        return {
            "schema_version": 1,
            "kind": "agent_gpu_deep_planning_review",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": False,
            "errors": ["--use-ollama is required for GPU deep planning review"],
            "warnings": [],
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "apply_mode": "report_only_gpu_deep_planning",
            "elapsed_seconds": 0,
            "round_count": 0,
            "recommendation_count": 0,
            "raw_recommendation_candidate_count": 0,
            "filtered_recommendation_count": 0,
            "json_parse_error_count": 0,
            "repair_attempt_count": 0,
            "empty_recommendations_reason": "valid_json_empty_recommendations",
            "evidence_ready_for_manual_patch_count": evidence_ready_count,
            "recommended_next_layer": "collect_more_evidence",
            "recommendations": [],
            "decision": {"ready_for_patch_plan": False, "reason": "provider execution not enabled"},
            "guardrails": {"provider_execution_requires_use_ollama": True, "patch_application_performed": False},
        }

    base_url = normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL)
    with OllamaModelManager(base_url=base_url, keep_alive=args.keep_alive, shutdown_server=False, startup_timeout=args.startup_timeout) as manager:
        for index, batch in enumerate(batches, start=1):
            if index > args.max_rounds:
                break
            if time.perf_counter() >= deadline and rounds:
                break
            prompt = build_prompt(
                objective=args.objective,
                evidence=evidence,
                refined=refined,
                context_reports=context_reports,
                batch=batch,
                round_index=index,
                elapsed_seconds=time.perf_counter() - start,
            )
            round_start = time.perf_counter()
            try:
                response, model_used = manager.generate(args.ollama_model, prompt, max_new_tokens=args.max_new_tokens, temperature=args.temperature)
                parsed, parse_diagnostics = parse_model_json_with_diagnostics(response)
            except Exception as exc:  # noqa: BLE001 - report-only provider diagnostics.
                response = ""
                parsed = {"summary": "provider error", "confidence": "low", "recommendations": [], "missing_evidence": [str(exc)], "next_best_action": "inspect provider error"}
                parse_diagnostics = {
                    "json_ok": False,
                    "parse_error": f"{type(exc).__name__}: {exc}",
                    "repair_attempt_count": 0,
                    "model_output_missing_required_fields": False,
                }
                errors.append(f"round {index}: {type(exc).__name__}: {exc}")
            round_diagnostics = recommendation_diagnostics_for_round(parsed, parse_diagnostics, evidence_ready_count)
            rounds.append(
                {
                    "round": index,
                    "elapsed_seconds": round(time.perf_counter() - round_start, 3),
                    "file_count": len(batch),
                    "files": [item.path for item in batch],
                    "response_chars": len(response),
                    "raw_response_preview": response[:3000],
                    "parsed_response": parsed,
                    **round_diagnostics,
                }
            )

    recommendations = merge_recommendations(rounds)
    diagnostics = aggregate_recommendation_diagnostics(rounds, evidence)
    ready = [rec for rec in recommendations if rec.get("status") == "ready_for_patch_plan"]
    needs_context = [rec for rec in recommendations if rec.get("status") == "needs_more_context"]
    fallback_recommended = (
        diagnostics["evidence_ready_for_manual_patch_count"] > 0
        and diagnostics["filtered_recommendation_count"] == 0
    )
    decision = {
        "ready_for_patch_plan": bool(ready),
        "ready_count": len(ready),
        "needs_more_context_count": len(needs_context),
        "fallback_patch_plan_recommended": fallback_recommended,
        "recommended_next_layer": diagnostics["recommended_next_layer"],
        "manual_review_required": True,
    }
    return {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_review",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_gpu_deep_planning",
        "model_used": model_used,
        "ollama_base_url": base_url,
        "budget_minutes": args.budget_minutes,
        "elapsed_seconds": round(time.perf_counter() - start, 3),
        "context_file_count": len(context_files),
        "round_count": len(rounds),
        "rounds": rounds,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        **diagnostics,
        "decision": decision,
        "guardrails": {
            "provider_execution_requires_use_ollama": True,
            "provider_execution_performed": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "manual_review_required": True,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--objective", default="Use explicit local GPU/Ollama reasoning to derive the safest next IA-Carmine patch plan from current review evidence.")
    parser.add_argument("--evidence", default=DEFAULT_EVIDENCE)
    parser.add_argument("--refined-review", default=DEFAULT_REFINED)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--context-root", action="append", default=[])
    parser.add_argument("--max-context-files", type=int, default=160)
    parser.add_argument("--max-chars-per-file", type=int, default=8000)
    parser.add_argument("--files-per-round", type=int, default=10)
    parser.add_argument("--budget-minutes", type=int, default=30)
    parser.add_argument("--max-rounds", type=int, default=24)
    parser.add_argument("--use-ollama", action="store_true")
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--keep-alive", default="35m")
    parser.add_argument("--startup-timeout", type=float, default=30.0)
    parser.add_argument("--max-new-tokens", type=int, default=1800)
    parser.add_argument("--temperature", type=float, default=0.1)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_deep_review(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(build_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "elapsed_seconds": report["elapsed_seconds"],
                "round_count": report["round_count"],
                "recommendation_count": report["recommendation_count"],
                "raw_recommendation_candidate_count": report.get("raw_recommendation_candidate_count"),
                "filtered_recommendation_count": report.get("filtered_recommendation_count"),
                "empty_recommendations_reason": report.get("empty_recommendations_reason"),
                "evidence_ready_for_manual_patch_count": report.get("evidence_ready_for_manual_patch_count"),
                "ready_for_patch_plan": report["decision"].get("ready_for_patch_plan"),
                "recommended_next_layer": report["decision"].get("recommended_next_layer"),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())

