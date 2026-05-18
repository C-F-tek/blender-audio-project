#!/usr/bin/env python3
"""Wire heap/exchange lifecycle entry and exit into the unified launcher.

The patcher is deliberately idempotent and non-destructive. It creates a backup,
modifies only the launcher, and validates the resulting PowerShell syntax.

The wiring does not guide the dynamic center of the run. It adds:
- entry envelope before the official/provider dynamic center;
- exit product after generated patch specs review bridge when present;
- lifecycle validation before the unified chain contract.
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
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout + result.stderr


def entry_block() -> str:
    return r"""
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-BEGIN
$HeapExchangeObserverDir = $ObserverOutputDir
if ([string]::IsNullOrWhiteSpace($HeapExchangeObserverDir)) {
    $HeapExchangeObserverDir = Join-Path $OutputDir ("local_ai_runs/{0}_observer" -f $DataStamp)
}
$HeapExchangeEntryJson = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.json"
$HeapExchangeEntryMd = Join-Path $AiPacketsDir "heap_exchange_runtime_entry.md"
$HeapExchangeRuntimeState = Join-Path $AiPacketsDir "heap_exchange_runtime_state.jsonl"
$HeapExchangeEntryArgs = @(
    "Tools/ai/heap_exchange/runtime_entry/cli.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--task-file", $TaskFile,
    "--observer-dir", $HeapExchangeObserverDir,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--output", $HeapExchangeEntryJson,
    "--markdown-output", $HeapExchangeEntryMd
)
$HeapExchangeEntryOk = Invoke-Checked "Build heap/exchange runtime entry" {
    & $ResolvedPythonExe @HeapExchangeEntryArgs
}
$ReportFiles += $HeapExchangeEntryJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeEntryMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-ENTRY-END
""".strip("\n")


def exit_block() -> str:
    return r"""
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-BEGIN
$HeapExchangeExitJson = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.json"
$HeapExchangeExitMd = Join-Path $AiPacketsDir "heap_exchange_runtime_exit_product.md"
$HeapExchangeExitArgs = @(
    "Tools/ai/heap_exchange/runtime_exit/cli.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--observer-dir", $HeapExchangeObserverDir,
    "--output", $HeapExchangeExitJson,
    "--markdown-output", $HeapExchangeExitMd
)
if ($PrepareReviewPr -or $ReviewPrFromGeneratedPatchSpecs) { $HeapExchangeExitArgs += "--require-concrete-product" }
$HeapExchangeExitOk = Invoke-Checked "Build heap/exchange runtime exit product" {
    & $ResolvedPythonExe @HeapExchangeExitArgs
}
$ReportFiles += $HeapExchangeExitJson
$ContextFiles = Add-ExistingContextFile -Current $ContextFiles -PathValue $HeapExchangeExitMd
# IA-CARMINE-HEAP-EXCHANGE-RUNTIME-EXIT-END
""".strip("\n")


def lifecycle_block() -> str:
    return r"""
# IA-CARMINE-HEAP-EXCHANGE-LIFECYCLE-GATE-BEGIN
$HeapExchangeLifecycleJson = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.json" -f $DataStamp)
$HeapExchangeLifecycleMd = Join-Path $OutputDir ("validation/heap_exchange_runtime_lifecycle_{0}.md" -f $DataStamp)
$HeapExchangeLifecycleArgs = @(
    "Tools/validation/heap_exchange/runtime_lifecycle_check/cli.py",
    "--repo-root", ".",
    "--stamp", $DataStamp,
    "--runtime-entry", $HeapExchangeEntryJson,
    "--runtime-state", $HeapExchangeRuntimeState,
    "--runtime-exit", $HeapExchangeExitJson,
    "--observer-dir", $HeapExchangeObserverDir,
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
""".strip("\n")


def line_has_label(line: str, label: str) -> bool:
    return label in line


def brace_delta(line: str) -> int:
    # Good enough for this launcher: labels live on Invoke-Checked scriptblock lines,
    # and inner braces are PowerShell control blocks that should be balanced.
    return line.count("{") - line.count("}")


def find_invoke_checked_block_end(lines: list[str], label: str) -> int | None:
    start: int | None = None
    for index, line in enumerate(lines):
        if line_has_label(line, label):
            start = index
            break
    if start is None:
        return None

    depth = 0
    seen_open = False
    for index in range(start, len(lines)):
        depth += brace_delta(lines[index])
        if "{" in lines[index]:
            seen_open = True
        if seen_open and depth <= 0:
            return index
    return None


def insert_after_invoke_checked_label(
    text: str, label: str, block: str, marker: str
) -> tuple[str, bool]:
    if marker in text:
        return text, False
    lines = text.splitlines()
    end = find_invoke_checked_block_end(lines, label)
    if end is None:
        raise RuntimeError(f"Invoke-Checked anchor not found or unterminated: {label}")
    new_lines = lines[: end + 1] + ["", *block.splitlines(), ""] + lines[end + 1 :]
    return "\n".join(new_lines) + "\n", True


def insert_before_anchor(
    text: str, anchor_terms: list[str], block: str, marker: str
) -> tuple[str, bool]:
    if marker in text:
        return text, False
    lines = text.splitlines()
    anchor_index: int | None = None
    for index, line in enumerate(lines):
        if any(term in line for term in anchor_terms):
            anchor_index = index
            break
    if anchor_index is None:
        diagnostics = [
            f"{idx + 1}: {line}"
            for idx, line in enumerate(lines)
            if any(
                word in line.lower()
                for word in (
                    "product",
                    "separation",
                    "patch_suggestion",
                    "chain",
                    "review pr",
                )
            )
        ]
        raise RuntimeError(
            "could not locate insertion anchor. Diagnostics:\n" + "\n".join(diagnostics[:80])
        )
    new_lines = lines[:anchor_index] + ["", *block.splitlines(), ""] + lines[anchor_index:]
    return "\n".join(new_lines) + "\n", True


def insert_entry(text_lf: str) -> tuple[str, bool]:
    if ENTRY_MARKER in text_lf:
        return text_lf, False
    try:
        return insert_after_invoke_checked_label(
            text_lf,
            "Build AI workload quality routing report",
            entry_block(),
            ENTRY_MARKER,
        )
    except RuntimeError:
        return insert_before_anchor(
            text_lf,
            [
                "Run official local AI pipeline adapter",
                "Run Ollama advisory packet",
                "IA-CARMINE-STRICT-REAL-RUN-ACTIVATION-END",
            ],
            entry_block(),
            ENTRY_MARKER,
        )


def insert_exit(text_lf: str) -> tuple[str, bool]:
    if EXIT_MARKER in text_lf:
        return text_lf, False
    try:
        return insert_after_invoke_checked_label(
            text_lf,
            "Apply generated patch specs for review PR",
            exit_block(),
            EXIT_MARKER,
        )
    except RuntimeError:
        return insert_before_anchor(
            text_lf,
            [
                "Validate unified heap/exchange chain contract",
                "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN",
            ],
            exit_block(),
            EXIT_MARKER,
        )


def patch_launcher(text_lf: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    text_lf, changed = insert_entry(text_lf)
    if changed:
        changes.append("insert_heap_exchange_runtime_entry")
    text_lf, changed = insert_exit(text_lf)
    if changed:
        changes.append("insert_heap_exchange_runtime_exit")
    text_lf, changed = insert_before_anchor(
        text_lf,
        [
            "Validate unified heap/exchange chain contract",
            "IA-CARMINE-UNIFIED-CHAIN-CONTRACT-GATE-BEGIN",
        ],
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
        "Tools/ai/heap_exchange/runtime_entry/cli.py",
        "Tools/ai/heap_exchange/runtime_exit/cli.py",
        "Tools/validation/heap_exchange/runtime_lifecycle_check/cli.py",
    ):
        if token not in text_lf:
            errors.append(f"missing required lifecycle token: {token}")

    entry_pos = text_lf.find("Build heap/exchange runtime entry")
    official_pos = text_lf.find("Run official local AI pipeline adapter")
    exit_pos = text_lf.find("Build heap/exchange runtime exit product")
    chain_pos = text_lf.find("Validate unified heap/exchange chain contract")
    lifecycle_pos = text_lf.find("Validate heap/exchange runtime lifecycle")

    if entry_pos < 0 or exit_pos < 0 or lifecycle_pos < 0:
        errors.append("one or more lifecycle phase labels are missing after patch")
    if official_pos >= 0 and entry_pos > official_pos:
        errors.append("heap/exchange entry must be before official/provider dynamic center")
    if chain_pos >= 0 and exit_pos > chain_pos:
        errors.append("heap/exchange exit must be before unified chain contract")
    if chain_pos >= 0 and lifecycle_pos > chain_pos:
        errors.append("heap/exchange lifecycle gate must be before unified chain contract")
    if re.search(r"^\s*throw\s*$", text_lf, flags=re.MULTILINE):
        errors.append("naked throw remains in launcher")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument("--target", default="Tools/workflow/_powershell/run_unified_local_ai_refactor.ps1")
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
