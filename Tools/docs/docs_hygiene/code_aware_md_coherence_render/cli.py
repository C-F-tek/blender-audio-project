from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core import render_markdown


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a code-aware Markdown coherence report.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--input", required=True, help="JSON report produced by build_code_aware_md_coherence.")
    parser.add_argument("--output", default="")
    parser.add_argument("--max-rows", type=int, default=120)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    input_path = Path(args.input)
    if not input_path.is_absolute():
        input_path = repo_root / input_path
    try:
        loaded = json.loads(input_path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"[ERROR] cannot read report: {exc}")
        return 2
    if not isinstance(loaded, dict):
        print("[ERROR] input report must be a JSON object")
        return 2

    markdown = render_markdown(loaded, args.max_rows)
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
