"""CLI for building the project AI index."""

from __future__ import annotations

import argparse

from .builder import build_project_ai_index
from .config import DEFAULT_MAX_CHUNK_CHARS

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build primary project code index for AI patch planning."
    )
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--max-chunk-chars", type=int, default=DEFAULT_MAX_CHUNK_CHARS)
    args = parser.parse_args()
    build_project_ai_index(force=args.force, max_chunk_chars=args.max_chunk_chars)


if __name__ == "__main__":
    main()
