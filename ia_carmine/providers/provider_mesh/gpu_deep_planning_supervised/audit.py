from __future__ import annotations

from .common import *  # noqa: F403

def checkpoint_paths(checkpoint_dir: Path, round_index: int) -> tuple[Path, Path, Path]:
    base = checkpoint_dir / f"round_{round_index:03d}"
    return (
        base.with_suffix(".json"),
        base.with_suffix(".md"),
        base.with_name(base.name + "_npu_audit.json"),
    )

def run_npu_audit_for_checkpoint(
    repo_root: Path, checkpoint_json: Path, audit_json: Path, args: argparse.Namespace
) -> dict[str, Any]:
    command = [
        sys.executable,
        "ia_carmine/providers/provider_mesh/npu_gpu_deep_review_auditor/cli.py",
        "--repo-root",
        ".",
        "--gpu-review",
        str(checkpoint_json),
        "--output",
        str(audit_json),
        "--markdown-output",
        str(audit_json.with_suffix(".md")),
        "--context-output",
        str(audit_json.with_name(audit_json.stem + "_context.md")),
        "--npu-output",
        str(audit_json.with_name(audit_json.stem + "_npu.md")),
        "--npu-notes-output",
        str(audit_json.with_name(audit_json.stem + "_npu_notes.md")),
        "--npu-metadata-output",
        str(audit_json.with_name(audit_json.stem + "_metadata.json")),
        "--timeout-seconds",
        str(args.npu_auditor_timeout_seconds),
    ]
    if args.run_npu_auditor_provider:
        command.append("--run-npu")
    else:
        command.extend(["--run-npu", "--metadata-only"])
    returncode, stdout, stderr, error = run_command(
        command, repo_root, args.npu_auditor_timeout_seconds + 30
    )
    audit: dict[str, Any] = {
        "checkpoint": repo_rel(checkpoint_json, repo_root),
        "audit_output": repo_rel(audit_json, repo_root),
        "returncode": returncode,
        "stdout_tail": stdout,
        "stderr_tail": stderr,
        "error": error or "",
        "blocking": False,
        "classification": "missing_audit_output",
        "provider_execution_requested": bool(args.run_npu_auditor_provider),
        "provider_load_attempted": False,
        "provider_execution_succeeded": False,
        "provider_execution_performed": False,
        "dependency_missing": False,
    }
    if audit_json.exists():
        try:
            data = read_json(audit_json)
            nested = data.get("npu_auditor", {})
            audit.update(
                {
                    "kind": data.get("kind"),
                    "passed": data.get("passed"),
                    "provider_execution_requested": data.get(
                        "provider_execution_requested",
                        nested.get("provider_execution_requested"),
                    ),
                    "provider_load_attempted": data.get(
                        "provider_load_attempted", nested.get("provider_load_attempted")
                    ),
                    "provider_execution_succeeded": data.get(
                        "provider_execution_succeeded",
                        nested.get("provider_execution_succeeded"),
                    ),
                    "provider_execution_performed": data.get(
                        "provider_execution_performed",
                        nested.get("provider_execution_performed"),
                    ),
                    "dependency_missing": data.get(
                        "dependency_missing", nested.get("dependency_missing")
                    ),
                    "classification": nested.get("classification") or data.get("classification"),
                    "gpu_review_blocked": data.get("decision", {}).get("gpu_review_blocked"),
                    "warnings": data.get("warnings", []),
                }
            )
        except Exception as exc:  # noqa: BLE001
            audit["error"] = f"{audit['error']} {type(exc).__name__}: {exc}".strip()
    return audit

def compact_context_report(repo_root: Path, path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"path": repo_rel(path, repo_root), "error": "missing"}
    try:
        data = read_json(path)
    except Exception as exc:  # noqa: BLE001 - live context reports are advisory.
        return {
            "path": repo_rel(path, repo_root),
            "error": f"{type(exc).__name__}: {exc}",
        }
    return {
        "path": repo_rel(path, repo_root),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "summary": data.get("summary", {}),
        "decision": data.get("decision", {}),
        "event_count": data.get("event_count") or data.get("heap_snapshot", {}).get("event_count"),
        "pending_broker_request_count": data.get("pending_broker_request_count")
        or data.get("heap_snapshot", {}).get("pending_broker_request_count"),
    }

def refresh_live_context_reports(
    context_reports: list[dict[str, Any]], repo_root: Path, paths: list[str]
) -> int:
    refreshed = 0
    for value in paths:
        report = compact_context_report(repo_root, resolve_path(repo_root, value))
        report["kind"] = report.get("kind") or "live_runtime_context_report"
        report["live_context_report"] = True
        key = report.get("path")
        for index, item in enumerate(context_reports):
            if isinstance(item, dict) and item.get("path") == key:
                context_reports[index] = report
                break
        else:
            context_reports.append(report)
        if not report.get("error"):
            refreshed += 1
    return refreshed
