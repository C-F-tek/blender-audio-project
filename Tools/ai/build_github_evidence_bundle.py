#!/usr/bin/env python3
"""Build compact Git-trackable evidence from local generated reports.

The repository ignores ``output/`` by design, so long local validation/provider
reports should not be pasted into chat or committed directly. This helper reads
selected local reports and writes a compact evidence bundle under a normal docs
path that can be reviewed and pushed with Git CLI.

It does not execute providers and does not modify runtime outputs.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_REPORTS = (
    "output/validation/ai_workload_report_quality.json",
    "output/validation/ai_workload_quality_lane_routing.json",
    "output/validation/npu_decode_quality_remediation.json",
    "output/validation/npu_decode_smoke_diagnostic.json",
    "output/validation/local_provider_probe.json",
    "output/validation/npu_runtime_output_manifest.json",
    "output/validation/provider_result_report.json",
)

DEFAULT_SELECTED_CHUNKS_EVIDENCE = (
    "docs/LOCAL_VALIDATION_EVIDENCE/full_context_golden_selected_chunks_evidence.json",
)


def split_path_values(items: list[str]) -> list[str]:
    out: list[str] = []
    for item in items:
        for part in str(item).split(","):
            normalized = part.strip().strip("'\"")
            if normalized:
                out.append(normalized)
    return out


def read_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def compact_value(value: Any, *, max_string: int = 500) -> Any:
    if isinstance(value, str):
        return value if len(value) <= max_string else value[:max_string] + "...[truncated]"
    if isinstance(value, list):
        return [compact_value(item, max_string=max_string) for item in value[:20]]
    if isinstance(value, dict):
        return {str(key): compact_value(item, max_string=max_string) for key, item in value.items()}
    return value


def as_list(value: Any) -> list[Any]:
    if isinstance(value, list):
        return value
    if value is None:
        return []
    return [value]


def list_contains(value: Any, expected: str) -> bool:
    return any(str(item).lower() == expected.lower() for item in as_list(value))


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def repo_relative(path: Path, repo_root: Path) -> str:
    if path.is_absolute() and path.is_relative_to(repo_root):
        return path.relative_to(repo_root).as_posix()
    return str(path).replace("\\", "/")


def summarize_report(path: Path, repo_root: Path) -> dict[str, Any]:
    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {
            "path": rel,
            "exists": path.exists(),
            "json_ok": False,
            "kind": None,
            "passed": None,
            "summary": {},
        }

    summary: dict[str, Any] = {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }
    for key in (
        "usable_lanes",
        "unusable_lanes",
        "primary_advisory_provider",
        "policy",
        "mode",
        "provider",
        "python_exe",
        "device",
        "model_dir",
        "proposal_count",
    ):
        if key in data:
            summary[key] = compact_value(data.get(key))
    checks = data.get("checks") if isinstance(data.get("checks"), dict) else {}
    if checks:
        summary["checks"] = compact_value(
            {
                key: checks.get(key)
                for key in (
                    "classification",
                    "usable_for_advisory",
                    "npu_usable_for_advisory",
                    "npu_classification",
                    "metrics",
                    "npu_metrics",
                    "provider_envelope",
                    "promotion_gate",
                    "required_promotion_gate",
                )
                if key in checks
            },
            max_string=350,
        )
    routing = data.get("routing") if isinstance(data.get("routing"), dict) else {}
    if routing:
        summary["routing"] = compact_value(
            {
                "advisory_lanes": routing.get("advisory_lanes"),
                "excluded_advisory_lanes": routing.get("excluded_advisory_lanes"),
                "primary_advisory_provider": routing.get("primary_advisory_provider"),
                "trusted_context_files": routing.get("trusted_context_files"),
                "excluded_context_files": routing.get("excluded_context_files"),
            },
            max_string=350,
        )
    context = data.get("context") if isinstance(data.get("context"), dict) else {}
    if context:
        summary["context"] = compact_value(
            {
                "context_files": context.get("context_files"),
                "excluded_context_files": context.get("excluded_context_files"),
                "advisory_context_routing": context.get("advisory_context_routing"),
            },
            max_string=350,
        )
    ollama = data.get("ollama") if isinstance(data.get("ollama"), dict) else {}
    if ollama:
        summary["ollama"] = compact_value(
            {
                "used": ollama.get("used"),
                "model": ollama.get("model"),
                "error": ollama.get("error"),
                "text_preview": (ollama.get("text") or "")[:500],
            },
            max_string=500,
        )

    return {
        "path": rel,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "summary": summary,
    }


def summarize_selected_chunks_evidence(path: Path, repo_root: Path) -> dict[str, Any]:
    """Return compact selected-chunks evidence without reading raw context packs."""

    rel = repo_relative(path, repo_root)
    data = read_json(path)
    if data is None:
        return {
            "path": rel,
            "exists": path.exists(),
            "json_ok": False,
            "kind": None,
            "passed": None,
            "summary": {},
        }

    summary: dict[str, Any] = {
        "schema_version": data.get("schema_version"),
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "provider_execution_performed": data.get("provider_execution_performed"),
        "source_writes_performed": data.get("source_writes_performed"),
        "selected_count": data.get("selected_count"),
        "total_selected_chars": data.get("total_selected_chars"),
        "max_chunks": data.get("max_chunks"),
        "max_total_chars": data.get("max_total_chars"),
        "source_bundle": data.get("source_bundle"),
        "source_chunks": data.get("source_chunks"),
        "decision": compact_value(data.get("decision") or {}),
        "errors": compact_value(data.get("errors") or []),
        "warnings": compact_value(data.get("warnings") or []),
    }
    return {
        "path": rel,
        "exists": True,
        "json_ok": True,
        "kind": data.get("kind"),
        "passed": data.get("passed"),
        "summary": summary,
    }


def discover_selected_chunks_evidence(repo_root: Path, explicit_paths: list[str]) -> list[Path]:
    """Discover compact selected-chunks evidence files if the run produced them.

    Only Git-trackable compact evidence under docs/LOCAL_VALIDATION_EVIDENCE is
    discovered. Raw output/ai_context_packs bundles stay ignored and are not read
    unless a caller explicitly passes a path.
    """

    candidates = split_path_values(explicit_paths)
    if not candidates:
        candidates = list(DEFAULT_SELECTED_CHUNKS_EVIDENCE)
        evidence_dir = repo_root / "docs" / "LOCAL_VALIDATION_EVIDENCE"
        if evidence_dir.exists():
            for path in sorted(evidence_dir.glob("*selected_chunks_evidence.json")):
                rel = repo_relative(path, repo_root)
                if rel not in candidates:
                    candidates.append(rel)

    resolved: list[Path] = []
    seen: set[str] = set()
    for raw in candidates:
        path = resolve_repo_path(repo_root, raw)
        key = path.resolve().as_posix() if path.exists() else path.as_posix()
        if key not in seen and path.exists():
            resolved.append(path)
            seen.add(key)
    return resolved


def report_summaries(reports: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [item.get("summary", {}) for item in reports if isinstance(item.get("summary"), dict)]


def selected_chunks_evidence_seen(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    return any(item.get("exists") is True and item.get("json_ok") is True for item in selected_chunks_evidence)


def selected_chunks_built(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(selected_chunks_evidence):
        decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
        if decision.get("selected_chunks_built") is True:
            return True
        if isinstance(summary.get("selected_count"), int) and summary.get("selected_count", 0) > 0:
            return True
    return False


def selected_chunks_budget_respected(selected_chunks_evidence: list[dict[str, Any]]) -> bool:
    for summary in report_summaries(selected_chunks_evidence):
        decision = summary.get("decision") if isinstance(summary.get("decision"), dict) else {}
        if decision.get("budget_respected") is True:
            return True
        total_chars = summary.get("total_selected_chars")
        max_total_chars = summary.get("max_total_chars")
        if isinstance(total_chars, int) and isinstance(max_total_chars, int) and total_chars <= max_total_chars:
            return True
    return False


def npu_marked_unusable(reports: list[dict[str, Any]]) -> bool:
    """Return whether validation evidence marks NPU output unusable for advisory.

    Older evidence bundles only checked excluded context files. Current reports can
    express the same decision through ai_workload_report_quality.unusable_lanes,
    lane routing excluded_advisory_lanes, or the NPU decode remediation checks.
    """

    for summary in report_summaries(reports):
        if list_contains(summary.get("unusable_lanes"), "npu"):
            return True
        checks = summary.get("checks") if isinstance(summary.get("checks"), dict) else {}
        if checks.get("npu_usable_for_advisory") is False:
            return True
        if str(checks.get("npu_classification") or "").lower() in {"unusable_output", "unusable"}:
            return True
    return False


def npu_marked_excluded_from_advisory(reports: list[dict[str, Any]]) -> bool:
    """Return whether routing/evidence excludes NPU from advisory context."""

    for summary in report_summaries(reports):
        routing = summary.get("routing") if isinstance(summary.get("routing"), dict) else {}
        if list_contains(routing.get("excluded_advisory_lanes"), "npu"):
            return True
        for ctx in as_list(routing.get("excluded_context_files")):
            if isinstance(ctx, dict) and ctx.get("lane") == "npu" and ctx.get("trusted") is False:
                return True

        context = summary.get("context") if isinstance(summary.get("context"), dict) else {}
        excluded_context = context.get("excluded_context_files") or []
        if "output/ai_packets/npu_real_workload_report.md" in excluded_context:
            return True
        advisory_routing = context.get("advisory_context_routing") if isinstance(context.get("advisory_context_routing"), dict) else {}
        if list_contains(advisory_routing.get("excluded_advisory_lanes"), "npu"):
            return True
    return False


def npu_excluded_when_unusable(reports: list[dict[str, Any]]) -> bool:
    return npu_marked_unusable(reports) and npu_marked_excluded_from_advisory(reports)


def build_bundle(
    repo_root: Path,
    report_paths: list[str],
    basename: str,
    output_dir: Path,
    selected_chunks_paths: list[str],
) -> tuple[dict[str, Any], str]:
    resolved = []
    for raw in report_paths:
        resolved.append(resolve_repo_path(repo_root, raw))
    reports = [summarize_report(path, repo_root) for path in resolved]
    selected_paths = discover_selected_chunks_evidence(repo_root, selected_chunks_paths)
    selected_chunks_evidence = [
        summarize_selected_chunks_evidence(path, repo_root)
        for path in selected_paths
    ]

    bundle = {
        "schema_version": 1,
        "kind": "github_validation_evidence_bundle",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": str(repo_root),
        "source_reports": [item["path"] for item in reports],
        "source_selected_chunks_evidence": [item["path"] for item in selected_chunks_evidence],
        "reports": reports,
        "selected_chunks_evidence": selected_chunks_evidence,
        "decision": {
            "ollama_gpu_primary_advisory": any(
                (item.get("summary", {}).get("primary_advisory_provider", {}) or {}).get("provider") == "ollama"
                or (item.get("summary", {}).get("routing", {}).get("primary_advisory_provider", {}) or {}).get("provider") == "ollama"
                or (item.get("summary", {}).get("ollama", {}) or {}).get("used") is True
                for item in reports
            ),
            "npu_excluded_when_unusable": npu_excluded_when_unusable(reports),
            "provider_execution_seen": any(item.get("summary", {}).get("provider_execution_performed") is True for item in reports),
            "npu_decode_smoke_passed": any(
                item.get("kind") == "npu_decode_smoke_diagnostic" and item.get("passed") is True and item.get("summary", {}).get("provider_execution_performed") is True
                for item in reports
            ),
            "selected_chunks_evidence_seen": selected_chunks_evidence_seen(selected_chunks_evidence),
            "selected_chunks_built": selected_chunks_built(selected_chunks_evidence),
            "budget_respected": selected_chunks_budget_respected(selected_chunks_evidence),
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{basename}.json"
    md_path = output_dir / f"{basename}.md"
    json_path.write_text(json.dumps(bundle, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    md_path.write_text(render_markdown(bundle), encoding="utf-8")
    return bundle, f"{json_path}\n{md_path}"


def render_report_entry(lines: list[str], item: dict[str, Any]) -> None:
    summary = item.get("summary", {})
    lines.append(f"### `{item['path']}`")
    lines.append("")
    lines.append(f"- Exists: `{item['exists']}`")
    lines.append(f"- JSON OK: `{item['json_ok']}`")
    lines.append(f"- Kind: `{item.get('kind')}`")
    lines.append(f"- Passed: `{item.get('passed')}`")
    if summary.get("provider_execution_performed") is not None:
        lines.append(f"- Provider execution performed: `{summary.get('provider_execution_performed')}`")
    if summary.get("source_writes_performed") is not None:
        lines.append(f"- Source writes performed: `{summary.get('source_writes_performed')}`")
    if summary.get("selected_count") is not None:
        lines.append(f"- Selected count: `{summary.get('selected_count')}`")
    if summary.get("total_selected_chars") is not None:
        lines.append(f"- Total selected chars: `{summary.get('total_selected_chars')}`")
    if summary.get("max_total_chars") is not None:
        lines.append(f"- Max total chars: `{summary.get('max_total_chars')}`")
    if summary.get("usable_lanes") is not None:
        lines.append(f"- Usable lanes: `{summary.get('usable_lanes')}`")
    if summary.get("unusable_lanes") is not None:
        lines.append(f"- Unusable lanes: `{summary.get('unusable_lanes')}`")
    if summary.get("primary_advisory_provider"):
        lines.append(f"- Primary advisory provider: `{summary.get('primary_advisory_provider')}`")
    if summary.get("python_exe"):
        lines.append(f"- Python executable: `{summary.get('python_exe')}`")
    errors = summary.get("errors") or []
    warnings = summary.get("warnings") or []
    if errors:
        lines.append(f"- Errors: `{errors}`")
    if warnings:
        lines.append(f"- Warnings: `{warnings}`")
    routing = summary.get("routing") or {}
    if routing:
        lines.append(f"- Routing: `{routing}`")
    decision = summary.get("decision") or {}
    if decision:
        lines.append(f"- Decision: `{decision}`")
    ollama = summary.get("ollama") or {}
    if ollama:
        lines.append(f"- Ollama: `{ollama}`")
    lines.append("")


def render_markdown(bundle: dict[str, Any]) -> str:
    lines = ["# Local Validation Evidence Bundle", ""]
    lines.append(f"- Generated at: `{bundle['generated_at']}`")
    lines.append(f"- Kind: `{bundle['kind']}`")
    lines.append("")
    lines.append("## Decision summary")
    for key, value in bundle["decision"].items():
        lines.append(f"- `{key}`: `{value}`")
    lines.append("")
    lines.append("## Reports")
    lines.append("")
    for item in bundle["reports"]:
        render_report_entry(lines, item)

    selected = bundle.get("selected_chunks_evidence") or []
    if selected:
        lines.append("## Selected chunks evidence")
        lines.append("")
        for item in selected:
            render_report_entry(lines, item)

    lines.append("## Git push helper")
    lines.append("")
    lines.append("```powershell")
    lines.append("git add docs/LOCAL_VALIDATION_EVIDENCE/")
    lines.append('git commit -m "test: add local ai workflow evidence bundle"')
    lines.append("git push")
    lines.append("```")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--basename", default="latest_ai_workflow_evidence")
    parser.add_argument("--output-dir", default="docs/LOCAL_VALIDATION_EVIDENCE")
    parser.add_argument("--report", action="append", default=[])
    parser.add_argument(
        "--selected-chunks-evidence",
        action="append",
        default=[],
        help=(
            "Compact selected-chunks evidence JSON path. Repeatable or "
            "comma-separated. If omitted, docs/LOCAL_VALIDATION_EVIDENCE/"
            "*selected_chunks_evidence.json is discovered when present."
        ),
    )
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir
    report_paths = split_path_values(args.report) or list(DEFAULT_REPORTS)
    bundle, outputs = build_bundle(
        repo_root,
        report_paths,
        args.basename,
        output_dir,
        list(args.selected_chunks_evidence or []),
    )
    print(json.dumps({"passed": True, "outputs": outputs.splitlines(), "decision": bundle["decision"]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
