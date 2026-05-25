#!/usr/bin/env python3
"""Fixture builder for the heap final readable product smoke."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import write_text_evidence_fields
from ia_carmine._shared.heap_final_readable_synthesis import render_markdown
from ia_carmine.runtime.heap_context_closure.product_state import build_product_state
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import build_gpu1_closure_decision_packet

TRUNCATED_DIFF_MARKER = "[diff " + "truncated]"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def repo_rel(repo_root: Path, path: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def build_fixture(repo_root: Path, work_dir: Path) -> tuple[Path, Path]:
    run_dir = work_dir / "heap_context_closure_smoke"
    documents_dir = work_dir / "documents"
    documents_dir.mkdir(parents=True, exist_ok=True)
    manifest = documents_dir / "DOWNLOADS.txt"
    write_text(manifest, "Smoke package\n")
    fixture_repo = work_dir / "fixture_repo"
    (fixture_repo / "Tools" / "ai").mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "init"], cwd=fixture_repo, text=True, capture_output=True, check=False)
    write_text(fixture_repo / "Tools" / "ai" / "worktree_extra.py", "print('extra')\n")
    matrix_path = run_dir / "broker_bridge" / "tool_outputs" / "smoke_heap_code_execution_tool.json"
    virtual_dev_path = run_dir / "broker_bridge" / "tool_outputs" / "smoke_heap_virtual_dev_environment.json"
    debug_lab_path = run_dir / "debug_lab" / "smoke_debug_lab.json"
    diff_artifact = work_dir / "candidate_diffs" / "final_readable_product.diff"
    full_diff = "diff --git a/ia_carmine/product/code_product/final_readable_product/cli.py b/ia_carmine/product/code_product/final_readable_product/cli.py\n@@\n+FULL_DIFF_SENTINEL = 'present only in artifact diff'\n"
    write_text(diff_artifact, full_diff)
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    provider_dir = run_dir / "provider_teamwork"
    target = "ia_carmine/product/code_product/final_readable_product/cli.py"
    proposal_1 = "smoke:proposal:001"
    proposal_2 = "smoke:proposal:002"
    one_turn_gate_path = provider_dir / "gpu1_one_turn_runtime_gate.json"
    one_turn_fields = {
        "gpu1_one_turn_runtime_gate_present": True,
        "gpu1_one_turn_runtime_gate_path": repo_rel(repo_root, one_turn_gate_path),
        "gpu1_one_turn_runtime_gate_passed": True,
        "gpu1_one_turn_native_tool_call_count": 1,
        "gpu1_one_turn_broker_request_count": 1,
        "gpu1_one_turn_broker_result_count": 1,
        "gpu1_one_turn_broker_result_passed_count": 1,
        "gpu1_one_turn_role_tool_reinjected": True,
        "gpu1_one_turn_tool_result_consumed": True,
        "gpu1_one_turn_final_product_protocol_valid": True,
        "gpu1_one_turn_operator_delta_valid": True,
        "gpu1_one_turn_final_product_delta_valid": True,
        "gpu1_one_turn_blocker": "",
        "gpu1_one_turn_errors": [],
    }
    proposal_1_delta = (
        "Initial smoke final-product delta. This first revision is intentionally "
        "rejected by quality gates and must remain raw evidence, not the product.\n\n"
        + full_diff
    )
    proposal_1_response = (
        "FINAL_PRODUCT_KIND: text_and_code\n"
        "FINAL_PRODUCT_ACTION: append\n"
        "CURRENT_POINTER:\n"
        "- previous_block_id=\n"
        "- refines_block_id=\n"
        "- resume_from_block_id=\n"
        "CONSUMED_EVIDENCE:\n"
        "- consumed_gpu0_block_id=\n"
        "- consumed_npu_block_ids=\n"
        "- tool_or_matrix_refs=\n"
        "NEXT_RUNTIME_INTENT:\n"
        "- wait for sidecar review and refine the final-product delta\n"
        "FINAL_PRODUCT_DELTA:\n"
        + proposal_1_delta
        + "\nTARGET_FILES:\n- "
        + target
        + "\nPROBLEM:\n- smoke rejected first revision\nPATCH_SKETCH_UNIFIED_DIFF:\n"
        + full_diff
    )
    proposal_2_delta = (
        "Refined smoke final-product delta. The final product is one product with "
        "this text surface and a verified code surface.\n\n"
        + full_diff
    )
    proposal_2_response = (
        "FINAL_PRODUCT_KIND: text_and_code\n"
        "FINAL_PRODUCT_ACTION: append\n"
        "CURRENT_POINTER:\n"
        f"- previous_block_id={proposal_1}\n"
        f"- refines_block_id={proposal_1}\n"
        f"- resume_from_block_id={proposal_1}\n"
        "CONSUMED_EVIDENCE:\n"
        "- consumed_gpu0_block_id=smoke:gpu0:002\n"
        "- consumed_npu_block_ids=smoke:npu:002\n"
        f"- tool_or_matrix_refs={repo_rel(repo_root, matrix_path)}\n"
        "NEXT_RUNTIME_INTENT:\n"
        "- compose the final-product text surface deterministically from deltas\n"
        "FINAL_PRODUCT_DELTA:\n"
        + proposal_2_delta
        + "\nTARGET_FILES:\n- "
        + target
        + "\nPATCH_SKETCH_UNIFIED_DIFF:\n"
        + full_diff
    )
    gpu1_packet = build_gpu1_closure_decision_packet(
        gpu1_block_id=proposal_2,
        gpu1_revision=2,
        gpu1_decision="finalize_product",
        target_files=[target],
        quality_passed=True,
        evidence_refs=[repo_rel(repo_root, matrix_path), "smoke:gpu1:002"],
        exit_decision="PATCHABLE_TARGET",
        pointer_action="RESUME_FORWARD",
        refines_block_id=proposal_1,
        consumed_gpu0_block_ids=["smoke:gpu0:002"],
        consumed_npu_block_ids=["smoke:npu:002"],
        response_text=proposal_2_response,
        source="cpu_post_gate_smoke",
    )
    packet_fingerprint = str(gpu1_packet.get("packet_fingerprint") or "")
    write_json(
        proposal_dir / "heap_proposal_revision_001.json",
        {
            "revision": 1,
            "block_id": proposal_1,
            "block_type": "proposal_chunk",
            "previous_block_id": "",
            "next_block_id": proposal_2,
            "refines_block_id": "",
            "resume_from_block_id": "",
            "pointer_action": "STAY_FORWARD",
            "target_files": [target],
            "exit_decision": "PATCHABLE_TARGET",
            "quality_passed": False,
            "accepted": False,
            "final_product_kind": "text_and_code",
            "final_product_action": "append",
            "final_product_delta_valid": True,
            "final_product_protocol": {
                "passed": True,
                "kind": "text_and_code",
                "action": "append",
                "pointer_protocol_operational": True,
                "errors": [],
            },
            **write_text_evidence_fields(
                repo_root,
                run_dir / "text_artifacts",
                prefix="response_text",
                name="proposal_001_response_text",
                text=proposal_1_response,
                kind="smoke_proposal_response_text",
                producer="heap_final_readable_product_smoke",
                suffix=".md",
            ),
            **write_text_evidence_fields(
                repo_root,
                run_dir / "text_artifacts",
                prefix="final_product_delta",
                name="proposal_001_final_product_delta",
                text=proposal_1_delta,
                kind="smoke_final_product_delta",
                producer="heap_final_readable_product_smoke",
                suffix=".md",
            ),
        },
    )
    write_json(
        proposal_dir / "heap_proposal_revision_002.json",
        {
            "revision": 2,
            "block_id": proposal_2,
            "block_type": "proposal_chunk",
            "previous_block_id": proposal_1,
            "next_block_id": "",
            "refines_block_id": proposal_1,
            "resume_from_block_id": proposal_1,
            "pointer_action": "RESUME_FORWARD",
            "target_files": [target],
            "exit_decision": "PATCHABLE_TARGET",
            "gpu1_block_ref": "smoke:gpu1:002",
            "gpu0_review_block_refs": ["smoke:gpu0:002"],
            "npu_audit_block_refs": ["smoke:npu:002"],
            "consumed_block_ids": ["smoke:gpu0:002", "smoke:npu:002"],
            "broker_result_refs": [repo_rel(repo_root, matrix_path)],
            "matrix_report_refs": [repo_rel(repo_root, matrix_path)],
            "gpu1_closure_decision_packet": gpu1_packet,
            "final_product_kind": "text_and_code",
            "final_product_action": "append",
            "final_product_delta_valid": True,
            "final_product_protocol": {
                "passed": True,
                "kind": "text_and_code",
                "action": "append",
                "pointer_protocol_operational": True,
                "errors": [],
            },
            "quality_passed": True,
            "accepted": True,
            **one_turn_fields,
            **write_text_evidence_fields(
                repo_root,
                run_dir / "text_artifacts",
                prefix="response_text",
                name="proposal_002_response_text",
                text=proposal_2_response,
                kind="smoke_proposal_response_text",
                producer="heap_final_readable_product_smoke",
                suffix=".md",
            ),
            **write_text_evidence_fields(
                repo_root,
                run_dir / "text_artifacts",
                prefix="final_product_delta",
                name="proposal_002_final_product_delta",
                text=proposal_2_delta,
                kind="smoke_final_product_delta",
                producer="heap_final_readable_product_smoke",
                suffix=".md",
            ),
        },
    )
    for lane, role, block_type, block_id, action in (
        ("gpu1_planner", "gpu1_planner", "provider_proposal_block", "smoke:gpu1:002", "PROPOSE"),
        ("gpu0_peer", "gpu0_reviewer_refiner", "review_refinement_block", "smoke:gpu0:002", "REFINE"),
        ("npu_micro_task_auditor", "npu_auditor", "audit_block", "smoke:npu:002", "AUDIT"),
    ):
        provider_fields: dict[str, Any] = {}
        if lane == "gpu1_planner":
            provider_fields.update(
                {
                    "provider_backend": "ollama",
                    "provider_compute_device": "ollama/gpu1",
                    "provider_device_verified": True,
                    "provider_loaded": True,
                    "ollama_full_gpu_verified": True,
                    "ollama_compute_verified": True,
                    "done": True,
                    "eval_count": 96,
                    "provider_model": "qwen2.5-coder:14b",
                    **one_turn_fields,
                }
            )
        elif lane == "gpu0_peer":
            provider_fields.update(
                {
                    "provider_backend": "ollama",
                    "provider_compute_device": "ollama/gpu0-vulkan",
                    "provider_device_verified": True,
                    "provider_loaded": True,
                    "ollama_residency_verified": True,
                    "ollama_compute_verified": True,
                    "done": True,
                    "eval_count": 96,
                    "provider_model": "qwen3:1.7b",
                    "gpu0_secondary_schema_valid": True,
                    "gpu0_checked_current_packet": True,
                    "checked_block_id": proposal_2,
                    "checked_gpu1_revision": "2",
                    "expected_gpu1_block_id": proposal_2,
                    "expected_gpu1_revision": "2",
                    "reviewed_gpu1_block_id": proposal_2,
                    "reviewed_revision": "2",
                    "review_target_pointer": proposal_2,
                    "expected_packet_fingerprint": packet_fingerprint,
                    "reviewed_packet_fingerprint": packet_fingerprint,
                    "gpu1_closure_decision_packet_fingerprint": packet_fingerprint,
                    "gpu1_closure_decision_packet": gpu1_packet,
                    "gpu0_decision": "congruent",
                    "gpu0_effective_decision": "congruent",
                    "role_decision": "agree_close",
                }
            )
        else:
            provider_fields.update(
                {
                    "provider_backend": "openvino",
                    "provider_compute_device": "openvino/NPU",
                    "provider_device_verified": True,
                    "provider_model": "openvino_npu_micro",
                    "npu_peer_evidence_verified": True,
                    "npu_response_schema_valid": True,
                    "npu_device_workload_requested": True,
                    "npu_device_workload_performed": True,
                    "npu_micro_audit_performed": True,
                    "npu_micro_provider_model_loaded": True,
                    "npu_micro_provider_execution_performed": True,
                    "npu_native_tool_loop_error": "",
                    "npu_native_tool_loop_required": False,
                    "npu_peer_followup_required": False,
                }
            )
        provider_response_text = f"{role} performed=true reviewed {proposal_2}"
        write_json(
            provider_dir / f"{lane}.json",
            {
                "lane": lane,
                "role": role,
                "block_type": block_type,
                "provider_block_id": block_id,
                "proposal_block_id": proposal_2,
                "revision": 2,
                "refines_block_id": proposal_2,
                "resume_from_block_id": proposal_2,
                "pointer_action": action,
                "target_files": [target],
                "decision": "accept",
                "provider_execution_performed": True,
                "semantic_provider_execution_performed": True,
                "native_tool_loop_performed": True,
                "native_tool_call_count": 1,
                "selected_model": "qwen2.5-coder:14b" if lane == "gpu1_planner" else "",
                "workload": {"performed": True},
                **write_text_evidence_fields(
                    repo_root,
                    run_dir / "text_artifacts",
                    prefix="response_text",
                    name=f"{lane}_response_text",
                    text=provider_response_text,
                    kind="smoke_provider_response_text",
                    producer="heap_final_readable_product_smoke",
                    suffix=".md",
                ),
                **provider_fields,
            },
        )
    write_json(
        one_turn_gate_path,
        {
            "schema_version": 1,
            "kind": "gpu1_one_turn_runtime_gate",
            "revision": 2,
            "passed": True,
            "provider_execution_performed": True,
            "gpu1_turn0_provider_performed": True,
            "gpu1_turn0_native_tool_call_count": 1,
            "broker_request_count": 1,
            "broker_result_count": 1,
            "broker_result_passed_count": 1,
            "role_tool_reinjected": True,
            "gpu1_turn1_provider_performed": True,
            "tool_result_consumed_by_gpu1": True,
            "final_product_protocol_valid": True,
            "operator_delta_valid": True,
            "final_product_delta_valid": True,
            "gpu0_npu_started_before_gpu1_one_turn_closed": False,
            **one_turn_fields,
            "errors": [],
            "warnings": [],
        },
    )
    write_json(
        virtual_dev_path,
        {
            "kind": "heap_virtual_development_environment",
            "passed": True,
            "target_count": 2,
            "validation_count": 1,
            "targets": [
                {
                    "target_file": "ia_carmine/product/code_product/final_readable_product/cli.py",
                    "ast_ok": True,
                    "import_ok": True,
                    "help_ok": True,
                },
                {
                    "target_file": "ia_carmine/_shared/heap_final_readable_synthesis.py",
                    "ast_ok": True,
                    "import_ok": True,
                    "help_ok": True,
                },
            ],
            "guardrails": {
                "free_shell_exposed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "git_write_performed": False,
            },
        },
    )
    write_json(debug_lab_path, {"kind": "debug_lab", "passed": True})
    write_json(
        matrix_path,
        {
            "schema_version": 1,
            "kind": "heap_code_execution_tool",
            "passed": True,
            "repo_root": str(fixture_repo),
            "debug_lab_report": repo_rel(repo_root, debug_lab_path),
            "debug_lab_passed": True,
            "target_count": 2,
            "concrete_code_proposal_count": 2,
            "guardrails": {
                "free_shell_exposed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "git_write_performed": False,
            },
            "concrete_code_proposals": [
                {
                    "target_file": "ia_carmine/product/code_product/final_readable_product/cli.py",
                    "implementation_status": "validated_patch_candidate",
                    "source": "patch_candidate_synthesis",
                    "diff_source": "evidence_owned",
                    "git_status": "artifact patch candidate",
                    "code_or_patch_sketch": "diff --git a/ia_carmine/product/code_product/final_readable_product/cli.py b/ia_carmine/product/code_product/final_readable_product/cli.py\n@@\n+def build_report(...):\n+    pass\n..." + TRUNCATED_DIFF_MARKER,
                    "diff_path": str(diff_artifact),
                    "validation_commands": [
                        "python -m py_compile ia_carmine/product/code_product/final_readable_product/cli.py",
                        "python -m Tools.validation run_heap_final_readable_product_smoke",
                        "git diff --check",
                    ],
                },
                {
                    "target_file": "ia_carmine/runtime/heap_context_closure/cli.py",
                    "implementation_status": "developed_change_present",
                    "git_status": "M ia_carmine/runtime/heap_context_closure/cli.py",
                    "code_or_patch_sketch": "diff --git a/ia_carmine/runtime/heap_context_closure/cli.py b/ia_carmine/runtime/heap_context_closure/cli.py\n+    final_readable_product_command = [...]\n",
                    "validation_commands": ["python -m py_compile ia_carmine/runtime/heap_context_closure/cli.py"],
                },
                {
                    "target_file": "ia_carmine/_shared/heap_final_code_product.py",
                    "implementation_status": "verified_target_no_worktree_diff",
                    "git_status": "",
                    "diff_hunk_count": 0,
                    "code_or_patch_sketch": "",
                    "validation_commands": ["python -m py_compile ia_carmine/_shared/heap_final_code_product.py"],
                },
            ],
        },
    )
    write_json(
        run_dir / "heap_final_proposal_composer.json",
        {
            "schema_version": 1,
            "kind": "heap_final_proposal_composer",
            "documents_dir": str(documents_dir),
            "download_manifest_txt": str(manifest),
            "product_status": "blocked_with_reason",
            "quality_output_passed": False,
            "accepted_proposal_count": 1,
            "accepted_final_product_delta_count": 1,
            "final_product_delta_applied_count": 1,
            "rejected_proposal_count": 1,
            "proposal_count": 2,
            "provider_report_count": 3,
            "gpu1_one_turn_gate_passed_count": 1,
            "gpu1_one_turn_gate_failed_count": 0,
            "gpu1_one_turn_gate_blockers": [],
            "gpu1_one_turn_runtime_gate_paths": [repo_rel(repo_root, one_turn_gate_path)],
            **one_turn_fields,
            "gpu0_review_count": 1,
            "npu_audit_count": 1,
            "provider_execution_performed": True,
            "startup_manifest": {
                "input_ready_before_heap": True,
                "contract": {"input_ready_before_heap": True},
                "artifacts": {"context": repo_rel(repo_root, matrix_path)},
            },
            "provider_reports": [{"provider_execution_performed": True, **one_turn_fields}],
            "proposals": [{"block_id": proposal_1}, {"block_id": proposal_2, **one_turn_fields}],
            "gpu0_reviews": [{"block_id": "smoke:gpu0:002"}],
            "npu_audits": [{"block_id": "smoke:npu:002"}],
            "blocking_issues": ["smoke keeps provider product blocked while code matrix is concrete"],
            "operator_decision": {
                "decision": "BLOCKED_PROVIDER_REVIEW",
                "accepted_count": 0,
                "rejected_count": 1,
                "accepted_proposals": [],
                "rejected_proposals": [
                    {
                        "name": "provider_candidate",
                        "reasons": ["invented source path"],
                    }
                ],
            },
        },
    )
    write_json(
        run_dir / "heap_runtime_completeness_gate_report.json",
        {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate",
            "passed": True,
            "provider_execution_performed": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            **one_turn_fields,
            "metrics": {
                "product_status": "blocked_with_reason",
                "completed_requirements": ["preflight", "code_execution_matrix"],
                "missing_requirements": [],
                "code_execution_matrix_required": True,
                "code_execution_matrix_passed": True,
                "code_execution_matrix_reports": [repo_rel(repo_root, matrix_path)],
                "runtime_debug_lab_passed": True,
                "virtual_dev_environment_passed": True,
                "virtual_dev_environment_reports": [repo_rel(repo_root, virtual_dev_path)],
                "generic_write_lanes": ["gpu1_planner"],
                "generic_write_no_tool_capture_count": 1,
                "generic_write_capture_failed_count": 1,
                "lane_tiers": {
                    "gpu1_planner": "primary",
                    "gpu0_peer": "coworker_medium",
                    "npu_micro_task_auditor": "micro_fast",
                },
                "lane_authority": {
                    "gpu1_planner": "leader",
                    "gpu0_peer": "coworker",
                    "npu_micro_task_auditor": "micro_tool",
                },
                "lane_context_budgets": {
                    "gpu1_planner": {"ollama_num_ctx": 8192, "max_new_tokens": 900},
                    "gpu0_peer": {"ollama_num_ctx": 4096, "max_new_tokens": 512},
                    "npu_micro_task_auditor": {
                        "max_prompt_chars": 1200,
                        "max_context_chars": 8000,
                        "max_new_tokens": 384,
                    },
                },
                "gpu1_context_budget": {"ollama_num_ctx": 8192, "max_new_tokens": 900},
                "gpu0_context_budget": {"ollama_num_ctx": 4096, "max_new_tokens": 512},
                "npu_context_budget": {
                    "max_prompt_chars": 1200,
                    "max_context_chars": 8000,
                    "max_new_tokens": 384,
                },
                "context_hierarchy_valid": True,
                "gpu1_replight_valid": True,
                "gpu1_boot_leader_ready": True,
                "gpu1_primary_workload_valid": True,
                "gpu1_primary_evidence_valid": True,
                "gpu1_primary_evidence_source": "native_tool_result",
                "leader_source": "native_tool_result",
                "gpu1_native_tool_call_count": 1,
                **one_turn_fields,
                "sidecars_start_policy": "after_gpu1_residency_handshake",
                "parallel_provider_overlap_seconds": 12.5,
                "device_identity_map": [
                    {
                        "logical_lane": "gpu0_peer",
                        "provider_backend_device_id": "vulkan:1",
                        "windows_task_manager_device_hint": "Windows GPU 0 / Intel(R) Graphics",
                        "vulkan_visible_device": "1",
                        "vulkan_device_name": "Intel(R) Graphics",
                        "vulkan_vendor_id": "0x8086",
                        "device_identity_verified": True,
                    }
                ],
                "gpu1_primary_workload_chars": 1400,
                "gpu1_primary_workload_tokens": 180,
                "gpu1_leader_valid": True,
                "gpu1_leader_block_id": "smoke:gpu1:002",
                "soft_lock_closure_owner_decision": "finalize_product",
                "gpu0_closure_agreement": "agree_close",
                "npu_closure_advisory": "evidence_ready_non_closer",
                "cpu_closure_validation": "ready_to_close",
                "closure_quorum_status": "ready_to_close",
                "closure_quorum_reason": "candidate subgraph has current GPU0 review and consumed peers",
                "gpu1_closure_decision_packet": gpu1_packet,
                "gpu1_closure_decision_packet_valid": True,
                "latest_gpu1_decision": "finalize_product",
                "latest_gpu1_block_id": proposal_2,
                "latest_gpu1_revision": "2",
                "latest_gpu1_block_requires_gpu0_review": True,
                "latest_gpu1_block_reviewed_by_gpu0": True,
                "gpu0_review_invalid_requires_gpu1_retry": False,
                "gpu0_secondary_schema_valid": True,
                "latest_gpu0_effective_decision": "congruent",
                "latest_gpu0_role_decision": "agree_close",
                "latest_gpu0_checked_current_packet": True,
                "latest_gpu0_packet_stale_after_gpu1_packet_rewrite": False,
                "latest_gpu0_reviewed_packet_fingerprint": packet_fingerprint,
                "latest_gpu1_packet_fingerprint": packet_fingerprint,
                "latest_gpu0_expected_gpu1_block_id": proposal_2,
                "latest_gpu0_expected_gpu1_revision": "2",
                "consumed_peer_block_ids": ["smoke:gpu0:002", "smoke:npu:002"],
                "gpu1_consumed_gpu0_peer": True,
                "gpu1_consumed_npu_peer": True,
                "gpu0_peer_followup_pending_count": 1,
                "npu_peer_followup_pending_count": 1,
                "generic_write_refined_product": {
                    "eligible": False,
                    "capture_count": 1,
                    "generic_write_no_tool_capture_count": 1,
                    "generic_write_capture_failed_count": 0,
                    "generic_write_capture_failures": [],
                    "generic_write_lanes": ["gpu1_planner"],
                    "gpu0_peer_followup_pending_count": 0,
                    "npu_peer_followup_pending_count": 0,
                    "latest_consumed_by_gpu1": False,
                    "captures": [
                        {
                            "lane": "gpu1_planner",
                            "revision": 2,
                            "provider_response_excerpt": "GPU1 refined product evidence after sidecar congruence check",
                        }
                    ],
                },
            },
            "real_run_output_contract": {
                "product_status": "blocked_with_reason",
                "missing_requirements": [],
            },
        },
    )
    write_json(run_dir / "heap_context_preflight_gate.json", {"passed": True})
    write_json(run_dir / "external_heap_postrun_package.json", {"passed": True, "product_acceptance_passed": True})
    write_json(run_dir / "external_heap_revision_context.json", {"terminal_no_patchable_target": True})
    composer_json = run_dir / "heap_final_proposal_composer.json"
    causality_json = run_dir / "heap_final_causality_normalized.json"
    pointer_json = run_dir / "external_heap_block_pointer_manifest.json"
    for command in (
        [sys.executable, "-m", "ia_carmine.cli", "build_external_heap_block_pointer_manifest", "--repo-root", ".", "--run-dir", str(run_dir)],
        [sys.executable, "-m", "ia_carmine.cli", "normalize_heap_final_causality", "--composer-json", str(composer_json), "--pointer-manifest", str(pointer_json), "--output", str(causality_json)],
        [sys.executable, "-m", "ia_carmine.cli", "build_external_heap_revision_context", "--pointer-manifest", str(pointer_json), "--composer-json", str(composer_json), "--causality-json", str(causality_json), "--output", str(run_dir / "external_heap_revision_context.json"), "--no-documents-copy"],
    ):
        subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    return run_dir, documents_dir
