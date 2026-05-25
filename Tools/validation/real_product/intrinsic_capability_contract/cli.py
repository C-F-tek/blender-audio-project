#!/usr/bin/env python3
"""Validate the canonical run intrinsic heap/universe capability contract."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def has(text: str, token: str) -> bool:
    return token in text


def exists(repo_root: Path, rel: str) -> bool:
    return (repo_root / rel).exists()


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = ["# Real Product Intrinsic Capability Contract", "", f"- Passed: `{report.get('passed')}`", ""]
    for item in report.get("contract_order") or []:
        lines.append(f"- `{item}`: `{report.get(item)}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    dispatch = read_text(repo_root / "ia_carmine/dispatch.py")
    run_cli = read_text(repo_root / "ia_carmine/runtime/run/cli.py")
    profiles = read_text(repo_root / "ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json")
    profile_builder = read_text(repo_root / "ia_carmine/product/operator_product_core/profiles.py")
    runner = read_text(repo_root / "ia_carmine/product/operator_product_core/runner.py")
    heap_closure = read_text(repo_root / "ia_carmine/runtime/heap_context_closure/launcher.py")
    matrix_lab = read_text(repo_root / "ia_carmine/runtime/heap_gate/matrix_lab.py")
    matrix_evidence = read_text(repo_root / "ia_carmine/runtime/heap_gate/matrix_lab_evidence.py")
    matrix_tool = read_text(repo_root / "ia_carmine/runtime/heap_runtime/code_execution_tool/cli.py")
    synthesis = read_text(repo_root / "ia_carmine/product/patch_product/candidate_synthesis/cli.py")
    synthesis_evidence = read_text(
        repo_root / "ia_carmine/product/patch_product/candidate_synthesis/evidence_diff.py"
    )
    final_product = read_text(repo_root / "ia_carmine/_shared/heap_final_code_product.py")
    final_readable_product = read_text(repo_root / "ia_carmine/product/code_product/final_readable_product/cli.py")
    artifact_intake = read_text(repo_root / "ia_carmine/product/code_product/artifact_intake/cli.py")
    prepare = read_text(repo_root / "ia_carmine/product/agent_review/review_pr_cli.py")
    provider_loop = read_text(repo_root / "ia_carmine/_shared/provider_tool_loop.py")
    npu_report = read_text(repo_root / "ia_carmine/providers/provider_mesh/npu_micro_task_companion_report/cli.py")
    gpu0_report = read_text(repo_root / "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py")

    checks: dict[str, bool] = {
        "task_md_input": has(run_cli, "--request-file")
        and has(run_cli, "Task markdown not found")
        and has(profile_builder, "--request-file"),
        "heap_exchange_activation": has(profile_builder, "heap_context_closure")
        and has(heap_closure, "heap_runtime_context_closure_launcher")
        and has(profiles, "external_heap_block_pointer_v1"),
        "gpu1_primary_advisory": has(profiles, "gpu1_planner")
        and has(provider_loop, "build_heap_patch_proposal_prompt"),
        "gpu0_ollama_vulkan_workload": has(profiles, "gpu0_reviewer_refiner")
        and has(gpu0_report.lower(), "ollama_gpu0_vulkan_required")
        and has(gpu0_report, "run_ollama_probe"),
        "npu_peer_micro_lane": has(profiles, "npu_auditor")
        and has(npu_report.lower(), "npu")
        and has(provider_loop, "IA_CARMINE_NPU_MODEL_DIR"),
        "shared_memory_evidence": exists(repo_root, "ia_carmine/memory/agent_memory/sqlite_cli.py")
        and exists(repo_root, "ia_carmine/context/agent_context/shared_toolbox_bundle/cli.py"),
        "static_deterministic_script_lane": exists(
            repo_root, "ia_carmine/product/patch_product/candidate_synthesis/cli.py"
        )
        and has(matrix_lab, "synthesize_patch_candidates")
        and has(matrix_evidence, "patch_candidate_synthesis_passed_count"),
        "provider_evidence_to_matrix_code_product": has(matrix_lab, "evidence_report")
        and has(matrix_tool, "--evidence-report")
        and has(synthesis, "build_evidence_candidates")
        and has(synthesis_evidence, "diff --git")
        and has(synthesis_evidence, "git apply"),
        "heap_exchange_close": has(runner, "operator_product_launcher_run.json")
        and has(runner, "operator_product_lab_summary.json")
        and has(final_product, "render_code_product_section"),
        "product_readiness": has(runner, "launcher_passed")
        and has(runner, "code_product_metrics")
        and has(final_readable_product, "final_product_surface_ready")
        and has(final_readable_product, "text_product_ready")
        and has(final_readable_product, "final_product_delta_applied_count")
        and has(final_readable_product, "final_product_blockers")
        and has(final_readable_product, "truncation_marker")
        and has(artifact_intake, "--apply-safe"),
        "agent_review_prepare_pr": '"agent_review_prepare_pr"' in dispatch
        and has(prepare, "create")
        and has(prepare, "draft"),
        "final_pr_product": has(runner, "code_product_metrics")
        and has(runner, "review_report")
        and has(runner, "review_required"),
    }
    order = [
        "task_md_input",
        "heap_exchange_activation",
        "gpu1_primary_advisory",
        "gpu0_ollama_vulkan_workload",
        "npu_peer_micro_lane",
        "shared_memory_evidence",
        "static_deterministic_script_lane",
        "provider_evidence_to_matrix_code_product",
        "heap_exchange_close",
        "product_readiness",
        "agent_review_prepare_pr",
        "final_pr_product",
    ]
    errors = [f"missing intrinsic capability: {name}" for name in order if not checks.get(name)]
    return {
        "schema_version": 1,
        "kind": "real_product_intrinsic_capability_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "contract_order": order,
        **checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/real_product_intrinsic_capability_contract.json")
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
