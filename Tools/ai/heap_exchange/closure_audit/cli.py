#!/usr/bin/env python3
"""Build heap/exchange closure audit report.

This is not the dynamic NPU role. GPU1/GPU0/NPU remain dynamic peers in the
heap/exchange loop. This report represents the deterministic/script audit lane
that can be reused before declaring the heap/exchange closed and before the
final reviewable PR product is accepted.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai.heap_exchange.io import append_jsonl, load_jsonl

try:
    from Tools.validation._shared.report_utils import (
        resolve_output_path,
        write_json_report,
        write_text_report,
    )
except ImportError:  # pragma: no cover
    from Tools.validation._shared.report_utils import (  # type: ignore
        resolve_output_path,
        write_json_report,
        write_text_report,
    )


def repo_path(repo_root: Path, raw: str) -> Path | None:
    if not raw:
        return None
    path = Path(raw)
    return path if path.is_absolute() else repo_root / path


def rel(repo_root: Path, path: Path | None) -> str:
    if path is None:
        return ""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_json(path: Path | None) -> tuple[dict[str, Any] | None, str | None]:
    if path is None:
        return None, "not provided"
    if not path.exists():
        return None, "missing"
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "json root is not an object"
    return data, None


def peer_ids(peer_manifest: dict[str, Any] | None) -> set[str]:
    peers = set()
    for item in (peer_manifest or {}).get("dynamic_peers") or []:
        if isinstance(item, dict) and item.get("id"):
            peers.add(str(item["id"]).lower())
    for key in ("gpu1_role", "gpu0_role", "npu_role"):
        if (peer_manifest or {}).get(key):
            peers.add(key.split("_")[0])
    return peers


def has_audit_lane(peer_manifest: dict[str, Any] | None, events: list[dict[str, Any]]) -> bool:
    manifest_text = json.dumps(peer_manifest or {}, ensure_ascii=False).lower()
    events_text = json.dumps(events, ensure_ascii=False).lower()
    text = manifest_text + "\n" + events_text
    return "deterministic" in text and ("audit" in text or "script" in text)


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap/Exchange Closure Audit",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Closure state: `{report.get('closure_state')}`",
        f"- Dynamic peer count: `{report.get('dynamic_peer_count')}`",
        f"- Deterministic audit lane available: `{report.get('deterministic_audit_lane_available')}`",
        "",
        "## Rule",
        "",
        "Closure audit is a deterministic/script lane reused before heap/exchange closure. It does not redefine the NPU dynamic role; NPU remains the microoperation/efficiency peer.",
        "",
    ]
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--heap-peer-runtime", default="")
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    peer_path = repo_path(repo_root, args.heap_peer_runtime)
    runtime_state_path = repo_path(repo_root, args.runtime_state)
    observer_dir = repo_path(repo_root, args.observer_dir)
    output = (
        repo_path(repo_root, args.output)
        or repo_root / "output/ai_packets" / args.stamp / "heap_exchange_closure_audit.json"
    )
    markdown_output = (
        repo_path(repo_root, args.markdown_output)
        or repo_root / "output/ai_packets" / args.stamp / "heap_exchange_closure_audit.md"
    )

    peer_manifest, peer_error = load_json(peer_path)
    events, events_error = load_jsonl(runtime_state_path)

    peers = peer_ids(peer_manifest)
    required_peers = {"gpu1", "gpu0", "npu"}
    missing_peers = sorted(required_peers - peers)
    audit_available = has_audit_lane(peer_manifest, events)

    errors: list[str] = []
    warnings: list[str] = []
    if peer_error:
        errors.append(f"heap_peer_runtime load failed: {peer_error}")
    if events_error and events_error != "not provided":
        warnings.append(f"runtime_state: {events_error}")
    if missing_peers:
        errors.append(f"missing dynamic peers before closure: {missing_peers}")
    if not audit_available:
        errors.append("deterministic/script audit lane not available before heap/exchange closure")

    report = {
        "schema_version": 1,
        "kind": "heap_exchange_closure_audit",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": args.stamp,
        "passed": not errors,
        "closure_state": "ready_for_final_chain_contract" if not errors else "blocked",
        "source_of_knowledge": "heap_exchange",
        "dynamic_peer_count": len(peers),
        "required_dynamic_peers": sorted(required_peers),
        "observed_dynamic_peers": sorted(peers),
        "deterministic_audit_lane_available": audit_available,
        "npu_dynamic_role": "microoperation_efficiency_peer",
        "audit_lane_role": "deterministic_script_audit_before_heap_exchange_closure",
        "heap_peer_runtime": rel(repo_root, peer_path),
        "runtime_state": rel(repo_root, runtime_state_path),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": errors,
        "warnings": warnings,
    }

    write_json_report(report, resolve_output_path(repo_root, output.as_posix()))
    write_text_report(
        render_markdown(report),
        resolve_output_path(repo_root, markdown_output.as_posix()),
    )

    append_jsonl(
        runtime_state_path,
        {
            "kind": "heap_exchange_closure_audit",
            "schema_version": 1,
            "stamp": args.stamp,
            "passed": report["passed"],
            "closure_state": report["closure_state"],
            "summary": "deterministic/script closure audit evaluated before final chain contract",
            "npu_dynamic_role": "microoperation_efficiency_peer",
            "audit_lane_role": "deterministic_script_audit_before_heap_exchange_closure",
            "source_file": rel(repo_root, output),
        },
    )

    if observer_dir:
        append_jsonl(
            observer_dir / "ai_public_events.jsonl",
            {
                "kind": "ai_public_exchange_event",
                "schema_version": 1,
                "lane": "deterministic_audit",
                "speaker": "heap_exchange_closure_audit",
                "event_type": "closure_audit",
                "passed": report["passed"],
                "summary": "deterministic/script audit lane evaluated before heap/exchange closure",
                "stamp": args.stamp,
                "source_file": rel(repo_root, output),
                "raw_thinking_exposed": False,
            },
        )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
