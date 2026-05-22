from __future__ import annotations

import json
import re
import subprocess
import threading
import time
from typing import Any

GPU_ENGINE_RE = re.compile(
    r"pid_(?P<pid>\d+).*?phys_(?P<phys>\d+).*?engtype_(?P<engine>[^)\\]+)",
    re.IGNORECASE,
)


class GpuRuntimeSampler:
    def __init__(
        self,
        *,
        interval_seconds: float = 0.5,
        target_pid: int | None = None,
    ) -> None:
        self.interval_seconds = max(0.1, float(interval_seconds))
        self.target_pid = target_pid
        self.samples: list[dict[str, Any]] = []
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def start(self) -> None:
        if self._thread is not None:
            return
        self._thread = threading.Thread(target=self._run, name="gpu-runtime-sampler", daemon=True)
        self._thread.start()

    def stop(self) -> dict[str, Any]:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=2.0)
        return gpu_runtime_summary(self.samples)

    def _run(self) -> None:
        while not self._stop.is_set():
            self.samples.append(self._sample_once())
            self._stop.wait(self.interval_seconds)
        self.samples.append(self._sample_once())

    def _sample_once(self) -> dict[str, Any]:
        sample = sample_nvidia_gpu()
        windows = sample_windows_gpu_engines(self.target_pid)
        sample["windows_gpu_counters_available"] = windows.get("windows_gpu_counters_available")
        sample["windows_gpu_engine_samples"] = windows.get("engine_samples") or []
        sample["windows_gpu_target_engine_samples"] = windows.get("target_engine_samples") or []
        sample["windows_gpu_counter_errors"] = windows.get("errors") or []
        sample["errors"].extend(windows.get("errors") or [])
        return sample


def sample_nvidia_gpu() -> dict[str, Any]:
    sample: dict[str, Any] = {
        "sample_time": time.time(),
        "nvidia_smi_available": False,
        "gpus": [],
        "compute_processes": [],
        "errors": [],
    }
    gpu_query = [
        "nvidia-smi",
        "--query-gpu=timestamp,uuid,name,utilization.gpu,memory.used,power.draw,pstate",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(gpu_query, text=True, capture_output=True, timeout=3, check=False)
    except Exception as exc:  # noqa: BLE001 - telemetry is report evidence.
        sample["errors"].append(f"gpu_query:{type(exc).__name__}: {exc}")
        return sample
    if completed.returncode != 0:
        sample["errors"].append((completed.stderr or completed.stdout or "nvidia-smi failed")[:400])
        return sample
    sample["nvidia_smi_available"] = True
    for line in (completed.stdout or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 7:
            continue
        sample["gpus"].append(
            {
                "timestamp": parts[0],
                "uuid": parts[1],
                "name": parts[2],
                "utilization_gpu_percent": _int_or_none(parts[3]),
                "memory_used_mib": _int_or_none(parts[4]),
                "power_draw_w": _float_or_none(parts[5]),
                "pstate": parts[6],
            }
        )
    sample["compute_processes"] = _compute_processes()
    return sample


def sample_windows_gpu_engines(target_pid: int | None = None) -> dict[str, Any]:
    sample: dict[str, Any] = {
        "sample_time": time.time(),
        "windows_gpu_counters_available": False,
        "target_pid": target_pid,
        "engine_samples": [],
        "target_engine_samples": [],
        "errors": [],
    }
    command = [
        "powershell",
        "-NoProfile",
        "-Command",
        (
            "$ErrorActionPreference='Stop';"
            "Get-Counter '\\GPU Engine(*)\\Utilization Percentage' | "
            "Select-Object -ExpandProperty CounterSamples | "
            "Select-Object Path,CookedValue | ConvertTo-Json -Depth 3"
        ),
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=5, check=False)
    except Exception as exc:  # noqa: BLE001 - telemetry is report evidence.
        sample["errors"].append(f"windows_gpu_counter:{type(exc).__name__}: {exc}")
        return sample
    if completed.returncode != 0:
        sample["errors"].append((completed.stderr or completed.stdout or "Get-Counter failed")[:400])
        return sample
    try:
        payload = json.loads(completed.stdout or "[]")
    except json.JSONDecodeError as exc:
        sample["errors"].append(f"windows_gpu_counter_json:{exc}")
        return sample
    rows = payload if isinstance(payload, list) else [payload]
    for row in rows:
        if not isinstance(row, dict):
            continue
        parsed = _parse_engine_path(str(row.get("Path") or ""))
        value = _float_or_none(row.get("CookedValue"))
        if value is None:
            continue
        parsed["utilization_percent"] = value
        sample["engine_samples"].append(parsed)
        if target_pid and parsed.get("pid") == target_pid:
            sample["target_engine_samples"].append(parsed)
    sample["windows_gpu_counters_available"] = True
    return sample


def gpu_runtime_summary(samples: list[dict[str, Any]]) -> dict[str, Any]:
    gpus = [
        gpu
        for sample in samples
        if isinstance(sample, dict)
        for gpu in sample.get("gpus") or []
        if isinstance(gpu, dict)
    ]
    processes = [
        proc
        for sample in samples
        if isinstance(sample, dict)
        for proc in sample.get("compute_processes") or []
        if isinstance(proc, dict)
    ]
    windows_engine_samples = [
        engine
        for sample in samples
        if isinstance(sample, dict)
        for engine in sample.get("windows_gpu_engine_samples") or []
        if isinstance(engine, dict)
    ]
    windows_target_samples = [
        engine
        for sample in samples
        if isinstance(sample, dict)
        for engine in sample.get("windows_gpu_target_engine_samples") or []
        if isinstance(engine, dict)
    ]
    util_values = [
        int(gpu["utilization_gpu_percent"])
        for gpu in gpus
        if isinstance(gpu.get("utilization_gpu_percent"), int)
    ]
    mem_values = [
        int(gpu["memory_used_mib"])
        for gpu in gpus
        if isinstance(gpu.get("memory_used_mib"), int)
    ]
    process_names = sorted(
        {
            str(proc.get("process_name") or "").strip()
            for proc in processes
            if str(proc.get("process_name") or "").strip()
        }
    )
    gpu_process_observed = any("ollama" in name.lower() for name in process_names) or bool(processes)
    util_peak = max(util_values) if util_values else 0
    mem_peak = max(mem_values) if mem_values else 0
    windows_peak = _peak_util(windows_engine_samples)
    windows_target_peak = _peak_util(windows_target_samples)
    windows_phys0_peak = _peak_util(
        [item for item in windows_engine_samples if str(item.get("phys")) == "0"]
    )
    windows_phys1_peak = _peak_util(
        [item for item in windows_engine_samples if str(item.get("phys")) == "1"]
    )
    return {
        "gpu_runtime_samples": samples[-12:],
        "gpu_runtime_sample_count": len(samples),
        "gpu_utilization_peak_percent": util_peak,
        "gpu_memory_used_peak_mib": mem_peak,
        "gpu_process_observed": gpu_process_observed,
        "gpu_process_names": process_names[:20],
        "windows_gpu_engine_utilization_peak_percent": windows_peak,
        "windows_gpu_engine_phys0_utilization_peak_percent": windows_phys0_peak,
        "windows_gpu_engine_phys1_utilization_peak_percent": windows_phys1_peak,
        "windows_gpu_engine_target_utilization_peak_percent": windows_target_peak,
        "windows_gpu_engine_target_sample_count": len(windows_target_samples),
        "windows_gpu_engine_target_compute_observed": bool(windows_target_peak >= 1.0),
        "windows_gpu_engine_compute_observed": bool(windows_peak >= 1.0),
        "gpu_runtime_sampler_errors": [
            err
            for sample in samples
            if isinstance(sample, dict)
            for err in (sample.get("errors") or [])
        ][:8],
        "gpu_compute_observed": bool(
            gpu_process_observed or util_peak >= 5 or windows_target_peak >= 1.0
        ),
    }


def _compute_processes() -> list[dict[str, Any]]:
    command = [
        "nvidia-smi",
        "--query-compute-apps=pid,process_name,used_memory",
        "--format=csv,noheader,nounits",
    ]
    try:
        completed = subprocess.run(command, text=True, capture_output=True, timeout=3, check=False)
    except Exception:
        return []
    if completed.returncode != 0:
        return []
    processes: list[dict[str, Any]] = []
    for line in (completed.stdout or "").splitlines():
        parts = [part.strip() for part in line.split(",")]
        if len(parts) < 3:
            continue
        processes.append(
            {
                "pid": _int_or_none(parts[0]),
                "process_name": parts[1],
                "used_memory_mib": _int_or_none(parts[2]),
            }
        )
    return processes


def _int_or_none(value: Any) -> int | None:
    try:
        parsed = int(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def _float_or_none(value: Any) -> float | None:
    try:
        parsed = float(str(value).strip())
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def _parse_engine_path(path: str) -> dict[str, Any]:
    match = GPU_ENGINE_RE.search(path)
    if not match:
        return {"path": path, "pid": None, "phys": "", "engine_type": ""}
    return {
        "path": path,
        "pid": _int_or_none(match.group("pid")),
        "phys": match.group("phys"),
        "engine_type": match.group("engine"),
    }


def _peak_util(samples: list[dict[str, Any]]) -> float:
    values = [
        float(item["utilization_percent"])
        for item in samples
        if isinstance(item.get("utilization_percent"), (int, float))
    ]
    return round(max(values), 4) if values else 0.0
