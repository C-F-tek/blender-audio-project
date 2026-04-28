#!/usr/bin/env python3
"""Hierarchical AI context packets for smart prompt decomposition.

This module does not shrink knowledge. It decomposes project knowledge into
addressable capsules, ranks them for the current task, and writes rich JSON/MD
intermediate artifacts that any AI can inspect later.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_OUTPUT_DIR = ROOT / "output" / "ai_pipeline" / "smart_context"
DEFAULT_MAX_PACKET_CHARS = 22000
DEFAULT_MAX_CAPSULE_CHARS = 3200


@dataclass
class ContextCapsule:
    capsule_id: str
    source: str
    path: str
    kind: str
    title: str
    priority: int
    size_chars: int
    sha256: str
    keywords: list[str]
    summary: str
    content: str


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "_", value)
    value = re.sub(r"_+", "_", value).strip("_")
    return value or "context"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def compact_text(value: Any, limit: int = 800) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def keywordize(text: str, max_items: int = 24) -> list[str]:
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_]{4,}", text.lower())
    stop = {"this", "that", "with", "from", "sono", "come", "deve", "della", "delle", "json", "true", "false", "none", "null", "path", "file", "data", "output", "input"}
    counts: dict[str, int] = {}
    for word in words:
        if word in stop or word.isdigit():
            continue
        counts[word] = counts.get(word, 0) + 1
    return [word for word, _count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:max_items]]


def read_text(path: Path, limit: int | None = None) -> str:
    if not path.exists() or not path.is_file():
        return ""
    text = path.read_text(encoding="utf-8", errors="replace")
    return text if limit is None else text[:limit]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def add_capsule(capsules: list[ContextCapsule], source: str, path: str, kind: str, title: str, value: Any, priority: int, max_chars: int) -> None:
    content = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    if len(content) > max_chars:
        content = content[:max_chars].rstrip() + "\n..."
    summary = compact_text(content, 750)
    raw_id = f"{source}:{path}:{title}:{sha256_text(content)[:10]}"
    capsules.append(ContextCapsule(
        capsule_id=sha256_text(raw_id)[:16],
        source=source,
        path=path,
        kind=kind,
        title=title,
        priority=priority,
        size_chars=len(content),
        sha256=sha256_text(content),
        keywords=keywordize(title + " " + summary),
        summary=summary,
        content=content,
    ))


def json_capsules(source: str, rel_path: str, data: Any, max_chars: int) -> list[ContextCapsule]:
    capsules: list[ContextCapsule] = []
    if isinstance(data, dict):
        important = ["track_identity", "analysis_summary", "track_summary", "scene_preferences", "conversation_memory", "pipeline_state", "technical_files", "must_keep", "workflow_policy", "segments", "frames", "recommended_scene_plan", "audio_mapping_plan", "implementation_plan", "scene_script", "support_files", "safety"]
        for key in important:
            if key not in data:
                continue
            value = data[key]
            if key == "frames" and isinstance(value, list):
                add_capsule(capsules, source, f"{rel_path}.{key}.manifest", "frame_manifest", "Full Blender keyframes manifest", {"frame_count": len(value), "first": value[:2], "last": value[-2:]}, 10, max_chars)
            elif key == "segments" and isinstance(value, list):
                for idx, start in enumerate(range(0, len(value), 8), start=1):
                    add_capsule(capsules, source, f"{rel_path}.{key}[{start}:{start + 8}]", "music_segments", f"Music segments {idx}", value[start:start + 8], 8, max_chars)
            else:
                add_capsule(capsules, source, f"{rel_path}.{key}", "json_section", key, value, 9 if key in {"scene_preferences", "conversation_memory", "pipeline_state", "technical_files"} else 7, max_chars)
        remaining = {k: v for k, v in data.items() if k not in important}
        if remaining:
            add_capsule(capsules, source, f"{rel_path}.remaining", "json_remainder", f"Remainder of {rel_path}", remaining, 4, max_chars)
    elif isinstance(data, list):
        for idx, start in enumerate(range(0, len(data), 12), start=1):
            add_capsule(capsules, source, f"{rel_path}[{start}:{start + 12}]", "json_list_chunk", f"List chunk {idx}", data[start:start + 12], 5, max_chars)
    else:
        add_capsule(capsules, source, rel_path, "json_scalar", rel_path, data, 3, max_chars)
    return capsules


def text_capsules(source: str, rel_path: str, text: str, max_chars: int) -> list[ContextCapsule]:
    capsules: list[ContextCapsule] = []
    if not text.strip():
        return capsules
    paragraphs = re.split(r"\n(?=#|##|###|\- |\d+\.)", text)
    current = ""
    index = 1
    for paragraph in paragraphs:
        if current and len(current) + len(paragraph) + 2 > max_chars:
            title = compact_text(current.splitlines()[0] if current.splitlines() else rel_path, 120)
            add_capsule(capsules, source, f"{rel_path}#chunk-{index}", "text_chunk", title, current, 5, max_chars)
            current = paragraph
            index += 1
        else:
            current = (current + "\n" + paragraph).strip()
    if current:
        title = compact_text(current.splitlines()[0] if current.splitlines() else rel_path, 120)
        add_capsule(capsules, source, f"{rel_path}#chunk-{index}", "text_chunk", title, current, 5, max_chars)
    return capsules


def rel_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except Exception:
        return str(path)


def discover_sources(repo_root: Path, track_stem: str, explicit_files: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in explicit_files:
        path = Path(item)
        if not path.is_absolute():
            path = repo_root / path
        if path.exists() and path.is_file():
            paths.append(path)
    out = repo_root / "output"
    for name in [f"{track_stem}_scene_brief.json", f"{track_stem}_music_context.json", f"{track_stem}_analysis_ai_context.json", f"{track_stem}_analysis_blender_keyframes.json", f"{track_stem}_dual_ai_scene_plan.json", f"{track_stem}_ai_implementation_draft.json", "spaziotempo_asset_inventory.json"]:
        path = out / name
        if path.exists():
            paths.append(path)
    for path in [repo_root / "docs" / "LOCAL_WORKSTATION_TARGET.md", repo_root / "indexAI" / "project_code_index.md", repo_root / "indexAI" / "project_code_manifest.json", repo_root / "indexAI" / "task_capsules" / "blender_51_compat.json", repo_root / "indexAI" / "task_capsules" / "resource_budget.json", repo_root / "Tools" / "npu" / "npu_music_context.md", repo_root / "Tools" / "npu" / "npu_code_index.md"]:
        if path.exists():
            paths.append(path)
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = str(path.resolve(strict=False)).lower()
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def build_capsules(repo_root: Path, track_stem: str, explicit_files: list[str], max_capsule_chars: int) -> list[ContextCapsule]:
    capsules: list[ContextCapsule] = []
    for path in discover_sources(repo_root, track_stem, explicit_files):
        rel = rel_path(path, repo_root)
        source = path.stem
        if path.suffix.lower() == ".json":
            data = read_json(path)
            if data is not None:
                capsules.extend(json_capsules(source, rel, data, max_capsule_chars))
        elif path.suffix.lower() in {".md", ".txt", ".py"}:
            capsules.extend(text_capsules(source, rel, read_text(path, 240000), max_capsule_chars))
    return capsules


def rank_score(capsule: ContextCapsule, task: str) -> float:
    tokens = set(keywordize(task, 80))
    hay = set(capsule.keywords)
    hay.update(keywordize(capsule.path + " " + capsule.title + " " + capsule.summary, 80))
    overlap = len(tokens & hay)
    return overlap * 3.0 + capsule.priority * 0.4


def build_packet(repo_root: Path, track_stem: str, task: str, explicit_files: list[str], max_packet_chars: int, max_capsule_chars: int) -> dict[str, Any]:
    capsules = build_capsules(repo_root, track_stem, explicit_files, max_capsule_chars)
    ranked = sorted(capsules, key=lambda item: rank_score(item, task), reverse=True)
    selected: list[ContextCapsule] = []
    used = 0
    for capsule in ranked:
        estimated = len(capsule.content) + 420
        if selected and used + estimated > max_packet_chars:
            continue
        selected.append(capsule)
        used += estimated
        if used >= max_packet_chars:
            break
    selected_ids = {item.capsule_id for item in selected}
    return {
        "schema_version": 1,
        "kind": "smart_ai_context_packet",
        "generated_at": now_iso(),
        "track_stem": track_stem,
        "task": task,
        "policy": {
            "method": "hierarchical_chunked_context",
            "max_packet_chars": max_packet_chars,
            "max_capsule_chars": max_capsule_chars,
            "full_data_rule": "Selected capsules are passed to the AI; full files remain referenced by path and sha256.",
            "token_strategy": "Expand by capsule_id, not by dumping all project files into one prompt.",
        },
        "counts": {"capsules_total": len(capsules), "capsules_selected": len(selected), "packet_chars_estimate": used},
        "selected_capsules": [asdict(item) for item in selected],
        "capsule_manifest": [
            {"capsule_id": item.capsule_id, "source": item.source, "path": item.path, "kind": item.kind, "title": item.title, "priority": item.priority, "size_chars": item.size_chars, "sha256": item.sha256, "keywords": item.keywords, "selected": item.capsule_id in selected_ids, "rank_score": round(rank_score(item, task), 4)}
            for item in ranked
        ],
        "next_context_actions": [
            "If confidence is low, request one or more capsule_id values instead of expanding the whole context.",
            "Use frame manifests for planning; load the full keyframe JSON only in generated/runtime Blender code.",
            "Run NPU guardrail review on this packet before heavy Ollama/GPU generation.",
        ],
    }


def write_markdown(packet: dict[str, Any], path: Path) -> None:
    lines = ["# Smart AI Context Packet", "", f"Generated: `{packet.get('generated_at')}`", f"Track: `{packet.get('track_stem')}`", f"Task: `{packet.get('task')}`", "", "## Selected Capsules"]
    for capsule in packet.get("selected_capsules", []):
        lines.extend(["", f"### {capsule.get('capsule_id')} — {capsule.get('title')}", f"- Source: `{capsule.get('source')}`", f"- Path: `{capsule.get('path')}`", f"- Kind: `{capsule.get('kind')}`", f"- SHA-256: `{capsule.get('sha256')}`", "", capsule.get("summary") or ""])
    lines.extend(["", "## Manifest"])
    for item in packet.get("capsule_manifest", [])[:160]:
        mark = "selected" if item.get("selected") else "available"
        lines.append(f"- `{item.get('capsule_id')}` [{mark}] `{item.get('path')}` score={item.get('rank_score')}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--track-stem", required=True)
    ap.add_argument("--task", default="Scene Director and Blender Python generation context")
    ap.add_argument("--include-file", action="append", default=[])
    ap.add_argument("--output-dir", default=str(DEFAULT_OUTPUT_DIR))
    ap.add_argument("--max-packet-chars", type=int, default=DEFAULT_MAX_PACKET_CHARS)
    ap.add_argument("--max-capsule-chars", type=int, default=DEFAULT_MAX_CAPSULE_CHARS)
    args = ap.parse_args()
    repo_root = Path(args.repo_root).resolve()
    out_dir = Path(args.output_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.track_stem)
    packet = build_packet(repo_root, args.track_stem, args.task, args.include_file, args.max_packet_chars, args.max_capsule_chars)
    packet_path = out_dir / f"{slug}_smart_context_packet.json"
    manifest_path = out_dir / f"{slug}_smart_context_manifest.json"
    md_path = out_dir / f"{slug}_smart_context_packet.md"
    packet_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    manifest_path.write_text(json.dumps(packet.get("capsule_manifest", []), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    write_markdown(packet, md_path)
    print(json.dumps({"packet": str(packet_path), "manifest": str(manifest_path), "markdown": str(md_path), "counts": packet.get("counts")}, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
