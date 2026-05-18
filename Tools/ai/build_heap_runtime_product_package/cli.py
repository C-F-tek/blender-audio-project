#!/usr/bin/env python3
"""Build the heap-runtime final product package.

The package is intentionally deterministic and provider-free: it composes the
reports and artifacts already produced by the heap/team runtime, broker,
telemetry, recommendations and patch-plan lanes into a small product surface
that downstream bundle builders can consume.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.report_utils import write_json_report
except ImportError:
    from Tools.validation._shared.report_utils import (  # type: ignore
        write_json_report,
    )


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()


def resolve_repo_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists() or not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def compact_report(path: Path, repo_root: Path) -> dict[str, Any]:
    data = read_json(path)
    item: dict[str, Any] = {
        "path": repo_rel(path, repo_root),
        "exists": path.exists(),
        "json_ok": data is not None,
        "kind": data.get("kind") if data else None,
        "passed": data.get("passed") if data else None,
        "provider_execution_performed": (
            data.get("provider_execution_performed") if data else None
        ),
        "patch_application_performed": (data.get("patch_application_performed") if data else None),
        "source_writes_performed": (data.get("source_writes_performed") if data else None),
        "errors": (data.get("errors") if data else []) or [],
        "warnings": (data.get("warnings") if data else []) or [],
    }
    if data and isinstance(data.get("metrics"), dict):
        item["metrics"] = {
            key: data["metrics"].get(key)
            for key in (
                "heap_read_count",
                "heap_write_count",
                "tool_request_count",
                "tool_execution_count",
                "decision_count",
                "candidate_operation_count",
                "product_status",
            )
            if key in data["metrics"]
        }
    if data and isinstance(data.get("state"), dict):
        product = data["state"].get("product")
        if isinstance(product, dict):
            item["product"] = {
                "required": product.get("required"),
                "status": product.get("status"),
                "reason": product.get("reason"),
            }
    return item


def compact_artifact(path: Path, repo_root: Path) -> dict[str, Any]:
    item: dict[str, Any] = {
        "path": repo_rel(path, repo_root),
        "exists": path.exists(),
        "suffix": path.suffix.lower(),
        "size_bytes": path.stat().st_size if path.exists() and path.is_file() else None,
    }
    if (
        path.exists()
        and path.is_file()
        and path.suffix.lower() in {".md", ".txt", ".json", ".jsonl", ".mmd"}
    ):
        text = path.read_text(encoding="utf-8-sig", errors="replace")
        item["preview"] = text[:1200]
        item["preview_chars"] = min(len(text), 1200)
    return item


def infer_product_status(reports: list[dict[str, Any]]) -> tuple[str, str, list[str]]:
    errors: list[str] = []
    if not reports:
        return (
            "blocked_with_reason",
            "no run reports supplied",
            ["no run reports supplied"],
        )

    failed = [item for item in reports if item.get("passed") is False]
    explicit_ready = [
        item
        for item in reports
        if isinstance(item.get("metrics"), dict)
        and item["metrics"].get("product_status") in {"ready", "blocked_with_reason"}
    ]
    product_items = [
        item
        for item in reports
        if isinstance(item.get("product"), dict)
        and item["product"].get("status") in {"ready", "blocked_with_reason"}
    ]

    if failed:
        errors.append(f"{len(failed)} supplied report(s) are failed")
        return "blocked_with_reason", "one or more source reports failed", errors
    if explicit_ready:
        status = explicit_ready[-1]["metrics"].get("product_status")
        reason = f"heap runtime report declared product_status={status}"
        return str(status), reason, []
    if product_items:
        product = product_items[-1]["product"]
        return (
            str(product.get("status")),
            str(product.get("reason") or "product status supplied by source report"),
            [],
        )
    return "ready", "all supplied reports are readable and non-failing", []


def write_manifest(output_dir: Path, report: dict[str, Any]) -> dict[str, Any]:
    manifest = {
        "schema_version": 1,
        "kind": "heap_runtime_product_manifest",
        "generated_at": report["generated_at"],
        "passed": report["passed"],
        "product_status": report["product_status"],
        "output": report["output"],
        "report_count": len(report["reports"]),
        "artifact_count": len(report["artifacts"]),
        "reports": [item["path"] for item in report["reports"]],
        "artifacts": [item["path"] for item in report["artifacts"]],
        "guardrails": report["guardrails"],
    }
    (output_dir / "heap_runtime_product_manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return manifest


def write_evidence_index(output_dir: Path, report: dict[str, Any]) -> dict[str, Any]:
    evidence = {
        "schema_version": 1,
        "kind": "heap_runtime_product_evidence_index",
        "generated_at": report["generated_at"],
        "passed": report["passed"],
        "product_status": report["product_status"],
        "report_summaries": report["reports"],
        "artifact_manifest": report["artifacts"],
    }
    (output_dir / "heap_runtime_product_evidence_index.json").write_text(
        json.dumps(evidence, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return evidence


def write_readiness(output_dir: Path, report: dict[str, Any]) -> dict[str, Any]:
    readiness = {
        "schema_version": 1,
        "kind": "heap_runtime_product_readiness",
        "generated_at": report["generated_at"],
        "passed": report["passed"],
        "product_status": report["product_status"],
        "ready_for_review": report["product_status"] == "ready" and report["passed"],
        "reason": report["product_reason"],
        "errors": report["errors"],
        "warnings": report["warnings"],
    }
    (output_dir / "heap_runtime_product_readiness.json").write_text(
        json.dumps(readiness, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return readiness


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Runtime Product Package",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Product status: `{report.get('product_status')}`",
        f"- Reason: {report.get('product_reason')}",
        f"- Report count: `{len(report.get('reports') or [])}`",
        f"- Artifact count: `{len(report.get('artifacts') or [])}`",
        "",
        "## Reports",
        "",
    ]
    for item in report.get("reports") or []:
        lines.append(
            f"- `{item.get('path')}` kind=`{item.get('kind')}` passed=`{item.get('passed')}`"
        )
    lines.extend(["", "## Artifacts", ""])
    for item in report.get("artifacts") or []:
        lines.append(
            f"- `{item.get('path')}` exists=`{item.get('exists')}` size=`{item.get('size_bytes')}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return "\n".join(lines) + "\n"


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    output_dir = resolve_repo_path(repo_root, args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_paths = [resolve_repo_path(repo_root, value) for value in args.run_report]
    artifact_paths = [resolve_repo_path(repo_root, value) for value in args.run_artifact]

    reports = [compact_report(path, repo_root) for path in report_paths if str(path).strip()]
    artifacts = [compact_artifact(path, repo_root) for path in artifact_paths if str(path).strip()]

    missing_reports = [item["path"] for item in reports if not item["exists"]]
    warnings = [f"missing run report: {path}" for path in missing_reports]
    product_status, product_reason, status_errors = infer_product_status(
        [item for item in reports if item["exists"]]
    )

    errors = list(status_errors)
    passed = not errors and product_status in {"ready", "blocked_with_reason"}

    output_path = resolve_repo_path(repo_root, args.output)
    report = {
        "schema_version": 1,
        "kind": "heap_runtime_product_package",
        "generated_at": now_iso(),
        "repo_root": repo_root.as_posix(),
        "request": args.request,
        "output": repo_rel(output_path, repo_root),
        "output_dir": repo_rel(output_dir, repo_root),
        "passed": passed,
        "product_status": product_status,
        "product_reason": product_reason,
        "reports": reports,
        "artifacts": artifacts,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
        "guardrails": {
            "deterministic_composition_only": True,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "raw_output_commit_allowed": False,
        },
    }
    write_manifest(output_dir, report)
    write_evidence_index(output_dir, report)
    write_readiness(output_dir, report)
    report["manifest"] = repo_rel(output_dir / "heap_runtime_product_manifest.json", repo_root)
    report["evidence_index"] = repo_rel(
        output_dir / "heap_runtime_product_evidence_index.json", repo_root
    )
    report["readiness"] = repo_rel(output_dir / "heap_runtime_product_readiness.json", repo_root)

    (output_dir / "heap_runtime_product.md").write_text(render_markdown(report), encoding="utf-8")
    (output_dir / "README.md").write_text(
        "# Heap Runtime Product Package\n\n"
        "Deterministic product package built from heap/runtime reports and artifacts.\n"
        "Raw runtime artifacts remain under output/** and are not commit targets.\n",
        encoding="utf-8",
    )
    write_json_report(report, output_path)
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--request", default="")
    parser.add_argument("--output", required=True)
    parser.add_argument("--run-report", action="append", default=[])
    parser.add_argument("--run-artifact", action="append", default=[])
    parser.add_argument("--no-external-probes", action="store_true")
    parser.add_argument("--timeout-seconds", type=int, default=8)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = build_report(args)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
