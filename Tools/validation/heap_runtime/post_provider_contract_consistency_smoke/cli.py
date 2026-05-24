#!/usr/bin/env python3
"""Validate post-provider target, validation, workload, context and composer contracts."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
from ia_carmine._shared.live_flow_lanes import merge_provider_statuses, provider_status
from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine.product.heap_final_proposals.artifacts import (
    collect_gpu0_reviews,
    collect_npu_audits,
    list_proposals,
    list_provider_reports,
)
from ia_carmine.product.heap_final_proposals.cli import _proposal_summary
from ia_carmine.product.heap_final_proposals.normalize_final_causality.cli import (
    build_report as build_causality_report,
)
from ia_carmine.runtime.external_heap.block_pointer_manifest.cli import build_pointer_edges
from ia_carmine.runtime.external_heap.revision_context.report import build_report
from ia_carmine.runtime.heap_gate.provider_universe_abort import block_provider_universe_run
from ia_carmine.runtime.heap_gate.proposal_cycle_a import RuntimeGateProposalCycleAMixin
from ia_carmine.runtime.runtime_tool.file_refs.classifier import (
    extract_rejected_validation_refs,
    extract_validation_refs,
)


class _Owner(RuntimeGateProposalCycleAMixin):
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.stamp = "post-provider-smoke"
        self.provider_reports: list[dict[str, Any]] = []


def _make_repo(root: Path) -> None:
    (root / "ia_carmine").mkdir(parents=True, exist_ok=True)
    (root / "ia_carmine" / "README.md").write_text("# ia_carmine\n", encoding="utf-8")
    (root / "Tools" / "validation").mkdir(parents=True, exist_ok=True)
    (root / "Tools" / "validation" / "dispatch.py").write_text("TOOLS = {}\n", encoding="utf-8")


def _target_contract_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    owner = _Owner(repo)
    response = """
## TARGET_FILES
- ia_carmine/README.md
- scripts/analyze.py

## VALIDATION_COMMANDS
python -m doctest ia_carmine/README.md
"""
    contract = owner.proposal_target_contract(
        response_text=response,
        quality={"verified_source_file_refs": ["Tools/validation/dispatch.py"]},
        anchored_sources=["Tools/validation/dispatch.py"],
        revision=0,
    )
    passed = (
        contract["declared_target_files"] == ["ia_carmine/README.md", "scripts/analyze.py"]
        and contract["verified_declared_target_files"] == ["ia_carmine/README.md"]
        and contract["allowlist_candidate_files"] == ["Tools/validation/dispatch.py"]
        and any(item.get("path") == "scripts/analyze.py" for item in contract["rejected_unverified_refs"])
    )
    return passed, contract


def _validation_command_check() -> tuple[bool, dict[str, Any]]:
    command_text = """
## VALIDATION_COMMANDS
- python -m doctest ia_carmine/README.md
"""
    bare_text = """
## VALIDATION_COMMANDS
- ia_carmine/README.md
"""
    commands = extract_validation_refs(command_text)
    bare_commands = extract_validation_refs(bare_text)
    rejected = extract_rejected_validation_refs(bare_text)
    return (
        commands == ["python -m doctest ia_carmine/README.md"]
        and bare_commands == []
        and rejected == ["ia_carmine/README.md"],
        {"commands": commands, "bare_commands": bare_commands, "rejected": rejected},
    )


def _provider_workload_split_check() -> tuple[bool, dict[str, Any]]:
    gpu1_status = provider_work_status(
        lane="gpu1_planner",
        report={
            "provider_device_verified": True,
            "ollama_residency_verified": True,
            "ollama_compute_verified": True,
            "provider_loaded": True,
            "selected_model": "qwen2.5-coder:14b",
            "eval_count": 128,
            "done": True,
            "response_text": "HEAP_DELTA_PROPOSAL with enough useful provider text for a concrete review.",
            "quality_passed": False,
        },
    )
    npu_status = provider_work_status(
        lane="npu_micro_task_auditor",
        report={
            "provider_device_verified": True,
            "provider_compute_device": "openvino/NPU",
            "npu_peer_evidence_verified": True,
            "npu_micro_provider_model_loaded": True,
            "npu_micro_provider_execution_performed": True,
            "npu_device_workload_performed": True,
            "response_text": "NPU audit evidence is available and useful for GPU1 follow-up.",
            "npu_native_tool_loop_error": "openvino_native_tool_loop_timeout",
            "npu_peer_followup_required": True,
        },
    )
    passed = (
        gpu1_status.get("workload_passed") is True
        and gpu1_status.get("semantic_contract_passed") is False
        and gpu1_status.get("provider_requirement_complete") is False
        and npu_status.get("workload_passed") is True
        and npu_status.get("semantic_contract_passed") is False
        and npu_status.get("provider_requirement_complete") is False
    )
    return passed, {"gpu1": gpu1_status, "npu": npu_status}


def _revision_context_check() -> tuple[bool, dict[str, Any]]:
    pointer = {
        "provider_execution_performed": True,
        "edge_count": 4,
        "roles_present": ["gpu1_planner", "npu_auditor"],
        "provider_rejections": [{"provider_id": "gpu0_peer"}],
        "provider_rejection_reasons": ["gpu0_secondary_schema_invalid"],
        "blocks": [
            {"block_id": "gpu1:000", "role": "gpu1_planner", "block_type": "provider_evidence_block"},
            {
                "block_id": "npu:000",
                "role": "npu_auditor",
                "block_type": "audit_block",
                "refines_block_id": "gpu1:000",
            },
        ],
    }
    report = build_report(pointer, {}, {"causal_chain_passed": True})
    return (
        report.get("operational_revision_context") is False
        and report.get("contract_passed") is False
        and report.get("passed") is False,
        report,
    )


def _composer_identity_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    run_dir = repo / "run"
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    proposal_dir.mkdir(parents=True, exist_ok=True)
    proposal = {
        "revision": 0,
        "block_id": "proposal:000",
        "source": "gpu1",
        "quality_passed": True,
        "target_files": ["ia_carmine/README.md"],
        "declared_target_files": ["ia_carmine/README.md"],
        "verified_declared_target_files": ["ia_carmine/README.md"],
        "allowlist_candidate_files": ["Tools/validation/dispatch.py"],
        "rejected_unverified_refs": [{"path": "scripts/analyze.py", "reason": "target_file_not_found"}],
        "validation_commands": ["python -m doctest ia_carmine/README.md"],
        "provider_execution_performed": True,
        "implementation_quality": {"passed": True, "errors": []},
        "proposal_progress": {"passed": True, "errors": []},
        "response_text": "valid proposal",
    }
    (proposal_dir / "heap_proposal_revision_000.json").write_text(
        json.dumps(proposal, indent=2) + "\n",
        encoding="utf-8",
    )
    loaded = list_proposals(run_dir)
    summary = _proposal_summary(loaded[0]) if loaded else {}
    passed = (
        summary.get("block_id") == "proposal:000"
        and summary.get("target_files") == ["ia_carmine/README.md"]
        and summary.get("verified_declared_target_files") == ["ia_carmine/README.md"]
        and summary.get("validation_commands") == ["python -m doctest ia_carmine/README.md"]
        and summary.get("provider_execution_performed") is True
    )
    return passed, summary


def _causality_pointer_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    composer = {
        "startup_manifest": {
            "input_ready_before_heap": True,
            "artifacts": {"tool_catalog_json": "startup/tool_catalog.json"},
        },
        "startup_reconciliation": {"passed": True},
        "provider_report_count": 3,
        "proposal_count": 1,
        "gpu0_review_count": 1,
        "npu_audit_count": 1,
        "product_status": "blocked_with_reason",
        "quality_output_passed": False,
        "accepted_proposal_count": 0,
        "rejected_proposal_count": 1,
        "blocking_issues": ["blocked"],
    }
    pointer = {
        "passed": False,
        "all_pointers_closed": False,
        "open_pointer_count_final": 1,
        "provider_rejections": [{"provider_id": "gpu0_peer"}],
        "provider_rejection_reasons": ["gpu0_secondary_schema_invalid"],
    }
    report = build_causality_report(composer, repo / "composer.json", pointer)
    chain = report.get("causal_chain") if isinstance(report.get("causal_chain"), dict) else {}
    return (
        report.get("causal_chain_passed") is False
        and "external pointer manifest did not pass" in (chain.get("reasons") or [])
        and "pointer manifest has provider rejections" in (chain.get("reasons") or []),
        report,
    )


def _composer_provider_filter_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    run_dir = repo / "provider-filter-run"
    provider_dir = run_dir / "provider_teamwork"
    provider_dir.mkdir(parents=True, exist_ok=True)
    payloads = {
        "gpu1_ollama_provider_probe.json": {"lane": "gpu1_planner", "passed": True, "provider_execution_performed": True, "response_text": "gpu1 production"},
        "gpu0_ollama_vulkan_peer.json": {"lane": "gpu0_peer", "passed": True, "provider_execution_performed": True, "response_text": "gpu0 review"},
        "npu_micro_task_auditor.json": {"lane": "npu_micro_task_auditor", "passed": True, "provider_execution_performed": True, "npu_device_workload": {"performed": True}, "response_text": "npu audit"},
        "provider_launch_manifest.json": {"kind": "provider_launch_manifest", "lane": "orchestrator"},
        "provider_teamwork_leader_packet.json": {"kind": "provider_teamwork_leader_packet", "lane": "gpu1_planner"},
        "provider_runtime_plan.json": {"kind": "provider_runtime_plan", "lane": "orchestrator"},
        "provider_role_coexistence.json": {"kind": "provider_role_coexistence", "lane": "orchestrator"},
        "gpu1_planner_provider_replight.json": {"lane": "gpu1_planner", "replight_mode": True, "replight_passed": True},
    }
    for name, payload in payloads.items():
        (provider_dir / name).write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    reports = list_provider_reports(run_dir)
    gpu0_reviews = collect_gpu0_reviews([], reports)
    npu_audits = collect_npu_audits([], reports)
    detail = {
        "provider_report_count": len(reports),
        "gpu0_review_count": len(gpu0_reviews),
        "npu_audit_count": len(npu_audits),
        "lanes": [item.get("lane") for item in reports],
    }
    return (
        len(reports) == 3
        and len(gpu0_reviews) == 1
        and len(npu_audits) == 1
        and sorted(detail["lanes"]) == ["gpu0_peer", "gpu1_planner", "npu_micro_task_auditor"],
        detail,
    )


def _reconcile_status_namespace_check(repo_root: Path, temp: Path) -> tuple[bool, dict[str, Any]]:
    startup = temp / "startup.json"
    heap = temp / "heap.json"
    output = temp / "reconcile.json"
    markdown = temp / "reconcile.md"
    startup.write_text(
        json.dumps(
            {
                "passed": True,
                "input_ready_before_heap": True,
                "artifacts": {"tool_catalog_json": str(temp / "tool_catalog.json")},
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    heap.write_text(
        json.dumps(
            {
                "product_status": "blocked_with_reason",
                "completed_requirements": [],
                "missing_requirements": [],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "ia_carmine",
            "reconcile_heap_report_with_startup_reload",
            "--repo-root",
            str(repo_root),
            "--startup-manifest",
            str(startup),
            "--heap-report",
            str(heap),
            "--output",
            str(output),
            "--markdown-output",
            str(markdown),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    heap_after = json.loads(heap.read_text(encoding="utf-8"))
    report = json.loads(output.read_text(encoding="utf-8")) if output.exists() else {}
    detail = {
        "returncode": result.returncode,
        "heap_product_status": heap_after.get("product_status"),
        "suggestion": heap_after.get("startup_reconciliation_product_status_suggestion"),
        "report_product_status_preserved": report.get("product_status_preserved"),
        "stderr": result.stderr[-500:],
    }
    return (
        result.returncode == 0
        and heap_after.get("product_status") == "blocked_with_reason"
        and heap_after.get("startup_reconciliation_product_status_suggestion")
        == "blocked_waiting_for_provider_or_proposal",
        detail,
    )


class _AbortGate:
    def __init__(self, repo_root: Path) -> None:
        self.repo_root = repo_root
        self.stamp = "abort-smoke"
        self.errors: list[str] = []
        self.decision_count = 0
        self.candidate_operation_count = 0
        self.provider_universe_blocked_reason = ""
        self.state: dict[str, Any] = {
            "decisions": [],
            "product": {},
            "candidate_operations": [],
        }
        self.events: list[dict[str, Any]] = []
        self.heap = type("Heap", (), {"paths": type("Paths", (), {"events": repo_root / "events.jsonl"})()})()

    def publish(self, source: str, event_type: str, payload: dict[str, Any], **kwargs: Any) -> None:
        self.events.append({"source": source, "event_type": event_type, "payload": payload, **kwargs})

    def request_text(self) -> str:
        return "abort smoke"

    def build_final_response_text(self, _events: list[dict[str, Any]]) -> str:
        return ""

    def read_events(self) -> list[dict[str, Any]]:
        return list(self.events)

    def response_source(self) -> str:
        return ""

    def provider_refs(self) -> list[str]:
        return []

    def provider_response_texts(self) -> list[str]:
        return []

    def provider_role_decisions(self) -> list[str]:
        return []


def _provider_abort_candidate_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    gate = _AbortGate(repo)
    reason = "provider_universe_primary_lane_not_ready:gpu1_planner"
    block_provider_universe_run(gate, reason, round_id=1, revision=0)
    candidate_events = [item for item in gate.events if item.get("event_type") == "candidate_operation"]
    detail = {
        "candidate_operation_count": gate.candidate_operation_count,
        "candidate_operations": gate.state.get("candidate_operations"),
        "candidate_event_count": len(candidate_events),
    }
    return (
        gate.candidate_operation_count > 0
        and bool(gate.state.get("candidate_operations"))
        and len(candidate_events) > 0,
        detail,
    )


def _pointer_self_edge_check() -> tuple[bool, dict[str, Any]]:
    edges = build_pointer_edges(
        [
            {
                "block_id": "proposal:000",
                "previous_block_id": "proposal:000",
                "next_block_id": "proposal:000",
                "refines_block_id": "proposal:000",
                "resume_from_block_id": "proposal:000",
            }
        ]
    )
    return edges == [], {"edges": edges}


def _live_flow_replight_precedence_check(repo: Path) -> tuple[bool, dict[str, Any]]:
    provider_dir = repo / "live-flow-run" / "provider_teamwork"
    provider_dir.mkdir(parents=True, exist_ok=True)
    production = provider_dir / "gpu1_ollama_provider_probe.json"
    replight = provider_dir / "gpu1_planner_provider_replight.json"
    production.write_text(
        json.dumps(
            {
                "lane": "gpu1_planner",
                "provider_model": "qwen2.5-coder:14b",
                "response_text": "production response with real proposal text",
                "provider_compute_device": "ollama/gpu1",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    replight.write_text(
        json.dumps(
            {
                "lane": "gpu1_planner",
                "replight_mode": True,
                "replight_passed": True,
                "provider_loaded": True,
                "response_text": "ok",
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    merged = merge_provider_statuses([], provider_status(provider_dir))
    gpu1 = next((item for item in merged if item.get("lane") == "gpu1_planner"), {})
    detail = {"gpu1": gpu1}
    return (
        str(gpu1.get("output") or "").endswith("gpu1_ollama_provider_probe.json")
        and str(gpu1.get("replight_output") or "").endswith("gpu1_planner_provider_replight.json"),
        detail,
    )


def run_smoke(repo_root: Path) -> dict[str, Any]:
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}
    errors: list[str] = []
    try:
        with tempfile.TemporaryDirectory(prefix="post-provider-contract-") as temp:
            repo = Path(temp)
            _make_repo(repo)
            checks["target_contract_no_anchor_contamination"], details["target_contract"] = _target_contract_check(repo)
            checks["validation_commands_are_commands"], details["validation_commands"] = _validation_command_check()
            checks["provider_workload_semantic_split"], details["provider_workload"] = _provider_workload_split_check()
            checks["external_revision_context_not_passed_when_non_operational"], details["revision_context"] = _revision_context_check()
            checks["composer_preserves_proposal_identity"], details["composer"] = _composer_identity_check(repo)
            checks["causality_requires_pointer_validity"], details["causality"] = _causality_pointer_check(repo)
            checks["composer_filters_non_lane_provider_reports"], details["provider_filter"] = _composer_provider_filter_check(repo)
            checks["reconcile_namespaces_product_status"], details["reconcile"] = _reconcile_status_namespace_check(repo_root, repo)
            checks["abort_publishes_blocked_candidate_operation"], details["abort_candidate"] = _provider_abort_candidate_check(repo)
            checks["pointer_manifest_skips_self_edges"], details["pointer_self_edge"] = _pointer_self_edge_check()
            checks["live_flow_prefers_production_over_replight"], details["live_flow"] = _live_flow_replight_precedence_check(repo)
    except Exception as exc:  # noqa: BLE001
        errors.append(f"{type(exc).__name__}: {exc}")
    errors.extend(name for name, passed in checks.items() if not passed)
    return {
        "schema_version": 1,
        "kind": "post_provider_contract_consistency_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "checks": checks,
        "details": details,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/post_provider_contract_consistency_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    print(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
