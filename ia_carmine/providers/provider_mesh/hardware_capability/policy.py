from __future__ import annotations

from typing import Any

# IA-Carmine workstation policy:
# - keep GPU1 as Ollama primary advisory;
# - use GPU0 only through Ollama/Vulkan as peer reviewer/refiner;
# - use OpenVINO only for the NPU micro/audit lane;
# - keep CPU shared for orchestration, validation, fallback and reporting.

CUDA_PRIMARY_DEVICE = "GPU 1 / NVIDIA RTX 5080"
OLLAMA_GPU0_VULKAN_DEVICE = "GPU0 / Ollama Vulkan"
OPENVINO_NPU_DEVICE = "Intel AI Boost"
OPENVINO_GPU1_RESERVED_DEVICE = "NVIDIA RTX 5080"


def _device_details(openvino: dict[str, Any], device: str) -> dict[str, Any]:
    details = openvino.get("device_details")
    if isinstance(details, dict):
        item = details.get(device)
        if isinstance(item, dict):
            return item
    return {}


def _full_name(openvino: dict[str, Any], device: str, fallback: str) -> str:
    return str(_device_details(openvino, device).get("full_device_name") or fallback)


def _capabilities(openvino: dict[str, Any], device: str) -> list[str]:
    value = _device_details(openvino, device).get("optimization_capabilities")
    if isinstance(value, list):
        return [str(item) for item in value]
    return []


def openvino_device_visible(openvino: dict[str, Any], device: str) -> bool:
    devices = openvino.get("devices")
    return isinstance(devices, list) and device in {str(item) for item in devices}


def nvidia_available(nvidia: dict[str, Any]) -> bool:
    return bool(nvidia.get("available"))


def build_hardware_runtime_policy(
    openvino: dict[str, Any], nvidia: dict[str, Any]
) -> dict[str, Any]:
    """Return the canonical runtime lane policy for IA-Carmine."""
    gpu0_visible = openvino_device_visible(openvino, "GPU.0") or openvino_device_visible(
        openvino, "GPU"
    )
    gpu1_visible = openvino_device_visible(openvino, "GPU.1")
    npu_visible = openvino_device_visible(openvino, "NPU")

    return {
        "schema_version": 1,
        "kind": "runtime_hardware_lane_policy",
        "cuda_gpu_primary": {
            "device": CUDA_PRIMARY_DEVICE,
            "owner": "Ollama/CUDA",
            "role": "primary_advisory_provider",
            "exclusive": True,
            "visible": nvidia_available(nvidia),
            "openvino_workload_allowed": False,
            "rationale": "Reserve RTX compute/VRAM for the primary Ollama advisory provider.",
        },
        "cpu_shared": {
            "device": "CPU",
            "owner": "shared",
            "role": "orchestration_validation_fallback",
            "exclusive": False,
            "visible": True,
            "workload_allowed": True,
        },
        "ollama_gpu0_vulkan": {
            "device": "GPU0",
            "full_device_name": _full_name(openvino, "GPU.0", OLLAMA_GPU0_VULKAN_DEVICE),
            "owner": "Ollama/Vulkan",
            "role": "peer_reviewer_refiner",
            "visible": gpu0_visible,
            "openvino_workload_allowed": False,
            "ollama_workload_required": True,
            "allowed_workloads": [
                "peer_review",
                "refinement",
                "native_tool_calling",
            ],
            "not_primary_advisory": True,
            "optimization_capabilities": _capabilities(openvino, "GPU.0"),
        },
        "openvino_npu": {
            "device": "NPU",
            "full_device_name": _full_name(openvino, "NPU", OPENVINO_NPU_DEVICE),
            "owner": "OpenVINO",
            "role": "auditor_guardrail",
            "visible": npu_visible,
            "openvino_workload_allowed": npu_visible,
            "allowed_workloads": ["audit", "decode_guardrail", "discrepancy_check"],
            "probe_only_is_not_auditor_evidence": True,
            "optimization_capabilities": _capabilities(openvino, "NPU"),
        },
        "openvino_gpu1_reserved": {
            "device": "GPU.1",
            "full_device_name": _full_name(openvino, "GPU.1", OPENVINO_GPU1_RESERVED_DEVICE),
            "owner": "OpenVINO visibility only",
            "role": "reserved_for_cuda_ollama",
            "visible": gpu1_visible,
            "openvino_workload_allowed": False,
            "policy": "reserved_for_cuda_ollama",
            "rationale": "OpenVINO may see the NVIDIA dGPU, but workloads are blocked to avoid contention with Ollama/CUDA.",
            "optimization_capabilities": _capabilities(openvino, "GPU.1"),
        },
    }


def policy_warnings(policy: dict[str, Any]) -> list[str]:
    warnings: list[str] = []
    if not policy.get("cuda_gpu_primary", {}).get("visible"):
        warnings.append("CUDA/Ollama primary GPU is not visible through nvidia-smi diagnostics.")
    if not policy.get("ollama_gpu0_vulkan", {}).get("visible"):
        warnings.append("GPU0 is not visible for Ollama/Vulkan peer-lane diagnostics.")
    if not policy.get("openvino_npu", {}).get("visible"):
        warnings.append("OpenVINO NPU auditor lane is not visible.")
    if policy.get("openvino_gpu1_reserved", {}).get("visible"):
        warnings.append(
            "OpenVINO GPU.1 is visible but intentionally reserved for CUDA/Ollama; OpenVINO workloads are blocked by policy."
        )
    return warnings
