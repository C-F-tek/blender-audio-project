#!/usr/bin/env python3
"""Smoke test GPU1 recovery scheduling for invalid sidecar pointer reviews."""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import (
    bind_gpu0_secondary_to_gpu1_packet,
    parse_gpu0_secondary_response,
)
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    build_gpu1_closure_decision_packet,
)
from ia_carmine.runtime.heap_gate.provider_lane_hierarchy import (
    context_hierarchy_payload,
    gpu0_max_new_tokens,
)
from ia_carmine.runtime.heap_gate.provider_recovery import (
    maybe_run_provider_recovery,
    provider_recovery_status,
)
from ia_carmine.runtime.heap_gate.provider_universe_abort import (
    block_provider_universe_run,
    provider_universe_abort_reason,
    recoverable_sidecar_failure_reason,
)
from Tools.validation._shared.report_utils import write_json_report, write_text_report


class _Heap:
    paths = SimpleNamespace(events=Path("events.jsonl"))

    def pending_broker_requests(self) -> bool:
        return False


class _Args:
    allow_provider_generation = True
    max_provider_revisions = 2
    max_new_tokens = 900
    gpu0_max_new_tokens = 256
    ollama_num_ctx = 16384
    gpu0_ollama_num_ctx = 2048
    npu_max_context_chars = 8000
    npu_max_prompt_chars = 1200
    npu_max_new_tokens = 384
    keep_alive = "120s"
    field_sources = {
        "gpu0_max_new_tokens": "cli_arg",
        "gpu0_ollama_num_ctx": "cli_arg",
        "ollama_num_ctx": "cli_arg",
        "max_new_tokens": "cli_arg",
        "npu_max_context_chars": "cli_arg",
        "npu_max_prompt_chars": "cli_arg",
        "npu_max_new_tokens": "cli_arg",
        "max_provider_revisions": "cli_arg",
        "keep_alive": "cli_arg",
    }


class _Owner:
    def __init__(self) -> None:
        packet = build_gpu1_closure_decision_packet(
            gpu1_block_id="smoke:gpu1:000",
            gpu1_revision=0,
            gpu1_decision="needs_refine",
            quality_passed=False,
            reject_reasons=["source_refs_missing"],
            evidence_refs=["smoke:guru"],
            response_text="raw gpu1 evidence",
            source="smoke",
        )
        fingerprint = str(packet.get("packet_fingerprint") or "")
        parsed = parse_gpu0_secondary_response(
            (
                '{"gpu0_decision":"incongruent","checked_block_id":"smoke:gpu1:000",'
                '"checked_gpu1_revision":"0","reviewed_packet_fingerprint":"%s",'
                '"incongruence_reasons":["source_refs_missing"],'
                '"required_gpu1_next_action":"GPU1 congruence check"}'
            )
            % fingerprint,
            fallback_block_id="smoke:gpu1:000",
            fallback_revision="0",
            fallback_packet_fingerprint=fingerprint,
        )
        gpu0 = bind_gpu0_secondary_to_gpu1_packet(
            parsed,
            {"gpu1_closure_decision_packet": packet},
        )
        self.args = _Args()
        self.stamp = "smoke"
        self.repo_root = Path(".").resolve()
        self.heap = _Heap()
        self.provider_revision_count = 0
        self.provider_recovery_attempt_count = 0
        self.provider_revision_feedback = ""
        self.provider_universe_blocked_reason = ""
        self.provider_universe_deferred_block_reason = ""
        self.state: dict[str, Any] = {"decisions": [], "product": {}}
        self.decision_count = 0
        self.errors: list[str] = []
        self.provider_reports: list[dict[str, Any]] = [
            {
                "lane": "gpu1_planner",
                "revision": 0,
                "provider_block_id": "smoke:gpu1_provider:000",
                "proposal_block_id": "smoke:gpu1:000",
                "provider_work_verified": True,
                "gpu1_primary_workload_valid": True,
            },
            {
                "lane": "gpu0_peer",
                "revision": 0,
                "provider_block_id": "smoke:gpu0:000",
                "provider_work_verified": True,
                "provider_role_counted": True,
                "provider_execution_performed": True,
                "response_text": "truncated json",
                **gpu0,
            },
            {
                "lane": "npu_micro_task_auditor",
                "revision": 0,
                "provider_block_id": "smoke:npu:000",
                "npu_peer_evidence_verified": True,
                "npu_operational_audit": {
                    "decision": "reject_until_guardrails_and_validation_are_concrete"
                },
                "response_text": "reject_until_guardrails_and_validation_are_concrete",
            },
        ]
        self.published: list[dict[str, Any]] = []
        self.heap_events: list[dict[str, Any]] = []
        self.persisted: list[dict[str, Any]] = []
        self.warnings: list[str] = []
        self._response = "GPU1 recovery raw evidence with consumed_gpu0_block_id=smoke:gpu0:000"

    def latest_proposal_iteration_report(self) -> dict[str, Any]:
        return {
            "revision": 0,
            "block_id": "smoke:gpu1:000",
            "quality_passed": False,
            "reject_reason": "gpu0_secondary_schema_invalid",
        }

    def latest_rejected_proposal_requires_retry(self) -> bool:
        return True

    def build_rejected_proposal_retry_feedback(self) -> str:
        return "REJECTED_GPU1_BLOCK_RETRY_REQUIRED"

    def read_events(self) -> list[dict[str, Any]]:
        return []

    def request_text(self) -> str:
        return "smoke request"

    def request_input_ref_or_tail(self) -> dict[str, Any]:
        text = self.request_text()
        return {
            "source": "provider_recovery_pointer_contract_smoke",
            "tail": text[-4000:],
            "chars": len(text),
            "full_text_in_json": False,
        }

    def response_text_ref_or_tail(
        self,
        text: str,
        *,
        name: str,
        kind: str,
        producer: str,
    ) -> dict[str, Any]:
        return {
            "source": producer,
            "name": name,
            "kind": kind,
            "tail": str(text or "")[-4000:],
            "chars": len(str(text or "")),
            "full_text_in_json": False,
        }

    def provider_response_refs_or_tails(self) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for report in self.provider_reports:
            text = str(report.get("response_text") or "")
            if not text:
                continue
            out.append(
                {
                    "lane": report.get("lane"),
                    "tail": text[-4000:],
                    "chars": len(text),
                    "full_text_in_json": False,
                }
            )
        return out

    def prefixed_text_evidence_fields(
        self,
        prefix: str,
        evidence: dict[str, Any],
    ) -> dict[str, Any]:
        return {
            f"{prefix}_tail": evidence.get("tail", ""),
            f"{prefix}_chars": evidence.get("chars", 0),
            f"{prefix}_source": evidence.get("source", ""),
            f"{prefix}_full_text_in_json": evidence.get("full_text_in_json", False),
        }

    def build_final_response_text(self, _events: list[dict[str, Any]]) -> str:
        return "blocked primary failure"

    def response_source(self) -> str:
        return "smoke"

    def provider_refs(self) -> list[str]:
        return []

    def provider_response_texts(self) -> list[str]:
        return []

    def provider_role_decisions(self) -> list[dict[str, Any]]:
        return []

    def publish_provider_native_tool_calls(self, _round_id: int, _events: list[dict[str, Any]]) -> bool:
        return False

    def run_bridge(self) -> None:
        raise AssertionError("bridge should not run in this smoke")

    def response_text(self) -> str:
        return self._response

    def response_file_reference_quality(self, _text: str) -> dict[str, Any]:
        return {"passed": False}

    def persist_current_gpu1_proposal_iteration(
        self, revision: int, events: list[dict[str, Any]], source: str
    ) -> list[dict[str, Any]]:
        self.persisted.append({"revision": revision, "source": source})
        return events

    def publish_shared_evidence_facts(self, _round_id: int, _events: list[dict[str, Any]]) -> None:
        return None

    def run_provider_teamwork(self, _round_id: int, revision: int = 0) -> None:
        self.provider_reports.append(
            {
                "lane": "gpu1_planner",
                "revision": revision,
                "provider_block_id": f"smoke:gpu1_provider:{revision:03d}",
                "proposal_block_id": f"smoke:gpu1:{revision:03d}",
                "provider_work_verified": True,
                "gpu1_primary_workload_valid": True,
            }
        )

    def publish(self, lane: str, kind: str, payload: dict[str, Any], **kwargs: Any) -> None:
        self.published.append({"lane": lane, "kind": kind, "payload": payload, **kwargs})

    def append_heap_exchange_event(self, event: dict[str, Any]) -> None:
        self.heap_events.append(event)


def run_smoke(repo_root: Path) -> dict[str, Any]:
    owner = _Owner()
    status_before = provider_recovery_status(owner, [])
    abort_reason = provider_universe_abort_reason(
        [{"lane": report.get("lane"), "provider_report": report} for report in owner.provider_reports]
    )
    sidecar_reason = recoverable_sidecar_failure_reason(
        {"lane": "gpu0_peer", "provider_report": owner.provider_reports[1]}
    )
    loaded_only_reason = recoverable_sidecar_failure_reason(
        {
            "lane": "gpu0_peer",
            "provider_report": {
                "lane": "gpu0_peer",
                "status": "failed",
                "provider_loaded": True,
                "gpu0_secondary_schema_valid": False,
                "response_text": "raw prose without compute proof",
            },
        }
    )
    blocked_owner = _Owner()
    blocked_owner.provider_universe_blocked_reason = "blocked_with_reason"
    maybe_run_provider_recovery(blocked_owner, 1, [])
    deferred_block_owner = _Owner()
    block_provider_universe_run(deferred_block_owner, "gpu0_peer_followup_pending", 1, 0)
    primary_block_owner = _Owner()
    block_provider_universe_run(primary_block_owner, "gpu1_primary_workload_invalid", 1, 0)
    events_after = maybe_run_provider_recovery(owner, 1, [])
    status_after = provider_recovery_status(owner, events_after)
    config = context_hierarchy_payload(owner.args, gpu1_ctx=owner.args.ollama_num_ctx)
    repo_root = Path(".").resolve()
    proposal_source = (
        repo_root / "ia_carmine/runtime/heap_gate/proposal_cycle_a.py"
    ).read_text(encoding="utf-8", errors="replace")
    pointer_source = (
        repo_root / "ia_carmine/runtime/external_heap/block_pointer_manifest/cli.py"
    ).read_text(encoding="utf-8", errors="replace")
    checks = {
        "recovery_required_before": status_before.get("provider_recovery_required") is True,
        "gpu0_incongruent_reason_present": "sidecar_incongruent"
        in status_before.get("provider_recovery_reasons", []),
        "npu_pending_reason_present": "npu_followup_pending"
        in status_before.get("provider_recovery_reasons", []),
        "sidecar_scope_mode_packet_review_only": status_before.get("sidecar_scope_mode")
        == "packet_review_only",
        "sidecar_invalid_recorded": status_before.get("sidecar_invalid") is True,
        "sidecar_incongruent_recorded": status_before.get("sidecar_incongruent") is True,
        "gpu1_congruence_check_required": status_before.get("gpu1_congruence_check_required")
        is True,
        "recoverable_sidecar_not_hard_abort": abort_reason == "",
        "recoverable_sidecar_reason_preserved": str(sidecar_reason).startswith(
            "sidecar_incongruent"
        )
        or str(sidecar_reason).startswith("sidecar_invalid"),
        "loaded_only_sidecar_does_not_trigger_recovery": loaded_only_reason == "",
        "blocked_reason_does_not_skip_recoverable_sidecar": blocked_owner.provider_recovery_attempt_count
        == 1,
        "terminal_product_deferred_until_gpu1_recovery": not any(
            item.get("kind") == "product_signal" for item in deferred_block_owner.published
        )
        and deferred_block_owner.provider_universe_blocked_reason == ""
        and deferred_block_owner.provider_universe_deferred_block_reason == "gpu0_peer_followup_pending"
        and any(
            item.get("kind") == "validation_signal"
            and item.get("payload", {}).get("decision")
            == "defer_terminal_block_until_gpu1_recovery"
            for item in deferred_block_owner.published
        ),
        "primary_gpu1_failure_not_deferred_by_sidecar_state": (
            primary_block_owner.provider_universe_blocked_reason
            == "gpu1_primary_workload_invalid"
            and primary_block_owner.provider_universe_deferred_block_reason == ""
            and any(item.get("kind") == "product_signal" for item in primary_block_owner.published)
        ),
        "gpu1_recovery_attempted": owner.provider_recovery_attempt_count == 1,
        "gpu1_recovery_attempted_metric": status_after.get("gpu1_recovery_attempted") is True,
        "gpu1_congruence_check_performed": status_after.get("gpu1_congruence_check_performed")
        is True,
        "gpu1_recovery_revision_persisted": owner.persisted == [
            {"revision": 1, "source": "gpu1_recovery_revision"}
        ],
        "gpu0_pointer_preserved": status_before.get("latest_gpu0_review_target_pointer")
        == "smoke:gpu1:000",
        "gpu0_budget_operator_visible": gpu0_max_new_tokens(owner.args) == 256
        and config["operator_effective_config"]["gpu0.max_new_tokens"]["source"] == "cli_arg",
        "gpu0_ctx_operator_visible": (
            config["operator_effective_config"]["gpu0.ollama_num_ctx"]["effective_value"]
            == 2048
            and config["operator_effective_config"]["gpu0.ollama_num_ctx"]["source"] == "cli_arg"
        ),
        "status_after_still_graph_based": status_after.get("provider_recovery_required") is True,
        "gpu1_recovery_persists_consumed_sidecar_ids": (
            '"consumed_gpu0_block_ids": consumed_gpu0_block_ids' in proposal_source
            and '"consumed_npu_block_ids": consumed_npu_block_ids' in proposal_source
            and '"consumed_provider_block_ids": consumed_provider_block_ids'
            in proposal_source
            and '"consumed_provider_block_ids":' in pointer_source
        ),
    }
    return {
        "schema_version": 1,
        "kind": "provider_recovery_pointer_contract_smoke",
        "repo_root": repo_root.as_posix(),
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": all(checks.values()),
        "checks": checks,
        "status_before": status_before,
        "status_after": status_after,
        "errors": [name for name, passed in checks.items() if not passed],
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Provider Recovery Pointer Contract Smoke", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    for key, value in (report.get("checks") or {}).items():
        lines.append(f"- {key}: `{value}`")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/provider_recovery_pointer_contract_smoke.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/provider_recovery_pointer_contract_smoke.md",
    )
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root)
    write_json_report(report, repo_root / args.output)
    write_text_report(render_markdown(report), repo_root / args.markdown_output)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
