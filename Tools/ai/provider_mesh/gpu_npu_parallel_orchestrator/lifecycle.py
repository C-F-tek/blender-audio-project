from __future__ import annotations

import argparse
import time
from pathlib import Path

from .broker import (
    execute_gpu_runtime_tool_requests_from_report,
    run_orchestrator_runtime_tool_bootstrap,
    write_mesh_bootstrap_seed,
)
from .common import (
    append_runtime_heap_event,
    collect_stdout_stderr,
    now_iso,
    read_json,
    record_round_id,
    repo_rel,
    resolve_path,
    run_command_async,
    terminate_process,
    write_runtime_heap_snapshot,
)
from .gpu_lanes import (
    build_gpu_command,
    harvest_finished_gpu0_peer_supports,
    launch_due_gpu0_peer_supports,
    launch_gpu0_peer_support,
)
from .npu_audits import (
    harvest_finished_audits,
    launch_due_audits,
    run_npu_runtime_tool_broker_for_audit,
)
from .npu_micro import (
    execute_npu_micro_runtime_tool_broker,
    harvest_finished_npu_micro_supports,
    launch_due_npu_micro_supports,
    launch_npu_micro_support,
)
from .state import OrchestratorRunState


def start_orchestrator_state(args: argparse.Namespace) -> OrchestratorRunState:
    repo_root = Path(args.repo_root).resolve()
    start = time.perf_counter()
    checkpoint_dir = resolve_path(repo_root, args.checkpoint_dir)
    gpu_output = resolve_path(repo_root, args.gpu_output)
    gpu_markdown = resolve_path(repo_root, args.gpu_markdown_output)
    checkpoint_dir.mkdir(parents=True, exist_ok=True)
    bootstrap = run_orchestrator_runtime_tool_bootstrap(args, repo_root)
    args.orchestrator_runtime_tool_bootstrap_result = bootstrap
    mesh_seed = write_mesh_bootstrap_seed(
        repo_root=repo_root,
        checkpoint_dir=checkpoint_dir,
        orchestrator_runtime_tool_bootstrap=bootstrap,
    )
    gpu_command = build_gpu_command(args, repo_root, checkpoint_dir, gpu_output, gpu_markdown)
    gpu_process = run_command_async(gpu_command, repo_root)
    return OrchestratorRunState(
        args=args,
        repo_root=repo_root,
        start=start,
        checkpoint_dir=checkpoint_dir,
        gpu_output=gpu_output,
        gpu_markdown=gpu_markdown,
        orchestrator_runtime_tool_bootstrap=bootstrap,
        mesh_bootstrap_seed=mesh_seed,
        gpu_command=gpu_command,
        gpu_process=gpu_process,
    )


def launch_startup_support_lanes(state: OrchestratorRunState) -> None:
    args = state.args
    append_runtime_heap_event(
        args=args,
        repo_root=state.repo_root,
        warnings=state.warnings,
        source="orchestrator",
        event_type="provider_state",
        payload={
            "state": "mesh_bootstrap_started",
            "gpu1_process_started": True,
            "gpu0_peer_support_enabled": bool(getattr(args, "run_gpu0_peer_support_provider", False)),
            "npu_micro_support_enabled": bool(getattr(args, "run_npu_micro_support_provider", False)),
            "legacy_npu_auditor_provider_requested": bool(getattr(args, "run_npu_auditor_provider", False)),
            "lanes_ready_at_start": ["gpu1", "gpu0", "npu", "deterministic", "broker"],
        },
    )
    launch_gpu0_peer_support(
        args=args,
        repo_root=state.repo_root,
        round_id=0,
        checkpoint=state.mesh_bootstrap_seed,
        active_supports=state.active_gpu0_supports,
        support_records=state.gpu0_support_records,
        warnings=state.warnings,
        gpu1_active=True,
    )
    write_runtime_heap_snapshot(args=args, repo_root=state.repo_root, warnings=state.warnings)
    launch_npu_micro_support(
        args=args,
        repo_root=state.repo_root,
        round_id=0,
        source_report=state.mesh_bootstrap_seed,
        active_supports=state.active_npu_micro_supports,
        support_records=state.npu_micro_support_records,
        warnings=state.warnings,
        gpu1_active=True,
    )


def poll_until_gpu_finishes(state: OrchestratorRunState) -> None:
    args = state.args
    try:
        while state.gpu_process.poll() is None:
            launch_due_gpu0_peer_supports(
                args=args,
                repo_root=state.repo_root,
                checkpoint_dir=state.checkpoint_dir,
                launched_rounds=state.launched_gpu0_support_rounds,
                active_supports=state.active_gpu0_supports,
                support_records=state.gpu0_support_records,
                warnings=state.warnings,
                gpu1_active=True,
            )
            launch_due_npu_micro_supports(
                args=args,
                repo_root=state.repo_root,
                checkpoint_dir=state.checkpoint_dir,
                launched_rounds=state.launched_npu_micro_rounds,
                active_supports=state.active_npu_micro_supports,
                support_records=state.npu_micro_support_records,
                warnings=state.warnings,
                gpu1_active=True,
            )
            launch_due_audits(
                args=args,
                repo_root=state.repo_root,
                checkpoint_dir=state.checkpoint_dir,
                launched_rounds=state.launched_rounds,
                active_audits=state.active_audits,
                audit_records=state.audit_records,
            )
            harvest_active_support_lanes(state, gpu1_active=True)
            time.sleep(args.poll_seconds)
    except KeyboardInterrupt:
        state.warnings.append(
            "KeyboardInterrupt received; terminating GPU process and active provider peer support lanes"
        )
        terminate_process(state.gpu_process)
        for process in state.active_gpu0_supports.values():
            terminate_process(process)
        for process in state.active_npu_micro_supports.values():
            terminate_process(process)
        for process in state.active_audits.values():
            terminate_process(process)


def harvest_active_support_lanes(state: OrchestratorRunState, *, gpu1_active: bool) -> None:
    harvest_finished_gpu0_peer_supports(
        args=state.args,
        repo_root=state.repo_root,
        active_supports=state.active_gpu0_supports,
        support_records=state.gpu0_support_records,
        warnings=state.warnings,
    )
    harvest_finished_npu_micro_supports(
        args=state.args,
        repo_root=state.repo_root,
        active_supports=state.active_npu_micro_supports,
        support_records=state.npu_micro_support_records,
        warnings=state.warnings,
        gpu1_active=gpu1_active,
    )
    harvest_finished_audits(
        repo_root=state.repo_root,
        active_audits=state.active_audits,
        audit_records=state.audit_records,
    )


def close_support_lanes(state: OrchestratorRunState) -> None:
    args = state.args
    state.gpu_stdout, state.gpu_stderr = collect_stdout_stderr(state.gpu_process)
    launch_due_gpu0_peer_supports(
        args=args,
        repo_root=state.repo_root,
        checkpoint_dir=state.checkpoint_dir,
        launched_rounds=state.launched_gpu0_support_rounds,
        active_supports=state.active_gpu0_supports,
        support_records=state.gpu0_support_records,
        warnings=state.warnings,
        gpu1_active=False,
    )
    launch_due_npu_micro_supports(
        args=args,
        repo_root=state.repo_root,
        checkpoint_dir=state.checkpoint_dir,
        launched_rounds=state.launched_npu_micro_rounds,
        active_supports=state.active_npu_micro_supports,
        support_records=state.npu_micro_support_records,
        warnings=state.warnings,
        gpu1_active=False,
    )
    launch_due_audits(
        args=args,
        repo_root=state.repo_root,
        checkpoint_dir=state.checkpoint_dir,
        launched_rounds=state.launched_rounds,
        active_audits=state.active_audits,
        audit_records=state.audit_records,
    )
    wait_for_close_barrier(state)
    terminated_gpu0, terminated_npu_micro, terminated_audits = terminate_remaining_lanes(state)
    harvest_active_support_lanes(state, gpu1_active=False)
    mark_terminated_records(state.gpu0_support_records, terminated_gpu0)
    mark_terminated_records(state.npu_micro_support_records, terminated_npu_micro)
    mark_terminated_records(state.audit_records, terminated_audits)
    mark_uncollected_processes(state)


def wait_for_close_barrier(state: OrchestratorRunState) -> None:
    args = state.args
    close_deadline = time.perf_counter() + max(
        0,
        args.npu_final_wait_seconds,
        args.npu_micro_support_final_wait_seconds,
        args.gpu0_peer_support_final_wait_seconds,
    )
    while (
        state.active_gpu0_supports or state.active_npu_micro_supports or state.active_audits
    ) and time.perf_counter() < close_deadline:
        harvest_active_support_lanes(state, gpu1_active=False)
        time.sleep(args.poll_seconds)


def terminate_remaining_lanes(state: OrchestratorRunState) -> tuple[set[int], set[int], set[int]]:
    terminated_gpu0: set[int] = set()
    terminated_npu_micro: set[int] = set()
    terminated_audits: set[int] = set()
    for round_id, process in list(state.active_gpu0_supports.items()):
        terminate_process(process)
        terminated_gpu0.add(round_id)
        state.warnings.append(f"GPU0 peer support round {round_id} terminated after close barrier budget")
    for round_id, process in list(state.active_npu_micro_supports.items()):
        terminate_process(process)
        terminated_npu_micro.add(round_id)
        state.warnings.append(f"NPU micro support round {round_id} terminated after close barrier budget")
    for round_id, process in list(state.active_audits.items()):
        terminate_process(process)
        terminated_audits.add(round_id)
        state.warnings.append(f"NPU audit round {round_id} terminated after final wait budget")
    return terminated_gpu0, terminated_npu_micro, terminated_audits


def mark_terminated_records(records: list[dict[str, object]], terminated_rounds: set[int]) -> None:
    for record in records:
        if record_round_id(record) in terminated_rounds:
            record["status"] = "terminated"
            record["terminated_after_close_barrier"] = True


def mark_uncollected_processes(state: OrchestratorRunState) -> None:
    mark_uncollected_group(
        state.active_gpu0_supports,
        state.gpu0_support_records,
        "gpu0_peer_support_process_still_active_after_close_barrier_termination",
    )
    mark_uncollected_group(
        state.active_npu_micro_supports,
        state.npu_micro_support_records,
        "npu_micro_support_process_still_active_after_close_barrier_termination",
    )
    mark_uncollected_group(
        state.active_audits,
        state.audit_records,
        "npu_audit_process_still_active_after_close_barrier_termination",
    )


def mark_uncollected_group(active: dict[int, object], records: list[dict[str, object]], error: str) -> None:
    for round_id, process in list(active.items()):
        record = next((item for item in records if record_round_id(item) == round_id), None)
        if record is not None:
            record.update(
                {
                    "finished_at": now_iso(),
                    "status": "terminated_uncollected",
                    "returncode": process.returncode,
                    "terminated_after_close_barrier": True,
                    "error": error,
                }
            )
        active.pop(round_id, None)


def load_gpu_report(state: OrchestratorRunState) -> None:
    if state.gpu_output.exists():
        try:
            state.gpu_report = read_json(state.gpu_output)
        except Exception as exc:  # noqa: BLE001
            state.errors.append(f"unable to parse GPU report: {type(exc).__name__}: {exc}")
    else:
        state.errors.append(f"GPU output missing: {repo_rel(state.gpu_output, state.repo_root)}")


def execute_post_gpu_runtime_brokers(state: OrchestratorRunState) -> None:
    for audit in state.audit_records:
        if audit.get("npu_tool_requests") and not audit.get("npu_runtime_tool_broker"):
            audit["npu_runtime_tool_broker"] = run_npu_runtime_tool_broker_for_audit(
                args=state.args,
                repo_root=state.repo_root,
                audit_record=audit,
            )
            broker = audit["npu_runtime_tool_broker"]
            if broker.get("error"):
                state.warnings.append(
                    f"NPU runtime tool broker round {audit.get('round')}: {broker.get('error')}"
                )
            if broker.get("returncode") not in (None, 0):
                state.warnings.append(
                    f"NPU runtime tool broker round {audit.get('round')}: returncode={broker.get('returncode')}"
                )
    for micro in state.npu_micro_support_records:
        execute_npu_micro_runtime_tool_broker(
            args=state.args,
            repo_root=state.repo_root,
            micro=micro,
            warnings=state.warnings,
            gpu1_active=False,
        )
    state.gpu_runtime_tool_brokers = (
        execute_gpu_runtime_tool_requests_from_report(
            args=state.args,
            repo_root=state.repo_root,
            gpu_report=state.gpu_report,
        )
        if getattr(state.args, "enable_runtime_tool_broker", False)
        else []
    )
    for broker in state.gpu_runtime_tool_brokers:
        if broker.get("error"):
            state.warnings.append(
                f"GPU runtime tool broker round {broker.get('round')}: {broker.get('error')}"
            )
        if broker.get("returncode") not in (None, 0):
            state.warnings.append(
                f"GPU runtime tool broker round {broker.get('round')}: returncode={broker.get('returncode')}"
            )
