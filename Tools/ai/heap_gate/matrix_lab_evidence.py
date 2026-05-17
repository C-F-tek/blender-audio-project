"""Evidence-reading methods for runtime matrix and debug-lab execution."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import Any, Path, read_json, repo_rel, safe_int


class RuntimeGateMatrixLabEvidenceMixin:
    def virtual_dev_environment_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "virtual_dev_environment":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in ("json_report", "markdown_report"):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def virtual_dev_environment_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.virtual_dev_environment_required():
            return True
        return self._requirement_passed(events, "virtual_dev_environment")

    def code_execution_matrix_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "code_execution_matrix":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in (
                "json_report",
                "markdown_report",
                "request_file",
                "debug_lab_report",
                "debug_lab_markdown",
            ):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def code_execution_matrix_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.code_execution_matrix_required():
            return True
        return self._requirement_passed(events, "code_execution_matrix")

    def code_execution_matrix_summaries(self, events: list[dict[str, Any]]) -> list[dict[str, Any]]:
        summaries: list[dict[str, Any]] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "code_execution_matrix":
                continue
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            if summary:
                summaries.append(summary)
        return summaries

    def code_execution_matrix_metric_count(self, events: list[dict[str, Any]], key: str) -> int:
        values = [
            safe_int(summary.get(key), default=0)
            for summary in self.code_execution_matrix_summaries(events)
        ]
        return max(values) if values else 0

    def _resolve_runtime_report_ref(self, value: Any) -> Path | None:
        text = str(value or "").strip()
        if not text:
            return None
        path = Path(text)
        return path if path.is_absolute() else self.repo_root / text

    def matrix_patch_candidate_evidence(
        self,
        events: list[dict[str, Any]],
        limit: int = 8,
    ) -> list[dict[str, Any]]:
        items: list[dict[str, Any]] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "code_execution_matrix":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            report_path = self._resolve_runtime_report_ref(outputs.get("json_report"))
            if not report_path or not report_path.is_file():
                continue
            matrix = read_json(report_path)
            if not isinstance(matrix, dict):
                continue
            synthesis_path = self._resolve_runtime_report_ref(
                matrix.get("patch_candidate_synthesis_report")
            )
            synthesis = read_json(synthesis_path) if synthesis_path and synthesis_path.is_file() else {}
            candidates = self._matrix_candidates(matrix, synthesis)
            for candidate in candidates:
                item = self._candidate_evidence_item(candidate, matrix, report_path, synthesis_path)
                if item and item not in items:
                    items.append(item)
                if len(items) >= limit:
                    return items
        return items

    def _matrix_candidates(self, matrix: dict[str, Any], synthesis: dict[str, Any]) -> list[dict[str, Any]]:
        candidates = matrix.get("concrete_code_proposals")
        if not isinstance(candidates, list):
            candidates = []
        out = [item for item in candidates if isinstance(item, dict)]
        if isinstance(synthesis, dict):
            for candidate in synthesis.get("candidates") or []:
                if isinstance(candidate, dict) and candidate.get("passed") is True:
                    out.append(
                        {
                            "target_file": candidate.get("target_file"),
                            "implementation_status": "validated_patch_candidate",
                            "source": "patch_candidate_synthesis",
                            "diff_path": candidate.get("diff_path"),
                            "reason": candidate.get("reason"),
                            "validation_commands": candidate.get("validation_commands"),
                        }
                    )
        return out

    def _candidate_evidence_item(
        self,
        candidate: dict[str, Any],
        matrix: dict[str, Any],
        report_path: Path,
        synthesis_path: Path | None,
    ) -> dict[str, Any] | None:
        target = str(candidate.get("target_file") or "").replace("\\", "/")
        if not target or not self.repo_source_file_exists(target):
            return None
        return {
            "target_file": target,
            "implementation_status": candidate.get("implementation_status"),
            "source": candidate.get("source") or "code_execution_matrix",
            "matrix_report": repo_rel(self.repo_root, report_path),
            "patch_candidate_synthesis_report": (
                repo_rel(self.repo_root, synthesis_path)
                if synthesis_path and synthesis_path.is_file()
                else ""
            ),
            "diff_path": candidate.get("diff_path"),
            "reason": candidate.get("reason"),
            "validation_commands": candidate.get("validation_commands") or [],
            "concrete_code_proposal_count": matrix.get("concrete_code_proposal_count"),
            "patch_candidate_synthesis_passed_count": matrix.get(
                "patch_candidate_synthesis_passed_count"
            ),
        }

    def matrix_patch_candidate_feedback(self, events: list[dict[str, Any]]) -> str:
        evidence = self.matrix_patch_candidate_evidence(events, limit=8)
        if not evidence:
            return ""
        lines = [
            "BROKER/MATRIX EVIDENCE TO CONSUME IN THIS POINTER LOOP:",
            "- These are real broker artifacts, not prose. The next proposal revision must consume them or explicitly reject them.",
            "- Copy TARGET_FILES exactly from target_file below; do not invent alternate paths or basenames.",
            "- If a diff_path is present, cite it as artifact evidence and preserve its validation commands.",
        ]
        for item in evidence:
            commands = item.get("validation_commands")
            command_text = (
                "; ".join(str(cmd) for cmd in commands[:3]) if isinstance(commands, list) else ""
            )
            lines.append(
                "- target_file={target}; status={status}; source={source}; matrix={matrix}; diff_path={diff}; reason={reason}; validation={validation}".format(
                    target=item.get("target_file"),
                    status=item.get("implementation_status"),
                    source=item.get("source"),
                    matrix=item.get("matrix_report"),
                    diff=item.get("diff_path") or "",
                    reason=item.get("reason") or "",
                    validation=command_text,
                )
            )
        return "\n".join(lines)

    def runtime_debug_lab_reports(self, events: list[dict[str, Any]]) -> list[str]:
        refs: list[str] = []
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != "runtime_debug_lab_execution":
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            for key in ("json_report", "markdown_report", "request_file"):
                value = str(outputs.get(key) or "").strip()
                if value and value not in refs:
                    refs.append(value)
        return refs

    def runtime_debug_lab_passed(self, events: list[dict[str, Any]]) -> bool:
        if not self.runtime_debug_lab_required():
            return True
        return self._requirement_passed(events, "runtime_debug_lab_execution")

    def _requirement_passed(self, events: list[dict[str, Any]], requirement_name: str) -> bool:
        for payload in self.broker_results(events):
            requirement = str(
                payload.get("requirement")
                or self.requirement_for_tool(str(payload.get("tool") or ""))
            )
            if requirement != requirement_name:
                continue
            if payload.get("blocked") or safe_int(payload.get("returncode"), default=1) != 0:
                continue
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            if summary.get("passed") is False:
                continue
            return True
        return False
