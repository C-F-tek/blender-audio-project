from __future__ import annotations

from .common import *  # noqa: F403
from .reporting import write_outputs
from .runner import run_review

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--objective",
        default="Review Markdown documentation, code, RAW artifacts, SQLite memory metadata and provider tool inventories, then propose manual-review-only follow-up patches or docs updates.",
    )
    parser.add_argument("--include-all-docs", action="store_true")
    parser.add_argument("--include-all-code", action="store_true")
    parser.add_argument("--include-output", action="store_true")
    parser.add_argument("--include-index", action="store_true")
    parser.add_argument("--include-raw", action="store_true")
    parser.add_argument("--include-sqlite-memory", action="store_true")
    parser.add_argument("--max-files", type=int, default=0)
    parser.add_argument("--max-chars-per-file", type=int, default=80_000)
    parser.add_argument("--max-raw-files", type=int, default=500)
    parser.add_argument("--max-sqlite-tables", type=int, default=30)
    parser.add_argument("--file-sample-limit", type=int, default=240)
    parser.add_argument("--report-file", action="append", default=[])
    parser.add_argument(
        "--use-ollama",
        action="store_true",
        help="Explicitly run live Ollama/GPU semantic review.",
    )
    parser.add_argument("--ollama-model", default=None)
    parser.add_argument("--ollama-max-new-tokens", type=int, default=1600)
    parser.add_argument("--output", default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--markdown-output", default=DEFAULT_OUTPUT_MD)
    parser.add_argument("--proposal-output", default=DEFAULT_PROPOSALS_JSON)
    args = parser.parse_args()
    review, proposals = run_review(args)
    write_outputs(review, proposals, args)
    print(
        json.dumps(
            {
                "passed": review["passed"],
                "output": args.output,
                "markdown": args.markdown_output,
                "proposals": args.proposal_output,
                "provider_execution_performed": review["provider_execution_performed"],
                "proposal_count": proposals["proposal_count"],
            },
            indent=2,
        )
    )
    return 0 if review["passed"] else 2
