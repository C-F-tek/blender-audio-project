"""CLI entrypoint for track-summary generation."""

from __future__ import annotations

import argparse
from pathlib import Path

from .defaults import default_analysis_json, default_summary_json
from .summary import TrackSummaryBuilder, TrackSummaryOptions


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create a technical summary from analysis JSON.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--analysis-json")
    parser.add_argument("--out-json")
    parser.add_argument("--skip-music-context", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    repo_root = Path(args.repo_root).expanduser().resolve()
    analysis_json = Path(args.analysis_json) if args.analysis_json else default_analysis_json(repo_root)
    out_json = Path(args.out_json) if args.out_json else default_summary_json(repo_root)
    if not analysis_json.is_absolute():
        analysis_json = repo_root / analysis_json
    if not out_json.is_absolute():
        out_json = repo_root / out_json

    TrackSummaryBuilder().build(
        TrackSummaryOptions(
            analysis_json=analysis_json,
            out_json=out_json,
            repo_root=repo_root,
            update_music_context=not args.skip_music_context,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
