from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .core import collect_md_refs, is_active_md, is_excluded_rel


def main() -> int:
    parser = argparse.ArgumentParser(description="Inventory path references in active Markdown files.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="")
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    documents: list[dict[str, Any]] = []
    for path in sorted(repo_root.rglob("*.md")):
        try:
            rel = path.relative_to(repo_root).as_posix()
        except ValueError:
            continue
        if is_excluded_rel(rel) or not is_active_md(rel):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig", errors="replace")
        except OSError:
            continue
        refs = sorted(collect_md_refs(text))
        if refs:
            documents.append({"path": rel, "reference_count": len(refs), "references": refs})

    report = {
        "schema_version": 1,
        "kind": "code_aware_md_refs",
        "passed": True,
        "repo_root": str(repo_root),
        "document_count": len(documents),
        "documents": documents,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
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
