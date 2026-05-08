#!/usr/bin/env python3
"""Smoke-test validator support for IA-Carmine Markdown split directories.

This test is report-only. It creates a temporary miniature repository tree and
verifies that the Markdown validators/inventory treat ``name.md`` directories as
containers, not as readable Markdown files.
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from Tools.validation import build_markdown_inventory
from Tools.validation import check_file_line_limits
from Tools.validation import check_markdown_line_limits


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def build_fixture(root: Path) -> None:
    write(root / "AGENTS.md", "# AGENTS\n\nFixture policy entrypoint.")
    write(root / "README.md", "# Fixture\n\n- [Docs](docs/README.md)")
    write(root / "WORKFLOW.md", "# Workflow\n\nFixture workflow.")
    write(
        root / "docs" / "README.md",
        """
        # Docs

        - [Example split](example.md/README.md)
        - [Plain doc](plain.md)
        """,
    )
    write(root / "docs" / "plain.md", "# Plain\n\nA normal Markdown file.")
    write(
        root / "docs" / "example.md" / "README.md",
        """
        <!-- IA-CARMINE-MD-SPLIT: index -->
        # Example split index

        - [Part 1](part-001.md)
        - [Part 2](part-002.md)
        """,
    )
    write(
        root / "docs" / "example.md" / "part-001.md",
        """
        <!-- IA-CARMINE-MD-SPLIT: part -->
        # Example part 1

        Content part one.
        """,
    )
    write(
        root / "docs" / "example.md" / "part-002.md",
        """
        <!-- IA-CARMINE-MD-SPLIT: part -->
        # Example part 2

        Content part two.
        """,
    )


def require(condition: bool, errors: list[str], message: str) -> None:
    if not condition:
        errors.append(message)


def checked_file_items(root: Path) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    for path in sorted(
        check_file_line_limits.iter_candidate_files(
            root,
            check_file_line_limits.DEFAULT_INCLUDE_SUFFIXES,
            set(check_file_line_limits.DEFAULT_EXCLUDED_DIRS),
        )
    ):
        items.append(
            {
                "path": check_file_line_limits.normalize_rel(path, root),
                "kind": check_file_line_limits.classify_file(path, root),
                "split_container": check_file_line_limits.split_container_for(path, root) or "",
            }
        )
    return items


def run_smoke() -> dict[str, Any]:
    errors: list[str] = []
    with tempfile.TemporaryDirectory(prefix="ia_carmine_md_split_smoke_") as temp_dir:
        root = Path(temp_dir)
        build_fixture(root)

        md_files = check_markdown_line_limits.iter_markdown(root, ["docs"], include_evidence=False)
        md_containers = check_markdown_line_limits.collect_split_containers(root, ["docs"], include_evidence=False)
        md_roles = {check_markdown_line_limits.markdown_role(path, root) for path in md_files}
        md_paths = {check_markdown_line_limits.rel(path, root) for path in md_files}

        file_report = check_file_line_limits.build_report(
            root,
            max_lines=50,
            include_suffixes=check_file_line_limits.DEFAULT_INCLUDE_SUFFIXES,
            excluded_dirs=set(check_file_line_limits.DEFAULT_EXCLUDED_DIRS),
        )
        file_items = checked_file_items(root)
        file_kinds = {item["kind"] for item in file_items}
        inventory_report = build_markdown_inventory.build_report(root)
        inventory_split_items = [
            item for item in inventory_report["items"] if item.get("directory_form_md_suffix")
        ]
        inventory_prune_split_items = [
            item for item in inventory_split_items if item.get("prune_candidate")
        ]

        require(len(md_containers) == 1, errors, "markdown line limit did not discover exactly one split container")
        require("docs/example.md/README.md" in md_paths, errors, "split README was not read as a Markdown file")
        require("docs/example.md/part-001.md" in md_paths, errors, "split part was not read as a Markdown file")
        require("docs/example.md" not in md_paths, errors, "split container directory was treated as a Markdown file")
        require({"split_index", "split_part"}.issubset(md_roles), errors, "markdown roles did not include split_index and split_part")

        require(file_report["split_container_count"] == 1, errors, "file line limit did not report one split container")
        require("split_markdown_index" in file_kinds, errors, "file line limit did not classify split index")
        require("split_markdown_part" in file_kinds, errors, "file line limit did not classify split part")

        require(inventory_report["split_container_count"] == 1, errors, "inventory did not report one split container")
        require(inventory_report["split_markdown_file_count"] >= 3, errors, "inventory split Markdown file count is too low")
        require(not inventory_prune_split_items, errors, "split members were marked as prune candidates")

        return {
            "schema_version": 1,
            "kind": "md_split_dir_validator_smoke",
            "generated_at": datetime.now().isoformat(timespec="seconds"),
            "passed": not errors,
            "errors": errors,
            "fixture_files_seen_by_markdown_limit": sorted(md_paths),
            "markdown_limit_roles": sorted(md_roles),
            "markdown_limit_split_containers": [check_markdown_line_limits.rel(path, root) for path in md_containers],
            "file_line_limit_split_container_count": file_report["split_container_count"],
            "file_line_limit_checked_items": file_items,
            "inventory_split_container_count": inventory_report["split_container_count"],
            "inventory_split_markdown_file_count": inventory_report["split_markdown_file_count"],
            "inventory_split_items": inventory_split_items,
            "provider_execution_performed": False,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "persistent_memory_write_performed": False,
        }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Markdown split directory validator smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Error count: `{len(report['errors'])}`",
        f"- Markdown split containers: `{len(report['markdown_limit_split_containers'])}`",
        f"- Inventory split files: `{report['inventory_split_markdown_file_count']}`",
        "",
    ]
    if report["errors"]:
        lines.extend(["## Errors", ""])
        for error in report["errors"]:
            lines.append(f"- {error}")
        lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Smoke-test Markdown split directory validator support.")
    parser.add_argument("--output", default="output/validation/md_split_dir_validator_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/md_split_dir_validator_smoke.md")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    report = run_smoke()
    output = REPO_ROOT / args.output
    markdown_output = REPO_ROOT / args.markdown_output
    output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    markdown_output.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
