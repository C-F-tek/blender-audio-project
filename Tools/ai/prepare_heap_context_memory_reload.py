#!/usr/bin/env python3
"""Prepare input-ready context and memory reload artifacts for heap runtime.

The startup reload is tool-owned: it runs the repository tools that know how to
build tool catalogs, memory inventory, operational memory status/search,
transient request context and AI context packs. Partial tool failure is not
automatically fatal when useful artifacts were produced; the manifest records the
degradation and the heap task file carries that fact into the shared runtime
state before provider lanes start.
"""
from __future__ import annotations

import argparse
import hashlib
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

SEMANTIC_CHUNK_ROOTS = (
    "Tools/ai",
    "Tools/validation",
    "Tools/workflow",
    "docs/LOCAL_AI_TASKS",
)

REPO_SCAN_EXCLUDED_DIRS = {
    ".git",
    ".venv",
    "venv",
    ".venv314",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    "renders",
    "output",
    "indexAI/code_chunks",
}

REPO_SCAN_TEXT_SUFFIXES = {
    ".py",
    ".ps1",
    ".md",
    ".txt",
    ".json",
    ".yml",
    ".yaml",
    ".toml",
    ".ini",
    ".cfg",
    ".csv",
    ".bat",
    ".sh",
}


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def read_request_file(repo_root: Path, value: str) -> str:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.read_text(encoding="utf-8-sig", errors="replace")


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


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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


def summarize_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    item: dict[str, Any] = {
        "path": repo_rel(repo_root, path),
        "exists": path.exists(),
        "size_bytes": None,
        "suffix": path.suffix.lower(),
        "json_ok": False,
        "json_passed": None,
        "kind": "",
        "useful": False,
    }
    if not path.exists() or not path.is_file():
        return item
    try:
        size = path.stat().st_size
    except OSError:
        size = 0
    item["size_bytes"] = size
    item["useful"] = size > 0
    if path.suffix.lower() == ".json" and size > 0:
        data = read_json(path)
        item["json_ok"] = bool(data)
        item["json_passed"] = data.get("passed") if data else None
        item["kind"] = str(data.get("kind") or data.get("report_kind") or "")
        if data:
            item["summary_fields"] = {
                key: data.get(key)
                for key in (
                    "passed",
                    "profile",
                    "included_file_count",
                    "truncated_file_count",
                    "provider_execution_performed",
                    "patch_application_performed",
                    "source_writes_performed",
                )
                if key in data
            }
    return item


def run_tool(
    command: list[str],
    repo_root: Path,
    *,
    name: str,
    requirement: str,
    required: bool,
    artifact_paths: list[Path] | None = None,
) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    artifacts = [summarize_artifact(path, repo_root) for path in (artifact_paths or [])]
    existing_artifacts = [item["path"] for item in artifacts if item.get("exists")]
    useful_artifacts = [item["path"] for item in artifacts if item.get("useful")]
    passed = completed.returncode == 0
    artifact_useful = bool(useful_artifacts)
    effective_passed = passed or artifact_useful
    degraded = (not passed) and artifact_useful
    hard_failed = (not passed) and (not artifact_useful)
    return {
        "name": name,
        "requirement": requirement,
        "required": required,
        "command": command,
        "returncode": completed.returncode,
        "passed": passed,
        "effective_passed": effective_passed,
        "degraded": degraded,
        "hard_failed": hard_failed,
        "artifact_useful": artifact_useful,
        "artifact_paths": [item["path"] for item in artifacts],
        "existing_artifact_paths": existing_artifacts,
        "useful_artifact_paths": useful_artifacts,
        "artifact_summaries": artifacts,
        "stdout_tail": (completed.stdout or "")[-3000:],
        "stderr_tail": (completed.stderr or "")[-3000:],
    }



def is_repo_scan_excluded(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/").strip("/")
    parts = normalized.split("/")
    for excluded in REPO_SCAN_EXCLUDED_DIRS:
        excluded = excluded.strip("/")
        if not excluded:
            continue
        if "/" in excluded:
            if normalized == excluded or normalized.startswith(excluded + "/"):
                return True
        elif excluded in parts:
            return True
    return False


def repo_scan_files(repo_root: Path, *, max_files: int, suffixes: set[str] | None = None) -> list[Path]:
    suffix_filter = suffixes or REPO_SCAN_TEXT_SUFFIXES
    files: list[Path] = []
    for root, dirs, names in __import__("os").walk(repo_root):
        root_path = Path(root)
        dirs[:] = [
            dirname
            for dirname in dirs
            if not is_repo_scan_excluded(repo_rel(repo_root, root_path / dirname))
        ]
        for name in names:
            path = root_path / name
            rel_path = repo_rel(repo_root, path)
            if is_repo_scan_excluded(rel_path):
                continue
            if path.suffix.lower() not in suffix_filter:
                continue
            files.append(path)
            if len(files) >= max_files:
                return sorted(files, key=lambda item: repo_rel(repo_root, item).lower())
    return sorted(files, key=lambda item: repo_rel(repo_root, item).lower())


def repo_scan_context_files(repo_root: Path, *, max_files: int) -> list[str]:
    priority_names = {"AGENTS.md", "README.md", "WORKFLOW.md"}
    selected: list[str] = []

    for rel_path in CANONICAL_CONTEXT_FILES:
        if (repo_root / rel_path).is_file() and rel_path not in selected:
            selected.append(rel_path)

    for path in repo_scan_files(repo_root, max_files=max_files, suffixes={".md"}):
        rel_path = repo_rel(repo_root, path)
        if path.name in priority_names or rel_path.startswith("docs/"):
            if rel_path not in selected:
                selected.append(rel_path)
        if len(selected) >= max_files:
            break

    return selected[:max_files]


def repo_scan_semantic_candidates(repo_root: Path, *, max_files: int) -> list[Path]:
    return repo_scan_files(
        repo_root,
        max_files=max_files,
        suffixes={".py", ".ps1", ".md", ".json", ".yml", ".yaml", ".toml"},
    )


def existing_context_files(repo_root: Path, max_files: int = 240) -> list[str]:
    return repo_scan_context_files(repo_root, max_files=max_files)


def build_repo_docs_map(repo_root: Path, context_files: list[str], output_dir: Path) -> dict[str, str]:
    docs = []
    for rel_path in context_files:
        full = repo_root / rel_path
        text = read_text(full, max_chars=1200)
        docs.append(
            {
                "path": rel_path,
                "size_bytes": full.stat().st_size if full.exists() else 0,
                "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if text else "",
                "preview": text,
            }
        )
    data = {
        "schema_version": 1,
        "kind": "heap_startup_repo_docs_map",
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "document_count": len(docs),
        "documents": docs,
    }
    json_path = output_dir / "startup_repo_docs_map.json"
    md_path = output_dir / "startup_repo_docs_map.md"
    write_json(json_path, data)
    lines = ["# Heap Startup Repo Docs Map", ""]
    for item in docs:
        lines.append(f"- `{item['path']}` size=`{item['size_bytes']}`")
    write_markdown(md_path, "\n".join(lines) + "\n")
    return {"repo_docs_map_json": repo_rel(repo_root, json_path), "repo_docs_map_markdown": repo_rel(repo_root, md_path)}


def collect_semantic_code_chunks(repo_root: Path, output_dir: Path, request: str, limit: int = 48) -> dict[str, str]:
    keywords = [part.lower() for part in request.replace("_", " ").replace("-", " ").split() if len(part) >= 4]
    candidates: list[Path] = repo_scan_semantic_candidates(repo_root, max_files=max(1000, limit * 80))
    ranked: list[tuple[int, Path]] = []
    for path in candidates:
        rel = repo_rel(repo_root, path)
        rel_lower = rel.lower()
        score = sum(3 for key in keywords if key in rel_lower)
        if any(token in rel_lower for token in ("heap", "context", "memory", "provider", "gpu", "npu", "composer")):
            score += 8
        if path.name in {
            "run_heap_runtime_context_closure.py",
            "prepare_heap_context_memory_reload.py",
            "compose_heap_final_proposals.py",
            "run_heap_runtime_completeness_gate.py",
            "build_ai_context_pack.py",
            "agent_runtime_sqlite_memory.py",
        }:
            score += 20
        ranked.append((score, path))
    ranked.sort(key=lambda item: (-item[0], repo_rel(repo_root, item[1])))
    chunks = []
    for score, path in ranked[:limit]:
        rel = repo_rel(repo_root, path)
        text = read_text(path, max_chars=1800)
        chunks.append(
            {
                "path": rel,
                "score": score,
                "size_bytes": path.stat().st_size if path.exists() else 0,
                "preview": text,
                "sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest() if text else "",
            }
        )
    data = {
        "schema_version": 1,
        "kind": "heap_startup_semantic_code_chunks",
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "chunk_count": len(chunks),
        "selection_policy": "deterministic_path_keyword_ranker",
        "chunks": chunks,
    }
    json_path = output_dir / "startup_semantic_code_chunks.json"
    md_path = output_dir / "startup_semantic_code_chunks.md"
    write_json(json_path, data)
    lines = ["# Heap Startup Semantic Code Chunks", ""]
    for item in chunks:
        lines.extend([f"## `{item['path']}`", "", f"- Score: `{item['score']}`", "", "```text", item["preview"], "```", ""])
    write_markdown(md_path, "\n".join(lines))
    return {
        "semantic_code_chunks_json": repo_rel(repo_root, json_path),
        "semantic_code_chunks_markdown": repo_rel(repo_root, md_path),
    }


def write_semantic_evidence(commands: list[dict[str, Any]], repo_root: Path, output_dir: Path) -> dict[str, str]:
    evidence_items = []
    for command in commands:
        evidence_items.append(
            {
                "name": command.get("name"),
                "requirement": command.get("requirement"),
                "passed": command.get("passed"),
                "effective_passed": command.get("effective_passed"),
                "degraded": command.get("degraded"),
                "hard_failed": command.get("hard_failed"),
                "useful_artifact_paths": command.get("useful_artifact_paths", []),
            }
        )
    data = {
        "schema_version": 1,
        "kind": "heap_startup_semantic_evidence_chunks",
        "passed": all(bool(item.get("effective_passed")) for item in commands if item.get("required")),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "evidence_count": len(evidence_items),
        "evidence": evidence_items,
    }
    json_path = output_dir / "startup_semantic_evidence_chunks.json"
    md_path = output_dir / "startup_semantic_evidence_chunks.md"
    write_json(json_path, data)
    lines = ["# Heap Startup Semantic Evidence Chunks", ""]
    for item in evidence_items:
        lines.append(
            f"- `{item['requirement']}` name=`{item['name']}` passed=`{item['passed']}` "
            f"effective=`{item['effective_passed']}` degraded=`{item['degraded']}`"
        )
    write_markdown(md_path, "\n".join(lines) + "\n")
    return {
        "semantic_evidence_chunks_json": repo_rel(repo_root, json_path),
        "semantic_evidence_chunks_markdown": repo_rel(repo_root, md_path),
    }


def build_context_loaded_block(artifacts: dict[str, str]) -> list[str]:
    key_labels = (
        ("tool_catalog_json", "tool catalog"),
        ("shared_memory_json", "memory inventory"),
        ("operational_memory_status_json", "operational memory status"),
        ("operational_memory_search_json", "operational memory search"),
        ("shared_context_json", "transient request context"),
        ("ai_context_pack_json", "AI context pack"),
        ("semantic_code_chunks_json", "semantic chunks"),
        ("semantic_evidence_chunks_json", "semantic evidence chunks"),
        ("repo_docs_map_json", "repo docs map"),
    )
    lines = ["CONTEXT LOADED INTO HEAP:"]
    for key, label in key_labels:
        value = artifacts.get(key, "")
        lines.append(f"- {label}: `{value or 'not_available'}`")
    return lines


def build_task_markdown(
    *,
    repo_root: Path,
    request: str,
    stamp: str,
    context_files: list[str],
    artifacts: dict[str, str],
    commands: list[dict[str, Any]],
    warnings: list[str],
    startup_reload_degraded: bool,
    degraded_requirements: list[str],
    blocking_requirements: list[str],
) -> str:
    lines: list[str] = [
        "# Heap Startup Input-Ready Context",
        "",
        f"- Stamp: `{stamp}`",
        "- Source: `prepare_heap_context_memory_reload.py`",
        "- Mode: `tool_owned_pre_provider_reload`",
        f"- Startup reload degraded: `{startup_reload_degraded}`",
        f"- Degraded requirements: `{degraded_requirements}`",
        f"- Blocking requirements: `{blocking_requirements}`",
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
        "- Treat listed artifacts as the current source of knowledge for repo, docs, tool catalog and memory inventory.",
        "- If startup_reload_degraded is true, continue but carry the degradation as a fact in the heap.",
        "- Do not answer from a single token window: write proposal chunks and let the final composer assemble them.",
        "- GPU0 must refine or reject generic/stub chunks using source anchors and quality diagnosis.",
        "- NPU must contribute bounded audit/workload evidence when enabled.",
        "- Advisory context-pack failures do not block heap startup when useful artifacts exist.",
        "",
        "## Context loaded into heap",
        "",
        *build_context_loaded_block(artifacts),
        "",
        "## Startup artifacts",
        "",
    ]
    for name, value in artifacts.items():
        if value:
            lines.append(f"- `{name}`: `{value}`")
    lines.extend(["", "## Startup tool executions", ""])
    for item in commands:
        lines.append(
            "- "
            + f"name=`{item.get('name')}` "
            + f"required=`{item.get('required')}` "
            + f"passed=`{item.get('passed')}` "
            + f"effective_passed=`{item.get('effective_passed')}` "
            + f"degraded=`{item.get('degraded')}` "
            + f"rc=`{item.get('returncode')}` "
            + f"artifacts=`{item.get('useful_artifact_paths')}`"
        )
    if warnings:
        lines.extend(["", "## Startup warnings", ""])
        for warning in warnings:
            lines.append(f"- {warning}")
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




def append_artifact_ref(refs: list[str], value: Any) -> None:
    if not isinstance(value, str) or not value.strip():
        return
    normalized = value.replace("\\", "/")
    if normalized not in refs:
        refs.append(normalized)


def collect_startup_artifact_refs(artifacts: dict[str, str], commands: list[dict[str, Any]]) -> list[str]:
    refs: list[str] = []
    for value in artifacts.values():
        append_artifact_ref(refs, value)
    for execution in commands:
        if not isinstance(execution, dict):
            continue
        for key in ("useful_artifact_paths", "existing_artifact_paths", "artifact_paths"):
            for value in execution.get(key) or []:
                append_artifact_ref(refs, value)
        for summary in execution.get("artifact_summaries") or []:
            if isinstance(summary, dict):
                append_artifact_ref(refs, summary.get("path"))
        for artifact in execution.get("artifacts") or []:
            if isinstance(artifact, dict):
                append_artifact_ref(refs, artifact.get("path"))
            else:
                append_artifact_ref(refs, artifact)
    return refs


def build_operational_memory_write_content(
    *,
    repo_root: Path,
    stamp: str,
    request: str,
    startup_reload_degraded: bool,
    degraded_requirements: list[str],
    blocking_requirements: list[str],
    artifacts: dict[str, str],
    commands: list[dict[str, Any]],
) -> str:
    payload = {
        "schema_version": 1,
        "kind": "heap_startup_operational_memory_note",
        "stamp": stamp,
        "request_preview": request[:1200],
        "startup_reload_degraded": startup_reload_degraded,
        "degraded_requirements": degraded_requirements,
        "blocking_requirements": blocking_requirements,
        "artifact_refs": collect_startup_artifact_refs(artifacts, commands)[:80],
        "tool_execution_summary": [
            {
                "name": item.get("name"),
                "requirement": item.get("requirement"),
                "passed": item.get("passed"),
                "effective_passed": item.get("effective_passed"),
                "degraded": item.get("degraded"),
                "useful_artifact_paths": item.get("useful_artifact_paths", []),
            }
            for item in commands
        ],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--request", default="")
    parser.add_argument("--request-file", default="", help="Read startup request text from file to avoid long Windows command lines.")
    parser.add_argument("--stamp", default="")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--max-memory-chars", type=int, default=64000)
    parser.add_argument("--max-context-files", type=int, default=80)
    parser.add_argument("--startup-scan-context-files", type=int, default=10000)
    parser.add_argument("--max-chars-per-file", type=int, default=12000)
    parser.add_argument(
        "--strict-ai-context-pack",
        action="store_true",
        help="Treat build_ai_context_pack failures as startup-blocking.",
    )
    parser.add_argument(
        "--strict-startup-reload",
        action="store_true",
        help="Return failure when any startup reload tool is degraded, even if artifacts are useful.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp or now_stamp()
    project_python = resolve_project_python(repo_root, args.python_exe)
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    request_text = read_request_file(repo_root, args.request_file) if args.request_file else (args.request or "")

    artifacts: dict[str, str] = {}
    commands: list[dict[str, Any]] = []
    warnings: list[str] = []

    required_context_json = output_dir / "startup_required_ai_context_files.json"
    required_context_md = output_dir / "startup_required_ai_context_files.md"
    cmd = [
        project_python,
        "Tools/ai/ensure_ai_context_required_files.py",
        "--repo-root",
        ".",
        "--profile",
        "project_self_improvement",
        "--output",
        str(required_context_json),
        "--markdown-output",
        str(required_context_md),
        "--apply",
    ]
    commands.append(
        run_tool(
            cmd,
            repo_root,
            name="required_context_files_reload",
            requirement="required_context_files",
            required=True,
            artifact_paths=[required_context_json, required_context_md],
        )
    )
    artifacts["required_context_files_json"] = repo_rel(repo_root, required_context_json)
    artifacts["required_context_files_markdown"] = repo_rel(repo_root, required_context_md)

    context_files = existing_context_files(repo_root, max_files=args.startup_scan_context_files)

    artifacts.update(build_repo_docs_map(repo_root, context_files, output_dir))
    artifacts.update(collect_semantic_code_chunks(repo_root, output_dir, request_text, limit=max(12, min(args.max_context_files, 64))))

    tool_catalog_json = output_dir / "startup_tool_catalog.json"
    tool_catalog_md = output_dir / "startup_tool_catalog.md"
    commands.append(
        run_tool(
            [
                project_python,
                "Tools/ai/build_agent_agnostic_tool_inventory.py",
                "--repo-root",
                ".",
                "--output",
                str(tool_catalog_json),
                "--markdown-output",
                str(tool_catalog_md),
            ],
            repo_root,
            name="tool_catalog_reload",
            requirement="tool_catalog",
            required=True,
            artifact_paths=[tool_catalog_json, tool_catalog_md],
        )
    )
    artifacts["tool_catalog_json"] = repo_rel(repo_root, tool_catalog_json)
    artifacts["tool_catalog_markdown"] = repo_rel(repo_root, tool_catalog_md)

    memory_json = output_dir / "startup_memory_inventory.json"
    memory_md = output_dir / "startup_memory_inventory.md"
    commands.append(
        run_tool(
            [
                project_python,
                "Tools/ai/build_agent_memory_inventory.py",
                "--repo-root",
                ".",
                "--objective",
                request_text or "heap startup memory reload",
                "--max-memory-chars",
                str(args.max_memory_chars),
                "--output",
                str(memory_json),
                "--markdown-output",
                str(memory_md),
            ],
            repo_root,
            name="shared_memory_reload",
            requirement="shared_memory",
            required=True,
            artifact_paths=[memory_json, memory_md],
        )
    )
    artifacts["shared_memory_json"] = repo_rel(repo_root, memory_json)
    artifacts["shared_memory_markdown"] = repo_rel(repo_root, memory_md)

    operational_status_json = output_dir / "startup_operational_memory_status.json"
    operational_status_md = output_dir / "startup_operational_memory_status.md"
    commands.append(
        run_tool(
            [
                project_python,
                "Tools/ai/agent_runtime_sqlite_memory.py",
                "--repo-root",
                ".",
                "--action",
                "status",
                "--scope",
                "operational",
                "--output",
                str(operational_status_json),
                "--markdown-output",
                str(operational_status_md),
            ],
            repo_root,
            name="operational_memory_status_reload",
            requirement="operational_memory_status",
            required=False,
            artifact_paths=[operational_status_json, operational_status_md],
        )
    )
    artifacts["operational_memory_status_json"] = repo_rel(repo_root, operational_status_json)
    artifacts["operational_memory_status_markdown"] = repo_rel(repo_root, operational_status_md)

    operational_search_json = output_dir / "startup_operational_memory_search.json"
    operational_search_md = output_dir / "startup_operational_memory_search.md"
    commands.append(
        run_tool(
            [
                project_python,
                "Tools/ai/agent_runtime_sqlite_memory.py",
                "--repo-root",
                ".",
                "--action",
                "search",
                "--scope",
                "operational",
                "--query",
                "heap context memory reload provider proposal GPU0 NPU",
                "--limit",
                "20",
                "--output",
                str(operational_search_json),
                "--markdown-output",
                str(operational_search_md),
            ],
            repo_root,
            name="operational_memory_search_reload",
            requirement="operational_memory_search",
            required=False,
            artifact_paths=[operational_search_json, operational_search_md],
        )
    )
    artifacts["operational_memory_search_json"] = repo_rel(repo_root, operational_search_json)
    artifacts["operational_memory_search_markdown"] = repo_rel(repo_root, operational_search_md)

    startup_request_file = output_dir / "heap_startup_request.md"
    startup_request_file.write_text(request_text or "heap startup request", encoding="utf-8")
    startup_raw_file_list = output_dir / "startup_context_raw_files.txt"
    startup_raw_file_list.write_text("\n".join(context_files) + "\n", encoding="utf-8")
    artifacts["startup_context_raw_file_list"] = repo_rel(repo_root, startup_raw_file_list)

    transient_json = output_dir / "startup_transient_request_context.json"
    transient_md = output_dir / "startup_transient_request_context.md"
    transient_command = [
        project_python,
        "Tools/ai/build_agent_transient_request_context.py",
        "--repo-root",
        ".",
        "--objective",
        "heap startup context/memory reload before provider lanes",
        "--memory-note-file",
        str(startup_request_file),
        "--raw-file-list",
        str(startup_raw_file_list),
        "--report-file",
        str(tool_catalog_json),
        "--report-file",
        str(memory_json),
        "--report-file",
        str(operational_status_json),
        "--report-file",
        str(operational_search_json),
        "--max-raw-files",
        str(min(args.startup_scan_context_files, max(args.max_context_files, 240))),
        "--max-chars-per-file",
        str(args.max_chars_per_file),
        "--output",
        str(transient_json),
        "--markdown-output",
        str(transient_md),
    ]
    commands.append(
        run_tool(
            transient_command,
            repo_root,
            name="shared_context_reload",
            requirement="shared_context_chunks",
            required=True,
            artifact_paths=[transient_json, transient_md],
        )
    )
    artifacts["shared_context_json"] = repo_rel(repo_root, transient_json)
    artifacts["shared_context_markdown"] = repo_rel(repo_root, transient_md)

    context_pack_dir = output_dir / "startup_ai_context_pack"
    context_evidence_dir = output_dir / "startup_ai_context_pack_evidence"
    context_basename = f"heap_startup_context_pack_{stamp}"
    context_pack_json = context_pack_dir / f"{context_basename}.json"
    context_pack_md = context_pack_dir / f"{context_basename}.md"
    context_pack_evidence_json = context_evidence_dir / f"{context_basename}_evidence.json"
    context_pack_evidence_md = context_evidence_dir / f"{context_basename}_evidence.md"
    context_pack_result = run_tool(
        [
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
        ],
        repo_root,
        name="ai_context_pack_reload",
        requirement="ai_context_pack",
        required=bool(args.strict_ai_context_pack),
        artifact_paths=[
            context_pack_json,
            context_pack_md,
            context_pack_evidence_json,
            context_pack_evidence_md,
        ],
    )
    commands.append(context_pack_result)
    artifacts["ai_context_pack_json"] = repo_rel(repo_root, context_pack_json)
    artifacts["ai_context_pack_markdown"] = repo_rel(repo_root, context_pack_md)
    artifacts["ai_context_pack_evidence_json"] = repo_rel(repo_root, context_pack_evidence_json)
    artifacts["ai_context_pack_evidence_markdown"] = repo_rel(repo_root, context_pack_evidence_md)

    if context_pack_result["degraded"]:
        pack_payload = read_json(context_pack_json)
        pack_errors = pack_payload.get("errors") if isinstance(pack_payload.get("errors"), list) else []
        pack_warnings = pack_payload.get("warnings") if isinstance(pack_payload.get("warnings"), list) else []
        warning = (
            "ai_context_pack_reload returned non-zero "
            + f"rc={context_pack_result['returncode']} but useful artifacts exist"
        )
        if pack_errors:
            warning += "; errors=" + "; ".join(str(item) for item in pack_errors[:5])
        warnings.append(warning)
        for item in pack_warnings[:5]:
            warnings.append(f"ai_context_pack warning: {item}")

    artifacts.update(write_semantic_evidence(commands, repo_root, output_dir))

    task_file = output_dir / "heap_startup_input_ready_context.md"
    artifacts["heap_task_file"] = repo_rel(repo_root, task_file)
    artifacts["startup_request_file"] = repo_rel(repo_root, startup_request_file)

    preliminary_required_commands = [item for item in commands if item.get("required")]
    preliminary_optional_commands = [item for item in commands if not item.get("required")]
    blocking_requirements = [
        str(item.get("requirement"))
        for item in preliminary_required_commands
        if not item.get("effective_passed")
    ]
    degraded_requirements = [str(item.get("requirement")) for item in commands if item.get("degraded")]
    optional_failed_requirements = [
        str(item.get("requirement"))
        for item in preliminary_optional_commands
        if not item.get("effective_passed")
    ]
    startup_reload_degraded = bool(degraded_requirements or optional_failed_requirements)

    operational_write_json = output_dir / "startup_operational_memory_write.json"
    operational_write_md = output_dir / "startup_operational_memory_write.md"
    operational_write_content = output_dir / "startup_operational_memory_content.md"
    operational_write_content.write_text(
        build_operational_memory_write_content(
            repo_root=repo_root,
            stamp=stamp,
            request=request_text,
            startup_reload_degraded=startup_reload_degraded,
            degraded_requirements=degraded_requirements,
            blocking_requirements=blocking_requirements,
            artifacts=artifacts,
            commands=commands,
        ),
        encoding="utf-8",
    )
    artifacts["operational_memory_content_file"] = repo_rel(repo_root, operational_write_content)
    commands.append(
        run_tool(
            [
                project_python,
                "Tools/ai/agent_runtime_sqlite_memory.py",
                "--repo-root",
                ".",
                "--action",
                "remember",
                "--scope",
                "operational",
                "--request-id",
                f"heap_startup_reload_{stamp}",
                "--role",
                "heap_startup_reload",
                "--summary",
                "startup context/memory reload manifest",
                "--content-file",
                str(operational_write_content),
                "--tag",
                "heap_startup_context",
                "--tag",
                stamp,
                "--output",
                str(operational_write_json),
                "--markdown-output",
                str(operational_write_md),
            ],
            repo_root,
            name="operational_memory_write_reload",
            requirement="operational_memory_write",
            required=False,
            artifact_paths=[operational_write_json, operational_write_md],
        )
    )
    artifacts["operational_memory_write_json"] = repo_rel(repo_root, operational_write_json)
    artifacts["operational_memory_write_markdown"] = repo_rel(repo_root, operational_write_md)

    required_commands = [item for item in commands if item.get("required")]
    optional_commands = [item for item in commands if not item.get("required")]
    blocking_requirements = [str(item.get("requirement")) for item in required_commands if not item.get("effective_passed")]
    degraded_requirements = [str(item.get("requirement")) for item in commands if item.get("degraded")]
    optional_failed_requirements = [str(item.get("requirement")) for item in optional_commands if not item.get("effective_passed")]
    startup_reload_degraded = bool(degraded_requirements or optional_failed_requirements)
    required_passed = not blocking_requirements
    optional_passed = all(bool(item.get("effective_passed")) for item in optional_commands)
    input_ready_before_heap = required_passed and bool(context_files)

    task_markdown = build_task_markdown(
        repo_root=repo_root,
        request=request_text,
        stamp=stamp,
        context_files=context_files,
        artifacts=artifacts,
        commands=commands,
        warnings=warnings,
        startup_reload_degraded=startup_reload_degraded,
        degraded_requirements=degraded_requirements,
        blocking_requirements=blocking_requirements,
    )
    task_file.write_text(task_markdown, encoding="utf-8")

    strict_startup = bool(args.strict_startup_reload or args.strict_ai_context_pack)
    passed = bool(input_ready_before_heap and (not strict_startup or not startup_reload_degraded))
    manifest = {
        "schema_version": 1,
        "kind": "heap_context_memory_reload_manifest",
        "stamp": stamp,
        "repo_root": repo_root.as_posix(),
        "project_python": project_python,
        "request_file": artifacts.get("startup_request_file", ""),
        "request_chars": len(request_text),
        "request_sha256": hashlib.sha256(request_text.encode("utf-8", errors="replace")).hexdigest() if request_text else "",
        "request_preview": request_text[:4000],
        "passed": passed,
        "input_ready_before_heap": input_ready_before_heap,
        "load_context_into_heap": True,
        "startup_reload_degraded": startup_reload_degraded,
        "strict_startup_reload": strict_startup,
        "required_reload_passed": required_passed,
        "optional_reload_passed": optional_passed,
        "blocking_requirements": blocking_requirements,
        "degraded_requirements": degraded_requirements,
        "optional_failed_requirements": optional_failed_requirements,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "context_file_count": len(context_files),
        "context_files": context_files,
        "artifacts": artifacts,
        "tool_executions": commands,
        "startup_warnings": warnings,
        "required_requirements": [item["requirement"] for item in required_commands],
        "optional_requirements": [item["requirement"] for item in optional_commands],
        "heap_task_file": artifacts["heap_task_file"],
        "contract": {
            "input_ready_before_heap": input_ready_before_heap,
            "load_context_into_heap": True,
            "tool_catalog_loaded": bool(artifacts.get("tool_catalog_json")),
            "shared_memory_loaded": bool(artifacts.get("shared_memory_json")),
            "operational_memory_loaded": bool(artifacts.get("operational_memory_status_json")),
            "operational_memory_write_recorded": bool(artifacts.get("operational_memory_write_json")),
            "repo_docs_loaded": bool(artifacts.get("repo_docs_map_json")),
            "semantic_code_chunks_loaded": bool(artifacts.get("semantic_code_chunks_json")),
            "ai_context_pack_loaded": bool(artifacts.get("ai_context_pack_json")) and context_pack_result.get("artifact_useful"),
            "semantic_evidence_chunks_loaded": bool(artifacts.get("semantic_evidence_chunks_json")),
            "heap_task_file_written": task_file.exists(),
            "advisory_context_pack_non_blocking": not bool(args.strict_ai_context_pack),
            "final_composer_required": True,
        },
    }
    manifest_path = output_dir / "heap_context_memory_reload_manifest.json"
    manifest_md = output_dir / "heap_context_memory_reload_manifest.md"
    write_json(manifest_path, manifest)
    manifest_md.write_text(task_markdown, encoding="utf-8")

    print_payload = {
        "schema_version": manifest["schema_version"],
        "kind": manifest["kind"],
        "stamp": manifest["stamp"],
        "passed": manifest["passed"],
        "input_ready_before_heap": manifest["input_ready_before_heap"],
        "startup_reload_degraded": manifest["startup_reload_degraded"],
        "required_reload_passed": manifest["required_reload_passed"],
        "optional_reload_passed": manifest["optional_reload_passed"],
        "request_file": manifest.get("request_file", ""),
        "request_chars": manifest.get("request_chars", 0),
        "request_sha256": manifest.get("request_sha256", ""),
        "context_file_count": manifest.get("context_file_count", 0),
        "artifact_count": len(manifest.get("artifacts", {})),
        "tool_execution_count": len(manifest.get("tool_executions", [])),
        "blocking_requirements": manifest.get("blocking_requirements", []),
        "degraded_requirements": manifest.get("degraded_requirements", []),
        "optional_failed_requirements": manifest.get("optional_failed_requirements", []),
        "manifest": repo_rel(repo_root, manifest_path),
        "markdown": repo_rel(repo_root, manifest_md),
        "heap_task_file": manifest.get("heap_task_file", ""),
    }
    print(json.dumps(print_payload, indent=2, ensure_ascii=False))
    return 0 if passed or (input_ready_before_heap and not strict_startup) else 2


if __name__ == "__main__":
    raise SystemExit(main())
