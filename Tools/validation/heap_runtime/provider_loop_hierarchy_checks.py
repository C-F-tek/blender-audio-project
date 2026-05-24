"""Provider loop hierarchy smoke checks for GPU1/GPU0/NPU lanes."""

from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any


def run_provider_loop_hierarchy_checks(repo_root: Path) -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_command_specs import build_provider_command_specs
    from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import (
        GPU1_LANE,
    )
    from ia_carmine.runtime.heap_gate.provider_lane_policy import (
        GPU0_LANE,
        NPU_LANE,
        provider_lanes_for_revision,
    )

    errors: list[str] = []
    args = _args()
    fake = _FakeGate(repo_root, args)
    with TemporaryDirectory(prefix="provider-hierarchy-smoke-") as tmp:
        specs = {
            str(item.get("lane")): item
            for item in build_provider_command_specs(
                fake, Path(tmp), revision=1, selected_lanes={GPU1_LANE, GPU0_LANE, NPU_LANE}
            )
        }
    gpu1 = specs.get(GPU1_LANE, {})
    gpu0 = specs.get(GPU0_LANE, {})
    npu = specs.get(NPU_LANE, {})
    if gpu1.get("provider_model") != args.provider_model:
        errors.append(f"GPU1 provider model is not explicit args.provider_model={args.provider_model}")
    if gpu1.get("lane_tier") != "primary" or gpu1.get("authority") != "leader":
        errors.append("GPU1 is not marked as primary leader")
    if gpu0.get("lane_tier") != "coworker_medium" or gpu0.get("authority") != "coworker":
        errors.append("GPU0 is not marked as coworker_medium coworker")
    if gpu0.get("vulkan_visible_device") != "1" or gpu0.get("vulkan_vendor_id") != "0x8086":
        errors.append("GPU0 Vulkan coworker identity does not expose Intel Vulkan index 1")
    if gpu0.get("windows_task_manager_device_hint") != "Windows GPU 0 / Intel(R) Graphics":
        errors.append("GPU0 Windows/Vulkan device identity hint is missing")
    if npu.get("lane_tier") != "micro_fast" or npu.get("authority") != "micro_tool":
        errors.append("NPU is not marked as micro_fast micro_tool")
    gpu1_ctx = int(gpu1.get("context_budget", {}).get("ollama_num_ctx") or 0)
    gpu0_ctx = int(gpu0.get("context_budget", {}).get("ollama_num_ctx") or 0)
    if gpu0_ctx <= 0 or gpu1_ctx <= gpu0_ctx:
        errors.append(f"context hierarchy invalid: gpu1_ctx={gpu1_ctx}, gpu0_ctx={gpu0_ctx}")
    if gpu0_ctx != args.gpu0_ollama_num_ctx:
        errors.append("GPU0 context budget does not use explicit --gpu0-ollama-num-ctx")
    gpu0_command = [str(item) for item in gpu0.get("command", [])]
    if "--strict-provider-model" not in gpu0_command:
        errors.append("GPU0 coworker command can silently switch away from qwen3:1.7b")
    if _arg_after(gpu0_command, "--ollama-context-candidates") != str(gpu0_ctx):
        errors.append("GPU0 coworker command does not constrain context candidates to its medium ctx")
    rev1_owner = SimpleNamespace(skip_npu_on_soft_lock_targeted_refine=False)
    revision_lanes = provider_lanes_for_revision(rev1_owner, 1)
    if NPU_LANE not in revision_lanes or not rev1_owner.provider_revision_lane_policy.get("npu_rerun_each_revision"):
        errors.append("NPU is not rerun on later provider revisions")
    execution = (repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py").read_text(
        encoding="utf-8", errors="replace"
    )
    if "gpu1_leader_started_before_sidecars" not in execution:
        errors.append("provider loop does not start GPU1 leader before sidecars")
    if "async_packet_review_only" not in execution:
        errors.append("provider loop does not start sidecars as async packet-review evidence")
    if "gpu1_boot_leader_ready" not in execution:
        errors.append("provider loop does not distinguish GPU1 boot leadership from final evidence")
    if "capture_gpu1_primary_evidence_before_sidecars" not in execution:
        errors.append("provider loop does not capture GPU1 primary evidence before sidecars")
    if "gpu1_primary_evidence_missing_before_sidecars" not in execution:
        errors.append("provider loop does not block missing GPU1 final evidence before sidecars")
    return {"name": "provider_lane_hierarchy", "errors": errors}


class _FakeGate:
    def __init__(self, repo_root: Path, args: SimpleNamespace) -> None:
        self.repo_root = repo_root
        self.args = args
        self.provider_leader_packet_path = "provider_teamwork_leader_packet.json"
        self.selected_provider_model = ""
        self.selected_ollama_num_ctx = 8192
        self.provider_role_coexistence_preflight = {
            "gpu0_vulkan_server": {
                "vulkan_device_selection": {
                    "resolved": "1",
                    "target_device": {
                        "vendorID": "0x8086",
                        "deviceName": "Intel(R) Graphics",
                        "deviceType": "PHYSICAL_DEVICE_TYPE_INTEGRATED_GPU",
                    },
                }
            }
        }

    def child_python(self) -> str:
        return "python"

    def request_text(self) -> str:
        return "smoke request"


def _args() -> SimpleNamespace:
    return SimpleNamespace(
        allow_npu_device_workload=True,
        allow_provider_generation=True,
        budget_minutes=5,
        gpu0_iterations=16,
        gpu0_min_seconds=0.1,
        gpu0_base_url="http://127.0.0.1:11435",
        gpu0_model="qwen3:1.7b",
        gpu0_vulkan_visible_devices="1",
        keep_alive="120s",
        max_new_tokens=900,
        npu_device_workload_iterations=2500,
        npu_device_workload_seconds=3.0,
        npu_max_context_chars=8000,
        npu_max_new_tokens=384,
        npu_max_prompt_chars=1200,
        npu_micro_timeout_seconds=60,
        ollama_context_candidates="8192,4096",
        ollama_gpu_layers="all",
        ollama_num_ctx=8192,
        gpu0_ollama_num_ctx=2048,
        gpu0_max_new_tokens=256,
        gpu1_base_url="http://127.0.0.1:11434",
        operator_gpu_observation="",
        provider_model="qwen3-coder:latest",
        request_file="",
        startup_manifest="",
        strict_provider_model=False,
        task_file="",
        timeout_seconds=600,
    )


def _arg_after(command: list[str], flag: str) -> str:
    if flag not in command:
        return ""
    index = command.index(flag)
    return command[index + 1] if index + 1 < len(command) else ""
