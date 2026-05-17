#!/usr/bin/env python3
"""Build an external heap block-pointer manifest from a run directory.

The manifest is external to the gate. It models the heap/universe product
contract as persistent blocks with navigation and refinement pointers:

- previous_block_id / next_block_id for forward continuation;
- refines_block_id for back-refinement;
- resume_from_block_id for continuing after a rewrite;
- role ownership for gpu1_planner, gpu0_reviewer_refiner and npu_auditor.

These pointers are not a side channel: they are the product graph used to recover
old decisions, backtrack, refine, resume, and compose the final long-form heap
answer beyond a single provider token window. Provider execution evidence remains
a separate guardrail flag and must not be inferred from block presence alone.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

DEFAULT_ROLES = ("gpu1_planner", "gpu0_reviewer_refiner", "npu_auditor")
POINTER_PRODUCT_CONTRACT = {
    "product_contract": True,
    "decision_recovery": True,
    "supports_forward_navigation": True,
    "supports_backrefinement": True,
    "supports_resume": True,
    "provider_execution_is_separate_guardrail": True,
}
EXECUTION_TRUE_PATTERNS = (
    re.compile(
        r"\b(provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)\b\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"[\"'](provider_execution_performed|gpu0_provider_execution_performed|gpu1_provider_execution_performed|npu_provider_execution_performed|workload_performed)[\"']\s*:\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(NPU|GPU|provider|workload)[^\n]{0,120}\bperformed\s*[:=]\s*true\b",
        re.IGNORECASE,
    ),
    re.compile(r"\bperformed\s*=\s*true\b", re.IGNORECASE),
)
EXECUTION_BOOL_KEYS = {
    "provider_execution_performed",
    "gpu0_provider_execution_performed",
    "gpu1_provider_execution_performed",
    "npu_provider_execution_performed",
    "workload_performed",
}
WORKLOAD_CONTAINER_KEYS = {
    "npu_device_workload",
    "gpu_device_workload",
    "device_workload",
    "workload",
}


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def read_text(path: Path, limit: int) -> str:
    try:
        text = path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def compact_text(value: Any, limit: int) -> str:
    text = str(value or "")
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]\n"
    return text


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def mapping_has_execution_evidence(value: Any, parent_key: str = "") -> bool:
    if isinstance(value, dict):
        for key, item in value.items():
            key_text = str(key)
            key_lower = key_text.lower()
            if key_lower in EXECUTION_BOOL_KEYS and normalize_bool(item):
                return True
            if (
                key_lower == "performed"
                and parent_key.lower() in WORKLOAD_CONTAINER_KEYS
                and normalize_bool(item)
            ):
                return True
            if mapping_has_execution_evidence(item, key_text):
                return True
    elif isinstance(value, list):
        return any(mapping_has_execution_evidence(item, parent_key) for item in value)
    return False


def text_has_execution_evidence(text: str) -> bool:
    return any(pattern.search(text) for pattern in EXECUTION_TRUE_PATTERNS)


def provider_execution_evidence(data: dict[str, Any], preview: str) -> bool:
    return mapping_has_execution_evidence(data) or text_has_execution_evidence(preview)


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return str(path)


def stable_id(prefix: str, value: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8", errors="replace")).hexdigest()[:16]
    return f"{prefix}_{digest}"


def append_block(blocks: list[dict[str, Any]], block: dict[str, Any]) -> None:
    if not any(existing.get("block_id") == block.get("block_id") for existing in blocks):
        blocks.append(block)


def proposal_blocks(repo_root: Path, run_dir: Path, max_block_chars: int) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    proposal_dir = run_dir / "team_context" / "proposal_iterations"
    proposal_files = (
        sorted(proposal_dir.glob("heap_proposal_revision_*.json")) if proposal_dir.exists() else []
    )
    previous_id = ""
    for index, path in enumerate(proposal_files, start=1):
        data = read_json(path)
        md_path = path.with_suffix(".md")
        diagnostic_preview = read_text(md_path if md_path.exists() else path, max_block_chars)
        candidate_preview = compact_text(
            data.get("response_text") or data.get("proposal_text") or "",
            max_block_chars,
        )
        preview = candidate_preview or diagnostic_preview
        block_id = stable_id(
            "proposal", f"{repo_rel(repo_root, path)}:{data.get('revision')}:{index}"
        )
        block = {
            "block_id": block_id,
            "block_type": "proposal_chunk",
            "role": "gpu1_planner",
            "step_index": index,
            "revision": data.get("revision"),
            "source_path": repo_rel(repo_root, path),
            "markdown_path": repo_rel(repo_root, md_path) if md_path.exists() else "",
            "previous_block_id": previous_id,
            "next_block_id": "",
            "refines_block_id": (
                previous_id if data.get("quality_passed") is not True and previous_id else ""
            ),
            "resume_from_block_id": previous_id,
            "quality_passed": data.get("quality_passed"),
            "accepted": data.get("quality_passed") is True,
            "sha256": (
                hashlib.sha256(preview.encode("utf-8", errors="replace")).hexdigest()
                if preview
                else ""
            ),
            "preview": preview,
            "candidate_response_preview": candidate_preview,
            "diagnostic_preview": diagnostic_preview,
            "preview_source": (
                "candidate_response" if candidate_preview else "diagnostic_markdown"
            ),
            "pointer_contract": {
                "product_contract": True,
                "decision_recovery": True,
                "navigation_role": "proposal_chain",
                "can_continue_to_next": True,
                "can_backrefine": bool(previous_id),
                "requires_review": data.get("quality_passed") is not True,
            },
        }
        if previous_id:
            for existing in blocks:
                if existing.get("block_id") == previous_id:
                    existing["next_block_id"] = block_id
        append_block(blocks, block)
        previous_id = block_id
    return blocks


def provider_blocks(repo_root: Path, run_dir: Path, max_block_chars: int) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    provider_dir = run_dir / "provider_teamwork"
    provider_files = sorted(provider_dir.glob("*.json")) if provider_dir.exists() else []
    for index, path in enumerate(provider_files, start=1):
        data = read_json(path)
        lane = str(
            data.get("lane")
            or data.get("role")
            or data.get("report_kind")
            or data.get("kind")
            or path.stem
        ).lower()
        if "gpu0" in lane:
            role = "gpu0_reviewer_refiner"
            block_type = "review_refinement_block"
        elif "npu" in lane:
            role = "npu_auditor"
            block_type = "audit_block"
        else:
            role = "gpu1_planner"
            block_type = "provider_evidence_block"
        text = str(data.get("response_text") or "")
        if not text:
            text = json.dumps(data, indent=2, ensure_ascii=False)
        if max_block_chars > 0 and len(text) > max_block_chars:
            text = text[:max_block_chars] + "\n...[truncated]\n"
        block_id = stable_id("provider", f"{repo_rel(repo_root, path)}:{role}:{index}")
        provider_execution = provider_execution_evidence(data, text)
        append_block(
            blocks,
            {
                "block_id": block_id,
                "block_type": block_type,
                "role": role,
                "step_index": index,
                "source_path": repo_rel(repo_root, path),
                "previous_block_id": "",
                "next_block_id": "",
                "refines_block_id": "",
                "resume_from_block_id": "",
                "quality_passed": data.get("passed"),
                "provider_execution_performed": provider_execution,
                "sha256": (
                    hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
                    if text
                    else ""
                ),
                "preview": text,
                "pointer_contract": {
                    "product_contract": True,
                    "decision_recovery": True,
                    "navigation_role": "peer_decision_evidence",
                    "can_continue_to_next": False,
                    "can_backrefine": role == "gpu0_reviewer_refiner",
                    "requires_review": role != "gpu0_reviewer_refiner",
                },
            },
        )
    return blocks


def block_provider_execution_performed(block: dict[str, Any]) -> bool:
    """Return true only for explicit provider/workload execution evidence.

    Pointer blocks are part of the heap product contract and decision-recovery
    graph. Their presence is required for the final product, but it must not be
    used as proof that a provider or hardware workload actually executed.
    """
    if normalize_bool(block.get("provider_execution_performed")):
        return True
    preview = str(block.get("preview") or "")
    return text_has_execution_evidence(preview)


def build_pointer_edges(blocks: list[dict[str, Any]]) -> list[dict[str, str]]:
    ids = {str(block.get("block_id")) for block in blocks}
    edges: list[dict[str, str]] = []
    for block in blocks:
        source = str(block.get("block_id") or "")
        for field, edge_type in (
            ("previous_block_id", "previous"),
            ("next_block_id", "next"),
            ("refines_block_id", "refines"),
            ("resume_from_block_id", "resume_from"),
        ):
            target = str(block.get(field) or "")
            if source and target and target in ids:
                edges.append(
                    {
                        "source_block_id": source,
                        "target_block_id": target,
                        "edge_type": edge_type,
                    }
                )
    return edges


def build_report(
    repo_root: Path, run_dir: Path, max_block_chars: int, max_blocks: int
) -> dict[str, Any]:
    all_blocks = proposal_blocks(repo_root, run_dir, max_block_chars) + provider_blocks(
        repo_root, run_dir, max_block_chars
    )
    blocks = all_blocks[:max_blocks] if max_blocks > 0 else all_blocks
    edges = build_pointer_edges(blocks)
    roles_present = sorted({str(block.get("role")) for block in blocks if block.get("role")})
    all_roles_present = sorted(
        {str(block.get("role")) for block in all_blocks if block.get("role")}
    )
    accepted_blocks = [block for block in blocks if block.get("accepted") is True]
    rejected_blocks = [
        block
        for block in blocks
        if block.get("block_type") == "proposal_chunk" and block.get("accepted") is not True
    ]
    all_accepted_blocks = [block for block in all_blocks if block.get("accepted") is True]
    all_rejected_blocks = [
        block
        for block in all_blocks
        if block.get("block_type") == "proposal_chunk" and block.get("accepted") is not True
    ]
    return {
        "schema_version": 1,
        "kind": "external_heap_block_pointer_manifest",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "run_dir": repo_rel(repo_root, run_dir),
        "protocol": "external_heap_block_pointer_v1",
        "passed": True,
        "pointer_product_contract": POINTER_PRODUCT_CONTRACT,
        "pointer_contract_role": "product_graph_decision_recovery_and_long_response_composition",
        "provider_execution_semantics": "separate_guardrail_true_only_with_explicit_provider_or_workload_evidence",
        "roles_expected": list(DEFAULT_ROLES),
        "roles_present": roles_present,
        "all_roles_present": all_roles_present,
        "block_count": len(blocks),
        "source_block_count": len(all_blocks),
        "max_blocks_applied": max_blocks > 0 and len(all_blocks) > len(blocks),
        "edge_count": len(edges),
        "accepted_block_count": len(accepted_blocks),
        "source_accepted_block_count": len(all_accepted_blocks),
        "rejected_proposal_block_count": len(rejected_blocks),
        "source_rejected_proposal_block_count": len(all_rejected_blocks),
        "has_forward_pointers": any(edge.get("edge_type") == "next" for edge in edges),
        "has_backrefinement_pointers": any(edge.get("edge_type") == "refines" for edge in edges),
        "has_resume_pointers": any(edge.get("edge_type") == "resume_from" for edge in edges),
        "blocks": blocks,
        "edges": edges,
        "provider_execution_performed": any(
            block_provider_execution_performed(block) for block in all_blocks
        ),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": [],
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Block Pointer Manifest",
        "",
        f"- Protocol: `{report.get('protocol')}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Pointer product contract: `{report.get('pointer_product_contract')}`",
        f"- Pointer contract role: `{report.get('pointer_contract_role')}`",
        f"- Provider execution semantics: `{report.get('provider_execution_semantics')}`",
        f"- Block count: `{report.get('block_count')}`",
        f"- Source block count: `{report.get('source_block_count')}`",
        f"- Max blocks applied: `{report.get('max_blocks_applied')}`",
        f"- Edge count: `{report.get('edge_count')}`",
        f"- Roles present: `{report.get('roles_present')}`",
        f"- All roles present: `{report.get('all_roles_present')}`",
        f"- Forward pointers: `{report.get('has_forward_pointers')}`",
        f"- Back-refinement pointers: `{report.get('has_backrefinement_pointers')}`",
        f"- Resume pointers: `{report.get('has_resume_pointers')}`",
        "",
        "## Blocks",
        "",
    ]
    for block in report.get("blocks") or []:
        lines.extend(
            [
                f"### `{block.get('block_id')}`",
                "",
                f"- Type: `{block.get('block_type')}`",
                f"- Role: `{block.get('role')}`",
                f"- Source: `{block.get('source_path')}`",
                f"- Previous: `{block.get('previous_block_id')}`",
                f"- Next: `{block.get('next_block_id')}`",
                f"- Refines: `{block.get('refines_block_id')}`",
                f"- Resume from: `{block.get('resume_from_block_id')}`",
                f"- Accepted: `{block.get('accepted')}`",
                f"- Preview source: `{block.get('preview_source')}`",
                f"- Pointer contract: `{block.get('pointer_contract')}`",
                "",
            ]
        )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--max-block-chars", type=int, default=9000)
    parser.add_argument("--max-blocks", type=int, default=0)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    run_dir = Path(args.run_dir).resolve()
    output = (
        Path(args.output).resolve()
        if args.output
        else run_dir / "external_heap_block_pointer_manifest.json"
    )
    markdown_output = (
        Path(args.markdown_output).resolve() if args.markdown_output else output.with_suffix(".md")
    )
    report = build_report(repo_root, run_dir, args.max_block_chars, args.max_blocks)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
