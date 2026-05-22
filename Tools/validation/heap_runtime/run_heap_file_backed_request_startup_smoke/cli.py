#!/usr/bin/env python3
"""Smoke-test heap request/startup plumbing without runtime memory transport files."""

from __future__ import annotations

import json
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read(rel_path: str) -> str:
    return (repo_root() / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    launcher = "\n".join(
        [
            read("ia_carmine/runtime/heap_context_closure/launcher.py"),
            read("ia_carmine/runtime/heap_context_closure/commands.py"),
        ]
    )
    prepare = "\n".join(
        [
            read("ia_carmine/context/heap_context_memory_reload/cli.py"),
            read("ia_carmine/context/heap_context_memory_reload/runner.py"),
            read("ia_carmine/context/heap_context_memory_reload/memory_write.py"),
        ]
    )
    gate = "\n".join(
        [
            read("ia_carmine/runtime/heap_runtime/completeness_gate/cli.py"),
            read("ia_carmine/runtime/heap_gate/runtime_init.py"),
            read("ia_carmine/runtime/heap_gate/runtime_common.py"),
        ]
    )
    transient = read("ia_carmine/context/agent_context/transient_request_context/cli.py")
    sqlite_memory = "\n".join(
        [
            read("ia_carmine/memory/agent_memory/sqlite_cli.py"),
            read("ia_carmine/memory/agent_memory/sqlite_report.py"),
        ]
    )

    require(
        '"request_transport"] = "inline_cli"' in launcher,
        "launcher must not write a generated runtime request file",
        errors,
    )
    require(
        "def request_args" in launcher
        and '"--request-file"' in launcher
        and '"--request"' in launcher,
        "launcher must use operator request-file when present and inline only for small direct requests",
        errors,
    )
    require(
        'state["heap_request_file"].write_text' not in launcher,
        "launcher must not write heap_operator_request.md as runtime transport",
        errors,
    )
    require(
        '"--request-file"' in prepare,
        "startup reload must accept --request-file",
        errors,
    )
    require(
        "build_transient_context(context_args)" in prepare
        and 'memory_note=[state.request_text or "heap startup request"]' in prepare,
        "startup reload must pass transient request note in memory",
        errors,
    )
    require(
        "raw_file=raw_files" in prepare,
        "startup reload must pass existing raw files in memory",
        errors,
    )
    require(
        '"--raw-file-list"' not in prepare,
        "startup reload must not create a raw-file-list transport file",
        errors,
    )
    require(
        '"startup_context_raw_file_count"' in prepare,
        "startup reload must record raw-file count without a transport file",
        errors,
    )
    require(
        '"--memory-note-file",' not in prepare,
        "startup reload must not pass transient memory note by file",
        errors,
    )
    require(
        "build_sqlite_memory_report(memory_args)" in prepare and "content=content" in prepare,
        "startup reload must pass operational memory content in memory to SQLite memory",
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
