"""Build deterministic patch suggestion reports from task Markdown."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.product.patch_product.patch_suggestion_bundle.operations import discover_operations
from ia_carmine.product.patch_product.patch_suggestion_bundle.product import build_manual_review_product
from ia_carmine._shared.report_io import write_text_report

PATCH_FENCE_TOKENS = ("patch_suggestion", "patch-suggestion", "patch suggestions")


def is_patch_suggestion_fence(info: str) -> bool:
    """Return true when a fenced block is a task patch suggestion payload."""
    normalized = info.strip().lower().replace("_", "-")
    return any(token.replace("_", "-") in normalized for token in PATCH_FENCE_TOKENS)


def extract_patch_suggestion_blocks(markdown: str) -> list[dict[str, Any]]:
    """Extract JSON payloads from patch suggestion fenced code blocks."""
    blocks: list[dict[str, Any]] = []
    collecting = False
    buffer: list[str] = []
    fence_line = 0
    for line_number, line in enumerate(markdown.splitlines(), start=1):
        stripped = line.strip()
        if stripped.startswith("```"):
            if collecting:
                text = "\n".join(buffer).strip()
                try:
                    payload = json.loads(text)
                    if isinstance(payload, dict):
                        payload.setdefault("_task_fence_line", fence_line)
                        blocks.append(payload)
                    elif isinstance(payload, list):
                        blocks.append({"_task_fence_line": fence_line, "suggestions": payload})
                except json.JSONDecodeError as exc:
                    blocks.append(
                        {
                            "_task_fence_line": fence_line,
                            "_task_fence_error": f"JSONDecodeError: {exc}",
                            "suggestions": [],
                        }
                    )
                collecting = False
                buffer = []
                fence_line = 0
                continue
            info = stripped[3:].strip()
            if is_patch_suggestion_fence(info):
                collecting = True
                buffer = []
                fence_line = line_number
                continue
        elif collecting:
            buffer.append(line)
    if collecting:
        blocks.append(
            {
                "_task_fence_line": fence_line,
                "_task_fence_error": "unterminated patch suggestion fence",
                "suggestions": [],
            }
        )
    return blocks


def suggestion_items_from_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Collect suggestion dictionaries from parsed task blocks."""
    suggestions: list[dict[str, Any]] = []
    for block in blocks:
        raw_items = block.get("suggestions")
        if isinstance(raw_items, list):
            suggestions.extend(item for item in raw_items if isinstance(item, dict))
        elif any(key in block for key in ("operation", "target_file", "path", "target")):
            suggestions.append(
                {key: value for key, value in block.items() if not key.startswith("_")}
            )
    return suggestions


def build_task_patch_suggestion_report(
    repo_root: Path,
    task_file: Path,
    stamp: str,
    *,
    allow_empty: bool = False,
    empty_reason: str = "",
) -> dict[str, Any]:
    """Read a task Markdown file and return a patch suggestion report."""
    errors: list[str] = []
    warnings: list[str] = []
    if not task_file.exists():
        errors.append(f"task file missing: {task_file}")
        markdown = ""
    else:
        markdown = task_file.read_text(encoding="utf-8-sig")
    blocks = extract_patch_suggestion_blocks(markdown)
    suggestions = suggestion_items_from_blocks(blocks)
    for block in blocks:
        if block.get("_task_fence_error"):
            errors.append(f"line {block.get('_task_fence_line')}: {block.get('_task_fence_error')}")
    if not blocks:
        warnings.append("no patch_suggestion_json fenced block found in task Markdown")
    operations, manual_review = discover_operations({"suggestions": suggestions})
    product = build_manual_review_product(
        manual_review,
        operation_count=len(operations),
        failed_count=0,
    )
    no_task_product = not bool(suggestions)
    deferred_to_runtime_product = bool(allow_empty and no_task_product and not errors)
    if deferred_to_runtime_product:
        warnings.append(
            empty_reason
            or "task Markdown has no direct patch suggestions; runtime/generated patch-spec product is expected downstream"
        )
    return {
        "schema_version": 1,
        "kind": "task_markdown_patch_suggestions",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "Stamp": stamp,
        "task_file": task_file.relative_to(repo_root).as_posix(),
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "fence_block_count": len(blocks),
        "suggestion_count": len(suggestions),
        "operation_count": len(operations),
        "manual_review_required": bool(manual_review),
        "manual_review_product": product,
        "suggestions": suggestions,
        "allow_empty": bool(allow_empty),
        "deferred_to_runtime_product": deferred_to_runtime_product,
        "empty_reason": empty_reason,
        "passed": not errors and (bool(suggestions) or deferred_to_runtime_product),
        "errors": errors,
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compact Markdown summary."""
    lines = [
        "# Task Markdown Patch Suggestions",
        "",
        f"- Passed: {report.get('passed')}",
        f"- Stamp: `{report.get('Stamp')}`",
        f"- Task file: `{report.get('task_file')}`",
        f"- Fence blocks: {report.get('fence_block_count')}",
        f"- Suggestions: {report.get('suggestion_count')}",
        f"- Deterministic operations: {report.get('operation_count')}",
        f"- Deferred to runtime product: {report.get('deferred_to_runtime_product')}",
        f"- Patch application performed: {report.get('patch_application_performed')}",
        "",
        "## Suggestions",
        "",
    ]
    for item in report.get("suggestions") or []:
        lines.append(
            f"- `{item.get('id') or item.get('proposal_id') or ''}` -> `{item.get('target_file') or item.get('path') or ''}`"
        )
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    return "\n".join(lines) + "\n"


def write_markdown(report: dict[str, Any], output: Path) -> str:
    """Write the Markdown summary."""
    return write_text_report(render_markdown(report), output)
