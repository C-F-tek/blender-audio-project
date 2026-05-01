#!/usr/bin/env python3
"""Run a non-blocking NPU auditor over a GPU deep planning review.

The NPU lane is intentionally a smoke/audit guardrail, not primary advisory.
This tool prepares a compact context from the GPU/Ollama deep-planning report
and optionally invokes Tools/npu/run_npu_review.py with OpenVINO/NPU. Any NPU
failure or unusable output is captured as a warning and never blocks the GPU
review or patch-planning flow.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_GPU_REVIEW = "output/ai_pipeline/agent_gpu_deep_planning_review.json"
DEFAULT_CONTEXT = "output/ai_pipeline/npu_gpu_deep_review_audit_context.md"
DEFAULT_NPU_OUT = "output/ai_pipeline/npu_gpu_deep_review_audit.md"
DEFAULT_NPU_NOTES = "output/ai_pipeline/npu_gpu_deep_review_audit_notes.md"
DEFAULT_NPU_METADATA = "output/validation/npu_gpu_deep_review_audit_metadata.json"
DEFAULT_OUTPUT = "output/validation/npu_gpu_deep_review_audit.json"
DEFAULT_MARKDOWN = "output/validation/npu_gpu_deep_review_audit.md"


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve()


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def compact_json(data: Any, max_chars: int) -> str:
    text = json.dumps(data, indent=2, ensure_ascii=False)
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]"
    return text


def build_context(gpu_review: dict[str, Any]) -> str:
    recommendations = gpu_review.get("recommendations", [])
    decision = gpu_review.get("decision", {})
    rounds = gpu_review.get("rounds", [])
    compact_rounds = []
    for item in rounds[:8]:
        compact_rounds.append(
            {
                "round": item.get("round"),
                "elapsed_seconds": item.get("elapsed_seconds"),
                "file_count": item.get("file_count"),
                "files": item.get("files", [])[:20],
                "parsed_response": item.get("parsed_response", {}),
            }
        )
    payload = {
        "role": "NPU audit guardrail for GPU/Ollama deep planning review",
        "instructions": [
            "Audit the GPU review for drift, over-broad patch plans, unsupported claims, missing evidence and guardrail violations.",
            "Do not create a patch.",
            "Do not act as primary advisory provider.",
            "Return concise Markdown with: Verdict, Drift Risks, Evidence Gaps, Guardrail Notes, Non-blocking Recommendation.",
        ],
        "gpu_review_summary": {
            "kind": gpu_review.get("kind"),
            "passed": gpu_review.get("passed"),
            "provider_execution_performed": gpu_review.get("provider_execution_performed"),
            "patch_application_performed": gpu_review.get("patch_application_performed"),
            "model_used": gpu_review.get("model_used"),
            "round_count": gpu_review.get("round_count"),
            "recommendation_count": gpu_review.get("recommendation_count"),
            "decision": decision,
            "guardrails": gpu_review.get("guardrails", {}),
        },
        "recommendations": recommendations,
        "rounds": compact_rounds,
    }
    return "# NPU GPU Deep Review Audit Context\n\n" + compact_json(payload, 42000) + "\n"


def text_metrics(text: str) -> dict[str, Any]:
    chars = len(text)
    alpha = sum(1 for char in text if char.isalpha())
    digit = sum(1 for char in text if char.isdigit())
    words = [part for part in text.replace("\n", " ").split(" ") if part.strip()]
    return {
        "chars": chars,
        "alpha_chars": alpha,
        "digit_chars": digit,
        "word_count": len(words),
        "alpha_ratio": round(alpha / chars, 4) if chars else 0,
        "digit_ratio": round(digit / chars, 4) if chars else 0,
        "markdown_heading_count": text.count("\n#") + (1 if text.startswith("#") else 0),
    }


def classify_npu_output(text: str, returncode: int, error: str | None) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if error:
        warnings.append(error)
    if returncode != 0:
        warnings.append(f"NPU auditor command returned {returncode}")
    if not text.strip():
        warnings.append("NPU auditor produced empty output")
        return "missing_or_empty", warnings
    metrics = text_metrics(text)
    if metrics["word_count"] < 20 or metrics["alpha_ratio"] < 0.25 or metrics["digit_ratio"] > 0.65:
        warnings.append("NPU auditor output appears unusable or non-linguistic")
        return "unusable_output", warnings
    return "usable_audit_text", warnings


def run_command(command: list[str], repo_root: Path, timeout_seconds: int) -> tuple[int, str, str, str | None]:
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            timeout=timeout_seconds,
            check=False,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
        )
        return completed.returncode, completed.stdout[-12000:], completed.stderr[-12000:], None
    except subprocess.TimeoutExpired as exc:
        return 124, exc.stdout or "", exc.stderr or "", f"TimeoutExpired: {timeout_seconds}s"
    except Exception as exc:  # noqa: BLE001 - non-blocking auditor.
        return 1, "", "", f"{type(exc).__name__}: {exc}"


def run_auditor(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    gpu_review_path = resolve_path(repo_root, args.gpu_review)
    gpu_review = read_json(gpu_review_path)
    context_path = resolve_path(repo_root, args.context_output)
    npu_out = resolve_path(repo_root, args.npu_output)
    npu_notes = resolve_path(repo_root, args.npu_notes_output)
    npu_metadata = resolve_path(repo_root, args.npu_metadata_output)
    context_path.parent.mkdir(parents=True, exist_ok=True)
    context_path.write_text(build_context(gpu_review), encoding="utf-8")

    command = [
        sys.executable,
        "Tools/npu/run_npu_review.py",
        "--engine",
        "npu",
        "--mode",
        "onepass",
        "--context",
        str(context_path),
        "--out",
        str(npu_out),
        "--notes-out",
        str(npu_notes),
        "--metadata-out",
        str(npu_metadata),
        "--max-context-chars",
        str(args.max_context_chars),
        "--max-prompt-chars",
        str(args.max_prompt_chars),
        "--max-new-tokens",
        str(args.max_new_tokens),
    ]
    if args.metadata_only:
        command.append("--metadata-only")

    returncode = None
    stdout = ""
    stderr = ""
    error = None
    npu_text = ""
    provider_execution_performed = False
    generated_output_written = False
    if args.run_npu:
        returncode, stdout, stderr, error = run_command(command, repo_root, args.timeout_seconds)
        provider_execution_performed = not args.metadata_only
        generated_output_written = npu_out.exists() and not args.metadata_only
        if npu_out.exists():
            try:
                npu_text = npu_out.read_text(encoding="utf-8-sig", errors="replace")
            except OSError as exc:
                error = f"{type(exc).__name__}: {exc}"
    else:
        returncode = 0
        stdout = "NPU auditor skipped by default. Pass --run-npu to execute OpenVINO/NPU."

    classification, warnings = classify_npu_output(npu_text, int(returncode or 0), error)
    if not args.run_npu:
        classification = "not_executed"
        warnings = ["NPU auditor was not executed; context artifact was prepared only"]

    blocking = False
    report = {
        "schema_version": 1,
        "kind": "npu_gpu_deep_review_audit",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "passed": True,
        "errors": [],
        "warnings": warnings,
        "provider_execution_performed": provider_execution_performed,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "apply_mode": "report_only_non_blocking_npu_audit",
        "non_blocking": True,
        "blocking": blocking,
        "gpu_review": repo_rel(gpu_review_path, repo_root),
        "context_output": repo_rel(context_path, repo_root),
        "npu_output": repo_rel(npu_out, repo_root),
        "npu_notes_output": repo_rel(npu_notes, repo_root),
        "npu_metadata_output": repo_rel(npu_metadata, repo_root),
        "npu_auditor": {
            "requested": bool(args.run_npu),
            "metadata_only": bool(args.metadata_only),
            "returncode": returncode,
            "classification": classification,
            "provider_execution_performed": provider_execution_performed,
            "generated_output_written": generated_output_written,
            "stdout_tail": stdout,
            "stderr_tail": stderr,
            "output_metrics": text_metrics(npu_text),
        },
        "decision": {
            "gpu_review_blocked": False,
            "npu_primary_advisory": False,
            "npu_audit_usable": classification == "usable_audit_text",
            "recommendation": "continue_manual_review; treat NPU audit as non-blocking guardrail signal only",
        },
        "guardrails": {
            "non_blocking_auditor": True,
            "npu_primary_advisory": False,
            "provider_execution_requires_run_npu": True,
            "patch_application_performed": False,
            "real_github_pr_created": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }
    return report


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# NPU GPU Deep Review Audit", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Non-blocking: `{report['non_blocking']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    lines.append(f"- Classification: `{report['npu_auditor']['classification']}`")
    lines.append(f"- GPU review blocked: `{report['decision']['gpu_review_blocked']}`")
    lines.append("")
    if report["warnings"]:
        lines.append("## Warnings")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
        lines.append("")
    lines.append("## Decision")
    for key, value in report["decision"].items():
        lines.append(f"- `{key}`: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--gpu-review", default=DEFAULT_GPU_REVIEW)
    parser.add_argument("--run-npu", action="store_true", help="Explicitly execute OpenVINO/NPU auditor. Without this, only context is prepared.")
    parser.add_argument("--metadata-only", action="store_true", help="Ask run_npu_review.py to write metadata only without loading provider.")
    parser.add_argument("--timeout-seconds", type=int, default=900)
    parser.add_argument("--max-context-chars", type=int, default=42000)
    parser.add_argument("--max-prompt-chars", type=int, default=15000)
    parser.add_argument("--max-new-tokens", type=int, default=900)
    parser.add_argument("--context-output", default=DEFAULT_CONTEXT)
    parser.add_argument("--npu-output", default=DEFAULT_NPU_OUT)
    parser.add_argument("--npu-notes-output", default=DEFAULT_NPU_NOTES)
    parser.add_argument("--npu-metadata-output", default=DEFAULT_NPU_METADATA)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_auditor(args)
    output = resolve_path(repo_root, args.output)
    markdown_output = resolve_path(repo_root, args.markdown_output)
    write_json(output, report)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": report["passed"],
                "output": str(output),
                "markdown": str(markdown_output),
                "provider_execution_performed": report["provider_execution_performed"],
                "patch_application_performed": report["patch_application_performed"],
                "non_blocking": report["non_blocking"],
                "classification": report["npu_auditor"]["classification"],
                "gpu_review_blocked": report["decision"]["gpu_review_blocked"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
