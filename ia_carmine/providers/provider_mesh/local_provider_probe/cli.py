#!/usr/bin/env python3
"""Run explicit local provider probes and normalize report-only results."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any
import sys

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from ia_carmine._shared.provider_ollama_probe import run_ollama_probe
from ia_carmine._shared.provider_probe_paths import ensure_repo_imports
from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine._shared.file_backed_transport import (
    compact_text_fields as shared_compact_text_fields,
    write_text_artifact,
)


def _option_supplied(argv: list[str], option: str) -> bool:
    return any(item == option or item.startswith(f"{option}=") for item in argv)


def _config_sources(args: argparse.Namespace, argv: list[str]) -> dict[str, str]:
    option_map = {
        "model": "--model",
        "timeout": "--timeout",
        "max_new_tokens": "--max-new-tokens",
        "ollama_num_ctx": "--ollama-num-ctx",
        "ollama_gpu_layers": "--ollama-gpu-layers",
        "ollama_num_thread": "--ollama-num-thread",
        "ollama_context_candidates": "--ollama-context-candidates",
        "ollama_base_url": "--ollama-base-url",
        "strict_provider_model": "--strict-provider-model",
        "operator_gpu_observation": "--operator-gpu-observation",
        "ollama_lane": "--ollama-lane",
        "ollama_role": "--ollama-role",
        "keep_alive": "--keep-alive",
        "require_ollama_gpu_residency": "--require-ollama-gpu-residency",
        "npu_python_exe": "--npu-python-exe",
    }
    return {
        key: "cli_arg" if _option_supplied(argv, option) else "standalone_default"
        for key, option in option_map.items()
        if getattr(args, key, None) not in (None, "")
    }


def propagated_positive_int(name: str, value: int) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise ValueError(f"{name} must be a positive operator/heap propagated value")
    return parsed


def run_npu_probe(
    repo_root: Path,
    timeout: float,
    npu_python_exe: str | None = None,
    prompt: str | None = None,
    max_new_tokens: int = 64,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from ia_carmine.providers.npu.provider_mesh._shared.npu_runtime import (  # noqa: PLC0415
        DEFAULT_NPU_PYTHON,
        _parse_last_json_line,
        _run_python,
    )
    from ia_carmine.providers.npu.pipeline import parse_provider_result  # noqa: PLC0415
    from ia_carmine._shared.provider_tool_loop import openvino_tool_loop_report  # noqa: PLC0415
    started = time.perf_counter()
    code = r"""
import json
import numpy as np
import openvino as ov
core = ov.Core()
devices = core.available_devices
result = {"ok": "NPU" in devices, "lane": "npu", "devices": devices}
print(json.dumps(result))
"""
    python_exe = Path(npu_python_exe).expanduser() if npu_python_exe else DEFAULT_NPU_PYTHON
    ok, text, exit_code = _run_python(python_exe, code, timeout=timeout)
    parsed_payload = _parse_last_json_line(text) if ok else {"error": text, "exit_code": exit_code}
    parsed = parse_provider_result(
        {"text": json.dumps(parsed_payload)},
        provider="openvino_npu",
        model="device_probe",
        executed=True,
        allow_json=True,
    )
    tool_loop = openvino_tool_loop_report(
        repo_root=repo_root,
        prompt=prompt or "List the broker tool call you would request for code validation.",
        timeout_seconds=timeout,
        max_new_tokens=propagated_positive_int("max_new_tokens", max_new_tokens),
        python_exe=str(python_exe),
        device="NPU",
    )
    report = {
        "lane": "npu",
        "passed": (
            ok and bool(parsed_payload.get("ok")) if isinstance(parsed_payload, dict) else False
        ),
        "provider_execution_performed": False,
        "provider_backend": "openvino",
        "provider_compute_device": "openvino/NPU" if parsed_payload.get("ok") else "openvino/NPU_unavailable",
        "provider_device_verified": bool(parsed_payload.get("ok")),
        "provider_unload_performed": True,
        "provider_unload_verified": True,
        "provider_inactivity_unload_seconds": 120,
        "openvino_npu_unload_policy": "child_process_exit_releases_model",
        "cpu_provider_fallback_performed": False,
        "elapsed_sec": round(time.perf_counter() - started, 4),
        "parsed_result": parsed.to_dict(),
        "openvino_native_tool_loop": tool_loop,
        "native_tool_loop_provider": "openvino_genai",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": bool(tool_loop.get("native_tool_loop_supported")),
        "native_tool_loop_performed": bool(tool_loop.get("native_tool_loop_performed")),
        "native_tool_call_count": int(tool_loop.get("native_tool_call_count") or 0),
        "tool_calls": tool_loop.get("tool_calls") or [],
        "npu_micro_provider_model_loaded": bool(tool_loop.get("native_tool_loop_performed")),
        "npu_micro_provider_execution_performed": False,
        "npu_device_workload_requested": False,
        "npu_device_workload_performed": False,
        "raw_exit_code": exit_code,
        "raw_preview": text[:300],
    }
    report.update(provider_work_status(lane="npu_micro_task_auditor", report=report, default_role="npu_auditor"))
    report["passed"] = bool(report["provider_work_verified"])
    return report

def read_prompt_file(repo_root: Path, prompt_file: str) -> str:
    """Read an optional provider prompt from disk.

    This keeps large heap/GPU1 prompts out of Windows argv and makes the exact
    provider input inspectable as a run artifact.
    """
    if not prompt_file:
        return ""
    path = Path(prompt_file)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig")


def materialize_provider_prompt(
    repo_root: Path,
    output_path: Path,
    prompt: str,
) -> dict[str, Any]:
    """Persist the exact provider prompt sent to Ollama as report metadata."""
    return write_text_artifact(
        repo_root,
        output_path.parent / "provider_prompt_payload",
        name="request_prompt",
        text=prompt or "",
        kind="ollama_request_prompt",
        producer="local_provider_probe",
        suffix=".md",
    )


def mirror_single_provider_lane(report: dict[str, Any], lane_report: dict[str, Any]) -> dict[str, Any]:
    """Expose the actual provider lane at top level for gates and workload checks."""
    mirror_keys = (
        "lane",
        "provider_id",
        "provider_role",
        "provider_model",
        "provider_backend",
        "provider_compute_device",
        "provider_device_verified",
        "provider_execution_performed",
        "provider_loaded",
        "response_text_ref",
        "response_text_chars",
        "response_text_sha256",
        "response_text_tail",
        "response_text_tail_chars",
        "response_text_full_text_in_json",
        "response_text_transport",
        "provider_heap_delta_text_ref",
        "provider_heap_delta_text_chars",
        "provider_heap_delta_text_sha256",
        "provider_heap_delta_text_tail",
        "provider_heap_delta_text_tail_chars",
        "provider_heap_delta_text_full_text_in_json",
        "raw_response_chars",
        "text_preview",
        "target_files",
        "validation_commands",
        "tool_calls",
        "textual_tool_calls",
        "native_tool_loop_requested",
        "native_tool_loop_supported",
        "native_tool_loop_performed",
        "native_tool_loop_classification",
        "provider_native_tool_call_required",
        "provider_native_tool_api_attempted",
        "provider_native_tool_api_completed",
        "provider_native_tool_api_adapter_available",
        "provider_native_tool_api_supported",
        "provider_native_tool_api_error",
        "provider_native_tool_api_attempt_error",
        "provider_native_tool_api_unavailable",
        "provider_native_tool_api_attempt_failed",
        "provider_native_tool_call_required_unmet",
        "native_tool_call_count",
        "textual_tool_call_count",
        "generated_phrase",
        "prompt_token_count",
        "completion_token_count",
        "tokens_per_second",
        "native_tool_calling_supported",
        "broker_tools_available_count",
        "available_tool_names",
        "functionalities",
        "replight_passed",
        "replight_blocked_reason",
        "selected_model",
        "requested_provider_model",
        "selected_provider_model",
        "model_switch_reason",
        "full_gpu_residency_required",
        "full_gpu_residency_verified",
        "provider_repair_attempts",
        "product_blocked_reason",
        "provider_stage",
        "provider_work_verified",
        "provider_role_counted",
        "provider_rejection_reason",
        "role_rejection_reason",
        "device_detected",
        "model_loaded",
        "health_check_passed",
        "workload_performed",
        "useful_output_produced",
        "gpu_runtime_samples",
        "gpu_utilization_peak_percent",
        "gpu_memory_used_peak_mib",
        "gpu_process_observed",
        "ollama_residency_verified",
        "ollama_compute_verified",
        "heap_delta_text_present",
        "heap_delta_text_required",
        "provider_output_complete",
        "response_likely_incomplete",
        "prompt_attempts",
        "eval_count",
        "prompt_eval_count",
    )
    for key in mirror_keys:
        if key in lane_report:
            report[key] = lane_report[key]
    report["wrapper_kind"] = report.get("kind")
    report["kind"] = "local_provider_probe"
    return report


def _compact_provider_payload(
    repo_root: Path,
    output_dir: Path,
    payload: dict[str, Any],
    *,
    name: str,
) -> dict[str, Any]:
    compact = shared_compact_text_fields(
        repo_root,
        output_dir / "provider_report_artifacts",
        payload,
        (
            "response_text",
            "provider_heap_delta_text",
            "gpu0_raw_response_text",
            "request_prompt",
            "raw_preview",
        ),
        name=name,
        producer="local_provider_probe",
        kind_prefix="local_provider_probe",
        suffix=".md",
    )
    text_keys = {
        "response_text",
        "provider_heap_delta_text",
        "gpu0_raw_response_text",
        "request_prompt",
        "raw_preview",
    }
    for key in text_keys:
        compact.pop(key, None)
    nested = compact.get("openvino_native_tool_loop")
    if isinstance(nested, dict):
        compact["openvino_native_tool_loop"] = _compact_provider_payload(
            repo_root,
            output_dir,
            nested,
            name=f"{name}_openvino_native_tool_loop",
        )
    child = compact.get("child")
    if isinstance(child, dict):
        compact["child"] = _compact_provider_payload(
            repo_root,
            output_dir,
            child,
            name=f"{name}_child",
        )
    return compact


def build_report(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from ia_carmine._shared.provider_tool_loop import build_heap_patch_proposal_prompt  # noqa: PLC0415
    from ia_carmine.providers.npu.pipeline import (  # noqa: PLC0415
        build_provider_result_report,
        parse_provider_result,
    )

    lane_reports: list[dict[str, Any]] = []
    errors: list[str] = []
    effective_prompt = args.prompt
    if getattr(args, "prompt_file", ""):
        try:
            file_prompt = read_prompt_file(repo_root, args.prompt_file)
            if file_prompt.strip():
                effective_prompt = file_prompt
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            errors.append(f"prompt_file: {type(exc).__name__}: {exc}")
    if args.run_ollama:
        try:
            if not args.replight_mode:
                effective_prompt = build_heap_patch_proposal_prompt(effective_prompt)
            partial_output = Path(args.output)
            if not partial_output.is_absolute():
                partial_output = repo_root / partial_output
            prompt_ref = materialize_provider_prompt(repo_root, partial_output, effective_prompt)
            lane_reports.append(
                run_ollama_probe(
                    repo_root,
                    args.model,
                    effective_prompt,
                    max_new_tokens=propagated_positive_int(
                        "max_new_tokens", args.max_new_tokens
                    ),
                    num_ctx=args.ollama_num_ctx,
                    gpu_layers=args.ollama_gpu_layers,
                    num_thread=args.ollama_num_thread,
                    keep_alive=args.keep_alive,
                    partial_output=partial_output,
                    require_gpu_residency=args.require_ollama_gpu_residency,
                    replight_mode=args.replight_mode,
                    context_candidates=args.ollama_context_candidates,
                    strict_provider_model=args.strict_provider_model,
                    operator_gpu_observation=args.operator_gpu_observation,
                    lane=args.ollama_lane,
                    role=args.ollama_role,
                    base_url=args.ollama_base_url,
                    unload_model=not args.defer_unload,
                    prompt_ref=prompt_ref,
                )
            )
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            lane_reports.append(
                {
                    "lane": "ollama",
                    "passed": False,
                    "provider_execution_performed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    if args.run_npu:
        try:
            lane_reports.append(
                run_npu_probe(
                    repo_root,
                    args.timeout,
                    args.npu_python_exe,
                    effective_prompt,
                    max_new_tokens=propagated_positive_int(
                        "max_new_tokens", args.max_new_tokens
                    ),
                )
            )
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            lane_reports.append(
                {
                    "lane": "npu",
                    "passed": False,
                    "provider_execution_performed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    parsed_results = [
        parse_provider_result(
            {"text": json.dumps({"lane": item.get("lane"), "passed": item.get("passed")})},
            provider=str(item.get("lane") or "unknown"),
            model=str(item.get("selected_model") or "probe"),
            executed=bool(item.get("provider_execution_performed")),
            allow_json=True,
        )
        for item in lane_reports
    ]
    provider_report = build_provider_result_report(
        provider="local_probe",
        model=args.model or "auto",
        results=parsed_results,
        provider_execution_performed=any(
            item.get("provider_work_verified") for item in lane_reports
        ),
    )
    for item in lane_reports:
        if item.get("passed") is False:
            item_errors = item.get("errors") if isinstance(item.get("errors"), list) else []
            reason = item.get("error") or " | ".join(str(e) for e in item_errors) or "probe failed"
            errors.append(f"{item.get('lane')}: {reason}")
    devices = [
        str(item.get("provider_compute_device") or "")
        for item in lane_reports
        if str(item.get("provider_compute_device") or "").strip()
    ]

    partial_output = Path(args.output)
    if not partial_output.is_absolute():
        partial_output = repo_root / partial_output
    safe_lane_reports = [
        _compact_provider_payload(
            repo_root,
            partial_output.parent,
            item,
            name=f"lane_report_{index}_{item.get('lane') or 'unknown'}",
        )
        for index, item in enumerate(lane_reports)
        if isinstance(item, dict)
    ]

    report = {
        "schema_version": 1,
        "kind": "local_provider_probe",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "config_sources": getattr(args, "config_sources", {}),
        "standalone_default_fields": [
            key
            for key, source in getattr(args, "config_sources", {}).items()
            if source == "standalone_default"
        ],
        "provider_execution_performed": any(
            item.get("provider_work_verified") for item in lane_reports
        ),
        "provider_backend": "local_provider_probe",
        "provider_compute_device": ",".join(devices),
        "provider_device_verified": bool(
            lane_reports and all(item.get("provider_device_verified") for item in lane_reports)
        ),
        "cpu_provider_fallback_performed": any(
            item.get("cpu_provider_fallback_performed") for item in lane_reports
        ),
        "lane_reports": safe_lane_reports,
        "provider_result_report": provider_report,
        "canonical_run_provider_evidence": bool(args.canonical_run_provider_evidence),
        "canonical_run_fingerprint": str(args.canonical_run_fingerprint or ""),
    }
    if args.run_ollama and len(safe_lane_reports) == 1 and isinstance(safe_lane_reports[0], dict):
        return mirror_single_provider_lane(report, safe_lane_reports[0])
    return report

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/local_provider_probe.json")
    parser.add_argument("--model", help="Preferred Ollama model.")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--ollama-num-ctx", type=int, default=16384)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default="all")
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default="8192,4096")
    parser.add_argument("--ollama-base-url", default="")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--ollama-lane", default="gpu1_planner")
    parser.add_argument("--ollama-role", default="")
    parser.add_argument("--keep-alive", default="0s")
    parser.add_argument("--defer-unload", action="store_true")
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=True)
    parser.add_argument("--replight-mode", action="store_true")
    parser.add_argument("--npu-python-exe", default="")
    parser.add_argument("--run-ollama", action="store_true")
    parser.add_argument("--run-npu", action="store_true")
    parser.add_argument("--canonical-run-provider-evidence", action="store_true")
    parser.add_argument("--canonical-run-fingerprint", default="")
    raw_argv = sys.argv[1:]
    args = parser.parse_args(raw_argv)
    args.config_sources = _config_sources(args, raw_argv)
    if not args.run_ollama and not args.run_npu:
        parser.error("At least one explicit probe flag is required: --run-ollama or --run-npu")
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {
        "passed": report["passed"],
        "output": str(output),
        "provider_execution_performed": report["provider_execution_performed"],
    }
    print(json.dumps(summary, indent=2))
    return 0 if report["passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
