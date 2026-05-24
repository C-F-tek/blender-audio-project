#!/usr/bin/env python3
"""Smoke-test IA-Carmine file-backed transport invariants."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

from Tools.validation.runtime_tool.run_file_backed_transport_contract_smoke.helpers import (
    blackboard_broker_transport_errors,
    fake_ollama_report_context,
    legacy_dispatch_absent_errors,
    strict_text_accessor_errors,
)


def read(repo_root: Path, rel_path: str) -> str:
    return (repo_root / rel_path).read_text(encoding="utf-8-sig")


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def build_report(repo_root: Path) -> dict[str, object]:
    from ia_carmine._shared.file_backed_transport import (
        INLINE_TEXT_MAX_CHARS,
        MAX_FILE_WINDOW_CHARS,
        artifact_ref,
        validate_runtime_payload_manifest,
    )
    from ia_carmine._shared.provider_ollama_report import build_ollama_probe_report
    from ia_carmine.runtime.runtime_tool.agent_runtime_debug_lab.cli import load_request_json
    from ia_carmine.runtime.runtime_tool.broker.context_builders import runtime_sqlite_memory
    from ia_carmine.runtime.runtime_tool.broker.executor import (
        load_requests_data,
        materialize_transport_args,
    )
    from ia_carmine.runtime.runtime_tool.generic_write.cli import (
        build_report as build_generic_write_report,
    )

    files = {
        "transport": "ia_carmine/_shared/file_backed_transport.py",
        "provider_prompt": "ia_carmine/runtime/heap_gate/provider_prompt.py",
        "runtime_builders": "ia_carmine/runtime/runtime_tool/broker/runtime_builders.py",
        "broker_executor": "ia_carmine/runtime/runtime_tool/broker/executor.py",
        "provider_tool_loop": "ia_carmine/_shared/provider_tool_loop.py",
        "startup_manifest": "ia_carmine/context/heap_context_memory_reload/manifest.py",
        "startup_task_docs": "ia_carmine/context/heap_context_memory_reload/task_docs.py",
        "rag_startup": "ia_carmine/context/heap_context_memory_reload/rag_startup.py",
        "dynamic_gpu1_context": "ia_carmine/context/heap_context_memory_reload/dynamic_gpu1_context.py",
        "provider_ollama_report": "ia_carmine/_shared/provider_ollama_report.py",
        "provider_ollama_probe": "ia_carmine/_shared/provider_ollama_probe.py",
        "local_provider_probe": "ia_carmine/providers/provider_mesh/local_provider_probe/cli.py",
        "file_window": "ia_carmine/runtime/runtime_tool/file_window/cli.py",
        "broker_registry": "ia_carmine/runtime/runtime_tool/broker/registry.py",
        "blackboard": "ia_carmine/runtime/provider_runtime_blackboard/cli.py",
        "blackboard_heap": "ia_carmine/runtime/provider_runtime_blackboard/heap.py",
        "blackboard_bridge": "ia_carmine/runtime/provider_runtime_blackboard/broker_bridge/cli.py",
        "context_builders": "ia_carmine/runtime/runtime_tool/broker/context_builders.py",
        "sqlite_report": "ia_carmine/memory/agent_memory/sqlite_report.py",
        "startup_common": "ia_carmine/context/heap_context_memory_reload/common.py",
        "debug_lab": "ia_carmine/runtime/runtime_tool/agent_runtime_debug_lab/cli.py",
        "generic_write": "ia_carmine/runtime/runtime_tool/generic_write/cli.py",
        "provider_context": "ia_carmine/runtime/heap_gate/provider_context.py",
        "run_loop": "ia_carmine/runtime/heap_gate/run_loop.py",
        "arbiter_product": "ia_carmine/runtime/heap_gate/arbiter_product.py",
        "heap_exchange": "ia_carmine/runtime/heap_gate/heap_exchange.py",
        "proposal_cycle_a": "ia_carmine/runtime/heap_gate/proposal_cycle_a.py",
        "provider_report_absorption": "ia_carmine/runtime/heap_gate/provider_report_absorption.py",
        "openvino_npu_probe": "ia_carmine/providers/provider_mesh/openvino_npu_model_probe/cli.py",
        "ollama_gpu0_peer": "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py",
        "ia_dispatch": "ia_carmine/dispatch.py",
        "validation_dispatch": "Tools/validation/dispatch.py",
        "current_contract": "docs/CURRENT_RUNTIME_MARKDOWN_CONTRACT.md",
        "agents": "AGENTS.md",
        "chatgpt": "CHATGPT.md",
        "runtime_tool_context": "ia_carmine/runtime/runtime_tool/TOOL_CONTEXT.md",
        "heap_gate_context": "ia_carmine/runtime/heap_gate/TOOL_CONTEXT.md",
        "provider_teamwork_packet": "ia_carmine/runtime/heap_gate/provider_teamwork_packet.py",
        "provider_command_specs": "ia_carmine/runtime/heap_gate/provider_command_specs.py",
    }
    source = {key: read(repo_root, path) for key, path in files.items()}
    errors: list[str] = []
    smoke_dir = repo_root / "output" / "validation" / "file_backed_transport_contract_smoke"
    smoke_dir.mkdir(parents=True, exist_ok=True)

    require(
        "write_transport_manifest" in source["transport"]
        and "artifact_ref" in source["transport"]
        and "read_json_windows_safe" in source["transport"],
        "file-backed transport helper must expose manifest refs, artifact refs and Windows-safe readers",
        errors,
    )
    require(
        "write_large_text_evidence" in source["transport"]
        and "full_text_in_json" in source["transport"],
        "file-backed transport helper must expose a shared JSON-safe large text evidence writer",
        errors,
    )
    require(
        '"source": source or producer or "unknown"' in source["transport"]
        and "validate_runtime_payload_manifest" in source["transport"],
        "artifact refs must include source/provenance and manifests must be checksum-validatable",
        errors,
    )
    require(
        "STARTUP_CONTEXT_REFS_FOR_GPU1" in source["provider_prompt"]
        and "file_backed_artifact_refs" in source["provider_prompt"],
        "provider startup digest must be an artifact-ref control surface",
        errors,
    )
    require(
        "artifact_reference_with_excerpt" not in source["provider_prompt"]
        and "excerpt only" not in source["provider_prompt"],
        "provider startup digest must not return operational excerpts",
        errors,
    )
    require(
        "chunk[:4000]" not in source["runtime_builders"]
        and 'command.extend(["--text-file", str(ref["path"])])' in source["runtime_builders"],
        "runtime_file_refs must materialize inline text as --text-file without chunk slicing",
        errors,
    )
    require(
        "TEXT_ARG_FILE_TARGETS" in source["broker_executor"]
        and "write_text_artifact" in source["broker_executor"]
        and "write_json_artifact" in source["broker_executor"],
        "broker executor must materialize text/json payload args before validation/execution",
        errors,
    )
    require(
        "prompt[:3500]" not in source["provider_tool_loop"]
        and "provider_delta[:1800]" not in source["provider_tool_loop"]
        and "runtime_file_window" in source["provider_tool_loop"],
        "provider tool selection prompt must not slice prompt/provider delta and must expose file windows",
        errors,
    )
    require(
        '"request_preview"' not in source["startup_manifest"]
        and '"request_ref": request_ref' in source["startup_manifest"],
        "startup manifest must use request_ref instead of request_preview",
        errors,
    )
    require(
        '"request_preview"' not in source["startup_task_docs"]
        and '"request_file": artifacts.get("startup_request_file", "")' in source["startup_task_docs"],
        "startup operational memory note must use request file refs instead of request excerpts",
        errors,
    )
    require(
        "state.request_text[:4000]" not in source["rag_startup"]
        and 'state.artifacts.get("startup_request_file")' in source["rag_startup"],
        "RAG startup must use task-file refs and not sliced request text",
        errors,
    )
    require(
        "ia_carmine_runtime_payload_manifest" in source["dynamic_gpu1_context"]
        and '"payload_manifest_ref"' in source["dynamic_gpu1_context"]
        and '"payload_manifest_validation"' in source["dynamic_gpu1_context"]
        and '"source": ref.get("source")' in source["dynamic_gpu1_context"]
        and '"no_operational_excerpts": True' in source["dynamic_gpu1_context"],
        "dynamic GPU1 pack must publish a payload manifest and no-operational-excerpts policy",
        errors,
    )
    require(
        '"request_prompt": prompt' not in source["provider_ollama_report"]
        and '"request_prompt": prompt or ""' not in source["provider_ollama_probe"]
        and "request_prompt_ref" in source["provider_ollama_report"]
        and "request_prompt_sha256" in source["provider_ollama_report"]
        and "materialize_provider_prompt" in source["local_provider_probe"],
        "Ollama reports must expose request_prompt refs/checksums, not the prompt body",
        errors,
    )
    require(
        "read_text_window_bytes" in source["file_window"]
        and "runtime_file_window_path_outside_repo_root" in source["file_window"]
        and "MAX_FILE_WINDOW_CHARS" in source["file_window"]
        and "read_text_windows_safe(target)" not in source["file_window"],
        "runtime_file_window must be repo-bound and stream a bounded window instead of reading whole files",
        errors,
    )
    require(
        '"maximum": MAX_FILE_WINDOW_CHARS' in source["broker_registry"]
        and '"content_file"' in source["broker_registry"]
        and '"content": STRING' not in source["broker_registry"],
        "tool schemas must bound runtime_file_window.limit and expose only runtime_sqlite_memory.content_file",
        errors,
    )
    require(
        "content_inline_requires_content_file" in source["sqlite_report"],
        "runtime_sqlite_memory CLI/report must reject inline remember content and require content_file",
        errors,
    )
    require(
        "json_safe_coordination_payload" in source["provider_context"]
        and "provider_response_refs_or_tails" in source["provider_context"]
        and "request_input_ref_or_tail" in source["provider_context"],
        "provider context must expose JSON-safe refs/tails helpers for reports and prompts",
        errors,
    )
    require(
        '"request_input": self.request_text()' not in source["run_loop"]
        and '"response_text": final_response_text' not in source["run_loop"]
        and '"provider_reports": self.provider_reports,' not in source["run_loop"]
        and "provider_reports_refs_or_tails()" in source["run_loop"],
        "heap run_loop report JSON must use refs/tails and sanitized provider reports",
        errors,
    )
    require(
        '"request_input": owner.request_text()' not in source["arbiter_product"]
        and '"provider_response_texts": owner.provider_response_texts()' not in source["arbiter_product"]
        and "provider_response_refs_or_tails" in source["arbiter_product"],
        "arbiter product JSON must use refs/tails instead of full provider text maps",
        errors,
    )
    require(
        '"request": self.request_text()' not in source["heap_exchange"]
        and '"provider_contributions": self.provider_response_texts()' not in source["heap_exchange"]
        and "provider_contribution_refs_or_tails" in source["heap_exchange"],
        "heap exchange JSON must use refs/tails for request and provider contributions",
        errors,
    )
    require(
        '"gpu1_free_text_evidence": response_text' not in source["proposal_cycle_a"]
        and '"gpu1_free_text_evidence", gpu1_free_text_evidence' in source["proposal_cycle_a"]
        and '"response_text_preview"' in source["proposal_cycle_a"],
        "proposal iteration JSON must store GPU1 free text as ref/hash/tail, not full text",
        errors,
    )
    require(
        '"observed_request": gate.request_text()' not in source["provider_report_absorption"]
        and '"observed_response": provider_report.get("response_text")' not in source["provider_report_absorption"]
        and "observed_response_evidence" in source["provider_report_absorption"],
        "provider claim absorption must publish observed request/response refs instead of full text",
        errors,
    )
    require(
        '"request_prompt": args.prompt' not in source["openvino_npu_probe"]
        and "request_prompt_ref" in source["openvino_npu_probe"],
        "OpenVINO NPU report must not write request_prompt inline",
        errors,
    )
    require(
        "prompt_ref=prompt_evidence.get" in source["ollama_gpu0_peer"],
        "GPU0 Ollama peer report must pass a prompt artifact ref to the Ollama probe",
        errors,
    )
    require(
        "payload_json_large_requires_payload_file" in source["blackboard"]
        and "payload_ref=payload_ref" in source["blackboard"],
        "provider runtime blackboard must reject large inline payloads and preserve payload_ref evidence",
        errors,
    )
    require(
        "validate_runtime_payload_manifest" in source["blackboard"]
        and "payload_manifest_invalid" in source["blackboard"],
        "provider runtime blackboard must validate runtime payload manifests on --payload-file ingress",
        errors,
    )
    require(
        '"request": gate.request_text()' not in source["provider_teamwork_packet"]
        and "leader_prompt_excerpt" not in source["provider_teamwork_packet"]
        and 'gate, "request"' in source["provider_teamwork_packet"]
        and 'gate, "leader_prompt"' in source["provider_teamwork_packet"]
        and '["--request", gate.request_text()]' not in source["provider_command_specs"],
        "provider packet/commands must use request and leader prompt artifact refs, not inline payloads",
        errors,
    )
    require(
        '"tool": str(raw_payload.get("tool") or "")' in source["blackboard_heap"]
        and '"args_keys": sorted(str(key) for key in args)[:32]' in source["blackboard_heap"]
        and "_payload_from_ref" in source["blackboard_bridge"]
        and "payload_ref_sha256_mismatch" in source["blackboard_bridge"],
        "file-backed broker_request events must keep an executable envelope and hydrate payload_ref with checksum verification",
        errors,
    )
    require(
        "request_json_large_requires_request_file" in source["broker_executor"],
        "broker must reject large inline --request-json with request_json_large_requires_request_file",
        errors,
    )
    require(
        "read_text_window_bytes" in source["startup_common"]
        and "text[:max_chars]" not in source["startup_common"],
        "startup bounded previews must read a bounded byte window instead of full file then slicing",
        errors,
    )
    require(
        "request_json_large_requires_request_file" in source["debug_lab"]
        and "INLINE_TEXT_MAX_CHARS" in source["debug_lab"],
        "agent_runtime_debug_lab direct CLI must reject large inline --request-json",
        errors,
    )
    require(
        '"refined_request": refined_request' not in source["generic_write"]
        and "refined_request_ref" in source["generic_write"]
        and "write_large_text_evidence" in source["generic_write"],
        "generic_write JSON report must store refined_request as ref/hash/tail, not full text",
        errors,
    )
    require(
        '"runtime_sqlite_memory": {"content": "content_file"}' in source["broker_executor"]
        and '"--content-file"' in source["context_builders"]
        and '("content", "--content")' not in source["context_builders"],
        "runtime_sqlite_memory content must be materialized as --content-file",
        errors,
    )
    require(
        "LEGACY_NON_RUN_UNICA_COMMANDS" in source["ia_dispatch"]
        and "LEGACY_NON_RUN_UNICA_VALIDATION_COMMANDS" in source["validation_dispatch"],
        "legacy provider/gateway commands must be explicitly marked non-run-unica",
        errors,
    )

    prompt = "PROMPT-BODY-" + ("x" * 100_000)
    fake_ctx = fake_ollama_report_context(repo_root, prompt)
    prompt_report = build_ollama_probe_report(fake_ctx)
    require(
        prompt_report.get("request_prompt_chars") == len(prompt)
        and prompt_report.get("request_prompt_sha256")
        and prompt_report.get("request_prompt") != prompt
        and "request_prompt" not in prompt_report,
        "large prompt report must contain chars/hash/ref metadata and not the prompt body",
        errors,
    )
    big_response = "RESPONSE-BODY-" + ("y" * 100_000)
    response_report = build_ollama_probe_report(
        fake_ollama_report_context(repo_root, prompt="prompt", response_text=big_response)
    )
    response_ref = response_report.get("response_text_ref")
    short_response = build_ollama_probe_report(
        fake_ollama_report_context(repo_root, prompt="prompt", response_text="ok")
    )
    require(
        response_report.get("response_text_chars") == len(big_response)
        and response_report.get("response_text_sha256")
        and isinstance(response_ref, dict)
        and bool(response_ref.get("sha256"))
        and response_report.get("response_text") != big_response
        and "response_text" not in response_report,
        "large provider response report must contain ref/hash/tail metadata and not the response body",
        errors,
    )
    require(
        "response_text" not in short_response
        and bool(short_response.get("response_text_ref", {}).get("sha256")),
        "short provider response report must also be artifact-backed",
        errors,
    )

    manifest_file = smoke_dir / "manifest_artifact.txt"
    manifest_file.write_text("manifest validator body", encoding="utf-8")
    good_ref = artifact_ref(
        manifest_file,
        repo_root,
        kind="smoke_manifest_artifact",
        producer="file_backed_transport_contract_smoke",
    )
    good_manifest = smoke_dir / "manifest_good.json"
    good_manifest.write_text(
        json.dumps({
            "schema_version": 1,
            "kind": "ia_carmine_runtime_payload_manifest",
            "job_id": "file-backed-smoke",
            "run_dir": str(smoke_dir.relative_to(repo_root)).replace("\\", "/"),
            "artifact_refs": [good_ref],
        }, indent=2)
        + "\n",
        encoding="utf-8",
    )
    bad_ref = dict(good_ref)
    bad_ref["bytes"] = int(bad_ref.get("bytes") or 0) + 1
    bad_manifest = smoke_dir / "manifest_bad.json"
    bad_manifest.write_text(
        json.dumps({
            "schema_version": 1,
            "kind": "ia_carmine_runtime_payload_manifest",
            "job_id": "file-backed-smoke",
            "run_dir": str(smoke_dir.relative_to(repo_root)).replace("\\", "/"),
            "artifact_refs": [bad_ref],
        }, indent=2)
        + "\n",
        encoding="utf-8",
    )
    require(
        validate_runtime_payload_manifest(repo_root, good_manifest).get("passed") is True
        and validate_runtime_payload_manifest(repo_root, bad_manifest).get("passed") is False,
        "manifest validator must pass valid refs and block corrupted bytes/sha metadata",
        errors,
    )

    valid_window_file = smoke_dir / "window.txt"
    valid_window_file.write_text("0123456789" * 2000, encoding="utf-8")
    window_ok = subprocess.run(
        [
            sys.executable,
            "-m",
            "ia_carmine",
            "runtime_file_window",
            "--repo-root",
            str(repo_root),
            "--path",
            str(valid_window_file.relative_to(repo_root)),
            "--offset",
            "10",
            "--limit",
            "32",
            "--output",
            str(smoke_dir / "runtime_file_window_ok.json"),
            "--markdown-output",
            str(smoke_dir / "runtime_file_window_ok.md"),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    window_limit_fail = subprocess.run(
        [
            sys.executable,
            "-m",
            "ia_carmine",
            "runtime_file_window",
            "--repo-root",
            str(repo_root),
            "--path",
            str(valid_window_file.relative_to(repo_root)),
            "--limit",
            str(MAX_FILE_WINDOW_CHARS + 1),
            "--output",
            str(smoke_dir / "runtime_file_window_limit.json"),
            "--markdown-output",
            str(smoke_dir / "runtime_file_window_limit.md"),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    outside_path = (repo_root.parent / "__outside_runtime_file_window_smoke__.txt").resolve()
    window_outside_fail = subprocess.run(
        [
            sys.executable,
            "-m",
            "ia_carmine",
            "runtime_file_window",
            "--repo-root",
            str(repo_root),
            "--path",
            str(outside_path),
            "--limit",
            "32",
            "--output",
            str(smoke_dir / "runtime_file_window_outside.json"),
            "--markdown-output",
            str(smoke_dir / "runtime_file_window_outside.md"),
        ],
        cwd=repo_root,
        text=True,
        capture_output=True,
    )
    require(
        window_ok.returncode == 0
        and window_limit_fail.returncode != 0
        and window_outside_fail.returncode != 0,
        "runtime_file_window must pass repo artifacts and reject oversize limits/outside absolute paths",
        errors,
    )

    errors.extend(blackboard_broker_transport_errors(repo_root, smoke_dir))

    large_request_data, _, _, large_request_errors = load_requests_data(
        repo_root,
        SimpleNamespace(
            request_data=None,
            request_packet=None,
            request_json='{"body":"' + ("x" * (INLINE_TEXT_MAX_CHARS + 1)) + '"}',
            request_file="",
            payload_file="",
        ),
    )
    sqlite_args = {"content": "memory body"}
    sqlite_refs = materialize_transport_args(
        repo_root=repo_root,
        out_dir=smoke_dir,
        request_id="sqlite_memory",
        tool_name="runtime_sqlite_memory",
        request_args=sqlite_args,
    )
    sqlite_command, _ = runtime_sqlite_memory(repo_root, smoke_dir, "sqlite_memory", {"content": "memory body"})
    require(
        not large_request_data
        and "request_json_large_requires_request_file" in large_request_errors
        and sqlite_args.get("content_file")
        and sqlite_refs
        and "--content-file" in sqlite_command
        and "--content" not in sqlite_command,
        "broker must reject large request_json and route runtime_sqlite_memory.content through content_file",
        errors,
    )
    _large_debug_request, large_debug_error = load_request_json(
        '{"body":"' + ("x" * (INLINE_TEXT_MAX_CHARS + 1)) + '"}'
    )
    generic_provider = smoke_dir / "generic_provider.json"
    generic_provider.write_text(
        json.dumps(
            {
                "lane": "gpu1_planner",
                "revision": 1,
                "passed": True,
                "provider_execution_performed": True,
                "provider_work_verified": True,
                "response_text": "provider generic write text",
                "native_tool_call_count": 0,
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )
    generic_report = build_generic_write_report(
        SimpleNamespace(
            repo_root=str(repo_root),
            request_file="",
            operator_request="operator request",
            provider_report=str(generic_provider.relative_to(repo_root)),
            proposal_text="",
            proposal_text_file="",
            capture_mode="no_tool_capture",
            evidence_report=[],
            source_lane="gpu1_planner",
            source_revision="1",
            gpu1_followup_required="",
            peer_followup_required="",
            provider_role="",
            reason="smoke",
            output=str((smoke_dir / "generic_write.json").relative_to(repo_root)),
        )
    )
    require(
        large_debug_error == "request_json_large_requires_request_file"
        and "refined_request" not in generic_report
        and bool(generic_report.get("refined_request_ref", {}).get("sha256"))
        and bool(generic_report.get("refined_request_tail")),
        "direct debug lab must reject large inline JSON and generic_write must emit refined_request ref/tail",
        errors,
    )

    errors.extend(legacy_dispatch_absent_errors())
    errors.extend(strict_text_accessor_errors(repo_root, smoke_dir))
    docs_phrase = "HTTP/API coordinates"
    for key in ("current_contract", "agents", "chatgpt", "runtime_tool_context", "heap_gate_context"):
        require(
            docs_phrase in source[key] and "ia_carmine_runtime_payload_manifest" in source[key],
            f"{files[key]} must document HTTP coordinates / filesystem transports mass",
            errors,
        )
    return {
        "schema_version": 1,
        "kind": "file_backed_transport_contract_smoke",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "repo_root": repo_root.as_posix(),
        "passed": not errors,
        "errors": errors,
        "warnings": [],
        "provider_execution_performed": False,
        "patch_application_performed": False,
        "source_writes_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/file_backed_transport_contract_smoke.json")
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    report = build_report(repo_root)
    output = Path(args.output)
    if not output.is_absolute():
        output = repo_root / output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
