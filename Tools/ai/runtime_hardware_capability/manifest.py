from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai.runtime_hardware_capability.probes import (
    cpu_diagnostics,
    detect_openvino_devices,
    nvidia_smi_diagnostics,
)

SAFE_SIDE_EFFECTS = ["read_only", "report_only"]


def capability_entry(
    *,
    name: str,
    resource: str,
    role: str,
    status: str,
    provider: str,
    diagnostics: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one normalized capability entry."""
    return {
        "name": name,
        "resource": resource,
        "role": role,
        "provider": provider,
        "status": status,
        "allowed_side_effects": SAFE_SIDE_EFFECTS,
        "source_writes_allowed": False,
        "patch_application_allowed": False,
        "persistent_memory_write_allowed": False,
        "media_runtime_allowed": False,
        "network_or_secret_access_allowed": False,
        "timeout_seconds_default": 120,
        "diagnostics": diagnostics or {},
    }


def build_manifest(repo_root: Path) -> dict[str, Any]:
    """Build a hardware capability manifest from safe local detection."""
    openvino = detect_openvino_devices()
    openvino_devices = set(openvino.get("devices") or [])
    nvidia = nvidia_smi_diagnostics()

    capabilities = [
        capability_entry(
            name="cpu_deterministic_tools",
            resource="CPU",
            role="validators_inventory_reporting",
            status="available",
            provider="python_stdlib",
            diagnostics=cpu_diagnostics(),
        ),
        capability_entry(
            name="openvino_gpu0_report_only",
            resource="GPU.0",
            role="openvino_coworker_report_only",
            status="available" if "GPU.0" in openvino_devices or "GPU" in openvino_devices else "unavailable",
            provider="openvino",
            diagnostics={"openvino": openvino},
        ),
        capability_entry(
            name="openvino_npu_tool_proxy_report_only",
            resource="NPU",
            role="bounded_tool_proxy_report_only",
            status="available" if "NPU" in openvino_devices else "unavailable",
            provider="openvino_genai",
            diagnostics={"openvino": openvino},
        ),
        capability_entry(
            name="nvidia_gpu_ollama_primary_advisory",
            resource="NVIDIA_GPU",
            role="primary_advisory_when_enabled",
            status="available" if nvidia.get("available") else "unavailable",
            provider="ollama_or_cuda_runtime",
            diagnostics={"nvidia_smi": nvidia},
        ),
    ]

    warnings: list[str] = []
    if not openvino.get("available"):
        warnings.append("OpenVINO import/device detection unavailable; GPU.0/NPU are reported unavailable.")
    if not nvidia.get("available"):
        warnings.append("nvidia-smi unavailable or failed; NVIDIA GPU advisory visibility is degraded.")

    return {
        "schema_version": 1,
        "kind": "runtime_hardware_capability_manifest",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "mode": "report_only",
        "hardware_detection_performed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "persistent_memory_write_performed": False,
        "media_runtime_performed": False,
        "capabilities": capabilities,
        "required_resources_visible": {
            "CPU": any(item["resource"] == "CPU" for item in capabilities),
            "GPU.0": any(item["resource"] == "GPU.0" for item in capabilities),
            "NPU": any(item["resource"] == "NPU" for item in capabilities),
        },
        "errors": [],
        "warnings": warnings,
        "passed": True,
    }
