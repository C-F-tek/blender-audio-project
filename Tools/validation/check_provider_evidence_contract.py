#!/usr/bin/env python3
"""Validate strict provider evidence for full-toolbox GPU/NPU runs.

This validator is report-only. It does not execute providers, does not apply
patches and does not mutate source files. Its job is to separate four states
that were previously conflated in telemetry:

- provider requested;
- provider wrapper/probe executed;
- GPU/Ollama primary advisory produced real rounds;
- NPU auditor produced real audit evidence.
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_optional_json(repo_root: Path, value: str, *, required: bool) -> tuple[dict[str, Any], list[str], str]:
    if not value:
        return {}, ["required input argument missing"] if required else [], ""
    path = resolve_path(repo_root, value)
    rel = repo_rel(repo_root, path)
    if not path.exists():
        return {}, [f"required input missing: {rel}"] if required else [f"optional input missing: {rel}"], rel
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report validation must capture details.
        return {}, [f"{rel}: {type(exc).__name__}: {exc}"], rel
    if not isinstance(data, dict):
        return {}, [f"{rel}: JSON root is not an object"], rel
    return data, [], rel


def safe_int(value: Any, default: int = 0) -> int:
    if isinstance(value, bool):
        return default
    try:
        if value in (None, ""):
            return default
        return int(value)
    except (TypeError, ValueError):
        return default


def safe_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def first_text(*values: Any) -> str:
    for value in values:
        if value not in (None, ""):
            return str(value)
    return ""


def is_fallback_artifact(report: dict[str, Any]) -> bool:
    return str(report.get("classification") or "") == "required_provider_artifact_missing"


def gpu_provider_evidence(gpu_report: dict[str, Any]) -> dict[str, Any]:
    rounds = safe_list(gpu_report.get("rounds"))
    round_count = safe_int(gpu_report.get("round_count"), len(rounds))
    provider_performed = bool(gpu_report.get("provider_execution_performed"))
    provider_empty = bool(gpu_report.get("provider_empty_response") or gpu_report.get("provider_empty_response_count"))
    provider_error = first_text(gpu_report.get("provider_error"), "; ".join(map(str, safe_list(gpu_report.get("errors")))))
    real = bool(
        gpu_report
        and not is_fallback_artifact(gpu_report)
        and provider_performed
        and round_count > 0
        and not provider_empty
    )
    return {
        "real": real,
        "passed": gpu_report.get("passed"),
        "provider_execution_performed": provider_performed,
        "round_count": round_count,
        "recommendation_count": safe_int(gpu_report.get("recommendation_count")),
        "provider_empty_response": provider_empty,
        "classification": gpu_report.get("classification"),
        "provider_error": provider_error,
    }


def npu_provider_evidence(orchestrator: dict[str, Any]) -> dict[str, Any]:
    audits = [item for item in safe_list(orchestrator.get("npu_audits")) if isinstance(item, dict)]
    success_count = sum(
        1
        for item in audits
        if item.get("provider_execution_succeeded") is True
        or item.get("provider_execution_performed") is True
        or item.get("classification") == "usable_audit_text"
    )
    load_attempt_count = sum(1 for item in audits if item.get("provider_load_attempted") is True)
    requested_count = sum(1 for item in audits if item.get("provider_execution_requested") is True)
    return {
        "real": success_count > 0,
        "audit_count": len(audits),
        "requested_count": requested_count,
        "load_attempt_count": load_attempt_count,
        "success_count": success_count,
        "lane_mode": orchestrator.get("npu_lane_mode"),
        "lane": orchestrator.get("npu_lane") if isinstance(orchestrator.get("npu_lane"), dict) else {},
    }


def probe_evidence(probe: dict[str, Any]) -> dict[str, Any]:
    lane_reports = [item for item in safe_list(probe.get("lane_reports")) if isinstance(item, dict)]
    out: dict[str, Any] = {
        "present": bool(probe),
        "passed": probe.get("passed"),
        "provider_execution_performed": bool(probe.get("provider_execution_performed")),
        "lane_count": len(lane_reports),
        "lanes": {},
    }
    lanes: dict[str, Any] = {}
    for item in lane_reports:
        lane = str(item.get("lane") or "unknown")
        parsed = item.get("parsed_result") if isinstance(item.get("parsed_result"), dict) else {}
        lanes[lane] = {
            "passed": item.get("passed"),
            "provider_execution_performed": item.get("provider_execution_performed"),
            "text_chars": parsed.get("text_chars"),
            "error": first_text(item.get("error"), parsed.get("error")),
            "selected_model": item.get("selected_model"),
        }
    out["lanes"] = lanes
    return out


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    errors: list[str] = []
    warnings: list[str] = []

    orchestrator, orch_errors, orch_path = read_optional_json(repo_root, args.orchestrator, required=True)
    gpu_report, gpu_errors, gpu_path = read_optional_json(repo_root, args.gpu_report, required=True)
    gpu_npu_sync, sync_errors, sync_path = read_optional_json(repo_root, args.gpu_npu_sync, required=False)
    local_probe, probe_errors, probe_path = read_optional_json(repo_root, args.local_provider_probe, required=False)

    errors.extend(orch_errors)
    errors.extend(gpu_errors)
    warnings.extend(sync_errors)
    warnings.extend(probe_errors)

    gpu = gpu_provider_evidence(gpu_report)
    npu = npu_provider_evidence(orchestrator)
    probe = probe_evidence(local_probe)

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
    if is_fallback_artifact(gpu_report):
        errors.append("GPU report is a required_provider_artifact_missing fallback, not real provider evidence")
    if is_fallback_artifact(orchestrator):
        errors.append("orchestrator report is a required_provider_artifact_missing fallback, not real provider evidence")
    if orchestrator and orchestrator.get("gpu_returncode") not in (None, 0):
        errors.append(f"GPU subprocess returned non-zero exit code: {orchestrator.get('gpu_returncode')}")
    if local_probe and local_probe.get("passed") is False:
        warnings.append(f"local provider probe degraded: {local_probe.get('errors')}")

    provider_execution_observed = bool(gpu["real"] or npu["real"])
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
        },
        "gpu": gpu,
        "npu": npu,
        "local_probe": probe,
        "gpu_npu_sync_metrics": gpu_npu_sync.get("metrics") if isinstance(gpu_npu_sync.get("metrics"), dict) else {},
        "decision": {
            "gpu_provider_ready": gpu["real"],
            "npu_auditor_ready": npu["real"],
            "probe_only_is_not_provider_evidence": True,
            "strict_provider_contract_satisfied": not errors,
            "recommended_next_action": "run_full0to10_provider_lane" if errors else "continue_bundle_review",
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
    lines = ["# Provider Evidence Contract", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    lines.append(f"- GPU real provider evidence: `{gpu.get('real')}`")
    lines.append(f"- GPU round count: `{gpu.get('round_count')}`")
    lines.append(f"- GPU provider error: `{gpu.get('provider_error')}`")
    lines.append(f"- NPU real auditor evidence: `{npu.get('real')}`")
    lines.append(f"- NPU audit count: `{npu.get('audit_count')}`")
    lines.append(f"- NPU success count: `{npu.get('success_count')}`")
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--orchestrator", required=True)
    parser.add_argument("--gpu-report", required=True)
    parser.add_argument("--gpu-npu-sync", default="")
    parser.add_argument("--local-provider-probe", default="output/validation/local_provider_probe.json")
    parser.add_argument("--require-gpu-provider", action="store_true")
    parser.add_argument("--require-npu-auditor", action="store_true")
    parser.add_argument("--output", default="output/validation/provider_evidence_contract.json")
    parser.add_argument("--markdown-output", default="output/validation/provider_evidence_contract.md")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_path(repo_root, args.output)
    markdown = resolve_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
