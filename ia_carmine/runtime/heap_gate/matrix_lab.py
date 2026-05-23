"""RuntimeGateMatrixLabMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from ia_carmine.runtime.heap_gate.runtime_common import (
    BASE_REQUIREMENTS,
    PROVIDER_REQUIREMENTS,
    Any,
    Path,
    RuntimeTargetPlanner,
    json,
    read_json,
    repo_rel,
    request_focus_text,
    safe_int,
    tokenize,
)
from ia_carmine.runtime.heap_gate.matrix_lab_evidence import RuntimeGateMatrixLabEvidenceMixin

PROVIDER_CONSUMABLE_REQUIREMENTS = {
    "runtime_file_refs",
    "startup_memory_index_batch",
    "provider_input_memory_index_batch",
    "virtual_dev_environment",
    "code_execution_matrix",
    "runtime_debug_lab_execution",
}


class RuntimeGateMatrixLabMixin(RuntimeGateMatrixLabEvidenceMixin):
    def runtime_debug_lab_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        required_terms = (
            "mvp",
            "lab python",
            "laboratorio python",
            "python funzion",
            "debug lab",
            "implementa",
            "implementazione",
            "codice effettivo",
            "funzionante",
        )
        return any(term in text for term in required_terms)

    def code_execution_matrix_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        hints = (
            "codice",
            "code",
            "coding",
            "test",
            "validazione",
            "validation",
            "patch",
            "proposte concrete",
            "proposta concreta",
            "esecuzione",
            "execution",
            "heap/universo",
            "universo",
        )
        return self.implementation_output_required() or any(hint in text for hint in hints)

    def patch_candidate_synthesis_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        hints = (
            "implement",
            "refactor",
            "rifattoriz",
            "oob",
            "oop",
            "patch",
            "code product",
            "codice concreto",
            "proposte concrete",
        )
        return self.code_execution_matrix_required() and (
            self.implementation_output_required() or any(hint in text for hint in hints)
        )

    def request_terms(self) -> set[str]:
        return tokenize(f"{request_focus_text(self.request_text())} {self.args.objective}")

    def code_execution_matrix_targets(self) -> list[str]:
        if self._code_execution_matrix_targets_cache is not None:
            return list(self._code_execution_matrix_targets_cache)
        planner = RuntimeTargetPlanner(self.repo_root, self.repo_runtime_universe)
        changed_count = len(planner.changed_source_candidates())
        plan = planner.plan(
            request_text=self.request_text(),
            explicit_candidates=self.real_source_file_candidates(limit=80),
            limit=max(1, min(64, max(changed_count, int(self.args.files_per_round) * 4))),
        )
        self._code_execution_matrix_targets_cache = [item.path for item in plan]
        return list(self._code_execution_matrix_targets_cache)

    def virtual_dev_environment_required(self) -> bool:
        text = f"{self.request_text()} {self.args.objective}".lower()
        hints = (
            "ambiente",
            "debug",
            "runtime",
            "svilupp",
            "caricare",
            "script",
            "pointer",
            "universo",
            "virtual",
        )
        return self.implementation_output_required() or any(hint in text for hint in hints)

    def provider_revision_evidence_ready(self, events: list[dict[str, Any]]) -> bool:
        """Return True when requested provider-consumable evidence has responded.

        This is deliberately weaker than final product readiness. Matrix, virtual
        dev and debug-lab failures are useful GPU1 feedback; only pending broker
        work blocks the next provider revision.
        """
        for item in self.next_unattempted_plan_items(events):
            requirement = str(item.get("requirement") or "")
            if requirement in PROVIDER_CONSUMABLE_REQUIREMENTS:
                return False
        return not self.provider_consumable_evidence_status(events).get("pending")

    def provider_consumable_evidence_status(
        self, events: list[dict[str, Any]]
    ) -> dict[str, Any]:
        pending_events = list(getattr(self.heap, "pending_broker_requests", lambda: [])())
        requested: list[str] = []
        pending: list[dict[str, Any]] = []
        results: list[dict[str, Any]] = []
        for event in events:
            if event.get("event_type") not in {"broker_request", "broker_result"}:
                continue
            payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
            requirement = self._provider_consumable_requirement(payload)
            if not requirement:
                continue
            if requirement not in requested:
                requested.append(requirement)
            if event.get("event_type") == "broker_result":
                results.append(payload)
        for event in pending_events:
            payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
            requirement = self._provider_consumable_requirement(payload)
            if not requirement:
                continue
            if requirement not in requested:
                requested.append(requirement)
            pending.append(
                {
                    "id": str(event.get("correlation_id") or payload.get("id") or ""),
                    "tool": str(payload.get("tool") or ""),
                    "requirement": requirement,
                }
            )
        resolved = sorted(
            {
                self._provider_consumable_requirement(result)
                for result in results
                if self._provider_consumable_requirement(result)
            }
        )
        return {
            "provider_consumable_evidence_requested": requested,
            "provider_consumable_evidence_resolved": resolved,
            "provider_consumable_evidence_pending": pending,
            "pending": bool(pending),
            "complete_or_failed_with_report": bool(requested) and not pending,
        }

    def provider_consumable_evidence_feedback(
        self, events: list[dict[str, Any]],
        max_items: int = 8,
    ) -> str:
        lines: list[str] = []
        for payload in self.broker_results(events):
            requirement = self._provider_consumable_requirement(payload)
            if not requirement:
                continue
            outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
            refs = [
                str(outputs.get(key) or "")
                for key in (
                    "json_report",
                    "markdown_report",
                    "request_file",
                    "debug_lab_report",
                    "debug_lab_markdown",
                )
                if str(outputs.get(key) or "").strip()
            ]
            summary = payload.get("summary") if isinstance(payload.get("summary"), dict) else {}
            lines.append(
                "- {tool}->{requirement} rc={rc} refs={refs} summary={summary}".format(
                    tool=payload.get("tool"),
                    requirement=requirement,
                    rc=payload.get("returncode"),
                    refs=";".join(refs[:3]) or str(payload.get("broker_report") or ""),
                    summary=summary,
                )
            )
            if len(lines) >= max_items:
                break
        if not lines:
            return ""
        return "\n".join(
            [
                "PROVIDER_CONSUMABLE_BROKER_EVIDENCE:",
                "- These broker results are input to the next GPU1 pointer revision, not post-provider decoration.",
                *lines,
            ]
        )

    def _provider_consumable_requirement(self, payload: dict[str, Any]) -> str:
        requirement = str(
            payload.get("requirement")
            or self.requirement_for_tool(str(payload.get("tool") or ""))
        )
        if requirement == "runtime_debug_lab":
            requirement = "runtime_debug_lab_execution"
        if requirement in PROVIDER_CONSUMABLE_REQUIREMENTS:
            return requirement
        tool = str(payload.get("tool") or "")
        if tool == "runtime_sqlite_memory" and requirement in {
            "startup_memory_index_batch",
            "provider_input_memory_index_batch",
        }:
            return requirement
        return ""

    def virtual_dev_environment_targets(self) -> list[str]:
        return [
            path
            for path in self.code_execution_matrix_targets()
            if path.replace("\\", "/").endswith(("/cli.py", "/__main__.py"))
        ]

    def virtual_dev_environment_plan_items(
        self, context_dir: Path, request: str
    ) -> list[dict[str, Any]]:
        if not self.virtual_dev_environment_required():
            return []
        return [
            {
                "stage": 4,
                "requirement": "virtual_dev_environment",
                "id": "heap-virtual-dev-environment",
                "tool": "run_heap_virtual_dev_environment",
                "args": {
                    "target_file": self.virtual_dev_environment_targets(),
                    "validation_script": [
                        "Tools/validation/heap_runtime/virtual_dev_environment_smoke/cli.py",
                        "Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py",
                    ],
                    "dynamic_import": True,
                    "help_probe": True,
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 120), 600),
                    "tail_chars": 5000,
                },
                "reason": "provide a controlled development environment where heap tools are loaded, probed, debugged and validated before final composition",
            }
        ]

    def code_execution_matrix_plan_items(
        self, context_dir: Path, request: str
    ) -> list[dict[str, Any]]:
        if not self.code_execution_matrix_required():
            return []
        matrix_dir = context_dir / "code_execution_matrix"
        matrix_dir.mkdir(parents=True, exist_ok=True)
        targets = self.code_execution_matrix_targets()
        evidence_reports = [*self.provider_refs(), *self.proposal_iteration_artifacts()]
        request_args = (
            {"operator_request_file": str(getattr(self.args, "request_file", "") or "")}
            if str(getattr(self.args, "request_file", "") or "").strip()
            else {"operator_request": request}
        )
        return [
            {
                "stage": 4,
                "requirement": "code_execution_matrix",
                "id": "heap-code-execution-matrix",
                "tool": "run_heap_code_execution_matrix",
                "args": {
                    "target_file": targets,
                    "validation_script": [
                        "Tools/validation/heap_final_proposals/test_proposal_gate/cli.py",
                        "Tools/validation/heap_runtime/code_execution_tool_smoke/cli.py",
                        "Tools/validation/heap_runtime/virtual_dev_environment_smoke/cli.py",
                        "Tools/validation/heap_runtime/run_heap_final_readable_product_smoke/cli.py",
                    ],
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 120), 600),
                    "tail_chars": 5000,
                    "max_diff_chars": 80000,
                    **request_args,
                    "evidence_report": evidence_reports,
                    "synthesize_patch_candidates": self.patch_candidate_synthesis_required(),
                    "force_patch_candidate_synthesis": self.patch_candidate_synthesis_required(),
                    "max_patch_candidates": min(64, max(1, len(targets))),
                },
                "reason": "execute concrete compile/test/diff evidence for heap coding proposals before product acceptance",
            }
        ]

    def runtime_debug_lab_dir(self) -> Path:
        path = self.runtime_context_dir() / "runtime_debug_lab"
        path.mkdir(parents=True, exist_ok=True)
        return path

    def runtime_debug_lab_source_paths(self) -> list[str]:
        candidates = [
            "tools/ai/agent_runtime_debug_lab/cli.py",
            "tools/ai/agent_runtime_debug_lab/policy.py",
            "tools/ai/agent_runtime_debug_lab/reporting.py",
            "tools/ai/agent_runtime_debug_lab/runner.py",
            "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py",
            "tools/ai/runtime_tool/agent_broker.py",
        ]
        return [path for path in candidates if (self.repo_root / path).exists()]

    def build_runtime_debug_lab_request(self) -> tuple[dict[str, Any], str, str]:
        lab_dir = self.runtime_debug_lab_dir()
        report_path = lab_dir / f"agent_runtime_debug_lab_{self.stamp}.json"
        markdown_path = lab_dir / f"agent_runtime_debug_lab_{self.stamp}.md"
        source_paths = self.runtime_debug_lab_source_paths()
        request = {
            "schema_version": 1,
            "kind": "agent_runtime_debug_lab_request",
            "operations": [
                {
                    "id": "compile_debug_lab_sources",
                    "type": "python_compile",
                    "paths": source_paths,
                    "timeout_seconds": 300,
                },
                {
                    "id": "git_diff_check",
                    "type": "git_diff_check",
                    "timeout_seconds": 120,
                },
                {
                    "id": "git_status_short",
                    "type": "git_status_short",
                    "timeout_seconds": 120,
                },
            ],
        }
        return (
            request,
            repo_rel(self.repo_root, report_path),
            repo_rel(self.repo_root, markdown_path),
        )

    def runtime_debug_lab_plan_items(self, context_dir: Path, request: str) -> list[dict[str, Any]]:
        if not self.runtime_debug_lab_required():
            return []
        request_json, output, markdown_output = self.build_runtime_debug_lab_request()
        return [
            {
                "stage": 4,
                "requirement": "runtime_debug_lab_execution",
                "id": "runtime-debug-lab-execution",
                "tool": "agent_runtime_debug_lab",
                "args": {
                    "request_json": request_json,
                    "output": output,
                    "markdown_output": markdown_output,
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 60), 600),
                    "tail_chars": 4000,
                },
                "reason": "execute the reusable report-only Python debug lab before claiming an MVP/lab product",
            }
        ]

    def required_requirements_order(self) -> list[str]:
        order = list(BASE_REQUIREMENTS)
        if self.args.allow_provider_generation:
            order.extend(PROVIDER_REQUIREMENTS)
        if self.virtual_dev_environment_required() and "virtual_dev_environment" not in order:
            order.append("virtual_dev_environment")
        if self.code_execution_matrix_required() and "code_execution_matrix" not in order:
            order.append("code_execution_matrix")
        if self.runtime_debug_lab_required() and "runtime_debug_lab_execution" not in order:
            order.append("runtime_debug_lab_execution")
        return order
