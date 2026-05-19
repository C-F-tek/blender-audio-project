"""Provider process execution and output classification."""

from __future__ import annotations

import os
import subprocess
from typing import Any

from .common import OPENVINO_GENAI_MISSING

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

def provider_load_attempted(stdout: str, stderr: str) -> bool:
    combined = f"{stdout}\n{stderr}"
    return "[NPU] Loading model:" in combined or "[NPU] Device: NPU" in combined

def dependency_missing(stdout: str, stderr: str, error: str | None) -> bool:
    combined = f"{stdout}\n{stderr}\n{error or ''}"
    return OPENVINO_GENAI_MISSING in combined

def classify_npu_output(
    text: str,
    returncode: int,
    error: str | None,
    stdout: str,
    stderr: str,
    metadata_only: bool,
) -> tuple[str, list[str]]:
    warnings: list[str] = []
    if metadata_only:
        return "metadata_only", warnings
    if error:
        warnings.append(error)
    if dependency_missing(stdout, stderr, error):
        warnings.append(
            "NPU auditor dependency missing: Python module openvino_genai is not importable; install PyPI package openvino-genai in the active NPU Python environment"
        )
        return "dependency_missing_openvino_genai", warnings
    if returncode != 0:
        warnings.append(f"NPU auditor command returned {returncode}")
    if not text.strip():
        warnings.append("NPU provider returned an empty response")
        return "provider_empty_response", warnings
    metrics = text_metrics(text)
    if metrics["word_count"] < 20 or metrics["alpha_ratio"] < 0.25 or metrics["digit_ratio"] > 0.65:
        warnings.append("NPU auditor output appears unusable or non-linguistic")
        return "unusable_output", warnings
    return "usable_audit_text", warnings

def run_command(
    command: list[str], repo_root: Path, timeout_seconds: int
) -> tuple[int, str, str, str | None]:
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
        return (
            completed.returncode,
            completed.stdout[-12000:],
            completed.stderr[-12000:],
            None,
        )
    except subprocess.TimeoutExpired as exc:
        return (
            124,
            exc.stdout or "",
            exc.stderr or "",
            f"TimeoutExpired: {timeout_seconds}s",
        )
    except Exception as exc:  # noqa: BLE001 - non-blocking auditor.
        return 1, "", "", f"{type(exc).__name__}: {exc}"
