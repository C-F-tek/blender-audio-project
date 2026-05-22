"""Orchestrate heap runtime context closure phases."""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any
from .commands import heap_command, startup_command
from .common import (
    load_json,
    load_operator_request,
    now_stamp,
    resolve_project_python,
    resolve_repo_root,
    resolve_revision_context,
    run_command,
    terminate_provider_launch_manifest_processes,
    write_documents_run_manifest,
    write_json,
)
from .fallback import write_fallback_heap_report
from .postrun import run_external_postrun_package, run_final_readable_product
from .preflight_policy import classify_preflight_gate
from .requesting import augmented_request, startup_can_continue
from .summary import build_launcher_summary
def run_launcher(args: Any) -> int:
    state = _prepare_state(args)
    _write_started_manifest(args, state)
    _resolve_revision_context(args, state)
    _write_heap_request(args, state)
    _run_preflight(args, state)
    _run_startup(args, state)
    _run_heap(args, state)
    _run_reconciliation(args, state)
    _run_composer(args, state)
    _run_postrun(args, state)
    _write_completed_manifest(args, state)
    summary = build_launcher_summary(args, state)
    write_json(state["run_dir"] / "heap_runtime_context_closure_launcher.json", summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["launcher_passed"] else 2
def _prepare_state(args: Any) -> dict[str, Any]:
    repo_root = resolve_repo_root(args.repo_root)
    base_request, operator_request_file = load_operator_request(
        repo_root,
        args.request,
        args.request_file,
    )
    stamp = args.stamp or now_stamp()
    run_dir = (
        Path(args.output_dir)
        if args.output_dir
        else repo_root / "output" / "validation" / f"heap_context_closure_{stamp}"
    ).resolve()
    run_dir.mkdir(parents=True, exist_ok=True)
    startup_dir = run_dir / "startup_context_memory_reload"
    return {
        "repo_root": repo_root,
        "base_request": base_request,
        "operator_request_file": operator_request_file,
        "stamp": stamp,
        "project_python": resolve_project_python(repo_root, args.python_exe),
        "run_dir": run_dir,
        "report_file": run_dir / "heap_runtime_completeness_gate_report.json",
        "markdown_file": run_dir / "heap_runtime_completeness_gate_report.md",
        "heap_request_file": "",
        "startup_dir": startup_dir,
        "startup_manifest": startup_dir / "heap_context_memory_reload_manifest.json",
        "startup_task_file": startup_dir / "heap_startup_input_ready_context.md",
        "preflight_report": run_dir / "heap_context_preflight_gate.json",
        "preflight_markdown": run_dir / "heap_context_preflight_gate.md",
    }
def _write_started_manifest(args: Any, state: dict[str, Any]) -> None:
    if args.documents_root and not args.no_documents:
        write_documents_run_manifest(
            documents_root=args.documents_root,
            repo_root=state["repo_root"],
            run_dir=state["run_dir"],
            stamp=state["stamp"],
            request_file=state["operator_request_file"],
            status="started",
        )


def _resolve_revision_context(args: Any, state: dict[str, Any]) -> None:
    path, payload, policy = resolve_revision_context(state["repo_root"], args.revision_context)
    state.update(
        {
            "revision_context_path": path,
            "revision_context_payload": payload,
            "revision_context_selection_policy": policy,
        }
    )


def _write_heap_request(args: Any, state: dict[str, Any]) -> None:
    heap_request = augmented_request(
        state["base_request"],
        revision_context_path=state["revision_context_path"],
        revision_context_payload=state["revision_context_payload"],
        revision_context_max_tasks=args.revision_context_max_tasks,
    )
    state["heap_request"] = heap_request
    state["request_transport"] = "inline_cli"
    if state.get("operator_request_file"):
        state["request_transport"] = "operator_request_file"


def _empty_result(passed: bool = True, returncode: int | None = 0) -> dict[str, Any]:
    return {
        "passed": passed,
        "returncode": returncode,
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }


def _run_preflight(args: Any, state: dict[str, Any]) -> None:
    result = _empty_result()
    if not args.skip_preflight:
        command = [
            state["project_python"],
            "-m",
            "Tools.validation",
            "run_real_product_preflight_gate",
            "--repo-root",
            ".",
            "--output",
            str(state["preflight_report"]),
            "--markdown-output",
            str(state["preflight_markdown"]),
            "--timeout-seconds",
            str(args.preflight_timeout_seconds),
        ]
        result = run_command(
            command,
            state["repo_root"],
            timeout_seconds=max(30, int(args.preflight_timeout_seconds) + 30),
            flow_dir=state["run_dir"],
            phase="preflight",
        )
    report = load_json(state["preflight_report"])
    policy = classify_preflight_gate(
        skipped=bool(args.skip_preflight),
        result=result,
        report=report,
    )
    state["preflight_result"] = result
    state["preflight_report_payload"] = report
    state["preflight_policy"] = policy
    state["preflight_blocks_startup"] = bool(policy["preflight_blocks_startup"])
    state["preflight_nonblocking_for_provider_generation"] = bool(
        policy["preflight_failed_but_runtime_allowed"]
    )


def _run_startup(args: Any, state: dict[str, Any]) -> None:
    result = _empty_result(passed=False, returncode=None)
    result["skipped"] = False
    payload: dict[str, Any] = {}
    performed = False
    if args.skip_startup_reload:
        result.update({"passed": True, "returncode": 0, "skipped": True})
    elif state["preflight_blocks_startup"]:
        result.update(
            {
                "passed": False,
                "returncode": 2,
                "skipped": True,
                "stderr_tail": "startup context/memory reload skipped because preflight failed",
            }
        )
    else:
        command = startup_command(args, state)
        if args.strict_startup_reload:
            command.append("--strict-startup-reload")
        performed = True
        result = run_command(
            command,
            state["repo_root"],
            flow_dir=state["run_dir"],
            phase="startup_context_memory_reload",
        )
        if state["preflight_nonblocking_for_provider_generation"]:
            result["preflight_nonblocking_for_provider_generation"] = True
            result["preflight_before_startup_passed"] = False
        payload = load_json(state["startup_manifest"])

    can_continue = startup_can_continue(
        startup_result=result,
        startup_payload=payload,
        startup_task_file=state["startup_task_file"],
        strict_startup_reload=args.strict_startup_reload,
        skipped=bool(args.skip_startup_reload),
    )
    state.update(
        {
            "startup_result": result,
            "startup_payload": payload,
            "startup_reload_performed": performed,
            "can_continue": can_continue,
            "startup_reload_degraded": bool(
                performed
                and (
                    payload.get("startup_reload_degraded")
                    or (not result.get("passed") and can_continue)
                )
            ),
        }
    )


def _run_heap(args: Any, state: dict[str, Any]) -> None:
    command = heap_command(args, state)
    if state["startup_manifest"].exists():
        command.extend(["--startup-manifest", str(state["startup_manifest"])])
    if state["startup_task_file"].exists():
        command.extend(["--task-file", str(state["startup_task_file"])])

    if state["can_continue"]:
        try:
            heap_result = run_command(
                command,
                state["repo_root"],
                timeout_seconds=None,
                flow_dir=state["run_dir"],
                phase="heap_runtime_gate",
            )
        except BaseException:
            state["provider_orphan_cleanup"] = terminate_provider_launch_manifest_processes(
                run_dir=state["run_dir"],
                repo_root=state["repo_root"],
                reason="heap runtime gate interrupted before closure cleanup",
            )
            raise
    else:
        heap_result = {
            "command": command,
            "returncode": 2,
            "stdout_tail": "",
            "stderr_tail": "startup context/memory reload hard failed; fallback heap report will be composed",
            "passed": False,
        }
    state["heap_result"] = heap_result
    state["fallback_heap_report_written"] = False
    cleanup_reason = ""
    if not heap_result.get("passed"):
        cleanup_reason = "heap command failed before launcher completion"
    if not state["report_file"].exists():
        cleanup_reason = "heap report missing after heap command"
    if cleanup_reason:
        cleanup = terminate_provider_launch_manifest_processes(
            run_dir=state["run_dir"],
            repo_root=state["repo_root"],
            reason=cleanup_reason,
        )
        state["provider_orphan_cleanup"] = cleanup
        heap_result["provider_orphan_cleanup"] = cleanup
    elif (state["run_dir"] / "provider_teamwork").exists():
        cleanup = terminate_provider_launch_manifest_processes(
            run_dir=state["run_dir"],
            repo_root=state["repo_root"],
            reason="heap command completed provider cleanup",
        )
        state["provider_orphan_cleanup"] = cleanup
        heap_result["provider_orphan_cleanup"] = cleanup
    else:
        state["provider_orphan_cleanup"] = {}
    if not state["report_file"].exists():
        reason = (
            "startup context/memory reload hard failed"
            if not state["can_continue"]
            else "heap report missing after heap command"
        )
        write_fallback_heap_report(
            repo_root=state["repo_root"],
            stamp=state["stamp"],
            run_dir=state["run_dir"],
            report_file=state["report_file"],
            markdown_file=state["markdown_file"],
            request=state["heap_request"],
            startup_payload=state["startup_payload"],
            startup_result=state["startup_result"],
            heap_result=heap_result,
            reason=reason,
        )
        state["fallback_heap_report_written"] = True
def _run_reconciliation(args: Any, state: dict[str, Any]) -> None:
    state["startup_heap_reconcile_report"] = (
        state["run_dir"] / "heap_startup_context_reconciliation.json"
    )
    state["startup_heap_reconcile_markdown"] = (
        state["run_dir"] / "heap_startup_context_reconciliation.md"
    )
    result = _empty_result()
    if state["report_file"].exists() and state["startup_manifest"].exists():
        command = [
            state["project_python"],
            "-m",
            "ia_carmine",
            "reconcile_heap_report_with_startup_reload",
            "--repo-root",
            ".",
            "--startup-manifest",
            str(state["startup_manifest"]),
            "--heap-report",
            str(state["report_file"]),
            "--output",
            str(state["startup_heap_reconcile_report"]),
            "--markdown-output",
            str(state["startup_heap_reconcile_markdown"]),
        ]
        if state["startup_reload_degraded"] and state["can_continue"] and not args.strict_startup_reload:
            command.append("--allow-degraded-startup")
        result = run_command(
            command,
            state["repo_root"],
            flow_dir=state["run_dir"],
            phase="startup_heap_reconciliation",
        )
    state["startup_heap_reconcile_result"] = result


def _run_composer(args: Any, state: dict[str, Any]) -> None:
    command = [
        state["project_python"],
        "-m",
        "ia_carmine",
        "heap_final_proposals",
        "--repo-root",
        ".",
        "--run-dir",
        str(state["run_dir"]),
        "--report-file",
        str(state["report_file"]),
        "--output",
        str(state["run_dir"] / "heap_final_proposal_composer.json"),
        "--markdown-output",
        str(state["run_dir"] / "heap_final_proposal_composer.md"),
    ]
    if not args.no_documents:
        command.append("--write-documents")
        if args.documents_root:
            command.extend(["--documents-root", args.documents_root])
    result = run_command(
        command,
        state["repo_root"],
        flow_dir=state["run_dir"],
        phase="heap_final_proposals",
    )
    composer_report = load_json(state["run_dir"] / "heap_final_proposal_composer.json")
    state.update(
        {
            "composer_result": result,
            "composer_report": composer_report,
            "composer_packaging_performed": bool(
                (state["run_dir"] / "heap_final_proposal_composer.json").exists()
                and (state["run_dir"] / "heap_final_proposal_composer.md").exists()
            ),
            "composer_documents_dir": str(composer_report.get("documents_dir", "") or ""),
            "composer_documents_outputs": _list_or_empty(
                composer_report.get("documents_outputs")
            ),
            "final_proposal_txt": str(composer_report.get("primary_txt", "") or ""),
            "final_proposal_markdown": str(composer_report.get("primary_markdown", "") or ""),
            "final_proposal_json": str(composer_report.get("primary_json", "") or ""),
            "final_download_manifest_txt": str(
                composer_report.get("download_manifest_txt", "") or ""
            ),
            "proposal_txt_outputs": _list_or_empty(composer_report.get("proposal_txt_outputs")),
        }
    )


def _run_postrun(args: Any, state: dict[str, Any]) -> None:
    external_result, external_payload = run_external_postrun_package(
        repo_root=state["repo_root"],
        project_python=state["project_python"],
        run_dir=state["run_dir"],
        timeout_seconds=args.timeout_seconds,
        composer_packaging_performed=state["composer_packaging_performed"],
    )
    final_result, final_payload = run_final_readable_product(
        repo_root=state["repo_root"],
        project_python=state["project_python"],
        run_dir=state["run_dir"],
        report_file=state["report_file"],
        composer_documents_dir=state["composer_documents_dir"],
        composer_packaging_performed=state["composer_packaging_performed"],
    )
    state.update(
        {
            "external_postrun_result": external_result,
            "external_postrun_payload": external_payload,
            "final_readable_result": final_result,
            "final_readable_payload": final_payload,
        }
    )


def _write_completed_manifest(args: Any, state: dict[str, Any]) -> None:
    if args.documents_root and not args.no_documents:
        write_documents_run_manifest(
            documents_root=args.documents_root,
            repo_root=state["repo_root"],
            run_dir=state["run_dir"],
            stamp=state["stamp"],
            request_file=state["operator_request_file"],
            status="completed" if state["final_readable_result"].get("passed") else "blocked",
        )


def _list_or_empty(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []
