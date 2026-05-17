"""RuntimeGateMatrixLabMixin extracted from the heap runtime completeness gate."""

from __future__ import annotations

from Tools.ai.heap_gate.runtime_common import (
    REQUIREMENT_ORDER,
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
from Tools.ai.heap_gate.matrix_lab_evidence import RuntimeGateMatrixLabEvidenceMixin


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
        plan = planner.plan(
            request_text=self.request_text(),
            explicit_candidates=self.real_source_file_candidates(limit=80),
            limit=max(1, min(32, int(self.args.files_per_round) * 4)),
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

    def virtual_dev_environment_targets(self) -> list[str]:
        return self.code_execution_matrix_targets()

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
                        "Tools/validation/run_heap_virtual_dev_environment_smoke/cli.py",
                        "Tools/validation/run_heap_final_readable_product_smoke/cli.py",
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
        return [
            {
                "stage": 4,
                "requirement": "code_execution_matrix",
                "id": "heap-code-execution-matrix",
                "tool": "run_heap_code_execution_matrix",
                "args": {
                    "target_file": self.code_execution_matrix_targets(),
                    "validation_script": [
                        "Tools/validation/test_proposal_gate/cli.py",
                        "Tools/validation/run_heap_code_execution_tool_smoke/cli.py",
                        "Tools/validation/run_heap_virtual_dev_environment_smoke/cli.py",
                        "Tools/validation/run_heap_final_readable_product_smoke/cli.py",
                    ],
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 120), 600),
                    "tail_chars": 5000,
                    "max_diff_chars": 80000,
                    "operator_request": request,
                    "synthesize_patch_candidates": self.patch_candidate_synthesis_required(),
                    "force_patch_candidate_synthesis": self.patch_candidate_synthesis_required(),
                    "max_patch_candidates": min(5, max(1, int(self.args.files_per_round))),
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
            "tools/ai/run_heap_runtime_completeness_gate.py",
            "tools/ai/agent_runtime_tool_broker.py",
        ]
        return [path for path in candidates if (self.repo_root / path).exists()]

    def write_runtime_debug_lab_request(self) -> tuple[str, str, str]:
        lab_dir = self.runtime_debug_lab_dir()
        request_path = lab_dir / f"agent_runtime_debug_lab_request_{self.stamp}.json"
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
        request_path.write_text(
            json.dumps(request, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        return (
            repo_rel(self.repo_root, request_path),
            repo_rel(self.repo_root, report_path),
            repo_rel(self.repo_root, markdown_path),
        )

    def runtime_debug_lab_plan_items(self, context_dir: Path, request: str) -> list[dict[str, Any]]:
        if not self.runtime_debug_lab_required():
            return []
        request_file, output, markdown_output = self.write_runtime_debug_lab_request()
        return [
            {
                "stage": 4,
                "requirement": "runtime_debug_lab_execution",
                "id": "runtime-debug-lab-execution",
                "tool": "agent_runtime_debug_lab",
                "args": {
                    "request_file": request_file,
                    "output": output,
                    "markdown_output": markdown_output,
                    "timeout_seconds": min(max(int(self.args.timeout_seconds), 60), 600),
                    "tail_chars": 4000,
                },
                "reason": "execute the reusable report-only Python debug lab before claiming an MVP/lab product",
            }
        ]

    def required_requirements_order(self) -> list[str]:
        order = list(REQUIREMENT_ORDER)
        if self.virtual_dev_environment_required() and "virtual_dev_environment" not in order:
            order.append("virtual_dev_environment")
        if self.code_execution_matrix_required() and "code_execution_matrix" not in order:
            order.append("code_execution_matrix")
        if self.runtime_debug_lab_required() and "runtime_debug_lab_execution" not in order:
            order.append("runtime_debug_lab_execution")
        return order
