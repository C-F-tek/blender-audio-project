"""Argument normalization for provider-native broker tool calls."""

from __future__ import annotations

from typing import Any

from ia_carmine.runtime.heap_gate.broker_result_validation import broker_result_report


def enrich_runtime_file_window_args(owner: Any, args: dict[str, Any]) -> None:
    normalized_from: dict[str, str] = {}
    if "length" in args and "limit" not in args:
        args["limit"] = args.pop("length")
        normalized_from["limit"] = "length"
    source_request_id = str(
        args.get("source_broker_request_id") or args.get("broker_request_id") or ""
    ).strip()
    if args.get("ref_id") and source_request_id and not args.get("startup_manifest"):
        report_ref = _brokered_search_report_ref(owner, source_request_id)
        if report_ref:
            args.setdefault("startup_manifest", report_ref)
            args.setdefault("source_report_ref", report_ref)
            args.setdefault("strict_startup_refs", True)
    if args.get("ref_id") and source_request_id and args.get("startup_manifest"):
        args.setdefault("source_report_ref", str(args.get("startup_manifest") or ""))
    try:
        manifest_path, _manifest = owner.startup_manifest_from_task_file()
    except Exception:
        manifest_path = None
    if manifest_path and not args.get("startup_manifest"):
        args.setdefault("startup_manifest", str(manifest_path))
        args.setdefault("strict_startup_refs", True)
    if normalized_from:
        existing = args.get("argument_normalized_from")
        merged = existing if isinstance(existing, dict) else {}
        merged.update(normalized_from)
        args["argument_normalized_from"] = merged
    args.setdefault("offset", 0)
    args.setdefault("limit", 16000)


def _brokered_search_report_ref(owner: Any, source_request_id: str) -> str:
    try:
        events = owner.read_events()
    except Exception:
        events = []
    for payload in reversed(owner.broker_results(events)):
        ids = {
            str(payload.get("id") or "").strip(),
            str(payload.get("request_id") or "").strip(),
            str(payload.get("normalized_request_id") or "").strip(),
        }
        if source_request_id not in ids:
            continue
        outputs = payload.get("outputs") if isinstance(payload.get("outputs"), dict) else {}
        report_ref = str(outputs.get("json_report") or outputs.get("evidence_json") or "").strip()
        if not report_ref:
            continue
        report = broker_result_report(payload, repo_root=getattr(owner, "repo_root", None))
        if str(report.get("kind") or "") not in {
            "repo_search_rg",
            "repo_search_git_grep",
            "repo_find_fd",
            "repo_json_query_jq",
        }:
            continue
        if not isinstance(report.get("runtime_file_window_authorized_refs"), list):
            continue
        if str(report.get("source_broker_request_id") or "") != source_request_id:
            continue
        if report.get("broker_authorized") is not True:
            continue
        return report_ref
    return ""
