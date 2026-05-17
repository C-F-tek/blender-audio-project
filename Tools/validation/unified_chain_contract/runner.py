"""Unified chain contract runner."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any

from .common import (
    REQUIRED_HEAP_PEERS,
    add_edge,
    load_json,
    load_jsonl,
    rel,
    resolve_output_path,
    write_json_report,
    write_text_report,
)
from .evidence import (
    concrete_operation_count_from_apply,
    has_closure_audit_evidence,
    has_productive_exchange_event,
    has_shared_memory_evidence,
    has_tool_capability_evidence,
    has_tool_usage_evidence,
    peer_presence,
)
from .markdown import render_markdown
from .paths import discover_contract_paths

def run_contract(args: Any) -> int:
    repo_root = Path(args.repo_root).resolve()
    stamp = args.stamp
    mode_name = args.mode_name

    paths = discover_contract_paths(repo_root, args, stamp, mode_name)
    manifest_path = paths["manifest"]
    official_path = paths["official"]
    gpu0_path = paths["gpu0"]
    apply_path = paths["apply"]
    product_path = paths["product"]
    review_pr_path = paths["review_pr"]
    ai_events_path = paths["ai_events"]
    tool_capability_path = paths["tool_capability"]
    tool_usage_path = paths["tool_usage"]
    heap_peer_path = paths["heap_peer"]
    shared_memory_path = paths["shared_memory"]
    closure_audit_path = paths["closure_audit"]

    edges: list[dict[str, Any]] = []

    manifest, manifest_error = load_json(manifest_path) if manifest_path else (None, "missing")
    add_edge(
        edges,
        name="launcher_to_manifest",
        producer="unified launcher",
        consumer="chain contract",
        expected="unified_local_ai_refactor_manifest.json exists and is JSON object",
        actual="present"
        if manifest and not manifest_error
        else f"missing/invalid: {manifest_error}",
        passed=bool(manifest and not manifest_error),
        action="Ensure the unified launcher completed far enough to write the pipeline manifest.",
        artifacts=[rel(repo_root, manifest_path)],
    )

    official, official_error = load_json(official_path)
    official_passed = bool(
        official
        and not official_error
        and (official.get("passed") is True or official.get("status") == "passed")
    )
    add_edge(
        edges,
        name="context_to_official_adapter",
        producer="context_pack/agent_state/provider inputs",
        consumer="official local AI adapter",
        expected="official phase report exists and passed=true/status=passed",
        actual=(
            f"passed={official.get('passed')} status={official.get('status')} return_code={official.get('return_code')}"
            if official
            else f"missing/invalid: {official_error}"
        ),
        passed=official_passed,
        action="Inspect output/validation/<stamp>_phase_official.json and its stdout/stderr process logs.",
        artifacts=[rel(repo_root, official_path)],
    )

    gpu0, gpu0_error = load_json(gpu0_path)
    gpu0_passed = bool(
        gpu0 and not gpu0_error and gpu0.get("openvino_gpu0_workload_passed") is True
    )
    add_edge(
        edges,
        name="provider_to_gpu0_workload",
        producer="provider workload routing",
        consumer="OpenVINO GPU.0 evidence",
        expected="GPU.0 visible and workload passed",
        actual=(
            f"visible={gpu0.get('openvino_gpu0_visible')} performed={gpu0.get('openvino_gpu0_workload_performed')} passed={gpu0.get('openvino_gpu0_workload_passed')}"
            if gpu0
            else f"missing/invalid: {gpu0_error}"
        ),
        passed=gpu0_passed,
        action="Run with -RunOpenVinoGpu0Workload and repository .venv containing numpy/openvino.",
        artifacts=[rel(repo_root, gpu0_path)],
    )

    events: list[dict[str, Any]] = []
    events_error = "not required"
    exchange_passed = True
    if args.require_ai_exchange:
        events, events_error = (
            load_jsonl(ai_events_path)
            if ai_events_path
            else ([], "missing observer ai_public_events.jsonl")
        )
        exchange_passed = bool(
            events and not events_error and has_productive_exchange_event(events)
        )
    add_edge(
        edges,
        name="provider_to_ai_exchange",
        producer="provider/Ollama/official adapter",
        consumer="AI public or peer exchange evidence",
        expected="ai_public_events.jsonl has at least one proposal/decision/patch/recommendation event"
        if args.require_ai_exchange
        else "not required for this invocation",
        actual=(
            f"event_count={len(events)} error={events_error}"
            if args.require_ai_exchange
            else "not required"
        ),
        passed=exchange_passed,
        action="Emit public exchange events from provider/official phases or disable --require-ai-exchange only for diagnostic runs.",
        artifacts=[rel(repo_root, ai_events_path)],
    )

    tool_capability_report, tool_capability_error = (
        load_json(tool_capability_path) if tool_capability_path else (None, "missing")
    )
    tool_usage_report, tool_usage_error = (
        load_json(tool_usage_path) if tool_usage_path else (None, "missing")
    )
    heap_peer_report, heap_peer_error = (
        load_json(heap_peer_path) if heap_peer_path else (None, "missing")
    )
    shared_memory_report, shared_memory_error = (
        load_json(shared_memory_path) if shared_memory_path else (None, "missing")
    )
    closure_audit_report, closure_audit_error = (
        load_json(closure_audit_path) if closure_audit_path else (None, "missing")
    )

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
        expected="tool capability manifest and runtime tool usage telemetry"
        if args.require_provider_tool_evidence
        else "not required for this invocation",
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
        expected="GPU1 primary advisory, GPU0 companion/tool worker and NPU microoperation/efficiency peer"
        if args.require_heap_peer_runtime
        else "not required for this invocation",
        actual=f"peers={peers} heap_peer_error={heap_peer_error}",
        passed=peer_runtime_passed,
        action="Emit heap peer runtime evidence showing GPU1, GPU0 and NPU participating as linked heap/exchange peers. Audit remains a deterministic/script lane that can be reused for a complete heap/exchange audit before closure; it is not the dynamic NPU peer role.",
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
        expected="shared memory or AI-to-AI bundle evidence"
        if args.require_shared_memory_evidence
        else "not required for this invocation",
        actual=f"shared_memory_ok={shared_memory_ok} shared_memory_error={shared_memory_error}",
        passed=shared_memory_passed,
        action="Emit shared memory / AI-to-AI bundle evidence so the heap remains the source of knowledge for provider peers.",
        artifacts=[rel(repo_root, shared_memory_path), rel(repo_root, ai_events_path)],
    )

    closure_audit_ok = has_closure_audit_evidence(closure_audit_report)
    closure_audit_passed = True
    if args.require_heap_closure_audit:
        closure_audit_passed = closure_audit_ok
    add_edge(
        edges,
        name="heap_exchange_to_closure_audit",
        producer="dynamic heap/exchange center",
        consumer="deterministic/script closure audit lane",
        expected="heap_exchange_closure_audit passed and ready_for_final_chain_contract"
        if args.require_heap_closure_audit
        else "not required for this invocation",
        actual=f"closure_audit_ok={closure_audit_ok} closure_audit_error={closure_audit_error}",
        passed=closure_audit_passed,
        action="Run deterministic/script closure audit before final chain contract. This lane can audit the complete heap/exchange without changing the NPU dynamic microoperation/efficiency role.",
        artifacts=[rel(repo_root, closure_audit_path)],
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
        expected="current-stamp apply report with concrete deterministic operations"
        if args.require_concrete_patch_specs
        else "not required for this invocation",
        actual=(
            f"operation_count={apply_report.get('operation_count')} concrete_ops={concrete_ops} changed_count={changed_count} applied_count={applied_count}"
            if apply_report
            else f"missing/invalid: {apply_error}"
        ),
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
            or product_report.get("patch_product_status")
            in {"deterministic_patch_operations_ready", "product_facing_patch_suggestions_ready"}
        )
    )
    if args.require_review_pr_product:
        product_ready = bool(product_ready and changed_count > 0)
    add_edge(
        edges,
        name="review_bridge_to_product_separation",
        producer="generated patch specs review bridge",
        consumer="patch suggestion product separation / prepare_review_pr",
        expected="product separation passed and review PR has concrete changed files"
        if args.require_review_pr_product
        else "product separation report when present",
        actual=(
            f"passed={product_report.get('passed')} status={product_report.get('patch_product_status')} ready={product_report.get('ready_for_patch_suggestion_review')} changed_count={changed_count}"
            if product_report
            else f"missing/invalid: {product_error}"
        ),
        passed=product_ready
        if args.require_review_pr_product
        else bool(product_report and not product_error),
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
        expected="review_pr_prepare report passed with product commit and staged files"
        if args.require_review_pr_product
        else "not required for this invocation",
        actual=(
            f"passed={review_pr_report.get('passed')} commit={review_pr_report.get('git_commit_performed')} product_commit={review_pr_report.get('product_commit')} staged_files={len(staged_paths)} pr_created={review_pr_report.get('github_pr_created')}"
            if review_pr_report
            else f"missing/invalid: {review_pr_error}"
        ),
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
        "require_heap_closure_audit": bool(args.require_heap_closure_audit),
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
        write_text_report(
            render_markdown(report), resolve_output_path(repo_root, args.markdown_output)
        )
    return 0 if report["passed"] else 2
