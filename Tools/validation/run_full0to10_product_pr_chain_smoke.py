#!/usr/bin/env python3
"""End-to-end smoke for the unified run patch product PR chain.

This smoke keeps a legacy filename for compatibility, but it validates the
single unified run product chain. Full0To10 is not a separate pipeline and not a
runtime profile here. It has been absorbed by the unified run semantics:
controlled input, dynamic heap/exchange center, deterministic product exit and
reviewable PR output.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

try:
    from report_utils import resolve_output_path, write_json_report, write_text_report
except ImportError:
    from Tools.validation.report_utils import resolve_output_path, write_json_report, write_text_report  # type: ignore


STAMP = "full0to10_product_pr_chain_smoke_20990101-010203"
MARKER = "full0to10_product_pr_chain_smoke_marker"
PREVIEW_CHARS = 6000


def inspect_real_workflow(source_repo: Path) -> dict[str, Any]:
    """Verify the canonical product PR chain across workflow + extracted helpers."""
    files = {
        "workflow": source_repo / "Tools/workflow/run_unified_local_ai_refactor.ps1",
        "review_pr_args_builder": source_repo / "Tools/ai/build_review_pr_prepare_args.py",
        "chain_args_builder": source_repo / "Tools/ai/build_unified_chain_contract_args.py",
        "chain_contract": source_repo / "Tools/validation/check_unified_chain_contract.py",
        "manifest_schema_validator": source_repo / "Tools/validation/check_unified_run_manifest_schema.py",
        "legacy_alias_registry": source_repo / "Tools/ai/unified_run_legacy_alias_registry.json",
        "closure_audit": source_repo / "Tools/ai/build_heap_exchange_closure_audit.py",
    }

    texts = {
        name: path.read_text(encoding="utf-8-sig", errors="replace") if path.exists() else ""
        for name, path in files.items()
    }

    required_tokens = {
        "workflow:heap_exchange_entry": ("workflow", "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN"),
        "workflow:heap_exchange_entry_ensure": ("workflow", "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-ENSURE-BEGIN"),
        "workflow:heap_peer_runtime_manifest": ("workflow", "build_heap_peer_runtime_manifest.py"),
        "workflow:heap_peer_runtime_marker": ("workflow", "IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-BEGIN"),
        "workflow:heap_exchange_closure_audit": ("workflow", "build_heap_exchange_closure_audit.py"),
        "workflow:heap_exchange_closure_audit_marker": ("workflow", "IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-BEGIN"),
        "workflow:heap_exchange_exit_after_patch_suggestion": ("workflow", "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN"),
        "workflow:heap_exchange_lifecycle": ("workflow", "check_heap_exchange_runtime_lifecycle.py"),
        "workflow:task_patch_suggestion_report": ("workflow", "build_task_patch_suggestion_report.py"),
        "workflow:patch_suggestion_final_phase": ("workflow", "Patch suggestion final phase product"),
        "workflow:patch_suggestion_product_separation": ("workflow", "Validate patch suggestion product separation"),
        "workflow:patch_suggestion_product_gate": ("workflow", "--require-product"),
        "workflow:review_pr_prepare_args_builder": ("workflow", "build_review_pr_prepare_args.py"),
        "workflow:review_pr_prepare": ("workflow", "Prepare review branch and PR"),
        "workflow:final_chain_contract_gate": ("workflow", "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN"),
        "workflow:final_chain_args_builder": ("workflow", "build_unified_chain_contract_args.py"),

        "review_args:auto_include": ("review_pr_args_builder", "--auto-include-from-apply-report"),
        "review_args:apply_report": ("review_pr_args_builder", "--apply-report"),

        "chain_args:review_pr_report": ("chain_args_builder", "--review-pr-report"),
        "chain_args:review_pr_product": ("chain_args_builder", "--require-review-pr-product"),
        "chain_args:provider_tool_evidence": ("chain_args_builder", "--require-provider-tool-evidence"),
        "chain_args:closure_audit_report": ("chain_args_builder", "--closure-audit-report"),
        "chain_args:require_heap_closure_audit": ("chain_args_builder", "--require-heap-closure-audit"),

        "chain_contract:provider_tool_edge": ("chain_contract", "provider_to_tool_evidence"),
        "chain_contract:peer_runtime_edge": ("chain_contract", "heap_exchange_to_peer_runtime"),
        "chain_contract:shared_memory_edge": ("chain_contract", "heap_exchange_to_shared_memory"),
        "chain_contract:closure_audit_edge": ("chain_contract", "heap_exchange_to_closure_audit"),
        "chain_contract:review_pr_product_edge": ("chain_contract", "product_separation_to_review_pr_product"),

        "manifest_schema_validator:file": ("manifest_schema_validator", "unified_run_manifest_schema_validation"),
        "legacy_alias_registry:file": ("legacy_alias_registry", "unified_run_legacy_alias_registry"),
        "closure_audit:file": ("closure_audit", "heap_exchange_closure_audit"),
    }

    missing = [
        name
        for name, (file_key, token) in required_tokens.items()
        if token not in texts.get(file_key, "")
    ]

    workflow_text = texts["workflow"]
    ordered_tokens = [
        ("heap_exchange_entry", "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN"),
        ("heap_peer_runtime_manifest", "IA-CARMINE-HEAP-PEER-RUNTIME-MANIFEST-BEGIN"),
        ("heap_exchange_closure_audit", "IA-CARMINE-HEAP-EXCHANGE-CLOSURE-AUDIT-BEGIN"),
        ("patch_suggestion_final_phase", "Patch suggestion final phase product"),
        ("heap_exchange_exit_after_patch_suggestion", "IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-AFTER-PATCH-SUGGESTION-BEGIN"),
        ("patch_suggestion_product_separation", "Validate patch suggestion product separation"),
        ("review_pr_prepare", "Prepare review branch and PR"),
        ("final_chain_contract", "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-FINAL-GATE-BEGIN"),
    ]
    positions = [
        {"phase": name, "position": workflow_text.find(token)}
        for name, token in ordered_tokens
    ]

    errors = []
    if missing:
        errors.extend(f"workflow distributed trace missing token: {name}" for name in missing)
    if any(item["position"] < 0 for item in positions):
        errors.append("canonical workflow product PR chain positions unavailable")
    elif positions != sorted(positions, key=lambda item: item["position"]):
        errors.append("canonical workflow product PR chain is not in execution order")

    return {
        "path": files["workflow"].as_posix(),
        "inspected_files": {name: path.as_posix() for name, path in files.items()},
        "passed": not errors,
        "missing_tokens": missing,
        "ordered_chain": positions,
        "errors": errors,
    }


def stream(text: str) -> dict[str, Any]:
    """Return a bounded stream summary."""
    return {"chars": len(text), "preview": text[:PREVIEW_CHARS], "truncated": len(text) > PREVIEW_CHARS}


def run(command: list[str], cwd: Path, env: dict[str, str], timeout_seconds: int) -> dict[str, Any]:
    """Run a smoke command with timeout and compact output."""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
        return {
            "command": command,
            "returncode": result.returncode,
            "stdout": stream(result.stdout),
            "stderr": stream(result.stderr),
            "error": "",
        }
    except subprocess.TimeoutExpired as exc:
        return {
            "command": command,
            "returncode": 124,
            "stdout": stream(exc.stdout or ""),
            "stderr": stream(exc.stderr or ""),
            "error": f"TimeoutExpired: {timeout_seconds}s",
        }


def write_json(path: Path, data: dict[str, Any]) -> None:
    """Write a JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def seed_repo(tmp: Path) -> Path:
    """Create a small git repository with task and target docs."""
    repo = tmp / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-b", "master"], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "config", "user.email", "smoke@example.invalid"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.name", "Full0To10 Product Smoke"], cwd=repo, check=True)
    (repo / "docs" / "LOCAL_AI_TASKS").mkdir(parents=True)
    (repo / "docs" / "LOCAL_VALIDATION_EVIDENCE").mkdir(parents=True)
    target = repo / "docs" / "LOCAL_AI_TASKS" / "obsolete-monolithic-docs-review-2026-05-07.md"
    target.write_text("# Obsolete Review\n\nSeed content.\n", encoding="utf-8")
    task = repo / "docs" / "LOCAL_AI_TASKS" / "smoke-task.md"
    task.write_text(
        "\n".join(
            [
                "# Smoke Task",
                "",
                "```patch_suggestion",
                json.dumps(
                    {
                        "suggestions": [
                            {
                                "id": "full0to10_product_pr_chain_smoke",
                                "family": "docs",
                                "title": "Append smoke marker",
                                "operation": "append_once",
                                "target_file": target.relative_to(repo).as_posix(),
                                "marker": MARKER,
                                "content": f"\n{MARKER}: product PR chain smoke.\n",
                                "patch_sketch": ["Append a deterministic marker to the target doc."],
                                "validation_commands": ["git diff --check"],
                                "stop_conditions": ["Do not stage output/**."],
                            }
                        ]
                    },
                    indent=2,
                ),
                "```",
                "",
            ]
        ),
        encoding="utf-8",
    )
    subprocess.run(["git", "add", "."], cwd=repo, check=True, capture_output=True, text=True)
    subprocess.run(["git", "commit", "-m", "seed smoke repo"], cwd=repo, check=True, capture_output=True, text=True)
    return repo


def load_json(path: Path) -> dict[str, Any]:
    """Load a JSON object."""
    return json.loads(path.read_text(encoding="utf-8-sig"))


def render_markdown(report: dict[str, Any]) -> str:
    """Render a compact Markdown report."""
    lines = [
        "# Unified Run Product PR Chain Smoke",
        "",
        f"- Passed: `{report['passed']}`",
        f"- Timeout seconds: `{report['timeout_seconds']}`",
        f"- Command count: `{len(report.get('commands', []))}`",
        f"- Deterministic operation count: `{report.get('deterministic_operation_count')}`",
        f"- PR preparation committed: `{report.get('review_pr_commit_performed')}`",
        f"- Chain contract passed: `{report.get('chain_contract_passed')}`",
        f"- Real workflow trace passed: `{report.get('workflow_trace', {}).get('passed')}`",
        "- Legacy name: `full0to10_product_pr_chain_smoke`",
        "- Runtime model: `single unified run`",
    ]
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def parse_args() -> argparse.Namespace:
    """Parse CLI args."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/full0to10_product_pr_chain_smoke.json")
    parser.add_argument("--markdown-output", default="output/validation/full0to10_product_pr_chain_smoke.md")
    parser.add_argument("--timeout-seconds", type=int, default=60)
    return parser.parse_args()


def main() -> int:
    """CLI entrypoint."""
    args = parse_args()
    source_repo = Path(args.repo_root).resolve()
    env = dict(os.environ)
    env["PYTHONPATH"] = str(source_repo)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    errors: list[str] = []
    commands: list[dict[str, Any]] = []
    workflow_trace = inspect_real_workflow(source_repo)
    if workflow_trace.get("passed") is not True:
        errors.extend(f"workflow trace: {error}" for error in workflow_trace.get("errors", []))
        for token in workflow_trace.get("missing_tokens", []):
            errors.append(f"workflow trace missing token: {token}")
    with tempfile.TemporaryDirectory(prefix="full0to10-product-pr-smoke-") as tmp_raw:
        repo = seed_repo(Path(tmp_raw))
        task = repo / "docs/LOCAL_AI_TASKS/smoke-task.md"
        task_json = repo / "output/validation/task_patch_suggestions.json"
        task_md = repo / "output/validation/task_patch_suggestions.md"
        apply_json = repo / "output/validation/patch_suggestion_bundle_apply.json"
        separation_json = repo / "output/validation/patch_suggestion_product_separation.json"
        review_json = repo / "output/validation/review_pr_prepare.json"
        review_md = repo / "output/validation/review_pr_prepare.md"
        evidence_json = repo / "docs/LOCAL_VALIDATION_EVIDENCE/review_pr_prepare.json"
        evidence_md = repo / "docs/LOCAL_VALIDATION_EVIDENCE/review_pr_prepare.md"
        chain_json = repo / "output/validation/unified_chain_contract.json"
        manifest_json = repo / f"output/local_ai_runs/{STAMP}_unified/pipeline/unified_local_ai_refactor_manifest.json"
        official_json = repo / f"output/validation/{STAMP}_phase_official.json"
        gpu0_json = repo / f"output/validation/openvino_gpu0_workload_{STAMP}.json"
        branch = f"CARMINEai/product-pr-chain-smoke-{STAMP}"
        write_json(manifest_json, {"schema_version": 1, "kind": "unified_local_ai_refactor_manifest", "stamp": STAMP})
        write_json(official_json, {"schema_version": 1, "kind": "unified_launcher_phase_status", "phase": "official", "passed": True, "status": "passed", "return_code": 0})
        write_json(gpu0_json, {"schema_version": 1, "kind": "openvino_gpu0_workload", "passed": True, "openvino_gpu0_visible": True, "openvino_gpu0_workload_performed": True, "openvino_gpu0_workload_passed": True})
        steps = [
            [
                sys.executable,
                str(source_repo / "Tools/ai/build_task_patch_suggestion_report.py"),
                "--repo-root",
                str(repo),
                "--task-file",
                str(task),
                "--Stamp",
                STAMP,
                "--output",
                str(task_json),
                "--markdown-output",
                str(task_md),
            ],
            [
                sys.executable,
                str(source_repo / "Tools/ai/apply_patch_suggestion_bundle.py"),
                "--repo-root",
                str(repo),
                "--Stamp",
                STAMP,
                "--suggestion-report",
                str(task_json),
                "--no-current-suggestions",
                "--output",
                str(apply_json),
                "--create-review-branch",
                branch,
                "--allow-dirty-branch",
                "--apply",
                "--allow-dirty",
            ],
            [
                sys.executable,
                str(source_repo / "Tools/validation/check_patch_suggestion_product_separation.py"),
                "--repo-root",
                str(repo),
                "--report",
                str(apply_json),
                "--require-product",
                "--output",
                str(separation_json),
            ],
            [
                sys.executable,
                str(source_repo / "Tools/ai/prepare_review_pr.py"),
                "--repo-root",
                str(repo),
                "--Stamp",
                STAMP,
                "--task-file",
                str(task),
                "--branch",
                branch,
                "--base",
                "master",
                "--title",
                f"docs(ai): product PR chain smoke {STAMP}",
                "--commit-message",
                "docs(ai): product PR chain smoke",
                "--apply-report",
                str(apply_json),
                "--auto-include-from-apply-report",
                "--output",
                str(review_json),
                "--markdown-output",
                str(review_md),
                "--evidence-output",
                str(evidence_json),
                "--evidence-markdown-output",
                str(evidence_md),
                "--allow-dirty-branch",
            ],
            [
                sys.executable,
                str(source_repo / "Tools/validation/check_unified_chain_contract.py"),
                "--repo-root",
                str(repo),
                "--stamp",
                STAMP,
                "--manifest",
                str(manifest_json),
                "--official-report",
                str(official_json),
                "--gpu0-report",
                str(gpu0_json),
                "--apply-report",
                str(apply_json),
                "--product-separation-report",
                str(separation_json),
                "--review-pr-report",
                str(review_json),
                "--require-concrete-patch-specs",
                "--require-review-pr-product",
                "--output",
                str(chain_json),
            ],
        ]
        for step in steps:
            result = run(step, repo, env, args.timeout_seconds)
            commands.append(result)
            if result["returncode"] != 0:
                errors.append(f"command failed: {Path(step[1]).name} rc={result['returncode']} {result['error']}")

        apply_report = load_json(apply_json) if apply_json.exists() else {}
        separation = load_json(separation_json) if separation_json.exists() else {}
        review = load_json(review_json) if review_json.exists() else {}
        chain = load_json(chain_json) if chain_json.exists() else {}
        target_text = (repo / "docs/LOCAL_AI_TASKS/obsolete-monolithic-docs-review-2026-05-07.md").read_text(encoding="utf-8")
        if MARKER not in target_text:
            errors.append("deterministic marker was not applied")
        if apply_report.get("operation_count") != 1:
            errors.append(f"expected one deduped operation, found {apply_report.get('operation_count')}")
        if apply_report.get("applied_count") != 1:
            errors.append(f"expected one applied operation, found {apply_report.get('applied_count')}")
        if separation.get("passed") is not True:
            errors.append("product separation validation did not pass")
        if review.get("git_commit_performed") is not True:
            errors.append("review PR preparation did not create product commit")
        if review.get("auto_include_from_apply_report") is not True:
            errors.append("review PR preparation did not use apply-report auto include")
        if not review.get("auto_include_paths"):
            errors.append("review PR preparation did not discover auto include paths")
        if chain.get("passed") is not True:
            errors.append("unified chain contract did not pass after review PR preparation")
        if not any(edge.get("edge") == "product_separation_to_review_pr_product" and edge.get("passed") is True for edge in chain.get("edges") or []):
            errors.append("unified chain contract did not validate the review PR product edge")
        if review.get("github_pr_created") is True or review.get("git_push_performed") is True:
            errors.append("smoke unexpectedly pushed or created a GitHub PR")

    report = {
        "schema_version": 1,
        "kind": "unified_run_product_pr_chain_smoke",
        "legacy_smoke_name": "full0to10_product_pr_chain_smoke",
        "full0to10_legacy_alias_absorbed_by_unified_run": True,
        "repo_root": source_repo.as_posix(),
        "passed": not errors,
        "timeout_seconds": args.timeout_seconds,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "unified_run_model": "single_dynamic_heap_exchange_run",
        "git_push_performed": False,
        "github_pr_created": False,
        "deterministic_operation_count": apply_report.get("operation_count"),
        "review_pr_commit_performed": review.get("git_commit_performed"),
        "review_pr_auto_include_from_apply_report": review.get("auto_include_from_apply_report"),
        "chain_contract_passed": chain.get("passed"),
        "workflow_trace": workflow_trace,
        "commands": commands,
        "errors": errors,
        "warnings": [],
    }
    output = resolve_output_path(source_repo, args.output)
    markdown = resolve_output_path(source_repo, args.markdown_output)
    print(write_json_report(report, output), end="")
    write_text_report(render_markdown(report), markdown)
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
