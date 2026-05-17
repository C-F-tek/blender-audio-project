"""CLI for building NPU knowledge broker packets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .builder import build_packet
from .common import repo_relative, resolve_repo_path
from .constants import PACKET_KIND
from .markdown import render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--objective", required=True)
    parser.add_argument("--selected-chunks", default="")
    parser.add_argument("--context-pack", default="")
    parser.add_argument("--adapter-manifest", default="")
    parser.add_argument("--output", default="output/ai_pipeline/npu_knowledge_broker_packet.json")
    parser.add_argument(
        "--markdown-output", default="output/ai_pipeline/npu_knowledge_broker_packet.md"
    )
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
    print(
        json.dumps(
            {
                "passed": True,
                "kind": PACKET_KIND,
                "candidate_count": packet["candidate_count"],
                "output": repo_relative(output, repo_root),
                "markdown_output": repo_relative(markdown_output, repo_root),
            },
            indent=2,
            ensure_ascii=False,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
