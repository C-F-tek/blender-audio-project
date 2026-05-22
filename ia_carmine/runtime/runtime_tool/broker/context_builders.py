"""Allowlisted context, semantic-chunk, debug-lab and memory builders."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ia_carmine.providers.provider_mesh.runtime.python_runtime import resolve_child_python

from .common import base_outputs, repo_rel, resolve_path, safe_id, split_values, truthy


def build_ai_context_pack_tool(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    profile = str(args.get("profile") or "core_ai_backend")
    basename = safe_id(args.get("basename") or request_id, "ai_context_pack")
    output_dir = resolve_path(
        repo_root, str(args.get("output_dir") or out_dir / f"{request_id}_context_pack")
    )
    evidence_dir = resolve_path(
        repo_root,
        str(args.get("evidence_dir") or out_dir / f"{request_id}_context_pack_evidence"),
    )
    evidence_basename = safe_id(
        args.get("evidence_basename") or f"{basename}_evidence",
        "ai_context_pack_evidence",
    )
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "ai_context_pack",
        "--repo-root",
        ".",
        "--profile",
        profile,
        "--basename",
        basename,
        "--output-dir",
        repo_rel(output_dir, repo_root),
        "--evidence-dir",
        repo_rel(evidence_dir, repo_root),
        "--evidence-basename",
        evidence_basename,
        "--max-total-chars",
        str(args.get("max_total_chars") or 64000),
        "--max-file-chars",
        str(args.get("max_file_chars") or 4000),
    ]
    if truthy(args.get("no_evidence")):
        command.append("--no-evidence")
    pack_json = output_dir / f"{basename}.json"
    pack_md = output_dir / f"{basename}.md"
    evidence_json = evidence_dir / f"{evidence_basename}.json"
    evidence_md = evidence_dir / f"{evidence_basename}.md"
    return command, {
        "json_report": repo_rel(pack_json, repo_root),
        "markdown_report": repo_rel(pack_md, repo_root),
        "evidence_json": repo_rel(evidence_json, repo_root),
        "evidence_markdown": repo_rel(evidence_md, repo_root),
    }


def build_semantic_evidence_chunk_manifest(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    basename = safe_id(args.get("basename") or request_id, "semantic_evidence_chunks")
    output_dir = resolve_path(
        repo_root,
        str(args.get("output_dir") or out_dir / f"{request_id}_semantic_chunks"),
    )
    chunk_dir = resolve_path(
        repo_root,
        str(args.get("chunk_output_dir") or output_dir / f"{basename}_chunks"),
    )
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "semantic_evidence_chunks",
        "--repo-root",
        ".",
        "--basename",
        basename,
        "--output-dir",
        repo_rel(output_dir, repo_root),
        "--chunk-output-dir",
        repo_rel(chunk_dir, repo_root),
        "--chunk-max-chars",
        str(args.get("chunk_max_chars") or 12000),
        "--chunk-overlap-lines",
        str(args.get("chunk_overlap_lines") or 12),
        "--no-ollama",
    ]
    for source in split_values(args.get("source")):
        command.extend(["--source", source])
    zip_output = str(args.get("zip_output") or "").strip()
    if zip_output:
        command.extend(["--zip-output", zip_output])
    manifest_json = output_dir / f"{basename}_chunk_manifest.json"
    manifest_md = output_dir / f"{basename}_chunk_manifest.md"
    return command, {
        "json_report": repo_rel(manifest_json, repo_root),
        "markdown_report": repo_rel(manifest_md, repo_root),
        "chunk_output_dir": repo_rel(chunk_dir, repo_root),
    }


def run_agent_runtime_debug_lab(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    request_file = str(args.get("request_file") or "").strip()
    request_json = args.get("request_json")
    report = resolve_path(
        repo_root,
        str(args.get("output") or out_dir / f"{request_id}_agent_runtime_debug_lab.json"),
    )
    markdown = resolve_path(
        repo_root,
        str(args.get("markdown_output") or out_dir / f"{request_id}_agent_runtime_debug_lab.md"),
    )
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "agent_runtime_debug_lab",
        "--repo-root",
        ".",
        "--output",
        repo_rel(report, repo_root),
        "--markdown-output",
        repo_rel(markdown, repo_root),
    ]
    if request_json is not None:
        command = ["in_process", "ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.runner.run_request"]
    elif request_file:
        command.extend(["--request-file", request_file])
    if args.get("timeout_seconds") is not None:
        command.extend(["--timeout-seconds", str(args.get("timeout_seconds"))])
    if args.get("tail_chars") is not None:
        command.extend(["--tail-chars", str(args.get("tail_chars"))])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
        "request_file": request_file,
        "request_transport": "in_memory" if request_json is not None else "request_file",
    }


def runtime_sqlite_memory(
    repo_root: Path, out_dir: Path, request_id: str, args: dict[str, Any]
) -> tuple[list[str], dict[str, str]]:
    report, markdown = base_outputs(out_dir, request_id, "runtime_sqlite_memory")
    command = [
        resolve_child_python(repo_root),
        "-m",
        "ia_carmine",
        "agent_runtime_sqlite_memory",
        "--repo-root",
        ".",
        "--action",
        str(args.get("action") or "status"),
        "--scope",
        str(args.get("scope") or "operational"),
        "--request-id",
        request_id,
        "--output",
        str(report),
        "--markdown-output",
        str(markdown),
    ]
    for source, flag in (
        ("database", "--database"),
        ("persistent_database", "--persistent-database"),
        ("summary", "--summary"),
        ("content", "--content"),
        ("role", "--role"),
        ("query", "--query"),
        ("confirm", "--confirm"),
    ):
        if args.get(source) is not None:
            command.extend([flag, str(args[source])])
    if args.get("limit") is not None:
        command.extend(["--limit", str(args["limit"])])
    if truthy(args.get("allow_persistent_write")):
        command.append("--allow-persistent-write")
    for tag in split_values(args.get("tag")):
        command.extend(["--tag", tag])
    return command, {
        "json_report": repo_rel(report, repo_root),
        "markdown_report": repo_rel(markdown, repo_root),
    }
