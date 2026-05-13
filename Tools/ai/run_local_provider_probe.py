#!/usr/bin/env python3
"""Run explicit local provider probes and normalize their results.

This tool is opt-in and report-only. It can run a tiny Ollama generation probe
and a tiny OpenVINO NPU device/tensor probe, then parses the already-obtained
results through app-agnostic provider result helpers.

It does not run Blender, does not generate scene code and does not change the
legacy dual-AI runtime pipeline.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any


def ensure_repo_imports(repo_root: Path) -> None:
    for path in (repo_root, repo_root / "Tools" / "npu"):
        text = str(path)
        if text not in sys.path:
            sys.path.insert(0, text)


def heap_patch_prompt_required(prompt: str) -> bool:
    """Return True when the provider prompt is a heap proposal-generation task."""
    text = (prompt or "").lower()
    markers = (
        "heap chunk/composer contract",
        "startup_context_digest_for_gpu1",
        "external heap revision context",
        "target_files",
        "forced concrete delta required",
        "proposal chunks",
    )
    return any(marker in text for marker in markers)


def build_heap_patch_proposal_prompt(prompt: str) -> str:
    """Wrap heap prompts so GPU1 cannot answer with a documentation summary.

    The heap already sends large startup context and previous pointer history.
    Without a final, stronger contract at the end of the prompt, local LLMs tend
    to summarize the docs section repeatedly. This wrapper keeps the full context
    available but makes the final instruction unambiguous and quality-gate aware:
    emit a concrete patch proposal with repo-relative targets, diff/code markers,
    validation commands and an explicit exit decision.
    """
    if not heap_patch_prompt_required(prompt):
        return prompt
    return (
        "IA-CARMINE GPU1 PROVIDER MODE: CONCRETE PATCH PROPOSAL ONLY.\n"
        "You are not a documentation summarizer. You are the GPU1 patch planner inside the heap.\n"
        "Use the context, pointers, startup artifacts, memory hits, source anchors and prior vetoes below as evidence.\n"
        "Your output is consumed by deterministic quality gates. Generic summaries are invalid.\n\n"
        "BEGIN_HEAP_CONTEXT_AND_POINTERS\n"
        f"{prompt.rstrip()}\n"
        "END_HEAP_CONTEXT_AND_POINTERS\n\n"
        "FINAL OUTPUT CONTRACT - OBEY EXACTLY:\n"
        "Return one Markdown block for the NEXT concrete heap delta only. Do not try to solve the whole project in one response.\n"
        "The heap persists pointer history, proposal chunks, provider reports and revision context; use them as working memory.\n"
        "At startup, inspect the whole universe and create a mental work queue, but emit only the current patchable delta.\n"
        "When a later delta introduces imports/symbols/contracts that affect earlier blocks, move backward using BACKTRACK_PROPAGATE, then resume forward.\n"
        "GPU0_REVIEW_REQUEST and NPU_AUDIT_REQUEST are real peer work orders: write them so the next heap cycle can verify this delta.\n\n"
        "# HEAP_DELTA_PROPOSAL\n"
        "EXIT_DECISION=PATCHABLE_TARGET\n"
        "POINTER_ACTION=STAY_FORWARD | BACKTRACK_PROPAGATE | RESUME_FORWARD | SPLIT_TASKS | NO_PATCHABLE_TARGET\n"
        "CURRENT_POINTER:\n"
        "- previous_block_id=<id-or-empty>\n"
        "- refines_block_id=<id-or-empty>\n"
        "- resume_from_block_id=<id-or-empty>\n\n"
        "CURRENT_ITERATION_SCOPE:\n"
        "- State the single concrete slice handled in this revision.\n"
        "- Keep unresolved work in BACKLOG_TASKS instead of answering everything now.\n\n"
        "TARGET_FILES:\n"
        "- tools/.../real_existing_file.py\n\n"
        "PROBLEM:\n"
        "- Describe the concrete runtime/code defect in one or two bullets.\n\n"
        "EVIDENCE:\n"
        "- Cite concrete artifact paths, function names, report fields or error strings from the heap context.\n\n"
        "IMPLEMENTATION_CHANGES:\n"
        "- Describe exact code changes, functions, arguments and control-flow changes for this delta only.\n\n"
        "PROPAGATION_TASKS:\n"
        "- If this delta introduces an import, symbol, schema field, CLI flag or contract, list older blocks/files that must be revisited.\n"
        "- Use POINTER_ACTION=BACKTRACK_PROPAGATE when propagation must happen before moving forward.\n\n"
        "BACKLOG_TASKS:\n"
        "- List later chunks that should be handled after this delta.\n"
        "- Each backlog item must include target file candidates and validation evidence needed.\n\n"
        "GPU0_REVIEW_REQUEST:\n"
        "- Ask GPU0 to verify concrete file/path/diff validity for this delta, not just hardware readiness.\n\n"
        "NPU_AUDIT_REQUEST:\n"
        "- Ask NPU to audit guardrails, placeholder risk, source-write claims and validation commands for this delta.\n\n"
        "PATCH_SKETCH:\n"
        "```diff\n"
        "diff --git a/tools/.../real_existing_file.py b/tools/.../real_existing_file.py\n"
        "@@\n"
        "- old concrete behavior\n"
        "+ new concrete behavior\n"
        "```\n\n"
        "VALIDATION_COMMANDS:\n"
        "```powershell\n"
        "$RepoPy = (Resolve-Path .\\.venv\\Scripts\\python.exe).Path\n"
        "$env:PYTHONPATH = (Resolve-Path .).Path\n"
        "& $RepoPy -m py_compile .\\Tools\\...\\real_existing_file.py\n"
        "```\n\n"
        "RISKS:\n"
        "- State compatibility risk and rollback path.\n\n"
        "EXIT_DECISION_RULES:\n"
        "- Use EXIT_DECISION=PATCHABLE_TARGET when at least one exact repo-relative target file is patchable now.\n"
        "- Use POINTER_ACTION=BACKTRACK_PROPAGATE when this delta requires modifying earlier assumptions/imports/contracts before continuing.\n"
        "- Use POINTER_ACTION=RESUME_FORWARD only after propagation tasks are resolved.\n"
        "- Use EXIT_DECISION=NO_PATCHABLE_TARGET only when no concrete edit is possible from supplied evidence; still list closest real target files and missing evidence.\n"
        "- Never output a README/docs/project summary.\n"
        "- Never repeat a previous proposal if the heap veto reported similarity >= 0.95.\n"
        "- Never emit TODO/FIXME/placeholder/pass-only code.\n"
    )


def run_ollama_probe(
    repo_root: Path,
    model: str | None,
    prompt: str | None = None,
    max_new_tokens: int = 64,
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.npu.ollama_runtime import (  # noqa: PLC0415
        OllamaSession,
        choose_model,
        is_server_ready,
        list_models,
        list_models_from_disk,
    )
    from Tools.npu.pipeline import parse_provider_result  # noqa: PLC0415

    started = time.perf_counter()
    models = list_models() if is_server_ready() else list_models_from_disk()
    selected_model = choose_model(model, models)
    if not selected_model:
        return {
            "lane": "ollama",
            "passed": False,
            "provider_execution_performed": False,
            "error": "no Ollama model available",
            "elapsed_sec": round(time.perf_counter() - started, 4),
        }
    if prompt and prompt.strip():
        prompts = [prompt.strip()]
    else:
        prompts = [
            'Return exactly this JSON object and no prose: {"ok": true, "lane": "ollama"}',
            '{"ok": true, "lane": "ollama"}',
        ]

    text = ""
    prompt_attempts: list[dict[str, Any]] = []
    with OllamaSession(
        model=selected_model, shutdown_server=False, unload_model=True
    ) as session:
        for index, prompt in enumerate(prompts, start=1):
            candidate = session.generate(
                prompt,
                max_new_tokens=max_new_tokens,
                temperature=0.0,
            )
            candidate = candidate or ""
            prompt_attempts.append(
                {
                    "attempt": index,
                    "prompt_chars": len(prompt),
                    "text_chars": len(candidate),
                    "text_preview": candidate[:120],
                    "max_new_tokens": max_new_tokens,
                }
            )
            if candidate.strip():
                text = candidate
                break

    parsed = parse_provider_result(
        {"response": text},
        provider="ollama",
        model=selected_model,
        executed=True,
        allow_json=True,
    )
    empty_output = not text.strip()
    return {
        "lane": "ollama",
        "passed": (not empty_output) and (parsed.ok or bool(prompt and prompt.strip())),
        "provider_execution_performed": True,
        "elapsed_sec": round(time.perf_counter() - started, 4),
        "selected_model": selected_model,
        "request_prompt": prompt or "",
        "response_text": text.strip(),
        "model_count": len(models),
        "server_ready": is_server_ready(),
        "empty_output": empty_output,
        "error": "empty Ollama generation output" if empty_output else None,
        "parsed_result": parsed.to_dict(),
        "prompt_attempts": prompt_attempts,
        "text_preview": text[:200],
    }


def run_npu_probe(
    repo_root: Path, timeout: float, npu_python_exe: str | None = None
) -> dict[str, Any]:
    ensure_repo_imports(repo_root)
    from Tools.npu.npu_runtime import (  # noqa: PLC0415
        DEFAULT_NPU_PYTHON,
        _parse_last_json_line,
        _run_python,
    )
    from Tools.npu.pipeline import parse_provider_result  # noqa: PLC0415

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
    python_exe = (
        Path(npu_python_exe).expanduser() if npu_python_exe else DEFAULT_NPU_PYTHON
    )
    ok, text, exit_code = _run_python(python_exe, code, timeout=timeout)
    parsed_payload = (
        _parse_last_json_line(text) if ok else {"error": text, "exit_code": exit_code}
    )
    parsed = parse_provider_result(
        {"text": json.dumps(parsed_payload)},
        provider="openvino_npu",
        model="device_probe",
        executed=True,
        allow_json=True,
    )
    return {
        "lane": "npu",
        "passed": (
            ok and bool(parsed_payload.get("ok"))
            if isinstance(parsed_payload, dict)
            else False
        ),
        "provider_execution_performed": True,
        "elapsed_sec": round(time.perf_counter() - started, 4),
        "parsed_result": parsed.to_dict(),
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
            lane_reports.append(
                run_ollama_probe(
                    repo_root,
                    args.model,
                    effective_prompt,
                    max_new_tokens=max(1, min(args.max_new_tokens, 4096)),
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
                run_npu_probe(repo_root, args.timeout, args.npu_python_exe)
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
            {
                "text": json.dumps(
                    {"lane": item.get("lane"), "passed": item.get("passed")}
                )
            },
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
    parser.add_argument(
        "--output", default="output/validation/local_provider_probe.json"
    )
    parser.add_argument("--model", help="Preferred Ollama model.")
    parser.add_argument(
        "--prompt",
        default="",
        help="Optional user prompt for observable provider response.",
    )
    parser.add_argument(
        "--prompt-file",
        default="",
        help="Optional UTF-8 file containing the provider prompt.",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    parser.add_argument(
        "--max-new-tokens",
        type=int,
        default=64,
        help="Maximum Ollama tokens for an observable response.",
    )
    parser.add_argument(
        "--npu-python-exe", default="", help="Explicit NPU/OpenVINO Python executable."
    )
    parser.add_argument("--run-ollama", action="store_true")
    parser.add_argument("--run-npu", action="store_true")
    args = parser.parse_args()

    if not args.run_ollama and not args.run_npu:
        parser.error(
            "At least one explicit probe flag is required: --run-ollama or --run-npu"
        )

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root, args)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "provider_execution_performed": report["provider_execution_performed"],
            },
            indent=2,
        )
    )
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
