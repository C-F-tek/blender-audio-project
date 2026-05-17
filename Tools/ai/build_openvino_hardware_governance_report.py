#!/usr/bin/env python3
"""Build a lightweight OpenVINO hardware governance report.

This report does not run inference. It only probes available OpenVINO devices
and records the IA-Carmine routing policy used by the provider mesh.
"""

from __future__ import annotations

import argparse
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def probe_openvino_devices() -> tuple[list[str], str]:
    try:
        from openvino import Core  # type: ignore
    except Exception as exc:  # noqa: BLE001 - report remains advisory.
        return [], f"{type(exc).__name__}: {exc}"
    try:
        return list(Core().available_devices), ""
    except Exception as exc:  # noqa: BLE001 - report remains advisory.
        return [], f"{type(exc).__name__}: {exc}"


def build_governance(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    devices, error = probe_openvino_devices()
    has_gpu0 = "GPU.0" in devices
    has_gpu1 = "GPU.1" in devices
    has_npu = "NPU" in devices
    gpu0_model_dir = os.environ.get("IA_CARMINE_GPU0_COMPANION_MODEL_DIR", "")
    mode = args.npu_micro_start_mode
    warnings: list[str] = []
    if error:
        warnings.append(f"OpenVINO probe unavailable: {error}")
    if has_gpu1:
        warnings.append(
            "GPU.1 is visible to OpenVINO but reserved for Ollama/CUDA; do not route OpenVINO work there by default."
        )
    if mode == "startup":
        warnings.append(
            "NPU startup mode may contend with GPU0/GPU1 on short live provider runs; deferred is preferred for local workstation use."
        )
    if not gpu0_model_dir:
        warnings.append(
            "IA_CARMINE_GPU0_COMPANION_MODEL_DIR is not configured; GPU0 semantic peer mode will classify as unconfigured/fallback."
        )

    routing = {
        "gpu1_primary_advisory": {
            "owner": "Ollama/CUDA",
            "preferred_device": "RTX 5080 / CUDA / GPU1",
            "openvino_device": None,
            "policy": "reserved_for_primary_advisory_not_openvino_workload",
        },
        "gpu0_companion_peer": {
            "owner": "OpenVINO companion worker",
            "preferred_device": "GPU.0" if has_gpu0 else "CPU fallback / unavailable",
            "semantic_model_configured": bool(gpu0_model_dir),
            "policy": "use GPU.0 when visible; never steal GPU.1 from Ollama",
        },
        "npu_micro_support": {
            "owner": "OpenVINO NPU micro support",
            "preferred_device": "NPU" if has_npu else "disabled/degraded",
            "start_mode": mode,
            "policy": "live seed through broker while GPU mesh is active; provider execution may be deferred to avoid contention",
        },
        "deterministic_validators": {
            "owner": "Python validators",
            "preferred_device": "CPU",
            "policy": "heavy audit authority stays deterministic and report-only",
        },
    }
    recommendation = "deferred" if has_npu and (has_gpu0 or has_gpu1) else "disabled"
    return {
        "schema_version": 1,
        "kind": "openvino_hardware_governance_report",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "classification": (
            "openvino_probe_available" if not error else "openvino_probe_unavailable_advisory"
        ),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "available_devices": devices,
        "probe_error": error,
        "gpu0_visible": has_gpu0,
        "gpu1_visible": has_gpu1,
        "npu_visible": has_npu,
        "gpu0_companion_model_dir_configured": bool(gpu0_model_dir),
        "requested_npu_micro_start_mode": mode,
        "recommended_npu_micro_start_mode": recommendation,
        "routing_policy": routing,
        "warnings": warnings,
        "errors": [],
        "guardrails": {
            "report_only": True,
            "no_inference_performed": True,
            "gpu1_reserved_for_ollama_cuda": True,
            "gpu0_openvino_explicit_device_only": True,
            "npu_micro_support_non_blocking": True,
            "patch_application_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# OpenVINO Hardware Governance Report",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Classification: `{report['classification']}`",
        f"- Available devices: `{report.get('available_devices')}`",
        f"- GPU0 visible: `{report.get('gpu0_visible')}`",
        f"- GPU1 visible: `{report.get('gpu1_visible')}`",
        f"- NPU visible: `{report.get('npu_visible')}`",
        f"- Requested NPU micro start mode: `{report.get('requested_npu_micro_start_mode')}`",
        f"- Recommended NPU micro start mode: `{report.get('recommended_npu_micro_start_mode')}`",
        "",
        "## Routing policy",
        "",
    ]
    for name, policy in report.get("routing_policy", {}).items():
        lines.append(f"### `{name}`")
        lines.append(f"- Owner: `{policy.get('owner')}`")
        lines.append(f"- Preferred device: `{policy.get('preferred_device')}`")
        lines.append(f"- Policy: {policy.get('policy')}")
        lines.append("")
    if report.get("warnings"):
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--npu-micro-start-mode",
        default="deferred",
        choices=["startup", "deferred", "live-seed-only", "disabled"],
    )
    parser.add_argument("--output", default="output/validation/openvino_hardware_governance.json")
    parser.add_argument(
        "--markdown-output", default="output/validation/openvino_hardware_governance.md"
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_governance(repo_root, args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(repo_rel(output, repo_root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
