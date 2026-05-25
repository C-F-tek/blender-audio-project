#!/usr/bin/env python3
"""Smoke-test operator product launcher command and safe-apply integration."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from ia_carmine.product.operator_product_core import (
        LauncherConfig,
        analyze_code_product,
        build_heap_command,
        resolve_config,
        run_dir_for,
    )
except ImportError:  # pragma: no cover
    repo_root_for_import = Path(__file__).resolve().parents[3]
    if str(repo_root_for_import) not in sys.path:
        sys.path.insert(0, str(repo_root_for_import))
    from ia_carmine.product.operator_product_core import (  # type: ignore
        LauncherConfig,
        analyze_code_product,
        build_heap_command,
        resolve_config,
        run_dir_for,
    )


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_fixture(work_dir: Path) -> tuple[Path, Path]:
    repo = work_dir / "fixture_repo"
    target = repo / "Tools" / "operator_target.py"
    write_text(target, "VALUE = 1\n")
    subprocess.run(["git", "init"], cwd=repo, capture_output=True, text=True, check=False)
    code_product = work_dir / "CODE_PRODUCT_FULL_PATCH.md"
    write_text(
        code_product,
        """# CODE_PRODUCT_FULL_PATCH

## Code / Patch

### Tools/operator_target.py

- Git status: `M Tools/operator_target.py`
- Implementation status: `developed_change_present`
- Diff hunks: `1`

```diff
diff --git a/Tools/operator_target.py b/Tools/operator_target.py
--- a/Tools/operator_target.py
+++ b/Tools/operator_target.py
@@ -1 +1 @@
-VALUE = 1
+VALUE = 2
```

### Tools/operator_new.py

- Git status: `?? Tools/operator_new.py`
- Implementation status: `developed_change_present`
- Diff hunks: `0`

```diff
new file: Tools/operator_new.py

VALUE = 3
```
""",
    )
    return repo, code_product


def render_markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Operator Product Launcher Smoke",
        "",
        f"- Passed: `{report.get('passed')}`",
        f"- Command built: `{report.get('command_built')}`",
        f"- Safe apply passed: `{report.get('safe_apply_passed')}`",
        "",
        "## Checks",
        "",
    ]
    for item in report.get("checks", []):
        lines.append(f"- `{item.get('name')}`: `{item.get('passed')}`")
    if report.get("errors"):
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])
    return "\n".join(lines) + "\n"


def run_core_runtime_guard_suite(repo_root: Path, work_dir: Path, timeout_seconds: int) -> dict[str, Any]:
    output = work_dir / "core_runtime_guard_suite.json"
    command = [
        sys.executable,
        "Tools/validation/runtime_universe/run_core_runtime_guard_suite/cli.py",
        "--repo-root",
        str(repo_root),
        "--output",
        str(output),
        "--markdown-output",
        str(work_dir / "core_runtime_guard_suite.md"),
        "--step-output-dir",
        str(work_dir / "core_runtime_guard_suite_steps"),
        "--timeout-seconds",
        str(timeout_seconds),
    ]
    completed = subprocess.run(
        command,
        cwd=repo_root,
        text=True,
        capture_output=True,
        check=False,
        timeout=max(30, timeout_seconds),
    )
    report: dict[str, Any] = {}
    if output.exists():
        try:
            report = json.loads(output.read_text(encoding="utf-8-sig"))
        except Exception as exc:  # noqa: BLE001
            report = {"passed": False, "errors": [f"parse failed: {type(exc).__name__}: {exc}"]}
    return {
        "command": command,
        "returncode": completed.returncode,
        "passed": completed.returncode == 0 and report.get("passed") is True,
        "report": report,
        "stdout_tail": (completed.stdout or "")[-4000:],
        "stderr_tail": (completed.stderr or "")[-4000:],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--work-dir", default="output/validation/operator_product_launcher_smoke")
    parser.add_argument(
        "--output", default="output/validation/operator_product_launcher_smoke.json"
    )
    parser.add_argument(
        "--markdown-output", default="output/validation/operator_product_launcher_smoke.md"
    )
    parser.add_argument("--timeout-seconds", type=int, default=180)
    args = parser.parse_args()
    repo_root = Path(args.repo_root).resolve()
    work_dir = (repo_root / args.work_dir).resolve()
    if work_dir.exists():
        work_dir.relative_to((repo_root / "output" / "validation").resolve())
        shutil.rmtree(work_dir)
    request_file = work_dir / "operator_request.md"
    write_text(request_file, "# Operator launcher smoke\n\nProduce a reviewable code product.\n")
    config = LauncherConfig(
        repo_root=repo_root,
        request_file=request_file,
        intermediate_root=work_dir / "intermediate",
        final_root=work_dir / "documents",
        python_exe=sys.executable,
        stamp="operator_launcher_smoke",
        objective="operator product launcher smoke",
        revision_context="off",
        budget_minutes=1,
        max_iterations=1,
        min_runtime_rounds=1,
        min_proposal_iterations=0,
        max_rounds=1,
        files_per_round=4,
        max_provider_revisions=1,
        timeout_seconds=60,
        preflight_timeout_seconds=30,
        provider_model="explicit_gpu1_model_for_smoke",
        gpu1_base_url="http://gpu1-ollama.invalid",
        gpu0_model="explicit_gpu0_model_for_smoke",
        gpu0_base_url="http://gpu0-ollama.invalid",
        gpu0_vulkan_visible_devices="1",
        ollama_num_ctx=4096,
        gpu0_ollama_num_ctx=2048,
        ollama_gpu_layers="all",
        ollama_context_candidates="4096",
        npu_model_dir="C:/explicit/npu-model",
        max_new_tokens=256,
        gpu0_max_new_tokens=64,
        keep_alive="30s",
        gpu0_iterations=1,
        gpu0_min_seconds=0.1,
        npu_micro_timeout_seconds=10,
        npu_max_context_chars=2000,
        npu_max_prompt_chars=1000,
        npu_max_new_tokens=128,
        npu_device_workload_seconds=0.1,
        npu_device_workload_iterations=1,
        startup_max_memory_chars=32000,
        startup_max_context_files=2080,
        startup_scan_context_files=2080,
        startup_max_chars_per_file=20000,
        startup_provider_input_workers=2,
        startup_required_context_profile="project_self_improvement",
        startup_operational_memory_query="operator launcher smoke",
        startup_operational_memory_limit=2,
        rag_db="output/ai_runtime_memory/rag/rag.sqlite",
        rag_profile="runtime_code_context",
        rag_index_policy="auto",
        rag_embedding_endpoint="http://rag-embedding.invalid",
        rag_embedding_model="bge-m3",
        rag_ingest_batch_size=4,
        rag_embed_smoke_batch_size=4,
        rag_chunk_min_chars=1500,
        rag_chunk_max_chars=4000,
        rag_chunk_overlap_chars=300,
        rag_max_file_size=250000,
        rag_top_k=5,
        rag_char_budget=8000,
        context_document_count=4,
        context_document_preview_chars=400,
        semantic_code_chunk_limit=4,
        semantic_code_chunk_preview_chars=400,
        semantic_evidence_chunk_limit=4,
        memory_search_limit=2,
        tool_catalog_limit=20,
        revision_context_max_tasks=2,
        tool_inventory_roots="Tools,ia_carmine",
        semantic_path_boosts="ia_carmine/runtime/heap_gate,ia_carmine/runtime/run",
        ai_context_pack_profile="core_ai_backend",
        code_interpreter_inputs="ia_carmine,Tools",
        duplication_audit_roots="ia_carmine,Tools",
        provider_prompt_tool_catalog_cap=20,
    )
    command = build_heap_command(config)
    resolved = resolve_config(config)
    core_guard_suite = run_core_runtime_guard_suite(repo_root, work_dir, args.timeout_seconds)
    fixture_repo, code_product = build_fixture(work_dir)
    apply_report = analyze_code_product(
        fixture_repo,
        code_product,
        run_dir_for(resolved),
        apply_safe=True,
        require_all_integrated=True,
        python_exe=sys.executable,
    )
    checks = [
        {
            "name": "targets_heap_closure",
            "passed": command[:4] == [
                resolved.python_exe,
                "-m",
                "ia_carmine.runtime.heap_context_closure.cli",
                "--repo-root",
            ],
        },
        {
            "name": "uses_request_file",
            "passed": "--request-file" in command and str(request_file) in command,
        },
        {"name": "uses_output_dir", "passed": "--output-dir" in command},
        {"name": "uses_documents_root", "passed": "--documents-root" in command},
        {
            "name": "uses_context_file_override",
            "passed": "--startup-max-context-files" in command and "2080" in command,
        },
        {
            "name": "uses_scan_file_override",
            "passed": "--startup-scan-context-files" in command and "2080" in command,
        },
        {
            "name": "uses_chars_per_file_override",
            "passed": "--startup-max-chars-per-file" in command and "20000" in command,
        },
        {
            "name": "uses_files_per_round_override",
            "passed": "--files-per-round" in command and "4" in command,
        },
        {
            "name": "explicit_config_no_provider_generation",
            "passed": "--allow-provider-generation" not in command,
        },
        {
            "name": "core_runtime_guard_suite",
            "passed": core_guard_suite.get("passed") is True,
        },
        {"name": "safe_apply_passed", "passed": apply_report.get("passed") is True},
        {
            "name": "safe_apply_wrote_two",
            "passed": apply_report.get("safe_apply", {}).get("applied_count") == 2,
        },
        {
            "name": "fixture_modified",
            "passed": (fixture_repo / "Tools" / "operator_target.py")
            .read_text(encoding="utf-8")
            .strip()
            == "VALUE = 2",
        },
        {
            "name": "fixture_new_file",
            "passed": (fixture_repo / "Tools" / "operator_new.py").exists(),
        },
    ]
    errors = [str(item["name"]) for item in checks if not item.get("passed")]
    report = {
        "schema_version": 1,
        "kind": "operator_product_launcher_smoke",
        "passed": not errors,
        "command_built": bool(command),
        "command": command,
        "safe_apply_passed": apply_report.get("passed"),
        "safe_apply_report": str(run_dir_for(resolved) / "code_product_apply_safe.json"),
        "core_runtime_guard_suite": core_guard_suite,
        "provider_execution_performed": False,
        "patch_application_performed": apply_report.get("patch_application_performed"),
        "source_writes_performed": apply_report.get("source_writes_performed"),
        "checks": checks,
        "errors": errors,
    }
    output = (repo_root / args.output).resolve()
    markdown = (repo_root / args.markdown_output).resolve()
    write_json(output, report)
    write_text(markdown, render_markdown(report))
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["passed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
