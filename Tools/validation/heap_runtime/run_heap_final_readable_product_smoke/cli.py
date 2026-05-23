#!/usr/bin/env python3
"""Smoke test the heap final readable product assembler."""
from __future__ import annotations
import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.runtime.heap_context_closure.product_state import build_product_state

TRUNCATED_DIFF_MARKER = "[diff " + "truncated]"
def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")
def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)
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
            "response_text": "TARGET_FILES:\n- "
            + target
            + "\nPROBLEM:\n- smoke rejected first revision\nPATCH_SKETCH_UNIFIED_DIFF:\n"
            + full_diff,
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
            "broker_result_refs": [repo_rel(repo_root, matrix_path)],
            "matrix_report_refs": [repo_rel(repo_root, matrix_path)],
            "quality_passed": True,
            "accepted": True,
            "response_text": "TARGET_FILES:\n- " + target + "\nPATCH_SKETCH_UNIFIED_DIFF:\n" + full_diff,
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
                    "npu_micro_provider_model_loaded": False,
                    "npu_micro_provider_execution_performed": False,
                    "npu_native_tool_loop_error": "openvino_native_tool_loop_timeout",
                    "npu_native_tool_loop_required": False,
                    "npu_peer_followup_required": True,
                }
            )
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
                "response_text": f"{role} performed=true reviewed {proposal_2}",
                **provider_fields,
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
            "rejected_proposal_count": 1,
            "proposal_count": 2,
            "provider_report_count": 3,
            "gpu0_review_count": 1,
            "npu_audit_count": 1,
            "provider_execution_performed": True,
            "startup_manifest": {
                "input_ready_before_heap": True,
                "contract": {"input_ready_before_heap": True},
                "artifacts": {"context": repo_rel(repo_root, matrix_path)},
            },
            "provider_reports": [{"provider_execution_performed": True}],
            "proposals": [{"block_id": proposal_1}, {"block_id": proposal_2}],
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
                "generic_write_lanes": ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
                "generic_write_no_tool_capture_count": 3,
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
                "gpu1_primary_evidence_source": "generic_write",
                "leader_source": "generic_write",
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
                "consumed_peer_block_ids": ["smoke:gpu0:002", "smoke:npu:002"],
                "gpu1_consumed_gpu0_peer": True,
                "gpu1_consumed_npu_peer": True,
                "gpu0_peer_followup_pending_count": 1,
                "npu_peer_followup_pending_count": 1,
                "generic_write_refined_product": {
                    "eligible": False,
                    "capture_count": 3,
                    "generic_write_no_tool_capture_count": 3,
                    "generic_write_capture_failed_count": 1,
                    "generic_write_capture_failures": [
                        {
                            "lane": "npu_micro_task_auditor",
                            "revision": 1,
                            "errors": ["generic_write: unsupported args smoke fixture"],
                        }
                    ],
                    "generic_write_lanes": ["gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"],
                    "gpu0_peer_followup_pending_count": 1,
                    "npu_peer_followup_pending_count": 1,
                    "latest_consumed_by_gpu1": False,
                    "captures": [
                        {
                            "lane": "npu_micro_task_auditor",
                            "revision": 2,
                            "provider_response_excerpt": "MICRO_TASK=target_reference_audit DECISION=NPU_TIMEOUT_BOUNDARY",
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
    write_json(run_dir / "external_heap_postrun_package.json", {"passed": True, "product_acceptance_passed": False})
    write_json(run_dir / "external_heap_revision_context.json", {"terminal_no_patchable_target": True})
    composer_json = run_dir / "heap_final_proposal_composer.json"
    causality_json = run_dir / "heap_final_causality_normalized.json"
    pointer_json = run_dir / "external_heap_block_pointer_manifest.json"
    for command in (
        [sys.executable, "-m", "ia_carmine.cli", "normalize_heap_final_causality", "--composer-json", str(composer_json), "--output", str(causality_json)],
        [sys.executable, "-m", "ia_carmine.cli", "build_external_heap_block_pointer_manifest", "--repo-root", ".", "--run-dir", str(run_dir)],
        [sys.executable, "-m", "ia_carmine.cli", "build_external_heap_revision_context", "--pointer-manifest", str(pointer_json), "--composer-json", str(composer_json), "--causality-json", str(causality_json), "--output", str(run_dir / "external_heap_revision_context.json"), "--no-documents-copy"],
    ):
        subprocess.run(command, cwd=repo_root, text=True, capture_output=True, check=False)
    return run_dir, documents_dir
def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    work_dir = Path(args.work_dir).resolve() if args.work_dir else repo_root / "output" / "validation" / f"heap_final_readable_product_smoke_{now_stamp()}"
    run_dir, documents_dir = build_fixture(repo_root, work_dir)
    output = run_dir / "heap_final_readable_product.json"
    markdown = run_dir / "heap_final_readable_product.md"
    text = run_dir / "heap_final_readable_product.txt"
    command = [
        sys.executable,
        "ia_carmine/product/code_product/final_readable_product/cli.py",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
        "--text-output",
        str(text),
        "--documents-dir",
        str(documents_dir),
        "--zip-documents",
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=max(30, int(args.timeout_seconds)),
    )
    product = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    final_md = documents_dir / "FINAL_READABLE_PRODUCT.md"
    full_code_product = documents_dir / "CODE_PRODUCT_FULL_PATCH.md"
    zip_path = Path(str(documents_dir) + ".zip")
    body = final_md.read_text(encoding="utf-8-sig") if final_md.exists() else ""
    code_product_body = full_code_product.read_text(encoding="utf-8-sig") if full_code_product.exists() else ""
    required_phrases = ["Decisione finale", "Final document status", "Piano applicabile", "Sequenza di applicazione", "Laboratorio operativo", "Sa usarlo", "Code product", "Universo pointer e memoria", "Perche il provider non si applica", "Decisione operatore", "Peer follow-up pending", "MICRO_TASK=target_reference_audit", "Capture failed", "Gerarchia GPU1/GPU0/NPU", "GPU1 primary workload", "GPU1 primary evidence", "Generic write", "GPU1/NVIDIA", "GPU0/Vulkan", "coworker_medium", "NPU/OpenVINO", "micro_fast", "context_budget", "Parallel provider overlap", "Device identity map"]
    missing = [phrase for phrase in required_phrases if phrase not in body]
    pointer_reconstruction = (
        product.get("pointer_reconstruction")
        if isinstance(product.get("pointer_reconstruction"), dict)
        else {}
    )
    pointer_contract = (
        pointer_reconstruction.get("contract")
        if isinstance(pointer_reconstruction.get("contract"), dict)
        else {}
    )
    launcher_product_state = build_product_state(
        code_product_contract={"path": str(full_code_product), "real_code_product_ready": False},
        external_contract={
            "provider_execution_performed": True,
            "resume_from_block_id": "smoke:proposal:000",
            "latest_block_id": "smoke:gpu0_peer:000",
            "provider_rejection_reasons": [],
            "missing_roles": [],
            "pointer_block_count": 3,
        },
        final_result={"passed": False},
        final_payload={
            "product_kind": "blocked_continuation_product",
            "product_blocked_reason": "gpu0_peer_followup_pending",
            "soft_close_reason": "gpu0_peer_followup_pending",
        },
        launcher_contract_errors=["final readable product did not pass"],
    )
    launcher_reason_preserved = (
        launcher_product_state.get("product_blocked_reason") == "gpu0_peer_followup_pending"
        and launcher_product_state.get("soft_close_reason") == "gpu0_peer_followup_pending"
    )
    passed = (
        completed.returncode == 0
        and product.get("passed") is True
        and product.get("pointer_reconstruction_passed") is True
        and pointer_contract.get("final_code_product_composed_from_pointer_graph") is True
        and pointer_contract.get("single_run_not_single_direction") is True
        and final_md.exists()
        and full_code_product.exists()
        and "CODE_PRODUCT_FULL_PATCH" in code_product_body
        and "ia_carmine/product/code_product/final_readable_product/cli.py" in code_product_body
        and "FULL_DIFF_SENTINEL" in code_product_body
        and TRUNCATED_DIFF_MARKER not in code_product_body
        and "[code product excerpt truncated" not in body
        and "ia_carmine/runtime/heap_context_closure/cli.py" not in code_product_body
        and "ia_carmine/_shared/heap_final_code_product.py" not in code_product_body
        and "ia_carmine/worktree_extra.py" not in code_product_body
        and "Final assembler worktree fallback: `disabled`" in code_product_body
        and "Code product status: `BLOCKED_WITH_CODE_PRODUCT_REVIEW`" in code_product_body
        and "[no worktree diff captured]" not in code_product_body
        and zip_path.exists()
        and not missing
        and launcher_reason_preserved
    )
    report = {
        "schema_version": 1,
        "kind": "heap_final_readable_product_smoke",
        "passed": passed,
        "work_dir": str(work_dir),
        "run_dir": str(run_dir),
        "documents_dir": str(documents_dir),
        "product_json": str(output),
        "documents_markdown": str(final_md),
        "full_code_product": str(full_code_product),
        "documents_zip": str(zip_path),
        "missing_required_phrases": missing,
        "pointer_reconstruction_passed": product.get("pointer_reconstruction_passed"),
        "pointer_reconstruction": pointer_reconstruction,
        "launcher_reason_preserved": launcher_reason_preserved,
        "launcher_product_state": launcher_product_state,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "command": command,
    }
    report_output = Path(args.output).resolve() if args.output else work_dir / "smoke.json"
    write_json(report_output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=90)
    return parser.parse_args()
def main() -> int:
    report = run_smoke(parse_args())
    return 0 if report.get("passed") else 2
if __name__ == "__main__":
    raise SystemExit(main())
