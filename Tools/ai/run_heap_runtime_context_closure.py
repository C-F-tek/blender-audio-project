#!/usr/bin/env python3
"""Launch heap runtime with explicit context/memory reload and composer closure.

This wrapper keeps the canonical heap gate as the runtime owner, but makes the
startup contract explicit:

- prepare input-ready repo/docs/tool/memory context using existing report-only
  unified-run tools;
- pass that prepared context to the heap as the task file before provider lanes;
- require proposal chunks rather than a single provider answer;
- keep GPU0/NPU as companion review lanes;
- run a bounded real NPU workload when explicitly enabled;
- compose final chunks into a Documents package even when product quality is
  blocked, because blocked proposals are still operator evidence.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


DEFAULT_REQUEST = (
    "Esegui heap runtime con proposal chunks multi-parte. "
    "Non comprimere tutto nella sola risposta GPU1: salva blocchi par1/par2/par3, "
    "fai review GPU0 dei blocchi non operativi, fai micro-audit NPU se disponibile, "
    "usa debug lab e chiudi con composer finale su file persistenti."
)


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def run_command(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "passed": completed.returncode == 0,
    }


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def augmented_request(base_request: str) -> str:
    operator = base_request.strip() or DEFAULT_REQUEST
    return (
        operator
        + "\n\nHEAP CHUNK/COMPOSER CONTRACT:\n"
        + "- Treat context as persistent chunks, not as a single response window.\n"
        + "- Startup context/memory/tool/docs reload has already prepared a task-file artifact; consume it as the current heap input.\n"
        + "- Write proposal iteration artifacts for every useful partial block.\n"
        + "- GPU0 must reject or refine generic/stub chunks.\n"
        + "- NPU must produce bounded audit/workload evidence when enabled.\n"
        + "- Exit product may be blocked when placeholders/stubs remain.\n"
        + "- Final operator package is composed from proposal_iterations, provider reports and context artifacts."
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--budget-minutes", type=int, default=10)
    parser.add_argument("--max-iterations", type=int, default=6)
    parser.add_argument("--max-provider-revisions", type=int, default=6)
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=5.0)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=5000)
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--no-documents", action="store_true")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--skip-startup-reload", action="store_true")
    parser.add_argument("--startup-max-memory-chars", type=int, default=64000)
    parser.add_argument("--startup-max-context-files", type=int, default=80)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=12000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    stamp = args.stamp or now_stamp()
    project_python = resolve_project_python(repo_root, args.python_exe)
    run_dir = Path(args.output_dir) if args.output_dir else repo_root / "output" / "validation" / f"heap_context_closure_{stamp}"
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    report_file = run_dir / "heap_runtime_completeness_gate_report.json"
    markdown_file = run_dir / "heap_runtime_completeness_gate_report.md"
    startup_dir = run_dir / "startup_context_memory_reload"
    startup_manifest = startup_dir / "heap_context_memory_reload_manifest.json"
    startup_task_file = startup_dir / "heap_startup_input_ready_context.md"

    startup_result: dict[str, Any] = {
        "passed": True,
        "returncode": 0,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    startup_payload: dict[str, Any] = {}
    if not args.skip_startup_reload:
        startup_command = [
            project_python,
            "Tools/ai/prepare_heap_context_memory_reload.py",
            "--repo-root",
            ".",
            "--request",
            augmented_request(args.request),
            "--stamp",
            stamp,
            "--python-exe",
            project_python,
            "--output-dir",
            str(startup_dir),
            "--max-memory-chars",
            str(args.startup_max_memory_chars),
            "--max-context-files",
            str(args.startup_max_context_files),
            "--max-chars-per-file",
            str(args.startup_max_chars_per_file),
        ]
        startup_result = run_command(startup_command, repo_root)
        startup_payload = load_json(startup_manifest)

    heap_command = [
        project_python,
        "Tools/ai/run_heap_runtime_completeness_gate.py",
        "--repo-root",
        ".",
        "--request",
        augmented_request(args.request),
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-iterations",
        str(args.max_iterations),
        "--max-provider-revisions",
        str(args.max_provider_revisions),
        "--timeout-seconds",
        str(args.timeout_seconds),
        "--allow-npu-device-workload",
        "--npu-device-workload-seconds",
        str(args.npu_device_workload_seconds),
        "--npu-device-workload-iterations",
        str(args.npu_device_workload_iterations),
        "--output-dir",
        str(run_dir),
        "--output",
        str(report_file),
        "--markdown-output",
        str(markdown_file),
    ]
    if startup_task_file.exists():
        heap_command.extend(["--task-file", str(startup_task_file)])

    heap_result = run_command(heap_command, repo_root) if startup_result["passed"] else {
        "command": heap_command,
        "returncode": 2,
        "stdout_tail": "",
        "stderr_tail": "startup context/memory reload failed; heap run skipped",
        "passed": False,
    }

    composer_command = [
        project_python,
        "Tools/ai/compose_heap_final_proposals.py",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--report-file",
        str(report_file),
        "--output",
        str(run_dir / "heap_final_proposal_composer.json"),
        "--markdown-output",
        str(run_dir / "heap_final_proposal_composer.md"),
    ]
    if not args.no_documents:
        composer_command.append("--write-documents")
        if args.documents_root:
            composer_command.extend(["--documents-root", args.documents_root])

    composer_result = run_command(composer_command, repo_root) if report_file.exists() else {
        "command": composer_command,
        "returncode": 2,
        "stdout_tail": "",
        "stderr_tail": "heap report missing; composer skipped",
        "passed": False,
    }
    composer_report = load_json(run_dir / "heap_final_proposal_composer.json")
    composer_packaging_performed = bool((run_dir / "heap_final_proposal_composer.json").exists() and (run_dir / "heap_final_proposal_composer.md").exists())

    summary = {
        "schema_version": 1,
        "kind": "heap_runtime_context_closure_launcher",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "run_dir": str(run_dir),
        "startup_reload_performed": not args.skip_startup_reload,
        "startup_reload_passed": bool(startup_result["passed"]),
        "startup_manifest": str(startup_manifest) if startup_manifest.exists() else "",
        "startup_task_file": str(startup_task_file) if startup_task_file.exists() else "",
        "startup_artifacts": startup_payload.get("artifacts", {}) if isinstance(startup_payload, dict) else {},
        "heap_report": str(report_file),
        "heap_markdown": str(markdown_file),
        "heap_returncode": heap_result["returncode"],
        "composer_returncode": composer_result["returncode"],
        "heap_passed": heap_result["passed"],
        "composer_passed": composer_result["passed"],
        "composer_packaging_performed": composer_packaging_performed,
        "composer_blocking_issue_count": composer_report.get("blocking_issue_count"),
        "composer_documents_dir": composer_report.get("documents_dir", ""),
        "launcher_passed": bool(startup_result["passed"] and heap_result["passed"] and composer_packaging_performed),
        "heap_stdout_tail": heap_result["stdout_tail"],
        "heap_stderr_tail": heap_result["stderr_tail"],
        "startup_stdout_tail": startup_result["stdout_tail"],
        "startup_stderr_tail": startup_result["stderr_tail"],
        "composer_stdout_tail": composer_result["stdout_tail"],
        "composer_stderr_tail": composer_result["stderr_tail"],
    }

    launcher_report = run_dir / "heap_runtime_context_closure_launcher.json"
    launcher_report.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["launcher_passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
