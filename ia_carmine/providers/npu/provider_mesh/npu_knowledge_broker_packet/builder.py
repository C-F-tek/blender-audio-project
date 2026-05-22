"""Packet builder for the NPU knowledge broker."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .candidates import add_candidate
from .common import normalize_path
from .constants import APPLY_MODE, NPU_ROLE, PACKET_KIND
from .sources import add_adapter_manifest, add_context_pack, add_selected_chunks

def build_packet(
    repo_root: Path,
    objective: str,
    selected_chunks: str,
    context_pack: str,
    adapter_manifest: str,
    max_candidates: int,
) -> dict[str, Any]:
    objective_terms = {
        term.lower()
        for term in objective.replace("/", " ").replace("-", " ").replace("_", " ").split()
        if len(term) >= 3
    }
    candidates: dict[str, dict[str, Any]] = {}
    source_refs: dict[str, list[str]] = {
        "selected_chunks": [],
        "context_pack": [],
        "adapter_manifest": [],
    }

    if selected_chunks:
        source_refs["selected_chunks"] = add_selected_chunks(
            candidates, repo_root, selected_chunks, objective_terms
        )
    if context_pack:
        source_refs["context_pack"] = add_context_pack(
            candidates, repo_root, context_pack, objective_terms
        )
    if adapter_manifest:
        source_refs["adapter_manifest"] = add_adapter_manifest(
            candidates, repo_root, adapter_manifest, objective_terms
        )

    # Always keep core contract files visible as fallback context.
    fallback_files = [
        "AGENTS.md",
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
        "docs/LOCAL_AI_WORKFLOW.md",
        "docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md",
        "ia_carmine/context/agent_context/semantic_evidence_chunks/select_code_chunks/cli.py",
        "Tools/validation/agent_context/check_selected_semantic_chunks/cli.py",
        "Tools/validation/pipeline/check_local_ai_adapter_manifest/cli.py",
        "Tools/workflow/_powershell/run_local_ai_task_via_pipeline.ps1",
    ]
    for path in fallback_files:
        if (repo_root / path).exists():
            add_candidate(
                candidates,
                path,
                "fallback_contract",
                objective_terms,
                "core local AI/NPU contract file",
                5,
            )

    ranked = sorted(candidates.values(), key=lambda item: (-int(item["score"]), item["path"]))[
        :max_candidates
    ]
    return {
        "schema_version": 1,
        "kind": PACKET_KIND,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": repo_root.as_posix(),
        "objective": objective,
        "npu_role": NPU_ROLE,
        "apply_mode": APPLY_MODE,
        "provider_execution_performed": False,
        "provider_execution_required": False,
        "source_writes_performed": False,
        "patch_application_performed": False,
        "primary_advisory_provider": "ollama_gpu",
        "npu_promoted_to_advisory": False,
        "openvino_gpu_primary_lane": False,
        "inputs": {
            "selected_chunks": normalize_path(selected_chunks),
            "context_pack": normalize_path(context_pack),
            "adapter_manifest": normalize_path(adapter_manifest),
        },
        "source_refs": source_refs,
        "candidate_count": len(ranked),
        "max_candidates": max_candidates,
        "candidate_context": ranked,
        "decision": {
            "knowledge_broker_packet_built": True,
            "provider_execution_seen": False,
            "source_writes_performed": False,
            "patch_application_performed": False,
            "npu_advisory_promotion_requested": False,
            "requires_primary_advisory_review": True,
        },
        "warnings": [],
        "errors": [],
    }
