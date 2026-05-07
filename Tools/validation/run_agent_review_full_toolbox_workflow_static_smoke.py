#!/usr/bin/env python3
"""Static smoke-test for the full toolbox decision-loop workflow script."""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore

DEFAULT_WORKFLOW = "Tools/workflow/run_agent_review_full_toolbox_decision_loop.ps1"
DEFAULT_OUTPUT = "output/validation/agent_review_full_toolbox_workflow_static_smoke.json"
DEFAULT_MARKDOWN = "output/validation/agent_review_full_toolbox_workflow_static_smoke.md"

REQUIRED_TOKENS = {
    "python_control_shim": "run_agent_review_full_toolbox_decision_loop.py",
    "python_engine_package": "py_engine",
    "python_mesh_package": "py_mesh",
    "python_product_package": "py_product",
    "legacy_powershell_fallback_explicit": "UseLegacyPowerShellImplementation",
    "explicit_provider_flag": "[switch]$RunGpuNpuProvider",
    "explicit_legacy_npu_auditor_flag": "[switch]$RunLegacyNpuAuditorProvider",
    "gpu0_peer_support_provider": "--run-gpu0-peer-support-provider",
    "npu_micro_support_provider": "--run-npu-micro-support-provider",
    "npu_micro_start_mode": "NpuMicroStartMode",
    "npu_peer_deferred_placeholder": "write_npu_peer_nonblocking_placeholder",
    "npu_micro_start_mode_workflow": "NpuMicroStartMode",
    "npu_micro_deferred_warning": "provider mesh keeps NPU off the live GPU1/GPU0 critical path",
    "openvino_hardware_governance": "build_openvino_hardware_governance_report.py",
    "runtime_heap_to_orchestrator": "--runtime-heap-stamp",
    "gpu0_support_strict_contract": "--require-openvino-gpu0-secondary",
    "memory_reload_reuse": "run_full_memory_tool_regeneration.ps1",
    "line_count_reuse": "build_python_line_count_csv.py",
    "code_interpreter_reuse": "build_code_interpreter_report",
    "gpu_npu_orchestrator_reuse": "run_agent_gpu_npu_parallel_orchestrator.py",
    "decision_loop_reuse": "run_agent_review_decision_loop.py",
    "post_validation_packet_reuse": "run_post_validation_ai_packet.ps1",
    "shared_toolbox_bundle_reuse": "build_shared_toolbox_ai_to_ai_bundle",
    "final_tool_product_reuse": "build_full0to10_final_tool_product.py",
    "patch_notes_quality_product": "build_patch_notes_quality_product.py",
    "task_markdown_input": "TaskMarkdown",
    "github_evidence_bundle_reuse": "build_github_evidence_bundle",
    "bundle_validation_reuse": "check_github_evidence_bundle",
    "scoped_validation_contract": "check_validation_report_contract.py",
    "report_only_guardrail": "patch_application_performed",
    "sqlite_guardrail": "sqlite_write_performed",
    "persistent_memory_guardrail": "persistent_memory_write_performed",
    "raw_output_guardrail": "raw_output_commit_allowed",
}

FORBIDDEN_TOKENS = {
    "git_commit": "git commit",
    "git_push": "git push",
    "patch_apply": "Apply-Patch",
    "blender_runtime": "blender.exe",
    "sqlite_mutation_literal": "--action write",
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Agent Review Full Toolbox Workflow Static Smoke", ""]
    lines.append(f"- Passed: `{report['passed']}`")
    lines.append(f"- Workflow: `{report['workflow']}`")
    lines.append(f"- Inspected file count: `{len(report.get('inspected_files', []))}`")
    lines.append(f"- Required token count: `{report['required_token_count']}`")
    lines.append(f"- Missing token count: `{report['missing_token_count']}`")
    lines.append(f"- Forbidden token hit count: `{report['forbidden_token_hit_count']}`")
    lines.append(f"- Provider execution performed: `{report['provider_execution_performed']}`")
    lines.append(f"- Patch application performed: `{report['patch_application_performed']}`")
    if report.get("errors"):
        lines.append("")
        lines.append("## Errors")
        lines.append("")
        for error in report["errors"]:
            lines.append(f"- {error}")
    if report.get("warnings"):
        lines.append("")
        lines.append("## Warnings")
        lines.append("")
        for warning in report["warnings"]:
            lines.append(f"- {warning}")
    return "\n".join(lines) + "\n"


def run_smoke(repo_root: Path, workflow_value: str) -> dict[str, Any]:
    workflow = Path(workflow_value)
    if not workflow.is_absolute():
        workflow = repo_root / workflow
    errors: list[str] = []
    warnings: list[str] = []
    text = ""
    inspected_files: list[str] = []
    if not workflow.exists():
        errors.append(f"missing workflow: {rel(workflow, repo_root)}")
    else:
        inspected_files.append(rel(workflow, repo_root))
        workflow_texts = [workflow.read_text(encoding="utf-8-sig", errors="replace")]
        implementation = workflow.with_suffix("") / "main.ps1"
        python_runner = workflow.with_suffix(".py")
        engine_dir = workflow.with_suffix("")
        engine_modules = sorted(engine_dir.glob("py_*.py")) if engine_dir.exists() else []
        for candidate in (python_runner, implementation, *engine_modules):
            if candidate.exists():
                inspected_files.append(rel(candidate, repo_root))
                workflow_texts.append(candidate.read_text(encoding="utf-8-sig", errors="replace"))
        text = "\n".join(workflow_texts)

    missing = []
    for name, token in REQUIRED_TOKENS.items():
        if token not in text:
            missing.append(name)
            errors.append(f"missing required token {name}: {token}")

    forbidden_hits = []
    lower_text = text.lower()
    for name, token in FORBIDDEN_TOKENS.items():
        if token.lower() in lower_text:
            forbidden_hits.append(name)
            errors.append(f"forbidden token present {name}: {token}")

    if "--run-npu-auditor-provider" in text and "if ($RunLegacyNpuAuditorProvider)" not in text:
        errors.append("legacy NPU provider auditor flag must stay gated by -RunLegacyNpuAuditorProvider")

    if "provider_execution_performed = [bool]$RunGpuNpuProvider" not in text and '"provider_execution_performed": bool(ctx.args.RunGpuNpuProvider)' not in text:
        errors.append("workflow report must expose provider_execution_performed from explicit flag state")

    if "evidence_to_commit" not in text:
        errors.append("workflow must publish evidence_to_commit so users do not stage output/**")

    if "Do not stage output/**" not in text:
        warnings.append("workflow should print explicit output/** staging warning")

    return {
        "schema_version": 1,
        "kind": "agent_review_full_toolbox_workflow_static_smoke",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "workflow": rel(workflow, repo_root),
        "inspected_files": inspected_files,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "sqlite_write_performed": False,
        "persistent_memory_write_performed": False,
        "manual_review_required": True,
        "required_token_count": len(REQUIRED_TOKENS),
        "missing_token_count": len(missing),
        "missing_tokens": missing,
        "forbidden_token_hit_count": len(forbidden_hits),
        "forbidden_token_hits": forbidden_hits,
        "guardrails": {
            "static_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "sqlite_write_performed": False,
            "persistent_memory_write_performed": False,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--workflow", default=DEFAULT_WORKFLOW)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = run_smoke(repo_root, args.workflow)
    output = resolve_output_path(repo_root, args.output)
    markdown_output = resolve_output_path(repo_root, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown_output)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
