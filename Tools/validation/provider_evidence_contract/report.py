"""Report assembly and Markdown for provider evidence contract."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from .common import is_fallback_artifact, now_iso, read_optional_json, resolve_path, safe_list
from .evidence import (
    gpu_provider_evidence,
    gpu0_peer_support_evidence,
    npu_micro_support_evidence,
    npu_provider_evidence,
    openvino_gpu0_secondary_evidence,
    probe_evidence,
)

def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    orchestrator, orch_errors, orch_path = read_optional_json(
        repo_root, args.orchestrator, required=True
    )
    gpu_report, gpu_errors, gpu_path = read_optional_json(repo_root, args.gpu_report, required=True)
    gpu_npu_sync, sync_errors, sync_path = read_optional_json(
        repo_root, args.gpu_npu_sync, required=False
    )
    local_probe, probe_errors, probe_path = read_optional_json(
        repo_root, args.local_provider_probe, required=False
    )
    hardware_manifest, hardware_errors, hardware_path = read_optional_json(
        repo_root, args.hardware_manifest, required=False
    )
    openvino_gpu0_workload, gpu0_errors, gpu0_path = read_optional_json(
        repo_root, args.openvino_gpu0_workload, required=False
    )

    errors.extend(orch_errors)
    errors.extend(gpu_errors)
    warnings.extend(sync_errors)
    warnings.extend(probe_errors)
    warnings.extend(hardware_errors)
    warnings.extend(gpu0_errors)

    gpu = gpu_provider_evidence(gpu_report)
    npu = npu_provider_evidence(orchestrator)
    npu_micro = npu_micro_support_evidence(orchestrator)
    probe = probe_evidence(local_probe)
    openvino_gpu0_secondary = openvino_gpu0_secondary_evidence(openvino_gpu0_workload)
    gpu0_peer_support = gpu0_peer_support_evidence(orchestrator)
    openvino_gpu0_secondary_real = bool(
        openvino_gpu0_secondary["real"] or gpu0_peer_support["real"]
    )
    hardware_policy = (
        hardware_manifest.get("hardware_lane_policy")
        if isinstance(hardware_manifest.get("hardware_lane_policy"), dict)
        else {}
    )
    cuda_primary = (
        hardware_policy.get("cuda_gpu_primary", {})
        if isinstance(hardware_policy.get("cuda_gpu_primary"), dict)
        else {}
    )
    openvino_gpu0 = (
        hardware_policy.get("openvino_gpu0", {})
        if isinstance(hardware_policy.get("openvino_gpu0"), dict)
        else {}
    )
    openvino_npu = (
        hardware_policy.get("openvino_npu", {})
        if isinstance(hardware_policy.get("openvino_npu"), dict)
        else {}
    )
    openvino_gpu1_reserved = (
        hardware_policy.get("openvino_gpu1_reserved", {})
        if isinstance(hardware_policy.get("openvino_gpu1_reserved"), dict)
        else {}
    )

    if args.require_gpu_provider and not gpu["real"]:
        errors.append(
            "GPU provider evidence missing or degraded: "
            f"performed={gpu['provider_execution_performed']} round_count={gpu['round_count']} "
            f"empty={gpu['provider_empty_response']} classification={gpu['classification']} "
            f"error={gpu['provider_error']}"
        )
    if args.require_npu_auditor and not npu["real"]:
        errors.append(
            "NPU auditor evidence missing or probe-only: "
            f"audit_count={npu['audit_count']} load_attempt_count={npu['load_attempt_count']} "
            f"success_count={npu['success_count']} lane_mode={npu['lane_mode']}"
        )
    if args.require_openvino_gpu0_secondary and not openvino_gpu0_secondary_real:
        errors.append(
            "OpenVINO GPU.0 secondary workload evidence missing or degraded: "
            f"visible={openvino_gpu0_secondary['openvino_gpu0_visible']} "
            f"probe={openvino_gpu0_secondary['openvino_gpu0_probe_performed']} "
            f"workload={openvino_gpu0_secondary['openvino_gpu0_workload_performed']} "
            f"passed={openvino_gpu0_secondary['openvino_gpu0_workload_passed']} "
            f"provider={openvino_gpu0_secondary['openvino_gpu0_provider_execution_performed']} "
            f"selected={openvino_gpu0_secondary['selected_device']} "
            f"errors={openvino_gpu0_secondary['errors']} "
            f"orchestrator_peer_success={gpu0_peer_support['success_count']} "
            f"orchestrator_peer_overlap={gpu0_peer_support['overlap_count']}"
        )
    if (
        args.forbid_openvino_gpu1_workload
        and openvino_gpu0_secondary["openvino_gpu1_workload_performed"]
    ):
        errors.append(
            "hardware policy violation: OpenVINO GPU.1 workload was performed, but GPU.1 is reserved for CUDA/Ollama"
        )
    if is_fallback_artifact(gpu_report):
        errors.append(
            "GPU report is a required_provider_artifact_missing fallback, not real provider evidence"
        )
    if is_fallback_artifact(orchestrator):
        errors.append(
            "orchestrator report is a required_provider_artifact_missing fallback, not real provider evidence"
        )
    if orchestrator and orchestrator.get("gpu_returncode") not in (None, 0):
        errors.append(
            f"GPU subprocess returned non-zero exit code: {orchestrator.get('gpu_returncode')}"
        )
    if local_probe and local_probe.get("passed") is False:
        warnings.append(f"local provider probe degraded: {local_probe.get('errors')}")
    if hardware_policy:
        if cuda_primary.get("exclusive") is not True:
            errors.append("hardware policy violation: CUDA/Ollama primary GPU must be exclusive")
        if cuda_primary.get("openvino_workload_allowed") is not False:
            errors.append(
                "hardware policy violation: CUDA/Ollama primary GPU must not allow OpenVINO workload"
            )
        if openvino_gpu0.get("not_primary_advisory") is not True:
            errors.append(
                "hardware policy violation: OpenVINO GPU.0 must not satisfy primary GPU advisory"
            )
        if openvino_npu.get("probe_only_is_not_auditor_evidence") is not True:
            errors.append(
                "hardware policy violation: NPU probe-only evidence must not satisfy auditor evidence"
            )
        if openvino_gpu1_reserved.get("openvino_workload_allowed") is not False:
            errors.append(
                "hardware policy violation: OpenVINO GPU.1/RTX must be reserved for CUDA/Ollama"
            )

    provider_execution_observed = bool(
        gpu["real"] or npu["real"] or npu_micro["real"] or openvino_gpu0_secondary_real
    )
    return {
        "schema_version": 1,
        "kind": "provider_evidence_contract",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_requested": bool(args.require_gpu_provider or args.require_npu_auditor),
        "provider_execution_performed": provider_execution_observed,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "manual_review_required": True,
        "inputs": {
            "orchestrator": orch_path,
            "gpu_report": gpu_path,
            "gpu_npu_sync": sync_path,
            "local_provider_probe": probe_path,
            "hardware_manifest": hardware_path,
            "openvino_gpu0_workload": gpu0_path,
        },
        "cuda_gpu_primary_real": gpu["real"],
        "openvino_gpu0_secondary_real": openvino_gpu0_secondary_real,
        "openvino_gpu0_secondary_file_real": openvino_gpu0_secondary["real"],
        "gpu0_peer_support_real": gpu0_peer_support["real"],
        "npu_auditor_real": npu["real"],
        "npu_micro_support_real": npu_micro["real"],
        "openvino_gpu1_reserved_visible": bool(
            openvino_gpu1_reserved.get("visible")
            or openvino_gpu0_secondary.get("openvino_gpu1_reserved_visible")
        ),
        "gpu": gpu,
        "openvino_gpu0_secondary": openvino_gpu0_secondary,
        "gpu0_peer_support": gpu0_peer_support,
        "npu": npu,
        "npu_micro_support": npu_micro,
        "local_probe": probe,
        "hardware_policy": hardware_policy,
        "gpu_npu_sync_metrics": gpu_npu_sync.get("metrics")
        if isinstance(gpu_npu_sync.get("metrics"), dict)
        else {},
        "decision": {
            "gpu_provider_ready": gpu["real"],
            "openvino_gpu0_secondary_ready": openvino_gpu0_secondary_real,
            "gpu0_peer_support_ready": gpu0_peer_support["real"],
            "npu_micro_support_ready": npu_micro["real"],
            "gpu0_does_not_satisfy_cuda_primary": True,
            "npu_probe_only_is_not_auditor_evidence": True,
            "openvino_gpu1_workload_forbidden": True,
            "npu_auditor_ready": npu["real"],
            "probe_only_is_not_provider_evidence": True,
            "strict_provider_contract_satisfied": not errors,
            "recommended_next_action": "run_heap_provider_lane"
            if errors
            else "continue_bundle_review",
        },
        "guardrails": {
            "report_only": True,
            "provider_settings_changed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "blender_runtime_execution_performed": False,
            "ffmpeg_execution_performed": False,
            "raw_output_commit_allowed": False,
        },
    }

def render_markdown(report: dict[str, Any]) -> str:
    gpu = report.get("gpu", {}) if isinstance(report.get("gpu"), dict) else {}
    npu = report.get("npu", {}) if isinstance(report.get("npu"), dict) else {}
    npu_micro = (
        report.get("npu_micro_support", {})
        if isinstance(report.get("npu_micro_support"), dict)
        else {}
    )
    gpu0 = (
        report.get("openvino_gpu0_secondary", {})
        if isinstance(report.get("openvino_gpu0_secondary"), dict)
        else {}
    )
    gpu0_peer = (
        report.get("gpu0_peer_support", {})
        if isinstance(report.get("gpu0_peer_support"), dict)
        else {}
    )
    lines = ["# Provider Evidence Contract", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    lines.append(f"- GPU real provider evidence: `{gpu.get('real')}`")
    lines.append(f"- GPU round count: `{gpu.get('round_count')}`")
    lines.append(f"- GPU provider error: `{gpu.get('provider_error')}`")
    lines.append(f"- OpenVINO GPU.0 secondary real evidence: `{gpu0.get('real')}`")
    lines.append(f"- OpenVINO GPU.0 visible: `{gpu0.get('openvino_gpu0_visible')}`")
    lines.append(
        f"- OpenVINO GPU.0 workload performed: `{gpu0.get('openvino_gpu0_workload_performed')}`"
    )
    lines.append(f"- OpenVINO GPU.0 workload passed: `{gpu0.get('openvino_gpu0_workload_passed')}`")
    lines.append(f"- GPU0 orchestrator peer support real evidence: `{gpu0_peer.get('real')}`")
    lines.append(f"- GPU0 orchestrator peer support count: `{gpu0_peer.get('support_count')}`")
    lines.append(f"- GPU0 orchestrator peer success count: `{gpu0_peer.get('success_count')}`")
    lines.append(f"- GPU0 orchestrator peer overlap count: `{gpu0_peer.get('overlap_count')}`")
    lines.append(
        f"- OpenVINO GPU.1 reserved visible: `{gpu0.get('openvino_gpu1_reserved_visible')}`"
    )
    lines.append(
        f"- OpenVINO GPU.1 workload performed: `{gpu0.get('openvino_gpu1_workload_performed')}`"
    )
    lines.append(f"- NPU real auditor evidence: `{npu.get('real')}`")
    lines.append(f"- NPU audit count: `{npu.get('audit_count')}`")
    lines.append(f"- NPU success count: `{npu.get('success_count')}`")
    lines.append(f"- NPU micro support real evidence: `{npu_micro.get('real')}`")
    lines.append(f"- NPU micro support count: `{npu_micro.get('support_count')}`")
    lines.append(f"- NPU micro provider success count: `{npu_micro.get('provider_success_count')}`")
    lines.append(f"- NPU micro tool success count: `{npu_micro.get('tool_success_count')}`")
    lines.append(f"- NPU micro overlap count: `{npu_micro.get('overlap_count')}`")
    lines.append(f"- NPU micro tool requests: `{npu_micro.get('tool_request_count')}`")
    lines.append(
        f"- NPU micro runtime tool executions: `{npu_micro.get('runtime_tool_execution_count')}`"
    )
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        for item in report.get("errors", []):
            lines.append(f"- {item}")
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        for item in report.get("warnings", [])[:30]:
            lines.append(f"- {item}")
    lines.append("")
    return "\n".join(lines)
