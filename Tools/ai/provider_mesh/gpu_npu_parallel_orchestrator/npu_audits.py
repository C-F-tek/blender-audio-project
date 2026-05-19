from __future__ import annotations

from .common import *  # noqa: F403
from .broker import run_orchestrator_runtime_tool_broker_packet

def run_npu_runtime_tool_broker_for_audit(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    audit_record: dict[str, Any],
) -> dict[str, Any]:
    tool_requests = (
        audit_record.get("npu_tool_requests")
        if isinstance(audit_record.get("npu_tool_requests"), list)
        else []
    )
    round_id = int(audit_record.get("round") or 0)
    if not getattr(args, "enable_runtime_tool_broker", False):
        return {
            "enabled": False,
            "executed": False,
            "requested_tool_count": len(tool_requests),
            "tool_execution_count": 0,
            "blocked_tool_count": 0,
            "failed_tool_count": 0,
            "tool_results": [],
            "guardrails": {
                "broker_execution_requires_enable_runtime_tool_broker": True,
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }
    if not tool_requests:
        return {
            "enabled": True,
            "executed": False,
            "requested_tool_count": 0,
            "tool_execution_count": 0,
            "blocked_tool_count": 0,
            "failed_tool_count": 0,
            "tool_results": [],
            "guardrails": {
                "patch_application_performed": False,
                "persistent_memory_write_performed": False,
            },
        }

    result = run_orchestrator_runtime_tool_broker_packet(
        args=args,
        repo_root=repo_root,
        tool_requests=tool_requests,
        request_kind="npu_auditor_runtime_tool_requests",
        output_subdir=f"npu_round_{round_id:03d}",
        output_prefix=f"npu_round_{round_id:03d}",
        source="npu_auditor",
    )
    result["round"] = round_id
    result["source_audit"] = audit_record.get("audit_output")
    return result

def build_npu_command(
    args: argparse.Namespace, repo_root: Path, checkpoint: Path, audit_json: Path
) -> list[str]:
    command = [
        resolve_child_python(),
        "-m",
        "Tools.ai",
        "npu_gpu_deep_review_auditor",
        "--repo-root",
        ".",
        "--gpu-review",
        str(checkpoint),
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
        "--max-context-chars",
        str(args.npu_max_context_chars),
        "--max-prompt-chars",
        str(args.npu_max_prompt_chars),
        "--max-new-tokens",
        str(args.npu_max_new_tokens),
    ]
    round_id = checkpoint_round(checkpoint) or 0
    for context_report in collect_runtime_tool_context_reports(args, repo_root, round_id):
        command.extend(["--runtime-tool-context-report", str(context_report)])
    if args.run_npu_auditor_provider:
        command.append("--run-npu")
    else:
        command.extend(["--run-npu", "--metadata-only"])
    if args.npu_python:
        command.extend(["--npu-python", args.npu_python])
    return command

def should_launch_npu_audit(round_id: int, every_rounds: int) -> bool:
    return round_id == 1 or round_id % max(1, every_rounds) == 0

def launch_due_audits(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    launched_rounds: set[int],
    active_audits: dict[int, subprocess.Popen[str]],
    audit_records: list[dict[str, Any]],
) -> None:
    if not getattr(args, "run_npu_auditor_provider", False):
        return
    if len(active_audits) >= args.max_concurrent_npu_audits:
        return
    checkpoints = sorted(
        checkpoint_dir.glob("round_*.json"),
        key=lambda path: checkpoint_round(path) or 0,
    )
    for checkpoint in checkpoints:
        round_id = checkpoint_round(checkpoint)
        if round_id is None or round_id in launched_rounds:
            continue
        effective_every_rounds = effective_npu_auditor_every_rounds(args, audit_records)
        if not should_launch_npu_audit(round_id, effective_every_rounds):
            launched_rounds.add(round_id)
            continue
        if len(active_audits) >= args.max_concurrent_npu_audits:
            return
        audit_json = checkpoint.with_name(f"round_{round_id:03d}_npu_async_audit.json")
        command = build_npu_command(args, repo_root, checkpoint, audit_json)
        process = run_command_async(command, repo_root)
        launched_rounds.add(round_id)
        active_audits[round_id] = process
        audit_records.append(
            {
                "round": round_id,
                "checkpoint": repo_rel(checkpoint, repo_root),
                "audit_output": repo_rel(audit_json, repo_root),
                "started_at": now_iso(),
                "status": "running",
                "command": command,
                "npu_lane_mode_at_launch": npu_lane_diagnostics(args, audit_records).get("mode"),
                "npu_effective_auditor_every_rounds_at_launch": effective_npu_auditor_every_rounds(
                    args, audit_records
                ),
            }
        )

def harvest_finished_audits(
    *,
    repo_root: Path,
    active_audits: dict[int, subprocess.Popen[str]],
    audit_records: list[dict[str, Any]],
) -> None:
    for round_id, process in list(active_audits.items()):
        if process.poll() is None:
            continue
        stdout, stderr = collect_stdout_stderr(process)
        for record in audit_records:
            if record.get("round") == round_id and record.get("status") == "running":
                record["finished_at"] = now_iso()
                record["status"] = "finished"
                record["returncode"] = process.returncode
                record["stdout_tail"] = stdout
                record["stderr_tail"] = stderr
                audit_path = resolve_path(repo_root, record["audit_output"])
                if audit_path.exists():
                    try:
                        data = read_json(audit_path)
                        nested = data.get("npu_auditor", {})
                        record.update(
                            {
                                "classification": nested.get("classification"),
                                "provider_execution_requested": data.get(
                                    "provider_execution_requested",
                                    nested.get("provider_execution_requested"),
                                ),
                                "provider_load_attempted": data.get(
                                    "provider_load_attempted",
                                    nested.get("provider_load_attempted"),
                                ),
                                "provider_execution_succeeded": data.get(
                                    "provider_execution_succeeded",
                                    nested.get("provider_execution_succeeded"),
                                ),
                                "provider_execution_performed": data.get(
                                    "provider_execution_performed",
                                    nested.get("provider_execution_performed"),
                                ),
                                "dependency_missing": data.get(
                                    "dependency_missing",
                                    nested.get("dependency_missing"),
                                ),
                                "warnings": data.get("warnings", []),
                                "runtime_tool_context_seen": data.get("runtime_tool_context_seen"),
                                "runtime_tool_context_report_count": data.get(
                                    "runtime_tool_context_report_count"
                                ),
                                "npu_tool_request_count": data.get("tool_request_count"),
                                "npu_valid_tool_request_count": data.get(
                                    "valid_tool_request_count"
                                ),
                                "npu_invalid_tool_request_count": data.get(
                                    "invalid_tool_request_count"
                                ),
                                "npu_deterministic_tool_fallback_used": data.get(
                                    "npu_deterministic_tool_fallback_used"
                                ),
                                "npu_deterministic_tool_fallback_count": data.get(
                                    "npu_deterministic_tool_fallback_count"
                                ),
                                "npu_tool_requests": data.get("tool_requests", [])[:8],
                                "gpu_review_blocked": data.get("decision", {}).get(
                                    "gpu_review_blocked"
                                ),
                            }
                        )
                    except Exception as exc:  # noqa: BLE001
                        record["parse_error"] = f"{type(exc).__name__}: {exc}"
                break
        del active_audits[round_id]
