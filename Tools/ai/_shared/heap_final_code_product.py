#!/usr/bin/env python3
"""Render lab evidence and code product excerpts for final heap documents."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from Tools.ai.runtime_tool.file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.runtime_tool.file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )


def as_dict(value: Any) -> dict[str, Any]:
    return value if isinstance(value, dict) else {}


def as_list(value: Any) -> list[Any]:
    return value if isinstance(value, list) else []


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}
    return data if isinstance(data, dict) else {}


def repo_root_from_run_dir(run_dir: Path) -> Path:
    for path in [run_dir, *run_dir.parents]:
        if (path / "AGENTS.md").exists() or (path / ".git").exists():
            return path
    try:
        return run_dir.parents[2]
    except IndexError:
        return run_dir


def evidence_path(run_dir: Path, value: Any) -> Path:
    raw = Path(str(value or ""))
    if raw.is_absolute():
        return raw
    text = str(value or "").replace("\\", "/")
    if text.startswith("output/"):
        return repo_root_from_run_dir(run_dir) / raw
    return run_dir / raw


def first_json_report(run_dir: Path, values: list[Any]) -> tuple[str, dict[str, Any]]:
    for value in values:
        text = str(value)
        if not text.endswith(".json"):
            continue
        path = evidence_path(run_dir, text)
        payload = read_json(path)
        if payload:
            return text, payload
    return "", {}


def truncate_code(text: str, limit: int = 1800) -> str:
    body = str(text or "").strip()
    if len(body) <= limit:
        return body
    return (
        body[:limit].rstrip()
        + "\n...[code product excerpt truncated; full file/diff in workspace and matrix report]"
    )


def item_has_code_product(item: dict[str, Any]) -> bool:
    status = str(item.get("implementation_status") or "")
    source = str(item.get("source") or "")
    if status != "validated_patch_candidate" and source != "patch_candidate_synthesis":
        return False
    sketch = str(item.get("code_or_patch_sketch") or "").strip()
    if not sketch or sketch == "[no worktree diff captured]":
        return False
    if status == "verified_target_no_worktree_diff":
        return False
    return True


def normalize_target(value: Any) -> str:
    return str(value or "").strip().strip("`'\"").replace("\\", "/").lstrip("./")


def is_reviewable_product_target(target: str, repo_root: Path | None = None) -> bool:
    normalized = normalize_target(target)
    if not normalized:
        return False
    resolver = RuntimeFileRefResolver(repo_root or Path.cwd())
    ref = resolver.resolve(
        normalized,
        provenance=RuntimeRefProvenance.MATRIX_REPORT,
        consumers=(RuntimeConsumer.FINAL_ASSEMBLER,),
    )
    return ref.patchable


def matrix_repo_root(matrix: dict[str, Any]) -> Path:
    raw = str(matrix.get("repo_root") or "").strip()
    return Path(raw).resolve(strict=False) if raw else Path.cwd()


def diff_hunk_count(payload: str) -> int:
    return sum(1 for line in str(payload or "").splitlines() if line.startswith("@@ "))


def full_code_or_patch(matrix: dict[str, Any], item: dict[str, Any]) -> str:
    return str(item.get("code_or_patch_sketch") or "").rstrip()


def code_product_items(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        as_dict(item)
        for item in as_list(matrix.get("concrete_code_proposals"))
        if isinstance(item, dict) and item_has_code_product(item)
    ]


def code_product_status(matrix: dict[str, Any], gate_product_status: str = "") -> str:
    if code_product_items(matrix):
        if gate_product_status and gate_product_status != "ready":
            return "BLOCKED_WITH_CODE_PRODUCT_REVIEW"
        return "APPLY_REVIEW_READY"
    if (
        matrix.get("passed") is True
        and int(matrix.get("verified_target_count") or matrix.get("target_count") or 0) > 0
        and matrix.get("patch_candidate_synthesis_requested") is True
    ):
        return "TARGETS_FOUND_BUT_NO_VALID_PATCH_CANDIDATE"
    return "NO_APPLICABLE_CODE_PRODUCT"


def full_code_product_items(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    return code_product_items(matrix)


def render_lab_section(
    *, run_dir: Path, gate: dict[str, Any], matrix: dict[str, Any], matrix_path: str
) -> list[str]:
    metrics = as_dict(gate.get("metrics"))
    virtual_report_path, virtual = first_json_report(
        run_dir, as_list(metrics.get("virtual_dev_environment_reports"))
    )
    debug_report = str(matrix.get("debug_lab_report") or "")
    debug_path = evidence_path(run_dir, debug_report) if debug_report else Path()
    debug = read_json(debug_path) if debug_report else {}
    virtual_targets = as_list(virtual.get("targets"))
    ok_virtual_targets = [
        item
        for item in virtual_targets
        if as_dict(item).get("ast_ok")
        and as_dict(item).get("import_ok")
        and as_dict(item).get("help_ok")
    ]
    guardrails = as_dict(matrix.get("guardrails"))
    virtual_guardrails = as_dict(virtual.get("guardrails"))
    return [
        "## Laboratorio operativo",
        "",
        "- Il lab non e' una promessa testuale: e' stato chiamato via broker durante la run.",
        f"- Virtual dev report: `{virtual_report_path}`.",
        f"- Virtual dev passed: `{virtual.get('passed')}` su `{len(ok_virtual_targets)}/{len(virtual_targets)}` target con AST/import/help probe.",
        f"- Validation scripts nel virtual dev: `{virtual.get('validation_count')}`.",
        f"- Code matrix report: `{matrix_path}`.",
        f"- Debug lab report: `{debug_report}`.",
        f"- Debug lab passed: `{matrix.get('debug_lab_passed') or debug.get('passed')}`.",
        f"- Debug lab target count: `{matrix.get('target_count')}`.",
        f"- Guardrails matrix: free_shell=`{guardrails.get('free_shell_exposed')}` source_writes=`{guardrails.get('source_writes_performed')}` patch_apply=`{guardrails.get('patch_application_performed')}` git_write=`{guardrails.get('git_write_performed')}`.",
        f"- Guardrails virtual dev: free_shell=`{virtual_guardrails.get('free_shell_exposed')}` source_writes=`{virtual_guardrails.get('source_writes_performed')}` patch_apply=`{virtual_guardrails.get('patch_application_performed')}` git_write=`{virtual_guardrails.get('git_write_performed')}`.",
        "- Sa usarlo: `True`; ha caricato moduli, fatto import dinamico, provato --help, lanciato smoke e prodotto code matrix/debug lab evidence.",
        "",
    ]


def render_code_product_section(matrix: dict[str, Any]) -> list[str]:
    lines = [
        "## Code product",
        "",
        "Questi sono gli estratti di prodotto codice usciti dalla matrice deterministica. Per i file modificati sono diff excerpt; per i file nuovi sono new-file excerpt. I chunk GPU1 respinti non sono inclusi qui come prodotto.",
        "Il patch/code completo disponibile nella matrix viene pubblicato anche come `CODE_PRODUCT_FULL_PATCH.md` nel pacchetto Documents della run.",
        "",
    ]
    product_items = full_code_product_items(matrix)
    for data in product_items:
        target = str(data.get("target_file") or "")
        sketch = truncate_code(full_code_or_patch(matrix, data))
        if not target or not sketch:
            continue
        lines.extend(
            [
                f"### {target}",
                "",
                f"- Git status: `{data.get('git_status')}`.",
                f"- Implementation status: `{data.get('implementation_status')}`.",
                "",
                "```diff",
                sketch,
                "```",
                "",
            ]
        )
    if not product_items:
        lines.extend(["- Nessun diff/code effettivo catturato dalla matrix.", ""])
    return lines


def render_full_code_product_markdown(
    matrix: dict[str, Any], matrix_path: str, gate_product_status: str = ""
) -> str:
    product_items = full_code_product_items(matrix)
    matrix_product_items = code_product_items(matrix)
    matrix_items = as_list(matrix.get("concrete_code_proposals"))
    status = code_product_status(matrix, gate_product_status)
    lines = [
        "# CODE_PRODUCT_FULL_PATCH",
        "",
        "Artifact generato dalla run. Contiene solo diff/code effettivo disponibile nella code execution matrix; non include target verificati senza diff e non include chunk provider respinti dal gate.",
        "",
        "## Provenienza",
        "",
        f"- Matrix report: `{matrix_path}`",
        f"- Matrix passed: `{matrix.get('passed')}`",
        f"- Debug lab report: `{matrix.get('debug_lab_report')}`",
        f"- Debug lab passed: `{matrix.get('debug_lab_passed')}`",
        f"- Matrix concrete proposal count: `{matrix.get('concrete_code_proposal_count', len(matrix_items))}`",
        f"- Matrix code product count: `{len(matrix_product_items)}`",
        f"- Code product status: `{status}`",
        f"- Gate product status: `{gate_product_status or 'unknown'}`",
        f"- Patch candidate synthesis requested: `{matrix.get('patch_candidate_synthesis_requested')}`",
        f"- Patch candidate synthesis passed count: `{matrix.get('patch_candidate_synthesis_passed_count')}`",
        "- Worktree diff fallback: `disabled`",
        f"- Verified target count: `{matrix.get('verified_target_count', matrix.get('target_count'))}`",
        "",
        "## Guardrail",
        "",
    ]
    guardrails = as_dict(matrix.get("guardrails"))
    for key in (
        "free_shell_exposed",
        "source_writes_performed",
        "patch_application_performed",
        "git_write_performed",
    ):
        lines.append(f"- {key}: `{guardrails.get(key)}`")
    lines.extend(["", "## Code / Patch", ""])
    for data in product_items:
        target = str(data.get("target_file") or "")
        sketch = full_code_or_patch(matrix, data)
        if not target:
            continue
        lines.extend(
            [
                f"### {target}",
                "",
                f"- Git status: `{data.get('git_status')}`",
                f"- Implementation status: `{data.get('implementation_status')}`",
                f"- Diff hunks: `{data.get('diff_hunk_count')}`",
                f"- Validation commands: `{data.get('validation_commands')}`",
                "",
                "```diff",
                sketch,
                "```",
                "",
            ]
        )
    if not product_items:
        lines.extend(
            [
                "- Nessun diff/code effettivo catturato dalla matrix.",
                f"- Status: `{status}`.",
                "- Questo artifact non e' un prodotto applicabile: usare la matrix come evidenza di blocco, non come patch.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
