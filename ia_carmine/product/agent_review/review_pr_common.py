"""Shared helpers for review PR preparation."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path
from typing import Any

from Tools.validation._shared.report_utils import write_text_report

FORBIDDEN_PREFIXES = (
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
    "docs/LOCAL_VALIDATION_EVIDENCE/",
    "renders/",
)
FORBIDDEN_SUFFIXES = (".db", ".sqlite", ".sqlite3")
AUTO_TARGET_KEYS = ("path", "target", "target_file", "file", "file_path", "written_path")
AUTO_TARGET_LIST_KEYS = ("target_files", "paths", "files", "written_paths")
AUTO_PRODUCT_SECTIONS = (
    "manual_review_product",
    "essential_patch_suggestion_items",
    "product_facing_manual_review_items",
)

def run_command(repo_root: Path, command: list[str]) -> dict[str, Any]:
    result = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip()[:4000],
        "stderr": result.stderr.strip()[:4000],
        "ok": result.returncode == 0,
    }

def git(repo_root: Path, args: list[str]) -> dict[str, Any]:
    return run_command(repo_root, ["git", *args])

def normalize_repo_path(repo_root: Path, raw: str) -> tuple[str, str | None]:
    if not raw.strip():
        return "", "empty include path"
    candidate = Path(raw)
    full = candidate if candidate.is_absolute() else repo_root / candidate
    try:
        resolved = full.resolve()
        relative = resolved.relative_to(repo_root.resolve())
    except ValueError:
        return "", "include path is outside the repository"
    normalized = relative.as_posix().lstrip("./")
    if not normalized or normalized == ".":
        return "", "repository root cannot be staged as an include path"
    if normalized.startswith(".git/") or normalized == ".git":
        return "", ".git cannot be staged"
    if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
        return "", f"forbidden generated/runtime path: {normalized}"
    if normalized.lower().endswith(FORBIDDEN_SUFFIXES):
        return "", f"forbidden database/runtime artifact: {normalized}"
    if not resolved.exists():
        return "", f"include path does not exist: {normalized}"
    return normalized, None

def normalize_include_paths(repo_root: Path, raw_paths: list[str]) -> tuple[list[str], list[str]]:
    paths: list[str] = []
    errors: list[str] = []
    for raw in raw_paths:
        path, error = normalize_repo_path(repo_root, raw)
        if error:
            errors.append(f"{raw}: {error}")
        elif path not in paths:
            paths.append(path)
    return paths, errors

def load_report(repo_root: Path, raw: str) -> tuple[dict[str, Any] | None, dict[str, Any]]:
    candidate = Path(raw)
    full = candidate if candidate.is_absolute() else repo_root / candidate
    try:
        path = full.resolve()
        rel = path.relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return None, {
            "path": raw,
            "exists": False,
            "json_ok": False,
            "error": "outside repository",
        }
    info: dict[str, Any] = {"path": rel, "exists": path.exists(), "json_ok": False}
    if not path.is_file():
        info["error"] = "report does not exist or is not a file"
        return None, info
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001
        info["error"] = f"{type(exc).__name__}: {exc}"
        return None, info
    if not isinstance(data, dict):
        info["error"] = "report root must be a JSON object"
        return None, info
    info.update(
        {
            "json_ok": True,
            "kind": data.get("kind"),
            "passed": data.get("passed"),
            "apply_requested": data.get("apply_requested"),
            "patch_application_performed": data.get("patch_application_performed"),
            "source_writes_performed": data.get("source_writes_performed"),
        }
    )
    return data, info

def path_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for entry in value for item in path_values(entry)]
    if isinstance(value, dict):
        found: list[str] = []
        for key in AUTO_TARGET_KEYS + AUTO_TARGET_LIST_KEYS:
            found.extend(path_values(value.get(key)))
        for nested in value.values():
            if isinstance(nested, (dict, list)):
                found.extend(path_values(nested))
        return found
    return []

def discover_auto_include_paths(
    repo_root: Path, reports: list[str]
) -> tuple[list[str], list[dict[str, Any]], list[str], list[str]]:
    paths: list[str] = []
    infos: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    for raw in reports:
        data, info = load_report(repo_root, raw)
        infos.append(info)
        if data is None:
            errors.append(f"{raw}: {info.get('error')}")
            continue
        if data.get("kind") != "patch_suggestion_bundle_apply":
            warnings.append(f"{info.get('path')}: unexpected report kind {data.get('kind')!r}")
        for item in data.get("results") or []:
            if (
                isinstance(item, dict)
                and item.get("ok") is not False
                and (item.get("changed") or item.get("applied"))
            ):
                paths.extend(path_values(item.get("path")))
        for key in AUTO_PRODUCT_SECTIONS:
            paths.extend(path_values(data.get(key)))
    include_paths: list[str] = []
    for raw in paths:
        path, error = normalize_repo_path(repo_root, raw)
        if not error and path not in include_paths:
            include_paths.append(path)
    return include_paths, infos, errors, warnings

def remote_repo_name(repo_root: Path, remote: str) -> str:
    result = git(repo_root, ["remote", "get-url", remote])
    if not result["ok"]:
        return ""
    url = str(result["stdout"]).strip()
    if url.endswith(".git"):
        url = url[:-4]
    if url.startswith("git@github.com:"):
        return url.split(":", 1)[1]
    marker = "github.com/"
    if marker in url:
        return url.split(marker, 1)[1]
    return ""

def staged_files(repo_root: Path) -> list[str]:
    result = git(repo_root, ["diff", "--cached", "--name-only"])
    if not result["ok"]:
        return []
    return [
        line.strip().replace("\\", "/")
        for line in str(result["stdout"]).splitlines()
        if line.strip()
    ]

def stage_paths(repo_root: Path, paths: list[str]) -> dict[str, Any]:
    if not paths:
        return {"requested": False, "ok": True, "commands": [], "staged_files": []}
    result = git(repo_root, ["add", "--", *paths])
    return {
        "requested": True,
        "ok": bool(result["ok"]),
        "commands": [result],
        "staged_files": staged_files(repo_root),
    }

def reject_forbidden_staged(paths: list[str], include_paths: list[str]) -> list[str]:
    errors: list[str] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        allowed = any(
            normalized == item or normalized.startswith(item.rstrip("/") + "/")
            for item in include_paths
        )
        if not allowed:
            errors.append(f"staged path outside allowlist: {normalized}")
        if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            errors.append(f"forbidden staged path: {normalized}")
        if normalized.lower().endswith(FORBIDDEN_SUFFIXES):
            errors.append(f"forbidden staged database artifact: {normalized}")
    return errors

def create_commit(repo_root: Path, message: str) -> dict[str, Any]:
    if not staged_files(repo_root):
        return {"requested": False, "committed": False, "head": "", "commands": []}
    commit = git(repo_root, ["commit", "-m", message])
    head = git(repo_root, ["rev-parse", "HEAD"]) if commit["ok"] else {"stdout": ""}
    return {
        "requested": True,
        "committed": bool(commit["ok"]),
        "head": str(head.get("stdout") or "").strip(),
        "commands": [commit, head],
    }

def default_pr_body(args: argparse.Namespace, report_path: str) -> str:
    return (
        "## Full Run Review PR\n\n"
        f"- Stamp: `{args.Stamp}`\n- Task file: `{args.task_file}`\n- Branch: `{args.branch}`\n"
        f"- Base: `{args.base}`\n- Draft requested: `{bool(args.draft_pr)}`\n"
        f"- Product: patch suggestion final phase + review evidence\n- Evidence report: `{report_path}`\n\n"
        "Guardrails: no merge to master, no force-push, no output/** commit, no DB/render commit.\n"
    )

def write_markdown(report: dict[str, Any], output: Path) -> str:
    lines = [
        "# Review PR Preparation",
        "",
        f"- Passed: {report.get('passed')}",
        f"- Branch: `{report.get('branch')}`",
        f"- Base: `{report.get('base_branch')}`",
        f"- Commit performed: {report.get('git_commit_performed')}",
        f"- Push performed: {report.get('git_push_performed')}",
        f"- PR created: {report.get('github_pr_created')}",
        f"- PR draft requested: {report.get('github_pr_draft_requested')}",
        f"- PR URL: {report.get('github_pr_url') or ''}",
        f"- Product commit: `{report.get('product_commit') or ''}`",
        f"- Auto include from apply report: {report.get('auto_include_from_apply_report')}",
        "",
        "## Staged Product Paths",
        "",
    ]
    lines.extend(f"- `{path}`" for path in (report.get("include_paths") or []))
    for title, key in (("Errors", "errors"), ("Warnings", "warnings")):
        if report.get(key):
            lines.extend(["", f"## {title}", "", *[f"- {item}" for item in report[key]]])
    return write_text_report("\n".join(lines) + "\n", output)
