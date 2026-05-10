#!/usr/bin/env python3
"""Smoke-test the heap/provider/team exchange lab.

Default smoke is provider-safe: it validates deterministic exchange and provider
permit state without executing a model. Use --execute-ollama-gpu1 to run the real
GPU1/Ollama provider path on an operator-controlled workstation.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def run_lab(repo_root: Path, name: str, extra_args: list[str], timeout_seconds: int) -> tuple[subprocess.CompletedProcess[str], dict[str, Any], Path]:
    run_dir = repo_root / "output" / "validation" / f"heap_provider_team_exchange_{name}_{stamp()}"
    run_dir.mkdir(parents=True, exist_ok=True)
    output = run_dir / "report.json"
    markdown = run_dir / "report.md"
    env = os.environ.copy()
    env["PYTHONPATH"] = str(repo_root) + (os.pathsep + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    command = [
        sys.executable,
        "Tools/ai/run_heap_provider_team_exchange_lab.py",
        "--repo-root", ".",
        "--stamp", run_dir.name,
        "--max-iterations", "4",
        "--budget-minutes", "2",
        "--max-rounds", "4",
        "--timeout-seconds", str(timeout_seconds),
        "--events", (run_dir / "events.jsonl").relative_to(repo_root).as_posix(),
        "--snapshot", (run_dir / "state.json").relative_to(repo_root).as_posix(),
        "--heap-markdown", (run_dir / "state.md").relative_to(repo_root).as_posix(),
        "--bridge-dir", (run_dir / "broker_bridge").relative_to(repo_root).as_posix(),
        "--bridge-output", (run_dir / "broker_bridge.json").relative_to(repo_root).as_posix(),
        "--bridge-markdown-output", (run_dir / "broker_bridge.md").relative_to(repo_root).as_posix(),
        "--output", output.relative_to(repo_root).as_posix(),
        "--markdown-output", markdown.relative_to(repo_root).as_posix(),
        *extra_args,
    ]
    completed = subprocess.run(command, cwd=repo_root, env=env, capture_output=True, text=True, check=False, timeout=timeout_seconds + 90)
    return completed, read_json(output), run_dir


def validate_common(label: str, report: dict[str, Any], errors: list[str]) -> None:
    if report.get("passed") is not True:
        errors.append(f"{label}: lab did not pass")
    metrics = report.get("metrics") if isinstance(report.get("metrics"), dict) else {}
    for key in ("heap_read_count", "heap_write_count", "tool_request_count", "tool_execution_count", "decision_count", "candidate_operation_count"):
        if int(metrics.get(key) or 0) <= 0:
            errors.append(f"{label}: metric {key} must be >0")
    if metrics.get("product_status") not in {"ready", "blocked_with_reason"}:
        errors.append(f"{label}: product_status must be ready or blocked_with_reason")
    role_counts = metrics.get("role_event_counts") if isinstance(metrics.get("role_event_counts"), dict) else {}
    for lane in ("gpu1", "gpu0", "npu", "broker", "orchestrator"):
        lane_state = role_counts.get(lane) if isinstance(role_counts.get(lane), dict) else {}
        if int(lane_state.get("event_count") or 0) <= 0:
            errors.append(f"{label}: lane {lane} must write at least one heap event")
    for key in ("patch_application_performed", "source_writes_performed", "persistent_memory_write_performed"):
        if report.get(key) is not False:
            errors.append(f"{label}: {key} must be false")


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Provider Team Exchange Lab Smoke", "", f"- Passed: `{report.get('passed')}`"]
    lines.extend(["", "## Runs", ""])
    for run in report.get("runs", []):
        if not isinstance(run, dict):
            continue
        metrics = run.get("metrics") if isinstance(run.get("metrics"), dict) else {}
        lines.append(f"- `{run.get('label')}`: passed=`{run.get('passed')}` product=`{metrics.get('product_status')}` provider_performed=`{metrics.get('provider_execution_performed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_provider_team_exchange_lab_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/heap_provider_team_exchange_lab_smoke.md")
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--execute-ollama-gpu1", action="store_true")
    parser.add_argument("--ollama-url", default="http://localhost:11434")
    parser.add_argument("--ollama-model", default="gpt-oss:20b")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    runs: list[dict[str, Any]] = []

    default_completed, default_report, default_dir = run_lab(repo_root, "default", [], args.timeout_seconds)
    if default_completed.returncode != 0:
        errors.append(f"default: returncode={default_completed.returncode}; tail={(default_completed.stderr or default_completed.stdout)[-1500:]}")
    validate_common("default", default_report, errors)
    if default_report.get("metrics", {}).get("provider_execution_performed") is not False:
        errors.append("default: provider_execution_performed must be false")
    runs.append({"label": "default", "returncode": default_completed.returncode, "run_dir": default_dir.relative_to(repo_root).as_posix(), "passed": default_report.get("passed"), "metrics": default_report.get("metrics", {})})

    permit_completed, permit_report, permit_dir = run_lab(repo_root, "permit_dry", ["--allow-provider-generation", "--operator-intent"], args.timeout_seconds)
    if permit_completed.returncode != 0:
        errors.append(f"permit_dry: returncode={permit_completed.returncode}; tail={(permit_completed.stderr or permit_completed.stdout)[-1500:]}")
    validate_common("permit_dry", permit_report, errors)
    permit_metrics = permit_report.get("metrics", {}) if isinstance(permit_report.get("metrics"), dict) else {}
    if permit_metrics.get("budget_decision") != "allow_provider_generation":
        errors.append("permit_dry: budget_decision must allow provider generation")
    if permit_metrics.get("provider_execution_performed") is not False:
        errors.append("permit_dry: provider must not execute without --execute-ollama-gpu1")
    runs.append({"label": "permit_dry", "returncode": permit_completed.returncode, "run_dir": permit_dir.relative_to(repo_root).as_posix(), "passed": permit_report.get("passed"), "metrics": permit_metrics})

    if args.execute_ollama_gpu1:
        provider_args = [
            "--allow-provider-generation",
            "--operator-intent",
            "--execute-ollama-gpu1",
            "--require-provider-output",
            "--ollama-url",
            args.ollama_url,
            "--ollama-model",
            args.ollama_model,
        ]
        provider_completed, provider_report, provider_dir = run_lab(repo_root, "ollama_gpu1", provider_args, args.timeout_seconds)
        if provider_completed.returncode != 0:
            errors.append(f"ollama_gpu1: returncode={provider_completed.returncode}; tail={(provider_completed.stderr or provider_completed.stdout)[-2000:]}")
        validate_common("ollama_gpu1", provider_report, errors)
        provider_metrics = provider_report.get("metrics", {}) if isinstance(provider_report.get("metrics"), dict) else {}
        if provider_metrics.get("provider_execution_performed") is not True:
            errors.append("ollama_gpu1: provider_execution_performed must be true")
        if int(provider_metrics.get("provider_output_count") or 0) <= 0:
            errors.append("ollama_gpu1: provider_output_count must be >0")
        runs.append({"label": "ollama_gpu1", "returncode": provider_completed.returncode, "run_dir": provider_dir.relative_to(repo_root).as_posix(), "passed": provider_report.get("passed"), "metrics": provider_metrics})

    report = {
        "schema_version": 1,
        "kind": "heap_provider_team_exchange_lab_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "runs": runs,
        "provider_execution_performed": bool(args.execute_ollama_gpu1 and not errors),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "persistent_memory_write_performed": False,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
