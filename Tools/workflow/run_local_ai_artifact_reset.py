#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

CONFIRM_TEXT = "DELETE LOCAL AI ARTIFACTS"

TARGETS = [
    ("local_ai_runs", "output/local_ai_runs", False),
    ("ai_pipeline", "output/ai_pipeline", False),
    ("validation_reports", "output/validation", False),
    ("ai_context_packs", "output/ai_context_packs", False),
    ("patch_specs", "output/patch_specs", False),
    ("agent_memory", "indexAI/agent_memory", True),
    ("generated_index_context", "indexAI/code_chunks", True),
    ("generated_project_chunks", "indexAI/project_code_chunks", True),
]


def parse_dt(value: str) -> datetime:
    text = value.strip()
    if not text:
        return datetime.min
    # PowerShell ToString("s") produces ISO without timezone.
    return datetime.fromisoformat(text)


def relpath(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except Exception:
        return path.as_posix().replace("\\", "/")


def is_active_artifact(rel: str, active_stamps: set[str]) -> bool:
    normalized = rel.replace("\\", "/")
    for stamp in active_stamps:
        if not stamp:
            continue
        if normalized.startswith(f"output/local_ai_runs/{stamp}_"):
            return True
        if normalized.startswith(f"output/ai_packets/{stamp}/"):
            return True
        if normalized.startswith(f"output/validation/prerun_local_ai_reset_{stamp}"):
            return True
    return False


def iter_top_level_candidates(root: Path, before: datetime, include_memory: bool, include_index: bool, active_stamps: set[str]):
    for category, rel_root, optional in TARGETS:
        if category == "agent_memory" and not include_memory:
            continue
        if category in {"generated_index_context", "generated_project_chunks"} and not include_index:
            continue
        base = root / rel_root
        if not base.exists():
            continue
        for child in base.iterdir():
            child_rel = relpath(child, root)
            if is_active_artifact(child_rel, active_stamps):
                continue
            try:
                mtime = datetime.fromtimestamp(child.stat().st_mtime)
            except OSError:
                continue
            if before != datetime.min and mtime >= before:
                continue
            yield category, child


def remove_path(path: Path) -> tuple[bool, str | None]:
    try:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        else:
            path.unlink(missing_ok=True)
        return True, None
    except Exception as exc:  # noqa: BLE001
        return False, f"{type(exc).__name__}: {exc}"


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_markdown(path: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Local AI bounded reset",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Apply reset: `{report.get('apply_reset')}`",
        f"- Candidate count: `{report.get('candidate_count')}`",
        f"- Deleted count: `{report.get('deleted_count')}`",
        f"- Failed count: `{report.get('failed_count')}`",
        f"- Reset before date: `{report.get('reset_before_date')}`",
        "",
        "## Candidate preview",
        "",
    ]
    for item in report.get("candidate_preview", []):
        lines.append(f"- `{item.get('path')}` category=`{item.get('category')}` deleted=`{item.get('deleted')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {err}" for err in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warn}" for warn in report["warnings"])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Bounded local AI artifact reset for pre-run cleanup.")
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--before-date", default="")
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--confirm-reset-text", default="")
    parser.add_argument("--include-memory-reset", action="store_true")
    parser.add_argument("--include-generated-index-reset", action="store_true")
    parser.add_argument("--active-stamp", action="append", default=[])
    parser.add_argument("--output", default="output/validation/local_ai_bounded_reset.json")
    parser.add_argument("--markdown-output", default="output/validation/local_ai_bounded_reset.md")
    parser.add_argument("--max-preview", type=int, default=200)
    args = parser.parse_args()

    repo_root = Path(args.repo_root).resolve()
    before = parse_dt(args.before_date) if args.before_date else datetime.min
    errors: list[str] = []
    warnings: list[str] = []

    if args.apply and args.confirm_reset_text != CONFIRM_TEXT:
        errors.append("apply reset requires exact confirmation text")

    active_stamps = {str(item).strip() for item in args.active_stamp if str(item).strip()}

    candidates = list(
        iter_top_level_candidates(
            repo_root,
            before,
            include_memory=args.include_memory_reset,
            include_index=args.include_generated_index_reset,
            active_stamps=active_stamps,
        )
    )

    preview: list[dict[str, Any]] = []
    deleted_count = 0
    failed_count = 0

    for category, path in candidates:
        rel = relpath(path, repo_root)
        deleted = False
        error = None
        if args.apply and not errors:
            ok, error = remove_path(path)
            deleted = ok
            if ok:
                deleted_count += 1
            else:
                failed_count += 1
                errors.append(f"failed to remove {rel}: {error}")
        if len(preview) < args.max_preview:
            preview.append(
                {
                    "path": rel,
                    "category": category,
                    "deleted": deleted,
                    "error": error,
                }
            )

    if len(candidates) > args.max_preview:
        warnings.append(f"candidate preview truncated to {args.max_preview} of {len(candidates)} top-level candidates")

    report = {
        "schema_version": 1,
        "kind": "local_ai_bounded_reset",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "apply_reset": bool(args.apply),
        "reset_before_date": before.isoformat() if before != datetime.min else None,
        "include_memory_reset": bool(args.include_memory_reset),
        "include_generated_index_reset": bool(args.include_generated_index_reset),
        "active_stamps": sorted(active_stamps),
        "candidate_count": len(candidates),
        "deleted_count": deleted_count,
        "failed_count": failed_count,
        "candidate_preview": preview,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "blender_runtime_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "errors": errors,
        "warnings": warnings,
    }

    output = repo_root / args.output if not Path(args.output).is_absolute() else Path(args.output)
    md_output = repo_root / args.markdown_output if not Path(args.markdown_output).is_absolute() else Path(args.markdown_output)
    write_json(output, report)
    write_markdown(md_output, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
