#!/usr/bin/env python3
"""Guard against runtime target/script-gaming hardcodes."""

from __future__ import annotations

import argparse
import importlib
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any

CORE_RUNTIME_GUARD = True


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def read(repo_root: Path, rel: str) -> str:
    return (repo_root / rel).read_text(encoding="utf-8-sig", errors="replace")


def check_absent(text: str, needle: str, rel: str, errors: list[str], reason: str) -> None:
    if needle in text:
        errors.append(f"{rel}: {reason}: {needle}")


def tuple_block(text: str, name: str) -> str:
    match = re.search(rf"{re.escape(name)}\s*=\s*\((.*?)\)", text, re.DOTALL)
    return match.group(1) if match else ""


def build_report(repo_root: Path) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    files = {
        rel: read(repo_root, rel)
        for rel in (
            "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py",
            "ia_carmine/runtime/heap_runtime/virtual_dev_environment/cli.py",
            "ia_carmine/_shared/heap_code_execution_tool_core.py",
            "ia_carmine/_shared/heap_final_code_product.py",
            "ia_carmine/runtime/heap_gate/target_planner.py",
            "ia_carmine/runtime/heap_gate/provider_command_specs.py",
            "ia_carmine/runtime/heap_gate/provider_context.py",
            "ia_carmine/runtime/heap_gate/tool_plan_builder.py",
            "ia_carmine/context/heap_context_memory_reload/runner.py",
            "ia_carmine/_shared/provider_tool_loop.py",
            "ia_carmine/runtime/runtime_tool/file_refs/allowlist.py",
            "ia_carmine/runtime/run/cli.py",
            "ia_carmine/runtime/run/universe_config.py",
            "ia_carmine/runtime/run/dry_run_report.py",
            "ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py",
            "ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py",
            "ia_carmine/runtime/runtime_tool/broker/context_builders.py",
            "ia_carmine/dispatch.py",
            "ia_carmine/_shared/tool_dispatch.py",
            "ia_carmine/product/operator_product_core/direct_command.py",
            "ia_carmine/product/operator_product_core/cli.py",
            "ia_carmine/product/operator_product_core/view/cli.py",
            "ia_carmine/product/operator_product_core/profiles.py",
            "ia_carmine/runtime/heap_context_closure/common.py",
            "ia_carmine/runtime/heap_context_closure/cli.py",
            "ia_carmine/runtime/heap_context_closure/commands.py",
            "ia_carmine/context/agent_context/rag_context/common.py",
            "ia_carmine/context/agent_context/rag_context/ingest_repo_cli.py",
            "ia_carmine/context/agent_context/rag_context/query_context_cli.py",
            "ia_carmine/context/agent_context/rag_context/build_context_pack_cli.py",
            "ia_carmine/providers/npu/provider_mesh/_shared/npu_runtime.py",
            "Tools/workflow/dispatch.py",
            "Tools/npu/dispatch.py",
            "Tools/validation/dispatch.py",
            "Tools/validation/validation_gate/cli.py",
            "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py",
            "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/context.py",
            "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/tool_policy.py",
            "Tools/validation/heap_runtime/completeness_gate_smoke/cli.py",
            "Tools/validation/heap_runtime/completeness_gate_smoke/request.py",
            "Tools/validation/agent_context/run_rag_ollama_embed_smoke/cli.py",
            "Tools/validation/dispatch.py",
            "Tools/validation/runtime_universe/run_core_runtime_guard_suite/cli.py",
        )
    }

    gate = files["ia_carmine/runtime/heap_runtime/completeness_gate/cli.py"]
    for needle in (
        '"ia_carmine/product/heap_final_proposals/cli.py"',
        '"ia_carmine/_shared/heap_proposal_gate.py"',
        '"ia_carmine/runtime/runtime_tool/agent_broker/cli.py"',
    ):
        check_absent(
            gate,
            needle,
            "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py",
            errors,
            "static matrix target fallback is forbidden",
        )

    for rel in (
        "ia_carmine/runtime/heap_runtime/virtual_dev_environment/cli.py",
        "ia_carmine/runtime/runtime_tool/agent_runtime_debug_lab/policy.py",
    ):
        path = repo_root / rel
        if not path.exists():
            warnings.append(f"{rel}: not present in this checkout")
            continue
        text = read(repo_root, rel)
        check_absent(
            tuple_block(text, "DENY_PREFIXES"),
            '"Scripting/"',
            rel,
            errors,
            "Scripting must not be globally denied",
        )

    planner = files["ia_carmine/runtime/heap_gate/target_planner.py"]
    check_absent(
        planner,
        'rel_path.startswith(("ia_carmine/"',
        "ia_carmine/runtime/heap_gate/target_planner.py",
        errors,
        "target planner must not bias runtime selection toward ia_carmine",
    )

    provider_loop = files["ia_carmine/_shared/provider_tool_loop.py"]
    for needle in ('Path.home() / "ProjectsDir"', 'Path.home() / "blender"', 'repo_root.parent / "npu-models"'):
        check_absent(
            provider_loop,
            needle,
            "ia_carmine/_shared/provider_tool_loop.py",
            errors,
            "OpenVINO model discovery must come from runtime env/config, not static fallback dirs",
        )

    allowlist = files["ia_carmine/runtime/runtime_tool/file_refs/allowlist.py"]
    for needle in ('"Scripting/v61b_backgood/"', '"old script legacy/"', '"Tools/npu/npu_code_chunks/"'):
        check_absent(
            allowlist,
            needle,
            "ia_carmine/runtime/runtime_tool/file_refs/allowlist.py",
            errors,
            "repo-specific ignored paths must be enforced by git-ignore, not duplicated as target hardcode",
        )

    final_product = files["ia_carmine/_shared/heap_final_code_product.py"]
    for needle in (
        "DENY_PRODUCT_PREFIXES",
        "PRODUCT_SUFFIXES",
        "def worktree_code_product",
        "def git_status_lines",
        "def worktree_product_items",
        '"worktree_status"',
        '"developed_change_present"',
        "include_worktree_extras",
    ):
        check_absent(
            final_product,
            needle,
            "ia_carmine/_shared/heap_final_code_product.py",
            errors,
            "final code product must not use local worktree diff fallback as runtime product",
        )

    core_suite = files["Tools/validation/runtime_universe/run_core_runtime_guard_suite/cli.py"]
    check_absent(
        core_suite,
        "CORE_STEPS",
        "Tools/validation/runtime_universe/run_core_runtime_guard_suite/cli.py",
        errors,
        "core guard suite must discover CORE_RUNTIME_GUARD smokes at runtime",
    )

    final_catalog = repo_root / "ia_carmine/heap_final_readable_catalog.py"
    if final_catalog.exists():
        errors.append(
            "ia_carmine/heap_final_readable_catalog.py: static final-product wording catalog is forbidden"
        )

    final_synthesis = read(repo_root, "ia_carmine/_shared/heap_final_readable_synthesis.py")
    if re.search(r'"Tools/(?:ai|validation)/[^"]+\.py"', final_synthesis):
        errors.append(
            "ia_carmine/_shared/heap_final_readable_synthesis.py: static target file paths are forbidden"
        )

    provider_specs = files["ia_carmine/runtime/heap_gate/provider_command_specs.py"]
    for needle in (
        "IA_CARMINE_GPU1_MODEL",
        "IA_CARMINE_GPU0_MODEL",
        "IA_CARMINE_GPU0_OLLAMA_BASE_URL",
        "IA_CARMINE_GPU0_VULKAN_VISIBLE_DEVICES",
        "IA_CARMINE_GPU1_OLLAMA_BASE_URL",
    ):
        check_absent(
            provider_specs,
            needle,
            "ia_carmine/runtime/heap_gate/provider_command_specs.py",
            errors,
            "provider model/URL/device values must come from explicit resolved CLI config",
        )
    for rel in (
        "ia_carmine/runtime/heap_context_closure/cli.py",
        "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py",
    ):
        text = read(repo_root, rel)
        if "canonical_run_config_required_for_provider_generation" not in text:
            errors.append(
                f"{rel}: provider-generation direct entrypoint must require canonical run config"
            )

    tool_plan = files["ia_carmine/runtime/heap_gate/tool_plan_builder.py"]
    for needle in (
        '"output/ai_runtime_memory/rag/rag.sqlite"',
        '"http://127.0.0.1:11434"',
        '"bge-m3"',
        '["tools/ai", "tools/npu", "tools/workflow"]',
        '["ia_carmine", "Tools/workflow", "Tools/npu"]',
    ):
        check_absent(
            tool_plan,
            needle,
            "ia_carmine/runtime/heap_gate/tool_plan_builder.py",
            errors,
            "RAG/tooling roots must come from explicit resolved CLI config",
        )

    provider_context = files["ia_carmine/runtime/heap_gate/provider_context.py"]
    check_absent(
        provider_context,
        "min(24",
        "ia_carmine/runtime/heap_gate/provider_context.py",
        errors,
        "provider prompt tool catalog limit must not clamp to an unreported local constant",
    )

    startup_runner = files["ia_carmine/context/heap_context_memory_reload/runner.py"]
    for needle in (
        "max_workers=4",
        '"heap context memory reload provider proposal GPU0 NPU"',
    ):
        check_absent(
            startup_runner,
            needle,
            "ia_carmine/context/heap_context_memory_reload/runner.py",
            errors,
            "startup workers/query must come from explicit resolved CLI config",
        )

    run_cli = files["ia_carmine/runtime/run/cli.py"]
    for needle in ("--profile", "--profiles-file", "profiles_file", "profile_runtime_config_not_allowed"):
        check_absent(
            run_cli,
            needle,
            "ia_carmine/runtime/run/cli.py",
            errors,
            "canonical run must not expose runtime profiles at all",
        )
    for needle in (
        "-ProcessGateTask",
        "DEFAULT_INTERMEDIATE_ROOT",
        "DEFAULT_BRANCH",
        'default="spark_direct"',
        "default_final_root",
    ):
        check_absent(
            run_cli,
            needle,
            "ia_carmine/runtime/run/cli.py",
            errors,
            "canonical run must not derive task/run/output/branch surfaces from hidden defaults",
        )
    for needle in ("default=DEFAULT_RUN_LABEL", "operator_product_launcher", "Path.home()"):
        check_absent(
            files["ia_carmine/product/operator_product_core/cli.py"],
            needle,
            "ia_carmine/product/operator_product_core/cli.py",
            errors,
            "operator-product compatibility wrapper must not synthesize local review surfaces",
        )
    check_absent(
        files["ia_carmine/product/operator_product_core/view/cli.py"],
        "default_final_root",
        "ia_carmine/product/operator_product_core/view/cli.py",
        errors,
        "operator-product GUI must require explicit final output directory",
    )
    universe_config = files["ia_carmine/runtime/run/universe_config.py"]
    for needle in ("_profile_applied_fields", "profile_sources", '"profile"'):
        check_absent(
            universe_config,
            needle,
            "ia_carmine/runtime/run/universe_config.py",
            errors,
            "universe config resolver must be CLI-only",
        )
    dry_run = files["ia_carmine/runtime/run/dry_run_report.py"]
    for needle in ("profile_plus_explicit", "profile_surface", "profile:"):
        check_absent(
            dry_run,
            needle,
            "ia_carmine/runtime/run/dry_run_report.py",
            errors,
            "dry-run report must not describe profile config sources",
        )

    dispatch = files["ia_carmine/dispatch.py"]
    for needle in (
        '"heap_context_closure"',
        '"run_heap_runtime_completeness_gate"',
        '"heap_runtime_launcher_command"',
    ):
        check_absent(
            dispatch,
            needle,
            "ia_carmine/dispatch.py",
            errors,
            "run bypass surface must not be publicly registered",
        )

    tool_dispatch = files["ia_carmine/_shared/tool_dispatch.py"]
    for needle in ("package_cli", "_file_exposes_main", "glob(\"*.py\")"):
        check_absent(
            tool_dispatch,
            needle,
            "ia_carmine/_shared/tool_dispatch.py",
            errors,
            "dispatcher must not resolve unregistered package fallback tools",
        )
    for required in ("VISIBLE_STATES", "ALLOW_INTERNAL_ENV", "public_tools", "_tool_allowed"):
        if required not in tool_dispatch:
            errors.append(
                "ia_carmine/_shared/tool_dispatch.py: dispatcher must enforce public/compat/internal metadata"
            )

    expected_public = {
        "ia_carmine.dispatch": {"run", "runtime_tool_broker"},
        "Tools.validation.dispatch": {
            "validator_unico",
            "smoke_unico",
            "test_unico",
        },
        "Tools.workflow.dispatch": set(),
        "Tools.npu.dispatch": set(),
    }
    for module_name, expected in expected_public.items():
        try:
            module = importlib.import_module(module_name)
            mapping = getattr(module, "TOOL_MAIN_TARGETS", {})
            visibility = getattr(module, "TOOL_VISIBILITY", {})
            actual = {
                name
                for name in mapping
                if visibility.get(name, "public") == "public"
            }
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{module_name}: cannot inspect dispatcher visibility: {exc}")
            continue
        if actual != expected:
            errors.append(
                f"{module_name}: public dispatcher surface mismatch; expected={sorted(expected)} actual={sorted(actual)}"
            )

    direct_command = files["ia_carmine/product/operator_product_core/direct_command.py"]
    if "ia_carmine.runtime.heap_context_closure.cli" not in direct_command:
        errors.append(
            "ia_carmine/product/operator_product_core/direct_command.py: canonical run must invoke heap closure as internal module"
        )
    check_absent(
        direct_command,
        '"ia_carmine.cli",\n        "heap_context_closure"',
        "ia_carmine/product/operator_product_core/direct_command.py",
        errors,
        "canonical run must not route internal closure through public dispatcher",
    )

    profiles = files["ia_carmine/product/operator_product_core/profiles.py"]
    for needle in ("load_profiles", "select_profile", "apply_profile_to_args", "json.loads"):
        check_absent(
            profiles,
            needle,
            "ia_carmine/product/operator_product_core/profiles.py",
            errors,
            "legacy runtime profile loader must not exist",
        )

    closure_common = files["ia_carmine/runtime/heap_context_closure/common.py"]
    closure_cli = files["ia_carmine/runtime/heap_context_closure/cli.py"]
    for needle in (".venv314", "sys.executable", "auto_latest"):
        check_absent(
            closure_common,
            needle,
            "ia_carmine/runtime/heap_context_closure/common.py",
            errors,
            "heap closure must not infer Python or revision context",
        )
        check_absent(
            closure_cli,
            needle,
            "ia_carmine/runtime/heap_context_closure/cli.py",
            errors,
            "heap closure must not advertise implicit latest revision context",
        )
    if "provider_python_explicit_required" not in closure_common:
        errors.append("ia_carmine/runtime/heap_context_closure/common.py: explicit python requirement missing")
    for needle in ("DEFAULT_REQUEST", 'default=DEFAULT_REQUEST', "now_stamp()"):
        check_absent(
            closure_cli,
            needle,
            "ia_carmine/runtime/heap_context_closure/cli.py",
            errors,
            "heap closure CLI must require explicit request/output/stamp/objective",
        )
    for required in ("operator_request_required", "output_dir_required", "stamp_required", "objective_required"):
        if required not in closure_cli:
            errors.append(
                "ia_carmine/runtime/heap_context_closure/cli.py: closure must reject missing explicit runtime surfaces"
            )

    closure_commands = files["ia_carmine/runtime/heap_context_closure/commands.py"]
    if "ia_carmine.runtime.heap_runtime.completeness_gate.cli" not in closure_commands:
        errors.append(
            "ia_carmine/runtime/heap_context_closure/commands.py: completeness gate must be internal module command"
        )
    check_absent(
        closure_commands,
        '"run_heap_runtime_completeness_gate"',
        "ia_carmine/runtime/heap_context_closure/commands.py",
        errors,
        "heap closure must not route completeness gate through public dispatcher",
    )

    provider_role = files["ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py"]
    gpu0_peer = files["ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py"]
    gpu1_preflight = files["Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py"]
    for rel, text in (
        ("ia_carmine/providers/provider_mesh/provider_role_coexistence/cli.py", provider_role),
        ("ia_carmine/providers/provider_mesh/ollama_gpu0_peer_report/cli.py", gpu0_peer),
        ("Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/cli.py", gpu1_preflight),
    ):
        for needle in (
            'default="http://127.0.0.1:11434"',
            'default="http://127.0.0.1:11435"',
            'default="qwen2.5-coder:14b"',
            'default="qwen3:1.7b"',
            'default="auto"',
            'default="8192,4096"',
            'default="bge-m3"',
        ):
            check_absent(text, needle, rel, errors, "provider validators must require explicit runtime config")

    context_builders = files["ia_carmine/runtime/runtime_tool/broker/context_builders.py"]
    if 'required_tool_arg(args, "rag_profile")' not in context_builders:
        errors.append(
            "ia_carmine/runtime/runtime_tool/broker/context_builders.py: broker RAG tool must require explicit rag_profile"
        )
    if '"--rag-profile"' not in context_builders:
        errors.append(
            "ia_carmine/runtime/runtime_tool/broker/context_builders.py: broker RAG command must pass --rag-profile"
        )
    for needle in (
        '"http://127.0.0.1:11434"',
        '"bge-m3"',
        '"output/ai_runtime_memory/rag/rag.sqlite"',
    ):
        check_absent(
            context_builders,
            needle,
            "ia_carmine/runtime/runtime_tool/broker/context_builders.py",
            errors,
            "broker RAG tool must receive endpoint/model/db explicitly",
        )

    for rel in (
        "ia_carmine/context/agent_context/rag_context/common.py",
        "ia_carmine/context/agent_context/rag_context/ingest_repo_cli.py",
        "ia_carmine/context/agent_context/rag_context/query_context_cli.py",
        "ia_carmine/context/agent_context/rag_context/build_context_pack_cli.py",
        "Tools/validation/agent_context/run_rag_ollama_embed_smoke/cli.py",
    ):
        text = files[rel]
        for needle in (
            '"http://127.0.0.1:11434"',
            '"bge-m3"',
            '"output/ai_runtime_memory/rag/rag.sqlite"',
        ):
            check_absent(text, needle, rel, errors, "RAG live runtime config must be explicit")
        if rel.endswith("common.py"):
            if 'missing.append("--rag-profile")' not in text:
                errors.append(f"{rel}: RAG profile must be explicit")
        elif '"--rag-profile"' not in text:
            errors.append(f"{rel}: RAG CLI must expose --rag-profile")
    if '"provider_execution_performed": False' in files["Tools/validation/agent_context/run_rag_ollama_embed_smoke/cli.py"]:
        errors.append(
            "Tools/validation/agent_context/run_rag_ollama_embed_smoke/cli.py: live embedding smoke must not report provider_execution_performed=false"
        )

    validation_dispatch = files["Tools/validation/dispatch.py"]
    check_absent(
        validation_dispatch,
        '"run_heap_runtime_completeness_gate_smoke"',
        "Tools/validation/dispatch.py",
        errors,
        "complete runtime fixture smoke must not be a public validation bypass",
    )
    check_absent(
        validation_dispatch,
        '"run_real_product_profile_smoke"',
        "Tools/validation/dispatch.py",
        errors,
        "retired runtime profile smoke must not be public validation",
    )
    for public_name in ('"validator_unico"', '"smoke_unico"', '"test_unico"'):
        if public_name not in validation_dispatch:
            errors.append(f"Tools/validation/dispatch.py: missing public canonical validation command {public_name}")
    validation_gate = files["Tools/validation/validation_gate/cli.py"]
    check_absent(
        validation_gate,
        'default="quick"',
        "Tools/validation/validation_gate/cli.py",
        errors,
        "validation gate mode/suite must be explicit",
    )
    for required in ('"--mode"', '"--section"', "missing explicit validation mode"):
        if required not in validation_gate:
            errors.append(
                "Tools/validation/validation_gate/cli.py: public validator must route by explicit --mode and optional --section"
            )

    completeness_gate = files["ia_carmine/runtime/heap_runtime/completeness_gate/cli.py"]
    for needle in (
        "prove complete heap-driven teamwork loop",
        'default="deferred"',
        "default=DEFAULT_OUTPUT",
        "default=DEFAULT_MARKDOWN",
        "default=0)",
    ):
        check_absent(
            completeness_gate,
            needle,
            "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py",
            errors,
            "completeness gate must require explicit objective/output/lane defaults",
        )
    for required in (
        "explicit_runtime_gate_args_required",
        "--objective",
        "--npu-micro-start-mode",
        "--max-degraded-lanes",
        "--output",
        "--markdown-output",
    ):
        if required not in completeness_gate:
            errors.append(
                "ia_carmine/runtime/heap_runtime/completeness_gate/cli.py: completeness gate explicit-args guard incomplete"
            )

    completeness_smoke = files["Tools/validation/heap_runtime/completeness_gate_smoke/cli.py"]
    for needle in ('default="qwen2.5-coder:14b"', '"--budget-minutes",\n        "5"'):
        check_absent(
            completeness_smoke,
            needle,
            "Tools/validation/heap_runtime/completeness_gate_smoke/cli.py",
            errors,
            "completeness smoke must require explicit runtime sizing/model",
        )
    completeness_request = files["Tools/validation/heap_runtime/completeness_gate_smoke/request.py"]
    for needle in ("Tools\" / \"ai", "HEAP_DELTA_PROPOSAL", "EXIT_DECISION=", "POINTER_ACTION="):
        check_absent(
            completeness_request,
            needle,
            "Tools/validation/heap_runtime/completeness_gate_smoke/request.py",
            errors,
            "complete smoke request must use current FINAL_PRODUCT_DELTA contract and current source refs",
        )

    gpu1_context = files["Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/context.py"]
    for needle in (
        '"output/ai_runtime_memory/rag/rag.sqlite"',
        '"auto"',
        '"12"',
        '"24000"',
        '"4"',
        '"project_self_improvement"',
        '"core_ai_backend"',
    ):
        check_absent(
            gpu1_context,
            needle,
            "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/context.py",
            errors,
            "GPU1 preflight startup refresh must use explicit args, not local defaults",
        )
    for rel in (
        "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/context.py",
        "Tools/validation/heap_runtime/gpu1_native_tool_loop_preflight/tool_policy.py",
        "ia_carmine/_shared/provider_tool_loop.py",
    ):
        check_absent(
            files[rel],
            "build_python_line_count_csv",
            rel,
            errors,
            "full repo line-count inventory is not an exposed GPU1 preflight tool",
        )

    npu_runtime = files["ia_carmine/providers/npu/provider_mesh/_shared/npu_runtime.py"]
    for needle in ('Path.home() / "blender"', '"Phi-3.5-mini-instruct-int4-cw-ov"'):
        check_absent(
            npu_runtime,
            needle,
            "ia_carmine/providers/npu/provider_mesh/_shared/npu_runtime.py",
            errors,
            "NPU model path must come from explicit config/env",
        )

    workflow_dispatch = files["Tools/workflow/dispatch.py"]
    npu_dispatch = files["Tools/npu/dispatch.py"]
    for needle in ("ps1:", '"run_', '"build_', '"startup_', '"workflow_', '"npu_'):
        check_absent(
            workflow_dispatch,
            needle,
            "Tools/workflow/dispatch.py",
            errors,
            "retired workflow dispatcher must not keep wrapper/tool registry entries",
        )
    for needle in ("ps1:", '"run_', '"build_', '"npu_', '"music_', '"project_'):
        check_absent(
            npu_dispatch,
            needle,
            "Tools/npu/dispatch.py",
            errors,
            "retired NPU dispatcher must not keep wrapper/tool registry entries",
        )
    legacy_wrapper_paths = [
        Path("Tools") / "workflow" / "_powershell",
        Path("Tools") / "workflow" / "run_unified_local_ai_refactor",
        Path("Tools") / "workflow" / "run_unified_real_product_pr",
        Path("Tools") / "workflow" / "run_local_ai_task_via_pipeline",
        Path("Tools") / "npu" / "_powershell",
    ]
    for rel_path in legacy_wrapper_paths:
        path = repo_root / rel_path
        if path.exists() and any(path.rglob("*.ps1")):
            errors.append(f"{rel_path.as_posix()}: legacy PowerShell wrapper files must be removed")

    return {
        "schema_version": 1,
        "kind": "runtime_hardcode_guard_smoke",
        "generated_at": now_iso(),
        "passed": not errors,
        "errors": errors,
        "warnings": warnings,
        "source_writes_performed": False,
        "patch_application_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--output", default="output/validation/runtime_hardcode_guard_smoke.json")
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
