#!/usr/bin/env python3
"""Run explicit local provider probes and normalize report-only results."""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Any
import sys

repo_root_for_import = Path(__file__).resolve().parents[3]
if str(repo_root_for_import) not in sys.path:
    sys.path.insert(0, str(repo_root_for_import))

from Tools.ai._shared.provider_ollama_probe import run_ollama_probe
from Tools.ai._shared.provider_probe_paths import ensure_repo_imports


def run_npu_probe(
    repo_root: Path,
    timeout: float,
    npu_python_exe: str | None = None,
    prompt: str | None = None,
    max_new_tokens: int = 64,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.npu.provider_mesh._shared.npu_runtime import (  # noqa: PLC0415
        DEFAULT_NPU_PYTHON,
        _parse_last_json_line,
        _run_python,
    )
    from Tools.npu.pipeline import parse_provider_result  # noqa: PLC0415
    from Tools.ai._shared.provider_tool_loop import openvino_tool_loop_report  # noqa: PLC0415
    started = time.perf_counter()
    code = r"""
import json
import numpy as np
import openvino as ov
core = ov.Core()
devices = core.available_devices
result = {"ok": "NPU" in devices, "lane": "npu", "devices": devices}
print(json.dumps(result))
"""
    python_exe = Path(npu_python_exe).expanduser() if npu_python_exe else DEFAULT_NPU_PYTHON
    ok, text, exit_code = _run_python(python_exe, code, timeout=timeout)
    parsed_payload = _parse_last_json_line(text) if ok else {"error": text, "exit_code": exit_code}
    parsed = parse_provider_result(
        {"text": json.dumps(parsed_payload)},
        provider="openvino_npu",
        model="device_probe",
        executed=True,
        allow_json=True,
    )
    tool_loop = openvino_tool_loop_report(
        repo_root=repo_root,
        prompt=prompt or "List the broker tool call you would request for code validation.",
        timeout_seconds=timeout,
        max_new_tokens=max(1, min(max_new_tokens, 512)),
        python_exe=str(python_exe),
        device="NPU",
    )
    return {
        "lane": "npu",
        "passed": (
            ok and bool(parsed_payload.get("ok")) if isinstance(parsed_payload, dict) else False
        ),
        "provider_execution_performed": True,
        "elapsed_sec": round(time.perf_counter() - started, 4),
        "parsed_result": parsed.to_dict(),
        "openvino_native_tool_loop": tool_loop,
        "native_tool_loop_provider": "openvino_genai",
        "native_tool_loop_requested": True,
        "native_tool_loop_supported": bool(tool_loop.get("native_tool_loop_supported")),
        "native_tool_loop_performed": bool(tool_loop.get("native_tool_loop_performed")),
        "native_tool_call_count": int(tool_loop.get("native_tool_call_count") or 0),
        "tool_calls": tool_loop.get("tool_calls") or [],
        "raw_exit_code": exit_code,
        "raw_preview": text[:300],
    }

def read_prompt_file(repo_root: Path, prompt_file: str) -> str:
    """Read an optional provider prompt from disk.

    This keeps large heap/GPU1 prompts out of Windows argv and makes the exact
    provider input inspectable as a run artifact.
    """
    if not prompt_file:
        return ""
    path = Path(prompt_file)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig")

def build_report(repo_root: Path, args: argparse.Namespace) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.ai._shared.provider_tool_loop import build_heap_patch_proposal_prompt  # noqa: PLC0415
    from Tools.npu.pipeline import (  # noqa: PLC0415
        build_provider_result_report,
        parse_provider_result,
    )

    lane_reports: list[dict[str, Any]] = []
    errors: list[str] = []
    effective_prompt = args.prompt
    if getattr(args, "prompt_file", ""):
        try:
            file_prompt = read_prompt_file(repo_root, args.prompt_file)
            if file_prompt.strip():
                effective_prompt = file_prompt
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            errors.append(f"prompt_file: {type(exc).__name__}: {exc}")
    if args.run_ollama:
        try:
            effective_prompt = build_heap_patch_proposal_prompt(effective_prompt)
            partial_output = Path(args.output)
            if not partial_output.is_absolute():
                partial_output = repo_root / partial_output
            lane_reports.append(
                run_ollama_probe(
                    repo_root,
                    args.model,
                    effective_prompt,
                    max_new_tokens=max(1, min(args.max_new_tokens, 4096)),
                    num_ctx=args.ollama_num_ctx,
                    keep_alive=args.keep_alive,
                    partial_output=partial_output,
                )
            )
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            lane_reports.append(
                {
                    "lane": "ollama",
                    "passed": False,
                    "provider_execution_performed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
    if args.run_npu:
        try:
            lane_reports.append(
                run_npu_probe(
                    repo_root,
                    args.timeout,
                    args.npu_python_exe,
                    effective_prompt,
                    max_new_tokens=max(1, min(args.max_new_tokens, 512)),
                )
            )
        except Exception as exc:  # noqa: BLE001 - report-only tool.
            lane_reports.append(
                {
                    "lane": "npu",
                    "passed": False,
                    "provider_execution_performed": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    parsed_results = [
        parse_provider_result(
            {"text": json.dumps({"lane": item.get("lane"), "passed": item.get("passed")})},
            provider=str(item.get("lane") or "unknown"),
            model=str(item.get("selected_model") or "probe"),
            executed=bool(item.get("provider_execution_performed")),
            allow_json=True,
        )
        for item in lane_reports
    ]
    provider_report = build_provider_result_report(
        provider="local_probe",
        model=args.model or "auto",
        results=parsed_results,
        provider_execution_performed=any(
            item.get("provider_execution_performed") for item in lane_reports
        ),
    )
    for item in lane_reports:
        if item.get("passed") is False:
            errors.append(f"{item.get('lane')}: {item.get('error') or 'probe failed'}")

    return {
        "schema_version": 1,
        "kind": "local_provider_probe",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": any(
            item.get("provider_execution_performed") for item in lane_reports
        ),
        "lane_reports": lane_reports,
        "provider_result_report": provider_report,
    }

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/local_provider_probe.json")
    parser.add_argument("--model", help="Preferred Ollama model.")
    parser.add_argument("--prompt", default="")
    parser.add_argument("--prompt-file", default="")
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument("--max-new-tokens", type=int, default=64)
    parser.add_argument("--ollama-num-ctx", type=int, default=16384)
    parser.add_argument("--keep-alive", default="0s")
    parser.add_argument("--npu-python-exe", default="")
    parser.add_argument("--run-ollama", action="store_true")
    parser.add_argument("--run-npu", action="store_true")
    args = parser.parse_args()
    if not args.run_ollama and not args.run_npu:
        parser.error("At least one explicit probe flag is required: --run-ollama or --run-npu")
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    summary = {
        "passed": report["passed"],
        "output": str(output),
        "provider_execution_performed": report["provider_execution_performed"],
    }
    print(json.dumps(summary, indent=2))
    return 0 if report["passed"] else 2

if __name__ == "__main__":
    raise SystemExit(main())
