#!/usr/bin/env python3
"""Smoke-test file-backed heap request/startup transport surfaces."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[4]


def read(repo_root: Path, rel_path: str) -> str:
    return (repo_root / rel_path).read_text(encoding="utf-8")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def build_report(repo_root: Path) -> dict[str, object]:
    errors: list[str] = []
    launcher = "\n".join(
        [
            read(repo_root, "ia_carmine/runtime/heap_context_closure/launcher.py"),
            read(repo_root, "ia_carmine/runtime/heap_context_closure/commands.py"),
        ]
    )
    prepare = "\n".join(
        [
            read(repo_root, "ia_carmine/context/heap_context_memory_reload/cli.py"),
            read(repo_root, "ia_carmine/context/heap_context_memory_reload/runner.py"),
            read(repo_root, "ia_carmine/context/heap_context_memory_reload/memory_write.py"),
        ]
    )
    gate = "\n".join(
        [
            read(repo_root, "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py"),
            read(repo_root, "ia_carmine/runtime/heap_gate/runtime_init.py"),
            read(repo_root, "ia_carmine/runtime/heap_gate/runtime_common.py"),
        ]
    )
    transient = read(repo_root, "ia_carmine/context/agent_context/transient_request_context/cli.py")
    sqlite_memory = "\n".join(
        [
            read(repo_root, "ia_carmine/memory/agent_memory/sqlite_cli.py"),
            read(repo_root, "ia_carmine/memory/agent_memory/sqlite_report.py"),
        ]
    )
    file_transport = read(repo_root, "ia_carmine/_shared/file_backed_transport.py")
    startup_runner = read(repo_root, "ia_carmine/context/heap_context_memory_reload/runner.py")
    startup_manifest = read(repo_root, "ia_carmine/context/heap_context_memory_reload/manifest.py")
    rag_startup = read(repo_root, "ia_carmine/context/heap_context_memory_reload/rag_startup.py")
    gpu1_dynamic_pack = read(repo_root, "ia_carmine/context/heap_context_memory_reload/dynamic_gpu1_context.py")
    provider_prompt = read(repo_root, "ia_carmine/runtime/heap_gate/provider_prompt.py")

    require(
        '"request_transport"] = "heap_augmented_request_file"' in launcher
        and '"heap_augmented_request.md"' in launcher
        and '"heap_request_file"' in launcher,
        "launcher must materialize the augmented heap request as the active request artifact",
        errors,
    )
    require(
        "http_coordinates_filesystem_transports_mass" in file_transport
        and "write_transport_manifest" in file_transport
        and "read_json_windows_safe" in file_transport,
        "shared file-backed transport helper must define manifest/checksum/Windows-safe readers",
        errors,
    )
    require(
        "_materialize_startup_request(state)" in startup_runner
        and 'state.output_dir / "payload"' in startup_runner
        and '"startup_request_file"' in startup_runner,
        "startup reload must materialize the operator request as a run payload artifact",
        errors,
    )
    require(
        'state.artifacts.get("startup_request_file")' in rag_startup
        and 'state.request_text[:4000]' not in rag_startup,
        "RAG startup must consume the request artifact instead of a sliced inline query",
        errors,
    )
    require(
        '"request_ref": request_ref' in startup_manifest
        and '"request_preview"' not in startup_manifest,
        "startup manifest must expose request_ref metadata instead of request_preview",
        errors,
    )
    require(
        "ia_carmine_runtime_payload_manifest" in gpu1_dynamic_pack
        and '"payload_manifest_ref"' in gpu1_dynamic_pack
        and '"no_operational_excerpts": True' in gpu1_dynamic_pack,
        "GPU1 dynamic context pack must write a file-backed runtime payload manifest",
        errors,
    )
    require(
        "STARTUP_CONTEXT_REFS_FOR_GPU1" in provider_prompt
        and "file_backed_artifact_refs" in provider_prompt
        and "artifact_reference_with_excerpt" not in provider_prompt
        and "excerpt only" not in provider_prompt,
        "GPU1 startup prompt digest must be ref-only and not operational excerpts",
        errors,
    )
    require(
        "def request_args" in launcher
        and 'state.get("heap_request_file")' in launcher
        and '"--request-file"' in launcher,
        "launcher child commands must prefer the generated heap request artifact",
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
        '"--content-file"' in prepare and "startup_operational_memory_write_input.md" in prepare,
        "startup reload must pass operational memory content as a file-backed payload",
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

    return {
        "schema_version": 1,
        "kind": "heap_file_backed_request_startup_smoke",
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default="")
    parser.add_argument("--output", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(args.repo_root).resolve() if args.repo_root else default_repo_root()
    report = build_report(repo_root)

    if args.output:
        output = Path(args.output)
        if not output.is_absolute():
            output = repo_root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
