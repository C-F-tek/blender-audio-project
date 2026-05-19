"""GPU1 leader packet builder for same-heap provider teamwork."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import Any, now_iso, repo_rel, safe_dict, safe_int


def _compact_artifacts(artifacts: dict[str, Any], limit: int = 24) -> dict[str, str]:
    selected: dict[str, str] = {}
    priority = (
        "tool_catalog_json",
        "tool_catalog_markdown",
        "operational_memory_search_json",
        "operational_memory_search_markdown",
        "semantic_code_chunks_json",
        "semantic_code_chunks_markdown",
        "semantic_evidence_chunks_json",
        "semantic_evidence_chunks_markdown",
        "ai_context_pack_json",
        "ai_context_pack_markdown",
        "shared_context_json",
        "shared_memory_json",
        "repo_docs_map_json",
        "required_context_files_json",
        "heap_task_file",
    )
    for key in priority:
        value = str(artifacts.get(key) or "").strip()
        if value:
            selected[key] = value
        if len(selected) >= limit:
            break
    return selected


def build_provider_teamwork_leader_packet(
    gate: Any, round_id: int, revision: int, leader_prompt: str
) -> dict[str, Any]:
    """Build the artifact consumed by GPU0/NPU before they start.

    The packet is not a cosmetic launch note. It is the compact same-heap
    contract: startup artifacts, universe report refs, source allowlist,
    broker/tool evidence and pointer/resume rules become provider input.
    """
    events = gate.read_events()
    manifest_path, manifest = gate.startup_manifest_from_task_file()
    artifacts = (
        manifest.get("artifacts")
        if isinstance(manifest, dict) and isinstance(manifest.get("artifacts"), dict)
        else {}
    )
    universe_refs = gate.write_runtime_universe_report()
    heap_paths = {
        "events": repo_rel(gate.repo_root, gate.heap.paths.events),
        "snapshot": repo_rel(gate.repo_root, gate.heap.paths.snapshot),
        "markdown": repo_rel(gate.repo_root, gate.heap.paths.markdown),
    }
    return {
        "kind": "provider_teamwork_leader_packet",
        "role": "gpu1_primary_advisory_leader",
        "lane": "gpu1_planner",
        "revision": revision,
        "round": round_id,
        "created_at": now_iso(),
        "request": gate.request_text(),
        "heap_universe_contract": {
            "chat_is_client": True,
            "heap_is_source_of_truth": True,
            "request_md_is_ingress_only": True,
            "static_files_are_artifacts_not_runtime_database": True,
            "startup_manifest_is_context_data_plane": bool(manifest_path),
            "operational_sqlite_memory_required_when_available": True,
            "same_heap_lanes": ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
            "provider_text_alone_is_not_tool_execution_proof": True,
            "composer_assembles_heap_state_only": True,
        },
        "same_heap_teamwork_contract": [
            "GPU1 is the primary advisor/leader and must produce file-grounded proposal blocks.",
            "GPU0 is a parallel peer and may jump through previous/refines/resume pointers to review/refine impacted blocks.",
            "NPU is a parallel peer and may jump through previous/refines/resume pointers to audit impacted blocks.",
            "GPU1 commands final synthesis and integrates GPU0/NPU vetoes and refinement signals.",
            "Broker/tool calls are optional enrichment, but executed tool outputs become heap facts.",
            "GPU1 must consume GPU0/NPU peer evidence before final synthesis.",
        ],
        "pointer_contract": {
            "previous_block_id": "navigate backward through persisted proposal blocks",
            "next_block_id": "resume forward after back-refinement",
            "refines_block_id": "connect refinement to the block it changes",
            "resume_from_block_id": "restart from the correct cursor after propagation",
            "gpu1_authority": "leader may backtrack/propagate/resume and command synthesis",
            "gpu0_peer_authority": "peer may backtrack/review/refine impacted blocks",
            "npu_peer_authority": "peer may backtrack/audit impacted blocks",
            "requires_concrete_rewrite": (
                "rewrite non-concrete candidates before symbol propagation"
            ),
            "no_patchable_target_exit": "EXIT_DECISION=NO_PATCHABLE_TARGET",
        },
        "startup_context_plane": {
            "primary": "heap_context_memory_reload_manifest.json",
            "readable_task_md": "artifact_reference_only_not_runtime_database",
            "memory": "operational SQLite write/search plus shared/persistent inventory evidence",
            "context": "semantic chunks, AI context pack, repo docs map and broker outputs",
            "target_resolution": "runtime_file_refs resolves source targets before lab/matrix",
            "tool_execution": "broker-owned tool calls only; provider text is not execution",
        },
        "propagation_contract": [
            "An import, variable, class or contract discovered later creates propagation tasks for earlier compatible blocks.",
            "If requires_concrete_rewrite=true, rewrite sketch/stub candidates before propagating symbols.",
            "GPU1 commands propagation, then GPU0 and NPU can independently jump to affected pointers and re-evaluate in parallel before GPU1 resumes forward.",
            "Use only verified repo-relative source paths from SOURCE_PATH_ALLOWLIST_CONTRACT.",
            "If no target is verifiable, return EXIT_DECISION=NO_PATCHABLE_TARGET.",
        ],
        "startup_manifest": repo_rel(gate.repo_root, manifest_path) if manifest_path else "",
        "startup_artifacts": _compact_artifacts(safe_dict(artifacts)),
        "runtime_universe": {
            "summary": gate.repo_runtime_universe.summary(),
            "reports": universe_refs,
        },
        "runtime_heap_refs": heap_paths,
        "broker_tool_catalog": gate.broker_tool_catalog_summary(
            max_items=max(1, safe_int(getattr(gate.args, "tool_catalog_limit", 24), 24))
        ),
        "broker_tool_evidence": gate.tool_evidence_summary(events, max_items=12),
        "source_allowlist_contract": gate.render_source_allowlist_contract(limit=32),
        "verified_source_candidates": gate.real_source_file_candidates(events, limit=32),
        "revision_feedback": str(gate.provider_revision_feedback or ""),
        "leader_prompt_excerpt": leader_prompt[:6000],
    }
