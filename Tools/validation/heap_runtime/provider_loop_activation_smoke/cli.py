from __future__ import annotations

import argparse
import io
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any

from Tools.validation.heap_runtime.provider_loop_hierarchy_checks import (
    run_provider_loop_hierarchy_checks,
)
from Tools.validation.heap_runtime.provider_loop_primary_evidence_checks import run_provider_loop_primary_evidence_checks
from Tools.validation.heap_runtime.provider_loop_tail_checks import (
    check_bounded_npu_micro_tasks,
    check_external_heap_health_report_filter,
    check_final_cleanup,
    check_gpu1_workload_absorption,
    check_rejected_gpu1_retry_contract,
)
def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    checks = [
        _check_heap_loop_bootstrap_import_contract(repo_root),
        _check_independent_sidecar_watchdogs(repo_root),
        _check_boot_handoff(repo_root),
        _check_gpu0_command_contract(repo_root),
        _check_ollama_native_tool_lane_contract(repo_root),
        _check_vulkan_identity_contract(repo_root),
        _check_provider_residency_lifecycle(repo_root),
        run_provider_loop_hierarchy_checks(repo_root),
        run_provider_loop_primary_evidence_checks(repo_root),
        check_gpu1_workload_absorption(repo_root),
        check_rejected_gpu1_retry_contract(repo_root),
        check_external_heap_health_report_filter(repo_root),
        check_bounded_npu_micro_tasks(repo_root),
        check_final_cleanup(repo_root),
    ]
    errors = [error for check in checks for error in check.get("errors", [])]
    report = {
        "schema_version": 1,
        "kind": "provider_loop_activation_smoke",
        "repo_root": str(repo_root),
        "passed": not errors,
        "checks": checks,
        "errors": errors,
    }
    if args.output:
        output = _resolve(repo_root, args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2
def _check_heap_loop_bootstrap_import_contract(repo_root: Path) -> dict[str, Any]:
    loop_steps = _read(repo_root, "ia_carmine/runtime/heap_gate/loop_steps.py")
    errors: list[str] = []
    if "safe_dict(" in loop_steps and "safe_dict," not in loop_steps:
        errors.append("loop_steps.py uses safe_dict but does not import it from runtime_common")
    return {"name": "heap_loop_bootstrap_import_contract", "errors": errors}
def _check_independent_sidecar_watchdogs(repo_root: Path) -> dict[str, Any]:
    from ia_carmine.runtime.heap_gate.provider_time import build_provider_lane_time_contracts

    process_collection = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_process_collection.py")
    provider_execution = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_execution.py")
    run_loop = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop.py")
    args = SimpleNamespace(budget_minutes=5, timeout_seconds=600, npu_micro_timeout_seconds=60)
    contracts = build_provider_lane_time_contracts(args)
    errors: list[str] = []
    if "sidecar join timeout after primary closure owner completed" in process_collection:
        errors.append("provider process collection still kills sidecars after primary completion")
    if "sidecar_expired" in process_collection or "_primary_completed_perf" in process_collection:
        errors.append("provider process collection still computes primary-completion sidecar expiry")
    if contracts["gpu0_peer"].get("sidecar_join_after_primary_seconds") != 0:
        errors.append("GPU0 sidecar join after primary is not disabled")
    if contracts["npu_micro_task_auditor"].get("sidecar_join_after_primary_seconds") != 0:
        errors.append("NPU sidecar join after primary is not disabled")
    if "collect_provider_processes(\n                self,\n                prepared," in provider_execution:
        errors.append("provider loop still blocks GPU1 on full prepared sidecar join")
    if "poll_pending_provider_sidecars(round_id)" not in run_loop:
        errors.append("run loop does not poll async sidecars without blocking GPU1")
    if "pending_provider_sidecar_collections.append" not in provider_execution:
        errors.append("provider loop does not retain async sidecar process handles")
    return {"name": "independent_sidecar_watchdogs", "errors": errors}
def _check_boot_handoff(repo_root: Path) -> dict[str, Any]:
    coexistence = _read(repo_root, "ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py")
    preflight = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_coexistence_preflight.py")
    errors: list[str] = []
    for marker in ("--handoff-provider-loop", "deferred_until_provider_cleanup"):
        if marker not in coexistence:
            errors.append(f"provider role coexistence missing {marker}")
    if "--handoff-provider-loop" not in preflight:
        errors.append("runtime boot preflight does not request provider-loop handoff")
    return {"name": "boot_handoff", "errors": errors}


def _check_gpu0_command_contract(repo_root: Path) -> dict[str, Any]:
    gpu0 = _read(repo_root, "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py")
    specs = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_command_specs.py")
    metrics = _read(repo_root, "ia_carmine/runtime/heap_gate/run_loop_metrics.py")
    errors: list[str] = []
    if "--startup-manifest" not in gpu0:
        errors.append("GPU0 CLI does not accept --startup-manifest")
    if "--server-evidence" not in gpu0:
        errors.append("GPU0 CLI does not accept boot handoff server evidence")
    if "startup_manifest_context" not in gpu0:
        errors.append("GPU0 CLI does not ingest startup manifest context")
    if "--server-evidence" not in specs:
        errors.append("runtime GPU0 command does not pass boot handoff evidence")
    if "_gpu0_server_evidence_path" not in specs:
        errors.append("runtime GPU0 command does not inherit prior GPU0 server evidence")
    if "_gpu0_max_new_tokens" not in specs:
        errors.append("runtime GPU0 command does not bound peer max_new_tokens separately")
    if "--restart-gpu0-vulkan-server" in specs:
        errors.append("runtime GPU0 command still forces Vulkan server restart")
    if '"provider_model": gpu0_model' not in specs:
        errors.append("GPU0 spec does not expose provider_model for cleanup")
    if "--defer-unload" not in specs:
        errors.append("runtime GPU0 command does not defer model unload until cleanup")
    if "gpu0-sidecar-timeout-seconds" in specs or "gpu0_sidecar_timeout_seconds" in specs:
        errors.append("runtime added forbidden GPU0 sidecar timeout truncation flag")
    if "packet_review_only" not in specs or "sidecar_scope_mode" not in specs:
        errors.append("runtime sidecar command specs do not expose packet_review_only scope")
    for marker in (
        "gpu1_idle_after_primary_seconds",
        "sidecar_alone_after_gpu1_seconds",
        "gpu1_congruence_check_performed",
    ):
        if marker not in metrics:
            errors.append(f"provider lane metrics missing {marker}")
    if "args.defer_unload" not in gpu0:
        errors.append("GPU0 CLI does not support provider-cycle unload deferral")
    if "final synthesis" not in gpu0 or "complete alternate plan" not in gpu0:
        errors.append("GPU0 prompt does not forbid final synthesis / alternate full planning")
    if 'report.get("ollama_unload_verified")' in _extract_function(gpu0, "_gpu0_workload_verified"):
        errors.append("GPU0 workload verification still requires unload as proof")
    return {"name": "gpu0_command_contract", "errors": errors}


def _check_ollama_native_tool_lane_contract(repo_root: Path) -> dict[str, Any]:
    native = _read(repo_root, "ia_carmine/runtime/heap_gate/tool_broker_native_calls.py")
    followup = _read(repo_root, "ia_carmine/runtime/heap_gate/generic_write_followup.py")
    provider_context = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_context.py")
    gpu0 = _read(repo_root, "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py")
    loop = _read(repo_root, "ia_carmine/_shared/provider_tool_loop.py")
    terminal = _read(repo_root, "ia_carmine/runtime/heap_gate/terminal_invariants.py")
    team_packet = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_teamwork_packet.py")
    errors: list[str] = []
    if 'PRIMARY_NATIVE_TOOL_CALL_LANES = {"gpu1_planner"}' not in native:
        errors.append("GPU1 primary native tool lane set is missing")
    if 'PEER_NATIVE_TOOL_CALL_LANES = {"gpu0_peer"}' not in native:
        errors.append("GPU0 peer native tool lane set is missing")
    if "OPERATIVE_NATIVE_TOOL_CALL_LANES = PRIMARY_NATIVE_TOOL_CALL_LANES | PEER_NATIVE_TOOL_CALL_LANES" not in native:
        errors.append("operative native tool lane set does not separate primary and peer lanes")
    if 'DIAGNOSTIC_NATIVE_TOOL_CALL_LANES = {"npu_micro_task_auditor"}' not in native:
        errors.append("NPU diagnostic native tool lane set is missing")
    if 'lane not in OPERATIVE_NATIVE_TOOL_CALL_LANES' not in native:
        errors.append("native tool router does not gate operative broker requests by lane set")
    if "no_tool_capture" not in native or "NO_TOOL_GENERIC_WRITE_CAPTURE_LANES" not in native:
        errors.append("native tool router does not capture useful no-tool Ollama responses")
    if "gpu1_followup_required" not in native or "tool_result_scope" not in native:
        errors.append("native tool router does not stamp lane authority on broker requests")
    if "generic_write_refinement" not in native:
        errors.append("generic_write native call is not mapped to refinement evidence")
    registry = _read(repo_root, "ia_carmine/runtime/runtime_tool/broker/registry.py")
    for arg in ("source_revision", "gpu1_followup_required", "peer_followup_required", "provider_role"):
        if arg not in registry:
            errors.append(f"generic_write broker registry does not allow {arg}")
    if "generic_write" not in loop or "run_heap_virtual_dev_environment" not in loop:
        errors.append("Ollama native tool list does not expose generic_write/dev/matrix tools")
    for source, name in ((provider_context, "GPU1 prompt"), (gpu0, "GPU0 prompt")):
        if "BROKER_NATIVE_TOOL_RULE" not in source or "generic_write" not in source:
            errors.append(f"{name} lacks generic_write native broker instruction")
    if "GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS = 3" not in followup:
        errors.append("generic_write follow-up does not require three refinements")
    if "generic_write_next_turn_required" not in followup:
        errors.append("generic_write follow-up does not force next GPU1 turn")
    if "gpu0_peer_followup_pending_count" not in followup:
        errors.append("GPU0 peer evidence does not force later GPU1 consumption")
    if "npu_peer_followup_pending_count" not in followup:
        errors.append("NPU peer evidence does not force later GPU1 consumption")
    if "code_product_allowed_after_three_refinements" not in followup:
        errors.append("generic_write cannot become refined product after three iterations")
    if (
        "generic_write_followup_pending_count" not in terminal
        or "gpu0_peer_followup_pending_count" not in terminal
        or "npu_peer_followup_pending_count" not in terminal
    ):
        errors.append("terminal invariants do not block pending generic_write/GPU0/NPU follow-up")
    if "same_tool_schema_peer_only" not in team_packet:
        errors.append("provider teamwork packet does not scope GPU0 as peer-only same-schema lane")
    if "_provider_packet_tool_catalog_limit" not in team_packet or "provider_prompt_tool_catalog_cap" not in team_packet:
        errors.append("provider teamwork packet ignores provider_prompt_tool_catalog_cap")
    errors.extend(_probe_native_tool_routing())
    errors.extend(_probe_no_tool_generic_write_capture())
    errors.extend(_probe_generic_write_broker_metadata_args(repo_root))
    errors.extend(_probe_npu_peer_evidence_timeout())
    errors.extend(_probe_npu_generic_write_result_hydration())
    errors.extend(_probe_generic_write_no_tool_product())
    errors.extend(_probe_peer_pointer_requires_later_gpu1())
    errors.extend(_probe_final_readable_generic_write_section(repo_root))
    errors.extend(_probe_unicode_json_print())
    return {"name": "ollama_native_tool_lane_contract", "errors": errors}


def _probe_native_tool_routing() -> list[str]:
    from ia_carmine.runtime.heap_gate.tool_broker_native_calls import publish_provider_native_tool_calls
    owner = _FakeNativeOwner(
        [
            _fake_report("gpu1_planner", "gpu1.json", "generic_write", 0),
            _fake_report("gpu0_peer", "gpu0.json", "generic_write", 0),
            _fake_report("npu_micro_task_auditor", "npu.json", "generic_write", 0),
        ]
    )
    published = publish_provider_native_tool_calls(owner, 1, [])
    lanes = [item.get("lane") for item in owner.state["tool_requests"]]
    diagnostics = [
        item
        for item in owner.published
        if item.get("event_type") == "validation_signal"
        and item.get("payload", {}).get("kind")
        in {"provider_peer_native_tool_call_diagnostic_only", "sidecar_generic_write_non_decision"}
    ]
    errors: list[str] = []
    if published != 1:
        errors.append(f"expected one operative GPU1 broker request, got {published}")
    if lanes != ["gpu1_planner"]:
        errors.append(f"expected only GPU1 generic_write request lane, got {lanes}")
    gpu1_request = owner.state["tool_requests"][0] if owner.state["tool_requests"] else {}
    if gpu1_request.get("tool_result_scope") != "primary_product_evidence":
        errors.append("GPU1 native request is not scoped as primary product evidence")
    if gpu1_request.get("gpu1_followup_required"):
        errors.append("GPU1 native request incorrectly requires a later GPU1 follow-up")
    diagnostic_lanes = [item.get("payload", {}).get("lane") for item in diagnostics]
    if diagnostic_lanes != ["gpu0_peer", "npu_micro_task_auditor"]:
        errors.append(f"sidecar generic_write calls did not stay diagnostic: {diagnostic_lanes}")
    return errors


def _probe_no_tool_generic_write_capture() -> list[str]:
    from ia_carmine.runtime.heap_gate.tool_broker_native_calls import publish_provider_native_tool_calls
    owner = _FakeNativeOwner(
        [
            _fake_no_tool_report("gpu1_planner", "gpu1-no-tool.json", 0),
            _fake_no_tool_report("gpu0_peer", "gpu0-no-tool.json", 0),
            _fake_no_tool_report("npu_micro_task_auditor", "npu-no-tool.json", 0),
        ]
    )
    published = publish_provider_native_tool_calls(owner, 1, [])
    requests = owner.state["tool_requests"]
    lanes = [item.get("lane") for item in requests]
    capture_modes = [item.get("args", {}).get("capture_mode") for item in requests]
    errors: list[str] = []
    if published != 0:
        errors.append(f"expected no broker request for no-tool prose, got {published}")
    if lanes:
        errors.append(f"expected no no-tool capture request lanes, got {lanes}")
    if capture_modes:
        errors.append(f"expected no no-tool capture modes, got {capture_modes}")
    primary_raw = [
        item.get("payload", {}).get("lane")
        for item in owner.published
        if item.get("payload", {}).get("kind") == "primary_free_text_without_native_tool_call"
    ]
    if primary_raw != ["gpu1_planner"]:
        errors.append(f"GPU1 no-tool prose did not stay raw evidence: {primary_raw}")
    raw_lanes = [
        item.get("payload", {}).get("lane")
        for item in owner.published
        if item.get("payload", {}).get("kind") == "sidecar_free_text_raw_evidence_non_decision"
    ]
    if raw_lanes != ["gpu0_peer", "npu_micro_task_auditor"]:
        errors.append(f"sidecar no-tool prose did not stay raw evidence: {raw_lanes}")
    return errors


def _probe_generic_write_broker_metadata_args(repo_root: Path) -> list[str]:
    from ia_carmine.runtime.runtime_tool.broker.executor import build_report
    errors: list[str] = []
    with TemporaryDirectory(prefix="generic-write-broker-") as tmp:
        root = Path(tmp)
        request = root / "request.md"
        provider = root / "provider.json"
        request.write_text("operator request", encoding="utf-8")
        provider.write_text(
            json.dumps(
                {
                    "lane": "npu_micro_task_auditor",
                    "revision": 0,
                    "provider_role": "npu_auditor",
                    "response_text": "MICRO_TASK=target_reference_audit\nDECISION=NPU_TIMEOUT_BOUNDARY",
                    "tool_calls": [],
                },
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )
        report = build_report(
            SimpleNamespace(
                repo_root=str(repo_root),
                request_data={
                    "kind": "agent_runtime_tool_requests",
                    "tool_requests": [
                        {
                            "id": "generic-write-metadata",
                            "tool": "generic_write",
                            "requirement": "generic_write_refinement",
                            "args": {
                                "request_file": str(request),
                                "provider_report": str(provider),
                                "proposal_text": "MICRO_TASK=target_reference_audit",
                                "capture_mode": "no_tool_capture",
                                "source_lane": "npu_micro_task_auditor",
                                "source_revision": "0",
                                "gpu1_followup_required": "true",
                                "peer_followup_required": "true",
                                "provider_role": "npu_auditor",
                                "reason": "smoke metadata args",
                            },
                        }
                    ],
                },
                request_packet=None,
                request_json="",
                request_file="",
                stamp="generic-write-broker-smoke",
                tool_output_dir=str(root / "tool_outputs"),
                timeout_seconds=30,
                dry_run=False,
            )
        )
        result = (report.get("tool_results") or [{}])[0]
        error_text = " ".join(str(item) for item in result.get("errors", []))
        if "unsupported args" in error_text:
            errors.append("generic_write broker still rejects metadata args")
        if result.get("executed") is not True or result.get("returncode") != 0:
            errors.append(f"generic_write broker metadata args did not execute cleanly: {result.get('errors')}")
        if not result.get("outputs", {}).get("json_report"):
            errors.append("generic_write broker metadata args did not produce json_report")
    return errors


class _FakeNativeOwner:
    def __init__(self, provider_reports: list[dict[str, Any]]) -> None:
        self.stamp = "smoke"
        self.args = SimpleNamespace(request_file="")
        self.provider_native_tool_call_ids: set[str] = set()
        self.state = {"needs": [], "tool_requests": []}
        self.tool_request_count = 0
        self.errors: list[str] = []
        self.published: list[dict[str, Any]] = []
        self.provider_reports = provider_reports

    def tool_plan(self) -> list[dict[str, Any]]:
        return []

    def enrich_plan_item_args(self, item: dict[str, Any], _events: list[dict[str, Any]]) -> dict[str, Any]:
        return dict(item)

    def provider_plan_item_for_tool_call(self, call: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any] | None:
        from ia_carmine.runtime.heap_gate.tool_broker_native_calls import provider_plan_item_for_tool_call

        return provider_plan_item_for_tool_call(self, call, events)

    def proposal_iteration_artifacts(self) -> list[str]:
        return []

    def request_text(self) -> str:
        return "smoke request"

    def publish(self, source: str, event_type: str, payload: dict[str, Any], **kwargs: Any) -> None:
        self.published.append({"source": source, "event_type": event_type, "payload": payload, **kwargs})


def _fake_report(lane: str, output: str, tool: str, revision: int) -> dict[str, Any]:
    return {
        "lane": lane,
        "output": output,
        "revision": revision,
        "response_text": f"{lane} response",
        "tool_calls": [
            {
                "id": f"{lane}_call",
                "tool": tool,
                "args": {},
                "reason": "smoke",
                "native_provider": "ollama",
                "native_shape": "ollama-python.message.tool_calls[].function",
            }
        ],
    }


def _fake_no_tool_report(lane: str, output: str, revision: int) -> dict[str, Any]:
    report = {
        "lane": lane,
        "output": output,
        "revision": revision,
        "response_text": f"{lane} useful prose response",
        "tool_calls": [],
        "provider_work_verified": True,
        "operational_provider_activity": True,
        "useful_output_produced": True,
    }
    if lane == "npu_micro_task_auditor":
        report.update(
            {
                "provider_device_verified": True,
                "provider_compute_device": "openvino/NPU",
                "npu_peer_evidence_verified": True,
                "npu_device_workload_performed": True,
                "npu_micro_audit_performed": True,
                "npu_native_tool_loop_error": "openvino_native_tool_loop_timeout",
                "npu_native_tool_loop_required": False,
            }
        )
    return report


def _probe_npu_peer_evidence_timeout() -> list[str]:
    from ia_carmine._shared.provider_work_verification import provider_work_status
    report = {
        "lane": "npu_micro_task_auditor",
        "provider_compute_device": "openvino/NPU",
        "provider_device_verified": True,
        "npu_peer_evidence_verified": True,
        "npu_response_schema_valid": True,
        "npu_device_workload_requested": True,
        "npu_device_workload_performed": True,
        "npu_micro_audit_performed": True,
        "npu_micro_provider_model_loaded": False,
        "npu_micro_provider_execution_performed": False,
        "npu_native_tool_loop_error": "openvino_native_tool_loop_timeout",
        "npu_native_tool_loop_required": False,
        "response_text": "MICRO_TASK=section_presence_audit\nCHECKED=x\nFINDINGS=y\nDECISION=NPU_TIMEOUT_BOUNDARY\nREASON=openvino_native_tool_loop_timeout",
    }
    status = provider_work_status(lane="npu_micro_task_auditor", report=report)
    errors: list[str] = []
    if status.get("workload_passed") is not True:
        errors.append("NPU peer evidence with workload+micro-audit did not count as workload")
    if status.get("semantic_contract_passed") is not False:
        errors.append("NPU follow-up pending/timeout should not pass semantic contract")
    if status.get("provider_requirement_complete") is not False:
        errors.append("NPU follow-up pending/timeout should not complete provider requirement")
    if status.get("provider_work_verified") is not False:
        errors.append("provider_work_verified must remain an alias of provider_requirement_complete")
    if status.get("provider_role") != "npu_auditor":
        errors.append("verified NPU peer evidence did not count as npu_auditor")
    if report.get("npu_micro_provider_model_loaded") is not False:
        errors.append("NPU native model-loaded flag must remain false on tool-loop timeout")
    if report.get("npu_native_tool_loop_error") != "openvino_native_tool_loop_timeout":
        errors.append("NPU native tool-loop timeout was not preserved")
    return errors
def _probe_npu_generic_write_result_hydration() -> list[str]:
    from ia_carmine.runtime.heap_gate.generic_write_followup import generic_write_document_product
    from ia_carmine.runtime.provider_runtime_blackboard.broker_bridge.cli import mapped_request_payload
    errors: list[str] = []
    with TemporaryDirectory(prefix="npu-generic-write-hydration-") as tmp:
        root = Path(tmp)
        provider = {
            "lane": "npu_micro_task_auditor",
            "revision": 0,
            "provider_block_id": "npu:0",
            "passed": True,
            "provider_execution_performed": True,
            "provider_work_verified": True,
            "response_text": "MICRO_TASK=target_reference_audit\nDECISION=NPU_TIMEOUT_BOUNDARY",
        }
        (root / "npu.json").write_text(json.dumps(provider), encoding="utf-8")
        report = {"passed": True, "source_lane": provider["lane"], "provider_report": "npu.json", "capture_mode": "no_tool_capture", "provider_summary": provider, "provider_response_excerpt": provider["response_text"]}
        (root / "generic.json").write_text(json.dumps(report), encoding="utf-8")
        request_id = "20260523_provider-no-tool-capture_npu_micro_task_auditor_000_generic_writ"
        result_id = request_id + "_generic_write_md"
        payload = mapped_request_payload({request_id: {"lane": "npu_micro_task_auditor"}}, result_id)
        if payload.get("lane") != "npu_micro_task_auditor":
            errors.append("broker bridge did not recover truncated NPU request payload")
        owner = SimpleNamespace(repo_root=root, provider_reports=[{"lane": "gpu1_planner", "revision": 0}])
        broker_payload = {"tool": "generic_write", "lane": None, "revision": None, "gpu1_followup_required": None, "blocked": False, "returncode": 0, "summary": {"passed": True}, "outputs": {"json_report": "generic.json"}, "errors": []}
        product = generic_write_document_product(owner, [{"event_type": "broker_result", "payload": broker_payload}])
        checks = [
            ("npu_micro_task_auditor" not in product.get("generic_write_lanes", []), "NPU generic_write was incorrectly counted as operative"),
            (product.get("npu_peer_followup_pending_count") == 0, "NPU generic_write still creates generic_write follow-up"),
            ("MICRO_TASK=target_reference_audit" not in str(product.get("captures")), "NPU generic_write prose entered product captures"),
        ]
        errors.extend(message for passed, message in checks if not passed)
    return errors
def _probe_generic_write_no_tool_product() -> list[str]:
    from ia_carmine.runtime.heap_gate.generic_write_followup import generic_write_document_product
    from ia_carmine.runtime.runtime_tool.generic_write.cli import build_report
    errors: list[str] = []
    with TemporaryDirectory(prefix="generic-write-smoke-") as tmp:
        root = Path(tmp)
        (root / "request.md").write_text("operator asks for a code plan", encoding="utf-8")
        broker_report = {
            "kind": "agent_runtime_tool_broker",
            "passed": False,
            "tool_results": [
                {
                    "id": "tool-001",
                    "tool": "run_heap_code_execution_matrix",
                    "executed": True,
                    "blocked": False,
                    "returncode": 2,
                    "errors": ["runtime boom"],
                    "warnings": [],
                }
            ],
            "errors": ["matrix failed"],
            "warnings": [],
        }
        (root / "broker.json").write_text(
            json.dumps(broker_report, ensure_ascii=False), encoding="utf-8"
        )
        events: list[dict[str, Any]] = []
        for revision in range(3):
            provider = {
                "lane": "gpu1_planner",
                "revision": revision,
                "provider_block_id": f"gpu1:{revision}",
                "passed": True,
                "provider_execution_performed": True,
                "provider_work_verified": True,
                "response_text": f"provider prose output {revision}\n```python\nprint({revision})\n```",
                "native_tool_call_count": 0,
            }
            provider_path = root / f"provider-{revision}.json"
            provider_path.write_text(json.dumps(provider, ensure_ascii=False), encoding="utf-8")
            report = build_report(
                SimpleNamespace(
                    repo_root=str(root),
                    request_file="request.md",
                    operator_request="",
                    provider_report=provider_path.name,
                    proposal_text="",
                    capture_mode="no_tool_capture",
                    evidence_report=["broker.json"],
                    source_lane="gpu1_planner",
                    reason="smoke no-tool capture",
                )
            )
            if "provider prose output" not in report.get("refined_request", ""):
                errors.append("generic_write no-tool report does not include provider prose output")
            if "runtime boom" not in report.get("refined_request", ""):
                errors.append("generic_write no-tool report hides failed broker/runtime errors")
            report_path = root / f"generic-write-{revision}.json"
            report_path.write_text(json.dumps(report, ensure_ascii=False), encoding="utf-8")
            events.append(
                {
                    "event_type": "broker_result",
                    "payload": {
                        "tool": "generic_write",
                        "lane": "gpu1_planner",
                        "revision": revision,
                        "blocked": False,
                        "returncode": 0,
                        "summary": {"passed": True},
                        "outputs": {"json_report": report_path.name},
                    },
                }
            )

        class Owner:
            pass
        owner = Owner()
        owner.repo_root = root
        owner.provider_reports = [{"lane": "gpu1_planner", "revision": 3}]
        owner.gpu1_consumed_generic_write_block_ids = ["gpu1:0", "gpu1:1", "gpu1:2"]
        product = generic_write_document_product(owner, events)
        if not product.get("eligible"):
            errors.append("three consumed generic_write captures did not become eligible")
        if product.get("patch_application_performed") or product.get("source_writes_performed"):
            errors.append("generic_write refined product incorrectly claims source writes")
        if "provider prose output 2" not in product.get("latest_refined_request", ""):
            errors.append("generic_write refined product does not include latest provider prose")
        if "runtime boom" not in product.get("latest_refined_request", ""):
            errors.append("generic_write refined product does not include runtime error evidence")
    return errors


def _probe_peer_pointer_requires_later_gpu1() -> list[str]:
    from ia_carmine.runtime.heap_gate.pointer_soft_lock import pointer_closure_summary
    peer_final = [
        {"block_id": "p0", "role": "gpu1_planner", "accepted": True},
        {
            "block_id": "npu0",
            "role": "npu_auditor",
            "accepted": True,
            "refines_block_id": "p0",
        },
    ]
    consumed = [
        *peer_final,
        {
            "block_id": "p1",
            "role": "gpu1_planner",
            "accepted": True,
            "previous_block_id": "npu0",
        },
    ]
    peer_table = pointer_closure_summary(peer_final).get("pointer_closure_table", [])
    consumed_table = pointer_closure_summary(consumed).get("pointer_closure_table", [])
    peer_row = next((row for row in peer_table if row.get("pointer_id") == "npu0"), {})
    consumed_row = next((row for row in consumed_table if row.get("pointer_id") == "npu0"), {})
    errors: list[str] = []
    if peer_row.get("closure_status") != "deferred_to_resume":
        errors.append("final NPU peer block closed without later GPU1 consumption")
    if consumed_row.get("closure_status") != "merged_into_final_product":
        errors.append("NPU peer block consumed by later GPU1 did not close")
    return errors


def _probe_final_readable_generic_write_section(repo_root: Path) -> list[str]:
    text = _read(repo_root, "ia_carmine/_shared/heap_final_readable_synthesis.py")
    errors: list[str] = []
    if "## Generic write" not in text:
        errors.append("final readable product does not render a generic_write section")
    if "provider_response_excerpt" not in text or "Runtime/tool errors catturati" not in text:
        errors.append("final readable generic_write section does not expose prose/runtime errors")
    return errors


def _probe_unicode_json_print() -> list[str]:
    from ia_carmine._shared.report_io import print_json_report
    previous_stdout = sys.stdout
    buffer = io.BytesIO()
    sys.stdout = io.TextIOWrapper(buffer, encoding="cp1252", errors="strict")
    errors: list[str] = []
    try:
        print_json_report({"emoji": "🔍", "passed": True})
        sys.stdout.flush()
        output = buffer.getvalue().decode("cp1252")
        if "\\ud83d\\udd0d" not in output and "\\U0001f50d" not in output and "\\ud83d" not in output:
            errors.append("Unicode fallback did not emit ASCII escaped JSON")
    except UnicodeEncodeError:
        errors.append("print_json_report still raises UnicodeEncodeError on cp1252 stdout")
    finally:
        sys.stdout = previous_stdout
    return errors


def _check_vulkan_identity_contract(repo_root: Path) -> dict[str, Any]:
    vulkan = _read(repo_root, "ia_carmine/providers/ollama/vulkan_devices.py")
    context = _read(repo_root, "ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md")
    errors: list[str] = []
    if 'vendor == "0x8086"' not in vulkan:
        errors.append("Vulkan GPU0 auto-selection is not pinned to Intel vendor identity")
    if "Windows Task Manager numbering" not in context:
        errors.append("provider mesh context does not document Windows/Vulkan index mismatch")
    if "GGML_VK_VISIBLE_DEVICES" not in context:
        errors.append("provider mesh context does not document resolved Vulkan visible device")
    return {"name": "vulkan_identity_contract", "errors": errors}


def _check_provider_residency_lifecycle(repo_root: Path) -> dict[str, Any]:
    provider_time = _read(repo_root, "ia_carmine/runtime/heap_gate/provider_time.py")
    heap_context = _read(repo_root, "ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md")
    mesh_context = _read(repo_root, "ia_carmine/providers/provider_mesh/TOOL_CONTEXT.md")
    errors: list[str] = []
    for marker in (
        "keep_gpu1_gpu0_loaded_across_provider_revisions_until_production_cycle_cleanup",
        "ollama_model_unload_only_at_provider_production_cycle_cleanup",
    ):
        if marker not in provider_time:
            errors.append(f"provider time contract missing residency marker {marker}")
    if "GPU1 must remain resident for the whole provider production cycle" not in heap_context:
        errors.append("heap gate context does not document GPU1 production-cycle residency")
    if "model unload and GPU0 `11435` shutdown are final cleanup" not in mesh_context:
        errors.append("provider mesh context does not document final cleanup residency")
    return {"name": "provider_residency_lifecycle", "errors": errors}


def _read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8", errors="replace")


def _extract_function(text: str, name: str) -> str:
    marker = f"def {name}("
    start = text.find(marker)
    if start < 0:
        return ""
    next_def = text.find("\ndef ", start + len(marker))
    return text[start:] if next_def < 0 else text[start:next_def]


def _resolve(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


if __name__ == "__main__":
    raise SystemExit(main())
