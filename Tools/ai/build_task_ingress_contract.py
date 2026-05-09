#!/usr/bin/env python3
"""Build task ingress contract for unified heap/exchange runs.

The task Markdown is the external request entering the system. This report binds
that request to the heap/exchange runtime so downstream evidence, peer runtime,
closure audit and final review PR product can prove where the work originated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover
    from report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


def repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def extract_headings(text: str, limit: int = 30) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            headings.append(stripped)
            if len(headings) >= limit:
                break
    return headings


def classify_intent(text: str) -> dict[str, Any]:
    lower = text.lower()
    signals = {
        "requests_code_change": any(token in lower for token in ("patch", "modifica", "codice", "script", "fix", "refactor", "implement")),
        "requests_review_pr_product": any(token in lower for token in ("pr", "pull request", "review", "merge")),
        "mentions_heap_exchange": any(token in lower for token in ("heap", "exchange", "heep", "escange")),
        "mentions_provider_peers": any(token in lower for token in ("gpu0", "gpu1", "npu", "provider")),
        "mentions_shared_memory": any(token in lower for token in ("memoria", "memory", "shared", "ai-to-ai", "bundle")),
    }
    return {
        "signals": signals,
        "requires_reviewable_product": bool(signals["requests_code_change"] or signals["requests_review_pr_product"]),
        "requires_heap_exchange": bool(signals["mentions_heap_exchange"] or signals["mentions_provider_peers"] or signals["mentions_shared_memory"]),
    }


def append_jsonl(path: Path | None, event: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(event)
    payload.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    path.open("a", encoding="utf-8", newline="\n").write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Task Ingress Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Task file: `{report.get('task_file')}`",
        f"- SHA256: `{report.get('task_sha256')}`",
        f"- Requires heap/exchange: `{report.get('intent', {}).get('requires_heap_exchange')}`",
        f"- Requires reviewable product: `{report.get('intent', {}).get('requires_reviewable_product')}`",
        "",
        "## Headings",
        "",
    ]
    headings = report.get("headings") or []
    if headings:
        lines.extend(f"- `{heading}`" for heading in headings)
    else:
        lines.append("- none")
    lines.extend(
        [
            "",
            "## Contract",
            "",
            "The task Markdown is the ingress request. It must be visible to heap/exchange runtime evidence and must be traceable to the final reviewable PR product.",
            "",
        ]
    )
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--task-file", required=True)
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--markdown-output", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    task_path = repo_path(repo_root, args.task_file)
    runtime_state = repo_path(repo_root, args.runtime_state) if args.runtime_state else None
    observer_dir = repo_path(repo_root, args.observer_dir) if args.observer_dir else None

    errors: list[str] = []
    warnings: list[str] = []
    text = ""

    if not task_path.exists():
        errors.append(f"task file missing: {task_path}")
    elif not task_path.is_file():
        errors.append(f"task path is not a file: {task_path}")
    else:
        text = task_path.read_text(encoding="utf-8-sig", errors="replace")
        if not text.strip():
            errors.append("task Markdown is empty")

    intent = classify_intent(text)
    report = {
        "schema_version": 1,
        "kind": "task_ingress_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": args.stamp,
        "passed": not errors,
        "task_file": rel(repo_root, task_path),
        "task_sha256": sha256_text(text) if text else "",
        "line_count": len(text.splitlines()) if text else 0,
        "char_count": len(text),
        "headings": extract_headings(text),
        "intent": intent,
        "source_of_knowledge": "heap_exchange",
        "expected_final_product": "reviewable_pr_with_concrete_changes",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }

    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown_output)

    append_jsonl(
        runtime_state,
        {
            "kind": "task_ingress_contract",
            "schema_version": 1,
            "stamp": args.stamp,
            "task_file": report["task_file"],
            "task_sha256": report["task_sha256"],
            "requires_heap_exchange": intent["requires_heap_exchange"],
            "requires_reviewable_product": intent["requires_reviewable_product"],
            "summary": "task Markdown ingress contract registered in heap/exchange runtime state",
            "source_file": rel(repo_root, output),
        },
    )

    if observer_dir:
        append_jsonl(
            observer_dir / "ai_public_events.jsonl",
            {
                "kind": "ai_public_exchange_event",
                "schema_version": 1,
                "lane": "ingress",
                "speaker": "task_ingress_contract",
                "event_type": "task_ingress",
                "stamp": args.stamp,
                "task_file": report["task_file"],
                "task_sha256": report["task_sha256"],
                "summary": "Task Markdown entered heap/exchange as source request",
                "source_file": rel(repo_root, output),
                "raw_thinking_exposed": False,
            },
        )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
