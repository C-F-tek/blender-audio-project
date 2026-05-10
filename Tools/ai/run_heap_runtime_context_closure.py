#!/usr/bin/env python3
"""Launch heap runtime with explicit context/memory reload and composer closure.

The wrapper makes startup reload a first-class pre-provider phase. Degraded
preload does not skip the heap when a usable task file and artifact manifest
exist. If the heap itself cannot emit a report, the wrapper writes a deterministic
fallback heap report so the final composer always exports an operator-readable
package under Documents when requested.
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


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


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


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def augmented_request(base_request: str) -> str:
    operator = base_request.strip() or DEFAULT_REQUEST
    return (
        operator
        + "\n\nHEAP CHUNK/COMPOSER CONTRACT:\n"
        + "- Treat context as persistent chunks, not as a single response window.\n"
        + "- Startup context/memory/tool/docs reload has prepared a task-file artifact; consume it as current heap input.\n"
        + "- If startup_reload_degraded=true, carry it as an explicit heap fact and continue with degraded context.\n"
        + "- Write proposal iteration artifacts for every useful partial block.\n"
        + "- GPU0 must review/refine/reject proposal chunks using source anchors, quality errors and prior iteration context.\n"
        + "- NPU must produce bounded audit/workload evidence when enabled and that evidence must enter proposal chunks.\n"
        + "- Exit product may be blocked when placeholders/stubs remain.\n"
        + "- Final operator package is composed from proposal_iterations, provider reports and context artifacts."
    )


def startup_artifact_refs(startup_payload: dict[str, Any]) -> list[str]:
    artifacts = startup_payload.get("artifacts") if isinstance(startup_payload.get("artifacts"), dict) else {}
    refs: list[str] = []
    for value in artifacts.values():
        if isinstance(value, str) and value and value not in refs:
            refs.append(value)
    return refs


def startup_can_continue(
    *,
    startup_result: dict[str, Any],
    startup_payload: dict[str, Any],
    startup_task_file: Path,
    strict_startup_reload: bool,
    skipped: bool,
) -> bool:
    if skipped:
        return True
    if startup_result.get("passed") is True:
        return True
    if strict_startup_reload:
        return False
    if startup_payload.get("input_ready_before_heap") is True and startup_task_file.exists():
        return True
    if startup_task_file.exists() and startup_artifact_refs(startup_payload):
        return True
    return False


def write_fallback_heap_report(
    *,
    repo_root: Path,
    stamp: str,
    run_dir: Path,
    report_file: Path,
    markdown_file: Path,
    request: str,
    startup_payload: dict[str, Any],
    startup_result: dict[str, Any],
    heap_result: dict[str, Any],
    reason: str,
) -> dict[str, Any]:
    context_refs = startup_artifact_refs(startup_payload)
    blocking = [reason]
    if startup_payload.get("startup_reload_degraded"):
        blocking.append("startup_reload_degraded=True")
    for item in startup_payload.get("blocking_requirements", []) if isinstance(startup_payload.get("blocking_requirements"), list) else []:
        blocking.append(f"startup blocking requirement: {item}")
    report = {
        "schema_version": 1,
        "kind": "heap_runtime_completeness_gate",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "request": request,
        "passed": False,
        "fallback_heap_report": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": blocking,
        "warnings": startup_payload.get("startup_warnings", []) if isinstance(startup_payload.get("startup_warnings"), list) else [],
        "metrics": {
            "stamp": stamp,
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "provider_revision_count": 0,
            "startup_reload_degraded": bool(startup_payload.get("startup_reload_degraded")),
        },
        "real_run_output_contract": {
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "runtime_debug_lab_required": True,
            "runtime_debug_lab_passed": False,
            "context_artifact_refs": context_refs,
            "startup_manifest": repo_rel(repo_root, run_dir / "startup_context_memory_reload" / "heap_context_memory_reload_manifest.json"),
            "startup_task_file": repo_rel(repo_root, run_dir / "startup_context_memory_reload" / "heap_startup_input_ready_context.md"),
            "startup_reload_degraded": bool(startup_payload.get("startup_reload_degraded")),
            "fallback_reason": reason,
        },
        "startup_context_memory_reload": startup_payload,
        "command_results": {
            "startup": startup_result,
            "heap": heap_result,
        },
    }
    write_json(report_file, report)
    lines = [
        "# Heap Runtime Fallback Report",
        "",
        f"- Product status: `{report['metrics']['product_status']}`",
        f"- Quality output passed: `{report['metrics']['quality_output_passed']}`",
        f"- Fallback reason: `{reason}`",
        f"- Startup reload degraded: `{startup_payload.get('startup_reload_degraded')}`",
        "",
        "## Context artifacts",
        "",
    ]
    lines.extend(f"- `{ref}`" for ref in context_refs)
    lines.extend(["", "## Blocking issues", ""])
    lines.extend(f"- {item}" for item in blocking)
    markdown_file.parent.mkdir(parents=True, exist_ok=True)
    markdown_file.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default=DEFAULT_REQUEST)
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--budget-minutes", type=int, default=10)
    parser.add_argument("--max-iterations", type=int, default=6)
    parser.add_argument("--max-provider-revisions", type=int, default=6)
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=5.0)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=5000)
    parser.add_argument("--documents-root", default="")
    parser.add_argument("--no-documents", action="store_true")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--skip-preflight", action="store_true")
    parser.add_argument("--preflight-timeout-seconds", type=int, default=120)
    parser.add_argument("--skip-startup-reload", action="store_true")
    parser.add_argument("--strict-startup-reload", action="store_true")
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

    preflight_report = run_dir / "heap_context_preflight_gate.json"
    preflight_markdown = run_dir / "heap_context_preflight_gate.md"
    preflight_result: dict[str, Any] = {
        "passed": True,
        "returncode": 0,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    if not args.skip_preflight:
        preflight_command = [
            project_python,
            "Tools/validation/run_real_product_preflight_gate.py",
            "--repo-root",
            ".",
            "--output",
            str(preflight_report),
            "--markdown-output",
            str(preflight_markdown),
            "--timeout-seconds",
            str(args.preflight_timeout_seconds),
        ]
        preflight_result = run_command(preflight_command, repo_root)

    startup_result: dict[str, Any] = {
        "passed": True,
        "returncode": 0,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    startup_payload: dict[str, Any] = {}
    if preflight_result["passed"] and not args.skip_startup_reload:
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
        if args.strict_startup_reload:
            startup_command.append("--strict-startup-reload")
        startup_result = run_command(startup_command, repo_root)
        startup_payload = load_json(startup_manifest)

    can_continue = startup_can_continue(
        startup_result=startup_result,
        startup_payload=startup_payload,
        startup_task_file=startup_task_file,
        strict_startup_reload=args.strict_startup_reload,
        skipped=args.skip_startup_reload,
    )
    startup_reload_degraded = bool(
        (not args.skip_startup_reload)
        and (
            startup_payload.get("startup_reload_degraded")
            or (not startup_result.get("passed") and can_continue)
        )
    )

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

    if getattr(args, "allow_provider_generation", False):
        heap_command.append("--allow-provider-generation")
        heap_command.append("--operator-intent")

    if can_continue:
        heap_result = run_command(heap_command, repo_root)
    else:
        heap_result = {
            "command": heap_command,
            "returncode": 2,
            "stdout_tail": "",
            "stderr_tail": "startup context/memory reload hard failed; fallback heap report will be composed",
            "passed": False,
        }

    fallback_heap_report_written = False
    if not report_file.exists():
        reason = (
            "startup context/memory reload hard failed"
            if not can_continue
            else "heap report missing after heap command"
        )
        write_fallback_heap_report(
            repo_root=repo_root,
            stamp=stamp,
            run_dir=run_dir,
            report_file=report_file,
            markdown_file=markdown_file,
            request=augmented_request(args.request),
            startup_payload=startup_payload,
            startup_result=startup_result,
            heap_result=heap_result,
            reason=reason,
        )
        fallback_heap_report_written = True


    startup_heap_reconcile_report = run_dir / "heap_startup_context_reconciliation.json"
    startup_heap_reconcile_markdown = run_dir / "heap_startup_context_reconciliation.md"
    startup_heap_reconcile_result: dict[str, Any] = {
        "passed": True,
        "returncode": 0,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    if report_file.exists() and startup_manifest.exists():
        startup_heap_reconcile_command = [
            project_python,
            "Tools/ai/reconcile_heap_report_with_startup_reload.py",
            "--repo-root",
            ".",
            "--startup-manifest",
            str(startup_manifest),
            "--heap-report",
            str(report_file),
            "--output",
            str(startup_heap_reconcile_report),
            "--markdown-output",
            str(startup_heap_reconcile_markdown),
        ]
        startup_heap_reconcile_result = run_command(startup_heap_reconcile_command, repo_root)

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

    composer_result = run_command(composer_command, repo_root)
    composer_report = load_json(run_dir / "heap_final_proposal_composer.json")
    composer_packaging_performed = bool((run_dir / "heap_final_proposal_composer.json").exists() and (run_dir / "heap_final_proposal_composer.md").exists())
    composer_documents_dir = str(composer_report.get("documents_dir", "") or "")
    composer_documents_outputs = composer_report.get("documents_outputs") if isinstance(composer_report.get("documents_outputs"), list) else []
    final_proposal_txt = str(composer_report.get("primary_txt", "") or "")
    final_proposal_markdown = str(composer_report.get("primary_markdown", "") or "")
    final_proposal_json = str(composer_report.get("primary_json", "") or "")
    final_download_manifest_txt = str(composer_report.get("download_manifest_txt", "") or "")
    proposal_txt_outputs = composer_report.get("proposal_txt_outputs") if isinstance(composer_report.get("proposal_txt_outputs"), list) else []

    summary = {
        "schema_version": 1,
        "kind": "heap_runtime_context_closure_launcher",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "run_dir": str(run_dir),
        "preflight_performed": not args.skip_preflight,
        "preflight_passed": bool(preflight_result["passed"]),
        "preflight_report": str(preflight_report) if preflight_report.exists() else "",
        "preflight_markdown": str(preflight_markdown) if preflight_markdown.exists() else "",
        "preflight_returncode": preflight_result["returncode"],
        "startup_reload_performed": not args.skip_startup_reload,
        "startup_reload_passed": bool(startup_result["passed"]),
        "startup_reload_degraded": startup_reload_degraded,
        "startup_can_continue": can_continue,
        "strict_startup_reload": bool(args.strict_startup_reload),
        "startup_manifest": str(startup_manifest) if startup_manifest.exists() else "",
        "startup_heap_reconcile_returncode": startup_heap_reconcile_result["returncode"],
        "startup_heap_reconcile_passed": bool(startup_heap_reconcile_result["passed"]),
        "startup_heap_reconcile_report": str(startup_heap_reconcile_report) if startup_heap_reconcile_report.exists() else "",
        "startup_heap_reconcile_markdown": str(startup_heap_reconcile_markdown) if startup_heap_reconcile_markdown.exists() else "",
        "startup_task_file": str(startup_task_file) if startup_task_file.exists() else "",
        "startup_artifacts": startup_payload.get("artifacts", {}) if isinstance(startup_payload, dict) else {},
        "startup_blocking_requirements": startup_payload.get("blocking_requirements", []) if isinstance(startup_payload, dict) else [],
        "startup_degraded_requirements": startup_payload.get("degraded_requirements", []) if isinstance(startup_payload, dict) else [],
        "heap_report": str(report_file),
        "heap_markdown": str(markdown_file),
        "heap_returncode": heap_result["returncode"],
        "composer_returncode": composer_result["returncode"],
        "heap_passed": heap_result["passed"],
        "composer_passed": composer_result["passed"],
        "fallback_heap_report_written": fallback_heap_report_written,
        "composer_packaging_performed": composer_packaging_performed,
        "composer_blocking_issue_count": composer_report.get("blocking_issue_count"),
        "composer_documents_dir": composer_documents_dir,
        "composer_documents_outputs": composer_documents_outputs,
        "final_proposal_txt": final_proposal_txt,
        "final_proposal_markdown": final_proposal_markdown,
        "final_proposal_json": final_proposal_json,
        "final_download_manifest_txt": final_download_manifest_txt,
        "proposal_txt_outputs": proposal_txt_outputs,
        "download_hint": composer_report.get("download_hint", ""),
        "launcher_passed": bool(startup_result["passed"] and heap_result["passed"] and composer_result["passed"]),
        "launcher_packaging_succeeded": bool(composer_packaging_performed and (can_continue or fallback_heap_report_written)),
        "preflight_stdout_tail": preflight_result["stdout_tail"],
        "preflight_stderr_tail": preflight_result["stderr_tail"],
        "heap_stdout_tail": heap_result["stdout_tail"],
        "heap_stderr_tail": heap_result["stderr_tail"],
        "startup_stdout_tail": startup_result["stdout_tail"],
        "startup_stderr_tail": startup_result["stderr_tail"],
        "composer_stdout_tail": composer_result["stdout_tail"],
        "composer_stderr_tail": composer_result["stderr_tail"],
    }

    launcher_report = run_dir / "heap_runtime_context_closure_launcher.json"
    write_json(launcher_report, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["launcher_packaging_succeeded"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
