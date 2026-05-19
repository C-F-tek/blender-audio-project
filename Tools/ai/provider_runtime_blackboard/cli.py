"""CLI for provider runtime blackboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .common import EVENT_TYPES, LANES, tool_catalog_snapshot
from .heap import ProviderRuntimeHeap

def parse_payload(raw: str = "", payload_file: str = "") -> dict[str, Any]:
    if payload_file:
        path = Path(payload_file)
        if not path.is_absolute():
            path = Path.cwd() / path
        try:
            raw = path.read_text(encoding="utf-8-sig")
        except OSError as exc:
            raise ValueError(
                f"payload file unreadable: {path}; error={type(exc).__name__}: {exc}"
            ) from exc

    if not raw:
        return {}

    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        preview = raw[:500].replace("\r", "\\r").replace("\n", "\\n")
        source = f"file={payload_file}" if payload_file else "inline --payload-json"
        raise ValueError(
            f"payload JSON parse failed from {source}; length={len(raw)}; "
            f"preview=[{preview}]; error={exc}"
        ) from exc

    if not isinstance(data, dict):
        raise ValueError("payload JSON must be an object")
    return data

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--events", default="")
    parser.add_argument("--snapshot", default="")
    parser.add_argument("--markdown-output", default="")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init")
    init.add_argument("--source", default="orchestrator")

    append = sub.add_parser("append-event")
    append.add_argument("--source", required=True)
    append.add_argument("--target", default="")
    append.add_argument("--event-type", required=True)
    append.add_argument("--round", type=int, default=None)
    append.add_argument("--correlation-id", default="")
    append.add_argument("--payload-json", default="{}")
    append.add_argument("--payload-file", default="")

    sub.add_parser("snapshot")
    sub.add_parser("tool-catalog")
    sub.add_parser("pending-broker-requests")
    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    heap = ProviderRuntimeHeap.from_args(
        repo_root, args.stamp, args.events, args.snapshot, args.markdown_output
    )

    if args.command == "init":
        heap.append_event(
            source=args.source,
            event_type="provider_state",
            payload={
                "state": "heap_initialized",
                "lanes": list(LANES),
                "event_types": list(EVENT_TYPES),
            },
        )
        result = heap.write_snapshot()
    elif args.command == "append-event":
        event = heap.append_event(
            source=args.source,
            target=args.target or None,
            event_type=args.event_type,
            round_id=args.round,
            correlation_id=args.correlation_id or None,
            payload=parse_payload(args.payload_json, args.payload_file),
        )
        result = {"passed": True, "event": event, "snapshot": heap.write_snapshot()}
    elif args.command == "tool-catalog":
        result = tool_catalog_snapshot()
    elif args.command == "pending-broker-requests":
        result = {
            "passed": True,
            "pending_broker_requests": heap.pending_broker_requests(),
        }
    else:
        result = heap.write_snapshot()

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0
