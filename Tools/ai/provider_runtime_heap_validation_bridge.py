#!/usr/bin/env python3
"""Publish deterministic validation reports into the provider runtime heap."""
from __future__ import annotations

import argparse
import glob
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_runtime_heap import ProviderRuntimeHeap  # type: ignore
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

DEFAULT_OUTPUT = "output/validation/provider_runtime_heap_validation_bridge_{stamp}.json"
DEFAULT_MARKDOWN = "output/validation/provider_runtime_heap_validation_bridge_{stamp}.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_report(path: Path) -> tuple[dict[str, Any], str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - validation bridge must report unreadable inputs.
        return {}, f"{type(exc).__name__}: {exc}"
    return (data if isinstance(data, dict) else {}), ""


def expand_report_files(repo_root: Path, values: list[str], globs: list[str], stamp: str) -> list[Path]:
    paths: list[Path] = []
    for value in values:
        path = resolve_output_path(repo_root, value)
        if path.exists() and path not in paths:
            paths.append(path)
    for pattern in globs:
        normalized = pattern.format(stamp=stamp)
        full_pattern = str(resolve_output_path(repo_root, normalized))
        for match in sorted(glob.glob(full_pattern, recursive=True)):
            path = Path(match).resolve()
            if path.is_file() and path.suffix.lower() == ".json" and path not in paths:
                paths.append(path)
    return paths


def report_payload(repo_root: Path, path: Path, data: dict[str, Any], read_error: str) -> dict[str, Any]:
    guardrails = data.get("guardrails") if isinstance(data.get("guardrails"), dict) else {}
    return {
        "source_report": repo_rel(repo_root, path),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "errors": data.get("errors", [read_error] if read_error else []),
        "warnings": data.get("warnings", []),
        "provider_execution_performed": bool(data.get("provider_execution_performed") or guardrails.get("provider_execution_performed")),
        "patch_application_performed": bool(data.get("patch_application_performed") or guardrails.get("patch_application_performed")),
        "source_writes_performed": bool(data.get("source_writes_performed") or guardrails.get("source_writes_performed")),
        "validator_authority": "deterministic_cpu_validation_lane",
    }


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(repo_root, args.stamp, args.events, args.snapshot, args.heap_markdown)
    report_paths = expand_report_files(repo_root, args.report_file, args.report_glob, args.stamp)

    events: list[dict[str, Any]] = []
    errors: list[str] = []
    failed_reports = 0

    for index, path in enumerate(report_paths, start=1):
        data, read_error = read_report(path)
        payload = report_payload(repo_root, path, data, read_error)
        if read_error:
            errors.append(f"{repo_rel(repo_root, path)}: {read_error}")
        if payload.get("passed") is False:
            failed_reports += 1
        events.append(
            heap.append_event(
                source="deterministic",
                target=args.target or None,
                event_type="validation_signal",
                correlation_id=f"validation-{index:03d}",
                payload=payload,
            )
        )

    snapshot = heap.write_snapshot()
    if args.require_all_passed and failed_reports:
        errors.append(f"{failed_reports} validation report(s) reported passed=false")

    return {
        "schema_version": 1,
        "kind": "provider_runtime_heap_validation_bridge",
        "generated_at": now_iso(),
        "stamp": args.stamp,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "report_count": len(report_paths),
        "validation_signal_event_count": len(events),
        "failed_report_count": failed_reports,
        "heap_snapshot": {
            "event_count": snapshot.get("event_count"),
            "pending_broker_request_count": snapshot.get("pending_broker_request_count"),
            "event_log": snapshot.get("event_log"),
        },
        "reports": [repo_rel(repo_root, path) for path in report_paths],
        "guardrails": {
            "provider_execution_performed": False,
            "direct_tool_execution_allowed": False,
            "broker_required_for_tool_execution": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Runtime Heap Validation Bridge", ""]
    for key in ("passed", "stamp", "report_count", "validation_signal_event_count", "failed_report_count"):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.append("")
    lines.append("## Reports")
    lines.append("")
    for path in report.get("reports", []):
        lines.append(f"- `{path}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--target", default="gpu1")
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument("--report-glob", action="append", default=[])
    parser.add_argument("--require-all-passed", action="store_true")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve_output_path(repo_root, args.output.format(stamp=args.stamp))
    markdown = resolve_output_path(repo_root, args.markdown_output.format(stamp=args.stamp))
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 1


if __name__ == "__main__":
    raise SystemExit(main())
