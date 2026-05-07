#!/usr/bin/env python3
"""Prepare a GitHub review PR from a full-run patch-suggestion product."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any

from Tools.ai.patch_suggestion_bundle.common import compact_artifact_stamp
from Tools.ai.patch_suggestion_bundle.git_branch import create_review_branch, validate_branch_name
from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report


FORBIDDEN_PREFIXES = ("output/", "indexAI/code_chunks/", "indexAI/project_code_chunks/", "renders/")
FORBIDDEN_SUFFIXES = (".db", ".sqlite", ".sqlite3")
DEFAULT_APPLY_REPORT_GLOBS = (
    "output/validation/patch_suggestion_bundle_apply*{stamp}*.json",
    "output/validation/patch_suggestion_bundle_apply.json",
)


def run_command(repo_root: Path, command: list[str]) -> dict[str, Any]:
    """Run a command and return a compact result."""
    result = subprocess.run(command, cwd=repo_root, check=False, capture_output=True, text=True)
    return {
        "command": command,
        "returncode": result.returncode,
        "stdout": result.stdout.strip()[:4000],
        "stderr": result.stderr.strip()[:4000],
        "ok": result.returncode == 0,
    }


def git(repo_root: Path, args: list[str]) -> dict[str, Any]:
    """Run git with no shell interpolation."""
    return run_command(repo_root, ["git", *args])


def repo_relative(repo_root: Path, path: Path) -> str:
    """Return repo-relative path when possible."""
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.as_posix()


def load_json_object(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    """Read a JSON object report."""
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # noqa: BLE001 - report exact validation failure.
        return None, f"{type(exc).__name__}: {exc}"
    if not isinstance(data, dict):
        return None, "JSON root is not an object"
    return data, None


def split_csv_values(values: list[str]) -> list[str]:
    """Split repeatable/comma-separated path values."""
    out: list[str] = []
    for value in values:
        for item in str(value).split(","):
            cleaned = item.strip().strip("'\"")
            if cleaned and cleaned not in out:
                out.append(cleaned)
    return out


def normalize_repo_path(repo_root: Path, raw: str) -> tuple[str, str | None]:
    """Normalize a path and reject paths outside the repo or generated runtime areas."""
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
    """Return unique safe repo-relative include paths."""
    paths: list[str] = []
    errors: list[str] = []
    for raw in raw_paths:
        path, error = normalize_repo_path(repo_root, raw)
        if error:
            errors.append(f"{raw}: {error}")
        elif path not in paths:
            paths.append(path)
    return paths, errors


def remote_repo_name(repo_root: Path, remote: str) -> str:
    """Resolve owner/name from the configured remote URL when possible."""
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
    """Return currently staged paths."""
    result = git(repo_root, ["diff", "--cached", "--name-only"])
    if not result["ok"]:
        return []
    return [line.strip().replace("\\", "/") for line in str(result["stdout"]).splitlines() if line.strip()]


def stage_paths(repo_root: Path, paths: list[str]) -> dict[str, Any]:
    """Stage exact allowlisted paths."""
    if not paths:
        return {"requested": False, "ok": True, "commands": [], "staged_files": []}
    result = git(repo_root, ["add", "--", *paths])
    return {"requested": True, "ok": bool(result["ok"]), "commands": [result], "staged_files": staged_files(repo_root)}


def reject_forbidden_staged(paths: list[str], include_paths: list[str]) -> list[str]:
    """Find staged paths outside the allowlist or forbidden policy."""
    errors: list[str] = []
    for path in paths:
        normalized = path.replace("\\", "/")
        allowed = any(normalized == item or normalized.startswith(item.rstrip("/") + "/") for item in include_paths)
        if not allowed:
            errors.append(f"staged path outside allowlist: {normalized}")
        if any(normalized.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            errors.append(f"forbidden staged path: {normalized}")
        if normalized.lower().endswith(FORBIDDEN_SUFFIXES):
            errors.append(f"forbidden staged database artifact: {normalized}")
    return errors


def create_commit(repo_root: Path, message: str) -> dict[str, Any]:
    """Commit staged changes and return the resulting HEAD."""
    if not staged_files(repo_root):
        return {"requested": False, "committed": False, "head": "", "commands": []}
    commit = git(repo_root, ["commit", "-m", message])
    head = git(repo_root, ["rev-parse", "HEAD"]) if commit["ok"] else {"stdout": ""}
    return {"requested": True, "committed": bool(commit["ok"]), "head": str(head.get("stdout") or "").strip(), "commands": [commit, head]}


def discover_apply_reports(repo_root: Path, stamp: str) -> list[Path]:
    """Find patch_suggestion_bundle_apply reports for a run stamp."""
    artifact_stamp = compact_artifact_stamp(stamp) if stamp else ""
    candidates: list[Path] = []
    for pattern in DEFAULT_APPLY_REPORT_GLOBS:
        rendered = pattern.format(stamp=artifact_stamp or stamp)
        candidates.extend(sorted(repo_root.glob(rendered)))
    out: list[Path] = []
    seen: set[str] = set()
    for path in candidates:
        key = path.resolve().as_posix()
        if key not in seen and path.is_file():
            seen.add(key)
            out.append(path)
    return out


def paths_from_apply_report(data: dict[str, Any]) -> list[str]:
    """Return paths actually changed/applied by patch_suggestion_bundle_apply."""
    if data.get("kind") != "patch_suggestion_bundle_apply":
        return []
    if data.get("apply_requested") is not True:
        return []
    results = data.get("results") if isinstance(data.get("results"), list) else []
    paths: list[str] = []
    for item in results:
        if not isinstance(item, dict) or item.get("ok") is not True:
            continue
        if item.get("applied") is True or item.get("changed") is True:
            path = str(item.get("path") or "").replace("\\", "/").strip()
            if path and path not in paths:
                paths.append(path)
    return paths


def auto_include_from_apply_reports(repo_root: Path, args: argparse.Namespace) -> tuple[list[str], list[dict[str, Any]], list[str]]:
    """Collect include paths from explicit or discovered apply reports."""
    raw_reports = split_csv_values(list(args.include_from_apply_report or []))
    reports = [(repo_root / item).resolve() if not Path(item).is_absolute() else Path(item).resolve() for item in raw_reports]
    if not reports and not args.no_auto_include_from_apply_report:
        reports = discover_apply_reports(repo_root, args.Stamp)
    paths: list[str] = []
    items: list[dict[str, Any]] = []
    warnings: list[str] = []
    for report in reports:
        data, error = load_json_object(report)
        rel = repo_relative(repo_root, report)
        item: dict[str, Any] = {"path": rel, "exists": report.exists(), "json_ok": error is None, "error": error, "paths": []}
        if error:
            warnings.append(f"unable to read apply report {rel}: {error}")
        elif data is not None:
            report_paths = paths_from_apply_report(data)
            item.update({"kind": data.get("kind"), "passed": data.get("passed"), "apply_requested": data.get("apply_requested"), "applied_count": data.get("applied_count"), "changed_count": data.get("changed_count"), "paths": report_paths})
            for path in report_paths:
                if path not in paths:
                    paths.append(path)
        items.append(item)
    return paths, items, warnings


def default_pr_body(args: argparse.Namespace, report_path: str) -> str:
    """Build a compact PR body for manual review."""
    return "\n".join([
        "## Full Run Review PR",
        "",
        f"- Stamp: `{args.Stamp}`",
        f"- Task file: `{args.task_file}`",
        f"- Branch: `{args.branch}`",
        f"- Base: `{args.base}`",
        "- Product: task Markdown -> deterministic patch apply -> review PR",
        f"- Evidence report: `{report_path}`",
        f"- Draft PR: `{not args.ready_for_review}`",
        "",
        "Guardrails: no merge to master, no force-push, no output/** commit, no DB/render commit.",
    ]) + "\n"


def write_markdown(report: dict[str, Any], output: Path) -> str:
    """Write a compact Markdown companion for the review PR report."""
    lines = [
        "# Review PR Preparation",
        "",
        f"- Passed: {report.get('passed')}",
        f"- Branch: `{report.get('branch')}`",
        f"- Base: `{report.get('base_branch')}`",
        f"- Commit performed: {report.get('git_commit_performed')}",
        f"- Push performed: {report.get('git_push_performed')}",
        f"- PR created: {report.get('github_pr_created')}",
        f"- Draft PR requested: {report.get('github_pr_draft_requested')}",
        f"- PR URL: {report.get('github_pr_url') or ''}",
        f"- Product commit: `{report.get('product_commit') or ''}`",
        f"- Evidence report committed: {report.get('git_evidence_commit_performed', False)}",
        "",
        "## Staged Product Paths",
        "",
    ]
    lines.extend(f"- `{path}`" for path in report.get("include_paths") or [])
    if report.get("auto_include_paths"):
        lines.extend(["", "## Auto-detected Paths", ""])
        lines.extend(f"- `{path}`" for path in report.get("auto_include_paths") or [])
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--Stamp", default="")
    parser.add_argument("--task-file", default="")
    parser.add_argument("--branch", required=True)
    parser.add_argument("--base", default="master")
    parser.add_argument("--remote", default="origin")
    parser.add_argument("--title", required=True)
    parser.add_argument("--body", default="")
    parser.add_argument("--body-file", default="")
    parser.add_argument("--commit-message", required=True)
    parser.add_argument("--include-path", action="append", default=[])
    parser.add_argument("--include-from-apply-report", action="append", default=[])
    parser.add_argument("--no-auto-include-from-apply-report", action="store_true")
    parser.add_argument("--output", default="output/validation/review_pr_prepare.json")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--evidence-output", default="")
    parser.add_argument("--evidence-markdown-output", default="")
    parser.add_argument("--allowed-branch-prefix", action="append", default=["CARMINEai/"])
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--create-pr", action="store_true")
    parser.add_argument("--ready-for-review", action="store_true", help="Create a non-draft PR. Default is draft.")
    parser.add_argument("--allow-dirty-branch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    """CLI entrypoint."""
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output = resolve_output_path(repo_root, args.output)
    md_output = resolve_output_path(repo_root, args.markdown_output) if args.markdown_output else None
    evidence_output = resolve_output_path(repo_root, args.evidence_output) if args.evidence_output else None
    evidence_md = resolve_output_path(repo_root, args.evidence_markdown_output) if args.evidence_markdown_output else None
    errors: list[str] = []
    warnings: list[str] = []
    commands: list[dict[str, Any]] = []

    ok, reason = validate_branch_name(args.branch, list(args.allowed_branch_prefix))
    if not ok:
        errors.append(str(reason))
    base_branch = args.base
    if base_branch not in {"master", "main"}:
        errors.append("review PR base must be master or main")

    explicit_paths = split_csv_values(list(args.include_path or []))
    auto_paths, auto_reports, auto_warnings = auto_include_from_apply_reports(repo_root, args)
    warnings.extend(auto_warnings)
    include_paths, include_errors = normalize_include_paths(repo_root, [*explicit_paths, *auto_paths])
    errors.extend(include_errors)
    if not include_paths and not args.dry_run:
        warnings.append("no include paths resolved from CLI or patch_suggestion_bundle_apply reports")

    if args.dry_run:
        branch_prepare = {"requested": bool(args.branch), "branch": args.branch, "created": False, "switched": False, "dry_run": True, "errors": [], "warnings": []}
    else:
        branch_prepare = create_review_branch(repo_root, args.branch, allowed_prefixes=list(args.allowed_branch_prefix), allow_dirty=bool(args.allow_dirty_branch))
    errors.extend(branch_prepare.get("errors") or [])
    warnings.extend(branch_prepare.get("warnings") or [])

    stage_result: dict[str, Any] = {"requested": False, "ok": False, "staged_files": []}
    product_commit: dict[str, Any] = {"committed": False, "head": ""}
    push_result: dict[str, Any] = {"requested": False, "ok": False}
    pr_result: dict[str, Any] = {"requested": False, "ok": False, "url": ""}

    if not errors and not args.dry_run:
        stage_result = stage_paths(repo_root, include_paths)
        commands.extend(stage_result.get("commands") or [])
        if not stage_result.get("ok"):
            errors.append("git add failed for review PR include paths")
        staged = stage_result.get("staged_files") or []
        errors.extend(reject_forbidden_staged(staged, include_paths))
        if not staged:
            errors.append("no staged product changes found for review PR")
        if not errors:
            product_commit = create_commit(repo_root, args.commit_message)
            commands.extend(product_commit.get("commands") or [])
            if not product_commit.get("committed"):
                errors.append("product commit failed")
        if args.push and not errors:
            push_result = git(repo_root, ["push", "-u", args.remote, args.branch])
            commands.append(push_result)
            if not push_result["ok"]:
                errors.append("git push failed")
        if args.create_pr and args.push and not errors:
            body = args.body
            if args.body_file:
                body = Path(args.body_file).read_text(encoding="utf-8")
            if not body:
                body = default_pr_body(args, str(evidence_output or output))
            body_file = output.with_suffix(".body.md")
            body_file.parent.mkdir(parents=True, exist_ok=True)
            body_file.write_text(body, encoding="utf-8")
            repo_name = remote_repo_name(repo_root, args.remote)
            command = ["gh", "pr", "create", "--repo", repo_name, "--base", base_branch, "--head", args.branch, "--title", args.title, "--body-file", str(body_file)]
            if not args.ready_for_review:
                command.append("--draft")
            pr_result = run_command(repo_root, command)
            commands.append(pr_result)
            if pr_result["ok"]:
                pr_result["url"] = str(pr_result["stdout"]).splitlines()[-1].strip()
            else:
                errors.append("gh pr create failed")

    report = {
        "schema_version": 1,
        "kind": "review_pr_prepare",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "Stamp": args.Stamp,
        "task_file": args.task_file.replace("\\", "/"),
        "branch": args.branch,
        "base_branch": base_branch,
        "include_paths": include_paths,
        "explicit_include_paths": explicit_paths,
        "auto_include_paths": auto_paths,
        "auto_include_reports": auto_reports,
        "provider_execution_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_branch_created": bool(branch_prepare.get("created")),
        "git_commit_performed": bool(product_commit.get("committed")),
        "git_push_performed": bool(push_result.get("ok")),
        "github_pr_created": bool(pr_result.get("ok")),
        "github_pr_draft_requested": bool(args.create_pr and not args.ready_for_review),
        "github_pr_url": pr_result.get("url") or "",
        "product_commit": product_commit.get("head") or "",
        "evidence_commit": "",
        "branch_prepare": branch_prepare,
        "stage_result": stage_result,
        "push_result": push_result,
        "pr_result": pr_result,
        "commands": commands,
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
    }

    if evidence_output and not args.dry_run and not errors:
        write_json_report(report, evidence_output)
        if evidence_md:
            write_markdown(report, evidence_md)
        evidence_paths = [evidence_output.relative_to(repo_root).as_posix()]
        if evidence_md:
            evidence_paths.append(evidence_md.relative_to(repo_root).as_posix())
        evidence_stage = stage_paths(repo_root, evidence_paths)
        report["evidence_stage_result"] = evidence_stage
        if not evidence_stage.get("ok"):
            report.setdefault("errors", []).append("review PR evidence stage failed")
        evidence_commit = create_commit(repo_root, f"docs(ai): add review PR evidence {args.Stamp}".strip())
        report["evidence_commit"] = evidence_commit.get("head") or ""
        report["git_evidence_commit_performed"] = bool(evidence_commit.get("committed"))
        if not evidence_commit.get("committed"):
            report.setdefault("errors", []).append("review PR evidence commit failed")
        if args.push and evidence_commit.get("committed"):
            second_push = git(repo_root, ["push", args.remote, args.branch])
            report["evidence_push_result"] = second_push
            report["git_push_performed"] = bool(second_push.get("ok"))
            if not second_push.get("ok"):
                report.setdefault("errors", []).append("review PR evidence push failed")

    report["passed"] = not report.get("errors")
    write_json_report(report, output)
    if md_output:
        write_markdown(report, md_output)
    print(write_json_report(report), end="")
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
