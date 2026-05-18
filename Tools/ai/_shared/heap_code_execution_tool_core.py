"""Core helpers for the heap code execution matrix tool."""

from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.provider_mesh.runtime.python_runtime import command_env
    from Tools.ai.runtime_tool.file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.provider_mesh.runtime.python_runtime import command_env  # type: ignore
    from Tools.ai.runtime_tool.file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def validate_target(repo_root: Path, raw: str) -> tuple[str, str]:
    ref = RuntimeFileRefResolver(repo_root).resolve(
        raw,
        provenance=RuntimeRefProvenance.TOOL_REQUEST,
        consumers=(RuntimeConsumer.MATRIX, RuntimeConsumer.LAB),
    )
    if not ref.patchable:
        return ref.repo_relative or str(raw or ""), ref.reason
    return ref.repo_relative, ""


def validate_validation_script(repo_root: Path, raw: str) -> tuple[str, str]:
    ref = RuntimeFileRefResolver(repo_root).resolve(
        raw,
        provenance=RuntimeRefProvenance.TOOL_REQUEST,
        consumers=(RuntimeConsumer.BROKER_TOOL,),
        validation_ref=True,
    )
    if not ref.validation_only:
        return ref.repo_relative or str(raw or ""), ref.reason
    return ref.repo_relative, ""


def split_values(values: list[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        for part in str(value).split(","):
            normalized = part.strip().strip("'\"")
            if normalized and normalized not in out:
                out.append(normalized)
    return out


def git_diff_excerpt(repo_root: Path, rel_path: str, max_chars: int) -> dict[str, Any]:
    status = subprocess.run(
        ["git", "status", "--short", "--", rel_path],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    status_text = (status.stdout or "").strip()
    completed = subprocess.run(
        ["git", "diff", "--", rel_path],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    diff = completed.stdout or ""
    if status_text.startswith("??") and not diff.strip():
        try:
            text = (repo_root / rel_path).read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            text = ""
        diff = f"new file: {rel_path}\n\n{text}"
    return {
        "target_file": rel_path,
        "changed_in_worktree": bool(diff.strip()),
        "git_status": status_text,
        "returncode": completed.returncode,
        "diff_hunk_count": diff.count("\n@@"),
        "diff_excerpt": diff[:max_chars]
        + ("\n...[diff truncated]" if len(diff) > max_chars else ""),
    }


def build_debug_lab_request(
    target_files: list[str],
    validation_scripts: list[str],
    validation_args: list[str],
) -> dict[str, Any]:
    operations: list[dict[str, Any]] = []
    python_targets = [item for item in target_files if item.endswith(".py")]
    if python_targets:
        operations.append(
            {
                "id": "compile_heap_code_targets",
                "type": "python_compile",
                "paths": python_targets,
                "timeout_seconds": 300,
            }
        )
    for index, script in enumerate(validation_scripts, start=1):
        operations.append(
            {
                "id": f"run_validation_script_{index:02d}",
                "type": "python_script",
                "script": script,
                "args": validation_args,
                "timeout_seconds": 300,
            }
        )
    operations.extend(
        [
            {"id": "git_diff_check", "type": "git_diff_check", "timeout_seconds": 120},
            {"id": "git_status_short", "type": "git_status_short", "timeout_seconds": 120},
        ]
    )
    return {
        "schema_version": 1,
        "kind": "agent_runtime_debug_lab_request",
        "generated_by": "python -m Tools.ai run_heap_code_execution_tool",
        "operations": operations,
    }


def run_debug_lab(
    repo_root: Path,
    request_path: Path,
    report_path: Path,
    markdown_path: Path,
    timeout_seconds: int,
    tail_chars: int,
) -> tuple[int, str, str]:
    command = [
        sys.executable,
        "-m",
        "Tools.ai",
        "agent_runtime_debug_lab",
        "--repo-root",
        ".",
        "--request-file",
        repo_rel(repo_root, request_path),
        "--output",
        repo_rel(repo_root, report_path),
        "--markdown-output",
        repo_rel(repo_root, markdown_path),
        "--timeout-seconds",
        str(timeout_seconds),
        "--tail-chars",
        str(tail_chars),
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        env=command_env(repo_root),
        text=True,
        capture_output=True,
        check=False,
        timeout=max(timeout_seconds + 30, 60),
    )
    return completed.returncode, completed.stdout[-tail_chars:], completed.stderr[-tail_chars:]


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    return data if isinstance(data, dict) else {}


def default_debug_lab_paths(repo_root: Path, output: Path) -> tuple[Path, Path]:
    stem = output.stem or "heap_code_execution_tool"
    safe_stem = "".join(char if char.isalnum() or char in "._-" else "_" for char in stem).strip(
        "._-"
    )
    safe_stem = safe_stem or "heap_code_execution_tool"
    debug_dir = repo_root / "output" / "validation" / "heap_code_execution_tool_debug"
    return (
        debug_dir / f"{safe_stem}_debug_lab.json",
        debug_dir / f"{safe_stem}_debug_lab.md",
    )


def matrix_target_items(
    target_files: list[str],
    diffs: list[dict[str, Any]],
    validation_commands: list[str],
) -> list[dict[str, Any]]:
    diff_by_path = {item.get("target_file"): item for item in diffs}
    items: list[dict[str, Any]] = []
    for target in target_files:
        diff = diff_by_path.get(target, {})
        changed = bool(diff.get("changed_in_worktree"))
        items.append(
            {
                "target_file": target,
                "implementation_status": (
                    "developed_change_present" if changed else "verified_target_no_worktree_diff"
                ),
                "code_or_patch_sketch": diff.get("diff_excerpt") or "",
                "git_status": diff.get("git_status") or "",
                "diff_hunk_count": diff.get("diff_hunk_count", 0),
                "validation_commands": validation_commands,
                "acceptance_criteria": [
                    "target file exists under an allowlisted repo path",
                    "debug lab request compiles Python targets when applicable",
                    "validation scripts execute through allowlisted debug lab operations",
                    "git diff --check remains clean",
                ],
            }
        )
    return items


def proposal_items(
    target_files: list[str],
    diffs: list[dict[str, Any]],
    validation_commands: list[str],
) -> list[dict[str, Any]]:
    return [
        item
        for item in matrix_target_items(target_files, diffs, validation_commands)
        if item.get("implementation_status") == "developed_change_present"
        and str(item.get("code_or_patch_sketch") or "").strip()
    ]


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Code Execution Tool", ""]
    for key in (
        "passed",
        "target_count",
        "validation_script_count",
        "debug_lab_returncode",
        "debug_lab_passed",
        "provider_execution_performed",
        "patch_application_performed",
        "source_writes_performed",
        "patch_candidate_synthesis_requested",
        "patch_candidate_synthesis_passed_count",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.extend(["", "## Reports", ""])
    for key in (
        "request_file",
        "debug_lab_report",
        "debug_lab_markdown",
        "patch_candidate_synthesis_report",
    ):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.extend(["", "## Concrete Code Proposals", ""])
    for item in report.get("concrete_code_proposals", []):
        lines.append(f"### `{item.get('target_file')}`")
        lines.append(f"- Status: `{item.get('implementation_status')}`")
        lines.append(f"- Git status: `{item.get('git_status')}`")
        lines.append(f"- Diff hunks: `{item.get('diff_hunk_count')}`")
        lines.append(f"- Validation commands: `{item.get('validation_commands')}`")
        if item.get("code_or_patch_sketch"):
            lines.extend(["", "```diff", str(item["code_or_patch_sketch"]), "```"])
        lines.append("")
    verified = [
        item
        for item in report.get("verified_targets", [])
        if item.get("implementation_status") != "developed_change_present"
    ]
    if verified:
        lines.extend(["", "## Verified Targets Without Code Product", ""])
        for item in verified:
            lines.append(f"- `{item.get('target_file')}`: `{item.get('implementation_status')}`")
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"
