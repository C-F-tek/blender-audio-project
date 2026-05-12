#!/usr/bin/env python3
"""Run the external heap post-run package chain.

This orchestrator is outside the gate. It does not replace the existing composer
and does not modify provider/tool-call semantics. It only runs the external
post-run adapters in the correct order for an existing heap_context_closure_* run:

1. normalize_heap_final_causality.py
2. build_external_heap_block_pointer_manifest.py
3. compose_external_heap_block_response.py
4. build_external_heap_revision_context.py

Packaging is degradable: a product-quality failure in one adapter must be
reported, but must not prevent later adapters from producing pointer/revision
artifacts when their input files exist. A blocked product still needs a complete
operator package and next-run revision context.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any


REQUIRED_COMPOSER_JSON = "heap_final_proposal_composer.json"


def resolve_repo_root(value: str) -> Path:
    return Path(value).resolve()


def is_complete_heap_run_dir(path: Path) -> bool:
    return path.is_dir() and path.name.startswith("heap_context_closure_") and (path / REQUIRED_COMPOSER_JSON).exists()


def latest_run_dir(repo_root: Path) -> Path | None:
    validation_dir = repo_root / "output" / "validation"
    if not validation_dir.exists():
        return None
    candidates = sorted(
        [path for path in validation_dir.iterdir() if is_complete_heap_run_dir(path)],
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return candidates[0].resolve() if candidates else None


def resolve_run_dir(repo_root: Path, value: str) -> Path:
    if value.strip():
        path = Path(value)
        if not path.is_absolute():
            path = repo_root / path
        return path.resolve()
    latest = latest_run_dir(repo_root)
    if latest is None:
        raise SystemExit("no complete heap_context_closure_* run directory with heap_final_proposal_composer.json found under output/validation")
    return latest


def resolve_project_python(repo_root: Path, explicit: str = "") -> str:
    if explicit:
        return str(Path(explicit).resolve())
    for candidate in (
        repo_root / ".venv" / "Scripts" / "python.exe",
        repo_root / "venv" / "Scripts" / "python.exe",
        repo_root / ".venv314" / "Scripts" / "python.exe",
    ):
        if candidate.exists():
            return str(candidate.resolve())
    return sys.executable


def run_command(command: list[str], repo_root: Path) -> dict[str, Any]:
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
    )
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def required_file(path: Path, label: str) -> None:
    if not path.exists():
        raise SystemExit(f"missing required {label}: {path}")


def json_file_passed(path: Path, *keys: str) -> bool | None:
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return None
    if not isinstance(data, dict):
        return None
    for key in keys:
        value = data.get(key)
        if isinstance(value, bool):
            return value
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--python-exe", default="")
    parser.add_argument("--run-dir", default="", help="Defaults to latest complete output/validation/heap_context_closure_* directory.")
    parser.add_argument("--max-block-chars", type=int, default=9000)
    parser.add_argument("--max-blocks", type=int, default=0)
    parser.add_argument("--include-rejected-history", action="store_true")
    parser.add_argument("--include-peer-blocks", action="store_true")
    parser.add_argument("--no-documents-copy", action="store_true")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = resolve_repo_root(args.repo_root)
    project_python = resolve_project_python(repo_root, args.python_exe)
    run_dir = resolve_run_dir(repo_root, args.run_dir)

    composer_json = run_dir / REQUIRED_COMPOSER_JSON
    required_file(composer_json, "composer json")

    causality_json = run_dir / "heap_final_causality_normalized.json"
    pointer_json = run_dir / "external_heap_block_pointer_manifest.json"
    long_response_md = run_dir / "external_heap_primary_long_response.md"
    revision_json = run_dir / "external_heap_revision_context.json"

    commands: list[tuple[str, list[str]]] = []
    commands.append(
        (
            "normalize_causality",
            [
                project_python,
                "Tools/ai/normalize_heap_final_causality.py",
                "--composer-json",
                str(composer_json),
                "--output",
                str(causality_json),
            ],
        )
    )
    commands.append(
        (
            "build_pointer_manifest",
            [
                project_python,
                "Tools/ai/build_external_heap_block_pointer_manifest.py",
                "--repo-root",
                ".",
                "--run-dir",
                str(run_dir),
                "--max-block-chars",
                str(args.max_block_chars),
                "--max-blocks",
                str(args.max_blocks),
            ],
        )
    )
    long_command = [
        project_python,
        "Tools/ai/compose_external_heap_block_response.py",
        "--pointer-manifest",
        str(pointer_json),
        "--composer-json",
        str(composer_json),
        "--causality-json",
        str(causality_json),
        "--output",
        str(long_response_md),
    ]
    if args.include_rejected_history:
        long_command.append("--include-rejected-history")
    if args.include_peer_blocks:
        long_command.append("--include-peer-blocks")
    if args.no_documents_copy:
        long_command.append("--no-documents-copy")
    commands.append(("compose_long_response", long_command))

    revision_command = [
        project_python,
        "Tools/ai/build_external_heap_revision_context.py",
        "--pointer-manifest",
        str(pointer_json),
        "--composer-json",
        str(composer_json),
        "--causality-json",
        str(causality_json),
        "--output",
        str(revision_json),
    ]
    if args.no_documents_copy:
        revision_command.append("--no-documents-copy")
    commands.append(("build_revision_context", revision_command))

    results: list[dict[str, Any]] = []
    hard_failure = False
    for name, command in commands:
        result = run_command(command, repo_root)
        result["name"] = name
        results.append(result)
        # Continue after product-quality failures so blocked runs still emit the
        # pointer graph, long response, and revision context. Stop only when the
        # failed step did not produce the file required by later steps.
        if not result["passed"]:
            if name == "normalize_causality" and causality_json.exists():
                result["degraded_continuation"] = True
                result["degraded_reason"] = "causality normalization wrote a blocked/failed product report; continuing packaging"
                continue
            if name == "build_pointer_manifest" and pointer_json.exists():
                result["degraded_continuation"] = True
                result["degraded_reason"] = "pointer manifest exists despite non-zero returncode; continuing packaging"
                continue
            hard_failure = True
            break

    pointer_report = {}
    if pointer_json.exists():
        try:
            pointer_data = json.loads(pointer_json.read_text(encoding="utf-8-sig"))
            pointer_report = pointer_data if isinstance(pointer_data, dict) else {}
        except Exception:
            pointer_report = {}

    causality_passed = json_file_passed(causality_json, "causal_chain_passed", "product_acceptance_passed")
    pointer_passed = json_file_passed(pointer_json, "passed")
    long_response_passed = json_file_passed(long_response_md.with_suffix(".json"), "passed")
    revision_passed = json_file_passed(revision_json, "passed")
    packaging_complete = all(path.exists() for path in (causality_json, pointer_json, long_response_md, revision_json))
    command_failures = [result for result in results if not result.get("passed")]

    report = {
        "schema_version": 2,
        "kind": "external_heap_postrun_package",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "run_dir": str(run_dir),
        "run_dir_selection_policy": "latest_complete_heap_context_closure_with_composer_json" if not args.run_dir else "explicit_run_dir",
        "passed": packaging_complete and not hard_failure,
        "product_acceptance_passed": causality_passed,
        "packaging_complete": packaging_complete,
        "hard_failure": hard_failure,
        "causality_json": str(causality_json),
        "pointer_manifest_json": str(pointer_json),
        "long_response_markdown": str(long_response_md),
        "revision_context_json": str(revision_json),
        "causality_passed": causality_passed,
        "pointer_passed": pointer_passed,
        "long_response_passed": long_response_passed,
        "revision_passed": revision_passed,
        "provider_execution_performed": pointer_report.get("provider_execution_performed") is True,
        "patch_application_performed": False,
        "source_writes_performed": False,
        "results": results,
        "errors": [result["stderr_tail"] for result in command_failures if result.get("stderr_tail") and not result.get("degraded_continuation")],
        "warnings": [
            f"degraded postrun step: {result.get('name')} returncode={result.get('returncode')}"
            for result in command_failures
            if result.get("degraded_continuation")
        ],
    }
    output = Path(args.output).resolve() if args.output else run_dir / "external_heap_postrun_package.json"
    write_json(output, report)
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
