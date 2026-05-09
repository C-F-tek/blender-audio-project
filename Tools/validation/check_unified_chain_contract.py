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

TOOL_EVIDENCE_HINTS = (
    "tool",
    "capability",
    "capabilities",
    "tool_usage",
    "runtime_tool",
    "telemetry",
)

REQUIRED_HEAP_PEERS = {
    "gpu1": ("gpu1", "primary", "advisory", "planner"),
    "gpu0": ("gpu0", "companion", "tool", "openvino", "worker"),
    "npu": ("npu", "audit", "efficiency", "observer"),
}

SHARED_MEMORY_HINTS = (
    "shared_memory",
    "memory",
    "bundle",
    "ai_to_ai",
    "heap",
    "exchange",
    "context",
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


def has_tool_capability_evidence(report: dict[str, Any] | None) -> bool:
    if not report:
        return False
    if report.get("passed") is False:
        return False
    text = json.dumps(report, ensure_ascii=False).lower()
    explicit_count = 0
    for key in ("tool_count", "capability_count", "runtime_tool_count", "available_tool_count"):
        try:
            explicit_count = max(explicit_count, int(report.get(key) or 0))
        except (TypeError, ValueError):
            pass
    if explicit_count > 0:
        return True
    for key in ("tools", "capabilities", "tool_capabilities", "runtime_tools", "available_tools"):
        value = report.get(key)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, dict) and value:
            return True
    return "tool" in text and any(hint in text for hint in TOOL_EVIDENCE_HINTS)


def has_tool_usage_evidence(report: dict[str, Any] | None) -> bool:
    if not report:
        return False
    if report.get("passed") is False:
        return False
    text = json.dumps(report, ensure_ascii=False).lower()
    for key in ("tool_usage_count", "runtime_tool_usage_count", "tool_invocation_count", "used_tool_count"):
        try:
            if int(report.get(key) or 0) > 0:
                return True
        except (TypeError, ValueError):
            pass
    for key in ("tool_usage", "tool_usages", "runtime_tool_usage", "tool_invocations", "used_tools", "tools_used"):
        value = report.get(key)
        if isinstance(value, list) and value:
            return True
        if isinstance(value, dict) and value:
            return True
    return ("tool" in text or "capability" in text) and any(token in text for token in ("used", "usage", "invoked", "telemetry"))


def peer_presence(report: dict[str, Any] | None, events: list[dict[str, Any]]) -> dict[str, bool]:
    text_parts: list[str] = []
    if report:
        text_parts.append(json.dumps(report, ensure_ascii=False).lower())
    if events:
        text_parts.append(json.dumps(events, ensure_ascii=False).lower())
    text = "\n".join(text_parts)

    found: dict[str, bool] = {}
    for peer, hints in REQUIRED_HEAP_PEERS.items():
        found[peer] = peer in text and any(hint in text for hint in hints)
    return found


def has_shared_memory_evidence(report: dict[str, Any] | None, events: list[dict[str, Any]]) -> bool:
    text_parts: list[str] = []
    if report:
        text_parts.append(json.dumps(report, ensure_ascii=False).lower())
    if events:
        text_parts.append(json.dumps(events, ensure_ascii=False).lower())
    text = "\n".join(text_parts)
    if not text:
        return False
    return any(hint in text for hint in SHARED_MEMORY_HINTS)


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
    parser.add_argument("--review-pr-report", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--ai-public-events", default="")
    parser.add_argument("--tool-capability-manifest", default="")
    parser.add_argument("--tool-usage-telemetry", default="")
    parser.add_argument("--heap-peer-runtime", default="")
    parser.add_argument("--shared-memory-evidence", default="")
    parser.add_argument("--require-ai-exchange", action="store_true")
    parser.add_argument("--require-provider-tool-evidence", action="store_true")
    parser.add_argument("--require-heap-peer-runtime", action="store_true")
    parser.add_argument("--require-shared-memory-evidence", action="store_true")
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
    review_pr_path = repo_path(repo_root, args.review_pr_report) if args.review_pr_report else repo_root / f"output/validation/review_pr_prepare_{mode_name}_{stamp}.json"
    observer_dir = repo_path(repo_root, args.observer_dir) if args.observer_dir else discover_observer_dir(repo_root, stamp)
    ai_events_path = repo_path(repo_root, args.ai_public_events) if args.ai_public_events else ((observer_dir / "ai_public_events.jsonl") if observer_dir else None)
    tool_capability_path = repo_path(repo_root, args.tool_capability_manifest) if args.tool_capability_manifest else discover_first(
        repo_root,
        [
            f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
            f"output/**/tool_capability_manifest*{stamp}*.json",
        ],
    )
    tool_usage_path = repo_path(repo_root, args.tool_usage_telemetry) if args.tool_usage_telemetry else discover_first(
        repo_root,
        [
            f"output/**/full_toolbox_run_telemetry_summary*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary*{stamp}*.json",
            f"output/**/tool_usage*{stamp}*.json",
            f"output/**/runtime_tool_usage*{stamp}*.json",
        ],
    )
    heap_peer_path = repo_path(repo_root, args.heap_peer_runtime) if args.heap_peer_runtime else discover_first(
        repo_root,
        [
            f"output/**/heap_peer_runtime*{stamp}*.json",
            f"output/**/runtime_tool_capability_manifest*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/runtime_tool_capability_manifest*{stamp}*.json",
            f"output/**/full_toolbox_run_telemetry_summary*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/full_toolbox_run_telemetry_summary*{stamp}*.json",
        ],
    )
    shared_memory_path = repo_path(repo_root, args.shared_memory_evidence) if args.shared_memory_evidence else discover_first(
        repo_root,
        [
            f"output/**/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/shared_toolbox_ai_to_ai_bundle*{stamp}*.json",
            f"output/**/full_memory_tool_regeneration_bundle*{stamp}*.json",
            f"docs/LOCAL_VALIDATION_EVIDENCE/full_memory_tool_regeneration_bundle*{stamp}*.json",
            f"output/**/heap_exchange*{stamp}*.json",
        ],
    )

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

    tool_capability_report, tool_capability_error = load_json(tool_capability_path) if tool_capability_path else (None, "missing")
    tool_usage_report, tool_usage_error = load_json(tool_usage_path) if tool_usage_path else (None, "missing")
    heap_peer_report, heap_peer_error = load_json(heap_peer_path) if heap_peer_path else (None, "missing")
    shared_memory_report, shared_memory_error = load_json(shared_memory_path) if shared_memory_path else (None, "missing")

    tool_capability_ok = has_tool_capability_evidence(tool_capability_report)
    tool_usage_ok = has_tool_usage_evidence(tool_usage_report)
    tool_evidence_passed = True
    if args.require_provider_tool_evidence:
        tool_evidence_passed = bool(tool_capability_ok and tool_usage_ok)
    add_edge(
        edges,
        name="provider_to_tool_evidence",
        producer="provider/heap exchange runtime",
        consumer="runtime tool capability and usage evidence",
        expected="tool capability manifest and runtime tool usage telemetry" if args.require_provider_tool_evidence else "not required for this invocation",
        actual=(
            f"capability_ok={tool_capability_ok} capability_error={tool_capability_error} "
            f"usage_ok={tool_usage_ok} usage_error={tool_usage_error}"
        ),
        passed=tool_evidence_passed,
        action="When provider/exchange is required, emit runtime_tool_capability_manifest and full_toolbox/tool-usage telemetry before declaring the chain complete.",
        artifacts=[rel(repo_root, tool_capability_path), rel(repo_root, tool_usage_path)],
    )

    peers = peer_presence(heap_peer_report, events)
    peer_runtime_passed = True
    if args.require_heap_peer_runtime:
        peer_runtime_passed = all(peers.get(peer, False) for peer in REQUIRED_HEAP_PEERS)
    add_edge(
        edges,
        name="heap_exchange_to_peer_runtime",
        producer="dynamic heap/exchange center",
        consumer="GPU1/GPU0/NPU peer runtime",
        expected="GPU1 primary advisory, GPU0 companion/tool worker and NPU audit/efficiency peers" if args.require_heap_peer_runtime else "not required for this invocation",
        actual=f"peers={peers} heap_peer_error={heap_peer_error}",
        passed=peer_runtime_passed,
        action="Emit heap peer runtime evidence showing GPU1, GPU0 and NPU participating as linked heap/exchange peers.",
        artifacts=[rel(repo_root, heap_peer_path), rel(repo_root, ai_events_path)],
    )

    shared_memory_ok = has_shared_memory_evidence(shared_memory_report, events)
    shared_memory_passed = True
    if args.require_shared_memory_evidence:
        shared_memory_passed = shared_memory_ok
    add_edge(
        edges,
        name="heap_exchange_to_shared_memory",
        producer="dynamic heap/exchange center",
        consumer="shared memory / AI-to-AI bundle evidence",
        expected="shared memory or AI-to-AI bundle evidence" if args.require_shared_memory_evidence else "not required for this invocation",
        actual=f"shared_memory_ok={shared_memory_ok} shared_memory_error={shared_memory_error}",
        passed=shared_memory_passed,
        action="Emit shared memory / AI-to-AI bundle evidence so the heap remains the source of knowledge for provider peers.",
        artifacts=[rel(repo_root, shared_memory_path), rel(repo_root, ai_events_path)],
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

    review_pr_report, review_pr_error = load_json(review_pr_path)
    staged_paths = []
    if review_pr_report and isinstance(review_pr_report.get("stage_result"), dict):
        staged_paths = review_pr_report["stage_result"].get("staged_files") or []

    review_pr_ready = bool(
        review_pr_report
        and not review_pr_error
        and review_pr_report.get("passed") is True
        and review_pr_report.get("git_commit_performed") is True
        and review_pr_report.get("product_commit")
        and staged_paths
    )

    add_edge(
        edges,
        name="product_separation_to_review_pr_product",
        producer="patch suggestion product separation / apply report",
        consumer="prepare_review_pr.py",
        expected="review_pr_prepare report passed with product commit and staged files" if args.require_review_pr_product else "not required for this invocation",
        actual=(f"passed={review_pr_report.get('passed')} commit={review_pr_report.get('git_commit_performed')} product_commit={review_pr_report.get('product_commit')} staged_files={len(staged_paths)} pr_created={review_pr_report.get('github_pr_created')}" if review_pr_report else f"missing/invalid: {review_pr_error}"),
        passed=review_pr_ready if args.require_review_pr_product else True,
        action="Run prepare_review_pr.py after deterministic apply and require a concrete product commit before declaring the chain complete.",
        artifacts=[rel(repo_root, review_pr_path)],
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
        "require_provider_tool_evidence": bool(args.require_provider_tool_evidence),
        "require_heap_peer_runtime": bool(args.require_heap_peer_runtime),
        "require_shared_memory_evidence": bool(args.require_shared_memory_evidence),
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
