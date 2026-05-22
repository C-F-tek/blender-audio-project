"""CLI for review PR preparation."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
from typing import Any

from ia_carmine.product.patch_product.patch_suggestion_bundle.git_branch import create_review_branch, validate_branch_name
from Tools.validation._shared.report_utils import resolve_output_path, write_json_report

from .review_pr_common import (
    create_commit,
    default_pr_body,
    discover_auto_include_paths,
    git,
    normalize_include_paths,
    reject_forbidden_staged,
    remote_repo_name,
    run_command,
    stage_paths,
    write_markdown,
)

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
    parser.add_argument(
        "--allowed-branch-prefix", action="append", default=["CARMINEai/", "codex/"]
    )
    parser.add_argument("--push", action="store_true")
    parser.add_argument("--create-pr", action="store_true")
    parser.add_argument("--draft-pr", action="store_true")
    parser.add_argument("--allow-dirty-branch", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()

def validate_pr_flags(args: argparse.Namespace) -> list[str]:
    errors: list[str] = []
    if args.create_pr and not args.push:
        errors.append("--create-pr requires --push so the requested branch exists on the remote")
    if args.draft_pr and not args.create_pr:
        errors.append("--draft-pr requires --create-pr")
    return errors

def create_github_pr(
    repo_root: Path, args: argparse.Namespace, body: str, body_file: Path
) -> dict[str, Any]:
    body_file.parent.mkdir(parents=True, exist_ok=True)
    body_file.write_text(body, encoding="utf-8")
    command = [
        "gh",
        "pr",
        "create",
        "--repo",
        remote_repo_name(repo_root, args.remote),
        "--base",
        args.base,
        "--head",
        args.branch,
        "--title",
        args.title,
        "--body-file",
        str(body_file),
    ]
    if args.draft_pr:
        command.append("--draft")
    result = run_command(repo_root, command)
    if result["ok"]:
        result["url"] = str(result["stdout"]).splitlines()[-1].strip()
    return result

def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve()
    output = resolve_output_path(repo_root, args.output)
    md_output = (
        resolve_output_path(repo_root, args.markdown_output) if args.markdown_output else None
    )
    evidence_output = (
        resolve_output_path(repo_root, args.evidence_output) if args.evidence_output else None
    )
    evidence_md = (
        resolve_output_path(repo_root, args.evidence_markdown_output)
        if args.evidence_markdown_output
        else None
    )
    errors: list[str] = validate_pr_flags(args)
    warnings: list[str] = []
    commands: list[dict[str, Any]] = []
    ok, reason = validate_branch_name(args.branch, list(args.allowed_branch_prefix))
    if not ok:
        errors.append(str(reason))
    if args.base not in {"master", "main"}:
        errors.append("review PR base must be master or main")
    auto_include_paths: list[str] = []
    apply_report_infos: list[dict[str, Any]] = []
    if args.auto_include_from_apply_report:
        if not args.apply_report:
            errors.append("--auto-include-from-apply-report requires at least one --apply-report")
        else:
            auto_include_paths, apply_report_infos, auto_errors, auto_warnings = (
                discover_auto_include_paths(repo_root, args.apply_report)
            )
            errors.extend(auto_errors)
            warnings.extend(auto_warnings)
            source_write_reports = [
                info
                for info in apply_report_infos
                if info.get("source_writes_performed") is True
                or info.get("patch_application_performed") is True
            ]
            if not source_write_reports and not args.include_path:
                errors.append(
                    "auto include from apply report requires at least one report with "
                    "source_writes_performed=true or patch_application_performed=true; "
                    "run deterministic suggestions with apply enabled before agent_review_prepare_pr.py"
                )
            if not auto_include_paths and not args.include_path:
                errors.append("no safe product include paths discovered from apply reports")
            elif not auto_include_paths:
                warnings.append(
                    "no product include paths discovered from apply reports; using explicit include paths only"
                )
    include_paths, include_errors = normalize_include_paths(
        repo_root, args.include_path + auto_include_paths
    )
    errors.extend(include_errors)
    if args.dry_run:
        branch_prepare = {
            "requested": bool(args.branch),
            "branch": args.branch,
            "created": False,
            "switched": False,
            "dry_run": True,
            "errors": [],
            "warnings": [],
        }
    else:
        branch_prepare = create_review_branch(
            repo_root,
            args.branch,
            allowed_prefixes=list(args.allowed_branch_prefix),
            allow_dirty=bool(args.allow_dirty_branch),
        )
    errors.extend(branch_prepare.get("errors") or [])
    warnings.extend(branch_prepare.get("warnings") or [])
    stage_result: dict[str, Any] = {"requested": False, "ok": False, "staged_files": []}
    product_commit: dict[str, Any] = {"committed": False, "head": ""}
    push_result: dict[str, Any] = {"requested": False, "ok": False}
    pr_result: dict[str, Any] = {
        "requested": bool(args.create_pr),
        "ok": False,
        "url": "",
        "draft_requested": bool(args.draft_pr),
    }
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
        if args.create_pr and not errors:
            body = args.body
            if args.body_file:
                body = Path(args.body_file).read_text(encoding="utf-8")
            if not body:
                body = default_pr_body(args, str(evidence_output or output))
            pr_result = create_github_pr(repo_root, args, body, output.with_suffix(".body.md"))
            commands.append(pr_result)
            if not pr_result["ok"]:
                errors.append("gh pr create failed")
    report = {
        "schema_version": 1,
        "kind": "review_pr_prepare",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "Stamp": args.Stamp,
        "task_file": args.task_file.replace("\\", "/"),
        "branch": args.branch,
        "base_branch": args.base,
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
        "github_pr_draft_requested": bool(args.draft_pr),
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
        evidence_commit = create_commit(
            repo_root, f"docs(ai): add review PR evidence {args.Stamp}".strip()
        )
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
