#!/usr/bin/env python3
"""Guard against runtime target/script-gaming hardcodes."""

from __future__ import annotations

import argparse
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
