"""Markdown chunk writing for music context."""

from __future__ import annotations

import json
from pathlib import Path

from .common import CHUNK_DIR, rel_to_root, sha256_text

def markdown_table_rows(rows: list[dict], keys: list[str]) -> str:
    lines = ["|" + "|".join(keys) + "|", "|" + "|".join(["---"] * len(keys)) + "|"]
    for row in rows:
        lines.append("|" + "|".join(str(row.get(key, "")) for key in keys) + "|")
    return "\n".join(lines)

def write_chunk(path: Path, title: str, body: str) -> dict:
    text = f"# {title}\n\n{body.strip()}\n"
    path.write_text(text, encoding="utf-8")
    return {
        "path": rel_to_root(path),
        "chars": len(text),
        "sha256": sha256_text(text),
    }

def write_music_chunks(context: dict, scene_records: list[dict]) -> list[dict]:
    CHUNK_DIR.mkdir(parents=True, exist_ok=True)
    for old_chunk in CHUNK_DIR.glob("chunk_*.md"):
        old_chunk.unlink()

    chunks = []
    chunk_index = 1

    overview = {
        "analysis_summary": context.get("analysis_summary"),
        "track_summary": context.get("track_summary"),
        "ai_memory_context": context.get("ai_memory_context"),
        "scene_summaries": [record["summary"] for record in scene_records],
    }
    chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_music_overview.md"
    chunks.append(
        {
            "index": chunk_index,
            "kind": "overview",
            **write_chunk(
                chunk_path,
                "NPU Music Overview",
                f"```json\n{json.dumps(overview, indent=2, ensure_ascii=False)}\n```",
            ),
        }
    )
    chunk_index += 1

    for segment in context.get("segments", []):
        table = markdown_table_rows(
            segment.get("sampled_frames", []),
            ["time", "low", "mid", "high", "onset", "beat"],
        )
        payload = {key: value for key, value in segment.items() if key not in {"sampled_frames"}}
        body = [
            "## Segment Summary\n",
            f"```json\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n```\n",
            "## Sampled Frame Curve\n",
            table,
        ]
        chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_audio_segment_{segment['index']:03d}.md"
        chunks.append(
            {
                "index": chunk_index,
                "kind": "audio_segment",
                "segment_index": segment["index"],
                "start_sec": segment["start_sec"],
                "end_sec": segment["end_sec"],
                **write_chunk(
                    chunk_path, f"NPU Audio Segment {segment['index']:03d}", "\n\n".join(body)
                ),
            }
        )
        chunk_index += 1

    for record in scene_records:
        body = [
            "## Scene Summary\n",
            f"```json\n{json.dumps(record['summary'], indent=2, ensure_ascii=False)}\n```\n",
            "## Source\n",
            "```text\n",
            record["content"],
            "\n```",
        ]
        safe_name = Path(record["file"]).stem.replace(" ", "_")
        chunk_path = CHUNK_DIR / f"chunk_{chunk_index:03d}_scene_{safe_name}.md"
        chunks.append(
            {
                "index": chunk_index,
                "kind": "scene_spec",
                "source": record["file"],
                **write_chunk(chunk_path, f"NPU Scene Spec {record['file']}", "".join(body)),
            }
        )
        chunk_index += 1

    return chunks
