from __future__ import annotations

import io
import json
import sys
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any

from Tools.validation.heap_runtime.provider_loop_code_delta_checks import (
    probe_code_delta_file_read_contract,
)

def check_ollama_native_tool_lane_contract(repo_root: Path) -> dict[str, Any]:
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
    try:
        from ia_carmine._shared.provider_tool_loop import ollama_tool_visibility

        visibility = ollama_tool_visibility(
            include_generic_write=False,
            gpu1_concrete_only=True,
        )
    except Exception as exc:
        visibility = {"actual_chat_tool_names": [], "hidden_tool_reasons": {}}
        errors.append(f"GPU1 concrete tool visibility probe failed: {exc}")
    actual_tools = set(visibility.get("actual_chat_tool_names") or [])
    hidden_reasons = (
        visibility.get("hidden_tool_reasons")
        if isinstance(visibility.get("hidden_tool_reasons"), dict)
        else {}
    )
    forbidden_concrete_tools = {
        "generic_write",
        "agent_runtime_debug_lab",
        "run_heap_code_execution_matrix",
        "run_heap_virtual_dev_environment",
        "synthesize_patch_candidates",
        "analyze_code_product_artifact",
    }
    leaked_tools = sorted(actual_tools & forbidden_concrete_tools)
    if leaked_tools:
        errors.append(f"GPU1 concrete chat tool list exposes late-stage/refinement tools: {leaked_tools}")
    missing_hidden = [
        name for name in sorted(forbidden_concrete_tools)
        if name not in hidden_reasons
    ]
    if missing_hidden:
        errors.append(f"GPU1 concrete chat tool hidden reasons missing: {missing_hidden}")
    for marker in (
        "ollama_tool_visibility",
        "actual_chat_tool_names",
        "hidden_tool_names",
        "hidden_tool_reasons",
    ):
        if marker not in loop:
            errors.append(f"Ollama tool visibility report lacks {marker}")
    for source, name in (
        (loop, "provider_tool_loop"),
        (_read(repo_root, "ia_carmine/runtime/heap_gate/provider_prompt.py"), "provider_prompt"),
        (_read(repo_root, "ia_carmine/runtime/heap_gate/provider_time.py"), "provider_time"),
        (_read(repo_root, "ia_carmine/_shared/heap_final_readable_synthesis.py"), "heap_final_readable_synthesis"),
    ):
        if "HEAP_DELTA_PROPOSAL" in source:
            errors.append(f"{name} still advertises HEAP_DELTA_PROPOSAL on active provider path")
    if "FINAL_PRODUCT_DELTA" not in loop:
        errors.append("provider_tool_loop fallback does not use FINAL_PRODUCT_DELTA")
    for source, name in ((provider_context, "GPU1 prompt"), (gpu0, "GPU0 prompt")):
        if "BROKER_NATIVE_TOOL_RULE" not in source or "generic_write" not in source:
            errors.append(f"{name} lacks generic_write native broker instruction")
    for marker in (
        "FINAL_PRODUCT_DELTA",
        "FINAL_PRODUCT_KIND",
        "FINAL_PRODUCT_ACTION",
        "CURRENT_POINTER",
        "CONSUMED_EVIDENCE",
        "NEXT_RUNTIME_INTENT",
        "FILE_READ_GROUNDING_RULE",
        "runtime_file_window",
    ):
        if marker not in provider_context:
            errors.append(f"GPU1 prompt lacks {marker} final-product delta contract")
    for forbidden in (
        "FINAL_PRODUCT_KIND: text|code|text_and_code|blocked",
        "FINAL_PRODUCT_ACTION: append|replace|supersede|refine|blocked",
    ):
        if forbidden in provider_context:
            errors.append(f"GPU1 prompt still allows blocked in final-product protocol: {forbidden}")
    if "gpu1_blocked_not_allowed_as_final_product_delta" not in terminal:
        errors.append("terminal invariants do not expose GPU1 blocked-output final-product blocker")
    if "gpu1_code_delta_without_file_read" not in terminal:
        errors.append("terminal invariants do not block code deltas without brokered file-read evidence")
    if "code_delta_file_read_required" not in team_packet:
        errors.append("provider teamwork packet does not advertise code-delta file-read grounding")
    if "GENERIC_WRITE_PRODUCT_MIN_REFINEMENTS = 3" not in followup:
        errors.append("generic_write follow-up does not require three refinements")
    if "generic_write_next_turn_required" not in followup:
        errors.append("generic_write follow-up does not force next GPU1 turn")
    if "gpu0_peer_followup_pending_count" not in followup:
        errors.append("GPU0 peer evidence does not force later GPU1 consumption")
    if "npu_peer_followup_pending_count" not in followup:
        errors.append("NPU peer evidence does not force later GPU1 consumption")
    if '"kind": "generic_write_refined_request"' not in followup:
        errors.append("generic_write follow-up is not declassified to refined request evidence")
    if '"eligible": False' not in followup:
        errors.append("generic_write follow-up can still become product eligible")
    if '"code_product_allowed_after_three_refinements": False' not in followup:
        errors.append("generic_write can still become refined product after three iterations")
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
    errors.extend(probe_code_delta_file_read_contract(repo_root))
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
    if gpu1_request.get("tool_result_scope") != "primary_pending_gpu1_resume_evidence":
        errors.append("GPU1 native request is not scoped as pending GPU1 resume evidence")
    if gpu1_request.get("gpu1_followup_required") is not True:
        errors.append("GPU1 native request does not require a later GPU1 follow-up")
    if gpu1_request.get("cannot_close_product") is not True:
        errors.append("GPU1 native request can still close product before resume")
    diagnostic_lanes = [item.get("payload", {}).get("lane") for item in diagnostics]
    if diagnostic_lanes != ["gpu0_peer", "npu_micro_task_auditor"]:
        errors.append(f"sidecar generic_write calls did not stay diagnostic: {diagnostic_lanes}")
    window_owner = _FakeNativeOwner(
        [
            _fake_report(
                "gpu1_planner",
                "gpu1-window.json",
                "runtime_file_window",
                0,
                args={"path": "AGENTS.md", "length": 123},
            )
        ]
    )
    manifest = window_owner.provider_work_dir() / "startup_manifest.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "kind": "startup_manifest_fixture",
                "refs": {"agents": {"ref_id": "agents", "path": "AGENTS.md"}},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    window_owner.startup_manifest_path = manifest
    publish_provider_native_tool_calls(window_owner, 1, [])
    window_request = (
        window_owner.state["tool_requests"][0]
        if window_owner.state["tool_requests"]
        else {}
    )
    window_args = window_request.get("args") if isinstance(window_request.get("args"), dict) else {}
    if window_args.get("strict_startup_refs") is not True or not window_args.get("startup_manifest"):
        errors.append("runtime_file_window broker request is not enriched with strict startup refs")
    if window_args.get("limit") != 123:
        errors.append("runtime_file_window length alias was not normalized to limit")
    normalized_from = (
        window_args.get("argument_normalized_from")
        if isinstance(window_args.get("argument_normalized_from"), dict)
        else {}
    )
    if normalized_from.get("limit") != "length":
        errors.append("runtime_file_window length alias normalization was not recorded")
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
        self.repo_root = Path.cwd().resolve()
        self.startup_manifest_path: Path | None = None
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
    def provider_work_dir(self) -> Path:
        return self.repo_root / "output" / "validation" / "provider_loop_activation_smoke"

    def startup_manifest_from_task_file(self) -> tuple[Path | None, dict[str, Any]]:
        if self.startup_manifest_path:
            return self.startup_manifest_path, {}
        return None, {}

    def publish(self, source: str, event_type: str, payload: dict[str, Any], **kwargs: Any) -> None:
        self.published.append({"source": source, "event_type": event_type, "payload": payload, **kwargs})


def _fake_report(
    lane: str,
    output: str,
    tool: str,
    revision: int,
    *,
    args: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "lane": lane,
        "output": output,
        "revision": revision,
        "response_text": f"{lane} response",
        "tool_calls": [
            {
                "id": f"{lane}_call",
                "tool": tool,
                "args": dict(args or {}),
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
            refined_tail = str(report.get("refined_request_tail") or "")
            if "provider prose output" not in refined_tail:
                errors.append("generic_write no-tool report does not include provider prose output")
            if "runtime boom" not in refined_tail:
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
        if product.get("eligible"):
            errors.append("three consumed generic_write captures became product eligible")
        if not product.get("diagnostic_evidence_ready"):
            errors.append("three consumed generic_write captures did not become diagnostic evidence")
        if product.get("patch_application_performed") or product.get("source_writes_performed"):
            errors.append("generic_write refined request evidence incorrectly claims source writes")
        if "provider prose output 2" not in product.get("latest_refined_request", ""):
            errors.append("generic_write refined request evidence does not include latest provider prose")
        if "runtime boom" not in product.get("latest_refined_request", ""):
            errors.append("generic_write refined request evidence does not include runtime error evidence")
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


def _read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8", errors="replace")
