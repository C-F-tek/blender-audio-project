"""OpenVINO GPU.0 contract for Full0To10."""
from __future__ import annotations

from typing import Any


def build_gpu0_contract(capability: dict[str, Any]) -> dict[str, Any]:
    npu = capability.get("npu", {}) if isinstance(capability, dict) else {}
    devices = [str(item) for item in npu.get("devices", [])]
    gpu0_visible = "GPU.0" in devices
    return {
        "kind": "openvino_gpu0_contract",
        "passed": True,
        "role": "secondary_diagnostic_accelerator",
        "device_visible": gpu0_visible,
        "relationship_to_primary_gpu": "must_not_steal_ollama_gpu_lane",
        "allowed_actions": [
            "OpenVINO diagnostic",
            "capability listing",
            "secondary audit",
            "future promoted workload only with explicit patch",
        ],
        "blocked_actions": [
            "primary advisory default",
            "silent GPU provider takeover",
            "implicit generation",
        ],
    }
