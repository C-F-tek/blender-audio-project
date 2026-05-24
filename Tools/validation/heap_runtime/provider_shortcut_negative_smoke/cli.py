#!/usr/bin/env python3
"""Negative smoke for provider execution and sidecar shortcut regressions."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
from typing import Any

from ia_carmine.product.heap_final_proposals.common import (
    provider_report_execution_performed,
)
from ia_carmine.product.heap_final_proposals.normalize_final_causality.cli import (
    provider_execution_performed as causality_provider_execution_performed,
)
from ia_carmine.product.code_product.final_readable_product.product_contract import (
    final_product_blockers,
)
from ia_carmine.product.generated_patch_specs.proposal_common import (
    EXPECTED_APPLY_MODE,
    EXPECTED_PROPOSAL_KIND,
)
from ia_carmine.product.generated_patch_specs.proposal_manifest import build_patch_specs
from ia_carmine.context.heap_context_memory_reload.manifest import build_manifest
from ia_carmine.runtime.external_heap.block_pointer_manifest.provider_graph import (
    provider_blocks,
)
from ia_carmine.runtime.heap_gate.run_loop_metrics import _lane_has_model_execution
from ia_carmine.runtime.heap_gate.proposal_cycle_a import RuntimeGateProposalCycleAMixin
from ia_carmine.runtime.heap_gate.generic_write_followup import (
    generic_write_document_product_eligible,
)
from ia_carmine.runtime.heap_gate.provider_recovery import provider_recovery_status
from ia_carmine.runtime.heap_gate.provider_commands import RuntimeGateProviderCommandsMixin
from ia_carmine.runtime.heap_gate.provider_teamwork_packet import (
    _provider_packet_tool_catalog_limit,
)
from ia_carmine.runtime.heap_gate.tool_broker import RuntimeGateToolBrokerMixin
from ia_carmine.runtime.heap_gate.tool_broker_native_calls import (
    publish_provider_native_tool_calls,
)


def run_smoke(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    fake_unverified = {
        "lane": "gpu1_planner",
        "response_text": "provider_execution_performed=true but this is only prose",
        "provider_work_verified": False,
    }
    if provider_report_execution_performed(fake_unverified):
        errors.append("composer accepted response_text/provider_execution_performed=true as execution")
    if causality_provider_execution_performed({"provider_reports": [fake_unverified]}):
        errors.append("causality accepted unverified provider report as execution")
    owner = SimpleNamespace(provider_reports=[fake_unverified])
    if RuntimeGateProposalCycleAMixin.provider_work_verified_for_revision(owner, 0):
        errors.append("proposal cycle accepted non-empty provider_reports as execution")
    attempted_not_verified = {
        "lane": "gpu1_planner",
        "provider_backend": "ollama",
        "provider_execution_attempted": True,
        "provider_io_observed": True,
        "provider_execution_performed": False,
        "provider_work_verified": False,
        "response_text": "GPU1 text exists but compute/semantic proof is missing.",
    }
    if _lane_has_model_execution([attempted_not_verified], "gpu1_planner"):
        errors.append("lane metrics accepted attempted/raw response as verified model execution")
    if not _npu_peer_evidence_not_verified_role():
        errors.append("NPU peer evidence availability was counted as verified provider role")
    blockers = _weak_gate_final_product_blockers()
    if not any("verified pointer evidence" in item for item in blockers):
        errors.append("final product accepted weak gate provider_execution_performed fallback")
    gate_failed_blockers = _gate_failed_final_product_blockers()
    if not any("heap runtime completeness gate did not pass" in item for item in gate_failed_blockers):
        errors.append("final readable product ignored failed heap gate")
    if not _generated_patch_specs_reject_raw_provider_claim(repo_root):
        errors.append("generated patch specs accepted raw provider_execution_performed claim")
    graph = _build_pointer_graph()
    invalid_blocks = [
        block
        for block in graph
        if block.get("block_type") == "observed_invalid_provider_evidence"
    ]
    if len(invalid_blocks) != 2:
        errors.append(f"expected two observed-invalid sidecar blocks, got {len(invalid_blocks)}")
    if any(block.get("provider_role_counted") for block in invalid_blocks):
        errors.append("observed-invalid sidecar block counted as verified role")
    if any(not block.get("refines_block_id") for block in invalid_blocks):
        errors.append("observed-invalid sidecar block is not linked to GPU1/proposal pointer")
    if _sidecar_generic_write_published():
        errors.append("GPU0/NPU generic_write entered operative broker requests")
    if not _npu_revision_refs_are_current_only():
        errors.append("proposal cycle backfilled stale NPU ref from a previous revision")
    if not _generic_write_requires_matching_current_consumed_refs():
        errors.append("generic_write product eligibility accepted stale consumed refs")
    if not _generic_write_consumption_persisted_in_packet_source(repo_root):
        errors.append("generic_write consumed refs are not persisted into GPU1 packet/artifact")
    if _provider_packet_tool_catalog_limit(
        SimpleNamespace(args=SimpleNamespace(tool_catalog_limit=80, provider_prompt_tool_catalog_cap=20))
    ) != 20:
        errors.append("provider teamwork packet ignores provider_prompt_tool_catalog_cap")
    if _profile_caps_are_unbounded(repo_root):
        errors.append("heap runtime launcher profiles still default provider_prompt_tool_catalog_cap to 0")
    if not _startup_manifest_carries_effective_config(repo_root):
        errors.append("startup manifest does not expose startup_effective_config")
    if not _inner_runtime_fallbacks_report_derived_config(repo_root):
        errors.append("inner runtime fallbacks are not exposed as derived_config")
    if not _standalone_provider_tools_report_default_sources(repo_root):
        errors.append("standalone provider tools do not expose standalone_default config sources")
    if not _full_run_rejects_standalone_default_provider_evidence(repo_root):
        errors.append("full-run provider absorption does not reject standalone_default evidence")
    if not _full_run_accepts_fingerprinted_canonical_provider_evidence(repo_root):
        errors.append("canonical fingerprinted provider evidence is still rejected as standalone")
    if not _lane_manifest_preserves_derived_config(repo_root):
        errors.append("provider launch manifest does not preserve lane derived_config")
    requirement_report = _requirement_semantics_report()
    if requirement_report.get("missing_requirements"):
        errors.append("attempted sidecar requirements were reported as missing")
    expected_failed = {"gpu0_provider_peer", "npu_micro_task_auditor"}
    if set(requirement_report.get("failed_requirements") or []) != expected_failed:
        errors.append("attempted sidecar failures were not separated from missing requirements")
    return {
        "schema_version": 1,
        "kind": "provider_shortcut_negative_smoke",
        "passed": not errors,
        "errors": errors,
        "requirement_semantics": requirement_report,
    }


def _npu_peer_evidence_not_verified_role() -> bool:
    owner = SimpleNamespace(
        args=SimpleNamespace(max_provider_revisions=2),
        provider_revision_count=0,
        provider_recovery_attempt_count=0,
        provider_reports=[
            {
                "lane": "npu_micro_task_auditor",
                "provider_role": "npu_auditor",
                "revision": 0,
                "provider_block_id": "npu:semantic-reject",
                "npu_peer_evidence_verified": True,
                "semantic_contract_passed": False,
                "provider_work_verified": False,
                "provider_rejection_reason": "provider_semantic_contract_failed",
                "response_text": "NPU evidence exists but semantic contract rejected it.",
            }
        ],
        latest_proposal_iteration_report=lambda: {},
        latest_rejected_proposal_requires_retry=lambda: False,
    )
    status = provider_recovery_status(owner, [])
    return (
        "npu_auditor" not in set(status.get("roles_verified") or [])
        and "npu_auditor" in set(status.get("roles_observed_invalid") or [])
    )


def _weak_gate_final_product_blockers() -> list[str]:
    with TemporaryDirectory(prefix="provider-shortcut-contract-") as tmp:
        markdown = Path(tmp) / "FINAL.md"
        markdown.write_text("ok", encoding="utf-8")
        return final_product_blockers(
            markdown_output=markdown,
            final_document_status="APPLY_REVIEW_READY",
            concrete_code_proposal_count=1,
            code_product_metrics={
                "diff_git_blocks": 1,
                "empty_code_product_marker": False,
                "no_applicable_marker": False,
                "truncation_marker": False,
            },
            code_product_ready=True,
            pointer={
                "passed": True,
                "edge_count": 1,
                "all_roles_present": [
                    "gpu1_planner",
                    "gpu0_reviewer_refiner",
                    "npu_auditor",
                ],
                "provider_execution_performed": False,
            },
            revision={"linked_gpu0_block_count": 1, "linked_npu_block_count": 1},
            matrix={"passed": True},
            gate={"provider_execution_performed": True},
        )


def _gate_failed_final_product_blockers() -> list[str]:
    with TemporaryDirectory(prefix="provider-shortcut-gate-failed-") as tmp:
        markdown = Path(tmp) / "FINAL.md"
        markdown.write_text("ok", encoding="utf-8")
        return final_product_blockers(
            markdown_output=markdown,
            final_document_status="APPLY_REVIEW_READY",
            concrete_code_proposal_count=1,
            code_product_metrics={
                "diff_git_blocks": 1,
                "empty_code_product_marker": False,
                "no_applicable_marker": False,
                "truncation_marker": False,
            },
            code_product_ready=True,
            pointer={
                "passed": True,
                "edge_count": 1,
                "all_roles_present": [
                    "gpu1_planner",
                    "gpu0_reviewer_refiner",
                    "npu_auditor",
                ],
                "provider_execution_performed": True,
            },
            revision={"linked_gpu0_block_count": 1, "linked_npu_block_count": 1},
            matrix={"passed": True},
            gate={"passed": False, "errors": ["heap_failed"]},
        )


def _generated_patch_specs_reject_raw_provider_claim(repo_root: Path) -> bool:
    with TemporaryDirectory(prefix="provider-shortcut-patch-spec-") as tmp:
        root = Path(tmp)
        proposal = root / "proposal.json"
        proposal.write_text(
            json.dumps(
                {
                    "kind": EXPECTED_PROPOSAL_KIND,
                    "apply_mode": EXPECTED_APPLY_MODE,
                    "provider_execution_performed": True,
                    "provider_work_verified": False,
                    "proposals": [],
                },
                indent=2,
            ),
            encoding="utf-8",
        )
        manifest = build_patch_specs(
            repo_root=repo_root,
            proposal_path=proposal,
            output_dir=root / "out",
            basename="smoke",
            max_proposals=None,
            require_provider_execution=True,
        )
    return (
        manifest.get("provider_execution_claim_seen") is True
        and manifest.get("provider_execution_performed") is False
        and manifest.get("passed") is False
        and any("provider_work_verified=true" in str(item) for item in manifest.get("errors") or [])
    )


def _requirement_semantics_report() -> dict[str, Any]:
    owner = _FakeRequirementOwner(
        [
            {
                "lane": "gpu0_peer",
                "requirement": "gpu0_provider_peer",
                "provider_backend": "ollama",
                "provider_compute_device": "ollama/gpu0-vulkan",
                "provider_execution_performed": True,
                "provider_work_verified": False,
                "response_text": "sidecar observed but invalid",
            },
            {
                "lane": "npu_micro_task_auditor",
                "requirement": "npu_micro_task_auditor",
                "provider_execution_performed": True,
                "provider_work_verified": False,
                "response_text": "sidecar observed but invalid",
            },
        ]
    )
    return {
        "missing_requirements": owner.missing_requirements([]),
        "unattempted_requirements": owner.unattempted_requirements([]),
        "failed_requirements": owner.failed_requirements([]),
        "unsatisfied_requirements": owner.unsatisfied_requirements([]),
    }


def _profile_caps_are_unbounded(repo_root: Path) -> bool:
    profile = repo_root / "ia_carmine/runtime/run/profiles/heap_runtime_launcher_profiles.json"
    try:
        data = json.loads(profile.read_text(encoding="utf-8-sig"))
    except Exception:
        return True
    text = json.dumps(data)
    return '"provider_prompt_tool_catalog_cap": 0' in text


def _startup_manifest_carries_effective_config(repo_root: Path) -> bool:
    with TemporaryDirectory(prefix="provider-shortcut-startup-config-") as tmp:
        root = Path(tmp)
        task_file = root / "task.md"
        task_file.write_text("task", encoding="utf-8")
        effective = {
            "startup_provider_input_workers": 7,
            "startup_required_context_profile": "project_self_improvement",
            "startup_operational_memory_query": "smoke query",
            "startup_operational_memory_limit": 3,
            "parallel_provider_input_lanes": "repo_docs_map,tool_catalog",
        }
        manifest = build_manifest(
            stamp="smoke",
            repo_root=repo_root,
            project_python="python",
            request_text="request",
            context_files=["AGENTS.md"],
            artifacts={
                "heap_task_file": "task.md",
                "startup_parallel_provider_input_lanes": effective[
                    "parallel_provider_input_lanes"
                ],
            },
            commands=[],
            warnings=[],
            task_file=task_file,
            context_delta={},
            context_pack_result={"artifact_useful": True},
            strict_ai_context_pack=False,
            strict_startup_reload=False,
            startup_effective_config=effective,
        )
    return (
        manifest.get("startup_effective_config") == effective
        and manifest.get("contract", {}).get("startup_effective_config") == effective
    )


def _inner_runtime_fallbacks_report_derived_config(repo_root: Path) -> bool:
    runtime_init = (repo_root / "ia_carmine/runtime/heap_gate/runtime_init.py").read_text(
        encoding="utf-8", errors="replace"
    )
    command_specs = (repo_root / "ia_carmine/runtime/heap_gate/provider_command_specs.py").read_text(
        encoding="utf-8", errors="replace"
    )
    coexistence = (
        repo_root / "ia_carmine/runtime/heap_gate/provider_coexistence_preflight.py"
    ).read_text(encoding="utf-8", errors="replace")
    provider_time = (repo_root / "ia_carmine/runtime/heap_gate/provider_time.py").read_text(
        encoding="utf-8", errors="replace"
    )
    return bool(
        "derived_runtime_config" in runtime_init
        and "derived_config" in command_specs
        and "ollama_context_candidates" in command_specs
        and "fixed_health_probe_budget" in coexistence
        and "gpu0.sidecar_budget_seconds" in provider_time
    )


def _standalone_provider_tools_report_default_sources(repo_root: Path) -> bool:
    files = [
        repo_root / "ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py",
        repo_root / "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py",
        repo_root / "ia_carmine/providers/provider_mesh/local_provider_probe/cli.py",
        repo_root / "ia_carmine/providers/ollama/role_models.py",
    ]
    texts = [path.read_text(encoding="utf-8", errors="replace") for path in files]
    return all(
        "config_sources" in text
        and "standalone_default_fields" in text
        and "standalone_default" in text
        for text in texts
    )


def _full_run_rejects_standalone_default_provider_evidence(repo_root: Path) -> bool:
    source = (repo_root / "ia_carmine/runtime/heap_gate/provider_commands.py").read_text(
        encoding="utf-8", errors="replace"
    )
    return bool(
        "standalone_default_fields" in source
        and "standalone_default_config_not_accepted_as_full_run_provider_evidence" in source
        and 'report_data["provider_work_verified"] = False' in source
        and 'report_data["provider_role_counted"] = False' in source
    )


def _full_run_accepts_fingerprinted_canonical_provider_evidence(repo_root: Path) -> bool:
    owner = RuntimeGateProviderCommandsMixin()
    owner.args = SimpleNamespace(canonical_run_fingerprint="canonical-smoke")
    owner.repo_root = repo_root
    owner.provider_execution_performed = False
    report = {
        "provider_id": "gpu1_planner",
        "provider_backend": "ollama",
        "provider_compute_device": "ollama/gpu1",
        "provider_loaded": True,
        "provider_device_verified": True,
        "device_identity_verified": True,
        "ollama_full_gpu_verified": True,
        "ollama_compute_verified": True,
        "selected_model": "qwen2.5-coder:14b",
        "completion_token_count": 1024,
        "eval_count": 1024,
        "done": True,
        "response_text": "HEAP_DELTA_PROPOSAL\nTARGET_FILES:\n- ia_carmine/runtime/heap_gate/provider_commands.py\nPATCH_SKETCH:\n```diff\n@@\n+ok\n```",
        "passed": True,
        "standalone_default_fields": ["strict_provider_model"],
        "canonical_run_provider_evidence": True,
        "canonical_run_fingerprint": "canonical-smoke",
    }
    summary = owner.summarize_provider_report(
        {"lane": "gpu1_planner", "role": "gpu1_provider_planner", "requirement": "gpu1_provider_planner", "output": "gpu1.json"},
        subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr=""),
        report,
    )
    return bool(
        summary.get("provider_work_verified")
        and not str(summary.get("provider_rejection_reason") or "").startswith(
            "standalone_default_config_not_accepted"
        )
        and report.get("standalone_default_fields_ignored_reason")
        == "canonical_run_provider_evidence_fingerprint_verified"
    )


def _lane_manifest_preserves_derived_config(repo_root: Path) -> bool:
    source = (repo_root / "ia_carmine/runtime/heap_gate/provider_lane_launch.py").read_text(
        encoding="utf-8", errors="replace"
    )
    execution = (repo_root / "ia_carmine/runtime/heap_gate/provider_execution.py").read_text(
        encoding="utf-8", errors="replace"
    )
    return bool(
        '"derived_config": derived_config' in source
        and 'spec.get("derived_config") or []' in execution
        and "time_counter_contract" in source
    )


def _build_pointer_graph() -> list[dict[str, Any]]:
    with TemporaryDirectory(prefix="provider-shortcut-graph-") as tmp:
        root = Path(tmp)
        provider_dir = root / "provider_teamwork"
        provider_dir.mkdir()
        _write(provider_dir / "gpu1.json", _gpu1_report())
        _write(provider_dir / "gpu0.json", _gpu0_incongruent_report())
        _write(provider_dir / "npu.json", _npu_invalid_report())
        return provider_blocks(root, root, 4000)


def _sidecar_generic_write_published() -> bool:
    owner = _FakeNativeOwner(
        [
            _tool_report("gpu0_peer", "gpu0.json"),
            _tool_report("npu_micro_task_auditor", "npu.json"),
        ]
    )
    publish_provider_native_tool_calls(owner, 1, [])
    return bool(owner.state["tool_requests"])


def _npu_revision_refs_are_current_only() -> bool:
    class _ProposalOwner(RuntimeGateProposalCycleAMixin):
        def __init__(self) -> None:
            self.provider_reports = [
            {
                "lane": "gpu1_planner",
                "revision": 1,
                "provider_block_id": "gpu1:001",
                "provider_device_verified": True,
                "provider_loaded": True,
                "done": True,
                "completion_token_count": 260,
                "ollama_compute_verified": True,
                "response_text": "GPU1 verified current packet with enough concrete content for execution.",
            },
            {
                "lane": "gpu0_peer",
                "revision": 1,
                "provider_block_id": "gpu0:001",
                "provider_backend": "ollama",
                "provider_compute_device": "ollama/gpu0-vulkan",
                "provider_model": "qwen3:1.7b",
                "provider_device_verified": True,
                "provider_loaded": True,
                "completion_token_count": 260,
                "ollama_compute_verified": True,
                "gpu0_secondary_schema_valid": True,
                "response_text": "GPU0 verified packet review with structured current packet evidence.",
            },
            {
                "lane": "npu_micro_task_auditor",
                "revision": 0,
                "provider_block_id": "npu:000",
                "provider_execution_performed": True,
                "provider_work_verified": False,
                "npu_peer_evidence_verified": True,
            },
            ]

    owner = _ProposalOwner()
    refs = RuntimeGateProposalCycleAMixin.provider_block_refs_for_revision(owner, 1)
    return refs.get("gpu1") == ["gpu1:001"] and refs.get("gpu0") == ["gpu0:001"] and refs.get("npu") == []


def _generic_write_requires_matching_current_consumed_refs() -> bool:
    with TemporaryDirectory(prefix="provider-shortcut-generic-write-") as tmp:
        root = Path(tmp)
        events: list[dict[str, Any]] = []
        for index in range(3):
            report_path = root / f"generic_{index}.json"
            report_path.write_text(
                json.dumps(
                    {
                        "source_lane": "gpu1_planner",
                        "source_revision": 2,
                        "source_provider_passed": True,
                        "source_provider_execution_performed": True,
                        "source_provider_work_verified": True,
                        "source_provider_block_id": f"current:{index}",
                        "capture_mode": "tool_call",
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            events.append(
                {
                    "event_type": "broker_result",
                    "payload": {
                        "tool": "generic_write",
                        "returncode": 0,
                        "summary": {"passed": True},
                        "outputs": {"json_report": report_path.name},
                    },
                }
            )

        owner = SimpleNamespace(
            repo_root=root,
            gpu1_consumed_generic_write_block_ids=["old:0", "old:1", "old:2"],
            provider_reports=[],
            broker_result_digest=lambda payload: "fallback",
        )
        stale_allowed = generic_write_document_product_eligible(owner, events)
        owner.gpu1_consumed_generic_write_block_ids = [
            "current:0",
            "current:1",
            "current:2",
        ]
        current_allowed = generic_write_document_product_eligible(owner, events)
        return stale_allowed is False and current_allowed is True


def _generic_write_consumption_persisted_in_packet_source(repo_root: Path) -> bool:
    packet_source = (repo_root / "ia_carmine/runtime/heap_gate/gpu1_closure_packet.py").read_text(
        encoding="utf-8", errors="replace"
    )
    proposal_source = (repo_root / "ia_carmine/runtime/heap_gate/proposal_cycle_a.py").read_text(
        encoding="utf-8", errors="replace"
    )
    followup_source = (repo_root / "ia_carmine/runtime/heap_gate/generic_write_followup.py").read_text(
        encoding="utf-8", errors="replace"
    )
    return bool(
        "consumed_generic_write_refs" in packet_source
        and "consumed_generic_write_refs=consumed_generic_write_refs" in proposal_source
        and '"consumed_generic_write_refs": consumed_generic_write_refs' in proposal_source
        and "generic_write_consumed_by_gpu1" in followup_source
    )


def _gpu1_report() -> dict[str, Any]:
    return {
        "lane": "gpu1_planner",
        "provider_block_id": "gpu1:000",
        "provider_model": "qwen2.5-coder:14b",
        "provider_loaded": True,
        "done": True,
        "completion_token_count": 240,
        "ollama_residency_verified": True,
        "ollama_compute_verified": True,
        "response_text": "GPU1 primary packet with enough concrete words for useful evidence.",
    }


def _gpu0_incongruent_report() -> dict[str, Any]:
    return {
        "lane": "gpu0_peer",
        "provider_backend": "ollama",
        "provider_compute_device": "ollama/gpu0-vulkan",
        "provider_block_id": "gpu0:000",
        "provider_model": "qwen3:1.7b",
        "provider_loaded": True,
        "completion_token_count": 220,
        "ollama_residency_verified": True,
        "ollama_compute_verified": True,
        "gpu0_secondary_schema_valid": False,
        "gpu0_effective_decision": "incongruent",
        "checked_block_id": "gpu1:000",
        "response_text": "GPU0 sidecar says incongruent evidence for the current GPU1 packet.",
    }


def _npu_invalid_report() -> dict[str, Any]:
    return {
        "lane": "npu_micro_task_auditor",
        "provider_block_id": "npu:000",
        "provider_compute_device": "openvino/NPU",
        "provider_device_verified": True,
        "npu_peer_evidence_verified": True,
        "npu_peer_followup_required": True,
        "response_text": "NPU sidecar reject until guardrails and validation are concrete.",
    }


def _tool_report(lane: str, output: str) -> dict[str, Any]:
    return {
        "lane": lane,
        "output": output,
        "revision": 0,
        "response_text": f"{lane} sidecar text",
        "tool_calls": [{"id": f"{lane}_generic", "tool": "generic_write", "args": {}}],
    }


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


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


class _FakeRequirementOwner(RuntimeGateToolBrokerMixin):
    def __init__(self, provider_reports: list[dict[str, Any]]) -> None:
        self.provider_reports = provider_reports
        self.args = SimpleNamespace(allow_provider_generation=False)

    def required_requirements_order(self) -> tuple[str, ...]:
        return ("gpu0_provider_peer", "npu_micro_task_auditor")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()
    report = run_smoke(Path(args.repo_root).resolve())
    if args.output:
        output = (Path(args.repo_root) / args.output).resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
