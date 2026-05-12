#!/usr/bin/env python3
"""Smoke test for the report-only Ollama tool gateway.

The smoke does not contact Ollama. It validates import/compile and basic path
policy guardrails for the gateway module.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import py_compile
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT = "output/validation/ollama_tool_gateway_smoke.json"
DEFAULT_MARKDOWN = "output/validation/ollama_tool_gateway_smoke.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def load_gateway(repo_root: Path) -> Any:
    target = repo_root / "Tools" / "ai" / "ollama_tool_gateway.py"
    spec = importlib.util.spec_from_file_location("ollama_tool_gateway_smoke_target", target)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load ollama_tool_gateway module spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_report(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    gateway_path = repo_root / "Tools" / "ai" / "ollama_tool_gateway.py"

    try:
        py_compile.compile(str(gateway_path), doraise=True)
    except py_compile.PyCompileError as exc:
        errors.append(f"py_compile failed: {exc}")

    module = None
    if not errors:
        try:
            module = load_gateway(repo_root)
        except Exception as exc:  # noqa: BLE001 - smoke report.
            errors.append(f"module load failed: {type(exc).__name__}: {exc}")

    policy_checks: list[dict[str, Any]] = []
    if module is not None:
        samples = {
            "AGENTS.md": "",
            ".claude/settings.local.json": "path is explicitly denied",
            "output/runtime.json": "path prefix is denied",
            "indexAI/code_chunks/demo.md": "path prefix is denied",
            "docs/token_dump.md": "path fragment is denied",
        }
        for sample_path, expected_error in samples.items():
            actual = module.path_policy_error(sample_path)
            passed = actual == expected_error
            policy_checks.append(
                {
                    "path": sample_path,
                    "expected": expected_error,
                    "actual": actual,
                    "passed": passed,
                }
            )
            if not passed:
                errors.append(
                    f"policy mismatch for {sample_path}: expected {expected_error!r}, got {actual!r}"
                )

    return {
        "schema_version": 1,
        "kind": "ollama_tool_gateway_smoke",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "ollama_request_performed": False,
        "gateway_path": repo_rel(gateway_path, repo_root),
        "policy_checks": policy_checks,
        "guardrails": {
            "report_only": True,
            "provider_execution_performed": False,
            "ollama_request_performed": False,
            "patch_application_performed": False,
            "git_write_performed": False,
            "source_writes_performed": False,
            "blender_runtime_touched": False,
        },
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Ollama Tool Gateway Smoke", ""]
    for key in (
        "passed",
        "provider_execution_performed",
        "ollama_request_performed",
        "patch_application_performed",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.append("")
    lines.append("## Policy checks")
    lines.append("")
    for item in report.get("policy_checks", []):
        lines.append(f"- `{item['path']}` passed=`{item['passed']}` actual=`{item['actual']}`")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    markdown = Path(args.markdown_output)
    if not output.is_absolute():
        output = repo_root / output
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": report["passed"], "output": str(output), "markdown": str(markdown)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
