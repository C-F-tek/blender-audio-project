"""Document package writer for heap final proposal composition."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from Tools.ai.heap_final_proposals.artifacts import proposal_text_for_review

try:
    from Tools.ai._shared.heap_proposal_gate import record_operator_decision
except ImportError:  # pragma: no cover
    from Tools.ai._shared.heap_proposal_gate import record_operator_decision  # type: ignore


def write_documents_package(
    *,
    stamp: str,
    doc_dir: Path,
    markdown: str,
    json_data: dict[str, Any],
    proposals: list[dict[str, Any]],
) -> dict[str, Any]:
    doc_dir.mkdir(parents=True, exist_ok=True)
    written: list[str] = []
    proposal_txt_outputs: list[str] = []
    proposal_chunk_outputs: list[str] = []
    md_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.md"
    txt_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.txt"
    json_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}.json"
    manifest_path = doc_dir / f"aicarmine_heap_final_proposals_{stamp}_DOWNLOADS.txt"
    md_path.write_text(markdown, encoding="utf-8")
    txt_path.write_text(markdown, encoding="utf-8")
    json_path.write_text(
        json.dumps(json_data, indent=2, ensure_ascii=False, default=str) + "\n",
        encoding="utf-8",
    )
    written.extend([str(md_path), str(txt_path), str(json_path)])
    operator_decision = json_data.get("operator_decision")
    if isinstance(operator_decision, dict):
        decision_path = record_operator_decision(
            doc_dir,
            operator_decision,
            list(operator_decision.get("targets_considered") or []),
        )
        written.append(str(decision_path))
    chunk_dir = doc_dir / "proposal_chunks"
    chunk_txt_dir = doc_dir / "proposal_chunks_txt"
    chunk_dir.mkdir(parents=True, exist_ok=True)
    chunk_txt_dir.mkdir(parents=True, exist_ok=True)
    for proposal in proposals:
        _copy_proposal_chunks(proposal, chunk_dir, written, proposal_chunk_outputs)
        txt_target = chunk_txt_dir / f"{Path(str(proposal.get('name') or 'proposal')).stem}.txt"
        txt_target.write_text(proposal_text_for_review(proposal, None), encoding="utf-8")
        written.append(str(txt_target))
        proposal_txt_outputs.append(str(txt_target))
    manifest_lines = [
        "IA-Carmine heap final proposal download package",
        "",
        f"Primary TXT: {txt_path}",
        f"Primary Markdown: {md_path}",
        f"Primary JSON: {json_path}",
        "",
        "Proposal TXT chunks:",
        *[f"- {path}" for path in proposal_txt_outputs],
        "",
        "All outputs:",
        *[f"- {path}" for path in written],
    ]
    manifest_path.write_text("\n".join(manifest_lines) + "\n", encoding="utf-8")
    written.append(str(manifest_path))
    return {
        "documents_dir": str(doc_dir),
        "documents_outputs": written,
        "primary_markdown": str(md_path),
        "primary_txt": str(txt_path),
        "primary_json": str(json_path),
        "download_manifest_txt": str(manifest_path),
        "proposal_chunk_outputs": proposal_chunk_outputs,
        "proposal_txt_outputs": proposal_txt_outputs,
    }


def _copy_proposal_chunks(
    proposal: dict[str, Any],
    chunk_dir: Path,
    written: list[str],
    proposal_chunk_outputs: list[str],
) -> None:
    for key in ("markdown_path", "json_path"):
        path = proposal.get(key)
        if isinstance(path, Path) and path.exists():
            target = chunk_dir / path.name
            shutil.copyfile(path, target)
            written.append(str(target))
            proposal_chunk_outputs.append(str(target))
