#!/usr/bin/env python3
"""Smoke for explicit CLI-only Universo IA operator config resolution."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any


def run(repo_root: Path, command: list[str]) -> dict[str, Any]:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (
        os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else ""
    )
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=env,
        text=True,
        capture_output=True,
        timeout=120,
        check=False,
    )
    payload: dict[str, Any] = {}
    if completed.stdout.strip().startswith("{"):
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError:
            payload = {}
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "payload": payload,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Universo Config Resolver Smoke", "", f"- Passed: `{report.get('passed')}`", ""]
    for check in report.get("checks") or []:
        lines.append(f"- `{check.get('name')}`: `{check.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/universe_config_resolver_smoke.json")
    parser.add_argument(
        "--markdown-output",
        default="output/validation/universe_config_resolver_smoke.md",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    base = [sys.executable, "-m", "ia_carmine.cli", "run", "--repo-root", "."]
    missing = run(repo_root, [*base, "--dry-run"])
    explicit_args = [
        "--dry-run",
        "--budget-minutes",
        "5",
        "--max-iterations",
        "5",
        "--min-runtime-rounds",
        "1",
        "--min-proposal-iterations",
        "0",
        "--max-rounds",
        "8",
        "--files-per-round",
        "4",
        "--max-provider-revisions",
        "5",
        "--timeout-seconds",
        "600",
        "--preflight-timeout-seconds",
        "90",
        "--revision-context",
        "auto_latest",
        "--revision-context-max-tasks",
        "6",
        "--provider-model",
        "qwen2.5-coder:14b",
        "--gpu1-base-url",
        "http://127.0.0.1:11434",
        "--gpu0-model",
        "qwen3:1.7b",
        "--gpu0-base-url",
        "http://127.0.0.1:11435",
        "--gpu0-vulkan-visible-devices",
        "1",
        "--ollama-num-ctx",
        "16384",
        "--ollama-gpu-layers",
        "all",
        "--ollama-context-candidates",
        "8192,4096",
        "--npu-model-dir",
        "C:/explicit/npu-model",
        "--max-new-tokens",
        "900",
        "--gpu0-max-new-tokens",
        "96",
        "--keep-alive",
        "120s",
        "--gpu0-iterations",
        "16",
        "--gpu0-min-seconds",
        "0.1",
        "--npu-micro-timeout-seconds",
        "60",
        "--npu-max-context-chars",
        "8000",
        "--npu-max-prompt-chars",
        "1200",
        "--npu-max-new-tokens",
        "384",
        "--npu-device-workload-seconds",
        "3.0",
        "--npu-device-workload-iterations",
        "2500",
        "--startup-max-memory-chars",
        "32000",
        "--startup-max-context-files",
        "48",
        "--startup-scan-context-files",
        "48",
        "--startup-max-chars-per-file",
        "8000",
        "--startup-provider-input-workers",
        "6",
        "--startup-required-context-profile",
        "project_self_improvement",
        "--startup-operational-memory-query",
        "operator_product_launcher run-unica heap context closure provider lanes",
        "--startup-operational-memory-limit",
        "8",
        "--rag-db",
        "output/ai_runtime_memory/rag/rag.sqlite",
        "--rag-index-policy",
        "auto",
        "--rag-embedding-endpoint",
        "http://127.0.0.1:11434",
        "--rag-embedding-model",
        "bge-m3",
        "--rag-ingest-batch-size",
        "8",
        "--rag-embed-smoke-batch-size",
        "8",
        "--rag-chunk-min-chars",
        "1500",
        "--rag-chunk-max-chars",
        "4000",
        "--rag-chunk-overlap-chars",
        "300",
        "--rag-max-file-size",
        "250000",
        "--rag-top-k",
        "20",
        "--rag-char-budget",
        "32000",
        "--context-document-count",
        "24",
        "--context-document-preview-chars",
        "1200",
        "--semantic-code-chunk-limit",
        "32",
        "--semantic-code-chunk-preview-chars",
        "1400",
        "--semantic-evidence-chunk-limit",
        "24",
        "--memory-search-limit",
        "12",
        "--tool-catalog-limit",
        "80",
        "--tool-inventory-roots",
        "Tools,ia_carmine",
        "--semantic-path-boosts",
        "ia_carmine/runtime/heap_gate,ia_carmine/runtime/run,ia_carmine/context,Tools/validation",
        "--ai-context-pack-profile",
        "core_ai_backend",
        "--code-interpreter-inputs",
        "ia_carmine,Tools,docs",
        "--duplication-audit-roots",
        "ia_carmine,Tools",
        "--provider-prompt-tool-catalog-cap",
        "80",
        "--allow-provider-generation",
        "--require-ollama-gpu-residency",
        "--allow-npu-device-workload",
    ]
    resolved = run(
        repo_root,
        [*base, *explicit_args],
    )
    rejected_config_result = run(repo_root, [*base, "--dry-run", "--operator-config", "x.json"])
    payload = resolved.get("payload") if isinstance(resolved.get("payload"), dict) else {}
    sources = payload.get("field_sources") if isinstance(payload.get("field_sources"), dict) else {}
    effective = (
        payload.get("effective_universe_config")
        if isinstance(payload.get("effective_universe_config"), dict)
        else {}
    )
    checks = [
        {
            "name": "missing_explicit_parameters_fail",
            "passed": missing["returncode"] != 0
            and "missing explicit Universo IA run parameter" in missing["stderr_tail"] + missing["stdout_tail"],
        },
        {
            "name": "explicit_cli_only_dry_run_passes",
            "passed": resolved["returncode"] == 0 and bool(payload.get("expanded_heap_command")),
        },
        {
            "name": "no_operator_config_source_surface",
            "passed": "operator_config_path" not in payload
            and "operator_config_sha256" not in payload,
        },
        {
            "name": "cli_source_recorded",
            "passed": sources.get("provider_model") == "cli_arg"
            and sources.get("files_per_round") == "cli_arg"
            and effective.get("provider_model") == "qwen2.5-coder:14b"
            and effective.get("files_per_round") == 4,
        },
        {
            "name": "files_per_round_propagated_to_expanded_command",
            "passed": "--files-per-round" in (payload.get("expanded_heap_command") or [])
            and "4" in (payload.get("expanded_heap_command") or []),
        },
        {
            "name": "operator_config_flag_rejected",
            "passed": rejected_config_result["returncode"] != 0
            and "operator-config" in rejected_config_result["stderr_tail"] + rejected_config_result["stdout_tail"],
        },
    ]
    errors = [check["name"] for check in checks if not check.get("passed")]
    report = {
        "schema_version": 1,
        "kind": "universe_config_resolver_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "checks": checks,
        "errors": errors,
        "missing_result": missing,
        "resolved_result": resolved,
        "rejected_config_result": rejected_config_result,
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown = Path(args.markdown_output)
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
