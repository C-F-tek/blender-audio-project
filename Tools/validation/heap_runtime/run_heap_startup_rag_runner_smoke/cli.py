#!/usr/bin/env python3
"""Execute the startup RAG runner path with fixture artifacts only."""

from __future__ import annotations

import argparse
import json
import tempfile
from argparse import Namespace
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine.context.heap_context_memory_reload.runner_state import ReloadRun
from ia_carmine.context.heap_context_memory_reload.common import write_json
from ia_carmine.context.heap_context_memory_reload import rag_startup
from ia_carmine.context.heap_context_memory_reload.runner import record_inprocess_tool as runner_record_tool
from ia_carmine.runtime.heap_context_closure.requesting import startup_can_continue


def _tool_result(
    *,
    name: str,
    requirement: str,
    required: bool,
    command: list[str],
    artifact_paths: list[Path],
) -> dict[str, Any]:
    return {
        "name": name,
        "requirement": requirement,
        "required": required,
        "command": command,
        "returncode": 0,
        "passed": True,
        "effective_passed": True,
        "degraded": False,
        "hard_failed": False,
        "artifact_useful": True,
        "artifact_paths": [str(path) for path in artifact_paths],
        "existing_artifact_paths": [str(path) for path in artifact_paths],
        "useful_artifact_paths": [str(path) for path in artifact_paths],
        "artifact_summaries": [],
        "stdout_tail": "",
        "stderr_tail": "",
    }


def _fake_run_tool(
    command: list[str],
    _repo_root: Path,
    *,
    name: str,
    requirement: str,
    required: bool,
    artifact_paths: list[Path] | None = None,
) -> dict[str, Any]:
    paths = artifact_paths or []
    json_path = next(path for path in paths if path.suffix == ".json")
    md_path = next(path for path in paths if path.suffix == ".md")
    payload = {
        "schema_version": 1,
        "kind": "rag_context_pack",
        "passed": True,
        "context_pack_id": "fixture-rag-pack",
        "retrieved_count": 1,
        "total_selected_chars": 42,
        "sources": ["docs/fixture.md"],
        "chunks": [
            {
                "chunk_id": "fixture-chunk",
                "source_path": "docs/fixture.md",
                "chunk_index": 0,
                "char_start": 0,
                "char_end": 42,
                "text": "GPU1 evidence is anchored to a real file.",
                "text_hash": "fixture-hash",
                "fused_score": 1.0,
            }
        ],
        "retrieval_event_id": "fixture-event",
        "warnings": [],
        "errors": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json(json_path, payload)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    md_path.write_text("# Fixture RAG Context Pack\n", encoding="utf-8")
    return _tool_result(
        name=name,
        requirement=requirement,
        required=required,
        command=command,
        artifact_paths=paths,
    )


def run_smoke() -> dict[str, Any]:
    errors: list[str] = []
    checks: list[dict[str, Any]] = []
    original_run_tool = rag_startup.run_tool
    try:
        with tempfile.TemporaryDirectory(prefix="startup-rag-runner-smoke-") as temp:
            repo = Path(temp) / "repo"
            output_dir = repo / "output" / "startup"
            output_dir.mkdir(parents=True, exist_ok=True)
            ai_json = output_dir / "ai_context_pack.json"
            write_json(
                ai_json,
                {
                    "schema_version": 1,
                    "kind": "ai_context_pack",
                    "passed": True,
                    "generated_at": "fixture",
                    "included_file_count": 1,
                    "files": [{"path": "docs/fixture.md", "role": "fixture"}],
                    "warnings": [],
                    "errors": [],
                },
            )
            state = ReloadRun(
                args=Namespace(
                    request_file="",
                    rag_db="output/ai_runtime_memory/rag/rag.sqlite",
                    rag_profile="runtime_code_context",
                    rag_top_k=4,
                    rag_char_budget=8000,
                    rag_embedding_endpoint="mock://fixture",
                    rag_embedding_model="bge-m3",
                    rag_skip_query_embedding=True,
                ),
                repo_root=repo,
                stamp="fixture",
                project_python="python",
                output_dir=output_dir,
                request_text="GPU1 generic_write evidence must use startup RAG.",
            )
            state.artifacts["ai_context_pack_json"] = "output/startup/ai_context_pack.json"
            rag_startup.run_tool = _fake_run_tool
            rag_startup.write_startup_progress(
                state,
                step="rag_ingest_embeddings",
                extra={
                    "rag_index_ready": False,
                    "embedding_written_count": 7,
                    "missing_embedding_count_after": 1,
                },
            )
            progress_path = output_dir / "startup_rag_progress.json"
            progress_payload = json.loads(progress_path.read_text(encoding="utf-8"))
            checks.append(
                {
                    "id": "rag_progress_exposes_gpu1_embedding_activity",
                    "passed": progress_payload.get("step") == "rag_ingest_embeddings"
                    and progress_payload.get("resource_lane") == "ollama_embedding_gpu1"
                    and progress_payload.get("ollama_embedding_performed") is True
                    and progress_payload.get("provider_execution_performed") is False
                    and progress_payload.get("providers_not_started_reason")
                    == "startup_rag_index_not_ready",
                    "evidence": progress_payload,
                }
            )
            can_continue = startup_can_continue(
                startup_result={"passed": False, "returncode": 2},
                startup_payload={
                    "input_ready_before_heap": False,
                    "blocking_requirements": ["rag_repo_ingest"],
                    "artifacts": {},
                },
                startup_task_file=output_dir / "heap_startup_input_ready_context.md",
                strict_startup_reload=False,
                skipped=False,
            )
            checks.append(
                {
                    "id": "rag_block_prevents_provider_start",
                    "passed": can_continue is False,
                    "evidence": {"startup_can_continue": can_continue},
                }
            )
            rag_startup.run_rag_context_pack(state)
            rag_startup.write_unified_context_pack(state, record_tool=runner_record_tool)
            checks.append(
                {
                    "id": "rag_context_pack_ref_written",
                    "passed": bool(state.artifacts.get("rag_context_pack_json")),
                    "evidence": state.artifacts.get("rag_context_pack_json", ""),
                }
            )
            checks.append(
                {
                    "id": "retrieval_event_id_recorded",
                    "passed": state.artifacts.get("rag_retrieval_event_id") == "fixture-event",
                    "evidence": state.artifacts.get("rag_retrieval_event_id", ""),
                }
            )
            checks.append(
                {
                    "id": "unified_context_pack_written",
                    "passed": bool(state.artifacts.get("startup_context_pack_json"))
                    and (repo / state.artifacts["startup_context_pack_json"]).exists(),
                    "evidence": state.artifacts.get("startup_context_pack_json", ""),
                }
            )
            checks.append(
                {
                    "id": "all_required_records_passed",
                    "passed": all(item.get("effective_passed") for item in state.commands),
                    "evidence": [item.get("requirement") for item in state.commands],
                }
            )
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{type(exc).__name__}: {exc}")
    finally:
        rag_startup.run_tool = original_run_tool
    errors.extend(str(item["id"]) for item in checks if not item.get("passed"))
    return {
        "schema_version": 1,
        "kind": "heap_startup_rag_runner_smoke",
        "passed": not errors,
        "checks": checks,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_startup_rag_runner_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke()
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
