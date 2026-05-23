from __future__ import annotations

from pathlib import Path
from typing import Any


def check_gpu1_workload_absorption(repo_root: Path) -> dict[str, Any]:
    local_probe = _read(repo_root, "ia_carmine/providers/provider_mesh/local_provider_probe/cli.py")
    commands = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_commands.py")
    provider_context = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_context.py")
    provider_prompt_text = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_prompt_text.py")
    errors: list[str] = []
    if "mirror_single_provider_lane" not in local_probe or "args.run_ollama" not in local_probe:
        errors.append("GPU1 provider wrapper still mirrors only replight lanes")
    for marker in ("response_text", "target_files", "validation_commands", "provider_work_verified"):
        if marker not in local_probe:
            errors.append(f"local provider probe does not mirror {marker}")
    if "lane_report_lane in {\"ollama\", lane}" not in commands:
        errors.append("runtime summarizer does not absorb lane-specific Ollama reports")
    if "_empty_report_value" not in commands:
        errors.append("runtime summarizer cannot overwrite empty top-level wrapper fields")
    if "--defer-unload" not in _read(repo_root, "ia_carmine/runtime/heap_gate/provider_command_specs.py"):
        errors.append("GPU1 provider loop does not defer model unload until cleanup")
    if "runtime_file_refs/SOURCE_PATH_ALLOWLIST_CONTRACT" not in provider_context:
        errors.append("GPU1 prompt does not anchor target files to runtime_file_refs allowlist")
    if "basename o path ricordati ma non allowlisted" not in provider_prompt_text:
        errors.append("GPU1 pointer protocol does not forbid remembered basename targets")
    return {"name": "gpu1_workload_absorption", "errors": errors}


def check_rejected_gpu1_retry_contract(repo_root: Path) -> dict[str, Any]:
    refinement = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_refinement.py")
    run_loop = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop.py")
    terminal = _read(repo_root, "ia_carmine/runtime/heap_gate/terminal_invariants.py")
    errors: list[str] = []
    for marker in (
        "latest_rejected_proposal_requires_retry",
        "REJECTED_GPU1_BLOCK_RETRY_REQUIRED",
        "validator_action=generate_new_gpu1_revision_for_same_block",
        "run_provider_teamwork(round_id, revision=self.provider_revision_count)",
    ):
        if marker not in refinement:
            errors.append(f"GPU1 retry contract missing {marker}")
    if "and self.provider_revision_evidence_ready(events)" not in run_loop:
        errors.append("run loop does not require matrix/lab evidence before GPU1 retry")
    if "or self.latest_rejected_proposal_requires_retry()" in run_loop:
        errors.append("run loop bypasses required matrix/lab evidence for rejected GPU1 retry")
    if "mandatory provider revision retry" not in terminal:
        errors.append("terminal invariants do not block rejected proposal without retry")
    errors.extend(_probe_rejected_gpu1_retry_helper())
    return {"name": "rejected_gpu1_retry_contract", "errors": errors}


def check_external_heap_health_report_filter(repo_root: Path) -> dict[str, Any]:
    graph = _read(repo_root, "ia_carmine/runtime/external_heap/block_pointer_manifest/provider_graph.py")
    errors: list[str] = []
    if "provider_role_coexistence" not in graph:
        errors.append("external heap provider graph may still count boot coexistence as provider work")
    if "provider_replight" not in graph or "replight_mode" not in graph:
        errors.append("external heap provider graph may still count replight health reports as provider work")
    return {"name": "external_heap_health_report_filter", "errors": errors}


def check_bounded_npu_micro_tasks(repo_root: Path) -> dict[str, Any]:
    npu = (
        _read(repo_root, "ia_carmine/_shared/npu_micro_task_companion_cli.py")
        + "\n"
        + _read(repo_root, "ia_carmine/_shared/npu_micro_task_contract.py")
    )
    errors: list[str] = []
    for marker in (
        "section_presence_audit",
        "target_reference_audit",
        "validation_command_audit",
        "risk_guardrail_audit",
        "NPU_DONE",
        "NPU_REJECT",
        "NPU_NO_ACTION",
        "NPU_TIMEOUT_BOUNDARY",
        "MICRO_TASK=",
        "CHECKED=",
        "FINDINGS=",
        "DECISION=",
        "REASON=",
    ):
        if marker not in npu:
            errors.append(f"NPU micro-task contract missing {marker}")
    return {"name": "bounded_npu_micro_tasks", "errors": errors}


def check_final_cleanup(repo_root: Path) -> dict[str, Any]:
    launcher = _read(repo_root, "ia_carmine/runtime/heap_context_closure/launcher.py")
    common = _read(repo_root, "ia_carmine/runtime/heap_context_closure/common.py")
    errors: list[str] = []
    if "heap command completed provider cleanup" not in launcher:
        errors.append("launcher does not run provider cleanup after successful heap command")
    if "provider_base_url" not in common or "_stop_gpu0_vulkan_server" not in common:
        errors.append("provider cleanup does not know GPU0 base URL/server stop")
    return {"name": "final_cleanup", "errors": errors}


def _probe_rejected_gpu1_retry_helper() -> list[str]:
    from ia_carmine.runtime.heap_gate.provider_refinement import RuntimeGateProviderRefinementMixin

    class FakeGate(RuntimeGateProviderRefinementMixin):
        provider_universe_blocked_reason = ""

        def __init__(self, report: dict[str, Any], blocked: str = "") -> None:
            self.report = report
            self.provider_universe_blocked_reason = blocked

        def latest_proposal_iteration_report(self) -> dict[str, Any]:
            return self.report

    rejected = {"quality_passed": False, "exit_decision": "PATCHABLE_TARGET"}
    terminal = {
        "quality_passed": False,
        "exit_decision": "NO_PATCHABLE_TARGET",
        "response_text": "BLOCKED_NO_VERIFIED_TARGET_REASON: no target",
    }
    errors: list[str] = []
    if not FakeGate(rejected).latest_rejected_proposal_requires_retry():
        errors.append("fake rejected GPU1 proposal did not require retry")
    if FakeGate(terminal).latest_rejected_proposal_requires_retry():
        errors.append("valid NO_PATCHABLE_TARGET proposal still required retry")
    if FakeGate(rejected, blocked="gpu0_ollama_vulkan_required").latest_rejected_proposal_requires_retry():
        errors.append("provider failure did not suppress retry requirement")
    return errors


def _read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8", errors="replace")
