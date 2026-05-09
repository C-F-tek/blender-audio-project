#!/usr/bin/env python3
"""Validate the unified local-AI orchestration as a producer/consumer chain.

This validator converts the launcher from a loose sequence of phases into a
machine-checkable chain contract. Each edge verifies that a producer phase emits
an artifact that the next consumer phase can actually use.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:  # pragma: no cover - direct execution from repo root
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


DEFAULT_MODE_NAME = "agent_state_chunks_context_pack_contract_evidence_full_validation_json_md_official_patch_specs_provider_python_smoke"
CONCRETE_OPERATION_NAMES = {
    "replace_once",
    "append_once",
    "insert_after_once",
    "insert_before_once",
    "write_file",
}
EXCHANGE_EVENT_HINTS = (
    "proposal",
    "decision",
    "patch",
    "patch_spec",
    "recommendation",
    "summary",
    "tool_result",
)


def repo_path(repo_root: Path, value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def load_json(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report validator must not crash on bad evidence
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not an object"
    return data, None


def load_jsonl(path: Path) -> tuple[list[dict[str, Any]], str | None]:
    if not path.exists():
        return [], "missing"
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, line in enumerate(path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1):
        stripped = line.strip()
        if not stripped:
            continue
        try:
            value = json.loads(stripped)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"line {index}: {type(exc).__name__}: {exc}")
            continue
        if isinstance(value, dict):
            events.append(value)
    return events, "; ".join(errors) if errors else None


def discover_first(repo_root: Path, patterns: list[str]) -> Path | None:
    for pattern in patterns:
        matches = sorted(repo_root.glob(pattern), key=lambda item: item.stat().st_mtime if item.exists() else 0, reverse=True)
        if matches:
            return matches[0]
    return None


def discover_apply_report(repo_root: Path, stamp: str, mode_name: str) -> Path | None:
    patterns = [
        f"output/validation/patch_suggestion_bundle_apply_{mode_name}_{stamp}.json",
        f"output/validation/generated_patch_specs_review_pr_apply*{stamp}*.json",
        f"output/validation/*generated_patch_specs*{stamp}*.json",
        f"output/validation/*patch_suggestion_bundle_apply*{stamp}*.json",
    ]
    for pattern in patterns:
        for path in sorted(repo_root.glob(pattern), key=lambda item: item.stat().st_mtime, reverse=True):
            data, error = load_json(path)
            if error:
                continue
            if data and data.get("kind") == "patch_suggestion_bundle_apply":
                return path
    return None


def discover_observer_dir(repo_root: Path, stamp: str) -> Path | None:
    candidates = sorted(
        repo_root.glob(f"output/local_ai_runs/*{stamp}*_observer"),
        key=lambda item: item.stat().st_mtime if item.exists() else 0,
        reverse=True,
    )
    return candidates[0] if candidates else None


def event_kind(event: dict[str, Any]) -> str:
    for key in ("kind", "type", "event", "phase", "status"):
        value = event.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip().lower()
    return ""


def has_productive_exchange_event(events: list[dict[str, Any]]) -> bool:
    for event in events:
        kind = event_kind(event)
        text = json.dumps(event, ensure_ascii=False).lower()
        if any(hint in kind or hint in text for hint in EXCHANGE_EVENT_HINTS):
            return True
    return False


def concrete_operation_count_from_apply(report: dict[str, Any]) -> int:
    count = int(report.get("operation_count") or 0)
    if count > 0:
        return count
    concrete = 0
    for item in report.get("results") or []:
        if not isinstance(item, dict):
            continue
        op = str(item.get("operation") or "").strip().lower()
        if op in CONCRETE_OPERATION_NAMES:
            concrete += 1
    return concrete


def add_edge(edges: list[dict[str, Any]], *, name: str, producer: str, consumer: str, expected: str, actual: str, passed: bool, action: str, artifacts: list[str] | None = None) -> None:
    edges.append({
        "edge": name,
        "producer": producer,
        "consumer": consumer,
        "expected": expected,
        "actual": actual,
        "passed": passed,
        "action": action,
        "artifacts": artifacts or [],
    })


def rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Unified Chain Contract",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Broken edge count: `{len(report.get('broken_edges') or [])}`",
        "",
        "## Edges",
        "",
        "| Edge | Passed | Actual | Action |",
        "|---|---:|---|---|",
    ]
    for edge in report.get("edges") or []:
        lines.append(
            f"| `{edge.get('edge')}` | `{edge.get('passed')}` | {str(edge.get('actual') or '').replace('|', '/')} | {str(edge.get('action') or '').replace('|', '/')} |"
        )
    if report.get("broken_edges"):
        lines.extend(["", "## Broken edges", ""])
        for edge in report["broken_edges"]:
            lines.extend([
                f"### {edge.get('edge')}",
                "",
                f"- Producer: `{edge.get('producer')}`",
                f"- Consumer: `{edge.get('consumer')}`",
                f"- Expected: {edge.get('expected')}",
                f"- Actual: {edge.get('actual')}",
                f"- Action: {edge.get('action')}",
                "",
            ])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--mode-name", default=DEFAULT_MODE_NAME)
    parser.add_argument("--manifest", default="")
    parser.add_argument("--official-report", default="")
    parser.add_argument("--gpu0-report", default="")
    parser.add_argument("--apply-report", default="")
    parser.add_argument("--product-separation-report", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--ai-public-events", default="")
    parser.add_argument("--require-ai-exchange", action="store_true")
    parser.add_argument("--require-concrete-patch-specs", action="store_true")
    parser.add_argument("--require-review-pr-product", action="store_true")
    parser.add_argument("--output", default="output/validation/unified_chain_contract.json")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp
    mode_name = args.mode_name

    manifest_path = repo_path(repo_root, args.manifest) if args.manifest else discover_first(
        repo_root,
        [f"output/local_ai_runs/*{stamp}*/pipeline/unified_local_ai_refactor_manifest.json"],
    )
    official_path = repo_path(repo_root, args.official_report) if args.official_report else repo_root / f"output/validation/{stamp}_phase_official.json"
    gpu0_path = repo_path(repo_root, args.gpu0_report) if args.gpu0_report else repo_root / f"output/validation/openvino_gpu0_workload_{stamp}.json"
    apply_path = repo_path(repo_root, args.apply_report) if args.apply_report else discover_apply_report(repo_root, stamp, mode_name)
    product_path = repo_path(repo_root, args.product_separation_report) if args.product_separation_report else repo_root / f"output/validation/patch_suggestion_product_separation_{mode_name}_{stamp}.json"
    observer_dir = repo_path(repo_root, args.observer_dir) if args.observer_dir else discover_observer_dir(repo_root, stamp)
    ai_events_path = repo_path(repo_root, args.ai_public_events) if args.ai_public_events else ((observer_dir / "ai_public_events.jsonl") if observer_dir else None)

    edges: list[dict[str, Any]] = []

    manifest, manifest_error = load_json(manifest_path) if manifest_path else (None, "missing")
    add_edge(
        edges,
        name="launcher_to_manifest",
        producer="unified launcher",
        consumer="chain contract",
        expected="unified_local_ai_refactor_manifest.json exists and is JSON object",
        actual="present" if manifest and not manifest_error else f"missing/invalid: {manifest_error}",
        passed=bool(manifest and not manifest_error),
        action="Ensure the unified launcher completed far enough to write the pipeline manifest.",
        artifacts=[rel(repo_root, manifest_path)],
    )

    official, official_error = load_json(official_path)
    official_passed = bool(official and not official_error and (official.get("passed") is True or official.get("status") == "passed"))
    add_edge(
        edges,
        name="context_to_official_adapter",
        producer="context_pack/agent_state/provider inputs",
        consumer="official local AI adapter",
        expected="official phase report exists and passed=true/status=passed",
        actual=(f"passed={official.get('passed')} status={official.get('status')} return_code={official.get('return_code')}" if official else f"missing/invalid: {official_error}"),
        passed=official_passed,
        action="Inspect output/validation/<stamp>_phase_official.json and its stdout/stderr process logs.",
        artifacts=[rel(repo_root, official_path)],
    )

    gpu0, gpu0_error = load_json(gpu0_path)
    gpu0_passed = bool(gpu0 and not gpu0_error and gpu0.get("openvino_gpu0_workload_passed") is True)
    add_edge(
        edges,
        name="provider_to_gpu0_workload",
        producer="provider workload routing",
        consumer="OpenVINO GPU.0 evidence",
        expected="GPU.0 visible and workload passed",
        actual=(f"visible={gpu0.get('openvino_gpu0_visible')} performed={gpu0.get('openvino_gpu0_workload_performed')} passed={gpu0.get('openvino_gpu0_workload_passed')}" if gpu0 else f"missing/invalid: {gpu0_error}"),
        passed=gpu0_passed,
        action="Run with -RunOpenVinoGpu0Workload and repository .venv containing numpy/openvino.",
        artifacts=[rel(repo_root, gpu0_path)],
    )

    events: list[dict[str, Any]] = []
    events_error = "not required"
    exchange_passed = True
    if args.require_ai_exchange:
        events, events_error = load_jsonl(ai_events_path) if ai_events_path else ([], "missing observer ai_public_events.jsonl")
        exchange_passed = bool(events and not events_error and has_productive_exchange_event(events))
    add_edge(
        edges,
        name="provider_to_ai_exchange",
        producer="provider/Ollama/official adapter",
        consumer="AI public or peer exchange evidence",
        expected="ai_public_events.jsonl has at least one proposal/decision/patch/recommendation event" if args.require_ai_exchange else "not required for this invocation",
        actual=(f"event_count={len(events)} error={events_error}" if args.require_ai_exchange else "not required"),
        passed=exchange_passed,
        action="Emit public exchange events from provider/official phases or disable --require-ai-exchange only for diagnostic runs.",
        artifacts=[rel(repo_root, ai_events_path)],
    )

    apply_report, apply_error = load_json(apply_path) if apply_path else (None, "missing")
    concrete_ops = concrete_operation_count_from_apply(apply_report) if apply_report else 0
    changed_count = int(apply_report.get("changed_count") or 0) if apply_report else 0
    applied_count = int(apply_report.get("applied_count") or 0) if apply_report else 0
    patch_specs_passed = True
    if args.require_concrete_patch_specs:
        patch_specs_passed = bool(apply_report and not apply_error and concrete_ops > 0)
    add_edge(
        edges,
        name="patch_specs_to_review_bridge",
        producer="generated patch specs",
        consumer="apply_generated_patch_specs_for_review_pr",
        expected="current-stamp apply report with concrete deterministic operations" if args.require_concrete_patch_specs else "not required for this invocation",
        actual=(f"operation_count={apply_report.get('operation_count')} concrete_ops={concrete_ops} changed_count={changed_count} applied_count={applied_count}" if apply_report else f"missing/invalid: {apply_error}"),
        passed=patch_specs_passed,
        action="Generate replace_once/append_once/insert_after_once/insert_before_once/write_file operations; metadata-only specs must not advance to PR product.",
        artifacts=[rel(repo_root, apply_path)],
    )

    product_report, product_error = load_json(product_path)
    product_ready = bool(
        product_report
        and not product_error
        and (
            product_report.get("passed") is True
            or product_report.get("ready_for_patch_suggestion_review") is True
            or product_report.get("patch_product_status") in {"deterministic_patch_operations_ready", "product_facing_patch_suggestions_ready"}
        )
    )
    if args.require_review_pr_product:
        product_ready = bool(product_ready and changed_count > 0)
    add_edge(
        edges,
        name="review_bridge_to_product_separation",
        producer="generated patch specs review bridge",
        consumer="patch suggestion product separation / prepare_review_pr",
        expected="product separation passed and review PR has concrete changed files" if args.require_review_pr_product else "product separation report when present",
        actual=(f"passed={product_report.get('passed')} status={product_report.get('patch_product_status')} ready={product_report.get('ready_for_patch_suggestion_review')} changed_count={changed_count}" if product_report else f"missing/invalid: {product_error}"),
        passed=product_ready if args.require_review_pr_product else bool(product_report and not product_error),
        action="Block prepare_review_pr until product separation has deterministic operations or product-facing suggestions with concrete targets.",
        artifacts=[rel(repo_root, product_path)],
    )

    broken_edges = [edge for edge in edges if not edge["passed"]]
    report = {
        "schema_version": 1,
        "kind": "unified_chain_contract",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": stamp,
        "mode_name": mode_name,
        "passed": not broken_edges,
        "require_ai_exchange": bool(args.require_ai_exchange),
        "require_concrete_patch_specs": bool(args.require_concrete_patch_specs),
        "require_review_pr_product": bool(args.require_review_pr_product),
        "edges": edges,
        "broken_edges": broken_edges,
        "errors": [f"{edge['edge']}: {edge['actual']}" for edge in broken_edges],
        "warnings": [],
    }

    output = resolve_output_path(repo_root, args.output)
    print(write_json_report(report, output), end="")
    if args.markdown_output:
        write_text_report(render_markdown(report), resolve_output_path(repo_root, args.markdown_output))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
