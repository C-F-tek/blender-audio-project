#!/usr/bin/env python3
"""Build provider-result reports from existing or simulated payloads.

This script is runtime-safe and report-only. It never executes providers, never
opens Ollama/NPU sessions, never touches Blender, and never mutates legacy
runtime outputs. It only consumes payloads that already exist or deterministic
inline samples and writes a normalized provider_result_report JSON.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def ensure_repo_imports(repo_root: Path) -> None:
    text = str(repo_root)
    if text not in sys.path:
        sys.path.insert(0, text)


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def load_json_payload(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def sample_payloads() -> list[dict[str, Any]]:
    return [
        {
            "provider": "ollama",
            "model": "sample-model",
            "payload": {"response": '```json\n{"ok": true, "lane": "ollama"}\n```'},
            "allow_json": True,
        },
        {
            "provider": "openvino_npu",
            "model": "device-probe",
            "payload": {"text": '{"ok": true, "lane": "npu"}'},
            "allow_json": True,
        },
        {
            "provider": "openai_compatible",
            "model": "sample-chat-model",
            "payload": {
                "choices": [{"message": {"content": "plain text response"}}],
                "usage": {"total_tokens": 4},
            },
            "allow_json": False,
        },
    ]


def normalize_input_payloads(repo_root: Path, args: argparse.Namespace) -> list[dict[str, Any]]:
    payloads: list[dict[str, Any]] = []
    for raw_path in split_path_values(args.payload or []):
        path = Path(raw_path)
        if not path.is_absolute():
            path = repo_root / path
        payloads.append(
            {
                "provider": args.provider,
                "model": args.model,
                "payload": load_json_payload(path),
                "allow_json": not args.no_json_parse,
                "source_path": path.relative_to(repo_root).as_posix()
                if path.is_relative_to(repo_root)
                else str(path),
            }
        )
    for raw_inline in args.inline_json or []:
        payloads.append(
            {
                "provider": args.provider,
                "model": args.model,
                "payload": json.loads(raw_inline),
                "allow_json": not args.no_json_parse,
                "source_path": "inline-json",
            }
        )
    if args.use_samples or not payloads:
        payloads.extend(sample_payloads())
    return payloads


def build_report(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.npu.pipeline import (  # noqa: PLC0415
        build_provider_result_report,
        parse_provider_result,
    )

    payloads = normalize_input_payloads(repo_root, args)
    parsed_results = [
        parse_provider_result(
            item["payload"],
            provider=str(item.get("provider") or args.provider),
            model=str(item.get("model") or args.model),
            executed=False,
            allow_json=bool(item.get("allow_json", True)),
        )
        for item in payloads
    ]
    report = build_provider_result_report(
        provider=args.provider,
        model=args.model,
        results=parsed_results,
        provider_execution_performed=False,
    )
    report.update(
        {
            "repo_root": str(repo_root),
            "mode": "runtime_safe_report_only",
            "payload_count": len(payloads),
            "payload_sources": [item.get("source_path", "sample") for item in payloads],
        }
    )
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--provider", default="runtime_safe_payload")
    parser.add_argument("--model", default="payload-only")
    parser.add_argument(
        "--payload",
        action="append",
        default=[],
        help="Existing provider payload JSON file. Repeatable or comma-separated.",
    )
    parser.add_argument(
        "--inline-json",
        action="append",
        default=[],
        help="Inline provider payload JSON object. Repeatable.",
    )
    parser.add_argument(
        "--use-samples", action="store_true", help="Include deterministic sample payloads."
    )
    parser.add_argument("--no-json-parse", action="store_true")
    parser.add_argument("--output", default="output/validation/provider_result_report.json")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report.get("passed"),
                "output": str(output),
                "provider_execution_performed": report.get("provider_execution_performed"),
            },
            indent=2,
        )
    )
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
