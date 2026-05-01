#!/usr/bin/env python3
"""Run GPU/Ollama deep planning with non-blocking intermediate NPU audits.

This supervised runner is the long-running IA-Carmine planning mode:

- GPU/Ollama performs multi-round reasoning over repository evidence;
- each round writes an intermediate checkpoint JSON/Markdown artifact;
- optional NPU auditor inspects checkpoints as a non-blocking guardrail;
- NPU failures, unusable text or missing OpenVINO are warnings only;
- repeated deterministic NPU dependency failures are circuit-broken;
- no patch is applied and no GitHub PR is created.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.run_agent_gpu_deep_planning_review import (
        DEFAULT_EVIDENCE,
        DEFAULT_REFINED,
        aggregate_recommendation_diagnostics,
        build_markdown,
        build_prompt,
        collect_repo_context,
        evidence_ready_for_manual_patch_count,
        extract_evidence_files,
        merge_recommendations,
        parse_model_json_with_diagnostics,
        read_json,
        recommendation_diagnostics_for_round,
        resolve_path,
        repo_rel,
        split_batches,
    )
    from Tools.npu.ollama_runtime import DEFAULT_BASE_URL, OllamaModelManager, normalize_base_url
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.run_agent_gpu_deep_planning_review import (  # type: ignore
        DEFAULT_EVIDENCE,
        DEFAULT_REFINED,
        aggregate_recommendation_diagnostics,
        build_markdown,
        build_prompt,
        collect_repo_context,
        evidence_ready_for_manual_patch_count,
        extract_evidence_files,
        merge_recommendations,
        parse_model_json_with_diagnostics,
        read_json,
        recommendation_diagnostics_for_round,
        resolve_path,
        repo_rel,
        split_batches,
    )
    from Tools.npu.ollama_runtime import DEFAULT_BASE_URL, OllamaModelManager, normalize_base_url  # type: ignore

DEFAULT_OUTPUT = "output/ai_pipeline/agent_gpu_deep_planning_supervised.json"
DEFAULT_MARKDOWN = "output/ai_pipeline/agent_gpu_deep_planning_supervised.md"
DEFAULT_CHECKPOINT_DIR = "output/ai_pipeline/gpu_deep_planning_checkpoints"
TERMINAL_NPU_AUDIT_CLASSIFICATIONS = {"dependency_missing_openvino_genai"}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def run_command(command: list[str], repo_root: Path, timeout_seconds: int) -> tuple[int, str, str, str | None]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:], None
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "", f"TimeoutExpired: {timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001 - non-blocking auditor runner.
        return 1, "", "", f"{type(exc).__name__}: {exc}"


def build_report(
    *,
    repo_root: Path,
    args: argparse.Namespace,
    evidence: dict[str, Any],
    refined: dict[str, Any],
    context_reports: list[dict[str, Any]],
    context_file_count: int,
    rounds: list[dict[str, Any]],
    npu_audits: list[dict[str, Any]],
    model_used: str,
    errors: list[str],
    warnings: list[str],
    started_at: float,
    npu_auditor_disabled_reason: str = "",
) -> dict[str, Any]:
    recommendations = merge_recommendations(rounds)
    diagnostics = aggregate_recommendation_diagnostics(rounds, evidence)
    ready = [rec for rec in recommendations if rec.get("status") == "ready_for_patch_plan"]
    needs_context = [rec for rec in recommendations if rec.get("status") == "needs_more_context"]
    unusable_npu = [audit for audit in npu_audits if audit.get("classification") not in {"usable_audit_text", "not_executed", "metadata_only"}]
    npu_success_count = sum(1 for audit in npu_audits if audit.get("provider_execution_succeeded") is True or audit.get("classification") == "usable_audit_text")
    npu_requested_count = sum(1 for audit in npu_audits if audit.get("provider_execution_requested") is True)
    fallback_recommended = (
        diagnostics["evidence_ready_for_manual_patch_count"] > 0
        and diagnostics["filtered_recommendation_count"] == 0
    )
    return {
        "schema_version": 1,
        "kind": "agent_gpu_deep_planning_supervised",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
        "model_used": model_used,
        "ollama_base_url": normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL),
        "budget_minutes": args.budget_minutes,
        "elapsed_seconds": round(time.perf_counter() - started_at, 3),
        "context_file_count": context_file_count,
        "round_count": len(rounds),
        "rounds": rounds,
        "npu_audit_count": len(npu_audits),
        "npu_audit_requested_count": npu_requested_count,
        "npu_audit_success_count": npu_success_count,
        "npu_auditor_disabled_reason": npu_auditor_disabled_reason,
        "npu_audits": npu_audits,
        "recommendation_count": len(recommendations),
        "recommendations": recommendations,
        **diagnostics,
        "decision": {
            "ready_for_patch_plan": bool(ready),
            "ready_count": len(ready),
            "needs_more_context_count": len(needs_context),
            "fallback_patch_plan_recommended": fallback_recommended,
            "npu_auditor_non_blocking": True,
            "npu_unusable_or_failed_count": len(unusable_npu),
            "npu_audit_success_count": npu_success_count,
            "npu_auditor_disabled_reason": npu_auditor_disabled_reason,
            "recommended_next_layer": diagnostics["recommended_next_layer"],
            "manual_review_required": True,
        },
        "inputs": {
            "evidence_kind": evidence.get("kind"),
            "refined_kind": refined.get("kind"),
            "context_report_count": len(context_reports),
        },
        "guardrails": {
            "provider_execution_requires_use_ollama": True,
            "npu_auditor_requires_include_npu_auditor": True,
            "npu_auditor_non_blocking": True,
            "npu_primary_advisory": False,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
            "manual_review_required": True,
        },
    }


def checkpoint_paths(checkpoint_dir: Path, round_index: int) -> tuple[Path, Path, Path]:
    base = checkpoint_dir / f"round_{round_index:03d}"
    return base.with_suffix(".json"), base.with_suffix(".md"), base.with_name(base.name + "_npu_audit.json")


def run_npu_audit_for_checkpoint(repo_root: Path, checkpoint_json: Path, audit_json: Path, args: argparse.Namespace) -> dict[str, Any]:
    command = [
        sys.executable,
        "Tools/ai/run_npu_gpu_deep_review_auditor.py",
        "--repo-root",
        ".",
        "--gpu-review",
        str(checkpoint_json),
        "--output",
        str(audit_json),
        "--markdown-output",
        str(audit_json.with_suffix(".md")),
        "--context-output",
        str(audit_json.with_name(audit_json.stem + "_context.md")),
        "--npu-output",
        str(audit_json.with_name(audit_json.stem + "_npu.md")),
        "--npu-notes-output",
        str(audit_json.with_name(audit_json.stem + "_npu_notes.md")),
        "--npu-metadata-output",
        str(audit_json.with_name(audit_json.stem + "_metadata.json")),
        "--timeout-seconds",
        str(args.npu_auditor_timeout_seconds),
    ]
    if args.run_npu_auditor_provider:
        command.append("--run-npu")
    else:
        command.extend(["--run-npu", "--metadata-only"])
    returncode, stdout, stderr, error = run_command(command, repo_root, args.npu_auditor_timeout_seconds + 30)
    audit: dict[str, Any] = {
        "checkpoint": repo_rel(checkpoint_json, repo_root),
        "audit_output": repo_rel(audit_json, repo_root),
        "returncode": returncode,
        "stdout_tail": stdout,
        "stderr_tail": stderr,
        "error": error or "",
        "blocking": False,
        "classification": "missing_audit_output",
        "provider_execution_requested": bool(args.run_npu_auditor_provider),
        "provider_load_attempted": False,
        "provider_execution_succeeded": False,
        "provider_execution_performed": False,
        "dependency_missing": False,
    }
    if audit_json.exists():
        try:
            data = read_json(audit_json)
            nested = data.get("npu_auditor", {})
            audit.update(
                {
                    "kind": data.get("kind"),
                    "passed": data.get("passed"),
                    "provider_execution_requested": data.get("provider_execution_requested", nested.get("provider_execution_requested")),
                    "provider_load_attempted": data.get("provider_load_attempted", nested.get("provider_load_attempted")),
                    "provider_execution_succeeded": data.get("provider_execution_succeeded", nested.get("provider_execution_succeeded")),
                    "provider_execution_performed": data.get("provider_execution_performed", nested.get("provider_execution_performed")),
                    "dependency_missing": data.get("dependency_missing", nested.get("dependency_missing")),
                    "classification": nested.get("classification") or data.get("classification"),
                    "gpu_review_blocked": data.get("decision", {}).get("gpu_review_blocked"),
                    "warnings": data.get("warnings", []),
                }
            )
        except Exception as exc:  # noqa: BLE001
            audit["error"] = f"{audit['error']} {type(exc).__name__}: {exc}".strip()
    return audit


def run_supervised(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    started_at = time.perf_counter()
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

    if not args.use_ollama:
        return {
            "schema_version": 1,
            "kind": "agent_gpu_deep_planning_supervised",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": False,
            "errors": ["--use-ollama is required"],
            "warnings": [],
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "apply_mode": "report_only_gpu_deep_planning_with_non_blocking_npu_audit",
            "elapsed_seconds": 0,
            "round_count": 0,
            "npu_audit_count": 0,
            "recommendation_count": 0,
            "raw_recommendation_candidate_count": 0,
            "filtered_recommendation_count": 0,
            "json_parse_error_count": 0,
            "repair_attempt_count": 0,
            "empty_recommendations_reason": "valid_json_empty_recommendations",
            "evidence_ready_for_manual_patch_count": evidence_ready_count,
            "recommended_next_layer": "collect_more_evidence",
            "decision": {"ready_for_patch_plan": False, "manual_review_required": True},
            "guardrails": {"provider_execution_requires_use_ollama": True, "patch_application_performed": False},
        }

    evidence_paths = extract_evidence_files(evidence)
    context_roots = list(args.context_root or []) + evidence_paths
    if not context_roots:
        context_roots = ["docs", "Tools/ai", "Tools/validation", "Tools/workflow"]
    context_files = collect_repo_context(repo_root, context_roots, args.max_context_files, args.max_chars_per_file)
    batches = split_batches(context_files, args.files_per_round)
    checkpoint_dir = resolve_path(repo_root, args.checkpoint_dir)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)

    deadline = started_at + max(1, args.budget_minutes) * 60
    rounds: list[dict[str, Any]] = []
    npu_audits: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    model_used = args.ollama_model or ""
    base_url = normalize_base_url(args.ollama_base_url or DEFAULT_BASE_URL)
    npu_auditor_disabled_reason = ""

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
                elapsed_seconds=time.perf_counter() - started_at,
            )
            round_start = time.perf_counter()
            try:
                response, model_used = manager.generate(args.ollama_model, prompt, max_new_tokens=args.max_new_tokens, temperature=args.temperature)
                parsed, parse_diagnostics = parse_model_json_with_diagnostics(response)
            except Exception as exc:  # noqa: BLE001
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
            round_data = {
                "round": index,
                "elapsed_seconds": round(time.perf_counter() - round_start, 3),
                "file_count": len(batch),
                "files": [item.path for item in batch],
                "response_chars": len(response),
                "raw_response_preview": response[:3000],
                "parsed_response": parsed,
                **round_diagnostics,
            }
            rounds.append(round_data)
            interim_report = build_report(
                repo_root=repo_root,
                args=args,
                evidence=evidence,
                refined=refined,
                context_reports=context_reports,
                context_file_count=len(context_files),
                rounds=rounds,
                npu_audits=npu_audits,
                model_used=model_used,
                errors=errors,
                warnings=warnings,
                started_at=started_at,
                npu_auditor_disabled_reason=npu_auditor_disabled_reason,
            )
            checkpoint_json, checkpoint_md, audit_json = checkpoint_paths(checkpoint_dir, index)
            write_json(checkpoint_json, interim_report)
            checkpoint_md.write_text(build_markdown(interim_report), encoding="utf-8")
            should_audit = (
                args.include_npu_auditor
                and not npu_auditor_disabled_reason
                and index % max(1, args.npu_auditor_every_rounds) == 0
            )
            if should_audit:
                audit = run_npu_audit_for_checkpoint(repo_root, checkpoint_json, audit_json, args)
                npu_audits.append(audit)
                if audit.get("error"):
                    warnings.append(f"NPU audit round {index}: {audit.get('error')}")
                classification = str(audit.get("classification") or "")
                if classification not in {"usable_audit_text", "metadata_only", "not_executed"}:
                    warnings.append(f"NPU audit round {index}: classification={classification}")
                if classification in TERMINAL_NPU_AUDIT_CLASSIFICATIONS:
                    npu_auditor_disabled_reason = classification
                    warnings.append(f"NPU auditor circuit breaker enabled after round {index}: {classification}")

    return build_report(
        repo_root=repo_root,
        args=args,
        evidence=evidence,
        refined=refined,
        context_reports=context_reports,
        context_file_count=len(context_files),
        rounds=rounds,
        npu_audits=npu_audits,
        model_used=model_used,
        errors=errors,
        warnings=warnings,
        started_at=started_at,
        npu_auditor_disabled_reason=npu_auditor_disabled_reason,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--objective", default="Use explicit local GPU/Ollama reasoning to derive the safest next IA-Carmine patch plan while a non-blocking NPU auditor checks intermediate artifacts.")
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
    parser.add_argument("--include-npu-auditor", action="store_true")
    parser.add_argument("--run-npu-auditor-provider", action="store_true", help="Actually execute OpenVINO/NPU auditor. Without this, auditor uses metadata-only mode.")
    parser.add_argument("--npu-auditor-every-rounds", type=int, default=1)
    parser.add_argument("--npu-auditor-timeout-seconds", type=int, default=900)
    parser.add_argument("--checkpoint-dir", default=DEFAULT_CHECKPOINT_DIR)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_supervised(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
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
                "npu_audit_count": report["npu_audit_count"],
                "npu_audit_success_count": report["npu_audit_success_count"],
                "npu_auditor_disabled_reason": report["npu_auditor_disabled_reason"],
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
