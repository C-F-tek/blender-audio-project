"""RuntimeGateProposalCycleAMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

import os

from ia_carmine._shared.heap_proposal_gate import (
    is_reviewable_target_path,
    is_source_allowed,
    load_allowlist,
    normalize_repo_path,
)
from ia_carmine.runtime.heap_gate.runtime_common import (
    PROPOSAL_ITERATION_MAX_CHARS,
    PROPOSAL_ITERATION_SUMMARY_CHARS,
    Any,
    Path,
    re,
    repo_rel,
    safe_int,
    write_json_report,
    write_text_report,
)
from ia_carmine.runtime.runtime_tool.file_refs.classifier import (
    extract_rejected_validation_refs,
    extract_target_refs,
    extract_validation_refs,
)
from ia_carmine.runtime.heap_gate.proposal_assessment import build_heap_parallel_cycle_assessment
from ia_carmine.runtime.heap_gate.proposal_cycle_artifacts import (
    build_cross_lane_proposal_veto,
    render_proposal_iteration_markdown,
    write_heap_parallel_cycle_artifact,
    write_heap_refinement_task_artifact,
)
from ia_carmine.runtime.heap_gate.pointer_soft_lock import (
    gpu1_closure_decision_from_text,
    runtime_soft_lock_state,
)
from ia_carmine.runtime.heap_gate.gpu1_closure_packet import (
    build_gpu1_closure_decision_packet,
    derive_gpu1_decision,
)
from ia_carmine.runtime.heap_gate.gpu1_tool_result_consumption import gpu1_tool_result_consumption_state
from ia_carmine.runtime.heap_gate.gpu1_one_turn_gate import (
    ONE_TURN_SUMMARY_FIELDS,
    strict_one_turn_gate_passed,
)
from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import normalize_gpu0_decision
from ia_carmine.runtime.heap_gate.generic_write_followup import passed_generic_write_results
from ia_carmine._shared.provider_work_verification import provider_work_status
from ia_carmine.runtime.heap_gate.final_product_delta_protocol import (
    code_file_read_contract,
    exit_decision as proposal_exit_decision,
    final_product_protocol as build_final_product_protocol,
    pointer_action as proposal_pointer_action,
    pointer_field as proposal_pointer_field,
)


class RuntimeGateProposalCycleAMixin:
    def provider_work_verified_for_revision(self, revision: int) -> bool:
        for report in self.provider_reports:
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            lane = str(report.get("lane") or report.get("provider_id") or "")
            status = provider_work_status(lane=lane, report=report)
            if status.get("provider_work_verified"):
                return True
        return False

    def proposal_block_id_for_revision(self, revision: int) -> str:
        return f"{self.stamp}:proposal:{int(revision):03d}"

    def provider_block_refs_for_revision(self, revision: int) -> dict[str, list[str]]:
        refs = {
            "gpu1": [],
            "gpu0": [],
            "npu": [],
            "observed_gpu1": [],
            "observed_gpu0": [],
            "observed_npu": [],
            "observed_provider": [],
        }
        for report in self.provider_reports:
            report_revision = safe_int(report.get("revision"), default=0)
            if report_revision != int(revision):
                continue
            block_id = str(report.get("provider_block_id") or report.get("block_id") or "")
            if not block_id:
                continue
            lane = str(report.get("lane") or "")
            if lane == "gpu1_planner":
                refs["observed_gpu1"].append(block_id)
            elif lane == "gpu0_peer":
                refs["observed_gpu0"].append(block_id)
            elif lane == "npu_micro_task_auditor":
                refs["observed_npu"].append(block_id)
            if lane in {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"}:
                refs["observed_provider"].append(block_id)
            if lane in {"gpu1_planner", "gpu0_peer", "npu_micro_task_auditor"} and not self._verified_provider_ref(
                lane, report
            ):
                continue
            if lane == "gpu1_planner":
                refs["gpu1"].append(block_id)
            elif lane == "gpu0_peer":
                refs["gpu0"].append(block_id)
            elif lane == "npu_micro_task_auditor":
                refs["npu"].append(block_id)
        return refs

    def _verified_provider_ref(self, lane: str, report: dict[str, Any]) -> bool:
        status = provider_work_status(lane=lane, report=report)
        rejection = (
            str(report.get("provider_rejection_reason") or "").strip()
            or str(report.get("product_blocked_reason") or "").strip()
            or str(status.get("provider_rejection_reason") or "").strip()
            or str(status.get("role_rejection_reason") or "").strip()
        )
        return bool(status.get("provider_work_verified") and not rejection)

    def gpu1_output_gate_for_revision(self, revision: int) -> dict[str, Any]:
        issues: list[str] = []
        for report in self.provider_reports:
            if report.get("lane") != "gpu1_planner":
                continue
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            if report.get("response_likely_incomplete"):
                issues.append("gpu1_response_likely_incomplete")
            if report.get("heap_delta_text_required") and not report.get("heap_delta_text_present"):
                issues.append("gpu1_missing_heap_delta_text")
        return {"passed": not issues, "issues": list(dict.fromkeys(issues))}

    def gpu1_one_turn_gate_for_revision(self, revision: int) -> dict[str, Any]:
        for report in reversed(self.provider_reports):
            if str(report.get("lane") or "") != "gpu1_planner":
                continue
            if safe_int(report.get("revision"), default=0) != int(revision):
                continue
            if any(key in report for key in ONE_TURN_SUMMARY_FIELDS):
                return {
                    key: report.get(key)
                    for key in ONE_TURN_SUMMARY_FIELDS
                    if key in report
                }
        return {
            "gpu1_one_turn_runtime_gate_present": False,
            "gpu1_one_turn_runtime_gate_passed": False,
            "gpu1_one_turn_blocker": "gpu1_one_turn_runtime_gate_missing",
            "gpu1_one_turn_errors": ["gpu1_one_turn_runtime_gate_missing"],
        }

    def latest_peer_decision_for_revision(self, lane: str, revision: int) -> dict[str, Any]:
        for report in reversed(self.provider_reports):
            if str(report.get("lane") or "") != lane:
                continue
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            return report
        return {}

    def generic_write_refs_for_revision(self, events: list[dict[str, Any]], revision: int) -> list[str]:
        refs: list[str] = []
        for payload in passed_generic_write_results(events, owner=self):
            if safe_int(payload.get("revision"), default=-1) != int(revision):
                continue
            if str(payload.get("lane") or "") != "gpu1_planner":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            ref = str(
                outputs.get("json_report")
                or payload.get("output")
                or payload.get("path")
                or payload.get("source_file")
                or payload.get("source_provider_block_id")
                or ""
            )
            if ref and ref not in refs:
                refs.append(ref)
        for report in self.provider_reports:
            report_revision = safe_int(report.get("revision"), default=0)
            if report_revision != int(revision):
                continue
            if str(report.get("leader_source") or "") == "generic_write":
                if not self._verified_provider_ref("gpu1_planner", report):
                    continue
                ref = str(report.get("output") or "")
                if ref and ref not in refs:
                    refs.append(ref)
        return refs

    def proposal_consumed_npu_block_ids(
        self, response_text: str, provider_block_refs: dict[str, list[str]]
    ) -> list[str]:
        values: list[str] = []
        for field in ("consumed_npu_block_id", "consumed_npu_block_ids"):
            raw = proposal_pointer_field(response_text, field)
            if not raw:
                continue
            cleaned = raw.strip().strip("[]")
            for item in re.split(r"[,;\s]+", cleaned):
                value = item.strip().strip("'\"")
                if value and value not in values:
                    values.append(value)
        allowed = set(provider_block_refs.get("npu") or [])
        return [item for item in values if item in allowed]

    def proposal_target_files(
        self,
        response_text: str,
        quality: dict[str, Any],
        anchored_sources: list[str],
        revision: int,
    ) -> list[str]:
        return self.proposal_target_contract(
            response_text=response_text,
            quality=quality,
            anchored_sources=anchored_sources,
            revision=revision,
        )["verified_declared_target_files"]

    def proposal_target_contract(
        self,
        *,
        response_text: str,
        quality: dict[str, Any],
        anchored_sources: list[str],
        revision: int,
    ) -> dict[str, Any]:
        declared: list[str] = []
        for report in self.provider_reports:
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            value = report.get("target_files")
            if isinstance(value, list):
                declared.extend(str(item) for item in value)
        declared.extend(extract_target_refs(response_text))
        declared = self._unique_normalized_paths(declared)
        allowlist_candidates = self._unique_existing_candidates(
            [
                *anchored_sources[:12],
                *[
                    str(item)
                    for key in ("verified_source_file_refs", "verified_file_refs")
                    for item in (quality.get(key) if isinstance(quality.get(key), list) else [])
                ],
            ]
        )
        allowed_sources, allowlist_enforced, allowlist_path = load_allowlist(
            os.getenv("PROPOSAL_ALLOWLIST_PATH", "config/allowlist.json"),
            self.repo_root,
        )
        verified: list[str] = []
        rejected: list[dict[str, str]] = []
        for item in declared:
            reason = self._target_rejection_reason(
                item,
                allowed_sources=allowed_sources,
                allowlist_enforced=allowlist_enforced,
            )
            if reason:
                rejected.append({"path": item, "reason": reason})
                continue
            verified.append(item)
        return {
            "declared_target_files": declared,
            "verified_declared_target_files": verified,
            "allowlist_candidate_files": allowlist_candidates,
            "rejected_unverified_refs": rejected,
            "allowlist_enforced": allowlist_enforced,
            "allowlist_path": allowlist_path if allowlist_enforced else "",
        }

    def _target_rejection_reason(
        self,
        value: str,
        *,
        allowed_sources: set[str],
        allowlist_enforced: bool,
    ) -> str:
        normalized = normalize_repo_path(value)
        if not normalized:
            return "empty_target"
        if normalized.startswith(("output/", "indexAI/", "renders/")):
            return "forbidden_generated_target_prefix"
        if not is_reviewable_target_path(normalized):
            return "not_reviewable_target_path"
        if not (self.repo_root / normalized).is_file():
            return "target_file_not_found"
        if allowlist_enforced and not is_source_allowed(normalized, allowed_sources):
            return "target_not_in_source_allowlist"
        return ""

    def _unique_existing_candidates(self, values: list[str]) -> list[str]:
        result: list[str] = []
        for item in self._unique_normalized_paths(values):
            if is_reviewable_target_path(item) and (self.repo_root / item).is_file():
                result.append(item)
        return result

    def _unique_normalized_paths(self, values: list[str]) -> list[str]:
        result: list[str] = []
        for item in values:
            normalized = normalize_repo_path(item)
            if normalized and normalized not in result:
                result.append(normalized)
        return result

    def proposal_validation_commands(self, response_text: str, revision: int) -> dict[str, list[str]]:
        commands: list[str] = []
        rejected: list[str] = []
        for report in self.provider_reports:
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            values = report.get("validation_commands")
            if isinstance(values, list):
                for value in values:
                    text = str(value or "").strip()
                    if text and text not in commands:
                        commands.append(text)
            rejected_values = report.get("rejected_validation_refs")
            if isinstance(rejected_values, list):
                for value in rejected_values:
                    text = str(value or "").strip()
                    if text and text not in rejected:
                        rejected.append(text)
        for value in extract_validation_refs(response_text):
            if value not in commands:
                commands.append(value)
        for value in extract_rejected_validation_refs(response_text):
            if value not in rejected:
                rejected.append(value)
        return {
            "validation_commands": commands,
            "rejected_validation_refs": rejected,
        }

    def proposal_iteration_dir(self) -> Path:
        path = self.runtime_context_dir() / "proposal_iterations"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def heap_parallel_cycle_assessment(
        self,
        revision: int,
        source: str,
        deterministic_reviews: dict[str, Any],
        npu_audit: dict[str, Any],
    ) -> dict[str, Any]:
        return build_heap_parallel_cycle_assessment(
            owner=self,
            revision=revision,
            source=source,
            deterministic_reviews=deterministic_reviews,
            npu_audit=npu_audit,
        )

    def write_proposal_iteration_artifact(
        self,
        revision: int,
        response_text: str,
        quality: dict[str, Any],
        events: list[dict[str, Any]],
        source: str = "gpu1",
    ) -> dict[str, str]:
        from ia_carmine.runtime.heap_gate.proposal_iteration_writer import (
            write_proposal_iteration_artifact,
        )

        return write_proposal_iteration_artifact(
            self,
            revision=revision,
            response_text=response_text,
            quality=quality,
            events=events,
            source=source,
        )
