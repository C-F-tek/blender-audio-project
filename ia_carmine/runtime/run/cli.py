"""Canonical non-GUI heap/universe operator run.

This command is the single operator product entry for the current heap/universe
product runtime:

``python -m ia_carmine.cli run --request-file <task.md>``
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from ia_carmine._shared.live_flow_monitor import CRLF_WARNING_RE
from ia_carmine.product.operator_product_core import LauncherConfig, OperatorProductController
from ia_carmine.product.operator_product_core.io_utils import now_stamp
from ia_carmine.product.operator_product_core.direct_command import resolve_config, resolve_project_python
from ia_carmine.runtime.run.dry_run_report import dry_run_report
from ia_carmine.runtime.run.preflight_files import PRODUCT_PREFLIGHT_FILES
from ia_carmine.runtime.run.universe_config import (
    ResolvedUniverseRunConfig,
    apply_resolved_config_to_args,
    launcher_config_metadata,
    resolve_universe_config,
)

DEFAULT_TASK_FILE = "IA-Carmine_GUI_launcher_final_code_product_task.md"
DEFAULT_INTERMEDIATE_ROOT = "output/validation/operator_product_launcher_lab"
DEFAULT_BRANCH = "codex/code-product-intake"

def default_task_md() -> Path:
    home = Path(os.environ.get("USERPROFILE") or Path.home())
    return home / "Downloads" / DEFAULT_TASK_FILE

def default_final_root(stamp: str) -> Path:
    return Path("output") / "validation" / stamp / "final_product"

def process_gate_task_path(repo_root: Path, stamp: str) -> Path:
    return repo_root / "output" / "local_ai_task_inputs" / f"heap-exchange-process-gate-{stamp}.md"

def write_process_gate_task(repo_root: Path, stamp: str) -> Path:
    task_path = process_gate_task_path(repo_root, stamp)
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(
        "\n".join(
            [
                f"# Heap Exchange Process Gate - {stamp}",
                "",
                "## Objective",
                "",
                "Execute the IA-Carmine product path through the canonical entrypoint.",
                "",
                "## Input Contract",
                "",
                "- Entrypoint: `python -m ia_carmine.cli run`.",
                "- Route: ia_carmine.runtime.run -> operator_product_core -> heap_context_closure -> completeness gate.",
                "- Provider universe roles are hard requirements for real product runs.",
                "- Use existing repo modules only; do not create a parallel runner, mode switch or storage layer.",
                "- Treat this Markdown as controlled task input; startup reload must convert useful context into structured heap evidence.",
                "",
                "## Required Runtime Evidence",
                "",
                "- Local request enters the heap runtime blackboard.",
                "- Startup context/memory reload writes structured manifest evidence.",
                "- GPU1 primary planner, GPU0 coworker/reviewer and NPU microtask auditor publish pointer-linked provider blocks.",
                "- Matrix/lab evidence validates concrete targets and patch candidates before final product acceptance.",
                "- Product exit is either reviewable code product evidence or `blocked_with_reason`.",
                "",
                "## Failure Policy",
                "",
                "A smoke, static report, package write or provider-only proposal is not product success.",
                "Missing GPU1/GPU0/NPU operational provider evidence is a contract failure, not a warning.",
                "Smoke/full-run wrappers are downstream verification, not entry commands.",
                "`patch_application_performed` remains false unless an explicit apply boundary is requested.",
                "",
            ]
        ),
        encoding="utf-8",
    )
    return task_path

def run_checked(command: list[str], *, cwd: Path) -> None:
    completed = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        check=False,
        capture_output=True,
    )
    suppressed = _print_filtered_output(completed.stdout or "", stream_name="stdout")
    suppressed += _print_filtered_output(completed.stderr or "", stream_name="stderr")
    if suppressed:
        print(f"[preflight] compressed {suppressed} git CRLF line-ending warnings")
    if completed.returncode != 0:
        raise SystemExit(f"command failed with exit code {completed.returncode}: {command}")


def _print_filtered_output(text: str, *, stream_name: str) -> int:
    suppressed = 0
    kept: list[str] = []
    for line in text.splitlines():
        if CRLF_WARNING_RE.match(line.strip()):
            suppressed += 1
        else:
            kept.append(line)
    if kept:
        print("\n".join(kept))
    return suppressed

def git_sync(repo_root: Path, branch: str) -> None:
    run_checked(["git", "fetch", "origin"], cwd=repo_root)
    run_checked(["git", "checkout", branch], cwd=repo_root)
    run_checked(["git", "pull", "--ff-only", "origin", branch], cwd=repo_root)
    run_checked(["git", "status", "--short"], cwd=repo_root)


def preflight(repo_root: Path, python_exe: str) -> None:
    run_checked([python_exe, "-m", "py_compile", *PRODUCT_PREFLIGHT_FILES], cwd=repo_root)
    run_checked(["git", "diff", "--check"], cwd=repo_root)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-RepoRoot", "--repo-root", dest="repo_root", default=".")
    parser.add_argument("--print-effective-config", action="store_true")
    parser.add_argument("--emit-expanded-command", action="store_true")
    parser.add_argument("--effective-config-output", default="")
    parser.add_argument(
        "-TaskFile",
        "--request-file",
        "--task-md",
        dest="request_file",
        default="",
    )
    parser.add_argument("-ProcessGateTask", dest="process_gate_task", action="store_true")
    parser.add_argument("--run-label", default="spark_direct")
    parser.add_argument("--intermediate-root", default=DEFAULT_INTERMEDIATE_ROOT)
    parser.add_argument("--final-root", default="")
    parser.add_argument("-PythonExe", "--python-exe", dest="python_exe", default="")
    parser.add_argument("-Stamp", "--stamp", dest="stamp", default="")
    parser.add_argument("--budget-minutes", type=int, default=None)
    parser.add_argument("--max-iterations", type=int, default=None)
    parser.add_argument("--min-runtime-rounds", type=int, default=None)
    parser.add_argument("--min-proposal-iterations", type=int, default=None)
    parser.add_argument("--max-rounds", type=int, default=None)
    parser.add_argument("--files-per-round", type=int, default=None)
    parser.add_argument("--max-provider-revisions", type=int, default=None)
    parser.add_argument("--preflight-timeout-seconds", type=int, default=None)
    parser.add_argument(
        "-Model",
        "--model",
        "--provider-model",
        dest="provider_model",
        default=None,
        help="Required for real provider runs: explicit GPU1/Ollama model for the heap provider lane.",
    )
    parser.add_argument("--gpu1-base-url", default=None)
    parser.add_argument("--gpu0-model", default=None)
    parser.add_argument("--gpu0-base-url", default=None)
    parser.add_argument("--gpu0-vulkan-visible-devices", default=None)
    parser.add_argument("--strict-provider-model", action="store_true")
    parser.add_argument("-MaxNewTokens", "--max-new-tokens", dest="max_new_tokens", type=int, default=None)
    parser.add_argument("--gpu0-max-new-tokens", dest="gpu0_max_new_tokens", type=int, default=None)
    parser.add_argument("--ollama-num-ctx", dest="ollama_num_ctx", type=int, default=None)
    parser.add_argument("--ollama-gpu-layers", "--ollama-num-gpu", dest="ollama_gpu_layers", default=None)
    parser.add_argument("--ollama-num-thread", dest="ollama_num_thread", type=int, default=None)
    parser.add_argument("--ollama-context-candidates", default=None)
    parser.add_argument("--gpu0-model-dir", default=None)
    parser.add_argument("--npu-model-dir", default=None)
    parser.add_argument("--operator-gpu-observation", default=None)
    parser.add_argument("-KeepAlive", "--keep-alive", dest="keep_alive", default=None)
    parser.add_argument("--gpu0-iterations", dest="gpu0_iterations", type=int, default=None)
    parser.add_argument("--gpu0-min-seconds", dest="gpu0_min_seconds", type=float, default=None)
    parser.add_argument("--npu-micro-timeout-seconds", dest="npu_micro_timeout_seconds", type=int, default=None)
    parser.add_argument("--npu-max-context-chars", dest="npu_max_context_chars", type=int, default=None)
    parser.add_argument("--npu-max-prompt-chars", dest="npu_max_prompt_chars", type=int, default=None)
    parser.add_argument("--npu-max-new-tokens", dest="npu_max_new_tokens", type=int, default=None)
    parser.add_argument("--npu-device-workload-seconds", type=float, default=None)
    parser.add_argument("--npu-device-workload-iterations", type=int, default=None)
    parser.add_argument("--startup-max-memory-chars", type=int, default=None)
    parser.add_argument("--startup-max-context-files", type=int, default=None)
    parser.add_argument("--startup-scan-context-files", type=int, default=None)
    parser.add_argument("--startup-max-chars-per-file", type=int, default=None)
    parser.add_argument("--rag-db", default=None)
    parser.add_argument("--rag-index-policy", choices=("auto", "always", "never"), default=None)
    parser.add_argument("--rag-embedding-endpoint", default=None)
    parser.add_argument("--rag-embedding-model", default=None)
    parser.add_argument("--rag-ingest-batch-size", type=int, default=None)
    parser.add_argument("--rag-embed-smoke-batch-size", type=int, default=None)
    parser.add_argument("--rag-chunk-min-chars", type=int, default=None)
    parser.add_argument("--rag-chunk-max-chars", type=int, default=None)
    parser.add_argument("--rag-chunk-overlap-chars", type=int, default=None)
    parser.add_argument("--rag-max-file-size", type=int, default=None)
    parser.add_argument("--rag-top-k", type=int, default=None)
    parser.add_argument("--rag-char-budget", type=int, default=None)
    parser.add_argument("--rag-allow-missing-embeddings", action="store_true")
    parser.add_argument("--context-document-count", dest="context_document_count", type=int, default=None)
    parser.add_argument(
        "--context-document-preview-chars",
        dest="context_document_preview_chars",
        type=int,
        default=None,
    )
    parser.add_argument("--semantic-code-chunk-limit", dest="semantic_code_chunk_limit", type=int, default=None)
    parser.add_argument(
        "--semantic-code-chunk-preview-chars",
        dest="semantic_code_chunk_preview_chars",
        type=int,
        default=None,
    )
    parser.add_argument(
        "--semantic-evidence-chunk-limit",
        dest="semantic_evidence_chunk_limit",
        type=int,
        default=None,
    )
    parser.add_argument("--memory-search-limit", dest="memory_search_limit", type=int, default=None)
    parser.add_argument("--tool-catalog-limit", dest="tool_catalog_limit", type=int, default=None)
    parser.add_argument("--startup-provider-input-workers", type=int, default=None)
    parser.add_argument("--startup-required-context-profile", default=None)
    parser.add_argument(
        "--startup-operational-memory-query",
        default=None,
    )
    parser.add_argument("--startup-operational-memory-limit", type=int, default=None)
    parser.add_argument("--tool-inventory-roots", default=None)
    parser.add_argument("--semantic-path-boosts", default=None)
    parser.add_argument("--ai-context-pack-profile", default=None)
    parser.add_argument("--code-interpreter-inputs", default=None)
    parser.add_argument("--duplication-audit-roots", default=None)
    parser.add_argument("--provider-prompt-tool-catalog-cap", type=int, default=None)
    parser.add_argument(
        "--allow-provider-generation",
        action="store_true",
        default=False,
        help="Compatibility flag; real runs request GPU1/GPU0/NPU provider generation by default.",
    )
    parser.add_argument(
        "--require-ollama-gpu-residency",
        action="store_true",
        default=False,
        help="Canonical run requires ollama ps accelerator proof for GPU1; CPU-only fallback is blocked.",
    )
    parser.add_argument(
        "--allow-npu-device-workload",
        dest="allow_npu_device_workload",
        action="store_true",
        default=False,
        help="Opt in to bounded NPU device workload; semantic NPU audit still runs without it.",
    )
    parser.add_argument("--skip-startup-reload", action="store_true")
    parser.add_argument("--strict-startup-reload", action="store_true")
    parser.add_argument("--no-documents", action="store_true")
    parser.add_argument("--revision-context", default=None)
    parser.add_argument("--revision-context-max-tasks", type=int, default=None)
    parser.add_argument("--timeout-seconds", type=int, default=None)
    parser.add_argument("--git-sync", action="store_true")
    parser.add_argument("--branch", default=DEFAULT_BRANCH)
    parser.add_argument("-DryRun", "--dry-run", dest="dry_run", action="store_true")
    return parser


def provided_dests(parser: argparse.ArgumentParser, argv: list[str]) -> set[str]:
    option_to_dest: dict[str, str] = {}
    for action in parser._actions:
        for option in action.option_strings:
            option_to_dest[option] = action.dest
    found: set[str] = set()
    for token in argv:
        if not token.startswith("-"):
            continue
        option = token.split("=", 1)[0]
        dest = option_to_dest.get(option)
        if dest:
            found.add(dest)
    return found
def resolve_request_file(args: argparse.Namespace, repo_root: Path, stamp: str) -> Path:
    if args.request_file:
        return Path(args.request_file)
    if args.process_gate_task:
        if args.dry_run:
            return process_gate_task_path(repo_root, stamp)
        return write_process_gate_task(repo_root, stamp)
    return default_task_md()


def build_config(
    args: argparse.Namespace,
    repo_root: Path,
    stamp: str,
    resolved_universe: ResolvedUniverseRunConfig,
) -> LauncherConfig:
    request_file = resolve_request_file(args, repo_root, stamp)
    final_root = Path(args.final_root) if args.final_root else default_final_root(stamp)
    metadata = launcher_config_metadata(resolved_universe)
    return LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=Path(args.intermediate_root),
        final_root=final_root,
        run_label=args.run_label,
        python_exe=args.python_exe,
        stamp=stamp,
        revision_context=args.revision_context,
        budget_minutes=args.budget_minutes,
        max_iterations=args.max_iterations,
        min_runtime_rounds=args.min_runtime_rounds,
        min_proposal_iterations=args.min_proposal_iterations,
        max_rounds=args.max_rounds,
        files_per_round=args.files_per_round,
        max_provider_revisions=args.max_provider_revisions,
        timeout_seconds=args.timeout_seconds,
        preflight_timeout_seconds=args.preflight_timeout_seconds,
        provider_model=args.provider_model,
        strict_provider_model=args.strict_provider_model,
        gpu1_base_url=args.gpu1_base_url,
        gpu0_model=args.gpu0_model,
        gpu0_base_url=args.gpu0_base_url,
        gpu0_vulkan_visible_devices=args.gpu0_vulkan_visible_devices,
        ollama_num_ctx=args.ollama_num_ctx,
        ollama_gpu_layers=args.ollama_gpu_layers,
        ollama_num_thread=args.ollama_num_thread,
        ollama_context_candidates=args.ollama_context_candidates,
        gpu0_model_dir=args.gpu0_model_dir,
        npu_model_dir=args.npu_model_dir,
        operator_gpu_observation=args.operator_gpu_observation,
        max_new_tokens=args.max_new_tokens,
        gpu0_max_new_tokens=args.gpu0_max_new_tokens,
        keep_alive=args.keep_alive,
        gpu0_iterations=args.gpu0_iterations,
        gpu0_min_seconds=args.gpu0_min_seconds,
        npu_micro_timeout_seconds=args.npu_micro_timeout_seconds,
        npu_max_context_chars=args.npu_max_context_chars,
        npu_max_prompt_chars=args.npu_max_prompt_chars,
        npu_max_new_tokens=args.npu_max_new_tokens,
        npu_device_workload_seconds=args.npu_device_workload_seconds,
        npu_device_workload_iterations=args.npu_device_workload_iterations,
        startup_max_memory_chars=args.startup_max_memory_chars,
        startup_max_context_files=args.startup_max_context_files,
        startup_scan_context_files=args.startup_scan_context_files,
        startup_max_chars_per_file=args.startup_max_chars_per_file,
        rag_db=args.rag_db,
        rag_index_policy=args.rag_index_policy,
        rag_embedding_endpoint=args.rag_embedding_endpoint,
        rag_embedding_model=args.rag_embedding_model,
        rag_ingest_batch_size=args.rag_ingest_batch_size,
        rag_embed_smoke_batch_size=args.rag_embed_smoke_batch_size,
        rag_chunk_min_chars=args.rag_chunk_min_chars,
        rag_chunk_max_chars=args.rag_chunk_max_chars,
        rag_chunk_overlap_chars=args.rag_chunk_overlap_chars,
        rag_max_file_size=args.rag_max_file_size,
        rag_top_k=args.rag_top_k,
        rag_char_budget=args.rag_char_budget,
        rag_allow_missing_embeddings=args.rag_allow_missing_embeddings,
        context_document_count=args.context_document_count,
        context_document_preview_chars=args.context_document_preview_chars,
        semantic_code_chunk_limit=args.semantic_code_chunk_limit,
        semantic_code_chunk_preview_chars=args.semantic_code_chunk_preview_chars,
        semantic_evidence_chunk_limit=args.semantic_evidence_chunk_limit,
        memory_search_limit=args.memory_search_limit,
        tool_catalog_limit=args.tool_catalog_limit,
        revision_context_max_tasks=args.revision_context_max_tasks,
        startup_provider_input_workers=args.startup_provider_input_workers,
        startup_required_context_profile=args.startup_required_context_profile,
        startup_operational_memory_query=args.startup_operational_memory_query,
        startup_operational_memory_limit=args.startup_operational_memory_limit,
        tool_inventory_roots=args.tool_inventory_roots,
        semantic_path_boosts=args.semantic_path_boosts,
        ai_context_pack_profile=args.ai_context_pack_profile,
        code_interpreter_inputs=args.code_interpreter_inputs,
        duplication_audit_roots=args.duplication_audit_roots,
        provider_prompt_tool_catalog_cap=args.provider_prompt_tool_catalog_cap,
        allow_provider_generation=args.allow_provider_generation,
        require_ollama_gpu_residency=args.require_ollama_gpu_residency,
        allow_npu_device_workload=args.allow_npu_device_workload,
        skip_startup_reload=args.skip_startup_reload,
        strict_startup_reload=args.strict_startup_reload,
        no_documents=args.no_documents,
        effective_universe_config=metadata["effective_universe_config"],
        field_sources=metadata["field_sources"],
    )


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    args = parser.parse_args(raw_argv)
    repo_root = Path(args.repo_root).resolve()
    supplied_dests = provided_dests(parser, raw_argv)
    resolved_universe = resolve_universe_config(
        repo_root=repo_root,
        args=args,
        provided_dests=supplied_dests,
    )
    apply_resolved_config_to_args(args, resolved_universe)

    stamp = args.stamp or now_stamp()
    config = build_config(args, repo_root, stamp, resolved_universe)
    cfg = resolve_config(config)
    python_exe = resolve_project_python(repo_root, args.python_exe)
    plan_only = bool(args.dry_run or args.print_effective_config or args.emit_expanded_command)

    if not cfg.request_file.exists() and not plan_only:
        raise SystemExit(f"Task markdown not found: {cfg.request_file}")
    if args.git_sync:
        if plan_only:
            print(f"[dry-run] would sync origin/{args.branch}")
        else:
            git_sync(repo_root, args.branch)
    if not plan_only:
        preflight(repo_root, python_exe)

    if plan_only:
        report = dry_run_report(config)
        if args.effective_config_output:
            output = Path(args.effective_config_output)
            if not output.is_absolute():
                output = repo_root / output
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if args.print_effective_config or args.emit_expanded_command or args.dry_run:
            print(json.dumps(report, indent=2, ensure_ascii=False))
        if args.print_effective_config or args.emit_expanded_command:
            return 0
        return 0

    controller = OperatorProductController(config)
    report = controller.run(timeout=args.timeout_seconds)
    report.update(
        {
            "canonical_entrypoint": "python -m ia_carmine.cli run",
            "single_product_entry": True,
            "parallel_product_entry": False,
            "smoke_product_entry": False,
            "python_exe": python_exe,
            "internal_runtime": "ia_carmine.product.operator_product_core.OperatorProductController",
            "heap_runtime": "ia_carmine.runtime.heap_context_closure",
        }
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report.get("passed") is True else 2

if __name__ == "__main__":
    raise SystemExit(main())
