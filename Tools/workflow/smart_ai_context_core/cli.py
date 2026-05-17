from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import DEFAULT_MAX_CAPSULE_CHARS, DEFAULT_MAX_PACKET_CHARS, slugify
from .packet import build_packet, write_md


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--track-stem", required=True)
    parser.add_argument("--task", default="Scene Director and Blender Python generation context")
    parser.add_argument("--include-file", action="append", default=[])
    parser.add_argument("--output-dir", default="output/ai_pipeline/smart_context")
    parser.add_argument("--max-packet-chars", type=int, default=DEFAULT_MAX_PACKET_CHARS)
    parser.add_argument("--max-capsule-chars", type=int, default=DEFAULT_MAX_CAPSULE_CHARS)
    args = parser.parse_args()

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
    packet_path.write_text(json.dumps(packet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
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
