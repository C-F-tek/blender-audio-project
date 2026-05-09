#!/usr/bin/env python3
"""Wire heap/exchange lifecycle entry and exit into the unified launcher.

The patcher is deliberately idempotent and non-destructive. It creates a backup,
modifies only the launcher, and validates the resulting PowerShell syntax.

The wiring does not guide the dynamic center of the run. It adds:
- entry envelope after workload routing;
- exit product after generated patch specs review bridge;
- lifecycle validation before product separation.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

ENTRY_MARKER = "# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN"
EXIT_MARKER = "# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN"
LIFECYCLE_MARKER = "# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-BEGIN"


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def write_preserved(path: Path, text_lf: str, newline: str) -> None:
    path.write_text(text_lf.rstrip("\n").replace("\n", newline) + newline, encoding="utf-8-sig")


def run_parser(path: Path) -> tuple[bool, str]:
    ps_path = str(path).replace("'", "''")
    command = (
        "$tokens=$null;"
        "$errors=$null;"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{ps_path}',[ref]$tokens,[ref]$errors);"
        "if($errors.Count -gt 0){$errors | ForEach-Object { Write-Error $_.Message };exit 1}else{exit 0}"
    )
    result = subprocess.run(["powershell.exe", "-NoProfile", "-Command", command], capture_output=True, text=True, check=False)
    return result.returncode == 0, result.stdout + result.stderr


def entry_block() -> str:
    return r'''
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN
$HeapExchangeEntryJson = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.json"
$HeapExchangeEntryMd = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.md"
$HeapExchangeRuntimeState = Join-Path $AiPacketsDir "heap_exchange_runtime_state.jsonl"
$HeapExchangeEntryArgs = @(
    "Tools/ai/build_heap_exchange_runtime_entry.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--task-file", $TaskFile,
    "--observer-dir", $ObserverDir,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--output", $HeapExchangeEntryJson,
    "--markdown-output", $HeapExchangeEntryMd
)
if (Test-Path -LiteralPath $Gpu0WorkloadJson -PathType Leaf) { $HeapExchangeEntryArgs += @("--gpu0-report", $Gpu0WorkloadJson) }
if (Test-Path -LiteralPath $OfficialPhaseJson -PathType Leaf) { $HeapExchangeEntryArgs += @("--official-report", $OfficialPhaseJson) }
if (Test-Path -LiteralPath "output/validation/ai_workload_report_quality.json" -PathType Leaf) { $HeapExchangeEntryArgs += @("--workload-quality-report", "output/validation/ai_workload_report_quality.json") }
$HeapExchangeEntryOk = Invoke-Checked "Build heap/exchange runtime entry" {
    & $ResolvedPythonExe @HeapExchangeEntryArgs
}
$ReportFiles += $HeapExchangeEntryJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeEntryMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-END
'''.strip("\n")


def exit_block() -> str:
    return r'''
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN
$HeapExchangeExitJson = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.json"
$HeapExchangeExitMd = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.md"
$HeapExchangeExitArgs = @(
    "Tools/ai/build_heap_exchange_runtime_exit.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $ObserverDir,
    "--output", $HeapExchangeExitJson,
    "--markdown-output", $HeapExchangeExitMd
)
if (Test-Path -LiteralPath $GeneratedPatchSpecsApplyJson -PathType Leaf) { $HeapExchangeExitArgs += @("--apply-report", $GeneratedPatchSpecsApplyJson) }
if ($PrepareReviewPr -or $ReviewPrFromGeneratedPatchSpecs) { $HeapExchangeExitArgs += "--require-concrete-product" }
$HeapExchangeExitOk = Invoke-Checked "Build heap/exchange runtime exit product" {
    & $ResolvedPythonExe @HeapExchangeExitArgs
}
$ReportFiles += $HeapExchangeExitJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeExitMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-END
'''.strip("\n")


def lifecycle_block() -> str:
    return r'''
# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-BEGIN
$HeapExchangeLifecycleJson = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.json" -f $DataStamp)
$HeapExchangeLifecycleMd = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.md" -f $DataStamp)
$HeapExchangeLifecycleArgs = @(
    "Tools/validation/check_heap_exchange_runtime_lifecycle.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--runtime-exit", $HeapExchangeExitJson,
    "--observer-dir", $ObserverDir,
    "--require-public-events",
    "--output", $HeapExchangeLifecycleJson,
    "--markdown-output", $HeapExchangeLifecycleMd
)
if ($PrepareReviewPr -or $ReviewPrFromGeneratedPatchSpecs) { $HeapExchangeLifecycleArgs += "--require-concrete-exit" }
$HeapExchangeLifecycleOk = Invoke-Checked "Validate heap/exchange runtime lifecycle" {
    & $ResolvedPythonExe @HeapExchangeLifecycleArgs
}
$ReportFiles += $HeapExchangeLifecycleJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeLifecycleMd
# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-END
'''.strip("\n")


def insert_after_phase(text: str, phase_label: str, block: str, marker: str) -> tuple[str, bool]:
    if marker in text:
        return text, False
    idx = text.find(phase_label)
    if idx < 0:
        raise RuntimeError(f"anchor not found: {phase_label}")
    next_phase = text.find("\n=== ", idx + len(phase_label))
    if next_phase < 0:
        raise RuntimeError(f"next phase anchor not found after: {phase_label}")
    return text[:next_phase].rstrip("\n") + "\n\n" + block + "\n" + text[next_phase:], True


def insert_before_anchor(text: str, anchor_terms: list[str], block: str, marker: str) -> tuple[str, bool]:
    if marker in text:
        return text, False
    lines = text.splitlines()
    anchor_index: int | None = None
    for index, line in enumerate(lines):
        if any(term in line for term in anchor_terms):
            anchor_index = index
            break
    if anchor_index is None:
        diagnostics = [f"{idx + 1}: {line}" for idx, line in enumerate(lines) if any(word in line.lower() for word in ("product", "separation", "patch_suggestion", "chain"))]
        raise RuntimeError("could not locate lifecycle insertion anchor. Diagnostics:\n" + "\n".join(diagnostics[:60]))
    new_lines = lines[:anchor_index] + ["", *block.splitlines(), ""] + lines[anchor_index:]
    return "\n".join(new_lines) + "\n", True


def patch_launcher(text_lf: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    text_lf, changed = insert_after_phase(text_lf, "=== Build AI workload quality routing report ===", entry_block(), ENTRY_MARKER)
    if changed:
        changes.append("insert_heap_exchange_runtime_entry")
    text_lf, changed = insert_after_phase(text_lf, "=== Apply generated patch specs for review PR ===", exit_block(), EXIT_MARKER)
    if changed:
        changes.append("insert_heap_exchange_runtime_exit")
    text_lf, changed = insert_before_anchor(
        text_lf,
        ["Validate unified heap/exchange chain contract", "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN"],
        lifecycle_block(),
        LIFECYCLE_MARKER,
    )
    if changed:
        changes.append("insert_heap_exchange_lifecycle_gate")
    return text_lf, changes


def validate_policy(text_lf: str) -> list[str]:
    errors: list[str] = []
    for token in (
        ENTRY_MARKER,
        EXIT_MARKER,
        LIFECYCLE_MARKER,
        "Build heap/exchange runtime entry",
        "Build heap/exchange runtime exit product",
        "Validate heap/exchange runtime lifecycle",
        "Tools/ai/build_heap_exchange_runtime_entry.py",
        "Tools/ai/build_heap_exchange_runtime_exit.py",
        "Tools/validation/check_heap_exchange_runtime_lifecycle.py",
    ):
        if token not in text_lf:
            errors.append(f"missing required lifecycle token: {token}")
    if text_lf.find("Build heap/exchange runtime entry") > text_lf.find("Run official local AI pipeline adapter"):
        errors.append("heap/exchange entry must be before official/provider dynamic center")
    if text_lf.find("Build heap/exchange runtime exit product") > text_lf.find("Validate unified heap/exchange chain contract"):
        errors.append("heap/exchange exit must be before unified chain contract")
    if re.search(r"^\s*throw\s*$", text_lf, flags=re.MULTILINE):
        errors.append("naked throw remains in launcher")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target", default="Tools/workflow/run_unified_local_ai_refactor.ps1")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    target = (repo / args.target).resolve()
    backup_dir = repo / "output" / "validation" / "heap_exchange_lifecycle_wiring_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    parser_ok, parser_output = run_parser(target)
    if not parser_ok:
        print("PRE_PATCH_POWERSHELL_PARSE_FAILED")
        print(parser_output)
        return 2

    original = read_text(target)
    newline = detect_newline(original)
    original_lf = normalize_lf(original)
    patched_lf, changes = patch_launcher(original_lf)
    errors = validate_policy(patched_lf)
    if errors:
        print("POLICY_VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 3

    if patched_lf == original_lf:
        print("NO_CHANGES_NEEDED")
        print(f"line_count={len(original_lf.splitlines())}")
        return 0

    backup = backup_dir / f"{target.name}.{datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
    shutil.copy2(target, backup)
    if args.dry_run:
        print("DRY_RUN")
        print(f"changes={','.join(changes)}")
        print(f"backup={backup}")
        print(f"line_count={len(patched_lf.splitlines())}")
        return 0

    write_preserved(target, patched_lf, newline)
    parser_ok, parser_output = run_parser(target)
    if not parser_ok:
        shutil.copy2(backup, target)
        print("POWERSHELL_PARSE_FAILED_RESTORED_BACKUP")
        print(parser_output)
        return 4

    print("PATCHED")
    print(f"target={target.relative_to(repo).as_posix()}")
    print(f"backup={backup.relative_to(repo).as_posix()}")
    print(f"changes={','.join(changes)}")
    print(f"line_count={len(read_text(target).splitlines())}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
