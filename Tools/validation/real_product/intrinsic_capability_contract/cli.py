#!/usr/bin/env python3
"""Validate the real product profile intrinsic heap/exchange capability contract."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""


def check_token(text: str, token: str) -> bool:
    return token in text


def has_real_product_mode_contract(wrapper_text: str) -> bool:
    if '"-Mode", "all"' in wrapper_text:
        return True
    return (
        '"-Mode", $RealProductPostPreflightModes' in wrapper_text
        and "$RealProductPostPreflightModes" in wrapper_text
        and "official,provider" in wrapper_text
        and "patch_specs,evidence,contract,full_validation" in wrapper_text
    )


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Real Product Intrinsic Capability Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Task MD input: `{report.get('task_md_input')}`",
        f"- Heap/exchange activation: `{report.get('heap_exchange_activation')}`",
        f"- GPU1 primary advisory: `{report.get('gpu1_primary_advisory')}`",
        f"- GPU0 workload: `{report.get('gpu0_openvino_workload')}`",
        f"- NPU peer micro lane: `{report.get('npu_peer_micro_lane')}`",
        f"- Shared memory/evidence: `{report.get('shared_memory_evidence')}`",
        f"- Static deterministic script lane: `{report.get('static_deterministic_script_lane')}`",
        f"- Heap/exchange close: `{report.get('heap_exchange_close')}`",
        f"- Product readiness: `{report.get('product_readiness')}`",
        f"- Runtime flow map evidence: `{report.get('runtime_flow_map_evidence')}`",
        f"- agent_review_prepare_pr.py: `{report.get('agent_review_prepare_pr')}`",
        f"- Final PR product: `{report.get('final_pr_product')}`",
        "",
        "## Contract order",
        "",
    ]
    for item in report.get("contract_order") or []:
        lines.append(f"- {item}")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def build_report(repo_root: Path) -> dict[str, Any]:
    wrapper = repo_root / "Tools/workflow/_powershell/run_unified_real_product_pr.ps1"
    launcher = repo_root / "Tools/workflow/_powershell/run_unified_local_ai_refactor.ps1"
    readiness = repo_root / "Tools/validation/repository_product/review_pr_product_readiness/cli.py"
    args_builder = repo_root / "Tools/ai/repository_product/review_pr_prepare_args/cli.py"
    prepare = repo_root / "Tools/ai/agent_review/review_pr_cli.py"

    wrapper_text = read_text(wrapper)
    launcher_text = read_text(launcher)
    readiness_text = read_text(readiness)
    args_builder_text = read_text(args_builder)
    prepare_text = read_text(prepare)

    checks: dict[str, bool] = {
        "task_md_input": check_token(wrapper_text, "[string]$TaskFile")
        and check_token(wrapper_text, '"-TaskFile", $TaskRel')
        and check_token(launcher_text, "IA-CARMINE-TASK-INGRESS-CONTRACT-BEGIN"),
        "heap_exchange_activation": has_real_product_mode_contract(wrapper_text)
        and check_token(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-BEGIN")
        and check_token(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-PRE-REVIEW-BRIDGE-BEGIN"),
        "gpu1_primary_advisory": check_token(wrapper_text, "-UsePrimaryAdvisoryProvider")
        and check_token(wrapper_text, "-UseOllamaAdvisory"),
        "gpu0_openvino_workload": check_token(wrapper_text, "-RunOpenVinoGpu0Workload"),
        "npu_peer_micro_lane": (
            check_token(wrapper_text, '[string]$NpuMicroStartMode = "startup"')
            or check_token(wrapper_text, '[string]$NpuMicroStartMode = "peer"')
        )
        and check_token(wrapper_text, "-NpuMicroStartMode")
        and check_token(wrapper_text, "-RunNpuProbe")
        and check_token(wrapper_text, "-RunNpuDecodeSmoke"),
        "runtime_flow_map_evidence": (repo_root / "Tools/ai/runtime_universe/flow_map/cli.py").exists()
        and check_token(launcher_text, "IA-CARMINE-RUNTIME-FLOW-MAP-BEGIN")
        and check_token(launcher_text, "build_runtime_flow_map.py")
        and check_token(launcher_text, "runtime_flow_"),
        "shared_memory_evidence": check_token(wrapper_text, "-SaveInputsToMemoryDb")
        and check_token(wrapper_text, "-BuildEvidence")
        and check_token(launcher_text, "shared_memory_evidence"),
        "static_deterministic_script_lane": check_token(
            wrapper_text, "-BuildTaskPatchSuggestionReport"
        )
        and check_token(wrapper_text, "-GeneratePatchSpecs")
        and (
            check_token(wrapper_text, "-ReviewPrApplyDeterministicSuggestions")
            or check_token(wrapper_text, "-ReviewPrFromGeneratedPatchSpecs")
        )
        and check_token(args_builder_text, "require_product_input"),
        "heap_exchange_close": check_token(
            launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN"
        )
        and check_token(
            launcher_text, "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN"
        )
        and check_token(launcher_text, "IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-END"),
        "product_readiness": check_token(launcher_text, "review_pr_product_readiness")
        and check_token(readiness_text, "prepare_review_pr_ready")
        and check_token(readiness_text, "has_concrete_product"),
        "agent_review_prepare_pr": check_token(launcher_text, "build_review_pr_prepare_args")
        and check_token(launcher_text, "Prepare review branch and PR")
        and check_token(prepare_text, "gh")
        and check_token(prepare_text, "pr")
        and check_token(prepare_text, "create"),
        "final_pr_product": check_token(wrapper_text, "-ReviewPrPush")
        and check_token(wrapper_text, "-ReviewPrCreate")
        and check_token(wrapper_text, "-ReviewPrDraft")
        and check_token(prepare_text, "--create-pr")
        and check_token(prepare_text, "--draft-pr"),
    }

    contract_order = [
        "Task MD IN",
        "heap/exchange activation",
        "GPU1 primary advisory",
        "GPU0 OpenVINO/tool workload",
        "NPU peer micro lane",
        "shared memory / evidence / static deterministic script",
        "heap/exchange CLOSE",
        "runtime flow map evidence",
        "product readiness",
        "agent_review_prepare_pr.py",
        "PR finale testabile",
    ]

    errors = [
        f"missing intrinsic capability: {name}" for name, passed in checks.items() if not passed
    ]

    return {
        "schema_version": 1,
        "kind": "real_product_intrinsic_capability_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "wrapper": wrapper.as_posix(),
        "launcher": launcher.as_posix(),
        "readiness_gate": readiness.as_posix(),
        "args_builder": args_builder.as_posix(),
        "agent_review_prepare_pr": prepare.as_posix(),
        "contract_order": contract_order,
        **checks,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output", default="output/validation/real_product_intrinsic_capability_contract.json"
    )
    parser.add_argument("--markdown-output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
