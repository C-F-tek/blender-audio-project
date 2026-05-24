"""CLI for provider runtime blackboard."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ia_carmine._shared.file_backed_transport import (
    INLINE_TEXT_MAX_CHARS,
    artifact_ref,
    read_json_windows_safe,
    read_text_windows_safe,
    validate_runtime_payload_manifest,
    write_json_artifact,
)
from .common import EVENT_TYPES, LANES, tool_catalog_snapshot
from .heap import ProviderRuntimeHeap

SEMANTIC_FILE_BACKED_KEYS = {
    "context_pack",
    "heap_events",
    "provider_output",
    "response_text",
    "patch_candidate",
    "chunks",
    "tool_results",
}


def inline_semantic_payload_keys(data: Any) -> list[str]:
    found: set[str] = set()
    if isinstance(data, dict):
        for key, value in data.items():
            text = str(key)
            if text in SEMANTIC_FILE_BACKED_KEYS:
                found.add(text)
            found.update(inline_semantic_payload_keys(value))
    elif isinstance(data, list):
        for item in data:
            found.update(inline_semantic_payload_keys(item))
    return sorted(found)


def parse_payload(
    raw: str = "",
    payload_file: str = "",
    *,
    repo_root: Path | None = None,
) -> tuple[dict[str, Any], dict[str, Any]]:
    if payload_file:
        path = Path(payload_file)
        if not path.is_absolute():
            path = (repo_root or Path.cwd()) / path
        try:
            data = read_json_windows_safe(path)
        except OSError as exc:
            raise ValueError(
                f"payload file unreadable: {path}; error={type(exc).__name__}: {exc}"
            ) from exc
        except json.JSONDecodeError as exc:
            raw_preview = read_text_windows_safe(path)[:500].replace("\r", "\\r").replace("\n", "\\n")
            raise ValueError(
                f"payload JSON parse failed from file={payload_file}; preview=[{raw_preview}]; error={exc}"
            ) from exc
        if data.get("kind") == "ia_carmine_runtime_payload_manifest":
            validation = validate_runtime_payload_manifest(repo_root or Path.cwd(), path)
            if not validation.get("passed"):
                errors = ",".join(str(item) for item in validation.get("errors", [])[:6])
                raise ValueError(f"payload_manifest_invalid:{errors}")
        payload_ref = artifact_ref(
            path,
            repo_root or Path.cwd(),
            kind="provider_runtime_blackboard_payload",
            producer="provider_runtime_blackboard",
        )
        return data, payload_ref

    if not raw:
        return {}, {}
    if len(raw) > INLINE_TEXT_MAX_CHARS:
        raise ValueError("payload_json_large_requires_payload_file")

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
    semantic_keys = inline_semantic_payload_keys(data)
    if semantic_keys:
        raise ValueError(
            "payload_file_required_for_semantic_payload_keys:"
            + ",".join(semantic_keys)
        )
    return data, {}

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
        try:
            payload, payload_ref = parse_payload(
                args.payload_json,
                args.payload_file,
                repo_root=repo_root,
            )
        except ValueError as exc:
            result = {
                "passed": False,
                "error": str(exc),
                "provider_execution_performed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
            }
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 2
        if args.event_type == "broker_request" and not payload_ref and payload:
            payload_ref = write_json_artifact(
                repo_root,
                repo_root / "output" / "validation" / "provider_runtime_blackboard_payloads",
                name=args.correlation_id or payload.get("id") or "broker_request",
                payload=payload,
                kind="provider_runtime_blackboard_payload",
                producer="provider_runtime_blackboard",
            )
        event = heap.append_event(
            source=args.source,
            target=args.target or None,
            event_type=args.event_type,
            round_id=args.round,
            correlation_id=args.correlation_id or None,
            payload=payload,
            payload_ref=payload_ref,
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
