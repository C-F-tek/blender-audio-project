#!/usr/bin/env python3
"""Compatibility command for the GPU0 peer worker.

GPU0 is now an Ollama/Vulkan peer lane. This command preserves the historical
entrypoint name while delegating to the canonical Ollama GPU0 peer report.
"""

from __future__ import annotations

import argparse
import sys

from ia_carmine.providers.provider_mesh.ollama_gpu0_peer_report.cli import main as ollama_gpu0_main


def main() -> int:
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--iterations", default="")
    parser.add_argument("--min-seconds", default="")
    parser.add_argument("--role", default="")
    parser.add_argument("--device", default="")
    parser.add_argument("--production-support", action="store_true")
    parser.add_argument("--allow-non-observable", action="store_true")
    known, remaining = parser.parse_known_args()
    _ = known
    sys.argv = [sys.argv[0], *remaining]
    return ollama_gpu0_main()


if __name__ == "__main__":
    raise SystemExit(main())
