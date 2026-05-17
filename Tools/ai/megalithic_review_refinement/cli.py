"""CLI for megalithic review refinement."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .common import (
    DEFAULT_MARKDOWN,
    DEFAULT_OUTPUT,
    DEFAULT_PROPOSALS,
    DEFAULT_PROPOSALS_OUTPUT,
    DEFAULT_REVIEW,
    read_json,
    write_json,
)
from .report import refine_review, render_markdown

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--review", default=DEFAULT_REVIEW)
    parser.add_argument(
        "--proposals",
        default=DEFAULT_PROPOSALS,
        help="Original proposals artifact; currently read for provenance only.",
    )
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--proposal-output", default=DEFAULT_PROPOSALS_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    args = parser.parse_args()

    review = read_json(Path(args.review))
    read_json(Path(args.proposals)) if Path(args.proposals).exists() else {}
    refined, proposals = refine_review(review)
    write_json(Path(args.output), refined)
    write_json(Path(args.proposal_output), proposals)
    markdown_output = Path(args.markdown_output)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text(render_markdown(refined, proposals), encoding="utf-8")
    print(
        json.dumps(
            {
                "passed": refined["passed"],
                "output": args.output,
                "proposal_output": args.proposal_output,
                "markdown": args.markdown_output,
                "proposal_count": proposals["proposal_count"],
                "provider_execution_performed": refined["provider_execution_performed"],
                "patch_application_performed": False,
            },
            indent=2,
        )
    )
    return 0
