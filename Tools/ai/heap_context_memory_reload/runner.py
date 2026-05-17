"""Runtime orchestration for heap startup reload."""

from __future__ import annotations

import json
from pathlib import Path

from Tools.ai.heap_context_memory_reload.builders import (
    build_repo_docs_map,
    collect_semantic_code_chunks,
    write_semantic_evidence,
)
from Tools.ai.heap_context_memory_reload.common import read_json, repo_rel, run_tool, write_json
from Tools.ai.heap_context_memory_reload.manifest import (
    build_manifest,
    build_print_payload,
)
from Tools.ai.heap_context_memory_reload.memory_write import (
    build_final_task_markdown,
    run_operational_memory_write,
)
from Tools.ai.heap_context_memory_reload.runner_state import ReloadRun
from Tools.ai.heap_context_memory_reload.scanner import existing_context_files


def run_reload(state: ReloadRun) -> int:
    state.output_dir.mkdir(parents=True, exist_ok=True)
    _run_required_context(state)
    _build_context_maps(state)
    _run_tool_catalog(state)
    _run_memory_inventory(state)
    _run_operational_memory_reads(state)
    _run_transient_context(state)
    _run_ai_context_pack(state)
    state.artifacts.update(write_semantic_evidence(state.commands, state.repo_root, state.output_dir))
    task_file = state.output_dir / "heap_startup_input_ready_context.md"
    state.artifacts["heap_task_file"] = repo_rel(state.repo_root, task_file)
    run_operational_memory_write(state)
    task_markdown = build_final_task_markdown(state)
    task_file.write_text(task_markdown, encoding="utf-8")
    manifest = build_manifest(
        stamp=state.stamp,
        repo_root=state.repo_root,
        project_python=state.project_python,
        request_text=state.request_text,
        context_files=state.context_files,
        artifacts=state.artifacts,
        commands=state.commands,
        warnings=state.warnings,
        task_file=task_file,
        context_pack_result=state.context_pack_result,
        strict_ai_context_pack=bool(state.args.strict_ai_context_pack),
        strict_startup_reload=bool(state.args.strict_startup_reload),
    )
    manifest_path = state.output_dir / "heap_context_memory_reload_manifest.json"
    manifest_md = state.output_dir / "heap_context_memory_reload_manifest.md"
    write_json(manifest_path, manifest)
    manifest_md.write_text(task_markdown, encoding="utf-8")
    print_payload = build_print_payload(manifest, state.repo_root, manifest_path, manifest_md)
    print(json.dumps(print_payload, indent=2, ensure_ascii=False))
    strict_startup = bool(state.args.strict_startup_reload or state.args.strict_ai_context_pack)
    return 0 if manifest["passed"] or (manifest["input_ready_before_heap"] and not strict_startup) else 2


def _run_required_context(state: ReloadRun) -> None:
    context_json = state.output_dir / "startup_required_ai_context_files.json"
    context_md = state.output_dir / "startup_required_ai_context_files.md"
    state.commands.append(
        run_tool(
            [
                state.project_python,
                "-m",
                "Tools.ai",
                "ensure_ai_context_required_files",
                "--repo-root",
                ".",
                "--profile",
                "project_self_improvement",
                "--output",
                str(context_json),
                "--markdown-output",
                str(context_md),
                "--apply",
            ],
            state.repo_root,
            name="required_context_files_reload",
            requirement="required_context_files",
            required=True,
            artifact_paths=[context_json, context_md],
        )
    )
    state.artifacts["required_context_files_json"] = repo_rel(state.repo_root, context_json)
    state.artifacts["required_context_files_markdown"] = repo_rel(state.repo_root, context_md)


def _build_context_maps(state: ReloadRun) -> None:
    state.context_files = existing_context_files(
        state.repo_root,
        max_files=state.args.startup_scan_context_files,
    )
    state.artifacts.update(build_repo_docs_map(state.repo_root, state.context_files, state.output_dir))
    state.artifacts.update(
        collect_semantic_code_chunks(
            state.repo_root,
            state.output_dir,
            state.request_text,
            limit=max(12, min(state.args.max_context_files, 64)),
        )
    )


def _run_tool_catalog(state: ReloadRun) -> None:
    tool_catalog_json = state.output_dir / "startup_tool_catalog.json"
    tool_catalog_md = state.output_dir / "startup_tool_catalog.md"
    state.commands.append(
        run_tool(
            [
                state.project_python,
                "-m",
                "Tools.ai",
                "build_agent_agnostic_tool_inventory",
                "--repo-root",
                ".",
                "--output",
                str(tool_catalog_json),
                "--markdown-output",
                str(tool_catalog_md),
            ],
            state.repo_root,
            name="tool_catalog_reload",
            requirement="tool_catalog",
            required=True,
            artifact_paths=[tool_catalog_json, tool_catalog_md],
        )
    )
    state.artifacts["tool_catalog_json"] = repo_rel(state.repo_root, tool_catalog_json)
    state.artifacts["tool_catalog_markdown"] = repo_rel(state.repo_root, tool_catalog_md)


def _run_memory_inventory(state: ReloadRun) -> None:
    memory_json = state.output_dir / "startup_memory_inventory.json"
    memory_md = state.output_dir / "startup_memory_inventory.md"
    state.commands.append(
        run_tool(
            [
                state.project_python,
                "-m",
                "Tools.ai",
                "build_agent_memory_inventory",
                "--repo-root",
                ".",
                "--objective",
                state.request_text or "heap startup memory reload",
                "--max-memory-chars",
                str(state.args.max_memory_chars),
                "--output",
                str(memory_json),
                "--markdown-output",
                str(memory_md),
            ],
            state.repo_root,
            name="shared_memory_reload",
            requirement="shared_memory",
            required=True,
            artifact_paths=[memory_json, memory_md],
        )
    )
    state.artifacts["shared_memory_json"] = repo_rel(state.repo_root, memory_json)
    state.artifacts["shared_memory_markdown"] = repo_rel(state.repo_root, memory_md)


def _run_operational_memory_reads(state: ReloadRun) -> None:
    status_json = state.output_dir / "startup_operational_memory_status.json"
    status_md = state.output_dir / "startup_operational_memory_status.md"
    search_json = state.output_dir / "startup_operational_memory_search.json"
    search_md = state.output_dir / "startup_operational_memory_search.md"
    _run_memory_action(state, "status", [], status_json, status_md, "operational_memory_status")
    _run_memory_action(
        state,
        "search",
        ["--query", "heap context memory reload provider proposal GPU0 NPU", "--limit", "20"],
        search_json,
        search_md,
        "operational_memory_search",
    )


def _run_memory_action(
    state: ReloadRun,
    action: str,
    extra: list[str],
    output_json: Path,
    output_md: Path,
    requirement: str,
) -> None:
    state.commands.append(
        run_tool(
            [
                state.project_python,
                "-m",
                "Tools.ai",
                "agent_runtime_sqlite_memory",
                "--repo-root",
                ".",
                "--action",
                action,
                "--scope",
                "operational",
                *extra,
                "--output",
                str(output_json),
                "--markdown-output",
                str(output_md),
            ],
            state.repo_root,
            name=f"{requirement}_reload",
            requirement=requirement,
            required=False,
            artifact_paths=[output_json, output_md],
        )
    )
    state.artifacts[f"{requirement}_json"] = repo_rel(state.repo_root, output_json)
    state.artifacts[f"{requirement}_markdown"] = repo_rel(state.repo_root, output_md)


def _run_transient_context(state: ReloadRun) -> None:
    startup_request_file = state.output_dir / "heap_startup_request.md"
    startup_request_file.write_text(state.request_text or "heap startup request", encoding="utf-8")
    raw_file_list = state.output_dir / "startup_context_raw_files.txt"
    raw_file_list.write_text("\n".join(state.context_files) + "\n", encoding="utf-8")
    state.artifacts["startup_context_raw_file_list"] = repo_rel(state.repo_root, raw_file_list)
    transient_json = state.output_dir / "startup_transient_request_context.json"
    transient_md = state.output_dir / "startup_transient_request_context.md"
    state.commands.append(
        run_tool(
            [
                state.project_python,
                "-m",
                "Tools.ai",
                "build_agent_transient_request_context",
                "--repo-root",
                ".",
                "--objective",
                "heap startup context/memory reload before provider lanes",
                "--memory-note-file",
                str(startup_request_file),
                "--raw-file-list",
                str(raw_file_list),
                "--report-file",
                str(state.output_dir / "startup_tool_catalog.json"),
                "--report-file",
                str(state.output_dir / "startup_memory_inventory.json"),
                "--report-file",
                str(state.output_dir / "startup_operational_memory_status.json"),
                "--report-file",
                str(state.output_dir / "startup_operational_memory_search.json"),
                "--max-raw-files",
                str(min(state.args.startup_scan_context_files, max(state.args.max_context_files, 240))),
                "--max-chars-per-file",
                str(state.args.max_chars_per_file),
                "--output",
                str(transient_json),
                "--markdown-output",
                str(transient_md),
            ],
            state.repo_root,
            name="shared_context_reload",
            requirement="shared_context_chunks",
            required=True,
            artifact_paths=[transient_json, transient_md],
        )
    )
    state.artifacts["shared_context_json"] = repo_rel(state.repo_root, transient_json)
    state.artifacts["shared_context_markdown"] = repo_rel(state.repo_root, transient_md)
    state.artifacts["startup_request_file"] = repo_rel(state.repo_root, startup_request_file)


def _run_ai_context_pack(state: ReloadRun) -> None:
    pack_dir = state.output_dir / "startup_ai_context_pack"
    evidence_dir = state.output_dir / "startup_ai_context_pack_evidence"
    basename = f"heap_startup_context_pack_{state.stamp}"
    pack_json = pack_dir / f"{basename}.json"
    pack_md = pack_dir / f"{basename}.md"
    evidence_json = evidence_dir / f"{basename}_evidence.json"
    evidence_md = evidence_dir / f"{basename}_evidence.md"
    state.context_pack_result = run_tool(
        [
            state.project_python,
            "-m",
            "Tools.ai",
            "build_ai_context_pack",
            "--repo-root",
            ".",
            "--profile",
            "project_self_improvement",
            "--output-dir",
            str(pack_dir),
            "--basename",
            basename,
            "--evidence-dir",
            str(evidence_dir),
            "--evidence-basename",
            f"{basename}_evidence",
        ],
        state.repo_root,
        name="ai_context_pack_reload",
        requirement="ai_context_pack",
        required=bool(state.args.strict_ai_context_pack),
        artifact_paths=[pack_json, pack_md, evidence_json, evidence_md],
    )
    state.commands.append(state.context_pack_result)
    state.artifacts["ai_context_pack_json"] = repo_rel(state.repo_root, pack_json)
    state.artifacts["ai_context_pack_markdown"] = repo_rel(state.repo_root, pack_md)
    state.artifacts["ai_context_pack_evidence_json"] = repo_rel(state.repo_root, evidence_json)
    state.artifacts["ai_context_pack_evidence_markdown"] = repo_rel(state.repo_root, evidence_md)
    if state.context_pack_result["degraded"]:
        pack_payload = read_json(pack_json)
        warning = (
            "ai_context_pack_reload returned non-zero "
            + f"rc={state.context_pack_result['returncode']} but useful artifacts exist"
        )
        errors = pack_payload.get("errors") if isinstance(pack_payload.get("errors"), list) else []
        if errors:
            warning += "; errors=" + "; ".join(str(item) for item in errors[:5])
        state.warnings.append(warning)
        warnings = pack_payload.get("warnings") if isinstance(pack_payload.get("warnings"), list) else []
        state.warnings.extend(f"ai_context_pack warning: {item}" for item in warnings[:5])
