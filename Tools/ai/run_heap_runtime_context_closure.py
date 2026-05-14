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

REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"
REVISION_CONTEXT_MARKER = "EXTERNAL HEAP REVISION CONTEXT FROM PREVIOUS RUN"


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
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


def resolve_repo_file(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def load_operator_request(
    repo_root: Path,
    inline_request: str,
    request_file: str,
) -> tuple[str, str]:
    if not request_file:
        return inline_request, ""
    path = resolve_repo_file(repo_root, request_file)
    try:
        return path.read_text(encoding="utf-8-sig"), str(path)
    except Exception as exc:
        raise SystemExit(
            f"cannot read --request-file {path}: {type(exc).__name__}: {exc}"
        ) from exc


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
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def is_complete_heap_run_dir(path: Path) -> bool:
    return (
        path.is_dir()
        and path.name.startswith("heap_context_closure_")
        and (path / REQUIRED_COMPOSER_JSON).exists()
    )


def latest_revision_context(repo_root: Path) -> tuple[Path | None, dict[str, Any], str]:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None, {}, "none"
    candidates = sorted(
        [
            run_dir / "external_heap_revision_context.json"
            for run_dir in validation_dir.iterdir()
            if is_complete_heap_run_dir(run_dir)
            and (run_dir / "external_heap_revision_context.json").exists()
        ],
        key=lambda path: path.stat().st_mtime if path.exists() else 0,
        reverse=True,
    )
    if not candidates:
        return None, {}, "none"
    path = candidates[0].resolve()
    return (
        path,
        load_json(path),
        "latest_complete_heap_context_closure_with_composer_json",
    )


def resolve_revision_context(
    repo_root: Path, value: str
) -> tuple[Path | None, dict[str, Any], str]:
    mode = str(value or "auto_latest").strip()
    if not mode or mode.lower() in {"off", "none", "false", "0"}:
        return None, {}, "off"
    if mode == "auto_latest":
        return latest_revision_context(repo_root)
    path = Path(mode)
    if not path.is_absolute():
        path = repo_root / path
    path = path.resolve()
    return path, load_json(path), "explicit_revision_context"


def revision_context_prompt(
    payload: dict[str, Any], path: Path | None, max_tasks: int
) -> str:
    if not payload:
        return ""
    tasks = payload.get("tasks") if isinstance(payload.get("tasks"), list) else []
    selected = tasks[: max(0, int(max_tasks))]
    candidate_summary = (
        payload.get("candidate_applicability_summary")
        if isinstance(payload.get("candidate_applicability_summary"), dict)
        else {}
    )
    lines = [
        "",
        REVISION_CONTEXT_MARKER + ":",
        f"- path: {path if path else ''}",
        f"- protocol: {payload.get('protocol')}",
        f"- product_acceptance_status: {payload.get('product_acceptance_status')}",
        f"- product_acceptance_passed: {payload.get('product_acceptance_passed')}",
        f"- requires_concrete_rewrite: {payload.get('requires_concrete_rewrite')}",
        f"- priority_next_action: {payload.get('priority_next_action')}",
        f"- candidate_applicability_summary: {json.dumps(candidate_summary, ensure_ascii=False)}",
        f"- resume_from_block_id: {payload.get('resume_from_block_id')}",
        f"- latest_block_id: {payload.get('latest_block_id')}",
        f"- task_count: {len(tasks)}",
        "- GPU1 must consume rewrite/propagation tasks before emitting new proposal blocks.",
        "- If requires_concrete_rewrite=true, GPU1 must first rewrite non-concrete candidates with real repo paths and concrete operations.",
        "- GPU1 must not propagate symbols from candidates marked non-concrete or from sketch/stub code.",
        "- GPU1 may move backward to propagate imports, variables, functions, classes and contracts, then resume forward.",
        "- GPU0 and NPU tasks are parallel recheck/audit work over old pointers.",
        "TASKS:",
    ]
    for idx, task in enumerate(selected, start=1):
        if not isinstance(task, dict):
            continue
        lines.append(
            f"{idx}. {task.get('task_id')} role={task.get('role')} type={task.get('task_type')} "
            f"target={task.get('target_block_id')} resume={task.get('resume_from_block_id')}"
        )
        if task.get("candidate_applicability_flags"):
            lines.append(
                f"   candidate_applicability_flags={json.dumps(task.get('candidate_applicability_flags'), ensure_ascii=False)}"
            )
        if task.get("symbol_propagation_skipped"):
            lines.append(
                f"   symbol_propagation_skipped={task.get('symbol_propagation_skipped')} "
                f"reason={task.get('symbol_propagation_skip_reason')}"
            )
        if task.get("discovered_symbols"):
            lines.append(
                f"   discovered_symbols={json.dumps(task.get('discovered_symbols'), ensure_ascii=False)}"
            )
        if task.get("rejection_reasons"):
            lines.append(
                f"   rejection_reasons={json.dumps(task.get('rejection_reasons'), ensure_ascii=False)}"
            )
        if task.get("instruction"):
            lines.append(f"   instruction={task.get('instruction')}")
    if len(tasks) > len(selected):
        lines.append(
            f"- omitted_tasks={len(tasks) - len(selected)}; read full revision context artifact for remaining tasks."
        )
    return "\n".join(lines)


def augmented_request(
    base_request: str,
    revision_context_path: Path | None = None,
    revision_context_payload: dict[str, Any] | None = None,
    revision_context_max_tasks: int = 12,
) -> str:
    operator = base_request.strip() or DEFAULT_REQUEST
    revision_payload = revision_context_payload or {}
    revision_text = ""
    if REVISION_CONTEXT_MARKER not in operator:
        revision_text = revision_context_prompt(
            revision_payload, revision_context_path, revision_context_max_tasks
        )
    return (
        operator
        + revision_text
        + "\n\nHEAP CHUNK/COMPOSER CONTRACT:\n"
        + "- Treat context as persistent chunks, not as a single response window.\n"
        + "- Startup context/memory/tool/docs reload has prepared a task-file artifact; consume it as current heap input.\n"
        + "- If startup_reload_degraded=true, carry it as an explicit heap fact and continue with degraded context.\n"
        + "- Write proposal iteration artifacts for every useful partial block.\n"
        + "- GPU1 may re-open, extend and enrich previously written proposal chunks; a richer final document can be a composed refinement of prior chunks, not only a brand-new answer.\n"
        + "- When prior chunks are thin but valid, iterate on them by adding concrete targets, acceptance criteria, validation commands, risks and package boundaries.\n"
        + "- Do not restart from scratch just because the final document needs more depth; cite previous chunk/revision ids when enriching them.\n"
        + "- GPU0 must review/refine/reject proposal chunks using source anchors, quality errors and prior iteration context.\n"
        + "- NPU must produce bounded audit/workload evidence when enabled and that evidence must enter proposal chunks.\n"
        + "- Exit product may be blocked when placeholders/stubs remain.\n"
        + "- Final operator package is composed from proposal_iterations, provider reports and context artifacts."
    )


def startup_artifact_refs(startup_payload: dict[str, Any]) -> list[str]:
    artifacts = (
        startup_payload.get("artifacts")
        if isinstance(startup_payload.get("artifacts"), dict)
        else {}
    )
    refs: list[str] = []
    for value in artifacts.values():
        if isinstance(value, str) and value and value not in refs:
            refs.append(value)
    for execution in startup_payload.get("tool_executions") or []:
        if not isinstance(execution, dict):
            continue
        for key in (
            "useful_artifact_paths",
            "existing_artifact_paths",
            "artifact_paths",
        ):
            for value in execution.get(key) or []:
                if isinstance(value, str) and value and value not in refs:
                    refs.append(value)
        for summary in execution.get("artifact_summaries") or []:
            if not isinstance(summary, dict):
                continue
            value = summary.get("path")
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
    if (
        startup_payload.get("input_ready_before_heap") is True
        and startup_task_file.exists()
    ):
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
    for item in (
        startup_payload.get("blocking_requirements", [])
        if isinstance(startup_payload.get("blocking_requirements"), list)
        else []
    ):
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
        "warnings": (
            startup_payload.get("startup_warnings", [])
            if isinstance(startup_payload.get("startup_warnings"), list)
            else []
        ),
        "metrics": {
            "stamp": stamp,
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "provider_revision_count": 0,
            "startup_reload_degraded": bool(
                startup_payload.get("startup_reload_degraded")
            ),
        },
        "real_run_output_contract": {
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "runtime_debug_lab_required": True,
            "runtime_debug_lab_passed": False,
            "context_artifact_refs": context_refs,
            "startup_manifest": repo_rel(
                repo_root,
                run_dir
                / "startup_context_memory_reload"
                / "heap_context_memory_reload_manifest.json",
            ),
            "startup_task_file": repo_rel(
                repo_root,
                run_dir
                / "startup_context_memory_reload"
                / "heap_startup_input_ready_context.md",
            ),
            "startup_reload_degraded": bool(
                startup_payload.get("startup_reload_degraded")
            ),
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
    parser.add_argument(
        "--request-file",
        default="",
        help="UTF-8 file containing the operator request. Overrides --request when set.",
    )
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--budget-minutes", type=int, default=10)
    parser.add_argument("--max-iterations", type=int, default=6)
    parser.add_argument("--min-runtime-rounds", type=int, default=1)
    parser.add_argument("--min-proposal-iterations", type=int, default=0)
    parser.add_argument("--max-provider-revisions", type=int, default=6)
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=12,
        help="Gate planning rounds; must be high enough to complete base evidence before provider lanes.",
    )
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
    parser.add_argument("--startup-scan-context-files", type=int, default=10000)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=12000)
    parser.add_argument(
        "--revision-context",
        default="auto_latest",
        help="Revision context path, 'auto_latest' or 'off'. Default auto-loads latest complete heap run context.",
    )
    parser.add_argument("--revision-context-max-tasks", type=int, default=12)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    base_request, operator_request_file = load_operator_request(
        repo_root,
        args.request,
        args.request_file,
    )
    stamp = args.stamp or now_stamp()
    project_python = resolve_project_python(repo_root, args.python_exe)
    run_dir = (
        Path(args.output_dir)
        if args.output_dir
        else repo_root / "output" / "validation" / f"heap_context_closure_{stamp}"
    )
    run_dir = run_dir.resolve()
    run_dir.mkdir(parents=True, exist_ok=True)

    (
        revision_context_path,
        revision_context_payload,
        revision_context_selection_policy,
    ) = resolve_revision_context(
        repo_root,
        args.revision_context,
    )
    heap_request = augmented_request(
        base_request,
        revision_context_path=revision_context_path,
        revision_context_payload=revision_context_payload,
        revision_context_max_tasks=args.revision_context_max_tasks,
    )

    report_file = run_dir / "heap_runtime_completeness_gate_report.json"
    markdown_file = run_dir / "heap_runtime_completeness_gate_report.md"
    heap_request_file = run_dir / "heap_operator_request.md"
    heap_request_file.write_text(heap_request, encoding="utf-8")

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
        "passed": False,
        "returncode": None,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
        "skipped": False,
    }
    startup_payload: dict[str, Any] = {}
    startup_reload_performed = False
    if args.skip_startup_reload:
        startup_result.update({"passed": True, "returncode": 0, "skipped": True})
    elif not preflight_result["passed"]:
        startup_result.update(
            {
                "passed": False,
                "returncode": 2,
                "skipped": True,
                "stderr_tail": "startup context/memory reload skipped because preflight failed",
            }
        )
    else:
        startup_command = [
            project_python,
            "Tools/ai/prepare_heap_context_memory_reload.py",
            "--repo-root",
            ".",
            "--request-file",
            str(heap_request_file),
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
            "--startup-scan-context-files",
            str(args.startup_scan_context_files),
            "--max-chars-per-file",
            str(args.startup_max_chars_per_file),
        ]
        if args.strict_startup_reload:
            startup_command.append("--strict-startup-reload")
        startup_reload_performed = True
        startup_result = run_command(startup_command, repo_root)
        startup_payload = load_json(startup_manifest)

    can_continue = startup_can_continue(
        startup_result=startup_result,
        startup_payload=startup_payload,
        startup_task_file=startup_task_file,
        strict_startup_reload=args.strict_startup_reload,
        skipped=bool(args.skip_startup_reload),
    )
    startup_reload_degraded = bool(
        startup_reload_performed
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
        "--request-file",
        str(heap_request_file),
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-iterations",
        str(args.max_iterations),
        "--min-runtime-rounds",
        str(args.min_runtime_rounds),
        "--min-proposal-iterations",
        str(args.min_proposal_iterations),
        "--max-rounds",
        str(args.max_rounds),
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
            request=heap_request,
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
        if startup_reload_degraded and can_continue and not args.strict_startup_reload:
            startup_heap_reconcile_command.append("--allow-degraded-startup")
        startup_heap_reconcile_result = run_command(
            startup_heap_reconcile_command, repo_root
        )

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
    composer_packaging_performed = bool(
        (run_dir / "heap_final_proposal_composer.json").exists()
        and (run_dir / "heap_final_proposal_composer.md").exists()
    )
    composer_documents_dir = str(composer_report.get("documents_dir", "") or "")
    composer_documents_outputs = (
        composer_report.get("documents_outputs")
        if isinstance(composer_report.get("documents_outputs"), list)
        else []
    )
    final_proposal_txt = str(composer_report.get("primary_txt", "") or "")
    final_proposal_markdown = str(composer_report.get("primary_markdown", "") or "")
    final_proposal_json = str(composer_report.get("primary_json", "") or "")
    final_download_manifest_txt = str(
        composer_report.get("download_manifest_txt", "") or ""
    )
    proposal_txt_outputs = (
        composer_report.get("proposal_txt_outputs")
        if isinstance(composer_report.get("proposal_txt_outputs"), list)
        else []
    )

    external_postrun_result: dict[str, Any] = {
        "performed": False,
        "passed": False,
        "returncode": None,
        "report": "",
        "stdout_tail": "",
        "stderr_tail": "",
    }
    if composer_packaging_performed:
        external_postrun_report = run_dir / "external_heap_postrun_package.json"
        external_postrun_command = [
            project_python,
            "Tools/ai/run_external_heap_postrun_package.py",
            "--repo-root",
            ".",
            "--python-exe",
            project_python,
            "--run-dir",
            str(run_dir),
            "--include-rejected-history",
            "--include-peer-blocks",
            "--max-block-chars",
            "50000",
            "--max-blocks",
            "0",
            "--output",
            str(external_postrun_report),
        ]
        try:
            completed = subprocess.run(
                external_postrun_command,
                cwd=repo_root,
                text=True,
                capture_output=True,
                check=False,
                timeout=max(60, int(args.timeout_seconds)),
            )
            external_postrun_result.update(
                {
                    "performed": True,
                    "passed": completed.returncode == 0,
                    "returncode": completed.returncode,
                    "report": str(external_postrun_report),
                    "command": external_postrun_command,
                    "stdout_tail": (completed.stdout or "")[-4000:],
                    "stderr_tail": (completed.stderr or "")[-4000:],
                }
            )
        except Exception as exc:  # noqa: BLE001 - post-run package is report-only.
            external_postrun_result.update(
                {
                    "performed": True,
                    "passed": False,
                    "returncode": -1,
                    "report": str(external_postrun_report),
                    "command": external_postrun_command,
                    "stderr_tail": f"{type(exc).__name__}: {exc}",
                }
            )

    external_postrun_payload = load_json(
        Path(str(external_postrun_result.get("report") or ""))
    )
    external_long_response_markdown = str(
        external_postrun_payload.get("long_response_markdown", "") or ""
    )
    external_revision_context_json = str(
        external_postrun_payload.get("revision_context_json", "") or ""
    )
    external_pointer_manifest_json = str(
        external_postrun_payload.get("pointer_manifest_json", "") or ""
    )

    final_readable_result: dict[str, Any] = {
        "performed": False,
        "passed": False,
        "returncode": None,
        "report": "",
        "markdown": "",
        "text": "",
        "documents_zip": "",
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    final_readable_payload: dict[str, Any] = {}
    if composer_packaging_performed:
        final_readable_report = run_dir / "heap_final_readable_product.json"
        final_readable_markdown = run_dir / "heap_final_readable_product.md"
        final_readable_text = run_dir / "heap_final_readable_product.txt"
        final_readable_command = [
            project_python,
            "Tools/ai/assemble_heap_final_readable_product.py",
            "--repo-root",
            ".",
            "--run-dir",
            str(run_dir),
            "--composer-json",
            str(run_dir / "heap_final_proposal_composer.json"),
            "--gate-report",
            str(report_file),
            "--output",
            str(final_readable_report),
            "--markdown-output",
            str(final_readable_markdown),
            "--text-output",
            str(final_readable_text),
        ]
        if composer_documents_dir:
            final_readable_command.extend(
                [
                    "--documents-dir",
                    composer_documents_dir,
                    "--zip-documents",
                ]
            )
        completed = run_command(final_readable_command, repo_root)
        final_readable_payload = load_json(final_readable_report)
        final_readable_result.update(
            {
                "performed": True,
                "passed": bool(completed.get("passed"))
                and bool(final_readable_payload.get("passed")),
                "returncode": completed.get("returncode"),
                "report": str(final_readable_report),
                "markdown": str(final_readable_markdown),
                "text": str(final_readable_text),
                "documents_zip": str(
                    final_readable_payload.get("documents_zip", "") or ""
                ),
                "stdout_tail": completed.get("stdout_tail", ""),
                "stderr_tail": completed.get("stderr_tail", ""),
                "command": final_readable_command,
            }
        )

    summary = {
        "schema_version": 1,
        "kind": "heap_runtime_context_closure_launcher",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "run_dir": str(run_dir),
        "revision_context_selection_policy": revision_context_selection_policy,
        "revision_context_path": (
            str(revision_context_path) if revision_context_path else ""
        ),
        "revision_context_loaded": bool(revision_context_payload),
        "operator_request_file": operator_request_file,
        "request_file": str(heap_request_file),
        "revision_context_task_count": (
            len(revision_context_payload.get("tasks", []))
            if isinstance(revision_context_payload.get("tasks"), list)
            else 0
        ),
        "revision_context_requires_concrete_rewrite": revision_context_payload.get(
            "requires_concrete_rewrite"
        ),
        "revision_context_priority_next_action": revision_context_payload.get(
            "priority_next_action"
        ),
        "revision_context_candidate_applicability_summary": (
            revision_context_payload.get("candidate_applicability_summary")
            if isinstance(
                revision_context_payload.get("candidate_applicability_summary"), dict
            )
            else {}
        ),
        "max_iterations_requested": args.max_iterations,
        "min_runtime_rounds_requested": args.min_runtime_rounds,
        "min_proposal_iterations_requested": args.min_proposal_iterations,
        "max_rounds_forwarded": args.max_rounds,
        "preflight_performed": not args.skip_preflight,
        "preflight_passed": bool(preflight_result["passed"]),
        "preflight_report": str(preflight_report) if preflight_report.exists() else "",
        "preflight_markdown": (
            str(preflight_markdown) if preflight_markdown.exists() else ""
        ),
        "preflight_returncode": preflight_result["returncode"],
        "startup_reload_performed": startup_reload_performed,
        "startup_reload_passed": bool(startup_result["passed"]),
        "startup_reload_degraded": startup_reload_degraded,
        "startup_can_continue": can_continue,
        "strict_startup_reload": bool(args.strict_startup_reload),
        "startup_manifest": str(startup_manifest) if startup_manifest.exists() else "",
        "startup_heap_reconcile_returncode": startup_heap_reconcile_result[
            "returncode"
        ],
        "startup_heap_reconcile_passed": bool(startup_heap_reconcile_result["passed"]),
        "startup_heap_reconcile_report": (
            str(startup_heap_reconcile_report)
            if startup_heap_reconcile_report.exists()
            else ""
        ),
        "startup_heap_reconcile_markdown": (
            str(startup_heap_reconcile_markdown)
            if startup_heap_reconcile_markdown.exists()
            else ""
        ),
        "startup_reconcile_degraded_policy_used": bool(
            startup_reload_degraded and can_continue and not args.strict_startup_reload
        ),
        "startup_task_file": (
            str(startup_task_file) if startup_task_file.exists() else ""
        ),
        "startup_artifacts": (
            startup_payload.get("artifacts", {})
            if isinstance(startup_payload, dict)
            else {}
        ),
        "startup_artifact_ref_count": (
            len(startup_artifact_refs(startup_payload))
            if isinstance(startup_payload, dict)
            else 0
        ),
        "startup_blocking_requirements": (
            startup_payload.get("blocking_requirements", [])
            if isinstance(startup_payload, dict)
            else []
        ),
        "startup_degraded_requirements": (
            startup_payload.get("degraded_requirements", [])
            if isinstance(startup_payload, dict)
            else []
        ),
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
        "external_postrun_package_performed": bool(
            external_postrun_result.get("performed")
        ),
        "external_postrun_package_passed": bool(external_postrun_result.get("passed")),
        "external_postrun_package_returncode": external_postrun_result.get(
            "returncode"
        ),
        "external_postrun_package_report": external_postrun_result.get("report", ""),
        "external_long_response_markdown": external_long_response_markdown,
        "external_revision_context_json": external_revision_context_json,
        "external_pointer_manifest_json": external_pointer_manifest_json,
        "final_readable_product_performed": bool(
            final_readable_result.get("performed")
        ),
        "final_readable_product_passed": bool(final_readable_result.get("passed")),
        "final_readable_product_report": final_readable_result.get("report", ""),
        "final_readable_product_markdown": final_readable_result.get("markdown", ""),
        "final_readable_product_text": final_readable_result.get("text", ""),
        "final_readable_product_documents_outputs": final_readable_payload.get(
            "documents_outputs", {}
        ),
        "final_readable_product_zip": final_readable_result.get("documents_zip", ""),
        "download_hint": composer_report.get("download_hint", ""),
        "launcher_passed": bool(
            can_continue and heap_result["passed"] and composer_result["passed"]
        ),
        "launcher_packaging_succeeded": bool(
            composer_packaging_performed
            and final_readable_result.get("passed")
            and (can_continue or fallback_heap_report_written)
        ),
        "preflight_stdout_tail": preflight_result["stdout_tail"],
        "preflight_stderr_tail": preflight_result["stderr_tail"],
        "heap_stdout_tail": heap_result["stdout_tail"],
        "heap_stderr_tail": heap_result["stderr_tail"],
        "preflight_command": preflight_result.get("command", []),
        "startup_command": startup_result.get("command", []),
        "heap_command": heap_result.get("command", []),
        "composer_command": composer_result.get("command", []),
        "external_postrun_command": external_postrun_result.get("command", []),
        "final_readable_product_command": final_readable_result.get("command", []),
        "startup_stdout_tail": startup_result["stdout_tail"],
        "startup_stderr_tail": startup_result["stderr_tail"],
        "composer_stdout_tail": composer_result["stdout_tail"],
        "composer_stderr_tail": composer_result["stderr_tail"],
        "external_postrun_stdout_tail": external_postrun_result.get("stdout_tail", ""),
        "external_postrun_stderr_tail": external_postrun_result.get("stderr_tail", ""),
        "final_readable_product_stdout_tail": final_readable_result.get(
            "stdout_tail", ""
        ),
        "final_readable_product_stderr_tail": final_readable_result.get(
            "stderr_tail", ""
        ),
    }

    launcher_report = run_dir / "heap_runtime_context_closure_launcher.json"
    write_json(launcher_report, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["launcher_packaging_succeeded"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
