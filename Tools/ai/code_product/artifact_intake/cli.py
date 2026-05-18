from __future__ import annotations

import argparse

from .analyzer import analyze
from .common import DEFAULT_MARKDOWN, DEFAULT_OUTPUT


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze run-produced CODE_PRODUCT_FULL_PATCH.md artifacts.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--code-product", required=True)
    parser.add_argument("--output", default=DEFAULT_OUTPUT)
    parser.add_argument("--markdown-output", default=DEFAULT_MARKDOWN)
    parser.add_argument("--require-all-integrated", action="store_true")
    parser.add_argument(
        "--apply-safe",
        action="store_true",
        help="Apply only fully forward-applicable safe sections, then re-analyze.",
    )
    return parser.parse_args()


def main() -> int:
    report = analyze(parse_args())
    return 0 if report.get("passed") else 2
