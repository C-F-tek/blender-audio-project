from __future__ import annotations

import re
import os
import subprocess
from pathlib import Path
from typing import Any
from ia_carmine._shared.ollama_server_process import ollama_host_env

CPU_GPU_PERCENT_RE = re.compile(
    r"(?P<cpu>\d+(?:\.\d+)?)%\s*/\s*(?P<gpu>\d+(?:\.\d+)?)%\s*CPU\s*/\s*GPU",
    re.IGNORECASE,
)
GPU_PERCENT_RE = re.compile(r"(?P<gpu>\d+(?:\.\d+)?)%\s*GPU", re.IGNORECASE)
CPU_PERCENT_RE = re.compile(r"(?P<cpu>\d+(?:\.\d+)?)%\s*CPU", re.IGNORECASE)


def ollama_ps_snapshot(
    ollama_exe: str | Path | None,
    selected_model: str,
    phase: str,
    *,
    base_url: str | None = None,
    timeout_seconds: float = 5.0,
) -> dict[str, Any]:
    snapshot: dict[str, Any] = {
        "phase": phase,
        "command_performed": False,
        "model": selected_model,
        "returncode": None,
        "model_line": "",
        "processor": "",
        "ollama_cpu_percent": None,
        "ollama_gpu_percent": None,
        "gpu_present": False,
        "cpu_present": False,
        "gpu_only": False,
        "stdout_tail": "",
        "stderr_tail": "",
        "errors": [],
    }
    if base_url:
        snapshot["base_url"] = base_url
    if not ollama_exe:
        snapshot["errors"].append("ollama executable not resolved")
        return snapshot
    command = [str(ollama_exe), "ps"]
    snapshot["command"] = command
    env = os.environ.copy()
    if base_url:
        env["OLLAMA_HOST"] = ollama_host_env(base_url)
    try:
        completed = subprocess.run(
            command,
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
            env=env,
        )
    except Exception as exc:  # noqa: BLE001 - provider proof must be reported, not raised.
        snapshot["errors"].append(f"ollama ps failed: {type(exc).__name__}: {exc}")
        return snapshot

    stdout = completed.stdout or ""
    stderr = completed.stderr or ""
    line = _find_model_line(stdout, selected_model)
    processor = line or ""
    percent = _parse_processor_percentages(processor)
    upper = processor.upper()
    cpu_percent = percent.get("cpu")
    gpu_percent = percent.get("gpu")
    cpu_present = "CPU" in upper or (cpu_percent is not None and cpu_percent > 0)
    gpu_present = "GPU" in upper or (gpu_percent is not None and gpu_percent > 0)
    gpu_only = bool(gpu_present and not cpu_present)
    if gpu_percent is not None and gpu_percent >= 99.9 and not (cpu_percent and cpu_percent > 0):
        gpu_only = True
    snapshot.update(
        {
            "command_performed": True,
            "returncode": completed.returncode,
            "model_line": line,
            "processor": processor,
            "ollama_cpu_percent": cpu_percent,
            "ollama_gpu_percent": gpu_percent,
            "gpu_present": gpu_present,
            "cpu_present": cpu_present,
            "gpu_only": gpu_only,
            "stdout_tail": stdout[-2000:],
            "stderr_tail": stderr[-1000:],
        }
    )
    if completed.returncode != 0:
        snapshot["errors"].append(f"ollama ps returncode={completed.returncode}")
    if not line:
        snapshot["errors"].append("selected model not visible in ollama ps")
    return snapshot


def gpu_residency_summary(
    snapshots: list[dict[str, Any]],
    *,
    full_gpu_requested: bool = False,
) -> dict[str, Any]:
    usable = [item for item in snapshots if isinstance(item, dict)]
    proof = next((item for item in usable if item.get("phase") == "during" and item.get("gpu_only")), None)
    proof = proof or next((item for item in usable if item.get("gpu_only")), None)
    primary = next((item for item in usable if item.get("phase") == "during"), None) or (
        proof or (usable[-1] if usable else {})
    )
    cpu_percent = _max_percent(usable, "ollama_cpu_percent")
    gpu_percent = _max_percent(usable, "ollama_gpu_percent")
    cpu_present = any(item.get("cpu_present") for item in usable)
    gpu_present = any(item.get("gpu_present") for item in usable)
    cpu_layer_offload_present = bool(cpu_present and gpu_present)
    cpu_only = bool(cpu_present and not gpu_present)
    if proof:
        device = "ollama/gpu"
        status = "gpu_only_verified"
    elif gpu_present:
        device = "ollama/gpu_partial_offload" if cpu_present else "ollama/gpu"
        status = (
            "ollama_gpu_verified_partial_layer_offload"
            if cpu_present
            else "gpu_presence_verified"
        )
    elif cpu_only:
        device = "ollama/cpu_only"
        status = "cpu_only_detected"
    elif gpu_present:
        device = "ollama/gpu_unproven"
        status = "gpu_presence_unverified"
    else:
        device = "ollama/unproven"
        status = "unproven"
    provider_verified = bool(proof) if full_gpu_requested else bool(gpu_present)
    if provider_verified:
        blocked_reason = ""
    elif full_gpu_requested and cpu_layer_offload_present:
        blocked_reason = "gpu1_ollama_full_gpu_residency_required_cpu_gpu_split"
    else:
        blocked_reason = "gpu1_ollama_gpu_residency_unproven_or_cpu_bound"
    return {
        "provider_backend": "ollama",
        "provider_compute_device": device,
        "provider_device_verified": provider_verified,
        "cpu_provider_fallback_performed": bool(cpu_only),
        "ollama_cpu_layer_offload_present": cpu_layer_offload_present,
        "ollama_gpu_accelerated_verified": bool(gpu_present),
        "ollama_cpu_percent": cpu_percent,
        "ollama_gpu_percent": gpu_percent,
        "ollama_full_gpu_requested": bool(full_gpu_requested),
        "ollama_full_gpu_verified": bool(proof),
        "full_gpu_residency_required": bool(full_gpu_requested),
        "full_gpu_residency_verified": bool(proof),
        "ollama_gpu_residency_status": status,
        "ollama_gpu_residency_proof_phase": str(proof.get("phase") if proof else ""),
        "ollama_gpu_residency_model_line": str(primary.get("model_line") or ""),
        "product_blocked_reason": blocked_reason,
    }


def _find_model_line(stdout: str, selected_model: str) -> str:
    selected = str(selected_model or "").strip()
    lines = [line.strip() for line in str(stdout or "").splitlines() if line.strip()]
    if not selected:
        return ""
    for line in lines:
        if line.lower().startswith("name "):
            continue
        if selected in line:
            return " ".join(line.split())
    selected_name = selected.split(":", 1)[0]
    for line in lines:
        if selected_name and selected_name in line:
            return " ".join(line.split())
    return ""


def _parse_processor_percentages(processor: str) -> dict[str, float | None]:
    text = str(processor or "")
    pair = CPU_GPU_PERCENT_RE.search(text)
    if pair:
        return {"cpu": float(pair.group("cpu")), "gpu": float(pair.group("gpu"))}
    gpu = GPU_PERCENT_RE.search(text)
    cpu = CPU_PERCENT_RE.search(text)
    return {
        "cpu": float(cpu.group("cpu")) if cpu else None,
        "gpu": float(gpu.group("gpu")) if gpu else None,
    }


def _max_percent(snapshots: list[dict[str, Any]], key: str) -> float | None:
    values = [item.get(key) for item in snapshots if isinstance(item.get(key), (int, float))]
    return max(values) if values else None
