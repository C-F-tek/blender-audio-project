#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import resolve_output_path, write_json_report  # type: ignore


STAMP = "20990101-010203"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def run(cmd: list[str], cwd: Path) -> dict[str, Any]:
    proc = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False)
    return {
        "command": cmd,
        "returncode": proc.returncode,
        "stdout_tail": proc.stdout[-3000:],
        "stderr_tail": proc.stderr[-3000:],
    }


def seed_repo(repo: Path) -> None:
    (repo / "Tools/validation").mkdir(parents=True)
    (repo / "Tools/ai").mkdir(parents=True)
    (repo / "Tools/validation/README.md").write_text("# Validation\n", encoding="utf-8")
    (repo / "Tools/ai/repository_product/repository_change_proposals/cli.py").write_text(
        "# placeholder\n", encoding="utf-8"
    )
    (repo / "Tools/ai/generated_patch_specs/proposal_cli.py").write_text(
        "# placeholder\n", encoding="utf-8"
    )
    run(["git", "init"], repo)
    run(["git", "config", "user.email", "smoke@example.invalid"], repo)
    run(["git", "config", "user.name", "Smoke"], repo)
    run(["git", "add", "."], repo)
    run(["git", "commit", "-m", "init"], repo)


def seed_runtime_reports(repo: Path) -> None:
    write_json(
        repo / f"output/validation/openvino_gpu0_provider_support_{STAMP}.json",
        {
            "schema_version": 1,
            "kind": "openvino_gpu0_secondary_workload",
            "Stamp": STAMP,
            "passed": True,
            "openvino_gpu0_observable_workload_passed": True,
        },
    )
    write_json(
        repo / f"output/validation/npu_micro_task_companion_report_{STAMP}.json",
        {
            "schema_version": 2,
            "kind": "npu_micro_task_companion_report",
            "Stamp": STAMP,
            "passed": True,
            "npu_peer_activity_requested": True,
            "npu_peer_activity_performed": False,
            "npu_device_execution_performed": False,
            "npu_activity_classification": "diagnostic_report_only",
        },
    )
    run_dir = repo / f"output/local_ai_runs/{STAMP}_unified/ai_packets"
    write_json(
        run_dir / "heap_exchange_runtime_entry.json",
        {
            "schema_version": 1,
            "kind": "heap_exchange_runtime_entry",
            "Stamp": STAMP,
            "passed": True,
        },
    )
    write_json(
        run_dir / "heap_peer_runtime_manifest.json",
        {
            "schema_version": 1,
            "kind": "heap_peer_runtime_manifest",
            "Stamp": STAMP,
            "passed": True,
            "peers": ["gpu1", "gpu0", "npu"],
        },
    )
    write_json(
        repo / f"output/validation/runtime_evidence_correlation_{STAMP}.json",
        {
            "schema_version": 1,
            "kind": "runtime_evidence_correlation",
            "stamp": STAMP,
            "passed": True,
        },
    )
    write_json(
        run_dir / "heap_exchange_runtime_exit_product.json",
        {
            "schema_version": 1,
            "kind": "heap_exchange_runtime_exit_product",
            "stamp": STAMP,
            "passed": False,
            "operation_count": 0,
            "concrete_operation_count": 0,
        },
    )
    write_json(
        repo / f"output/validation/heap_exchange_runtime_lifecycle_{STAMP}.json",
        {
            "schema_version": 1,
            "kind": "heap_exchange_runtime_lifecycle",
            "stamp": STAMP,
            "passed": False,
            "concrete_exit_required": True,
        },
    )
    write_json(
        repo / "output/validation/generated_patch_specs_review_pr_apply.json",
        {
            "schema_version": 1,
            "kind": "patch_suggestion_bundle_apply",
            "generated_at": "2099-01-01T01:02:03",
            "passed": False,
            "manifest": {
                "path": f"output/patch_specs/{STAMP}_proposal_patch_specs_manifest.json",
                "discovery_filter_stamp": STAMP,
            },
            "loaded_specs": [
                {"path": f"output/patch_specs/{STAMP}_proposal_patch_specs/P-EMPTY.json"}
            ],
            "operation_count": 0,
            "changed_count": 0,
            "manual_review_items": [
                {
                    "id": "P-EMPTY",
                    "reason": "metadata-only draft operation has no concrete replacements",
                    "target_files": ["Tools/validation/README.md"],
                }
            ],
        },
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/repository_change_proposals_runtime_evidence_smoke.json",
    )
    args = parser.parse_args()

    source_repo = Path(args.repo_root).resolve()
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="runtime-evidence-proposals-smoke-") as temp_dir:
        repo = Path(temp_dir) / "repo"
        repo.mkdir(parents=True)
        seed_repo(repo)
        seed_runtime_reports(repo)

        proposals = run(
            [
                "python",
                str(source_repo / "Tools/ai/repository_product/repository_change_proposals/cli.py"),
                "--repo-root",
                str(repo),
                "--profile",
                "core",
                "--runtime-report-stamp",
                STAMP,
                "--output-dir",
                "output/ai_pipeline",
                "--basename",
                f"{STAMP}_repository_change_proposals",
            ],
            repo,
        )
        proposal_json = repo / "output/ai_pipeline" / f"{STAMP}_repository_change_proposals.json"
        proposal_report = json.loads(proposal_json.read_text(encoding="utf-8"))

        specs = run(
            [
                "python",
                str(source_repo / "Tools/ai/generated_patch_specs/proposal_cli.py"),
                "--repo-root",
                str(repo),
                "--proposal",
                str(proposal_json),
                "--output-dir",
                "output/patch_specs",
                "--basename",
                f"{STAMP}_proposal_patch_specs",
            ],
            repo,
        )
        manifest = repo / "output/patch_specs" / f"{STAMP}_proposal_patch_specs_manifest.json"
        manifest_report = json.loads(manifest.read_text(encoding="utf-8"))

        apply_report_path = repo / "output/validation/apply.json"
        applied = run(
            [
                "python",
                str(source_repo / "Tools/ai/generated_patch_specs/apply_cli.py"),
                "--repo-root",
                str(repo),
                "--manifest",
                str(manifest),
                "--output",
                str(apply_report_path),
                "--apply",
                "--allow-dirty",
                "--create-review-branch",
                "codex/runtime-evidence-smoke",
                "--allow-dirty-branch",
            ],
            repo,
        )
        apply_report = json.loads(apply_report_path.read_text(encoding="utf-8"))

    proposal_ids = [
        item.get("id") for item in proposal_report.get("proposals", []) if isinstance(item, dict)
    ]
    if proposals["returncode"] != 0:
        errors.append("repository change proposal builder failed")
    if "P-RUNTIME-PEER-EVIDENCE-FEED" not in proposal_ids:
        errors.append("runtime peer evidence proposal was not emitted")
    if "P-NEXT-NPU-OBSERVABILITY" in proposal_ids:
        errors.append("runtime evidence should avoid fallback P-NEXT-NPU-OBSERVABILITY")
    if specs["returncode"] != 0:
        errors.append("patch spec builder failed")
    if manifest_report.get("concrete_spec_count", 0) < 1:
        errors.append("patch spec manifest did not contain concrete operations")
    if applied["returncode"] != 0:
        errors.append(
            "generated patch spec apply should succeed with concrete runtime-evidence proposal"
        )
    runtime_summary = (
        (proposal_report.get("proposals") or [{}])[0].get("evidence_summary") or {}
    ).get("runtime_peer_evidence") or {}
    if not runtime_summary.get("latest_apply_report_path", "").endswith(
        "generated_patch_specs_review_pr_apply.json"
    ):
        errors.append(
            "proposal builder did not discover nested-stamp generated patch-spec apply report"
        )
    if not runtime_summary.get("heap_exit_product_present"):
        errors.append("proposal builder did not discover heap exchange exit product")
    if not runtime_summary.get("heap_lifecycle_present"):
        errors.append("proposal builder did not discover heap exchange lifecycle report")
    if apply_report.get("operation_count", 0) < 1:
        errors.append("apply report did not include concrete operation")
    if apply_report.get("changed_count", 0) < 1:
        errors.append("apply report did not change a reviewable source/doc file")
    metadata_manual_items = [
        item
        for item in apply_report.get("manual_review_items") or []
        if isinstance(item, dict) and "metadata-only" in str(item.get("reason") or "")
    ]
    if metadata_manual_items:
        errors.append(
            "concrete runtime-evidence specs should not retain metadata-only companion operations"
        )

    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "repository_change_proposals_runtime_evidence_smoke",
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "cases": {
            "proposals": proposals,
            "specs": specs,
            "apply": applied,
        },
        "proposal_ids": proposal_ids,
        "manifest": manifest_report,
        "apply_report": apply_report,
        "errors": errors,
        "warnings": [],
    }
    print(write_json_report(report, resolve_output_path(source_repo, args.output)), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
