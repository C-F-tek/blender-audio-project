#!/usr/bin/env python3
"""Build concrete advisory repository change proposals.

This tool is intentionally non-mutating. It reads local validation reports,
resource-lane reports and post-validation AI packets, then writes concrete
proposal JSON/Markdown that a human or trusted agent can review.

It never applies patches, never edits source files and never runs providers.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_OUTPUT_DIR = "output/ai_pipeline"
DEFAULT_BASENAME = "repository_change_proposals"

DEFAULT_REPORTS = (
    "output/validation/python_syntax.json",
    "output/validation/npu_pipeline_modules.json",
    "output/validation/npu_pipeline_helper_tests.json",
    "output/validation/npu_pipeline_docs.json",
    "output/validation/npu_runtime_output_manifest.json",
    "output/validation/local_ai_resource_lanes.json",
    "output/validation/execution_plan_status.json",
    "output/validation/validation_report_contract.json",
    "output/ai_pipeline/repository_update_suggestions.json",
)


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"exists": False, "path": str(path), "data": None, "error": "missing"}
    try:
        return {"exists": True, "path": str(path), "data": json.loads(path.read_text(encoding="utf-8-sig")), "error": ""}
    except Exception as exc:  # noqa: BLE001 - advisory report.
        return {"exists": True, "path": str(path), "data": None, "error": f"{type(exc).__name__}: {exc}"}


def report_by_kind(reports: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    by_kind: dict[str, dict[str, Any]] = {}
    for report in reports:
        data = report.get("data")
        if isinstance(data, dict):
            kind = str(data.get("kind") or Path(report["path"]).stem)
            by_kind[kind] = data
    return by_kind


def proposal(
    *,
    proposal_id: str,
    priority: str,
    area: str,
    title: str,
    rationale: str,
    target_files: list[str],
    change_type: str,
    sketch: list[str],
    validation: list[str],
    stop_conditions: list[str],
    do_not_touch: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "id": proposal_id,
        "priority": priority,
        "area": area,
        "title": title,
        "rationale": rationale,
        "target_files": target_files,
        "change_type": change_type,
        "apply_mode": "manual_review_only",
        "patch_sketch": sketch,
        "validation_commands": validation,
        "stop_conditions": stop_conditions,
        "do_not_touch": do_not_touch
        or [
            "runtime Blender files",
            "Ready To Jazz migration",
            "full analysis JSON",
            "generated indexes by hand",
            "provider execution behavior unless explicitly scoped",
        ],
    }


def build_proposals(reports: list[dict[str, Any]], *, profile: str) -> list[dict[str, Any]]:
    by_kind = report_by_kind(reports)
    proposals: list[dict[str, Any]] = []

    execution_plan_status = by_kind.get("execution_plan_status")
    if execution_plan_status and execution_plan_status.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-EXEC-PLAN-STATUS",
                priority="P1",
                area="execution_plans",
                title="Fix execution-plan folder/status drift",
                rationale="The execution-plan validator reports terminal-status plans in the wrong folder or invalid status markers.",
                target_files=["docs/EXECUTION_PLANS/active/", "docs/EXECUTION_PLANS/completed/", "docs/EXECUTION_PLANS/abandoned/"],
                change_type="docs_move_or_status_fix",
                sketch=[
                    "Move plans with top-level `## Status` = `completed` from active/ to completed/.",
                    "Move abandoned plans to abandoned/ or change their top-level status back to active/planned if still open.",
                    "Do not treat folder README.md files as execution plans.",
                ],
                validation=[
                    "python .\\Tools\\validation\\check_execution_plan_status.py --repo-root . --output .\\output\\validation\\execution_plan_status.json",
                    "python .\\Tools\\validation\\check_docs_links.py --repo-root . --output .\\output\\validation\\docs_links.json",
                ],
                stop_conditions=["Any moved plan has unclear status or contains active unfinished work."],
            )
        )

    npu_manifest = by_kind.get("npu_runtime_output_manifest")
    if npu_manifest and npu_manifest.get("blocked_count", 0):
        proposals.append(
            proposal(
                proposal_id="P-NPU-MANIFEST-BLOCKED-OUTPUTS",
                priority="P1",
                area="npu_observability",
                title="Review blocked NPU runtime output paths",
                rationale="The runtime-output manifest found paths outside the exact legacy output allowlist.",
                target_files=["Tools/npu/build_runtime_output_manifest.py", "Tools/npu/pipeline/artifact_paths.py", "docs/JSON_SCHEMAS.md"],
                change_type="policy_review",
                sketch=[
                    "Inspect each blocked output path in `output/validation/npu_runtime_output_manifest.json`.",
                    "If the path is a legitimate legacy runtime output, add it to the exact allowlist with a focused test.",
                    "If not legitimate, keep it blocked and document why.",
                ],
                validation=[
                    "python .\\Tools\\npu\\build_runtime_output_manifest.py --repo-root . --output .\\output\\validation\\npu_runtime_output_manifest.json",
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1",
                ],
                stop_conditions=["A blocked path points to source code, full analysis JSON or an unreviewed generated destination."],
            )
        )

    resource_lanes = by_kind.get("local_ai_resource_lanes")
    if resource_lanes:
        ready = set(resource_lanes.get("ready_lanes") or [])
        available = set(resource_lanes.get("available_lanes") or [])
        if {"npu", "gpu", "ollama"} - ready:
            proposals.append(
                proposal(
                    proposal_id="P-RESOURCE-LANE-PREFLIGHTS",
                    priority="P2",
                    area="local_ai_resources",
                    title="Stabilize local NPU/GPU/Ollama resource-lane readiness",
                    rationale="One or more local AI resource lanes are unavailable or not ready. Keeping this as observability improves future parallel pipeline work.",
                    target_files=["Tools/ai/check_local_resource_lanes.py", "Tools/workflow/run_post_validation_ai_packet.ps1", "Tools/validation/README.md"],
                    change_type="preflight_hardening",
                    sketch=[
                        f"Ready lanes currently reported: {sorted(ready)}.",
                        f"Available lanes currently reported: {sorted(available)}.",
                        "Keep missing lanes as warnings unless explicitly required with `--require-lane`.",
                        "Add narrower diagnostics for lanes that are available but not ready.",
                    ],
                    validation=[
                        "python .\\Tools\\ai\\check_local_resource_lanes.py --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
                        "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_post_validation_ai_packet.ps1 -Profile npu -ReportFile output/validation/local_ai_resource_lanes.json",
                    ],
                    stop_conditions=["A lane probe would need long generation, Blender execution, GPU render or provider behavior changes."],
                )
            )

    validation_contract = by_kind.get("validation_report_contract")
    if validation_contract and validation_contract.get("passed") is False:
        proposals.append(
            proposal(
                proposal_id="P-REPORT-CONTRACT-CONSISTENCY",
                priority="P1",
                area="validation_contracts",
                title="Normalize validation report root fields",
                rationale="The validation-report contract checker found reports missing common fields or using inconsistent types.",
                target_files=["Tools/validation/*.py", "Tools/npu/pipeline/reports.py", "docs/JSON_SCHEMAS.md"],
                change_type="contract_normalization",
                sketch=[
                    "Add missing root fields additively: schema_version, kind, repo_root, passed, errors, warnings where applicable.",
                    "Do not remove validator-specific fields.",
                    "Keep strict mode opt-in until all local reports are aligned.",
                ],
                validation=[
                    "python .\\Tools\\validation\\check_validation_report_contract.py --repo-root . --output .\\output\\validation\\validation_report_contract.json",
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_local_validation_after_refactor.ps1 -SkipPull -ContinueOnError -MatrixWorkers 12 -RepeatCases 2",
                ],
                stop_conditions=["A proposed normalization would change the meaning of existing report fields."],
            )
        )

    if not proposals:
        proposals.append(
            proposal(
                proposal_id="P-NEXT-NPU-OBSERVABILITY",
                priority="P2",
                area="npu_backend",
                title="Add additive NPU observability before provider execution changes",
                rationale="Current reports do not indicate blocking failures. The next safe app-agnostic step is deeper observability, not provider behavior changes.",
                target_files=[
                    "Tools/npu/build_runtime_output_manifest.py",
                    "Tools/ai/check_local_resource_lanes.py",
                    "Tools/ai/suggest_repository_updates.py",
                    "docs/JSON_SCHEMAS.md",
                    "Tools/validation/README.md",
                ],
                change_type="observability_extension",
                sketch=[
                    "Include runtime-output manifest and resource-lane reports in the default NPU packet profile.",
                    "Add proposal generation output next to packet JSON/Markdown.",
                    "Keep every output advisory and generated under output/.",
                ],
                validation=[
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_npu_pipeline_helper_validation.ps1",
                    "python .\\Tools\\ai\\check_local_resource_lanes.py --repo-root . --parallel --output .\\output\\validation\\local_ai_resource_lanes.json --markdown-output .\\output\\validation\\local_ai_resource_lanes.md",
                    "powershell.exe -ExecutionPolicy Bypass -File .\\Tools\\workflow\\run_post_validation_ai_packet.ps1 -Profile npu -OutputDir output/ai_packets -Basename npu_after_tests -ReportFile output/validation/local_ai_resource_lanes.json -ReportFile output/validation/npu_runtime_output_manifest.json",
                ],
                stop_conditions=["Any change requires modifying provider execution, prompt prose, Blender runtime or generated indexes manually."],
            )
        )

    return proposals


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Repository Change Proposals", ""]
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Profile: `{report['profile']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Proposal count: `{len(report['proposals'])}`")
    lines.append("")
    for item in report["proposals"]:
        lines.append(f"## {item['id']} — {item['title']}")
        lines.append("")
        lines.append(f"- Priority: `{item['priority']}`")
        lines.append(f"- Area: `{item['area']}`")
        lines.append(f"- Change type: `{item['change_type']}`")
        lines.append(f"- Apply mode: `{item['apply_mode']}`")
        lines.append(f"- Rationale: {item['rationale']}")
        lines.append("")
        lines.append("### Target files")
        for path in item["target_files"]:
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("### Patch sketch")
        for step in item["patch_sketch"]:
            lines.append(f"- {step}")
        lines.append("")
        lines.append("### Validation")
        for command in item["validation_commands"]:
            lines.append(f"- `{command}`")
        lines.append("")
        lines.append("### Stop conditions")
        for condition in item["stop_conditions"]:
            lines.append(f"- {condition}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("These are proposals only. They must not be auto-applied without explicit review.")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--profile", default="core")
    parser.add_argument("--output-dir", default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--basename", default=DEFAULT_BASENAME)
    parser.add_argument("--report-file", action="append", default=[])
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report_paths = list(DEFAULT_REPORTS) + list(args.report_file or [])
    loaded_reports = [read_json_if_exists(repo_root / path) for path in dict.fromkeys(report_paths)]
    proposals = build_proposals(loaded_reports, profile=args.profile)

    output_dir = repo_root / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    output_json = output_dir / f"{args.basename}.json"
    output_md = output_dir / f"{args.basename}.md"

    report = {
        "schema_version": 1,
        "kind": "repository_change_proposals",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "profile": args.profile,
        "passed": True,
        "errors": [],
        "warnings": [],
        "apply_mode": "manual_review_only",
        "reports_read": [item["path"] for item in loaded_reports],
        "proposals": proposals,
    }

    output_json.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    output_md.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps({"passed": True, "json": str(output_json), "markdown": str(output_md), "proposal_count": len(proposals)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
