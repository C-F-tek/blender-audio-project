"""Brief GPU1 residency preflight before sidecar lanes start."""

from __future__ import annotations

import time

from ia_carmine._shared.ollama_gpu_residency import (
    gpu_residency_summary,
    ollama_ps_snapshot,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any, Path, read_json


def wait_for_gpu1_residency_preflight(
    gate: Any,
    item: dict[str, Any],
    *,
    max_wait_seconds: float = 30.0,
) -> dict[str, Any]:
    """Poll a running GPU1 lane only until Ollama GPU residency is proven.

    The separate provider replight gate proves live loading/generation before
    this point. This preflight is only the short parallelism handshake for the
    full GPU1 proposal lane, so GPU0/NPU sidecars can start without waiting for
    the full proposal text.
    """

    process = item.get("process")
    started_perf = float(item.get("started_perf") or time.perf_counter())
    output_path = Path(item.get("spec", {}).get("output") or "")
    model = str(
        getattr(gate, "selected_provider_model", "")
        or getattr(gate.args, "provider_model", "")
        or ""
    ).strip()
    full_gpu_requested = str(getattr(gate.args, "ollama_gpu_layers", "") or "all").lower() in {
        "all",
        "-1",
    }
    snapshots: list[dict[str, Any]] = []
    deadline = time.perf_counter() + max(1.0, float(max_wait_seconds))
    last_report: dict[str, Any] = {}
    last_summary: dict[str, Any] = {}
    if item.get("completed") is not None and process is None:
        if output_path:
            last_report = read_json(output_path)
        return _preflight_result(
            _blocked_reason(last_report, {}),
            False,
            started_perf,
            last_report,
            [],
        )

    while True:
        if output_path:
            last_report = read_json(output_path)
            report_model = str(
                last_report.get("selected_provider_model")
                or last_report.get("selected_model")
                or ""
            ).strip()
            if report_model:
                model = report_model
            if bool(last_report.get("provider_device_verified")):
                return _preflight_result(
                    "passed_from_provider_report",
                    True,
                    started_perf,
                    last_report,
                    [],
                )

        snapshot = ollama_ps_snapshot(
            "ollama",
            selected_model=model,
            phase="gpu1_residency_preflight",
            timeout_seconds=2,
        )
        snapshots.append(snapshot)
        last_summary = gpu_residency_summary(
            snapshots,
            full_gpu_requested=full_gpu_requested,
        )
        if bool(last_summary.get("provider_device_verified")):
            return _preflight_result(
                "passed_from_ollama_ps",
                True,
                started_perf,
                last_summary,
                snapshots,
            )
        if process is not None and process.poll() is not None:
            if output_path:
                last_report = read_json(output_path)
            reason = _blocked_reason(last_report, last_summary)
            return _preflight_result(
                reason,
                False,
                started_perf,
                last_report or last_summary,
                snapshots,
            )

        if time.perf_counter() >= deadline:
            reason = _blocked_reason(last_report, last_summary)
            if reason == "gpu1_ollama_gpu_residency_unproven_or_cpu_bound":
                reason = "gpu1_residency_preflight_unproven"
            return _preflight_result(
                reason,
                False,
                started_perf,
                last_report or last_summary,
                snapshots,
            )

        time.sleep(1.0)


def _blocked_reason(report: dict[str, Any], summary: dict[str, Any]) -> str:
    exact = str(
        report.get("product_blocked_reason")
        or summary.get("product_blocked_reason")
        or ""
    ).strip()
    if exact:
        return exact
    device = str(summary.get("provider_compute_device") or report.get("provider_compute_device") or "")
    if device == "ollama/cpu_or_mixed":
        return "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"
    return "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"


def _preflight_result(
    status: str,
    passed: bool,
    started_perf: float,
    evidence: dict[str, Any],
    snapshots: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "kind": "gpu1_residency_preflight",
        "status": status,
        "passed": passed,
        "elapsed_seconds": round(time.perf_counter() - started_perf, 6),
        "provider_device_verified": bool(evidence.get("provider_device_verified")),
        "provider_compute_device": evidence.get("provider_compute_device", ""),
        "ollama_cpu_percent": evidence.get("ollama_cpu_percent"),
        "ollama_gpu_percent": evidence.get("ollama_gpu_percent"),
        "ollama_full_gpu_verified": bool(evidence.get("ollama_full_gpu_verified")),
        "ollama_full_gpu_requested": bool(evidence.get("ollama_full_gpu_requested")),
        "product_blocked_reason": evidence.get("product_blocked_reason", ""),
        "snapshot_count": len(snapshots),
        "snapshots": snapshots[-3:],
    }
