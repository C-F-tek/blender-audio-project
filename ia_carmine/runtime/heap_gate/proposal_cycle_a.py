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
from ia_carmine.runtime.heap_gate.gpu0_secondary_decision import normalize_gpu0_decision
from ia_carmine._shared.provider_work_verification import provider_work_status


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
        refs = {"gpu1": [], "gpu0": [], "npu": []}
        for report in self.provider_reports:
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            block_id = str(report.get("provider_block_id") or report.get("block_id") or "")
            if not block_id:
                continue
            lane = str(report.get("lane") or "")
            if lane == "gpu1_planner":
                refs["gpu1"].append(block_id)
            elif lane == "gpu0_peer":
                refs["gpu0"].append(block_id)
            elif lane == "npu_micro_task_auditor":
                refs["npu"].append(block_id)
        if int(revision) > 0 and not refs["npu"]:
            for report in reversed(self.provider_reports):
                if report.get("lane") != "npu_micro_task_auditor":
                    continue
                try:
                    report_revision = int(report.get("revision") or 0)
                except (TypeError, ValueError):
                    report_revision = 0
                if report_revision >= int(revision):
                    continue
                if not (report.get("passed") and report.get("operational_provider_activity")):
                    continue
                block_id = str(report.get("provider_block_id") or report.get("block_id") or "")
                if block_id:
                    refs["npu"].append(block_id)
                    break
        return refs

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

    def proposal_pointer_action(self, response_text: str, quality_passed: bool) -> str:
        match = re.search(r"POINTER_ACTION\s*=\s*([A-Z_]+)", response_text or "")
        if match:
            return match.group(1)
        if "EXIT_DECISION=NO_PATCHABLE_TARGET" in (response_text or ""):
            return "NO_PATCHABLE_TARGET"
        return "STAY_FORWARD" if quality_passed else "BACKTRACK_PROPAGATE"

    def proposal_exit_decision(self, response_text: str, target_files: list[str]) -> str:
        match = re.search(r"EXIT_DECISION\s*=\s*([A-Z_]+)", response_text or "")
        if match:
            return match.group(1)
        if target_files:
            return "PATCHABLE_TARGET"
        return "NO_PATCHABLE_TARGET"

    def proposal_pointer_field(self, response_text: str, field_name: str) -> str:
        pattern = rf"(?im)^\s*-?\s*{re.escape(field_name)}\s*=\s*([^\n\r]+)"
        match = re.search(pattern, response_text or "")
        if match:
            return match.group(1).strip()
        pattern = rf"(?im)^\s*{re.escape(field_name)}\s*:\s*([^\n\r]+)"
        match = re.search(pattern, response_text or "")
        return match.group(1).strip() if match else ""

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
        for event in events:
            payload = event.get("payload") if isinstance(event.get("payload"), dict) else event
            text = " ".join(
                str(payload.get(key) or "")
                for key in ("kind", "tool", "tool_name", "output", "path", "source_file")
            )
            if "generic_write" not in text:
                continue
            ref = str(payload.get("output") or payload.get("path") or payload.get("source_file") or "")
            if ref and ref not in refs:
                refs.append(ref)
        for report in self.provider_reports:
            try:
                report_revision = int(report.get("revision") or 0)
            except (TypeError, ValueError):
                report_revision = 0
            if report_revision != int(revision):
                continue
            if str(report.get("leader_source") or "") == "generic_write":
                ref = str(report.get("output") or "")
                if ref and ref not in refs:
                    refs.append(ref)
        return refs

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
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_proposal_revision_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        previous_report = self.latest_proposal_iteration_report()
        previous = self.latest_proposal_iteration_block(max_chars=PROPOSAL_ITERATION_SUMMARY_CHARS)
        block_id = self.proposal_block_id_for_revision(revision)
        previous_block_id = str(previous_report.get("block_id") or "") if previous_report else ""
        anchored_sources = self.real_source_file_candidates(events, limit=20)
        deterministic_reviews = self.deterministic_lane_reviews(response_text, quality, events)
        implementation_quality = (
            deterministic_reviews.get("implementation_quality")
            if isinstance(deterministic_reviews.get("implementation_quality"), dict)
            else {}
        )
        proposal_progress = self.proposal_revision_progress_report(response_text, quality)
        npu_audit = self.npu_workload_audit_report()
        parallel_cycle = self.heap_parallel_cycle_assessment(
            revision=revision,
            source=source,
            deterministic_reviews=deterministic_reviews,
            npu_audit=npu_audit,
        )
        write_heap_parallel_cycle_artifact(self, revision, parallel_cycle)
        cross_lane_veto = build_cross_lane_proposal_veto(
            self,
            response_text=response_text,
            implementation_quality=implementation_quality,
            proposal_progress=proposal_progress,
            deterministic_reviews=deterministic_reviews,
            npu_audit=npu_audit,
            parallel_cycle=parallel_cycle,
            revision=revision,
        )
        if cross_lane_veto.get("vetoed"):
            self.provider_revision_feedback = str(cross_lane_veto.get("refinement_prompt") or "")
            write_heap_refinement_task_artifact(self, revision, cross_lane_veto)
        provider_block_refs = self.provider_block_refs_for_revision(revision)
        gpu1_output_gate = self.gpu1_output_gate_for_revision(revision)
        linked_provider_block_gate = {
            "gpu1_block_refs": provider_block_refs["gpu1"],
            "gpu0_review_block_refs": provider_block_refs["gpu0"],
            "npu_audit_block_refs": provider_block_refs["npu"],
            "passed": bool(provider_block_refs["gpu1"] and provider_block_refs["gpu0"] and provider_block_refs["npu"]),
        }
        target_contract = self.proposal_target_contract(
            response_text=response_text,
            quality=quality,
            anchored_sources=anchored_sources,
            revision=revision,
        )
        target_files = target_contract["verified_declared_target_files"]
        validation_commands = self.proposal_validation_commands(response_text, revision)
        previous_gpu0_report = (
            self.latest_peer_decision_for_revision("gpu0_peer", int(revision) - 1)
            if int(revision) > 0
            else {}
        )
        previous_gpu0_decision = normalize_gpu0_decision(
            previous_gpu0_report.get("gpu0_effective_decision")
            or previous_gpu0_report.get("gpu0_decision")
            or previous_gpu0_report.get("role_decision")
            or ""
        )
        previous_gpu0_block_id = str(
            previous_gpu0_report.get("provider_block_id")
            or previous_gpu0_report.get("block_id")
            or ""
        )
        previous_gpu0_requires_refine = previous_gpu0_decision in {
            "veto",
            "refine_required",
            "incongruent",
        }
        declared_refines_block_id = self.proposal_pointer_field(
            response_text, "refines_block_id"
        )
        declared_consumed_gpu0_block_id = self.proposal_pointer_field(
            response_text, "consumed_gpu0_block_id"
        )
        missing_link_reasons: list[str] = []
        if not provider_block_refs["gpu1"]:
            missing_link_reasons.append("missing linked GPU1 provider block")
        if not provider_block_refs["gpu0"]:
            missing_link_reasons.append("missing linked GPU0 review/refinement block")
        if not provider_block_refs["npu"]:
            missing_link_reasons.append("missing linked NPU audit block")
        quality_passed = bool(
            quality.get("passed")
            and implementation_quality.get("passed")
            and proposal_progress.get("passed")
            and parallel_cycle.get("passed")
            and linked_provider_block_gate["passed"]
            and gpu1_output_gate["passed"]
            and not cross_lane_veto.get("vetoed")
        )
        pointer_action = self.proposal_pointer_action(response_text, quality_passed)
        exit_decision = self.proposal_exit_decision(response_text, target_files)
        reject_reasons = [
            *[str(item) for item in cross_lane_veto.get("reasons", [])],
            *missing_link_reasons,
            *[str(item) for item in gpu1_output_gate.get("issues", [])],
        ]
        continuity_errors: list[str] = []
        if previous_gpu0_requires_refine:
            if not declared_refines_block_id or declared_refines_block_id != previous_block_id:
                continuity_errors.append("gpu1_refine_not_linked_to_gpu0_veto")
            if not declared_consumed_gpu0_block_id or declared_consumed_gpu0_block_id != previous_gpu0_block_id:
                continuity_errors.append("gpu1_refine_missing_consumed_gpu0_block_id")
        if continuity_errors:
            reject_reasons.extend(continuity_errors)
            quality_passed = False
            pointer_action = self.proposal_pointer_action(response_text, quality_passed)
            exit_decision = self.proposal_exit_decision(response_text, target_files)
        soft_lock_state = getattr(self, "_last_soft_lock_state", {}) or {}
        if getattr(self, "runtime_soft_close_reached", lambda: False)():
            soft_lock_state = runtime_soft_lock_state(self, events)
        closure_owner_decision = derive_gpu1_decision(
            quality_passed=quality_passed,
            exit_decision=exit_decision,
            pointer_action=pointer_action,
            reject_reasons=[str(item) for item in reject_reasons if str(item).strip()],
            response_text=response_text,
        )
        closure_owner_decision = closure_owner_decision or gpu1_closure_decision_from_text(
            response_text,
            {
                "quality_passed": quality_passed,
                "exit_decision": exit_decision,
                "reject_reason": "; ".join(dict.fromkeys(item for item in reject_reasons if item)),
            },
        )
        evidence_refs = [
            *provider_block_refs["gpu1"],
            *self.broker_output_refs(events),
            *self.code_execution_matrix_reports(events),
        ]
        generic_write_refs = self.generic_write_refs_for_revision(events, revision)
        gpu1_packet = build_gpu1_closure_decision_packet(
            gpu1_block_id=block_id,
            gpu1_revision=revision,
            gpu1_decision=closure_owner_decision,
            target_files=target_files,
            quality_passed=quality_passed,
            reject_reasons=[str(item) for item in reject_reasons if str(item).strip()],
            evidence_refs=evidence_refs,
            generic_write_refs=generic_write_refs,
            exit_decision=exit_decision,
            pointer_action=pointer_action,
            refines_block_id=declared_refines_block_id,
            consumed_gpu0_block_id=declared_consumed_gpu0_block_id,
            consumed_gpu0_block_ids=(
                [declared_consumed_gpu0_block_id] if declared_consumed_gpu0_block_id else []
            ),
            consumed_npu_block_ids=[],
            response_text=response_text,
            source="proposal_cycle_a",
        )
        self.current_gpu1_closure_decision_packet = gpu1_packet
        clipped = (response_text or "")[:PROPOSAL_ITERATION_MAX_CHARS]
        data = {
            "schema_version": 1,
            "kind": "heap_proposal_iteration",
            "block_id": block_id,
            "block_type": "proposal_chunk",
            "stamp": self.stamp,
            "revision": revision,
            "source": source,
            "provider_execution_performed": self.provider_work_verified_for_revision(revision),
            "previous_block_id": previous_block_id,
            "next_block_id": "",
            "refines_block_id": declared_refines_block_id,
            "resume_from_block_id": previous_block_id or block_id,
            "pointer_action": pointer_action,
            "declared_target_files": target_contract["declared_target_files"],
            "verified_declared_target_files": target_contract["verified_declared_target_files"],
            "allowlist_candidate_files": target_contract["allowlist_candidate_files"],
            "rejected_unverified_refs": target_contract["rejected_unverified_refs"],
            "validation_commands": validation_commands["validation_commands"],
            "rejected_validation_refs": validation_commands["rejected_validation_refs"],
            "target_contract": target_contract,
            "target_files": target_files,
            "exit_decision": exit_decision,
            "gpu1_closure_decision_packet": gpu1_packet,
            "gpu1_decision": gpu1_packet.get("gpu1_decision"),
            "required_refines_block_id": previous_block_id if previous_gpu0_requires_refine else "",
            "required_consumed_gpu0_block_id": previous_gpu0_block_id if previous_gpu0_requires_refine else "",
            "consumed_gpu0_block_id": declared_consumed_gpu0_block_id,
            "consumed_gpu0_block_ids": (
                [declared_consumed_gpu0_block_id] if declared_consumed_gpu0_block_id else []
            ),
            "gpu1_refine_continuity": {
                "required": previous_gpu0_requires_refine,
                "passed": not continuity_errors,
                "errors": continuity_errors,
                "previous_gpu1_block_id": previous_block_id,
                "previous_gpu0_block_id": previous_gpu0_block_id,
                "previous_gpu0_decision": previous_gpu0_decision,
                "declared_refines_block_id": declared_refines_block_id,
                "declared_consumed_gpu0_block_id": declared_consumed_gpu0_block_id,
            },
            "gpu1_block_ref": provider_block_refs["gpu1"][0] if provider_block_refs["gpu1"] else "",
            "gpu0_review_block_refs": provider_block_refs["gpu0"],
            "npu_audit_block_refs": provider_block_refs["npu"],
            "broker_result_refs": self.broker_output_refs(events),
            "matrix_report_refs": self.code_execution_matrix_reports(events),
            "generic_write_refs": generic_write_refs,
            "linked_provider_block_gate": linked_provider_block_gate,
            "gpu1_output_gate": gpu1_output_gate,
            "quality_passed": quality_passed,
            "response_file_reference_quality": quality,
            "implementation_quality": implementation_quality,
            "proposal_progress": proposal_progress,
            "gpu0_review": deterministic_reviews.get("gpu0_review"),
            "npu_micro_task_piece": deterministic_reviews.get("npu_micro_task_piece"),
            "npu_workload_audit": npu_audit,
            "parallel_cycle": parallel_cycle,
            "cross_lane_veto": cross_lane_veto,
            "accepted": quality_passed,
            "reject_reason": "; ".join(dict.fromkeys(item for item in reject_reasons if item)),
            "soft_lock_state": soft_lock_state.get("soft_lock_state"),
            "soft_lock_closure_owner_decision": closure_owner_decision,
            "gpu0_closure_agreement": soft_lock_state.get("gpu0_closure_agreement"),
            "npu_closure_advisory": soft_lock_state.get("npu_closure_advisory"),
            "cpu_closure_validation": soft_lock_state.get("cpu_closure_validation"),
            "closure_quorum_status": soft_lock_state.get("closure_quorum_status"),
            "closure_quorum_reason": soft_lock_state.get("closure_quorum_reason"),
            "soft_lock_targeted_refine_used": soft_lock_state.get(
                "soft_lock_targeted_refine_used", False
            ),
            "anchored_source_candidates": anchored_sources,
            "previous_iteration_available": bool(previous),
            "gpu1_free_text_evidence": response_text or "",
            "gpu1_free_text_evidence_chars": len(response_text or ""),
            "gpu1_free_text_evidence_sha256": gpu1_packet.get("response_text_sha256") or "",
            "gpu1_free_text_evidence_visible_even_when_invalid": True,
            "response_text": clipped,
        }
        write_json_report(data, json_path)
        md = render_proposal_iteration_markdown(
            revision=revision,
            block_id=block_id,
            source=source,
            quality_passed=quality_passed,
            pointer_action=pointer_action,
            exit_decision=exit_decision,
            previous_block_id=previous_block_id,
            data=data,
            provider_block_refs=provider_block_refs,
            deterministic_reviews=deterministic_reviews,
            implementation_quality=implementation_quality,
            proposal_progress=proposal_progress,
            npu_audit=npu_audit,
            parallel_cycle=parallel_cycle,
            cross_lane_veto=cross_lane_veto,
            anchored_sources=anchored_sources,
            clipped=clipped,
        )
        write_text_report(md, md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "proposal_iteration",
                "lane": source,
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "block_id": block_id,
                "previous_block_id": previous_block_id,
                "refines_block_id": data["refines_block_id"],
                "resume_from_block_id": data["resume_from_block_id"],
                "pointer_action": pointer_action,
                "target_files": target_files,
                "quality_passed": quality_passed,
                "proposal_progress_passed": bool(proposal_progress.get("passed")),
                "npu_workload_performed": bool(npu_audit.get("performed")),
                "summary": f"provider proposal revision {revision} persisted as reusable heap chunk",
            }
        )
        return refs
