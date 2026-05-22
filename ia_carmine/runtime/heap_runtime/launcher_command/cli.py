"""Compatibility notice for the retired external-parameter launcher command."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    report = {
        "schema_version": 1,
        "kind": "heap_runtime_launcher_command_retired",
        "repo_root": repo_root.as_posix(),
        "passed": False,
        "execution_performed": False,
        "external_parameter_loading_performed": False,
        "replacement": "python -m ia_carmine.cli run --dry-run",
        "errors": [
            "heap_runtime_launcher_command was retired; use ia_carmine run explicit CLI parameters"
        ],
        "warnings": [],
    }
    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
