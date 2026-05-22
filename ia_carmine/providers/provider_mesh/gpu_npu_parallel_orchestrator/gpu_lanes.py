from __future__ import annotations

from .common import *  # noqa: F403
from .support_lanes import (
    harvest_support_records,
    launch_due_checkpoint_supports,
    launch_support_with_record,
    support_launch_blocked,
    support_diagnostic_details,
    support_response_payload,
    support_repo_rel,
)


def build_gpu_command(
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    gpu_output: Path,
    gpu_markdown: Path,
) -> list[str]:
    command = [
        resolve_child_python(),
        "ia_carmine/providers/provider_mesh/gpu_deep_planning_supervised/cli.py",
        "--repo-root",
        ".",
        "--use-ollama",
        "--budget-minutes",
        str(args.budget_minutes),
        "--max-rounds",
        str(args.max_rounds),
        "--files-per-round",
        str(args.files_per_round),
        "--max-context-files",
        str(args.max_context_files),
        "--max-chars-per-file",
        str(args.max_chars_per_file),
        "--max-new-tokens",
        str(args.max_new_tokens),
        "--keep-alive",
        args.keep_alive,
        "--evidence",
        args.evidence,
        "--refined-review",
        args.refined_review,
        "--checkpoint-dir",
        str(checkpoint_dir),
        "--output",
        str(gpu_output),
        "--markdown-output",
        str(gpu_markdown),
    ]
    if args.ollama_model:
        command.extend(["--ollama-model", args.ollama_model])
    if args.ollama_base_url:
        command.extend(["--ollama-base-url", args.ollama_base_url])
    if args.enable_runtime_tool_broker and getattr(
        args, "gpu_runner_direct_runtime_tool_broker", False
    ):
        command.append("--enable-runtime-tool-broker")
        command.extend(["--runtime-tool-output-dir", args.runtime_tool_output_dir])
        command.extend(["--runtime-tool-timeout-seconds", str(args.runtime_tool_timeout_seconds)])
        command.extend(
            [
                "--runtime-tool-max-requests-per-round",
                str(args.runtime_tool_max_requests_per_round),
            ]
        )
        if args.disable_runtime_tool_bootstrap:
            command.append("--disable-runtime-tool-bootstrap")
    bootstrap_report = getattr(args, "orchestrator_runtime_tool_bootstrap_result", {})
    if (
        args.enable_runtime_tool_broker
        and isinstance(bootstrap_report, dict)
        and bootstrap_report.get("broker_output")
    ):
        command.extend(["--report-file", str(bootstrap_report["broker_output"])])
    if args.enable_runtime_tool_broker and getattr(args, "runtime_heap_snapshot", ""):
        command.extend(["--live-context-report", str(args.runtime_heap_snapshot)])
        command.append("--refresh-live-context-each-round")
    for report_file in args.report_file:
        command.extend(["--report-file", report_file])
    for context_root in args.context_root:
        command.extend(["--context-root", context_root])
    return command


def launch_gpu0_peer_support(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    round_id: int,
    checkpoint: Path | None,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool,
) -> bool:
    if support_launch_blocked(
        args=args,
        round_id=round_id,
        active_supports=active_supports,
        support_records=support_records,
        enabled_attr="run_gpu0_peer_support_provider",
        max_concurrent_attr="max_concurrent_gpu0_peer_support",
    ):
        return False

    support_json = gpu0_peer_support_output_path(args, repo_root, round_id)
    command = build_gpu0_peer_support_command(args, support_json, round_id)
    checkpoint_rel = support_repo_rel(checkpoint, repo_root)
    correlation_id = f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support-{round_id:03d}"
    launch_support_with_record(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        round_id=round_id,
        active_supports=active_supports,
        support_records=support_records,
        command=command,
        record={
            "round": round_id,
            "checkpoint": checkpoint_rel,
            "support_output": repo_rel(support_json, repo_root),
            "support_markdown": repo_rel(support_json.with_suffix(".md"), repo_root),
            "started_at": now_iso(),
            "status": "running",
            "command": command,
            "launched_while_gpu1_active": bool(gpu1_active),
            "provider_execution_requested": True,
            "provider_execution_performed": False,
        },
        lane="gpu0",
        correlation_id=correlation_id,
        payload={
            "summary": "GPU0 peer support launched while GPU1 primary advisory continues.",
            "round": round_id,
            "checkpoint": checkpoint_rel,
            "output": repo_rel(support_json, repo_root),
            "gpu1_active": bool(gpu1_active),
            "direct_tool_execution": False,
            "provider_lane": "Ollama GPU0 Vulkan",
        },
        diagnostic_message="GPU0 peer support subprocess launched.",
        diagnostic_details={
            "round": round_id,
            "output": repo_rel(support_json, repo_root),
            "gpu1_active": bool(gpu1_active),
        },
    )
    return True


def launch_due_gpu0_peer_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    launched_rounds: set[int],
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool,
) -> None:
    launch_due_checkpoint_supports(
        args=args,
        repo_root=repo_root,
        checkpoint_dir=checkpoint_dir,
        launched_rounds=launched_rounds,
        active_supports=active_supports,
        support_records=support_records,
        warnings=warnings,
        gpu1_active=gpu1_active,
        enabled_attr="run_gpu0_peer_support_provider",
        every_rounds=args.gpu0_peer_support_every_rounds,
        max_concurrent_attr="max_concurrent_gpu0_peer_support",
        should_launch=should_launch_gpu0_peer_support,
        launch_support=launch_gpu0_peer_support,
        checkpoint_parameter="checkpoint",
    )


def harvest_finished_gpu0_peer_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
) -> None:
    harvest_support_records(
        args=args,
        repo_root=repo_root,
        active_supports=active_supports,
        support_records=support_records,
        warnings=warnings,
        output_key="support_output",
        lane="gpu0",
        label="GPU0 peer support",
        correlation_prefix=f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support",
        diagnostic_message="GPU0 peer support provider evidence completed.",
        absorb_report=_absorb_gpu0_support_report,
        status_builder=_gpu0_diagnostic_status,
        diagnostic_details=lambda round_id, process, record: support_diagnostic_details(
            round_id,
            process,
            record,
            output_key="support_output",
        ),
        response_payload=lambda round_id, _process, record: support_response_payload(
            round_id,
            record,
            summary="GPU0 peer support provider evidence completed.",
            output_key="support_output",
            extra_keys=("provider_execution_performed", "provider_work_verified"),
            constants={"direct_tool_execution": False},
        ),
    )


def _absorb_gpu0_support_report(record: dict[str, Any], support_path: Path) -> None:
    if not support_path.exists():
        record["error"] = "gpu0_peer_support_output_missing"
        return
    try:
        data = read_json(support_path)
    except Exception as exc:  # noqa: BLE001
        record["error"] = f"{type(exc).__name__}: {exc}"
        return
    record.update(
        {
            "passed": data.get("passed"),
            "provider_execution_performed": data.get("provider_execution_performed"),
            "provider_work_verified": data.get("provider_work_verified"),
            "provider_backend": data.get("provider_backend"),
            "provider_compute_device": data.get("provider_compute_device"),
            "provider_device_verified": data.get("provider_device_verified"),
            "errors": data.get("errors", []),
            "warnings": data.get("warnings", []),
        }
    )


def _gpu0_diagnostic_status(process: subprocess.Popen[str], record: dict[str, Any]) -> str:
    ready = process.returncode == 0 and (
        record.get("provider_execution_performed") is True
        or record.get("provider_work_verified") is True
    )
    return "ready" if ready else "degraded"
