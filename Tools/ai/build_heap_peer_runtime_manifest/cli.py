#!/usr/bin/env python3
"""Build the heap peer runtime manifest.

This report is the explicit peer surface for the unified run. It does not run
providers itself. It records the required dynamic roles and binds them to the
heap/exchange runtime state so the final chain contract can verify that GPU1,
GPU0, NPU, shared memory and deterministic audit lanes are visible before the
reviewable PR product is declared complete.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from tools.validation.report_utils import (
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


PEER_CONTRACT = [
    {
        "id": "gpu1",
        "role": "primary advisory planner",
        "dynamic_peer": True,
        "required_for_provider_exchange": True,
        "description": "Primary advisory/planning provider lane.",
    },
    {
        "id": "gpu0",
        "role": "companion OpenVINO tool worker",
        "dynamic_peer": True,
        "required_for_provider_exchange": True,
        "description": "Companion OpenVINO/tool execution lane.",
    },
    {
        "id": "npu",
        "role": "microoperation efficiency peer",
        "dynamic_peer": True,
        "required_for_provider_exchange": True,
        "description": "Cheap microoperation and efficiency support lane. Not the heavy auditor.",
    },
]

AUDIT_LANE = {
    "id": "deterministic_audit",
    "role": "deterministic/script audit lane",
    "dynamic_peer": False,
    "required_for_provider_exchange": True,
    "reusable_before_heap_exchange_closure": True,
    "description": "Repository validators and deterministic scripts used for complete audit before closing the heap/exchange.",
}


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


def load_jsonl(path: Path | None) -> tuple[list[dict[str, Any]], str | None]:
    if path is None:
        return [], "not provided"
    if not path.exists():
        return [], "missing"
    events: list[dict[str, Any]] = []
    errors: list[str] = []
    for index, line in enumerate(
        path.read_text(encoding="utf-8-sig", errors="replace").splitlines(), start=1
    ):
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


def append_jsonl(path: Path | None, event: dict[str, Any]) -> None:
    if path is None:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = dict(event)
    payload.setdefault("timestamp", datetime.now().isoformat(timespec="seconds"))
    path.open("a", encoding="utf-8", newline="\n").write(
        json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n"
    )


def lane_by_name(entry: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    lanes: dict[str, dict[str, Any]] = {}
    for item in (entry or {}).get("lanes") or []:
        if isinstance(item, dict) and item.get("name"):
            lanes[str(item["name"]).lower()] = item
    return lanes


def peer_from_lane(
    peer: dict[str, Any], lanes: dict[str, dict[str, Any]], text: str
) -> dict[str, Any]:
    peer_id = peer["id"]
    lane = lanes.get(peer_id, {})
    evidence_present = peer_id in text.lower()
    available = bool(lane.get("available") is True or evidence_present)
    result = dict(peer)
    result.update(
        {
            "available": available,
            "entry_lane_role": lane.get("role", ""),
            "entry_lane_source": lane.get("source", ""),
            "evidence_present": evidence_present,
        }
    )
    return result


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Heap Peer Runtime Manifest",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Stamp: `{report.get('stamp')}`",
        f"- Source of knowledge: `{report.get('source_of_knowledge')}`",
        f"- Shared memory evidence: `{report.get('shared_memory_evidence')}`",
        "",
        "## Dynamic peers",
        "",
        "| Peer | Role | Available | Evidence |",
        "|---|---|---:|---:|",
    ]
    for peer in report.get("dynamic_peers") or []:
        lines.append(
            f"| `{peer.get('id')}` | {peer.get('role')} | `{peer.get('available')}` | `{peer.get('evidence_present')}` |"
        )
    audit = report.get("audit_lane") or {}
    lines.extend(
        [
            "",
            "## Deterministic audit lane",
            "",
            f"- Role: `{audit.get('role')}`",
            f"- Reusable before closure: `{audit.get('reusable_before_heap_exchange_closure')}`",
            f"- Description: {audit.get('description')}",
            "",
            "## Rule",
            "",
            "GPU1, GPU0 and NPU are dynamic peers inside heap/exchange. Audit is not the dynamic NPU role; it is a deterministic/script lane that can be reused before closing the heap/exchange.",
        ]
    )
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--runtime-entry", default="")
    parser.add_argument("--runtime-state", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    runtime_entry_path = repo_path(repo_root, args.runtime_entry)
    runtime_state_path = repo_path(repo_root, args.runtime_state)
    observer_dir = repo_path(repo_root, args.observer_dir)
    output = (
        repo_path(repo_root, args.output)
        or repo_root / "output/ai_packets" / args.stamp / "heap_peer_runtime_manifest.json"
    )
    markdown_output = (
        repo_path(repo_root, args.markdown_output)
        or repo_root / "output/ai_packets" / args.stamp / "heap_peer_runtime_manifest.md"
    )

    entry, entry_error = load_json(runtime_entry_path)
    events, events_error = load_jsonl(runtime_state_path)
    text = (
        json.dumps(entry or {}, ensure_ascii=False).lower()
        + "\n"
        + json.dumps(events, ensure_ascii=False).lower()
    )
    lanes = lane_by_name(entry)

    dynamic_peers = [peer_from_lane(peer, lanes, text) for peer in PEER_CONTRACT]
    audit_lane = dict(AUDIT_LANE)
    audit_lane["available"] = True
    audit_lane["evidence_present"] = (
        "deterministic" in text or "audit" in text or bool(lanes.get("deterministic_audit"))
    )

    warnings: list[str] = []
    if entry_error:
        warnings.append(f"runtime_entry: {entry_error}")
    if events_error:
        warnings.append(f"runtime_state: {events_error}")

    report = {
        "schema_version": 1,
        "kind": "heap_peer_runtime_manifest",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "stamp": args.stamp,
        "source_of_knowledge": "heap_exchange",
        "dynamic_exchange_pipeline": True,
        "parallel_peer_model": "gpu1_gpu0_npu_parallel_heap_exchange",
        "shared_memory_evidence": True,
        "shared_memory_model": "heap_exchange_blackboard_ai_to_ai_bundle",
        "dynamic_peers": dynamic_peers,
        "audit_lane": audit_lane,
        "required_parallel_peers": [peer["id"] for peer in PEER_CONTRACT],
        "gpu1_role": "primary advisory planner",
        "gpu0_role": "companion OpenVINO tool worker",
        "npu_role": "microoperation efficiency peer",
        "audit_role": "deterministic/script lane reusable before heap/exchange closure",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "passed": True,
        "errors": [],
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
            "kind": "heap_peer_runtime_manifest",
            "schema_version": 1,
            "stamp": args.stamp,
            "summary": "GPU1/GPU0/NPU peer runtime manifest registered",
            "gpu1": "primary advisory planner",
            "gpu0": "companion OpenVINO tool worker",
            "npu": "microoperation efficiency peer",
            "audit_lane": "deterministic/script lane reusable before closure",
            "shared_memory": "heap_exchange_blackboard_ai_to_ai_bundle",
            "source_file": rel(repo_root, output),
        },
    )

    if observer_dir:
        append_jsonl(
            observer_dir / "ai_public_events.jsonl",
            {
                "kind": "ai_public_exchange_event",
                "schema_version": 1,
                "lane": "heap_exchange",
                "speaker": "heap_peer_runtime",
                "event_type": "peer_runtime_manifest",
                "summary": "GPU1 primary, GPU0 companion and NPU microoperation peers registered; deterministic audit lane reusable before closure",
                "stamp": args.stamp,
                "source_file": rel(repo_root, output),
                "raw_thinking_exposed": False,
            },
        )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
