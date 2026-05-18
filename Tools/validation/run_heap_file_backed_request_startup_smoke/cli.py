#!/usr/bin/env python3
"""Smoke-test file-backed heap request and startup raw-file-list plumbing."""

from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[3]


def read(rel_path: str) -> str:
    return (repo_root() / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    launcher = "\n".join(
        [
            read("Tools/ai/heap_context_closure/launcher.py"),
            read("Tools/ai/heap_context_closure/commands.py"),
        ]
    )
    prepare = "\n".join(
        [
            read("Tools/ai/heap_context_memory_reload/cli.py"),
            read("Tools/ai/heap_context_memory_reload/runner.py"),
            read("Tools/ai/heap_context_memory_reload/memory_write.py"),
        ]
    )
    gate = "\n".join(
        [
            read("Tools/ai/heap_runtime/completeness_gate/cli.py"),
            read("Tools/ai/heap_gate/runtime_init.py"),
            read("Tools/ai/heap_gate/runtime_common.py"),
        ]
    )
    transient = read("Tools/ai/agent_context/transient_request_context/cli.py")
    sqlite_memory = "\n".join(
        [
            read("Tools/ai/agent_memory/sqlite_cli.py"),
            read("Tools/ai/agent_memory/sqlite_report.py"),
        ]
    )

    require(
        '"heap_request_file": run_dir / "heap_operator_request.md"' in launcher,
        "launcher must persist augmented request to run_dir file",
        errors,
    )
    require(
        'str(state["heap_request_file"])' in launcher,
        "launcher must pass request file to startup reload",
        errors,
    )
    require(
        'str(state["heap_request_file"])' in launcher,
        "launcher must pass request file to heap gate",
        errors,
    )
    require(
        '"--request-file"' in prepare,
        "startup reload must accept --request-file",
        errors,
    )
    require(
        'startup_request_file = state.output_dir / "heap_startup_request.md"' in prepare,
        "startup reload must materialize startup request file",
        errors,
    )
    require(
        'raw_file_list = state.output_dir / "startup_context_raw_files.txt"' in prepare,
        "startup reload must materialize context raw-file list",
        errors,
    )
    require(
        '"--raw-file-list"' in prepare and "str(raw_file_list)" in prepare,
        "startup reload must pass raw files by list file",
        errors,
    )
    require(
        'transient_command.extend(["--raw-file", rel_path])' not in prepare,
        "startup reload must not expand every raw-file on argv",
        errors,
    )
    require(
        '"--memory-note-file",' in prepare,
        "startup reload must pass transient memory note by file",
        errors,
    )
    require(
        '"--content-file",' in prepare,
        "startup reload must pass operational memory content by file",
        errors,
    )
    require(
        '"--request-file"' in gate,
        "heap gate must accept --request-file",
        errors,
    )
    require(
        "args.request = read_request_file(self.repo_root, args.request_file)" in gate,
        "heap gate must load request text from file",
        errors,
    )
    require(
        '"--memory-note-file"' in transient,
        "transient context tool must accept memory note files",
        errors,
    )
    require(
        '"--raw-file-list"' in transient,
        "transient context tool must accept raw file lists",
        errors,
    )
    require(
        "read_raw_file_list(repo_root, value)" in transient,
        "transient context tool must load raw file list",
        errors,
    )
    require(
        '"--content-file"' in sqlite_memory,
        "sqlite memory tool must accept content file",
        errors,
    )
    require(
        "content_text = read_arg_file(repo_root, args.content_file)" in sqlite_memory,
        "sqlite memory tool must load content file",
        errors,
    )
    require(
        "content=content_text" in sqlite_memory,
        "sqlite memory remember must use file-backed content",
        errors,
    )

    report = {
        "schema_version": 1,
        "kind": "heap_file_backed_request_startup_smoke",
        "passed": not errors,
        "errors": errors,
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
