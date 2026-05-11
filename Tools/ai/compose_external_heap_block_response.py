#!/usr/bin/env python3
"""Compose the primary external-heap long response from block pointers.

The gate remains untouched. This adapter reads the block-pointer manifest and
existing composer/causality reports, then produces the main human-readable heap
answer as a file artifact. It is intentionally file-based so the answer can grow
beyond the provider token window.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime
from pathlib import Path
from typing import Any


def read_json(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    try:
        data = json.loads(Path(path_value).read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def compact(text: str, limit: int) -> str:
    if limit <= 0 or len(text) <= limit:
        return text
    return text[:limit] + "\n...[truncated by external heap long-response composer]\n"


def blocks(pointer: dict[str, Any], block_type: str) -> list[dict[str, Any]]:
    items = [
        item for item in pointer.get("blocks") or []
        if isinstance(item, dict) and item.get("block_type") == block_type
    ]
    return sorted(items, key=lambda item: int(item.get("step_index") or 0))


def proposal_blocks(pointer: dict[str, Any]) -> list[dict[str, Any]]:
    return blocks(pointer, "proposal_chunk")


def role_blocks(pointer: dict[str, Any], role: str) -> list[dict[str, Any]]:
    items = [
        item for item in pointer.get("blocks") or []
        if isinstance(item, dict) and item.get("role") == role
    ]
    return sorted(items, key=lambda item: int(item.get("step_index") or 0))


def status_lines(pointer: dict[str, Any], causality: dict[str, Any]) -> list[str]:
    lines = [
        f"- Pointer protocol: `{pointer.get('protocol')}`",
        f"- Blocks: `{pointer.get('block_count')}`",
        f"- Edges: `{pointer.get('edge_count')}`",
        f"- Roles present: `{pointer.get('roles_present')}`",
        f"- Forward pointers: `{pointer.get('has_forward_pointers')}`",
        f"- Back-refinement pointers: `{pointer.get('has_backrefinement_pointers')}`",
        f"- Resume pointers: `{pointer.get('has_resume_pointers')}`",
    ]
    if causality:
        lines.extend(
            [
                f"- Causal chain: `{causality.get('causal_chain_status')}` / `{causality.get('causal_chain_passed')}`",
                f"- Product acceptance: `{causality.get('product_acceptance_status')}` / `{causality.get('product_acceptance_passed')}`",
            ]
        )
    return lines


def block_section(title: str, block: dict[str, Any], max_chars: int) -> list[str]:
    return [
        f"### {title}: `{block.get('block_id')}`",
        "",
        f"- Role: `{block.get('role')}`",
        f"- Source: `{block.get('source_path')}`",
        f"- Previous: `{block.get('previous_block_id')}`",
        f"- Next: `{block.get('next_block_id')}`",
        f"- Refines: `{block.get('refines_block_id')}`",
        f"- Resume from: `{block.get('resume_from_block_id')}`",
        f"- Accepted: `{block.get('accepted')}`",
        "",
        "```markdown",
        compact(str(block.get("preview") or ""), max_chars),
        "```",
        "",
    ]


def build_markdown(
    pointer: dict[str, Any],
    composer: dict[str, Any],
    causality: dict[str, Any],
    *,
    max_chars: int,
    include_rejected_history: bool,
    include_peer_blocks: bool,
) -> tuple[str, dict[str, Any]]:
    proposals = proposal_blocks(pointer)
    accepted = [item for item in proposals if item.get("accepted") is True]
    rendered = accepted if accepted else (proposals if include_rejected_history else [])
    gpu0 = role_blocks(pointer, "gpu0_reviewer_refiner")
    npu = role_blocks(pointer, "npu_auditor")
    gpu1 = role_blocks(pointer, "gpu1_planner")

    lines = [
        "# External Heap Primary Long Response",
        "",
        "Questo e' l'output principale file-based dell'heap esterno. Ricostruisce una risposta lunga usando blocchi persistenti e puntatori, non la singola finestra token del provider.",
        "",
        "## Stato",
        "",
        *status_lines(pointer, causality),
        "",
        "## Risposta ricostruita dai blocchi",
        "",
    ]
    if not rendered:
        lines.extend(["- Nessun blocco accettato disponibile. Il prodotto resta bloccato; vedere storia e peer review.", ""])
    for index, block in enumerate(rendered, start=1):
        lines.extend(block_section(f"Proposal block {index}", block, max_chars))

    blocking = composer.get("blocking_issues") if isinstance(composer.get("blocking_issues"), list) else []
    if blocking:
        lines.extend(["## Blocking issues", ""])
        lines.extend(f"- {item}" for item in blocking)
        lines.append("")

    if include_peer_blocks:
        lines.extend(["## GPU0 reviewer/refiner blocks", ""])
        for index, block in enumerate(gpu0, start=1):
            lines.extend(block_section(f"GPU0 block {index}", block, max_chars))
        lines.extend(["## NPU audit blocks", ""])
        for index, block in enumerate(npu, start=1):
            lines.extend(block_section(f"NPU block {index}", block, max_chars))

    stats = {
        "proposal_block_count": len(proposals),
        "accepted_proposal_block_count": len(accepted),
        "rendered_proposal_block_count": len(rendered),
        "gpu1_block_count": len(gpu1),
        "gpu0_block_count": len(gpu0),
        "npu_block_count": len(npu),
        "blocking_issue_count": len(blocking),
    }
    return "\n".join(lines).rstrip() + "\n", stats


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pointer-manifest", required=True)
    parser.add_argument("--composer-json", default="")
    parser.add_argument("--causality-json", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--json-output", default="")
    parser.add_argument("--max-block-chars", type=int, default=12000)
    parser.add_argument("--include-rejected-history", action="store_true")
    parser.add_argument("--include-peer-blocks", action="store_true")
    args = parser.parse_args()

    pointer_path = Path(args.pointer_manifest).resolve()
    pointer = read_json(str(pointer_path))
    if not pointer:
        raise SystemExit(f"pointer manifest unreadable: {pointer_path}")
    composer = read_json(args.composer_json)
    causality = read_json(args.causality_json)
    output = Path(args.output).resolve() if args.output else pointer_path.with_name("external_heap_primary_long_response.md")
    json_output = Path(args.json_output).resolve() if args.json_output else output.with_suffix(".json")
    markdown, stats = build_markdown(
        pointer,
        composer,
        causality,
        max_chars=args.max_block_chars,
        include_rejected_history=args.include_rejected_history,
        include_peer_blocks=args.include_peer_blocks,
    )
    report = {
        "schema_version": 1,
        "kind": "external_heap_primary_long_response_composer",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "pointer_manifest": str(pointer_path),
        "composer_json": str(Path(args.composer_json).resolve()) if args.composer_json else "",
        "causality_json": str(Path(args.causality_json).resolve()) if args.causality_json else "",
        "output": str(output),
        "stats": stats,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": [],
    }
    write_text(output, markdown)
    write_json(json_output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
