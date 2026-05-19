"""Report builders for root tool package promotion."""

from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime
from pathlib import Path

from .references import Reference, ReferenceRewrite, relative


def render_markdown(report: dict[str, object]) -> str:
    if report.get("kind") == "root_tool_package_promotion_batch":
        lines = [
            "# Root Tool Package Promotion Batch",
            "",
            f"- Generated at: `{report['generated_at']}`",
            f"- Apply: `{report['apply']}`",
            f"- Source writes: `{report['source_writes_performed']}`",
            f"- Area: `{report['area']}`",
            f"- Summary: `{json.dumps(report['summary'], ensure_ascii=False)}`",
            "",
            "## Selected",
            "",
        ]
        selected = report["selected"]
        assert isinstance(selected, list)
        lines.extend(f"- `{item}`" for item in selected)
        skipped = report["skipped"]
        assert isinstance(skipped, list)
        if skipped:
            lines.extend(["", "## Skipped", ""])
            for item in skipped[:100]:
                assert isinstance(item, dict)
                details = " ".join(
                    f"{key}=`{value}`" for key, value in item.items() if key != "tool"
                )
                lines.append(f"- `{item['tool']}` {details}".rstrip())
        return "\n".join(lines) + "\n"

    lines = [
        "# Root Tool Package Promotion",
        "",
        f"- Generated at: `{report['generated_at']}`",
        f"- Apply: `{report['apply']}`",
        f"- Source writes: `{report['source_writes_performed']}`",
        f"- Source: `{report['source']}`",
        f"- Package: `{report['package_dir']}`",
        "",
        "## References",
        "",
        "| Path | Line | Text |",
        "|---|---:|---|",
    ]
    refs = report["references"]
    assert isinstance(refs, list)
    for item in refs[:200]:
        assert isinstance(item, dict)
        text = str(item["text"]).replace("|", "\\|")
        lines.append(f"| `{item['path']}` | {item['line']} | `{text}` |")
    if len(refs) > 200:
        lines.append(f"\n_Truncated {len(refs) - 200} more references; see JSON._")
    return "\n".join(lines) + "\n"


def build_report(
    *,
    root: Path,
    area: str,
    tool: str,
    source: Path,
    package_dir: Path,
    apply: bool,
    refs: list[Reference],
    actions: list[str],
    reference_rewrites: list[ReferenceRewrite],
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "root_tool_package_promotion",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "area": area,
        "tool": tool,
        "source": relative(root, source),
        "package_dir": relative(root, package_dir),
        "cli": relative(root, package_dir / "cli.py"),
        "init": relative(root, package_dir / "__init__.py"),
        "apply": apply,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": apply,
        "actions": actions,
        "references": [asdict(item) for item in refs],
        "reference_rewrites": [asdict(item) for item in reference_rewrites],
    }


def build_batch_report(
    *,
    root: Path,
    area: str,
    apply: bool,
    selected: list[str],
    skipped: list[dict[str, object]],
    promotions: list[dict[str, object]],
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "kind": "root_tool_package_promotion_batch",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": root.as_posix(),
        "area": area,
        "apply": apply,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": apply and bool(promotions),
        "summary": {
            "selected_count": len(selected),
            "promoted_count": len(promotions),
            "skipped_count": len(skipped),
        },
        "selected": selected,
        "skipped": skipped,
        "promotions": promotions,
    }
