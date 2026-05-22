"""GPU1 leader packet builder for same-heap provider teamwork."""

from __future__ import annotations

from ia_carmine.runtime.contractor_universe.surface import build_contractor_universe_surface_contract
from ia_carmine.runtime.heap_gate.provider_time import build_provider_lane_time_contracts
from ia_carmine.runtime.heap_gate.runtime_common import Any, now_iso, repo_rel, safe_dict, safe_int


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


def _compact_provider_reports(gate: Any, limit: int = 6) -> list[dict[str, Any]]:
    reports: list[dict[str, Any]] = []
    for report in reversed(getattr(gate, "provider_reports", []) or []):
        if not isinstance(report, dict):
            continue
        reports.append(
            {
                "lane": report.get("lane"),
                "role": report.get("role"),
                "status": report.get("status"),
                "passed": report.get("passed"),
                "output": report.get("output"),
                "provider_block_id": report.get("provider_block_id"),
                "proposal_block_id": report.get("proposal_block_id"),
                "operational_provider_activity": report.get("operational_provider_activity"),
                "provider_activity_classification": report.get(
                    "provider_activity_classification"
                ),
                "response_text_excerpt": str(report.get("response_text") or "")[:2400],
            }
        )
        if len(reports) >= limit:
            break
    return list(reversed(reports))


def build_provider_teamwork_leader_packet(
    gate: Any, round_id: int, revision: int, leader_prompt: str
) -> dict[str, Any]:
    """Build the shared artifact consumed by all provider lanes.

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
    time_contract = gate.provider_time_counter_contract()
    lane_time_contracts = build_provider_lane_time_contracts(gate.args)
    contractor_surface = build_contractor_universe_surface_contract(gate.args)
    lane_authority = {
        "gpu1_planner": "primary_open_review_close_synthesis",
        "gpu0_peer": "reviewer_refiner_not_primary_closer",
        "npu_micro_task_auditor": "microtask_tool_auditor_not_primary_closer",
    }
    return {
        "kind": "provider_teamwork_leader_packet",
        "role": "gpu1_primary_advisory_leader",
        "lane": "gpu1_planner",
        "revision": revision,
        "round": round_id,
        "created_at": now_iso(),
        "request": gate.request_text(),
        "closure_owner": "gpu1_planner",
        "revision_opened_by_gpu1": True,
        "revision_lane_policy": getattr(gate, "provider_revision_lane_policy", {}),
        "selected_lanes": getattr(gate, "provider_revision_lane_policy", {}).get(
            "selected_lanes",
            ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
        ),
        "lane_authority": lane_authority,
        "native_tool_calling_policy": {
            "gpu1_planner": "open_revision_and_may_drive_broker_native_tool_calls",
            "gpu0_peer": "review_refine_and_may_call_native_tools_as_evidence",
            "npu_micro_task_auditor": "micro_audit_native_tools_only",
        },
        "delta_context_mode": "startup_full_once_then_pointer_delta_revisions",
        "npu_micro_timeout_enforced": bool(
            lane_time_contracts["npu_micro_task_auditor"].get(
                "npu_micro_timeout_enforced"
            )
        ),
        "heap_universe_contract": {
            "chat_is_client": True,
            "heap_is_source_of_truth": True,
            "request_md_is_ingress_only": True,
            "static_files_are_artifacts_not_runtime_database": True,
            "startup_manifest_is_context_data_plane": bool(manifest_path),
            "operational_sqlite_memory_required_when_available": True,
            "same_heap_lanes": ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
            "unified_parallel_execution": True,
            "provider_text_alone_is_not_tool_execution_proof": True,
            "provider_roles_must_coexist_before_pointer_loop": True,
            "composer_assembles_heap_state_only": True,
            "contractor_universe_is_integrated_surface": True,
        },
        "provider_role_coexistence_preflight": getattr(
            gate, "provider_role_coexistence_preflight", {}
        ),
        "provider_boot_gate": getattr(gate, "provider_boot_gate", {}),
        "integrated_surface_map": {
            "ingress": "operator request/request-file through python -m ia_carmine.cli run",
            "startup_preload": "heap_context_memory_reload manifest, memory and context artifacts",
            "runtime_universe": "RepoRuntimeUniverseBuilder file/tool/evidence index",
            "heap_blackboard": "ProviderRuntimeHeap events, snapshot and heap exchange lifecycle",
            "contractor_scheduler": "contractor_universe UniverseHeap/LogicalClock semantics",
            "provider_lanes": "GPU1 primary, GPU0 coworker/refiner, NPU microtask/auditor",
            "broker": "runtime_tool broker and provider_runtime_broker_bridge",
            "memory_chunks": "SQLite memory, transient context, semantic code/evidence chunks",
            "matrix_lab": "code execution matrix, virtual dev environment and debug lab",
            "product_boundary": "patch candidate synthesis and CODE_PRODUCT_FULL_PATCH reconstruction",
        },
        "contractor_universe_surface_contract": contractor_surface,
        "time_counter_contract": time_contract,
        "lane_time_contracts": lane_time_contracts,
        "same_heap_teamwork_contract": [
            "GPU1 is the primary advisor/leader and must produce file-grounded proposal blocks.",
            "GPU0 is a stronger peer/reviewer/refiner lane and may do more sophisticated support work than NPU.",
            "NPU is a micro/audit lane and must not become the primary advisory or broker-driving center.",
            "All provider lanes start in the same provider universe; failure to start any selected lane blocks the universe.",
            "GPU1 commands final synthesis and integrates GPU0/NPU vetoes and refinement signals.",
            "Only GPU1 native tool calls may drive broker work; GPU0/NPU tool calls are peer diagnostics.",
            "GPU0 and NPU remain parallel peer lanes inside the same heap, not alternate product routes.",
            "GPU1 must consume GPU0/NPU peer evidence before final synthesis.",
            "GPU0 and NPU are bounded sidecars: their watchdogs prevent them from holding closure ownership.",
            "The time input is a shared counter for GPU1 closure; sidecars publish bounded evidence or timeout reports.",
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
        "primary_provider_evidence": _compact_provider_reports(gate, limit=6),
        "revision_feedback": str(gate.provider_revision_feedback or ""),
        "leader_prompt_excerpt": leader_prompt[:6000],
    }
