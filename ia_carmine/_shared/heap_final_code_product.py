#!/usr/bin/env python3
"""Render lab evidence and code product excerpts for final heap documents."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

try:
    from ia_carmine.runtime.runtime_tool.file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[2]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_tool.file_refs import (  # type: ignore
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


def read_text_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8-sig", errors="replace")
    except Exception:
        return ""


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


def _explicit_bool(value: Any) -> bool | None:
    return value if isinstance(value, bool) else None


def lab_status_summary(
    *, run_dir: Path, gate: dict[str, Any], matrix: dict[str, Any], matrix_path: str
) -> dict[str, Any]:
    metrics = as_dict(gate.get("metrics"))
    virtual_report_path, virtual = first_json_report(
        run_dir, as_list(metrics.get("virtual_dev_environment_reports"))
    )
    debug_report = str(matrix.get("debug_lab_report") or "")
    if debug_report:
        debug = read_json(evidence_path(run_dir, debug_report))
    else:
        debug_report, debug = first_json_report(
            run_dir, as_list(metrics.get("runtime_debug_lab_reports"))
        )
    target_count = int(matrix.get("target_count") or 0)
    verified_target_count = int(matrix.get("verified_target_count") or 0)
    report_refs = [ref for ref in (virtual_report_path, matrix_path, debug_report) if ref]
    pass_values = {
        "virtual_dev_environment": _explicit_bool(
            metrics.get("virtual_dev_environment_passed", virtual.get("passed"))
        ),
        "code_execution_matrix": _explicit_bool(
            matrix.get("passed", metrics.get("code_execution_matrix_passed"))
        ),
        "runtime_debug_lab": _explicit_bool(
            debug.get("passed", matrix.get("debug_lab_passed", metrics.get("runtime_debug_lab_passed")))
        ),
    }
    required_missing = any(
        bool(metrics.get(required)) and not report
        for required, report in (
            ("virtual_dev_environment_required", virtual_report_path),
            ("code_execution_matrix_required", matrix_path),
            ("runtime_debug_lab_required", debug_report),
        )
    )
    lab_failed = required_missing or any(value is False for value in pass_values.values())
    lab_evidence_written = bool(report_refs)
    lab_tool_request_count = int(metrics.get("lab_tool_request_count") or 0)
    lab_tool_execution_count = int(metrics.get("lab_tool_execution_count") or 0)
    lab_called = bool(lab_tool_request_count > 0)
    lab_usable = bool(
        lab_called
        and not lab_failed
        and lab_evidence_written
        and (
            verified_target_count > 0
            or target_count > 0
            or bool(as_list(virtual.get("targets")))
            or int(debug.get("operation_count") or debug.get("target_count") or 0) > 0
        )
    )
    if lab_failed and lab_called:
        lab_status = "requested_failed"
    elif lab_failed:
        lab_status = "not_requested"
    elif not lab_called:
        lab_status = "not_requested"
    elif not lab_usable:
        lab_status = "report_written_unusable" if lab_evidence_written else "requested_failed"
    elif target_count <= 0 and verified_target_count <= 0:
        lab_status = "requested_no_targets"
    elif all(value is True for value in pass_values.values() if value is not None):
        lab_status = "passed"
    else:
        lab_status = "usable"
    return {
        "lab_status": lab_status,
        "lab_called": lab_called,
        "lab_evidence_written": lab_evidence_written,
        "lab_report_written": lab_evidence_written,
        "lab_usable": lab_usable,
        "lab_report_refs": report_refs,
        "lab_pass_values": pass_values,
        "lab_required_missing": required_missing,
        "tool_request_count": int(metrics.get("tool_request_count") or 0),
        "tool_execution_count": int(metrics.get("tool_execution_count") or 0),
        "lab_tool_request_count": lab_tool_request_count,
        "lab_tool_execution_count": lab_tool_execution_count,
        "provider_native_tool_call_count": int(metrics.get("provider_native_tool_call_count") or 0),
        "provider_textual_tool_call_count": int(metrics.get("provider_textual_tool_call_count") or 0),
        "provider_native_tool_loop_requested_count": int(metrics.get("provider_native_tool_loop_requested_count") or 0),
        "provider_native_tool_missing_lanes": as_list(metrics.get("provider_native_tool_missing_lanes")),
        "virtual_report_path": virtual_report_path,
        "virtual": virtual,
        "debug_report": debug_report,
        "debug": debug,
    }


def item_has_code_product(item: dict[str, Any]) -> bool:
    status = str(item.get("implementation_status") or "")
    source = str(item.get("source") or "")
    diff_source = str(item.get("diff_source") or "").strip()
    if diff_source == "current_worktree_diagnostic":
        return False
    if source == "patch_candidate_synthesis" and diff_source not in {
        "provider_owned",
        "evidence_owned",
    }:
        return False
    if status != "validated_patch_candidate" and source != "patch_candidate_synthesis":
        return False
    if status == "verified_target_no_worktree_diff":
        return False
    diff_ref = str(item.get("diff_path") or "").strip()
    sketch = str(item.get("code_or_patch_sketch") or "").strip()
    if diff_ref:
        return True
    if not sketch or sketch == "[no worktree diff captured]":
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
    diff_ref = str(item.get("diff_path") or "").strip()
    if diff_ref:
        diff_path = Path(diff_ref)
        if not diff_path.is_absolute():
            diff_path = matrix_repo_root(matrix) / diff_path
        diff_text = read_text_file(diff_path)
        if diff_text.strip():
            return diff_text.rstrip()
    return str(item.get("code_or_patch_sketch") or "").rstrip()


def code_product_items(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        as_dict(item)
        for item in as_list(matrix.get("concrete_code_proposals"))
        if isinstance(item, dict) and item_has_code_product(item)
    ]


def matrix_has_reviewable_targets(matrix: dict[str, Any]) -> bool:
    return int(matrix.get("verified_target_count") or matrix.get("target_count") or 0) > 0


def code_product_status(matrix: dict[str, Any], gate_product_status: str = "") -> str:
    if code_product_items(matrix) and matrix_has_reviewable_targets(matrix):
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
    lab = lab_status_summary(run_dir=run_dir, gate=gate, matrix=matrix, matrix_path=matrix_path)
    virtual_report_path = str(lab.get("virtual_report_path") or "")
    virtual = as_dict(lab.get("virtual"))
    debug_report = str(lab.get("debug_report") or "")
    debug = as_dict(lab.get("debug"))
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
    lab_status = str(lab.get("lab_status") or "not_run")
    if lab_status in {"usable", "passed"}:
        intro = "- Il lab non e' una promessa testuale: evidenza operativa disponibile."
        capability_line = "- Sa usarlo: `True`; lab/matrix/debug hanno evidenza verificabile per target."
    elif lab_status == "requested_failed":
        intro = "- Il lab/tooling operativo e' stato tentato, ma almeno una evidenza richiesta e' fallita o manca."
        capability_line = "- Sa usarlo: `False`; tool/lab tentati ma non validi per chiudere il prodotto."
    elif lab_status in {"requested_no_targets", "report_written_unusable"}:
        intro = "- Il lab e' stato tentato, ma non ha prodotto target verificabili."
        capability_line = "- Sa usarlo: `False`; nessun target verificato da lab/matrix/debug."
    else:
        intro = "- Il lab non risulta tentato in questa run."
        capability_line = "- Sa usarlo: `False`; nessuna evidenza lab/matrix/debug scritta."
    return [
        "## Laboratorio operativo",
        "",
        intro,
        f"- Lab status: `{lab_status}`.",
        f"- Lab called: `{lab.get('lab_called')}`.",
        f"- Lab report written: `{lab.get('lab_report_written')}`.",
        f"- Lab usable: `{lab.get('lab_usable')}`.",
        f"- Lab evidence written: `{lab.get('lab_evidence_written')}`.",
        f"- Tool calling attempts: lab_requests=`{lab.get('lab_tool_request_count')}` lab_executions=`{lab.get('lab_tool_execution_count')}` total_requests=`{lab.get('tool_request_count')}` total_executions=`{lab.get('tool_execution_count')}` native_provider_calls=`{lab.get('provider_native_tool_call_count')}` textual_tool_calls=`{lab.get('provider_textual_tool_call_count')}`.",
        f"- Native tool loop requested: `{lab.get('provider_native_tool_loop_requested_count')}`; missing lanes: `{lab.get('provider_native_tool_missing_lanes')}`.",
        f"- Lab pass values: `{lab.get('lab_pass_values')}`; required_missing=`{lab.get('lab_required_missing')}`.",
        f"- Virtual dev report: `{virtual_report_path}`.",
        f"- Virtual dev passed: `{virtual.get('passed')}` su `{len(ok_virtual_targets)}/{len(virtual_targets)}` target con AST/import/help probe.",
        f"- Validation scripts nel virtual dev: `{virtual.get('validation_count')}`.",
        f"- Code matrix report: `{matrix_path}`.",
        f"- Debug lab report: `{debug_report}`.",
        f"- Debug lab passed: `{matrix.get('debug_lab_passed') or debug.get('passed')}`.",
        f"- Debug lab target count: `{matrix.get('target_count')}`.",
        f"- Guardrails matrix: free_shell=`{guardrails.get('free_shell_exposed')}` source_writes=`{guardrails.get('source_writes_performed')}` patch_apply=`{guardrails.get('patch_application_performed')}` git_write=`{guardrails.get('git_write_performed')}`.",
        f"- Guardrails virtual dev: free_shell=`{virtual_guardrails.get('free_shell_exposed')}` source_writes=`{virtual_guardrails.get('source_writes_performed')}` patch_apply=`{virtual_guardrails.get('patch_application_performed')}` git_write=`{virtual_guardrails.get('git_write_performed')}`.",
        capability_line,
        "",
    ]


def render_code_product_section(matrix: dict[str, Any]) -> list[str]:
    lines = [
        "## Code product",
        "",
    ]
    product_items = full_code_product_items(matrix) if matrix_has_reviewable_targets(matrix) else []
    if product_items:
        lines.extend(
            [
                "Questi sono i diff/code completi usciti dalla matrice deterministica. I chunk GPU1 respinti non sono inclusi qui come prodotto.",
                "Lo stesso patch/code completo viene pubblicato anche come `CODE_PRODUCT_FULL_PATCH.md` nel pacchetto Documents della run.",
                "",
            ]
        )
    for data in product_items:
        target = str(data.get("target_file") or "")
        sketch = full_code_or_patch(matrix, data)
        if not target or not sketch:
            continue
        lines.extend(
            [
                f"### {target}",
                "",
                f"- Git status: `{data.get('git_status')}`.",
                f"- Implementation status: `{data.get('implementation_status')}`.",
                f"- Diff source: `{data.get('diff_source') or 'unknown'}`.",
                "",
                "```diff",
                sketch,
                "```",
                "",
            ]
        )
    if not product_items:
        lines.extend(["- NO_APPLICABLE_CODE_PRODUCT.", "- Nessun diff/code effettivo catturato dalla matrix.", ""])
    return lines


def render_full_code_product_markdown(
    matrix: dict[str, Any],
    matrix_path: str,
    gate_product_status: str = "",
    blocked_reason: str = "",
) -> str:
    product_items = full_code_product_items(matrix) if matrix_has_reviewable_targets(matrix) else []
    matrix_product_items = code_product_items(matrix)
    matrix_items = as_list(matrix.get("concrete_code_proposals"))
    status = code_product_status(matrix, gate_product_status)
    reason_text = str(blocked_reason)
    provider_runtime_blocked = any(
        token in reason_text
        for token in ("gpu1_", "gpu0_", "npu_", "provider_runtime", "provider work rejected")
    )
    if provider_runtime_blocked:
        status = "PROVIDER_RUNTIME_BLOCKED"
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
        "- Final assembler worktree fallback: `disabled`",
        f"- Upstream worktree diagnostic candidate count: `{matrix.get('upstream_worktree_candidate_count', 0)}`",
        f"- Current worktree diff candidates allowed: `{matrix.get('allow_current_worktree_diff_candidates', False)}`",
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
                f"- Diff source: `{data.get('diff_source') or 'unknown'}`",
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
        marker = "NO_APPLICABLE_CODE_PRODUCT"
        detail_marker = (
            "PROVIDER_RUNTIME_BLOCKED_NO_CODE_PRODUCT"
            if provider_runtime_blocked
            else "PROVIDER_REPLIGHT_FAILED_NO_CODE_PRODUCT"
            if "provider_replight_failed" in reason_text
            else ""
        )
        lines.extend(
            [
                f"- Marker: `{marker}`.",
                f"- Block detail marker: `{detail_marker}`.",
                "- Nessun diff/code effettivo catturato dalla matrix.",
                f"- Status: `{status}`.",
                "- Questo artifact non e' un prodotto applicabile: usare la matrix come evidenza di blocco, non come patch.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
