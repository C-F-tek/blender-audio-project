"""RuntimeGateProposalCycleAMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    PROPOSAL_ITERATION_MAX_CHARS,
    PROPOSAL_ITERATION_SUMMARY_CHARS,
    Any,
    Path,
    re,
    repo_rel,
    write_json_report,
    write_text_report,
)
from Tools.ai.heap_gate.proposal_assessment import build_heap_parallel_cycle_assessment
from Tools.ai.heap_gate.proposal_prompt import build_refinement_prompt


class RuntimeGateProposalCycleAMixin:
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

    def write_heap_parallel_cycle_artifact(
        self, revision: int, assessment: dict[str, Any]
    ) -> dict[str, str]:
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_parallel_cycle_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        write_json_report(assessment, json_path)
        md_lines = [
            "# Heap Parallel Cycle Assessment",
            "",
            f"- Revision: `{revision}`",
            f"- Passed: `{assessment.get('passed')}`",
            f"- GPU1 present: `{assessment.get('gpu1_present')}`",
            f"- GPU0 present: `{assessment.get('gpu0_present')}`",
            f"- NPU present: `{assessment.get('npu_present')}`",
            f"- NPU workload ok: `{assessment.get('npu_workload_ok')}`",
            "",
            "## Missing lanes",
            "",
            *[f"- `{item}`" for item in assessment.get("missing_lanes", [])],
            "",
            "## Provider report lanes",
            "",
            *[f"- `{item}`" for item in assessment.get("provider_report_lanes", [])],
            "",
        ]
        write_text_report("\n".join(md_lines), md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "heap_parallel_cycle_assessment",
                "lane": "arbiter",
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "passed": bool(assessment.get("passed")),
                "summary": "same-heap multi-lane participation assessed before proposal acceptance",
            }
        )
        return refs

    def cross_lane_proposal_veto(
        self,
        response_text: str,
        implementation_quality: dict[str, Any],
        proposal_progress: dict[str, Any],
        deterministic_reviews: dict[str, Any],
        npu_audit: dict[str, Any],
        parallel_cycle: dict[str, Any],
        revision: int,
    ) -> dict[str, Any]:
        reasons: list[str] = []
        gpu0_review = deterministic_reviews.get("gpu0_review")
        npu_piece = deterministic_reviews.get("npu_micro_task_piece")
        placeholder_hits = (
            implementation_quality.get("placeholder_hits")
            if isinstance(implementation_quality, dict)
            else []
        )
        impl_errors = (
            implementation_quality.get("errors") if isinstance(implementation_quality, dict) else []
        )
        progress_errors = (
            proposal_progress.get("errors") if isinstance(proposal_progress, dict) else []
        )

        combined_gpu0 = "\n".join(str(item) for item in (gpu0_review or []))
        combined_npu = "\n".join(str(item) for item in (npu_piece or []))
        combined_response = str(response_text or "")

        if placeholder_hits:
            reasons.append(f"implementation_quality.placeholder_hits={placeholder_hits}")
        if impl_errors:
            reasons.append(f"implementation_quality.errors={impl_errors}")
        if progress_errors:
            reasons.append(f"proposal_progress.errors={progress_errors}")
        if parallel_cycle.get("passed") is not True:
            reasons.append(f"parallel_cycle_missing_lanes={parallel_cycle.get('missing_lanes')}")
        if re.search(
            r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b",
            combined_gpu0,
            re.IGNORECASE,
        ):
            reasons.append("GPU0 review contains placeholder/stub/TODO signal")
        if re.search(
            r"reject|reject_until|rifiut|non soddisfacente|non accett",
            combined_gpu0,
            re.IGNORECASE,
        ):
            reasons.append("GPU0 review contains reject signal")
        if re.search(
            r"placeholder|stub|todo_or_placeholder|\bTODO\b|\bFIXME\b",
            combined_npu,
            re.IGNORECASE,
        ):
            reasons.append("NPU micro-task contains placeholder/stub/TODO signal")
        if re.search(
            r"reject|reject_until|rifiut|non soddisfacente|non accett",
            combined_npu,
            re.IGNORECASE,
        ):
            reasons.append("NPU micro-task contains reject signal")
        if re.search(
            r"\bTODO\b|\bFIXME\b|placeholder|stub|da implementare",
            combined_response,
            re.IGNORECASE,
        ):
            reasons.append("response_text contains TODO/FIXME/placeholder/stub marker")
        if npu_audit and npu_audit.get("requested") and not npu_audit.get("performed"):
            reasons.append("NPU workload requested but not performed")

        reasons = list(dict.fromkeys(str(item) for item in reasons if str(item).strip()))
        vetoed = bool(reasons)
        refinement_prompt = ""
        if vetoed:
            source_candidates = self.real_source_file_candidates(self.read_events(), limit=24)
            refinement_prompt = build_refinement_prompt(
                revision=revision,
                reasons=reasons,
                source_candidates=source_candidates,
            )
        return {
            "vetoed": vetoed,
            "reasons": reasons,
            "gpu0_review": gpu0_review or [],
            "npu_micro_task_piece": npu_piece or [],
            "npu_workload_audit": npu_audit or {},
            "parallel_cycle": parallel_cycle,
            "refinement_prompt": refinement_prompt,
        }

    def write_heap_refinement_task_artifact(
        self, revision: int, veto: dict[str, Any]
    ) -> dict[str, str]:
        out_dir = self.proposal_iteration_dir()
        basename = f"heap_refinement_task_after_revision_{revision:03d}"
        json_path = out_dir / f"{basename}.json"
        md_path = out_dir / f"{basename}.md"
        payload = {
            "schema_version": 1,
            "kind": "heap_refinement_task",
            "stamp": self.stamp,
            "after_revision": revision,
            "vetoed": bool(veto.get("vetoed")),
            "reasons": veto.get("reasons", []),
            "parallel_cycle": veto.get("parallel_cycle", {}),
            "refinement_prompt": veto.get("refinement_prompt", ""),
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
        }
        write_json_report(payload, json_path)
        md_lines = [
            "# Heap Refinement Task",
            "",
            f"- After revision: `{revision}`",
            f"- Vetoed: `{bool(veto.get('vetoed'))}`",
            "",
            "## Reasons",
            "",
            *[f"- {item}" for item in veto.get("reasons", [])],
            "",
            "## Refinement prompt",
            "",
            "```text",
            str(veto.get("refinement_prompt") or ""),
            "```",
            "",
        ]
        write_text_report("\n".join(md_lines), md_path)
        refs = {
            "json": repo_rel(self.repo_root, json_path),
            "markdown": repo_rel(self.repo_root, md_path),
        }
        self.append_heap_exchange_event(
            {
                "kind": "heap_refinement_task",
                "lane": "arbiter",
                "round": revision,
                "path": refs["json"],
                "markdown": refs["markdown"],
                "summary": "cross-lane veto converted into next provider refinement task",
            }
        )
        return refs

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
        previous = self.latest_proposal_iteration_block(max_chars=PROPOSAL_ITERATION_SUMMARY_CHARS)
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
        self.write_heap_parallel_cycle_artifact(revision, parallel_cycle)
        cross_lane_veto = self.cross_lane_proposal_veto(
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
            self.write_heap_refinement_task_artifact(revision, cross_lane_veto)
        quality_passed = bool(
            quality.get("passed")
            and implementation_quality.get("passed")
            and proposal_progress.get("passed")
            and parallel_cycle.get("passed")
            and not cross_lane_veto.get("vetoed")
        )
        clipped = (response_text or "")[:PROPOSAL_ITERATION_MAX_CHARS]
        data = {
            "schema_version": 1,
            "kind": "heap_proposal_iteration",
            "stamp": self.stamp,
            "revision": revision,
            "source": source,
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
            "reject_reason": "; ".join(cross_lane_veto.get("reasons", [])),
            "anchored_source_candidates": anchored_sources,
            "previous_iteration_available": bool(previous),
            "response_text": clipped,
        }
        write_json_report(data, json_path)
        md = [
            "# Heap Proposal Iteration",
            "",
            f"- Revision: `{revision}`",
            f"- Source: `{source}`",
            f"- Quality passed: `{quality_passed}`",
            "",
            "## Deterministic lane reviews",
            "",
            "### GPU0 review",
            "",
            *[f"- {item}" for item in deterministic_reviews.get("gpu0_review", [])],
            "",
            "### NPU micro-task piece",
            "",
            *[f"- {item}" for item in deterministic_reviews.get("npu_micro_task_piece", [])],
            "",
            "### Implementation quality",
            "",
            f"- Passed: `{implementation_quality.get('passed')}`",
            f"- Errors: `{implementation_quality.get('errors')}`",
            "",
            "### Proposal progress",
            "",
            f"- Passed: `{proposal_progress.get('passed')}`",
            f"- Similarity: `{proposal_progress.get('similarity')}`",
            f"- Errors: `{proposal_progress.get('errors')}`",
            "",
            "### NPU workload audit",
            "",
            f"- Requested: `{npu_audit.get('requested')}`",
            f"- Performed: `{npu_audit.get('performed')}`",
            f"- Passed: `{npu_audit.get('passed')}`",
            f"- Iterations: `{npu_audit.get('iterations')}`",
            f"- Seconds: `{npu_audit.get('seconds')}`",
            f"- Python: `{npu_audit.get('python_exe')}`",
            "",
            "### Heap parallel cycle",
            "",
            f"- Passed: `{parallel_cycle.get('passed')}`",
            f"- Missing lanes: `{parallel_cycle.get('missing_lanes')}`",
            "",
            "### Cross-lane veto",
            "",
            f"- Vetoed: `{cross_lane_veto.get('vetoed')}`",
            f"- Reasons: `{cross_lane_veto.get('reasons')}`",
            "",
            "## Anchored source candidates",
            "",
            *[f"- `{item}`" for item in anchored_sources[:20]],
            "",
            "## Proposal chunk",
            "",
            clipped,
            "",
        ]
        write_text_report("\n".join(md), md_path)
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
                "quality_passed": quality_passed,
                "proposal_progress_passed": bool(proposal_progress.get("passed")),
                "npu_workload_performed": bool(npu_audit.get("performed")),
                "summary": f"provider proposal revision {revision} persisted as reusable heap chunk",
            }
        )
        return refs
