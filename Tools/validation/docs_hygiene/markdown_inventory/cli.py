#!/usr/bin/env python3
"""Build a report-only Markdown inventory.

Supports both regular Markdown files and IA-Carmine directory-form splits:

    name.md/README.md
    name.md/part-001.md
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from Tools.validation._shared.markdown_inventory_render import render_markdown
except ModuleNotFoundError:
    from Tools.validation._shared.markdown_inventory_render import render_markdown

IGNORED_DIR_NAMES = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "venv",
    "__pycache__",
    "node_modules",
    "output",
    "renders",
}
CANONICAL_INDEX_FILES = [
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "docs/README.md",
    "docs/LOCAL_AI_TASKS/README.md",
    "docs/MODULE_MAP.md",
    "Tools/validation/README.md",
    "Tools/npu/pipeline/README.md",
]
ROOT_COMMUNITY_DOCS = {
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "LICENSE.md",
    "SECURITY.md",
    "SUPPORT.md",
}
ROOT_POLICY_DOCS = {
    "AGENTS.md",
    "README.md",
    "WORKFLOW.md",
    "CHANGELOG.md",
    "AI_PATCH_BUNDLE_TECHNICAL_GOTCHAS.md",
    "TOOL_UTILI_CODING.md",
}
EVIDENCE_PREFIX = "docs/LOCAL_VALIDATION_EVIDENCE/"
TASK_PREFIX = "docs/LOCAL_AI_TASKS/"
EXECUTION_PLAN_PREFIX = "docs/EXECUTION_PLANS/"
GENERATED_INDEX_PREFIXES = ("indexAI/", "Tools/npu/npu_code_", "Tools/npu/npu_music_chunks/")
GENERATED_NPU_DOCS = {
    "Tools/npu/context_artifacts/generated_implementation_notes.md",
    "Tools/npu/context_artifacts/npu_music_context.md",
    "Tools/npu/context_artifacts/ollama_music_insights.md",
}
GITHUB_TEMPLATE_PREFIXES = (".github/ISSUE_TEMPLATE/",)
GITHUB_TEMPLATE_FILES = {".github/PULL_REQUEST_TEMPLATE.md"}


def repo_relative(path: Path, repo_root: Path) -> str:
    return path.resolve().relative_to(repo_root.resolve()).as_posix()


def split_container_for(path: Path, repo_root: Path) -> str | None:
    try:
        parts = path.resolve().relative_to(repo_root.resolve()).parts
    except ValueError:
        return None
    for index, part in enumerate(parts[:-1]):
        if part.endswith(".md"):
            return "/".join(parts[: index + 1])
    return None


def markdown_role(path: Path, repo_root: Path) -> str:
    if not split_container_for(path, repo_root):
        return "markdown_file"
    name = path.name.lower()
    if name == "readme.md":
        return "split_index"
    if name.startswith("part-") and name.endswith(".md"):
        return "split_part"
    return "split_auxiliary_markdown"


def is_under_ignored_dir(path: Path, repo_root: Path) -> bool:
    parts = path.resolve().relative_to(repo_root.resolve()).parts
    return any(part in IGNORED_DIR_NAMES for part in parts)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig", errors="replace")


def first_heading(text: str) -> str | None:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or None
    return None


def is_github_template(rel_path: str) -> bool:
    return rel_path in GITHUB_TEMPLATE_FILES or any(
        rel_path.startswith(prefix) for prefix in GITHUB_TEMPLATE_PREFIXES
    )


def classify_markdown(rel_path: str, role: str) -> str:
    split_categories = {
        "split_index": "markdown_split_index",
        "split_part": "markdown_split_part",
        "split_auxiliary_markdown": "markdown_split_auxiliary",
    }
    if role in split_categories:
        return split_categories[role]
    if rel_path in ROOT_POLICY_DOCS:
        return "root_policy_or_entrypoint"
    if rel_path in ROOT_COMMUNITY_DOCS:
        return "root_community_doc"
    if is_github_template(rel_path):
        return "github_template"
    if rel_path == ".aider.chat.history.md":
        return "local_tool_history"
    if rel_path.startswith(EVIDENCE_PREFIX):
        return "compact_evidence"
    if rel_path.startswith(TASK_PREFIX):
        return "local_ai_task_entrypoint"
    if rel_path.startswith(EXECUTION_PLAN_PREFIX):
        return "execution_plan"
    if rel_path in GENERATED_NPU_DOCS or any(
        rel_path.startswith(prefix) for prefix in GENERATED_INDEX_PREFIXES
    ):
        return "generated_or_index_context"
    if rel_path.endswith("/README.md") and rel_path.startswith("Tools/"):
        return "tool_readme"
    if rel_path.startswith("Tools/npu/"):
        return "npu_tool_context_doc"
    if rel_path.startswith("Scripting/"):
        return "blender_application_doc"
    if rel_path.startswith("docs/"):
        return "stable_project_doc"
    if rel_path.startswith("Tools/"):
        return "tool_or_runtime_doc"
    return "misc_markdown"


def lifecycle_for(category: str, rel_path: str) -> str:
    if rel_path in {
        "AGENTS.md",
        "README.md",
        "WORKFLOW.md",
        "docs/README.md",
        "docs/LOCAL_AI_TASKS/README.md",
    }:
        return "canonical_entrypoint"
    if category.startswith("markdown_split_"):
        return "split_container_member"
    if category in {"root_community_doc", "github_template"}:
        return "repository_community_control"
    if category == "local_tool_history":
        return "local_history_delete_candidate"
    if category == "compact_evidence":
        return "evidence_snapshot"
    if category == "local_ai_task_entrypoint":
        return "current_or_historical_task"
    if category == "execution_plan":
        return "state_record"
    if category == "generated_or_index_context":
        return "generated_context"
    if category == "npu_tool_context_doc":
        return "tool_context_review"
    if category in {"stable_project_doc", "root_policy_or_entrypoint", "tool_readme"}:
        return "maintained_source_doc"
    return "review_needed"


def build_index_text(repo_root: Path) -> dict[str, str]:
    texts: dict[str, str] = {}
    for rel in CANONICAL_INDEX_FILES:
        path = repo_root / rel
        if path.exists() and path.is_file():
            texts[rel] = read_text(path)
        elif path.exists() and path.is_dir():
            index = path / "README.md"
            if index.exists() and index.is_file():
                texts[f"{rel}/README.md"] = read_text(index)
    return texts


def indexed_by(rel_path: str, index_texts: dict[str, str]) -> list[str]:
    hits: list[str] = []
    basename = Path(rel_path).name
    container = rel_path.split(".md/", 1)[0] + ".md" if ".md/" in rel_path else ""
    for index_path, text in index_texts.items():
        if rel_path in text or f"`{rel_path}`" in text or basename in text:
            hits.append(index_path)
        elif container and container in text:
            hits.append(index_path)
    return hits


def collect_markdown(repo_root: Path) -> list[Path]:
    files = [
        path
        for path in repo_root.rglob("*.md")
        if path.is_file() and not is_under_ignored_dir(path, repo_root)
    ]
    return sorted(files, key=lambda item: repo_relative(item, repo_root).lower())


def collect_split_containers(repo_root: Path) -> list[str]:
    containers = [
        repo_relative(path, repo_root)
        for path in repo_root.rglob("*.md")
        if path.is_dir() and not is_under_ignored_dir(path, repo_root)
    ]
    return sorted(set(containers))


def is_prune_candidate(category: str, lifecycle: str, index_hits: list[str]) -> bool:
    if category.startswith("markdown_split_") or index_hits:
        return False
    return lifecycle == "local_history_delete_candidate" or category == "misc_markdown"


def requires_index_review(category: str, index_hits: list[str]) -> bool:
    if category.startswith("markdown_split_") or index_hits:
        return False
    return category in {
        "stable_project_doc",
        "tool_readme",
        "local_ai_task_entrypoint",
        "npu_tool_context_doc",
    }


def inventory_item(path: Path, repo_root: Path, index_texts: dict[str, str]) -> dict[str, Any]:
    rel = repo_relative(path, repo_root)
    text = read_text(path)
    role = markdown_role(path, repo_root)
    container = split_container_for(path, repo_root)
    category = classify_markdown(rel, role)
    lifecycle = lifecycle_for(category, rel)
    index_hits = indexed_by(rel, index_texts)
    return {
        "path": rel,
        "markdown_role": role,
        "split_container": container or "",
        "directory_form_md_suffix": bool(container),
        "category": category,
        "lifecycle": lifecycle,
        "heading": first_heading(text),
        "lines": len(text.splitlines()),
        "size_bytes": path.stat().st_size,
        "indexed_by": index_hits,
        "indexed": bool(index_hits) or rel in CANONICAL_INDEX_FILES,
        "prune_candidate": is_prune_candidate(category, lifecycle, index_hits),
        "requires_index_review": requires_index_review(category, index_hits),
    }


def count_by(items: list[dict[str, Any]], key: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for item in items:
        counts[item[key]] = counts.get(item[key], 0) + 1
    return counts


def build_report(repo_root: Path) -> dict[str, Any]:
    index_texts = build_index_text(repo_root)
    split_containers = collect_split_containers(repo_root)
    items = [inventory_item(path, repo_root, index_texts) for path in collect_markdown(repo_root)]
    missing_index = [item for item in items if item["requires_index_review"]]
    prune_candidates = [item for item in items if item["prune_candidate"]]
    return {
        "schema_version": 1,
        "kind": "markdown_inventory",
        "repo_root": str(repo_root),
        "passed": True,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "markdown_count": len(items),
        "split_container_count": len(split_containers),
        "split_containers": split_containers,
        "split_markdown_file_count": sum(1 for item in items if item["directory_form_md_suffix"]),
        "indexed_source_files": sorted(index_texts),
        "category_counts": count_by(items, "category"),
        "lifecycle_counts": count_by(items, "lifecycle"),
        "markdown_role_counts": count_by(items, "markdown_role"),
        "missing_index_count": len(missing_index),
        "prune_candidate_count": len(prune_candidates),
        "missing_index": missing_index,
        "prune_candidates": prune_candidates,
        "items": items,
        "errors": [],
        "warnings": [
            "This inventory is evidence for review. It does not delete or rewrite Markdown files.",
            "Directory-form Markdown split containers are represented by their README/part files.",
            "A missing index reference is not automatically obsolete; it means the file needs owner/lifecycle review.",
            "GitHub templates and root community docs are repository controls, not prune candidates.",
        ],
    }


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Build a report-only Markdown documentation inventory."
    )
    parser.add_argument("--repo-root", default=".", help="Repository root.")
    parser.add_argument(
        "--output", default="output/validation/markdown_inventory.json", help="JSON report output."
    )
    parser.add_argument("--markdown-output", default=None, help="Optional Markdown report output.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    write_json(Path(args.output), report)
    if args.markdown_output:
        write_text(Path(args.markdown_output), render_markdown(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
