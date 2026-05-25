"""Triple provider role coexistence preflight for the heap loop."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.provider_lane_policy import (
    GPU0_LANE,
    NPU_LANE,
    PRIMARY_LANE,
)
from ia_carmine._shared.ollama_provider_selection import provider_model_is_auto
from ia_carmine.runtime.heap_gate.runtime_common import (
    Any,
    Path,
    command_env,
    read_json,
    repo_rel,
    subprocess,
)
from ia_carmine.runtime.heap_gate.provider_lane_launch import write_provider_launch_manifest
from ia_carmine.runtime.heap_gate.provider_runtime_plan import write_provider_runtime_plan
from ia_carmine.runtime.heap_gate.provider_universe_abort import block_provider_universe_run


def enforce_provider_role_coexistence_preflight(
    gate: Any,
    work_dir: Path,
    launch_manifest: Path,
    prepared: list[dict[str, Any]],
    *,
    round_id: int,
    revision: int,
    selected_lanes: set[str],
    time_contract: dict[str, Any],
    reports: list[dict[str, Any]],
) -> bool:
    coexistence = run_provider_role_coexistence_preflight(
        gate,
        work_dir,
        selected_lanes=selected_lanes,
        revision=revision,
    )
    gate.provider_role_coexistence_preflight = coexistence
    gate.provider_boot_gate = coexistence
    write_provider_runtime_plan(
        gate,
        work_dir,
        selected_lanes=selected_lanes,
        stage="provider_roles_alive"
        if coexistence.get("passed")
        else "provider_boot_gate_failed",
        reports=reports,
    )
    reason = provider_role_coexistence_block_reason(coexistence)
    if not reason:
        return True
    block_provider_universe_run(gate, reason, round_id, revision)
    write_provider_launch_manifest(
        gate,
        launch_manifest,
        prepared,
        round_id,
        revision,
        time_contract,
        "provider_boot_gate_failed_before_provider_loop",
    )
    return False


def run_provider_role_coexistence_preflight(
    gate: Any,
    work_dir: Path,
    *,
    selected_lanes: set[str],
    revision: int,
) -> dict[str, Any]:
    required = {PRIMARY_LANE, GPU0_LANE, NPU_LANE}
    suffix = f"_revision{revision}" if revision else ""
    output = work_dir / f"provider_role_coexistence{suffix}.json"
    markdown = work_dir / f"provider_role_coexistence{suffix}.md"
    if not required.issubset(selected_lanes):
        return {
            "kind": "provider_boot_gate",
            "passed": True,
            "skipped": True,
            "reason": "selected_lanes_do_not_require_all_three_provider_roles",
            "selected_lanes": sorted(selected_lanes),
        }
    gpu1_model = _gpu1_model(gate)
    gpu1_ctx = int(getattr(gate, "selected_ollama_num_ctx", 0) or gate.args.ollama_num_ctx)
    gpu1_base_url = _gpu1_base_url(gate)
    gpu0_model = str(getattr(gate.args, "gpu0_model", "") or "").strip()
    gpu0_base_url = str(getattr(gate.args, "gpu0_base_url", "") or "").strip()
    gpu0_vulkan_devices = str(getattr(gate.args, "gpu0_vulkan_visible_devices", "") or "").strip()
    gpu_layers = str(getattr(gate.args, "ollama_gpu_layers", "") or "").strip()
    keep_alive = str(getattr(gate.args, "keep_alive", "") or "").strip()
    npu_model_dir = str(getattr(gate.args, "npu_model_dir", "") or "").strip()
    if not gpu1_base_url or not gpu0_model or not gpu0_base_url or not gpu0_vulkan_devices or not gpu_layers or not keep_alive or not npu_model_dir:
        raise RuntimeError("provider coexistence preflight requires explicit GPU1/GPU0/NPU provider config")
    preflight_max_new_tokens = 4
    npu_hold_seconds = 6
    command = [
        gate.child_python(),
        "-m",
        "ia_carmine",
        "ensure_provider_role_coexistence",
        "--repo-root",
        ".",
        "--python-exe",
        gate.child_python(),
        "--gpu1-model",
        gpu1_model,
        "--gpu1-base-url",
        gpu1_base_url,
        "--gpu0-model",
        gpu0_model,
        "--gpu0-base-url",
        gpu0_base_url,
        "--gpu0-vulkan-visible-devices",
        gpu0_vulkan_devices,
        "--keep-alive",
        keep_alive,
        "--num-ctx",
        str(gpu1_ctx),
        "--ollama-gpu-layers",
        gpu_layers,
        "--max-new-tokens",
        str(preflight_max_new_tokens),
        "--handoff-provider-loop",
        "--npu-hold-seconds",
        str(npu_hold_seconds),
        "--npu-timeout-seconds",
        str(max(60, int(getattr(gate.args, "npu_micro_timeout_seconds", 60)) + 30)),
        "--npu-model-dir",
        npu_model_dir,
        "--output",
        repo_rel(gate.repo_root, output),
        "--markdown-output",
        repo_rel(gate.repo_root, markdown),
    ]
    completed = subprocess.run(
        command,
        cwd=str(gate.repo_root),
        env=command_env(gate.repo_root),
        capture_output=True,
        text=True,
        timeout=max(90, int(getattr(gate.args, "npu_micro_timeout_seconds", 60)) + 60),
        check=False,
    )
    report = read_json(output)
    if not report:
        report = {
            "kind": "provider_role_coexistence",
            "passed": False,
            "errors": [f"coexistence_preflight_returncode_{completed.returncode}"],
        }
    report["preflight_command"] = command
    report["returncode"] = completed.returncode
    report["stdout_tail"] = (completed.stdout or "")[-1200:]
    report["stderr_tail"] = (completed.stderr or "")[-1200:]
    report["output"] = repo_rel(gate.repo_root, output)
    report["markdown_output"] = repo_rel(gate.repo_root, markdown)
    report["derived_config"] = [
        {
            "field": "provider_coexistence_preflight.max_new_tokens",
            "effective_value": preflight_max_new_tokens,
            "source": "fixed_health_probe_budget",
            "reason": "coexistence preflight is health/residency only, not provider product work",
        },
        {
            "field": "provider_coexistence_preflight.npu_hold_seconds",
            "effective_value": npu_hold_seconds,
            "source": "fixed_health_probe_hold",
            "reason": "short NPU hold keeps the three-role boot window observable",
        },
    ]
    return report


def provider_role_coexistence_block_reason(report: dict[str, Any]) -> str:
    if report.get("passed") is True:
        return ""
    if report.get("skipped") is True:
        return ""
    errors = report.get("errors") if isinstance(report.get("errors"), list) else []
    if errors:
        lanes = sorted({_error_lane(str(item)) for item in errors if str(item).strip()})
        lane_text = ",".join(lanes) if lanes else "provider_universe"
        return "provider_boot_gate_failed:" + lane_text + ":" + ",".join(str(item) for item in errors)
    return "provider_boot_gate_failed:provider_universe"


def _error_lane(error: str) -> str:
    if error.startswith("gpu1_") or "gpu1" in error:
        return PRIMARY_LANE
    if error.startswith("gpu0_") or "gpu0" in error:
        return GPU0_LANE
    if error.startswith("npu_") or "npu" in error:
        return NPU_LANE
    return "provider_universe"


def _gpu0_model() -> str:
    raise RuntimeError("gpu0 model must be read from gate args")


def _gpu1_model(gate: Any) -> str:
    requested = str(getattr(gate.args, "provider_model", "") or "").strip()
    if not requested or provider_model_is_auto(requested):
        raise RuntimeError("provider_model_explicit_required")
    selected = str(getattr(gate, "selected_provider_model", "") or "").strip()
    if selected and selected != requested:
        raise RuntimeError(
            "provider_model_selection_mismatch:"
            f"requested={requested}:selected={selected}"
        )
    for report in getattr(gate, "provider_replight_reports", []) or []:
        if not isinstance(report, dict) or str(report.get("lane") or "") != PRIMARY_LANE:
            continue
        report_model = str(
            report.get("selected_provider_model")
            or report.get("selected_model")
            or report.get("provider_model")
            or ""
        ).strip()
        if report_model and report_model != requested:
            raise RuntimeError(
                "provider_model_selection_mismatch:"
                f"requested={requested}:selected={report_model}"
            )
    return requested


def _gpu1_base_url(gate: Any) -> str:
    return str(getattr(gate.args, "gpu1_base_url", "") or "")


def _gpu0_vulkan_devices() -> str:
    raise RuntimeError("gpu0 vulkan device selection must be read from gate args")
