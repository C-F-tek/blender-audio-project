"""Post-run packaging helpers for heap context closure."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from .common import load_json, run_command


def run_external_postrun_package(
    *,
    repo_root: Path,
    project_python: str,
    run_dir: Path,
    timeout_seconds: int,
    composer_packaging_performed: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result: dict[str, Any] = {
        "performed": False,
        "passed": False,
        "returncode": None,
        "report": "",
        "stdout_tail": "",
        "stderr_tail": "",
    }
    if not composer_packaging_performed:
        return result, {}

    report = run_dir / "external_heap_postrun_package.json"
    command = [
        project_python,
        "-m",
        "Tools.ai",
        "run_external_heap_postrun_package",
        "--repo-root",
        ".",
        "--python-exe",
        project_python,
        "--run-dir",
        str(run_dir),
        "--include-rejected-history",
        "--include-peer-blocks",
        "--max-block-chars",
        "50000",
        "--max-blocks",
        "0",
        "--output",
        str(report),
    ]
    try:
        completed = subprocess.run(
            command,
            cwd=repo_root,
            text=True,
            capture_output=True,
            check=False,
            timeout=max(60, int(timeout_seconds)),
        )
        result.update(
            {
                "performed": True,
                "passed": completed.returncode == 0,
                "returncode": completed.returncode,
                "report": str(report),
                "command": command,
                "stdout_tail": (completed.stdout or "")[-4000:],
                "stderr_tail": (completed.stderr or "")[-4000:],
            }
        )
    except Exception as exc:
        result.update(
            {
                "performed": True,
                "passed": False,
                "returncode": -1,
                "report": str(report),
                "command": command,
                "stderr_tail": f"{type(exc).__name__}: {exc}",
            }
        )
    return result, load_json(Path(str(result.get("report") or "")))


def run_final_readable_product(
    *,
    repo_root: Path,
    project_python: str,
    run_dir: Path,
    report_file: Path,
    composer_documents_dir: str,
    composer_packaging_performed: bool,
) -> tuple[dict[str, Any], dict[str, Any]]:
    result: dict[str, Any] = {
        "performed": False,
        "passed": False,
        "returncode": None,
        "report": "",
        "markdown": "",
        "text": "",
        "documents_zip": "",
        "stdout_tail": "",
        "stderr_tail": "",
        "command": [],
    }
    if not composer_packaging_performed:
        return result, {}

    final_report = run_dir / "heap_final_readable_product.json"
    final_markdown = run_dir / "heap_final_readable_product.md"
    final_text = run_dir / "heap_final_readable_product.txt"
    command = [
        project_python,
        "-m",
        "Tools.ai",
        "assemble_heap_final_readable_product",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--composer-json",
        str(run_dir / "heap_final_proposal_composer.json"),
        "--gate-report",
        str(report_file),
        "--output",
        str(final_report),
        "--markdown-output",
        str(final_markdown),
        "--text-output",
        str(final_text),
    ]
    if composer_documents_dir:
        command.extend(["--documents-dir", composer_documents_dir, "--zip-documents"])
    completed = run_command(command, repo_root)
    payload = load_json(final_report)
    result.update(
        {
            "performed": True,
            "passed": bool(completed.get("passed")) and bool(payload.get("passed")),
            "returncode": completed.get("returncode"),
            "report": str(final_report),
            "markdown": str(final_markdown),
            "text": str(final_text),
            "documents_zip": str(payload.get("documents_zip", "") or ""),
            "stdout_tail": completed.get("stdout_tail", ""),
            "stderr_tail": completed.get("stderr_tail", ""),
            "command": command,
        }
    )
    return result, payload
