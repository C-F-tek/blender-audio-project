from __future__ import annotations

from .common import *  # noqa: F403

def build_gpu_command(
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    gpu_output: Path,
    gpu_markdown: Path,
) -> list[str]:
    command = [
        resolve_child_python(),
        "Tools/ai/gpu_deep_planning_supervised/cli.py",
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
    if not getattr(args, "run_gpu0_peer_support_provider", False):
        return False
    if round_id in active_supports:
        return False
    if len(active_supports) >= max(1, args.max_concurrent_gpu0_peer_support):
        return False
    if any(record_round_id(item) == round_id for item in support_records):
        return False

    support_json = gpu0_peer_support_output_path(args, repo_root, round_id)
    command = build_gpu0_peer_support_command(args, support_json, round_id)
    process = run_command_async(command, repo_root)
    active_supports[round_id] = process
    checkpoint_rel = repo_rel(checkpoint, repo_root) if checkpoint else ""
    support_records.append(
        {
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
        }
    )
    append_runtime_heap_event(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        source="orchestrator",
        target="gpu0",
        event_type="evidence_request",
        round_id=round_id,
        correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support-{round_id:03d}",
        payload={
            "summary": "GPU0 peer support launched while GPU1 primary advisory continues.",
            "round": round_id,
            "checkpoint": checkpoint_rel,
            "output": repo_rel(support_json, repo_root),
            "gpu1_active": bool(gpu1_active),
            "direct_tool_execution": False,
            "provider_lane": "OpenVINO GPU.0",
        },
    )
    record_runtime_lane_diagnostic(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        lane="gpu0",
        status="running",
        message="GPU0 peer support subprocess launched.",
        details={
            "round": round_id,
            "output": repo_rel(support_json, repo_root),
            "gpu1_active": bool(gpu1_active),
        },
        round_id=round_id,
        correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support-{round_id:03d}:diagnostic",
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
    if not getattr(args, "run_gpu0_peer_support_provider", False):
        return
    checkpoints = sorted(
        checkpoint_dir.glob("round_*.json"),
        key=lambda path: checkpoint_round(path) or 0,
    )
    for checkpoint in checkpoints:
        round_id = checkpoint_round(checkpoint)
        if round_id is None or round_id in launched_rounds:
            continue
        if not should_launch_gpu0_peer_support(round_id, args.gpu0_peer_support_every_rounds):
            launched_rounds.add(round_id)
            continue
        if len(active_supports) >= max(1, args.max_concurrent_gpu0_peer_support):
            return
        if launch_gpu0_peer_support(
            args=args,
            repo_root=repo_root,
            round_id=round_id,
            checkpoint=checkpoint,
            active_supports=active_supports,
            support_records=support_records,
            warnings=warnings,
            gpu1_active=gpu1_active,
        ):
            launched_rounds.add(round_id)

def harvest_finished_gpu0_peer_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
) -> None:
    for round_id, process in list(active_supports.items()):
        if process.poll() is None:
            continue
        stdout, stderr = collect_stdout_stderr(process)
        record = next(
            (item for item in support_records if record_round_id(item) == round_id),
            None,
        )
        if record is None:
            active_supports.pop(round_id, None)
            continue
        record.update(
            {
                "finished_at": now_iso(),
                "status": "finished",
                "returncode": process.returncode,
                "stdout_tail": stdout,
                "stderr_tail": stderr,
            }
        )
        record["elapsed_seconds"] = audit_elapsed_seconds(record)
        support_path = resolve_path(repo_root, str(record.get("support_output") or ""))
        if support_path.exists():
            try:
                data = read_json(support_path)
                record.update(
                    {
                        "passed": data.get("passed"),
                        "openvino_gpu0_visible": data.get("openvino_gpu0_visible"),
                        "openvino_gpu0_workload_performed": data.get(
                            "openvino_gpu0_workload_performed"
                        ),
                        "openvino_gpu0_workload_passed": data.get("openvino_gpu0_workload_passed"),
                        "provider_execution_performed": data.get("provider_execution_performed"),
                        "openvino_gpu0_provider_execution_performed": data.get(
                            "openvino_gpu0_provider_execution_performed"
                        ),
                        "selected_device": data.get("selected_device"),
                        "available_devices": data.get("available_devices"),
                        "errors": data.get("errors", []),
                        "warnings": data.get("warnings", []),
                    }
                )
            except Exception as exc:  # noqa: BLE001
                record["error"] = f"{type(exc).__name__}: {exc}"
        else:
            record["error"] = "gpu0_peer_support_output_missing"
        if process.returncode not in (None, 0):
            warnings.append(f"GPU0 peer support round {round_id}: returncode={process.returncode}")
        diagnostic_status = (
            "ready"
            if process.returncode == 0
            and (
                record.get("provider_execution_performed") is True
                or record.get("openvino_gpu0_provider_execution_performed") is True
                or record.get("openvino_gpu0_workload_passed") is True
            )
            else "degraded"
        )
        record_runtime_lane_diagnostic(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            lane="gpu0",
            status=diagnostic_status,
            message="GPU0 peer support provider evidence completed.",
            details={
                "round": round_id,
                "returncode": process.returncode,
                "passed": record.get("passed"),
                "output": record.get("support_output"),
                "errors": record.get("errors", []),
                "warnings": record.get("warnings", []),
            },
            round_id=round_id,
            correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support-{round_id:03d}:final-diagnostic",
        )
        append_runtime_heap_event(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            source="gpu0",
            target="gpu1",
            event_type="evidence_response",
            round_id=round_id,
            correlation_id=f"{getattr(args, 'runtime_heap_stamp', '')}:gpu0-peer-support-{round_id:03d}",
            payload={
                "summary": "GPU0 peer support provider evidence completed.",
                "round": round_id,
                "passed": record.get("passed"),
                "provider_execution_performed": record.get("provider_execution_performed"),
                "openvino_gpu0_workload_passed": record.get("openvino_gpu0_workload_passed"),
                "output": record.get("support_output"),
                "launched_while_gpu1_active": record.get("launched_while_gpu1_active"),
                "direct_tool_execution": False,
            },
        )
        active_supports.pop(round_id, None)
