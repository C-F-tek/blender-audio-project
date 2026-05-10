#!/usr/bin/env python3
"""Prepare input-ready context and memory reload artifacts for heap runtime.

This is the startup bridge between an operator request and the heap/exchange
loop. It reuses existing report-only tools from the unified run lane and writes a
single manifest plus a task Markdown file that can be passed to the heap with
`--task-file` before provider lanes start.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


CANONICAL_CONTEXT_FILES = (
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/LOCAL_AI_TASKS/read-first-reuse-first-small-files-rule-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/single-owner-scripts-and-flow-boundaries-2026-05-07.md",
    "docs/LOCAL_AI_TASKS/project-tool-registry.md",
    "docs/LOCAL_AI_TASKS/documentation-panorama-and-staleness-map-2026-05-09.md",
    "docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md",
    "Tools/ai/README.md",
    "Tools/workflow/README.md",
)


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def read_text(path: Path, max_chars: int = 6000) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if len(text) > max_chars:
        return text[:max_chars] + "\n...[truncated]\n"
    return text


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def run_tool(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-3000:],
        "stderr_tail": (completed.stderr or "")[-3000:],
    }


def existing_context_files(repo_root: Path) -> list[str]:
    return [path for path in CANONICAL_CONTEXT_FILES if (repo_root / path).is_file()]


def build_task_markdown(
    *,
    repo_root: Path,
    request: str,
    stamp: str,
    context_files: list[str],
    artifacts: dict[str, str],
    commands: list[dict[str, Any]],
) -> str:
    lines: list[str] = [
        "# Heap Startup Input-Ready Context",
        "",
        f"- Stamp: `{stamp}`",
        "- Source: `prepare_heap_context_memory_reload.py`",
        "- Mode: `report_only_pre_provider_reload`",
        "- Provider execution performed: `False`",
        "- Patch application performed: `False`",
        "- Source writes performed: `False`",
        "",
        "## Operator request",
        "",
        request.strip() or "(empty)",
        "",
        "## Reload contract for heap providers",
        "",
        "- Before GPU1 planning, consume this task file as startup heap context.",
        "- Treat the listed artifacts as the current source of knowledge for repo, docs, tool catalog and memory inventory.",
        "- Do not answer from a single token window: write proposal chunks and let the final composer assemble them.",
        "- GPU0 must refine or reject generic/stub chunks.",
        "- NPU must contribute bounded audit/workload evidence when enabled.",
        "",
        "## Startup artifacts",
        "",
    ]
    for name, value in artifacts.items():
        if value:
            lines.append(f"- `{name}`: `{value}`")
    lines.extend(["", "## Startup tool executions", ""])
    for item in commands:
        lines.append(f"- passed=`{item.get('passed')}` rc=`{item.get('returncode')}` command=`{' '.join(str(part) for part in item.get('command', []))}`")
    lines.extend(["", "## Canonical context files loaded", ""])
    for rel_path in context_files:
        lines.append(f"- `{rel_path}`")
    lines.extend(["", "## Context previews", ""])
    for rel_path in context_files:
        text = read_text(repo_root / rel_path, max_chars=2500)
        if not text:
            continue
        lines.extend([f"### `{rel_path}`", "", "```text", text, "```", ""])
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default="")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-memory-chars", type=int, default=64000)
    parser.add_argument("--max-context-files", type=int, default=80)
    parser.add_argument("--max-chars-per-file", type=int, default=12000)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    project_python = resolve_project_python(repo_root, args.python_exe)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    context_files = existing_context_files(repo_root)

    artifacts: dict[str, str] = {}
    commands: list[dict[str, Any]] = []

    tool_catalog_json = output_dir / "startup_tool_catalog.json"
    tool_catalog_md = output_dir / "startup_tool_catalog.md"
    cmd = [
        project_python,
        "Tools/ai/build_agent_agnostic_tool_inventory.py",
        "--repo-root",
        ".",
        "--output",
        str(tool_catalog_json),
        "--markdown-output",
        str(tool_catalog_md),
    ]
    commands.append(run_tool(cmd, repo_root))
    artifacts["tool_catalog_json"] = repo_rel(repo_root, tool_catalog_json)
    artifacts["tool_catalog_markdown"] = repo_rel(repo_root, tool_catalog_md)

    memory_json = output_dir / "startup_memory_inventory.json"
    memory_md = output_dir / "startup_memory_inventory.md"
    cmd = [
        project_python,
        "Tools/ai/build_agent_memory_inventory.py",
        "--repo-root",
        ".",
        "--objective",
        args.request or "heap startup memory reload",
        "--max-memory-chars",
        str(args.max_memory_chars),
        "--output",
        str(memory_json),
        "--markdown-output",
        str(memory_md),
    ]
    commands.append(run_tool(cmd, repo_root))
    artifacts["shared_memory_json"] = repo_rel(repo_root, memory_json)
    artifacts["shared_memory_markdown"] = repo_rel(repo_root, memory_md)

    transient_json = output_dir / "startup_transient_request_context.json"
    transient_md = output_dir / "startup_transient_request_context.md"
    cmd = [
        project_python,
        "Tools/ai/build_agent_transient_request_context.py",
        "--repo-root",
        ".",
        "--objective",
        "heap startup context/memory reload before provider lanes",
        "--memory-note",
        args.request or "heap startup request",
        "--report-file",
        str(tool_catalog_json),
        "--report-file",
        str(memory_json),
        "--max-raw-files",
        str(args.max_context_files),
        "--max-chars-per-file",
        str(args.max_chars_per_file),
        "--output",
        str(transient_json),
        "--markdown-output",
        str(transient_md),
    ]
    for rel_path in context_files:
        cmd.extend(["--raw-file", rel_path])
    commands.append(run_tool(cmd, repo_root))
    artifacts["shared_context_json"] = repo_rel(repo_root, transient_json)
    artifacts["shared_context_markdown"] = repo_rel(repo_root, transient_md)

    context_pack_dir = output_dir / "startup_ai_context_pack"
    context_evidence_dir = output_dir / "startup_ai_context_pack_evidence"
    context_basename = f"heap_startup_context_pack_{stamp}"
    cmd = [
        project_python,
        "Tools/ai/build_ai_context_pack.py",
        "--repo-root",
        ".",
        "--profile",
        "project_self_improvement",
        "--output-dir",
        str(context_pack_dir),
        "--basename",
        context_basename,
        "--evidence-dir",
        str(context_evidence_dir),
        "--evidence-basename",
        f"{context_basename}_evidence",
    ]
    commands.append(run_tool(cmd, repo_root))
    artifacts["ai_context_pack_json"] = repo_rel(repo_root, context_pack_dir / f"{context_basename}.json")
    artifacts["ai_context_pack_markdown"] = repo_rel(repo_root, context_pack_dir / f"{context_basename}.md")
    artifacts["ai_context_pack_evidence_json"] = repo_rel(repo_root, context_evidence_dir / f"{context_basename}_evidence.json")
    artifacts["ai_context_pack_evidence_markdown"] = repo_rel(repo_root, context_evidence_dir / f"{context_basename}_evidence.md")

    task_file = output_dir / "heap_startup_input_ready_context.md"
    task_markdown = build_task_markdown(
        repo_root=repo_root,
        request=args.request,
        stamp=stamp,
        context_files=context_files,
        artifacts=artifacts,
        commands=commands,
    )
    task_file.write_text(task_markdown, encoding="utf-8")
    artifacts["heap_task_file"] = repo_rel(repo_root, task_file)

    manifest = {
        "schema_version": 1,
        "kind": "heap_context_memory_reload_manifest",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "request": args.request,
        "passed": all(item.get("passed") for item in commands),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "context_file_count": len(context_files),
        "context_files": context_files,
        "artifacts": artifacts,
        "tool_executions": commands,
        "heap_task_file": artifacts["heap_task_file"],
        "contract": {
            "input_ready_before_heap": True,
            "load_context_into_heap": True,
            "reuse_existing_unified_run_tools": True,
            "final_composer_required": True,
        },
    }
    manifest_path = output_dir / "heap_context_memory_reload_manifest.json"
    manifest_md = output_dir / "heap_context_memory_reload_manifest.md"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_md.write_text(task_markdown, encoding="utf-8")

    print(json.dumps({**manifest, "manifest": repo_rel(repo_root, manifest_path), "markdown": repo_rel(repo_root, manifest_md)}, indent=2, ensure_ascii=False))
    return 0 if manifest["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
