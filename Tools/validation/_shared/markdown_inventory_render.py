from __future__ import annotations

from typing import Any


def render_table(lines: list[str], title: str, rows: list[dict[str, Any]]) -> None:
    lines.extend([f"## {title}", ""])
    if not rows:
        lines.extend([f"No {title.lower()} candidates.", ""])
        return
    lines.extend(["| Path | Category | Lifecycle | Lines | Heading |", "|---|---|---|---:|---|"])
    for item in rows:
        heading = (item.get("heading") or "").replace("|", "\\|")
        lines.append(
            f"| `{item['path']}` | `{item['category']}` | `{item['lifecycle']}` | {item['lines']} | {heading} |"
        )
    lines.append("")


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Markdown Documentation Inventory",
        "",
        f"- Kind: `{report['kind']}`",
        f"- Markdown files: `{report['markdown_count']}`",
        f"- Split containers: `{report['split_container_count']}`",
        f"- Split Markdown files: `{report['split_markdown_file_count']}`",
        f"- Missing index review count: `{report['missing_index_count']}`",
        f"- Prune candidate count: `{report['prune_candidate_count']}`",
        "- Provider execution performed: `False`",
        "- Patch application performed: `False`",
        "",
        "## Category counts",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    for category, count in sorted(report["category_counts"].items()):
        lines.append(f"| `{category}` | {count} |")
    lines.extend(["", "## Markdown role counts", "", "| Role | Count |", "|---|---:|"])
    for role, count in sorted(report["markdown_role_counts"].items()):
        lines.append(f"| `{role}` | {count} |")
    lines.append("")
    render_table(lines, "Missing index review", report["missing_index"])
    render_table(lines, "Prune candidates", report["prune_candidates"])
    lines.extend(
        [
            "## Full Markdown map",
            "",
            "| Path | Role | Category | Lifecycle | Indexed | Lines |",
            "|---|---|---|---|---|---:|",
        ]
    )
    for item in report["items"]:
        lines.append(
            f"| `{item['path']}` | `{item['markdown_role']}` | `{item['category']}` | "
            f"`{item['lifecycle']}` | `{item['indexed']}` | {item['lines']} |"
        )
    lines.append("")
    return "\n".join(lines)
