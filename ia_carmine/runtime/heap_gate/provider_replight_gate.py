"""Hard provider replight gate before full provider teamwork."""

from __future__ import annotations

from ia_carmine._shared.provider_replight import provider_replight_failure_reason
from ia_carmine.runtime.heap_gate.provider_command_specs import build_provider_command_specs
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    command_env,
    read_json,
    repo_rel,
    subprocess,
    write_json_report,
)


REQUIRED_REPLIGHT_LANES = ("gpu1_planner", "gpu0_peer", "npu_micro_task_auditor")


def run_provider_replight_gate(
    gate: Any,
    work_dir: Path,
    *,
    round_id: int,
    revision: int,
    selected_lanes: set[str] | None,
) -> str:
    """Run short live-provider checks and return a blocking reason if any fail."""

    lanes = tuple(lane for lane in REQUIRED_REPLIGHT_LANES if selected_lanes is None or lane in selected_lanes)
    if not lanes:
        return ""
    previous = list(getattr(gate, "provider_replight_reports", []) or [])
    if previous and all(
        any(
            (report.get("provider_id") or report.get("lane")) == lane
            and report.get("replight_passed") is True
            for report in previous
        )
        for lane in lanes
    ):
        return ""
    specs = {
        str(spec.get("lane")): _replight_spec(gate, spec, work_dir, revision)
        for spec in build_provider_command_specs(
            gate,
            work_dir,
            revision=revision,
            selected_lanes=set(lanes),
        )
    }
    reports: list[dict[str, Any]] = []
    gpu1 = specs.get("gpu1_planner")
    if gpu1:
        gpu1_report = _run_spec(gate, gpu1)
        reports.append(gpu1_report)
        _remember_selected_gpu1(gate, gpu1_report)
        reason = provider_replight_failure_reason(reports)
        gate.provider_replight_reports = reports
        if reason:
            return reason

    sidecars = [specs[lane] for lane in lanes if lane != "gpu1_planner" and lane in specs]
    reports.extend(_run_specs_parallel(gate, sidecars))
    gate.provider_replight_reports = reports
    missing = [lane for lane in lanes if lane not in {str(item.get("provider_id") or item.get("lane")) for item in reports}]
    if missing:
        return f"provider_replight_failed:{missing[0]}:missing_provider_report"
    return provider_replight_failure_reason(reports)


def _remember_selected_gpu1(gate: Any, report: dict[str, Any]) -> None:
    selected = str(
        report.get("selected_provider_model") or report.get("selected_model") or ""
    ).strip()
    if selected:
        gate.selected_provider_model = selected
    try:
        ctx = int(report.get("selected_ollama_num_ctx") or report.get("num_ctx") or 0)
    except (TypeError, ValueError):
        ctx = 0
    if ctx > 0:
        gate.selected_ollama_num_ctx = ctx


def _replight_spec(gate: Any, spec: dict[str, Any], work_dir: Path, revision: int) -> dict[str, Any]:
    lane = str(spec.get("lane"))
    suffix = f"_revision{revision}" if revision else ""
    output = work_dir / f"{lane}_provider_replight{suffix}.json"
    command = list(spec.get("command") or [])
    _replace_arg(command, "--output", repo_rel(gate.repo_root, output))
    if "--markdown-output" in command:
        md_output = work_dir / f"{lane}_provider_replight{suffix}.md"
        _replace_arg(command, "--markdown-output", repo_rel(gate.repo_root, md_output))
    if lane == "gpu1_planner":
        _insert_after(command, "--run-ollama", "--replight-mode")
        _replace_arg(command, "--prompt", _gpu1_replight_prompt(gate))
        _replace_arg(command, "--max-new-tokens", "64")
    result = dict(spec)
    result["output"] = output
    result["command"] = command
    result["replight_timeout_seconds"] = _timeout_for(spec)
    return result


def _run_specs_parallel(gate: Any, specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    running: list[tuple[dict[str, Any], subprocess.Popen[str]]] = []
    reports: list[dict[str, Any]] = []
    for spec in specs:
        try:
            process = subprocess.Popen(
                list(spec.get("command") or []),
                cwd=str(gate.repo_root),
                env=command_env(gate.repo_root),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            running.append((spec, process))
        except Exception as exc:  # noqa: BLE001 - report provider launch failure.
            reports.append(
                _write_failure_report(
                    spec,
                    f"provider_replight_failed:{spec.get('lane')}:launch_error:{type(exc).__name__}",
                    returncode=127,
                )
            )
    for spec, process in running:
        timeout = float(spec.get("replight_timeout_seconds") or 60)
        try:
            stdout, stderr = process.communicate(timeout=timeout)
            completed = subprocess.CompletedProcess(
                list(spec.get("command") or []), process.returncode, stdout or "", stderr or ""
            )
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            completed = subprocess.CompletedProcess(
                list(spec.get("command") or []),
                124,
                stdout or "",
                (stderr or "") + "\nprovider replight timeout",
            )
        reports.append(_report_for_completed(spec, completed))
    return reports


def _run_spec(gate: Any, spec: dict[str, Any]) -> dict[str, Any]:
    try:
        completed = subprocess.run(
            list(spec.get("command") or []),
            cwd=str(gate.repo_root),
            env=command_env(gate.repo_root),
            capture_output=True,
            text=True,
            timeout=float(spec.get("replight_timeout_seconds") or 60),
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        completed = subprocess.CompletedProcess(
            list(spec.get("command") or []),
            124,
            exc.stdout or "",
            (exc.stderr or "") + "\nprovider replight timeout",
        )
    return _report_for_completed(spec, completed)


def _report_for_completed(
    spec: dict[str, Any],
    completed: subprocess.CompletedProcess[str],
) -> dict[str, Any]:
    output = Path(spec.get("output") or "")
    report = read_json(output) if output else {}
    if not isinstance(report, dict) or not report:
        reason = f"provider_replight_failed:{spec.get('lane')}:process_returncode_{completed.returncode}"
        report = _write_failure_report(spec, reason, completed.returncode)
    report = extract_lane_report(report, str(spec.get("lane") or ""))
    report.setdefault("returncode", completed.returncode)
    report.setdefault("lane", spec.get("lane"))
    report.setdefault("provider_id", spec.get("lane"))
    report.setdefault("provider_role", spec.get("role"))
    report.setdefault("provider_backend", spec.get("provider_backend"))
    report.setdefault("provider_compute_device", spec.get("provider_compute_device"))
    report.setdefault("provider_replight_required", True)
    if report.get("replight_passed") is not True:
        report.setdefault(
            "replight_blocked_reason",
            f"provider_replight_failed:{spec.get('lane')}:"
            + (f"process_returncode_{completed.returncode}" if completed.returncode else "incomplete_replight"),
        )
    elif completed.returncode != 0:
        report["replight_passed"] = False
        report["replight_blocked_reason"] = (
            f"provider_replight_failed:{spec.get('lane')}:process_returncode_{completed.returncode}"
        )
    return report


def extract_lane_report(report: dict[str, Any], expected_lane: str) -> dict[str, Any]:
    """Return the actual provider lane report from wrappers like local_provider_probe."""

    if not isinstance(report, dict):
        return {}
    if (report.get("provider_id") or report.get("lane")) == expected_lane:
        return report
    lane_reports = report.get("lane_reports")
    if not isinstance(lane_reports, list):
        if str(report.get("kind") or "") == "local_provider_probe":
            reason = f"provider_replight_failed:{expected_lane}:missing_lane_report"
            return {**report, "provider_id": expected_lane, "lane": expected_lane, "replight_passed": False, "replight_blocked_reason": reason}
        return report
    for item in lane_reports:
        if not isinstance(item, dict):
            continue
        if _lane_matches(item, expected_lane):
            lane_report = dict(item)
            lane_report.setdefault("provider_id", expected_lane)
            return lane_report
    reason = f"provider_replight_failed:{expected_lane}:missing_lane_report"
    return {"provider_id": expected_lane, "lane": expected_lane, "replight_passed": False, "replight_blocked_reason": reason}


def _lane_matches(item: dict[str, Any], expected_lane: str) -> bool:
    provider_id = str(item.get("provider_id") or "").strip()
    lane = str(item.get("lane") or "").strip()
    if provider_id == expected_lane or lane == expected_lane:
        return True
    aliases = {
        "gpu1_planner": {"ollama"},
        "gpu0_peer": {"gpu0", "GPU.0", "ollama_gpu0", "ollama/gpu0-vulkan"},
        "npu_micro_task_auditor": {"npu", "openvino_npu"},
    }
    return lane in aliases.get(expected_lane, set())


def _write_failure_report(
    spec: dict[str, Any],
    reason: str,
    returncode: int,
) -> dict[str, Any]:
    report = {
        "lane": spec.get("lane"),
        "provider_id": spec.get("lane"),
        "provider_role": spec.get("role"),
        "provider_backend": spec.get("provider_backend"),
        "provider_compute_device": spec.get("provider_compute_device"),
        "provider_replight_required": True,
        "provider_loaded": False,
        "generated_phrase": "",
        "prompt_token_count": 0,
        "completion_token_count": 0,
        "tokens_per_second": None,
        "native_tool_calling_supported": False,
        "broker_tools_available_count": 0,
        "available_tool_names": [],
        "functionalities": [],
        "replight_passed": False,
        "replight_blocked_reason": reason,
        "product_blocked_reason": reason,
        "passed": False,
        "status": "failed",
        "returncode": returncode,
    }
    output = Path(spec.get("output") or "")
    if output:
        write_json_report(report, output)
    return report


def _gpu1_replight_prompt(gate: Any) -> str:
    return (
        "REPLIGHT provider vivo. Rispondi con una sola frase operativa in italiano "
        "che dica che GPU1/Ollama e' caricato, indica che puoi pianificare/sintetizzare "
        "e che puoi usare il broker/tool catalog quando richiesto. Non produrre patch."
    )


def _replace_arg(command: list[str], flag: str, value: str) -> None:
    if flag not in command:
        command.extend([flag, value])
        return
    index = command.index(flag)
    if index + 1 < len(command):
        command[index + 1] = value
    else:
        command.append(value)


def _insert_after(command: list[str], anchor: str, value: str) -> None:
    if value in command:
        return
    if anchor not in command:
        command.append(value)
        return
    command.insert(command.index(anchor) + 1, value)


def _timeout_for(spec: dict[str, Any]) -> float:
    lane = str(spec.get("lane") or "")
    if lane == "gpu1_planner":
        return min(90.0, max(30.0, float(spec.get("watchdog_timeout_seconds") or 60)))
    return min(75.0, max(20.0, float(spec.get("watchdog_timeout_seconds") or 60)))
