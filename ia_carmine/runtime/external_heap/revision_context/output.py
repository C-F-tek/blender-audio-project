"""Markdown and documents-copy outputs for revision context."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Any

def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Revision Context",
        "",
        f"- Protocol: `{report['protocol']}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Operational revision context: `{report.get('operational_revision_context')}`",
        f"- Proposal graph operational: `{report.get('proposal_graph_operational')}`",
        f"- Provider graph operational: `{report.get('provider_graph_operational')}`",
        f"- Can resume universe: `{report.get('can_resume_universe')}`",
        f"- Source run was fallback: `{report.get('source_run_was_fallback')}`",
        f"- Pointer contract role: `{report.get('pointer_contract_role')}`",
        f"- Provider execution semantics: `{report.get('provider_execution_semantics')}`",
        f"- Causal chain passed: `{report.get('causal_chain_passed')}`",
        f"- Product acceptance passed: `{report.get('product_acceptance_passed')}`",
        f"- Requires concrete rewrite: `{report.get('requires_concrete_rewrite')}`",
        f"- Priority next action: `{report.get('priority_next_action')}`",
        f"- Candidate applicability summary: `{report.get('candidate_applicability_summary')}`",
        f"- Pointer max blocks applied: `{report.get('pointer_max_blocks_applied')}`",
        f"- Pointer block count: `{report.get('pointer_block_count')}`",
        f"- Source block count: `{report.get('source_block_count')}`",
        f"- Resume from block: `{report.get('resume_from_block_id')}`",
        f"- Latest block: `{report.get('latest_block_id')}`",
        f"- Parallel task count: `{report.get('parallel_task_count')}`",
        f"- GPU1 tasks: `{report.get('gpu1_task_count')}`",
        f"- Provider recovery tasks: `{report.get('provider_recovery_task_count')}`",
        f"- GPU0 tasks: `{report.get('gpu0_task_count')}`",
        f"- NPU tasks: `{report.get('npu_task_count')}`",
        "",
        "## Runtime instruction",
        "",
        report["runtime_instruction"],
        "",
        "## Tasks",
        "",
    ]
    for task in report.get("tasks") or []:
        lines.extend(
            [
                f"### `{task.get('task_id')}`",
                "",
                f"- Role: `{task.get('role')}`",
                f"- Type: `{task.get('task_type')}`",
                f"- Target: `{task.get('target_block_id')}`",
                f"- Resume: `{task.get('resume_from_block_id')}`",
                f"- Candidate concrete enough: `{task.get('candidate_concrete_enough')}`",
                f"- Symbol propagation skipped: `{task.get('symbol_propagation_skipped')}`",
                f"- Candidate applicability flags: `{task.get('candidate_applicability_flags')}`",
                f"- Can add pointer information: `{task.get('can_add_pointer_information')}`",
                f"- Return to main block: `{task.get('return_to_main_block_id')}`",
                f"- Restart on rejected partial: `{task.get('restart_on_rejected_partial')}`",
                f"- First turn plan allowed: `{task.get('first_turn_plan_allowed')}`",
                f"- Instruction: {task.get('instruction')}",
                "",
            ]
        )
    return "\n".join(lines) + "\n"

def append_download_manifest(manifest_path: Path, output_paths: list[Path]) -> None:
    lines: list[str] = []
    if manifest_path.exists():
        try:
            lines = manifest_path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
        except Exception:
            lines = []
    existing = set(lines)
    additions = ["", "External heap revision context:"]
    for path in output_paths:
        line = f"- {path}"
        if line not in existing:
            additions.append(line)
    if len(additions) > 2:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text("\n".join(lines + additions).rstrip() + "\n", encoding="utf-8")

def attach_to_composer_documents(
    composer: dict[str, Any],
    json_path: Path,
    markdown_path: Path,
    explicit_documents_dir: str,
) -> dict[str, str]:
    documents_dir_value = explicit_documents_dir or str(composer.get("documents_dir") or "")
    if not documents_dir_value:
        return {}
    documents_dir = Path(documents_dir_value).expanduser().resolve()
    documents_dir.mkdir(parents=True, exist_ok=True)
    target_json = documents_dir / json_path.name
    target_md = documents_dir / markdown_path.name
    shutil.copyfile(json_path, target_json)
    shutil.copyfile(markdown_path, target_md)
    manifest_value = str(composer.get("download_manifest_txt") or "")
    if manifest_value:
        append_download_manifest(
            Path(manifest_value).expanduser().resolve(), [target_md, target_json]
        )
    return {
        "documents_dir": str(documents_dir),
        "documents_json": str(target_json),
        "documents_markdown": str(target_md),
        "download_manifest_txt": manifest_value,
    }
