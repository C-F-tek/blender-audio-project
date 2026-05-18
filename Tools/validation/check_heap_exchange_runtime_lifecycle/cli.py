#!/usr/bin/env python3
"""Validate heap/exchange runtime lifecycle evidence.

This validator checks the entry/exit envelope only. It intentionally does not
assert a fixed internal order for GPU/provider/NPU/runtime lanes.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai.heap_exchange.io import load_jsonl

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def repo_path(repo_root: Path, raw: str) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def discover_first(repo_root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(
            repo_root.glob(pattern),
            key=lambda item: item.stat().st_mtime if item.exists() else 0,
            reverse=True,
        )
        if matches:
            return matches[0]
    return None


def load_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, "not provided"
    if not path.exists():
        return None, "missing"
    try:
        value = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(value, dict):
        return None, "json root is not an object"
    return value, None


def event_kind(event: dict[str, Any]) -> str:
    return str(event.get("kind") or event.get("event_type") or "").strip().lower()


def add_check(
    checks: list[dict[str, Any]],
    *,
    name: str,
    passed: bool,
    expected: str,
    actual: str,
    action: str,
    artifacts: list[str] | None = None,
) -> None:
    checks.append(
        {
            "name": name,
            "passed": bool(passed),
            "expected": expected,
            "actual": actual,
            "action": action,
            "artifacts": artifacts or [],
        }
    )


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Exchange Runtime Lifecycle",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Broken check count: `{len(report.get('broken_checks') or [])}`",
        "",
        "## Checks",
        "",
        "| Check | Passed | Actual | Action |",
        "|---|---:|---|---|",
    ]
    for check in report.get("checks") or []:
        lines.append(
            f"| `{check.get('name')}` | `{check.get('passed')}` | {str(check.get('actual')).replace('|', '/')} | {str(check.get('action')).replace('|', '/')} |"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--runtime-entry", default="")
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--runtime-exit", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--require-public-events", action="store_true")
    parser.add_argument("--require-concrete-exit", action="store_true")
    parser.add_argument("--require-knowledge-surface", action="store_true")
    parser.add_argument("--min-available-lanes", type=int, default=2)
    parser.add_argument(
        "--output", default="output/validation/heap_exchange_runtime_lifecycle.json"
    )
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp
    packets_dir = repo_root / "output" / "ai_packets" / stamp

    entry_path = repo_path(repo_root, args.runtime_entry) or (
        packets_dir / "heap_exchange_runtime_entry.json"
    )
    state_path = repo_path(repo_root, args.runtime_state) or (
        packets_dir / "heap_exchange_runtime_state.jsonl"
    )
    exit_path = repo_path(repo_root, args.runtime_exit) or (
        packets_dir / "heap_exchange_runtime_exit_product.json"
    )
    observer_dir = repo_path(repo_root, args.observer_dir) or discover_first(
        repo_root, [f"output/local_ai_runs/*{stamp}*_observer"]
    )
    public_path = observer_dir / "ai_public_events.jsonl" if observer_dir else None

    entry, entry_error = load_json(entry_path)
    runtime_events, state_error = load_jsonl(state_path)
    exit_report, exit_error = load_json(exit_path)
    public_events, public_error = load_jsonl(public_path)

    checks: list[dict[str, Any]] = []
    available_lanes = int(entry.get("available_lane_count") or 0) if entry else 0
    entry_dynamic = bool(entry and entry.get("center_is_dynamic") is True)
    add_check(
        checks,
        name="entry_exists_and_dynamic",
        passed=bool(entry and not entry_error and entry_dynamic),
        expected="heap_exchange_runtime_entry exists and center_is_dynamic=true",
        actual=f"entry_error={entry_error} center_is_dynamic={entry_dynamic}",
        action="Run python -m Tools.ai heap_exchange_runtime_entry after agent-state/workload routing.",
        artifacts=[rel(repo_root, entry_path)],
    )

    knowledge = entry.get("knowledge_surface") if entry else None
    knowledge_events = [
        event for event in runtime_events if event_kind(event) == "knowledge_surface_registered"
    ]
    knowledge_ok = True
    if args.require_knowledge_surface:
        knowledge_ok = bool(
            isinstance(knowledge, dict)
            and entry.get("source_of_knowledge") == "heap_exchange"
            and knowledge.get("source_of_knowledge") == "heap_exchange"
            and knowledge.get("routing_model") == "dynamic_exchange_not_static_chain"
            and knowledge.get("static_chain_invocation_performed") is False
            and knowledge_events
        )
    add_check(
        checks,
        name="knowledge_surface_dynamic_not_static_chain",
        passed=knowledge_ok,
        expected="entry records heap_exchange knowledge surface and runtime state records knowledge_surface_registered"
        if args.require_knowledge_surface
        else "not required",
        actual=f"source_of_knowledge={(entry or {}).get('source_of_knowledge')} routing_model={(knowledge or {}).get('routing_model') if isinstance(knowledge, dict) else None} static_chain={(knowledge or {}).get('static_chain_invocation_performed') if isinstance(knowledge, dict) else None} knowledge_events={len(knowledge_events)}",
        action="Build entry with heap_exchange knowledge_surface and append knowledge_surface_registered event.",
        artifacts=[rel(repo_root, entry_path), rel(repo_root, state_path)],
    )

    add_check(
        checks,
        name="runtime_lanes_available",
        passed=available_lanes >= args.min_available_lanes,
        expected=f"available_lane_count >= {args.min_available_lanes}",
        actual=f"available_lane_count={available_lanes}",
        action="Register at least context/provider plus one hardware/runtime lane at entry.",
        artifacts=[rel(repo_root, entry_path)],
    )
    state_kinds = {event_kind(event) for event in runtime_events}
    add_check(
        checks,
        name="runtime_state_has_entry_and_lanes",
        passed=not state_error and "heap_entry" in state_kinds and "lane_registered" in state_kinds,
        expected="runtime_state jsonl contains heap_entry and lane_registered events",
        actual=f"state_error={state_error} event_kinds={sorted(state_kinds)} count={len(runtime_events)}",
        action="Append lifecycle events to heap_exchange_runtime_state.jsonl during entry/runtime/exit.",
        artifacts=[rel(repo_root, state_path)],
    )
    public_ok = True
    if args.require_public_events:
        public_kinds = {event_kind(event) for event in public_events}
        public_ok = not public_error and len(public_events) > 0
        public_actual = f"public_error={public_error} count={len(public_events)} event_kinds={sorted(public_kinds)}"
    else:
        public_actual = "not required"
    add_check(
        checks,
        name="public_exchange_events",
        passed=public_ok,
        expected="ai_public_events.jsonl has observable heap/exchange events"
        if args.require_public_events
        else "not required",
        actual=public_actual,
        action="Use Write-UnifiedRunAiPublicEvent or equivalent event emission in entry/runtime/exit.",
        artifacts=[rel(repo_root, public_path)],
    )
    concrete_count = int(exit_report.get("concrete_operation_count") or 0) if exit_report else 0
    exit_passed = bool(exit_report and not exit_error and exit_report.get("passed") is True)
    concrete_ok = exit_passed and (concrete_count > 0 if args.require_concrete_exit else True)
    add_check(
        checks,
        name="exit_product_concrete",
        passed=concrete_ok,
        expected="heap exit product exists and has concrete_operation_count > 0"
        if args.require_concrete_exit
        else "heap exit product exists and passed",
        actual=f"exit_error={exit_error} passed={exit_passed} concrete_operation_count={concrete_count}",
        action="Build heap exchange exit product after generated patch spec bridge and before PR product creation.",
        artifacts=[rel(repo_root, exit_path)],
    )

    broken = [check for check in checks if not check["passed"]]
    report = {
        "schema_version": 1,
        "kind": "heap_exchange_runtime_lifecycle",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": stamp,
        "passed": not broken,
        "checks": checks,
        "broken_checks": broken,
        "errors": [f"{check['name']}: {check['actual']}" for check in broken],
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    if args.markdown_output:
        write_text_report(
            render_markdown(report), resolve_output_path(repo_root, args.markdown_output)
        )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
