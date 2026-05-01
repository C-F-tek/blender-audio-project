#!/usr/bin/env python3
"""Build a report-only NPU knowledge-broker/context-oracle packet.

The packet is deterministic. It does not execute OpenVINO, NPU, GPU, Ollama,
Blender, FFmpeg or any provider. It ranks local context candidates from existing
selected-chunks/context-pack/adapter-manifest metadata so a primary advisory
model can receive bounded, validated context.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PACKET_KIND = "npu_knowledge_broker_packet"
APPLY_MODE = "context_only"
NPU_ROLE = "knowledge_broker_context_oracle"

FORBIDDEN_PREFIXES = (
    ".git/",
    ".venv/",
    "venv/",
    "indexAI/agent_memory/",
    "output/patch_specs/",
    "Scripting/ready_to_jazz_wow_youtube_profiles_audio_sync/",
)
FORBIDDEN_EXACT = {"Scripting/shared/blender_compat.py"}
FORBIDDEN_FRAGMENTS = ("full_analysis", "analysis_full")


def repo_relative(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def resolve_repo_path(repo_root: Path, raw: str) -> Path:
    path = Path(raw)
    return path.resolve() if path.is_absolute() else (repo_root / path).resolve()


def normalize_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/")


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists() or not path.is_file():
        return {}
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def path_allowed(path: str) -> bool:
    normalized = normalize_path(path)
    if not normalized or Path(normalized).is_absolute():
        return False
    if normalized in FORBIDDEN_EXACT:
        return False
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
        return False
    lower = normalized.lower()
    if any(fragment in lower for fragment in FORBIDDEN_FRAGMENTS) and lower.endswith(".json"):
        return False
    return True


def score_candidate(path: str, objective_terms: set[str], base_score: int = 0) -> tuple[int, list[str]]:
    text = normalize_path(path).lower()
    matched = sorted(term for term in objective_terms if term and term in text)
    score = base_score + len(matched) * 4
    if text.startswith("Tools/workflow/"):
        score += 8
    if text.startswith("Tools/ai/"):
        score += 7
    if text.startswith("Tools/validation/"):
        score += 7
    if text.startswith("Tools/npu/"):
        score += 6
    if text.startswith("docs/"):
        score += 4
    if "selected" in text or "chunk" in text:
        score += 3
    if "adapter" in text or "manifest" in text:
        score += 3
    if "npu" in text or "knowledge" in text or "broker" in text:
        score += 5
    return score, matched


def add_candidate(candidates: dict[str, dict[str, Any]], path: str, source: str, objective_terms: set[str], reason: str, base_score: int = 0) -> None:
    normalized = normalize_path(path)
    if not path_allowed(normalized):
        return
    score, matched = score_candidate(normalized, objective_terms, base_score)
    existing = candidates.get(normalized)
    if existing:
        existing["score"] = max(existing["score"], score)
        if source not in existing["sources"]:
            existing["sources"].append(source)
        if reason not in existing["reasons"]:
            existing["reasons"].append(reason)
        existing["matched_terms"] = sorted(set(existing["matched_terms"]) | set(matched))
        return
    candidates[normalized] = {
        "path": normalized,
        "score": score,
        "sources": [source],
        "reasons": [reason],
        "matched_terms": matched,
        "content_role": "candidate_context",
        "provider_execution_required": False,
        "source_write_allowed": False,
    }


def add_selected_chunks(candidates: dict[str, dict[str, Any]], repo_root: Path, selected_chunks: str, objective_terms: set[str]) -> list[str]:
    selected_path = resolve_repo_path(repo_root, selected_chunks)
    data = read_json(selected_path)
    source_paths: list[str] = []
    if not data:
        return source_paths
    add_candidate(candidates, repo_relative(selected_path, repo_root), "selected_chunks_bundle", objective_terms, "selected chunks bundle", 20)
    markdown_path = selected_path.with_suffix(".md")
    if markdown_path.exists():
        add_candidate(candidates, repo_relative(markdown_path, repo_root), "selected_chunks_markdown", objective_terms, "selected chunks markdown summary", 18)
    chunks = data.get("selected_chunks")
    if isinstance(chunks, list):
        for chunk in chunks:
            if not isinstance(chunk, dict):
                continue
            path = normalize_path(chunk.get("path"))
            if not path:
                continue
            source_paths.append(path)
            add_candidate(candidates, path, "selected_chunk_source", objective_terms, "source file referenced by selected chunk", int(chunk.get("score") or 0))
    return source_paths


def add_adapter_manifest(candidates: dict[str, dict[str, Any]], repo_root: Path, manifest: str, objective_terms: set[str]) -> list[str]:
    manifest_path = resolve_repo_path(repo_root, manifest)
    data = read_json(manifest_path)
    refs: list[str] = []
    if not data:
        return refs
    add_candidate(candidates, repo_relative(manifest_path, repo_root), "adapter_manifest", objective_terms, "local AI adapter manifest", 18)
    for key in ("context_files",):
        values = data.get(key)
        if isinstance(values, list):
            for item in values:
                path = normalize_path(item)
                refs.append(path)
                add_candidate(candidates, path, "adapter_manifest_context", objective_terms, "context file recorded by adapter manifest", 10)
    enrichment_outputs = data.get("enrichment_outputs")
    if isinstance(enrichment_outputs, dict):
        for key, item in enrichment_outputs.items():
            path = normalize_path(item)
            if path:
                refs.append(path)
                add_candidate(candidates, path, f"adapter_manifest_output:{key}", objective_terms, "enrichment output recorded by adapter manifest", 8)
    return refs


def add_context_pack(candidates: dict[str, dict[str, Any]], repo_root: Path, context_pack: str, objective_terms: set[str]) -> list[str]:
    pack_path = resolve_repo_path(repo_root, context_pack)
    data = read_json(pack_path)
    refs: list[str] = []
    if not data:
        return refs
    add_candidate(candidates, repo_relative(pack_path, repo_root), "context_pack", objective_terms, "bounded context pack", 16)
    md_path = pack_path.with_suffix(".md")
    if md_path.exists():
        add_candidate(candidates, repo_relative(md_path, repo_root), "context_pack_markdown", objective_terms, "bounded context pack markdown", 14)
    for key in ("included_files", "files", "context_files"):
        values = data.get(key)
        if isinstance(values, list):
            for item in values:
                if isinstance(item, dict):
                    path = normalize_path(item.get("path"))
                else:
                    path = normalize_path(item)
                if path:
                    refs.append(path)
                    add_candidate(candidates, path, f"context_pack:{key}", objective_terms, "file referenced by context pack", 7)
    return refs


def build_packet(repo_root: Path, objective: str, selected_chunks: str, context_pack: str, adapter_manifest: str, max_candidates: int) -> dict[str, Any]:
    objective_terms = {term.lower() for term in objective.replace("/", " ").replace("-", " ").replace("_", " ").split() if len(term) >= 3}
    candidates: dict[str, dict[str, Any]] = {}
    source_refs: dict[str, list[str]] = {
        "selected_chunks": [],
        "context_pack": [],
        "adapter_manifest": [],
    }

    if selected_chunks:
        source_refs["selected_chunks"] = add_selected_chunks(candidates, repo_root, selected_chunks, objective_terms)
    if context_pack:
        source_refs["context_pack"] = add_context_pack(candidates, repo_root, context_pack, objective_terms)
    if adapter_manifest:
        source_refs["adapter_manifest"] = add_adapter_manifest(candidates, repo_root, adapter_manifest, objective_terms)

    # Always keep core contract files visible as fallback context.
    fallback_files = [
        "AGENTS.md",
        "docs/LOCAL_AI_RUN_BOOTSTRAP.md",
        "docs/LOCAL_AI_WORKFLOW.md",
        "docs/LOCAL_AI_TASKS/full-context-ai-npu-golden-path.md",
        "Tools/ai/select_semantic_code_chunks.py",
        "Tools/validation/check_selected_semantic_chunks.py",
        "Tools/validation/check_local_ai_adapter_manifest.py",
        "Tools/workflow/run_local_ai_task_via_pipeline.ps1",
    ]
    for path in fallback_files:
        if (repo_root / path).exists():
            add_candidate(candidates, path, "fallback_contract", objective_terms, "core local AI/NPU contract file", 5)

    ranked = sorted(candidates.values(), key=lambda item: (-int(item["score"]), item["path"]))[:max_candidates]
    return {
        "schema_version": 1,
        "kind": PACKET_KIND,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repo_root": repo_root.as_posix(),
        "objective": objective,
        "npu_role": NPU_ROLE,
        "apply_mode": APPLY_MODE,
        "provider_execution_performed": False,
        "provider_execution_required": False,
        "source_writes_performed": False,
        "patch_application_performed": False,
        "primary_advisory_provider": "ollama_gpu",
        "npu_promoted_to_advisory": False,
        "openvino_gpu_primary_lane": False,
        "inputs": {
            "selected_chunks": normalize_path(selected_chunks),
            "context_pack": normalize_path(context_pack),
            "adapter_manifest": normalize_path(adapter_manifest),
        },
        "source_refs": source_refs,
        "candidate_count": len(ranked),
        "max_candidates": max_candidates,
        "candidate_context": ranked,
        "decision": {
            "knowledge_broker_packet_built": True,
            "provider_execution_seen": False,
            "source_writes_performed": False,
            "patch_application_performed": False,
            "npu_advisory_promotion_requested": False,
            "requires_primary_advisory_review": True,
        },
        "warnings": [],
        "errors": [],
    }


def render_markdown(packet: dict[str, Any]) -> str:
    lines = [
        "# NPU Knowledge Broker Packet",
        "",
        f"- Objective: {packet['objective']}",
        f"- NPU role: `{packet['npu_role']}`",
        f"- Apply mode: `{packet['apply_mode']}`",
        f"- Provider execution performed: `{packet['provider_execution_performed']}`",
        f"- NPU promoted to advisory: `{packet['npu_promoted_to_advisory']}`",
        f"- Candidate count: `{packet['candidate_count']}`",
        "",
        "## Candidate context",
        "",
    ]
    for item in packet["candidate_context"]:
        lines.append(f"### {item['path']}")
        lines.append(f"- Score: `{item['score']}`")
        lines.append(f"- Sources: `{', '.join(item['sources'])}`")
        if item.get("matched_terms"):
            lines.append(f"- Matched terms: `{', '.join(item['matched_terms'])}`")
        lines.append("- Reasons:")
        for reason in item.get("reasons", []):
            lines.append(f"  - {reason}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--selected-chunks", default="")
    parser.add_argument("--context-pack", default="")
    parser.add_argument("--adapter-manifest", default="")
    parser.add_argument("--output", default="output/ai_pipeline/npu_knowledge_broker_packet.json")
    parser.add_argument("--markdown-output", default="output/ai_pipeline/npu_knowledge_broker_packet.md")
    parser.add_argument("--max-candidates", type=int, default=24)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    packet = build_packet(
        repo_root=repo_root,
        objective=args.objective,
        selected_chunks=args.selected_chunks,
        context_pack=args.context_pack,
        adapter_manifest=args.adapter_manifest,
        max_candidates=args.max_candidates,
    )
    output = resolve_repo_path(repo_root, args.output)
    markdown_output = resolve_repo_path(repo_root, args.markdown_output)
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(packet), encoding="utf-8")
    print(json.dumps({
        "passed": True,
        "kind": PACKET_KIND,
        "candidate_count": packet["candidate_count"],
        "output": repo_relative(output, repo_root),
        "markdown_output": repo_relative(markdown_output, repo_root),
    }, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
