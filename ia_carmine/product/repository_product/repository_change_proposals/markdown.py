from __future__ import annotations

from .common import *  # noqa: F403

def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Repository Change Proposals", ""]
    lines.append(f"- Generated at: `{report['generated_at']}`")
    lines.append(f"- Profile: `{report['profile']}`")
    lines.append(f"- Apply mode: `{report['apply_mode']}`")
    lines.append(f"- Proposal count: `{len(report['proposals'])}`")
    if report.get("runtime_report_paths"):
        lines.append(f"- Runtime reports read: `{len(report['runtime_report_paths'])}`")
    lines.append("")
    for item in report["proposals"]:
        lines.append(f"## {item['id']} — {item['title']}")
        lines.append("")
        lines.append(f"- Priority: `{item['priority']}`")
        lines.append(f"- Area: `{item['area']}`")
        lines.append(f"- Change type: `{item['change_type']}`")
        lines.append(f"- Apply mode: `{item['apply_mode']}`")
        lines.append(f"- Rationale: {item['rationale']}")
        lines.append("")
        if item.get("evidence_summary"):
            lines.append("### Evidence summary")
            lines.append("")
            lines.append("```json")
            lines.append(json.dumps(item["evidence_summary"], indent=2, ensure_ascii=False))
            lines.append("```")
            lines.append("")
        lines.append("### Target files")
        for path in item["target_files"]:
            lines.append(f"- `{path}`")
        lines.append("")
        lines.append("### Patch sketch")
        for step in item["patch_sketch"]:
            lines.append(f"- {step}")
        lines.append("")
        if item.get("concrete_operations"):
            lines.append("### Concrete operations")
            for op in item["concrete_operations"]:
                lines.append(f"- `{op.get('operation')}` `{op.get('path')}`")
            lines.append("")
        if item.get("suggestion_outputs"):
            lines.append("### Suggestion outputs")
            for output in item["suggestion_outputs"]:
                lines.append(
                    f"- `{output.get('artifact_kind')}` `{output.get('path')}` "
                    f"({output.get('operation')}, {output.get('write_policy')})"
                )
            lines.append("")
        lines.append("### Validation")
        for command in item["validation_commands"]:
            lines.append(f"- `{command}`")
        lines.append("")
        lines.append("### Stop conditions")
        for condition in item["stop_conditions"]:
            lines.append(f"- {condition}")
        lines.append("")
    lines.append("## Guardrail")
    lines.append("")
    lines.append("These are proposals only. They must not be auto-applied without explicit review.")
    return "\n".join(lines) + "\n"
