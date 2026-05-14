#!/usr/bin/env python3
"""Smoke test the heap final readable product assembler."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


def now_stamp() -> str:
    return datetime.now().strftime("%Y%m%d-%H%M%S")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def repo_rel(repo_root: Path, path: Path) -> str:
    try:
        return (
            path.resolve(strict=False)
            .relative_to(repo_root.resolve(strict=False))
            .as_posix()
        )
    except ValueError:
        return str(path)


def build_fixture(repo_root: Path, work_dir: Path) -> tuple[Path, Path]:
    run_dir = work_dir / "heap_context_closure_smoke"
    documents_dir = work_dir / "documents"
    documents_dir.mkdir(parents=True, exist_ok=True)
    manifest = documents_dir / "DOWNLOADS.txt"
    write_text(manifest, "Smoke package\n")

    matrix_path = run_dir / "broker_bridge" / "tool_outputs" / "smoke_heap_code_execution_tool.json"
    virtual_dev_path = (
        run_dir / "broker_bridge" / "tool_outputs" / "smoke_heap_virtual_dev_environment.json"
    )
    debug_lab_path = run_dir / "debug_lab" / "smoke_debug_lab.json"
    write_json(
        virtual_dev_path,
        {
            "kind": "heap_virtual_development_environment",
            "passed": True,
            "target_count": 2,
            "validation_count": 1,
            "targets": [
                {"target_file": "Tools/ai/assemble_heap_final_readable_product.py", "ast_ok": True, "import_ok": True, "help_ok": True},
                {"target_file": "Tools/ai/heap_final_readable_synthesis.py", "ast_ok": True, "import_ok": True, "help_ok": True},
            ],
            "guardrails": {
                "free_shell_exposed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "git_write_performed": False,
            },
        },
    )
    write_json(debug_lab_path, {"kind": "debug_lab", "passed": True})
    write_json(
        matrix_path,
        {
            "schema_version": 1,
            "kind": "heap_code_execution_tool",
            "passed": True,
            "debug_lab_report": repo_rel(repo_root, debug_lab_path),
            "debug_lab_passed": True,
            "target_count": 2,
            "concrete_code_proposal_count": 2,
            "guardrails": {
                "free_shell_exposed": False,
                "patch_application_performed": False,
                "source_writes_performed": False,
                "git_write_performed": False,
            },
            "concrete_code_proposals": [
                {
                    "target_file": "Tools/ai/assemble_heap_final_readable_product.py",
                    "implementation_status": "developed_change_present",
                    "git_status": "?? Tools/ai/assemble_heap_final_readable_product.py",
                    "code_or_patch_sketch": "new file: Tools/ai/assemble_heap_final_readable_product.py\n\n+def build_report(...):\n+    pass\n",
                    "validation_commands": [
                        "python -m py_compile Tools/ai/assemble_heap_final_readable_product.py",
                        "python Tools/validation/run_heap_final_readable_product_smoke.py",
                        "git diff --check",
                    ],
                },
                {
                    "target_file": "Tools/ai/run_heap_runtime_context_closure.py",
                    "implementation_status": "developed_change_present",
                    "git_status": "M Tools/ai/run_heap_runtime_context_closure.py",
                    "code_or_patch_sketch": "diff --git a/Tools/ai/run_heap_runtime_context_closure.py b/Tools/ai/run_heap_runtime_context_closure.py\n+    final_readable_product_command = [...]\n",
                    "validation_commands": [
                        "python -m py_compile Tools/ai/run_heap_runtime_context_closure.py"
                    ],
                },
            ],
        },
    )
    write_json(
        run_dir / "heap_final_proposal_composer.json",
        {
            "schema_version": 1,
            "kind": "heap_final_proposal_composer",
            "documents_dir": str(documents_dir),
            "download_manifest_txt": str(manifest),
            "operator_decision": {
                "decision": "DIAGNOSTIC_ONLY",
                "accepted_proposals": [],
                "rejected_proposals": [
                    {
                        "name": "provider_candidate",
                        "reasons": ["invented source path"],
                    }
                ],
            },
        },
    )
    write_json(
        run_dir / "heap_runtime_completeness_gate_report.json",
        {
            "schema_version": 1,
            "kind": "heap_runtime_completeness_gate",
            "passed": True,
            "provider_execution_performed": True,
            "patch_application_performed": False,
            "source_writes_performed": False,
            "metrics": {
                "product_status": "blocked_with_reason",
                "completed_requirements": ["preflight", "code_execution_matrix"],
                "missing_requirements": [],
                "code_execution_matrix_required": True,
                "code_execution_matrix_passed": True,
                "code_execution_matrix_reports": [repo_rel(repo_root, matrix_path)],
                "runtime_debug_lab_passed": True,
                "virtual_dev_environment_passed": True,
                "virtual_dev_environment_reports": [repo_rel(repo_root, virtual_dev_path)],
            },
            "real_run_output_contract": {
                "product_status": "blocked_with_reason",
                "missing_requirements": [],
            },
        },
    )
    write_json(run_dir / "heap_context_preflight_gate.json", {"passed": True})
    write_json(
        run_dir / "external_heap_postrun_package.json",
        {"passed": True, "product_acceptance_passed": False},
    )
    write_json(
        run_dir / "external_heap_revision_context.json",
        {"terminal_no_patchable_target": True},
    )
    return run_dir, documents_dir


def run_smoke(args: argparse.Namespace) -> dict[str, Any]:
    repo_root = Path(args.repo_root).resolve()
    work_dir = (
        Path(args.work_dir).resolve()
        if args.work_dir
        else repo_root / "output" / "validation" / f"heap_final_readable_product_smoke_{now_stamp()}"
    )
    run_dir, documents_dir = build_fixture(repo_root, work_dir)
    output = run_dir / "heap_final_readable_product.json"
    markdown = run_dir / "heap_final_readable_product.md"
    text = run_dir / "heap_final_readable_product.txt"
    command = [
        sys.executable,
        "Tools/ai/assemble_heap_final_readable_product.py",
        "--repo-root",
        ".",
        "--run-dir",
        str(run_dir),
        "--output",
        str(output),
        "--markdown-output",
        str(markdown),
        "--text-output",
        str(text),
        "--documents-dir",
        str(documents_dir),
        "--zip-documents",
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=max(30, int(args.timeout_seconds)),
    )
    product = json.loads(output.read_text(encoding="utf-8-sig")) if output.exists() else {}
    final_md = documents_dir / "FINAL_READABLE_PRODUCT.md"
    full_code_product = documents_dir / "CODE_PRODUCT_FULL_PATCH.md"
    zip_path = Path(str(documents_dir) + ".zip")
    body = final_md.read_text(encoding="utf-8-sig") if final_md.exists() else ""
    code_product_body = (
        full_code_product.read_text(encoding="utf-8-sig")
        if full_code_product.exists()
        else ""
    )
    required_phrases = [
        "Decisione finale",
        "Final document status",
        "Piano applicabile",
        "Modifiche concrete",
        "Sequenza di applicazione",
        "Laboratorio operativo",
        "Sa usarlo",
        "Code product",
        "Universo pointer e memoria",
        "Perche il provider non si applica",
        "Decisione operatore",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in body]
    passed = (
        completed.returncode == 0
        and product.get("passed") is True
        and final_md.exists()
        and full_code_product.exists()
        and "CODE_PRODUCT_FULL_PATCH" in code_product_body
        and "Tools/ai/assemble_heap_final_readable_product.py" in code_product_body
        and zip_path.exists()
        and not missing
    )
    report = {
        "schema_version": 1,
        "kind": "heap_final_readable_product_smoke",
        "passed": passed,
        "work_dir": str(work_dir),
        "run_dir": str(run_dir),
        "documents_dir": str(documents_dir),
        "product_json": str(output),
        "documents_markdown": str(final_md),
        "full_code_product": str(full_code_product),
        "documents_zip": str(zip_path),
        "missing_required_phrases": missing,
        "returncode": completed.returncode,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
        "command": command,
    }
    report_output = Path(args.output).resolve() if args.output else work_dir / "smoke.json"
    write_json(report_output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return report


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default="")
    parser.add_argument("--output", default="")
    parser.add_argument("--timeout-seconds", type=int, default=90)
    return parser.parse_args()


def main() -> int:
    report = run_smoke(parse_args())
    return 0 if report.get("passed") else 2


if __name__ == "__main__":
    raise SystemExit(main())
