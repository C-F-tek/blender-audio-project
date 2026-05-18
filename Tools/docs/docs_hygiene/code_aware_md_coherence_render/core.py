from __future__ import annotations

import json
from typing import Any


def render_markdown(report: dict[str, Any], max_rows: int = 120) -> str:
    summary = report["summary"]
    lines = [
        "# MD/code coherence report",
        "",
        "## Summary",
        "",
        f"- Markdown files scanned: `{report['inventory']['markdown_file_count']}`",
        f"- Python scripts scanned: `{report['inventory']['python_script_count']}`",
        f"- PowerShell scripts scanned: `{report['inventory']['powershell_script_count']}`",
        f"- Finding count: `{summary['finding_count']}`",
        f"- By severity: `{json.dumps(summary['by_severity'], ensure_ascii=False)}`",
        f"- By kind: `{json.dumps(summary['by_kind'], ensure_ascii=False)}`",
        "",
        "## Top findings",
        "",
        "| Severity | Kind | Document | Target | Classification |",
        "|---|---|---|---|---|",
    ]
    severity_rank = {"high": 0, "medium": 1, "low": 2}
    findings = sorted(
        report["findings"],
        key=lambda f: (severity_rank.get(f["severity"], 9), f["kind"], f["path"], f["target"]),
    )
    for item in findings[:max_rows]:
        lines.append(
            f"| {item['severity']} | {item['kind']} | `{item['path']}` | `{item['target']}` | {item['classification']} |"
        )
    if len(findings) > max_rows:
        lines.extend(["", f"_Truncated: {len(findings) - max_rows} more findings in JSON report._"])
    lines.extend(
        [
            "",
            "## Policy",
            "",
            "Use this report to rewrite active Markdown from current code, not from historical evidence.",
            "Raw reports under `output/**` are local artifacts and must not be committed.",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"
