"""Public Documents mirror for operator product runs."""

from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from .models import LauncherConfig


def default_public_documents_root(stamp: str) -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Documents" / f"aicarmine_gui_launcher_lab_{stamp}"


def mirror_public_documents_package(
    config: LauncherConfig,
    run_report: dict[str, Any],
    lab_report: dict[str, Any],
) -> dict[str, Any]:
    root = default_public_documents_root(config.stamp)
    if config.no_documents:
        return _result(root, False, "no_documents_flag", [])
    root.mkdir(parents=True, exist_ok=True)
    outputs: list[str] = []
    source_dir = _source_documents_dir(run_report, lab_report)
    if source_dir and source_dir.exists() and source_dir.resolve() != root.resolve():
        outputs.extend(_copy_tree_contents(source_dir, root))
    outputs.extend(_copy_selected_run_artifacts(run_report, root / "_technical"))
    outputs.extend(_ensure_fallback_product_files(root, run_report, lab_report))
    return _result(root, True, "", outputs, source_dir)


def _result(
    root: Path,
    performed: bool,
    reason: str,
    outputs: list[str],
    source_dir: Path | None = None,
) -> dict[str, Any]:
    return {
        "public_documents_root": str(root),
        "public_documents_mirror_performed": performed,
        "public_documents_mirror_reason": reason,
        "public_documents_source_dir": str(source_dir or ""),
        "public_documents_outputs": sorted(dict.fromkeys(outputs)),
    }


def _source_documents_dir(run_report: dict[str, Any], lab_report: dict[str, Any]) -> Path | None:
    for payload in (
        run_report.get("launcher_summary_payload"),
        run_report,
        lab_report,
    ):
        if not isinstance(payload, dict):
            continue
        outputs = payload.get("final_readable_product_documents_outputs")
        if isinstance(outputs, dict):
            for value in outputs.values():
                path = Path(str(value or ""))
                if path.is_file():
                    return path.parent
        path = Path(str(payload.get("code_product") or ""))
        if path.is_file():
            return path.parent
    return None


def _copy_tree_contents(source: Path, target: Path) -> list[str]:
    outputs: list[str] = []
    for item in source.iterdir():
        destination = target / item.name
        if item.is_dir():
            shutil.copytree(item, destination, dirs_exist_ok=True)
            outputs.extend(str(path) for path in destination.rglob("*") if path.is_file())
        elif item.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(item, destination)
            outputs.append(str(destination))
    return outputs


def _copy_selected_run_artifacts(run_report: dict[str, Any], target: Path) -> list[str]:
    run_dir_text = str(run_report.get("intermediate_run_dir") or "")
    if not run_dir_text:
        return []
    run_dir = Path(run_dir_text)
    names = (
        "operator_product_launcher_run.json",
        "operator_product_launcher_run.md",
        "heap_runtime_context_closure_launcher.json",
        "heap_final_readable_product.json",
        "heap_final_readable_product.md",
        "heap_final_readable_product.txt",
        "external_heap_block_pointer_manifest.json",
        "external_heap_block_pointer_manifest.md",
        "external_heap_revision_context.json",
        "external_heap_revision_context.md",
    )
    outputs: list[str] = []
    if not run_dir.exists():
        return outputs
    target.mkdir(parents=True, exist_ok=True)
    for name in names:
        source = run_dir / name
        if source.is_file():
            destination = target / name
            shutil.copy2(source, destination)
            outputs.append(str(destination))
    for source in _gpu1_one_turn_gate_sources(run_report, run_dir):
        if source.is_file():
            destination = target / source.name
            shutil.copy2(source, destination)
            outputs.append(str(destination))
    return outputs


def _gpu1_one_turn_gate_sources(run_report: dict[str, Any], run_dir: Path) -> list[Path]:
    values: list[str] = []
    for payload in (run_report.get("launcher_summary_payload"), run_report):
        if isinstance(payload, dict):
            values.append(str(payload.get("gpu1_one_turn_runtime_gate_path") or ""))
    sources: list[Path] = []
    for value in values:
        if not value:
            continue
        path = Path(value)
        if not path.is_absolute():
            repo_root = run_dir.parent.parent.parent if len(run_dir.parents) >= 3 else run_dir
            path = repo_root / value if value.startswith("output/") else run_dir / value
        sources.append(path)
    provider_dir = run_dir / "provider_teamwork"
    if provider_dir.is_dir():
        sources.extend(provider_dir.glob("gpu1_one_turn_runtime_gate*.json"))
    return sorted({path.resolve(strict=False) for path in sources})


def _ensure_fallback_product_files(
    root: Path,
    run_report: dict[str, Any],
    lab_report: dict[str, Any],
) -> list[str]:
    status = str(lab_report.get("product_status") or run_report.get("product_status") or "")
    reason = str(
        lab_report.get("product_blocked_reason")
        or run_report.get("product_blocked_reason")
        or "not_proven"
    )
    outputs: list[str] = []
    files = {
        "FINAL_READABLE_PRODUCT.md": "\n".join(
            [
                "# IA-Carmine Final Product",
                "",
                f"- Status: `{status or 'blocked_with_reason'}`",
                f"- Blocked reason: `{reason}`",
                f"- Resume from block: `{run_report.get('resume_from_block_id') or ''}`",
                f"- Intermediate run dir: `{run_report.get('intermediate_run_dir') or ''}`",
                "",
            ]
        ),
        "OPERATOR_DECISION.txt": f"status={status or 'blocked_with_reason'}\nreason={reason}\n",
        "CODE_PRODUCT_FULL_PATCH.md": "\n".join(
            [
                "# CODE_PRODUCT_FULL_PATCH",
                "",
                "NO_APPLICABLE_CODE_PRODUCT",
                "",
                f"Blocked reason: {reason}",
                "",
            ]
        ),
        "PLAN_PRODUCT_FULL_PATCH.md": "\n".join(
            [
                "# PLAN_PRODUCT_FULL_PATCH",
                "",
                "technical_plan_product",
                "",
                f"Status: {status or 'blocked_with_reason'}",
                f"Blocked reason: {reason}",
                f"Resume from block: {run_report.get('resume_from_block_id') or ''}",
                "",
                "This fallback file is a final plan/evidence artifact, not an applicable diff.",
                "",
            ]
        ),
    }
    for name, text in files.items():
        path = root / name
        if not path.exists():
            path.write_text(text, encoding="utf-8")
        outputs.append(str(path))
    return outputs
