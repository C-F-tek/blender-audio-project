#!/usr/bin/env python3
"""Create artifact-owned patch candidates from verified local targets."""

from __future__ import annotations

import argparse
import ast
import difflib
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

try:
    from Tools.ai.runtime_file_refs import (
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from Tools.ai.code_product.patch_candidate_report import (
        candidate_report_passed,
        report_level_errors,
        report_level_warnings,
    )
    from Tools.ai.code_product.synthesis_patterns import candidate_transforms
    from Tools.validation._shared.report_utils import write_json_report, write_text_report
except ImportError:
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from Tools.ai.runtime_file_refs import (  # type: ignore
        RuntimeConsumer,
        RuntimeFileRefResolver,
        RuntimeRefProvenance,
    )
    from Tools.ai.code_product.patch_candidate_report import (  # type: ignore
        candidate_report_passed,
        report_level_errors,
        report_level_warnings,
    )
    from Tools.ai.code_product.synthesis_patterns import candidate_transforms  # type: ignore
    from Tools.validation._shared.report_utils import write_json_report, write_text_report  # type: ignore


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


def unified_diff(rel_path: str, before: str, after: str) -> str:
    lines = list(
        difflib.unified_diff(
            before.splitlines(),
            after.splitlines(),
            fromfile=f"a/{rel_path}",
            tofile=f"b/{rel_path}",
            lineterm="",
        )
    )
    body = "\n".join(lines)
    if not body.endswith("\n"):
        body += "\n"
    return f"diff --git a/{rel_path} b/{rel_path}\n{body}"


def git_apply_check(repo_root: Path, diff_path: Path, timeout: int) -> dict[str, Any]:
    completed = subprocess.run(
        ["git", "apply", "--check", "--ignore-whitespace", str(diff_path)],
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )
    return {
        "command": ["git", "apply", "--check", "--ignore-whitespace", str(diff_path)],
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-2000:],
        "stderr_tail": (completed.stderr or "")[-2000:],
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
    for ref in refs:
        if len(candidates) >= max(1, int(args.max_candidates)):
            break
        if not ref.patchable or not ref.repo_relative.endswith(".py"):
            continue
        path = repo_root / ref.repo_relative
        before = path.read_text(encoding="utf-8-sig", errors="replace")
        transforms = candidate_transforms(ref.repo_relative, before, str(args.operator_request or ""))
        if not transforms:
            continue
        transform = transforms[0]
        after = transform.updated_text
        reason = transform.reason
        if after == before:
            continue
        semantic_check = semantic_patch_check(ref.repo_relative, after)
        diff_text = unified_diff(ref.repo_relative, before, after)
        safe_name = ref.repo_relative.replace("/", "__").replace("\\", "__")
        diff_path = candidate_dir / f"{len(candidates)+1:03d}_{safe_name}.diff"
        diff_path.write_text(diff_text, encoding="utf-8")
        check = git_apply_check(repo_root, diff_path, max(30, int(args.timeout_seconds)))
        passed = check.get("passed") is True and semantic_check.get("passed") is True
        candidates.append(
            {
                "target_file": ref.repo_relative,
                "reason": reason,
                "pattern_id": transform.pattern_id,
                "evidence": [
                    "target resolved against local filesystem",
                    "candidate generated from current file contents",
                    "applicability checked with git apply --check",
                ],
                "unified_diff": diff_text,
                "diff_path": str(diff_path),
                "validation_commands": [
                    f"git apply --check --ignore-whitespace {diff_path}",
                    f"python -m py_compile {ref.repo_relative}",
                    "git diff --check",
                ],
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
        )
    if not candidates:
        warnings.append("no validated patch candidate pattern matched verified targets")
    warnings.extend(report_level_warnings(candidates))
    return {
        "schema_version": 1,
        "kind": "patch_candidate_synthesis",
        "generated_at": now_iso(),
        "repo_root": str(repo_root),
        "operator_request": str(args.operator_request or ""),
        "passed": candidate_report_passed(candidates),
        "target_ref_count": len(refs),
        "candidate_count": len(candidates),
        "patch_candidate_synthesis_passed_count": sum(1 for item in candidates if item.get("passed") is True),
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
                "",
                "```diff",
                str(item.get("unified_diff") or "").rstrip(),
                "```",
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
    parser.add_argument("--matrix-report", default="")
    parser.add_argument("--target-file", action="append", default=[])
    parser.add_argument("--candidate-dir", default="output/validation/patch_candidates")
    parser.add_argument("--output", default="output/validation/patch_candidate_synthesis.json")
    parser.add_argument("--markdown-output", default="output/validation/patch_candidate_synthesis.md")
    parser.add_argument("--max-candidates", type=int, default=3)
    parser.add_argument("--timeout-seconds", type=int, default=120)
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
