#!/usr/bin/env python3
"""Validate the live provider gate for IA-Carmine real-product runs.

The gate is intentionally stricter than static preflight contracts: when the
real product launcher requests the provider/advisory lane, a current provider
probe must prove that the requested live lanes executed and passed. This avoids
falling through to metadata-only proposal products when Ollama/provider lanes
silently degrade.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_json_object(path: Path) -> tuple[dict[str, Any] | None, str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - validation report should carry parse errors.
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, f"expected JSON object, got {type(data).__name__}"
    return data, ""


def lane_by_name(report: dict[str, Any], name: str) -> dict[str, Any] | None:
    for item in report.get("lane_reports") or []:
        if isinstance(item, dict) and str(item.get("lane") or "").lower() == name.lower():
            return item
    return None


def lane_summary(lane: dict[str, Any] | None) -> dict[str, Any]:
    if not lane:
        return {"present": False, "passed": False, "provider_execution_performed": False}
    return {
        "present": True,
        "passed": bool(lane.get("passed")),
        "provider_execution_performed": bool(lane.get("provider_execution_performed")),
        "selected_model": lane.get("selected_model") or lane.get("model"),
        "server_ready": lane.get("server_ready"),
        "empty_output": lane.get("empty_output"),
        "error": lane.get("error"),
        "elapsed_sec": lane.get("elapsed_sec"),
    }


def validate_gate(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    probe_path = Path(args.provider_probe)
    if not probe_path.is_absolute():
        probe_path = repo_root / probe_path

    errors: list[str] = []
    warnings: list[str] = []
    probe, read_error = read_json_object(probe_path)
    if read_error or probe is None:
        return {
            "schema_version": 1,
            "kind": "real_product_live_provider_gate",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "repo_root": repo_root.as_posix(),
            "provider_probe": str(probe_path),
            "passed": False,
            "errors": [f"provider probe is not readable: {read_error}"],
            "warnings": warnings,
            "provider_execution_performed": False,
            "checks": {},
            "lanes": {},
        }

    if probe.get("kind") != "local_provider_probe":
        errors.append("provider probe kind must be local_provider_probe")
    if probe.get("passed") is not True:
        errors.append("provider probe did not pass")
    if probe.get("provider_execution_performed") is not True:
        errors.append("provider probe did not perform live provider execution")

    lanes: dict[str, dict[str, Any]] = {}
    required_lanes: list[str] = []
    if args.require_ollama:
        required_lanes.append("ollama")
    if args.require_npu:
        required_lanes.append("npu")

    for name in required_lanes:
        lane = lane_by_name(probe, name)
        summary = lane_summary(lane)
        lanes[name] = summary
        if not summary["present"]:
            errors.append(f"required provider lane missing: {name}")
            continue
        if not summary["passed"]:
            errors.append(f"required provider lane did not pass: {name}")
        if not summary["provider_execution_performed"]:
            errors.append(f"required provider lane did not execute live provider work: {name}")

    if args.require_ollama and args.model:
        selected = str(lanes.get("ollama", {}).get("selected_model") or "")
        if not selected:
            errors.append("ollama lane did not report a selected model")
        elif selected != args.model:
            errors.append(f"ollama lane selected model {selected!r}, expected {args.model!r}")

    checks = {
        "probe_exists": probe_path.exists(),
        "probe_kind_ok": probe.get("kind") == "local_provider_probe",
        "probe_passed": probe.get("passed") is True,
        "probe_provider_execution_performed": probe.get("provider_execution_performed") is True,
        "required_lanes": required_lanes,
    }

    return {
        "schema_version": 1,
        "kind": "real_product_live_provider_gate",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "provider_probe": probe_path.as_posix(),
        "required_model": args.model or "",
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": probe.get("provider_execution_performed") is True,
        "checks": checks,
        "lanes": lanes,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Real Product Live Provider Gate", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Provider execution performed: `{report.get('provider_execution_performed')}`")
    lines.append(f"- Provider probe: `{report.get('provider_probe')}`")
    lines.append(f"- Required model: `{report.get('required_model')}`")
    lines.append("")
    lines.append("| Lane | Present | Passed | Executed | Selected model | Error |")
    lines.append("|---|---:|---:|---:|---|---|")
    for name, lane in (report.get("lanes") or {}).items():
        lines.append(
            f"| {name} | {lane.get('present')} | {lane.get('passed')} | "
            f"{lane.get('provider_execution_performed')} | `{lane.get('selected_model') or ''}` | "
            f"{lane.get('error') or ''} |"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report.get("errors") or [])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report.get("warnings") or [])
    lines.append("")
    lines.append("This is a live gate. Static contracts cannot satisfy it.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--provider-probe", required=True)
    parser.add_argument("--model", default="")
    parser.add_argument("--require-ollama", action="store_true")
    parser.add_argument("--require-npu", action="store_true")
    parser.add_argument(
        "--output", default="output/validation/real_product_live_provider_gate.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/real_product_live_provider_gate.md"
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = validate_gate(repo_root, args)
    output = resolve_output_path(repo_root, args.output)
    markdown = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
