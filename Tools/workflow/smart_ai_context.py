#!/usr/bin/env python3
"""Smart hierarchical AI context packets.

Instead of cutting prompts blindly, this script decomposes project data into
capsules, ranks them for a task, and writes rich JSON/Markdown intermediates.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_MAX_PACKET_CHARS = 22000
DEFAULT_MAX_CAPSULE_CHARS = 3200


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.strip().lower())
    return re.sub(r"_+", "_", value).strip("_") or "track"


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()


def compact(value: Any, limit: int = 900) -> str:
    text = " ".join(str(value or "").split())
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def keywords(text: str, limit: int = 24) -> list[str]:
    words = re.findall(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9_]{4,}", text.lower())
    stop = {
        "json",
        "true",
        "false",
        "none",
        "null",
        "path",
        "file",
        "data",
        "output",
        "input",
        "della",
        "delle",
        "come",
        "sono",
        "deve",
    }
    counts: dict[str, int] = {}
    for word in words:
        if word not in stop and not word.isdigit():
            counts[word] = counts.get(word, 0) + 1
    return [w for w, _ in sorted(counts.items(), key=lambda i: (-i[1], i[0]))[:limit]]


def read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8", errors="replace"))
    except Exception:
        return None


def read_text(path: Path, limit: int = 240000) -> str:
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[:limit]


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(root.resolve(strict=False)).as_posix()
    except Exception:
        return str(path)


def capsule(
    source: str, path: str, kind: str, title: str, value: Any, priority: int, max_chars: int
) -> dict[str, Any]:
    content = value if isinstance(value, str) else json.dumps(value, indent=2, ensure_ascii=False)
    if len(content) > max_chars:
        content = content[:max_chars].rstrip() + "\n..."
    summary = compact(content, 800)
    cid = sha(f"{source}:{path}:{title}:{sha(content)[:12]}")[:16]
    return {
        "capsule_id": cid,
        "source": source,
        "path": path,
        "kind": kind,
        "title": title,
        "priority": priority,
        "size_chars": len(content),
        "sha256": sha(content),
        "keywords": keywords(title + " " + summary),
        "summary": summary,
        "content": content,
    }


def json_capsules(source: str, path: str, data: Any, max_chars: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(data, dict):
        important = [
            "track_identity",
            "analysis_summary",
            "track_summary",
            "scene_preferences",
            "conversation_memory",
            "pipeline_state",
            "technical_files",
            "must_keep",
            "workflow_policy",
            "segments",
            "frames",
            "recommended_scene_plan",
            "audio_mapping_plan",
            "implementation_plan",
            "scene_script",
            "support_files",
            "safety",
        ]
        for key in important:
            if key not in data:
                continue
            value = data[key]
            if key == "frames" and isinstance(value, list):
                value = {"frame_count": len(value), "first": value[:2], "last": value[-2:]}
                out.append(
                    capsule(
                        source,
                        f"{path}.frames.manifest",
                        "frame_manifest",
                        "Full Blender keyframes manifest",
                        value,
                        10,
                        max_chars,
                    )
                )
            elif key == "segments" and isinstance(value, list):
                for idx, start in enumerate(range(0, len(value), 8), start=1):
                    out.append(
                        capsule(
                            source,
                            f"{path}.segments[{start}:{start + 8}]",
                            "music_segments",
                            f"Music segment capsule {idx}",
                            value[start : start + 8],
                            8,
                            max_chars,
                        )
                    )
            else:
                prio = (
                    9
                    if key
                    in {
                        "scene_preferences",
                        "conversation_memory",
                        "pipeline_state",
                        "technical_files",
                    }
                    else 7
                )
                out.append(
                    capsule(source, f"{path}.{key}", "json_section", key, value, prio, max_chars)
                )
        rest = {k: v for k, v in data.items() if k not in important}
        if rest:
            out.append(
                capsule(
                    source,
                    f"{path}.remaining",
                    "json_remainder",
                    f"Remainder of {path}",
                    rest,
                    4,
                    max_chars,
                )
            )
    elif isinstance(data, list):
        for idx, start in enumerate(range(0, len(data), 12), start=1):
            out.append(
                capsule(
                    source,
                    f"{path}[{start}:{start + 12}]",
                    "json_list_chunk",
                    f"List chunk {idx}",
                    data[start : start + 12],
                    5,
                    max_chars,
                )
            )
    return out


def text_capsules(source: str, path: str, text: str, max_chars: int) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for idx, start in enumerate(range(0, len(text), max_chars), start=1):
        chunk = text[start : start + max_chars]
        if chunk.strip():
            title = compact(chunk.splitlines()[0] if chunk.splitlines() else path, 120)
            out.append(
                capsule(source, f"{path}#chunk-{idx}", "text_chunk", title, chunk, 5, max_chars)
            )
    return out


def discover(repo: Path, track: str, explicit: list[str]) -> list[Path]:
    paths: list[Path] = []
    for item in explicit:
        p = Path(item)
        if not p.is_absolute():
            p = repo / p
        if p.exists() and p.is_file():
            paths.append(p)
    out = repo / "output"
    for name in [
        f"{track}_scene_brief.json",
        f"{track}_music_context.json",
        f"{track}_analysis_ai_context.json",
        f"{track}_analysis_blender_keyframes.json",
        f"{track}_dual_ai_scene_plan.json",
        f"{track}_ai_implementation_draft.json",
        "spaziotempo_asset_inventory.json",
    ]:
        p = out / name
        if p.exists():
            paths.append(p)
    for p in [
        repo / "docs" / "LOCAL_WORKSTATION_TARGET.md",
        repo / "indexAI" / "project_code_index.md",
        repo / "indexAI" / "project_code_manifest.json",
        repo / "indexAI" / "task_capsules" / "blender_51_compat.json",
        repo / "indexAI" / "task_capsules" / "resource_budget.json",
        repo / "Tools" / "npu" / "npu_music_context.md",
        repo / "Tools" / "npu" / "npu_code_index.md",
    ]:
        if p.exists():
            paths.append(p)
    seen: set[str] = set()
    unique: list[Path] = []
    for p in paths:
        k = str(p.resolve(strict=False)).lower()
        if k not in seen:
            seen.add(k)
            unique.append(p)
    return unique


def build_capsules(
    repo: Path, track: str, explicit: list[str], max_chars: int
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for p in discover(repo, track, explicit):
        r = rel(p, repo)
        src = p.stem
        if p.suffix.lower() == ".json":
            data = read_json(p)
            if data is not None:
                out.extend(json_capsules(src, r, data, max_chars))
        elif p.suffix.lower() in {".md", ".txt", ".py"}:
            out.extend(text_capsules(src, r, read_text(p), max_chars))
    return out


def score(c: dict[str, Any], task: str) -> float:
    t = set(keywords(task, 80))
    h = set(c.get("keywords") or []) | set(
        keywords(c.get("path", "") + " " + c.get("summary", ""), 80)
    )
    return len(t & h) * 3.0 + float(c.get("priority", 0)) * 0.4


def build_packet(
    repo: Path, track: str, task: str, explicit: list[str], max_packet: int, max_capsule: int
) -> dict[str, Any]:
    caps = build_capsules(repo, track, explicit, max_capsule)
    ranked = sorted(caps, key=lambda c: score(c, task), reverse=True)
    selected: list[dict[str, Any]] = []
    used = 0
    for c in ranked:
        need = int(c.get("size_chars", 0)) + 420
        if selected and used + need > max_packet:
            continue
        selected.append(c)
        used += need
        if used >= max_packet:
            break
    ids = {c["capsule_id"] for c in selected}
    manifest = [
        {
            k: c[k]
            for k in [
                "capsule_id",
                "source",
                "path",
                "kind",
                "title",
                "priority",
                "size_chars",
                "sha256",
                "keywords",
            ]
        }
        | {"selected": c["capsule_id"] in ids, "rank_score": round(score(c, task), 4)}
        for c in ranked
    ]
    return {
        "schema_version": 1,
        "kind": "smart_ai_context_packet",
        "generated_at": now_iso(),
        "track_stem": track,
        "task": task,
        "policy": {
            "method": "hierarchical_chunked_context",
            "full_data_rule": "Selected capsules are passed now; full files remain referenced by path and sha256.",
            "token_strategy": "Expand by capsule_id, not by dumping all project files into one prompt.",
        },
        "counts": {
            "capsules_total": len(caps),
            "capsules_selected": len(selected),
            "packet_chars_estimate": used,
        },
        "selected_capsules": selected,
        "capsule_manifest": manifest,
    }


def write_md(packet: dict[str, Any], path: Path) -> None:
    lines = [
        "# Smart AI Context Packet",
        "",
        f"Generated: `{packet['generated_at']}`",
        f"Track: `{packet['track_stem']}`",
        f"Task: `{packet['task']}`",
        "",
        "## Selected Capsules",
    ]
    for c in packet.get("selected_capsules", []):
        lines += [
            "",
            f"### {c['capsule_id']} — {c['title']}",
            f"- Path: `{c['path']}`",
            f"- Kind: `{c['kind']}`",
            f"- SHA: `{c['sha256']}`",
            "",
            c.get("summary", ""),
        ]
    lines += ["", "## Manifest"]
    for m in packet.get("capsule_manifest", [])[:160]:
        lines.append(
            f"- `{m['capsule_id']}` [{'selected' if m['selected'] else 'available'}] `{m['path']}` score={m['rank_score']}"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    ap.add_argument("--track-stem", required=True)
    ap.add_argument("--task", default="Scene Director and Blender Python generation context")
    ap.add_argument("--include-file", action="append", default=[])
    ap.add_argument("--output-dir", default="output/ai_pipeline/smart_context")
    ap.add_argument("--max-packet-chars", type=int, default=DEFAULT_MAX_PACKET_CHARS)
    ap.add_argument("--max-capsule-chars", type=int, default=DEFAULT_MAX_CAPSULE_CHARS)
    args = ap.parse_args()
    repo = Path(args.repo_root).resolve()
    out = Path(args.output_dir).resolve()
    out.mkdir(parents=True, exist_ok=True)
    slug = slugify(args.track_stem)
    packet = build_packet(
        repo,
        args.track_stem,
        args.task,
        args.include_file,
        args.max_packet_chars,
        args.max_capsule_chars,
    )
    packet_path = out / f"{slug}_smart_context_packet.json"
    manifest_path = out / f"{slug}_smart_context_manifest.json"
    md_path = out / f"{slug}_smart_context_packet.md"
    packet_path.write_text(
        json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    manifest_path.write_text(
        json.dumps(packet["capsule_manifest"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    write_md(packet, md_path)
    print(
        json.dumps(
            {
                "packet": str(packet_path),
                "manifest": str(manifest_path),
                "markdown": str(md_path),
                "counts": packet["counts"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
