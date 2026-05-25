#!/usr/bin/env python3
"""Create artifact-owned patch candidates from verified local targets."""

from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from ia_carmine.runtime.runtime_tool.file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from ia_carmine.product.code_product.patch_candidate_report import (
        candidate_report_passed,
        report_level_errors,
        report_level_warnings,
    )
    from ia_carmine.product.patch_product.candidate_synthesis.evidence_diff import build_evidence_candidates
    from ia_carmine._shared.report_io import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[4]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.runtime.runtime_tool.file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from ia_carmine.product.code_product.patch_candidate_report import (  # type: ignore
        candidate_report_passed,
        report_level_errors,
        report_level_warnings,
    )
    from ia_carmine.product.patch_product.candidate_synthesis.evidence_diff import (  # type: ignore
        build_evidence_candidates,
    )
    from ia_carmine._shared.report_io import write_json_report, write_text_report  # type: ignore


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def resolve(repo_root: Path, value: str | Path) -> Path:
    path = Path(value)
    return path if path.is_absolute() else repo_root / path


def split_values(values: list[str] | None) -> list[str]:
    out: list[str] = []
    for value in values or []:
        for item in str(value).split(","):
            cleaned = item.strip().strip("`'\"")
            if cleaned and cleaned not in out:
                out.append(cleaned)
    return out


def read_matrix_targets(path: Path) -> list[str]:
    if not path.exists():
        return []
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return []
    targets: list[str] = []
    for key in ("verified_targets", "concrete_code_proposals"):
        for item in data.get(key) or []:
            if isinstance(item, dict) and item.get("target_file"):
                target = str(item["target_file"]).replace("\\", "/")
                if target not in targets:
                    targets.append(target)
    return targets


def git_apply_cached_check(repo_root: Path, diff_path: Path, timeout: int) -> dict[str, Any]:
    completed = subprocess.run(
        ["git", "apply", "--check", "--cached", "--ignore-whitespace", str(diff_path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": [
            "git",
            "apply",
            "--check",
            "--cached",
            "--ignore-whitespace",
            str(diff_path),
        ],
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-2000:],
        "stderr_tail": (completed.stderr or "")[-2000:],
    }


def validation_commands_for_diff(rel_path: str, diff_path: Path, cached: bool) -> list[str]:
    mode = "--cached " if cached else ""
    commands = [f"git apply --check {mode}--ignore-whitespace {diff_path}"]
    if rel_path.endswith(".py"):
        commands.append(f"python -m py_compile {rel_path}")
    commands.append("git diff --check")
    return commands


def worktree_diff(repo_root: Path, rel_path: str) -> str:
    completed = subprocess.run(
        ["git", "diff", "--", rel_path],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.stdout or ""


def build_worktree_candidate(
    repo_root: Path,
    candidate_dir: Path,
    rel_path: str,
    patched_text: str,
    candidate_index: int,
    timeout: int,
) -> dict[str, Any] | None:
    diff_text = worktree_diff(repo_root, rel_path)
    if not diff_text.strip():
        return None
    safe_name = rel_path.replace("/", "__").replace("\\", "__")
    diff_path = candidate_dir / f"{candidate_index:03d}_{safe_name}.diff"
    diff_path.write_text(diff_text, encoding="utf-8")
    check = git_apply_cached_check(repo_root, diff_path, max(30, timeout))
    semantic_check = semantic_patch_check(rel_path, patched_text)
    passed = check.get("passed") is True and semantic_check.get("passed") is True
    return {
        "target_file": rel_path,
        "reason": "validate current worktree diff captured by code execution matrix",
        "pattern_id": "validated_current_worktree_diff",
        "diff_source": "current_worktree_diagnostic",
        "evidence": [
            "target resolved against local filesystem",
            "candidate copied from current git diff for the verified target",
            "applicability checked against git index with git apply --check --cached",
        ],
        "diff_ref": str(diff_path),
        "diff_sha256": hashlib.sha256(diff_text.encode("utf-8")).hexdigest(),
        "diff_chars": len(diff_text),
        "diff_tail": diff_text[-4000:],
        "diff_path": str(diff_path),
        "validation_commands": validation_commands_for_diff(rel_path, diff_path, cached=True),
        "applicability_check": check,
        "semantic_check": semantic_check,
        "passed": passed,
        "errors": []
        if passed
        else [
            item
            for item in (
                check.get("stderr_tail"),
                *(semantic_check.get("errors") or []),
            )
            if item
        ],
        "warnings": [],
    }


def semantic_patch_check(rel_path: str, patched_text: str) -> dict[str, Any]:
    if not rel_path.endswith(".py"):
        return {"passed": True, "checks": ["non_python_skip"]}
    try:
        ast.parse(patched_text, filename=rel_path)
    except SyntaxError as exc:
        return {
            "passed": False,
            "checks": ["python_ast_parse"],
            "errors": [f"{exc.__class__.__name__}: {exc}"],
        }
    return {"passed": True, "checks": ["python_ast_parse"], "errors": []}


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    resolver = RuntimeFileRefResolver(repo_root)
    matrix_targets = read_matrix_targets(resolve(repo_root, args.matrix_report)) if args.matrix_report else []
    target_inputs = split_values(args.target_file) + matrix_targets
    refs = resolver.resolve_many(
        target_inputs,
        provenance=RuntimeRefProvenance.MATRIX_REPORT,
        consumers=(RuntimeConsumer.MATRIX, RuntimeConsumer.FINAL_ASSEMBLER),
    )
    candidate_dir = resolve(repo_root, args.candidate_dir)
    candidate_dir.mkdir(parents=True, exist_ok=True)
    candidates: list[dict[str, Any]] = []
    warnings: list[str] = []
    evidence_reports = split_values(args.evidence_report)
    if evidence_reports:
        evidence_candidates, evidence_warnings = build_evidence_candidates(
            repo_root=repo_root,
            candidate_dir=candidate_dir,
            refs=refs,
            evidence_reports=evidence_reports,
            start_index=1,
            max_candidates=max(1, int(args.max_candidates)),
            timeout=max(30, int(args.timeout_seconds)),
        )
        candidates.extend(evidence_candidates)
        warnings.extend(evidence_warnings)
    allow_worktree = bool(getattr(args, "allow_current_worktree_diff_candidates", False))
    if allow_worktree:
        for ref in refs:
            if len(candidates) >= max(1, int(args.max_candidates)):
                break
            if not ref.patchable:
                continue
            path = repo_root / ref.repo_relative
            before = path.read_text(encoding="utf-8-sig", errors="replace")
            worktree_candidate = build_worktree_candidate(
                repo_root,
                candidate_dir,
                ref.repo_relative,
                before,
                len(candidates) + 1,
                max(30, int(args.timeout_seconds)),
            )
            if worktree_candidate:
                candidates.append(worktree_candidate)
    if not candidates:
        warnings.append(
            "no validated evidence-owned unified diff matched verified targets"
            if not allow_worktree
            else "no validated evidence/worktree unified diff matched verified targets"
        )
    warnings.extend(report_level_warnings(candidates))
    return {
        "schema_version": 1,
        "kind": "patch_candidate_synthesis",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "operator_request": str(args.operator_request or ""),
        "evidence_reports": evidence_reports,
        "passed": candidate_report_passed(candidates),
        "target_ref_count": len(refs),
        "candidate_count": len(candidates),
        "patch_candidate_synthesis_passed_count": sum(1 for item in candidates if item.get("passed") is True),
        "allow_current_worktree_diff_candidates": allow_worktree,
        "current_worktree_diagnostic_candidate_count": sum(
            1 for item in candidates if item.get("diff_source") == "current_worktree_diagnostic"
        ),
        "evidence_owned_candidate_count": sum(
            1 for item in candidates if item.get("diff_source") == "evidence_owned"
        ),
        "resolved_file_refs": [item.as_dict() for item in refs],
        "candidates": candidates,
        "source_writes_performed": False,
        "patch_application_performed": False,
        "git_write_performed": False,
        "guardrails": {
            "free_shell_exposed": False,
            "artifact_owned_write": True,
            "source_writes_performed": False,
            "patch_application_performed": False,
            "git_write_performed": False,
        },
        "errors": report_level_errors(candidates),
        "warnings": warnings,
    }


def render_markdown(report: dict[str, Any]) -> str:
    lines = ["# Patch Candidate Synthesis", ""]
    for key in ("passed", "target_ref_count", "candidate_count", "patch_candidate_synthesis_passed_count"):
        lines.append(f"- {key}: `{report.get(key)}`")
    lines.extend(["", "## Candidates", ""])
    for item in report.get("candidates") or []:
        lines.extend(
            [
                f"### `{item.get('target_file')}`",
                "",
                f"- Passed: `{item.get('passed')}`",
                f"- Reason: {item.get('reason')}",
                f"- Diff path: `{item.get('diff_path')}`",
                f"- Diff chars: `{item.get('diff_chars')}`",
                f"- Diff sha256: `{item.get('diff_sha256')}`",
                "",
            ]
        )
    if report.get("warnings"):
        lines.extend(["## Warnings", ""])
        lines.extend(f"- {item}" for item in report.get("warnings") or [])
    if report.get("errors"):
        lines.extend(["## Errors", ""])
        lines.extend(f"- {item}" for item in report.get("errors") or [])
    return "\n".join(lines).rstrip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--operator-request", default="")
    parser.add_argument("--operator-request-file", default="")
    parser.add_argument("--evidence-report", action="append", default=[])
    parser.add_argument("--matrix-report", default="")
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--candidate-dir", default="output/validation/patch_candidates")
    parser.add_argument("--output", default="output/validation/patch_candidate_synthesis.json")
    parser.add_argument("--markdown-output", default="output/validation/patch_candidate_synthesis.md")
    parser.add_argument("--max-candidates", type=int, default=3)
    parser.add_argument("--timeout-seconds", type=int, default=120)
    parser.add_argument("--allow-current-worktree-diff-candidates", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.operator_request_file and not args.operator_request:
        args.operator_request = Path(args.operator_request_file).read_text(encoding="utf-8-sig", errors="replace")
    repo_root = Path(args.repo_root).resolve()
    report = build_report(args)
    output = resolve(repo_root, args.output)
    markdown = resolve(repo_root, args.markdown_output)
    write_json_report(report, output)
    write_text_report(render_markdown(report), markdown)
    print(json.dumps({"passed": report["passed"], "output": str(output)}, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
