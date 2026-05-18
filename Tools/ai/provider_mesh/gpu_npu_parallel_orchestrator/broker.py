from __future__ import annotations

from .common import *  # noqa: F403

def write_mesh_bootstrap_seed(
    *,
    repo_root: Path,
    checkpoint_dir: Path,
    orchestrator_runtime_tool_bootstrap: dict[str, Any],
) -> Path:
    seed = checkpoint_dir / "orchestrator_mesh_bootstrap_seed.json"
    write_json(
        seed,
        {
            "schema_version": 1,
            "kind": "provider_mesh_bootstrap_seed",
            "generated_at": now_iso(),
            "repo_root": str(repo_root),
            "passed": True,
            "provider_execution_performed": False,
            "round": 0,
            "phase": "mesh_bootstrap",
            "runtime_tool_bootstrap": {
                "executed": orchestrator_runtime_tool_bootstrap.get("executed"),
                "passed": orchestrator_runtime_tool_bootstrap.get("passed"),
                "requested_tool_count": orchestrator_runtime_tool_bootstrap.get(
                    "requested_tool_count"
                ),
                "tool_execution_count": orchestrator_runtime_tool_bootstrap.get(
                    "tool_execution_count"
                ),
                "broker_output": orchestrator_runtime_tool_bootstrap.get("broker_output"),
            },
            "lanes_ready_at_start": {
                "gpu1": True,
                "gpu0": True,
                "npu": True,
                "deterministic_tools": True,
                "runtime_tool_broker": True,
            },
            "guardrails": {
                "report_only": True,
                "provider_seed_not_primary_advisory": True,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "broker_required_for_tool_execution": True,
            },
        },
    )
    return seed

def run_orchestrator_runtime_tool_broker_packet(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    tool_requests: list[dict[str, Any]],
    request_kind: str,
    output_subdir: str,
    output_prefix: str,
    source: str,
) -> dict[str, Any]:
    if not getattr(args, "enable_runtime_tool_broker", False):
        return {
            "enabled": False,
            "executed": False,
            "source": source,
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
            "source": source,
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
    output_root = resolve_path(repo_root, args.runtime_tool_output_dir)
    out_dir = output_root / output_subdir
    out_dir.mkdir(parents=True, exist_ok=True)
    request_file = out_dir / f"{output_prefix}_tool_requests.json"
    broker_output = out_dir / f"{output_prefix}_runtime_tool_broker.json"
    broker_markdown = out_dir / f"{output_prefix}_runtime_tool_broker.md"
    request_packet = {
        "schema_version": 1,
        "kind": request_kind,
        "repo_root": str(repo_root),
        "source": source,
        "tool_requests": tool_requests,
        "guardrails": {
            "free_shell_allowed": False,
            "broker_allowlist_required": True,
            "patch_application_allowed": False,
            "provider_execution_allowed": False,
            "persistent_memory_write_allowed": False,
            "manual_review_required": True,
        },
    }
    write_json(request_file, request_packet)
    command = [
        resolve_child_python(),
        "-m",
        "Tools.ai",
        "agent_runtime_tool_broker",
        "--repo-root",
        ".",
        "--request-file",
        str(request_file),
        "--tool-output-dir",
        str(out_dir),
        "--timeout-seconds",
        str(args.runtime_tool_timeout_seconds),
        "--output",
        str(broker_output),
        "--markdown-output",
        str(broker_markdown),
    ]
    returncode, stdout, stderr, error = run_command_sync(
        command, repo_root, args.runtime_tool_timeout_seconds + 30
    )
    broker_report: dict[str, Any] = {}
    broker_output_exists = broker_output.exists()
    if broker_output_exists:
        try:
            broker_report = read_json(broker_output)
        except Exception as exc:
            error = f"{error} {type(exc).__name__}: {exc}".strip()
    elif not error:
        error = "runtime_tool_broker_output_missing"
    return {
        "enabled": True,
        "executed": True,
        "source": source,
        "requested_tool_count": len(tool_requests),
        "command": command,
        "returncode": returncode,
        "stdout_tail": stdout,
        "stderr_tail": stderr,
        "error": error,
        "request_file": repo_rel(request_file, repo_root),
        "broker_output": repo_rel(broker_output, repo_root),
        "broker_markdown": repo_rel(broker_markdown, repo_root),
        "broker_output_exists": broker_output_exists,
        "passed": broker_report.get("passed"),
        "tool_request_count": broker_report.get("tool_request_count", len(tool_requests)),
        "tool_execution_count": broker_report.get("tool_execution_count", 0),
        "blocked_tool_count": broker_report.get("blocked_tool_count", 0),
        "failed_tool_count": broker_report.get("failed_tool_count", 0),
        "provider_execution_performed": broker_report.get("provider_execution_performed", False),
        "patch_application_performed": broker_report.get("patch_application_performed", False),
        "sqlite_write_performed": broker_report.get("sqlite_write_performed", False),
        "persistent_memory_write_performed": broker_report.get(
            "persistent_memory_write_performed", False
        ),
        "operational_sqlite_write_performed": broker_report.get(
            "operational_sqlite_write_performed", False
        ),
        "tool_results": broker_report.get("tool_results", [])[:8],
        "guardrails": broker_report.get("guardrails", {}),
    }

def run_orchestrator_runtime_tool_bootstrap(
    args: argparse.Namespace, repo_root: Path
) -> dict[str, Any]:
    if not getattr(args, "enable_runtime_tool_broker", False):
        return {
            "enabled": False,
            "executed": False,
            "bootstrap": True,
            "requested_tool_count": 0,
            "tool_results": [],
        }
    if getattr(args, "disable_runtime_tool_bootstrap", False):
        return {
            "enabled": True,
            "executed": False,
            "bootstrap": True,
            "disabled": True,
            "requested_tool_count": 0,
            "tool_results": [],
        }
    result = run_orchestrator_runtime_tool_broker_packet(
        args=args,
        repo_root=repo_root,
        tool_requests=[dict(item) for item in ORCHESTRATOR_RUNTIME_TOOL_BOOTSTRAP_REQUESTS],
        request_kind="orchestrator_runtime_tool_bootstrap_requests",
        output_subdir="round_000",
        output_prefix="round_000",
        source="orchestrator_bootstrap",
    )
    result["bootstrap"] = True
    result["bootstrap_tool_ids"] = [
        str(item["id"]) for item in ORCHESTRATOR_RUNTIME_TOOL_BOOTSTRAP_REQUESTS
    ]
    return result

def collect_gpu_tool_request_entries(
    gpu_report: dict[str, Any], max_requests_per_round: int
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    rounds = gpu_report.get("rounds", [])
    if not isinstance(rounds, list):
        return entries
    for round_item in rounds:
        if not isinstance(round_item, dict):
            continue
        parsed = (
            round_item.get("parsed_response")
            if isinstance(round_item.get("parsed_response"), dict)
            else {}
        )
        raw_requests = (
            parsed.get("tool_requests") if isinstance(parsed.get("tool_requests"), list) else []
        )
        tool_requests: list[dict[str, Any]] = []
        for index, item in enumerate(raw_requests[:max_requests_per_round], start=1):
            if not isinstance(item, dict):
                continue
            request = dict(item)
            request.setdefault(
                "id",
                f"gpu_round_{int(round_item.get('round') or 0):03d}_tool_{index:03d}",
            )
            request.setdefault(
                "reason", "GPU planner requested additional report-only tool evidence."
            )
            request["source"] = "gpu_planner"
            tool_requests.append(request)
        if tool_requests:
            entries.append(
                {
                    "round": int(round_item.get("round") or 0),
                    "tool_requests": tool_requests,
                }
            )
    return entries

def execute_gpu_runtime_tool_requests_from_report(
    *, args: argparse.Namespace, repo_root: Path, gpu_report: dict[str, Any]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for entry in collect_gpu_tool_request_entries(
        gpu_report, args.runtime_tool_max_requests_per_round
    ):
        round_id = int(entry.get("round") or 0)
        broker = run_orchestrator_runtime_tool_broker_packet(
            args=args,
            repo_root=repo_root,
            tool_requests=entry.get("tool_requests", []),
            request_kind="gpu_planner_orchestrated_runtime_tool_requests",
            output_subdir=f"gpu_round_{round_id:03d}",
            output_prefix=f"gpu_round_{round_id:03d}",
            source="gpu_planner",
        )
        broker["round"] = round_id
        results.append(broker)
    return results
