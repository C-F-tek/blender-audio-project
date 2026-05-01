#!/usr/bin/env python3
"""Validate textual quality of AI workload reports.

This validator is report-only. It evaluates already-generated AI workload output
files, such as NPU/OpenVINO and Ollama/GPU reports, and classifies each report as
usable or unusable for downstream packet/proposal context.

It does not execute providers, does not call Ollama/NPU/GPU, and does not modify
legacy runtime outputs.
"""
from __future__ import annotations

import argparse
import json
import string
from pathlib import Path
from typing import Any

from report_utils import resolve_output_path, write_json_report

DEFAULT_REPORTS = (
    ("npu", "output/ai_packets/npu_real_workload_report.md"),
    ("ollama", "output/ai_packets/ollama_gpu_real_workload_report.md"),
)

LANE_ROLES = {
    "ollama": {
        "provider": "ollama",
        "compute_lane": "gpu_cuda",
        "allowed_role_when_usable": "primary_advisory",
        "execution_mode": "explicit_only",
    },
    "npu": {
        "provider": "openvino_npu",
        "compute_lane": "npu",
        "allowed_role_when_usable": "knowledge_broker_or_probe",
        "execution_mode": "explicit_only",
    },
}

HEXISH_CHARS = set("0123456789abcdefABCDEF, .\n\r\t")
PRINTABLE = set(string.printable)


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def text_metrics(text: str) -> dict[str, Any]:
    total = len(text)
    alpha = sum(1 for char in text if char.isalpha())
    digits = sum(1 for char in text if char.isdigit())
    spaces = sum(1 for char in text if char.isspace())
    printable = sum(1 for char in text if char in PRINTABLE or char.isprintable())
    hexish = sum(1 for char in text if char in HEXISH_CHARS)
    words = [word for word in text.replace("`", " ").replace("#", " ").split() if any(ch.isalpha() for ch in word)]
    markdown_headings = sum(1 for line in text.splitlines() if line.strip().startswith("#"))
    sentence_markers = sum(text.count(item) for item in (". ", ":", ";", "\n- ", "\n1."))
    return {
        "chars": total,
        "alpha_chars": alpha,
        "digit_chars": digits,
        "space_chars": spaces,
        "printable_chars": printable,
        "hexish_chars": hexish,
        "word_count": len(words),
        "markdown_heading_count": markdown_headings,
        "sentence_marker_count": sentence_markers,
        "alpha_ratio": round(alpha / total, 4) if total else 0.0,
        "digit_ratio": round(digits / total, 4) if total else 0.0,
        "hexish_ratio": round(hexish / total, 4) if total else 0.0,
        "printable_ratio": round(printable / total, 4) if total else 0.0,
    }


def lane_role(lane: str) -> dict[str, Any]:
    return dict(LANE_ROLES.get(lane, {
        "provider": lane or "unknown",
        "compute_lane": "unknown",
        "allowed_role_when_usable": "context_only",
        "execution_mode": "explicit_only",
    }))


def advisory_use(lane: str, usable: bool) -> dict[str, Any]:
    role = lane_role(lane)
    if not usable:
        return {
            "allowed_as_advisory_context": False,
            "allowed_role": "excluded_from_advisory_context",
            "reason": "unusable_workload_report",
        }
    if lane == "ollama":
        return {
            "allowed_as_advisory_context": True,
            "allowed_role": "primary_advisory",
            "reason": "usable_text_primary_advisory_lane",
        }
    if lane == "npu":
        return {
            "allowed_as_advisory_context": False,
            "allowed_role": role["allowed_role_when_usable"],
            "reason": "npu_is_not_primary_advisory_lane",
        }
    return {
        "allowed_as_advisory_context": True,
        "allowed_role": role["allowed_role_when_usable"],
        "reason": "usable_text_context_lane",
    }


def classify_report(path: Path, *, lane: str, repo_root: Path) -> dict[str, Any]:
    rel_path = path.relative_to(repo_root).as_posix() if path.is_absolute() and path.is_relative_to(repo_root) else str(path)
    role = lane_role(lane)
    if not path.exists():
        return {
            "path": rel_path,
            "lane": lane,
            "provider": role["provider"],
            "compute_lane": role["compute_lane"],
            "exists": False,
            "usable": False,
            "classification": "missing",
            "advisory_use": advisory_use(lane, False),
            "provider_execution_performed": False,
            "errors": ["report file is missing"],
            "warnings": [],
            "metrics": {},
        }

    text = path.read_text(encoding="utf-8", errors="replace")
    metrics = text_metrics(text)
    errors: list[str] = []
    warnings: list[str] = []

    if metrics["chars"] < 120:
        errors.append("report is too short to be useful")
    if metrics["alpha_ratio"] < 0.18:
        errors.append("alphabetic character ratio is too low")
    if metrics["word_count"] < 20:
        errors.append("word count is too low")
    if metrics["hexish_ratio"] > 0.82 and metrics["alpha_ratio"] < 0.28:
        errors.append("report appears numeric/hex-like rather than natural language")
    if metrics["printable_ratio"] < 0.95:
        errors.append("report contains too many non-printable characters")
    if metrics["markdown_heading_count"] == 0 and metrics["sentence_marker_count"] < 3:
        warnings.append("report lacks Markdown headings and has few sentence markers")

    usable = not errors
    classification = "usable_text" if usable else "unusable_output"
    return {
        "path": rel_path,
        "lane": lane,
        "provider": role["provider"],
        "compute_lane": role["compute_lane"],
        "exists": True,
        "usable": usable,
        "classification": classification,
        "advisory_use": advisory_use(lane, usable),
        "provider_execution_performed": False,
        "errors": errors,
        "warnings": warnings,
        "metrics": metrics,
    }


def quality_decision(results: list[dict[str, Any]]) -> dict[str, Any]:
    usable_lanes = [item["lane"] for item in results if item.get("usable")]
    unusable_lanes = [item["lane"] for item in results if not item.get("usable")]
    ollama_primary = any(item["lane"] == "ollama" and item.get("usable") for item in results)
    npu_usable = any(item["lane"] == "npu" and item.get("usable") for item in results)
    npu_excluded = any(item["lane"] == "npu" and not item.get("advisory_use", {}).get("allowed_as_advisory_context") for item in results)
    return {
        "usable_lanes": usable_lanes,
        "unusable_lanes": unusable_lanes,
        "ollama_gpu_primary_advisory_allowed": ollama_primary,
        "npu_report_text_usable": npu_usable,
        "npu_excluded_from_primary_advisory": npu_excluded,
        "provider_execution_seen": False,
        "source_writes_performed": False,
        "routing_policy": "usable_text_lanes_only_for_advisory_context",
    }


def check_ai_workload_report_quality(repo_root: Path, report_specs: list[tuple[str, str]]) -> dict[str, Any]:
    results: list[dict[str, Any]] = []
    for lane, raw_path in report_specs:
        path = Path(raw_path)
        if not path.is_absolute():
            path = repo_root / path
        results.append(classify_report(path, lane=lane, repo_root=repo_root))

    blocking_errors = [
        f"{item['lane']}: {error}"
        for item in results
        for error in item.get("errors", [])
    ]
    warnings = [
        f"{item['lane']}: {warning}"
        for item in results
        for warning in item.get("warnings", [])
    ]
    usable_lanes = [item["lane"] for item in results if item.get("usable")]
    unusable_lanes = [item["lane"] for item in results if not item.get("usable")]

    return {
        "schema_version": 1,
        "kind": "ai_workload_report_quality",
        "repo_root": str(repo_root),
        "passed": not blocking_errors,
        "errors": blocking_errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "source_writes_performed": False,
        "policy": "usable_text_lanes_only_for_advisory_context",
        "mode": "report_only_workload_quality_gate",
        "usable_lanes": usable_lanes,
        "unusable_lanes": unusable_lanes,
        "decision": quality_decision(results),
        "checks": {
            "report_count": len(results),
            "usable_count": len(usable_lanes),
            "unusable_count": len(unusable_lanes),
            "results": results,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--report", action="append", default=[], help="Report spec as lane=path. Repeatable or comma-separated.")
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    specs: list[tuple[str, str]] = []
    for item in split_path_values(list(args.report or [])):
        if "=" not in item:
            parser.error(f"Invalid --report value, expected lane=path: {item}")
        lane, raw_path = item.split("=", 1)
        specs.append((lane.strip(), raw_path.strip()))
    if not specs:
        specs = list(DEFAULT_REPORTS)

    report = check_ai_workload_report_quality(repo_root, specs)
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
