#!/usr/bin/env python3
"""Smoke-test provider execution detection for external heap adapters.

The historical failure mode is a real provider/NPU workload represented only in
provider text, for example "performed=True", while downstream artifacts expose
provider_execution_performed=false. This smoke keeps the test bounded and does
not execute providers, Blender, SQLite or patch application.
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# External Heap Provider Execution Detection Smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Pointer provider execution: `{report['checks']['pointer_provider_execution']}`",
        f"- Composer provider execution: `{report['checks']['composer_provider_execution']}`",
        f"- Causality provider execution: `{report['checks']['causality_provider_execution']}`",
        "",
        "## Errors",
        "",
    ]
    errors = report.get("errors") or []
    lines.extend(f"- {item}" for item in errors) if errors else lines.append("- none")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--output",
        default="output/validation/external_heap_provider_execution_detection_smoke.json",
    )
    parser.add_argument(
        "--markdown-output",
        default="output/validation/external_heap_provider_execution_detection_smoke.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    sys.path.insert(0, str(repo_root))

    from ia_carmine.runtime.external_heap.block_pointer_manifest import cli as pointer_manifest
    from ia_carmine.product.heap_final_proposals import artifacts as legacy_composer
    from ia_carmine.product.heap_final_proposals.normalize_final_causality import cli as causality_normalizer

    smoke_dir = (
        repo_root / "output" / "validation" / "external_heap_provider_execution_detection_smoke_run"
    )
    shutil.rmtree(smoke_dir, ignore_errors=True)
    provider_dir = smoke_dir / "provider_teamwork"
    provider_dir.mkdir(parents=True, exist_ok=True)
    provider_payload = {
        "schema_version": 1,
        "kind": "npu_micro_task_auditor",
        "lane": "npu_micro_task_auditor",
        "passed": True,
        "provider_compute_device": "openvino/NPU",
        "provider_device_verified": True,
        "npu_peer_evidence_verified": True,
        "npu_micro_provider_model_loaded": True,
        "npu_micro_provider_execution_performed": True,
        "npu_device_workload_performed": True,
        "npu_response_schema_valid": True,
        "npu_peer_followup_required": False,
        "provider_execution_performed": None,
        "response_text": "NPU micro-task eseguita. Workload NPU reale richiesto: performed=True, passed=True, iterations=42, seconds=0.01.",
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    write_json(provider_dir / "npu_micro_task_auditor.json", provider_payload)

    pointer_report = pointer_manifest.build_report(
        repo_root, smoke_dir, max_block_chars=9000, max_blocks=0
    )
    composer_provider_reports = legacy_composer.list_provider_reports(smoke_dir)
    composer = {
        "provider_execution_performed": False,
        "provider_report_count": len(composer_provider_reports),
        "proposal_count": 0,
        "gpu0_review_count": 0,
        "npu_audit_count": 1,
        "provider_reports": [
            {
                "path": str(item.get("path") or ""),
                "kind": item.get("kind"),
                "lane": item.get("lane"),
                "passed": item.get("passed"),
                "provider_execution_performed": item.get("provider_execution_performed"),
                "response_text": item.get("response_text"),
            }
            for item in composer_provider_reports
        ],
        "npu_audits": [
            {
                "provider_execution_performed": None,
                "summary": provider_payload["response_text"],
            }
        ],
        "product_status": "blocked_with_reason",
        "quality_output_passed": False,
        "accepted_proposal_count": 0,
        "rejected_proposal_count": 0,
        "blocking_issues": ["smoke blocked product"],
    }
    causality_report = causality_normalizer.build_report(
        composer, smoke_dir / "heap_final_proposal_composer.json"
    )

    checks = {
        "pointer_provider_execution": pointer_report.get("provider_execution_performed") is True,
        "composer_provider_execution": bool(
            composer_provider_reports
            and composer_provider_reports[0].get("provider_execution_performed") is True
        ),
        "causality_provider_execution": causality_report.get("provider_execution_performed")
        is True,
        "no_patch_application": pointer_report.get("patch_application_performed") is False,
        "no_source_writes": pointer_report.get("source_writes_performed") is False,
    }
    errors = [name for name, passed in checks.items() if not passed]
    report = {
        "schema_version": 1,
        "kind": "external_heap_provider_execution_detection_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "output_artifact_writes_performed": True,
        "checks": checks,
        "errors": errors,
        "warnings": [],
    }
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    markdown = Path(args.markdown_output)
    if not markdown.is_absolute():
        markdown = repo_root / markdown
    write_json(output, report)
    write_markdown(markdown, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
