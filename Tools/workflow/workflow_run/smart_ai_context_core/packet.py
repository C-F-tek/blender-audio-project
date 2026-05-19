from __future__ import annotations

from pathlib import Path
from typing import Any

from .core import keywords, now_iso
from .discovery import build_capsules


def score(capsule: dict[str, Any], task: str) -> float:
    task_keywords = set(keywords(task, 80))
    capsule_keywords = set(capsule.get("keywords") or []) | set(
        keywords(capsule.get("path", "") + " " + capsule.get("summary", ""), 80)
    )
    return len(task_keywords & capsule_keywords) * 3.0 + float(capsule.get("priority", 0)) * 0.4


def build_packet(
    repo: Path, track: str, task: str, explicit: list[str], max_packet: int, max_capsule: int
) -> dict[str, Any]:
    capsules = build_capsules(repo, track, explicit, max_capsule)
    ranked = sorted(capsules, key=lambda item: score(item, task), reverse=True)
    selected = _select_capsules(ranked, max_packet)
    selected_ids = {item["capsule_id"] for item in selected}
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
            "capsules_total": len(capsules),
            "capsules_selected": len(selected),
            "packet_chars_estimate": _estimate_packet_chars(selected),
        },
        "selected_capsules": selected,
        "capsule_manifest": _manifest(ranked, selected_ids, task),
    }


def _select_capsules(ranked: list[dict[str, Any]], max_packet: int) -> list[dict[str, Any]]:
    selected: list[dict[str, Any]] = []
    used = 0
    for capsule in ranked:
        need = int(capsule.get("size_chars", 0)) + 420
        if selected and used + need > max_packet:
            continue
        selected.append(capsule)
        used += need
        if used >= max_packet:
            break
    return selected


def _estimate_packet_chars(selected: list[dict[str, Any]]) -> int:
    return sum(int(capsule.get("size_chars", 0)) + 420 for capsule in selected)


def _manifest(ranked: list[dict[str, Any]], selected_ids: set[str], task: str) -> list[dict[str, Any]]:
    keys = [
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
    return [
        {key: capsule[key] for key in keys}
        | {
            "selected": capsule["capsule_id"] in selected_ids,
            "rank_score": round(score(capsule, task), 4),
        }
        for capsule in ranked
    ]


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
    for capsule in packet.get("selected_capsules", []):
        lines += [
            "",
            f"### {capsule['capsule_id']} - {capsule['title']}",
            f"- Path: `{capsule['path']}`",
            f"- Kind: `{capsule['kind']}`",
            f"- SHA: `{capsule['sha256']}`",
            "",
            capsule.get("summary", ""),
        ]
    lines += ["", "## Manifest"]
    for item in packet.get("capsule_manifest", [])[:160]:
        state = "selected" if item["selected"] else "available"
        lines.append(f"- `{item['capsule_id']}` [{state}] `{item['path']}` score={item['rank_score']}")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
