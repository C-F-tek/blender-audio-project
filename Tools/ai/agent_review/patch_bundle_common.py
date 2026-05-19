"""Shared helpers for agent-review patch bundles."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai._shared.code_patch_plan_common import read_json_object

DEFAULT_PATCH_PLAN = "output/patch_specs/agent_review_patch_plan.json"
DEFAULT_OUTPUT_DIR = "output/validation/patch_bundles"
DEFAULT_OUTPUT = "output/validation/agent_review_patch_bundle_builder.json"
DEFAULT_MARKDOWN = "output/validation/agent_review_patch_bundle_builder.md"
DEFAULT_BASENAME = "agent_review_patch_bundle"

FORBIDDEN_TARGET_PREFIXES = (
    "output/",
    "renders/",
    ".git/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
)
FORBIDDEN_TARGET_SUFFIXES = (".db", ".sqlite", ".sqlite3")
MANAGED_BEGIN_PREFIX = "<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:BEGIN"
MANAGED_END_PREFIX = "<!-- IA-CARMINE:AGENT-REVIEW-PATCH-PLAN:END"

def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")

def stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")

def resolve_path(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    if not path.is_absolute():
        path = repo_root / path
    return path.resolve(strict=False)

def repo_rel(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve(strict=False).relative_to(repo_root.resolve(strict=False)).as_posix()
    except ValueError:
        return path.resolve(strict=False).as_posix()

def normalize_repo_path(value: Any) -> str:
    return str(value or "").strip().replace("\\", "/").strip("/")

def stable_id(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9_.-]+", "-", value).strip("-._").lower()
    if cleaned:
        return cleaned[:80]
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]

def safe_json(data: Any) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)

def target_path_error(path_value: str, repo_root: Path) -> str | None:
    normalized = normalize_repo_path(path_value)
    if not normalized:
        return "empty target path"
    if Path(normalized).is_absolute():
        return "absolute target paths are not allowed"
    full = (repo_root / normalized).resolve(strict=False)
    try:
        full.relative_to(repo_root.resolve(strict=False))
    except ValueError:
        return "target path escapes repository root"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_TARGET_PREFIXES):
        return f"forbidden target prefix: {normalized}"
    if any(normalized.lower().endswith(suffix) for suffix in FORBIDDEN_TARGET_SUFFIXES):
        return f"forbidden database target: {normalized}"
    if not full.exists():
        return "target file does not exist"
    if not full.is_file():
        return "target is not a file"
    return None

def is_markdown(path_value: str) -> bool:
    return normalize_repo_path(path_value).lower().endswith((".md", ".markdown"))

def load_patch_plan(path: Path) -> tuple[dict[str, Any], list[str]]:
    data, errors = read_json_object(path)
    return data, [str(error) for error in errors]

def plan_items(patch_plan: dict[str, Any]) -> list[dict[str, Any]]:
    items = patch_plan.get("patch_plans")
    if isinstance(items, list):
        return [item for item in items if isinstance(item, dict)]
    return []

def build_managed_block(plan: dict[str, Any], target: str) -> str:
    plan_id = stable_id(str(plan.get("id") or target))
    area = str(plan.get("area") or "unknown")
    source = str(plan.get("source") or "unknown")
    risk = str(plan.get("risk") or "unknown")
    rationale = str(plan.get("rationale") or "").strip()
    strategy = str(plan.get("edit_strategy") or plan.get("proposed_strategy") or "").strip()
    validation_commands = (
        plan.get("validation_commands") if isinstance(plan.get("validation_commands"), list) else []
    )
    stop_conditions = (
        plan.get("stop_conditions") if isinstance(plan.get("stop_conditions"), list) else []
    )
    block_id = f"{plan_id}:{stable_id(target)}"
    lines = [
        "",
        f"{MANAGED_BEGIN_PREFIX} id={block_id} -->",
        "",
        "### IA-Carmine agent-review patch note",
        "",
        "This managed note records an evidence-backed manual-review patch plan. It is intentionally compact and idempotent.",
        "",
        f"- Plan id: `{plan.get('id')}`",
        f"- Area: `{area}`",
        f"- Source: `{source}`",
        f"- Risk: `{risk}`",
        f"- Target: `{target}`",
    ]
    if rationale:
        lines.append(f"- Rationale: {rationale}")
    if strategy:
        lines.append(f"- Strategy: {strategy}")
    if validation_commands:
        lines.append("- Validation commands:")
        for command in validation_commands[:8]:
            lines.append(f"  - `{command}`")
    if stop_conditions:
        lines.append("- Stop conditions:")
        for condition in stop_conditions[:8]:
            lines.append(f"  - {condition}")
    lines.extend(["", f"{MANAGED_END_PREFIX} id={block_id} -->", ""])
    return "\n".join(lines)

def collect_operations(
    patch_plan: dict[str, Any], repo_root: Path
) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    operations: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    seen: set[str] = set()
    for plan in plan_items(patch_plan):
        plan_id = str(plan.get("id") or "unknown")
        targets = plan.get("target_files") if isinstance(plan.get("target_files"), list) else []
        if not targets:
            skipped.append({"id": plan_id, "reason": "plan has no target_files"})
            continue
        for raw_target in targets:
            target = normalize_repo_path(raw_target)
            key = f"{plan_id}:{target}"
            if key in seen:
                continue
            seen.add(key)
            error = target_path_error(target, repo_root)
            if error:
                skipped.append({"id": plan_id, "target": target, "reason": error})
                continue
            if not is_markdown(target):
                skipped.append(
                    {
                        "id": plan_id,
                        "target": target,
                        "reason": "non-Markdown targets are manual-review-only in this bundle",
                    }
                )
                continue
            full = resolve_path(repo_root, target)
            try:
                original = full.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                skipped.append(
                    {
                        "id": plan_id,
                        "target": target,
                        "reason": "target is not UTF-8 text",
                    }
                )
                continue
            block = build_managed_block(plan, target)
            block_hash = hashlib.sha256(block.encode("utf-8")).hexdigest()
            operations.append(
                {
                    "id": stable_id(key),
                    "plan_id": plan_id,
                    "target": target,
                    "kind": "markdown_managed_block",
                    "mode": "append_or_replace_managed_block",
                    "managed_begin_prefix": MANAGED_BEGIN_PREFIX,
                    "managed_end_prefix": MANAGED_END_PREFIX,
                    "block_hash_sha256": block_hash,
                    "original_sha256": hashlib.sha256(original.encode("utf-8")).hexdigest(),
                    "block": block,
                    "manual_review_required": True,
                }
            )
    return operations, skipped
