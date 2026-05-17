#!/usr/bin/env python3
"""Smoke test source anchor priority for implementation/code-product prompts."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

CORE_RUNTIME_GUARD = True

try:
    from tools.ai.heap_source_anchors import real_source_file_candidates
    from tools.validation.report_utils import write_json_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from tools.ai.heap_source_anchors import real_source_file_candidates  # type: ignore
    from tools.validation.report_utils import write_json_report  # type: ignore


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_report(repo_root: Path, work_dir: Path) -> dict[str, Any]:
    broker_json = work_dir / "broker_docs_noise.json"
    write_json(
        broker_json,
        {
            "target_file": "docs/AI_SESSION_NOTES/operator-product-launcher-2026-05-15.md",
            "evidence": [
                {"source_file": "docs/LOCAL_AI_TASKS/ai-orientation-map-2026-05-09.md"}
            ],
        },
    )
    request = (
        "verifica perche il GUI/operator launcher non produce CODE_PRODUCT_FULL_PATCH "
        "e proponi patch concrete di codice"
    )
    candidates = real_source_file_candidates(
        repo_root=repo_root,
        request_texts=[request],
        broker_output_refs=[broker_json.relative_to(repo_root).as_posix()],
        limit=12,
    )
    top_three = candidates[:3]
    errors: list[str] = []
    if not candidates:
        errors.append("no source candidates returned")
    if not any(Path(item).suffix.lower() == ".py" for item in top_three):
        errors.append("implementation request did not prioritize python source targets")
    if any(item.startswith("docs/") for item in top_three):
        errors.append("documentation noise entered top implementation targets")
    if not any("launcher" in item.lower() or "code_product" in item.lower() for item in candidates[:8]):
        errors.append("launcher/code-product source target not visible near top candidates")
    return {
        "schema_version": 1,
        "kind": "heap_source_anchor_priority_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "passed": not errors,
        "errors": errors,
        "request": request,
        "broker_noise": broker_json.relative_to(repo_root).as_posix(),
        "candidates": candidates,
        "source_writes_performed": False,
        "patch_application_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/heap_source_anchor_priority_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    work_dir = repo_root / "output" / "validation" / "heap_source_anchor_priority_smoke"
    report = build_report(repo_root, work_dir)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    print(write_json_report(report, output), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
