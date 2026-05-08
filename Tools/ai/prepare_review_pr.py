#!/usr/bin/env python3
"""Prepare a GitHub review PR from an explicit/full-run staging allowlist."""
from __future__ import annotations
import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Any
from Tools.ai.patch_suggestion_bundle.git_branch import create_review_branch, validate_branch_name
from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report
FORBIDDEN_PREFIXES = (
    "output/",
    "indexAI/code_chunks/",
    "indexAI/project_code_chunks/",
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
        return None, {"path": raw, "exists": False, "json_ok": False, "error": "outside repository"}
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
def discover_auto_include_paths(repo_root: Path, reports: list[str]) -> tuple[list[str], list[dict[str, Any]], list[str], list[str]]:
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
            if isinstance(item, dict) and item.get("ok") is not False and (item.get("changed") or item.get("applied")):
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
    return [line.strip().replace("\\", "/") for line in str(result["stdout"]).splitlines() if line.strip()]
def stage_paths(repo_root: Path, paths: list[str]) -> dict[str, Any]:
    if not paths:
        return {"requested": False, "ok": True, "commands": [], "staged_files": []}
    result = git(repo_root, ["add", "--", *paths])
    return {"requested": True, "ok": bool(result["ok"]), "commands": [result], "staged_files": staged_files(repo_root)}
def reject_forbidden_staged(paths: list[str], include_paths: list[str]) -> list[str]:
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
    if not staged_files(repo_root):
        return {"requested": False, "committed": False, "head": "", "commands": []}
    commit = git(repo_root, ["commit", "-m", message])
    head = git(repo_root, ["rev-parse", "HEAD"]) if commit["ok"] else {"stdout": ""}
    return {"requested": True, "committed": bool(commit["ok"]), "head": str(head.get("stdout") or "").strip(), "commands": [commit, head]}
def default_pr_body(args: argparse.Namespace, report_path: str) -> str:
    return "\n".join(
        [
            "## Full Run Review PR",
            "",
            f"- Stamp: `{args.Stamp}`",
            f"- Task file: `{args.task_file}`",
            f"- Branch: `{args.branch}`",
            f"- Base: `{args.base}`",
            f"- Product: patch suggestion final phase + review evidence",
            f"- Evidence report: `{report_path}`",
            "",
            "Guardrails: no merge to master, no force-push, no output/** commit, no DB/render commit.",
        ]
    ) + "\n"
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
        f"- PR URL: {report.get('github_pr_url') or ''}",
        f"- Product commit: `{report.get('product_commit') or ''}`",
        f"- Auto include from apply report: {report.get('auto_include_from_apply_report')}",
        f"- Evidence report committed: {report.get('git_evidence_commit_performed', False)}",
        "",
        "## Staged Product Paths",
        "",
    ]
    for path in report.get("include_paths") or []:
        lines.append(f"- `{path}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {item}" for item in report["errors"])
    if report.get("warnings"):
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {item}" for item in report["warnings"])
    return write_text_report("\n".join(lines) + "\n", output)
def parse_args() -> argparse.Namespace:
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
    parser.add_argument("--apply-report", action="append", default=[])
    parser.add_argument("--auto-include-from-apply-report", action="store_true")
    parser.add_argument("--output", default="output/validation/review_pr_prepare.json")
    parser.add_argument("--markdown-output", default="")
    parser.add_argument("--evidence-output", default="")
    parser.add_argument("--evidence-markdown-output", default="")
    parser.add_argument("--allowed-branch-prefix", action="append", default=["CARMINEai/"])
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--create-pr", action="store_true")
    parser.add_argument("--allow-dirty-branch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()
def main() -> int:
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
    if args.base not in {"master", "main"}:
        errors.append("review PR base must be master or main")
    auto_include_paths: list[str] = []
    apply_report_infos: list[dict[str, Any]] = []
    if args.auto_include_from_apply_report:
        if not args.apply_report:
            errors.append("--auto-include-from-apply-report requires at least one --apply-report")
        else:
            auto_include_paths, apply_report_infos, auto_errors, auto_warnings = discover_auto_include_paths(repo_root, args.apply_report)
            errors.extend(auto_errors)
            warnings.extend(auto_warnings)
            if not auto_include_paths and not args.include_path:
                errors.append("no safe product include paths discovered from apply reports")
            elif not auto_include_paths:
                warnings.append("no product include paths discovered from apply reports; using explicit include paths only")
    include_paths, include_errors = normalize_include_paths(repo_root, args.include_path + auto_include_paths)
    errors.extend(include_errors)
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
    evidence_commit: dict[str, Any] = {"committed": False, "head": ""}
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
            command = ["gh", "pr", "create", "--repo", remote_repo_name(repo_root, args.remote), "--base", base_branch, "--head", args.branch, "--title", args.title, "--body-file", str(body_file)]
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
        "manual_include_paths": args.include_path,
        "auto_include_from_apply_report": bool(args.auto_include_from_apply_report),
        "auto_include_paths": auto_include_paths,
        "apply_reports": apply_report_infos,
        "provider_execution_performed": False,
        "blender_execution_performed": False,
        "ffmpeg_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "git_branch_created": bool(branch_prepare.get("created")),
        "git_commit_performed": bool(product_commit.get("committed")),
        "git_push_performed": bool(push_result.get("ok")),
        "github_pr_created": bool(pr_result.get("ok")),
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
