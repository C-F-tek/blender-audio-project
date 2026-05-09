#!/usr/bin/env python3
from __future__ import annotations

import argparse
import glob
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


SURFACE_ORDER = [
    "preflight",
    "heap_entry",
    "heap_peer_runtime",
    "gpu0_peer",
    "npu_micro_peer",
    "shared_memory",
    "tool_broker",
    "closure_audit",
    "product_readiness",
    "review_pr_prepare",
    "unified_chain_contract",
]

SURFACE_HINTS: dict[str, tuple[str, ...]] = {
    "preflight": ("real_product_preflight_gate", "preflight", "full_product_pr_chain"),
    "heap_entry": ("heap_exchange_runtime_entry", "task_ingress", "heap/exchange", "runtime entry"),
    "heap_peer_runtime": ("heap_peer_runtime", "gpu1", "gpu0", "npu"),
    "gpu0_peer": ("gpu0", "openvino", "peer"),
    "npu_micro_peer": ("npu", "micro", "peer"),
    "shared_memory": ("shared", "memory", "ai-to-ai", "heap"),
    "tool_broker": ("tool", "broker", "capability", "telemetry"),
    "closure_audit": ("closure", "audit", "heap_exchange", "ready_for_final_chain_contract"),
    "product_readiness": ("review_pr_product_readiness", "product", "ready"),
    "review_pr_prepare": ("review_pr_prepare", "product_commit", "git_commit"),
    "unified_chain_contract": ("unified_chain_contract", "edge", "heap"),
}

DEFAULT_PATTERNS: dict[str, tuple[str, ...]] = {
    "preflight": (
        "output/validation/real_product_profile_preflight_{stamp}.json",
        "output/validation/real_product_preflight*{stamp}*.json",
        "output/validation/real_product_preflight_gate.json",
    ),
    "heap_entry": (
        "output/**/heap_exchange_runtime_entry*{stamp}*.json",
        "output/**/{stamp}*/**/heap_exchange_runtime_entry*.json",
        "output/**/heap_exchange_runtime_entry*.json",
    ),
    "heap_peer_runtime": (
        "output/**/heap_peer_runtime_manifest*{stamp}*.json",
        "output/**/{stamp}*/**/heap_peer_runtime_manifest*.json",
        "output/**/heap_peer_runtime_manifest*.json",
    ),
    "gpu0_peer": (
        "output/validation/openvino_gpu0_workload_{stamp}.json",
        "output/**/openvino_gpu0*{stamp}*.json",
        "output/**/{stamp}*/**/openvino_gpu0*.json",
    ),
    "npu_micro_peer": (
        "output/**/npu_micro*{stamp}*.json",
        "output/**/npu*micro*{stamp}*.json",
        "output/**/{stamp}*/**/npu*micro*.json",
        "output/**/npu*{stamp}*.json",
    ),
    "shared_memory": (
        "output/**/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
        "docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
        "output/**/full_memory_tool_regeneration_bundle*{stamp}*.json",
        "output/**/{stamp}*/**/*shared*memory*.json",
        "output/**/heap_peer_runtime_manifest*.json",
    ),
    "tool_broker": (
        "output/**/runtime_tool_capability_manifest*{stamp}*.json",
        "docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
        "output/**/full_toolbox_run_telemetry_summary*{stamp}*.json",
        "docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary*{stamp}*.json",
        "output/**/runtime_tool_usage*{stamp}*.json",
        "output/**/tool_usage*{stamp}*.json",
    ),
    "closure_audit": (
        "output/**/heap_exchange_closure_audit*{stamp}*.json",
        "docs/LOCAL_VALIDATION_EVIDENCE/heap_exchange_closure_audit*{stamp}*.json",
        "output/**/{stamp}*/**/heap_exchange_closure_audit*.json",
    ),
    "product_readiness": (
        "output/validation/review_pr_product_readiness_*_{stamp}.json",
        "output/validation/review_pr_product_readiness*{stamp}*.json",
    ),
    "review_pr_prepare": (
        "output/validation/review_pr_prepare_*_{stamp}.json",
        "output/validation/review_pr_prepare*{stamp}*.json",
        "docs/LOCAL_VALIDATION_EVIDENCE/review_pr_prepare_{stamp}.json",
    ),
    "unified_chain_contract": (
        "output/validation/unified_chain_contract_{stamp}.json",
        "output/**/unified_chain_contract*{stamp}*.json",
    ),
}

REPORT_PATH_ARGS = {
    "preflight": "preflight_report",
    "heap_entry": "heap_entry",
    "heap_peer_runtime": "heap_peer_runtime",
    "gpu0_peer": "gpu0_report",
    "npu_micro_peer": "npu_report",
    "shared_memory": "shared_memory_evidence",
    "tool_broker": "tool_broker_report",
    "closure_audit": "closure_audit_report",
    "product_readiness": "product_readiness_report",
    "review_pr_prepare": "review_pr_report",
    "unified_chain_contract": "unified_chain_contract",
}


def repo_path(repo_root: Path, value: str | None) -> Path | None:
    if not value:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path


def repo_rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path | None) -> tuple[dict[str, Any] | None, str]:
    if path is None:
        return None, "missing"
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not object"
    return data, ""


def text_blob(report: dict[str, Any] | None) -> str:
    if not report:
        return ""
    return json.dumps(report, ensure_ascii=False, sort_keys=True).lower()


def has_stamp(surface: str, stamp: str, path: Path | None, report: dict[str, Any] | None) -> bool:
    if not stamp:
        return True
    if path and stamp in path.as_posix():
        return True
    if not report:
        return False
    for key in ("stamp", "data_stamp", "run_stamp"):
        if str(report.get(key) or "") == stamp:
            return True
    text = text_blob(report)
    return stamp.lower() in text


def report_passed(report: dict[str, Any] | None) -> bool:
    if not report:
        return False
    return report.get("passed") is not False


def has_hints(surface: str, report: dict[str, Any] | None) -> bool:
    text = text_blob(report)
    if not text:
        return False
    return any(hint.lower() in text for hint in SURFACE_HINTS[surface])


def discover_surface(repo_root: Path, surface: str, stamp: str) -> Path | None:
    patterns = DEFAULT_PATTERNS[surface]
    for raw_pattern in patterns:
        pattern = str(repo_root / raw_pattern.format(stamp=stamp))
        matches = [
            Path(item)
            for item in glob.glob(pattern, recursive=True)
            if Path(item).is_file()
        ]
        if matches:
            matches.sort(key=lambda item: item.stat().st_mtime, reverse=True)
            return matches[0]
    return None


def build_surface(repo_root: Path, stamp: str, surface: str, explicit_path: Path | None, require_stamp: bool) -> dict[str, Any]:
    path = explicit_path if explicit_path else discover_surface(repo_root, surface, stamp)
    report, error = load_json(path)
    exists = bool(path and path.exists())
    stamp_ok = has_stamp(surface, stamp, path, report) if require_stamp else True
    passed_ok = report_passed(report)
    hints_ok = has_hints(surface, report)

    # Some runtime files are intentionally generic names inside a stamped run dir.
    # If the path was explicitly supplied, the caller already correlated it.
    if explicit_path and exists:
        stamp_ok = True

    ok = bool(exists and report and not error and stamp_ok and passed_ok and hints_ok)
    return {
        "surface": surface,
        "path": repo_rel(repo_root, path),
        "exists": exists,
        "json_ok": bool(report and not error),
        "kind": report.get("kind") if report else None,
        "passed_value": report.get("passed") if report else None,
        "stamp_ok": stamp_ok,
        "hints_ok": hints_ok,
        "ok": ok,
        "error": error,
    }


def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Runtime Evidence Correlation",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Missing surfaces: `{len(report.get('missing_surfaces') or [])}`",
        f"- Failed surfaces: `{len(report.get('failed_surfaces') or [])}`",
        "",
        "## Surfaces",
        "",
        "| Surface | OK | Stamp OK | Hints OK | Path |",
        "|---|---:|---:|---:|---|",
    ]
    for item in report.get("surfaces") or []:
        lines.append(
            f"| `{item.get('surface')}` | `{item.get('ok')}` | `{item.get('stamp_ok')}` | `{item.get('hints_ok')}` | `{item.get('path')}` |"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--output", default="output/validation/runtime_evidence_correlation.json")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--no-require-stamp", action="store_true")
    for dest in REPORT_PATH_ARGS.values():
        parser.add_argument(f"--{dest.replace('_', '-')}", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = str(args.stamp).strip()
    require_stamp = not bool(args.no_require_stamp)

    surfaces = []
    for surface in SURFACE_ORDER:
        explicit = repo_path(repo_root, getattr(args, REPORT_PATH_ARGS[surface]))
        surfaces.append(build_surface(repo_root, stamp, surface, explicit, require_stamp))

    missing_surfaces = [item["surface"] for item in surfaces if not item["exists"]]
    failed_surfaces = [item["surface"] for item in surfaces if item["exists"] and not item["ok"]]
    errors = []
    for item in surfaces:
        if item["ok"]:
            continue
        if not item["exists"]:
            errors.append(f"missing runtime evidence surface: {item['surface']}")
        elif not item["json_ok"]:
            errors.append(f"invalid runtime evidence JSON: {item['surface']} ({item['error']})")
        elif not item["stamp_ok"]:
            errors.append(f"runtime evidence surface is not correlated with stamp {stamp}: {item['surface']}")
        elif item["passed_value"] is False:
            errors.append(f"runtime evidence surface explicitly failed: {item['surface']}")
        elif not item["hints_ok"]:
            errors.append(f"runtime evidence surface lacks required semantic hints: {item['surface']}")
        else:
            errors.append(f"runtime evidence surface failed: {item['surface']}")

    report = {
        "schema_version": 1,
        "kind": "runtime_evidence_correlation",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": stamp,
        "require_stamp": require_stamp,
        "surface_order": SURFACE_ORDER,
        "surfaces": surfaces,
        "missing_surfaces": missing_surfaces,
        "failed_surfaces": failed_surfaces,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": not errors,
        "errors": errors,
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    write_json_report(report, output)
    if args.markdown_output:
        write_markdown(report, resolve_output_path(repo_root, args.markdown_output))
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
