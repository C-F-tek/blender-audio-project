#!/usr/bin/env python3
"""Build the heap/exchange runtime exit product.

The runtime center is allowed to be dynamic. This exit tool validates the only
thing that must be deterministic at the boundary: the run must expose concrete
reviewable operations, or fail with a precise reason before a misleading PR is
created.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.validation.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )

CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}


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


def load_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, "not provided"
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not an object"
    return data, None


def load_jsonl(path: Path | None) -> tuple[list[dict[str, Any]], str | None]:
    if path is None:
        return [], "not provided"
    if not path.exists():
        return [], "missing"
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, line in enumerate(
        path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1
    ):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"line {index}: {type(exc).__name__}: {exc}")
            continue
        if isinstance(value, dict):
            events.append(value)
    return events, "; ".join(errors) if errors else None


def append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    event = dict(event)
    event.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    path.open("a", encoding="utf-8", newline="\n").write(
        json.dumps(event, ensure_ascii=False, sort_keys=True) + "\n"
    )


def write_public_event(observer_dir: Path | None, event: dict[str, Any]) -> None:
    if observer_dir is None:
        return
    payload = {
        "kind": "ai_public_exchange_event",
        "schema_version": 1,
        "lane": "heap_exchange",
        "speaker": "runtime_exit",
        "event_type": event.get("kind", "heap_exit"),
        "summary": event.get("summary", "heap/exchange runtime exit product built"),
        "source_file": event.get("source_file", ""),
        "raw_thinking_exposed": False,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "stamp": event.get("stamp", ""),
    }
    append_jsonl(observer_dir / "ai_public_events.jsonl", payload)


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


def concrete_ops_from_apply(report: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not report:
        return []
    concrete: list[dict[str, Any]] = []
    for item in report.get("results") or []:
        if not isinstance(item, dict):
            continue
        op = str(item.get("operation") or "").strip().lower()
        if op in CONCRETE_OPERATION_NAMES:
            concrete.append(item)
    operation_count = int(report.get("operation_count") or 0)
    if operation_count and not concrete:
        concrete.append(
            {
                "operation_count": operation_count,
                "source": "apply_report_operation_count",
            }
        )
    return concrete


def concrete_candidates_from_runtime(
    events: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    candidates: list[dict[str, Any]] = []
    for event in events:
        kind = str(event.get("kind") or event.get("event_type") or "").lower()
        op = str(event.get("operation") or "").strip().lower()
        if kind in {
            "concrete_operation_candidate",
            "heap_exit_product",
            "patch_spec_candidate",
        } and (op in CONCRETE_OPERATION_NAMES or event.get("operation_count")):
            candidates.append(event)
    return candidates


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Exchange Runtime Exit Product",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Runtime event count: `{report.get('runtime_event_count')}`",
        f"- Concrete operation count: `{report.get('concrete_operation_count')}`",
        f"- Changed count: `{report.get('changed_count')}`",
        "",
        "## Boundary rule",
        "",
        "The dynamic heap/exchange center may choose its internal route. The exit boundary must expose concrete deterministic operations or stop before review PR creation.",
        "",
    ]
    if report.get("concrete_operations"):
        lines.extend(["## Concrete operations", ""])
        for item in report["concrete_operations"][:50]:
            lines.append(
                f"- `{item.get('path', item.get('source', 'runtime'))}` op=`{item.get('operation', item.get('operation_count'))}` changed=`{item.get('changed', '')}`"
            )
    if report.get("manual_review_items"):
        lines.extend(["", "## Manual review items", ""])
        for item in report["manual_review_items"][:50]:
            lines.append(
                f"- `{item.get('id')}` {item.get('reason')} targets=`{item.get('target_files')}`"
            )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--runtime-entry", default="")
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--apply-report", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--require-concrete-product", action="store_true")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp
    packets_dir = repo_root / "output" / "ai_packets" / stamp

    runtime_entry_path = repo_path(repo_root, args.runtime_entry) or (
        packets_dir / "heap_exchange_runtime_entry.json"
    )
    runtime_state_path = repo_path(repo_root, args.runtime_state) or (
        packets_dir / "heap_exchange_runtime_state.jsonl"
    )
    apply_report_path = repo_path(repo_root, args.apply_report) or discover_first(
        repo_root,
        [
            f"output/validation/*patch_suggestion_bundle_apply*{stamp}*.json",
            f"output/validation/*generated_patch_specs*{stamp}*.json",
        ],
    )
    observer_dir = repo_path(repo_root, args.observer_dir) or discover_first(
        repo_root, [f"output/local_ai_runs/*{stamp}*_observer"]
    )
    output = repo_path(repo_root, args.output) or (
        packets_dir / "heap_exchange_runtime_exit_product.json"
    )
    markdown_output = repo_path(repo_root, args.markdown_output) or (
        packets_dir / "heap_exchange_runtime_exit_product.md"
    )

    runtime_entry, entry_error = load_json(runtime_entry_path)
    runtime_events, runtime_error = load_jsonl(runtime_state_path)
    apply_report, apply_error = load_json(apply_report_path)

    concrete_operations = concrete_ops_from_apply(apply_report)
    runtime_candidates = concrete_candidates_from_runtime(runtime_events)
    if runtime_candidates and not concrete_operations:
        concrete_operations.extend(runtime_candidates)

    manual_items = []
    if apply_report and isinstance(apply_report.get("manual_review_items"), list):
        manual_items = apply_report.get("manual_review_items", [])[:200]

    changed_count = int(apply_report.get("changed_count") or 0) if apply_report else 0
    operation_count = (
        int(apply_report.get("operation_count") or 0) if apply_report else len(concrete_operations)
    )
    errors: list[str] = []
    warnings: list[str] = []
    if entry_error:
        errors.append(f"runtime entry invalid: {entry_error}")
    if runtime_error:
        errors.append(f"runtime state invalid: {runtime_error}")
    if apply_error:
        warnings.append(f"apply report unavailable at exit: {apply_error}")
    if args.require_concrete_product and not concrete_operations:
        errors.append("heap/exchange exit has no concrete deterministic operation candidate")
    if args.require_concrete_product and operation_count <= 0:
        errors.append("heap/exchange exit has operation_count=0")

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_runtime_exit_product",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "runtime_entry": rel(repo_root, runtime_entry_path),
        "runtime_state": rel(repo_root, runtime_state_path),
        "apply_report": rel(repo_root, apply_report_path),
        "observer_dir": rel(repo_root, observer_dir),
        "center_was_dynamic": bool(
            runtime_entry and runtime_entry.get("center_is_dynamic") is True
        ),
        "runtime_event_count": len(runtime_events),
        "operation_count": operation_count,
        "changed_count": changed_count,
        "concrete_operation_count": len(concrete_operations),
        "concrete_operations": concrete_operations[:200],
        "manual_review_required": bool(manual_items),
        "manual_review_items": manual_items,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    write_json_report(report, resolve_output_path(repo_root, output.as_posix()))
    write_text_report(
        render_markdown(report),
        resolve_output_path(repo_root, markdown_output.as_posix()),
    )
    append_jsonl(
        runtime_state_path,
        {
            "kind": "heap_exit",
            "schema_version": 1,
            "stamp": stamp,
            "summary": "heap/exchange runtime exit evaluated",
            "passed": report["passed"],
            "concrete_operation_count": len(concrete_operations),
        },
    )
    write_public_event(
        observer_dir,
        {
            "kind": "heap_exit",
            "stamp": stamp,
            "summary": f"heap/exchange exit concrete_ops={len(concrete_operations)} passed={report['passed']}",
            "source_file": rel(repo_root, output),
        },
    )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
