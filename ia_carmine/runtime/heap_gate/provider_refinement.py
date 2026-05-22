"""RuntimeGateProviderRefinementMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.pointer_soft_lock import (
    register_soft_lock_extension,
    runtime_soft_lock_state,
    soft_lock_feedback_text,
)
from ia_carmine.runtime.heap_gate.runtime_common import Any


class RuntimeGateProviderRefinementMixin:
    def publish_soft_lock_quorum_signal(
        self,
        round_id: int,
        soft_lock_state: dict[str, Any],
    ) -> None:
        signature = (
            soft_lock_state.get("closure_quorum_status"),
            soft_lock_state.get("soft_lock_closure_owner_decision"),
            soft_lock_state.get("gpu0_closure_agreement"),
            soft_lock_state.get("soft_lock_targeted_refine_used"),
            soft_lock_state.get("open_pointer_count_final"),
        )
        if getattr(self, "_last_soft_lock_quorum_signature", None) == signature:
            return
        self._last_soft_lock_quorum_signature = signature
        self.publish(
            "deterministic",
            "validation_signal",
            {
                "id": f"{self.stamp}:soft_lock_closure_quorum",
                **soft_lock_state,
            },
            target="gpu1",
            correlation_id=f"{self.stamp}:soft-lock-closure-quorum",
            round_id=round_id,
        )
        self.append_heap_exchange_event(
            {
                "kind": "soft_lock_closure_quorum",
                "lane": "deterministic_audit",
                "round": round_id,
                "closure_quorum_status": soft_lock_state.get("closure_quorum_status"),
                "soft_lock_closure_owner_decision": soft_lock_state.get(
                    "soft_lock_closure_owner_decision"
                ),
                "gpu0_closure_agreement": soft_lock_state.get("gpu0_closure_agreement"),
                "npu_closure_advisory": soft_lock_state.get("npu_closure_advisory"),
                "summary": soft_lock_state.get("closure_quorum_reason"),
            }
        )

    def terminal_no_patchable_provider_loop(self) -> dict[str, Any]:
        """Detect repeated fake-path provider output that should stop revisions."""
        report = self.latest_proposal_iteration_report()
        if not report:
            return {}
        try:
            revision = int(report.get("revision") or 0)
        except (TypeError, ValueError):
            revision = 0
        if revision < 1:
            return {}

        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        progress = (
            report.get("proposal_progress")
            if isinstance(report.get("proposal_progress"), dict)
            else {}
        )
        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        response_text = str(report.get("response_text") or "")
        unverified = [
            str(item)
            for item in (
                quality.get("unverified_source_file_refs")
                or quality.get("unverified_file_refs")
                or []
            )
            if str(item).strip()
        ]
        repeated_unverified = [
            str(item)
            for item in (progress.get("repeated_unverified_source_refs") or [])
            if str(item).strip()
        ]
        progress_errors = [
            str(item) for item in (progress.get("errors") or []) if str(item).strip()
        ]
        implementation_errors = [
            str(item) for item in (implementation.get("errors") or []) if str(item).strip()
        ]
        placeholder_hits = [
            str(item)
            for item in (implementation.get("placeholder_hits") or [])
            if str(item).strip()
        ]
        haystack = "\n".join(
            [response_text, *unverified, *repeated_unverified, *progress_errors]
        ).lower()
        fake_path_detected = any(
            marker in haystack
            for marker in (
                "tools/.../real_existing_file.py",
                "tools\\...\\real_existing_file.py",
                "real_existing_file.py",
                "<id-or-empty>",
            )
        )
        repeated = bool(repeated_unverified) or any(
            "similarity=" in item.lower() or "too similar" in item.lower()
            for item in progress_errors
        )
        placeholder = bool(placeholder_hits) or any(
            marker in "\n".join(implementation_errors).lower()
            for marker in ("placeholder", "todo", "stub")
        )
        repeated_unverified_loop = bool(repeated_unverified) and repeated
        if not ((fake_path_detected and (repeated or placeholder)) or repeated_unverified_loop):
            return {}

        reason = (
            "terminal_no_patchable_target: repeated provider output used fake, "
            "placeholder or non-allowlisted source paths after deterministic feedback"
        )
        feedback = "\n".join(
            [
                "EXIT_DECISION=NO_PATCHABLE_TARGET",
                "BLOCKED_NO_VERIFIED_TARGET_REASON=" + reason,
                "Do not request another GPU1 rewrite for this same unresolved candidate.",
                "Preserve the rejected chunk as diagnostic evidence and return to deterministic operator review.",
            ]
        )
        return {
            "terminal_no_patchable_target": True,
            "revision": revision,
            "reason": reason,
            "unverified_source_file_refs": unverified,
            "repeated_unverified_source_refs": repeated_unverified,
            "progress_errors": progress_errors,
            "implementation_errors": implementation_errors,
            "placeholder_hits": placeholder_hits,
            "feedback": feedback,
        }

    def proposal_cycle_requires_refinement(self, text: str, events: list[dict[str, Any]]) -> bool:
        """Return True when the current heap proposal block still needs another GPU1 pass."""
        if not self.detailed_output_expected():
            return False
        if self.latest_rejected_proposal_requires_retry():
            return True
        if not str(text or "").strip():
            return True
        # Raw response quality still matters, but the accepted/rejected proposal
        # artifact is the authoritative same-heap decision because it includes
        # GPU0 review, NPU audit, progress checks and the parallel-cycle verdict.
        if not self.quality_output_passed(text, events):
            return True
        if self.proposal_iteration_artifacts() and not self.latest_proposal_quality_passed():
            return True
        return False

    def persist_current_gpu1_proposal_iteration(
        self,
        revision: int,
        events: list[dict[str, Any]],
        source: str,
    ) -> list[dict[str, Any]]:
        """Persist the current GPU1 response as a proposal block before quality exit."""
        text = self.response_text()
        if not text:
            return events
        self.write_proposal_iteration_artifact(
            revision,
            text,
            self.response_file_reference_quality(text),
            events,
            source=source,
        )
        updated_events = self.read_events()
        self.publish_shared_evidence_facts(revision, updated_events)
        return updated_events

    def latest_no_patchable_target_exit_valid(self) -> bool:
        report = self.latest_proposal_iteration_report()
        if not report:
            return False
        exit_decision = str(report.get("exit_decision") or "").strip().upper()
        response_text = str(report.get("response_text") or "")
        quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        return exit_decision == "NO_PATCHABLE_TARGET" and (
            "BLOCKED_NO_VERIFIED_TARGET_REASON" in response_text
            or quality.get("no_patchable_target_declared") is True
        )

    def latest_rejected_proposal_requires_retry(self) -> bool:
        report = self.latest_proposal_iteration_report()
        if not report or report.get("quality_passed") is not False:
            return False
        if self.latest_no_patchable_target_exit_valid():
            return False
        if str(getattr(self, "provider_universe_blocked_reason", "") or "").strip():
            return False
        return True

    def build_rejected_proposal_retry_feedback(self) -> str:
        report = self.latest_proposal_iteration_report()
        if not report:
            return ""

        def compact(value: Any, limit: int = 500) -> str:
            text = str(value or "").replace("\n", " | ").strip()
            return text[:limit]

        file_quality = (
            report.get("response_file_reference_quality")
            if isinstance(report.get("response_file_reference_quality"), dict)
            else {}
        )
        implementation = (
            report.get("implementation_quality")
            if isinstance(report.get("implementation_quality"), dict)
            else {}
        )
        lines = [
            "REJECTED_GPU1_BLOCK_RETRY_REQUIRED:",
            f"- rejected_block_id={report.get('block_id') or ''}",
            f"- rejected_revision={report.get('revision')}",
            "- validator_action=generate_new_gpu1_revision_for_same_block",
            "- Rewrite the block; do not repeat rejected TARGET_FILES, diff headers or prose.",
            f"- response_file_reference_quality={compact(file_quality)}",
            f"- implementation_quality_errors={compact(implementation.get('errors'))}",
            f"- gpu0_decision={compact(report.get('gpu0_review'))}",
            f"- npu_decision={compact(report.get('npu_micro_task_piece'))}",
        ]
        if report.get("reject_reason"):
            lines.append(f"- reject_reason={compact(report.get('reject_reason'))}")
        return "\n".join(lines)

    def maybe_run_provider_quality_revisions(
        self, round_id: int, events: list[dict[str, Any]]
    ) -> list[dict[str, Any]]:
        while (
            self.detailed_output_expected()
            and self.proposal_cycle_requires_refinement(self.response_text(), events)
        ):
            terminal = self.terminal_no_patchable_provider_loop()
            if terminal:
                self.provider_revision_feedback = str(terminal.get("feedback") or "")
                self.publish(
                    "deterministic",
                    "validation_signal",
                    {
                        "id": f"{self.stamp}:provider_revision_terminal_no_patchable",
                        **terminal,
                    },
                    target="gpu1",
                    correlation_id=f"{self.stamp}:terminal-no-patchable",
                    round_id=round_id,
                )
                self.append_heap_exchange_event(
                    {
                        "kind": "provider_revision_terminal_no_patchable_target",
                        "lane": "deterministic_audit",
                        "round": round_id,
                        "revision": terminal.get("revision"),
                        "summary": terminal.get("reason"),
                    }
                )
                break
            if self.runtime_soft_close_reached():
                soft_lock_state = register_soft_lock_extension(self)
                self._last_soft_lock_state = soft_lock_state
                self.publish_soft_lock_quorum_signal(round_id, soft_lock_state)
                quorum_status = str(soft_lock_state.get("closure_quorum_status") or "")
                if quorum_status in {
                    "ready_to_close",
                    "blocked_continuation_ready",
                    "blocked_with_reason",
                }:
                    break
                if quorum_status == "targeted_refine_allowed":
                    if bool(getattr(self, "soft_lock_targeted_refine_used", False)):
                        break
                    self.soft_lock_targeted_refine_used = True
                    self.skip_npu_on_soft_lock_targeted_refine = True
                    soft_lock_state = runtime_soft_lock_state(self, events)
                    self._last_soft_lock_state = soft_lock_state
                    self.publish_soft_lock_quorum_signal(round_id, soft_lock_state)
                    self.provider_revision_feedback = "\n\n".join(
                        part
                        for part in (
                            self.provider_revision_feedback.strip(),
                            "SOFT_LOCK_TARGETED_REFINE: GPU0 veto/refine signal allows one focused GPU1 revision only. Do not relaunch broad exploration and do not ask NPU to close.",
                            soft_lock_feedback_text(soft_lock_state),
                        )
                        if part
                    )
                if "SOFT_CLOSE_SIGNAL:" not in self.provider_revision_feedback:
                    self.provider_revision_feedback = "\n\n".join(
                        part
                        for part in (
                            self.provider_revision_feedback.strip(),
                            (
                                "SOFT_CLOSE_SIGNAL: the time counter asks for coherent "
                                "closure, but it is not a hard cutoff. Continue pointer "
                                "propagation/refinement unless the heap has ready product "
                                "evidence or EXIT_DECISION=NO_PATCHABLE_TARGET."
                            ),
                            soft_lock_feedback_text(soft_lock_state),
                        )
                        if part
                    )
                else:
                    self.provider_revision_feedback = "\n\n".join(
                        part
                        for part in (
                            self.provider_revision_feedback.strip(),
                            (
                                "SOFT_LOCK_EXTENSION: still closing open pointers; "
                                f"open_pointer_count={soft_lock_state.get('open_pointer_count_final', 0)}."
                            ),
                        )
                        if part
                    )
            self.provider_revision_count += 1
            previous_veto_feedback = self.provider_revision_feedback.strip()
            retry_feedback = self.build_rejected_proposal_retry_feedback()
            quality_feedback = self.build_quality_failure_feedback(self.response_text(), events)
            self.provider_revision_feedback = "\n\n".join(
                part for part in (previous_veto_feedback, retry_feedback, quality_feedback) if part
            )
            self.publish(
                "deterministic",
                "validation_signal",
                {
                    "id": f"{self.stamp}:product_quality_failure:{self.provider_revision_count}",
                    "revision": self.provider_revision_count,
                    "retry_required": True,
                    "rejected_proposal": self.latest_proposal_iteration_report(),
                    "feedback": self.provider_revision_feedback,
                    "file_quality": self.response_file_reference_quality(self.response_text()),
                },
                target="gpu1",
                correlation_id=f"{self.stamp}:quality-revision:{self.provider_revision_count}",
                round_id=round_id,
            )
            self.append_heap_exchange_event(
                {
                    "kind": "product_quality_failure",
                    "lane": "deterministic_audit",
                    "round": round_id,
                    "revision": self.provider_revision_count,
                    "summary": self.provider_revision_feedback[:500],
                }
            )
            self.run_provider_teamwork(round_id, revision=self.provider_revision_count)
            if self.provider_universe_blocked_reason:
                return self.read_events()
            events = self.read_events()
            if self.publish_provider_native_tool_calls(round_id, events):
                if self.heap.pending_broker_requests():
                    self.run_bridge()
                events = self.read_events()
                self.publish_shared_evidence_facts(round_id, events)
                tool_lines = self.tool_evidence_lines(events, max_items=12)
                if tool_lines:
                    self.provider_revision_feedback = "\n\n".join(
                        part
                        for part in (
                            self.provider_revision_feedback.strip(),
                            "BROKER EVIDENCE FROM PROVIDER TOOL_CALLS:\n"
                            + "\n".join(tool_lines),
                        )
                        if part
                    )
            revised_text = self.response_text()
            revised_quality = self.response_file_reference_quality(revised_text)
            if revised_text:
                self.write_proposal_iteration_artifact(
                    self.provider_revision_count,
                    revised_text,
                    revised_quality,
                    events,
                    source="gpu1_revision",
                )
            self.publish_shared_evidence_facts(round_id, events)
        return events
