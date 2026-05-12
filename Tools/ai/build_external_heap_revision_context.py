#!/usr/bin/env python3
"""Build external heap revision context from block pointers.

This adapter is outside the gate. It converts a block-pointer manifest plus the
composer/causality reports into a next-run context that lets:

- GPU1 move forward or backward across proposal blocks;
- GPU1 propagate newly discovered imports/variables/contracts into older blocks;
- GPU0 and NPU independently re-check older pointers in parallel;
- the next run resume from the correct block instead of repeating generic output.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any


REVISION_TASK_PREVIEW_CHARS = 1600
REJECTION_MARKER_PATTERNS = (
    ("placeholder/stub", re.compile(r"placeholder/stub", re.IGNORECASE)),
    ("similarity=1.000", re.compile(r"similarity\s*=\s*1\.000", re.IGNORECASE)),
    ("TODO", re.compile(r"(^|\n)\s*(#|//)?\s*TODO\s*[:(]", re.IGNORECASE)),
    ("pass", re.compile(r"(^|[^A-Za-z0-9_])pass([^A-Za-z0-9_]|$)", re.IGNORECASE)),
    ("path/to/artifact", re.compile(r"path/to/artifact", re.IGNORECASE)),
)
CANDIDATE_APPLICABILITY_PATTERNS = (
    ("generic_patch_sketch", re.compile(r"\bCODE_OR_PATCH_SKETCH\b", re.IGNORECASE)),
    ("generic_missing_functionality", re.compile(r"implementa(?:re|zione)\s+(?:le\s+)?funzionalit", re.IGNORECASE)),
    ("synthetic_stub_function", re.compile(r"def\s+[A-Za-z_][A-Za-z0-9_]*\s*\([^)]*\)\s*:\s*(?:\n\s*#\s*Implementazione|\n\s*context_pack\s*=\s*\{)", re.IGNORECASE)),
    ("comment_only_implementation", re.compile(r"^\s*#\s*Implementazione\b", re.IGNORECASE | re.MULTILINE)),
    ("unverified_unit_test_path", re.compile(r"\bpytest\s+(?:\.\\)?Tests[/\\]unit[/\\]test_[A-Za-z0-9_./\\-]+\.py\b", re.IGNORECASE)),
    ("run_script_as_validation_only", re.compile(r"\bpython\s+Tools[/\\]ai[/\\][A-Za-z0-9_./\\-]+\.py\b", re.IGNORECASE)),
)


def read_json(path_value: str) -> dict[str, Any]:
    if not path_value:
        return {}
    try:
        data = json.loads(Path(path_value).read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def normalize_bool(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def compact_text(value: Any, limit: int) -> str:
    text = str(value or "")
    if limit > 0 and len(text) > limit:
        return text[:limit] + "\n...[truncated]"
    return text


def candidate_applicability_flags(text: str) -> list[str]:
    flags: list[str] = []
    for flag, pattern in CANDIDATE_APPLICABILITY_PATTERNS:
        if pattern.search(text) and flag not in flags:
            flags.append(flag)
    return flags


def candidate_concrete_enough(text: str) -> bool:
    return not candidate_applicability_flags(text)


def proposal_blocks(pointer: dict[str, Any]) -> list[dict[str, Any]]:
    blocks = [
        block for block in as_list(pointer.get("blocks"))
        if isinstance(block, dict) and block.get("block_type") == "proposal_chunk"
    ]
    return sorted(blocks, key=lambda block: int(block.get("step_index") or 0))


def peer_blocks(pointer: dict[str, Any], role: str) -> list[dict[str, Any]]:
    blocks = [
        block for block in as_list(pointer.get("blocks"))
        if isinstance(block, dict) and block.get("role") == role
    ]
    return sorted(blocks, key=lambda block: int(block.get("step_index") or 0))


def latest_block(blocks: list[dict[str, Any]]) -> dict[str, Any]:
    return blocks[-1] if blocks else {}


def clean_import_line(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("import ") or stripped.startswith("from "):
        return stripped
    return ""


def extract_symbols(text: str) -> dict[str, list[str]]:
    imports: set[str] = set()
    defs: set[str] = set()
    classes: set[str] = set()
    assignments: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        import_line = clean_import_line(line)
        if import_line:
            imports.add(import_line)
        def_match = re.match(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", line)
        if def_match:
            defs.add(def_match.group(1))
        class_match = re.match(r"^\s*class\s+([A-Za-z_][A-Za-z0-9_]*)\s*[:(]", line)
        if class_match:
            classes.add(class_match.group(1))
        assignment_match = re.match(r"^\s*([A-Z][A-Z0-9_]{2,}|[a-z_][a-z0-9_]{3,})\s*=", line)
        if assignment_match and not stripped.startswith(("return ", "if ", "for ", "while ")):
            assignments.add(assignment_match.group(1))
    return {
        "imports": sorted(imports),
        "defs": sorted(defs),
        "classes": sorted(classes),
        "assignments": sorted(assignments)[:80],
    }


def rejection_reasons(composer: dict[str, Any], block: dict[str, Any]) -> list[str]:
    source_name = Path(str(block.get("source_path") or "")).name
    reasons: list[str] = []
    for item in as_list(composer.get("rejected_proposals")):
        if not isinstance(item, dict):
            continue
        if item.get("name") == source_name:
            reason = str(item.get("reason") or "").strip()
            if reason:
                reasons.append(reason)
    preview = str(block.get("preview") or "")
    diagnostic_preview = str(block.get("diagnostic_preview") or "")
    marker_text = "\n".join(part for part in (preview, diagnostic_preview) if part)
    for marker, pattern in REJECTION_MARKER_PATTERNS:
        if pattern.search(marker_text) and marker not in reasons:
            reasons.append(marker)
    for flag in candidate_applicability_flags(str(block.get("candidate_response_preview") or preview)):
        reason = f"candidate_applicability.{flag}"
        if reason not in reasons:
            reasons.append(reason)
    return reasons


def task_block_context(block: dict[str, Any], preview_limit: int = REVISION_TASK_PREVIEW_CHARS) -> dict[str, Any]:
    source_preview = compact_text(block.get("preview"), preview_limit)
    candidate_preview = compact_text(block.get("candidate_response_preview"), preview_limit)
    diagnostic_preview = compact_text(block.get("diagnostic_preview"), preview_limit)
    candidate_flags = candidate_applicability_flags(str(block.get("candidate_response_preview") or block.get("preview") or ""))
    return {
        "source_path": str(block.get("source_path") or ""),
        "markdown_path": str(block.get("markdown_path") or ""),
        "previous_block_id": str(block.get("previous_block_id") or ""),
        "next_block_id": str(block.get("next_block_id") or ""),
        "refines_block_id": str(block.get("refines_block_id") or ""),
        "block_quality_passed": block.get("quality_passed"),
        "block_accepted": block.get("accepted"),
        "preview_source": str(block.get("preview_source") or ""),
        "source_preview": source_preview,
        "candidate_response_preview": candidate_preview,
        "diagnostic_preview": diagnostic_preview,
        "candidate_response_available": bool(candidate_preview.strip()),
        "diagnostic_preview_available": bool(diagnostic_preview.strip()),
        "candidate_applicability_flags": candidate_flags,
        "candidate_concrete_enough": not candidate_flags,
    }


def build_gpu1_tasks(proposals: list[dict[str, Any]], composer: dict[str, Any]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    previous_symbols: dict[str, set[str]] = {"imports": set(), "defs": set(), "classes": set(), "assignments": set()}
    for block in proposals:
        block_id = str(block.get("block_id") or "")
        symbol_text = str(block.get("candidate_response_preview") or block.get("preview") or "")
        concrete_candidate = candidate_concrete_enough(symbol_text)
        symbols = extract_symbols(symbol_text) if concrete_candidate else {"imports": [], "defs": [], "classes": [], "assignments": []}
        discovered: dict[str, list[str]] = {}
        for key, values in symbols.items():
            new_values = [value for value in values if value not in previous_symbols[key]]
            if new_values:
                discovered[key] = new_values
            previous_symbols[key].update(values)
        reasons = rejection_reasons(composer, block)
        if discovered and block.get("previous_block_id"):
            tasks.append(
                {
                    "task_id": f"gpu1_propagate_symbols_{block_id}",
                    "role": "gpu1_planner",
                    "task_type": "backpropagate_symbol_contract",
                    "source_block_id": block_id,
                    "target_block_id": block.get("previous_block_id"),
                    "resume_from_block_id": block_id,
                    "discovered_symbols": discovered,
                    "symbol_propagation_source_concrete": True,
                    "instruction": "Propaga import/variabili/classi/funzioni scoperte nel candidate_response_preview ai blocchi precedenti compatibili, poi riprendi dal source_block_id senza perdere il cursore forward.",
                    **task_block_context(block),
                }
            )
        if reasons:
            tasks.append(
                {
                    "task_id": f"gpu1_rewrite_rejected_{block_id}",
                    "role": "gpu1_planner",
                    "task_type": "rewrite_rejected_block",
                    "source_block_id": block_id,
                    "target_block_id": block_id,
                    "resume_from_block_id": block.get("resume_from_block_id") or block.get("previous_block_id") or block_id,
                    "rejection_reasons": reasons,
                    "symbol_propagation_skipped": not concrete_candidate,
                    "symbol_propagation_skip_reason": "candidate_not_concrete_enough" if not concrete_candidate else "",
                    "instruction": "Riscrivi il blocco usando candidate_response_preview come input primario e diagnostic_preview solo come diagnosi. Sostituisci sketch generici con patch plan verificabile: file repo reali, funzioni/classi esistenti, diff o operazioni concrete, comandi validazione esistenti. Mantieni i pointer previous/next/refines/resume.",
                    **task_block_context(block),
                }
            )
    return tasks


def build_peer_tasks(proposals: list[dict[str, Any]], gpu0: list[dict[str, Any]], npu: list[dict[str, Any]]) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    gpu0_available = bool(gpu0)
    npu_available = bool(npu)
    for block in proposals:
        block_id = str(block.get("block_id") or "")
        if block.get("accepted") is True:
            continue
        if gpu0_available:
            tasks.append(
                {
                    "task_id": f"gpu0_parallel_recheck_{block_id}",
                    "role": "gpu0_reviewer_refiner",
                    "task_type": "parallel_recheck_old_pointer",
                    "target_block_id": block_id,
                    "can_edit_pointer": True,
                    "instruction": "Rivaluta il candidate_response_preview anche se il blocco non e' l'ultimo. Usa diagnostic_preview solo come diagnosi. Se candidate_applicability_flags non e' vuoto, proponi refines_block_id e resume_from_block_id per una riscrittura concreta.",
                    **task_block_context(block),
                }
            )
        if npu_available:
            tasks.append(
                {
                    "task_id": f"npu_parallel_audit_{block_id}",
                    "role": "npu_auditor",
                    "task_type": "parallel_guardrail_audit_old_pointer",
                    "target_block_id": block_id,
                    "can_edit_pointer": False,
                    "instruction": "Audita candidate_response_preview per placeholder/stub, path inventati, source writes non dichiarati, ripetizioni e candidate_applicability_flags. Usa diagnostic_preview come contesto secondario. Restituisci decisione accept/reject e motivi.",
                    **task_block_context(block),
                }
            )
    return tasks


def choose_resume_block(proposals: list[dict[str, Any]]) -> str:
    accepted = [block for block in proposals if block.get("accepted") is True]
    if accepted:
        return str(accepted[-1].get("block_id") or "")
    if proposals:
        latest = proposals[-1]
        return str(latest.get("resume_from_block_id") or latest.get("previous_block_id") or latest.get("block_id") or "")
    return ""


def build_report(pointer: dict[str, Any], composer: dict[str, Any], causality: dict[str, Any]) -> dict[str, Any]:
    proposals = proposal_blocks(pointer)
    gpu0 = peer_blocks(pointer, "gpu0_reviewer_refiner")
    npu = peer_blocks(pointer, "npu_auditor")
    gpu1_tasks = build_gpu1_tasks(proposals, composer)
    peer_tasks = build_peer_tasks(proposals, gpu0, npu)
    all_tasks = gpu1_tasks + peer_tasks
    latest = latest_block(proposals)
    pointer_limited = bool(pointer.get("max_blocks_applied"))
    warnings: list[str] = []
    if pointer_limited:
        warnings.append("pointer manifest was limited by max_blocks; revision tasks are based on exposed blocks only")
    return {
        "schema_version": 1,
        "kind": "external_heap_revision_context",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "protocol": "external_heap_revision_context_v1",
        "passed": True,
        "source_pointer_protocol": pointer.get("protocol"),
        "pointer_product_contract": pointer.get("pointer_product_contract"),
        "pointer_contract_role": pointer.get("pointer_contract_role"),
        "provider_execution_semantics": pointer.get("provider_execution_semantics"),
        "causal_chain_status": causality.get("causal_chain_status"),
        "causal_chain_passed": causality.get("causal_chain_passed"),
        "product_acceptance_status": causality.get("product_acceptance_status"),
        "product_acceptance_passed": causality.get("product_acceptance_passed"),
        "proposal_block_count": len(proposals),
        "source_block_count": pointer.get("source_block_count"),
        "pointer_block_count": pointer.get("block_count"),
        "pointer_max_blocks_applied": pointer_limited,
        "roles_present": pointer.get("roles_present"),
        "all_roles_present": pointer.get("all_roles_present", pointer.get("roles_present")),
        "gpu0_block_count": len(gpu0),
        "npu_block_count": len(npu),
        "resume_from_block_id": choose_resume_block(proposals),
        "latest_block_id": latest.get("block_id", ""),
        "parallel_task_count": len(all_tasks),
        "gpu1_task_count": len(gpu1_tasks),
        "gpu0_task_count": len([task for task in peer_tasks if task.get("role") == "gpu0_reviewer_refiner"]),
        "npu_task_count": len([task for task in peer_tasks if task.get("role") == "npu_auditor"]),
        "tasks": all_tasks,
        "runtime_instruction": (
            "GPU1 puo' avanzare o tornare indietro sui pointer. Se scopre un import, variabile, classe o contratto "
            "necessario, deve generare un task di propagazione sui blocchi precedenti, far rivalutare in parallelo GPU0/NPU, "
            "poi riprendere dal resume_from_block_id mantenendo la catena next/previous/refines."
        ),
        "provider_execution_performed": normalize_bool(pointer.get("provider_execution_performed")),
        "patch_application_performed": False,
        "source_writes_performed": False,
        "errors": [],
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# External Heap Revision Context",
        "",
        f"- Protocol: `{report['protocol']}`",
        f"- Passed: `{report.get('passed')}`",
        f"- Pointer contract role: `{report.get('pointer_contract_role')}`",
        f"- Provider execution semantics: `{report.get('provider_execution_semantics')}`",
        f"- Causal chain passed: `{report.get('causal_chain_passed')}`",
        f"- Product acceptance passed: `{report.get('product_acceptance_passed')}`",
        f"- Pointer max blocks applied: `{report.get('pointer_max_blocks_applied')}`",
        f"- Pointer block count: `{report.get('pointer_block_count')}`",
        f"- Source block count: `{report.get('source_block_count')}`",
        f"- Resume from block: `{report.get('resume_from_block_id')}`",
        f"- Latest block: `{report.get('latest_block_id')}`",
        f"- Parallel task count: `{report.get('parallel_task_count')}`",
        f"- GPU1 tasks: `{report.get('gpu1_task_count')}`",
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


def attach_to_composer_documents(composer: dict[str, Any], json_path: Path, markdown_path: Path, explicit_documents_dir: str) -> dict[str, str]:
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
        append_download_manifest(Path(manifest_value).expanduser().resolve(), [target_md, target_json])
    return {
        "documents_dir": str(documents_dir),
        "documents_json": str(target_json),
        "documents_markdown": str(target_md),
        "download_manifest_txt": manifest_value,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pointer-manifest", required=True)
    parser.add_argument("--composer-json", default="")
    parser.add_argument("--causality-json", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--documents-dir", default="")
    parser.add_argument("--no-documents-copy", action="store_true")
    args = parser.parse_args()

    pointer_path = Path(args.pointer_manifest).resolve()
    pointer = read_json(str(pointer_path))
    if not pointer:
        raise SystemExit(f"pointer manifest unreadable: {pointer_path}")
    composer = read_json(args.composer_json)
    causality = read_json(args.causality_json)
    output = Path(args.output).resolve() if args.output else pointer_path.with_name("external_heap_revision_context.json")
    markdown = Path(args.markdown_output).resolve() if args.markdown_output else output.with_suffix(".md")
    report = build_report(pointer, composer, causality)
    report["documents_copy_performed"] = False
    report["documents_outputs"] = {}
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    if not args.no_documents_copy:
        documents_outputs = attach_to_composer_documents(composer, output, markdown, args.documents_dir)
        if documents_outputs:
            report["documents_copy_performed"] = True
            report["documents_outputs"] = documents_outputs
            write_json(output, report)
            documents_json = documents_outputs.get("documents_json")
            if documents_json:
                shutil.copyfile(output, Path(documents_json).expanduser().resolve())
        else:
            report["warnings"].append("composer documents_dir not found; revision context kept in run dir only")
            write_json(output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
