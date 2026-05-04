#!/usr/bin/env python3
"""Validate textual quality of AI workload reports.

Default contract:
- The important input is an output packet folder, by default output/ai_packets.
- A launcher may pass a run-scoped folder such as output/ai_packets/<DATASTAMP>.
- A launcher may also pass output/ai_packets; the tool then scans all immediate timestamp packet folders.
- The tool selects existing known workload reports from the selected folder set.
- Missing known reports are serialized as unselected/unavailable warnings by default.
- Explicit --report lane=path remains strict: a caller-selected missing report is blocking.

This validator is report-only. It does not execute providers, does not call
Ollama/NPU/GPU, and does not modify legacy runtime outputs.
"""
from __future__ import annotations

import argparse
import string
from pathlib import Path
from typing import Any

from report_utils import resolve_output_path, write_json_report

DEFAULT_REPORT_DIR = "output/ai_packets"
KNOWN_WORKLOAD_REPORTS = (
    ("npu", "npu_real_workload_report.md"),
    ("ollama", "ollama_gpu_real_workload_report.md"),
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


def relative_or_absolute_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()



def output_packet_report_dirs(repo_root: Path, report_dir: Path) -> list[Path]:
    """Return concrete packet directories selected by --report-dir.

    If --report-dir points to output/ai_packets, accept all immediate child
    directories as run packet folders. If it points to output/ai_packets/<stamp>,
    keep the selection scoped to that single run directory.
    """
    resolved_dir = report_dir if report_dir.is_absolute() else repo_root / report_dir
    if not resolved_dir.exists() or not resolved_dir.is_dir():
        return [resolved_dir]

    dirs: list[Path] = [resolved_dir]
    try:
        for child in sorted(resolved_dir.iterdir()):
            if child.is_dir():
                dirs.append(child)
    except OSError:
        pass

    seen: set[str] = set()
    unique: list[Path] = []
    for item in dirs:
        key = str(item.resolve(strict=False)).lower()
        if key in seen:
            continue
        seen.add(key)
        unique.append(item)
    return unique


def collect_output_folder_report_specs(
    repo_root: Path,
    report_dir: Path,
    *,
    include_missing_known_reports: bool = False,
) -> tuple[list[tuple[str, str]], list[dict[str, Any]]]:
    selected: list[tuple[str, str]] = []
    unselected: list[dict[str, Any]] = []
    selected_paths: set[str] = set()

    for packet_dir in output_packet_report_dirs(repo_root, report_dir):
        for lane, filename in KNOWN_WORKLOAD_REPORTS:
            candidate = packet_dir / filename
            key = str(candidate.resolve(strict=False)).lower()
            if candidate.exists() or include_missing_known_reports:
                if key not in selected_paths:
                    selected_paths.add(key)
                    selected.append((lane, str(candidate)))
            else:
                unselected.append({
                    "lane": lane,
                    "packet_dir": relative_or_absolute_path(packet_dir, repo_root),
                    "path": relative_or_absolute_path(candidate, repo_root),
                    "reason": "known_workload_report_missing_from_selected_output_folder",
                })

        known_names = {filename for _, filename in KNOWN_WORKLOAD_REPORTS}
        if packet_dir.exists() and packet_dir.is_dir():
            for candidate in sorted(packet_dir.glob("*workload_report*.md")):
                if candidate.name in known_names:
                    continue
                key = str(candidate.resolve(strict=False)).lower()
                if key in selected_paths:
                    continue
                lane = candidate.stem.replace("_real_workload_report", "").replace("_workload_report", "")
                lane = lane.replace("-", "_") or "unknown"
                selected_paths.add(key)
                selected.append((lane, str(candidate)))

    return selected, unselected

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
    rel_path = relative_or_absolute_path(path, repo_root)
    role = lane_role(lane)
    if not path.exists():
        return {
            "path": rel_path,
            "lane": lane,
            "provider": role["provider"],
            "compute_lane": role["compute_lane"],
            "exists": False,
            "usable": False,
            "classification": "missing_explicit_report",
            "advisory_use": advisory_use(lane, False),
            "provider_execution_performed": False,
            "errors": ["explicitly selected report file is missing"],
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
        "routing_policy": "selected_output_folder_workload_reports_only",
    }


def check_ai_workload_report_quality(
    repo_root: Path,
    report_specs: list[tuple[str, str]],
    *,
    selection_mode: str,
    report_dir: Path,
    unselected_known_reports: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
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

    unselected = list(unselected_known_reports or [])
    for item in unselected:
        warnings.append(
            f"{item.get('lane', 'unknown')}: known workload report not selected: {item.get('reason', 'unavailable')}"
        )

    if not results:
        warnings.append("no workload reports selected from output folder")

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
        "policy": "selected_output_folder_workload_reports_only",
        "mode": "report_only_workload_quality_gate",
        "selection_mode": selection_mode,
        "report_dir": relative_or_absolute_path(report_dir, repo_root),
        "packet_dirs": [
            relative_or_absolute_path(item, repo_root)
            for item in output_packet_report_dirs(repo_root, report_dir)
        ],
        "selected_reports": [
            {
                "lane": lane,
                "path": relative_or_absolute_path(Path(raw_path), repo_root),
            }
            for lane, raw_path in report_specs
        ],
        "unselected_known_reports": unselected,
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
    parser.add_argument("--report-dir", default=DEFAULT_REPORT_DIR)
    parser.add_argument("--report", action="append", default=[], help="Strict report spec as lane=path. Repeatable or comma-separated.")
    parser.add_argument(
        "--include-missing-known-reports",
        action="store_true",
        help="Include missing known lane reports as explicit selected reports. Missing selected reports then fail.",
    )
    parser.add_argument("--output", help="Optional JSON report path.")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report_dir = Path(args.report_dir)
    if not report_dir.is_absolute():
        report_dir = repo_root / report_dir

    specs: list[tuple[str, str]] = []
    selection_mode = "output_folder"
    unselected_known_reports: list[dict[str, Any]] = []

    for item in split_path_values(list(args.report or [])):
        if "=" not in item:
            parser.error(f"Invalid --report value, expected lane=path: {item}")
        lane, raw_path = item.split("=", 1)
        specs.append((lane.strip(), raw_path.strip()))

    if specs:
        selection_mode = "explicit_reports"
    else:
        specs, unselected_known_reports = collect_output_folder_report_specs(
            repo_root,
            report_dir,
            include_missing_known_reports=args.include_missing_known_reports,
        )
        if args.include_missing_known_reports:
            selection_mode = "output_folder_with_missing_known_reports"

    report = check_ai_workload_report_quality(
        repo_root,
        specs,
        selection_mode=selection_mode,
        report_dir=report_dir,
        unselected_known_reports=unselected_known_reports,
    )
    output = resolve_output_path(repo_root, args.output) if args.output else None
    text = write_json_report(report, output)
    print(text, end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
