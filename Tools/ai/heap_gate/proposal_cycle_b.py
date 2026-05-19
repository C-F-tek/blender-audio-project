"""RuntimeGateProposalCycleBMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    PLACEHOLDER_CODE_LABELS,
    PLACEHOLDER_CODE_PATTERNS,
    Any,
    SequenceMatcher,
    re,
    read_json,
    repo_rel,
    safe_int,
)


class RuntimeGateProposalCycleBMixin:
    def proposal_iteration_artifacts(self) -> list[str]:
        out_dir = self.proposal_iteration_dir()
        refs: list[str] = []
        for path in sorted(out_dir.glob("heap_proposal_revision_*.json")):
            refs.append(repo_rel(self.repo_root, path))
            md = path.with_suffix(".md")
            if md.exists():
                refs.append(repo_rel(self.repo_root, md))
        return refs

    def latest_proposal_iteration_block(self, max_chars: int = 4000) -> str:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.md"))
        if not candidates:
            return ""
        text = candidates[-1].read_text(encoding="utf-8", errors="replace")
        if len(text) <= max_chars:
            return text
        return text[-max_chars:]

    def latest_proposal_iteration_report(self) -> dict[str, Any]:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.json"))
        if not candidates:
            return {}
        return read_json(candidates[-1])

    def latest_proposal_quality_passed(self) -> bool:
        report = self.latest_proposal_iteration_report()
        if not report:
            return False
        return report.get("quality_passed") is True

    def latest_quality_proposal_iteration_block(self, max_chars: int = 4000) -> str:
        out_dir = self.proposal_iteration_dir()
        for json_path in reversed(sorted(out_dir.glob("heap_proposal_revision_*.json"))):
            report = read_json(json_path)
            if report.get("quality_passed") is not True:
                continue
            md_path = json_path.with_suffix(".md")
            if not md_path.exists():
                continue
            text = md_path.read_text(encoding="utf-8", errors="replace")
            if len(text) <= max_chars:
                return text
            return text[-max_chars:]
        return ""

    def normalized_proposal_text(self, value: str) -> str:
        normalized = re.sub(r"\s+", " ", str(value or "").strip().lower())
        normalized = re.sub(r"revision\s*[:` ]+\d+", "revision", normalized)
        return normalized

    def proposal_revision_progress_report(
        self, response_text: str, quality: dict[str, Any]
    ) -> dict[str, Any]:
        previous = self.latest_proposal_iteration_report()
        if not previous:
            return {
                "required": False,
                "passed": True,
                "reason": "first proposal iteration",
                "similarity": 0.0,
                "repeated_unverified_source_refs": [],
            }
        previous_text = str(previous.get("response_text") or "")
        current_norm = self.normalized_proposal_text(response_text)
        previous_norm = self.normalized_proposal_text(previous_text)
        similarity = (
            SequenceMatcher(None, previous_norm[:8000], current_norm[:8000]).ratio()
            if previous_norm and current_norm
            else 0.0
        )
        previous_quality = (
            previous.get("response_file_reference_quality")
            if isinstance(previous.get("response_file_reference_quality"), dict)
            else {}
        )
        previous_unverified = {
            str(item)
            for item in previous_quality.get("unverified_source_file_refs")
            or previous_quality.get("unverified_file_refs")
            or []
        }
        current_unverified = {
            str(item)
            for item in quality.get("unverified_source_file_refs")
            or quality.get("unverified_file_refs")
            or []
        }
        repeated_unverified = sorted(previous_unverified.intersection(current_unverified))
        errors: list[str] = []
        if similarity >= 0.94:
            errors.append(
                f"proposal revision too similar to previous iteration: similarity={similarity:.3f}"
            )
        if repeated_unverified:
            errors.append(f"proposal repeated unresolved source refs: {repeated_unverified}")
        return {
            "required": True,
            "passed": not errors,
            "reason": "proposal must improve previous heap chunk",
            "similarity": round(similarity, 4),
            "repeated_unverified_source_refs": repeated_unverified,
            "errors": errors,
        }

    def npu_workload_audit_report(self) -> dict[str, Any]:
        for report in reversed(self.provider_reports):
            if report.get("lane") != "npu_micro_task_auditor":
                continue
            output = str(report.get("output") or "")
            data = read_json(self.repo_root / output)
            workload = (
                data.get("npu_device_workload")
                if isinstance(data.get("npu_device_workload"), dict)
                else {}
            )
            if workload:
                return {
                    "source_file": output,
                    "requested": bool(workload.get("requested")),
                    "performed": bool(workload.get("performed")),
                    "passed": bool(workload.get("passed")),
                    "mode": workload.get("mode"),
                    "iterations": safe_int(workload.get("iterations")),
                    "seconds": workload.get("seconds"),
                    "python_exe": workload.get("python_exe"),
                    "errors": (
                        workload.get("errors") if isinstance(workload.get("errors"), list) else []
                    ),
                    "warnings": (
                        workload.get("warnings")
                        if isinstance(workload.get("warnings"), list)
                        else []
                    ),
                }
            return {
                "source_file": output,
                "requested": bool(data.get("npu_device_workload_requested")),
                "performed": bool(data.get("npu_device_workload_performed")),
                "passed": False,
                "mode": "npu_workload_report_missing",
                "iterations": 0,
                "seconds": 0.0,
                "errors": [],
                "warnings": [],
            }
        return {
            "requested": False,
            "performed": False,
            "passed": False,
            "mode": "npu_report_unavailable",
            "iterations": 0,
            "seconds": 0.0,
            "errors": [],
            "warnings": ["NPU provider report unavailable"],
        }

    def proposal_iteration_digest(self, max_blocks: int = 4, max_chars: int = 12000) -> str:
        out_dir = self.proposal_iteration_dir()
        candidates = sorted(out_dir.glob("heap_proposal_revision_*.md"))[-max_blocks:]
        if not candidates:
            return ""
        blocks: list[str] = []
        remaining = max_chars
        for path in candidates:
            text = path.read_text(encoding="utf-8", errors="replace").strip()
            if not text:
                continue
            block = f"## {path.name}\n\n{text}"
            if len(block) > remaining:
                block = block[-remaining:]
            blocks.append(block)
            remaining -= len(block)
            if remaining <= 0:
                break
        return "\n\n---\n\n".join(blocks)

    def implementation_output_required(self) -> bool:
        lowered = self.request_text().lower()
        hints = (
            "implement",
            "codice",
            "patch",
            "patch-plan",
            "patch plan",
            "proposal chunks concreti",
            "proposte concrete",
            "proposta concreta",
            "target_files",
            "target files",
            "path repo reali",
            "repo-relative",
            "blocca placeholder",
            "blocca stub",
            "senza placeholder",
            "senza stub",
            "refiner",
            "refinement",
        )
        return any(hint in lowered for hint in hints)

    def implementation_quality_report(
        self, text: str, events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        file_quality = self.response_file_reference_quality(text)
        lowered = (text or "").lower()
        existing_sources = (
            file_quality.get("existing_source_file_refs") if isinstance(file_quality, dict) else []
        )
        source_count = len(existing_sources or [])
        code_block_count = len(re.findall(r"```", text or "")) / 2
        operation_markers = [
            "target_file",
            "target_files",
            "unified_diff",
            "diff --git",
            "replace_once",
            "insert_after_once",
            "insert_before_once",
            "write_file",
            "def ",
            "class ",
            "python -m py_compile",
            "pytest",
            "git diff --check",
            "validazione",
            "validation",
        ]
        concrete_operation_markers = [marker for marker in operation_markers if marker in lowered]
        generic_markers = [
            "potresti",
            "si potrebbe",
            "considerare",
            "dovrebbe",
            "migliorare la manutenibil",
            "ottimizzare la gestione",
            "assicurarsi che",
            "aggiungere ulteriori test",
            "migliorare la sincronizzazione",
        ]
        generic_marker_hits = [marker for marker in generic_markers if marker in lowered]
        placeholder_hits = [
            label
            for label, pattern in zip(PLACEHOLDER_CODE_LABELS, PLACEHOLDER_CODE_PATTERNS)
            if re.search(pattern, text or "")
        ]
        has_actionable_structure = bool(code_block_count or concrete_operation_markers)
        required = self.implementation_output_required()
        errors: list[str] = []
        if required and source_count <= 0:
            errors.append("no verified source file references")
        invented_source_path_refs = list(file_quality.get("unverified_source_file_refs") or [])
        if required and invented_source_path_refs:
            errors.append(f"unverified source file refs: {invented_source_path_refs}")
            errors.append(f"invented/non-allowlisted source path refs: {invented_source_path_refs}")
        if required and file_quality.get("ambiguous_source_file_refs"):
            errors.append(
                f"ambiguous source file refs: {sorted(file_quality.get('ambiguous_source_file_refs', {}).keys())}"
            )
        if required and not file_quality.get("passed"):
            errors.append("source file reference quality failed")
        if required and not has_actionable_structure:
            errors.append("no code/diff/operation/validation markers")
        if required and placeholder_hits:
            errors.append(f"placeholder/stub code detected: {placeholder_hits}")
        if (
            required
            and generic_marker_hits
            and (not code_block_count or placeholder_hits)
            and len(concrete_operation_markers) < 3
        ):
            errors.append("generic advisory wording without enough implementation detail")
        passed = (not required) or (source_count > 0 and has_actionable_structure and not errors)
        return {
            "required": required,
            "passed": passed,
            "source_count": source_count,
            "code_block_count": code_block_count,
            "concrete_operation_markers": concrete_operation_markers,
            "generic_marker_hits": generic_marker_hits,
            "placeholder_hits": placeholder_hits,
            "invented_source_path_refs": invented_source_path_refs if required else [],
            "errors": errors,
        }

    def deterministic_lane_reviews(
        self, response_text: str, quality: dict[str, Any], events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        implementation_quality = self.implementation_quality_report(response_text, events)
        file_quality = self.response_file_reference_quality(response_text)
        gpu0_notes: list[str] = []
        if not implementation_quality.get("passed") and implementation_quality.get("required"):
            gpu0_notes.append(
                "GPU0 deterministic review: proposta non soddisfacente; manca implementazione concreta/codice/operazioni validabili."
            )
        if file_quality.get("unverified_source_file_refs"):
            gpu0_notes.append(
                f"GPU0 deterministic review: source refs non verificati={file_quality.get('unverified_source_file_refs')}."
            )
            gpu0_notes.append(
                "GPU0 deterministic review: invented_source_path veto; TARGET_FILES must come from source allowlist only."
            )
        if file_quality.get("ambiguous_source_file_refs"):
            gpu0_notes.append(
                f"GPU0 deterministic review: source refs ambigui={sorted(file_quality.get('ambiguous_source_file_refs', {}).keys())}."
            )
        if implementation_quality.get("placeholder_hits"):
            gpu0_notes.append(
                f"GPU0 deterministic review: placeholder/stub code rilevati={implementation_quality.get('placeholder_hits')}."
            )
        if not gpu0_notes:
            gpu0_notes.append(
                "GPU0 deterministic review: proposta usabile come blocco, soggetta a validazione finale."
            )
        npu_audit = self.npu_workload_audit_report()
        npu_notes = [
            "NPU micro-task piece: audit guardrail; verificare che il blocco non dichiari patch applicate, source write o provider execution NPU se non presenti.",
            f"NPU micro-task piece: implementation_quality_passed={implementation_quality.get('passed')}, file_quality_passed={file_quality.get('passed')}.",
            f"NPU micro-task piece: workload_requested={npu_audit.get('requested')}, workload_performed={npu_audit.get('performed')}, workload_passed={npu_audit.get('passed')}, iterations={npu_audit.get('iterations')}, seconds={npu_audit.get('seconds')}.",
        ]
        if (
            implementation_quality.get("placeholder_hits")
            or file_quality.get("unverified_source_file_refs")
            or file_quality.get("ambiguous_source_file_refs")
        ):
            if file_quality.get("unverified_source_file_refs"):
                npu_notes.append(
                    "NPU micro-task piece: veto=invented_source_path_or_non_allowlisted_target."
                )
            npu_notes.append(
                "NPU micro-task piece: decision=reject_until_concrete_code_and_full_repo_relative_paths."
            )
        return {
            "gpu0_review": gpu0_notes,
            "npu_micro_task_piece": npu_notes,
            "implementation_quality": implementation_quality,
        }

    def proposal_iteration_feedback(
        self, events: list[dict[str, Any]], quality: dict[str, Any] | None = None
    ) -> str:
        latest = self.latest_proposal_iteration_block(max_chars=3500)
        anchor = self.source_anchor_feedback(events, quality)
        matrix_feedback = self.matrix_patch_candidate_feedback(events)
        parts = [
            "HEAP PROPOSAL ITERATION MODE:",
            "NPU PIECE LANE REQUIRED: when provider generation/peer revision is permitted, NPU must contribute audit pieces, guardrail deltas, source anchors, or negative findings into the heap exchange instead of remaining only a device-visibility note.",
            "GPU0 REVIEW REQUIRED: if the previous proposal is generic, lacks code, lacks target paths, or only says what should be done, mark it as non soddisfacente and rewrite it as an operational block.",
            "The next revision must refine the previous proposal chunk and make it more operational.",
            "Do not restart from scratch. Preserve useful decisions, add verified repo-relative paths, signatures, commands, concrete implementation steps, validation commands and patch-level code.",
            "Use this exact structure in the next proposal: TARGET_FILES, PROBLEM, IMPLEMENTATION_CHANGES, PATCH_SKETCH_UNIFIED_DIFF, VALIDATION_COMMANDS, RISKS, EXIT_DECISION. PATCH_SKETCH_UNIFIED_DIFF must be a fenced unified diff with diff --git headers for allowlisted targets, or EXIT_DECISION=NO_PATCHABLE_TARGET.",
            "The final answer is assembled from proposal_iteration artifacts at heap exit, not only from raw GPU1 context.",
        ]
        if latest:
            parts.extend(["", "Previous proposal chunk:", latest])
        if matrix_feedback:
            parts.extend(["", matrix_feedback])
        if anchor:
            parts.extend(["", anchor])
        return "\n".join(parts)
