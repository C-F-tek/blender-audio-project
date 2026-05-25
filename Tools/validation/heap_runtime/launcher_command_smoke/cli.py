#!/usr/bin/env python3
"""Smoke-test external heap launcher command generation.

This smoke does not run providers and does not execute the heap runtime. It only
checks that explicit CLI-only command generation exposes the expected external heap
operator commands and injects an explicitly supplied revision context into the
reviewable launcher request.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def env_for(repo_root: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    env["IA_CARMINE_PYTHON"] = sys.executable
    return env


def explicit_run_args(revision_context: Path) -> list[str]:
    return [
        "--dry-run",
        "--run-label", "heap_runtime_launcher_command_smoke",
        "--intermediate-root", "output/validation/heap_runtime_launcher_command_smoke/intermediate",
        "--final-root", "output/validation/heap_runtime_launcher_command_smoke/final_product",
        "--objective", "heap runtime launcher command smoke",
        "--budget-minutes", "5",
        "--max-iterations", "5",
        "--min-runtime-rounds", "1",
        "--min-proposal-iterations", "0",
        "--max-rounds", "8",
        "--files-per-round", "4",
        "--max-provider-revisions", "5",
        "--timeout-seconds", "600",
        "--preflight-timeout-seconds", "90",
        "--revision-context", str(revision_context),
        "--revision-context-max-tasks", "6",
        "--provider-model", "explicit_gpu1_model_for_smoke",
        "--gpu1-base-url", "http://gpu1-ollama.invalid",
        "--gpu0-model", "explicit_gpu0_model_for_smoke",
        "--gpu0-base-url", "http://gpu0-ollama.invalid",
        "--gpu0-vulkan-visible-devices", "1",
        "--ollama-num-ctx", "16384",
        "--gpu0-ollama-num-ctx", "2048",
        "--ollama-gpu-layers", "all",
        "--ollama-context-candidates", "16384,8192",
        "--npu-model-dir", "explicit/npu-model",
        "--max-new-tokens", "900",
        "--gpu0-max-new-tokens", "96",
        "--keep-alive", "120s",
        "--gpu0-iterations", "16",
        "--gpu0-min-seconds", "0.1",
        "--npu-micro-start-mode", "deferred",
        "--npu-micro-timeout-seconds", "60",
        "--npu-final-wait-seconds", "60",
        "--npu-max-context-chars", "8000",
        "--npu-max-prompt-chars", "1200",
        "--npu-max-new-tokens", "384",
        "--npu-device-workload-seconds", "3.0",
        "--npu-device-workload-iterations", "2500",
        "--startup-max-memory-chars", "32000",
        "--startup-max-context-files", "48",
        "--startup-scan-context-files", "48",
        "--startup-max-chars-per-file", "8000",
        "--startup-provider-input-workers", "6",
        "--startup-required-context-profile", "project_self_improvement",
        "--startup-operational-memory-query", "operator_product_launcher run-unica heap context closure provider lanes",
        "--startup-operational-memory-limit", "8",
        "--rag-db", "output/ai_runtime_memory/rag/rag.sqlite",
        "--rag-profile", "runtime_code_context",
        "--rag-index-policy", "auto",
        "--rag-embedding-endpoint", "http://rag-embedding.invalid",
        "--rag-embedding-model", "bge-m3",
        "--rag-ingest-batch-size", "8",
        "--rag-embed-smoke-batch-size", "8",
        "--rag-chunk-min-chars", "1500",
        "--rag-chunk-max-chars", "4000",
        "--rag-chunk-overlap-chars", "300",
        "--rag-max-file-size", "250000",
        "--rag-top-k", "20",
        "--rag-char-budget", "32000",
        "--context-document-count", "24",
        "--context-document-preview-chars", "1200",
        "--semantic-code-chunk-limit", "32",
        "--semantic-code-chunk-preview-chars", "1400",
        "--semantic-evidence-chunk-limit", "24",
        "--memory-search-limit", "12",
        "--tool-catalog-limit", "80",
        "--tool-inventory-roots", "Tools,ia_carmine",
        "--semantic-path-boosts", "ia_carmine/runtime/heap_gate,ia_carmine/runtime/run,ia_carmine/context,Tools/validation",
        "--ai-context-pack-profile", "core_ai_backend",
        "--code-interpreter-inputs", "ia_carmine,Tools,docs",
        "--duplication-audit-roots", "ia_carmine,Tools",
        "--provider-prompt-tool-catalog-cap", "80",
        "--max-degraded-lanes", "0",
        "--allow-provider-generation",
        "--require-ollama-gpu-residency",
        "--allow-npu-device-workload",
    ]


def run(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env_for(repo_root),
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def load_heap_closure_module(repo_root: Path) -> Any:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from ia_carmine.runtime.heap_context_closure import requesting

    return requesting


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Runtime Launcher Command Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Revision context fixture path: `{report.get('revision_context_fixture_path')}`",
        f"- Output artifact writes performed: `{report.get('output_artifact_writes_performed')}`",
        "",
        "## Checks",
        "",
    ]
    for check in report.get("checks") or []:
        lines.append(f"- `{check.get('name')}`: `{check.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def write_revision_context_fixture(repo_root: Path) -> Path:
    run_dir = repo_root / "output" / "validation" / "heap_context_closure_smoke_revision_context"
    run_dir.mkdir(parents=True, exist_ok=True)
    fixture = run_dir / "external_heap_revision_context.json"
    fixture.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "kind": "external_heap_revision_context",
                "protocol": "external_heap_revision_context_v1",
                "product_acceptance_status": "blocked",
                "product_acceptance_passed": False,
                "requires_concrete_rewrite": True,
                "priority_next_action": "rewrite_non_concrete_candidates",
                "candidate_applicability_summary": {
                    "rewrite_task_count": 1,
                    "non_concrete_candidate_task_count": 1,
                    "concrete_candidate_task_count": 0,
                    "symbol_propagation_skipped_task_count": 1,
                    "flag_counts": {"generic_patch_sketch": 1},
                    "non_concrete_task_ids": ["gpu1_rewrite_rejected_proposal_smoke"],
                    "symbol_propagation_skipped_task_ids": ["gpu1_rewrite_rejected_proposal_smoke"],
                    "requires_concrete_rewrite": True,
                    "priority_next_action": "rewrite_non_concrete_candidates",
                },
                "resume_from_block_id": "proposal_smoke_previous",
                "latest_block_id": "proposal_smoke_latest",
                "tasks": [
                    {
                        "task_id": "gpu1_rewrite_rejected_proposal_smoke",
                        "role": "gpu1_planner",
                        "task_type": "rewrite_rejected_block",
                        "target_block_id": "proposal_smoke_latest",
                        "resume_from_block_id": "proposal_smoke_previous",
                        "candidate_applicability_flags": ["generic_patch_sketch"],
                        "candidate_concrete_enough": False,
                        "symbol_propagation_skipped": True,
                        "symbol_propagation_skip_reason": "candidate_not_concrete_enough",
                        "instruction": "Smoke fixture task.",
                    }
                ],
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return fixture


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/heap_runtime_launcher_command_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/heap_runtime_launcher_command_smoke.md"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    fixture_path = write_revision_context_fixture(repo_root)
    output_json = repo_root / "output" / "validation" / "heap_launcher_command_smoke.json"
    command = [
        sys.executable,
        "-m",
        "ia_carmine.cli",
        "run",
        "--repo-root",
        ".",
        "--request-file",
        "docs/README.md",
        *explicit_run_args(fixture_path),
        "--effective-config-output",
        str(output_json),
    ]
    result = run(command, repo_root)
    payload = read_json(output_json)
    generated_command = " ".join(str(item) for item in (payload.get("expanded_heap_command") or []))
    field_sources = payload.get("field_sources") if isinstance(payload.get("field_sources"), dict) else {}
    effective = (
        payload.get("effective_universe_config")
        if isinstance(payload.get("effective_universe_config"), dict)
        else {}
    )
    revision_fixture_payload = read_json(fixture_path)
    closure_module = load_heap_closure_module(repo_root)
    native_revision_prompt = closure_module.revision_context_prompt(
        revision_fixture_payload, fixture_path, 12
    )
    checks = [
        {"name": "command_builder_returncode_zero", "passed": result.get("passed") is True},
        {"name": "canonical_run_plan_schema", "passed": payload.get("kind") == "operator_universe_run_plan"},
        {
            "name": "explicit_cli_config_used",
            "passed": field_sources.get("provider_model") == "cli_arg"
            and effective.get("max_rounds") == 8,
        },
        {
            "name": "retired_launcher_command_not_used",
            "passed": "heap_runtime_launcher_command.py" not in " ".join(command)
            and "run_heap_runtime_launcher_command" not in " ".join(command),
        },
        {
            "name": "revision_context_selection_explicit",
            "passed": field_sources.get("revision_context") == "cli_arg"
            and effective.get("revision_context") == str(fixture_path),
        },
        {
            "name": "revision_context_forwarded_to_heap_closure",
            "passed": "--revision-context" in generated_command and str(fixture_path) in generated_command,
        },
        {
            "name": "rewrite_priority_exposed_in_report",
            "passed": revision_fixture_payload.get("requires_concrete_rewrite") is True
            and revision_fixture_payload.get("priority_next_action") == "rewrite_non_concrete_candidates",
        },
        {
            "name": "rewrite_priority_injected_by_closure_runtime",
            "passed": "requires_concrete_rewrite: True" in native_revision_prompt
            and "rewrite_non_concrete_candidates" in native_revision_prompt,
        },
        {
            "name": "symbol_propagation_skip_injected_by_closure_runtime",
            "passed": "symbol_propagation_skipped=True" in native_revision_prompt
            and "candidate_not_concrete_enough" in native_revision_prompt,
        },
        {
            "name": "native_closure_revision_prompt_exposes_rewrite_priority",
            "passed": "requires_concrete_rewrite: True" in native_revision_prompt
            and "rewrite_non_concrete_candidates" in native_revision_prompt,
        },
        {
            "name": "native_closure_revision_prompt_preserves_symbol_skip",
            "passed": "symbol_propagation_skipped=True" in native_revision_prompt
            and "candidate_not_concrete_enough" in native_revision_prompt,
        },
        {
            "name": "main_command_targets_heap_closure",
            "passed": "-m ia_carmine.runtime.heap_context_closure.cli" in generated_command,
        },
        {
            "name": "provider_flags_are_unified",
            "passed": "--allow-provider-generation" in generated_command
            and "--operator-intent" in generated_command,
        },
        {
            "name": "canonical_run_metadata_forwarded",
            "passed": "--canonical-run-metadata" in generated_command
            and "--canonical-run-fingerprint" in generated_command,
        },
    ]
    errors = [check["name"] for check in checks if not check.get("passed")]
    report = {
        "schema_version": 2,
        "kind": "heap_runtime_launcher_command_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "output_artifact_writes_performed": True,
        "revision_context_fixture_used": True,
        "revision_context_fixture_path": str(fixture_path),
        "generated_command_json": str(output_json),
        "native_revision_prompt_preview": native_revision_prompt[-4000:],
        "checks": checks,
        "command_result": result,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(repo_root, args.output)), end="")
    write_text_report(render_markdown(report), resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
