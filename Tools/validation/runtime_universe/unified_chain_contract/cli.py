"""CLI for unified chain contract validation."""

from __future__ import annotations

import argparse

from .runner import run_contract

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--stamp", required=True)
    parser.add_argument("--mode-name", required=True)
    parser.add_argument("--manifest", default="")
    parser.add_argument("--official-report", default="")
    parser.add_argument("--gpu0-report", default="")
    parser.add_argument("--apply-report", default="")
    parser.add_argument("--product-separation-report", default="")
    parser.add_argument("--review-pr-report", default="")
    parser.add_argument("--observer-dir", default="")
    parser.add_argument("--ai-public-events", default="")
    parser.add_argument("--tool-capability-manifest", default="")
    parser.add_argument("--heap-peer-runtime", default="")
    parser.add_argument("--shared-memory-evidence", default="")
    parser.add_argument("--closure-audit-report", default="")
    parser.add_argument("--require-ai-exchange", action="store_true")
    parser.add_argument("--require-provider-tool-evidence", action="store_true")
    parser.add_argument("--require-heap-peer-runtime", action="store_true")
    parser.add_argument("--require-shared-memory-evidence", action="store_true")
    parser.add_argument("--require-heap-closure-audit", action="store_true")
    parser.add_argument("--require-concrete-patch-specs", action="store_true")
    parser.add_argument("--require-review-pr-product", action="store_true")
    parser.add_argument("--output", default="output/validation/unified_chain_contract.json")
    parser.add_argument("--markdown-output", default="")
    return parser.parse_args()


def main() -> int:
    return run_contract(parse_args())
