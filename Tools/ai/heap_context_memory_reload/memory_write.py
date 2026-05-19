"""Operational-memory write step for heap startup reload."""

from __future__ import annotations

from argparse import Namespace
import json

from Tools.ai.agent_memory.common import DEFAULT_OPERATIONAL_DB, DEFAULT_PERSISTENT_DB
from Tools.ai.agent_memory.sqlite_report import (
    build_report as build_sqlite_memory_report,
    render_markdown as render_sqlite_memory_markdown,
)
from Tools.ai.heap_context_memory_reload.common import (
    repo_rel,
    summarize_artifact,
    write_json,
)
from Tools.ai.heap_context_memory_reload.manifest import requirement_status
from Tools.ai.heap_context_memory_reload.runner_state import ReloadRun
from Tools.ai.heap_context_memory_reload.task_docs import (
    build_operational_memory_write_content,
    build_task_markdown,
)


def run_operational_memory_write(state: ReloadRun) -> None:
    _required, _optional, blocking, degraded, optional_failed = requirement_status(state.commands)
    startup_reload_degraded = bool(degraded or optional_failed)
    content = build_operational_memory_write_content(
        stamp=state.stamp,
        request=state.request_text,
        startup_reload_degraded=startup_reload_degraded,
        degraded_requirements=degraded,
        blocking_requirements=blocking,
        artifacts=state.artifacts,
        commands=state.commands,
    )
    output_json = state.output_dir / "startup_operational_memory_write.json"
    output_md = state.output_dir / "startup_operational_memory_write.md"
    command = ["in_process", "Tools.ai.agent_memory.sqlite_report.build_report"]
    try:
        memory_args = Namespace(
            repo_root=str(state.repo_root),
            action="remember",
            scope="operational",
            database=DEFAULT_OPERATIONAL_DB,
            persistent_database=DEFAULT_PERSISTENT_DB,
            request_id=f"heap_startup_reload_{state.stamp}",
            summary="startup context/memory reload manifest",
            content=content,
            content_file="",
            role="heap_startup_reload",
            tag=["heap_startup_context", state.stamp],
            query="",
            limit=20,
            confirm="",
            allow_persistent_write=False,
            output=str(output_json),
            markdown_output=str(output_md),
        )
        report = build_sqlite_memory_report(memory_args)
        write_json(output_json, report)
        output_md.write_text(render_sqlite_memory_markdown(report), encoding="utf-8")
        stdout = json.dumps(
            {
                "passed": report.get("passed"),
                "scope": report.get("scope"),
                "operational_sqlite_write_performed": report.get(
                    "operational_sqlite_write_performed"
                ),
                "sqlite_search_backend": report.get("sqlite_search_backend"),
                "request_transport": "in_memory",
            },
            ensure_ascii=False,
        )
        returncode = 0 if report.get("passed") is True else 2
        stderr = ""
    except Exception as exc:  # noqa: BLE001
        stdout = ""
        stderr = f"{type(exc).__name__}: {exc}"
        returncode = 1
    artifacts = [summarize_artifact(path, state.repo_root) for path in [output_json, output_md]]
    useful_artifacts = [item["path"] for item in artifacts if item.get("useful")]
    state.commands.append(
        {
            "name": "operational_memory_write_reload",
            "requirement": "operational_memory_write",
            "required": False,
            "command": command,
            "returncode": returncode,
            "passed": returncode == 0,
            "effective_passed": returncode == 0 or bool(useful_artifacts),
            "degraded": returncode != 0 and bool(useful_artifacts),
            "hard_failed": returncode != 0 and not bool(useful_artifacts),
            "artifact_useful": bool(useful_artifacts),
            "artifact_paths": [item["path"] for item in artifacts],
            "existing_artifact_paths": [item["path"] for item in artifacts if item.get("exists")],
            "useful_artifact_paths": useful_artifacts,
            "artifact_summaries": artifacts,
            "stdout_tail": stdout[-3000:],
            "stderr_tail": stderr[-3000:],
        }
    )
    state.artifacts["operational_memory_write_json"] = repo_rel(state.repo_root, output_json)
    state.artifacts["operational_memory_write_markdown"] = repo_rel(state.repo_root, output_md)


def build_final_task_markdown(state: ReloadRun) -> str:
    _required, _optional, blocking, degraded, optional_failed = requirement_status(state.commands)
    return build_task_markdown(
        repo_root=state.repo_root,
        request=state.request_text,
        stamp=state.stamp,
        context_files=state.context_files,
        artifacts=state.artifacts,
        commands=state.commands,
        warnings=state.warnings,
        startup_reload_degraded=bool(degraded or optional_failed),
        degraded_requirements=degraded,
        blocking_requirements=blocking,
    )
