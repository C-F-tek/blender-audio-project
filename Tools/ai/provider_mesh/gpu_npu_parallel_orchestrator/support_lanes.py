from __future__ import annotations

from .common import (
    Any,
    Path,
    argparse,
    append_runtime_heap_event,
    audit_elapsed_seconds,
    checkpoint_round,
    collect_stdout_stderr,
    now_iso,
    record_round_id,
    record_runtime_lane_diagnostic,
    repo_rel,
    resolve_path,
    run_command_async,
    subprocess,
)

SupportLauncher = Any
ReportAbsorber = Any
StatusBuilder = Any
RecordPayloadBuilder = Any
RecordCallback = Any


def support_launch_blocked(
    *,
    args: argparse.Namespace,
    round_id: int,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    enabled_attr: str,
    max_concurrent_attr: str,
) -> bool:
    if not getattr(args, enabled_attr, False):
        return True
    if round_id in active_supports:
        return True
    limit = max(1, int(getattr(args, max_concurrent_attr)))
    if len(active_supports) >= limit:
        return True
    return any(record_round_id(item) == round_id for item in support_records)


def active_support_capacity_reached(
    args: argparse.Namespace,
    active_supports: dict[int, subprocess.Popen[str]],
    max_concurrent_attr: str,
) -> bool:
    return len(active_supports) >= max(1, int(getattr(args, max_concurrent_attr)))


def iter_unlaunched_checkpoints(
    checkpoint_dir: Path,
    launched_rounds: set[int],
) -> list[tuple[Path, int]]:
    checkpoints = sorted(
        checkpoint_dir.glob("round_*.json"),
        key=lambda path: checkpoint_round(path) or 0,
    )
    due: list[tuple[Path, int]] = []
    for checkpoint in checkpoints:
        round_id = checkpoint_round(checkpoint)
        if round_id is not None and round_id not in launched_rounds:
            due.append((checkpoint, round_id))
    return due


def launch_due_checkpoint_supports(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    checkpoint_dir: Path,
    launched_rounds: set[int],
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    gpu1_active: bool,
    enabled_attr: str,
    every_rounds: int,
    max_concurrent_attr: str,
    should_launch: Any,
    launch_support: SupportLauncher,
    checkpoint_parameter: str,
) -> None:
    if not getattr(args, enabled_attr, False):
        return
    for checkpoint, round_id in iter_unlaunched_checkpoints(checkpoint_dir, launched_rounds):
        if not should_launch(round_id, every_rounds):
            launched_rounds.add(round_id)
            continue
        if active_support_capacity_reached(args, active_supports, max_concurrent_attr):
            return
        kwargs = {
            "args": args,
            "repo_root": repo_root,
            "round_id": round_id,
            checkpoint_parameter: checkpoint,
            "active_supports": active_supports,
            "support_records": support_records,
            "warnings": warnings,
            "gpu1_active": gpu1_active,
        }
        if launch_support(**kwargs):
            launched_rounds.add(round_id)


def start_support_process(
    *,
    command: list[str],
    repo_root: Path,
    round_id: int,
    active_supports: dict[int, subprocess.Popen[str]],
) -> subprocess.Popen[str]:
    process = run_command_async(command, repo_root)
    active_supports[round_id] = process
    return process


def launch_support_with_record(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    round_id: int,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    command: list[str],
    record: dict[str, Any],
    lane: str,
    correlation_id: str,
    payload: dict[str, Any],
    diagnostic_message: str,
    diagnostic_details: dict[str, Any],
) -> None:
    start_support_process(
        command=command,
        repo_root=repo_root,
        round_id=round_id,
        active_supports=active_supports,
    )
    support_records.append(record)
    append_support_launch_events(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        lane=lane,
        correlation_id=correlation_id,
        round_id=round_id,
        payload=payload,
        diagnostic_message=diagnostic_message,
        diagnostic_details=diagnostic_details,
    )


def append_support_launch_events(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    lane: str,
    correlation_id: str,
    round_id: int,
    payload: dict[str, Any],
    diagnostic_message: str,
    diagnostic_details: dict[str, Any],
) -> None:
    append_runtime_heap_event(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        source="orchestrator",
        target=lane,
        event_type="evidence_request",
        round_id=round_id,
        correlation_id=correlation_id,
        payload=payload,
    )
    record_runtime_lane_diagnostic(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        lane=lane,
        status="running",
        message=diagnostic_message,
        details=diagnostic_details,
        round_id=round_id,
        correlation_id=f"{correlation_id}:diagnostic",
    )


def finished_support_records(
    *,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    output_key: str,
) -> list[tuple[int, subprocess.Popen[str], dict[str, Any], Path]]:
    finished: list[tuple[int, subprocess.Popen[str], dict[str, Any], Path]] = []
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
        output_path = resolve_path(repo_root, str(record.get(output_key) or ""))
        finished.append((round_id, process, record, output_path))
    return finished


def harvest_support_records(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    active_supports: dict[int, subprocess.Popen[str]],
    support_records: list[dict[str, Any]],
    warnings: list[str],
    output_key: str,
    lane: str,
    label: str,
    correlation_prefix: str,
    diagnostic_message: str,
    absorb_report: ReportAbsorber,
    status_builder: StatusBuilder,
    diagnostic_details: RecordPayloadBuilder,
    response_payload: RecordPayloadBuilder,
    after_record: RecordCallback | None = None,
) -> None:
    for round_id, process, record, output_path in finished_support_records(
        repo_root=repo_root,
        active_supports=active_supports,
        support_records=support_records,
        output_key=output_key,
    ):
        absorb_report(record, output_path)
        if process.returncode not in (None, 0):
            warnings.append(f"{label} round {round_id}: returncode={process.returncode}")
        correlation_id = f"{correlation_prefix}-{round_id:03d}"
        append_support_final_events(
            args=args,
            repo_root=repo_root,
            warnings=warnings,
            lane=lane,
            correlation_id=correlation_id,
            round_id=round_id,
            status=status_builder(process, record),
            diagnostic_message=diagnostic_message,
            diagnostic_details=diagnostic_details(round_id, process, record),
            response_payload=response_payload(round_id, process, record),
        )
        if after_record:
            after_record(round_id, process, record)
        active_supports.pop(round_id, None)


def append_support_final_events(
    *,
    args: argparse.Namespace,
    repo_root: Path,
    warnings: list[str],
    lane: str,
    correlation_id: str,
    round_id: int,
    status: str,
    diagnostic_message: str,
    diagnostic_details: dict[str, Any],
    response_payload: dict[str, Any],
) -> None:
    record_runtime_lane_diagnostic(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        lane=lane,
        status=status,
        message=diagnostic_message,
        details=diagnostic_details,
        round_id=round_id,
        correlation_id=f"{correlation_id}:final-diagnostic",
    )
    append_runtime_heap_event(
        args=args,
        repo_root=repo_root,
        warnings=warnings,
        source=lane,
        target="gpu1",
        event_type="evidence_response",
        round_id=round_id,
        correlation_id=correlation_id,
        payload=response_payload,
    )


def support_diagnostic_details(
    round_id: int,
    process: subprocess.Popen[str],
    record: dict[str, Any],
    *,
    output_key: str,
    extra_keys: tuple[str, ...] = (),
) -> dict[str, Any]:
    details = {
        "round": round_id,
        "returncode": process.returncode,
        "passed": record.get("passed"),
        "output": record.get(output_key),
        "errors": record.get("errors", []),
        "warnings": record.get("warnings", []),
    }
    for key in extra_keys:
        details[key] = record.get(key)
    return details


def support_response_payload(
    round_id: int,
    record: dict[str, Any],
    *,
    summary: str,
    output_key: str,
    extra_keys: tuple[str, ...] = (),
    field_map: dict[str, str] | None = None,
    constants: dict[str, Any] | None = None,
) -> dict[str, Any]:
    payload = {
        "summary": summary,
        "round": round_id,
        "passed": record.get("passed"),
        "output": record.get(output_key),
        "launched_while_gpu1_active": record.get("launched_while_gpu1_active"),
    }
    for key in extra_keys:
        payload[key] = record.get(key)
    for payload_key, record_key in (field_map or {}).items():
        payload[payload_key] = record.get(record_key)
    payload.update(constants or {})
    return payload


def support_repo_rel(path: Path | None, repo_root: Path) -> str:
    return repo_rel(path, repo_root) if path else ""
