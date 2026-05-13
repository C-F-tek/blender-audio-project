#!/usr/bin/env python3
"""Conservative non-destructive patcher for unified launcher error policy.

Scope:
- validate PowerShell parser before patching;
- remove legacy duplicate UNIFIED-LAUNCHER-ERROR output from the global trap;
- require centralized Write-UnifiedLauncherStructuredError;
- require no naked `throw`;
- backup before write;
- restore automatically if parser fails.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from datetime import datetime
from pathlib import Path

LEGACY_BLOCK = """    if ($null -ne $_ -and $null -ne $_.Exception) {
        [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] $($_.Exception.Message)")
        if (-not [string]::IsNullOrWhiteSpace($_.ScriptStackTrace)) {
            [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] $($_.ScriptStackTrace)")
        }
    } elseif (-not [string]::IsNullOrWhiteSpace($Script:UnifiedLauncherFailureMessage)) {
        [Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] $Script:UnifiedLauncherFailureMessage")
    }
"""


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def detect_newline(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def normalize_lf(text: str) -> str:
    return text.replace("\r\n", "\n").replace("\r", "\n")


def write_preserved(path: Path, text_lf: str, newline: str) -> None:
    path.write_text(
        text_lf.rstrip("\n").replace("\n", newline) + newline, encoding="utf-8-sig"
    )


def run_parser(path: Path) -> tuple[bool, str]:
    ps_path = str(path).replace("'", "''")
    command = (
        "$tokens=$null;"
        "$errors=$null;"
        f"$null=[System.Management.Automation.Language.Parser]::ParseFile('{ps_path}',[ref]$tokens,[ref]$errors);"
        "if($errors.Count -gt 0){"
        "$errors | ForEach-Object { Write-Error $_.Message };"
        "exit 1"
        "}else{exit 0}"
    )
    result = subprocess.run(
        ["powershell.exe", "-NoProfile", "-Command", command],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0, result.stdout + result.stderr


def find_global_trap(text_lf: str) -> str:
    marker = "trap {\n"
    count = text_lf.count(marker)
    if count != 1:
        raise RuntimeError(f"expected exactly one global trap block, found {count}")

    start = text_lf.index(marker)
    next_marker = "\n\n$ContextFiles = @()"
    end_marker_index = text_lf.find(next_marker, start)
    if end_marker_index == -1:
        raise RuntimeError(
            "could not locate global trap end before $ContextFiles section"
        )

    return text_lf[start:end_marker_index]


def validate_policy(text_lf: str) -> list[str]:
    errors: list[str] = []

    naked_throw_lines = [
        (idx + 1, line)
        for idx, line in enumerate(text_lf.splitlines())
        if re.match(r"^\s*throw\s*$", line)
    ]
    if naked_throw_lines:
        errors.append(f"naked throw lines remain: {naked_throw_lines}")

    required_tokens = [
        "$Script:UnifiedLauncherCurrentPhase",
        "function Get-UnifiedLauncherErrorAction",
        "function Write-UnifiedLauncherStructuredError",
        "[UNIFIED-LAUNCHER-ERROR] Phase:",
        "[UNIFIED-LAUNCHER-ERROR] Message:",
        "[UNIFIED-LAUNCHER-ERROR] Location:",
        "[UNIFIED-LAUNCHER-ERROR] Action:",
        "[PYTHON-GATE] RepoPy accepted and exported to IA_CARMINE_PYTHON.",
    ]

    for token in required_tokens:
        if token not in text_lf:
            errors.append(f"missing required token: {token}")

    trap = find_global_trap(text_lf)
    if "Write-UnifiedLauncherStructuredError -ErrorRecord $_" not in trap:
        errors.append("global trap does not call Write-UnifiedLauncherStructuredError")
    if "exit 2" not in trap:
        errors.append("global trap does not exit 2")
    if (
        '[Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] $($_.Exception.Message)")'
        in trap
    ):
        errors.append(
            "legacy duplicate exception message output remains in global trap"
        )
    if (
        '[Console]::Error.WriteLine("[UNIFIED-LAUNCHER-ERROR] $Script:UnifiedLauncherFailureMessage")'
        in trap
    ):
        errors.append("legacy duplicate failure message output remains in global trap")

    return errors


def patch(text_lf: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    trap_before = find_global_trap(text_lf)

    legacy_lf = normalize_lf(LEGACY_BLOCK)
    if legacy_lf in trap_before:
        text_lf = text_lf.replace(legacy_lf, "", 1)
        changes.append("remove_legacy_duplicate_trap_output")

    trap_after = find_global_trap(text_lf)
    if "Write-UnifiedLauncherStructuredError -ErrorRecord $_" not in trap_after:
        raise RuntimeError("structured error call missing after patch")
    if "exit 2" not in trap_after:
        raise RuntimeError("exit 2 missing after patch")

    return text_lf, changes


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".")
    parser.add_argument(
        "--target", default="Tools/workflow/run_unified_local_ai_refactor.ps1"
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    repo = Path(args.repo_root).resolve()
    target = (repo / args.target).resolve()
    backup_dir = repo / "output" / "validation" / "launcher_error_policy_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    parser_ok, parser_output = run_parser(target)
    if not parser_ok:
        print("PRE_PATCH_POWERSHELL_PARSE_FAILED")
        print(parser_output)
        return 2

    original = read_text(target)
    newline = detect_newline(original)
    original_lf = normalize_lf(original)

    patched_lf, changes = patch(original_lf)
    errors = validate_policy(patched_lf)
    if errors:
        print("POLICY_VALIDATION_FAILED")
        for error in errors:
            print(f"- {error}")
        return 3

    if patched_lf == original_lf:
        print("NO_CHANGES_NEEDED")
        print("policy=valid")
        print(f"line_count={len(original_lf.splitlines())}")
        return 0

    backup = (
        backup_dir / f"{target.name}.{datetime.now().strftime('%Y%m%d-%H%M%S')}.bak"
    )
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
