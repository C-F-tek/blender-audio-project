from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core import write_root_tool_guide


def main() -> int:
    parser = argparse.ArgumentParser(description="Write or preview the root Markdown split tool guide.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    writes: list[tuple[str, str]] = []

    def write(path: Path, text: str, apply: bool) -> int:
        if apply:
            path.write_text(text, encoding="utf-8")
        writes.append((path.as_posix(), text))
        return len(text.splitlines())

    def rel(path: Path, root: Path) -> str:
        try:
            return path.resolve().relative_to(root).as_posix()
        except ValueError:
            return path.as_posix()

    result = write_root_tool_guide(repo_root, args.apply, write, rel)
    report: dict[str, Any] = {
        "schema_version": 1,
        "kind": "markdown_split_tool_guide",
        "passed": True,
        "repo_root": str(repo_root),
        "apply": bool(args.apply),
        "result": result,
        "preview": writes[0][1] if writes else "",
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": bool(args.apply),
    }
    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
