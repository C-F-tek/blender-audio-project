"""Markdown renderer for selective execution plans."""

from __future__ import annotations

from typing import Any

def render_markdown(plan: dict[str, Any]) -> str:
    """Render a human-readable Markdown report."""
    provider = plan.get("provider_evidence_summary", {})
    dry_run = plan.get("dry_run_summary", {})
    lines = [
        "# Selective Execution Plan",
        "",
        f"- Generated at: `{plan.get('generated_at')}`",
        f"- Kind: `{plan.get('kind')}`",
        f"- Passed: `{plan.get('passed')}`",
        f"- Apply mode: `{plan.get('apply_mode')}`",
        f"- Provider execution performed: `{plan.get('provider_execution_performed')}`",
        f"- Patch application performed: `{plan.get('patch_application_performed')}`",
        "",
        "## Evidence Summary",
        "",
        f"- Context evidence passed: `{plan['inputs']['context_pack_evidence'].get('passed')}`",
        f"- Dry-run evidence passed: `{dry_run.get('passed')}`",
        f"- Dry-run case count: `{dry_run.get('case_count')}`",
        f"- Dry-run planned-only: `{dry_run.get('all_steps_planned_only')}`",
        f"- Provider execution seen: `{provider.get('provider_execution_seen')}`",
        f"- Ollama/GPU primary advisory: `{provider.get('ollama_gpu_primary_advisory')}`",
        f"- NPU decode smoke passed: `{provider.get('npu_decode_smoke_passed')}`",
        "",
        "## Recommended Validators",
        "",
    ]
    for item in plan.get("recommended_validators", []):
        lines.append(f"- `{item.get('name')}`: {item.get('reason')}")
        lines.append(f"  - Command: `{item.get('command')}`")
    lines.extend(["", "## Recommended Patch Specs", ""])
    for item in plan.get("recommended_patch_specs", []):
        lines.append(
            f"- `{item.get('id')}`: {item.get('title')} (blocked: `{item.get('blocked')}`)"
        )
        lines.append(f"  - Rationale: {item.get('rationale')}")
        lines.append(f"  - Targets: `{', '.join(item.get('target_files', []))}`")
    lines.extend(["", "## Blocked Actions", ""])
    if plan.get("blocked_actions"):
        for item in plan["blocked_actions"]:
            lines.append(f"- {item}")
    else:
        lines.append("None.")
    lines.extend(["", "## Local-only Actions for Carmine", ""])
    for item in plan.get("local_only_actions_for_carmine", []):
        lines.append(f"- {item}")
    lines.extend(["", "## GitHub-only Actions for AI", ""])
    for item in plan.get("github_only_actions_for_ai", []):
        lines.append(f"- {item}")
    lines.extend(["", "## Next Command Sets", ""])
    for name, commands in plan.get("next_command_set", {}).items():
        lines.append(f"### {name}")
        lines.append("")
        lines.append("```powershell")
        lines.extend(commands)
        lines.append("```")
        lines.append("")
    lines.extend(["## Risks", ""])
    if plan.get("risks"):
        for item in plan["risks"]:
            lines.append(f"- {item}")
    else:
        lines.append("None.")
    lines.extend(["", "## Warnings", ""])
    if plan.get("warnings"):
        for item in plan["warnings"]:
            lines.append(f"- {item}")
    else:
        lines.append("None.")
    return "\n".join(lines) + "\n"
