#!/usr/bin/env python3
"""Canonical CLI for the IA-Carmine heap runtime completeness gate."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

repo_root = Path(__file__).resolve().parents[3]
if str(repo_root) not in sys.path:
    sys.path.insert(0, str(repo_root))

from ia_carmine.runtime.heap_gate.heap_exchange import RuntimeGateHeapExchangeMixin
from ia_carmine.runtime.heap_gate.loop_steps import RuntimeGateLoopStepsMixin
from ia_carmine.runtime.heap_gate.matrix_lab import RuntimeGateMatrixLabMixin
from ia_carmine.runtime.heap_gate.proposal_cycle_a import RuntimeGateProposalCycleAMixin
from ia_carmine.runtime.heap_gate.proposal_cycle_b import RuntimeGateProposalCycleBMixin
from ia_carmine.runtime.heap_gate.provider_commands import RuntimeGateProviderCommandsMixin
from ia_carmine.runtime.heap_gate.provider_context import RuntimeGateProviderContextMixin
from ia_carmine.runtime.heap_gate.provider_execution import RuntimeGateProviderExecutionMixin
from ia_carmine.runtime.heap_gate.provider_prompt import RuntimeGateProviderPromptMixin
from ia_carmine.runtime.heap_gate.provider_refinement import RuntimeGateProviderRefinementMixin
from ia_carmine.runtime.heap_gate.run_loop import RuntimeGateRunLoopMixin
from ia_carmine.runtime.heap_gate.runtime_common import (
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    resolve_output_path,
    safe_dict,
    write_json_report,
    write_text_report,
)
from ia_carmine.runtime.heap_gate.runtime_init import RuntimeGateInitMixin
from ia_carmine.runtime.heap_gate.source_refs import RuntimeGateSourceRefsMixin
from ia_carmine.runtime.heap_gate.startup_context import RuntimeGateStartupContextMixin
from ia_carmine.runtime.heap_gate.tool_broker import RuntimeGateToolBrokerMixin


class HeapRuntimeCompletenessGate(
    RuntimeGateInitMixin,
    RuntimeGateSourceRefsMixin,
    RuntimeGateStartupContextMixin,
    RuntimeGateProposalCycleAMixin,
    RuntimeGateProposalCycleBMixin,
    RuntimeGateHeapExchangeMixin,
    RuntimeGateMatrixLabMixin,
    RuntimeGateToolBrokerMixin,
    RuntimeGateLoopStepsMixin,
    RuntimeGateProviderContextMixin,
    RuntimeGateProviderCommandsMixin,
    RuntimeGateProviderRefinementMixin,
    RuntimeGateProviderPromptMixin,
    RuntimeGateProviderExecutionMixin,
    RuntimeGateRunLoopMixin,
):
    """Runtime gate orchestrator assembled from focused OOP mixins."""


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Heap Runtime Completeness Gate", ""]
    lines.append(f"- Passed: `{report.get('passed')}`")
    lines.append(f"- Stamp: `{report.get('stamp')}`")
    metrics = safe_dict(report.get("metrics"))
    for key in (
        "heap_read_count",
        "heap_write_count",
        "tool_request_count",
        "tool_execution_count",
        "decision_count",
        "candidate_operation_count",
        "product_status",
        "completed_requirement_count",
        "required_requirement_count",
        "missing_requirements",
        "budget_exhausted",
        "budget_decision",
        "budget_max_iterations",
        "invocation_contract_ready",
        "invocation_gate_decision",
        "runtime_state_gate_passed",
        "runtime_state_degraded_lanes",
        "max_degraded_lanes",
    ):
        lines.append(f"- {key}: `{metrics.get(key)}`")
    product = safe_dict(safe_dict(report.get("state")).get("product"))
    lines.extend(
        [
            "",
            "## Product",
            "",
            f"- Status: `{product.get('status')}`",
            f"- Request: `{product.get('request_input')}`",
            f"- Response source: `{product.get('response_source')}`",
            f"- Response text: {product.get('response_text')}",
            f"- Reason: {product.get('reason')}",
        ]
    )
    lines.extend(["", "## Completed requirements", ""])
    for item in metrics.get("completed_requirements") or []:
        lines.append(f"- `{item}`")
    if metrics.get("missing_requirements"):
        lines.extend(["", "## Missing requirements", ""])
        for item in metrics.get("missing_requirements") or []:
            lines.append(f"- `{item}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors", []))
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", default="")
    parser.add_argument(
        "--objective",
        default=(
            "prove complete heap-driven teamwork loop over repository context, "
            "shared memory, brokered tools and all provider lanes"
        ),
    )
    parser.add_argument(
        "--request",
        default="",
        help="Optional real user request for heap heartbeat, e.g. ciao.",
    )
    parser.add_argument(
        "--request-file",
        default="",
        help="Read request text from file to avoid long Windows command lines.",
    )
    parser.add_argument(
        "--python-exe",
        default="",
        help=(
            "Explicit project Python executable for child tools. Defaults to "
            "repo .venv resolver; no system env fallback."
        ),
    )
    parser.add_argument(
        "--startup-manifest",
        default="",
        help="Structured startup context/memory reload manifest. Preferred over --task-file.",
    )
    parser.add_argument(
        "--task-file",
        default="",
        help="Legacy readable startup artifact fallback; not the primary runtime data plane.",
    )
    parser.add_argument(
        "--tool",
        default="run_gpu_planner_json_contract_smoke",
        help="Compatibility flag; complete gate uses its internal readiness tool plan.",
    )
    parser.add_argument("--max-iterations", type=int, default=4)
    parser.add_argument("--min-runtime-rounds", type=int, default=1)
    parser.add_argument("--min-proposal-iterations", type=int, default=0)
    parser.add_argument(
        "--max-provider-revisions",
        type=int,
        default=2,
        help="Retry provider teamwork when exit quality fails before closing the heap.",
    )
    parser.add_argument("--budget-minutes", type=int, default=5)
    parser.add_argument("--max-rounds", type=int, default=4)
    parser.add_argument("--files-per-round", type=int, default=4)
    parser.add_argument("--max-context-files", type=int, default=64)
    parser.add_argument("--max-chars-per-file", type=int, default=1800)
    parser.add_argument("--context-document-count", type=int, default=64)
    parser.add_argument("--context-document-preview-chars", type=int, default=1800)
    parser.add_argument("--semantic-code-chunk-limit", type=int, default=64)
    parser.add_argument("--semantic-code-chunk-preview-chars", type=int, default=1800)
    parser.add_argument("--semantic-evidence-chunk-limit", type=int, default=48)
    parser.add_argument("--memory-search-limit", type=int, default=20)
    parser.add_argument("--tool-catalog-limit", type=int, default=160)
    parser.add_argument("--max-new-tokens", type=int, default=1200)
    parser.add_argument("--ollama-num-ctx", type=int, default=16384)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default="all")
    parser.add_argument("--ollama-num-thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default="8192,4096")
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("--gpu0-model-dir", default="")
    parser.add_argument("--npu-model-dir", default="")
    parser.add_argument("--operator-gpu-observation", default="")
    parser.add_argument("--keep-alive", default="120s")
    parser.add_argument("--npu-micro-start-mode", default="deferred")
    parser.add_argument("--npu-micro-timeout-seconds", type=int, default=60)
    parser.add_argument("--npu-final-wait-seconds", type=int, default=60)
    parser.add_argument("--npu-max-context-chars", type=int, default=8000)
    parser.add_argument("--npu-max-prompt-chars", type=int, default=1200)
    parser.add_argument("--npu-max-new-tokens", type=int, default=384)
    parser.add_argument(
        "--allow-npu-device-workload",
        action="store_true",
        default=True,
        help="Opt in to a bounded real OpenVINO NPU micro workload for the NPU audit lane.",
    )
    parser.add_argument("--npu-device-workload-seconds", type=float, default=0.25)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=8)
    parser.add_argument("--allow-provider-generation", action="store_true")
    parser.add_argument("--operator-intent", action="store_true")
    parser.add_argument("--require-ollama-gpu-residency", action="store_true", default=True)
    parser.add_argument("--timeout-seconds", type=int, default=240)
    parser.add_argument("--provider-model", default="auto")
    parser.add_argument("--gpu0-iterations", type=int, default=16)
    parser.add_argument("--gpu0-min-seconds", type=float, default=0.1)
    parser.add_argument("--max-degraded-lanes", type=int, default=0)
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--heap-markdown", default="")
    parser.add_argument("--bridge-dir", default="")
    parser.add_argument("--bridge-output", default="")
    parser.add_argument("--bridge-markdown-output", default="")
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    gate = HeapRuntimeCompletenessGate(args)
    report = gate.run()
    output = resolve_output_path(
        gate.repo_root,
        gate.path_arg(args.output, DEFAULT_OUTPUT).format(stamp=gate.stamp),
    )
    markdown = resolve_output_path(
        gate.repo_root,
        gate.path_arg(args.markdown_output, DEFAULT_MARKDOWN).format(stamp=gate.stamp),
    )
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2


if __name__ == "__main__":
    raise SystemExit(main())
